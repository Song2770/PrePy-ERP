<template>
  <div class="page-container">
    <div class="page-header">
      <div class="header-left">
        <el-button @click="$router.back()">
          <el-icon><ArrowLeft /></el-icon>
          返回
        </el-button>
        <h1 class="page-title">采购订单详情</h1>
      </div>
      <div class="page-actions">
        <el-button
          v-if="purchaseOrder.status === 'draft'"
          type="warning"
          @click="editPurchaseOrder"
        >
          <el-icon><Edit /></el-icon>
          编辑
        </el-button>
        
        <el-dropdown
          @command="handleCommand"
          trigger="click"
        >
          <el-button type="primary">
            操作
            <el-icon><ArrowDown /></el-icon>
          </el-button>
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item
                v-if="purchaseOrder.status === 'draft'"
                command="send"
              >
                发送采购单
              </el-dropdown-item>
              <el-dropdown-item
                v-if="purchaseOrder.status === 'sent'"
                command="confirm"
              >
                确认采购单
              </el-dropdown-item>
              <el-dropdown-item
                v-if="['confirmed', 'partial_received'].includes(purchaseOrder.status)"
                command="receive"
              >
                收货登记
              </el-dropdown-item>
              <el-dropdown-item
                v-if="purchaseOrder.status !== 'completed' && purchaseOrder.status !== 'cancelled'"
                command="cancel"
              >
                取消采购单
              </el-dropdown-item>
              <el-dropdown-item command="duplicate">
                复制采购单
              </el-dropdown-item>
              <el-dropdown-item command="export">
                导出采购单
              </el-dropdown-item>
              <el-dropdown-item command="print">
                打印采购单
              </el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>
      </div>
    </div>

    <div v-loading="loading" class="detail-content">
      <!-- 基本信息 -->
      <el-card class="info-card" shadow="never">
        <template #header>
          <div class="card-header">
            <span class="card-title">基本信息</span>
            <el-tag :type="getStatusType(purchaseOrder.status)" size="large">
              {{ getStatusText(purchaseOrder.status) }}
            </el-tag>
          </div>
        </template>
        
        <el-row :gutter="24">
          <el-col :span="8">
            <div class="info-item">
              <label>采购单号：</label>
              <span class="value">{{ purchaseOrder.purchase_order_number }}</span>
            </div>
          </el-col>
          <el-col :span="8">
            <div class="info-item">
              <label>供应商：</label>
              <span class="value">{{ purchaseOrder.supplier_name }}</span>
            </div>
          </el-col>
          <el-col :span="8">
            <div class="info-item">
              <label>采购日期：</label>
              <span class="value">{{ formatDate(purchaseOrder.order_date) }}</span>
            </div>
          </el-col>
        </el-row>
        
        <el-row :gutter="24">
          <el-col :span="8">
            <div class="info-item">
              <label>预计到货：</label>
              <span class="value" :class="getDeliveryDateClass(purchaseOrder.expected_delivery_date, purchaseOrder.status)">
                {{ formatDate(purchaseOrder.expected_delivery_date) }}
              </span>
            </div>
          </el-col>
          <el-col :span="8">
            <div class="info-item">
              <label>采购员：</label>
              <span class="value">{{ purchaseOrder.buyer_name || '-' }}</span>
            </div>
          </el-col>
          <el-col :span="8">
            <div class="info-item">
              <label>创建时间：</label>
              <span class="value">{{ formatDateTime(purchaseOrder.created_at) }}</span>
            </div>
          </el-col>
        </el-row>
        
        <el-row :gutter="24">
          <el-col :span="24">
            <div class="info-item">
              <label>备注：</label>
              <span class="value">{{ purchaseOrder.notes || '-' }}</span>
            </div>
          </el-col>
        </el-row>
      </el-card>

      <!-- 供应商信息 -->
      <el-card v-if="supplierInfo" class="info-card" shadow="never">
        <template #header>
          <span class="card-title">供应商信息</span>
        </template>
        
        <el-row :gutter="24">
          <el-col :span="8">
            <div class="info-item">
              <label>供应商编码：</label>
              <span class="value">{{ supplierInfo.code }}</span>
            </div>
          </el-col>
          <el-col :span="8">
            <div class="info-item">
              <label>联系人：</label>
              <span class="value">{{ supplierInfo.contact_person || '-' }}</span>
            </div>
          </el-col>
          <el-col :span="8">
            <div class="info-item">
              <label>联系电话：</label>
              <span class="value">{{ supplierInfo.phone || '-' }}</span>
            </div>
          </el-col>
        </el-row>
        
        <el-row :gutter="24">
          <el-col :span="8">
            <div class="info-item">
              <label>邮箱：</label>
              <span class="value">{{ supplierInfo.email || '-' }}</span>
            </div>
          </el-col>
          <el-col :span="16">
            <div class="info-item">
              <label>地址：</label>
              <span class="value">{{ supplierInfo.address || '-' }}</span>
            </div>
          </el-col>
        </el-row>
      </el-card>

      <!-- 采购明细 -->
      <el-card class="info-card" shadow="never">
        <template #header>
          <span class="card-title">采购明细</span>
        </template>
        
        <el-table :data="orderLines" border>
          <el-table-column label="序号" type="index" width="60" align="center" />
          
          <el-table-column label="商品" width="200">
            <template #default="{ row }">
              <div class="product-info">
                <div class="product-name">{{ row.product_name }}</div>
                <div class="product-code">{{ row.product_code }}</div>
              </div>
            </template>
          </el-table-column>
          
          <el-table-column prop="product_spec" label="规格" width="120" />
          <el-table-column prop="product_unit" label="单位" width="80" />
          
          <el-table-column prop="quantity" label="采购数量" width="100" align="right" />
          
          <el-table-column prop="unit_price" label="单价" width="100" align="right">
            <template #default="{ row }">
              ¥{{ formatCurrency(row.unit_price) }}
            </template>
          </el-table-column>
          
          <el-table-column label="金额" width="120" align="right">
            <template #default="{ row }">
              <span class="amount-text">
                ¥{{ formatCurrency(row.quantity * row.unit_price) }}
              </span>
            </template>
          </el-table-column>
          
          <el-table-column prop="received_quantity" label="已收数量" width="100" align="right">
            <template #default="{ row }">
              <span :class="{ 'text-success': row.received_quantity >= row.quantity }">
                {{ row.received_quantity || 0 }}
              </span>
            </template>
          </el-table-column>
          
          <el-table-column label="收货进度" width="120">
            <template #default="{ row }">
              <div class="progress-container">
                <el-progress
                  :percentage="getLineProgress(row)"
                  :color="getProgressColor(row)"
                  :stroke-width="6"
                  :show-text="false"
                />
                <span class="progress-text">
                  {{ getLineProgress(row) }}%
                </span>
              </div>
            </template>
          </el-table-column>
          
          <el-table-column prop="notes" label="备注" min-width="150" />
        </el-table>
        
        <!-- 汇总信息 -->
        <div class="summary-section">
          <el-row :gutter="24">
            <el-col :span="6">
              <div class="summary-item">
                <label>商品总数：</label>
                <span class="summary-value">{{ totalQuantity }}</span>
              </div>
            </el-col>
            <el-col :span="6">
              <div class="summary-item">
                <label>商品金额：</label>
                <span class="summary-value">¥{{ formatCurrency(subtotalAmount) }}</span>
              </div>
            </el-col>
            <el-col :span="6">
              <div class="summary-item">
                <label>运费：</label>
                <span class="summary-value">¥{{ formatCurrency(purchaseOrder.shipping_fee) }}</span>
              </div>
            </el-col>
            <el-col :span="6">
              <div class="summary-item">
                <label>总金额：</label>
                <span class="summary-value total-amount">¥{{ formatCurrency(totalAmount) }}</span>
              </div>
            </el-col>
          </el-row>
        </div>
      </el-card>

      <!-- 收货记录 -->
      <el-card v-if="receiveRecords.length > 0" class="info-card" shadow="never">
        <template #header>
          <span class="card-title">收货记录</span>
        </template>
        
        <el-table :data="receiveRecords" border>
          <el-table-column label="收货日期" width="120">
            <template #default="{ row }">
              {{ formatDate(row.receive_date) }}
            </template>
          </el-table-column>
          
          <el-table-column prop="receiver_name" label="收货人" width="100" />
          <el-table-column prop="warehouse_name" label="仓库" width="120" />
          
          <el-table-column label="收货数量" width="100" align="right">
            <template #default="{ row }">
              {{ row.total_receive_quantity }}
            </template>
          </el-table-column>
          
          <el-table-column label="收货金额" width="120" align="right">
            <template #default="{ row }">
              ¥{{ formatCurrency(row.total_receive_amount) }}
            </template>
          </el-table-column>
          
          <el-table-column prop="notes" label="备注" min-width="150" />
          
          <el-table-column label="操作" width="100">
            <template #default="{ row }">
              <el-button
                type="primary"
                size="small"
                @click="viewReceiveDetail(row.id)"
              >
                查看
              </el-button>
            </template>
          </el-table-column>
        </el-table>
      </el-card>

      <!-- 操作历史 -->
      <el-card class="info-card" shadow="never">
        <template #header>
          <span class="card-title">操作历史</span>
        </template>
        
        <el-timeline>
          <el-timeline-item
            v-for="(record, index) in operationHistory"
            :key="index"
            :timestamp="formatDateTime(record.created_at)"
            :type="getTimelineType(record.action)"
          >
            <div class="timeline-content">
              <div class="timeline-title">
                {{ getActionText(record.action) }}
              </div>
              <div class="timeline-user">
                操作人：{{ record.operator_name }}
              </div>
              <div v-if="record.notes" class="timeline-notes">
                备注：{{ record.notes }}
              </div>
            </div>
          </el-timeline-item>
        </el-timeline>
      </el-card>
    </div>

    <!-- 收货登记对话框 -->
    <el-dialog
      v-model="showReceiveDialog"
      title="收货登记"
      width="900px"
    >
      <ReceiveForm
        v-if="showReceiveDialog"
        :purchase-order="purchaseOrder"
        @success="handleReceiveSuccess"
        @cancel="showReceiveDialog = false"
      />
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { api } from '@/utils/api'
import ReceiveForm from './components/ReceiveForm.vue'

