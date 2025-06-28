<template>
  <div class="pay-form">
    <el-form
      ref="formRef"
      :model="form"
      :rules="rules"
      label-width="120px"
      v-loading="loading"
    >
      <!-- 应付账款信息 -->
      <div class="form-section">
        <h3 class="section-title">应付账款信息</h3>
        <el-row :gutter="20">
          <el-col :span="12">
            <div class="info-item">
              <label>单据号：</label>
              <span>{{ payable.bill_number }}</span>
            </div>
            <div class="info-item">
              <label>供应商：</label>
              <span>{{ payable.supplier_name }}</span>
            </div>
            <div class="info-item">
              <label>应付金额：</label>
              <span class="amount total">¥{{ formatAmount(payable.total_amount) }}</span>
            </div>
          </el-col>
          <el-col :span="12">
            <div class="info-item">
              <label>已付金额：</label>
              <span class="amount paid">¥{{ formatAmount(payable.paid_amount) }}</span>
            </div>
            <div class="info-item">
              <label>未付金额：</label>
              <span class="amount pending">¥{{ formatAmount(payable.remaining_amount) }}</span>
            </div>
            <div class="info-item">
              <label>到期日期：</label>
              <span :class="getDueDateClass()">{{ payable.due_date }}</span>
            </div>
          </el-col>
        </el-row>
      </div>

      <!-- 付款信息 -->
      <div class="form-section">
        <h3 class="section-title">付款信息</h3>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="付款日期" prop="pay_date" required>
              <el-date-picker
                v-model="form.pay_date"
                type="date"
                placeholder="请选择付款日期"
                format="YYYY-MM-DD"
                value-format="YYYY-MM-DD"
                style="width: 100%;"
              />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="付款金额" prop="pay_amount" required>
              <el-input-number
                v-model="form.pay_amount"
                :precision="2"
                :min="0.01"
                :max="payable.remaining_amount"
                placeholder="请输入付款金额"
                style="width: 100%;"
                @change="calculateAfterAmount"
              />
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="付款方式" prop="payment_method" required>
              <el-select
                v-model="form.payment_method"
                placeholder="请选择付款方式"
                style="width: 100%;"
              >
                <el-option label="现金" value="cash" />
                <el-option label="银行转账" value="bank_transfer" />
                <el-option label="支票" value="check" />
                <el-option label="信用卡" value="credit_card" />
                <el-option label="支付宝" value="alipay" />
                <el-option label="微信支付" value="wechat_pay" />
                <el-option label="其他" value="other" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="付款账户" prop="account_id" required>
              <el-select
                v-model="form.account_id"
                placeholder="请选择付款账户"
                filterable
                style="width: 100%;"
              >
                <el-option
                  v-for="account in accounts"
                  :key="account.id"
                  :label="`${account.name} (${account.account_number})`"
                  :value="account.id"
                />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="银行流水号" prop="bank_reference">
              <el-input
                v-model="form.bank_reference"
                placeholder="请输入银行流水号"
              />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="付款人" prop="payer">
              <el-select
                v-model="form.payer"
                placeholder="请选择付款人"
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
        </el-row>
      </div>

      <!-- 费用信息 -->
      <div class="form-section">
        <h3 class="section-title">费用信息</h3>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="手续费" prop="handling_fee">
              <el-input-number
                v-model="form.handling_fee"
                :precision="2"
                :min="0"
                placeholder="请输入手续费"
                style="width: 100%;"
                @change="calculateAfterAmount"
              />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="汇率" prop="exchange_rate">
              <el-input-number
                v-model="form.exchange_rate"
                :precision="4"
                :min="0.0001"
                placeholder="请输入汇率"
                style="width: 100%;"
                @change="calculateAfterAmount"
              />
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="实际付款">
              <el-input-number
                v-model="actualPayAmount"
                :precision="2"
                :disabled="true"
                style="width: 100%;"
              />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="付款后余额">
              <el-input-number
                v-model="afterPayAmount"
                :precision="2"
                :disabled="true"
                style="width: 100%;"
              />
            </el-form-item>
          </el-col>
        </el-row>
      </div>

      <!-- 核销信息 -->
      <div class="form-section">
        <h3 class="section-title">核销信息</h3>
        <div class="write-off-header">
          <el-button size="small" @click="addWriteOffItem">
            <el-icon><Plus /></el-icon>
            添加核销项
          </el-button>
        </div>
        
        <el-table :data="form.write_off_items" border>
          <el-table-column prop="bill_type" label="单据类型" width="120">
            <template #default="{ row, $index }">
              <el-select
                v-model="row.bill_type"
                placeholder="请选择"
                size="small"
                @change="handleBillTypeChange($index)"
              >
                <el-option label="预付账款" value="advance" />
                <el-option label="其他应付" value="other_payable" />
              </el-select>
            </template>
          </el-table-column>
          
          <el-table-column prop="bill_number" label="单据号" width="150">
            <template #default="{ row, $index }">
              <el-select
                v-model="row.bill_number"
                placeholder="请选择单据"
                size="small"
                filterable
              >
                <el-option
                  v-for="bill in getAvailableBills(row.bill_type)"
                  :key="bill.bill_number"
                  :label="`${bill.bill_number} - ¥${formatAmount(bill.available_amount)}`"
                  :value="bill.bill_number"
                />
              </el-select>
            </template>
          </el-table-column>
          
          <el-table-column prop="write_off_amount" label="核销金额" width="120">
            <template #default="{ row }">
              <el-input-number
                v-model="row.write_off_amount"
                :precision="2"
                :min="0"
                size="small"
                style="width: 100%;"
              />
            </template>
          </el-table-column>
          
          <el-table-column prop="notes" label="备注">
            <template #default="{ row }">
              <el-input
                v-model="row.notes"
                placeholder="请输入备注"
                size="small"
              />
            </template>
          </el-table-column>
          
          <el-table-column label="操作" width="80">
            <template #default="{ $index }">
              <el-button
                size="small"
                type="danger"
                @click="removeWriteOffItem($index)"
              >
                删除
              </el-button>
            </template>
          </el-table-column>
        </el-table>
        
        <div v-if="form.write_off_items.length === 0" class="empty-write-off">
          <el-empty description="暂无核销项" :image-size="60" />
        </div>
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
      <el-button type="primary" @click="handleSave" :loading="saving">
        确认付款
      </el-button>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { api } from '@/utils/api'

