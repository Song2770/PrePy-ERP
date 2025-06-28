<template>
  <div class="receivable-form">
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
            <el-form-item label="客户" prop="customerId" required>
              <el-select
                v-model="form.customerId"
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
            <el-form-item label="单据号" prop="billNumber" required>
              <el-input
                v-model="form.billNumber"
                placeholder="系统自动生成或手动输入"
                maxlength="50"
              />
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="来源类型" prop="sourceType" required>
              <el-select
                v-model="form.sourceType"
                placeholder="请选择来源类型"
                style="width: 100%"
                @change="handleSourceTypeChange"
              >
                <el-option label="销售订单" value="sales_order" />
                <el-option label="服务订单" value="service_order" />
                <el-option label="手工录入" value="manual" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="来源单号" prop="sourceNumber">
              <el-select
                v-if="form.sourceType !== 'manual'"
                v-model="form.sourceNumber"
                placeholder="请选择来源单号"
                filterable
                style="width: 100%"
                @change="handleSourceNumberChange"
              >
                <el-option
                  v-for="order in sourceOrders"
                  :key="order.id"
                  :label="order.order_number"
                  :value="order.order_number"
                />
              </el-select>
              <el-input
                v-else
                v-model="form.sourceNumber"
                placeholder="请输入来源单号"
                maxlength="50"
              />
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="销售员" prop="salespersonId">
              <el-select
                v-model="form.salespersonId"
                placeholder="请选择销售员"
                filterable
                style="width: 100%"
              >
                <el-option
                  v-for="user in salespeople"
                  :key="user.id"
                  :label="user.name"
                  :value="user.id"
                />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="币种" prop="currency">
              <el-select
                v-model="form.currency"
                placeholder="请选择币种"
                style="width: 100%"
              >
                <el-option label="人民币 (CNY)" value="CNY" />
                <el-option label="美元 (USD)" value="USD" />
                <el-option label="欧元 (EUR)" value="EUR" />
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
            <el-form-item label="应收金额" prop="totalAmount" required>
              <el-input-number
                v-model="form.totalAmount"
                :min="0"
                :precision="2"
                :step="1"
                style="width: 100%"
                @change="calculateRemaining"
              />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="已收金额" prop="receivedAmount">
              <el-input-number
                v-model="form.receivedAmount"
                :min="0"
                :max="form.totalAmount"
                :precision="2"
                :step="1"
                style="width: 100%"
                @change="calculateRemaining"
              />
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="未收金额">
              <el-input
                :value="remainingAmount"
                readonly
                style="width: 100%"
              >
                <template #prefix>
                  <span>¥</span>
                </template>
              </el-input>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="税率(%)" prop="taxRate">
              <el-input-number
                v-model="form.taxRate"
                :min="0"
                :max="100"
                :precision="2"
                :step="1"
                style="width: 100%"
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
            <el-form-item label="开票日期" prop="billDate" required>
              <el-date-picker
                v-model="form.billDate"
                type="date"
                placeholder="选择开票日期"
                format="YYYY-MM-DD"
                value-format="YYYY-MM-DD"
                style="width: 100%"
              />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="到期日期" prop="dueDate" required>
              <el-date-picker
                v-model="form.dueDate"
                type="date"
                placeholder="选择到期日期"
                format="YYYY-MM-DD"
                value-format="YYYY-MM-DD"
                style="width: 100%"
                :disabled-date="disabledDate"
              />
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="账期(天)" prop="paymentTerms">
              <el-input-number
                v-model="form.paymentTerms"
                :min="0"
                :step="1"
                style="width: 100%"
                @change="calculateDueDate"
              />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="提醒天数" prop="reminderDays">
              <el-input-number
                v-model="form.reminderDays"
                :min="0"
                :step="1"
                style="width: 100%"
              />
            </el-form-item>
          </el-col>
        </el-row>
      </div>

      <!-- 客户信息 -->
      <div v-if="selectedCustomer" class="form-section">
        <h3 class="section-title">客户信息</h3>
        <el-row :gutter="20">
          <el-col :span="12">
            <div class="info-item">
              <label>客户名称：</label>
              <span>{{ selectedCustomer.name }}</span>
            </div>
            <div class="info-item">
              <label>联系人：</label>
              <span>{{ selectedCustomer.contact_person || '-' }}</span>
            </div>
            <div class="info-item">
              <label>联系电话：</label>
              <span>{{ selectedCustomer.phone || '-' }}</span>
            </div>
          </el-col>
          <el-col :span="12">
            <div class="info-item">
              <label>信用额度：</label>
              <span class="amount">¥{{ formatAmount(selectedCustomer.credit_limit) }}</span>
            </div>
            <div class="info-item">
              <label>已用额度：</label>
              <span class="amount used">¥{{ formatAmount(selectedCustomer.used_credit) }}</span>
            </div>
            <div class="info-item">
              <label>可用额度：</label>
              <span class="amount available">¥{{ formatAmount(selectedCustomer.available_credit) }}</span>
            </div>
          </el-col>
        </el-row>
      </div>

      <!-- 备注信息 -->
      <div class="form-section">
        <h3 class="section-title">备注信息</h3>
        <el-row :gutter="20">
          <el-col :span="24">
            <el-form-item label="备注" prop="notes">
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

      <!-- 附件上传 -->
      <div class="form-section">
        <h3 class="section-title">附件</h3>
        <el-upload
          v-model:file-list="form.attachments"
          :action="uploadUrl"
          :headers="uploadHeaders"
          :on-success="handleUploadSuccess"
          :on-error="handleUploadError"
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
              支持 jpg/png/pdf/doc/docx/xls/xlsx 格式，单个文件不超过 10MB
            </div>
          </template>
        </el-upload>
      </div>
    </el-form>

    <!-- 操作按钮 -->
    <div class="form-actions">
      <el-button @click="$emit('cancel')">
        取消
      </el-button>
      <el-button @click="saveDraft" :loading="saving">
        保存草稿
      </el-button>
      <el-button type="primary" @click="saveReceivable" :loading="saving">
        确认保存
      </el-button>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { api } from '@/utils/api'
