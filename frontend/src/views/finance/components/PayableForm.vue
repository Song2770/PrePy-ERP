<template>
  <div class="payable-form">
    <el-form
      ref="formRef"
      :model="form"
      :rules="rules"
      label-width="120px"
      v-loading="loading"
    >
      <!-- 基本信息 -->
      <div class="form-section">
        <h3 class="section-title">基本信息</h3>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="供应商" prop="supplier_id" required>
              <el-select
                v-model="form.supplier_id"
                placeholder="请选择供应商"
                filterable
                @change="handleSupplierChange"
                style="width: 100%;"
              >
                <el-option
                  v-for="supplier in suppliers"
                  :key="supplier.id"
                  :label="supplier.name"
                  :value="supplier.id"
                />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="单据号" prop="bill_number">
              <el-input
                v-model="form.bill_number"
                placeholder="系统自动生成"
                :disabled="!!form.id"
              />
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="来源类型" prop="source_type" required>
              <el-select
                v-model="form.source_type"
                placeholder="请选择来源类型"
                @change="handleSourceTypeChange"
                style="width: 100%;"
              >
                <el-option label="采购订单" value="purchase_order" />
                <el-option label="费用报销" value="expense" />
                <el-option label="手工录入" value="manual" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="来源单号" prop="source_number">
              <el-select
                v-if="form.source_type === 'purchase_order'"
                v-model="form.source_number"
                placeholder="请选择采购订单"
                filterable
                @change="handleSourceOrderChange"
                style="width: 100%;"
              >
                <el-option
                  v-for="order in sourceOrders"
                  :key="order.order_number"
                  :label="`${order.order_number} - ¥${formatAmount(order.total_amount)}`"
                  :value="order.order_number"
                />
              </el-select>
              <el-input
                v-else
                v-model="form.source_number"
                placeholder="请输入来源单号"
              />
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="采购员" prop="buyer">
              <el-select
                v-model="form.buyer"
                placeholder="请选择采购员"
                filterable
                style="width: 100%;"
              >
                <el-option
                  v-for="user in users"
                  :key="user.id"
                  :label="user.name"
                  :value="user.name"
                />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="币种" prop="currency">
              <el-select
                v-model="form.currency"
                placeholder="请选择币种"
                style="width: 100%;"
              >
                <el-option label="人民币" value="CNY" />
                <el-option label="美元" value="USD" />
                <el-option label="欧元" value="EUR" />
                <el-option label="日元" value="JPY" />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
      </div>

      <!-- 金额信息 -->
      <div class="form-section">
        <h3 class="section-title">金额信息</h3>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="应付金额" prop="total_amount" required>
              <el-input-number
                v-model="form.total_amount"
                :precision="2"
                :min="0"
                :max="999999999"
                placeholder="请输入应付金额"
                style="width: 100%;"
                @change="calculateAmounts"
              />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="税率" prop="tax_rate">
              <el-input-number
                v-model="form.tax_rate"
                :precision="2"
                :min="0"
                :max="100"
                placeholder="请输入税率"
                style="width: 100%;"
                @change="calculateAmounts"
              >
                <template #append>%</template>
              </el-input-number>
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="已付金额">
              <el-input-number
                v-model="form.paid_amount"
                :precision="2"
                :min="0"
                :max="form.total_amount"
                placeholder="已付金额"
                :disabled="true"
                style="width: 100%;"
              />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="未付金额">
              <el-input-number
                v-model="form.remaining_amount"
                :precision="2"
                :disabled="true"
                style="width: 100%;"
              />
            </el-form-item>
          </el-col>
        </el-row>
      </div>

      <!-- 日期信息 -->
      <div class="form-section">
        <h3 class="section-title">日期信息</h3>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="开票日期" prop="bill_date" required>
              <el-date-picker
                v-model="form.bill_date"
                type="date"
                placeholder="请选择开票日期"
                format="YYYY-MM-DD"
                value-format="YYYY-MM-DD"
                style="width: 100%;"
                @change="calculateDueDate"
              />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="到期日期" prop="due_date" required>
              <el-date-picker
                v-model="form.due_date"
                type="date"
                placeholder="请选择到期日期"
                format="YYYY-MM-DD"
                value-format="YYYY-MM-DD"
                style="width: 100%;"
              />
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="账期" prop="payment_terms">
              <el-input-number
                v-model="form.payment_terms"
                :min="0"
                :max="365"
                placeholder="请输入账期天数"
                style="width: 100%;"
                @change="calculateDueDate"
              >
                <template #append>天</template>
              </el-input-number>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="提醒天数" prop="reminder_days">
              <el-input-number
                v-model="form.reminder_days"
                :min="0"
                :max="30"
                placeholder="请输入提醒天数"
                style="width: 100%;"
              >
                <template #append>天</template>
              </el-input-number>
            </el-form-item>
          </el-col>
        </el-row>
      </div>

      <!-- 供应商信息 -->
      <div v-if="supplierInfo" class="form-section">
        <h3 class="section-title">供应商信息</h3>
        <el-row :gutter="20">
          <el-col :span="12">
            <div class="info-item">
              <label>供应商名称：</label>
              <span>{{ supplierInfo.name }}</span>
            </div>
            <div class="info-item">
              <label>联系人：</label>
              <span>{{ supplierInfo.contact_person || '-' }}</span>
            </div>
            <div class="info-item">
              <label>联系电话：</label>
              <span>{{ supplierInfo.phone || '-' }}</span>
            </div>
          </el-col>
          <el-col :span="12">
            <div class="info-item">
              <label>邮箱：</label>
              <span>{{ supplierInfo.email || '-' }}</span>
            </div>
            <div class="info-item">
              <label>地址：</label>
              <span>{{ supplierInfo.address || '-' }}</span>
            </div>
            <div class="info-item">
              <label>信用等级：</label>
              <el-rate
                :model-value="supplierInfo.credit_rating || 0"
                disabled
                show-score
                text-color="#ff9900"
              />
            </div>
          </el-col>
        </el-row>
      </div>

      <!-- 备注信息 -->
      <div class="form-section">
        <h3 class="section-title">备注信息</h3>
        <el-form-item label="备注" prop="notes">
          <el-input
            v-model="form.notes"
            type="textarea"
            :rows="4"
            placeholder="请输入备注信息"
            maxlength="500"
            show-word-limit
          />
        </el-form-item>
      </div>

      <!-- 附件上传 -->
      <div class="form-section">
        <h3 class="section-title">附件</h3>
        <el-form-item label="附件上传">
          <el-upload
            ref="uploadRef"
            :file-list="fileList"
            :auto-upload="false"
            :on-change="handleFileChange"
            :on-remove="handleFileRemove"
            :before-upload="beforeUpload"
            multiple
            drag
          >
            <el-icon class="el-icon--upload"><UploadFilled /></el-icon>
            <div class="el-upload__text">
              将文件拖到此处，或<em>点击上传</em>
            </div>
            <template #tip>
              <div class="el-upload__tip">
                支持 jpg/png/pdf/doc/xls 等格式，单个文件不超过 10MB
              </div>
            </template>
          </el-upload>
        </el-form-item>
      </div>
    </el-form>

    <!-- 操作按钮 -->
    <div class="form-actions">
      <el-button @click="handleCancel">取消</el-button>
      <el-button type="primary" @click="handleSave('draft')" :loading="saving">
        保存草稿
      </el-button>
      <el-button type="success" @click="handleSave('confirmed')" :loading="saving">
        确认提交
      </el-button>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted, watch } from 'vue'
