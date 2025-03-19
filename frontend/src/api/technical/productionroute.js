import request from '@/utils/request';

/**
 * 获取生产路线列表
 * @param {Object} params - 查询参数（分页、过滤等）
 * @returns {Promise} - 返回Promise对象
 */
export function getProductionRoutes(params) {
  return request({
    url: '/api/technical/production-routes',
    method: 'get',
    params
  });
}

/**
 * 获取单个生产路线详情
 * @param {Number} id - 生产路线ID
 * @returns {Promise} - 返回Promise对象
 */
export function getProductionRoute(id) {
  return request({
    url: `/api/technical/production-routes/${id}`,
    method: 'get'
  });
}

/**
 * 创建新生产路线
 * @param {Object} routeData - 生产路线数据
 * @returns {Promise} - 返回Promise对象
 */
export function createProductionRoute(routeData) {
  return request({
    url: '/api/technical/production-routes',
    method: 'post',
    data: routeData
  });
}

/**
 * 更新生产路线
 * @param {Number} id - 生产路线ID
 * @param {Object} routeData - 更新的生产路线数据
 * @returns {Promise} - 返回Promise对象
 */
export function updateProductionRoute(id, routeData) {
  return request({
    url: `/api/technical/production-routes/${id}`,
    method: 'put',
    data: routeData
  });
}

/**
 * 删除生产路线
 * @param {Number} id - 生产路线ID
 * @returns {Promise} - 返回Promise对象
 */
export function deleteProductionRoute(id) {
  return request({
    url: `/api/technical/production-routes/${id}`,
    method: 'delete'
  });
}

/**
 * 获取产品的生产路线
 * @param {Number} productId - 产品ID
 * @returns {Promise} - 返回Promise对象
 */
export function getProductProductionRoute(productId) {
  return request({
    url: `/api/technical/products/${productId}/production-route`,
    method: 'get'
  });
}

/**
 * 获取生产路线步骤列表
 * @param {Number} routeId - 生产路线ID
 * @returns {Promise} - 返回Promise对象
 */
export function getProductionRouteSteps(routeId) {
  return request({
    url: `/api/technical/production-routes/${routeId}/steps`,
    method: 'get'
  });
}

/**
 * 添加生产路线步骤
 * @param {Number} routeId - 生产路线ID
 * @param {Object} stepData - 步骤数据
 * @returns {Promise} - 返回Promise对象
 */
export function addProductionRouteStep(routeId, stepData) {
  return request({
    url: `/api/technical/production-routes/${routeId}/steps`,
    method: 'post',
    data: stepData
  });
}

/**
 * 更新生产路线步骤
 * @param {Number} routeId - 生产路线ID
 * @param {Number} stepId - 步骤ID
 * @param {Object} stepData - 步骤数据
 * @returns {Promise} - 返回Promise对象
 */
export function updateProductionRouteStep(routeId, stepId, stepData) {
  return request({
    url: `/api/technical/production-routes/${routeId}/steps/${stepId}`,
    method: 'put',
    data: stepData
  });
}

/**
 * 删除生产路线步骤
 * @param {Number} routeId - 生产路线ID
 * @param {Number} stepId - 步骤ID
 * @returns {Promise} - 返回Promise对象
 */
export function deleteProductionRouteStep(routeId, stepId) {
  return request({
    url: `/api/technical/production-routes/${routeId}/steps/${stepId}`,
    method: 'delete'
  });
}

/**
 * 调整生产路线步骤顺序
 * @param {Number} routeId - 生产路线ID
 * @param {Object} orderData - 排序数据，包含步骤ID和新顺序
 * @returns {Promise} - 返回Promise对象
 */
export function reorderProductionRouteSteps(routeId, orderData) {
  return request({
    url: `/api/technical/production-routes/${routeId}/steps/reorder`,
    method: 'put',
    data: orderData
  });
}

/**
 * 获取生产路线步骤详情
 * @param {Number} routeId - 生产路线ID
 * @param {Number} stepId - 步骤ID
 * @returns {Promise} - 返回Promise对象
 */
export function getProductionRouteStep(routeId, stepId) {
  return request({
    url: `/api/technical/production-routes/${routeId}/steps/${stepId}`,
    method: 'get'
  });
}

/**
 * 获取步骤所需资源列表
 * @param {Number} routeId - 生产路线ID
 * @param {Number} stepId - 步骤ID
 * @returns {Promise} - 返回Promise对象
 */
