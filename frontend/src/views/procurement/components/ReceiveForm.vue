<template>
  <div class="receive-form">
    <el-form
      ref="formRef"
      :model="form"
      :rules="rules"
      label-width="120px"
      @submit.prevent
    >
      <!-- 采购单信息 -->
      <div class="form-section">
        <h3 class="section-title">采购单信息</h3>
        <el-row :gutter="20">
          <el-col :span="8">
            <div class="info-item">
              <label>采购单号：</label>
              <span>{{ purchaseOrder.purchase_order_number }}</span>
            </div>
          </el-col>
          <el-col :span="8">
            <div class="info-item">
              <label>供应商：</label>
              <span>{{ purchaseOrder.supplier_name }}</span>
            </div>
          </el-col>
          <el-col :span="8">
            <div class="info-item">
              <label>采购日期：</label>
              <span>{{ formatDate(purchaseOrder.order_date) }}</span>
            </div>
          </el-col>
        </el-row>
      </div>

      <!-- 收货信息 -->
      <div class="form-section">
        <h3 class="section-title">收货信息</h3>
        <el-row :gutter="20">
          <el-col :span="8">
            <el-form-item label="收货日期" prop="receiveDate" required>
              <el-date-picker
                v-model="form.receiveDate"
                type="date"
                placeholder="选择收货日期"
                format="YYYY-MM-DD"
                value-format="YYYY-MM-DD"
                style="width: 100%"
              />
            </el-form-item>
          </el-col>
          
          <el-col :span="8">
            <el-form-item label="收货人" prop="receiverId">
              <el-select
                v-model="form.receiverId"
                placeholder="请选择收货人"
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
          
          <el-col :span="8">
            <el-form-item label="仓库" prop="warehouseId">
              <el-select
                v-model="form.warehouseId"
                placeholder="请选择仓库"
                filterable
                clearable
                style="width: 100%"
              >
                <el-option
                  v-for="warehouse in warehouses"
                  :key="warehouse.id"
                  :label="warehouse.name"
                  :value="warehouse.id"
                />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-row :gutter="20">
          <el-col :span="24">
            <el-form-item label="收货备注">
              <el-input
                v-model="form.notes"
                type="textarea"
                :rows="3"
                placeholder="请输入收货备注"
                maxlength="500"
                show-word-limit
              />
            </el-form-item>
          </el-col>
        </el-row>
      </div>

      <!-- 收货明细 -->
      <div class="form-section">
        <h3 class="section-title">收货明细</h3>
        
        <el-table :data="form.receiveLines" border>
          <el-table-column label="序号" type="index" width="60" align="center" />
          
          <el-table-column label="商品" width="200">
            <template #default="{ row }">
              <div class="product-info">
                <div class="product-name">{{ row.product_name }}</div>
                <div class="product-code">{{ row.product_code }}</div>
              </div>
            </template>
          </el-table-column>
          
          <el-table-column label="规格" width="120">
            <template #default="{ row }">
              <span>{{ row.product_spec || '-' }}</span>
            </template>
          </el-table-column>
          
          <el-table-column label="单位" width="80">
            <template #default="{ row }">
              <span>{{ row.product_unit || '-' }}</span>
            </template>
          </el-table-column>
          
          <el-table-column label="采购数量" width="100" align="right">
            <template #default="{ row }">
              <span>{{ row.ordered_quantity }}</span>
            </template>
          </el-table-column>
          
          <el-table-column label="已收数量" width="100" align="right">
            <template #default="{ row }">
              <span>{{ row.received_quantity || 0 }}</span>
            </template>
          </el-table-column>
          
          <el-table-column label="本次收货" width="120" required>
            <template #default="{ row }">
              <el-input-number
                v-model="row.current_receive_quantity"
                :min="0"
                :max="row.ordered_quantity - (row.received_quantity || 0)"
                :precision="2"
                :step="1"
                style="width: 100%"
                @change="validateReceiveQuantity(row)"
              />
            </template>
          </el-table-column>
          
          <el-table-column label="收货后库存" width="100" align="right">
            <template #default="{ row }">
              <span>{{ (row.received_quantity || 0) + (row.current_receive_quantity || 0) }}</span>
            </template>
          </el-table-column>
          
          <el-table-column label="单价" width="100" align="right">
            <template #default="{ row }">
              <span>¥{{ formatCurrency(row.unit_price) }}</span>
            </template>
          </el-table-column>
          
          <el-table-column label="收货金额" width="120" align="right">
            <template #default="{ row }">
              <span class="amount-text">
                ¥{{ formatCurrency((row.current_receive_quantity || 0) * row.unit_price) }}
              </span>
            </template>
          </el-table-column>
          
          <el-table-column label="质检状态" width="120">
            <template #default="{ row }">
              <el-select
                v-model="row.quality_status"
                placeholder="质检状态"
                size="small"
                style="width: 100%"
              >
                <el-option label="合格" value="qualified" />
                <el-option label="不合格" value="unqualified" />
                <el-option label="待检" value="pending" />
              </el-select>
            </template>
          </el-table-column>
          
          <el-table-column label="备注" width="150">
            <template #default="{ row }">
              <el-input
                v-model="row.notes"
                placeholder="备注"
                size="small"
                maxlength="100"
              />
            </template>
          </el-table-column>
        </el-table>
      </div>

      <!-- 收货汇总 -->
      <div class="form-section">
        <h3 class="section-title">收货汇总</h3>
        <el-row :gutter="20">
          <el-col :span="6">
            <div class="summary-item">
              <label>收货品种：</label>
              <span class="summary-value">{{ receiveItemCount }}</span>
            </div>
          </el-col>
          <el-col :span="6">
            <div class="summary-item">
              <label>收货数量：</label>
              <span class="summary-value">{{ totalReceiveQuantity }}</span>
            </div>
          </el-col>
          <el-col :span="6">
            <div class="summary-item">
              <label>收货金额：</label>
              <span class="summary-value">¥{{ formatCurrency(totalReceiveAmount) }}</span>
            </div>
          </el-col>
          <el-col :span="6">
            <div class="summary-item">
              <label>完成进度：</label>
              <span class="summary-value">{{ receiveProgress }}%</span>
            </div>
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
      <el-button type="primary" @click="saveReceive" :loading="saving">
        确认收货
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
  purchaseOrder: {
    type: Object,
    required: true
  }
})