import { ElMessage } from 'element-plus'
import { api } from '@/utils/api'

// 定义属性和事件
const props = defineProps({
  payable: {
    type: Object,
    default: () => null
  }
})

const emit = defineEmits(['save', 'cancel'])

// 响应式数据
const formRef = ref()
const uploadRef = ref()
const loading = ref(false)
const saving = ref(false)
const suppliers = ref([])
const users = ref([])
const sourceOrders = ref([])
const supplierInfo = ref(null)
const fileList = ref([])

// 表单数据
const form = reactive({
  id: null,
  supplier_id: '',
  bill_number: '',
  source_type: 'manual',
  source_number: '',
  buyer: '',
  currency: 'CNY',
  total_amount: 0,
  paid_amount: 0,
  remaining_amount: 0,
  tax_rate: 13,
  bill_date: '',
  due_date: '',
  payment_terms: 30,
  reminder_days: 3,
  notes: ''
})

// 表单验证规则
const rules = {
  supplier_id: [
    { required: true, message: '请选择供应商', trigger: 'change' }
  ],
  source_type: [
    { required: true, message: '请选择来源类型', trigger: 'change' }
  ],
  total_amount: [
    { required: true, message: '请输入应付金额', trigger: 'blur' },
    { type: 'number', min: 0.01, message: '应付金额必须大于0', trigger: 'blur' }
  ],
  bill_date: [
    { required: true, message: '请选择开票日期', trigger: 'change' }
  ],
  due_date: [
    { required: true, message: '请选择到期日期', trigger: 'change' }
  ]
}

