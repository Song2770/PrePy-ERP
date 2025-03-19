import request from '@/utils/request';

/**
 * 获取物料列表
 * @param {Object} params - 查询参数（分页、过滤等）
 * @returns {Promise} - 返回Promise对象
 */
export function getMaterials(params) {
  return request({
    url: '/api/technical/materials',
    method: 'get',
    params
  });
}

/**
 * 获取单个物料详情
 * @param {Number} id - 物料ID
 * @returns {Promise} - 返回Promise对象
 */
export function getMaterial(id) {
  return request({
    url: `/api/technical/materials/${id}`,
    method: 'get'
  });
}

/**
 * 创建新物料
 * @param {Object} materialData - 物料数据
 * @returns {Promise} - 返回Promise对象
 */
export function createMaterial(materialData) {
  return request({
    url: '/api/technical/materials',
    method: 'post',
    data: materialData
  });
}

/**
 * 更新物料
 * @param {Number} id - 物料ID
 * @param {Object} materialData - 更新的物料数据
 * @returns {Promise} - 返回Promise对象
 */
export function updateMaterial(id, materialData) {
  return request({
    url: `/api/technical/materials/${id}`,
    method: 'put',
    data: materialData
  });
}

/**
 * 删除物料
 * @param {Number} id - 物料ID
 * @returns {Promise} - 返回Promise对象
 */
export function deleteMaterial(id) {
  return request({
    url: `/api/technical/materials/${id}`,
    method: 'delete'
  });
}

/**
 * 搜索物料
 * @param {Object} params - 搜索参数
 * @returns {Promise} - 返回Promise对象
 */
export function searchMaterials(params) {
  return request({
    url: '/api/technical/materials/search',
    method: 'get',
    params
  });
}

/**
 * 获取物料分类列表
 * @returns {Promise} - 返回Promise对象
 */
export function getMaterialCategories() {
  return request({
    url: '/api/technical/material-categories',
    method: 'get'
  });
}

/**
 * 获取物料供应商列表
 * @param {Number} materialId - 物料ID
 * @returns {Promise} - 返回Promise对象
 */
export function getMaterialSuppliers(materialId) {
  return request({
    url: `/api/technical/materials/${materialId}/suppliers`,
    method: 'get'
  });
}

/**
 * 添加物料供应商
 * @param {Number} materialId - 物料ID
 * @param {Object} supplierData - 供应商数据
 * @returns {Promise} - 返回Promise对象
 */
export function addMaterialSupplier(materialId, supplierData) {
  return request({
    url: `/api/technical/materials/${materialId}/suppliers`,
    method: 'post',
    data: supplierData
  });
}

/**
 * 更新物料供应商
 * @param {Number} materialId - 物料ID
 * @param {Number} supplierId - 供应商ID
 * @param {Object} supplierData - 更新的供应商数据
 * @returns {Promise} - 返回Promise对象
 */
export function updateMaterialSupplier(materialId, supplierId, supplierData) {
  return request({
    url: `/api/technical/materials/${materialId}/suppliers/${supplierId}`,
    method: 'put',
    data: supplierData
  });
}

/**
 * 删除物料供应商
 * @param {Number} materialId - 物料ID
 * @param {Number} supplierId - 供应商ID
 * @returns {Promise} - 返回Promise对象
 */
export function deleteMaterialSupplier(materialId, supplierId) {
  return request({
    url: `/api/technical/materials/${materialId}/suppliers/${supplierId}`,
    method: 'delete'
  });
}

/**
 * 获取物料价格历史
 * @param {Number} materialId - 物料ID
 * @param {Object} params - 查询参数
 * @returns {Promise} - 返回Promise对象
 */
export function getMaterialPriceHistory(materialId, params) {
  return request({
    url: `/api/technical/materials/${materialId}/price-history`,
    method: 'get',
    params
  });
}

/**
 * 添加物料价格记录
 * @param {Number} materialId - 物料ID
 * @param {Object} priceData - 价格数据
 * @returns {Promise} - 返回Promise对象
 */
export function addMaterialPrice(materialId, priceData) {
  return request({
    url: `/api/technical/materials/${materialId}/prices`,
    method: 'post',
    data: priceData
  });
}

/**
 * 上传物料图片
 * @param {Number} materialId - 物料ID
 * @param {FormData} fileData - 图片文件数据
 * @returns {Promise} - 返回Promise对象
 */
export function uploadMaterialImage(materialId, fileData) {
  return request({
    url: `/api/technical/materials/${materialId}/image`,
    method: 'post',
    data: fileData,
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  });
}

