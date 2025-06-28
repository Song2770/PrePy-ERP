<template>
  <div class="purchase-order-form">
    <el-form
      ref="formRef"
      :model="form"
      :rules="rules"
      label-width="120px"
      @submit.prevent
    >
      <!-- 基本信息 -->
      <div class="form-section">
        <h3 class="section-title">基本信息</h3>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="供应商" prop="supplierId" required>
              <el-select
                v-model="form.supplierId"
                placeholder="请选择供应商"
                filterable
                clearable
                style="width: 100%"
                @change="handleSupplierChange"
              >
                <el-option
                  v-for="supplier in suppliers"
                  :key="supplier.id"
                  :label="supplier.name"
                  :value="supplier.id"
                >
                  <div class="supplier-option">
                    <span>{{ supplier.name }}</span>
                    <span class="supplier-code">{{ supplier.code }}</span>
                  </div>
                </el-option>
              </el-select>
            </el-form-item>
          </el-col>
          
          <el-col :span="12">
            <el-form-item label="采购日期" prop="orderDate" required>
              <el-date-picker
                v-model="form.orderDate"
                type="date"
                placeholder="选择采购日期"
                format="YYYY-MM-DD"
                value-format="YYYY-MM-DD"
                style="width: 100%"
              />
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="预计到货日期" prop="expectedDeliveryDate">
              <el-date-picker
                v-model="form.expectedDeliveryDate"
                type="date"
                placeholder="选择预计到货日期"
                format="YYYY-MM-DD"
                value-format="YYYY-MM-DD"
                style="width: 100%"
              />
            </el-form-item>
          </el-col>
          
          <el-col :span="12">
            <el-form-item label="采购员" prop="buyerId">
              <el-select
                v-model="form.buyerId"
                placeholder="请选择采购员"
                filterable
                clearable
                style="width: 100%"
              >
                <el-option
                  v-for="user in users"
                  :key="user.id"
                  :label="user.name"
                  :value="user.id"
                />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-row :gutter="20">
          <el-col :span="24">
            <el-form-item label="备注">
              <el-input
                v-model="form.notes"
                type="textarea"
                :rows="3"
                placeholder="请输入备注信息"
                maxlength="500"
                show-word-limit
              />
            </el-form-item>
          </el-col>
        </el-row>
      </div>

      <!-- 供应商信息 -->
      <div v-if="selectedSupplier" class="form-section">
        <h3 class="section-title">供应商信息</h3>
        <el-row :gutter="20">
          <el-col :span="8">
            <div class="info-item">
              <label>联系人：</label>
              <span>{{ selectedSupplier.contact_person || '-' }}</span>
            </div>
          </el-col>
          <el-col :span="8">
            <div class="info-item">
              <label>联系电话：</label>
              <span>{{ selectedSupplier.phone || '-' }}</span>
            </div>
          </el-col>
          <el-col :span="8">
            <div class="info-item">
              <label>邮箱：</label>
              <span>{{ selectedSupplier.email || '-' }}</span>
            </div>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="24">
            <div class="info-item">
              <label>地址：</label>
              <span>{{ selectedSupplier.address || '-' }}</span>
            </div>
          </el-col>
        </el-row>
      </div>

      <!-- 采购明细 -->
      <div class="form-section">
        <div class="section-header">
          <h3 class="section-title">采购明细</h3>
          <el-button type="primary" size="small" @click="addOrderLine">
            <el-icon><Plus /></el-icon>
            添加商品
          </el-button>
        </div>
        
        <el-table :data="form.orderLines" border>
          <el-table-column label="序号" type="index" width="60" align="center" />
          
          <el-table-column label="商品" width="250" required>
            <template #default="{ row, $index }">
              <el-select
                v-model="row.productId"
                placeholder="请选择商品"
                filterable
                clearable
                style="width: 100%"
                @change="(value) => handleProductChange(value, $index)"
              >
                <el-option
                  v-for="product in products"
                  :key="product.id"
                  :label="product.name"
                  :value="product.id"
                >
                  <div class="product-option">
                    <span>{{ product.name }}</span>
                    <span class="product-code">{{ product.code }}</span>
                  </div>
                </el-option>
              </el-select>
            </template>
          </el-table-column>
          
          <el-table-column label="规格" width="120">
            <template #default="{ row }">
              <span>{{ row.productSpec || '-' }}</span>
            </template>
          </el-table-column>
          
          <el-table-column label="单位" width="80">
            <template #default="{ row }">
              <span>{{ row.productUnit || '-' }}</span>
            </template>
          </el-table-column>
          
          <el-table-column label="采购数量" width="120" required>
            <template #default="{ row }">
              <el-input-number
                v-model="row.quantity"
                :min="0.01"
                :precision="2"
                :step="1"
                style="width: 100%"
                @change="calculateLineTotal(row)"
              />
            </template>
          </el-table-column>
          
          <el-table-column label="单价" width="120" required>
            <template #default="{ row }">
              <el-input-number
                v-model="row.unitPrice"
                :min="0"
                :precision="2"
                :step="0.01"
                style="width: 100%"
                @change="calculateLineTotal(row)"
              />
            </template>
          </el-table-column>
          
          <el-table-column label="金额" width="120">
            <template #default="{ row }">
              <span class="amount-text">¥{{ formatCurrency(row.totalPrice) }}</span>
            </template>
          </el-table-column>
          
          <el-table-column label="备注" width="150">
            <template #default="{ row }">
              <el-input
                v-model="row.notes"
                placeholder="备注"
                maxlength="100"
              />
            </template>
          </el-table-column>
          
          <el-table-column label="操作" width="80" fixed="right">
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
        
        <div v-if="form.orderLines.length === 0" class="empty-lines">
          <el-empty description="暂无采购明细" :image-size="80">
            <el-button type="primary" @click="addOrderLine">
              添加商品
            </el-button>
          </el-empty>
        </div>
      </div>

      <!-- 费用汇总 -->
      <div class="form-section">
        <h3 class="section-title">费用汇总</h3>
        <el-row :gutter="20">
          <el-col :span="6">
            <div class="summary-item">
              <label>商品总数：</label>
              <span class="summary-value">{{ totalQuantity }}</span>
            </div>
          </el-col>
          <el-col :span="6">
            <div class="summary-item">
              <label>商品金额：</label>
              <span class="summary-value">¥{{ formatCurrency(subtotalAmount) }}</span>
            </div>
          </el-col>
          <el-col :span="6">
            <div class="summary-item">
              <label>运费：</label>
              <el-input-number
                v-model="form.shippingFee"
                :min="0"
                :precision="2"
                :step="0.01"
                style="width: 120px"
                @change="calculateTotal"
              />
            </div>
          </el-col>
          <el-col :span="6">
            <div class="summary-item">
              <label>总金额：</label>
              <span class="summary-value total-amount">¥{{ formatCurrency(totalAmount) }}</span>
            </div>
          </el-col>
        </el-row>
      </div>
    </el-form>

    <!-- 操作按钮 -->
    <div class="form-actions">
      <el-button @click="$emit('cancel')">
        取消
      </el-button>
      <el-button type="info" @click="saveDraft" :loading="saving">
        保存草稿
      </el-button>
      <el-button type="primary" @click="saveAndSend" :loading="saving">
        保存并发送
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
const suppliers = ref([])
const products = ref([])
const users = ref([])
const selectedSupplier = ref(null)

