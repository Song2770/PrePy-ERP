<template>
  <div class="receivable-list">
    <!-- 页面头部 -->
    <div class="page-header">
      <div class="header-title">
        <h2>应收账款管理</h2>
        <p>管理客户应收账款，跟踪收款进度</p>
      </div>
      <div class="header-actions">
        <el-button type="primary" @click="showCreateDialog = true">
          <el-icon><Plus /></el-icon>
          新增应收
        </el-button>
        <el-button @click="exportData">
          <el-icon><Download /></el-icon>
          导出
        </el-button>
      </div>
    </div>

    <!-- 统计卡片 -->
    <div class="stats-cards">
      <el-row :gutter="20">
        <el-col :span="6">
          <div class="stat-card">
            <div class="stat-icon total">
              <el-icon><Money /></el-icon>
            </div>
            <div class="stat-content">
              <div class="stat-value">¥{{ formatAmount(stats.totalAmount) }}</div>
              <div class="stat-label">应收总额</div>
            </div>
          </div>
        </el-col>
        <el-col :span="6">
          <div class="stat-card">
            <div class="stat-icon overdue">
              <el-icon><Warning /></el-icon>
            </div>
            <div class="stat-content">
              <div class="stat-value">¥{{ formatAmount(stats.overdueAmount) }}</div>
              <div class="stat-label">逾期金额</div>
            </div>
          </div>
        </el-col>
        <el-col :span="6">
          <div class="stat-card">
            <div class="stat-icon pending">
              <el-icon><Clock /></el-icon>
            </div>
            <div class="stat-content">
              <div class="stat-value">¥{{ formatAmount(stats.pendingAmount) }}</div>
              <div class="stat-label">待收金额</div>
            </div>
          </div>
        </el-col>
        <el-col :span="6">
          <div class="stat-card">
            <div class="stat-icon received">
              <el-icon><Check /></el-icon>
            </div>
            <div class="stat-content">
              <div class="stat-value">¥{{ formatAmount(stats.receivedAmount) }}</div>
              <div class="stat-label">已收金额</div>
            </div>
          </div>
        </el-col>
      </el-row>
    </div>

    <!-- 搜索筛选 -->
    <div class="search-section">
      <el-form :model="searchForm" inline>
        <el-form-item label="客户">
          <el-select
            v-model="searchForm.customerId"
            placeholder="选择客户"
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
            placeholder="选择状态"
            clearable
            style="width: 150px"
          >
            <el-option label="待收款" value="pending" />
            <el-option label="部分收款" value="partial" />
            <el-option label="已收款" value="paid" />
            <el-option label="逾期" value="overdue" />
            <el-option label="坏账" value="bad_debt" />
          </el-select>
        </el-form-item>
        
        <el-form-item label="单据号">
          <el-input
            v-model="searchForm.billNumber"
            placeholder="输入单据号"
            clearable
            style="width: 200px"
          />
        </el-form-item>
        
        <el-form-item label="到期日期">
          <el-date-picker
            v-model="searchForm.dueDateRange"
            type="daterange"
            range-separator="至"
            start-placeholder="开始日期"
            end-placeholder="结束日期"
            format="YYYY-MM-DD"
            value-format="YYYY-MM-DD"
            style="width: 240px"
          />
        </el-form-item>
        
        <el-form-item>
          <el-button type="primary" @click="searchReceivables">
            <el-icon><Search /></el-icon>
            搜索
          </el-button>
          <el-button @click="resetSearch">
            <el-icon><Refresh /></el-icon>
            重置
          </el-button>
        </el-form-item>
      </el-form>
    </div>

    <!-- 应收账款列表 -->
    <div class="table-section">
      <el-table
        :data="receivables"
        v-loading="loading"
        border
        stripe
        @selection-change="handleSelectionChange"
      >
        <el-table-column type="selection" width="55" />
        
        <el-table-column prop="bill_number" label="单据号" width="150" fixed="left">
          <template #default="{ row }">
            <el-link type="primary" @click="viewDetail(row)">
              {{ row.bill_number }}
            </el-link>
          </template>
        </el-table-column>
        
        <el-table-column prop="customer_name" label="客户" width="150" />
        
        <el-table-column prop="source_type" label="来源类型" width="100">
          <template #default="{ row }">
            <el-tag :type="getSourceTypeColor(row.source_type)" size="small">
              {{ getSourceTypeText(row.source_type) }}
            </el-tag>
          </template>
        </el-table-column>
        
        <el-table-column prop="source_number" label="来源单号" width="150" />
        
        <el-table-column prop="total_amount" label="应收金额" width="120" align="right">
          <template #default="{ row }">
            <span class="amount">¥{{ formatAmount(row.total_amount) }}</span>
          </template>
        </el-table-column>
        
        <el-table-column prop="received_amount" label="已收金额" width="120" align="right">
          <template #default="{ row }">
            <span class="amount received">¥{{ formatAmount(row.received_amount) }}</span>
          </template>
        </el-table-column>
        
        <el-table-column prop="remaining_amount" label="未收金额" width="120" align="right">
          <template #default="{ row }">
            <span class="amount pending">¥{{ formatAmount(row.remaining_amount) }}</span>
          </template>
        </el-table-column>
        
        <el-table-column prop="bill_date" label="开票日期" width="120" />
        
        <el-table-column prop="due_date" label="到期日期" width="120">
          <template #default="{ row }">
            <span :class="getDueDateClass(row.due_date, row.status)">
              {{ row.due_date }}
            </span>
          </template>
        </el-table-column>
        
        <el-table-column prop="overdue_days" label="逾期天数" width="100" align="center">
          <template #default="{ row }">
            <span v-if="row.overdue_days > 0" class="overdue-days">
              {{ row.overdue_days }}天
            </span>
            <span v-else>-</span>
          </template>
        </el-table-column>
        
        <el-table-column prop="status" label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="getStatusType(row.status)" size="small">
              {{ getStatusText(row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        
        <el-table-column prop="salesperson" label="销售员" width="100" />
        
        <el-table-column label="操作" width="200" fixed="right">
          <template #default="{ row }">
            <el-button
              v-if="row.status !== 'paid' && row.status !== 'bad_debt'"
              type="primary"
              size="small"
              @click="showReceiveDialog(row)"
            >
              收款
            </el-button>
            <el-button size="small" @click="viewDetail(row)">
              详情
            </el-button>
            <el-dropdown @command="(command) => handleCommand(command, row)">
              <el-button size="small">
                更多<el-icon class="el-icon--right"><ArrowDown /></el-icon>
              </el-button>
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item command="edit">编辑</el-dropdown-item>
                  <el-dropdown-item command="remind">催收提醒</el-dropdown-item>
                  <el-dropdown-item command="writeOff" :disabled="row.status === 'paid'">核销</el-dropdown-item>
                  <el-dropdown-item command="badDebt" :disabled="row.status === 'paid' || row.status === 'bad_debt'">转坏账</el-dropdown-item>
                  <el-dropdown-item command="print">打印</el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
          </template>
        </el-table-column>
      </el-table>
      
      <!-- 分页 -->
      <div class="pagination-wrapper">
        <el-pagination
          v-model:current-page="pagination.current"
          v-model:page-size="pagination.size"
          :total="pagination.total"
          :page-sizes="[10, 20, 50, 100]"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="fetchReceivables"
          @current-change="fetchReceivables"
        />
      </div>
    </div>

    <!-- 批量操作 -->
    <div v-if="selectedRows.length > 0" class="batch-actions">
      <el-alert
        :title="`已选择 ${selectedRows.length} 条记录`"
        type="info"
        show-icon
        :closable="false"
      >
        <template #default>
          <div class="batch-buttons">
            <el-button size="small" @click="batchReceive">批量收款</el-button>
            <el-button size="small" @click="batchRemind">批量催收</el-button>
            <el-button size="small" @click="batchExport">批量导出</el-button>
          </div>
        </template>
      </el-alert>
    </div>

    <!-- 新增应收对话框 -->
    <el-dialog
      v-model="showCreateDialog"
      title="新增应收账款"
      width="800px"
      :close-on-click-modal="false"
    >
      <ReceivableForm
        @success="handleCreateSuccess"
        @cancel="showCreateDialog = false"
      />
    </el-dialog>

    <!-- 收款对话框 -->
    <el-dialog
      v-model="showReceiveFormDialog"
      title="收款登记"
      width="600px"
      :close-on-click-modal="false"
    >
      <ReceiveForm
        :receivable="currentReceivable"
        @success="handleReceiveSuccess"
        @cancel="showReceiveFormDialog = false"
      />
    </el-dialog>

    <!-- 应收详情对话框 -->
    <el-dialog
      v-model="showDetailDialog"
      title="应收账款详情"
      width="1000px"
      :close-on-click-modal="false"
    >
      <ReceivableDetail
        :receivable="currentReceivable"
        @close="showDetailDialog = false"
      />
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { api } from '@/utils/api'
import ReceivableForm from './components/ReceivableForm.vue'
import ReceiveForm from './components/ReceiveForm.vue'
import ReceivableDetail from './components/ReceivableDetail.vue'

// 响应式数据
const loading = ref(false)
const receivables = ref([])
const customers = ref([])
const selectedRows = ref([])
const showCreateDialog = ref(false)
const showReceiveFormDialog = ref(false)
const showDetailDialog = ref(false)
const currentReceivable = ref(null)

// 统计数据
const stats = ref({
  totalAmount: 0,
  overdueAmount: 0,
  pendingAmount: 0,
  receivedAmount: 0
})

// 搜索表单
const searchForm = reactive({
  customerId: null,
  status: null,
  billNumber: '',
  dueDateRange: null
})

// 分页数据
const pagination = reactive({
  current: 1,
  size: 20,
  total: 0
})

// 格式化金额
const formatAmount = (amount) => {
  return Number(amount || 0).toLocaleString('zh-CN', {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2
  })
}

// 获取来源类型颜色
const getSourceTypeColor = (type) => {
  const colorMap = {
    'sales_order': 'primary',
    'service_order': 'success',
    'manual': 'warning'
  }
  return colorMap[type] || 'info'
}

// 获取来源类型文本
const getSourceTypeText = (type) => {
  const textMap = {
    'sales_order': '销售订单',
    'service_order': '服务订单',
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
    'overdue': 'danger',
    'bad_debt': 'info'
  }
  return typeMap[status] || 'info'
}

// 获取状态文本
const getStatusText = (status) => {
  const textMap = {
    'pending': '待收款',
    'partial': '部分收款',
    'paid': '已收款',
    'overdue': '逾期',
    'bad_debt': '坏账'
  }
  return textMap[status] || '未知'
}

// 获取到期日期样式
const getDueDateClass = (dueDate, status) => {
  if (status === 'paid') return ''
  
  const today = new Date()
  const due = new Date(dueDate)
  const diffDays = Math.ceil((due - today) / (1000 * 60 * 60 * 24))
  
  if (diffDays < 0) return 'overdue'
  if (diffDays <= 7) return 'near-due'
  return ''
}

// 获取应收账款列表
const fetchReceivables = async () => {
  try {
    loading.value = true
    const params = {
      page: pagination.current,
      page_size: pagination.size,
      customer_id: searchForm.customerId,
      status: searchForm.status,
      bill_number: searchForm.billNumber
    }
    
    if (searchForm.dueDateRange) {
      params.due_date_start = searchForm.dueDateRange[0]
      params.due_date_end = searchForm.dueDateRange[1]
    }
    
    const response = await api.get('/finance/receivables', { params })
    receivables.value = response.data.items || []
    pagination.total = response.data.total || 0
  } catch (error) {
    console.error('获取应收账款列表失败:', error)
    ElMessage.error('获取应收账款列表失败')
  } finally {
    loading.value = false
  }
}

// 获取统计数据
const fetchStats = async () => {
  try {
    const response = await api.get('/finance/receivables/stats')
    stats.value = response.data || {}
  } catch (error) {
    console.error('获取统计数据失败:', error)
  }
}

// 获取客户列表
const fetchCustomers = async () => {
  try {
    const response = await api.get('/customers', {
      params: { page_size: 1000, status: 'active' }
    })
    customers.value = response.data.items || []
  } catch (error) {
    console.error('获取客户列表失败:', error)
  }
}

// 搜索应收账款
const searchReceivables = () => {
  pagination.current = 1
  fetchReceivables()
}

// 重置搜索
const resetSearch = () => {
  Object.assign(searchForm, {
    customerId: null,
    status: null,
    billNumber: '',
    dueDateRange: null
  })
  searchReceivables()
}

// 选择变化
const handleSelectionChange = (selection) => {
  selectedRows.value = selection
}

// 显示收款对话框
const showReceiveDialog = (row) => {
  currentReceivable.value = row
  showReceiveFormDialog.value = true
}

// 查看详情
const viewDetail = (row) => {
  currentReceivable.value = row
  showDetailDialog.value = true
}

// 处理命令
const handleCommand = async (command, row) => {
  switch (command) {
    case 'edit':
      // 编辑应收账款
      break
    case 'remind':
      await handleRemind(row)
      break
    case 'writeOff':
      await handleWriteOff(row)
      break
    case 'badDebt':
      await handleBadDebt(row)
      break
    case 'print':
      handlePrint(row)
      break
  }
}

// 催收提醒
const handleRemind = async (row) => {
  try {
    await ElMessageBox.confirm(
      `确定要发送催收提醒给客户 ${row.customer_name} 吗？`,
      '催收提醒',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    
    await api.post(`/finance/receivables/${row.id}/remind`)
    ElMessage.success('催收提醒发送成功')
  } catch (error) {
    if (error !== 'cancel') {
      console.error('发送催收提醒失败:', error)
      ElMessage.error('发送催收提醒失败')
    }
  }
}

// 核销
const handleWriteOff = async (row) => {
  try {
    await ElMessageBox.confirm(
      `确定要核销应收账款 ${row.bill_number} 吗？`,
      '核销确认',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    
    await api.post(`/finance/receivables/${row.id}/write-off`)
    ElMessage.success('核销成功')
    fetchReceivables()
    fetchStats()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('核销失败:', error)
      ElMessage.error('核销失败')
    }
  }
}

// 转坏账
const handleBadDebt = async (row) => {
  try {
    await ElMessageBox.confirm(
      `确定要将应收账款 ${row.bill_number} 转为坏账吗？`,
      '坏账确认',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    
    await api.post(`/finance/receivables/${row.id}/bad-debt`)
    ElMessage.success('转坏账成功')
    fetchReceivables()
    fetchStats()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('转坏账失败:', error)
      ElMessage.error('转坏账失败')
    }
  }
}

// 打印
const handlePrint = (row) => {
  window.open(`/finance/receivables/${row.id}/print`, '_blank')
}

// 批量收款
const batchReceive = () => {
  // 实现批量收款逻辑
  ElMessage.info('批量收款功能开发中')
}

// 批量催收
const batchRemind = async () => {
  try {
    await ElMessageBox.confirm(
      `确定要对选中的 ${selectedRows.value.length} 条记录发送催收提醒吗？`,
      '批量催收',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    
    const ids = selectedRows.value.map(row => row.id)
    await api.post('/finance/receivables/batch-remind', { ids })
    ElMessage.success('批量催收提醒发送成功')
  } catch (error) {
    if (error !== 'cancel') {
      console.error('批量催收失败:', error)
      ElMessage.error('批量催收失败')
    }
  }
}

// 批量导出
const batchExport = () => {
  const ids = selectedRows.value.map(row => row.id)
  const params = new URLSearchParams({ ids: ids.join(',') })
  window.open(`/finance/receivables/export?${params}`, '_blank')
}

// 导出数据
const exportData = () => {
  const params = new URLSearchParams({
    customer_id: searchForm.customerId || '',
    status: searchForm.status || '',
    bill_number: searchForm.billNumber || ''
  })
  
  if (searchForm.dueDateRange) {
    params.append('due_date_start', searchForm.dueDateRange[0])
    params.append('due_date_end', searchForm.dueDateRange[1])
  }
  
  window.open(`/finance/receivables/export?${params}`, '_blank')
}

// 处理创建成功
const handleCreateSuccess = () => {
  showCreateDialog.value = false
  fetchReceivables()
  fetchStats()
}

// 处理收款成功
const handleReceiveSuccess = () => {
  showReceiveFormDialog.value = false
  fetchReceivables()
  fetchStats()
}

// 组件挂载
onMounted(() => {
  fetchReceivables()
  fetchStats()
  fetchCustomers()
})
</script>

<style scoped>
.receivable-list {
  padding: 20px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 24px;
}

.header-title h2 {
  margin: 0 0 8px 0;
  font-size: 24px;
  font-weight: 600;
  color: #303133;
}

.header-title p {
  margin: 0;
  color: #606266;
  font-size: 14px;
}

.header-actions {
  display: flex;
  gap: 12px;
}

.stats-cards {
  margin-bottom: 24px;
}

.stat-card {
  display: flex;
  align-items: center;
  padding: 20px;
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.stat-icon {
  width: 48px;
  height: 48px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 16px;
  font-size: 24px;
  color: #fff;
}

.stat-icon.total {
  background: linear-gradient(135deg, #5c6bc0, #7986cb);
}

.stat-icon.overdue {
  background: linear-gradient(135deg, #f56c6c, #f78989);
}

.stat-icon.pending {
  background: linear-gradient(135deg, #e6a23c, #ebb563);
}

.stat-icon.received {
  background: linear-gradient(135deg, #67c23a, #85ce61);
}

.stat-content {
  flex: 1;
}

.stat-value {
  font-size: 24px;
  font-weight: 600;
  color: #303133;
  line-height: 1;
  margin-bottom: 4px;
}

.stat-label {
  font-size: 14px;
  color: #909399;
}

.search-section {
  margin-bottom: 20px;
  padding: 20px;
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.table-section {
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.amount {
  font-weight: 600;
  font-family: 'Courier New', monospace;
}

.amount.received {
  color: #67c23a;
}

.amount.pending {
  color: #e6a23c;
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

.pagination-wrapper {
  padding: 20px;
  text-align: right;
  border-top: 1px solid #ebeef5;
}

.batch-actions {
  position: fixed;
  bottom: 20px;
  left: 50%;
  transform: translateX(-50%);
  z-index: 1000;
  min-width: 400px;
}

.batch-buttons {
  margin-top: 8px;
  display: flex;
  gap: 8px;
}

:deep(.el-table) {
  font-size: 14px;
}

:deep(.el-table th) {
  background-color: #fafafa;
  font-weight: 600;
}

:deep(.el-table .cell) {
  padding: 8px 12px;
}

@media (max-width: 768px) {
  .receivable-list {
    padding: 12px;
  }
  
  .page-header {
    flex-direction: column;
    gap: 16px;
  }
  
  .header-actions {
    width: 100%;
    justify-content: flex-end;
  }
  
  .search-section :deep(.el-form) {
    flex-direction: column;
  }
  
  .search-section :deep(.el-form-item) {
    margin-right: 0;
    margin-bottom: 16px;
  }
  
  .batch-actions {
    left: 20px;
    right: 20px;
    transform: none;
    min-width: auto;
  }
}
</style>