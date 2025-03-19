import request from '@/utils/request';

/**
 * 获取BOM列表
 * @param {Object} params - 查询参数（分页、过滤等）
 * @returns {Promise} - 返回Promise对象
 */
export function getBoms(params) {
  return request({
    url: '/api/technical/boms',
    method: 'get',
    params
  });
}

/**
 * 获取单个BOM详情
 * @param {Number} id - BOM ID
 * @returns {Promise} - 返回Promise对象
 */
export function getBom(id) {
  return request({
    url: `/api/technical/boms/${id}`,
    method: 'get'
  });
}

/**
 * 获取产品的BOM
 * @param {Number} productId - 产品ID
 * @returns {Promise} - 返回Promise对象
 */
export function getProductBom(productId) {
  return request({
    url: `/api/technical/products/${productId}/bom`,
    method: 'get'
  });
}

/**
 * 创建新BOM
 * @param {Object} bomData - BOM数据
 * @returns {Promise} - 返回Promise对象
 */
export function createBom(bomData) {
  return request({
    url: '/api/technical/boms',
    method: 'post',
    data: bomData
  });
}

/**
 * 更新BOM
 * @param {Number} id - BOM ID
 * @param {Object} bomData - 更新的BOM数据
 * @returns {Promise} - 返回Promise对象
 */
export function updateBom(id, bomData) {
  return request({
    url: `/api/technical/boms/${id}`,
    method: 'put',
    data: bomData
  });
}

/**
 * 删除BOM
 * @param {Number} id - BOM ID
 * @returns {Promise} - 返回Promise对象
 */
export function deleteBom(id) {
  return request({
    url: `/api/technical/boms/${id}`,
    method: 'delete'
  });
}

/**
 * 获取BOM项列表
 * @param {Number} bomId - BOM ID
 * @returns {Promise} - 返回Promise对象
 */
export function getBomItems(bomId) {
  return request({
    url: `/api/technical/boms/${bomId}/items`,
    method: 'get'
  });
}

/**
 * 添加BOM项
 * @param {Number} bomId - BOM ID
 * @param {Object} itemData - BOM项数据
 * @returns {Promise} - 返回Promise对象
 */
export function addBomItem(bomId, itemData) {
  return request({
    url: `/api/technical/boms/${bomId}/items`,
    method: 'post',
    data: itemData
  });
}

/**
 * 更新BOM项
 * @param {Number} bomId - BOM ID
 * @param {Number} itemId - BOM项ID
 * @param {Object} itemData - 更新的BOM项数据
 * @returns {Promise} - 返回Promise对象
 */
export function updateBomItem(bomId, itemId, itemData) {
  return request({
    url: `/api/technical/boms/${bomId}/items/${itemId}`,
    method: 'put',
    data: itemData
  });
}

/**
 * 删除BOM项
 * @param {Number} bomId - BOM ID
 * @param {Number} itemId - BOM项ID
 * @returns {Promise} - 返回Promise对象
 */
export function deleteBomItem(bomId, itemId) {
  return request({
    url: `/api/technical/boms/${bomId}/items/${itemId}`,
    method: 'delete'
  });
}

/**
 * 复制BOM
 * @param {Number} id - 源BOM ID
 * @param {Object} copyData - 复制的配置数据
 * @returns {Promise} - 返回Promise对象
 */
export function copyBom(id, copyData) {
  return request({
    url: `/api/technical/boms/${id}/copy`,
    method: 'post',
    data: copyData
  });
}

/**
 * 激活BOM（设为当前版本）
 * @param {Number} id - BOM ID
 * @returns {Promise} - 返回Promise对象
 */
export function activateBom(id) {
  return request({
    url: `/api/technical/boms/${id}/activate`,
    method: 'put'
  });
}

/**
 * 替换BOM中的物料
 * @param {Number} id - BOM ID
 * @param {Object} replaceData - 替换的物料数据
 * @returns {Promise} - 返回Promise对象
 */
export function replaceBomMaterial(id, replaceData) {
  return request({
    url: `/api/technical/boms/${id}/replace-material`,
    method: 'post',
    data: replaceData
  });
}

/**
 * 计算BOM成本
 * @param {Number} id - BOM ID
 * @returns {Promise} - 返回Promise对象
 */
export function calculateBomCost(id) {
  return request({
    url: `/api/technical/boms/${id}/calculate-cost`,
    method: 'get'
  });
}

/**
 * 获取BOM的物料需求
 * @param {Number} id - BOM ID
 * @param {Object} params - 查询参数（如数量等）
 * @returns {Promise} - 返回Promise对象
 */
export function getBomMaterialRequirements(id, params) {
  return request({
    url: `/api/technical/boms/${id}/material-requirements`,
    method: 'get',
    params
  });
}

/**
 * 导出BOM数据
 * @param {Number} id - BOM ID
 * @param {String} format - 导出格式（如csv, xlsx等）
 * @returns {Promise} - 返回Promise对象
 */
export function exportBom(id, format = 'xlsx') {
  return request({
    url: `/api/technical/boms/${id}/export`,
    method: 'get',
    params: { format },
    responseType: 'blob'
  });
}

/**
 * 导入BOM数据
 * @param {Number} productId - 产品ID
 * @param {FormData} fileData - 导入的文件数据
 * @returns {Promise} - 返回Promise对象
 */
export function importBom(productId, fileData) {
  return request({
    url: '/api/technical/boms/import',
    method: 'post',
    data: fileData,
    params: { product_id: productId },
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  });
}

/**
 * BOM API钩子函数
 * @returns {Object} - 返回所有BOM相关API方法的对象
 */
export function useBomApi() {
  return {
    getBoms,
    getBom,
    getProductBom,
    createBom,
    updateBom,
    deleteBom,
    getBomItems,
    addBomItem,
    updateBomItem,
    deleteBomItem,
    copyBom,
    activateBom,
    replaceBomMaterial,
    calculateBomCost,
    getBomMaterialRequirements,
    exportBom,
    importBom
  };
} 