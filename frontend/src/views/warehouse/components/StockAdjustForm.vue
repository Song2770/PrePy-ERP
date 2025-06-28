<template>
  <div class="stock-adjust-form">
    <el-form
      ref="formRef"
      :model="form"
      :rules="rules"
      label-width="120px"
      @submit.prevent
    >
      <!-- 商品信息 -->
      <div class="form-section">
        <h3 class="section-title">商品信息</h3>
        <el-row :gutter="20">
          <el-col :span="12">
            <div class="info-item">
              <label>商品名称：</label>
              <span>{{ product?.product_name || '-' }}</span>
            </div>
          </el-col>
          <el-col :span="12">
            <div class="info-item">
              <label>商品编码：</label>
              <span>{{ product?.product_code || '-' }}</span>
            </div>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="12">
            <div class="info-item">
              <label>规格：</label>
              <span>{{ product?.product_spec || '-' }}</span>
            </div>
          </el-col>
          <el-col :span="12">
            <div class="info-item">
              <label>单位：</label>
              <span>{{ product?.product_unit || '-' }}</span>
            </div>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="12">
            <div class="info-item">
              <label>仓库：</label>
              <span>{{ product?.warehouse_name || '-' }}</span>
            </div>
          </el-col>
          <el-col :span="12">
            <div class="info-item">
              <label>当前库存：</label>
              <span class="current-stock">{{ product?.current_stock || 0 }}</span>
            </div>
          </el-col>
        </el-row>
      </div>

      <!-- 调整信息 -->
      <div class="form-section">
        <h3 class="section-title">调整信息</h3>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="调整类型" prop="adjustmentType" required>
              <el-radio-group v-model="form.adjustmentType" @change="handleTypeChange">
                <el-radio label="in">入库调整</el-radio>
                <el-radio label="out">出库调整</el-radio>
              </el-radio-group>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="调整原因" prop="reasonId" required>
              <el-select
                v-model="form.reasonId"
                placeholder="请选择调整原因"
                style="width: 100%"
              >
                <el-option
                  v-for="reason in adjustmentReasons"
                  :key="reason.id"
                  :label="reason.name"
                  :value="reason.id"
                />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="调整数量" prop="quantity" required>
              <el-input-number
                v-model="form.quantity"
                :min="0.01"
                :precision="2"
                :step="1"
                style="width: 100%"
                @change="calculateAfterStock"
              />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="调整后库存">
              <el-input
                :value="afterStock"
                readonly
                style="width: 100%"
              >
                <template #suffix>
                  <span :class="getAfterStockClass()">{{ afterStock }}</span>
                </template>
              </el-input>
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="单位成本" prop="unitCost">
              <el-input-number
                v-model="form.unitCost"
                :min="0"
                :precision="2"
                :step="0.01"
                style="width: 100%"
              />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="调整日期" prop="adjustmentDate" required>
              <el-date-picker
                v-model="form.adjustmentDate"
                type="date"
                placeholder="选择调整日期"
                format="YYYY-MM-DD"
                value-format="YYYY-MM-DD"
                style="width: 100%"
              />
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-row :gutter="20">
          <el-col :span="24">
            <el-form-item label="调整说明" prop="notes">
              <el-input
                v-model="form.notes"
                type="textarea"
                :rows="3"
                placeholder="请输入调整说明"
                maxlength="500"
                show-word-limit
              />
            </el-form-item>
          </el-col>
        </el-row>
      </div>

      <!-- 批次信息（如果商品需要批次管理） -->
      <div v-if="needBatchManagement" class="form-section">
        <h3 class="section-title">批次信息</h3>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="批次号" prop="batchNumber">
              <el-input
                v-model="form.batchNumber"
                placeholder="请输入批次号"
                maxlength="50"
              />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="生产日期" prop="productionDate">
              <el-date-picker
                v-model="form.productionDate"
                type="date"
                placeholder="选择生产日期"
                format="YYYY-MM-DD"
                value-format="YYYY-MM-DD"
                style="width: 100%"
              />
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="有效期至" prop="expiryDate">
              <el-date-picker
                v-model="form.expiryDate"
                type="date"
                placeholder="选择有效期"
                format="YYYY-MM-DD"
                value-format="YYYY-MM-DD"
                style="width: 100%"
              />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="供应商批次" prop="supplierBatch">
              <el-input
                v-model="form.supplierBatch"
                placeholder="请输入供应商批次"
                maxlength="50"
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
      <el-button type="primary" @click="saveAdjustment" :loading="saving">
        确认调整
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
  product: {
    type: Object,
    default: () => ({})
  }
})

const emit = defineEmits(['success', 'cancel'])

// 响应式数据
const formRef = ref()
const saving = ref(false)
const adjustmentReasons = ref([])
const needBatchManagement = ref(false)
const userStore = useUserStore()

