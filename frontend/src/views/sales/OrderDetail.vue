<template>
  <div class="page-container">
    <div class="page-header">
      <div class="header-left">
        <el-button @click="$router.go(-1)">
          <el-icon><ArrowLeft /></el-icon>
          返回
        </el-button>
        <h1 class="page-title">销售订单详情</h1>
      </div>
      
      <div class="page-actions">
        <el-button
          v-if="order.status === 'draft'"
          type="warning"
          @click="editOrder"
        >
          <el-icon><Edit /></el-icon>
          编辑
        </el-button>
        
        <el-button
          v-if="order.status === 'draft'"
          type="success"
          @click="confirmOrder"
        >
          <el-icon><Check /></el-icon>
          确认订单
        </el-button>
        
        <el-button
          v-if="order.status === 'confirmed'"
          type="danger"
          @click="cancelOrder"
        >
          <el-icon><Close /></el-icon>
          取消订单
        </el-button>
        
        <el-dropdown @command="handleCommand" trigger="click">
          <el-button>
            更多操作
            <el-icon><ArrowDown /></el-icon>
          </el-button>
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item command="duplicate">
                复制订单
              </el-dropdown-item>
              <el-dropdown-item command="export">
                导出PDF
              </el-dropdown-item>
              <el-dropdown-item command="print">
                打印订单
              </el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>
      </div>
    </div>

    <div v-loading="loading">
      <!-- 订单基本信息 -->
      <el-card class="info-card" shadow="never">
        <template #header>
          <div class="card-header">
            <span class="card-title">基本信息</span>
            <el-tag :type="getStatusType(order.status)" size="large">
              {{ getStatusText(order.status) }}
            </el-tag>
          </div>
        </template>
        
        <el-descriptions :column="3" border>
          <el-descriptions-item label="订单号">
            <span class="order-number">{{ order.order_number }}</span>
          </el-descriptions-item>
          
          <el-descriptions-item label="客户">
            <el-link type="primary" @click="viewCustomer(order.customer_id)">
              {{ order.customer_name }}
            </el-link>
          </el-descriptions-item>
          
          <el-descriptions-item label="销售员">
            {{ order.salesperson || '-' }}
          </el-descriptions-item>
          
          <el-descriptions-item label="订单日期">
            {{ formatDate(order.order_date) }}
          </el-descriptions-item>
          
          <el-descriptions-item label="交货日期">
            <span :class="getDeliveryDateClass(order.delivery_date)">
              {{ formatDate(order.delivery_date) }}
            </span>
          </el-descriptions-item>
          
          <el-descriptions-item label="订单金额">
            <span class="amount">¥{{ formatCurrency(order.total_amount) }}</span>
          </el-descriptions-item>
          
          <el-descriptions-item label="创建时间">
            {{ formatDateTime(order.created_at) }}
          </el-descriptions-item>
          
          <el-descriptions-item label="更新时间">
            {{ formatDateTime(order.updated_at) }}
          </el-descriptions-item>
          
          <el-descriptions-item label="创建人">
            {{ order.created_by || '-' }}
          </el-descriptions-item>
          
          <el-descriptions-item label="备注" :span="3">
            {{ order.notes || '-' }}
          </el-descriptions-item>
        </el-descriptions>
      </el-card>

      <!-- 订单明细 -->
      <el-card class="detail-card" shadow="never">
        <template #header>
          <span class="card-title">订单明细</span>
        </template>
        
        <el-table :data="order.order_lines" border>
          <el-table-column label="序号" type="index" width="60" />
          
          <el-table-column label="产品编码" prop="product_code" width="120" />
          
          <el-table-column label="产品名称" prop="product_name" min-width="150">
            <template #default="{ row }">
              <el-link type="primary" @click="viewProduct(row.product_id)">
                {{ row.product_name }}
              </el-link>
            </template>
          </el-table-column>
          
          <el-table-column label="规格" prop="product_specification" width="120" />
          
          <el-table-column label="数量" prop="quantity" width="100" align="right">
            <template #default="{ row }">
              {{ formatNumber(row.quantity) }}
            </template>
          </el-table-column>
          
          <el-table-column label="单位" prop="product_unit" width="80" />
          
          <el-table-column label="单价" prop="unit_price" width="120" align="right">
            <template #default="{ row }">
              ¥{{ formatCurrency(row.unit_price) }}
            </template>
          </el-table-column>
          
          <el-table-column label="金额" prop="total_price" width="120" align="right">
            <template #default="{ row }">
              ¥{{ formatCurrency(row.total_price) }}
            </template>
          </el-table-column>
          
          <el-table-column label="备注" prop="notes" min-width="150">
            <template #default="{ row }">
              {{ row.notes || '-' }}
            </template>
          </el-table-column>
        </el-table>
        
        <!-- 合计信息 -->
        <div class="summary-section">
          <el-row>
            <el-col :span="18">
              <div class="summary-label">订单总额：</div>
            </el-col>
            <el-col :span="6">
              <div class="summary-amount">¥{{ formatCurrency(order.total_amount) }}</div>
            </el-col>
          </el-row>
        </div>
      </el-card>

      <!-- 操作记录 -->
      <el-card class="history-card" shadow="never">
        <template #header>
          <span class="card-title">操作记录</span>
        </template>
        
        <el-timeline>
          <el-timeline-item
            v-for="(record, index) in operationHistory"
            :key="index"
            :timestamp="formatDateTime(record.created_at)"
            :type="getTimelineType(record.action)"
          >
            <div class="timeline-content">
              <div class="timeline-title">{{ record.action_text }}</div>
              <div class="timeline-user">操作人：{{ record.operator }}</div>
              <div v-if="record.notes" class="timeline-notes">{{ record.notes }}</div>
            </div>
          </el-timeline-item>
        </el-timeline>
      </el-card>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { api } from '@/utils/api'

