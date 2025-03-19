import axios from 'axios';

// 创建axios实例
const apiClient = axios.create({
  baseURL: '/api/v1',
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
  },
});

// 添加请求拦截器
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

/**
 * 登录用户
 * @param {Object} credentials - 用户凭证
 * @returns {Promise} - API响应
 */
export const login = async (credentials) => {
  const formData = new FormData();
  formData.append('username', credentials.username);
  formData.append('password', credentials.password);
  
  const response = await axios.post('/api/v1/auth/login', formData, {
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
    },
  });
  
  // 直接存储token到localStorage
  if (response.data && response.data.access_token) {
    localStorage.setItem('token', response.data.access_token);
    if (response.data.refresh_token) {
      localStorage.setItem('refreshToken', response.data.refresh_token);
    }
  }
  
  return response.data;
};

/**
 * 注册新用户
 * @param {Object} userData - 用户数据
 * @returns {Promise} - API响应
 */
export const register = async (userData) => {
  const response = await apiClient.post('/auth/register', userData);
  return response.data;
};

/**
 * 获取当前用户数据
 * @returns {Promise} - API响应
 */
export const fetchCurrentUser = async () => {
  const token = localStorage.getItem('token');
  if (!token) {
    throw new Error('No token found');
  }
  
  try {
    const response = await apiClient.get('/auth/me');
    return response.data;
  } catch (error) {
    if (error.response && error.response.status === 401) {
      // 清除无效的token
      localStorage.removeItem('token');
      localStorage.removeItem('refreshToken');
    }
    throw error;
  }
};

export default apiClient;