const route = useRoute()
const router = useRouter()

// 响应式数据
const loading = ref(false)
const purchaseOrder = ref({})
const supplierInfo = ref(null)
const orderLines = ref([])
const receiveRecords = ref([])
const operationHistory = ref([])
const showReceiveDialog = ref(false)

// 状态映射
const statusMap = {
  draft: { text: '草稿', type: 'info' },
  sent: { text: '已发送', type: 'warning' },
  confirmed: { text: '已确认', type: 'success' },
  partial_received: { text: '部分收货', type: 'warning' },
  completed: { text: '已完成', type: 'success' },
  cancelled: { text: '已取消', type: 'danger' }
}

// 操作映射
const actionMap = {
  create: '创建采购单',
  send: '发送采购单',
  confirm: '确认采购单',
  receive: '收货登记',
  cancel: '取消采购单',
  edit: '编辑采购单'
}

// 获取状态文本和类型
const getStatusText = (status) => statusMap[status]?.text || status
const getStatusType = (status) => statusMap[status]?.type || 'info'
const getActionText = (action) => actionMap[action] || action

// 获取时间线类型
const getTimelineType = (action) => {
  const typeMap = {
    create: 'primary',
    send: 'warning',
    confirm: 'success',
    receive: 'success',
    cancel: 'danger',
    edit: 'info'
  }
  return typeMap[action] || 'primary'
}

