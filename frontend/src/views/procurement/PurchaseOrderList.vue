<template>
  <div class="page-container">
    <div class="page-header">
      <h1 class="page-title">采购订单</h1>
      <div class="page-actions">
        <el-button type="primary" @click="showCreateDialog = true">
          <el-icon><Plus /></el-icon>
          新建采购单
        </el-button>
      </div>
    </div>

    <!-- 搜索和筛选 -->
    <el-card class="search-card" shadow="never">
      <el-form :model="searchForm" inline>
        <el-form-item label="采购单号">
          <el-input
            v-model="searchForm.purchaseOrderNumber"
            placeholder="请输入采购单号"
            clearable
            style="width: 200px"
          />
        </el-form-item>
        
        <el-form-item label="供应商">
          <el-select
            v-model="searchForm.supplierId"
            placeholder="请选择供应商"
            clearable
            filterable
            style="width: 200px"
          >
            <el-option
              v-for="supplier in suppliers"
              :key="supplier.id"
              :label="supplier.name"
              :value="supplier.id"
            />
          </el-select>
        </el-form-item>
        
        <el-form-item label="状态">
          <el-select
            v-model="searchForm.status"
            placeholder="请选择状态"
            clearable
            style="width: 150px"
          >
            <el-option label="草稿" value="draft" />
            <el-option label="已发送" value="sent" />
            <el-option label="已确认" value="confirmed" />
            <el-option label="部分收货" value="partial_received" />
            <el-option label="已完成" value="completed" />
            <el-option label="已取消" value="cancelled" />
          </el-select>
        </el-form-item>
        
        <el-form-item label="采购日期">
          <el-date-picker
            v-model="searchForm.dateRange"
            type="daterange"
            range-separator="至"
            start-placeholder="开始日期"
            end-placeholder="结束日期"
            format="YYYY-MM-DD"
            value-format="YYYY-MM-DD"
            style="width: 240px"
          />
        </el-date-picker>
        
        <el-form-item>
          <el-button type="primary" @click="handleSearch">
            <el-icon><Search /></el-icon>
            搜索
          </el-button>
          <el-button @click="handleReset">
            <el-icon><Refresh /></el-icon>
            重置
          </el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <!-- 采购订单列表 -->
    <el-card shadow="never">
      <el-table
        v-loading="loading"
        :data="purchaseOrders"
        stripe
        @selection-change="handleSelectionChange"
      >
        <el-table-column type="selection" width="55" />
        
        <el-table-column prop="purchase_order_number" label="采购单号" width="150">
          <template #default="{ row }">
            <el-link type="primary" @click="viewPurchaseOrder(row.id)">
              {{ row.purchase_order_number }}
            </el-link>
          </template>
        </el-table-column>
        
        <el-table-column prop="supplier_name" label="供应商" width="150" />
        
        <el-table-column prop="order_date" label="采购日期" width="120">
          <template #default="{ row }">
            {{ formatDate(row.order_date) }}
          </template>
        </el-table-column>
        
        <el-table-column prop="expected_delivery_date" label="预计到货" width="120">
          <template #default="{ row }">
            <span :class="getDeliveryDateClass(row.expected_delivery_date, row.status)">
              {{ formatDate(row.expected_delivery_date) }}
            </span>
          </template>
        </el-table-column>
        
        <el-table-column prop="total_amount" label="采购金额" width="120" align="right">
          <template #default="{ row }">
            ¥{{ formatCurrency(row.total_amount) }}
          </template>
        </el-table-column>
        
        <el-table-column prop="status" label="状态" width="120">
          <template #default="{ row }">
            <el-tag :type="getStatusType(row.status)">
              {{ getStatusText(row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        
        <el-table-column label="收货进度" width="150">
          <template #default="{ row }">
            <div class="progress-container">
              <el-progress
                :percentage="getReceiveProgress(row)"
                :color="getProgressColor(row)"
                :stroke-width="6"
                :show-text="false"
              />
              <span class="progress-text">
                {{ row.received_quantity || 0 }} / {{ row.total_quantity || 0 }}
              </span>
            </div>
          </template>
        </el-table-column>
        
        <el-table-column prop="created_at" label="创建时间" width="160">
          <template #default="{ row }">
            {{ formatDateTime(row.created_at) }}
          </template>
        </el-table-column>
        
        <el-table-column label="操作" width="200" fixed="right">
          <template #default="{ row }">
            <el-button
              type="primary"
              size="small"
              @click="viewPurchaseOrder(row.id)"
            >
              查看
            </el-button>
            
            <el-button
              v-if="row.status === 'draft'"
              type="warning"
              size="small"
              @click="editPurchaseOrder(row.id)"
            >
              编辑
            </el-button>
            
            <el-dropdown
              @command="(command) => handleCommand(command, row)"
              trigger="click"
            >
              <el-button size="small">
                更多
                <el-icon><ArrowDown /></el-icon>
              </el-button>
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item
                    v-if="row.status === 'draft'"
                    command="send"
                  >
                    发送采购单
                  </el-dropdown-item>
                  <el-dropdown-item
                    v-if="row.status === 'sent'"
                    command="confirm"
                  >
                    确认采购单
                  </el-dropdown-item>
                  <el-dropdown-item
                    v-if="['confirmed', 'partial_received'].includes(row.status)"
                    command="receive"
                  >
                    收货登记
                  </el-dropdown-item>
                  <el-dropdown-item
                    v-if="row.status !== 'completed' && row.status !== 'cancelled'"
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
                </el-dropdown-menu>
              </template>
            </el-dropdown>
          </template>
        </el-table-column>
      </el-table>
      
      <!-- 分页 -->
      <div class="pagination-container">
        <el-pagination
          v-model:current-page="pagination.page"
          v-model:page-size="pagination.size"
          :total="pagination.total"
          :page-sizes="[10, 20, 50, 100]"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        />
      </div>
    </el-card>

    <!-- 新建采购单对话框 -->
    <el-dialog
      v-model="showCreateDialog"
      title="新建采购订单"
      width="900px"
      :before-close="handleCloseDialog"
    >
      <PurchaseOrderForm
        v-if="showCreateDialog"
        @success="handleCreateSuccess"
        @cancel="showCreateDialog = false"
      />
    </el-dialog>

    <!-- 收货登记对话框 -->
    <el-dialog
      v-model="showReceiveDialog"
      title="收货登记"
      width="800px"
    >
      <ReceiveForm
        v-if="showReceiveDialog"
        :purchase-order="selectedPurchaseOrder"
        @success="handleReceiveSuccess"
        @cancel="showReceiveDialog = false"
      />
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { api } from '@/utils/api'
import PurchaseOrderForm from './components/PurchaseOrderForm.vue'
import ReceiveForm from './components/ReceiveForm.vue'

const router = useRouter()

// 响应式数据
const loading = ref(false)
const purchaseOrders = ref([])
const suppliers = ref([])
const selectedPurchaseOrders = ref([])
const showCreateDialog = ref(false)
const showReceiveDialog = ref(false)
const selectedPurchaseOrder = ref(null)

// 搜索表单
const searchForm = reactive({
  purchaseOrderNumber: '',
  supplierId: null,
  status: '',
  dateRange: []
})

// 分页
const pagination = reactive({
  page: 1,
  size: 20,
  total: 0
})

// 状态映射
const statusMap = {
  draft: { text: '草稿', type: 'info' },
  sent: { text: '已发送', type: 'warning' },
  confirmed: { text: '已确认', type: 'success' },
  partial_received: { text: '部分收货', type: 'warning' },
  completed: { text: '已完成', type: 'success' },
  cancelled: { text: '已取消', type: 'danger' }
}

// 获取状态文本和类型
const getStatusText = (status) => statusMap[status]?.text || status
const getStatusType = (status) => statusMap[status]?.type || 'info'

// 获取收货进度
const getReceiveProgress = (row) => {
  if (!row.total_quantity || row.total_quantity === 0) return 0
  return Math.round((row.received_quantity / row.total_quantity) * 100)
}

// 获取进度条颜色
const getProgressColor = (row) => {
  const progress = getReceiveProgress(row)
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

// 获取采购订单列表
const fetchPurchaseOrders = async () => {
  try {
    loading.value = true
    const params = {
      page: pagination.page,
      size: pagination.size,
      ...searchForm
    }
    
    // 处理日期范围
    if (searchForm.dateRange && searchForm.dateRange.length === 2) {
      params.start_date = searchForm.dateRange[0]
      params.end_date = searchForm.dateRange[1]
    }
    delete params.dateRange
    
    const response = await api.get('/procurement/purchase-orders', { params })
    purchaseOrders.value = response.data.items || []
    pagination.total = response.data.total || 0
  } catch (error) {
    console.error('获取采购订单列表失败:', error)
    ElMessage.error('获取采购订单列表失败')
  } finally {
    loading.value = false
  }
}

// 获取供应商列表
const fetchSuppliers = async () => {
  try {
    const response = await api.get('/suppliers')
    suppliers.value = response.data.items || []
  } catch (error) {
    console.error('获取供应商列表失败:', error)
  }
}

// 搜索
const handleSearch = () => {
  pagination.page = 1
  fetchPurchaseOrders()
}

// 重置
const handleReset = () => {
  Object.assign(searchForm, {
    purchaseOrderNumber: '',
    supplierId: null,
    status: '',
    dateRange: []
  })
  pagination.page = 1
  fetchPurchaseOrders()
}

// 分页变化
const handleSizeChange = (size) => {
  pagination.size = size
  pagination.page = 1
  fetchPurchaseOrders()
}

const handleCurrentChange = (page) => {
  pagination.page = page
  fetchPurchaseOrders()
}

// 选择变化
const handleSelectionChange = (selection) => {
  selectedPurchaseOrders.value = selection
}

// 查看采购订单
const viewPurchaseOrder = (id) => {
  router.push(`/procurement/purchase-orders/${id}`)
}

// 编辑采购订单
const editPurchaseOrder = (id) => {
  router.push(`/procurement/purchase-orders/${id}/edit`)
}

// 处理下拉菜单命令
const handleCommand = async (command, row) => {
  switch (command) {
    case 'send':
      await sendPurchaseOrder(row)
      break
    case 'confirm':
      await confirmPurchaseOrder(row)
      break
    case 'receive':
      openReceiveDialog(row)
      break
    case 'cancel':
      await cancelPurchaseOrder(row)
      break
    case 'duplicate':
      await duplicatePurchaseOrder(row)
      break
    case 'export':
      await exportPurchaseOrder(row)
      break
  }
}

// 发送采购单
const sendPurchaseOrder = async (order) => {
  try {
    await ElMessageBox.confirm(
      `确定要发送采购单 ${order.purchase_order_number} 吗？`,
      '发送采购单',
      {
        confirmButtonText: '确认',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    
    await api.patch(`/procurement/purchase-orders/${order.id}/send`)
    ElMessage.success('采购单发送成功')
    fetchPurchaseOrders()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('发送采购单失败:', error)
      ElMessage.error('发送采购单失败')
    }
  }
}

// 确认采购单
const confirmPurchaseOrder = async (order) => {
  try {
    await ElMessageBox.confirm(
      `确定要确认采购单 ${order.purchase_order_number} 吗？`,
      '确认采购单',
      {
        confirmButtonText: '确认',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    
    await api.patch(`/procurement/purchase-orders/${order.id}/confirm`)
    ElMessage.success('采购单确认成功')
    fetchPurchaseOrders()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('确认采购单失败:', error)
      ElMessage.error('确认采购单失败')
    }
  }
}

// 打开收货对话框
const openReceiveDialog = (order) => {
  selectedPurchaseOrder.value = order
  showReceiveDialog.value = true
}

// 取消采购单
const cancelPurchaseOrder = async (order) => {
  try {
    await ElMessageBox.confirm(
      `确定要取消采购单 ${order.purchase_order_number} 吗？`,
      '取消采购单',
      {
        confirmButtonText: '确认',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    
    await api.patch(`/procurement/purchase-orders/${order.id}/cancel`)
    ElMessage.success('采购单取消成功')
    fetchPurchaseOrders()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('取消采购单失败:', error)
      ElMessage.error('取消采购单失败')
    }
  }
}

// 复制采购单
const duplicatePurchaseOrder = async (order) => {
  try {
    await api.post(`/procurement/purchase-orders/${order.id}/duplicate`)
    ElMessage.success('采购单复制成功')
    fetchPurchaseOrders()
  } catch (error) {
    console.error('复制采购单失败:', error)
    ElMessage.error('复制采购单失败')
  }
}

// 导出采购单
const exportPurchaseOrder = async (order) => {
  try {
    const response = await api.get(`/procurement/purchase-orders/${order.id}/export`, {
      responseType: 'blob'
    })
    
    const url = window.URL.createObjectURL(new Blob([response.data]))
    const link = document.createElement('a')
    link.href = url
    link.setAttribute('download', `采购单_${order.purchase_order_number}.pdf`)
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

// 关闭对话框
const handleCloseDialog = (done) => {
  ElMessageBox.confirm('确定要关闭吗？未保存的数据将丢失。')
    .then(() => {
      done()
    })
    .catch(() => {})
}

// 创建成功
const handleCreateSuccess = () => {
  showCreateDialog.value = false
  fetchPurchaseOrders()
  ElMessage.success('采购单创建成功')
}

// 收货成功
const handleReceiveSuccess = () => {
  showReceiveDialog.value = false
  fetchPurchaseOrders()
  ElMessage.success('收货登记成功')
}

// 组件挂载
onMounted(() => {
  fetchPurchaseOrders()
  fetchSuppliers()
})
</script>

<style scoped>
.search-card {
  margin-bottom: 16px;
}

.pagination-container {
  margin-top: 16px;
  text-align: right;
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

:deep(.el-form--inline .el-form-item) {
  margin-right: 16px;
  margin-bottom: 16px;
}

:deep(.el-progress-bar__outer) {
  border-radius: 4px;
}
</style>