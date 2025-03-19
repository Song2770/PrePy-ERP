import request from '@/utils/request';

/**
 * 获取工作站列表
 * @param {Object} params - 查询参数（分页、过滤等）
 * @returns {Promise} - 返回Promise对象
 */
export function getWorkstations(params) {
  return request({
    url: '/api/technical/workstations',
    method: 'get',
    params
  });
}

/**
 * 获取单个工作站详情
 * @param {Number} id - 工作站ID
 * @returns {Promise} - 返回Promise对象
 */
export function getWorkstation(id) {
  return request({
    url: `/api/technical/workstations/${id}`,
    method: 'get'
  });
}

/**
 * 创建新工作站
 * @param {Object} workstationData - 工作站数据
 * @returns {Promise} - 返回Promise对象
 */
export function createWorkstation(workstationData) {
  return request({
    url: '/api/technical/workstations',
    method: 'post',
    data: workstationData
  });
}

/**
 * 更新工作站
 * @param {Number} id - 工作站ID
 * @param {Object} workstationData - 更新的工作站数据
 * @returns {Promise} - 返回Promise对象
 */
export function updateWorkstation(id, workstationData) {
  return request({
    url: `/api/technical/workstations/${id}`,
    method: 'put',
    data: workstationData
  });
}

/**
 * 删除工作站
 * @param {Number} id - 工作站ID
 * @returns {Promise} - 返回Promise对象
 */
export function deleteWorkstation(id) {
  return request({
    url: `/api/technical/workstations/${id}`,
    method: 'delete'
  });
}

/**
 * 按工作中心筛选工作站列表
 * @param {Number} workCenterId - 工作中心ID
 * @param {Object} params - 其他查询参数
 * @returns {Promise} - 返回Promise对象
 */
export function getWorkstationsByWorkCenter(workCenterId, params = {}) {
  return request({
    url: '/api/technical/workstations',
    method: 'get',
    params: { ...params, work_center: workCenterId }
  });
}

/**
 * 获取工作站产能利用率数据
 * @param {Number} id - 工作站ID
 * @param {Object} params - 查询参数（日期范围等）
 * @returns {Promise} - 返回Promise对象
 */
export function getWorkstationCapacityUtilization(id, params) {
  return request({
    url: `/api/technical/workstations/${id}/capacity-utilization`,
    method: 'get',
    params
  });
}

/**
 * 获取工作站负载数据
 * @param {Number} id - 工作站ID
 * @param {Object} params - 查询参数（日期范围等）
 * @returns {Promise} - 返回Promise对象
 */
export function getWorkstationWorkload(id, params) {
  return request({
    url: `/api/technical/workstations/${id}/workload`,
    method: 'get',
    params
  });
}

/**
 * 获取工作站统计数据
 * @param {Number} id - 工作站ID
 * @param {Object} params - 查询参数（日期范围等）
 * @returns {Promise} - 返回Promise对象
 */
export function getWorkstationStats(id, params) {
  return request({
    url: `/api/technical/workstations/${id}/stats`,
    method: 'get',
    params
  });
}

/**
 * 获取工作站维护记录
 * @param {Number} id - 工作站ID
 * @param {Object} params - 查询参数（分页等）
 * @returns {Promise} - 返回Promise对象
 */
export function getWorkstationMaintenanceRecords(id, params) {
  return request({
    url: `/api/technical/workstations/${id}/maintenance-records`,
    method: 'get',
    params
  });
}

/**
 * 添加工作站维护记录
 * @param {Number} id - 工作站ID
 * @param {Object} recordData - 维护记录数据
 * @returns {Promise} - 返回Promise对象
 */
export function addWorkstationMaintenanceRecord(id, recordData) {
  return request({
    url: `/api/technical/workstations/${id}/maintenance-records`,
    method: 'post',
    data: recordData
  });
}

/**
 * 获取工作站操作员列表
 * @param {Number} id - 工作站ID
 * @param {Object} params - 查询参数（分页等）
 * @returns {Promise} - 返回Promise对象
 */
export function getWorkstationOperators(id, params) {
  return request({
    url: `/api/technical/workstations/${id}/operators`,
    method: 'get',
    params
  });
}

/**
 * 分配操作员到工作站
 * @param {Number} id - 工作站ID
 * @param {Object} assignData - 分配数据（包含操作员ID列表）
 * @returns {Promise} - 返回Promise对象
 */
export function assignOperatorsToWorkstation(id, assignData) {
  return request({
    url: `/api/technical/workstations/${id}/operators`,
    method: 'post',
    data: assignData
  });
}

/**
 * 移除工作站操作员
 * @param {Number} workstationId - 工作站ID
 * @param {Number} operatorId - 操作员ID
 * @returns {Promise} - 返回Promise对象
 */
export function removeOperatorFromWorkstation(workstationId, operatorId) {
  return request({
    url: `/api/technical/workstations/${workstationId}/operators/${operatorId}`,
    method: 'delete'
  });
}

/**
 * 工作站API钩子函数
 * @returns {Object} - 返回所有工作站相关API方法的对象
 */
export function useWorkstationApi() {
  return {
    getWorkstations,
    getWorkstation,
    createWorkstation,
    updateWorkstation,
    deleteWorkstation,
    getWorkstationsByWorkCenter,
    getWorkstationCapacityUtilization,
    getWorkstationWorkload,
    getWorkstationStats,
    getWorkstationMaintenanceRecords,
    addWorkstationMaintenanceRecord,
    getWorkstationOperators,
    assignOperatorsToWorkstation,
    removeOperatorFromWorkstation
  };
} 