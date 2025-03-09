import apiClient from './auth';

/**
 * Fetch dashboard data
 * @returns {Promise} - API response
 */
export const fetchDashboardData = async () => {
  const response = await apiClient.get('/dashboard');
  return response.data;
};

/**
 * Fetch dashboard statistics
 * @param {string} period - Time period (day, week, month, year)
 * @returns {Promise} - API response
 */
export const fetchDashboardStats = async (period = 'month') => {
  const response = await apiClient.get(`/dashboard/stats?period=${period}`);
  return response.data;
};

/**
 * Fetch recent activities
 * @param {number} limit - Number of activities to fetch
 * @returns {Promise} - API response
 */
export const fetchRecentActivities = async (limit = 10) => {
  const response = await apiClient.get(`/dashboard/activities?limit=${limit}`);
  return response.data;
};

/**
 * Fetch sales data for chart
 * @param {string} period - Time period (day, week, month, year)
 * @returns {Promise} - API response
 */
export const fetchSalesChartData = async (period = 'month') => {
  const response = await apiClient.get(`/dashboard/sales-chart?period=${period}`);
  return response.data;
};

/**
 * Fetch inventory status
 * @returns {Promise} - API response
 */
export const fetchInventoryStatus = async () => {
  const response = await apiClient.get('/dashboard/inventory-status');
  return response.data;
};

export default {
  fetchDashboardData,
  fetchDashboardStats,
  fetchRecentActivities,
  fetchSalesChartData,
  fetchInventoryStatus
}; 