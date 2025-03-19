import request from '@/utils/request';

/**
 * 获取产品列表
 * @param {Object} params - 查询参数（分页、过滤等）
 * @returns {Promise} - 返回Promise对象
 */
export function getProducts(params) {
  return request({
    url: '/api/technical/products',
    method: 'get',
    params
  });
}

/**
 * 获取单个产品详情
 * @param {Number} id - 产品ID
 * @returns {Promise} - 返回Promise对象
 */
export function getProduct(id) {
  return request({
    url: `/api/technical/products/${id}`,
    method: 'get'
  });
}

/**
 * 创建新产品
 * @param {Object} productData - 产品数据
 * @returns {Promise} - 返回Promise对象
 */
export function createProduct(productData) {
  return request({
    url: '/api/technical/products',
    method: 'post',
    data: productData
  });
}

/**
 * 更新产品
 * @param {Number} id - 产品ID
 * @param {Object} productData - 更新的产品数据
 * @returns {Promise} - 返回Promise对象
 */
export function updateProduct(id, productData) {
  return request({
    url: `/api/technical/products/${id}`,
    method: 'put',
    data: productData
  });
}

/**
 * 删除产品
 * @param {Number} id - 产品ID
 * @returns {Promise} - 返回Promise对象
 */
export function deleteProduct(id) {
  return request({
    url: `/api/technical/products/${id}`,
    method: 'delete'
  });
}

/**
 * 搜索产品
 * @param {Object} params - 搜索参数
 * @returns {Promise} - 返回Promise对象
 */
export function searchProducts(params) {
  return request({
    url: '/api/technical/products/search',
    method: 'get',
    params
  });
}

/**
 * 获取产品分类列表
 * @returns {Promise} - 返回Promise对象
 */
export function getProductCategories() {
  return request({
    url: '/api/technical/product-categories',
    method: 'get'
  });
}

/**
 * 获取产品规格列表
 * @param {Number} productId - 产品ID
 * @returns {Promise} - 返回Promise对象
 */
export function getProductSpecifications(productId) {
  return request({
    url: `/api/technical/products/${productId}/specifications`,
    method: 'get'
  });
}

/**
 * 添加产品规格
 * @param {Number} productId - 产品ID
 * @param {Object} specData - 规格数据
 * @returns {Promise} - 返回Promise对象
 */
export function addProductSpecification(productId, specData) {
  return request({
    url: `/api/technical/products/${productId}/specifications`,
    method: 'post',
    data: specData
  });
}

/**
 * 更新产品规格
 * @param {Number} productId - 产品ID
 * @param {Number} specId - 规格ID
 * @param {Object} specData - 规格数据
 * @returns {Promise} - 返回Promise对象
 */
export function updateProductSpecification(productId, specId, specData) {
  return request({
    url: `/api/technical/products/${productId}/specifications/${specId}`,
    method: 'put',
    data: specData
  });
}

/**
 * 删除产品规格
 * @param {Number} productId - 产品ID
 * @param {Number} specId - 规格ID
 * @returns {Promise} - 返回Promise对象
 */
export function deleteProductSpecification(productId, specId) {
  return request({
    url: `/api/technical/products/${productId}/specifications/${specId}`,
    method: 'delete'
  });
}

/**
 * 获取产品成本历史
 * @param {Number} productId - 产品ID
 * @param {Object} params - 查询参数
 * @returns {Promise} - 返回Promise对象
 */
export function getProductCostHistory(productId, params) {
  return request({
    url: `/api/technical/products/${productId}/cost-history`,
    method: 'get',
    params
  });
}

/**
 * 上传产品图片
 * @param {Number} productId - 产品ID
 * @param {FormData} fileData - 图片文件数据
 * @returns {Promise} - 返回Promise对象
 */
export function uploadProductImage(productId, fileData) {
  return request({
    url: `/api/technical/products/${productId}/image`,
    method: 'post',
    data: fileData,
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  });
}

