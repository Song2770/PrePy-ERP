<template>
  <div class="stock-movements">
    <div class="page-header">
      <h1>库存移动</h1>
      <p>管理和查看库存移动记录</p>
    </div>
    
    <div class="content-card">
      <div class="filters">
        <el-form :inline="true" :model="filters" class="filter-form">
          <el-form-item label="产品名称">
            <el-input v-model="filters.productName" placeholder="请输入产品名称" clearable />
          </el-form-item>
          <el-form-item label="移动类型">
            <el-select v-model="filters.movementType" placeholder="请选择移动类型" clearable>
              <el-option label="入库" value="in" />
              <el-option label="出库" value="out" />
              <el-option label="调拨" value="transfer" />
              <el-option label="盘点" value="adjustment" />
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
        <el-button type="primary" @click="handleAdd">新增移动</el-button>
        <el-button type="success" @click="handleExport">导出记录</el-button>
      </div>

      <el-table :data="movementList" v-loading="loading" stripe>
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="productName" label="产品名称" min-width="150" />
        <el-table-column prop="sku" label="SKU" width="120" />
        <el-table-column prop="movementType" label="移动类型" width="100">
          <template #default="{ row }">
            <el-tag :type="getMovementTypeTag(row.movementType)">
              {{ getMovementTypeText(row.movementType) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="quantity" label="数量" width="100">
          <template #default="{ row }">
            <span :class="{ 'text-red': row.movementType === 'out', 'text-green': row.movementType === 'in' }">
              {{ row.movementType === 'out' ? '-' : '+' }}{{ row.quantity }}
            </span>
          </template>
        </el-table-column>
        <el-table-column prop="unit" label="单位" width="80" />
        <el-table-column prop="fromLocation" label="源位置" width="120" />
        <el-table-column prop="toLocation" label="目标位置" width="120" />
        <el-table-column prop="reason" label="移动原因" min-width="150" />
        <el-table-column prop="operator" label="操作人" width="100" />
        <el-table-column prop="createdAt" label="创建时间" width="160" />
        <el-table-column label="操作" width="120" fixed="right">
          <template #default="{ row }">
            <el-button type="primary" size="small" @click="handleView(row)">查看</el-button>
            <el-button type="danger" size="small" @click="handleDelete(row)" v-if="canDelete(row)">删除</el-button>
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
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'

// 响应式数据
const loading = ref(false)
const movementList = ref([])

const filters = reactive({
  productName: '',
  movementType: '',
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
    productName: '苹果手机',
    sku: 'PHONE001',
    movementType: 'in',
    quantity: 50,
    unit: '台',
    fromLocation: '供应商',
    toLocation: '仓库A',
    reason: '采购入库',
    operator: '张三',
    createdAt: '2024-01-15 10:30:00'
  },
  {
    id: 2,
    productName: '笔记本电脑',
    sku: 'LAPTOP001',
    movementType: 'out',
    quantity: 10,
    unit: '台',
    fromLocation: '仓库A',
    toLocation: '客户',
    reason: '销售出库',
    operator: '李四',
    createdAt: '2024-01-15 14:20:00'
  },
  {
    id: 3,
    productName: '无线鼠标',
    sku: 'MOUSE001',
    movementType: 'transfer',
    quantity: 20,
    unit: '个',
    fromLocation: '仓库A',
    toLocation: '仓库B',
    reason: '库存调拨',
    operator: '王五',
    createdAt: '2024-01-15 16:45:00'
  }
]

// 方法
const fetchMovements = async () => {
  loading.value = true
  try {
    // 模拟API调用
    await new Promise(resolve => setTimeout(resolve, 500))
    movementList.value = mockData
    pagination.total = mockData.length
  } catch (error) {
    ElMessage.error('获取库存移动记录失败')
  } finally {
    loading.value = false
  }
}

const handleSearch = () => {
  pagination.page = 1
  fetchMovements()
}

const handleReset = () => {
  Object.assign(filters, {
    productName: '',
    movementType: '',
    dateRange: []
  })
  handleSearch()
}

const handleAdd = () => {
  ElMessage.info('新增移动功能开发中')
}

const handleExport = () => {
  ElMessage.info('导出功能开发中')
}

const handleView = (row) => {
  ElMessage.info(`查看移动记录: ${row.id}`)
}

const handleDelete = async (row) => {
  try {
    await ElMessageBox.confirm('确定要删除这条移动记录吗？', '确认删除', {
      type: 'warning'
    })
    ElMessage.success('删除成功')
    fetchMovements()
  } catch {
    // 用户取消删除
  }
}

const handleSizeChange = (size) => {
  pagination.size = size
  fetchMovements()
}

const handlePageChange = (page) => {
  pagination.page = page
  fetchMovements()
}

const getMovementTypeTag = (type) => {
  const tagMap = {
    in: 'success',
    out: 'danger',
    transfer: 'warning',
    adjustment: 'info'
  }
  return tagMap[type] || 'info'
}

const getMovementTypeText = (type) => {
  const textMap = {
    in: '入库',
    out: '出库',
    transfer: '调拨',
    adjustment: '盘点'
  }
  return textMap[type] || '未知'
}

const canDelete = (row) => {
  // 只有当天创建的记录才能删除
  const today = new Date().toDateString()
  const recordDate = new Date(row.createdAt).toDateString()
  return today === recordDate
}

// 生命周期
onMounted(() => {
  fetchMovements()
})
</script>

<style scoped>
.stock-movements {
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

.text-red {
  color: #f56c6c;
}

.text-green {
  color: #67c23a;
}
</style>