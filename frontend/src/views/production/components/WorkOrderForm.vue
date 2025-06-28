<template>
  <div class="work-order-form">
    <el-form
      ref="formRef"
      :model="form"
      :rules="rules"
      label-width="120px"
      label-position="left"
    >
      <!-- 基本信息 -->
      <div class="form-section">
        <h3 class="section-title">基本信息</h3>
        
        <el-row :gutter="16">
          <el-col :span="12">
            <el-form-item label="产品" prop="product_id">
              <el-select
                v-model="form.product_id"
                placeholder="请选择产品"
                filterable
                style="width: 100%"
                @change="handleProductChange"
              >
                <el-option
                  v-for="product in products"
                  :key="product.id"
                  :label="product.name"
                  :value="product.id"
                />
              </el-select>
            </el-form-item>
          </el-col>
          
          <el-col :span="12">
            <el-form-item label="生产数量" prop="quantity">
              <el-input-number
                v-model="form.quantity"
                :min="1"
                :precision="2"
                style="width: 100%"
                placeholder="请输入生产数量"
              />
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-row :gutter="16">
          <el-col :span="12">
            <el-form-item label="计划开始日期" prop="planned_start_date">
              <el-date-picker
                v-model="form.planned_start_date"
                type="date"
                placeholder="请选择计划开始日期"
                format="YYYY-MM-DD"
                value-format="YYYY-MM-DD"
                style="width: 100%"
              />
            </el-form-item>
          </el-col>
          
          <el-col :span="12">
            <el-form-item label="计划完成日期" prop="planned_end_date">
              <el-date-picker
                v-model="form.planned_end_date"
                type="date"
                placeholder="请选择计划完成日期"
                format="YYYY-MM-DD"
                value-format="YYYY-MM-DD"
                style="width: 100%"
              />
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-row :gutter="16">
          <el-col :span="12">
            <el-form-item label="优先级" prop="priority">
              <el-select
                v-model="form.priority"
                placeholder="请选择优先级"
                style="width: 100%"
              >
                <el-option label="低" value="low" />
                <el-option label="普通" value="normal" />
                <el-option label="高" value="high" />
                <el-option label="紧急" value="urgent" />
              </el-select>
            </el-form-item>
          </el-col>
          
          <el-col :span="12">
            <el-form-item label="负责人" prop="responsible_person">
              <el-input
                v-model="form.responsible_person"
                placeholder="请输入负责人姓名"
              />
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-form-item label="备注">
          <el-input
            v-model="form.notes"
            type="textarea"
            :rows="3"
            placeholder="请输入备注信息"
          />
        </el-form-item>
      </div>
      
      <!-- 产品信息 -->
      <div v-if="selectedProduct" class="form-section">
        <h3 class="section-title">产品信息</h3>
        
        <el-descriptions :column="2" border>
          <el-descriptions-item label="产品编码">
            {{ selectedProduct.code }}
          </el-descriptions-item>
          
          <el-descriptions-item label="产品名称">
            {{ selectedProduct.name }}
          </el-descriptions-item>
          
          <el-descriptions-item label="规格">
            {{ selectedProduct.specification || '-' }}
          </el-descriptions-item>
          
          <el-descriptions-item label="单位">
            {{ selectedProduct.unit }}
          </el-descriptions-item>
          
          <el-descriptions-item label="标准成本">
            ¥{{ formatCurrency(selectedProduct.cost) }}
          </el-descriptions-item>
          
          <el-descriptions-item label="当前库存">
            {{ formatNumber(selectedProduct.stock_quantity) }} {{ selectedProduct.unit }}
          </el-descriptions-item>
        </el-descriptions>
      </div>
      
      <!-- 物料需求 -->
      <div v-if="materialRequirements.length > 0" class="form-section">
        <h3 class="section-title">物料需求</h3>
        
        <el-table :data="materialRequirements" border>
          <el-table-column label="序号" type="index" width="60" />
          
          <el-table-column label="物料编码" prop="material_code" width="120" />
          
          <el-table-column label="物料名称" prop="material_name" min-width="150" />
          
          <el-table-column label="规格" prop="specification" width="120" />
          
          <el-table-column label="单位用量" prop="unit_consumption" width="100" align="right">
            <template #default="{ row }">
              {{ formatNumber(row.unit_consumption) }}
            </template>
          </el-table-column>
          
          <el-table-column label="总需求" width="100" align="right">
            <template #default="{ row }">
              {{ formatNumber(row.unit_consumption * form.quantity) }}
            </template>
          </el-table-column>
          
          <el-table-column label="单位" prop="unit" width="80" />
          
          <el-table-column label="当前库存" prop="stock_quantity" width="100" align="right">
            <template #default="{ row }">
              <span :class="getStockClass(row)">
                {{ formatNumber(row.stock_quantity) }}
              </span>
            </template>
          </el-table-column>
          
          <el-table-column label="缺料数量" width="100" align="right">
            <template #default="{ row }">
              <span :class="getShortageClass(row)">
                {{ formatNumber(getShortageQuantity(row)) }}
              </span>
            </template>
          </el-table-column>
        </el-table>
        
        <!-- 物料状态提示 -->
        <div v-if="hasShortage" class="shortage-warning">
          <el-alert
            title="物料不足警告"
            type="warning"
            :description="`有 ${shortageCount} 种物料库存不足，请及时采购或调配库存。`"
            show-icon
            :closable="false"
          />
        </div>
      </div>
      
      <!-- 工艺路线 -->
      <div v-if="processRoutes.length > 0" class="form-section">
        <h3 class="section-title">工艺路线</h3>
        
        <el-table :data="processRoutes" border>
          <el-table-column label="序号" prop="sequence" width="80" align="center" />
          
          <el-table-column label="工序名称" prop="process_name" min-width="150" />
          
          <el-table-column label="工作中心" prop="work_center" width="120" />
          
          <el-table-column label="标准工时" prop="standard_hours" width="100" align="right">
            <template #default="{ row }">
              {{ formatNumber(row.standard_hours) }} 小时
            </template>
          </el-table-column>
          
          <el-table-column label="总工时" width="100" align="right">
            <template #default="{ row }">
              {{ formatNumber(row.standard_hours * form.quantity) }} 小时
            </template>
          </el-table-column>
          
          <el-table-column label="设备要求" prop="equipment_requirement" min-width="150" />
          
          <el-table-column label="质量要求" prop="quality_requirement" min-width="150" />
        </el-table>
      </div>
      
      <!-- 成本预估 -->
      <div class="form-section">
        <h3 class="section-title">成本预估</h3>
        
        <el-row :gutter="16">
          <el-col :span="8">
            <div class="cost-item">
              <div class="cost-label">物料成本</div>
              <div class="cost-value">¥{{ formatCurrency(materialCost) }}</div>
            </div>
          </el-col>
          
          <el-col :span="8">
            <div class="cost-item">
              <div class="cost-label">人工成本</div>
              <div class="cost-value">¥{{ formatCurrency(laborCost) }}</div>
            </div>
          </el-col>
          
          <el-col :span="8">
            <div class="cost-item">
              <div class="cost-label">制造费用</div>
              <div class="cost-value">¥{{ formatCurrency(overheadCost) }}</div>
            </div>
          </el-col>
        </el-row>
        
        <el-row>
          <el-col :span="24">
            <div class="total-cost">
              <div class="total-label">总成本预估</div>
              <div class="total-value">¥{{ formatCurrency(totalCost) }}</div>
            </div>
          </el-col>
        </el-row>
      </div>
    </el-form>
    
    <!-- 操作按钮 -->
    <div class="form-actions">
      <el-button @click="$emit('cancel')">取消</el-button>
      <el-button type="primary" @click="handleSave" :loading="saving">
        保存
      </el-button>
      <el-button type="success" @click="handleSaveAndStart" :loading="saving">
        保存并开始
      </el-button>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted, watch } from 'vue'
