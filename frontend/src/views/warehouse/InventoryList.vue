<template>
  <div class="page-container">
    <div class="page-header">
      <h1 class="page-title">库存管理</h1>
      <div class="page-actions">
        <el-button type="primary" @click="showAdjustDialog = true">
          <el-icon><Edit /></el-icon>
          库存调整
        </el-button>
        <el-button @click="exportInventory">
          <el-icon><Download /></el-icon>
          导出库存
        </el-button>
      </div>
    </div>

    <!-- 搜索和筛选 -->
    <el-card class="search-card" shadow="never">
      <el-form :model="searchForm" inline>
        <el-form-item label="商品名称">
          <el-input
            v-model="searchForm.productName"
            placeholder="请输入商品名称"
            clearable
            style="width: 200px"
          />
        </el-form-item>
        
        <el-form-item label="商品编码">
          <el-input
            v-model="searchForm.productCode"
            placeholder="请输入商品编码"
            clearable
            style="width: 200px"
          />
        </el-form-item>
        
        <el-form-item label="仓库">
          <el-select
            v-model="searchForm.warehouseId"
            placeholder="请选择仓库"
            clearable
            style="width: 200px"
          >
            <el-option
              v-for="warehouse in warehouses"
              :key="warehouse.id"
              :label="warehouse.name"
              :value="warehouse.id"
            />
          </el-select>
        </el-form-item>
        
        <el-form-item label="库存状态">
          <el-select
            v-model="searchForm.stockStatus"
            placeholder="请选择库存状态"
            clearable
            style="width: 150px"
          >
            <el-option label="正常" value="normal" />
            <el-option label="低库存" value="low" />
            <el-option label="缺货" value="out" />
            <el-option label="超储" value="over" />
          </el-select>
        </el-form-item>
        
        <el-form-item label="商品分类">
          <el-select
            v-model="searchForm.categoryId"
            placeholder="请选择分类"
            clearable
            style="width: 150px"
          >
            <el-option
              v-for="category in categories"
              :key="category.id"
              :label="category.name"
              :value="category.id"
            />
          </el-select>
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

    <!-- 统计卡片 -->
    <el-row :gutter="16" class="stats-row">
      <el-col :span="6">
        <el-card class="stat-card" shadow="never">
          <div class="stat-content">
            <div class="stat-value">{{ stats.totalProducts }}</div>
            <div class="stat-label">商品总数</div>
          </div>
          <div class="stat-icon">
            <el-icon><Box /></el-icon>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card" shadow="never">
          <div class="stat-content">
            <div class="stat-value">{{ stats.lowStockProducts }}</div>
            <div class="stat-label">低库存商品</div>
          </div>
          <div class="stat-icon warning">
            <el-icon><Warning /></el-icon>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card" shadow="never">
          <div class="stat-content">
            <div class="stat-value">{{ stats.outOfStockProducts }}</div>
            <div class="stat-label">缺货商品</div>
          </div>
          <div class="stat-icon danger">
            <el-icon><Close /></el-icon>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card" shadow="never">
          <div class="stat-content">
            <div class="stat-value">¥{{ formatCurrency(stats.totalValue) }}</div>
            <div class="stat-label">库存总价值</div>
          </div>
          <div class="stat-icon success">
            <el-icon><Money /></el-icon>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 库存列表 -->
    <el-card shadow="never">
      <el-table
        v-loading="loading"
        :data="inventoryList"
        stripe
        @selection-change="handleSelectionChange"
      >
        <el-table-column type="selection" width="55" />
        
        <el-table-column label="商品" width="250">
          <template #default="{ row }">
            <div class="product-info">
              <div class="product-name">{{ row.product_name }}</div>
              <div class="product-code">{{ row.product_code }}</div>
            </div>
          </template>
        </el-table-column>
        
        <el-table-column prop="product_spec" label="规格" width="120" />
        <el-table-column prop="product_unit" label="单位" width="80" />
        <el-table-column prop="warehouse_name" label="仓库" width="120" />
        
        <el-table-column label="当前库存" width="120" align="right">
          <template #default="{ row }">
            <span :class="getStockClass(row)">
              {{ row.current_stock }}
            </span>
          </template>
        </el-table-column>
        
        <el-table-column prop="available_stock" label="可用库存" width="120" align="right" />
        <el-table-column prop="reserved_stock" label="预留库存" width="120" align="right" />
        
        <el-table-column label="库存状态" width="100">
          <template #default="{ row }">
            <el-tag :type="getStockStatusType(row)">
              {{ getStockStatusText(row) }}
            </el-tag>
          </template>
        </el-table-column>
        
        <el-table-column label="安全库存" width="100" align="right">
          <template #default="{ row }">
            <span>{{ row.safety_stock || 0 }}</span>
          </template>
        </el-table-column>
        
        <el-table-column label="最大库存" width="100" align="right">
          <template #default="{ row }">
            <span>{{ row.max_stock || '-' }}</span>
          </template>
        </el-table-column>
        
        <el-table-column label="单价" width="100" align="right">
          <template #default="{ row }">
            ¥{{ formatCurrency(row.unit_cost) }}
          </template>
        </el-table-column>
        
        <el-table-column label="库存价值" width="120" align="right">
          <template #default="{ row }">
            <span class="amount-text">
              ¥{{ formatCurrency(row.current_stock * row.unit_cost) }}
            </span>
          </template>
        </el-table-column>
        
        <el-table-column prop="last_movement_date" label="最后变动" width="120">
          <template #default="{ row }">
            {{ formatDate(row.last_movement_date) }}
          </template>
        </el-table-column>
        
        <el-table-column label="操作" width="150" fixed="right">
          <template #default="{ row }">
            <el-button
              type="primary"
              size="small"
              @click="viewStockDetail(row)"
            >
              详情
            </el-button>
            
            <el-button
              type="warning"
              size="small"
              @click="adjustStock(row)"
            >
              调整
            </el-button>
          </template>
        </el-table-column>
      </el-table>
      
      <!-- 分页 -->
      <div class="pagination-container">
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
    </el-card>

    <!-- 库存调整对话框 -->
    <el-dialog
      v-model="showAdjustDialog"
      title="库存调整"
      width="600px"
    >
      <StockAdjustForm
        v-if="showAdjustDialog"
        :product="selectedProduct"
        @success="handleAdjustSuccess"
        @cancel="showAdjustDialog = false"
      />
    </el-dialog>

    <!-- 库存详情对话框 -->
    <el-dialog
      v-model="showDetailDialog"
      title="库存详情"
      width="800px"
    >
      <StockDetail
        v-if="showDetailDialog"
        :product="selectedProduct"
        @close="showDetailDialog = false"
      />
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { api } from '@/utils/api'
import StockAdjustForm from './components/StockAdjustForm.vue'
import StockDetail from './components/StockDetail.vue'