import { useUserStore } from '@/stores/user'

// 定义事件
const emit = defineEmits(['success', 'cancel'])

// 响应式数据
const formRef = ref()
const saving = ref(false)
const customers = ref([])
const salespeople = ref([])
const sourceOrders = ref([])
const selectedCustomer = ref(null)
const userStore = useUserStore()

// 表单数据
const form = reactive({
  customerId: null,
  billNumber: '',
  sourceType: 'manual',
  sourceNumber: '',
  salespersonId: null,
  currency: 'CNY',
  totalAmount: 0,
  receivedAmount: 0,
  taxRate: 13,
  billDate: new Date().toISOString().split('T')[0],
  dueDate: '',
  paymentTerms: 30,
  reminderDays: 3,
  notes: '',
  attachments: []
})

// 表单验证规则
const rules = {
  customerId: [
    { required: true, message: '请选择客户', trigger: 'change' }
  ],
  billNumber: [
    { required: true, message: '请输入单据号', trigger: 'blur' }
  ],
  sourceType: [
    { required: true, message: '请选择来源类型', trigger: 'change' }
  ],
  totalAmount: [
    { required: true, message: '请输入应收金额', trigger: 'blur' },
    { type: 'number', min: 0.01, message: '应收金额必须大于0', trigger: 'blur' }
  ],
  billDate: [
    { required: true, message: '请选择开票日期', trigger: 'change' }
  ],
  dueDate: [
    { required: true, message: '请选择到期日期', trigger: 'change' }
  ]
}

// 上传配置
const uploadUrl = computed(() => `${api.defaults.baseURL}/upload`)
const uploadHeaders = computed(() => ({
  Authorization: `Bearer ${userStore.token}`
}))

// 计算未收金额
const remainingAmount = computed(() => {
  return (form.totalAmount - form.receivedAmount).toFixed(2)
})

// 格式化金额
const formatAmount = (amount) => {
  return Number(amount || 0).toLocaleString('zh-CN', {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2
  })
}

// 禁用日期
const disabledDate = (time) => {
  if (!form.billDate) return false
  return time.getTime() < new Date(form.billDate).getTime()
}

// 获取客户列表
const fetchCustomers = async () => {
  try {
    const response = await api.get('/customers', {
      params: { page_size: 1000, status: 'active' }
    })
    customers.value = response.data.items || []
  } catch (error) {
    console.error('获取客户列表失败:', error)
  }
}

// 获取销售员列表
const fetchSalespeople = async () => {
  try {
    const response = await api.get('/users', {
      params: { role: 'salesperson', status: 'active' }
    })
    salespeople.value = response.data.items || []
  } catch (error) {
    console.error('获取销售员列表失败:', error)
  }
}

// 获取来源订单列表
const fetchSourceOrders = async (type, customerId) => {
  if (!type || type === 'manual' || !customerId) {
    sourceOrders.value = []
    return
  }
  
  try {
    const endpoint = type === 'sales_order' ? '/sales/orders' : '/service/orders'
    const response = await api.get(endpoint, {
      params: {
        customer_id: customerId,
        status: 'confirmed',
        page_size: 100
      }
    })
    sourceOrders.value = response.data.items || []
  } catch (error) {
    console.error('获取来源订单失败:', error)
    sourceOrders.value = []
  }
}

// 生成单据号
const generateBillNumber = async () => {
  try {
    const response = await api.get('/finance/receivables/generate-number')
    form.billNumber = response.data.number
  } catch (error) {
    console.error('生成单据号失败:', error)
  }
}

