<template>
  <div class="order-form">
    <el-form
      ref="formRef"
      :model="form"
      :rules="rules"
      label-width="100px"
      label-position="left"
    >
      <!-- 基本信息 -->
      <div class="form-section">
        <h3 class="section-title">基本信息</h3>
        
        <el-row :gutter="16">
          <el-col :span="12">
            <el-form-item label="客户" prop="customer_id">
              <el-select
                v-model="form.customer_id"
                placeholder="请选择客户"
                filterable
                style="width: 100%"
                @change="handleCustomerChange"
              >
                <el-option
                  v-for="customer in customers"
                  :key="customer.id"
                  :label="customer.name"
                  :value="customer.id"
                />
              </el-select>
            </el-form-item>
          </el-col>
          
          <el-col :span="12">
            <el-form-item label="订单日期" prop="order_date">
              <el-date-picker
                v-model="form.order_date"
                type="date"
                placeholder="请选择订单日期"
                format="YYYY-MM-DD"
                value-format="YYYY-MM-DD"
                style="width: 100%"
              />
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-row :gutter="16">
          <el-col :span="12">
            <el-form-item label="交货日期" prop="delivery_date">
              <el-date-picker
                v-model="form.delivery_date"
                type="date"
                placeholder="请选择交货日期"
                format="YYYY-MM-DD"
                value-format="YYYY-MM-DD"
                style="width: 100%"
              />
            </el-form-item>
          </el-col>
          
          <el-col :span="12">
            <el-form-item label="销售员" prop="salesperson">
              <el-input
                v-model="form.salesperson"
                placeholder="请输入销售员姓名"
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
      
      <!-- 订单明细 -->
      <div class="form-section">
        <div class="section-header">
          <h3 class="section-title">订单明细</h3>
          <el-button type="primary" size="small" @click="addOrderLine">
            <el-icon><Plus /></el-icon>
            添加明细
          </el-button>
        </div>
        
        <el-table :data="form.order_lines" border>
          <el-table-column label="序号" type="index" width="60" />
          
          <el-table-column label="产品" width="200">
            <template #default="{ row, $index }">
              <el-select
                v-model="row.product_id"
                placeholder="请选择产品"
                filterable
                style="width: 100%"
                @change="(value) => handleProductChange(value, $index)"
              >
                <el-option
                  v-for="product in products"
                  :key="product.id"
                  :label="product.name"
                  :value="product.id"
                />
              </el-select>
            </template>
          </el-table-column>
          
          <el-table-column label="规格" width="150">
            <template #default="{ row }">
              <span>{{ getProductSpec(row.product_id) }}</span>
            </template>
          </el-table-column>
          
          <el-table-column label="数量" width="120">
            <template #default="{ row, $index }">
              <el-input-number
                v-model="row.quantity"
                :min="1"
                :precision="2"
                style="width: 100%"
                @change="calculateLineTotal($index)"
              />
            </template>
          </el-table-column>
          
          <el-table-column label="单位" width="80">
            <template #default="{ row }">
              <span>{{ getProductUnit(row.product_id) }}</span>
            </template>
          </el-table-column>
          
          <el-table-column label="单价" width="120">
            <template #default="{ row, $index }">
              <el-input-number
                v-model="row.unit_price"
                :min="0"
                :precision="2"
                style="width: 100%"
                @change="calculateLineTotal($index)"
              />
            </template>
          </el-table-column>
          
          <el-table-column label="金额" width="120">
            <template #default="{ row }">
              <span>¥{{ formatCurrency(row.total_price) }}</span>
            </template>
          </el-table-column>
          
          <el-table-column label="备注" min-width="150">
            <template #default="{ row }">
              <el-input
                v-model="row.notes"
                placeholder="备注"
                size="small"
              />
            </template>
          </el-table-column>
          
          <el-table-column label="操作" width="80">
            <template #default="{ $index }">
              <el-button
                type="danger"
                size="small"
                @click="removeOrderLine($index)"
              >
                删除
              </el-button>
            </template>
          </el-table-column>
        </el-table>
        
        <!-- 合计信息 -->
        <div class="total-section">
          <el-row>
            <el-col :span="18">
              <div class="total-label">订单总额：</div>
            </el-col>
            <el-col :span="6">
              <div class="total-amount">¥{{ formatCurrency(totalAmount) }}</div>
            </el-col>
          </el-row>
        </div>
      </div>
    </el-form>
    
    <!-- 操作按钮 -->
    <div class="form-actions">
      <el-button @click="$emit('cancel')">取消</el-button>
      <el-button type="primary" @click="handleSave" :loading="saving">
        保存
      </el-button>
      <el-button type="success" @click="handleSaveAndConfirm" :loading="saving">
        保存并确认
      </el-button>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { api } from '@/utils/api'

// 定义事件
const emit = defineEmits(['success', 'cancel'])

// 响应式数据
const formRef = ref()
const saving = ref(false)
const customers = ref([])
const products = ref([])

// 表单数据
const form = reactive({
  customer_id: null,
  order_date: new Date().toISOString().split('T')[0],
  delivery_date: '',
  salesperson: '',
  notes: '',
  order_lines: []
})

// 表单验证规则
const rules = {
  customer_id: [
    { required: true, message: '请选择客户', trigger: 'change' }
  ],
  order_date: [
    { required: true, message: '请选择订单日期', trigger: 'change' }
  ],
  delivery_date: [
    { required: true, message: '请选择交货日期', trigger: 'change' }
  ]
}

