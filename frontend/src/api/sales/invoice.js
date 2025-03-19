import request from '@/utils/request';

/**
 * 获取销售发票列表
 * @param {Object} params - 查询参数（分页、过滤等）
 * @returns {Promise} - 返回Promise对象
 */
export function getInvoices(params) {
  return request({
    url: '/api/sales/invoices',
    method: 'get',
    params
  });
}

/**
 * 获取单个销售发票详情
 * @param {Number} id - 发票ID
 * @returns {Promise} - 返回Promise对象
 */
export function getInvoice(id) {
  return request({
    url: `/api/sales/invoices/${id}`,
    method: 'get'
  });
}

/**
 * 创建新销售发票
 * @param {Object} invoiceData - 发票数据
 * @returns {Promise} - 返回Promise对象
 */
export function createInvoice(invoiceData) {
  return request({
    url: '/api/sales/invoices',
    method: 'post',
    data: invoiceData
  });
}

/**
 * 更新销售发票
 * @param {Number} id - 发票ID
 * @param {Object} invoiceData - 更新的发票数据
 * @returns {Promise} - 返回Promise对象
 */
export function updateInvoice(id, invoiceData) {
  return request({
    url: `/api/sales/invoices/${id}`,
    method: 'put',
    data: invoiceData
  });
}

/**
 * 删除销售发票
 * @param {Number} id - 发票ID
 * @returns {Promise} - 返回Promise对象
 */
export function deleteInvoice(id) {
  return request({
    url: `/api/sales/invoices/${id}`,
    method: 'delete'
  });
}

/**
 * 更新发票状态
 * @param {Number} id - 发票ID
 * @param {String} status - 新状态
 * @returns {Promise} - 返回Promise对象
 */
export function updateInvoiceStatus(id, status) {
  return request({
    url: `/api/sales/invoices/${id}/status`,
    method: 'put',
    data: { status }
  });
}

/**
 * 从销售订单创建发票
 * @param {Number} orderId - 订单ID
 * @param {Object} additionalData - 额外发票数据
 * @returns {Promise} - 返回Promise对象
 */
export function createInvoiceFromOrder(orderId, additionalData = {}) {
  return request({
    url: `/api/sales/orders/${orderId}/invoice`,
    method: 'post',
    data: additionalData
  });
}

/**
 * 获取发票项列表
 * @param {Number} invoiceId - 发票ID
 * @returns {Promise} - 返回Promise对象
 */
export function getInvoiceItems(invoiceId) {
  return request({
    url: `/api/sales/invoices/${invoiceId}/items`,
    method: 'get'
  });
}

/**
 * 添加发票项
 * @param {Number} invoiceId - 发票ID
 * @param {Object} itemData - 发票项数据
 * @returns {Promise} - 返回Promise对象
 */
export function addInvoiceItem(invoiceId, itemData) {
  return request({
    url: `/api/sales/invoices/${invoiceId}/items`,
    method: 'post',
    data: itemData
  });
}

/**
 * 更新发票项
 * @param {Number} invoiceId - 发票ID
 * @param {Number} itemId - 发票项ID
 * @param {Object} itemData - 更新的发票项数据
 * @returns {Promise} - 返回Promise对象
 */
export function updateInvoiceItem(invoiceId, itemId, itemData) {
  return request({
    url: `/api/sales/invoices/${invoiceId}/items/${itemId}`,
    method: 'put',
    data: itemData
  });
}

/**
 * 删除发票项
 * @param {Number} invoiceId - 发票ID
 * @param {Number} itemId - 发票项ID
 * @returns {Promise} - 返回Promise对象
 */
export function deleteInvoiceItem(invoiceId, itemId) {
  return request({
    url: `/api/sales/invoices/${invoiceId}/items/${itemId}`,
    method: 'delete'
  });
}

/**
 * 记录发票付款
 * @param {Number} invoiceId - 发票ID
 * @param {Object} paymentData - 付款数据
 * @returns {Promise} - 返回Promise对象
 */
export function recordInvoicePayment(invoiceId, paymentData) {
  return request({
    url: `/api/sales/invoices/${invoiceId}/payments`,
    method: 'post',
    data: paymentData
  });
}

/**
 * 获取发票付款记录
 * @param {Number} invoiceId - 发票ID
 * @returns {Promise} - 返回Promise对象
 */
export function getInvoicePayments(invoiceId) {
  return request({
    url: `/api/sales/invoices/${invoiceId}/payments`,
    method: 'get'
  });
}

/**
 * 发送发票给客户
 * @param {Number} invoiceId - 发票ID
 * @param {Object} emailData - 邮件数据
 * @returns {Promise} - 返回Promise对象
 */
export function sendInvoiceEmail(invoiceId, emailData) {
  return request({
    url: `/api/sales/invoices/${invoiceId}/send`,
    method: 'post',
    data: emailData
  });
}

/**
 * 导出发票为PDF
 * @param {Number} id - 发票ID
 * @returns {Promise} - 返回Promise对象
 */
export function exportInvoicePdf(id) {
  return request({
    url: `/api/sales/invoices/${id}/export`,
    method: 'get',
    responseType: 'blob'
  });
}

/**
 * 获取发票统计数据
 * @param {Object} params - 查询参数
 * @returns {Promise} - 返回Promise对象
 */
export function getInvoiceStatistics(params) {
  return request({
    url: '/api/sales/invoices/statistics',
    method: 'get',
    params
  });
}

/**
 * 取消发票
 * @param {Number} id - 发票ID
 * @param {Object} data - 取消原因等数据
 * @returns {Promise} - 返回Promise对象
 */
export function cancelInvoice(id, data) {
  return request({
    url: `/api/sales/invoices/${id}/cancel`,
    method: 'post',
    data
  });
}

/**
 * 标记发票为已支付
 * @param {Number} id - 发票ID
 * @param {Object} paymentData - 支付信息数据
 * @returns {Promise} - 返回Promise对象
 */
export function markInvoiceAsPaid(id, paymentData) {
  return request({
    url: `/api/sales/invoices/${id}/mark-paid`,
    method: 'post',
    data: paymentData
  });
}

/**
 * 发票API钩子函数
 * @returns {Object} - 返回所有发票相关API方法的对象
 */
export function useInvoiceApi() {
  return {
    getInvoices,
    getInvoice,
    createInvoice,
    updateInvoice,
    deleteInvoice,
    updateInvoiceStatus,
    createInvoiceFromOrder,
    getInvoiceItems,
    addInvoiceItem,
    updateInvoiceItem,
    deleteInvoiceItem,
    recordInvoicePayment,
    getInvoicePayments,
    sendInvoiceEmail,
    exportInvoicePdf,
    getInvoiceStatistics,
    cancelInvoice,
    markInvoiceAsPaid
  };
} 