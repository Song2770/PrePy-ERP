import request from '@/utils/request';

/**
 * 搜索客户
 * @param {Object} params - 搜索参数
 * @param {string} params.query - 搜索关键词
 * @returns {Promise<Array>} - 返回客户列表
 */
export function searchCustomers(params) {
  return request({
    url: '/sales/customers/search',
    method: 'get',
    params: {
      keyword: params.query,
      page: 1,
      size: 10
    }
  });
}

/**
 * 获取客户详情
 * @param {number} id - 客户ID
 * @returns {Promise} - 返回Promise对象
 */
export function getCustomer(id) {
  return request({
    url: `/sales/customers/${id}`,
    method: 'get'
  });
}

/**
 * 创建客户
 * @param {Object} data - 客户数据
 * @returns {Promise} - 返回Promise对象
 */
export function createCustomer(data) {
  return request({
    url: '/sales/customers',
    method: 'post',
    data
  });
}

/**
 * 更新客户
 * @param {number} id - 客户ID
 * @param {Object} data - 更新的客户数据
 * @returns {Promise} - 返回Promise对象
 */
export function updateCustomer(id, data) {
  return request({
    url: `/sales/customers/${id}`,
    method: 'put',
    data
  });
}

/**
 * 删除客户
 * @param {number} id - 客户ID
 * @returns {Promise} - 返回Promise对象
 */
export function deleteCustomer(id) {
  return request({
    url: `/sales/customers/${id}`,
    method: 'delete'
  });
} 