<template>
  <div class="page-container">
    <div class="page-header">
      <h1 class="page-title">销售订单</h1>
      <div class="page-actions">
        <el-button type="primary" @click="showCreateDialog = true">
          <el-icon><Plus /></el-icon>
          新建订单
        </el-button>
      </div>
    </div>

    <!-- 搜索和筛选 -->
    <el-card class="search-card" shadow="never">
      <el-form :model="searchForm" inline>
        <el-form-item label="订单号">
          <el-input
            v-model="searchForm.orderNumber"
            placeholder="请输入订单号"
            clearable
            style="width: 200px"
          />
        </el-form-item>
        
        <el-form-item label="客户">
          <el-select
            v-model="searchForm.customerId"
            placeholder="请选择客户"
            clearable
            filterable
            style="width: 200px"
          >
            <el-option
              v-for="customer in customers"
              :key="customer.id"
              :label="customer.name"
              :value="customer.id"
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
            <el-option label="已确认" value="confirmed" />
            <el-option label="生产中" value="in_production" />
            <el-option label="已发货" value="shipped" />
            <el-option label="已完成" value="completed" />
            <el-option label="已取消" value="cancelled" />
          </el-select>
        </el-form-item>
        
        <el-form-item label="订单日期">
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

    <!-- 订单列表 -->
    <el-card shadow="never">
      <el-table
        v-loading="loading"
        :data="orders"
        stripe
        @selection-change="handleSelectionChange"
      >
        <el-table-column type="selection" width="55" />
        
        <el-table-column prop="order_number" label="订单号" width="150">
          <template #default="{ row }">
            <el-link type="primary" @click="viewOrder(row.id)">
              {{ row.order_number }}
            </el-link>
          </template>
        </el-table-column>
        
        <el-table-column prop="customer_name" label="客户" width="150" />
        
        <el-table-column prop="order_date" label="订单日期" width="120">
          <template #default="{ row }">
            {{ formatDate(row.order_date) }}
          </template>
        </el-table-column>
        
        <el-table-column prop="delivery_date" label="交货日期" width="120">
          <template #default="{ row }">
            {{ formatDate(row.delivery_date) }}
          </template>
        </el-table-column>
        
        <el-table-column prop="total_amount" label="订单金额" width="120" align="right">
          <template #default="{ row }">
            ¥{{ formatCurrency(row.total_amount) }}
          </template>
        </el-table-column>
        
        <el-table-column prop="status" label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="getStatusType(row.status)">
              {{ getStatusText(row.status) }}
            </el-tag>
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
              @click="viewOrder(row.id)"
            >
              查看
            </el-button>
            
            <el-button
              v-if="row.status === 'draft'"
              type="warning"
              size="small"
              @click="editOrder(row.id)"
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
                    command="confirm"
                  >
                    确认订单
                  </el-dropdown-item>
                  <el-dropdown-item
                    v-if="row.status === 'confirmed'"
                    command="cancel"
                  >
                    取消订单
                  </el-dropdown-item>
                  <el-dropdown-item command="duplicate">
                    复制订单
                  </el-dropdown-item>
                  <el-dropdown-item command="export">
                    导出订单
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

    <!-- 新建订单对话框 -->
    <el-dialog
      v-model="showCreateDialog"
      title="新建销售订单"
      width="800px"
      :before-close="handleCloseDialog"
    >
      <OrderForm
        v-if="showCreateDialog"
        @success="handleCreateSuccess"
        @cancel="showCreateDialog = false"
      />
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { api } from '@/utils/api'
import OrderForm from './components/OrderForm.vue'

const router = useRouter()

// 响应式数据
const loading = ref(false)
const orders = ref([])
const customers = ref([])
const selectedOrders = ref([])
const showCreateDialog = ref(false)