// 表单数据
const form = reactive({
  supplierId: null,
  orderDate: new Date().toISOString().split('T')[0],
  expectedDeliveryDate: '',
  buyerId: null,
  notes: '',
  shippingFee: 0,
  orderLines: []
})

// 表单验证规则
const rules = {
  supplierId: [
    { required: true, message: '请选择供应商', trigger: 'change' }
  ],
  orderDate: [
    { required: true, message: '请选择采购日期', trigger: 'change' }
  ]
}

// 计算属性
const totalQuantity = computed(() => {
  return form.orderLines.reduce((sum, line) => sum + (line.quantity || 0), 0)
})

const subtotalAmount = computed(() => {
  return form.orderLines.reduce((sum, line) => sum + (line.totalPrice || 0), 0)
})

const totalAmount = computed(() => {
  return subtotalAmount.value + (form.shippingFee || 0)
})

// 格式化货币
const formatCurrency = (amount) => {
  if (!amount) return '0.00'
  return Number(amount).toLocaleString('zh-CN', {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2
  })
}

// 获取供应商列表
const fetchSuppliers = async () => {
  try {
    const response = await api.get('/suppliers')
    suppliers.value = response.data.items || []
  } catch (error) {
    console.error('获取供应商列表失败:', error)
  }
}

// 获取商品列表
const fetchProducts = async () => {
  try {
    const response = await api.get('/products')
    products.value = response.data.items || []
  } catch (error) {
    console.error('获取商品列表失败:', error)
  }
}

// 获取用户列表
const fetchUsers = async () => {
  try {
    const response = await api.get('/users')
    users.value = response.data.items || []
  } catch (error) {
    console.error('获取用户列表失败:', error)
  }
}

// 供应商变化处理
const handleSupplierChange = (supplierId) => {
  selectedSupplier.value = suppliers.value.find(s => s.id === supplierId) || null
}

// 商品变化处理
const handleProductChange = (productId, index) => {
  const product = products.value.find(p => p.id === productId)
  if (product) {
    const line = form.orderLines[index]
    line.productName = product.name
    line.productCode = product.code
    line.productSpec = product.specification
    line.productUnit = product.unit
    line.unitPrice = product.purchase_price || 0
    calculateLineTotal(line)
  }
}