// 计算属性
const totalQuantity = computed(() => {
  return orderLines.value.reduce((sum, line) => sum + (line.quantity || 0), 0)
})

const subtotalAmount = computed(() => {
  return orderLines.value.reduce((sum, line) => {
    return sum + ((line.quantity || 0) * (line.unit_price || 0))
  }, 0)
})

const totalAmount = computed(() => {
  return subtotalAmount.value + (purchaseOrder.value.shipping_fee || 0)
})

// 获取行进度
const getLineProgress = (row) => {
  if (!row.quantity || row.quantity === 0) return 0
  return Math.round(((row.received_quantity || 0) / row.quantity) * 100)
}

// 获取进度条颜色
const getProgressColor = (row) => {
  const progress = getLineProgress(row)
  if (progress === 100) return '#67c23a'
  if (progress >= 80) return '#e6a23c'
  if (progress >= 50) return '#5c6bc0'
  return '#f56c6c'
}

// 获取交货日期样式
const getDeliveryDateClass = (date, status) => {
  if (!date || status === 'completed' || status === 'cancelled') return ''
  
  const today = new Date()
  const deliveryDate = new Date(date)
  const diffDays = Math.ceil((deliveryDate - today) / (1000 * 60 * 60 * 24))
  
  if (diffDays < 0) return 'overdue'
  if (diffDays <= 1) return 'urgent'
  if (diffDays <= 3) return 'warning'
  return ''
}

