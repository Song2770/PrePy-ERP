import request from '@/utils/request';

/**
 * 获取产品列表
 * @param {Object} params - 查询参数
 * @returns {Promise}
 */
export function getProducts(params) {
  return request({
    url: '/technical/products',
    method: 'get',
    params
  });
}

/**
 * 获取单个产品详情
 * @param {number} id - 产品ID
 * @returns {Promise}
 */
export function getProduct(id) {
  return request({
    url: `/technical/products/${id}`,
    method: 'get'
  });
}

/**
 * 创建新产品
 * @param {Object} productData - 产品数据
 * @returns {Promise}
 */
export function createProduct(productData) {
  return request({
    url: '/technical/products',
    method: 'post',
    data: productData
  });
}

/**
 * 更新产品
 * @param {number} id - 产品ID
 * @param {Object} productData - 更新的产品数据
 * @returns {Promise}
 */
export function updateProduct(id, productData) {
  return request({
    url: `/technical/products/${id}`,
    method: 'put',
    data: productData
  });
}

/**
 * 删除产品
 * @param {number} id - 产品ID
 * @returns {Promise}
 */
export function deleteProduct(id) {
  return request({
    url: `/technical/products/${id}`,
    method: 'delete'
  });
}

/**
 * 搜索产品
 * @param {Object} params - 搜索参数
 * @param {string} params.query - 搜索关键词
 * @returns {Promise} - 返回Promise对象
 */
export function searchProducts(params) {
  return request({
    url: '/technical/products/search',
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
 * @param {number} productId - 产品ID
 * @returns {Promise}
 */
export function getProductSpecifications(productId) {
  return request({
    url: `/technical/products/${productId}/specifications`,
    method: 'get'
  });
}

/**
 * 创建产品规格
 * @param {number} productId - 产品ID
 * @param {Object} specData - 规格数据
 * @returns {Promise}
 */
export function createProductSpecification(productId, specData) {
  return request({
    url: `/technical/products/${productId}/specifications`,
    method: 'post',
    data: specData
  });
}

/**
 * 更新产品规格
 * @param {number} productId - 产品ID
 * @param {number} specId - 规格ID
 * @param {Object} specData - 更新的规格数据
 * @returns {Promise}
 */
export function updateProductSpecification(productId, specId, specData) {
  return request({
    url: `/technical/products/${productId}/specifications/${specId}`,
    method: 'put',
    data: specData
  });
}

/**
 * 删除产品规格
 * @param {number} productId - 产品ID
 * @param {number} specId - 规格ID
 * @returns {Promise}
 */
export function deleteProductSpecification(productId, specId) {
  return request({
    url: `/technical/products/${productId}/specifications/${specId}`,
    method: 'delete'
  });
}

/**
 * 获取产品成本历史
 * @param {number} productId - 产品ID
 * @returns {Promise}
 */
export function getProductCostHistory(productId) {
  return request({
    url: `/technical/products/${productId}/cost-history`,
    method: 'get'
  });
}

/**
 * 上传产品图片
 * @param {number} productId - 产品ID
 * @param {File} imageFile - 图片文件
 * @returns {Promise}
 */
export function uploadProductImage(productId, imageFile) {
  const formData = new FormData();
  formData.append('image', imageFile);
  
  return request({
    url: `/technical/products/${productId}/image`,
    method: 'post',
    data: formData,
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  });
}

/**
 * 获取产品库存信息
 * @param {number} productId - 产品ID
 * @returns {Promise}
 */
export function getProductInventory(productId) {
  return request({
    url: `/technical/products/${productId}/inventory`,
    method: 'get'
  });
}

/**
 * 获取产品销售历史
 * @param {number} productId - 产品ID
 * @returns {Promise}
 */
export function getProductSalesHistory(productId) {
  return request({
    url: `/technical/products/${productId}/sales-history`,
    method: 'get'
  });
}

/**
 * 获取产品文档列表
 * @param {number} productId - 产品ID
 * @returns {Promise}
 */
export function getProductDocuments(productId) {
  return request({
    url: `/technical/products/${productId}/documents`,
    method: 'get'
  });
}

/**
 * 上传产品文档
 * @param {number} productId - 产品ID
 * @param {File} documentFile - 文档文件
 * @returns {Promise}
 */
export function uploadProductDocument(productId, documentFile) {
  const formData = new FormData();
  formData.append('document', documentFile);
  
  return request({
    url: `/technical/products/${productId}/documents`,
    method: 'post',
    data: formData,
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  });
}

/**
 * 删除产品文档
 * @param {number} productId - 产品ID
 * @param {number} documentId - 文档ID
 * @returns {Promise}
 */
export function deleteProductDocument(productId, documentId) {
  return request({
    url: `/technical/products/${productId}/documents/${documentId}`,
    method: 'delete'
  });
}

/**
 * 获取产品替代品列表
 * @param {number} productId - 产品ID
 * @returns {Promise}
 */
export function getProductAlternatives(productId) {
  return request({
    url: `/technical/products/${productId}/alternatives`,
    method: 'get'
  });
}

/**
 * 添加产品替代品
 * @param {number} productId - 产品ID
 * @param {Object} alternativeData - 替代品数据
 * @returns {Promise}
 */
export function addProductAlternative(productId, alternativeData) {
  return request({
    url: `/technical/products/${productId}/alternatives`,
    method: 'post',
    data: alternativeData
  });
}

/**
 * 更新产品替代品
 * @param {number} productId - 产品ID
 * @param {number} alternativeId - 替代品ID
 * @param {Object} alternativeData - 更新的替代品数据
 * @returns {Promise}
 */
export function updateProductAlternative(productId, alternativeId, alternativeData) {
  return request({
    url: `/technical/products/${productId}/alternatives/${alternativeId}`,
    method: 'put',
    data: alternativeData
  });
}

/**
 * 删除产品替代品
 * @param {number} productId - 产品ID
 * @param {number} alternativeId - 替代品ID
 * @returns {Promise}
 */
export function deleteProductAlternative(productId, alternativeId) {
  return request({
    url: `/technical/products/${productId}/alternatives/${alternativeId}`,
    method: 'delete'
  });
}

/**
 * 导出产品数据
 * @param {Object} params - 导出参数
 * @returns {Promise}
 */
export function exportProducts(params) {
  return request({
    url: '/technical/products/export',
    method: 'get',
    params,
    responseType: 'blob'
  });
}

/**
 * 导入产品数据
 * @param {File} file - 导入文件
 * @returns {Promise}
 */
export function importProducts(file) {
  const formData = new FormData();
  formData.append('file', file);
  
  return request({
    url: '/technical/products/import',
    method: 'post',
    data: formData,
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
    createProductSpecification,
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
    updateProductAlternative,
    deleteProductAlternative,
    exportProducts,
    importProducts
  };
} 