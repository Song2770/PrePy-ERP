import dayjs from 'dayjs';

/**
 * 格式化日期
 * @param {string|Date} date 日期
 * @param {string} format 格式
 * @returns {string} 格式化后的日期字符串
 */
export function formatDate(date, format = 'YYYY-MM-DD') {
  if (!date) return '';
  return dayjs(date).format(format);
}

/**
 * 格式化金额
 * @param {number} amount 金额
 * @param {string} currency 币种
 * @returns {string} 格式化后的金额字符串
 */
export function formatCurrency(amount, currency = 'CNY') {
  if (amount === null || amount === undefined) return '0.00';
  return new Intl.NumberFormat('zh-CN', {
    style: 'currency',
    currency: currency
  }).format(amount);
}

/**
 * 格式化百分比
 * @param {number} value 数值
 * @param {number} decimals 小数位数
 * @returns {string} 格式化后的百分比字符串
 */
export function formatPercent(value, decimals = 2) {
  if (value === null || value === undefined) return '0.00%';
  return `${Number(value).toFixed(decimals)}%`;
}

/**
 * 格式化文件大小
 * @param {number} bytes 字节数
 * @returns {string} 格式化后的文件大小字符串
 */
export function formatFileSize(bytes) {
  if (bytes === null || bytes === undefined) return '0 B';
  const units = ['B', 'KB', 'MB', 'GB', 'TB'];
  let size = bytes;
  let unitIndex = 0;
  while (size >= 1024 && unitIndex < units.length - 1) {
    size /= 1024;
    unitIndex++;
  }
  return `${size.toFixed(2)} ${units[unitIndex]}`;
}

/**
 * 格式化手机号码
 * @param {string} phone 手机号码
 * @returns {string} 格式化后的手机号码字符串
 */
export function formatPhone(phone) {
  if (!phone) return '';
  return phone.replace(/(\d{3})(\d{4})(\d{4})/, '$1-$2-$3');
}

/**
 * 格式化身份证号码
 * @param {string} idCard 身份证号码
 * @returns {string} 格式化后的身份证号码字符串
 */
export function formatIdCard(idCard) {
  if (!idCard) return '';
  return idCard.replace(/(\d{6})(\d{4})(\d{4})(\d{4})/, '$1-$2-$3-$4');
}

/**
 * 格式化银行卡号码
 * @param {string} bankCard 银行卡号码
 * @returns {string} 格式化后的银行卡号码字符串
 */
export function formatBankCard(bankCard) {
  if (!bankCard) return '';
  return bankCard.replace(/(\d{4})(?=\d)/g, '$1 ');
} 