// 格式化金额
const formatAmount = (amount) => {
  return Number(amount || 0).toLocaleString('zh-CN', {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2
  })
}

// 计算金额
const calculateAmounts = () => {
  form.remaining_amount = form.total_amount - form.paid_amount
}

// 计算到期日期
const calculateDueDate = () => {
  if (form.bill_date && form.payment_terms) {
    const billDate = new Date(form.bill_date)
    const dueDate = new Date(billDate.getTime() + form.payment_terms * 24 * 60 * 60 * 1000)
    form.due_date = dueDate.toISOString().split('T')[0]
  }
}

// 供应商变化
const handleSupplierChange = async (supplierId) => {
  if (supplierId) {
    try {
      const response = await api.get(`/suppliers/${supplierId}`)
      supplierInfo.value = response.data
      
      // 如果是采购订单类型，获取该供应商的采购订单
      if (form.source_type === 'purchase_order') {
        fetchSourceOrders(supplierId)
      }
    } catch (error) {
      console.error('获取供应商信息失败:', error)
    }
  } else {
    supplierInfo.value = null
    sourceOrders.value = []
  }
}

// 来源类型变化
const handleSourceTypeChange = (sourceType) => {
  form.source_number = ''
  if (sourceType === 'purchase_order' && form.supplier_id) {
    fetchSourceOrders(form.supplier_id)
  } else {
    sourceOrders.value = []
  }
}

// 来源订单变化
const handleSourceOrderChange = async (orderNumber) => {
  if (orderNumber) {
    try {
      const response = await api.get(`/procurement/purchase-orders/by-number/${orderNumber}`)
      const order = response.data
      
      // 自动填充相关信息
      form.total_amount = order.total_amount
      form.buyer = order.buyer
      calculateAmounts()
    } catch (error) {
      console.error('获取采购订单信息失败:', error)
    }
  }
}

// 获取供应商列表
const fetchSuppliers = async () => {
  try {
    const response = await api.get('/suppliers', {
      params: { page: 1, size: 1000, status: 'active' }
    })
    suppliers.value = response.data.items
  } catch (error) {
    console.error('获取供应商列表失败:', error)
  }
}

// 获取用户列表
const fetchUsers = async () => {
  try {
    const response = await api.get('/users', {
      params: { page: 1, size: 1000, role: 'buyer' }
    })
    users.value = response.data.items
  } catch (error) {
    console.error('获取用户列表失败:', error)
  }
}

