import request from '@/utils/request';

/**
 * 获取销售交付列表
 * @param {Object} params - 查询参数（分页、过滤等）
 * @returns {Promise} - 返回Promise对象
 */
export function getDeliveries(params) {
  return request({
    url: '/api/sales/deliveries',
    method: 'get',
    params
  });
}

/**
 * 获取单个销售交付详情
 * @param {Number} id - 交付ID
 * @returns {Promise} - 返回Promise对象
 */
export function getDelivery(id) {
  return request({
    url: `/api/sales/deliveries/${id}`,
    method: 'get'
  });
}

/**
 * 创建新销售交付
 * @param {Object} deliveryData - 交付数据
 * @returns {Promise} - 返回Promise对象
 */
export function createDelivery(deliveryData) {
  return request({
    url: '/api/sales/deliveries',
    method: 'post',
    data: deliveryData
  });
}

/**
 * 更新销售交付
 * @param {Number} id - 交付ID
 * @param {Object} deliveryData - 更新的交付数据
 * @returns {Promise} - 返回Promise对象
 */
export function updateDelivery(id, deliveryData) {
  return request({
    url: `/api/sales/deliveries/${id}`,
    method: 'put',
    data: deliveryData
  });
}

/**
 * 删除销售交付
 * @param {Number} id - 交付ID
 * @returns {Promise} - 返回Promise对象
 */
export function deleteDelivery(id) {
  return request({
    url: `/api/sales/deliveries/${id}`,
    method: 'delete'
  });
}

/**
 * 更新交付状态
 * @param {Number} id - 交付ID
 * @param {String} status - 新状态
 * @returns {Promise} - 返回Promise对象
 */
export function updateDeliveryStatus(id, status) {
  return request({
    url: `/api/sales/deliveries/${id}/status`,
    method: 'put',
    data: { status }
  });
}

/**
 * 从销售订单创建交付
 * @param {Number} orderId - 订单ID
 * @param {Object} deliveryData - 交付数据
 * @returns {Promise} - 返回Promise对象
 */
export function createDeliveryFromOrder(orderId, deliveryData) {
  return request({
    url: `/api/sales/orders/${orderId}/delivery`,
    method: 'post',
    data: deliveryData
  });
}

/**
 * 获取交付项列表
 * @param {Number} deliveryId - 交付ID
 * @returns {Promise} - 返回Promise对象
 */
export function getDeliveryItems(deliveryId) {
  return request({
    url: `/api/sales/deliveries/${deliveryId}/items`,
    method: 'get'
  });
}

/**
 * 添加交付项
 * @param {Number} deliveryId - 交付ID
 * @param {Object} itemData - 交付项数据
 * @returns {Promise} - 返回Promise对象
 */
export function addDeliveryItem(deliveryId, itemData) {
  return request({
    url: `/api/sales/deliveries/${deliveryId}/items`,
    method: 'post',
    data: itemData
  });
}

/**
 * 更新交付项
 * @param {Number} deliveryId - 交付ID
 * @param {Number} itemId - 交付项ID
 * @param {Object} itemData - 更新的交付项数据
 * @returns {Promise} - 返回Promise对象
 */
export function updateDeliveryItem(deliveryId, itemId, itemData) {
  return request({
    url: `/api/sales/deliveries/${deliveryId}/items/${itemId}`,
    method: 'put',
    data: itemData
  });
}

/**
 * 删除交付项
 * @param {Number} deliveryId - 交付ID
 * @param {Number} itemId - 交付项ID
 * @returns {Promise} - 返回Promise对象
 */
export function deleteDeliveryItem(deliveryId, itemId) {
  return request({
    url: `/api/sales/deliveries/${deliveryId}/items/${itemId}`,
    method: 'delete'
  });
}

/**
 * 确认交付完成
 * @param {Number} deliveryId - 交付ID
 * @param {Object} confirmData - 确认数据（如签收人信息等）
 * @returns {Promise} - 返回Promise对象
 */
