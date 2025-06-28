<template>
  <div class="operations-container">
    <div class="page-header">
      <h1>生产作业</h1>
      <el-button type="primary" @click="showAddDialog = true">
        <el-icon><Plus /></el-icon>
        新增作业
      </el-button>
    </div>

    <!-- 搜索栏 -->
    <div class="search-bar">
      <el-form :inline="true" :model="searchForm">
        <el-form-item label="作业编号">
          <el-input v-model="searchForm.operationNo" placeholder="请输入作业编号" clearable />
        </el-form-item>
        <el-form-item label="工单编号">
          <el-input v-model="searchForm.workOrderNo" placeholder="请输入工单编号" clearable />
        </el-form-item>
        <el-form-item label="状态">
          <el-select v-model="searchForm.status" placeholder="请选择状态" clearable>
            <el-option label="待开始" value="pending" />
            <el-option label="进行中" value="in_progress" />
            <el-option label="已完成" value="completed" />
            <el-option label="已暂停" value="paused" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch">搜索</el-button>
          <el-button @click="handleReset">重置</el-button>
        </el-form-item>
      </el-form>
    </div>

    <!-- 作业列表 -->
    <div class="table-container">
      <el-table :data="operations" v-loading="loading" stripe>
        <el-table-column prop="operationNo" label="作业编号" width="120" />
        <el-table-column prop="workOrderNo" label="工单编号" width="120" />
        <el-table-column prop="productName" label="产品名称" min-width="150" />
        <el-table-column prop="processName" label="工序名称" width="120" />
        <el-table-column prop="operator" label="操作员" width="100" />
        <el-table-column prop="plannedQty" label="计划数量" width="100" />
        <el-table-column prop="completedQty" label="完成数量" width="100" />
        <el-table-column prop="status" label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="getStatusType(row.status)">
              {{ getStatusText(row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="startTime" label="开始时间" width="150" />
        <el-table-column prop="endTime" label="结束时间" width="150" />
        <el-table-column label="操作" width="200" fixed="right">
          <template #default="{ row }">
            <el-button 
              v-if="row.status === 'pending'" 
              type="success" 
              size="small" 
              @click="handleStart(row)"
            >
              开始
            </el-button>
            <el-button 
              v-if="row.status === 'in_progress'" 
              type="warning" 
              size="small" 
              @click="handlePause(row)"
            >
              暂停
            </el-button>
            <el-button 
              v-if="row.status === 'paused'" 
              type="success" 
              size="small" 
              @click="handleResume(row)"
            >
              继续
            </el-button>
            <el-button 
              v-if="row.status === 'in_progress'" 
              type="primary" 
              size="small" 
              @click="handleComplete(row)"
            >
              完成
            </el-button>
            <el-button type="primary" size="small" @click="handleEdit(row)">编辑</el-button>
          </template>
        </el-table-column>
      </el-table>

      <!-- 分页 -->
      <div class="pagination-container">
        <el-pagination
          v-model:current-page="pagination.currentPage"
          v-model:page-size="pagination.pageSize"
          :page-sizes="[10, 20, 50, 100]"
          :total="pagination.total"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        />
      </div>
    </div>

    <!-- 新增/编辑对话框 -->
    <el-dialog
      v-model="showAddDialog"
      :title="editingOperation ? '编辑作业' : '新增作业'"
      width="600px"
      @close="handleDialogClose"
    >
      <el-form
        ref="operationFormRef"
        :model="operationForm"
        :rules="operationRules"
        label-width="100px"
      >
        <el-form-item label="作业编号" prop="operationNo">
          <el-input v-model="operationForm.operationNo" placeholder="请输入作业编号" />
        </el-form-item>
        <el-form-item label="工单编号" prop="workOrderNo">
          <el-select v-model="operationForm.workOrderNo" placeholder="请选择工单" filterable>
            <el-option
              v-for="order in workOrders"
              :key="order.workOrderNo"
              :label="order.workOrderNo"
              :value="order.workOrderNo"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="产品名称" prop="productName">
          <el-input v-model="operationForm.productName" placeholder="请输入产品名称" />
        </el-form-item>
        <el-form-item label="工序名称" prop="processName">
          <el-input v-model="operationForm.processName" placeholder="请输入工序名称" />
        </el-form-item>
        <el-form-item label="操作员" prop="operator">
          <el-input v-model="operationForm.operator" placeholder="请输入操作员" />
        </el-form-item>
        <el-form-item label="计划数量" prop="plannedQty">
          <el-input-number v-model="operationForm.plannedQty" :min="1" placeholder="请输入计划数量" />
        </el-form-item>
        <el-form-item label="完成数量" prop="completedQty">
          <el-input-number v-model="operationForm.completedQty" :min="0" placeholder="请输入完成数量" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showAddDialog = false">取消</el-button>
        <el-button type="primary" @click="handleSave" :loading="saving">保存</el-button>
      </template>
    </el-dialog>

    <!-- 完成作业对话框 -->
    <el-dialog
      v-model="showCompleteDialog"
      title="完成作业"
      width="400px"
    >
      <el-form :model="completeForm" label-width="100px">
        <el-form-item label="完成数量">
          <el-input-number 
            v-model="completeForm.completedQty" 
            :min="0" 
            :max="completeForm.plannedQty"
            placeholder="请输入完成数量" 
          />
        </el-form-item>
        <el-form-item label="备注">
          <el-input 
            v-model="completeForm.remark" 
            type="textarea" 
            placeholder="请输入备注" 
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showCompleteDialog = false">取消</el-button>
        <el-button type="primary" @click="confirmComplete">确认完成</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus } from '@element-plus/icons-vue'

// 响应式数据
const loading = ref(false)
const saving = ref(false)
const showAddDialog = ref(false)
const showCompleteDialog = ref(false)
const editingOperation = ref(null)
const operationFormRef = ref(null)
const currentOperation = ref(null)

// 搜索表单
const searchForm = reactive({
  operationNo: '',
  workOrderNo: '',
  status: ''
})

// 作业表单
const operationForm = reactive({
  operationNo: '',
  workOrderNo: '',
  productName: '',
  processName: '',
  operator: '',
  plannedQty: 1,
  completedQty: 0
})

// 完成表单
const completeForm = reactive({
  completedQty: 0,
  plannedQty: 0,
  remark: ''
})

// 表单验证规则
const operationRules = {
  operationNo: [{ required: true, message: '请输入作业编号', trigger: 'blur' }],
  workOrderNo: [{ required: true, message: '请选择工单', trigger: 'change' }],
  productName: [{ required: true, message: '请输入产品名称', trigger: 'blur' }],
  processName: [{ required: true, message: '请输入工序名称', trigger: 'blur' }],
  operator: [{ required: true, message: '请输入操作员', trigger: 'blur' }],
  plannedQty: [{ required: true, message: '请输入计划数量', trigger: 'blur' }]
}

// 分页
const pagination = reactive({
  currentPage: 1,
  pageSize: 10,
  total: 0
})

// 作业列表
const operations = ref([])

// 工单列表
const workOrders = ref([
  { workOrderNo: 'WO001', productName: '产品A' },
  { workOrderNo: 'WO002', productName: '产品B' },
  { workOrderNo: 'WO003', productName: '产品C' }
])

// 模拟数据
const mockOperations = [
  {
    id: 1,
    operationNo: 'OP001',
    workOrderNo: 'WO001',
    productName: '智能手机',
    processName: '组装',
    operator: '张三',
    plannedQty: 100,
    completedQty: 80,
    status: 'in_progress',
    startTime: '2024-01-15 08:00:00',
    endTime: ''
  },
  {
    id: 2,
    operationNo: 'OP002',
    workOrderNo: 'WO002',
    productName: '平板电脑',
    processName: '测试',
    operator: '李四',
    plannedQty: 50,
    completedQty: 50,
    status: 'completed',
    startTime: '2024-01-15 09:00:00',
    endTime: '2024-01-15 17:00:00'
  },
  {
    id: 3,
    operationNo: 'OP003',
    workOrderNo: 'WO003',
    productName: '笔记本电脑',
    processName: '包装',
    operator: '王五',
    plannedQty: 30,
    completedQty: 0,
    status: 'pending',
    startTime: '',
    endTime: ''
  }
]

// 方法
const getStatusType = (status) => {
  const statusMap = {
    pending: 'info',
    in_progress: 'warning',
    completed: 'success',
    paused: 'danger'
  }
  return statusMap[status] || 'info'
}

const getStatusText = (status) => {
  const statusMap = {
    pending: '待开始',
    in_progress: '进行中',
    completed: '已完成',
    paused: '已暂停'
  }
  return statusMap[status] || '未知'
}

const loadOperations = async () => {
  loading.value = true
  try {
    // 模拟API调用
    await new Promise(resolve => setTimeout(resolve, 500))
    operations.value = mockOperations
    pagination.total = mockOperations.length
  } catch (error) {
    ElMessage.error('加载作业列表失败')
  } finally {
    loading.value = false
  }
}

const handleSearch = () => {
  loadOperations()
}

const handleReset = () => {
  Object.assign(searchForm, {
    operationNo: '',
    workOrderNo: '',
    status: ''
  })
  loadOperations()
}

const handleStart = async (row) => {
  try {
    await ElMessageBox.confirm('确定要开始该作业吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    
    // 模拟API调用
    row.status = 'in_progress'
    row.startTime = new Date().toLocaleString()
    ElMessage.success('作业已开始')
  } catch (error) {
    // 用户取消操作
  }
}

const handlePause = async (row) => {
  try {
    await ElMessageBox.confirm('确定要暂停该作业吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    
    // 模拟API调用
    row.status = 'paused'
    ElMessage.success('作业已暂停')
  } catch (error) {
    // 用户取消操作
  }
}

const handleResume = async (row) => {
  try {
    await ElMessageBox.confirm('确定要继续该作业吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    
    // 模拟API调用
    row.status = 'in_progress'
    ElMessage.success('作业已继续')
  } catch (error) {
    // 用户取消操作
  }
}

const handleComplete = (row) => {
  currentOperation.value = row
  completeForm.completedQty = row.completedQty
  completeForm.plannedQty = row.plannedQty
  completeForm.remark = ''
  showCompleteDialog.value = true
}

const confirmComplete = async () => {
  try {
    // 模拟API调用
    currentOperation.value.status = 'completed'
    currentOperation.value.completedQty = completeForm.completedQty
    currentOperation.value.endTime = new Date().toLocaleString()
    
    showCompleteDialog.value = false
    ElMessage.success('作业已完成')
  } catch (error) {
    ElMessage.error('完成作业失败')
  }
}

const handleEdit = (row) => {
  editingOperation.value = row
  Object.assign(operationForm, row)
  showAddDialog.value = true
}

const handleSave = async () => {
  if (!operationFormRef.value) return
  
  try {
    await operationFormRef.value.validate()
    saving.value = true
    
    // 模拟API调用
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    if (editingOperation.value) {
      // 编辑
      const index = operations.value.findIndex(item => item.id === editingOperation.value.id)
      if (index > -1) {
        operations.value[index] = { ...operationForm, id: editingOperation.value.id, status: editingOperation.value.status }
      }
      ElMessage.success('编辑成功')
    } else {
      // 新增
      const newOperation = {
        ...operationForm,
        id: Date.now(),
        status: 'pending',
        startTime: '',
        endTime: ''
      }
      operations.value.unshift(newOperation)
      pagination.total++
      ElMessage.success('新增成功')
    }
    
    showAddDialog.value = false
  } catch (error) {
    console.error('保存失败:', error)
  } finally {
    saving.value = false
  }
}

const handleDialogClose = () => {
  editingOperation.value = null
  Object.assign(operationForm, {
    operationNo: '',
    workOrderNo: '',
    productName: '',
    processName: '',
    operator: '',
    plannedQty: 1,
    completedQty: 0
  })
  if (operationFormRef.value) {
    operationFormRef.value.clearValidate()
  }
}

const handleSizeChange = (size) => {
  pagination.pageSize = size
  loadOperations()
}

const handleCurrentChange = (page) => {
  pagination.currentPage = page
  loadOperations()
}

// 生命周期
onMounted(() => {
  loadOperations()
})
</script>

<style scoped>
.operations-container {
  padding: 20px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.page-header h1 {
  margin: 0;
  color: #303133;
}

.search-bar {
  background: #f5f7fa;
  padding: 20px;
  border-radius: 4px;
  margin-bottom: 20px;
}

.table-container {
  background: white;
  border-radius: 4px;
  overflow: hidden;
}

.pagination-container {
  display: flex;
  justify-content: center;
  padding: 20px;
}
</style>