// 获取来源订单列表
const fetchSourceOrders = async (supplierId) => {
  try {
    const response = await api.get('/procurement/purchase-orders', {
      params: {
        supplier_id: supplierId,
        status: 'confirmed',
        page: 1,
        size: 100
      }
    })
    sourceOrders.value = response.data.items
  } catch (error) {
    console.error('获取采购订单列表失败:', error)
  }
}

// 文件变化
const handleFileChange = (file, fileList) => {
  // 文件大小检查
  if (file.size > 10 * 1024 * 1024) {
    ElMessage.error('文件大小不能超过 10MB')
    return false
  }
}

// 文件移除
const handleFileRemove = (file, fileList) => {
  // 处理文件移除逻辑
}

// 上传前检查
const beforeUpload = (file) => {
  const allowedTypes = [
    'image/jpeg',
    'image/png',
    'application/pdf',
    'application/msword',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    'application/vnd.ms-excel',
    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
  ]
  
  if (!allowedTypes.includes(file.type)) {
    ElMessage.error('不支持的文件格式')
    return false
  }
  
  return true
}

// 保存
const handleSave = async (status) => {
  try {
    await formRef.value.validate()
    
    saving.value = true
    
    const formData = new FormData()
    
    // 添加表单数据
    Object.keys(form).forEach(key => {
      if (form[key] !== null && form[key] !== '') {
        formData.append(key, form[key])
      }
    })
    
    formData.append('status', status)
    
    // 添加文件
    if (uploadRef.value) {
      uploadRef.value.uploadFiles.forEach(file => {
        if (file.raw) {
          formData.append('attachments', file.raw)
        }
      })
    }
    
    let response
    if (form.id) {
      response = await api.put(`/finance/payables/${form.id}`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      })
    } else {
      response = await api.post('/finance/payables', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      })
    }
    
    ElMessage.success(form.id ? '更新成功' : '创建成功')
    emit('save', response.data)
  } catch (error) {
    if (error.name !== 'ElFormValidateError') {
      ElMessage.error(form.id ? '更新失败' : '创建失败')
      console.error(error)
    }
  } finally {
    saving.value = false
  }
}

// 取消
const handleCancel = () => {
  emit('cancel')
}

// 初始化表单
const initForm = () => {
  if (props.payable) {
    Object.assign(form, props.payable)
    
    // 如果有供应商ID，获取供应商信息
    if (form.supplier_id) {
      handleSupplierChange(form.supplier_id)
    }
  } else {
    // 设置默认值
    const today = new Date().toISOString().split('T')[0]
    form.bill_date = today
    calculateDueDate()
  }
}

// 监听props变化
watch(() => props.payable, initForm, { immediate: true })

// 组件挂载
onMounted(() => {
  fetchSuppliers()
  fetchUsers()
})
</script>

<style scoped>
.payable-form {
  padding: 20px;
}

.form-section {
  margin-bottom: 32px;
  padding: 20px;
  background: #fafafa;
  border-radius: 8px;
  border: 1px solid #e9ecef;
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

.form-actions {
  text-align: center;
  padding: 20px 0;
  border-top: 1px solid #e9ecef;
  margin-top: 20px;
}

.form-actions .el-button {
  margin: 0 8px;
  min-width: 100px;
}

:deep(.el-form-item__label) {
  font-weight: 600;
  color: #606266;
}

:deep(.el-input-number) {
  width: 100%;
}

:deep(.el-upload-dragger) {
  width: 100%;
  height: 120px;
}

:deep(.el-rate) {
  display: inline-flex;
  align-items: center;
}

@media (max-width: 768px) {
  .payable-form {
    padding: 12px;
  }
  
  .form-section {
    padding: 16px;
    margin-bottom: 20px;
  }
  
  :deep(.el-col) {
    margin-bottom: 16px;
  }
  
  .form-actions {
    text-align: center;
  }
  
  .form-actions .el-button {
    margin: 8px 4px;
    min-width: 80px;
  }
}
</style>