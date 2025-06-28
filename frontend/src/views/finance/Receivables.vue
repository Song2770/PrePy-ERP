<template>
  <div class="receivables">
    <div class="page-header">
      <h1>应收账款</h1>
      <p>管理客户应收账款和收款记录</p>
    </div>
    
    <div class="content-card">
      <div class="filters">
        <el-form :inline="true" :model="filters" class="filter-form">
          <el-form-item label="客户">
            <el-input v-model="filters.customerName" placeholder="请输入客户名称" clearable />
          </el-form-item>
          <el-form-item label="单据号">
            <el-input v-model="filters.documentNo" placeholder="请输入单据号" clearable />
          </el-form-item>
          <el-form-item label="状态">
            <el-select v-model="filters.status" placeholder="请选择状态" clearable>
              <el-option label="未收款" value="unpaid" />
              <el-option label="部分收款" value="partial_paid" />
              <el-option label="已收款" value="paid" />
              <el-option label="已逾期" value="overdue" />
            </el-select>
          </el-form-item>
          <el-form-item label="金额范围">
            <el-input-number v-model="filters.minAmount" placeholder="最小金额" :min="0" style="width: 120px" />
            <span style="margin: 0 8px">-</span>
            <el-input-number v-model="filters.maxAmount" placeholder="最大金额" :min="0" style="width: 120px" />
          </el-form-item>
          <el-form-item label="到期日期">
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
        <el-button type="primary" @click="handleAdd">新增应收</el-button>
        <el-button type="success" @click="handleBatchReceive">批量收款</el-button>
        <el-button type="warning" @click="handleExport">导出数据</el-button>
      </div>

      <el-table :data="receivableList" v-loading="loading" stripe>
        <el-table-column type="selection" width="55" />
        <el-table-column prop="documentNo" label="单据号" width="150" />
        <el-table-column prop="customerName" label="客户" min-width="150" />
        <el-table-column prop="contactPerson" label="联系人" width="100" />
        <el-table-column prop="totalAmount" label="应收金额" width="120">
          <template #default="{ row }">
            <span class="amount total">¥{{ row.totalAmount.toFixed(2) }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="receivedAmount" label="已收金额" width="120">
          <template #default="{ row }">
            <span class="amount received">¥{{ row.receivedAmount.toFixed(2) }}</span>
          </template>
        </el-table-column>
        <el-table-column label="未收金额" width="120">
          <template #default="{ row }">
            <span class="amount unreceived">¥{{ (row.totalAmount - row.receivedAmount).toFixed(2) }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="status" label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="getStatusTag(row.status)">
              {{ getStatusText(row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="dueDate" label="到期日期" width="120">
          <template #default="{ row }">
            <span :class="{ 'text-danger': isOverdue(row.dueDate), 'text-warning': isDueSoon(row.dueDate) }">
              {{ row.dueDate }}
            </span>
          </template>
        </el-table-column>
        <el-table-column prop="paymentTerms" label="收款条件" width="120" />
        <el-table-column prop="salesperson" label="销售员" width="100" />
        <el-table-column prop="createdAt" label="创建时间" width="160" />
        <el-table-column label="操作" width="200" fixed="right">
          <template #default="{ row }">
            <el-button type="primary" size="small" @click="handleView(row)">查看</el-button>
            <el-button type="warning" size="small" @click="handleEdit(row)" v-if="canEdit(row)">编辑</el-button>
            <el-button type="success" size="small" @click="handleReceive(row)" v-if="canReceive(row)">收款</el-button>
            <el-button type="info" size="small" @click="handleHistory(row)">记录</el-button>
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

    <!-- 应收统计卡片 -->
    <div class="stats-cards">
      <el-row :gutter="20">
        <el-col :span="6">
          <div class="stat-card">
            <div class="stat-icon total">
              <el-icon><Money /></el-icon>
            </div>
            <div class="stat-content">
              <div class="stat-value">¥{{ stats.totalReceivable.toFixed(0) }}</div>
              <div class="stat-label">应收总额</div>
            </div>
          </div>
        </el-col>
        <el-col :span="6">
          <div class="stat-card">
            <div class="stat-icon received">
              <el-icon><Check /></el-icon>
            </div>
            <div class="stat-content">
              <div class="stat-value">¥{{ stats.totalReceived.toFixed(0) }}</div>
              <div class="stat-label">已收总额</div>
            </div>
          </div>
        </el-col>
        <el-col :span="6">
          <div class="stat-card">
            <div class="stat-icon unreceived">
              <el-icon><Clock /></el-icon>
            </div>
            <div class="stat-content">
              <div class="stat-value">¥{{ stats.totalUnreceived.toFixed(0) }}</div>
              <div class="stat-label">未收总额</div>
            </div>
          </div>
        </el-col>
        <el-col :span="6">
          <div class="stat-card">
            <div class="stat-icon overdue">
              <el-icon><Warning /></el-icon>
            </div>
            <div class="stat-content">
              <div class="stat-value">{{ stats.overdueCount }}</div>
              <div class="stat-label">逾期笔数</div>
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
import { Money, Check, Clock, Warning } from '@element-plus/icons-vue'

// 响应式数据
const loading = ref(false)
const receivableList = ref([])

const filters = reactive({
  customerName: '',
  documentNo: '',
  status: '',
  minAmount: null,
  maxAmount: null,
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
    documentNo: 'AR202401001',
    customerName: '北京科技有限公司',
    contactPerson: '张经理',
    totalAmount: 125000.00,
    receivedAmount: 75000.00,
    status: 'partial_paid',
    dueDate: '2024-02-15',
    paymentTerms: '月结30天',
    salesperson: '李销售',
    createdAt: '2024-01-15 10:30:00'
  },
  {
    id: 2,
    documentNo: 'AR202401002',
    customerName: '上海贸易公司',
    contactPerson: '王总',
    totalAmount: 89500.00,
    receivedAmount: 0.00,
    status: 'unpaid',
    dueDate: '2024-02-20',
    paymentTerms: '现金',
    salesperson: '赵销售',
    createdAt: '2024-01-15 14:20:00'
  },
  {
    id: 3,
    documentNo: 'AR202401003',
    customerName: '广州制造企业',
    contactPerson: '刘主管',
    totalAmount: 256000.00,
    receivedAmount: 256000.00,
    status: 'paid',
    dueDate: '2024-01-25',
    paymentTerms: '预收款',
    salesperson: '李销售',
    createdAt: '2024-01-14 16:45:00'
  },
  {
    id: 4,
    documentNo: 'AR202401004',
    customerName: '深圳电子公司',
    contactPerson: '陈工程师',
    totalAmount: 45000.00,
    receivedAmount: 0.00,
    status: 'overdue',
    dueDate: '2024-01-10',
    paymentTerms: '月结15天',
    salesperson: '孙销售',
    createdAt: '2024-01-13 11:20:00'
  },
  {
    id: 5,
    documentNo: 'AR202401005',
    customerName: '杭州软件公司',
    contactPerson: '周总监',
    totalAmount: 78000.00,
    receivedAmount: 30000.00,
    status: 'partial_paid',
    dueDate: '2024-02-25',
    paymentTerms: '分期收款',
    salesperson: '钱销售',
    createdAt: '2024-01-12 08:30:00'
  },
  {
    id: 6,
    documentNo: 'AR202401006',
    customerName: '成都制药公司',
    contactPerson: '吴总',
    totalAmount: 180000.00,
    receivedAmount: 0.00,
    status: 'unpaid',
    dueDate: '2024-03-01',
    paymentTerms: '月结45天',
    salesperson: '李销售',
    createdAt: '2024-01-11 15:45:00'
  }
]

// 计算属性
const stats = computed(() => {
  const totalReceivable = receivableList.value.reduce((sum, item) => sum + item.totalAmount, 0)
  const totalReceived = receivableList.value.reduce((sum, item) => sum + item.receivedAmount, 0)
  const totalUnreceived = totalReceivable - totalReceived
  const overdueCount = receivableList.value.filter(item => item.status === 'overdue').length
  
  return {
    totalReceivable,
    totalReceived,
    totalUnreceived,
    overdueCount
  }
})

// 方法
const fetchReceivables = async () => {
  loading.value = true
  try {
    // 模拟API调用
    await new Promise(resolve => setTimeout(resolve, 500))
    receivableList.value = mockData
    pagination.total = mockData.length
  } catch (error) {
    ElMessage.error('获取应收账款列表失败')
  } finally {
    loading.value = false
  }
}

const handleSearch = () => {
  pagination.page = 1
  fetchReceivables()
}

const handleReset = () => {
  Object.assign(filters, {
    customerName: '',
    documentNo: '',
    status: '',
    minAmount: null,
    maxAmount: null,
    dateRange: []
  })
  handleSearch()
}

const handleAdd = () => {
  ElMessage.info('新增应收功能开发中')
}

const handleBatchReceive = () => {
  ElMessage.info('批量收款功能开发中')
}

const handleExport = () => {
  ElMessage.info('导出功能开发中')
}

const handleView = (row) => {
  ElMessage.info(`查看应收账款: ${row.documentNo}`)
}

const handleEdit = (row) => {
  ElMessage.info(`编辑应收账款: ${row.documentNo}`)
}

const handleReceive = (row) => {
  ElMessage.info(`收款功能开发中: ${row.documentNo}`)
}

const handleHistory = (row) => {
  ElMessage.info(`查看收款记录: ${row.documentNo}`)
}

const handleSizeChange = (size) => {
  pagination.size = size
  fetchReceivables()
}

const handlePageChange = (page) => {
  pagination.page = page
  fetchReceivables()
}

const getStatusTag = (status) => {
  const tagMap = {
    unpaid: 'warning',
    partial_paid: 'primary',
    paid: 'success',
    overdue: 'danger'
  }
  return tagMap[status] || 'info'
}

const getStatusText = (status) => {
  const textMap = {
    unpaid: '未收款',
    partial_paid: '部分收款',
    paid: '已收款',
    overdue: '已逾期'
  }
  return textMap[status] || '未知'
}

const canEdit = (row) => {
  return ['unpaid', 'partial_paid'].includes(row.status)
}

const canReceive = (row) => {
  return ['unpaid', 'partial_paid', 'overdue'].includes(row.status)
}

const isOverdue = (dueDate) => {
  const today = new Date()
  const due = new Date(dueDate)
  return due < today
}

const isDueSoon = (dueDate) => {
  const today = new Date()
  const due = new Date(dueDate)
  const diffTime = due.getTime() - today.getTime()
  const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))
  return diffDays <= 7 && diffDays > 0
}

// 生命周期
onMounted(() => {
  fetchReceivables()
})
</script>

<style scoped>
.receivables {
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
}

.amount.total {
  color: #5c6bc0;
}

.amount.received {
  color: #67c23a;
}

.amount.unreceived {
  color: #e6a23c;
}

.text-danger {
  color: #f56c6c;
}

.text-warning {
  color: #e6a23c;
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

.stat-icon.received {
  background: #67c23a;
}

.stat-icon.unreceived {
  background: #e6a23c;
}

.stat-icon.overdue {
  background: #f56c6c;
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