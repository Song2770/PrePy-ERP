import { defineStore } from 'pinia';
import { computed, ref } from 'vue';
import { login, register, fetchCurrentUser } from '@/api/auth';

export const useUserStore = defineStore('user', () => {
  // State
  const user = ref(null);
  
  // Getters
  const isLoggedIn = computed(() => {
    return !!localStorage.getItem('token');
  });
  const isAdmin = computed(() => user.value?.role === 'admin');
  const userRole = computed(() => user.value?.role);
  
  // Actions
  function setUser(userData) {
    user.value = userData;
  }
  
  function clearUser() {
    user.value = null;
    localStorage.removeItem('token');
    localStorage.removeItem('refreshToken');
  }
  
  async function loginUser(credentials) {
    try {
      const response = await login(credentials);
      if (response && response.access_token) {
        // 登录成功后获取用户数据
        await loadUserData();
        return true;
      }
      return false;
    } catch (error) {
      console.error('登录错误:', error);
      return false;
    }
  }
  
  async function registerUser(userData) {
    try {
      const response = await register(userData);
      return response;
    } catch (error) {
      console.error('注册错误:', error);
      throw error;
    }
  }
  
  async function logoutUser() {
    clearUser();
  }
  
  async function loadUserData() {
    try {
      if (!localStorage.getItem('token')) {
        return null;
      }
      
      const userData = await fetchCurrentUser();
      setUser(userData);
      return userData;
    } catch (error) {
      console.error('获取用户数据错误:', error);
      // 如果获取用户数据失败，清除用户状态
      if (error.response && error.response.status === 401) {
        clearUser();
      }
      return null;
    }
  }
  
  function initializeApp() {
    // 只在有token的情况下尝试加载用户数据
    if (localStorage.getItem('token')) {
      loadUserData().catch(() => {
        // 如果加载失败，静默处理
      });
    }
  }
  
  return {
    // State
    user,
    
    // Getters
    isLoggedIn,
    isAdmin,
    userRole,
    
    // Actions
    setUser,
    clearUser,
    loginUser,
    registerUser,
    logoutUser,
    loadUserData,
    initializeApp
  };
}); 