import { ElMessage } from 'element-plus'
import { api } from '@/utils/api'

// 定义事件
const emit = defineEmits(['success', 'cancel'])

// 响应式数据
const formRef = ref()
const saving = ref(false)
const products = ref([])
const materialRequirements = ref([])
const processRoutes = ref([])

// 表单数据
const form = reactive({
  product_id: null,
  quantity: 1,
  planned_start_date: new Date().toISOString().split('T')[0],
  planned_end_date: '',
  priority: 'normal',
  responsible_person: '',
  notes: ''
})

// 表单验证规则
const rules = {
  product_id: [
    { required: true, message: '请选择产品', trigger: 'change' }
  ],
  quantity: [
    { required: true, message: '请输入生产数量', trigger: 'blur' },
    { type: 'number', min: 1, message: '生产数量必须大于0', trigger: 'blur' }
  ],
  planned_start_date: [
    { required: true, message: '请选择计划开始日期', trigger: 'change' }
  ],
  planned_end_date: [
    { required: true, message: '请选择计划完成日期', trigger: 'change' }
  ],
  priority: [
    { required: true, message: '请选择优先级', trigger: 'change' }
  ]
}

// 计算属性
const selectedProduct = computed(() => {
  return products.value.find(p => p.id === form.product_id)
})

