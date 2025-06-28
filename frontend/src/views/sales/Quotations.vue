<template>
  <div class="quotations">
    <div class="page-header">
      <h1>销售报价</h1>
      <p>管理销售报价单和客户询价</p>
    </div>
    
    <div class="content-card">
      <div class="filters">
        <el-form :inline="true" :model="filters" class="filter-form">
          <el-form-item label="报价单号">
            <el-input v-model="filters.quotationNo" placeholder="请输入报价单号" clearable />
          </el-form-item>
          <el-form-item label="客户名称">
            <el-input v-model="filters.customerName" placeholder="请输入客户名称" clearable />
          </el-form-item>
          <el-form-item label="状态">
            <el-select v-model="filters.status" placeholder="请选择状态" clearable>
              <el-option label="草稿" value="draft" />
              <el-option label="已发送" value="sent" />
              <el-option label="已接受" value="accepted" />
              <el-option label="已拒绝" value="rejected" />
              <el-option label="已过期" value="expired" />
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
        <el-button type="primary" @click="handleAdd">新增报价</el-button>
        <el-button type="success" @click="handleTemplate">报价模板</el-button>
        <el-button type="warning" @click="handleExport">导出报价</el-button>
      </div>

      <el-table :data="quotationList" v-loading="loading" stripe>
        <el-table-column type="selection" width="55" />
        <el-table-column prop="quotationNo" label="报价单号" width="150" />
        <el-table-column prop="customerName" label="客户名称" min-width="150" />
        <el-table-column prop="contactPerson" label="联系人" width="120" />
        <el-table-column prop="phone" label="联系电话" width="130" />
        <el-table-column prop="totalAmount" label="报价金额" width="120">
          <template #default="{ row }">
            <span class="amount">¥{{ row.totalAmount.toFixed(2) }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="validDays" label="有效期" width="100">
          <template #default="{ row }">
            {{ row.validDays }}天
          </template>
        </el-table-column>
        <el-table-column prop="status" label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="getStatusTag(row.status)">
              {{ getStatusText(row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="expiryDate" label="到期日期" width="120">
          <template #default="{ row }">
            <span :class="{ 'text-danger': isExpiringSoon(row.expiryDate) }">
              {{ row.expiryDate }}
            </span>
          </template>
        </el-table-column>
        <el-table-column prop="salesperson" label="销售员" width="100" />
        <el-table-column prop="createdAt" label="创建时间" width="160" />
        <el-table-column label="操作" width="220" fixed="right">
          <template #default="{ row }">
            <el-button type="primary" size="small" @click="handleView(row)">查看</el-button>
            <el-button type="warning" size="small" @click="handleEdit(row)" v-if="canEdit(row)">编辑</el-button>
            <el-button type="success" size="small" @click="handleSend(row)" v-if="row.status === 'draft'">发送</el-button>
            <el-button type="info" size="small" @click="handleConvert(row)" v-if="row.status === 'accepted'">转订单</el-button>
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

    <!-- 报价统计卡片 -->
    <div class="stats-cards">
      <el-row :gutter="20">
        <el-col :span="6">
          <div class="stat-card">
            <div class="stat-icon total">
              <el-icon><Document /></el-icon>
            </div>
            <div class="stat-content">
              <div class="stat-value">{{ stats.totalQuotations }}</div>
              <div class="stat-label">总报价数</div>
            </div>
          </div>
        </el-col>
        <el-col :span="6">
          <div class="stat-card">
            <div class="stat-icon draft">
              <el-icon><Edit /></el-icon>
            </div>
            <div class="stat-content">
              <div class="stat-value">{{ stats.draftQuotations }}</div>
              <div class="stat-label">草稿</div>
            </div>
          </div>
        </el-col>
        <el-col :span="6">
          <div class="stat-card">
            <div class="stat-icon sent">
              <el-icon><Promotion /></el-icon>
            </div>
            <div class="stat-content">
              <div class="stat-value">{{ stats.sentQuotations }}</div>
              <div class="stat-label">已发送</div>
            </div>
          </div>
        </el-col>
        <el-col :span="6">
          <div class="stat-card">
            <div class="stat-icon accepted">
              <el-icon><Check /></el-icon>
            </div>
            <div class="stat-content">
              <div class="stat-value">{{ stats.acceptedQuotations }}</div>
              <div class="stat-label">已接受</div>
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
import { Document, Edit, Promotion, Check } from '@element-plus/icons-vue'

// 响应式数据
const loading = ref(false)
const quotationList = ref([])

const filters = reactive({
  quotationNo: '',
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
    quotationNo: 'QT202401001',
    customerName: '北京科技有限公司',
    contactPerson: '张经理',
    phone: '13800138000',
    totalAmount: 125000.00,
    validDays: 30,
    status: 'sent',
    expiryDate: '2024-02-15',
    salesperson: '李销售',
    createdAt: '2024-01-15 10:30:00'
  },
  {
    id: 2,
    quotationNo: 'QT202401002',
    customerName: '上海贸易公司',
    contactPerson: '王总',
    phone: '13800138001',
    totalAmount: 89500.00,
    validDays: 15,
    status: 'draft',
    expiryDate: '2024-02-01',
    salesperson: '赵销售',
    createdAt: '2024-01-15 14:20:00'
  },
  {
    id: 3,
    quotationNo: 'QT202401003',
    customerName: '广州制造企业',
    contactPerson: '刘主管',
    phone: '13800138002',
    totalAmount: 256000.00,
    validDays: 45,
    status: 'accepted',
    expiryDate: '2024-03-01',
    salesperson: '李销售',
    createdAt: '2024-01-14 16:45:00'
  },
  {
    id: 4,
    quotationNo: 'QT202401004',
    customerName: '深圳电子公司',
    contactPerson: '陈工程师',
    phone: '13800138003',
    totalAmount: 45000.00,
    validDays: 20,
    status: 'rejected',
    expiryDate: '2024-02-05',
    salesperson: '孙销售',
    createdAt: '2024-01-13 11:20:00'
  },
  {
    id: 5,
    quotationNo: 'QT202401005',
    customerName: '杭州软件公司',
    contactPerson: '周总监',
    phone: '13800138004',
    totalAmount: 78000.00,
    validDays: 30,
    status: 'expired',
    expiryDate: '2024-01-20',
    salesperson: '钱销售',
    createdAt: '2024-01-12 08:30:00'
  }
]

// 计算属性
const stats = computed(() => {
  const total = quotationList.value.length
  const draft = quotationList.value.filter(q => q.status === 'draft').length
  const sent = quotationList.value.filter(q => q.status === 'sent').length
  const accepted = quotationList.value.filter(q => q.status === 'accepted').length
  
  return {
    totalQuotations: total,
    draftQuotations: draft,
    sentQuotations: sent,
    acceptedQuotations: accepted
  }
})

// 方法
const fetchQuotations = async () => {
  loading.value = true
  try {
    // 模拟API调用
    await new Promise(resolve => setTimeout(resolve, 500))
    quotationList.value = mockData
    pagination.total = mockData.length
  } catch (error) {
    ElMessage.error('获取报价列表失败')
  } finally {
    loading.value = false
  }
}

const handleSearch = () => {
  pagination.page = 1
  fetchQuotations()
}

const handleReset = () => {
  Object.assign(filters, {
    quotationNo: '',
    customerName: '',
    status: '',
    dateRange: []
  })
  handleSearch()
}

const handleAdd = () => {
  ElMessage.info('新增报价功能开发中')
}

const handleTemplate = () => {
  ElMessage.info('报价模板功能开发中')
}

const handleExport = () => {
  ElMessage.info('导出功能开发中')
}

const handleView = (row) => {
  ElMessage.info(`查看报价: ${row.quotationNo}`)
}

const handleEdit = (row) => {
  ElMessage.info(`编辑报价: ${row.quotationNo}`)
}

const handleSend = async (row) => {
  try {
    await ElMessageBox.confirm(`确定要发送报价单 ${row.quotationNo} 吗？`, '发送报价', {
      type: 'warning'
    })
    row.status = 'sent'
    ElMessage.success('报价单发送成功')
  } catch {
    // 用户取消操作
  }
}

const handleConvert = async (row) => {
  try {
    await ElMessageBox.confirm(`确定要将报价单 ${row.quotationNo} 转换为销售订单吗？`, '转换订单', {
      type: 'warning'
    })
    ElMessage.success('报价单已转换为销售订单')
  } catch {
    // 用户取消操作
  }
}

const handleSizeChange = (size) => {
  pagination.size = size
  fetchQuotations()
}

const handlePageChange = (page) => {
  pagination.page = page
  fetchQuotations()
}

const getStatusTag = (status) => {
  const tagMap = {
    draft: 'info',
    sent: 'warning',
    accepted: 'success',
    rejected: 'danger',
    expired: 'danger'
  }
  return tagMap[status] || 'info'
}

const getStatusText = (status) => {
  const textMap = {
    draft: '草稿',
    sent: '已发送',
    accepted: '已接受',
    rejected: '已拒绝',
    expired: '已过期'
  }
  return textMap[status] || '未知'
}

const canEdit = (row) => {
  return ['draft', 'sent'].includes(row.status)
}

const isExpiringSoon = (expiryDate) => {
  const today = new Date()
  const expiry = new Date(expiryDate)
  const diffTime = expiry.getTime() - today.getTime()
  const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))
  return diffDays <= 7 && diffDays > 0
}

// 生命周期
onMounted(() => {
  fetchQuotations()
})
</script>

<style scoped>
.quotations {
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

.text-danger {
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

.stat-icon.draft {
  background: #909399;
}

.stat-icon.sent {
  background: #e6a23c;
}

.stat-icon.accepted {
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