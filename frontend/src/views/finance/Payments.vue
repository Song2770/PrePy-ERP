<template>
  <div class="payments">
    <div class="page-header">
      <h1>付款管理</h1>
      <p>管理付款记录、付款计划和资金流水</p>
    </div>
    
    <div class="content-card">
      <div class="filters">
        <el-form :inline="true" :model="filters" class="filter-form">
          <el-form-item label="付款单号">
            <el-input v-model="filters.paymentNumber" placeholder="请输入付款单号" clearable />
          </el-form-item>
          <el-form-item label="付款类型">
            <el-select v-model="filters.paymentType" placeholder="请选择类型" clearable>
              <el-option label="采购付款" value="purchase" />
              <el-option label="费用报销" value="expense" />
              <el-option label="工资发放" value="salary" />
              <el-option label="税费缴纳" value="tax" />
              <el-option label="其他付款" value="other" />
            </el-select>
          </el-form-item>
          <el-form-item label="收款方">
            <el-input v-model="filters.payee" placeholder="请输入收款方" clearable />
          </el-form-item>
          <el-form-item label="付款方式">
            <el-select v-model="filters.paymentMethod" placeholder="请选择方式" clearable>
              <el-option label="银行转账" value="bank_transfer" />
              <el-option label="现金支付" value="cash" />
              <el-option label="支票" value="check" />
              <el-option label="信用卡" value="credit_card" />
              <el-option label="支付宝" value="alipay" />
              <el-option label="微信支付" value="wechat" />
            </el-select>
          </el-form-item>
          <el-form-item label="状态">
            <el-select v-model="filters.status" placeholder="请选择状态" clearable>
              <el-option label="待审核" value="pending" />
              <el-option label="已审核" value="approved" />
              <el-option label="已付款" value="paid" />
              <el-option label="已拒绝" value="rejected" />
            </el-select>
          </el-form-item>
          <el-form-item label="付款日期">
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
        <el-button type="primary" @click="handleAdd">新增付款</el-button>
        <el-button type="success" @click="handleBatchImport">批量导入</el-button>
        <el-button type="warning" @click="handleExport">导出付款</el-button>
        <el-button type="info" @click="handleCashFlow">资金流水</el-button>
      </div>

      <el-table :data="paymentList" v-loading="loading" stripe>
        <el-table-column type="selection" width="55" />
        <el-table-column prop="paymentNumber" label="付款单号" width="150" />
        <el-table-column prop="paymentType" label="付款类型" width="100">
          <template #default="{ row }">
            <el-tag size="small" :type="getTypeTag(row.paymentType)">
              {{ getTypeText(row.paymentType) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="payee" label="收款方" min-width="150" />
        <el-table-column prop="amount" label="付款金额" width="120">
          <template #default="{ row }">
            <span class="amount">¥{{ row.amount.toFixed(2) }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="paymentMethod" label="付款方式" width="100">
          <template #default="{ row }">
            <el-tag size="small" type="info">
              {{ getMethodText(row.paymentMethod) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="bankAccount" label="付款账户" width="150" />
        <el-table-column prop="paymentDate" label="付款日期" width="120" />
        <el-table-column prop="dueDate" label="到期日期" width="120" />
        <el-table-column prop="status" label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="getStatusTag(row.status)">
              {{ getStatusText(row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="relatedDocument" label="关联单据" width="120" />
        <el-table-column prop="approver" label="审核人" width="100" />
        <el-table-column prop="remark" label="备注" width="150" show-overflow-tooltip />
        <el-table-column prop="createdBy" label="创建人" width="100" />
        <el-table-column prop="createdAt" label="创建时间" width="160" />
        <el-table-column label="操作" width="200" fixed="right">
          <template #default="{ row }">
            <el-button type="primary" size="small" @click="handleView(row)">查看</el-button>
            <el-button type="warning" size="small" @click="handleEdit(row)" v-if="row.status === 'pending'">编辑</el-button>
            <el-button type="success" size="small" @click="handleApprove(row)" v-if="row.status === 'pending'">审核</el-button>
            <el-dropdown trigger="click">
              <el-button type="info" size="small">
                更多<el-icon class="el-icon--right"><arrow-down /></el-icon>
              </el-button>
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item @click="handlePrint(row)">打印凭证</el-dropdown-item>
                  <el-dropdown-item @click="handleDownload(row)">下载凭证</el-dropdown-item>
                  <el-dropdown-item @click="handleCopy(row)">复制付款</el-dropdown-item>
                  <el-dropdown-item @click="handleVoucher(row)">生成凭证</el-dropdown-item>
                  <el-dropdown-item divided @click="handleReject(row)" v-if="row.status === 'pending'">拒绝付款</el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
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

    <!-- 付款统计卡片 -->
    <div class="stats-cards">
      <el-row :gutter="20">
        <el-col :span="6">
          <div class="stat-card">
            <div class="stat-icon total">
              <el-icon><CreditCard /></el-icon>
            </div>
            <div class="stat-content">
              <div class="stat-value">{{ stats.totalPayments }}</div>
              <div class="stat-label">总付款数</div>
            </div>
          </div>
        </el-col>
        <el-col :span="6">
          <div class="stat-card">
            <div class="stat-icon amount">
              <el-icon><Money /></el-icon>
            </div>
            <div class="stat-content">
              <div class="stat-value">¥{{ stats.totalAmount.toFixed(0) }}</div>
              <div class="stat-label">总付款金额</div>
            </div>
          </div>
        </el-col>
        <el-col :span="6">
          <div class="stat-card">
            <div class="stat-icon pending">
              <el-icon><Clock /></el-icon>
            </div>
            <div class="stat-content">
              <div class="stat-value">{{ stats.pendingPayments }}</div>
              <div class="stat-label">待审核付款</div>
            </div>
          </div>
        </el-col>
        <el-col :span="6">
          <div class="stat-card">
            <div class="stat-icon today">
              <el-icon><Calendar /></el-icon>
            </div>
            <div class="stat-content">
              <div class="stat-value">¥{{ stats.todayAmount.toFixed(0) }}</div>
              <div class="stat-label">今日付款</div>
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
import { CreditCard, Money, Clock, Calendar, ArrowDown } from '@element-plus/icons-vue'

// 响应式数据
const loading = ref(false)
const paymentList = ref([])

const filters = reactive({
  paymentNumber: '',
  paymentType: '',
  payee: '',
  paymentMethod: '',
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
    paymentNumber: 'PAY-2024-001',
    paymentType: 'purchase',
    payee: '深圳供应商有限公司',
    amount: 50000.00,
    paymentMethod: 'bank_transfer',
    bankAccount: '工商银行***1234',
    paymentDate: '2024-01-15',
    dueDate: '2024-01-20',
    status: 'paid',
    relatedDocument: 'PO-2024-001',
    approver: '财务经理',
    remark: '采购原材料付款',
    createdBy: '张采购',
    createdAt: '2024-01-15 10:30:00'
  },
  {
    id: 2,
    paymentNumber: 'PAY-2024-002',
    paymentType: 'expense',
    payee: '办公用品商店',
    amount: 2500.00,
    paymentMethod: 'cash',
    bankAccount: '现金',
    paymentDate: '2024-01-16',
    dueDate: '2024-01-16',
    status: 'approved',
    relatedDocument: 'EXP-2024-001',
    approver: '部门经理',
    remark: '办公用品采购',
    createdBy: '李行政',
    createdAt: '2024-01-16 14:20:00'
  },
  {
    id: 3,
    paymentNumber: 'PAY-2024-003',
    paymentType: 'salary',
    payee: '员工工资',
    amount: 180000.00,
    paymentMethod: 'bank_transfer',
    bankAccount: '建设银行***5678',
    paymentDate: '2024-01-25',
    dueDate: '2024-01-25',
    status: 'pending',
    relatedDocument: 'SAL-2024-01',
    approver: '',
    remark: '2024年1月工资发放',
    createdBy: '王人事',
    createdAt: '2024-01-17 16:45:00'
  },
  {
    id: 4,
    paymentNumber: 'PAY-2024-004',
    paymentType: 'tax',
    payee: '国家税务局',
    amount: 15000.00,
    paymentMethod: 'bank_transfer',
    bankAccount: '农业银行***9012',
    paymentDate: '2024-01-18',
    dueDate: '2024-01-31',
    status: 'approved',
    relatedDocument: 'TAX-2024-001',
    approver: '财务总监',
    remark: '增值税缴纳',
    createdBy: '赵会计',
    createdAt: '2024-01-18 11:20:00'
  },
  {
    id: 5,
    paymentNumber: 'PAY-2024-005',
    paymentType: 'other',
    payee: '物业管理公司',
    amount: 8000.00,
    paymentMethod: 'alipay',
    bankAccount: '支付宝',
    paymentDate: '2024-01-19',
    dueDate: '2024-01-19',
    status: 'rejected',
    relatedDocument: 'PROP-2024-001',
    approver: '财务经理',
    remark: '办公楼物业费',
    createdBy: '钱行政',
    createdAt: '2024-01-19 08:30:00'
  }
]

// 计算属性
const stats = computed(() => {
  const total = paymentList.value.length
  const totalAmount = paymentList.value.reduce((sum, pay) => sum + pay.amount, 0)
  const pending = paymentList.value.filter(pay => pay.status === 'pending').length
  const today = new Date().toISOString().split('T')[0]
  const todayAmount = paymentList.value
    .filter(pay => pay.paymentDate === today && pay.status === 'paid')
    .reduce((sum, pay) => sum + pay.amount, 0)
  
  return {
    totalPayments: total,
    totalAmount: totalAmount,
    pendingPayments: pending,
    todayAmount: todayAmount
  }
})

// 方法
const fetchPayments = async () => {
  loading.value = true
  try {
    // 模拟API调用
    await new Promise(resolve => setTimeout(resolve, 500))
    paymentList.value = mockData
    pagination.total = mockData.length
  } catch (error) {
    ElMessage.error('获取付款列表失败')
  } finally {
    loading.value = false
  }
}

const handleSearch = () => {
  pagination.page = 1
  fetchPayments()
}

const handleReset = () => {
  Object.assign(filters, {
    paymentNumber: '',
    paymentType: '',
    payee: '',
    paymentMethod: '',
    status: '',
    dateRange: []
  })
  handleSearch()
}

const handleAdd = () => {
  ElMessage.info('新增付款功能开发中')
}

const handleBatchImport = () => {
  ElMessage.info('批量导入功能开发中')
}

const handleExport = () => {
  ElMessage.info('导出功能开发中')
}

const handleCashFlow = () => {
  ElMessage.info('资金流水功能开发中')
}

const handleView = (row) => {
  ElMessage.info(`查看付款: ${row.paymentNumber}`)
}

const handleEdit = (row) => {
  ElMessage.info(`编辑付款: ${row.paymentNumber}`)
}

const handleApprove = async (row) => {
  try {
    await ElMessageBox.confirm(`确定要审核通过付款 ${row.paymentNumber} 吗？`, '审核付款', {
      type: 'warning'
    })
    row.status = 'approved'
    row.approver = '当前用户'
    ElMessage.success('付款审核通过')
  } catch {
    // 用户取消操作
  }
}

const handleReject = async (row) => {
  try {
    await ElMessageBox.confirm(`确定要拒绝付款 ${row.paymentNumber} 吗？`, '拒绝付款', {
      type: 'warning'
    })
    row.status = 'rejected'
    row.approver = '当前用户'
    ElMessage.success('付款已拒绝')
  } catch {
    // 用户取消操作
  }
}

const handlePrint = (row) => {
  ElMessage.info(`打印凭证: ${row.paymentNumber}`)
}

const handleDownload = (row) => {
  ElMessage.info(`下载凭证: ${row.paymentNumber}`)
}

const handleCopy = (row) => {
  ElMessage.info(`复制付款: ${row.paymentNumber}`)
}

const handleVoucher = (row) => {
  ElMessage.info(`生成凭证: ${row.paymentNumber}`)
}

const handleSizeChange = (size) => {
  pagination.size = size
  fetchPayments()
}

const handlePageChange = (page) => {
  pagination.page = page
  fetchPayments()
}

const getTypeTag = (type) => {
  const tagMap = {
    purchase: 'primary',
    expense: 'success',
    salary: 'warning',
    tax: 'danger',
    other: 'info'
  }
  return tagMap[type] || 'info'
}

const getTypeText = (type) => {
  const textMap = {
    purchase: '采购付款',
    expense: '费用报销',
    salary: '工资发放',
    tax: '税费缴纳',
    other: '其他付款'
  }
  return textMap[type] || '未知'
}

const getMethodText = (method) => {
  const textMap = {
    bank_transfer: '银行转账',
    cash: '现金支付',
    check: '支票',
    credit_card: '信用卡',
    alipay: '支付宝',
    wechat: '微信支付'
  }
  return textMap[method] || '未知'
}

const getStatusTag = (status) => {
  const tagMap = {
    pending: 'warning',
    approved: 'primary',
    paid: 'success',
    rejected: 'danger'
  }
  return tagMap[status] || 'info'
}

const getStatusText = (status) => {
  const textMap = {
    pending: '待审核',
    approved: '已审核',
    paid: '已付款',
    rejected: '已拒绝'
  }
  return textMap[status] || '未知'
}

// 生命周期
onMounted(() => {
  fetchPayments()
})
</script>

<style scoped>
.payments {
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
  color: #f56c6c;
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

.stat-icon.amount {
  background: #f56c6c;
}

.stat-icon.pending {
  background: #e6a23c;
}

.stat-icon.today {
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