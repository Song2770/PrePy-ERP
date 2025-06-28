<template>
  <div class="inventory-detail">
    <!-- 商品基本信息 -->
    <div class="detail-section">
      <h3 class="section-title">商品信息</h3>
      <el-row :gutter="20">
        <el-col :span="12">
          <div class="info-item">
            <label>商品名称：</label>
            <span>{{ inventory.product_name }}</span>
          </div>
          <div class="info-item">
            <label>商品编码：</label>
            <span>{{ inventory.product_code }}</span>
          </div>
          <div class="info-item">
            <label>商品分类：</label>
            <span>{{ inventory.category_name }}</span>
          </div>
          <div class="info-item">
            <label>规格型号：</label>
            <span>{{ inventory.product_spec || '-' }}</span>
          </div>
        </el-col>
        <el-col :span="12">
          <div class="info-item">
            <label>计量单位：</label>
            <span>{{ inventory.product_unit }}</span>
          </div>
          <div class="info-item">
            <label>仓库：</label>
            <span>{{ inventory.warehouse_name }}</span>
          </div>
          <div class="info-item">
            <label>存储位置：</label>
            <span>{{ inventory.storage_location || '-' }}</span>
          </div>
          <div class="info-item">
            <label>状态：</label>
            <el-tag :type="getStatusType(inventory.status)">{{ getStatusText(inventory.status) }}</el-tag>
          </div>
        </el-col>
      </el-row>
    </div>

    <!-- 库存信息 -->
    <div class="detail-section">
      <h3 class="section-title">库存信息</h3>
      <el-row :gutter="20">
        <el-col :span="6">
          <div class="stock-card">
            <div class="stock-label">当前库存</div>
            <div class="stock-value current">{{ inventory.current_stock }}</div>
          </div>
        </el-col>
        <el-col :span="6">
          <div class="stock-card">
            <div class="stock-label">可用库存</div>
            <div class="stock-value available">{{ inventory.available_stock }}</div>
          </div>
        </el-col>
        <el-col :span="6">
          <div class="stock-card">
            <div class="stock-label">预留库存</div>
            <div class="stock-value reserved">{{ inventory.reserved_stock }}</div>
          </div>
        </el-col>
        <el-col :span="6">
          <div class="stock-card">
            <div class="stock-label">在途库存</div>
            <div class="stock-value transit">{{ inventory.transit_stock || 0 }}</div>
          </div>
        </el-col>
      </el-row>
      
      <el-row :gutter="20" style="margin-top: 20px;">
        <el-col :span="6">
          <div class="stock-card">
            <div class="stock-label">安全库存</div>
            <div class="stock-value safety">{{ inventory.safety_stock }}</div>
          </div>
        </el-col>
        <el-col :span="6">
          <div class="stock-card">
            <div class="stock-label">最大库存</div>
            <div class="stock-value max">{{ inventory.max_stock }}</div>
          </div>
        </el-col>
        <el-col :span="6">
          <div class="stock-card">
            <div class="stock-label">单位成本</div>
            <div class="stock-value cost">¥{{ inventory.unit_cost }}</div>
          </div>
        </el-col>
        <el-col :span="6">
          <div class="stock-card">
            <div class="stock-label">库存价值</div>
            <div class="stock-value value">¥{{ inventory.total_value }}</div>
          </div>
        </el-col>
      </el-row>
    </div>

    <!-- 批次信息 -->
    <div v-if="batches.length > 0" class="detail-section">
      <h3 class="section-title">批次信息</h3>
      <el-table :data="batches" border>
        <el-table-column prop="batch_number" label="批次号" width="150" />
        <el-table-column prop="quantity" label="数量" width="100" align="right" />
        <el-table-column prop="production_date" label="生产日期" width="120" />
        <el-table-column prop="expiry_date" label="有效期至" width="120" />
        <el-table-column prop="supplier_batch" label="供应商批次" width="150" />
        <el-table-column prop="location" label="存储位置" />
        <el-table-column label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="getBatchStatusType(row.status)">{{ getBatchStatusText(row.status) }}</el-tag>
          </template>
        </el-table-column>
      </el-table>
    </div>

    <!-- 最近库存变动 -->
    <div class="detail-section">
      <h3 class="section-title">最近库存变动</h3>
      <el-table :data="movements" border v-loading="movementsLoading">
        <el-table-column prop="movement_date" label="变动日期" width="120" />
        <el-table-column label="变动类型" width="120">
          <template #default="{ row }">
            <el-tag :type="getMovementType(row.movement_type)">{{ getMovementText(row.movement_type) }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="reference_number" label="单据号" width="150" />
        <el-table-column label="变动数量" width="120" align="right">
          <template #default="{ row }">
            <span :class="getQuantityClass(row.movement_type)">{{ formatQuantity(row) }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="balance_after" label="变动后库存" width="120" align="right" />
        <el-table-column prop="unit_cost" label="单位成本" width="100" align="right">
          <template #default="{ row }">
            <span>¥{{ row.unit_cost }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="operator" label="操作人" width="100" />
        <el-table-column prop="notes" label="备注" show-overflow-tooltip />
      </el-table>
      
      <!-- 分页 -->
      <div class="pagination-wrapper">
        <el-pagination
          v-model:current-page="movementPage.current"
          v-model:page-size="movementPage.size"
          :total="movementPage.total"
          :page-sizes="[10, 20, 50]"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="fetchMovements"
          @current-change="fetchMovements"
        />
      </div>
    </div>

    <!-- 预警信息 -->
    <div v-if="hasWarnings" class="detail-section">
      <h3 class="section-title">预警信息</h3>
      <div class="warning-list">
        <el-alert
          v-for="warning in warnings"
          :key="warning.type"
          :title="warning.title"
          :description="warning.description"
          :type="warning.level"
          show-icon
          :closable="false"
          style="margin-bottom: 12px;"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { api } from '@/utils/api'

// 定义属性
const props = defineProps({
  inventory: {
    type: Object,
    required: true
  }
})

// 响应式数据
const batches = ref([])
const movements = ref([])
const movementsLoading = ref(false)

// 分页数据
const movementPage = reactive({
  current: 1,
  size: 10,
  total: 0
})

// 计算预警信息
const warnings = computed(() => {
  const result = []
  const inventory = props.inventory
  
  // 库存不足预警
  if (inventory.current_stock <= inventory.safety_stock) {
    result.push({
      type: 'low_stock',
      title: '库存不足预警',
      description: `当前库存 ${inventory.current_stock} 已低于安全库存 ${inventory.safety_stock}`,
      level: inventory.current_stock <= 0 ? 'error' : 'warning'
    })
  }
  
  // 库存过量预警
  if (inventory.current_stock > inventory.max_stock) {
    result.push({
      type: 'over_stock',
      title: '库存过量预警',
      description: `当前库存 ${inventory.current_stock} 已超过最大库存 ${inventory.max_stock}`,
      level: 'warning'
    })
  }
  
  // 长期无变动预警
  const lastMovementDate = new Date(inventory.last_movement_date)
  const daysSinceLastMovement = Math.floor((new Date() - lastMovementDate) / (1000 * 60 * 60 * 24))
  if (daysSinceLastMovement > 90) {
    result.push({
      type: 'no_movement',
      title: '长期无变动预警',
      description: `该商品已 ${daysSinceLastMovement} 天无库存变动`,
      level: 'info'
    })
  }
  
  return result
})

const hasWarnings = computed(() => warnings.value.length > 0)

// 获取状态类型
const getStatusType = (status) => {
  const statusMap = {
    'active': 'success',
    'inactive': 'info',
    'discontinued': 'danger'
  }
  return statusMap[status] || 'info'
}

// 获取状态文本
const getStatusText = (status) => {
  const statusMap = {
    'active': '正常',
    'inactive': '停用',
    'discontinued': '停产'
  }
  return statusMap[status] || '未知'
}

// 获取批次状态类型
const getBatchStatusType = (status) => {
  const statusMap = {
    'normal': 'success',
    'expired': 'danger',
    'near_expiry': 'warning'
  }
  return statusMap[status] || 'info'
}

// 获取批次状态文本
const getBatchStatusText = (status) => {
  const statusMap = {
    'normal': '正常',
    'expired': '已过期',
    'near_expiry': '临期'
  }
  return statusMap[status] || '未知'
}

// 获取变动类型
const getMovementType = (type) => {
  const typeMap = {
    'in': 'success',
    'out': 'danger',
    'adjustment': 'warning',
    'transfer': 'info'
  }
  return typeMap[type] || 'info'
}

// 获取变动文本
const getMovementText = (type) => {
  const typeMap = {
    'in': '入库',
    'out': '出库',
    'adjustment': '调整',
    'transfer': '调拨'
  }
  return typeMap[type] || '未知'
}

// 获取数量样式
const getQuantityClass = (type) => {
  return type === 'in' ? 'quantity-in' : 'quantity-out'
}

// 格式化数量
const formatQuantity = (row) => {
  const prefix = row.movement_type === 'in' ? '+' : '-'
  return `${prefix}${row.quantity}`
}

// 获取批次信息
const fetchBatches = async () => {
  try {
    const response = await api.get(`/warehouse/inventory/${props.inventory.id}/batches`)
    batches.value = response.data.items || []
  } catch (error) {
    console.error('获取批次信息失败:', error)
  }
}

// 获取库存变动记录
const fetchMovements = async () => {
  try {
    movementsLoading.value = true
    const params = {
      product_id: props.inventory.product_id,
      warehouse_id: props.inventory.warehouse_id,
      page: movementPage.current,
      page_size: movementPage.size
    }
    
    const response = await api.get('/warehouse/stock-movements', { params })
    movements.value = response.data.items || []
    movementPage.total = response.data.total || 0
  } catch (error) {
    console.error('获取库存变动记录失败:', error)
  } finally {
    movementsLoading.value = false
  }
}

// 组件挂载
onMounted(() => {
  fetchBatches()
  fetchMovements()
})
</script>

<style scoped>
.inventory-detail {
  padding: 20px;
}

.detail-section {
  margin-bottom: 32px;
  padding: 20px;
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.section-title {
  margin: 0 0 20px 0;
  font-size: 16px;
  font-weight: 600;
  color: #303133;
  border-bottom: 2px solid #5c6bc0;
  padding-bottom: 8px;
}

.info-item {
  margin-bottom: 12px;
  display: flex;
  align-items: center;
}

.info-item label {
  font-weight: 600;
  color: #606266;
  margin-right: 8px;
  min-width: 100px;
}

.stock-card {
  text-align: center;
  padding: 16px;
  background: #f8f9fa;
  border-radius: 8px;
  border: 1px solid #e9ecef;
}

.stock-label {
  font-size: 12px;
  color: #6c757d;
  margin-bottom: 8px;
}

.stock-value {
  font-size: 20px;
  font-weight: 600;
  line-height: 1;
}

.stock-value.current {
  color: #5c6bc0;
}

.stock-value.available {
  color: #67c23a;
}

.stock-value.reserved {
  color: #e6a23c;
}

.stock-value.transit {
  color: #909399;
}

.stock-value.safety {
  color: #f56c6c;
}

.stock-value.max {
  color: #909399;
}

.stock-value.cost {
  color: #606266;
}

.stock-value.value {
  color: #5c6bc0;
  font-weight: 700;
}

.quantity-in {
  color: #67c23a;
  font-weight: 600;
}

.quantity-out {
  color: #f56c6c;
  font-weight: 600;
}

.pagination-wrapper {
  margin-top: 20px;
  text-align: right;
}

.warning-list {
  max-height: 300px;
  overflow-y: auto;
}

:deep(.el-table) {
  font-size: 14px;
}

:deep(.el-table th) {
  background-color: #fafafa;
}

:deep(.el-alert) {
  border-radius: 6px;
}

@media (max-width: 768px) {
  .inventory-detail {
    padding: 12px;
  }
  
  .detail-section {
    padding: 16px;
    margin-bottom: 20px;
  }
  
  .stock-card {
    margin-bottom: 12px;
  }
  
  .pagination-wrapper {
    text-align: center;
  }
}
</style>