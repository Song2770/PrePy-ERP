import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import { ElMessage } from 'element-plus'
import api from '@/utils/api'

export const useUserStore = defineStore('user', () => {
  // 状态
  const token = ref(localStorage.getItem('token') || '')
  const userInfo = ref((() => {
    try {
      const stored = localStorage.getItem('userInfo')
      return stored ? JSON.parse(stored) : null
    } catch (error) {
      console.warn('Failed to parse userInfo from localStorage:', error)
      localStorage.removeItem('userInfo')
      return null
    }
  })())
  const loading = ref(false)

  // 计算属性
  const isAuthenticated = computed(() => {
    return !!token.value && !!userInfo.value
  })

  const userName = computed(() => {
    return userInfo.value?.full_name || userInfo.value?.username || '未知用户'
  })

  const userRole = computed(() => {
    return userInfo.value?.is_superuser ? '超级管理员' : '普通用户'
  })

  // 方法
  const login = async (credentials) => {
    try {
      loading.value = true
      console.log('正在登录...', credentials.username)
      
      const response = await api.post('/auth/login', credentials)
      const { access_token, user_info } = response.data
      
      // 保存token和用户信息
      token.value = access_token
      userInfo.value = user_info
      
      // 持久化存储
      localStorage.setItem('token', access_token)
      localStorage.setItem('userInfo', JSON.stringify(user_info))
      
      console.log('登录成功:', user_info.username)
      ElMessage.success('登录成功')
      
      return { success: true }
    } catch (error) {
      console.error('登录失败:', error)
      const message = error.response?.data?.detail || '登录失败，请检查用户名和密码'
      ElMessage.error(message)
      return { success: false, message }
    } finally {
      loading.value = false
    }
  }

  const logout = async () => {
    try {
      console.log('正在退出登录...')
      
      // 调用后端登出接口
      if (token.value) {
        await api.post('/auth/logout')
      }
    } catch (error) {
      console.error('退出登录请求失败:', error)
    } finally {
      // 清除本地状态
      token.value = ''
      userInfo.value = null
      
      // 清除持久化存储
      localStorage.removeItem('token')
      localStorage.removeItem('userInfo')
      
      console.log('已退出登录')
      ElMessage.success('已退出登录')
    }
  }

  const checkAuth = async () => {
    if (!token.value) {
      return false
    }

    try {
      console.log('检查用户认证状态...')
      const response = await api.get('/auth/me')
      userInfo.value = response.data
      
      // 更新本地存储的用户信息
      localStorage.setItem('userInfo', JSON.stringify(response.data))
      
      console.log('用户认证有效:', response.data.username)
      return true
    } catch (error) {
      console.error('用户认证失效:', error)
      
      // 认证失效，清除本地状态
      token.value = ''
      userInfo.value = null
      localStorage.removeItem('token')
      localStorage.removeItem('userInfo')
      
      return false
    }
  }

  const updateUserInfo = (newUserInfo) => {
    userInfo.value = { ...userInfo.value, ...newUserInfo }
    localStorage.setItem('userInfo', JSON.stringify(userInfo.value))
    console.log('用户信息已更新')
  }

  const refreshToken = async () => {
    try {
      console.log('刷新用户token...')
      const response = await api.post('/auth/refresh')
      const { access_token } = response.data
      
      token.value = access_token
      localStorage.setItem('token', access_token)
      
      console.log('Token刷新成功')
      return true
    } catch (error) {
      console.error('Token刷新失败:', error)
      await logout()
      return false
    }
  }

  return {
    // 状态
    token,
    userInfo,
    loading,
    
    // 计算属性
    isAuthenticated,
    userName,
    userRole,
    
    // 方法
    login,
    logout,
    checkAuth,
    updateUserInfo,
    refreshToken
  }
})