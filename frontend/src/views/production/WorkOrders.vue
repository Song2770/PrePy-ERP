<template>
  <div class="work-orders">
    <div class="page-header">
      <h1>生产工单</h1>
      <p>管理生产工单和生产计划</p>
    </div>
    
    <div class="content-card">
      <div class="filters">
        <el-form :inline="true" :model="filters" class="filter-form">
          <el-form-item label="工单号">
            <el-input v-model="filters.workOrderNo" placeholder="请输入工单号" clearable />
          </el-form-item>
          <el-form-item label="产品名称">
            <el-input v-model="filters.productName" placeholder="请输入产品名称" clearable />
          </el-form-item>
          <el-form-item label="状态">
            <el-select v-model="filters.status" placeholder="请选择状态" clearable>
              <el-option label="待开始" value="pending" />
              <el-option label="进行中" value="in_progress" />
              <el-option label="已暂停" value="paused" />
              <el-option label="已完成" value="completed" />
              <el-option label="已取消" value="cancelled" />
            </el-select>
          </el-form-item>
          <el-form-item label="优先级">
            <el-select v-model="filters.priority" placeholder="请选择优先级" clearable>
              <el-option label="低" value="low" />
              <el-option label="中" value="medium" />
              <el-option label="高" value="high" />
              <el-option label="紧急" value="urgent" />
            </el-select>
          </el-form-item>
          <el-form-item label="计划日期">
            <el-date-picker
              v-model="filters.dateRange"
              type="daterange"
              range-separator="至"
              start-placeholder="开始日期"
              end-placeholder="结束日期"
              format="YYYY-MM-DD"
              value-format="YYYY-MM-DD"
            />
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="handleSearch">搜索</el-button>
            <el-button @click="handleReset">重置</el-button>
          </el-form-item>
        </el-form>
      </div>

      <div class="table-actions">
        <el-button type="primary" @click="handleAdd">新增工单</el-button>
        <el-button type="success" @click="handleBatchStart">批量开始</el-button>
        <el-button type="warning" @click="handleExport">导出工单</el-button>
      </div>

      <el-table :data="workOrderList" v-loading="loading" stripe>
        <el-table-column type="selection" width="55" />
        <el-table-column prop="workOrderNo" label="工单号" width="150" />
        <el-table-column prop="productName" label="产品名称" min-width="150" />
        <el-table-column prop="productCode" label="产品编码" width="120" />
        <el-table-column prop="plannedQuantity" label="计划数量" width="100">
          <template #default="{ row }">
            {{ row.plannedQuantity }} {{ row.unit }}
          </template>
        </el-table-column>
        <el-table-column prop="completedQuantity" label="完成数量" width="100">
          <template #default="{ row }">
            {{ row.completedQuantity }} {{ row.unit }}
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
        <el-table-column prop="priority" label="优先级" width="100">
          <template #default="{ row }">
            <el-tag :type="getPriorityTag(row.priority)" size="small">
              {{ getPriorityText(row.priority) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="status" label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="getStatusTag(row.status)">
              {{ getStatusText(row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="plannedStartDate" label="计划开始" width="120" />
        <el-table-column prop="plannedEndDate" label="计划完成" width="120" />
        <el-table-column prop="actualStartDate" label="实际开始" width="120" />
        <el-table-column prop="responsiblePerson" label="负责人" width="100" />
        <el-table-column label="操作" width="200" fixed="right">
          <template #default="{ row }">
            <el-button type="primary" size="small" @click="handleView(row)">查看</el-button>
            <el-button type="warning" size="small" @click="handleEdit(row)" v-if="canEdit(row)">编辑</el-button>
            <el-button type="success" size="small" @click="handleStart(row)" v-if="row.status === 'pending'">开始</el-button>
            <el-button type="info" size="small" @click="handlePause(row)" v-if="row.status === 'in_progress'">暂停</el-button>
            <el-button type="success" size="small" @click="handleComplete(row)" v-if="canComplete(row)">完成</el-button>
          </template>
        </el-table-column>
      </el-table>

      <div class="pagination">
        <el-pagination
          v-model:current-page="pagination.page"
          v-model:page-size="pagination.size"
          :page-sizes="[10, 20, 50, 100]"
          :total="pagination.total"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="handleSizeChange"
          @current-change="handlePageChange"
        />
      </div>
    </div>

    <!-- 生产统计卡片 -->
    <div class="stats-cards">
      <el-row :gutter="20">
        <el-col :span="6">
          <div class="stat-card">
            <div class="stat-icon total">
              <el-icon><Document /></el-icon>
            </div>
            <div class="stat-content">
              <div class="stat-value">{{ stats.totalWorkOrders }}</div>
              <div class="stat-label">总工单数</div>
            </div>
          </div>
        </el-col>
        <el-col :span="6">
          <div class="stat-card">
            <div class="stat-icon pending">
              <el-icon><Clock /></el-icon>
            </div>
            <div class="stat-content">
              <div class="stat-value">{{ stats.pendingWorkOrders }}</div>
              <div class="stat-label">待开始</div>
            </div>
          </div>
        </el-col>
        <el-col :span="6">
          <div class="stat-card">
            <div class="stat-icon progress">
              <el-icon><Loading /></el-icon>
            </div>
            <div class="stat-content">
              <div class="stat-value">{{ stats.inProgressWorkOrders }}</div>
              <div class="stat-label">进行中</div>
            </div>
          </div>
        </el-col>
        <el-col :span="6">
          <div class="stat-card">
            <div class="stat-icon completed">
              <el-icon><Check /></el-icon>
            </div>
            <div class="stat-content">
              <div class="stat-value">{{ stats.completedWorkOrders }}</div>
              <div class="stat-label">已完成</div>
            </div>
          </div>
        </el-col>
      </el-row>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Document, Clock, Loading, Check } from '@element-plus/icons-vue'

// 响应式数据
const loading = ref(false)
const workOrderList = ref([])

const filters = reactive({
  workOrderNo: '',
  productName: '',
  status: '',
  priority: '',
  dateRange: []
})

const pagination = reactive({
  page: 1,
  size: 20,
  total: 0
})

// 模拟数据
const mockData = [
  {
    id: 1,
    workOrderNo: 'WO202401001',
    productName: '智能手机外壳',
    productCode: 'P001',
    plannedQuantity: 1000,
    completedQuantity: 750,
    unit: '个',
    priority: 'high',
    status: 'in_progress',
    plannedStartDate: '2024-01-15',
    plannedEndDate: '2024-01-25',
    actualStartDate: '2024-01-15',
    responsiblePerson: '张工程师'
  },
  {
    id: 2,
    workOrderNo: 'WO202401002',
    productName: '电路板组件',
    productCode: 'P002',
    plannedQuantity: 500,
    completedQuantity: 0,
    unit: '块',
    priority: 'medium',
    status: 'pending',
    plannedStartDate: '2024-01-20',
    plannedEndDate: '2024-01-30',
    actualStartDate: '',
    responsiblePerson: '李技师'
  },
  {
    id: 3,
    workOrderNo: 'WO202401003',
    productName: '显示屏模块',
    productCode: 'P003',
    plannedQuantity: 800,
    completedQuantity: 800,
    unit: '个',
    priority: 'urgent',
    status: 'completed',
    plannedStartDate: '2024-01-10',
    plannedEndDate: '2024-01-18',
    actualStartDate: '2024-01-10',
    responsiblePerson: '王主管'
  },
  {
    id: 4,
    workOrderNo: 'WO202401004',
    productName: '电池组装',
    productCode: 'P004',
    plannedQuantity: 600,
    completedQuantity: 300,
    unit: '组',
    priority: 'low',
    status: 'paused',
    plannedStartDate: '2024-01-12',
    plannedEndDate: '2024-01-22',
    actualStartDate: '2024-01-12',
    responsiblePerson: '赵技师'
  },
  {
    id: 5,
    workOrderNo: 'WO202401005',
    productName: '包装材料',
    productCode: 'P005',
    plannedQuantity: 2000,
    completedQuantity: 0,
    unit: '套',
    priority: 'medium',
    status: 'cancelled',
    plannedStartDate: '2024-01-25',
    plannedEndDate: '2024-02-05',
    actualStartDate: '',
    responsiblePerson: '孙操作员'
  }
]

// 计算属性
const stats = computed(() => {
  const total = workOrderList.value.length
  const pending = workOrderList.value.filter(wo => wo.status === 'pending').length
  const inProgress = workOrderList.value.filter(wo => wo.status === 'in_progress').length
  const completed = workOrderList.value.filter(wo => wo.status === 'completed').length
  
  return {
    totalWorkOrders: total,
    pendingWorkOrders: pending,
    inProgressWorkOrders: inProgress,
    completedWorkOrders: completed
  }
})

// 方法
const fetchWorkOrders = async () => {
  loading.value = true
  try {
    // 模拟API调用
    await new Promise(resolve => setTimeout(resolve, 500))
    workOrderList.value = mockData
    pagination.total = mockData.length
  } catch (error) {
    ElMessage.error('获取工单列表失败')
  } finally {
    loading.value = false
  }
}

const handleSearch = () => {
  pagination.page = 1
  fetchWorkOrders()
}

const handleReset = () => {
  Object.assign(filters, {
    workOrderNo: '',
    productName: '',
    status: '',
    priority: '',
    dateRange: []
  })
  handleSearch()
}

const handleAdd = () => {
  ElMessage.info('新增工单功能开发中')
}

const handleBatchStart = () => {
  ElMessage.info('批量开始功能开发中')
}

const handleExport = () => {
  ElMessage.info('导出功能开发中')
}

const handleView = (row) => {
  ElMessage.info(`查看工单: ${row.workOrderNo}`)
}

const handleEdit = (row) => {
  ElMessage.info(`编辑工单: ${row.workOrderNo}`)
}

const handleStart = async (row) => {
  try {
    await ElMessageBox.confirm(`确定要开始工单 ${row.workOrderNo} 吗？`, '开始生产', {
      type: 'warning'
    })
    row.status = 'in_progress'
    row.actualStartDate = new Date().toISOString().split('T')[0]
    ElMessage.success('工单已开始生产')
  } catch {
    // 用户取消操作
  }
}

const handlePause = async (row) => {
  try {
    await ElMessageBox.confirm(`确定要暂停工单 ${row.workOrderNo} 吗？`, '暂停生产', {
      type: 'warning'
    })
    row.status = 'paused'
    ElMessage.success('工单已暂停')
  } catch {
    // 用户取消操作
  }
}

const handleComplete = async (row) => {
  try {
    await ElMessageBox.confirm(`确定要完成工单 ${row.workOrderNo} 吗？`, '完成生产', {
      type: 'warning'
    })
    row.status = 'completed'
    row.completedQuantity = row.plannedQuantity
    ElMessage.success('工单已完成')
  } catch {
    // 用户取消操作
  }
}

const handleSizeChange = (size) => {
  pagination.size = size
  fetchWorkOrders()
}

const handlePageChange = (page) => {
  pagination.page = page
  fetchWorkOrders()
}

const getCompletionRate = (row) => {
  if (row.plannedQuantity === 0) return 0
  return Math.round((row.completedQuantity / row.plannedQuantity) * 100)
}

const getProgressColor = (row) => {
  const rate = getCompletionRate(row)
  if (rate >= 100) return '#67c23a'
  if (rate >= 80) return '#e6a23c'
  if (rate >= 50) return '#5c6bc0'
  return '#f56c6c'
}

const getPriorityTag = (priority) => {
  const tagMap = {
    low: 'info',
    medium: 'warning',
    high: 'danger',
    urgent: 'danger'
  }
  return tagMap[priority] || 'info'
}

const getPriorityText = (priority) => {
  const textMap = {
    low: '低',
    medium: '中',
    high: '高',
    urgent: '紧急'
  }
  return textMap[priority] || '未知'
}

const getStatusTag = (status) => {
  const tagMap = {
    pending: 'info',
    in_progress: 'warning',
    paused: 'danger',
    completed: 'success',
    cancelled: 'danger'
  }
  return tagMap[status] || 'info'
}

const getStatusText = (status) => {
  const textMap = {
    pending: '待开始',
    in_progress: '进行中',
    paused: '已暂停',
    completed: '已完成',
    cancelled: '已取消'
  }
  return textMap[status] || '未知'
}

const canEdit = (row) => {
  return ['pending', 'paused'].includes(row.status)
}

const canComplete = (row) => {
  return ['in_progress', 'paused'].includes(row.status)
}

// 生命周期
onMounted(() => {
  fetchWorkOrders()
})
</script>

<style scoped>
.work-orders {
  padding: 20px;
}

.page-header {
  margin-bottom: 20px;
}

.page-header h1 {
  margin: 0 0 8px 0;
  font-size: 24px;
  font-weight: 600;
  color: #303133;
}

.page-header p {
  margin: 0;
  color: #606266;
  font-size: 14px;
}

.content-card {
  background: white;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  margin-bottom: 20px;
}

.filters {
  margin-bottom: 20px;
  padding: 20px;
  background: #f8f9fa;
  border-radius: 6px;
}

.filter-form .el-form-item {
  margin-bottom: 0;
}

.table-actions {
  margin-bottom: 20px;
  display: flex;
  gap: 10px;
}

.pagination {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}

.stats-cards {
  margin-top: 20px;
}

.stat-card {
  background: white;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  display: flex;
  align-items: center;
  gap: 15px;
}

.stat-icon {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
  color: white;
}

.stat-icon.total {
  background: #5c6bc0;
}

.stat-icon.pending {
  background: #909399;
}

.stat-icon.progress {
  background: #e6a23c;
}

.stat-icon.completed {
  background: #67c23a;
}

.stat-content {
  flex: 1;
}

.stat-value {
  font-size: 24px;
  font-weight: 600;
  color: #303133;
  margin-bottom: 4px;
}

.stat-label {
  font-size: 14px;
  color: #606266;
}
</style>