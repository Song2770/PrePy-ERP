import request from '@/utils/request';

// 生产计划相关接口
/**
 * 获取生产计划列表
 * @param {Object} params - 查询参数
 * @returns {Promise}
 */
export function getProductionPlans(params) {
  return request({
    url: '/api/planning/production-plans',
    method: 'get',
    params
  });
}

/**
 * 获取生产计划详情
 * @param {String|Number} id - 生产计划ID
 * @returns {Promise}
 */
export function getProductionPlan(id) {
  return request({
    url: `/api/planning/production-plans/${id}`,
    method: 'get'
  });
}

/**
 * 创建生产计划
 * @param {Object} data - 生产计划数据
 * @returns {Promise}
 */
export function createProductionPlan(data) {
  return request({
    url: '/api/planning/production-plans',
    method: 'post',
    data
  });
}

/**
 * 更新生产计划
 * @param {String|Number} id - 生产计划ID
 * @param {Object} data - 更新数据
 * @returns {Promise}
 */
export function updateProductionPlan(id, data) {
  return request({
    url: `/api/planning/production-plans/${id}`,
    method: 'put',
    data
  });
}

/**
 * 删除生产计划
 * @param {String|Number} id - 生产计划ID
 * @returns {Promise}
 */
export function deleteProductionPlan(id) {
  return request({
    url: `/api/planning/production-plans/${id}`,
    method: 'delete'
  });
}

// 生产计划项目相关接口
export function addProductionPlanItem(planId, data) {
  return request({
    url: `/api/planning/production-plans/${planId}/items`,
    method: 'post',
    data
  });
}

export function updateProductionPlanItem(itemId, data) {
  return request({
    url: `/api/planning/production-plan-items/${itemId}`,
    method: 'put',
    data
  });
}

export function deleteProductionPlanItem(itemId) {
  return request({
    url: `/api/planning/production-plan-items/${itemId}`,
    method: 'delete'
  });
}

// 物料需求计划相关接口
/**
 * 运行MRP
 * @param {String|Number} productionPlanId - 生产计划ID
 * @param {Object} params - 参数
 * @returns {Promise}
 */
export function runMRP(productionPlanId, params) {
  return request({
    url: `/api/planning/production-plans/${productionPlanId}/run-mrp`,
    method: 'post',
    data: params
  });
}

/**
 * 获取MRP清单
 * @param {Object} params - 查询参数
 * @returns {Promise}
 */
export function getMrpList(params) {
  return request({
    url: '/api/planning/mrp',
    method: 'get',
    params
  });
}

/**
 * 获取MRP物料详情
 * @param {String|Number} id - MRP物料ID
 * @returns {Promise}
 */
export function getMrpItemDetails(id) {
  return request({
    url: `/api/planning/mrp/${id}/details`,
    method: 'get'
  });
}

/**
 * 根据MRP创建采购请求
 * @param {Object} data - 采购请求数据
 * @returns {Promise}
 */
export function createPurchaseRequestFromMrp(data) {
  return request({
    url: '/api/planning/mrp/create-purchase-request',
    method: 'post',
    data
  });
}

/**
 * 获取采购请求列表
 * @param {Object} params - 查询参数
 * @returns {Promise}
 */
export function getPurchaseRequests(params) {
  return request({
    url: '/api/purchasing/purchase-requests',
    method: 'get',
    params
  });
}

/**
 * 审批采购请求
 * @param {String|Number} id - 采购请求ID
 * @returns {Promise}
 */
export function approvePurchaseRequest(id) {
  return request({
    url: `/api/purchasing/purchase-requests/${id}/approve`,
    method: 'post'
  });
}

/**
 * 获取工单列表
 * @param {Object} params - 查询参数
 * @returns {Promise}
 */
export function getWorkOrders(params) {
  return request({
    url: '/api/production/work-orders',
    method: 'get',
    params
  });
}

/**
 * 根据生产计划获取工单
 * @param {String|Number} productionPlanId - 生产计划ID
 * @returns {Promise}
 */
export function getWorkOrdersByPlan(productionPlanId) {
  return request({
    url: `/api/production/work-orders/by-plan/${productionPlanId}`,
    method: 'get'
  });
}

export default {
  getProductionPlans,
  getProductionPlan,
  createProductionPlan,
  updateProductionPlan,
  deleteProductionPlan,
  addProductionPlanItem,
  updateProductionPlanItem,
  deleteProductionPlanItem,
  runMRP,
  getMrpList,
  getMrpItemDetails,
  createPurchaseRequestFromMrp,
  getPurchaseRequests,
  approvePurchaseRequest,
  getWorkOrders,
  getWorkOrdersByPlan
}; 