// 格式化日期
const formatDate = (date) => {
  if (!date) return '-'
  return new Date(date).toLocaleDateString('zh-CN')
}

// 格式化日期时间
const formatDateTime = (datetime) => {
  if (!datetime) return '-'
  return new Date(datetime).toLocaleString('zh-CN')
}

// 格式化货币
const formatCurrency = (amount) => {
  if (!amount) return '0.00'
  return Number(amount).toLocaleString('zh-CN', {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2
  })
}

// 获取采购单详情
const fetchPurchaseOrderDetail = async () => {
  try {
    loading.value = true
    const id = route.params.id
    
    // 获取采购单基本信息
    const response = await api.get(`/procurement/purchase-orders/${id}`)
    purchaseOrder.value = response.data
    
    // 获取供应商信息
    if (purchaseOrder.value.supplier_id) {
      const supplierResponse = await api.get(`/suppliers/${purchaseOrder.value.supplier_id}`)
      supplierInfo.value = supplierResponse.data
    }
    
    // 获取采购明细
    const linesResponse = await api.get(`/procurement/purchase-orders/${id}/lines`)
    orderLines.value = linesResponse.data
    
    // 获取收货记录
    const receivesResponse = await api.get(`/procurement/purchase-orders/${id}/receives`)
    receiveRecords.value = receivesResponse.data
    
    // 获取操作历史
    const historyResponse = await api.get(`/procurement/purchase-orders/${id}/history`)
    operationHistory.value = historyResponse.data
    
  } catch (error) {
    console.error('获取采购单详情失败:', error)
    ElMessage.error('获取采购单详情失败')
  } finally {
    loading.value = false
  }
}

// 编辑采购单
const editPurchaseOrder = () => {
  router.push(`/procurement/purchase-orders/${route.params.id}/edit`)
}

// 处理下拉菜单命令
const handleCommand = async (command) => {
  switch (command) {
    case 'send':
      await sendPurchaseOrder()
      break
    case 'confirm':
      await confirmPurchaseOrder()
      break
    case 'receive':
      openReceiveDialog()
      break
    case 'cancel':
      await cancelPurchaseOrder()
      break
    case 'duplicate':
      await duplicatePurchaseOrder()
      break
    case 'export':
      await exportPurchaseOrder()
      break
    case 'print':
      await printPurchaseOrder()
      break
  }
}

