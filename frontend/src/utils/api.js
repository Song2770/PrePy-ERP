import axios from 'axios'
import { ElMessage, ElMessageBox } from 'element-plus'
import { useUserStore } from '@/stores/user'
import router from '@/router'

console.log('正在初始化API工具...')

// 创建axios实例
const api = axios.create({
  baseURL: '/api',
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// 请求拦截器
api.interceptors.request.use(
  (config) => {
    const userStore = useUserStore()
    
    // 添加认证token
    if (userStore.token) {
      config.headers.Authorization = `Bearer ${userStore.token}`
    }
    
    console.log(`发送API请求: ${config.method?.toUpperCase()} ${config.url}`)
    return config
  },
  (error) => {
    console.error('请求拦截器错误:', error)
    return Promise.reject(error)
  }
)

// 响应拦截器
api.interceptors.response.use(
  (response) => {
    console.log(`API响应成功: ${response.config.method?.toUpperCase()} ${response.config.url}`)
    return response
  },
  async (error) => {
    const userStore = useUserStore()
    const { response } = error
    
    console.error(`API响应错误: ${error.config?.method?.toUpperCase()} ${error.config?.url}`, error)
    
    if (response) {
      const { status, data } = response
      
      switch (status) {
        case 401:
          // 未授权，清除用户信息并跳转到登录页
          console.log('用户认证失效，跳转到登录页')
          await userStore.logout()
          router.push({ name: 'Login' })
          ElMessage.error('登录已过期，请重新登录')
          break
          
        case 403:
          // 禁止访问
          ElMessage.error('没有权限访问该资源')
          break
          
        case 404:
          // 资源未找到
          ElMessage.error('请求的资源不存在')
          break
          
        case 422:
          // 数据验证错误
          const message = data?.detail || '数据验证失败'
          if (Array.isArray(data?.detail)) {
            const errors = data.detail.map(err => `${err.loc?.join('.')} ${err.msg}`).join(', ')
            ElMessage.error(`数据验证错误: ${errors}`)
          } else {
            ElMessage.error(message)
          }
          break
          
        case 500:
          // 服务器内部错误
          ElMessage.error('服务器内部错误，请稍后重试')
          break
          
        default:
          // 其他错误
          const errorMessage = data?.detail || data?.message || `请求失败 (${status})`
          ElMessage.error(errorMessage)
      }
    } else if (error.code === 'ECONNABORTED') {
      // 请求超时
      ElMessage.error('请求超时，请检查网络连接')
    } else if (error.message === 'Network Error') {
      // 网络错误
      ElMessage.error('网络连接失败，请检查网络设置')
    } else {
      // 其他错误
      ElMessage.error('请求失败，请稍后重试')
    }
    
    return Promise.reject(error)
  }
)

// 封装常用的HTTP方法
const request = {
  get: (url, config = {}) => api.get(url, config),
  post: (url, data = {}, config = {}) => api.post(url, data, config),
  put: (url, data = {}, config = {}) => api.put(url, data, config),
  patch: (url, data = {}, config = {}) => api.patch(url, data, config),
  delete: (url, config = {}) => api.delete(url, config)
}

// 文件上传方法
const uploadFile = (url, file, onProgress = null) => {
  const formData = new FormData()
  formData.append('file', file)
  
  return api.post(url, formData, {
    headers: {
      'Content-Type': 'multipart/form-data'
    },
    onUploadProgress: (progressEvent) => {
      if (onProgress && progressEvent.total) {
        const progress = Math.round((progressEvent.loaded * 100) / progressEvent.total)
        onProgress(progress)
      }
    }
  })
}

// 下载文件方法
const downloadFile = async (url, filename = null) => {
  try {
    const response = await api.get(url, {
      responseType: 'blob'
    })
    
    const blob = new Blob([response.data])
    const downloadUrl = window.URL.createObjectURL(blob)
    const link = document.createElement('a')
    
    link.href = downloadUrl
    link.download = filename || 'download'
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    
    window.URL.revokeObjectURL(downloadUrl)
    
    ElMessage.success('文件下载成功')
  } catch (error) {
    console.error('文件下载失败:', error)
    ElMessage.error('文件下载失败')
  }
}

// 批量请求方法
const batchRequest = async (requests) => {
  try {
    const responses = await Promise.allSettled(requests)
    return responses.map((response, index) => {
      if (response.status === 'fulfilled') {
        return { success: true, data: response.value.data, index }
      } else {
        console.error(`批量请求第${index + 1}个失败:`, response.reason)
        return { success: false, error: response.reason, index }
      }
    })
  } catch (error) {
    console.error('批量请求失败:', error)
    throw error
  }
}

// 重试请求方法
const retryRequest = async (requestFn, maxRetries = 3, delay = 1000) => {
  for (let i = 0; i < maxRetries; i++) {
    try {
      return await requestFn()
    } catch (error) {
      if (i === maxRetries - 1) {
        throw error
      }
      
      console.log(`请求失败，${delay}ms后进行第${i + 2}次重试...`)
      await new Promise(resolve => setTimeout(resolve, delay))
    }
  }
}

console.log('API工具初始化完成')

// 导出API实例和工具方法
export default api
export {
  request,
  uploadFile,
  downloadFile,
  batchRequest,
  retryRequest
}