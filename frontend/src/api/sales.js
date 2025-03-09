import apiClient from './auth';

// Customer API
export const fetchCustomers = async (params = {}) => {
  const response = await apiClient.get('/sales/customers', { params });
  return response.data;
};

export const fetchCustomer = async (id) => {
  const response = await apiClient.get(`/sales/customers/${id}`);
  return response.data;
};

export const createCustomer = async (customerData) => {
  const response = await apiClient.post('/sales/customers', customerData);
  return response.data;
};

export const updateCustomer = async (id, customerData) => {
  const response = await apiClient.put(`/sales/customers/${id}`, customerData);
  return response.data;
};

export const deleteCustomer = async (id) => {
  await apiClient.delete(`/sales/customers/${id}`);
  return true;
};

// Customer Contacts API
export const fetchCustomerContacts = async (customerId) => {
  const response = await apiClient.get(`/sales/customers/${customerId}/contacts`);
  return response.data;
};

export const createCustomerContact = async (contactData) => {
  const response = await apiClient.post('/sales/contacts', contactData);
  return response.data;
};

export const updateCustomerContact = async (id, contactData) => {
  const response = await apiClient.put(`/sales/contacts/${id}`, contactData);
  return response.data;
};

export const deleteCustomerContact = async (id) => {
  await apiClient.delete(`/sales/contacts/${id}`);
  return true;
};

// Quotation API
export const fetchQuotations = async (params = {}) => {
  const response = await apiClient.get('/sales/quotations', { params });
  return response.data;
};

export const fetchQuotation = async (id) => {
  const response = await apiClient.get(`/sales/quotations/${id}`);
  return response.data;
};

export const createQuotation = async (quotationData) => {
  const response = await apiClient.post('/sales/quotations', quotationData);
  return response.data;
};

export const updateQuotation = async (id, quotationData) => {
  const response = await apiClient.put(`/sales/quotations/${id}`, quotationData);
  return response.data;
};

export const deleteQuotation = async (id) => {
  await apiClient.delete(`/sales/quotations/${id}`);
  return true;
};

export const convertQuotationToOrder = async (id, orderData) => {
  const response = await apiClient.post(`/sales/quotations/${id}/convert`, orderData);
  return response.data;
};

// Sales Order API
export const fetchOrders = async (params = {}) => {
  const response = await apiClient.get('/sales/orders', { params });
  return response.data;
};

export const fetchOrder = async (id) => {
  const response = await apiClient.get(`/sales/orders/${id}`);
  return response.data;
};

export const createOrder = async (orderData) => {
  const response = await apiClient.post('/sales/orders', orderData);
  return response.data;
};

export const updateOrder = async (id, orderData) => {
  const response = await apiClient.put(`/sales/orders/${id}`, orderData);
  return response.data;
};

export const deleteOrder = async (id) => {
  await apiClient.delete(`/sales/orders/${id}`);
  return true;
};

// Invoice API
export const fetchInvoices = async (params = {}) => {
  const response = await apiClient.get('/sales/invoices', { params });
  return response.data;
};

export const fetchInvoice = async (id) => {
  const response = await apiClient.get(`/sales/invoices/${id}`);
  return response.data;
};

export const createInvoice = async (invoiceData) => {
  const response = await apiClient.post('/sales/invoices', invoiceData);
  return response.data;
};

export const updateInvoice = async (id, invoiceData) => {
  const response = await apiClient.put(`/sales/invoices/${id}`, invoiceData);
  return response.data;
};

export const deleteInvoice = async (id) => {
  await apiClient.delete(`/sales/invoices/${id}`);
  return true;
};

// Delivery API
export const fetchDeliveries = async (params = {}) => {
  const response = await apiClient.get('/sales/deliveries', { params });
  return response.data;
};

export const fetchDelivery = async (id) => {
  const response = await apiClient.get(`/sales/deliveries/${id}`);
  return response.data;
};

export const createDelivery = async (deliveryData) => {
  const response = await apiClient.post('/sales/deliveries', deliveryData);
  return response.data;
};

export const updateDelivery = async (id, deliveryData) => {
  const response = await apiClient.put(`/sales/deliveries/${id}`, deliveryData);
  return response.data;
};

export const deleteDelivery = async (id) => {
  await apiClient.delete(`/sales/deliveries/${id}`);
  return true;
};

export default {
  // Customers
  fetchCustomers,
  fetchCustomer,
  createCustomer,
  updateCustomer,
  deleteCustomer,
  
  // Customer Contacts
  fetchCustomerContacts,
  createCustomerContact,
  updateCustomerContact,
  deleteCustomerContact,
  
  // Quotations
  fetchQuotations,
  fetchQuotation,
  createQuotation,
  updateQuotation,
  deleteQuotation,
  convertQuotationToOrder,
  
  // Orders
  fetchOrders,
  fetchOrder,
  createOrder,
  updateOrder,
  deleteOrder,
  
  // Invoices
  fetchInvoices,
  fetchInvoice,
  createInvoice,
  updateInvoice,
  deleteInvoice,
  
  // Deliveries
  fetchDeliveries,
  fetchDelivery,
  createDelivery,
  updateDelivery,
  deleteDelivery
}; 