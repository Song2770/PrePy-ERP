<template>
  <div class="receive-form">
    <el-form
      ref="formRef"
      :model="form"
      :rules="rules"
      label-width="120px"
      @submit.prevent
    >
      <!-- 应收信息 -->
      <div class="form-section">
        <h3 class="section-title">应收信息</h3>
        <el-row :gutter="20">
          <el-col :span="12">
            <div class="info-item">
              <label>单据号：</label>
              <span>{{ receivable.bill_number }}</span>
            </div>
            <div class="info-item">
              <label>客户：</label>
              <span>{{ receivable.customer_name }}</span>
            </div>
            <div class="info-item">
              <label>应收金额：</label>
              <span class="amount total">¥{{ formatAmount(receivable.total_amount) }}</span>
            </div>
          </el-col>
          <el-col :span="12">
            <div class="info-item">
              <label>已收金额：</label>
              <span class="amount received">¥{{ formatAmount(receivable.received_amount) }}</span>
            </div>
            <div class="info-item">
              <label>未收金额：</label>
              <span class="amount pending">¥{{ formatAmount(receivable.remaining_amount) }}</span>
            </div>
            <div class="info-item">
              <label>到期日期：</label>
              <span :class="getDueDateClass()">{{ receivable.due_date }}</span>
            </div>
          </el-col>
        </el-row>
      </div>

      <!-- 收款信息 -->
      <div class="form-section">
        <h3 class="section-title">收款信息</h3>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="收款日期" prop="receiveDate" required>
              <el-date-picker
                v-model="form.receiveDate"
                type="date"
                placeholder="选择收款日期"
                format="YYYY-MM-DD"
                value-format="YYYY-MM-DD"
                style="width: 100%"
              />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="收款金额" prop="receiveAmount" required>
              <el-input-number
                v-model="form.receiveAmount"
                :min="0.01"
                :max="receivable.remaining_amount"
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
            <el-form-item label="收款方式" prop="paymentMethod" required>
              <el-select
                v-model="form.paymentMethod"
                placeholder="请选择收款方式"
                style="width: 100%"
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
            <el-form-item label="收款账户" prop="accountId">
              <el-select
                v-model="form.accountId"
                placeholder="请选择收款账户"
                filterable
                style="width: 100%"
              >
                <el-option
                  v-for="account in accounts"
                  :key="account.id"
                  :label="account.name"
                  :value="account.id"
                />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="银行流水号" prop="bankReference">
              <el-input
                v-model="form.bankReference"
                placeholder="请输入银行流水号"
                maxlength="50"
              />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="收款人" prop="receiverId">
              <el-select
                v-model="form.receiverId"
                placeholder="请选择收款人"
                filterable
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
      </div>

      <!-- 费用信息 -->
      <div class="form-section">
        <h3 class="section-title">费用信息</h3>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="手续费" prop="handlingFee">
              <el-input-number
                v-model="form.handlingFee"
                :min="0"
                :precision="2"
                :step="0.01"
                style="width: 100%"
                @change="calculateActualAmount"
              />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="汇率" prop="exchangeRate">
              <el-input-number
                v-model="form.exchangeRate"
                :min="0.0001"
                :precision="4"
                :step="0.0001"
                style="width: 100%"
                @change="calculateActualAmount"
              />
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="实收金额">
              <el-input
                :value="actualAmount"
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
            <el-form-item label="收款后余额">
              <el-input
                :value="remainingAfterReceive"
                readonly
                style="width: 100%"
                :class="getRemainingClass()"
              >
                <template #prefix>
                  <span>¥</span>
                </template>
              </el-input>
            </el-form-item>
          </el-col>
        </el-row>
      </div>

      <!-- 核销信息 -->
      <div v-if="form.receiveAmount > 0" class="form-section">
        <h3 class="section-title">核销信息</h3>
        <el-table :data="writeOffItems" border>
          <el-table-column prop="bill_number" label="单据号" width="150" />
          <el-table-column prop="bill_type" label="单据类型" width="100">
            <template #default="{ row }">
              <el-tag size="small">{{ getBillTypeText(row.bill_type) }}</el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="original_amount" label="原始金额" width="120" align="right">
            <template #default="{ row }">
              <span>¥{{ formatAmount(row.original_amount) }}</span>
            </template>
          </el-table-column>
          <el-table-column prop="remaining_amount" label="未核销金额" width="120" align="right">
            <template #default="{ row }">
              <span>¥{{ formatAmount(row.remaining_amount) }}</span>
            </template>
          </el-table-column>
          <el-table-column label="本次核销" width="150">
            <template #default="{ row, $index }">
              <el-input-number
                v-model="row.write_off_amount"
                :min="0"
                :max="Math.min(row.remaining_amount, form.receiveAmount)"
                :precision="2"
                :step="1"
                size="small"
                style="width: 100%"
                @change="updateWriteOffAmount($index)"
              />
            </template>
          </el-table-column>
          <el-table-column prop="notes" label="备注">
            <template #default="{ row, $index }">
              <el-input
                v-model="row.notes"
                placeholder="输入备注"
                size="small"
              />
            </template>
          </el-table-column>
        </el-table>
        
        <div class="write-off-summary">
          <el-row :gutter="20">
            <el-col :span="8">
              <div class="summary-item">
                <label>收款金额：</label>
                <span class="amount">¥{{ formatAmount(form.receiveAmount) }}</span>
              </div>
            </el-col>
            <el-col :span="8">
              <div class="summary-item">
                <label>已核销金额：</label>
                <span class="amount">¥{{ formatAmount(totalWriteOffAmount) }}</span>
              </div>
            </el-col>
            <el-col :span="8">
              <div class="summary-item">
                <label>未核销金额：</label>
                <span class="amount" :class="getUnwrittenClass()">¥{{ formatAmount(unwrittenAmount) }}</span>
              </div>
            </el-col>
          </el-row>
        </div>
      </div>

      <!-- 备注信息 -->
      <div class="form-section">
        <h3 class="section-title">备注信息</h3>
        <el-row :gutter="20">
          <el-col :span="24">
            <el-form-item label="收款备注" prop="notes">
              <el-input
                v-model="form.notes"
                type="textarea"
                :rows="3"
                placeholder="请输入收款备注"
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
              支持银行回单、收据等凭证文件，jpg/png/pdf 格式，单个文件不超过 10MB
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
      <el-button type="primary" @click="saveReceive" :loading="saving">
        确认收款
      </el-button>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { api } from '@/utils/api'