// 表单数据
const form = reactive({
  adjustmentType: 'in',
  reasonId: null,
  quantity: 1,
  unitCost: props.product?.unit_cost || 0,
  adjustmentDate: new Date().toISOString().split('T')[0],
  notes: '',
  batchNumber: '',
  productionDate: '',
  expiryDate: '',
  supplierBatch: '',
  attachments: []
})

// 表单验证规则
const rules = {
  adjustmentType: [
    { required: true, message: '请选择调整类型', trigger: 'change' }
  ],
  reasonId: [
    { required: true, message: '请选择调整原因', trigger: 'change' }
  ],
  quantity: [
    { required: true, message: '请输入调整数量', trigger: 'blur' },
    { type: 'number', min: 0.01, message: '调整数量必须大于0', trigger: 'blur' }
  ],
  adjustmentDate: [
    { required: true, message: '请选择调整日期', trigger: 'change' }
  ]
}

// 上传配置
const uploadUrl = computed(() => `${api.defaults.baseURL}/upload`)
const uploadHeaders = computed(() => ({
  Authorization: `Bearer ${userStore.token}`
}))

// 计算调整后库存
const afterStock = computed(() => {
  const currentStock = props.product?.current_stock || 0
  const quantity = form.quantity || 0
  
  if (form.adjustmentType === 'in') {
    return currentStock + quantity
  } else {
    return Math.max(0, currentStock - quantity)
  }
})

// 获取调整后库存样式
const getAfterStockClass = () => {
  const current = props.product?.current_stock || 0
  const after = afterStock.value
  const safety = props.product?.safety_stock || 0
  
  if (after <= 0) return 'stock-danger'
  if (after <= safety) return 'stock-warning'
  if (after > current) return 'stock-success'
  return 'stock-normal'
}

// 获取调整原因列表
const fetchAdjustmentReasons = async () => {
  try {
    const response = await api.get('/warehouse/adjustment-reasons')
    adjustmentReasons.value = response.data.items || []
  } catch (error) {
    console.error('获取调整原因失败:', error)
    // 使用默认原因
    adjustmentReasons.value = [
      { id: 1, name: '盘点调整' },
      { id: 2, name: '损耗调整' },
      { id: 3, name: '报废调整' },
      { id: 4, name: '退货调整' },
      { id: 5, name: '其他调整' }
    ]
  }
}

// 检查是否需要批次管理
const checkBatchManagement = async () => {
  try {
    if (props.product?.product_id) {
      const response = await api.get(`/products/${props.product.product_id}`)
      needBatchManagement.value = response.data.batch_management || false
    }
  } catch (error) {
    console.error('检查批次管理失败:', error)
  }
}

// 调整类型变化
const handleTypeChange = () => {
  calculateAfterStock()
}

// 计算调整后库存
const calculateAfterStock = () => {
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
    
    // 检查调整后库存
    if (form.adjustmentType === 'out' && afterStock.value < 0) {
      ElMessage.error('出库数量不能超过当前库存')
      return false
    }
    
    // 检查批次信息
    if (needBatchManagement.value && form.adjustmentType === 'in') {
      if (!form.batchNumber) {
        ElMessage.error('该商品需要批次管理，请输入批次号')
        return false
      }
    }
    
    return true
  } catch (error) {
    return false
  }
}

// 保存调整
const saveAdjustment = async () => {
  if (!(await validateForm())) return
  
  try {
    saving.value = true
    
    const data = {
      product_id: props.product.product_id,
      warehouse_id: props.product.warehouse_id,
      adjustment_type: form.adjustmentType,
      reason_id: form.reasonId,
      quantity: form.quantity,
      unit_cost: form.unitCost,
      adjustment_date: form.adjustmentDate,
      notes: form.notes,
      batch_number: form.batchNumber,
      production_date: form.productionDate,
      expiry_date: form.expiryDate,
      supplier_batch: form.supplierBatch,
      attachments: form.attachments.map(file => ({
        name: file.name,
        url: file.response?.url || file.url,
        size: file.size
      }))
    }
    
    await api.post('/warehouse/stock-movements', data)
    emit('success')
  } catch (error) {
    console.error('库存调整失败:', error)
    ElMessage.error('库存调整失败')
  } finally {
    saving.value = false
  }
}

// 组件挂载
onMounted(() => {
  fetchAdjustmentReasons()
  checkBatchManagement()
})
</script>

<style scoped>
.stock-adjust-form {
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

.current-stock {
  font-weight: 600;
  color: #5c6bc0;
  font-size: 16px;
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

/* 库存状态样式 */
.stock-normal {
  color: #67c23a;
}

.stock-warning {
  color: #e6a23c;
}

.stock-danger {
  color: #f56c6c;
}

.stock-success {
  color: #67c23a;
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

:deep(.el-radio-group) {
  display: flex;
  gap: 20px;
}
</style>