// 响应式数据
const loading = ref(false)
const inventoryList = ref([])
const warehouses = ref([])
const categories = ref([])
const selectedInventory = ref([])
const showAdjustDialog = ref(false)
const showDetailDialog = ref(false)
const selectedProduct = ref(null)

// 统计数据
const stats = reactive({
  totalProducts: 0,
  lowStockProducts: 0,
  outOfStockProducts: 0,
  totalValue: 0
})

// 搜索表单
const searchForm = reactive({
  productName: '',
  productCode: '',
  warehouseId: null,
  stockStatus: '',
  categoryId: null
})

// 分页
const pagination = reactive({
  page: 1,
  size: 20,
  total: 0
})

// 获取库存状态
const getStockStatus = (row) => {
  if (row.current_stock <= 0) return 'out'
  if (row.current_stock <= row.safety_stock) return 'low'
  if (row.max_stock && row.current_stock >= row.max_stock) return 'over'
  return 'normal'
}

// 获取库存状态文本
const getStockStatusText = (row) => {
  const status = getStockStatus(row)
  const statusMap = {
    normal: '正常',
    low: '低库存',
    out: '缺货',
    over: '超储'
  }
  return statusMap[status] || '正常'
}

// 获取库存状态类型
const getStockStatusType = (row) => {
  const status = getStockStatus(row)
  const typeMap = {
    normal: 'success',
    low: 'warning',
    out: 'danger',
    over: 'info'
  }
  return typeMap[status] || 'success'
}

// 获取库存数量样式
const getStockClass = (row) => {
  const status = getStockStatus(row)
  return {
    'stock-normal': status === 'normal',
    'stock-low': status === 'low',
    'stock-out': status === 'out',
    'stock-over': status === 'over'
  }
}

// 格式化日期
const formatDate = (date) => {
  if (!date) return '-'
  return new Date(date).toLocaleDateString('zh-CN')
}

// 格式化货币
const formatCurrency = (amount) => {
  if (!amount) return '0.00'
  return Number(amount).toLocaleString('zh-CN', {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2
  })
}