// 计算属性
const totalAmount = computed(() => {
  return form.order_lines.reduce((sum, line) => {
    return sum + (line.total_price || 0)
  }, 0)
})

// 格式化货币
const formatCurrency = (amount) => {
  if (!amount) return '0.00'
  return Number(amount).toLocaleString('zh-CN', {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2
  })
}

// 获取产品规格
const getProductSpec = (productId) => {
  const product = products.value.find(p => p.id === productId)
  return product?.specification || '-'
}

// 获取产品单位
const getProductUnit = (productId) => {
  const product = products.value.find(p => p.id === productId)
  return product?.unit || '-'
}

// 获取客户列表
const fetchCustomers = async () => {
  try {
    const response = await api.get('/customers')
    customers.value = response.data.items || []
  } catch (error) {
    console.error('获取客户列表失败:', error)
    ElMessage.error('获取客户列表失败')
  }
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

// 客户变化处理
const handleCustomerChange = (customerId) => {
  const customer = customers.value.find(c => c.id === customerId)
  if (customer) {
    // 可以根据客户设置默认的销售员等信息
    console.log('选择客户:', customer.name)
  }
}

// 产品变化处理
const handleProductChange = (productId, index) => {
  const product = products.value.find(p => p.id === productId)
  if (product) {
    // 设置默认单价
    form.order_lines[index].unit_price = product.price || 0
    form.order_lines[index].quantity = form.order_lines[index].quantity || 1
    calculateLineTotal(index)
  }
}

// 计算行总价
const calculateLineTotal = (index) => {
  const line = form.order_lines[index]
  line.total_price = (line.quantity || 0) * (line.unit_price || 0)
}

// 添加订单明细
const addOrderLine = () => {
  form.order_lines.push({
    product_id: null,
    quantity: 1,
    unit_price: 0,
    total_price: 0,
    notes: ''
  })
}

// 删除订单明细
const removeOrderLine = (index) => {
  form.order_lines.splice(index, 1)
}

// 保存订单
const handleSave = async () => {
  try {
    await formRef.value.validate()
    
    if (form.order_lines.length === 0) {
      ElMessage.warning('请至少添加一个订单明细')
      return
    }
    
    // 验证订单明细
    for (let i = 0; i < form.order_lines.length; i++) {
      const line = form.order_lines[i]
      if (!line.product_id) {
        ElMessage.warning(`第 ${i + 1} 行请选择产品`)
        return
      }
      if (!line.quantity || line.quantity <= 0) {
        ElMessage.warning(`第 ${i + 1} 行数量必须大于0`)
        return
      }
      if (!line.unit_price || line.unit_price < 0) {
        ElMessage.warning(`第 ${i + 1} 行单价不能为负数`)
        return
      }
    }
    
    saving.value = true
    
    const orderData = {
      ...form,
      total_amount: totalAmount.value,
      status: 'draft'
    }
    
    await api.post('/sales/orders', orderData)
    emit('success')
  } catch (error) {
    console.error('保存订单失败:', error)
    ElMessage.error('保存订单失败')
  } finally {
    saving.value = false
  }
}

// 保存并确认订单
const handleSaveAndConfirm = async () => {
  try {
    await formRef.value.validate()
    
    if (form.order_lines.length === 0) {
      ElMessage.warning('请至少添加一个订单明细')
      return
    }
    
    // 验证订单明细
    for (let i = 0; i < form.order_lines.length; i++) {
      const line = form.order_lines[i]
      if (!line.product_id) {
        ElMessage.warning(`第 ${i + 1} 行请选择产品`)
        return
      }
      if (!line.quantity || line.quantity <= 0) {
        ElMessage.warning(`第 ${i + 1} 行数量必须大于0`)
        return
      }
      if (!line.unit_price || line.unit_price < 0) {
        ElMessage.warning(`第 ${i + 1} 行单价不能为负数`)
        return
      }
    }
    
    saving.value = true
    
    const orderData = {
      ...form,
      total_amount: totalAmount.value,
      status: 'confirmed'
    }
    
    await api.post('/sales/orders', orderData)
    emit('success')
  } catch (error) {
    console.error('保存订单失败:', error)
    ElMessage.error('保存订单失败')
  } finally {
    saving.value = false
  }
}

// 组件挂载
onMounted(() => {
  fetchCustomers()
  fetchProducts()
  // 默认添加一行明细
  addOrderLine()
})
</script>

<style scoped>
.order-form {
  padding: 20px;
}

.form-section {
  margin-bottom: 32px;
  padding: 20px;
  background-color: #fafafa;
  border-radius: 8px;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.section-title {
  margin: 0 0 16px 0;
  font-size: 16px;
  font-weight: 600;
  color: #262626;
  border-left: 4px solid #5c6bc0;
  padding-left: 12px;
}

.total-section {
  margin-top: 16px;
  padding: 16px;
  background-color: #f0f9ff;
  border-radius: 6px;
  border: 1px solid #e1f5fe;
}

.total-label {
  font-size: 16px;
  font-weight: 600;
  color: #262626;
  text-align: right;
}

.total-amount {
  font-size: 18px;
  font-weight: 700;
  color: #f56c6c;
  text-align: right;
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
</style>