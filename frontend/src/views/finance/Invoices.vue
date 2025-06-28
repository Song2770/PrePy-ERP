<template>
  <div class="invoices">
    <div class="page-header">
      <h1>发票管理</h1>
      <p>管理销售发票、采购发票和税务信息</p>
    </div>
    
    <div class="content-card">
      <div class="filters">
        <el-form :inline="true" :model="filters" class="filter-form">
          <el-form-item label="发票号码">
            <el-input v-model="filters.invoiceNumber" placeholder="请输入发票号码" clearable />
          </el-form-item>
          <el-form-item label="发票类型">
            <el-select v-model="filters.invoiceType" placeholder="请选择类型" clearable>
              <el-option label="销售发票" value="sales" />
              <el-option label="采购发票" value="purchase" />
              <el-option label="专用发票" value="special" />
              <el-option label="普通发票" value="ordinary" />
            </el-select>
          </el-form-item>
          <el-form-item label="客户/供应商">
            <el-input v-model="filters.partner" placeholder="请输入客户或供应商" clearable />
          </el-form-item>
          <el-form-item label="状态">
            <el-select v-model="filters.status" placeholder="请选择状态" clearable>
              <el-option label="草稿" value="draft" />
              <el-option label="已开具" value="issued" />
              <el-option label="已发送" value="sent" />
              <el-option label="已收款" value="paid" />
              <el-option label="已作废" value="cancelled" />
            </el-select>
          </el-form-item>
          <el-form-item label="开票日期">
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
        <el-button type="primary" @click="handleAdd">开具发票</el-button>
        <el-button type="success" @click="handleBatchImport">批量导入</el-button>
        <el-button type="warning" @click="handleExport">导出发票</el-button>
        <el-button type="info" @click="handleTaxReport">税务报表</el-button>
      </div>

      <el-table :data="invoiceList" v-loading="loading" stripe>
        <el-table-column type="selection" width="55" />
        <el-table-column prop="invoiceNumber" label="发票号码" width="150" />
        <el-table-column prop="invoiceType" label="发票类型" width="100">
          <template #default="{ row }">
            <el-tag size="small" :type="getTypeTag(row.invoiceType)">
              {{ getTypeText(row.invoiceType) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="partner" label="客户/供应商" min-width="150" />
        <el-table-column prop="issueDate" label="开票日期" width="120" />
        <el-table-column prop="dueDate" label="到期日期" width="120" />
        <el-table-column prop="totalAmount" label="发票金额" width="120">
          <template #default="{ row }">
            <span class="amount">¥{{ row.totalAmount.toFixed(2) }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="taxAmount" label="税额" width="100">
          <template #default="{ row }">
            <span class="tax-amount">¥{{ row.taxAmount.toFixed(2) }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="netAmount" label="不含税金额" width="120">
          <template #default="{ row }">
            <span class="net-amount">¥{{ row.netAmount.toFixed(2) }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="taxRate" label="税率" width="80">
          <template #default="{ row }">
            <span>{{ (row.taxRate * 100).toFixed(1) }}%</span>
          </template>
        </el-table-column>
        <el-table-column prop="status" label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="getStatusTag(row.status)">
              {{ getStatusText(row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="relatedOrder" label="关联订单" width="120" />
        <el-table-column prop="createdBy" label="开票人" width="100" />
        <el-table-column prop="createdAt" label="创建时间" width="160" />
        <el-table-column label="操作" width="200" fixed="right">
          <template #default="{ row }">
            <el-button type="primary" size="small" @click="handleView(row)">查看</el-button>
            <el-button type="warning" size="small" @click="handleEdit(row)" v-if="row.status === 'draft'">编辑</el-button>
            <el-button type="success" size="small" @click="handleSend(row)" v-if="row.status === 'issued'">发送</el-button>
            <el-dropdown trigger="click">
              <el-button type="info" size="small">
                更多<el-icon class="el-icon--right"><arrow-down /></el-icon>
              </el-button>
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item @click="handlePrint(row)">打印发票</el-dropdown-item>
                  <el-dropdown-item @click="handleDownload(row)">下载PDF</el-dropdown-item>
                  <el-dropdown-item @click="handleCopy(row)">复制发票</el-dropdown-item>
                  <el-dropdown-item @click="handlePayment(row)" v-if="row.status === 'sent'">记录收款</el-dropdown-item>
                  <el-dropdown-item divided @click="handleCancel(row)" v-if="['draft', 'issued'].includes(row.status)">作废发票</el-dropdown-item>
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

    <!-- 发票统计卡片 -->
    <div class="stats-cards">
      <el-row :gutter="20">
        <el-col :span="6">
          <div class="stat-card">
            <div class="stat-icon total">
              <el-icon><Document /></el-icon>
            </div>
            <div class="stat-content">
              <div class="stat-value">{{ stats.totalInvoices }}</div>
              <div class="stat-label">总发票数</div>
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
              <div class="stat-label">总开票金额</div>
            </div>
          </div>
        </el-col>
        <el-col :span="6">
          <div class="stat-card">
            <div class="stat-icon tax">
              <el-icon><Coin /></el-icon>
            </div>
            <div class="stat-content">
              <div class="stat-value">¥{{ stats.totalTax.toFixed(0) }}</div>
              <div class="stat-label">总税额</div>
            </div>
          </div>
        </el-col>
        <el-col :span="6">
          <div class="stat-card">
            <div class="stat-icon pending">
              <el-icon><Clock /></el-icon>
            </div>
            <div class="stat-content">
              <div class="stat-value">{{ stats.pendingInvoices }}</div>
              <div class="stat-label">待收款发票</div>
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
import { Document, Money, Coin, Clock, ArrowDown } from '@element-plus/icons-vue'

// 响应式数据
const loading = ref(false)
const invoiceList = ref([])

const filters = reactive({
  invoiceNumber: '',
  invoiceType: '',
  partner: '',
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
    invoiceNumber: 'INV-2024-001',
    invoiceType: 'sales',
    partner: '深圳科技有限公司',
    issueDate: '2024-01-15',
    dueDate: '2024-02-14',
    totalAmount: 11800.00,
    taxAmount: 1800.00,
    netAmount: 10000.00,
    taxRate: 0.18,
    status: 'issued',
    relatedOrder: 'SO-2024-001',
    createdBy: '张会计',
    createdAt: '2024-01-15 10:30:00'
  },
  {
    id: 2,
    invoiceNumber: 'INV-2024-002',
    invoiceType: 'sales',
    partner: '上海制造集团',
    issueDate: '2024-01-16',
    dueDate: '2024-02-15',
    totalAmount: 5900.00,
    taxAmount: 900.00,
    netAmount: 5000.00,
    taxRate: 0.18,
    status: 'sent',
    relatedOrder: 'SO-2024-002',
    createdBy: '李会计',
    createdAt: '2024-01-16 14:20:00'
  },
  {
    id: 3,
    invoiceNumber: 'INV-2024-003',
    invoiceType: 'purchase',
    partner: '北京供应商公司',
    issueDate: '2024-01-17',
    dueDate: '2024-02-16',
    totalAmount: 3540.00,
    taxAmount: 540.00,
    netAmount: 3000.00,
    taxRate: 0.18,
    status: 'paid',
    relatedOrder: 'PO-2024-001',
    createdBy: '王会计',
    createdAt: '2024-01-17 16:45:00'
  },
  {
    id: 4,
    invoiceNumber: 'INV-2024-004',
    invoiceType: 'special',
    partner: '广州贸易公司',
    issueDate: '2024-01-18',
    dueDate: '2024-02-17',
    totalAmount: 2360.00,
    taxAmount: 360.00,
    netAmount: 2000.00,
    taxRate: 0.18,
    status: 'draft',
    relatedOrder: 'SO-2024-003',
    createdBy: '赵会计',
    createdAt: '2024-01-18 11:20:00'
  },
  {
    id: 5,
    invoiceNumber: 'INV-2024-005',
    invoiceType: 'ordinary',
    partner: '杭州创新科技',
    issueDate: '2024-01-19',
    dueDate: '2024-02-18',
    totalAmount: 1770.00,
    taxAmount: 270.00,
    netAmount: 1500.00,
    taxRate: 0.18,
    status: 'cancelled',
    relatedOrder: 'SO-2024-004',
    createdBy: '钱会计',
    createdAt: '2024-01-19 08:30:00'
  }
]

// 计算属性
const stats = computed(() => {
  const total = invoiceList.value.length
  const totalAmount = invoiceList.value.reduce((sum, inv) => sum + inv.totalAmount, 0)
  const totalTax = invoiceList.value.reduce((sum, inv) => sum + inv.taxAmount, 0)
  const pending = invoiceList.value.filter(inv => ['issued', 'sent'].includes(inv.status)).length
  
  return {
    totalInvoices: total,
    totalAmount: totalAmount,
    totalTax: totalTax,
    pendingInvoices: pending
  }
})

// 方法
const fetchInvoices = async () => {
  loading.value = true
  try {
    // 模拟API调用
    await new Promise(resolve => setTimeout(resolve, 500))
    invoiceList.value = mockData
    pagination.total = mockData.length
  } catch (error) {
    ElMessage.error('获取发票列表失败')
  } finally {
    loading.value = false
  }
}

const handleSearch = () => {
  pagination.page = 1
  fetchInvoices()
}

const handleReset = () => {
  Object.assign(filters, {
    invoiceNumber: '',
    invoiceType: '',
    partner: '',
    status: '',
    dateRange: []
  })
  handleSearch()
}

const handleAdd = () => {
  ElMessage.info('开具发票功能开发中')
}

const handleBatchImport = () => {
  ElMessage.info('批量导入功能开发中')
}

const handleExport = () => {
  ElMessage.info('导出功能开发中')
}

const handleTaxReport = () => {
  ElMessage.info('税务报表功能开发中')
}

const handleView = (row) => {
  ElMessage.info(`查看发票: ${row.invoiceNumber}`)
}

const handleEdit = (row) => {
  ElMessage.info(`编辑发票: ${row.invoiceNumber}`)
}

const handleSend = (row) => {
  ElMessage.info(`发送发票: ${row.invoiceNumber}`)
}

const handlePrint = (row) => {
  ElMessage.info(`打印发票: ${row.invoiceNumber}`)
}

const handleDownload = (row) => {
  ElMessage.info(`下载发票: ${row.invoiceNumber}`)
}

const handleCopy = (row) => {
  ElMessage.info(`复制发票: ${row.invoiceNumber}`)
}

const handlePayment = (row) => {
  ElMessage.info(`记录收款: ${row.invoiceNumber}`)
}

const handleCancel = async (row) => {
  try {
    await ElMessageBox.confirm(`确定要作废发票 ${row.invoiceNumber} 吗？`, '作废发票', {
      type: 'warning'
    })
    row.status = 'cancelled'
    ElMessage.success('发票已作废')
  } catch {
    // 用户取消操作
  }
}

const handleSizeChange = (size) => {
  pagination.size = size
  fetchInvoices()
}

const handlePageChange = (page) => {
  pagination.page = page
  fetchInvoices()
}

const getTypeTag = (type) => {
  const tagMap = {
    sales: 'primary',
    purchase: 'success',
    special: 'warning',
    ordinary: 'info'
  }
  return tagMap[type] || 'info'
}

const getTypeText = (type) => {
  const textMap = {
    sales: '销售发票',
    purchase: '采购发票',
    special: '专用发票',
    ordinary: '普通发票'
  }
  return textMap[type] || '未知'
}

const getStatusTag = (status) => {
  const tagMap = {
    draft: 'info',
    issued: 'primary',
    sent: 'warning',
    paid: 'success',
    cancelled: 'danger'
  }
  return tagMap[status] || 'info'
}

const getStatusText = (status) => {
  const textMap = {
    draft: '草稿',
    issued: '已开具',
    sent: '已发送',
    paid: '已收款',
    cancelled: '已作废'
  }
  return textMap[status] || '未知'
}

// 生命周期
onMounted(() => {
  fetchInvoices()
})
</script>

<style scoped>
.invoices {
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

.tax-amount {
  font-weight: 600;
  color: #e6a23c;
}

.net-amount {
  font-weight: 600;
  color: #5c6bc0;
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
  background: #67c23a;
}

.stat-icon.tax {
  background: #e6a23c;
}

.stat-icon.pending {
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