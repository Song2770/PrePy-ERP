<template>
  <div class="products">
    <div class="page-header">
      <h1>产品管理</h1>
      <p>管理产品信息、规格和库存</p>
    </div>
    
    <div class="content-card">
      <div class="filters">
        <el-form :inline="true" :model="filters" class="filter-form">
          <el-form-item label="产品名称">
            <el-input v-model="filters.productName" placeholder="请输入产品名称" clearable />
          </el-form-item>
          <el-form-item label="产品编码">
            <el-input v-model="filters.productCode" placeholder="请输入产品编码" clearable />
          </el-form-item>
          <el-form-item label="产品分类">
            <el-select v-model="filters.category" placeholder="请选择分类" clearable>
              <el-option label="电子产品" value="electronics" />
              <el-option label="机械设备" value="machinery" />
              <el-option label="原材料" value="materials" />
              <el-option label="办公用品" value="office" />
              <el-option label="其他" value="others" />
            </el-select>
          </el-form-item>
          <el-form-item label="状态">
            <el-select v-model="filters.status" placeholder="请选择状态" clearable>
              <el-option label="启用" value="active" />
              <el-option label="停用" value="inactive" />
              <el-option label="缺货" value="out_of_stock" />
            </el-select>
          </el-form-item>
          <el-form-item label="价格范围">
            <el-input-number v-model="filters.minPrice" placeholder="最低价" :min="0" style="width: 120px" />
            <span style="margin: 0 8px">-</span>
            <el-input-number v-model="filters.maxPrice" placeholder="最高价" :min="0" style="width: 120px" />
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="handleSearch">搜索</el-button>
            <el-button @click="handleReset">重置</el-button>
          </el-form-item>
        </el-form>
      </div>

      <div class="table-actions">
        <el-button type="primary" @click="handleAdd">新增产品</el-button>
        <el-button type="success" @click="handleBatchImport">批量导入</el-button>
        <el-button type="warning" @click="handleExport">导出产品</el-button>
      </div>

      <el-table :data="productList" v-loading="loading" stripe>
        <el-table-column type="selection" width="55" />
        <el-table-column label="产品图片" width="80">
          <template #default="{ row }">
            <el-avatar :size="50" :src="row.image" shape="square">
              <el-icon><Picture /></el-icon>
            </el-avatar>
          </template>
        </el-table-column>
        <el-table-column prop="productCode" label="产品编码" width="120" />
        <el-table-column prop="productName" label="产品名称" min-width="150" />
        <el-table-column prop="category" label="分类" width="100">
          <template #default="{ row }">
            <el-tag size="small">{{ getCategoryText(row.category) }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="specification" label="规格" width="120" />
        <el-table-column prop="unit" label="单位" width="80" />
        <el-table-column prop="salePrice" label="销售价" width="100">
          <template #default="{ row }">
            <span class="price">¥{{ row.salePrice.toFixed(2) }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="costPrice" label="成本价" width="100">
          <template #default="{ row }">
            <span class="price">¥{{ row.costPrice.toFixed(2) }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="stockQuantity" label="库存数量" width="100">
          <template #default="{ row }">
            <span :class="getStockClass(row.stockQuantity, row.minStock)">
              {{ row.stockQuantity }}
            </span>
          </template>
        </el-table-column>
        <el-table-column prop="minStock" label="最低库存" width="100" />
        <el-table-column prop="status" label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="getStatusTag(row.status)">
              {{ getStatusText(row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="supplier" label="主要供应商" width="120" />
        <el-table-column prop="createdAt" label="创建时间" width="160" />
        <el-table-column label="操作" width="180" fixed="right">
          <template #default="{ row }">
            <el-button type="primary" size="small" @click="handleView(row)">查看</el-button>
            <el-button type="warning" size="small" @click="handleEdit(row)">编辑</el-button>
            <el-button type="info" size="small" @click="handleStock(row)">库存</el-button>
            <el-dropdown trigger="click">
              <el-button type="info" size="small">
                更多<el-icon class="el-icon--right"><arrow-down /></el-icon>
              </el-button>
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item @click="handleCopy(row)">复制产品</el-dropdown-item>
                  <el-dropdown-item @click="handlePriceHistory(row)">价格历史</el-dropdown-item>
                  <el-dropdown-item @click="handleDisable(row)" v-if="row.status === 'active'">停用</el-dropdown-item>
                  <el-dropdown-item @click="handleEnable(row)" v-if="row.status === 'inactive'">启用</el-dropdown-item>
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

    <!-- 产品统计卡片 -->
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
            <div class="stat-icon active">
              <el-icon><Check /></el-icon>
            </div>
            <div class="stat-content">
              <div class="stat-value">{{ stats.activeProducts }}</div>
              <div class="stat-label">启用产品</div>
            </div>
          </div>
        </el-col>
        <el-col :span="6">
          <div class="stat-card">
            <div class="stat-icon low-stock">
              <el-icon><Warning /></el-icon>
            </div>
            <div class="stat-content">
              <div class="stat-value">{{ stats.lowStockProducts }}</div>
              <div class="stat-label">低库存</div>
            </div>
          </div>
        </el-col>
        <el-col :span="6">
          <div class="stat-card">
            <div class="stat-icon value">
              <el-icon><Money /></el-icon>
            </div>
            <div class="stat-content">
              <div class="stat-value">¥{{ stats.totalValue.toFixed(0) }}</div>
              <div class="stat-label">库存价值</div>
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
import { Picture, Box, Check, Warning, Money, ArrowDown } from '@element-plus/icons-vue'

// 响应式数据
const loading = ref(false)
const productList = ref([])

const filters = reactive({
  productName: '',
  productCode: '',
  category: '',
  status: '',
  minPrice: null,
  maxPrice: null
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
    productCode: 'P001',
    productName: '智能手机外壳',
    category: 'electronics',
    specification: '6.1寸',
    unit: '个',
    salePrice: 25.00,
    costPrice: 15.00,
    stockQuantity: 1500,
    minStock: 100,
    status: 'active',
    supplier: '深圳塑料厂',
    image: '',
    createdAt: '2024-01-15 10:30:00'
  },
  {
    id: 2,
    productCode: 'P002',
    productName: '电路板组件',
    category: 'electronics',
    specification: '10x8cm',
    unit: '块',
    salePrice: 120.00,
    costPrice: 80.00,
    stockQuantity: 50,
    minStock: 100,
    status: 'active',
    supplier: '上海电子公司',
    image: '',
    createdAt: '2024-01-15 14:20:00'
  },
  {
    id: 3,
    productCode: 'P003',
    productName: '显示屏模块',
    category: 'electronics',
    specification: '5.5寸OLED',
    unit: '个',
    salePrice: 180.00,
    costPrice: 120.00,
    stockQuantity: 800,
    minStock: 50,
    status: 'active',
    supplier: '广州显示科技',
    image: '',
    createdAt: '2024-01-14 16:45:00'
  },
  {
    id: 4,
    productCode: 'P004',
    productName: '锂电池组',
    category: 'electronics',
    specification: '3000mAh',
    unit: '组',
    salePrice: 45.00,
    costPrice: 30.00,
    stockQuantity: 0,
    minStock: 200,
    status: 'out_of_stock',
    supplier: '天津电池厂',
    image: '',
    createdAt: '2024-01-13 11:20:00'
  },
  {
    id: 5,
    productCode: 'P005',
    productName: '包装盒',
    category: 'materials',
    specification: '标准包装',
    unit: '个',
    salePrice: 2.50,
    costPrice: 1.20,
    stockQuantity: 5000,
    minStock: 1000,
    status: 'active',
    supplier: '杭州包装公司',
    image: '',
    createdAt: '2024-01-12 08:30:00'
  },
  {
    id: 6,
    productCode: 'P006',
    productName: '螺丝套装',
    category: 'materials',
    specification: 'M2-M5',
    unit: '套',
    salePrice: 8.00,
    costPrice: 5.00,
    stockQuantity: 2000,
    minStock: 500,
    status: 'active',
    supplier: '北京五金厂',
    image: '',
    createdAt: '2024-01-11 15:45:00'
  }
]

// 计算属性
const stats = computed(() => {
  const total = productList.value.length
  const active = productList.value.filter(p => p.status === 'active').length
  const lowStock = productList.value.filter(p => p.stockQuantity <= p.minStock).length
  const totalValue = productList.value.reduce((sum, p) => sum + (p.stockQuantity * p.costPrice), 0)
  
  return {
    totalProducts: total,
    activeProducts: active,
    lowStockProducts: lowStock,
    totalValue: totalValue
  }
})

// 方法
const fetchProducts = async () => {
  loading.value = true
  try {
    // 模拟API调用
    await new Promise(resolve => setTimeout(resolve, 500))
    productList.value = mockData
    pagination.total = mockData.length
  } catch (error) {
    ElMessage.error('获取产品列表失败')
  } finally {
    loading.value = false
  }
}

const handleSearch = () => {
  pagination.page = 1
  fetchProducts()
}

const handleReset = () => {
  Object.assign(filters, {
    productName: '',
    productCode: '',
    category: '',
    status: '',
    minPrice: null,
    maxPrice: null
  })
  handleSearch()
}

const handleAdd = () => {
  ElMessage.info('新增产品功能开发中')
}

const handleBatchImport = () => {
  ElMessage.info('批量导入功能开发中')
}

const handleExport = () => {
  ElMessage.info('导出功能开发中')
}

const handleView = (row) => {
  ElMessage.info(`查看产品: ${row.productName}`)
}

const handleEdit = (row) => {
  ElMessage.info(`编辑产品: ${row.productName}`)
}

const handleStock = (row) => {
  ElMessage.info(`库存管理: ${row.productName}`)
}

const handleCopy = (row) => {
  ElMessage.info(`复制产品: ${row.productName}`)
}

const handlePriceHistory = (row) => {
  ElMessage.info(`价格历史: ${row.productName}`)
}

const handleDisable = async (row) => {
  try {
    await ElMessageBox.confirm(`确定要停用产品 ${row.productName} 吗？`, '停用产品', {
      type: 'warning'
    })
    row.status = 'inactive'
    ElMessage.success('产品已停用')
  } catch {
    // 用户取消操作
  }
}

const handleEnable = async (row) => {
  try {
    await ElMessageBox.confirm(`确定要启用产品 ${row.productName} 吗？`, '启用产品', {
      type: 'warning'
    })
    row.status = 'active'
    ElMessage.success('产品已启用')
  } catch {
    // 用户取消操作
  }
}

const handleSizeChange = (size) => {
  pagination.size = size
  fetchProducts()
}

const handlePageChange = (page) => {
  pagination.page = page
  fetchProducts()
}

const getCategoryText = (category) => {
  const textMap = {
    electronics: '电子产品',
    machinery: '机械设备',
    materials: '原材料',
    office: '办公用品',
    others: '其他'
  }
  return textMap[category] || '未知'
}

const getStatusTag = (status) => {
  const tagMap = {
    active: 'success',
    inactive: 'info',
    out_of_stock: 'danger'
  }
  return tagMap[status] || 'info'
}

const getStatusText = (status) => {
  const textMap = {
    active: '启用',
    inactive: '停用',
    out_of_stock: '缺货'
  }
  return textMap[status] || '未知'
}

const getStockClass = (stock, minStock) => {
  if (stock === 0) return 'stock-zero'
  if (stock <= minStock) return 'stock-low'
  return 'stock-normal'
}

// 生命周期
onMounted(() => {
  fetchProducts()
})
</script>

<style scoped>
.products {
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

.price {
  font-weight: 600;
  color: #67c23a;
}

.stock-normal {
  color: #67c23a;
  font-weight: 600;
}

.stock-low {
  color: #e6a23c;
  font-weight: 600;
}

.stock-zero {
  color: #f56c6c;
  font-weight: 600;
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

.stat-icon.active {
  background: #67c23a;
}

.stat-icon.low-stock {
  background: #e6a23c;
}

.stat-icon.value {
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