export function confirmDelivery(deliveryId, confirmData) {
  return request({
    url: `/api/sales/deliveries/${deliveryId}/confirm`,
    method: 'post',
    data: confirmData
  });
}

/**
 * 标记交付为已发运
 * @param {Number} deliveryId - 交付ID
 * @param {Object} shippingData - 发运数据（如物流信息等）
 * @returns {Promise} - 返回Promise对象
 */
export function markAsShipped(deliveryId, shippingData) {
  return request({
    url: `/api/sales/deliveries/${deliveryId}/ship`,
    method: 'post',
    data: shippingData
  });
}

/**
 * 记录交付退回
 * @param {Number} deliveryId - 交付ID
 * @param {Object} returnData - 退回数据
 * @returns {Promise} - 返回Promise对象
 */
export function recordDeliveryReturn(deliveryId, returnData) {
  return request({
    url: `/api/sales/deliveries/${deliveryId}/return`,
    method: 'post',
    data: returnData
  });
}

/**
 * 获取交付跟踪信息
 * @param {Number} deliveryId - 交付ID
 * @returns {Promise} - 返回Promise对象
 */
export function getDeliveryTracking(deliveryId) {
  return request({
    url: `/api/sales/deliveries/${deliveryId}/tracking`,
    method: 'get'
  });
}

/**
 * 更新交付跟踪信息
 * @param {Number} deliveryId - 交付ID
 * @param {Object} trackingData - 跟踪数据
 * @returns {Promise} - 返回Promise对象
 */
export function updateDeliveryTracking(deliveryId, trackingData) {
  return request({
    url: `/api/sales/deliveries/${deliveryId}/tracking`,
    method: 'put',
    data: trackingData
  });
}

/**
 * 导出交付单为PDF
 * @param {Number} id - 交付ID
 * @returns {Promise} - 返回Promise对象
 */
export function exportDeliveryPdf(id) {
  return request({
    url: `/api/sales/deliveries/${id}/export`,
    method: 'get',
    responseType: 'blob'
  });
}

/**
 * 获取交付统计数据
 * @param {Object} params - 查询参数
 * @returns {Promise} - 返回Promise对象
 */
export function getDeliveryStatistics(params) {
  return request({
    url: '/api/sales/deliveries/statistics',
    method: 'get',
    params
  });
}

/**
 * 获取物流公司列表
 * @returns {Promise} - 返回Promise对象
 */
export function getLogisticsCompanies() {
  return request({
    url: '/api/sales/logistics-companies',
    method: 'get'
  });
}

/**
 * 打印交付单
 * @param {Number} id - 交付ID
 * @param {Object} options - 打印选项
 * @returns {Promise} - 返回Promise对象
 */
export function printDeliveryNote(id, options = {}) {
  return request({
    url: `/api/sales/deliveries/${id}/print`,
    method: 'post',
    data: options,
    responseType: 'blob'
  });
}

/**
 * 获取可发货的订单项
 * @param {Number} orderId - 订单ID
 * @returns {Promise} - 返回Promise对象
 */
export function getDeliverableItems(orderId) {
  return request({
    url: `/api/sales/orders/${orderId}/deliverable-items`,
    method: 'get'
  });
}

/**
 * 交付API钩子函数
 * @returns {Object} - 返回所有交付相关API方法的对象
 */
export function useDeliveryApi() {
  return {
    getDeliveries,
    getDelivery,
    createDelivery,
    updateDelivery,
    deleteDelivery,
    updateDeliveryStatus,
    createDeliveryFromOrder,
    getDeliveryItems,
    addDeliveryItem,
    updateDeliveryItem,
    deleteDeliveryItem,
    confirmDelivery,
    markAsShipped,
    recordDeliveryReturn,
    getDeliveryTracking,
    updateDeliveryTracking,
    exportDeliveryPdf,
    getDeliveryStatistics,
    getLogisticsCompanies,
    printDeliveryNote,
    getDeliverableItems
  };
} 