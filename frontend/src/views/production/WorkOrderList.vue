<template>
  <div class="page-container">
    <div class="page-header">
      <h1 class="page-title">生产工单</h1>
      <div class="page-actions">
        <el-button type="primary" @click="showCreateDialog = true">
          <el-icon><Plus /></el-icon>
          新建工单
        </el-button>
      </div>
    </div>

    <!-- 搜索和筛选 -->
    <el-card class="search-card" shadow="never">
      <el-form :model="searchForm" inline>
        <el-form-item label="工单号">
          <el-input
            v-model="searchForm.workOrderNumber"
            placeholder="请输入工单号"
            clearable
            style="width: 200px"
          />
        </el-form-item>
        
        <el-form-item label="产品">
          <el-select
            v-model="searchForm.productId"
            placeholder="请选择产品"
            clearable
            filterable
            style="width: 200px"
          >
            <el-option
              v-for="product in products"
              :key="product.id"
              :label="product.name"
              :value="product.id"
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
            <el-option label="计划中" value="planned" />
            <el-option label="进行中" value="in_progress" />
            <el-option label="已完成" value="completed" />
            <el-option label="已取消" value="cancelled" />
          </el-select>
        </el-form-item>
        
        <el-form-item label="计划日期">
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

    <!-- 工单列表 -->
    <el-card shadow="never">
      <el-table
        v-loading="loading"
        :data="workOrders"
        stripe
        @selection-change="handleSelectionChange"
      >
        <el-table-column type="selection" width="55" />
        
        <el-table-column prop="work_order_number" label="工单号" width="150">
          <template #default="{ row }">
            <el-link type="primary" @click="viewWorkOrder(row.id)">
              {{ row.work_order_number }}
            </el-link>
          </template>
        </el-table-column>
        
        <el-table-column prop="product_name" label="产品" width="150" />
        
        <el-table-column prop="quantity" label="计划数量" width="100" align="right">
          <template #default="{ row }">
            {{ formatNumber(row.quantity) }}
          </template>
        </el-table-column>
        
        <el-table-column prop="completed_quantity" label="完成数量" width="100" align="right">
          <template #default="{ row }">
            {{ formatNumber(row.completed_quantity) }}
          </template>
        </el-table-column>
        
        <el-table-column label="完成率" width="120">
          <template #default="{ row }">
            <el-progress
              :percentage="getCompletionRate(row)"
              :color="getProgressColor(row)"
              :stroke-width="8"
            />
          </template>
        </el-table-column>
        
        <el-table-column prop="planned_start_date" label="计划开始" width="120">
          <template #default="{ row }">
            {{ formatDate(row.planned_start_date) }}
          </template>
        </el-table-column>
        
        <el-table-column prop="planned_end_date" label="计划完成" width="120">
          <template #default="{ row }">
            <span :class="getDateClass(row.planned_end_date, row.status)">
              {{ formatDate(row.planned_end_date) }}
            </span>
          </template>
        </el-table-column>
        
        <el-table-column prop="status" label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="getStatusType(row.status)">
              {{ getStatusText(row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        
        <el-table-column prop="priority" label="优先级" width="100">
          <template #default="{ row }">
            <el-tag :type="getPriorityType(row.priority)" size="small">
              {{ getPriorityText(row.priority) }}
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
              @click="viewWorkOrder(row.id)"
            >
              查看
            </el-button>
            
            <el-button
              v-if="row.status === 'planned'"
              type="success"
              size="small"
              @click="startWorkOrder(row)"
            >
              开始
            </el-button>
            
            <el-button
              v-if="row.status === 'in_progress'"
              type="warning"
              size="small"
              @click="completeWorkOrder(row)"
            >
              完成
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
                    v-if="row.status === 'planned'"
                    command="edit"
                  >
                    编辑工单
                  </el-dropdown-item>
                  <el-dropdown-item
                    v-if="row.status !== 'completed' && row.status !== 'cancelled'"
                    command="cancel"
                  >
                    取消工单
                  </el-dropdown-item>
                  <el-dropdown-item command="duplicate">
                    复制工单
                  </el-dropdown-item>
                  <el-dropdown-item command="export">
                    导出工单
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

    <!-- 新建工单对话框 -->
    <el-dialog
      v-model="showCreateDialog"
      title="新建生产工单"
      width="800px"
      :before-close="handleCloseDialog"
    >
      <WorkOrderForm
        v-if="showCreateDialog"
        @success="handleCreateSuccess"
        @cancel="showCreateDialog = false"
      />
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { api } from '@/utils/api'
import WorkOrderForm from './components/WorkOrderForm.vue'

const router = useRouter()

// 响应式数据
const loading = ref(false)
const workOrders = ref([])
const products = ref([])
const selectedWorkOrders = ref([])
const showCreateDialog = ref(false)

// 搜索表单
const searchForm = reactive({
  workOrderNumber: '',
  productId: null,
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
  planned: { text: '计划中', type: 'info' },
  in_progress: { text: '进行中', type: 'warning' },
  completed: { text: '已完成', type: 'success' },
  cancelled: { text: '已取消', type: 'danger' }
}

// 优先级映射
const priorityMap = {
  low: { text: '低', type: 'info' },
  normal: { text: '普通', type: '' },
  high: { text: '高', type: 'warning' },
  urgent: { text: '紧急', type: 'danger' }
}

// 获取状态文本和类型
const getStatusText = (status) => statusMap[status]?.text || status
const getStatusType = (status) => statusMap[status]?.type || 'info'

// 获取优先级文本和类型
const getPriorityText = (priority) => priorityMap[priority]?.text || priority
const getPriorityType = (priority) => priorityMap[priority]?.type || 'info'

// 获取完成率
const getCompletionRate = (row) => {
  if (!row.quantity || row.quantity === 0) return 0
  return Math.round((row.completed_quantity / row.quantity) * 100)
}

// 获取进度条颜色
const getProgressColor = (row) => {
  const rate = getCompletionRate(row)
  if (rate === 100) return '#67c23a'
  if (rate >= 80) return '#e6a23c'
  if (rate >= 50) return '#5c6bc0'
  return '#f56c6c'
}

// 获取日期样式
const getDateClass = (date, status) => {
  if (!date || status === 'completed' || status === 'cancelled') return ''
  
  const today = new Date()
  const targetDate = new Date(date)
  const diffDays = Math.ceil((targetDate - today) / (1000 * 60 * 60 * 24))
  
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

// 格式化数字
const formatNumber = (number) => {
  if (!number) return '0'
  return Number(number).toLocaleString('zh-CN')
}

// 获取工单列表
const fetchWorkOrders = async () => {
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
    
    const response = await api.get('/production/work-orders', { params })
    workOrders.value = response.data.items || []
    pagination.total = response.data.total || 0
  } catch (error) {
    console.error('获取工单列表失败:', error)
    ElMessage.error('获取工单列表失败')
  } finally {
    loading.value = false
  }
}

// 获取产品列表
const fetchProducts = async () => {
  try {
    const response = await api.get('/products')
    products.value = response.data.items || []
  } catch (error) {
    console.error('获取产品列表失败:', error)
  }
}

// 搜索
const handleSearch = () => {
  pagination.page = 1
  fetchWorkOrders()
}

// 重置
const handleReset = () => {
  Object.assign(searchForm, {
    workOrderNumber: '',
    productId: null,
    status: '',
    dateRange: []
  })
  pagination.page = 1
  fetchWorkOrders()
}

// 分页变化
const handleSizeChange = (size) => {
  pagination.size = size
  pagination.page = 1
  fetchWorkOrders()
}

const handleCurrentChange = (page) => {
  pagination.page = page
  fetchWorkOrders()
}

// 选择变化
const handleSelectionChange = (selection) => {
  selectedWorkOrders.value = selection
}

// 查看工单
const viewWorkOrder = (id) => {
  router.push(`/production/work-orders/${id}`)
}

// 开始工单
const startWorkOrder = async (workOrder) => {
  try {
    await ElMessageBox.confirm(
      `确定要开始工单 ${workOrder.work_order_number} 吗？`,
      '开始工单',
      {
        confirmButtonText: '确认',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    
    await api.patch(`/production/work-orders/${workOrder.id}/start`)
    ElMessage.success('工单已开始')
    fetchWorkOrders()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('开始工单失败:', error)
      ElMessage.error('开始工单失败')
    }
  }
}

// 完成工单
const completeWorkOrder = async (workOrder) => {
  try {
    await ElMessageBox.confirm(
      `确定要完成工单 ${workOrder.work_order_number} 吗？`,
      '完成工单',
      {
        confirmButtonText: '确认',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    
    await api.patch(`/production/work-orders/${workOrder.id}/complete`)
    ElMessage.success('工单已完成')
    fetchWorkOrders()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('完成工单失败:', error)
      ElMessage.error('完成工单失败')
    }
  }
}

// 处理下拉菜单命令
const handleCommand = async (command, row) => {
  switch (command) {
    case 'edit':
      editWorkOrder(row)
      break
    case 'cancel':
      await cancelWorkOrder(row)
      break
    case 'duplicate':
      await duplicateWorkOrder(row)
      break
    case 'export':
      await exportWorkOrder(row)
      break
  }
}

// 编辑工单
const editWorkOrder = (workOrder) => {
  router.push(`/production/work-orders/${workOrder.id}/edit`)
}

// 取消工单
const cancelWorkOrder = async (workOrder) => {
  try {
    await ElMessageBox.confirm(
      `确定要取消工单 ${workOrder.work_order_number} 吗？`,
      '取消工单',
      {
        confirmButtonText: '确认',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    
    await api.patch(`/production/work-orders/${workOrder.id}/cancel`)
    ElMessage.success('工单取消成功')
    fetchWorkOrders()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('取消工单失败:', error)
      ElMessage.error('取消工单失败')
    }
  }
}

// 复制工单
const duplicateWorkOrder = async (workOrder) => {
  try {
    await api.post(`/production/work-orders/${workOrder.id}/duplicate`)
    ElMessage.success('工单复制成功')
    fetchWorkOrders()
  } catch (error) {
    console.error('复制工单失败:', error)
    ElMessage.error('复制工单失败')
  }
}

// 导出工单
const exportWorkOrder = async (workOrder) => {
  try {
    const response = await api.get(`/production/work-orders/${workOrder.id}/export`, {
      responseType: 'blob'
    })
    
    const url = window.URL.createObjectURL(new Blob([response.data]))
    const link = document.createElement('a')
    link.href = url
    link.setAttribute('download', `工单_${workOrder.work_order_number}.pdf`)
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    window.URL.revokeObjectURL(url)
    
    ElMessage.success('工单导出成功')
  } catch (error) {
    console.error('导出工单失败:', error)
    ElMessage.error('导出工单失败')
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
  fetchWorkOrders()
  ElMessage.success('工单创建成功')
}

// 组件挂载
onMounted(() => {
  fetchWorkOrders()
  fetchProducts()
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