export function getStepResources(routeId, stepId) {
  return request({
    url: `/api/technical/production-routes/${routeId}/steps/${stepId}/resources`,
    method: 'get'
  });
}

/**
 * 添加步骤所需资源
 * @param {Number} routeId - 生产路线ID
 * @param {Number} stepId - 步骤ID
 * @param {Object} resourceData - 资源数据
 * @returns {Promise} - 返回Promise对象
 */
export function addStepResource(routeId, stepId, resourceData) {
  return request({
    url: `/api/technical/production-routes/${routeId}/steps/${stepId}/resources`,
    method: 'post',
    data: resourceData
  });
}

/**
 * 更新步骤所需资源
 * @param {Number} routeId - 生产路线ID
 * @param {Number} stepId - 步骤ID
 * @param {Number} resourceId - 资源ID
 * @param {Object} resourceData - 资源数据
 * @returns {Promise} - 返回Promise对象
 */
export function updateStepResource(routeId, stepId, resourceId, resourceData) {
  return request({
    url: `/api/technical/production-routes/${routeId}/steps/${stepId}/resources/${resourceId}`,
    method: 'put',
    data: resourceData
  });
}

/**
 * 删除步骤所需资源
 * @param {Number} routeId - 生产路线ID
 * @param {Number} stepId - 步骤ID
 * @param {Number} resourceId - 资源ID
 * @returns {Promise} - 返回Promise对象
 */
export function deleteStepResource(routeId, stepId, resourceId) {
  return request({
    url: `/api/technical/production-routes/${routeId}/steps/${stepId}/resources/${resourceId}`,
    method: 'delete'
  });
}

/**
 * 计算生产路线成本
 * @param {Number} routeId - 生产路线ID
 * @param {Object} params - 计算参数（批量大小等）
 * @returns {Promise} - 返回Promise对象
 */
export function calculateRouteCost(routeId, params) {
  return request({
    url: `/api/technical/production-routes/${routeId}/cost-calculation`,
    method: 'get',
    params
  });
}

/**
 * 获取生产路线的工艺文档
 * @param {Number} routeId - 生产路线ID
 * @returns {Promise} - 返回Promise对象
 */
export function getRouteDocuments(routeId) {
  return request({
    url: `/api/technical/production-routes/${routeId}/documents`,
    method: 'get'
  });
}

/**
 * 添加生产路线工艺文档
 * @param {Number} routeId - 生产路线ID
 * @param {Object} documentData - 文档数据
 * @returns {Promise} - 返回Promise对象
 */
export function addRouteDocument(routeId, documentData) {
  return request({
    url: `/api/technical/production-routes/${routeId}/documents`,
    method: 'post',
    data: documentData
  });
}

/**
 * 删除生产路线工艺文档
 * @param {Number} routeId - 生产路线ID
 * @param {Number} documentId - 文档ID
 * @returns {Promise} - 返回Promise对象
 */
export function deleteRouteDocument(routeId, documentId) {
  return request({
    url: `/api/technical/production-routes/${routeId}/documents/${documentId}`,
    method: 'delete'
  });
}

/**
 * 获取生产路线版本历史
 * @param {Number} routeId - 生产路线ID
 * @returns {Promise} - 返回Promise对象
 */
export function getRouteVersions(routeId) {
  return request({
    url: `/api/technical/production-routes/${routeId}/versions`,
    method: 'get'
  });
}

/**
 * 创建生产路线新版本
 * @param {Number} routeId - 生产路线ID
 * @param {Object} versionData - 版本数据
 * @returns {Promise} - 返回Promise对象
 */
export function createRouteVersion(routeId, versionData) {
  return request({
    url: `/api/technical/production-routes/${routeId}/versions`,
    method: 'post',
    data: versionData
  });
}

/**
 * 获取特定版本的生产路线
 * @param {Number} routeId - 生产路线ID
 * @param {Number} versionId - 版本ID
 * @returns {Promise} - 返回Promise对象
 */
export function getRouteVersion(routeId, versionId) {
  return request({
    url: `/api/technical/production-routes/${routeId}/versions/${versionId}`,
    method: 'get'
  });
}

/**
 * 设置生产路线版本为当前版本
 * @param {Number} routeId - 生产路线ID
 * @param {Number} versionId - 版本ID
 * @returns {Promise} - 返回Promise对象
 */
export function setRouteVersionAsCurrent(routeId, versionId) {
  return request({
    url: `/api/technical/production-routes/${routeId}/versions/${versionId}/set-current`,
    method: 'put'
  });
}

