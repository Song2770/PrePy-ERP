import request from '@/utils/request';

/**
 * 获取工作中心列表
 * @param {Object} params - 查询参数（分页、过滤等）
 * @returns {Promise} - 返回Promise对象
 */
export function getWorkCenters(params) {
  return request({
    url: '/api/technical/workcenters',
    method: 'get',
    params
  });
}

/**
 * 获取单个工作中心详情
 * @param {Number} id - 工作中心ID
 * @returns {Promise} - 返回Promise对象
 */
export function getWorkCenter(id) {
  return request({
    url: `/api/technical/workcenters/${id}`,
    method: 'get'
  });
}

/**
 * 创建新工作中心
 * @param {Object} workCenterData - 工作中心数据
 * @returns {Promise} - 返回Promise对象
 */
export function createWorkCenter(workCenterData) {
  return request({
    url: '/api/technical/workcenters',
    method: 'post',
    data: workCenterData
  });
}

/**
 * 更新工作中心
 * @param {Number} id - 工作中心ID
 * @param {Object} workCenterData - 更新的工作中心数据
 * @returns {Promise} - 返回Promise对象
 */
export function updateWorkCenter(id, workCenterData) {
  return request({
    url: `/api/technical/workcenters/${id}`,
    method: 'put',
    data: workCenterData
  });
}

/**
 * 删除工作中心
 * @param {Number} id - 工作中心ID
 * @returns {Promise} - 返回Promise对象
 */
export function deleteWorkCenter(id) {
  return request({
    url: `/api/technical/workcenters/${id}`,
    method: 'delete'
  });
}

/**
 * 获取工作中心下的工作站列表
 * @param {Number} workCenterId - 工作中心ID
 * @param {Object} params - 查询参数（分页等）
 * @returns {Promise} - 返回Promise对象
 */
export function getWorkCenterWorkstations(workCenterId, params) {
  return request({
    url: `/api/technical/workcenters/${workCenterId}/workstations`,
    method: 'get',
    params
  });
}

/**
 * 获取工作中心产能利用率数据
 * @param {Number} id - 工作中心ID
 * @param {Object} params - 查询参数（日期范围等）
 * @returns {Promise} - 返回Promise对象
 */
export function getWorkCenterCapacityUtilization(id, params) {
  return request({
    url: `/api/technical/workcenters/${id}/capacity-utilization`,
    method: 'get',
    params
  });
}

/**
 * 获取工作中心负载数据
 * @param {Number} id - 工作中心ID
 * @param {Object} params - 查询参数（日期范围等）
 * @returns {Promise} - 返回Promise对象
 */
export function getWorkCenterWorkload(id, params) {
  return request({
    url: `/api/technical/workcenters/${id}/workload`,
    method: 'get',
    params
  });
}

/**
 * 获取工作中心统计数据
 * @param {Number} id - 工作中心ID
 * @param {Object} params - 查询参数（日期范围等）
 * @returns {Promise} - 返回Promise对象
 */
export function getWorkCenterStats(id, params) {
  return request({
    url: `/api/technical/workcenters/${id}/stats`,
    method: 'get',
    params
  });
}

/**
 * 获取工作中心维护记录
 * @param {Number} id - 工作中心ID
 * @param {Object} params - 查询参数（分页等）
 * @returns {Promise} - 返回Promise对象
 */
export function getWorkCenterMaintenanceRecords(id, params) {
  return request({
    url: `/api/technical/workcenters/${id}/maintenance-records`,
    method: 'get',
    params
  });
}

/**
 * 添加工作中心维护记录
 * @param {Number} id - 工作中心ID
 * @param {Object} recordData - 维护记录数据
 * @returns {Promise} - 返回Promise对象
 */
export function addWorkCenterMaintenanceRecord(id, recordData) {
  return request({
    url: `/api/technical/workcenters/${id}/maintenance-records`,
    method: 'post',
    data: recordData
  });
}

/**
 * 获取工作中心分配的操作员列表
 * @param {Number} id - 工作中心ID
 * @param {Object} params - 查询参数（分页等）
 * @returns {Promise} - 返回Promise对象
 */
export function getWorkCenterOperators(id, params) {
  return request({
    url: `/api/technical/workcenters/${id}/operators`,
    method: 'get',
    params
  });
}

/**
 * 分配操作员到工作中心
 * @param {Number} id - 工作中心ID
 * @param {Object} assignData - 分配数据（包含操作员ID列表）
 * @returns {Promise} - 返回Promise对象
 */
export function assignOperatorsToWorkCenter(id, assignData) {
  return request({
    url: `/api/technical/workcenters/${id}/operators`,
    method: 'post',
    data: assignData
  });
}