/**
 * 获取产品库存信息
 * @param {Number} productId - 产品ID
 * @returns {Promise} - 返回Promise对象
 */
export function getProductInventory(productId) {
  return request({
    url: `/api/technical/products/${productId}/inventory`,
    method: 'get'
  });
}

/**
 * 获取产品销售历史
 * @param {Number} productId - 产品ID
 * @param {Object} params - 查询参数
 * @returns {Promise} - 返回Promise对象
 */
export function getProductSalesHistory(productId, params) {
  return request({
    url: `/api/technical/products/${productId}/sales-history`,
    method: 'get',
    params
  });
}

/**
 * 获取产品文档列表
 * @param {Number} productId - 产品ID
 * @returns {Promise} - 返回Promise对象
 */
export function getProductDocuments(productId) {
  return request({
    url: `/api/technical/products/${productId}/documents`,
    method: 'get'
  });
}

/**
 * 上传产品文档
 * @param {Number} productId - 产品ID
 * @param {FormData} fileData - 文档文件数据
 * @returns {Promise} - 返回Promise对象
 */
export function uploadProductDocument(productId, fileData) {
  return request({
    url: `/api/technical/products/${productId}/documents`,
    method: 'post',
    data: fileData,
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  });
}

/**
 * 删除产品文档
 * @param {Number} productId - 产品ID
 * @param {Number} documentId - 文档ID
 * @returns {Promise} - 返回Promise对象
 */
export function deleteProductDocument(productId, documentId) {
  return request({
    url: `/api/technical/products/${productId}/documents/${documentId}`,
    method: 'delete'
  });
}

/**
 * 获取产品的替代品
 * @param {Number} productId - 产品ID
 * @returns {Promise} - 返回Promise对象
 */
export function getProductAlternatives(productId) {
  return request({
    url: `/api/technical/products/${productId}/alternatives`,
    method: 'get'
  });
}

/**
 * 添加产品替代品
 * @param {Number} productId - 产品ID
 * @param {Object} alternativeData - 替代品数据
 * @returns {Promise} - 返回Promise对象
 */
export function addProductAlternative(productId, alternativeData) {
  return request({
    url: `/api/technical/products/${productId}/alternatives`,
    method: 'post',
    data: alternativeData
  });
}

/**
 * 删除产品替代品
 * @param {Number} productId - 产品ID
 * @param {Number} alternativeId - 替代品ID
 * @returns {Promise} - 返回Promise对象
 */
export function deleteProductAlternative(productId, alternativeId) {
  return request({
    url: `/api/technical/products/${productId}/alternatives/${alternativeId}`,
    method: 'delete'
  });
}

/**
 * 导出产品数据
 * @param {Object} params - 查询参数
 * @returns {Promise} - 返回Promise对象
 */
export function exportProducts(params) {
  return request({
    url: '/api/technical/products/export',
    method: 'get',
    params,
    responseType: 'blob'
  });
}

/**
 * 导入产品数据
 * @param {FormData} fileData - 导入的文件数据
 * @returns {Promise} - 返回Promise对象
 */
export function importProducts(fileData) {
  return request({
    url: '/api/technical/products/import',
    method: 'post',
    data: fileData,
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  });
}

/**
 * 产品API钩子函数
 * @returns {Object} - 返回所有产品相关API方法的对象
 */
export function useProductApi() {
  return {
    getProducts,
    getProduct,
    createProduct,
    updateProduct,
    deleteProduct,
    searchProducts,
    getProductCategories,
    getProductSpecifications,
    addProductSpecification,
    updateProductSpecification,
    deleteProductSpecification,
    getProductCostHistory,
    uploadProductImage,
    getProductInventory,
    getProductSalesHistory,
    getProductDocuments,
    uploadProductDocument,
    deleteProductDocument,
    getProductAlternatives,
    addProductAlternative,
    deleteProductAlternative,
    exportProducts,
    importProducts
  };
} 