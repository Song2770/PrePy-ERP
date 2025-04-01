import request from '@/utils/request';

/**
 * 获取销售订单列表
 * @param {Object} params - 查询参数（分页、过滤等）
 * @returns {Promise} - 返回Promise对象
 */
export function getOrders(params) {
  return request({
    url: '/sales/orders',
    method: 'get',
    params
  });
}

/**
 * 获取单个销售订单详情
 * @param {Number} id - 订单ID
 * @returns {Promise} - 返回Promise对象
 */
export function getOrder(id) {
  return request({
    url: `/sales/orders/${id}`,
    method: 'get'
  });
}

/**
 * 创建新销售订单
 * @param {Object} orderData - 订单数据
 * @returns {Promise} - 返回Promise对象
 */
export function createOrder(orderData) {
  return request({
    url: '/sales/orders',
    method: 'post',
    data: orderData
  });
}

/**
 * 更新销售订单
 * @param {Number} id - 订单ID
 * @param {Object} orderData - 更新的订单数据
 * @returns {Promise} - 返回Promise对象
 */
export function updateOrder(id, orderData) {
  return request({
    url: `/sales/orders/${id}`,
    method: 'put',
    data: orderData
  });
}

/**
 * 删除销售订单
 * @param {Number} id - 订单ID
 * @returns {Promise} - 返回Promise对象
 */
export function deleteOrder(id) {
  return request({
    url: `/sales/orders/${id}`,
    method: 'delete'
  });
}

/**
 * 更新订单状态
 * @param {Number} id - 订单ID
 * @param {String} status - 新状态
 * @returns {Promise} - 返回Promise对象
 */
export function updateOrderStatus(id, status) {
  return request({
    url: `/sales/orders/${id}/status`,
    method: 'put',
    data: { status }
  });
}

/**
 * 从报价单创建订单
 * @param {Number} quotationId - 报价单ID
 * @param {Object} additionalData - 额外订单数据
 * @returns {Promise} - 返回Promise对象
 */
export function createOrderFromQuotation(quotationId, additionalData = {}) {
  return request({
    url: `/sales/quotations/${quotationId}/convert`,
    method: 'post',
    data: additionalData
  });
}

/**
 * 获取订单项列表
 * @param {Number} orderId - 订单ID
 * @returns {Promise} - 返回Promise对象
 */
export function getOrderItems(orderId) {
  return request({
    url: `/sales/orders/${orderId}/items`,
    method: 'get'
  });
}

/**
 * 添加订单项
 * @param {Number} orderId - 订单ID
 * @param {Object} itemData - 订单项数据
 * @returns {Promise} - 返回Promise对象
 */
export function addOrderItem(orderId, itemData) {
  return request({
    url: `/sales/orders/${orderId}/items`,
    method: 'post',
    data: itemData
  });
}

/**
 * 更新订单项
 * @param {Number} orderId - 订单ID
 * @param {Number} itemId - 订单项ID
 * @param {Object} itemData - 更新的订单项数据
 * @returns {Promise} - 返回Promise对象
 */
export function updateOrderItem(orderId, itemId, itemData) {
  return request({
    url: `/sales/orders/${orderId}/items/${itemId}`,
    method: 'put',
    data: itemData
  });
}

/**
 * 删除订单项
 * @param {Number} orderId - 订单ID
 * @param {Number} itemId - 订单项ID
 * @returns {Promise} - 返回Promise对象
 */
export function deleteOrderItem(orderId, itemId) {
  return request({
    url: `/sales/orders/${orderId}/items/${itemId}`,
    method: 'delete'
  });
}

/**
 * 获取订单的交付信息
 * @param {Number} orderId - 订单ID
 * @returns {Promise} - 返回Promise对象
 */
export function getOrderDeliveries(orderId) {
  return request({
    url: `/sales/orders/${orderId}/deliveries`,
    method: 'get'
  });
}

/**
 * 获取订单的发票信息
 * @param {Number} orderId - 订单ID
 * @returns {Promise} - 返回Promise对象
 */
export function getOrderInvoices(orderId) {
  return request({
    url: `/sales/orders/${orderId}/invoices`,
    method: 'get'
  });
}

/**
 * 导出订单为PDF
 * @param {Number} id - 订单ID
 * @returns {Promise} - 返回Promise对象
 */
export function exportOrderPdf(id) {
  return request({
    url: `/sales/orders/${id}/export`,
    method: 'get',
    responseType: 'blob'
  });
}

/**
 * 获取订单统计数据
 * @param {Object} params - 查询参数
 * @returns {Promise} - 返回Promise对象
 */
export function getOrderStatistics(params) {
  return request({
    url: '/sales/orders/statistics',
    method: 'get',
    params
  });
}

/**
 * 取消订单
 * @param {Number} id - 订单ID
 * @param {Object} data - 取消原因等数据
 * @returns {Promise} - 返回Promise对象
 */
export function cancelOrder(id, data) {
  return request({
    url: `/sales/orders/${id}/cancel`,
    method: 'post',
    data
  });
}

/**
 * 订单API钩子函数
 * @returns {Object} - 返回所有订单相关API方法的对象
 */
export function useOrderApi() {
  return {
    getOrders,
    getOrder,
    createOrder,
    updateOrder,
    deleteOrder,
    updateOrderStatus,
    createOrderFromQuotation,
    getOrderItems,
    addOrderItem,
    updateOrderItem,
    deleteOrderItem,
    getOrderDeliveries,
    getOrderInvoices,
    exportOrderPdf,
    getOrderStatistics,
    cancelOrder
  };
}