// 定义属性和事件
const props = defineProps({
  payable: {
    type: Object,
    required: true
  }
})

const emit = defineEmits(['save', 'cancel'])

// 响应式数据
const formRef = ref()
const uploadRef = ref()
const loading = ref(false)
const saving = ref(false)
const accounts = ref([])
const users = ref([])
const advanceBills = ref([])
const otherPayableBills = ref([])
const fileList = ref([])

// 表单数据
const form = reactive({
  payable_id: props.payable.id,
  pay_date: '',
  pay_amount: 0,
  payment_method: 'bank_transfer',
  account_id: '',
  bank_reference: '',
  payer: '',
  handling_fee: 0,
  exchange_rate: 1,
  write_off_items: [],
  notes: ''
})

// 表单验证规则
const rules = {
  pay_date: [
    { required: true, message: '请选择付款日期', trigger: 'change' }
  ],
  pay_amount: [
    { required: true, message: '请输入付款金额', trigger: 'blur' },
    { type: 'number', min: 0.01, message: '付款金额必须大于0', trigger: 'blur' }
  ],
  payment_method: [
    { required: true, message: '请选择付款方式', trigger: 'change' }
  ],
  account_id: [
    { required: true, message: '请选择付款账户', trigger: 'change' }
  ]
}

// 计算实际付款金额
const actualPayAmount = computed(() => {
  return form.pay_amount + form.handling_fee
})

// 计算付款后余额
const afterPayAmount = computed(() => {
  return props.payable.remaining_amount - form.pay_amount
})

// 格式化金额
const formatAmount = (amount) => {
  return Number(amount || 0).toLocaleString('zh-CN', {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2
  })
}

// 获取到期日期样式
const getDueDateClass = () => {
  if (props.payable.status === 'paid') return ''
  
  const today = new Date()
  const due = new Date(props.payable.due_date)
  const diffDays = Math.ceil((due - today) / (1000 * 60 * 60 * 24))
  
  if (diffDays < 0) return 'overdue'
  if (diffDays <= 7) return 'near-due'
  return ''
}

