<template>
  <div class="payable-detail">
    <!-- 基本信息 -->
    <div class="detail-section">
      <h3 class="section-title">基本信息</h3>
      <el-row :gutter="20">
        <el-col :span="12">
          <div class="info-item">
            <label>单据号：</label>
            <span>{{ payable.bill_number }}</span>
          </div>
          <div class="info-item">
            <label>供应商：</label>
            <span>{{ payable.supplier_name }}</span>
          </div>
          <div class="info-item">
            <label>来源类型：</label>
            <el-tag :type="getSourceTypeColor(payable.source_type)" size="small">
              {{ getSourceTypeText(payable.source_type) }}
            </el-tag>
          </div>
          <div class="info-item">
            <label>来源单号：</label>
            <span>{{ payable.source_number || '-' }}</span>
          </div>
          <div class="info-item">
            <label>采购员：</label>
            <span>{{ payable.buyer || '-' }}</span>
          </div>
        </el-col>
        <el-col :span="12">
          <div class="info-item">
            <label>状态：</label>
            <el-tag :type="getStatusType(payable.status)" size="small">
              {{ getStatusText(payable.status) }}
            </el-tag>
          </div>
          <div class="info-item">
            <label>币种：</label>
            <span>{{ payable.currency || 'CNY' }}</span>
          </div>
          <div class="info-item">
            <label>税率：</label>
            <span>{{ payable.tax_rate }}%</span>
          </div>
          <div class="info-item">
            <label>创建时间：</label>
            <span>{{ payable.created_at }}</span>
          </div>
          <div class="info-item">
            <label>创建人：</label>
            <span>{{ payable.creator || '-' }}</span>
          </div>
        </el-col>
      </el-row>
    </div>

    <!-- 金额信息 -->
    <div class="detail-section">
      <h3 class="section-title">金额信息</h3>
      <el-row :gutter="20">
        <el-col :span="6">
          <div class="amount-card">
            <div class="amount-label">应付金额</div>
            <div class="amount-value total">¥{{ formatAmount(payable.total_amount) }}</div>
          </div>
        </el-col>
        <el-col :span="6">
          <div class="amount-card">
            <div class="amount-label">已付金额</div>
            <div class="amount-value paid">¥{{ formatAmount(payable.paid_amount) }}</div>
          </div>
        </el-col>
        <el-col :span="6">
          <div class="amount-card">
            <div class="amount-label">未付金额</div>
            <div class="amount-value pending">¥{{ formatAmount(payable.remaining_amount) }}</div>
          </div>
        </el-col>
        <el-col :span="6">
          <div class="amount-card">
            <div class="amount-label">付款进度</div>
            <div class="amount-value progress">{{ paidProgress }}%</div>
            <el-progress
              :percentage="paidProgress"
              :color="getProgressColor(paidProgress)"
              :stroke-width="6"
              style="margin-top: 8px;"
            />
          </div>
        </el-col>
      </el-row>
    </div>

    <!-- 日期信息 -->
    <div class="detail-section">
      <h3 class="section-title">日期信息</h3>
      <el-row :gutter="20">
        <el-col :span="8">
          <div class="info-item">
            <label>开票日期：</label>
            <span>{{ payable.bill_date }}</span>
          </div>
        </el-col>
        <el-col :span="8">
          <div class="info-item">
            <label>到期日期：</label>
            <span :class="getDueDateClass()">{{ payable.due_date }}</span>
          </div>
        </el-col>
        <el-col :span="8">
          <div class="info-item">
            <label>逾期天数：</label>
            <span v-if="payable.overdue_days > 0" class="overdue-days">
              {{ payable.overdue_days }}天
            </span>
            <span v-else>-</span>
          </div>
        </el-col>
      </el-row>
      
      <el-row :gutter="20">
        <el-col :span="8">
          <div class="info-item">
            <label>账期：</label>
            <span>{{ payable.payment_terms }}天</span>
          </div>
        </el-col>
        <el-col :span="8">
          <div class="info-item">
            <label>提醒天数：</label>
            <span>{{ payable.reminder_days }}天</span>
          </div>
        </el-col>
        <el-col :span="8">
          <div class="info-item">
            <label>最后付款：</label>
            <span>{{ payable.last_pay_date || '-' }}</span>
          </div>
        </el-col>
      </el-row>
    </div>

    <!-- 供应商信息 -->
    <div v-if="supplierInfo" class="detail-section">
      <h3 class="section-title">供应商信息</h3>
      <el-row :gutter="20">
        <el-col :span="12">
          <div class="info-item">
            <label>供应商名称：</label>
            <span>{{ supplierInfo.name }}</span>
          </div>
          <div class="info-item">
            <label>联系人：</label>
            <span>{{ supplierInfo.contact_person || '-' }}</span>
          </div>
          <div class="info-item">
            <label>联系电话：</label>
            <span>{{ supplierInfo.phone || '-' }}</span>
          </div>
          <div class="info-item">
            <label>邮箱：</label>
            <span>{{ supplierInfo.email || '-' }}</span>
          </div>
        </el-col>
        <el-col :span="12">
          <div class="info-item">
            <label>信用等级：</label>
            <el-rate
              :model-value="supplierInfo.credit_rating || 0"
              disabled
              show-score
              text-color="#ff9900"
            />
          </div>
          <div class="info-item">
            <label>付款条件：</label>
            <span>{{ supplierInfo.payment_terms || '-' }}</span>
          </div>
          <div class="info-item">
            <label>开户银行：</label>
            <span>{{ supplierInfo.bank_name || '-' }}</span>
          </div>
          <div class="info-item">
            <label>银行账号：</label>
            <span>{{ supplierInfo.bank_account || '-' }}</span>
          </div>
        </el-col>
      </el-row>
    </div>

    <!-- 付款记录 -->
    <div class="detail-section">
      <h3 class="section-title">付款记录</h3>
      <el-table :data="paymentRecords" border v-loading="recordsLoading">
        <el-table-column prop="pay_date" label="付款日期" width="120" />
        <el-table-column prop="pay_amount" label="付款金额" width="120" align="right">
          <template #default="{ row }">
            <span class="amount paid">¥{{ formatAmount(row.pay_amount) }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="payment_method" label="付款方式" width="120">
          <template #default="{ row }">
            <el-tag size="small">{{ getPaymentMethodText(row.payment_method) }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="account_name" label="付款账户" width="150" />
        <el-table-column prop="bank_reference" label="银行流水号" width="150" />
        <el-table-column prop="payer" label="付款人" width="100" />
        <el-table-column prop="notes" label="备注" show-overflow-tooltip />
        <el-table-column label="操作" width="100">
          <template #default="{ row }">
            <el-button size="small" @click="viewPaymentDetail(row)">
              详情
            </el-button>
          </template>
        </el-table-column>
      </el-table>
      
      <div v-if="paymentRecords.length === 0" class="empty-records">
        <el-empty description="暂无付款记录" />
      </div>
    </div>

    <!-- 核销记录 -->
    <div class="detail-section">
      <h3 class="section-title">核销记录</h3>
      <el-table :data="writeOffRecords" border v-loading="writeOffLoading">
        <el-table-column prop="write_off_date" label="核销日期" width="120" />
        <el-table-column prop="write_off_amount" label="核销金额" width="120" align="right">
          <template #default="{ row }">
            <span class="amount">¥{{ formatAmount(row.write_off_amount) }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="write_off_type" label="核销类型" width="120">
          <template #default="{ row }">
            <el-tag size="small">{{ getWriteOffTypeText(row.write_off_type) }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="target_bill_number" label="对方单据" width="150" />
        <el-table-column prop="operator" label="操作人" width="100" />
        <el-table-column prop="notes" label="备注" show-overflow-tooltip />
      </el-table>
      
      <div v-if="writeOffRecords.length === 0" class="empty-records">
        <el-empty description="暂无核销记录" />
      </div>
    </div>

    <!-- 操作历史 -->
    <div class="detail-section">
      <h3 class="section-title">操作历史</h3>
      <el-timeline>
        <el-timeline-item
          v-for="(history, index) in operationHistory"
          :key="index"
          :timestamp="history.created_at"
          :type="getHistoryType(history.action)"
        >
          <div class="history-content">
            <div class="history-action">
              <el-tag :type="getHistoryTagType(history.action)" size="small">
                {{ getHistoryActionText(history.action) }}
              </el-tag>
              <span class="history-operator">{{ history.operator }}</span>
            </div>
            <div v-if="history.description" class="history-description">
              {{ history.description }}
            </div>
            <div v-if="history.amount" class="history-amount">
              金额：¥{{ formatAmount(history.amount) }}
            </div>
          </div>
        </el-timeline-item>
      </el-timeline>
      
      <div v-if="operationHistory.length === 0" class="empty-records">
        <el-empty description="暂无操作记录" />
      </div>
    </div>

    <!-- 备注信息 -->
    <div v-if="payable.notes" class="detail-section">
      <h3 class="section-title">备注信息</h3>
      <div class="notes-content">
        {{ payable.notes }}
      </div>
    </div>

    <!-- 附件信息 -->
    <div v-if="attachments.length > 0" class="detail-section">
      <h3 class="section-title">附件</h3>
      <div class="attachments-list">
        <div
          v-for="(attachment, index) in attachments"
          :key="index"
          class="attachment-item"
        >
          <el-icon class="attachment-icon"><Document /></el-icon>
          <div class="attachment-info">
            <div class="attachment-name">{{ attachment.name }}</div>
            <div class="attachment-size">{{ formatFileSize(attachment.size) }}</div>
          </div>
          <div class="attachment-actions">
            <el-button size="small" @click="previewAttachment(attachment)">
              预览
            </el-button>
            <el-button size="small" @click="downloadAttachment(attachment)">
              下载
            </el-button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { api } from '@/utils/api'

// 定义属性
const props = defineProps({
  payable: {
    type: Object,
    required: true
  }
})

// 响应式数据
const supplierInfo = ref(null)
const paymentRecords = ref([])
const writeOffRecords = ref([])
const operationHistory = ref([])
const attachments = ref([])
const recordsLoading = ref(false)
const writeOffLoading = ref(false)

// 计算付款进度
const paidProgress = computed(() => {
  if (props.payable.total_amount <= 0) return 0
  return Math.round((props.payable.paid_amount / props.payable.total_amount) * 100)
})

// 格式化金额
const formatAmount = (amount) => {
  return Number(amount || 0).toLocaleString('zh-CN', {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2
  })
}

// 格式化文件大小
const formatFileSize = (size) => {
  if (size < 1024) return size + ' B'
  if (size < 1024 * 1024) return (size / 1024).toFixed(1) + ' KB'
  return (size / (1024 * 1024)).toFixed(1) + ' MB'
}

// 获取来源类型颜色
const getSourceTypeColor = (type) => {
  const colorMap = {
    'purchase_order': 'primary',
    'expense': 'success',
    'manual': 'warning'
  }
  return colorMap[type] || 'info'
}

// 获取来源类型文本
const getSourceTypeText = (type) => {
  const textMap = {
    'purchase_order': '采购订单',
    'expense': '费用报销',
    'manual': '手工录入'
  }
  return textMap[type] || '未知'
}

// 获取状态类型
const getStatusType = (status) => {
  const typeMap = {
    'pending': 'warning',
    'partial': 'primary',
    'paid': 'success',
    'overdue': 'danger'
  }
  return typeMap[status] || 'info'
}

// 获取状态文本
const getStatusText = (status) => {
  const textMap = {
    'pending': '待付款',
    'partial': '部分付款',
    'paid': '已付款',
    'overdue': '逾期'
  }
  return textMap[status] || '未知'
}

// 获取进度条颜色
const getProgressColor = (percentage) => {
  if (percentage >= 100) return '#67c23a'
  if (percentage >= 80) return '#5c6bc0'
  if (percentage >= 50) return '#e6a23c'
  return '#f56c6c'
}

// 获取到期日期样式
const getDueDateClass = () => {
  if (props.payable.status === 'paid') return ''
  
  const today = new Date()
  const due = new Date(props.payable.due_date)
  const diffDays = Math.ceil((due - today) / (1000 * 60 * 60 * 24))
  
  if (diffDays < 0) return 'overdue'
  if (diffDays <= 7) return 'near-due'
  return ''
}

// 获取付款方式文本
const getPaymentMethodText = (method) => {
  const methodMap = {
    'cash': '现金',
    'bank_transfer': '银行转账',
    'check': '支票',
    'credit_card': '信用卡',
    'alipay': '支付宝',
    'wechat_pay': '微信支付',
    'other': '其他'
  }
  return methodMap[method] || '未知'
}

// 获取核销类型文本
const getWriteOffTypeText = (type) => {
  const typeMap = {
    'payment': '付款核销',
    'advance': '预付核销',
    'refund': '退款核销'
  }
  return typeMap[type] || '未知'
}

// 获取历史类型
const getHistoryType = (action) => {
  const typeMap = {
    'create': 'primary',
    'pay': 'success',
    'write_off': 'warning',
    'remind': 'info'
  }
  return typeMap[action] || 'info'
}

// 获取历史标签类型
const getHistoryTagType = (action) => {
  const typeMap = {
    'create': 'primary',
    'pay': 'success',
    'write_off': 'warning',
    'remind': 'info'
  }
  return typeMap[action] || 'info'
}

// 获取历史操作文本
const getHistoryActionText = (action) => {
  const textMap = {
    'create': '创建',
    'pay': '付款',
    'write_off': '核销',
    'remind': '催付提醒',
    'edit': '编辑',
    'cancel': '取消'
  }
  return textMap[action] || '未知操作'
}

// 获取供应商信息
const fetchSupplierInfo = async () => {
  try {
    const response = await api.get(`/suppliers/${props.payable.supplier_id}`)
    supplierInfo.value = response.data
  } catch (error) {
    console.error('获取供应商信息失败:', error)
  }
}

// 获取付款记录
const fetchPaymentRecords = async () => {
  try {
    recordsLoading.value = true
    const response = await api.get(`/finance/payables/${props.payable.id}/payments`)
    paymentRecords.value = response.data.items || []
  } catch (error) {
    console.error('获取付款记录失败:', error)
  } finally {
    recordsLoading.value = false
  }
}

// 获取核销记录
const fetchWriteOffRecords = async () => {
  try {
    writeOffLoading.value = true
    const response = await api.get(`/finance/payables/${props.payable.id}/write-offs`)
    writeOffRecords.value = response.data.items || []
  } catch (error) {
    console.error('获取核销记录失败:', error)
  } finally {
    writeOffLoading.value = false
  }
}

// 获取操作历史
const fetchOperationHistory = async () => {
  try {
    const response = await api.get(`/finance/payables/${props.payable.id}/history`)
    operationHistory.value = response.data.items || []
  } catch (error) {
    console.error('获取操作历史失败:', error)
  }
}

// 获取附件列表
const fetchAttachments = async () => {
  try {
    const response = await api.get(`/finance/payables/${props.payable.id}/attachments`)
    attachments.value = response.data.items || []
  } catch (error) {
    console.error('获取附件列表失败:', error)
  }
}

// 查看付款详情
const viewPaymentDetail = (record) => {
  // 实现付款详情查看逻辑
  console.log('查看付款详情:', record)
}

// 预览附件
const previewAttachment = (attachment) => {
  window.open(attachment.url, '_blank')
}

// 下载附件
const downloadAttachment = (attachment) => {
  const link = document.createElement('a')
  link.href = attachment.url
  link.download = attachment.name
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
}

// 组件挂载
onMounted(() => {
  fetchSupplierInfo()
  fetchPaymentRecords()
  fetchWriteOffRecords()
  fetchOperationHistory()
  fetchAttachments()
})
</script>

<style scoped>
.payable-detail {
  padding: 20px;
}

.detail-section {
  margin-bottom: 32px;
  padding: 20px;
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.section-title {
  margin: 0 0 20px 0;
  font-size: 16px;
  font-weight: 600;
  color: #303133;
  border-bottom: 2px solid #5c6bc0;
  padding-bottom: 8px;
}

.info-item {
  margin-bottom: 12px;
  display: flex;
  align-items: center;
}

.info-item label {
  font-weight: 600;
  color: #606266;
  margin-right: 8px;
  min-width: 100px;
}

.amount-card {
  text-align: center;
  padding: 16px;
  background: #f8f9fa;
  border-radius: 8px;
  border: 1px solid #e9ecef;
}

.amount-label {
  font-size: 12px;
  color: #6c757d;
  margin-bottom: 8px;
}

.amount-value {
  font-size: 20px;
  font-weight: 600;
  line-height: 1;
  font-family: 'Courier New', monospace;
}

.amount-value.total {
  color: #5c6bc0;
}

.amount-value.paid {
  color: #67c23a;
}

.amount-value.pending {
  color: #e6a23c;
}

.amount-value.progress {
  color: #606266;
}

.amount {
  font-weight: 600;
  font-family: 'Courier New', monospace;
}

.amount.paid {
  color: #67c23a;
}

.overdue {
  color: #f56c6c;
  font-weight: 600;
}

.near-due {
  color: #e6a23c;
  font-weight: 600;
}

.overdue-days {
  color: #f56c6c;
  font-weight: 600;
}

.empty-records {
  padding: 40px 0;
}

.history-content {
  padding: 8px 0;
}

.history-action {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 4px;
}

.history-operator {
  font-size: 12px;
  color: #909399;
}

.history-description {
  font-size: 14px;
  color: #606266;
  margin-bottom: 4px;
}

.history-amount {
  font-size: 12px;
  color: #5c6bc0;
  font-weight: 600;
}

.notes-content {
  padding: 16px;
  background: #f8f9fa;
  border-radius: 6px;
  border-left: 4px solid #5c6bc0;
  line-height: 1.6;
  color: #606266;
}

.attachments-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.attachment-item {
  display: flex;
  align-items: center;
  padding: 12px;
  background: #f8f9fa;
  border-radius: 6px;
  border: 1px solid #e9ecef;
}

.attachment-icon {
  font-size: 24px;
  color: #5c6bc0;
  margin-right: 12px;
}

.attachment-info {
  flex: 1;
}

.attachment-name {
  font-weight: 600;
  color: #303133;
  margin-bottom: 4px;
}

.attachment-size {
  font-size: 12px;
  color: #909399;
}

.attachment-actions {
  display: flex;
  gap: 8px;
}

:deep(.el-table) {
  font-size: 14px;
}

:deep(.el-table th) {
  background-color: #fafafa;
}

:deep(.el-timeline-item__content) {
  padding-bottom: 16px;
}

@media (max-width: 768px) {
  .payable-detail {
    padding: 12px;
  }
  
  .detail-section {
    padding: 16px;
    margin-bottom: 20px;
  }
  
  .amount-card {
    margin-bottom: 12px;
  }
  
  .attachment-item {
    flex-direction: column;
    align-items: flex-start;
    gap: 8px;
  }
  
  .attachment-actions {
    width: 100%;
    justify-content: flex-end;
  }
}
</style>