// 发送采购单
const sendPurchaseOrder = async () => {
  try {
    await ElMessageBox.confirm(
      `确定要发送采购单 ${purchaseOrder.value.purchase_order_number} 吗？`,
      '发送采购单',
      {
        confirmButtonText: '确认',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    
    await api.patch(`/procurement/purchase-orders/${route.params.id}/send`)
    ElMessage.success('采购单发送成功')
    fetchPurchaseOrderDetail()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('发送采购单失败:', error)
      ElMessage.error('发送采购单失败')
    }
  }
}

// 确认采购单
const confirmPurchaseOrder = async () => {
  try {
    await ElMessageBox.confirm(
      `确定要确认采购单 ${purchaseOrder.value.purchase_order_number} 吗？`,
      '确认采购单',
      {
        confirmButtonText: '确认',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    
    await api.patch(`/procurement/purchase-orders/${route.params.id}/confirm`)
    ElMessage.success('采购单确认成功')
    fetchPurchaseOrderDetail()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('确认采购单失败:', error)
      ElMessage.error('确认采购单失败')
    }
  }
}

// 打开收货对话框
const openReceiveDialog = () => {
  showReceiveDialog.value = true
}

// 取消采购单
const cancelPurchaseOrder = async () => {
  try {
    await ElMessageBox.confirm(
      `确定要取消采购单 ${purchaseOrder.value.purchase_order_number} 吗？`,
      '取消采购单',
      {
        confirmButtonText: '确认',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    
    await api.patch(`/procurement/purchase-orders/${route.params.id}/cancel`)
    ElMessage.success('采购单取消成功')
    fetchPurchaseOrderDetail()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('取消采购单失败:', error)
      ElMessage.error('取消采购单失败')
    }
  }
}

// 复制采购单
const duplicatePurchaseOrder = async () => {
  try {
    await api.post(`/procurement/purchase-orders/${route.params.id}/duplicate`)
    ElMessage.success('采购单复制成功')
    router.push('/procurement/purchase-orders')
  } catch (error) {
    console.error('复制采购单失败:', error)
    ElMessage.error('复制采购单失败')
  }
}

// 导出采购单
const exportPurchaseOrder = async () => {
  try {
    const response = await api.get(`/procurement/purchase-orders/${route.params.id}/export`, {
      responseType: 'blob'
    })
    
    const url = window.URL.createObjectURL(new Blob([response.data]))
    const link = document.createElement('a')
    link.href = url
    link.setAttribute('download', `采购单_${purchaseOrder.value.purchase_order_number}.pdf`)
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    window.URL.revokeObjectURL(url)
    
    ElMessage.success('采购单导出成功')
  } catch (error) {
    console.error('导出采购单失败:', error)
    ElMessage.error('导出采购单失败')
  }
}

// 打印采购单
const printPurchaseOrder = () => {
  window.print()
}

// 查看收货详情
const viewReceiveDetail = (receiveId) => {
  router.push(`/procurement/receives/${receiveId}`)
}

// 收货成功
const handleReceiveSuccess = () => {
  showReceiveDialog.value = false
  fetchPurchaseOrderDetail()
  ElMessage.success('收货登记成功')
}

// 组件挂载
onMounted(() => {
  fetchPurchaseOrderDetail()
})
</script>

<style scoped>
.header-left {
  display: flex;
  align-items: center;
  gap: 16px;
}

.detail-content {
  margin-top: 16px;
}

.info-card {
  margin-bottom: 16px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-title {
  font-size: 16px;
  font-weight: 600;
  color: #303133;
}

.info-item {
  margin-bottom: 16px;
  display: flex;
  align-items: center;
}

.info-item label {
  font-weight: 600;
  color: #606266;
  margin-right: 8px;
  min-width: 100px;
}

.info-item .value {
  color: #303133;
}

.product-info {
  line-height: 1.4;
}

.product-name {
  font-weight: 600;
  color: #303133;
}

.product-code {
  font-size: 12px;
  color: #909399;
}

.amount-text {
  font-weight: 600;
  color: #5c6bc0;
}

.text-success {
  color: #67c23a;
  font-weight: 600;
}

.progress-container {
  display: flex;
  align-items: center;
  gap: 8px;
}

.progress-text {
  font-size: 12px;
  color: #666;
  white-space: nowrap;
}

.summary-section {
  margin-top: 20px;
  padding-top: 20px;
  border-top: 1px solid #ebeef5;
}

.summary-item {
  display: flex;
  align-items: center;
  margin-bottom: 12px;
}

.summary-item label {
  font-weight: 600;
  color: #606266;
  margin-right: 8px;
  min-width: 80px;
}

.summary-value {
  font-weight: 600;
  color: #303133;
}

.total-amount {
  font-size: 18px;
  color: #f56c6c;
}

.timeline-content {
  padding-left: 16px;
}

.timeline-title {
  font-weight: 600;
  color: #303133;
  margin-bottom: 4px;
}

.timeline-user {
  font-size: 12px;
  color: #909399;
  margin-bottom: 4px;
}

.timeline-notes {
  font-size: 12px;
  color: #606266;
}

/* 日期样式 */
.overdue {
  color: #f56c6c;
  font-weight: 600;
}

.urgent {
  color: #e6a23c;
  font-weight: 600;
}

.warning {
  color: #f56c6c;
}

:deep(.el-table .el-table__cell) {
  padding: 8px 0;
}

:deep(.el-progress-bar__outer) {
  border-radius: 4px;
}

@media print {
  .page-header,
  .page-actions {
    display: none;
  }
  
  .detail-content {
    margin-top: 0;
  }
  
  .info-card {
    box-shadow: none;
    border: 1px solid #ddd;
  }
}
</style>