const route = useRoute()
const router = useRouter()

// 响应式数据
const loading = ref(false)
const order = ref({
  order_lines: []
})
const operationHistory = ref([])

// 状态映射
const statusMap = {
  draft: { text: '草稿', type: 'info' },
  confirmed: { text: '已确认', type: 'success' },
  in_production: { text: '生产中', type: 'warning' },
  shipped: { text: '已发货', type: 'primary' },
  completed: { text: '已完成', type: 'success' },
  cancelled: { text: '已取消', type: 'danger' }
}

// 时间线类型映射
const timelineTypeMap = {
  create: 'primary',
  confirm: 'success',
  cancel: 'danger',
  update: 'warning',
  complete: 'success'
}

// 获取状态文本
const getStatusText = (status) => statusMap[status]?.text || status

// 获取状态类型
const getStatusType = (status) => statusMap[status]?.type || 'info'

// 获取时间线类型
const getTimelineType = (action) => timelineTypeMap[action] || 'primary'

// 获取交货日期样式
const getDeliveryDateClass = (deliveryDate) => {
  if (!deliveryDate) return ''
  
  const today = new Date()
  const delivery = new Date(deliveryDate)
  const diffDays = Math.ceil((delivery - today) / (1000 * 60 * 60 * 24))
  
  if (diffDays < 0) return 'overdue'
  if (diffDays <= 3) return 'urgent'
  if (diffDays <= 7) return 'warning'
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

// 格式化数字
const formatNumber = (number) => {
  if (!number) return '0'
  return Number(number).toLocaleString('zh-CN')
}

// 获取订单详情
const fetchOrderDetail = async () => {
  try {
    loading.value = true
    const orderId = route.params.id
    const response = await api.get(`/sales/orders/${orderId}`)
    order.value = response.data
  } catch (error) {
    console.error('获取订单详情失败:', error)
    ElMessage.error('获取订单详情失败')
  } finally {
    loading.value = false
  }
}

// 获取操作记录
const fetchOperationHistory = async () => {
  try {
    const orderId = route.params.id
    const response = await api.get(`/sales/orders/${orderId}/history`)
    operationHistory.value = response.data || []
  } catch (error) {
    console.error('获取操作记录失败:', error)
  }
}

// 编辑订单
const editOrder = () => {
  router.push(`/sales/orders/${order.value.id}/edit`)
}

// 确认订单
const confirmOrder = async () => {
  try {
    await ElMessageBox.confirm(
      `确定要确认订单 ${order.value.order_number} 吗？`,
      '确认操作',
      {
        confirmButtonText: '确认',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    
    await api.patch(`/sales/orders/${order.value.id}/confirm`)
    ElMessage.success('订单确认成功')
    fetchOrderDetail()
    fetchOperationHistory()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('确认订单失败:', error)
      ElMessage.error('确认订单失败')
    }
  }
}

// 取消订单
const cancelOrder = async () => {
  try {
    await ElMessageBox.confirm(
      `确定要取消订单 ${order.value.order_number} 吗？`,
      '取消订单',
      {
        confirmButtonText: '确认',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    
    await api.patch(`/sales/orders/${order.value.id}/cancel`)
    ElMessage.success('订单取消成功')
    fetchOrderDetail()
    fetchOperationHistory()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('取消订单失败:', error)
      ElMessage.error('取消订单失败')
    }
  }
}

// 处理下拉菜单命令
const handleCommand = async (command) => {
  switch (command) {
    case 'duplicate':
      await duplicateOrder()
      break
    case 'export':
      await exportOrder()
      break
    case 'print':
      printOrder()
      break
  }
}

// 复制订单
const duplicateOrder = async () => {
  try {
    await api.post(`/sales/orders/${order.value.id}/duplicate`)
    ElMessage.success('订单复制成功')
    router.push('/sales/orders')
  } catch (error) {
    console.error('复制订单失败:', error)
    ElMessage.error('复制订单失败')
  }
}

// 导出订单
const exportOrder = async () => {
  try {
    const response = await api.get(`/sales/orders/${order.value.id}/export`, {
      responseType: 'blob'
    })
    
    const url = window.URL.createObjectURL(new Blob([response.data]))
    const link = document.createElement('a')
    link.href = url
    link.setAttribute('download', `订单_${order.value.order_number}.pdf`)
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    window.URL.revokeObjectURL(url)
    
    ElMessage.success('订单导出成功')
  } catch (error) {
    console.error('导出订单失败:', error)
    ElMessage.error('导出订单失败')
  }
}

// 打印订单
const printOrder = () => {
  window.print()
}

// 查看客户
const viewCustomer = (customerId) => {
  router.push(`/master-data/customers/${customerId}`)
}

// 查看产品
const viewProduct = (productId) => {
  router.push(`/master-data/products/${productId}`)
}

// 组件挂载
onMounted(() => {
  fetchOrderDetail()
  fetchOperationHistory()
})
</script>

<style scoped>
.header-left {
  display: flex;
  align-items: center;
  gap: 12px;
}

.info-card,
.detail-card,
.history-card {
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
  color: #262626;
}

.order-number {
  font-family: 'Courier New', monospace;
  font-weight: 600;
  color: #5c6bc0;
}

.amount {
  font-size: 16px;
  font-weight: 600;
  color: #f56c6c;
}

.summary-section {
  margin-top: 16px;
  padding: 16px;
  background-color: #f0f9ff;
  border-radius: 6px;
  border: 1px solid #e1f5fe;
}

.summary-label {
  font-size: 16px;
  font-weight: 600;
  color: #262626;
  text-align: right;
}

.summary-amount {
  font-size: 18px;
  font-weight: 700;
  color: #f56c6c;
  text-align: right;
}

.timeline-content {
  padding-left: 8px;
}

.timeline-title {
  font-weight: 600;
  color: #262626;
  margin-bottom: 4px;
}

.timeline-user {
  font-size: 12px;
  color: #666;
  margin-bottom: 2px;
}

.timeline-notes {
  font-size: 12px;
  color: #999;
}

/* 交货日期样式 */
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

:deep(.el-descriptions__label) {
  font-weight: 600;
}

:deep(.el-table .el-table__cell) {
  padding: 8px 0;
}

/* 打印样式 */
@media print {
  .page-header,
  .el-card__header {
    display: none !important;
  }
  
  .page-container {
    padding: 0 !important;
  }
  
  .el-card {
    box-shadow: none !important;
    border: none !important;
  }
}
</style>