// 客户变化处理
const handleCustomerChange = async (customerId) => {
  if (!customerId) {
    selectedCustomer.value = null
    return
  }
  
  try {
    const response = await api.get(`/customers/${customerId}`)
    selectedCustomer.value = response.data
    
    // 设置默认销售员
    if (response.data.salesperson_id) {
      form.salespersonId = response.data.salesperson_id
    }
    
    // 设置默认账期
    if (response.data.payment_terms) {
      form.paymentTerms = response.data.payment_terms
      calculateDueDate()
    }
    
    // 获取来源订单
    await fetchSourceOrders(form.sourceType, customerId)
  } catch (error) {
    console.error('获取客户信息失败:', error)
  }
}

// 来源类型变化处理
const handleSourceTypeChange = async (type) => {
  form.sourceNumber = ''
  if (form.customerId) {
    await fetchSourceOrders(type, form.customerId)
  }
}

// 来源单号变化处理
const handleSourceNumberChange = async (orderNumber) => {
  if (!orderNumber) return
  
  try {
    const order = sourceOrders.value.find(o => o.order_number === orderNumber)
    if (order) {
      form.totalAmount = order.total_amount
      form.billDate = order.order_date
      calculateDueDate()
    }
  } catch (error) {
    console.error('获取订单信息失败:', error)
  }
}

// 计算到期日期
const calculateDueDate = () => {
  if (form.billDate && form.paymentTerms) {
    const billDate = new Date(form.billDate)
    const dueDate = new Date(billDate.getTime() + form.paymentTerms * 24 * 60 * 60 * 1000)
    form.dueDate = dueDate.toISOString().split('T')[0]
  }
}

// 计算未收金额
const calculateRemaining = () => {
  // 触发计算属性更新
}

// 文件上传前验证
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
  
  const isAllowedType = allowedTypes.includes(file.type)
  const isLt10M = file.size / 1024 / 1024 < 10
  
  if (!isAllowedType) {
    ElMessage.error('只支持 jpg/png/pdf/doc/docx/xls/xlsx 格式的文件')
    return false
  }
  
  if (!isLt10M) {
    ElMessage.error('文件大小不能超过 10MB')
    return false
  }
  
  return true
}

// 文件上传成功
const handleUploadSuccess = (response, file) => {
  ElMessage.success('文件上传成功')
}

// 文件上传失败
const handleUploadError = (error, file) => {
  console.error('文件上传失败:', error)
  ElMessage.error('文件上传失败')
}

// 验证表单
const validateForm = async () => {
  try {
    await formRef.value.validate()
    
    // 检查信用额度
    if (selectedCustomer.value && selectedCustomer.value.credit_limit > 0) {
      const totalUsed = selectedCustomer.value.used_credit + form.totalAmount
      if (totalUsed > selectedCustomer.value.credit_limit) {
        ElMessage.warning('超出客户信用额度，请谨慎操作')
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
      ...form,
      status: 'draft',
      attachments: form.attachments.map(file => ({
        name: file.name,
        url: file.response?.url || file.url,
        size: file.size
      }))
    }
    
    await api.post('/finance/receivables', data)
    ElMessage.success('草稿保存成功')
    emit('success')
  } catch (error) {
    console.error('保存草稿失败:', error)
    ElMessage.error('保存草稿失败')
  } finally {
    saving.value = false
  }
}

// 保存应收账款
const saveReceivable = async () => {
  if (!(await validateForm())) return
  
  try {
    saving.value = true
    
    const data = {
      ...form,
      status: 'pending',
      attachments: form.attachments.map(file => ({
        name: file.name,
        url: file.response?.url || file.url,
        size: file.size
      }))
    }
    
    await api.post('/finance/receivables', data)
    ElMessage.success('应收账款创建成功')
    emit('success')
  } catch (error) {
    console.error('创建应收账款失败:', error)
    ElMessage.error('创建应收账款失败')
  } finally {
    saving.value = false
  }
}

// 组件挂载
onMounted(() => {
  fetchCustomers()
  fetchSalespeople()
  generateBillNumber()
  calculateDueDate()
})
</script>

<style scoped>
.receivable-form {
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

.info-item {
  margin-bottom: 12px;
  display: flex;
  align-items: center;
}

.info-item label {
  font-weight: 600;
  color: #606266;
  margin-right: 8px;
  min-width: 80px;
}

.amount {
  font-weight: 600;
  font-family: 'Courier New', monospace;
}

.amount.used {
  color: #e6a23c;
}

.amount.available {
  color: #67c23a;
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

:deep(.el-form-item) {
  margin-bottom: 20px;
}

:deep(.el-input-number .el-input__inner) {
  text-align: left;
}

:deep(.el-upload-dragger) {
  width: 100%;
  height: 120px;
}

@media (max-width: 768px) {
  .receivable-form {
    padding: 12px;
  }
  
  .form-section {
    padding: 16px;
    margin-bottom: 20px;
  }
  
  .form-actions {
    text-align: center;
  }
  
  .form-actions .el-button {
    margin: 0 6px 8px 6px;
  }
}
</style>