import { useUserStore } from '@/stores/user'

// 定义属性和事件
const props = defineProps({
  receivable: {
    type: Object,
    required: true
  }
})

const emit = defineEmits(['success', 'cancel'])

// 响应式数据
const formRef = ref()
const saving = ref(false)
const accounts = ref([])
const users = ref([])
const writeOffItems = ref([])
const userStore = useUserStore()

// 表单数据
const form = reactive({
  receiveDate: new Date().toISOString().split('T')[0],
  receiveAmount: 0,
  paymentMethod: 'bank_transfer',
  accountId: null,
  bankReference: '',
  receiverId: userStore.userId,
  handlingFee: 0,
  exchangeRate: 1,
  notes: '',
  attachments: []
})

// 表单验证规则
const rules = {
  receiveDate: [
    { required: true, message: '请选择收款日期', trigger: 'change' }
  ],
  receiveAmount: [
    { required: true, message: '请输入收款金额', trigger: 'blur' },
    { type: 'number', min: 0.01, message: '收款金额必须大于0', trigger: 'blur' }
  ],
  paymentMethod: [
    { required: true, message: '请选择收款方式', trigger: 'change' }
  ]
}

// 上传配置
const uploadUrl = computed(() => `${api.defaults.baseURL}/upload`)
const uploadHeaders = computed(() => ({
  Authorization: `Bearer ${userStore.token}`
}))

// 计算实收金额
const actualAmount = computed(() => {
  return (form.receiveAmount * form.exchangeRate - form.handlingFee).toFixed(2)
})

// 计算收款后余额
const remainingAfterReceive = computed(() => {
  return (props.receivable.remaining_amount - form.receiveAmount).toFixed(2)
})

// 计算总核销金额
const totalWriteOffAmount = computed(() => {
  return writeOffItems.value.reduce((sum, item) => sum + (item.write_off_amount || 0), 0)
})

