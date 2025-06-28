<template>
  <div class="purchase-orders">
    <div class="page-header">
      <h1>采购订单</h1>
      <p>管理采购订单和供应商采购</p>
    </div>
    
    <div class="content-card">
      <div class="filters">
        <el-form :inline="true" :model="filters" class="filter-form">
          <el-form-item label="订单号">
            <el-input v-model="filters.orderNo" placeholder="请输入订单号" clearable />
          </el-form-item>
          <el-form-item label="供应商">
            <el-input v-model="filters.supplierName" placeholder="请输入供应商名称" clearable />
          </el-form-item>
          <el-form-item label="状态">
            <el-select v-model="filters.status" placeholder="请选择状态" clearable>
              <el-option label="草稿" value="draft" />
              <el-option label="待审核" value="pending" />
              <el-option label="已审核" value="approved" />
              <el-option label="已发送" value="sent" />
              <el-option label="部分收货" value="partial_received" />
              <el-option label="已完成" value="completed" />
              <el-option label="已取消" value="cancelled" />
            </el-select>
          </el-form-item>
          <el-form-item label="采购员">
            <el-select v-model="filters.purchaser" placeholder="请选择采购员" clearable>
              <el-option label="张采购" value="zhang" />
              <el-option label="李采购" value="li" />
              <el-option label="王采购" value="wang" />
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
        <el-button type="primary" @click="handleAdd">新增采购单</el-button>
        <el-button type="success" @click="handleBatchApprove">批量审核</el-button>
        <el-button type="warning" @click="handleExport">导出订单</el-button>
      </div>

      <el-table :data="purchaseOrderList" v-loading="loading" stripe>
        <el-table-column type="selection" width="55" />
        <el-table-column prop="orderNo" label="订单号" width="150" />
        <el-table-column prop="supplierName" label="供应商" min-width="150" />
        <el-table-column prop="contactPerson" label="联系人" width="100" />
        <el-table-column prop="phone" label="联系电话" width="130" />
        <el-table-column prop="totalAmount" label="订单金额" width="120">
          <template #default="{ row }">
            <span class="amount">¥{{ row.totalAmount.toFixed(2) }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="itemCount" label="商品数量" width="100">
          <template #default="{ row }">
            {{ row.itemCount }}种
          </template>
        </el-table-column>
        <el-table-column prop="status" label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="getStatusTag(row.status)">
              {{ getStatusText(row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="expectedDate" label="期望交货" width="120" />
        <el-table-column prop="purchaser" label="采购员" width="100" />
        <el-table-column prop="createdAt" label="创建时间" width="160" />
        <el-table-column label="操作" width="220" fixed="right">
          <template #default="{ row }">
            <el-button type="primary" size="small" @click="handleView(row)">查看</el-button>
            <el-button type="warning" size="small" @click="handleEdit(row)" v-if="canEdit(row)">编辑</el-button>
            <el-button type="success" size="small" @click="handleApprove(row)" v-if="row.status === 'pending'">审核</el-button>
            <el-button type="info" size="small" @click="handleReceive(row)" v-if="canReceive(row)">收货</el-button>
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

    <!-- 采购统计卡片 -->
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
              <div class="stat-label">待审核</div>
            </div>
          </div>
        </el-col>
        <el-col :span="6">
          <div class="stat-card">
            <div class="stat-icon approved">
              <el-icon><Check /></el-icon>
            </div>
            <div class="stat-content">
              <div class="stat-value">{{ stats.approvedOrders }}</div>
              <div class="stat-label">已审核</div>
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
              <div class="stat-label">总金额</div>
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
import { Document, Clock, Check, Money } from '@element-plus/icons-vue'

// 响应式数据
const loading = ref(false)
const purchaseOrderList = ref([])

const filters = reactive({
  orderNo: '',
  supplierName: '',
  status: '',
  purchaser: '',
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
    orderNo: 'PO202401001',
    supplierName: '北京供应商有限公司',
    contactPerson: '张经理',
    phone: '13800138000',
    totalAmount: 125000.00,
    itemCount: 15,
    status: 'approved',
    expectedDate: '2024-02-15',
    purchaser: '张采购',
    createdAt: '2024-01-15 10:30:00'
  },
  {
    id: 2,
    orderNo: 'PO202401002',
    supplierName: '上海材料公司',
    contactPerson: '王总',
    phone: '13800138001',
    totalAmount: 89500.00,
    itemCount: 8,
    status: 'pending',
    expectedDate: '2024-02-20',
    purchaser: '李采购',
    createdAt: '2024-01-15 14:20:00'
  },
  {
    id: 3,
    orderNo: 'PO202401003',
    supplierName: '广州设备企业',
    contactPerson: '刘主管',
    phone: '13800138002',
    totalAmount: 256000.00,
    itemCount: 25,
    status: 'partial_received',
    expectedDate: '2024-02-10',
    purchaser: '王采购',
    createdAt: '2024-01-14 16:45:00'
  },
  {
    id: 4,
    orderNo: 'PO202401004',
    supplierName: '深圳电子公司',
    contactPerson: '陈工程师',
    phone: '13800138003',
    totalAmount: 45000.00,
    itemCount: 12,
    status: 'completed',
    expectedDate: '2024-01-25',
    purchaser: '张采购',
    createdAt: '2024-01-13 11:20:00'
  },
  {
    id: 5,
    orderNo: 'PO202401005',
    supplierName: '杭州原料公司',
    contactPerson: '周总监',
    phone: '13800138004',
    totalAmount: 78000.00,
    itemCount: 6,
    status: 'draft',
    expectedDate: '2024-02-25',
    purchaser: '李采购',
    createdAt: '2024-01-12 08:30:00'
  },
  {
    id: 6,
    orderNo: 'PO202401006',
    supplierName: '天津机械厂',
    contactPerson: '赵厂长',
    phone: '13800138005',
    totalAmount: 180000.00,
    itemCount: 20,
    status: 'sent',
    expectedDate: '2024-03-01',
    purchaser: '王采购',
    createdAt: '2024-01-11 15:45:00'
  }
]

// 计算属性
const stats = computed(() => {
  const total = purchaseOrderList.value.length
  const pending = purchaseOrderList.value.filter(po => po.status === 'pending').length
  const approved = purchaseOrderList.value.filter(po => po.status === 'approved').length
  const totalAmount = purchaseOrderList.value.reduce((sum, po) => sum + po.totalAmount, 0)
  
  return {
    totalOrders: total,
    pendingOrders: pending,
    approvedOrders: approved,
    totalAmount: totalAmount
  }
})

// 方法
const fetchPurchaseOrders = async () => {
  loading.value = true
  try {
    // 模拟API调用
    await new Promise(resolve => setTimeout(resolve, 500))
    purchaseOrderList.value = mockData
    pagination.total = mockData.length
  } catch (error) {
    ElMessage.error('获取采购订单列表失败')
  } finally {
    loading.value = false
  }
}

const handleSearch = () => {
  pagination.page = 1
  fetchPurchaseOrders()
}

const handleReset = () => {
  Object.assign(filters, {
    orderNo: '',
    supplierName: '',
    status: '',
    purchaser: '',
    dateRange: []
  })
  handleSearch()
}

const handleAdd = () => {
  ElMessage.info('新增采购单功能开发中')
}

const handleBatchApprove = () => {
  ElMessage.info('批量审核功能开发中')
}

const handleExport = () => {
  ElMessage.info('导出功能开发中')
}

const handleView = (row) => {
  ElMessage.info(`查看采购单: ${row.orderNo}`)
}

const handleEdit = (row) => {
  ElMessage.info(`编辑采购单: ${row.orderNo}`)
}

const handleApprove = async (row) => {
  try {
    await ElMessageBox.confirm(`确定要审核通过采购单 ${row.orderNo} 吗？`, '审核采购单', {
      type: 'warning'
    })
    row.status = 'approved'
    ElMessage.success('采购单审核通过')
  } catch {
    // 用户取消操作
  }
}

const handleReceive = (row) => {
  ElMessage.info(`收货功能开发中: ${row.orderNo}`)
}

const handleSizeChange = (size) => {
  pagination.size = size
  fetchPurchaseOrders()
}

const handlePageChange = (page) => {
  pagination.page = page
  fetchPurchaseOrders()
}

const getStatusTag = (status) => {
  const tagMap = {
    draft: 'info',
    pending: 'warning',
    approved: 'success',
    sent: 'primary',
    partial_received: 'warning',
    completed: 'success',
    cancelled: 'danger'
  }
  return tagMap[status] || 'info'
}

const getStatusText = (status) => {
  const textMap = {
    draft: '草稿',
    pending: '待审核',
    approved: '已审核',
    sent: '已发送',
    partial_received: '部分收货',
    completed: '已完成',
    cancelled: '已取消'
  }
  return textMap[status] || '未知'
}

const canEdit = (row) => {
  return ['draft', 'pending'].includes(row.status)
}

const canReceive = (row) => {
  return ['approved', 'sent', 'partial_received'].includes(row.status)
}

// 生命周期
onMounted(() => {
  fetchPurchaseOrders()
})
</script>

<style scoped>
.purchase-orders {
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

.stat-icon.approved {
  background: #67c23a;
}

.stat-icon.amount {
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