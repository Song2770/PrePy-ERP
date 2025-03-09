import axios from 'axios';
import { useUserStore } from '@/stores/user';

// Create axios instance
const apiClient = axios.create({
  baseURL: '/api/v1',
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
  },
});

// Add request interceptor to add auth token
apiClient.interceptors.request.use(
  (config) => {
    const userStore = useUserStore();
    if (userStore.token) {
      config.headers.Authorization = `Bearer ${userStore.token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Add response interceptor to handle token refresh
apiClient.interceptors.response.use(
  (response) => {
    return response;
  },
  async (error) => {
    const originalRequest = error.config;
    
    // If error is 401 and not already retried
    if (error.response.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      
      try {
        const userStore = useUserStore();
        const refreshed = await userStore.refreshUserToken();
        
        if (refreshed) {
          // Retry the request with new token
          originalRequest.headers.Authorization = `Bearer ${userStore.token}`;
          return apiClient(originalRequest);
        }
      } catch (refreshError) {
        console.error('Error refreshing token:', refreshError);
      }
    }
    
    return Promise.reject(error);
  }
);

/**
 * Login user
 * @param {Object} credentials - User credentials
 * @returns {Promise} - API response
 */
export const login = async (credentials) => {
  const formData = new FormData();
  formData.append('username', credentials.username);
  formData.append('password', credentials.password);
  
  const response = await apiClient.post('/auth/login', formData, {
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
    },
  });
  
  return response.data;
};

/**
 * Register new user
 * @param {Object} userData - User data
 * @returns {Promise} - API response
 */
export const register = async (userData) => {
  const response = await apiClient.post('/auth/register', userData);
  return response.data;
};

/**
 * Refresh access token
 * @param {string} refreshToken - Refresh token
 * @returns {Promise} - API response
 */
export const refreshToken = async (refreshToken) => {
  const response = await apiClient.post('/auth/refresh', { refresh_token: refreshToken });
  return response.data;
};

/**
 * Fetch current user data
 * @returns {Promise} - API response
 */
export const fetchCurrentUser = async () => {
  const response = await apiClient.get('/auth/me');
  return response.data;
};

export default apiClient; 