// 搜索表单
const searchForm = reactive({
  orderNumber: '',
  customerId: null,
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
  confirmed: { text: '已确认', type: 'success' },
  in_production: { text: '生产中', type: 'warning' },
  shipped: { text: '已发货', type: 'primary' },
  completed: { text: '已完成', type: 'success' },
  cancelled: { text: '已取消', type: 'danger' }
}

// 计算属性
const getStatusText = (status) => statusMap[status]?.text || status
const getStatusType = (status) => statusMap[status]?.type || 'info'

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

// 获取订单列表
const fetchOrders = async () => {
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
    
    const response = await api.get('/sales/orders', { params })
    orders.value = response.data.items || []
    pagination.total = response.data.total || 0
  } catch (error) {
    console.error('获取订单列表失败:', error)
    ElMessage.error('获取订单列表失败')
  } finally {
    loading.value = false
  }
}

// 获取客户列表
const fetchCustomers = async () => {
  try {
    const response = await api.get('/customers')
    customers.value = response.data.items || []
  } catch (error) {
    console.error('获取客户列表失败:', error)
  }
}

// 搜索
const handleSearch = () => {
  pagination.page = 1
  fetchOrders()
}

// 重置
const handleReset = () => {
  Object.assign(searchForm, {
    orderNumber: '',
    customerId: null,
    status: '',
    dateRange: []
  })
  pagination.page = 1
  fetchOrders()
}

// 分页变化
const handleSizeChange = (size) => {
  pagination.size = size
  pagination.page = 1
  fetchOrders()
}

const handleCurrentChange = (page) => {
  pagination.page = page
  fetchOrders()
}

// 选择变化
const handleSelectionChange = (selection) => {
  selectedOrders.value = selection
}

// 查看订单
const viewOrder = (id) => {
  router.push(`/sales/orders/${id}`)
}

// 编辑订单
const editOrder = (id) => {
  router.push(`/sales/orders/${id}/edit`)
}

// 处理下拉菜单命令
const handleCommand = async (command, row) => {
  switch (command) {
    case 'confirm':
      await confirmOrder(row)
      break
    case 'cancel':
      await cancelOrder(row)
      break
    case 'duplicate':
      await duplicateOrder(row)
      break
    case 'export':
      await exportOrder(row)
      break
  }
}

// 确认订单
const confirmOrder = async (order) => {
  try {
    await ElMessageBox.confirm(
      `确定要确认订单 ${order.order_number} 吗？`,
      '确认操作',
      {
        confirmButtonText: '确认',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    
    await api.patch(`/sales/orders/${order.id}/confirm`)
    ElMessage.success('订单确认成功')
    fetchOrders()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('确认订单失败:', error)
      ElMessage.error('确认订单失败')
    }
  }
}

// 取消订单
const cancelOrder = async (order) => {
  try {
    await ElMessageBox.confirm(
      `确定要取消订单 ${order.order_number} 吗？`,
      '取消订单',
      {
        confirmButtonText: '确认',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    
    await api.patch(`/sales/orders/${order.id}/cancel`)
    ElMessage.success('订单取消成功')
    fetchOrders()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('取消订单失败:', error)
      ElMessage.error('取消订单失败')
    }
  }
}

// 复制订单
const duplicateOrder = async (order) => {
  try {
    await api.post(`/sales/orders/${order.id}/duplicate`)
    ElMessage.success('订单复制成功')
    fetchOrders()
  } catch (error) {
    console.error('复制订单失败:', error)
    ElMessage.error('复制订单失败')
  }
}

// 导出订单
const exportOrder = async (order) => {
  try {
    const response = await api.get(`/sales/orders/${order.id}/export`, {
      responseType: 'blob'
    })
    
    const url = window.URL.createObjectURL(new Blob([response.data]))
    const link = document.createElement('a')
    link.href = url
    link.setAttribute('download', `订单_${order.order_number}.pdf`)
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
  fetchOrders()
  ElMessage.success('订单创建成功')
}

// 组件挂载
onMounted(() => {
  fetchOrders()
  fetchCustomers()
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

:deep(.el-table .el-table__cell) {
  padding: 8px 0;
}

:deep(.el-form--inline .el-form-item) {
  margin-right: 16px;
  margin-bottom: 16px;
}
</style>