import request from '@/utils/request';

/**
 * 获取文档列表
 * @param {Object} params - 查询参数（分页、过滤等）
 * @returns {Promise} - 返回Promise对象
 */
export function getDocuments(params) {
  return request({
    url: '/api/technical/documents',
    method: 'get',
    params
  });
}

/**
 * 获取单个文档详情
 * @param {Number} id - 文档ID
 * @returns {Promise} - 返回Promise对象
 */
export function getDocument(id) {
  return request({
    url: `/api/technical/documents/${id}`,
    method: 'get'
  });
}

/**
 * 创建新文档
 * @param {Object} documentData - 文档数据
 * @returns {Promise} - 返回Promise对象
 */
export function createDocument(documentData) {
  return request({
    url: '/api/technical/documents',
    method: 'post',
    data: documentData
  });
}

/**
 * 更新文档
 * @param {Number} id - 文档ID
 * @param {Object} documentData - 更新的文档数据
 * @returns {Promise} - 返回Promise对象
 */
export function updateDocument(id, documentData) {
  return request({
    url: `/api/technical/documents/${id}`,
    method: 'put',
    data: documentData
  });
}

/**
 * 删除文档
 * @param {Number} id - 文档ID
 * @returns {Promise} - 返回Promise对象
 */
export function deleteDocument(id) {
  return request({
    url: `/api/technical/documents/${id}`,
    method: 'delete'
  });
}

/**
 * 上传文档文件
 * @param {FormData} fileData - 文件数据
 * @returns {Promise} - 返回Promise对象
 */
export function uploadDocumentFile(fileData) {
  return request({
    url: '/api/technical/documents/upload',
    method: 'post',
    data: fileData,
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  });
}

/**
 * 下载文档文件
 * @param {Number} id - 文档ID
 * @returns {Promise} - 返回Promise对象
 */
export function downloadDocumentFile(id) {
  return request({
    url: `/api/technical/documents/${id}/download`,
    method: 'get',
    responseType: 'blob'
  });
}

/**
 * 预览文档
 * @param {Number} id - 文档ID
 * @returns {Promise} - 返回Promise对象
 */
export function previewDocument(id) {
  return request({
    url: `/api/technical/documents/${id}/preview`,
    method: 'get'
  });
}

/**
 * 搜索文档
 * @param {Object} params - 搜索参数
 * @returns {Promise} - 返回Promise对象
 */
export function searchDocuments(params) {
  return request({
    url: '/api/technical/documents/search',
    method: 'get',
    params
  });
}

/**
 * 获取文档分类列表
 * @returns {Promise} - 返回Promise对象
 */
export function getDocumentCategories() {
  return request({
    url: '/api/technical/document-categories',
    method: 'get'
  });
}

/**
 * 创建文档分类
 * @param {Object} categoryData - 分类数据
 * @returns {Promise} - 返回Promise对象
 */
export function createDocumentCategory(categoryData) {
  return request({
    url: '/api/technical/document-categories',
    method: 'post',
    data: categoryData
  });
}

/**
 * 更新文档分类
 * @param {Number} id - 分类ID
 * @param {Object} categoryData - 分类数据
 * @returns {Promise} - 返回Promise对象
 */
export function updateDocumentCategory(id, categoryData) {
  return request({
    url: `/api/technical/document-categories/${id}`,
    method: 'put',
    data: categoryData
  });
}

/**
 * 删除文档分类
 * @param {Number} id - 分类ID
 * @returns {Promise} - 返回Promise对象
 */
export function deleteDocumentCategory(id) {
  return request({
    url: `/api/technical/document-categories/${id}`,
    method: 'delete'
  });
}

/**
 * 获取文档版本历史
 * @param {Number} documentId - 文档ID
 * @returns {Promise} - 返回Promise对象
 */
export function getDocumentVersions(documentId) {
  return request({
    url: `/api/technical/documents/${documentId}/versions`,
    method: 'get'
  });
}

/**
 * 获取特定版本文档
 * @param {Number} documentId - 文档ID
 * @param {Number} versionId - 版本ID
 * @returns {Promise} - 返回Promise对象
 */
