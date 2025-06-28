<template>
  <div class="orders">
    <div class="page-header">
      <h1>销售订单</h1>
      <p>管理销售订单和客户订单信息</p>
    </div>
    
    <div class="content-card">
      <div class="filters">
        <el-form :inline="true" :model="filters" class="filter-form">
          <el-form-item label="订单号">
            <el-input v-model="filters.orderNo" placeholder="请输入订单号" clearable />
          </el-form-item>
          <el-form-item label="客户名称">
            <el-input v-model="filters.customerName" placeholder="请输入客户名称" clearable />
          </el-form-item>
          <el-form-item label="订单状态">
            <el-select v-model="filters.status" placeholder="请选择状态" clearable>
              <el-option label="待确认" value="pending" />
              <el-option label="已确认" value="confirmed" />
              <el-option label="生产中" value="producing" />
              <el-option label="已发货" value="shipped" />
              <el-option label="已完成" value="completed" />
              <el-option label="已取消" value="cancelled" />
            </el-select>
          </el-form-item>
          <el-form-item label="日期范围">
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
        <el-button type="primary" @click="handleAdd">新增订单</el-button>
        <el-button type="success" @click="handleImport">批量导入</el-button>
        <el-button type="warning" @click="handleExport">导出订单</el-button>
      </div>

      <el-table :data="orderList" v-loading="loading" stripe>
        <el-table-column type="selection" width="55" />
        <el-table-column prop="orderNo" label="订单号" width="150" />
        <el-table-column prop="customerName" label="客户名称" min-width="150" />
        <el-table-column prop="contactPerson" label="联系人" width="120" />
        <el-table-column prop="phone" label="联系电话" width="130" />
        <el-table-column prop="totalAmount" label="订单金额" width="120">
          <template #default="{ row }">
            <span class="amount">¥{{ row.totalAmount.toFixed(2) }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="status" label="订单状态" width="100">
          <template #default="{ row }">
            <el-tag :type="getStatusTag(row.status)">
              {{ getStatusText(row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="priority" label="优先级" width="100">
          <template #default="{ row }">
            <el-tag :type="getPriorityTag(row.priority)" size="small">
              {{ getPriorityText(row.priority) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="deliveryDate" label="交货日期" width="120" />
        <el-table-column prop="salesperson" label="销售员" width="100" />
        <el-table-column prop="createdAt" label="创建时间" width="160" />
        <el-table-column label="操作" width="200" fixed="right">
          <template #default="{ row }">
            <el-button type="primary" size="small" @click="handleView(row)">查看</el-button>
            <el-button type="warning" size="small" @click="handleEdit(row)" v-if="canEdit(row)">编辑</el-button>
            <el-button type="success" size="small" @click="handleConfirm(row)" v-if="row.status === 'pending'">确认</el-button>
            <el-button type="danger" size="small" @click="handleCancel(row)" v-if="canCancel(row)">取消</el-button>
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

    <!-- 订单统计卡片 -->
    <div class="stats-cards">
      <el-row :gutter="20">
        <el-col :span="6">
          <div class="stat-card">
            <div class="stat-icon total">
              <el-icon><Document /></el-icon>
            </div>
            <div class="stat-content">
              <div class="stat-value">{{ stats.totalOrders }}</div>
              <div class="stat-label">总订单数</div>
            </div>
          </div>
        </el-col>
        <el-col :span="6">
          <div class="stat-card">
            <div class="stat-icon pending">
              <el-icon><Clock /></el-icon>
            </div>
            <div class="stat-content">
              <div class="stat-value">{{ stats.pendingOrders }}</div>
              <div class="stat-label">待确认</div>
            </div>
          </div>
        </el-col>
        <el-col :span="6">
          <div class="stat-card">
            <div class="stat-icon processing">
              <el-icon><Loading /></el-icon>
            </div>
            <div class="stat-content">
              <div class="stat-value">{{ stats.processingOrders }}</div>
              <div class="stat-label">处理中</div>
            </div>
          </div>
        </el-col>
        <el-col :span="6">
          <div class="stat-card">
            <div class="stat-icon completed">
              <el-icon><Check /></el-icon>
            </div>
            <div class="stat-content">
              <div class="stat-value">{{ stats.completedOrders }}</div>
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
const orderList = ref([])

const filters = reactive({
  orderNo: '',
  customerName: '',
  status: '',
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
    orderNo: 'SO202401001',
    customerName: '北京科技有限公司',
    contactPerson: '张经理',
    phone: '13800138000',
    totalAmount: 125000.00,
    status: 'confirmed',
    priority: 'high',
    deliveryDate: '2024-02-15',
    salesperson: '李销售',
    createdAt: '2024-01-15 10:30:00'
  },
  {
    id: 2,
    orderNo: 'SO202401002',
    customerName: '上海贸易公司',
    contactPerson: '王总',
    phone: '13800138001',
    totalAmount: 89500.00,
    status: 'pending',
    priority: 'medium',
    deliveryDate: '2024-02-20',
    salesperson: '赵销售',
    createdAt: '2024-01-15 14:20:00'
  },
  {
    id: 3,
    orderNo: 'SO202401003',
    customerName: '广州制造企业',
    contactPerson: '刘主管',
    phone: '13800138002',
    totalAmount: 256000.00,
    status: 'producing',
    priority: 'high',
    deliveryDate: '2024-02-25',
    salesperson: '李销售',
    createdAt: '2024-01-14 16:45:00'
  },
  {
    id: 4,
    orderNo: 'SO202401004',
    customerName: '深圳电子公司',
    contactPerson: '陈工程师',
    phone: '13800138003',
    totalAmount: 45000.00,
    status: 'shipped',
    priority: 'low',
    deliveryDate: '2024-02-10',
    salesperson: '孙销售',
    createdAt: '2024-01-13 11:20:00'
  },
  {
    id: 5,
    orderNo: 'SO202401005',
    customerName: '杭州软件公司',
    contactPerson: '周总监',
    phone: '13800138004',
    totalAmount: 78000.00,
    status: 'completed',
    priority: 'medium',
    deliveryDate: '2024-02-05',
    salesperson: '钱销售',
    createdAt: '2024-01-12 08:30:00'
  }
]

// 计算属性
const stats = computed(() => {
  const total = orderList.value.length
  const pending = orderList.value.filter(order => order.status === 'pending').length
  const processing = orderList.value.filter(order => ['confirmed', 'producing', 'shipped'].includes(order.status)).length
  const completed = orderList.value.filter(order => order.status === 'completed').length
  
  return {
    totalOrders: total,
    pendingOrders: pending,
    processingOrders: processing,
    completedOrders: completed
  }
})

// 方法
const fetchOrders = async () => {
  loading.value = true
  try {
    // 模拟API调用
    await new Promise(resolve => setTimeout(resolve, 500))
    orderList.value = mockData
    pagination.total = mockData.length
  } catch (error) {
    ElMessage.error('获取订单列表失败')
  } finally {
    loading.value = false
  }
}

const handleSearch = () => {
  pagination.page = 1
  fetchOrders()
}

const handleReset = () => {
  Object.assign(filters, {
    orderNo: '',
    customerName: '',
    status: '',
    dateRange: []
  })
  handleSearch()
}

const handleAdd = () => {
  ElMessage.info('新增订单功能开发中')
}

const handleImport = () => {
  ElMessage.info('批量导入功能开发中')
}

const handleExport = () => {
  ElMessage.info('导出功能开发中')
}

const handleView = (row) => {
  ElMessage.info(`查看订单: ${row.orderNo}`)
}

const handleEdit = (row) => {
  ElMessage.info(`编辑订单: ${row.orderNo}`)
}

const handleConfirm = async (row) => {
  try {
    await ElMessageBox.confirm(`确定要确认订单 ${row.orderNo} 吗？`, '确认订单', {
      type: 'warning'
    })
    row.status = 'confirmed'
    ElMessage.success('订单确认成功')
  } catch {
    // 用户取消操作
  }
}

const handleCancel = async (row) => {
  try {
    await ElMessageBox.confirm(`确定要取消订单 ${row.orderNo} 吗？`, '取消订单', {
      type: 'warning'
    })
    row.status = 'cancelled'
    ElMessage.success('订单取消成功')
  } catch {
    // 用户取消操作
  }
}

const handleSizeChange = (size) => {
  pagination.size = size
  fetchOrders()
}

const handlePageChange = (page) => {
  pagination.page = page
  fetchOrders()
}

const getStatusTag = (status) => {
  const tagMap = {
    pending: 'warning',
    confirmed: 'primary',
    producing: 'info',
    shipped: 'success',
    completed: 'success',
    cancelled: 'danger'
  }
  return tagMap[status] || 'info'
}

const getStatusText = (status) => {
  const textMap = {
    pending: '待确认',
    confirmed: '已确认',
    producing: '生产中',
    shipped: '已发货',
    completed: '已完成',
    cancelled: '已取消'
  }
  return textMap[status] || '未知'
}

const getPriorityTag = (priority) => {
  const tagMap = {
    high: 'danger',
    medium: 'warning',
    low: 'info'
  }
  return tagMap[priority] || 'info'
}

const getPriorityText = (priority) => {
  const textMap = {
    high: '高',
    medium: '中',
    low: '低'
  }
  return textMap[priority] || '未知'
}

const canEdit = (row) => {
  return ['pending', 'confirmed'].includes(row.status)
}

const canCancel = (row) => {
  return ['pending', 'confirmed'].includes(row.status)
}

// 生命周期
onMounted(() => {
  fetchOrders()
})
</script>

<style scoped>
.orders {
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

.amount {
  font-weight: 600;
  color: #67c23a;
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
  background: #e6a23c;
}

.stat-icon.processing {
  background: #909399;
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