// 获取库存列表
const fetchInventoryList = async () => {
  try {
    loading.value = true
    const params = {
      page: pagination.page,
      size: pagination.size,
      ...searchForm
    }
    
    const response = await api.get('/warehouse/inventory', { params })
    inventoryList.value = response.data.items || []
    pagination.total = response.data.total || 0
  } catch (error) {
    console.error('获取库存列表失败:', error)
    ElMessage.error('获取库存列表失败')
  } finally {
    loading.value = false
  }
}

// 获取统计数据
const fetchStats = async () => {
  try {
    const response = await api.get('/warehouse/inventory/stats')
    Object.assign(stats, response.data)
  } catch (error) {
    console.error('获取统计数据失败:', error)
  }
}

// 获取仓库列表
const fetchWarehouses = async () => {
  try {
    const response = await api.get('/warehouses')
    warehouses.value = response.data.items || []
  } catch (error) {
    console.error('获取仓库列表失败:', error)
  }
}

// 获取分类列表
const fetchCategories = async () => {
  try {
    const response = await api.get('/categories')
    categories.value = response.data.items || []
  } catch (error) {
    console.error('获取分类列表失败:', error)
  }
}

// 搜索
const handleSearch = () => {
  pagination.page = 1
  fetchInventoryList()
}

// 重置
const handleReset = () => {
  Object.assign(searchForm, {
    productName: '',
    productCode: '',
    warehouseId: null,
    stockStatus: '',
    categoryId: null
  })
  pagination.page = 1
  fetchInventoryList()
}

// 分页变化
const handleSizeChange = (size) => {
  pagination.size = size
  pagination.page = 1
  fetchInventoryList()
}

const handleCurrentChange = (page) => {
  pagination.page = page
  fetchInventoryList()
}

// 选择变化
const handleSelectionChange = (selection) => {
  selectedInventory.value = selection
}

// 查看库存详情
const viewStockDetail = (row) => {
  selectedProduct.value = row
  showDetailDialog.value = true
}

// 调整库存
const adjustStock = (row) => {
  selectedProduct.value = row
  showAdjustDialog.value = true
}

// 导出库存
const exportInventory = async () => {
  try {
    const response = await api.get('/warehouse/inventory/export', {
      params: searchForm,
      responseType: 'blob'
    })
    
    const url = window.URL.createObjectURL(new Blob([response.data]))
    const link = document.createElement('a')
    link.href = url
    link.setAttribute('download', `库存报表_${new Date().toISOString().split('T')[0]}.xlsx`)
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    window.URL.revokeObjectURL(url)
    
    ElMessage.success('库存报表导出成功')
  } catch (error) {
    console.error('导出库存报表失败:', error)
    ElMessage.error('导出库存报表失败')
  }
}

// 调整成功
const handleAdjustSuccess = () => {
  showAdjustDialog.value = false
  fetchInventoryList()
  fetchStats()
  ElMessage.success('库存调整成功')
}

// 组件挂载
onMounted(() => {
  fetchInventoryList()
  fetchStats()
  fetchWarehouses()
  fetchCategories()
})
</script>

<style scoped>
.search-card {
  margin-bottom: 16px;
}

.stats-row {
  margin-bottom: 16px;
}

.stat-card {
  position: relative;
  overflow: hidden;
}

.stat-card :deep(.el-card__body) {
  padding: 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.stat-content {
  flex: 1;
}

.stat-value {
  font-size: 28px;
  font-weight: 600;
  color: #303133;
  line-height: 1;
  margin-bottom: 8px;
}

.stat-label {
  font-size: 14px;
  color: #909399;
}

.stat-icon {
  font-size: 40px;
  color: #5c6bc0;
  opacity: 0.8;
}

.stat-icon.warning {
  color: #e6a23c;
}

.stat-icon.danger {
  color: #f56c6c;
}

.stat-icon.success {
  color: #67c23a;
}

.pagination-container {
  margin-top: 16px;
  text-align: right;
}

.product-info {
  line-height: 1.4;
}

.product-name {
  font-weight: 600;
  color: #303133;
}

.product-code {
  font-size: 12px;
  color: #909399;
}

.amount-text {
  font-weight: 600;
  color: #5c6bc0;
}

/* 库存状态样式 */
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

.stock-over {
  color: #5c6bc0;
  font-weight: 600;
}

:deep(.el-table .el-table__cell) {
  padding: 8px 0;
}

:deep(.el-form--inline .el-form-item) {
  margin-right: 16px;
  margin-bottom: 16px;
}
</style>