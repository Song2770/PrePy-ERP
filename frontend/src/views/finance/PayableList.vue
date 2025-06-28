<template>
  <div class="payable-list">
    <!-- 统计卡片 -->
    <div class="stats-cards">
      <el-row :gutter="20">
        <el-col :span="6">
          <div class="stat-card total">
            <div class="stat-icon">
              <el-icon><Money /></el-icon>
            </div>
            <div class="stat-content">
              <div class="stat-value">¥{{ formatAmount(stats.total_amount) }}</div>
              <div class="stat-label">应付总额</div>
            </div>
          </div>
        </el-col>
        <el-col :span="6">
          <div class="stat-card overdue">
            <div class="stat-icon">
              <el-icon><Warning /></el-icon>
            </div>
            <div class="stat-content">
              <div class="stat-value">¥{{ formatAmount(stats.overdue_amount) }}</div>
              <div class="stat-label">逾期金额</div>
            </div>
          </div>
        </el-col>
        <el-col :span="6">
          <div class="stat-card pending">
            <div class="stat-icon">
              <el-icon><Clock /></el-icon>
            </div>
            <div class="stat-content">
              <div class="stat-value">¥{{ formatAmount(stats.pending_amount) }}</div>
              <div class="stat-label">待付金额</div>
            </div>
          </div>
        </el-col>
        <el-col :span="6">
          <div class="stat-card paid">
            <div class="stat-icon">
              <el-icon><Check /></el-icon>
            </div>
            <div class="stat-content">
              <div class="stat-value">¥{{ formatAmount(stats.paid_amount) }}</div>
              <div class="stat-label">已付金额</div>
            </div>
          </div>
        </el-col>
      </el-row>
    </div>

    <!-- 搜索和筛选 -->
    <div class="search-section">
      <el-card>
        <el-form :model="searchForm" inline>
          <el-form-item label="供应商">
            <el-select
              v-model="searchForm.supplier_id"
              placeholder="请选择供应商"
              clearable
              filterable
              style="width: 200px;"
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
              style="width: 150px;"
            >
              <el-option label="待付款" value="pending" />
              <el-option label="部分付款" value="partial" />
              <el-option label="已付款" value="paid" />
              <el-option label="逾期" value="overdue" />
            </el-select>
          </el-form-item>
          
          <el-form-item label="单据号">
            <el-input
              v-model="searchForm.bill_number"
              placeholder="请输入单据号"
              clearable
              style="width: 200px;"
            />
          </el-form-item>
          
          <el-form-item label="到期日期">
            <el-date-picker
              v-model="searchForm.due_date_range"
              type="daterange"
              range-separator="至"
              start-placeholder="开始日期"
              end-placeholder="结束日期"
              format="YYYY-MM-DD"
              value-format="YYYY-MM-DD"
              style="width: 240px;"
            />
          </el-form-item>
          
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
    </div>

    <!-- 操作栏 -->
    <div class="action-bar">
      <div class="action-left">
        <el-button type="primary" @click="handleCreate">
          <el-icon><Plus /></el-icon>
          新建应付
        </el-button>
        <el-button
          type="success"
          :disabled="selectedRows.length === 0"
          @click="handleBatchPay"
        >
          <el-icon><Money /></el-icon>
          批量付款
        </el-button>
        <el-button
          type="warning"
          :disabled="selectedRows.length === 0"
          @click="handleBatchRemind"
        >
          <el-icon><Bell /></el-icon>
          批量提醒
        </el-button>
      </div>
      <div class="action-right">
        <el-button @click="handleExport">
          <el-icon><Download /></el-icon>
          导出
        </el-button>
        <el-button @click="handleRefresh">
          <el-icon><Refresh /></el-icon>
          刷新
        </el-button>
      </div>
    </div>

    <!-- 数据表格 -->
    <div class="table-section">
      <el-table
        :data="tableData"
        v-loading="loading"
        border
        @selection-change="handleSelectionChange"
        @sort-change="handleSortChange"
      >
        <el-table-column type="selection" width="55" />
        
        <el-table-column prop="bill_number" label="单据号" width="150" sortable="custom">
          <template #default="{ row }">
            <el-link type="primary" @click="handleView(row)">
              {{ row.bill_number }}
            </el-link>
          </template>
        </el-table-column>
        
        <el-table-column prop="supplier_name" label="供应商" width="150" show-overflow-tooltip />
        
        <el-table-column prop="source_type" label="来源类型" width="120">
          <template #default="{ row }">
            <el-tag :type="getSourceTypeColor(row.source_type)" size="small">
              {{ getSourceTypeText(row.source_type) }}
            </el-tag>
          </template>
        </el-table-column>
        
        <el-table-column prop="source_number" label="来源单号" width="150" show-overflow-tooltip />
        
        <el-table-column prop="total_amount" label="应付金额" width="120" align="right" sortable="custom">
          <template #default="{ row }">
            <span class="amount total">¥{{ formatAmount(row.total_amount) }}</span>
          </template>
        </el-table-column>
        
        <el-table-column prop="paid_amount" label="已付金额" width="120" align="right">
          <template #default="{ row }">
            <span class="amount paid">¥{{ formatAmount(row.paid_amount) }}</span>
          </template>
        </el-table-column>
        
        <el-table-column prop="remaining_amount" label="未付金额" width="120" align="right">
          <template #default="{ row }">
            <span class="amount pending">¥{{ formatAmount(row.remaining_amount) }}</span>
          </template>
        </el-table-column>
        
        <el-table-column prop="bill_date" label="开票日期" width="120" sortable="custom" />
        
        <el-table-column prop="due_date" label="到期日期" width="120" sortable="custom">
          <template #default="{ row }">
            <span :class="getDueDateClass(row)">{{ row.due_date }}</span>
          </template>
        </el-table-column>
        
        <el-table-column prop="status" label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="getStatusType(row.status)" size="small">
              {{ getStatusText(row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        
        <el-table-column prop="buyer" label="采购员" width="100" />
        
        <el-table-column label="操作" width="200" fixed="right">
          <template #default="{ row }">
            <el-button size="small" @click="handleView(row)">
              查看
            </el-button>
            <el-button
              size="small"
              type="primary"
              v-if="row.status !== 'paid'"
              @click="handlePay(row)"
            >
              付款
            </el-button>
            <el-dropdown trigger="click" @command="(command) => handleCommand(command, row)">
              <el-button size="small">
                更多<el-icon class="el-icon--right"><ArrowDown /></el-icon>
              </el-button>
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item command="edit" v-if="row.status === 'pending'">
                    编辑
                  </el-dropdown-item>
                  <el-dropdown-item command="remind" v-if="row.status !== 'paid'">
                    催付提醒
                  </el-dropdown-item>
                  <el-dropdown-item command="duplicate">
                    复制
                  </el-dropdown-item>
                  <el-dropdown-item command="export">
                    导出
                  </el-dropdown-item>
                  <el-dropdown-item command="print">
                    打印
                  </el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
          </template>
        </el-table-column>
      </el-table>
      
      <!-- 分页 -->
      <div class="pagination-wrapper">
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
    </div>

    <!-- 新建/编辑对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="dialogTitle"
      width="80%"
      :close-on-click-modal="false"
    >
      <PayableForm
        v-if="dialogVisible"
        :payable="currentPayable"
        @save="handleSave"
        @cancel="handleCancel"
      />
    </el-dialog>

    <!-- 付款对话框 -->
    <el-dialog
      v-model="payDialogVisible"
      title="付款登记"
      width="60%"
      :close-on-click-modal="false"
    >
      <PayForm
        v-if="payDialogVisible"
        :payable="currentPayable"
        @save="handlePaySave"
        @cancel="handlePayCancel"
      />
    </el-dialog>

    <!-- 详情对话框 -->
    <el-dialog
      v-model="detailDialogVisible"
      title="应付账款详情"
      width="90%"
      :close-on-click-modal="false"
    >
      <PayableDetail
        v-if="detailDialogVisible"
        :payable="currentPayable"
      />
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { api } from '@/utils/api'
import PayableForm from './components/PayableForm.vue'
import PayForm from './components/PayForm.vue'
import PayableDetail from './components/PayableDetail.vue'

// 响应式数据
const loading = ref(false)
const tableData = ref([])
const selectedRows = ref([])
const suppliers = ref([])

// 统计数据
const stats = ref({
  total_amount: 0,
  overdue_amount: 0,
  pending_amount: 0,
  paid_amount: 0
})

// 搜索表单
const searchForm = reactive({
  supplier_id: '',
  status: '',
  bill_number: '',
  due_date_range: []
})

// 分页
const pagination = reactive({
  page: 1,
  size: 20,
  total: 0
})

// 排序
const sortField = ref('')
const sortOrder = ref('')

// 对话框
const dialogVisible = ref(false)
const payDialogVisible = ref(false)
const detailDialogVisible = ref(false)
const currentPayable = ref(null)

// 对话框标题
const dialogTitle = computed(() => {
  return currentPayable.value?.id ? '编辑应付账款' : '新建应付账款'
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

// 获取到期日期样式
const getDueDateClass = (row) => {
  if (row.status === 'paid') return ''
  
  const today = new Date()
  const due = new Date(row.due_date)
  const diffDays = Math.ceil((due - today) / (1000 * 60 * 60 * 24))
  
  if (diffDays < 0) return 'overdue'
  if (diffDays <= 7) return 'near-due'
  return ''
}

// 获取应付账款列表
const fetchPayables = async () => {
  try {
    loading.value = true
    const params = {
      page: pagination.page,
      size: pagination.size,
      ...searchForm
    }
    
    // 处理日期范围
    if (searchForm.due_date_range && searchForm.due_date_range.length === 2) {
      params.due_date_start = searchForm.due_date_range[0]
      params.due_date_end = searchForm.due_date_range[1]
      delete params.due_date_range
    }
    
    // 处理排序
    if (sortField.value) {
      params.sort_field = sortField.value
      params.sort_order = sortOrder.value
    }
    
    const response = await api.get('/finance/payables', { params })
    tableData.value = response.data.items
    pagination.total = response.data.total
  } catch (error) {
    ElMessage.error('获取应付账款列表失败')
    console.error(error)
  } finally {
    loading.value = false
  }
}

// 获取统计数据
const fetchStats = async () => {
  try {
    const response = await api.get('/finance/payables/stats')
    stats.value = response.data
  } catch (error) {
    console.error('获取统计数据失败:', error)
  }
}

// 获取供应商列表
const fetchSuppliers = async () => {
  try {
    const response = await api.get('/suppliers', {
      params: { page: 1, size: 1000, status: 'active' }
    })
    suppliers.value = response.data.items
  } catch (error) {
    console.error('获取供应商列表失败:', error)
  }
}

// 搜索
const handleSearch = () => {
  pagination.page = 1
  fetchPayables()
}

// 重置
const handleReset = () => {
  Object.assign(searchForm, {
    supplier_id: '',
    status: '',
    bill_number: '',
    due_date_range: []
  })
  pagination.page = 1
  sortField.value = ''
  sortOrder.value = ''
  fetchPayables()
}

// 刷新
const handleRefresh = () => {
  fetchPayables()
  fetchStats()
}

// 新建
const handleCreate = () => {
  currentPayable.value = null
  dialogVisible.value = true
}

// 查看
const handleView = (row) => {
  currentPayable.value = { ...row }
  detailDialogVisible.value = true
}

// 付款
const handlePay = (row) => {
  currentPayable.value = { ...row }
  payDialogVisible.value = true
}

// 批量付款
const handleBatchPay = () => {
  if (selectedRows.value.length === 0) {
    ElMessage.warning('请选择要付款的记录')
    return
  }
  
  ElMessageBox.confirm(
    `确定要对选中的 ${selectedRows.value.length} 条记录进行批量付款吗？`,
    '批量付款确认',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    }
  ).then(() => {
    // 实现批量付款逻辑
    console.log('批量付款:', selectedRows.value)
    ElMessage.success('批量付款操作已提交')
  })
}

// 批量提醒
const handleBatchRemind = () => {
  if (selectedRows.value.length === 0) {
    ElMessage.warning('请选择要提醒的记录')
    return
  }
  
  ElMessageBox.confirm(
    `确定要对选中的 ${selectedRows.value.length} 条记录发送催付提醒吗？`,
    '批量提醒确认',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    }
  ).then(async () => {
    try {
      const ids = selectedRows.value.map(row => row.id)
      await api.post('/finance/payables/batch-remind', { ids })
      ElMessage.success('催付提醒已发送')
    } catch (error) {
      ElMessage.error('发送催付提醒失败')
      console.error(error)
    }
  })
}

// 导出
const handleExport = () => {
  const params = { ...searchForm }
  if (searchForm.due_date_range && searchForm.due_date_range.length === 2) {
    params.due_date_start = searchForm.due_date_range[0]
    params.due_date_end = searchForm.due_date_range[1]
    delete params.due_date_range
  }
  
  window.open(`/api/finance/payables/export?${new URLSearchParams(params)}`)
}

// 选择变化
const handleSelectionChange = (selection) => {
  selectedRows.value = selection
}

// 排序变化
const handleSortChange = ({ prop, order }) => {
  sortField.value = prop
  sortOrder.value = order === 'ascending' ? 'asc' : 'desc'
  fetchPayables()
}

// 分页大小变化
const handleSizeChange = (size) => {
  pagination.size = size
  pagination.page = 1
  fetchPayables()
}

// 当前页变化
const handleCurrentChange = (page) => {
  pagination.page = page
  fetchPayables()
}

// 更多操作
const handleCommand = async (command, row) => {
  switch (command) {
    case 'edit':
      currentPayable.value = { ...row }
      dialogVisible.value = true
      break
    case 'remind':
      try {
        await api.post(`/finance/payables/${row.id}/remind`)
        ElMessage.success('催付提醒已发送')
      } catch (error) {
        ElMessage.error('发送催付提醒失败')
        console.error(error)
      }
      break
    case 'duplicate':
      currentPayable.value = { ...row, id: null, bill_number: '' }
      dialogVisible.value = true
      break
    case 'export':
      window.open(`/api/finance/payables/${row.id}/export`)
      break
    case 'print':
      window.open(`/api/finance/payables/${row.id}/print`)
      break
  }
}

// 保存
const handleSave = () => {
  dialogVisible.value = false
  fetchPayables()
  fetchStats()
}

// 取消
const handleCancel = () => {
  dialogVisible.value = false
}

// 付款保存
const handlePaySave = () => {
  payDialogVisible.value = false
  fetchPayables()
  fetchStats()
}

// 付款取消
const handlePayCancel = () => {
  payDialogVisible.value = false
}

// 组件挂载
onMounted(() => {
  fetchPayables()
  fetchStats()
  fetchSuppliers()
})
</script>

<style scoped>
.payable-list {
  padding: 20px;
}

.stats-cards {
  margin-bottom: 20px;
}

.stat-card {
  display: flex;
  align-items: center;
  padding: 20px;
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  border-left: 4px solid;
}

.stat-card.total {
  border-left-color: #5c6bc0;
}

.stat-card.overdue {
  border-left-color: #f56c6c;
}

.stat-card.pending {
  border-left-color: #e6a23c;
}

.stat-card.paid {
  border-left-color: #67c23a;
}

.stat-icon {
  font-size: 32px;
  margin-right: 16px;
  opacity: 0.8;
}

.stat-card.total .stat-icon {
  color: #5c6bc0;
}

.stat-card.overdue .stat-icon {
  color: #f56c6c;
}

.stat-card.pending .stat-icon {
  color: #e6a23c;
}

.stat-card.paid .stat-icon {
  color: #67c23a;
}

.stat-content {
  flex: 1;
}

.stat-value {
  font-size: 24px;
  font-weight: 600;
  line-height: 1;
  margin-bottom: 4px;
  font-family: 'Courier New', monospace;
}

.stat-label {
  font-size: 14px;
  color: #666;
}

.search-section {
  margin-bottom: 20px;
}

.action-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding: 16px;
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.action-left,
.action-right {
  display: flex;
  gap: 12px;
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

.amount.total {
  color: #5c6bc0;
}

.amount.paid {
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

.pagination-wrapper {
  padding: 20px;
  text-align: right;
  border-top: 1px solid #ebeef5;
}

:deep(.el-table) {
  font-size: 14px;
}

:deep(.el-table th) {
  background-color: #fafafa;
}

:deep(.el-table .cell) {
  padding: 8px 12px;
}

@media (max-width: 768px) {
  .payable-list {
    padding: 12px;
  }
  
  .stats-cards {
    margin-bottom: 16px;
  }
  
  .stat-card {
    margin-bottom: 12px;
  }
  
  .action-bar {
    flex-direction: column;
    gap: 12px;
    align-items: stretch;
  }
  
  .action-left,
  .action-right {
    justify-content: center;
  }
  
  :deep(.el-table) {
    font-size: 12px;
  }
  
  :deep(.el-dialog) {
    width: 95% !important;
    margin: 5vh auto;
  }
}
</style>