// 添加订单行
const addOrderLine = () => {
  form.orderLines.push({
    productId: null,
    productName: '',
    productCode: '',
    productSpec: '',
    productUnit: '',
    quantity: 1,
    unitPrice: 0,
    totalPrice: 0,
    notes: ''
  })
}

// 删除订单行
const removeOrderLine = (index) => {
  form.orderLines.splice(index, 1)
  calculateTotal()
}

// 计算行总价
const calculateLineTotal = (line) => {
  line.totalPrice = (line.quantity || 0) * (line.unitPrice || 0)
  calculateTotal()
}

// 计算总计
const calculateTotal = () => {
  // 触发计算属性更新
}

// 验证表单
const validateForm = async () => {
  try {
    await formRef.value.validate()
    
    if (form.orderLines.length === 0) {
      ElMessage.error('请至少添加一个商品')
      return false
    }
    
    for (let i = 0; i < form.orderLines.length; i++) {
      const line = form.orderLines[i]
      if (!line.productId) {
        ElMessage.error(`第 ${i + 1} 行请选择商品`)
        return false
      }
      if (!line.quantity || line.quantity <= 0) {
        ElMessage.error(`第 ${i + 1} 行请输入正确的数量`)
        return false
      }
      if (!line.unitPrice || line.unitPrice < 0) {
        ElMessage.error(`第 ${i + 1} 行请输入正确的单价`)
        return false
      }
    }
    
    return true
  } catch (error) {
    return false
  }
}

// 保存草稿
const saveDraft = async () => {
  if (!(await validateForm())) return
  
  try {
    saving.value = true
    
    const data = {
      supplier_id: form.supplierId,
      order_date: form.orderDate,
      expected_delivery_date: form.expectedDeliveryDate,
      buyer_id: form.buyerId,
      notes: form.notes,
      shipping_fee: form.shippingFee || 0,
      status: 'draft',
      order_lines: form.orderLines.map(line => ({
        product_id: line.productId,
        quantity: line.quantity,
        unit_price: line.unitPrice,
        notes: line.notes
      }))
    }
    
    await api.post('/procurement/purchase-orders', data)
    emit('success')
  } catch (error) {
    console.error('保存采购单失败:', error)
    ElMessage.error('保存采购单失败')
  } finally {
    saving.value = false
  }
}

// 保存并发送
const saveAndSend = async () => {
  if (!(await validateForm())) return
  
  try {
    saving.value = true
    
    const data = {
      supplier_id: form.supplierId,
      order_date: form.orderDate,
      expected_delivery_date: form.expectedDeliveryDate,
      buyer_id: form.buyerId,
      notes: form.notes,
      shipping_fee: form.shippingFee || 0,
      status: 'sent',
      order_lines: form.orderLines.map(line => ({
        product_id: line.productId,
        quantity: line.quantity,
        unit_price: line.unitPrice,
        notes: line.notes
      }))
    }
    
    await api.post('/procurement/purchase-orders', data)
    emit('success')
  } catch (error) {
    console.error('保存并发送采购单失败:', error)
    ElMessage.error('保存并发送采购单失败')
  } finally {
    saving.value = false
  }
}

// 组件挂载
onMounted(() => {
  fetchSuppliers()
  fetchProducts()
  fetchUsers()
  
  // 添加一行默认数据
  addOrderLine()
})
</script>

<style scoped>
.purchase-order-form {
  padding: 20px;
}

.form-section {
  margin-bottom: 32px;
  padding: 20px;
  background: #fafafa;
  border-radius: 8px;
}

.section-title {
  margin: 0 0 20px 0;
  font-size: 16px;
  font-weight: 600;
  color: #303133;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.supplier-option,
.product-option {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.supplier-code,
.product-code {
  font-size: 12px;
  color: #909399;
}

.info-item {
  margin-bottom: 12px;
}

.info-item label {
  font-weight: 600;
  color: #606266;
  margin-right: 8px;
}

.empty-lines {
  padding: 40px;
  text-align: center;
}

.amount-text {
  font-weight: 600;
  color: #5c6bc0;
}

.summary-item {
  display: flex;
  align-items: center;
  margin-bottom: 12px;
}

.summary-item label {
  font-weight: 600;
  color: #606266;
  margin-right: 8px;
  min-width: 80px;
}

.summary-value {
  font-weight: 600;
  color: #303133;
}

.total-amount {
  font-size: 18px;
  color: #f56c6c;
}

.form-actions {
  margin-top: 32px;
  padding-top: 20px;
  border-top: 1px solid #ebeef5;
  text-align: right;
}

.form-actions .el-button {
  margin-left: 12px;
}

:deep(.el-table .el-table__cell) {
  padding: 8px 0;
}

:deep(.el-form-item) {
  margin-bottom: 20px;
}

:deep(.el-input-number .el-input__inner) {
  text-align: left;
}
</style>