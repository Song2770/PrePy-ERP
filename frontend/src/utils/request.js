import axios from 'axios';
import { ElMessage } from 'element-plus';
import router from '@/router';

// 创建axios实例
const service = axios.create({
  baseURL: '/api',
  timeout: 15000
});

// 请求拦截器
service.interceptors.request.use(
  config => {
    // 从localStorage获取token
    const token = localStorage.getItem('token');
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`;
    }
    return config;
  },
  error => {
    console.error('请求错误:', error);
    return Promise.reject(error);
  }
);

// 响应拦截器
service.interceptors.response.use(
  response => {
    const res = response.data;
    
    // FastAPI通常直接返回数据，不包装在code字段中
    // 检查是否有明显的错误字段
    if (res.error || res.detail) {
      ElMessage.error(res.error || res.detail || '请求失败');
      return Promise.reject(new Error(res.error || res.detail || '请求失败'));
    }
    
    return res;
  },
  error => {
    console.error('响应错误:', error);
    
    // 处理HTTP错误
    if (error.response) {
      const responseData = error.response.data;
      const errorMessage = responseData.detail || responseData.message || '请求失败';
      
      switch (error.response.status) {
        case 401:
          // 未授权，清除token并跳转到登录页
          localStorage.removeItem('token');
          router.push('/login');
          ElMessage.error('登录已过期，请重新登录');
          break;
        case 403:
          ElMessage.error('没有权限访问');
          break;
        case 404:
          ElMessage.error('请求的资源不存在');
          break;
        case 422:
          // 处理验证错误
          if (responseData.detail && Array.isArray(responseData.detail)) {
            const validationErrors = responseData.detail.map(err => `${err.loc[1]}: ${err.msg}`).join('; ');
            ElMessage.error(validationErrors);
          } else {
            ElMessage.error(errorMessage);
          }
          break;
        case 500:
          ElMessage.error('服务器错误');
          break;
        default:
          ElMessage.error(errorMessage);
      }
    } else {
      ElMessage.error('网络错误，请检查网络连接');
    }
    
    return Promise.reject(error);
  }
);

export default service; 