/**
 * 移除工作中心操作员
 * @param {Number} workCenterId - 工作中心ID
 * @param {Number} operatorId - 操作员ID
 * @returns {Promise} - 返回Promise对象
 */
export function removeOperatorFromWorkCenter(workCenterId, operatorId) {
  return request({
    url: `/api/technical/workcenters/${workCenterId}/operators/${operatorId}`,
    method: 'delete'
  });
}

/**
 * 获取工作中心的生产计划
 * @param {Number} id - 工作中心ID
 * @param {Object} params - 查询参数（日期范围等）
 * @returns {Promise} - 返回Promise对象
 */
export function getWorkCenterSchedule(id, params) {
  return request({
    url: `/api/technical/workcenters/${id}/schedule`,
    method: 'get',
    params
  });
}

/**
 * 添加工作中心的排产任务
 * @param {Number} id - 工作中心ID
 * @param {Object} scheduleData - 排产数据
 * @returns {Promise} - 返回Promise对象
 */
export function addWorkCenterScheduleTask(id, scheduleData) {
  return request({
    url: `/api/technical/workcenters/${id}/schedule`,
    method: 'post',
    data: scheduleData
  });
}

/**
 * 更新工作中心的排产任务
 * @param {Number} workCenterId - 工作中心ID
 * @param {Number} taskId - 任务ID
 * @param {Object} taskData - 任务数据
 * @returns {Promise} - 返回Promise对象
 */
export function updateWorkCenterScheduleTask(workCenterId, taskId, taskData) {
  return request({
    url: `/api/technical/workcenters/${workCenterId}/schedule/${taskId}`,
    method: 'put',
    data: taskData
  });
}

/**
 * 删除工作中心的排产任务
 * @param {Number} workCenterId - 工作中心ID
 * @param {Number} taskId - 任务ID
 * @returns {Promise} - 返回Promise对象
 */
export function deleteWorkCenterScheduleTask(workCenterId, taskId) {
  return request({
    url: `/api/technical/workcenters/${workCenterId}/schedule/${taskId}`,
    method: 'delete'
  });
}

/**
 * 获取工作中心的产能配置
 * @param {Number} id - 工作中心ID
 * @returns {Promise} - 返回Promise对象
 */
export function getWorkCenterCapacity(id) {
  return request({
    url: `/api/technical/workcenters/${id}/capacity`,
    method: 'get'
  });
}

/**
 * 更新工作中心的产能配置
 * @param {Number} id - 工作中心ID
 * @param {Object} capacityData - 产能数据
 * @returns {Promise} - 返回Promise对象
 */
export function updateWorkCenterCapacity(id, capacityData) {
  return request({
    url: `/api/technical/workcenters/${id}/capacity`,
    method: 'put',
    data: capacityData
  });
}

/**
 * 获取工作中心的效率指标
 * @param {Number} id - 工作中心ID
 * @param {Object} params - 查询参数（日期范围等）
 * @returns {Promise} - 返回Promise对象
 */
export function getWorkCenterEfficiency(id, params) {
  return request({
    url: `/api/technical/workcenters/${id}/efficiency`,
    method: 'get',
    params
  });
}

/**
 * 导出工作中心数据
 * @param {Object} params - 导出参数
 * @returns {Promise} - 返回Promise对象
 */
export function exportWorkCenters(params) {
  return request({
    url: '/api/technical/workcenters/export',
    method: 'get',
    params,
    responseType: 'blob'
  });
}

/**
 * 导入工作中心数据
 * @param {FormData} fileData - 导入文件数据
 * @returns {Promise} - 返回Promise对象
 */
export function importWorkCenters(fileData) {
  return request({
    url: '/api/technical/workcenters/import',
    method: 'post',
    data: fileData,
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  });
}

/**
 * 工作中心API钩子函数
 * @returns {Object} - 返回所有工作中心相关API方法的对象
 */
export function useWorkCenterApi() {
  return {
    getWorkCenters,
    getWorkCenter,
    createWorkCenter,
    updateWorkCenter,
    deleteWorkCenter,
    getWorkCenterWorkstations,
    getWorkCenterCapacityUtilization,
    getWorkCenterWorkload,
    getWorkCenterStats,
    getWorkCenterMaintenanceRecords,
    addWorkCenterMaintenanceRecord,
    getWorkCenterOperators,
    assignOperatorsToWorkCenter,
    removeOperatorFromWorkCenter,
    getWorkCenterSchedule,
    addWorkCenterScheduleTask,
    updateWorkCenterScheduleTask,
    deleteWorkCenterScheduleTask,
    getWorkCenterCapacity,
    updateWorkCenterCapacity,
    getWorkCenterEfficiency,
    exportWorkCenters,
    importWorkCenters
  };
} 