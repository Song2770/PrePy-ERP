import { defineStore } from 'pinia';
import { computed, ref } from 'vue';
import { login, register, fetchCurrentUser, refreshToken } from '@/api/auth';

export const useUserStore = defineStore('user', () => {
  // State
  const user = ref(null);
  const token = ref(null);
  const refreshTokenValue = ref(null);
  
  // Getters
  const isLoggedIn = computed(() => !!token.value);
  const isAdmin = computed(() => user.value?.role === 'admin');
  const userRole = computed(() => user.value?.role);
  
  // Actions
  function setUser(userData) {
    user.value = userData;
  }
  
  function setToken(tokenValue, refreshTokenVal = null) {
    token.value = tokenValue;
    if (refreshTokenVal) {
      refreshTokenValue.value = refreshTokenVal;
    }
    
    // Save to localStorage
    localStorage.setItem('token', tokenValue);
    if (refreshTokenVal) {
      localStorage.setItem('refreshToken', refreshTokenVal);
    }
  }
  
  function clearUser() {
    user.value = null;
    token.value = null;
    refreshTokenValue.value = null;
    
    // Clear from localStorage
    localStorage.removeItem('token');
    localStorage.removeItem('refreshToken');
  }
  
  async function loginUser(credentials) {
    try {
      const response = await login(credentials);
      setToken(response.access_token, response.refresh_token);
      await fetchUserData();
      return true;
    } catch (error) {
      console.error('Login error:', error);
      return false;
    }
  }
  
  async function registerUser(userData) {
    try {
      const response = await register(userData);
      return response;
    } catch (error) {
      console.error('Registration error:', error);
      throw error;
    }
  }
  
  async function logoutUser() {
    clearUser();
  }
  
  async function fetchUserData() {
    try {
      const userData = await fetchCurrentUser();
      setUser(userData);
      return userData;
    } catch (error) {
      console.error('Error fetching user data:', error);
      if (error.response && error.response.status === 401) {
        // Try to refresh token
        await refreshUserToken();
      }
      return null;
    }
  }
  
  async function refreshUserToken() {
    if (!refreshTokenValue.value) {
      clearUser();
      return false;
    }
    
    try {
      const response = await refreshToken(refreshTokenValue.value);
      setToken(response.access_token);
      return true;
    } catch (error) {
      console.error('Token refresh error:', error);
      clearUser();
      return false;
    }
  }
  
  function initializeFromStorage() {
    const storedToken = localStorage.getItem('token');
    const storedRefreshToken = localStorage.getItem('refreshToken');
    
    if (storedToken) {
      setToken(storedToken, storedRefreshToken);
      fetchUserData();
    }
  }
  
  return {
    // State
    user,
    token,
    refreshTokenValue,
    
    // Getters
    isLoggedIn,
    isAdmin,
    userRole,
    
    // Actions
    setUser,
    setToken,
    clearUser,
    loginUser,
    registerUser,
    logoutUser,
    fetchUserData,
    refreshUserToken,
    initializeFromStorage,
  };
}); 