// 计算付款后金额
const calculateAfterAmount = () => {
  // 触发计算属性更新
}

// 获取可用单据
const getAvailableBills = (billType) => {
  switch (billType) {
    case 'advance':
      return advanceBills.value
    case 'other_payable':
      return otherPayableBills.value
    default:
      return []
  }
}

// 添加核销项
const addWriteOffItem = () => {
  form.write_off_items.push({
    bill_type: '',
    bill_number: '',
    write_off_amount: 0,
    notes: ''
  })
}

// 移除核销项
const removeWriteOffItem = (index) => {
  form.write_off_items.splice(index, 1)
}

// 单据类型变化
const handleBillTypeChange = (index) => {
  form.write_off_items[index].bill_number = ''
}

// 获取账户列表
const fetchAccounts = async () => {
  try {
    const response = await api.get('/finance/accounts', {
      params: { page: 1, size: 1000, status: 'active' }
    })
    accounts.value = response.data.items
  } catch (error) {
    console.error('获取账户列表失败:', error)
  }
}

// 获取用户列表
const fetchUsers = async () => {
  try {
    const response = await api.get('/users', {
      params: { page: 1, size: 1000 }
    })
    users.value = response.data.items
  } catch (error) {
    console.error('获取用户列表失败:', error)
  }
}

// 获取预付账款列表
const fetchAdvanceBills = async () => {
  try {
    const response = await api.get('/finance/advances', {
      params: {
        supplier_id: props.payable.supplier_id,
        status: 'available',
        page: 1,
        size: 100
      }
    })
    advanceBills.value = response.data.items
  } catch (error) {
    console.error('获取预付账款列表失败:', error)
  }
}

// 获取其他应付列表
const fetchOtherPayableBills = async () => {
  try {
    const response = await api.get('/finance/other-payables', {
      params: {
        supplier_id: props.payable.supplier_id,
        status: 'available',
        page: 1,
        size: 100
      }
    })
    otherPayableBills.value = response.data.items
  } catch (error) {
    console.error('获取其他应付列表失败:', error)
  }
}

// 文件变化
const handleFileChange = (file, fileList) => {
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
const handleSave = async () => {
  try {
    await formRef.value.validate()
    
    saving.value = true
    
    const formData = new FormData()
    
    // 添加表单数据
    Object.keys(form).forEach(key => {
      if (key === 'write_off_items') {
        formData.append(key, JSON.stringify(form[key]))
      } else if (form[key] !== null && form[key] !== '') {
        formData.append(key, form[key])
      }
    })
    
    // 添加文件
    if (uploadRef.value) {
      uploadRef.value.uploadFiles.forEach(file => {
        if (file.raw) {
          formData.append('attachments', file.raw)
        }
      })
    }
    
    const response = await api.post('/finance/payments', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
    
    ElMessage.success('付款登记成功')
    emit('save', response.data)
  } catch (error) {
    if (error.name !== 'ElFormValidateError') {
      ElMessage.error('付款登记失败')
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
  const today = new Date().toISOString().split('T')[0]
  form.pay_date = today
  form.pay_amount = props.payable.remaining_amount
}

// 组件挂载
onMounted(() => {
  initForm()
  fetchAccounts()
  fetchUsers()
  fetchAdvanceBills()
  fetchOtherPayableBills()
})
</script>

<style scoped>
.pay-form {
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

.amount {
  font-weight: 600;
  font-family: 'Courier New', monospace;
}

.amount.total {
  color: #5c6bc0;
}

.amount.paid {
  color: #67c23a;
}

.amount.pending {
  color: #e6a23c;
}

.overdue {
  color: #f56c6c;
  font-weight: 600;
}

.near-due {
  color: #e6a23c;
  font-weight: 600;
}

.write-off-header {
  margin-bottom: 16px;
  text-align: right;
}

.empty-write-off {
  padding: 40px 0;
  text-align: center;
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

:deep(.el-table) {
  font-size: 14px;
}

:deep(.el-table th) {
  background-color: #f5f7fa;
}

@media (max-width: 768px) {
  .pay-form {
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
  
  :deep(.el-table) {
    font-size: 12px;
  }
}
</style>