const materialCost = computed(() => {
  return materialRequirements.value.reduce((sum, material) => {
    const totalQuantity = material.unit_consumption * form.quantity
    return sum + (totalQuantity * (material.unit_cost || 0))
  }, 0)
})

const laborCost = computed(() => {
  const totalHours = processRoutes.value.reduce((sum, route) => {
    return sum + (route.standard_hours * form.quantity)
  }, 0)
  return totalHours * 50 // 假设每小时人工成本50元
})

const overheadCost = computed(() => {
  return (materialCost.value + laborCost.value) * 0.2 // 假设制造费用为20%
})

const totalCost = computed(() => {
  return materialCost.value + laborCost.value + overheadCost.value
})

const hasShortage = computed(() => {
  return materialRequirements.value.some(material => getShortageQuantity(material) > 0)
})

const shortageCount = computed(() => {
  return materialRequirements.value.filter(material => getShortageQuantity(material) > 0).length
})

// 格式化货币
const formatCurrency = (amount) => {
  if (!amount) return '0.00'
  return Number(amount).toLocaleString('zh-CN', {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2
  })
}

// 格式化数字
const formatNumber = (number) => {
  if (!number) return '0'
  return Number(number).toLocaleString('zh-CN')
}

// 获取缺料数量
const getShortageQuantity = (material) => {
  const required = material.unit_consumption * form.quantity
  const shortage = required - (material.stock_quantity || 0)
  return shortage > 0 ? shortage : 0
}

// 获取库存样式
const getStockClass = (material) => {
  const shortage = getShortageQuantity(material)
  return shortage > 0 ? 'shortage' : 'sufficient'
}

// 获取缺料样式
const getShortageClass = (material) => {
  const shortage = getShortageQuantity(material)
  return shortage > 0 ? 'shortage' : 'sufficient'
}

// 获取产品列表
const fetchProducts = async () => {
  try {
    const response = await api.get('/products')
    products.value = response.data.items || []
  } catch (error) {
    console.error('获取产品列表失败:', error)
    ElMessage.error('获取产品列表失败')
  }
}

// 获取物料需求
const fetchMaterialRequirements = async (productId) => {
  try {
    const response = await api.get(`/products/${productId}/bom`)
    materialRequirements.value = response.data || []
  } catch (error) {
    console.error('获取物料需求失败:', error)
    materialRequirements.value = []
  }
}

// 获取工艺路线
const fetchProcessRoutes = async (productId) => {
  try {
    const response = await api.get(`/products/${productId}/process-routes`)
    processRoutes.value = response.data || []
  } catch (error) {
    console.error('获取工艺路线失败:', error)
    processRoutes.value = []
  }
}