export function getDocumentVersion(documentId, versionId) {
  return request({
    url: `/api/technical/documents/${documentId}/versions/${versionId}`,
    method: 'get'
  });
}

/**
 * 创建文档版本
 * @param {Number} documentId - 文档ID
 * @param {FormData} versionData - 版本数据和文件
 * @returns {Promise} - 返回Promise对象
 */
export function createDocumentVersion(documentId, versionData) {
  return request({
    url: `/api/technical/documents/${documentId}/versions`,
    method: 'post',
    data: versionData,
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  });
}

/**
 * 获取文档相关联的产品列表
 * @param {Number} documentId - 文档ID
 * @param {Object} params - 查询参数（分页等）
 * @returns {Promise} - 返回Promise对象
 */
export function getDocumentRelatedProducts(documentId, params) {
  return request({
    url: `/api/technical/documents/${documentId}/related-products`,
    method: 'get',
    params
  });
}

/**
 * 关联文档到产品
 * @param {Number} documentId - 文档ID
 * @param {Object} relationData - 关联数据，包含产品ID
 * @returns {Promise} - 返回Promise对象
 */
export function linkDocumentToProduct(documentId, relationData) {
  return request({
    url: `/api/technical/documents/${documentId}/product-links`,
    method: 'post',
    data: relationData
  });
}

/**
 * 解除文档与产品的关联
 * @param {Number} documentId - 文档ID
 * @param {Number} productId - 产品ID
 * @returns {Promise} - 返回Promise对象
 */
export function unlinkDocumentFromProduct(documentId, productId) {
  return request({
    url: `/api/technical/documents/${documentId}/product-links/${productId}`,
    method: 'delete'
  });
}

/**
 * 分享文档（生成共享链接）
 * @param {Number} documentId - 文档ID
 * @param {Object} shareData - 分享设置
 * @returns {Promise} - 返回Promise对象
 */
export function shareDocument(documentId, shareData) {
  return request({
    url: `/api/technical/documents/${documentId}/share`,
    method: 'post',
    data: shareData
  });
}

/**
 * 获取文档审批流程
 * @param {Number} documentId - 文档ID
 * @returns {Promise} - 返回Promise对象
 */
export function getDocumentApprovalFlow(documentId) {
  return request({
    url: `/api/technical/documents/${documentId}/approval-flow`,
    method: 'get'
  });
}

/**
 * 提交文档审批
 * @param {Number} documentId - 文档ID
 * @param {Object} approvalData - 审批数据
 * @returns {Promise} - 返回Promise对象
 */
export function submitDocumentForApproval(documentId, approvalData) {
  return request({
    url: `/api/technical/documents/${documentId}/approval-flow`,
    method: 'post',
    data: approvalData
  });
}

/**
 * 审批文档
 * @param {Number} documentId - 文档ID
 * @param {Number} approvalId - 审批ID
 * @param {Object} approvalData - 审批结果数据
 * @returns {Promise} - 返回Promise对象
 */
export function approveDocument(documentId, approvalId, approvalData) {
  return request({
    url: `/api/technical/documents/${documentId}/approval-flow/${approvalId}`,
    method: 'put',
    data: approvalData
  });
}

/**
 * 导出文档数据
 * @param {Object} params - 导出参数
 * @returns {Promise} - 返回Promise对象
 */
export function exportDocuments(params) {
  return request({
    url: '/api/technical/documents/export',
    method: 'get',
    params,
    responseType: 'blob'
  });
}

/**
 * 文档API钩子函数
 * @returns {Object} - 返回所有文档相关API方法的对象
 */
export function useDocumentApi() {
  return {
    getDocuments,
    getDocument,
    createDocument,
    updateDocument,
    deleteDocument,
    uploadDocumentFile,
    downloadDocumentFile,
    previewDocument,
    searchDocuments,
    getDocumentCategories,
    createDocumentCategory,
    updateDocumentCategory,
    deleteDocumentCategory,
    getDocumentVersions,
    getDocumentVersion,
    createDocumentVersion,
    getDocumentRelatedProducts,
    linkDocumentToProduct,
    unlinkDocumentFromProduct,
    shareDocument,
    getDocumentApprovalFlow,
    submitDocumentForApproval,
    approveDocument,
    exportDocuments
  };
} 