/**
 * 获取物料库存信息
 * @param {Number} materialId - 物料ID
 * @returns {Promise} - 返回Promise对象
 */
export function getMaterialInventory(materialId) {
  return request({
    url: `/api/technical/materials/${materialId}/inventory`,
    method: 'get'
  });
}

/**
 * 获取物料库存历史
 * @param {Number} materialId - 物料ID
 * @param {Object} params - 查询参数
 * @returns {Promise} - 返回Promise对象
 */
export function getMaterialInventoryHistory(materialId, params) {
  return request({
    url: `/api/technical/materials/${materialId}/inventory-history`,
    method: 'get',
    params
  });
}

/**
 * 获取物料用途（被哪些产品使用）
 * @param {Number} materialId - 物料ID
 * @param {Object} params - 查询参数
 * @returns {Promise} - 返回Promise对象
 */
export function getMaterialUsage(materialId, params) {
  return request({
    url: `/api/technical/materials/${materialId}/usage`,
    method: 'get',
    params
  });
}

/**
 * 获取物料文档列表
 * @param {Number} materialId - 物料ID
 * @returns {Promise} - 返回Promise对象
 */
export function getMaterialDocuments(materialId) {
  return request({
    url: `/api/technical/materials/${materialId}/documents`,
    method: 'get'
  });
}

/**
 * 上传物料文档
 * @param {Number} materialId - 物料ID
 * @param {FormData} fileData - 文档文件数据
 * @returns {Promise} - 返回Promise对象
 */
export function uploadMaterialDocument(materialId, fileData) {
  return request({
    url: `/api/technical/materials/${materialId}/documents`,
    method: 'post',
    data: fileData,
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  });
}

/**
 * 删除物料文档
 * @param {Number} materialId - 物料ID
 * @param {Number} documentId - 文档ID
 * @returns {Promise} - 返回Promise对象
 */
export function deleteMaterialDocument(materialId, documentId) {
  return request({
    url: `/api/technical/materials/${materialId}/documents/${documentId}`,
    method: 'delete'
  });
}

/**
 * 获取物料的替代品
 * @param {Number} materialId - 物料ID
 * @returns {Promise} - 返回Promise对象
 */
export function getMaterialAlternatives(materialId) {
  return request({
    url: `/api/technical/materials/${materialId}/alternatives`,
    method: 'get'
  });
}

/**
 * 添加物料替代品
 * @param {Number} materialId - 物料ID
 * @param {Object} alternativeData - 替代品数据
 * @returns {Promise} - 返回Promise对象
 */
export function addMaterialAlternative(materialId, alternativeData) {
  return request({
    url: `/api/technical/materials/${materialId}/alternatives`,
    method: 'post',
    data: alternativeData
  });
}

/**
 * 删除物料替代品
 * @param {Number} materialId - 物料ID
 * @param {Number} alternativeId - 替代品ID
 * @returns {Promise} - 返回Promise对象
 */
export function deleteMaterialAlternative(materialId, alternativeId) {
  return request({
    url: `/api/technical/materials/${materialId}/alternatives/${alternativeId}`,
    method: 'delete'
  });
}

/**
 * 导出物料数据
 * @param {Object} params - 查询参数
 * @returns {Promise} - 返回Promise对象
 */
export function exportMaterials(params) {
  return request({
    url: '/api/technical/materials/export',
    method: 'get',
    params,
    responseType: 'blob'
  });
}

/**
 * 导入物料数据
 * @param {FormData} fileData - 导入的文件数据
 * @returns {Promise} - 返回Promise对象
 */
export function importMaterials(fileData) {
  return request({
    url: '/api/technical/materials/import',
    method: 'post',
    data: fileData,
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  });
}

/**
 * 物料API钩子函数
 * @returns {Object} - 返回所有物料相关API方法的对象
 */
export function useMaterialApi() {
  return {
    getMaterials,
    getMaterial,
    createMaterial,
    updateMaterial,
    deleteMaterial,
    searchMaterials,
    getMaterialCategories,
    getMaterialSuppliers,
    addMaterialSupplier,
    updateMaterialSupplier,
    deleteMaterialSupplier,
    getMaterialPriceHistory,
    addMaterialPrice,
    uploadMaterialImage,
    getMaterialInventory,
    getMaterialInventoryHistory,
    getMaterialUsage,
    getMaterialDocuments,
    uploadMaterialDocument,
    deleteMaterialDocument,
    getMaterialAlternatives,
    addMaterialAlternative,
    deleteMaterialAlternative,
    exportMaterials,
    importMaterials
  };
} 