/**
 * 复制生产路线
 * @param {Number} routeId - 生产路线ID
 * @param {Object} copyData - 复制数据（新名称等）
 * @returns {Promise} - 返回Promise对象
 */
export function copyProductionRoute(routeId, copyData) {
  return request({
    url: `/api/technical/production-routes/${routeId}/copy`,
    method: 'post',
    data: copyData
  });
}

/**
 * 获取生产路线审批流程
 * @param {Number} routeId - 生产路线ID
 * @returns {Promise} - 返回Promise对象
 */
export function getRouteApprovalFlow(routeId) {
  return request({
    url: `/api/technical/production-routes/${routeId}/approval-flow`,
    method: 'get'
  });
}

/**
 * 提交生产路线审批
 * @param {Number} routeId - 生产路线ID
 * @param {Object} approvalData - 审批数据
 * @returns {Promise} - 返回Promise对象
 */
export function submitRouteForApproval(routeId, approvalData) {
  return request({
    url: `/api/technical/production-routes/${routeId}/approval-flow`,
    method: 'post',
    data: approvalData
  });
}

/**
 * 审批生产路线
 * @param {Number} routeId - 生产路线ID
 * @param {Number} approvalId - 审批ID
 * @param {Object} approvalData - 审批结果数据
 * @returns {Promise} - 返回Promise对象
 */
export function approveRoute(routeId, approvalId, approvalData) {
  return request({
    url: `/api/technical/production-routes/${routeId}/approval-flow/${approvalId}`,
    method: 'put',
    data: approvalData
  });
}

/**
 * 获取生产路线统计数据
 * @param {Number} routeId - 生产路线ID
 * @param {Object} params - 查询参数（时间范围等）
 * @returns {Promise} - 返回Promise对象
 */
export function getRouteStatistics(routeId, params) {
  return request({
    url: `/api/technical/production-routes/${routeId}/statistics`,
    method: 'get',
    params
  });
}

/**
 * 获取推荐的生产路线模板
 * @param {Object} params - 查询参数（产品类型等）
 * @returns {Promise} - 返回Promise对象
 */
export function getRouteTemplates(params) {
  return request({
    url: '/api/technical/production-route-templates',
    method: 'get',
    params
  });
}

/**
 * 基于模板创建生产路线
 * @param {Number} templateId - 模板ID
 * @param {Object} routeData - 生产路线数据
 * @returns {Promise} - 返回Promise对象
 */
export function createRouteFromTemplate(templateId, routeData) {
  return request({
    url: `/api/technical/production-route-templates/${templateId}/create`,
    method: 'post',
    data: routeData
  });
}

/**
 * 导出生产路线数据
 * @param {Object} params - 导出参数
 * @returns {Promise} - 返回Promise对象
 */
export function exportProductionRoutes(params) {
  return request({
    url: '/api/technical/production-routes/export',
    method: 'get',
    params,
    responseType: 'blob'
  });
}

/**
 * 导入生产路线数据
 * @param {FormData} fileData - 导入的文件数据
 * @returns {Promise} - 返回Promise对象
 */
export function importProductionRoutes(fileData) {
  return request({
    url: '/api/technical/production-routes/import',
    method: 'post',
    data: fileData,
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  });
}

/**
 * 生产路线API钩子函数
 * @returns {Object} - 返回所有生产路线相关API方法的对象
 */
export function useProductionRouteApi() {
  return {
    getProductionRoutes,
    getProductionRoute,
    createProductionRoute,
    updateProductionRoute,
    deleteProductionRoute,
    getProductProductionRoute,
    getProductionRouteSteps,
    addProductionRouteStep,
    updateProductionRouteStep,
    deleteProductionRouteStep,
    reorderProductionRouteSteps,
    getProductionRouteStep,
    getStepResources,
    addStepResource,
    updateStepResource,
    deleteStepResource,
    calculateRouteCost,
    getRouteDocuments,
    addRouteDocument,
    deleteRouteDocument,
    getRouteVersions,
    createRouteVersion,
    getRouteVersion,
    setRouteVersionAsCurrent,
    copyProductionRoute,
    getRouteApprovalFlow,
    submitRouteForApproval,
    approveRoute,
    getRouteStatistics,
    getRouteTemplates,
    createRouteFromTemplate,
    exportProductionRoutes,
    importProductionRoutes
  };
} 