const emit = defineEmits(['success', 'cancel'])

// 响应式数据
const formRef = ref()
const saving = ref(false)
const users = ref([])
const warehouses = ref([])
const userStore = useUserStore()

// 表单数据
const form = reactive({
  receiveDate: new Date().toISOString().split('T')[0],
  receiverId: userStore.userInfo?.id,
  warehouseId: null,
  notes: '',
  receiveLines: [],
  attachments: []
})

// 表单验证规则
const rules = {
  receiveDate: [
    { required: true, message: '请选择收货日期', trigger: 'change' }
  ]
}

// 上传配置
const uploadUrl = computed(() => `${api.defaults.baseURL}/upload`)
const uploadHeaders = computed(() => ({
  Authorization: `Bearer ${userStore.token}`
}))

// 计算属性
const receiveItemCount = computed(() => {
  return form.receiveLines.filter(line => (line.current_receive_quantity || 0) > 0).length
})

const totalReceiveQuantity = computed(() => {
  return form.receiveLines.reduce((sum, line) => sum + (line.current_receive_quantity || 0), 0)
})

const totalReceiveAmount = computed(() => {
  return form.receiveLines.reduce((sum, line) => {
    return sum + ((line.current_receive_quantity || 0) * line.unit_price)
  }, 0)
})

const receiveProgress = computed(() => {
  const totalOrdered = form.receiveLines.reduce((sum, line) => sum + line.ordered_quantity, 0)
  const totalReceived = form.receiveLines.reduce((sum, line) => {
    return sum + (line.received_quantity || 0) + (line.current_receive_quantity || 0)
  }, 0)
  
  if (totalOrdered === 0) return 0
  return Math.round((totalReceived / totalOrdered) * 100)
})

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

// 获取用户列表
const fetchUsers = async () => {
  try {
    const response = await api.get('/users')
    users.value = response.data.items || []
  } catch (error) {
    console.error('获取用户列表失败:', error)
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

// 获取采购单明细
const fetchPurchaseOrderLines = async () => {
  try {
    const response = await api.get(`/procurement/purchase-orders/${props.purchaseOrder.id}/lines`)
    form.receiveLines = response.data.map(line => ({
      ...line,
      current_receive_quantity: 0,
      quality_status: 'qualified',
      notes: ''
    }))
  } catch (error) {
    console.error('获取采购单明细失败:', error)
    ElMessage.error('获取采购单明细失败')
  }
}

// 验证收货数量
const validateReceiveQuantity = (row) => {
  const maxQuantity = row.ordered_quantity - (row.received_quantity || 0)
  if (row.current_receive_quantity > maxQuantity) {
    row.current_receive_quantity = maxQuantity
    ElMessage.warning(`收货数量不能超过剩余数量 ${maxQuantity}`)
  }
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
    
    const hasReceiveQuantity = form.receiveLines.some(line => (line.current_receive_quantity || 0) > 0)
    if (!hasReceiveQuantity) {
      ElMessage.error('请至少输入一个商品的收货数量')
      return false
    }
    
    return true
  } catch (error) {
    return false
  }
}

// 保存收货
const saveReceive = async () => {
  if (!(await validateForm())) return
  
  try {
    saving.value = true
    
    const data = {
      purchase_order_id: props.purchaseOrder.id,
      receive_date: form.receiveDate,
      receiver_id: form.receiverId,
      warehouse_id: form.warehouseId,
      notes: form.notes,
      receive_lines: form.receiveLines
        .filter(line => (line.current_receive_quantity || 0) > 0)
        .map(line => ({
          purchase_order_line_id: line.id,
          product_id: line.product_id,
          receive_quantity: line.current_receive_quantity,
          quality_status: line.quality_status,
          notes: line.notes
        })),
      attachments: form.attachments.map(file => ({
        name: file.name,
        url: file.response?.url || file.url,
        size: file.size
      }))
    }
    
    await api.post('/procurement/receives', data)
    emit('success')
  } catch (error) {
    console.error('收货登记失败:', error)
    ElMessage.error('收货登记失败')
  } finally {
    saving.value = false
  }
}

// 组件挂载
onMounted(() => {
  fetchUsers()
  fetchWarehouses()
  fetchPurchaseOrderLines()
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
}

.info-item label {
  font-weight: 600;
  color: #606266;
  margin-right: 8px;
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

:deep(.el-upload-dragger) {
  width: 100%;
  height: 120px;
}
</style>