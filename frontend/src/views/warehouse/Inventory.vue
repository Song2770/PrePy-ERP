<template>
  <div class="inventory">
    <div class="page-header">
      <h1>库存管理</h1>
      <p>查看和管理产品库存信息</p>
    </div>
    
    <div class="content-card">
      <div class="filters">
        <el-form :inline="true" :model="filters" class="filter-form">
          <el-form-item label="产品名称">
            <el-input v-model="filters.productName" placeholder="请输入产品名称" clearable />
          </el-form-item>
          <el-form-item label="SKU">
            <el-input v-model="filters.sku" placeholder="请输入SKU" clearable />
          </el-form-item>
          <el-form-item label="分类">
            <el-select v-model="filters.category" placeholder="请选择分类" clearable>
              <el-option label="电子产品" value="electronics" />
              <el-option label="服装" value="clothing" />
              <el-option label="食品" value="food" />
              <el-option label="家具" value="furniture" />
            </el-select>
          </el-form-item>
          <el-form-item label="库存状态">
            <el-select v-model="filters.stockStatus" placeholder="请选择库存状态" clearable>
              <el-option label="正常" value="normal" />
              <el-option label="低库存" value="low" />
              <el-option label="缺货" value="out" />
              <el-option label="超量" value="excess" />
            </el-select>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="handleSearch">搜索</el-button>
            <el-button @click="handleReset">重置</el-button>
          </el-form-item>
        </el-form>
      </div>

      <div class="table-actions">
        <el-button type="primary" @click="handleAdd">新增产品</el-button>
        <el-button type="success" @click="handleImport">批量导入</el-button>
        <el-button type="warning" @click="handleExport">导出数据</el-button>
        <el-button type="info" @click="handleStockCheck">库存盘点</el-button>
      </div>

      <el-table :data="inventoryList" v-loading="loading" stripe>
        <el-table-column type="selection" width="55" />
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="productName" label="产品名称" min-width="150" />
        <el-table-column prop="sku" label="SKU" width="120" />
        <el-table-column prop="category" label="分类" width="100" />
        <el-table-column prop="currentStock" label="当前库存" width="100">
          <template #default="{ row }">
            <span :class="getStockClass(row)">
              {{ row.currentStock }}
            </span>
          </template>
        </el-table-column>
        <el-table-column prop="unit" label="单位" width="80" />
        <el-table-column prop="minStock" label="最低库存" width="100" />
        <el-table-column prop="maxStock" label="最高库存" width="100" />
        <el-table-column prop="location" label="存储位置" width="120" />
        <el-table-column prop="unitPrice" label="单价" width="100">
          <template #default="{ row }">
            ¥{{ row.unitPrice.toFixed(2) }}
          </template>
        </el-table-column>
        <el-table-column prop="totalValue" label="库存价值" width="120">
          <template #default="{ row }">
            ¥{{ (row.currentStock * row.unitPrice).toFixed(2) }}
          </template>
        </el-table-column>
        <el-table-column prop="stockStatus" label="库存状态" width="100">
          <template #default="{ row }">
            <el-tag :type="getStatusTag(row.stockStatus)">
              {{ getStatusText(row.stockStatus) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="lastUpdated" label="最后更新" width="160" />
        <el-table-column label="操作" width="180" fixed="right">
          <template #default="{ row }">
            <el-button type="primary" size="small" @click="handleView(row)">查看</el-button>
            <el-button type="warning" size="small" @click="handleEdit(row)">编辑</el-button>
            <el-button type="info" size="small" @click="handleAdjust(row)">调整</el-button>
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

    <!-- 库存统计卡片 -->
    <div class="stats-cards">
      <el-row :gutter="20">
        <el-col :span="6">
          <div class="stat-card">
            <div class="stat-icon total">
              <el-icon><Box /></el-icon>
            </div>
            <div class="stat-content">
              <div class="stat-value">{{ stats.totalProducts }}</div>
              <div class="stat-label">总产品数</div>
            </div>
          </div>
        </el-col>
        <el-col :span="6">
          <div class="stat-card">
            <div class="stat-icon normal">
              <el-icon><Check /></el-icon>
            </div>
            <div class="stat-content">
              <div class="stat-value">{{ stats.normalStock }}</div>
              <div class="stat-label">正常库存</div>
            </div>
          </div>
        </el-col>
        <el-col :span="6">
          <div class="stat-card">
            <div class="stat-icon warning">
              <el-icon><Warning /></el-icon>
            </div>
            <div class="stat-content">
              <div class="stat-value">{{ stats.lowStock }}</div>
              <div class="stat-label">低库存</div>
            </div>
          </div>
        </el-col>
        <el-col :span="6">
          <div class="stat-card">
            <div class="stat-icon danger">
              <el-icon><Close /></el-icon>
            </div>
            <div class="stat-content">
              <div class="stat-value">{{ stats.outOfStock }}</div>
              <div class="stat-label">缺货</div>
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
import { Box, Check, Warning, Close } from '@element-plus/icons-vue'

// 响应式数据
const loading = ref(false)
const inventoryList = ref([])

const filters = reactive({
  productName: '',
  sku: '',
  category: '',
  stockStatus: ''
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
    category: 'electronics',
    currentStock: 150,
    unit: '台',
    minStock: 50,
    maxStock: 500,
    location: '仓库A-01',
    unitPrice: 5999.00,
    stockStatus: 'normal',
    lastUpdated: '2024-01-15 10:30:00'
  },
  {
    id: 2,
    productName: '笔记本电脑',
    sku: 'LAPTOP001',
    category: 'electronics',
    currentStock: 25,
    unit: '台',
    minStock: 30,
    maxStock: 200,
    location: '仓库A-02',
    unitPrice: 8999.00,
    stockStatus: 'low',
    lastUpdated: '2024-01-15 14:20:00'
  },
  {
    id: 3,
    productName: '无线鼠标',
    sku: 'MOUSE001',
    category: 'electronics',
    currentStock: 0,
    unit: '个',
    minStock: 20,
    maxStock: 100,
    location: '仓库B-01',
    unitPrice: 199.00,
    stockStatus: 'out',
    lastUpdated: '2024-01-15 16:45:00'
  },
  {
    id: 4,
    productName: '办公椅',
    sku: 'CHAIR001',
    category: 'furniture',
    currentStock: 80,
    unit: '把',
    minStock: 10,
    maxStock: 50,
    location: '仓库C-01',
    unitPrice: 899.00,
    stockStatus: 'excess',
    lastUpdated: '2024-01-15 18:10:00'
  }
]

// 计算属性
const stats = computed(() => {
  const total = inventoryList.value.length
  const normal = inventoryList.value.filter(item => item.stockStatus === 'normal').length
  const low = inventoryList.value.filter(item => item.stockStatus === 'low').length
  const out = inventoryList.value.filter(item => item.stockStatus === 'out').length
  
  return {
    totalProducts: total,
    normalStock: normal,
    lowStock: low,
    outOfStock: out
  }
})

// 方法
const fetchInventory = async () => {
  loading.value = true
  try {
    // 模拟API调用
    await new Promise(resolve => setTimeout(resolve, 500))
    inventoryList.value = mockData
    pagination.total = mockData.length
  } catch (error) {
    ElMessage.error('获取库存数据失败')
  } finally {
    loading.value = false
  }
}

const handleSearch = () => {
  pagination.page = 1
  fetchInventory()
}

const handleReset = () => {
  Object.assign(filters, {
    productName: '',
    sku: '',
    category: '',
    stockStatus: ''
  })
  handleSearch()
}

const handleAdd = () => {
  ElMessage.info('新增产品功能开发中')
}

const handleImport = () => {
  ElMessage.info('批量导入功能开发中')
}

const handleExport = () => {
  ElMessage.info('导出功能开发中')
}

const handleStockCheck = () => {
  ElMessage.info('库存盘点功能开发中')
}

const handleView = (row) => {
  ElMessage.info(`查看产品: ${row.productName}`)
}

const handleEdit = (row) => {
  ElMessage.info(`编辑产品: ${row.productName}`)
}

const handleAdjust = (row) => {
  ElMessage.info(`调整库存: ${row.productName}`)
}

const handleSizeChange = (size) => {
  pagination.size = size
  fetchInventory()
}

const handlePageChange = (page) => {
  pagination.page = page
  fetchInventory()
}

const getStockClass = (row) => {
  if (row.currentStock === 0) return 'stock-out'
  if (row.currentStock <= row.minStock) return 'stock-low'
  if (row.currentStock >= row.maxStock) return 'stock-excess'
  return 'stock-normal'
}

const getStatusTag = (status) => {
  const tagMap = {
    normal: 'success',
    low: 'warning',
    out: 'danger',
    excess: 'info'
  }
  return tagMap[status] || 'info'
}

const getStatusText = (status) => {
  const textMap = {
    normal: '正常',
    low: '低库存',
    out: '缺货',
    excess: '超量'
  }
  return textMap[status] || '未知'
}

// 生命周期
onMounted(() => {
  fetchInventory()
})
</script>

<style scoped>
.inventory {
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

.stat-icon.normal {
  background: #67c23a;
}

.stat-icon.warning {
  background: #e6a23c;
}

.stat-icon.danger {
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

.stock-normal {
  color: #67c23a;
  font-weight: 600;
}

.stock-low {
  color: #e6a23c;
  font-weight: 600;
}

.stock-out {
  color: #f56c6c;
  font-weight: 600;
}

.stock-excess {
  color: #909399;
  font-weight: 600;
}
</style>