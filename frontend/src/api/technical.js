import apiClient from './auth';

// Product API
export const fetchProducts = async (params = {}) => {
  const response = await apiClient.get('/technical/products', { params });
  return response.data;
};

export const fetchProduct = async (id) => {
  const response = await apiClient.get(`/technical/products/${id}`);
  return response.data;
};

export const createProduct = async (productData) => {
  const response = await apiClient.post('/technical/products', productData);
  return response.data;
};

export const updateProduct = async (id, productData) => {
  const response = await apiClient.put(`/technical/products/${id}`, productData);
  return response.data;
};

export const deleteProduct = async (id) => {
  await apiClient.delete(`/technical/products/${id}`);
  return true;
};

// BOM API
export const fetchBOMs = async (params = {}) => {
  const response = await apiClient.get('/technical/boms', { params });
  return response.data;
};

export const fetchBOM = async (id) => {
  const response = await apiClient.get(`/technical/boms/${id}`);
  return response.data;
};

export const createBOM = async (bomData) => {
  const response = await apiClient.post('/technical/boms', bomData);
  return response.data;
};

export const updateBOM = async (id, bomData) => {
  const response = await apiClient.put(`/technical/boms/${id}`, bomData);
  return response.data;
};

export const deleteBOM = async (id) => {
  await apiClient.delete(`/technical/boms/${id}`);
  return true;
};

// BOM Items API
export const fetchBOMItems = async (bomId) => {
  const response = await apiClient.get(`/technical/boms/${bomId}/items`);
  return response.data;
};

export const addBOMItem = async (bomId, itemData) => {
  const response = await apiClient.post(`/technical/boms/${bomId}/items`, itemData);
  return response.data;
};

export const updateBOMItem = async (bomId, itemId, itemData) => {
  const response = await apiClient.put(`/technical/boms/${bomId}/items/${itemId}`, itemData);
  return response.data;
};

export const deleteBOMItem = async (bomId, itemId) => {
  await apiClient.delete(`/technical/boms/${bomId}/items/${itemId}`);
  return true;
};

// Workstation API
export const fetchWorkstations = async (params = {}) => {
  const response = await apiClient.get('/technical/workstations', { params });
  return response.data;
};

export const fetchWorkstation = async (id) => {
  const response = await apiClient.get(`/technical/workstations/${id}`);
  return response.data;
};

export const createWorkstation = async (workstationData) => {
  const response = await apiClient.post('/technical/workstations', workstationData);
  return response.data;
};

export const updateWorkstation = async (id, workstationData) => {
  const response = await apiClient.put(`/technical/workstations/${id}`, workstationData);
  return response.data;
};

export const deleteWorkstation = async (id) => {
  await apiClient.delete(`/technical/workstations/${id}`);
  return true;
};

// Production Route API
export const fetchRoutes = async (params = {}) => {
  const response = await apiClient.get('/technical/routes', { params });
  return response.data;
};

export const fetchRoute = async (id) => {
  const response = await apiClient.get(`/technical/routes/${id}`);
  return response.data;
};

export const createRoute = async (routeData) => {
  const response = await apiClient.post('/technical/routes', routeData);
  return response.data;
};

export const updateRoute = async (id, routeData) => {
  const response = await apiClient.put(`/technical/routes/${id}`, routeData);
  return response.data;
};

export const deleteRoute = async (id) => {
  await apiClient.delete(`/technical/routes/${id}`);
  return true;
};

// Technical Document API
export const fetchDocuments = async (params = {}) => {
  const response = await apiClient.get('/technical/documents', { params });
  return response.data;
};

export const fetchDocument = async (id) => {
  const response = await apiClient.get(`/technical/documents/${id}`);
  return response.data;
};

export const createDocument = async (documentData, file) => {
  const formData = new FormData();
  
  // Add document metadata
  Object.keys(documentData).forEach(key => {
    formData.append(key, documentData[key]);
  });
  
  // Add file if provided
  if (file) {
    formData.append('file', file);
  }
  
  const response = await apiClient.post('/technical/documents', formData, {
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  });
  
  return response.data;
};

export const updateDocument = async (id, documentData, file) => {
  const formData = new FormData();
  
  // Add document metadata
  Object.keys(documentData).forEach(key => {
    formData.append(key, documentData[key]);
  });
  
  // Add file if provided
  if (file) {
    formData.append('file', file);
  }
  
  const response = await apiClient.put(`/technical/documents/${id}`, formData, {
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  });
  
  return response.data;
};

export const deleteDocument = async (id) => {
  await apiClient.delete(`/technical/documents/${id}`);
  return true;
};

export const downloadDocument = async (id) => {
  const response = await apiClient.get(`/technical/documents/${id}/download`, {
    responseType: 'blob'
  });
  
  return response.data;
};

export default {
  // Products
  fetchProducts,
  fetchProduct,
  createProduct,
  updateProduct,
  deleteProduct,
  
  // BOMs
  fetchBOMs,
  fetchBOM,
  createBOM,
  updateBOM,
  deleteBOM,
  
  // BOM Items
  fetchBOMItems,
  addBOMItem,
  updateBOMItem,
  deleteBOMItem,
  
  // Workstations
  fetchWorkstations,
  fetchWorkstation,
  createWorkstation,
  updateWorkstation,
  deleteWorkstation,
  
  // Production Routes
  fetchRoutes,
  fetchRoute,
  createRoute,
  updateRoute,
  deleteRoute,
  
  // Technical Documents
  fetchDocuments,
  fetchDocument,
  createDocument,
  updateDocument,
  deleteDocument,
  downloadDocument
};