// 计算未核销金额
const unwrittenAmount = computed(() => {
  return form.receiveAmount - totalWriteOffAmount.value
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
  const today = new Date()
  const due = new Date(props.receivable.due_date)
  const diffDays = Math.ceil((due - today) / (1000 * 60 * 60 * 24))
  
  if (diffDays < 0) return 'overdue'
  if (diffDays <= 7) return 'near-due'
  return ''
}

// 获取余额样式
const getRemainingClass = () => {
  const remaining = parseFloat(remainingAfterReceive.value)
  return remaining <= 0 ? 'zero-balance' : ''
}

// 获取未核销金额样式
const getUnwrittenClass = () => {
  const unwritten = unwrittenAmount.value
  if (unwritten > 0) return 'positive'
  if (unwritten < 0) return 'negative'
  return 'zero'
}

// 获取单据类型文本
const getBillTypeText = (type) => {
  const typeMap = {
    'receivable': '应收账款',
    'advance': '预收款',
    'deposit': '保证金'
  }
  return typeMap[type] || '未知'
}

// 获取账户列表
const fetchAccounts = async () => {
  try {
    const response = await api.get('/finance/accounts', {
      params: { type: 'bank', status: 'active' }
    })
    accounts.value = response.data.items || []
  } catch (error) {
    console.error('获取账户列表失败:', error)
  }
}

// 获取用户列表
const fetchUsers = async () => {
  try {
    const response = await api.get('/users', {
      params: { status: 'active', page_size: 100 }
    })
    users.value = response.data.items || []
  } catch (error) {
    console.error('获取用户列表失败:', error)
  }
}

// 获取核销项目
const fetchWriteOffItems = async () => {
  try {
    const response = await api.get(`/finance/receivables/${props.receivable.id}/write-off-items`)
    writeOffItems.value = (response.data.items || []).map(item => ({
      ...item,
      write_off_amount: 0,
      notes: ''
    }))
  } catch (error) {
    console.error('获取核销项目失败:', error)
    // 默认核销项目
    writeOffItems.value = [{
      id: props.receivable.id,
      bill_number: props.receivable.bill_number,
      bill_type: 'receivable',
      original_amount: props.receivable.total_amount,
      remaining_amount: props.receivable.remaining_amount,
      write_off_amount: 0,
      notes: ''
    }]
  }
}

// 计算剩余金额
const calculateRemaining = () => {
  // 自动分配核销金额
  if (writeOffItems.value.length > 0 && form.receiveAmount > 0) {
    let remainingAmount = form.receiveAmount
    
    writeOffItems.value.forEach(item => {
      if (remainingAmount > 0) {
        const writeOffAmount = Math.min(remainingAmount, item.remaining_amount)
        item.write_off_amount = writeOffAmount
        remainingAmount -= writeOffAmount
      } else {
        item.write_off_amount = 0
      }
    })
  }
}

// 计算实收金额
const calculateActualAmount = () => {
  // 触发计算属性更新
}

// 更新核销金额
const updateWriteOffAmount = (index) => {
  // 确保核销金额不超过收款金额
  const totalWriteOff = writeOffItems.value.reduce((sum, item) => sum + (item.write_off_amount || 0), 0)
  if (totalWriteOff > form.receiveAmount) {
    const excess = totalWriteOff - form.receiveAmount
    writeOffItems.value[index].write_off_amount -= excess
  }
}

// 文件上传前验证
const beforeUpload = (file) => {
  const allowedTypes = [
    'image/jpeg',
    'image/png',
    'application/pdf'
  ]
  
  const isAllowedType = allowedTypes.includes(file.type)
  const isLt10M = file.size / 1024 / 1024 < 10
  
  if (!isAllowedType) {
    ElMessage.error('只支持 jpg/png/pdf 格式的文件')
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
    
    // 检查收款金额
    if (form.receiveAmount > props.receivable.remaining_amount) {
      ElMessage.error('收款金额不能超过未收金额')
      return false
    }
    
    // 检查核销金额
    if (totalWriteOffAmount.value > form.receiveAmount) {
      ElMessage.error('核销金额不能超过收款金额')
      return false
    }
    
    return true
  } catch (error) {
    return false
  }
}

// 保存收款
const saveReceive = async () => {
  if (!(await validateForm())) return
  
  try {
    saving.value = true
    
    const data = {
      receivable_id: props.receivable.id,
      receive_date: form.receiveDate,
      receive_amount: form.receiveAmount,
      payment_method: form.paymentMethod,
      account_id: form.accountId,
      bank_reference: form.bankReference,
      receiver_id: form.receiverId,
      handling_fee: form.handlingFee,
      exchange_rate: form.exchangeRate,
      notes: form.notes,
      write_off_items: writeOffItems.value.filter(item => item.write_off_amount > 0),
      attachments: form.attachments.map(file => ({
        name: file.name,
        url: file.response?.url || file.url,
        size: file.size
      }))
    }
    
    await api.post('/finance/receives', data)
    ElMessage.success('收款登记成功')
    emit('success')
  } catch (error) {
    console.error('收款登记失败:', error)
    ElMessage.error('收款登记失败')
  } finally {
    saving.value = false
  }
}

// 组件挂载
onMounted(() => {
  fetchAccounts()
  fetchUsers()
  fetchWriteOffItems()
  
  // 设置默认收款金额
  form.receiveAmount = props.receivable.remaining_amount
  calculateRemaining()
})
</script>

<style scoped>
.receive-form {
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

.amount.total {
  color: #5c6bc0;
}

.amount.received {
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

.zero-balance {
  color: #67c23a;
  font-weight: 600;
}

.write-off-summary {
  margin-top: 16px;
  padding: 16px;
  background: #f0f9ff;
  border-radius: 6px;
  border: 1px solid #b3d8ff;
}

.summary-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.summary-item label {
  font-weight: 600;
  color: #606266;
}

.summary-item .amount.positive {
  color: #e6a23c;
}

.summary-item .amount.negative {
  color: #f56c6c;
}

.summary-item .amount.zero {
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

:deep(.el-table) {
  font-size: 14px;
}

:deep(.el-table th) {
  background-color: #fafafa;
}

@media (max-width: 768px) {
  .receive-form {
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