// 产品变化处理
const handleProductChange = async (productId) => {
  if (productId) {
    await Promise.all([
      fetchMaterialRequirements(productId),
      fetchProcessRoutes(productId)
    ])
  } else {
    materialRequirements.value = []
    processRoutes.value = []
  }
}

// 监听数量变化
watch(() => form.quantity, () => {
  // 数量变化时重新计算成本
})

// 保存工单
const handleSave = async () => {
  try {
    await formRef.value.validate()
    
    // 验证日期
    if (new Date(form.planned_end_date) <= new Date(form.planned_start_date)) {
      ElMessage.warning('计划完成日期必须晚于计划开始日期')
      return
    }
    
    saving.value = true
    
    const workOrderData = {
      ...form,
      status: 'planned',
      estimated_cost: totalCost.value
    }
    
    await api.post('/production/work-orders', workOrderData)
    emit('success')
  } catch (error) {
    console.error('保存工单失败:', error)
    ElMessage.error('保存工单失败')
  } finally {
    saving.value = false
  }
}

// 保存并开始工单
const handleSaveAndStart = async () => {
  try {
    await formRef.value.validate()
    
    // 验证日期
    if (new Date(form.planned_end_date) <= new Date(form.planned_start_date)) {
      ElMessage.warning('计划完成日期必须晚于计划开始日期')
      return
    }
    
    // 检查物料是否充足
    if (hasShortage.value) {
      const result = await ElMessageBox.confirm(
        '存在物料不足的情况，是否仍要开始生产？',
        '物料不足警告',
        {
          confirmButtonText: '继续',
          cancelButtonText: '取消',
          type: 'warning'
        }
      )
      
      if (result !== 'confirm') {
        return
      }
    }
    
    saving.value = true
    
    const workOrderData = {
      ...form,
      status: 'in_progress',
      estimated_cost: totalCost.value,
      actual_start_date: new Date().toISOString().split('T')[0]
    }
    
    await api.post('/production/work-orders', workOrderData)
    emit('success')
  } catch (error) {
    if (error !== 'cancel') {
      console.error('保存工单失败:', error)
      ElMessage.error('保存工单失败')
    }
  } finally {
    saving.value = false
  }
}

// 组件挂载
onMounted(() => {
  fetchProducts()
})
</script>

<style scoped>
.work-order-form {
  padding: 20px;
}

.form-section {
  margin-bottom: 32px;
  padding: 20px;
  background-color: #fafafa;
  border-radius: 8px;
}

.section-title {
  margin: 0 0 16px 0;
  font-size: 16px;
  font-weight: 600;
  color: #262626;
  border-left: 4px solid #5c6bc0;
  padding-left: 12px;
}

.cost-item {
  text-align: center;
  padding: 16px;
  background-color: #f0f9ff;
  border-radius: 6px;
  border: 1px solid #e1f5fe;
}

.cost-label {
  font-size: 14px;
  color: #666;
  margin-bottom: 8px;
}

.cost-value {
  font-size: 18px;
  font-weight: 600;
  color: #5c6bc0;
}

.total-cost {
  text-align: center;
  padding: 20px;
  background-color: #fff2e8;
  border-radius: 6px;
  border: 1px solid #ffd591;
  margin-top: 16px;
}

.total-label {
  font-size: 16px;
  color: #666;
  margin-bottom: 8px;
}

.total-value {
  font-size: 24px;
  font-weight: 700;
  color: #fa8c16;
}

.shortage-warning {
  margin-top: 16px;
}

.shortage {
  color: #f56c6c;
  font-weight: 600;
}

.sufficient {
  color: #67c23a;
}

.form-actions {
  margin-top: 24px;
  text-align: right;
  padding-top: 16px;
  border-top: 1px solid #e8e8e8;
}

.form-actions .el-button {
  margin-left: 12px;
}

:deep(.el-table .el-table__cell) {
  padding: 8px 0;
}

:deep(.el-input-number .el-input__inner) {
  text-align: left;
}

:deep(.el-descriptions__label) {
  font-weight: 600;
}
</style>