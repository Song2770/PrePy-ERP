<template>
  <div class="suppliers-container">
    <div class="page-header">
      <h1>供应商管理</h1>
      <el-button type="primary" @click="showAddDialog = true">
        <el-icon><Plus /></el-icon>
        新增供应商
      </el-button>
    </div>

    <!-- 搜索栏 -->
    <div class="search-bar">
      <el-form :inline="true" :model="searchForm">
        <el-form-item label="供应商名称">
          <el-input v-model="searchForm.name" placeholder="请输入供应商名称" clearable />
        </el-form-item>
        <el-form-item label="联系人">
          <el-input v-model="searchForm.contact" placeholder="请输入联系人" clearable />
        </el-form-item>
        <el-form-item label="状态">
          <el-select v-model="searchForm.status" placeholder="请选择状态" clearable>
            <el-option label="启用" value="active" />
            <el-option label="禁用" value="inactive" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch">搜索</el-button>
          <el-button @click="handleReset">重置</el-button>
        </el-form-item>
      </el-form>
    </div>

    <!-- 供应商列表 -->
    <div class="table-container">
      <el-table :data="suppliers" v-loading="loading" stripe>
        <el-table-column prop="code" label="供应商编码" width="120" />
        <el-table-column prop="name" label="供应商名称" min-width="150" />
        <el-table-column prop="contact" label="联系人" width="100" />
        <el-table-column prop="phone" label="联系电话" width="130" />
        <el-table-column prop="email" label="邮箱" min-width="150" />
        <el-table-column prop="address" label="地址" min-width="200" />
        <el-table-column prop="status" label="状态" width="80">
          <template #default="{ row }">
            <el-tag :type="row.status === 'active' ? 'success' : 'danger'">
              {{ row.status === 'active' ? '启用' : '禁用' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="createTime" label="创建时间" width="150" />
        <el-table-column label="操作" width="180" fixed="right">
          <template #default="{ row }">
            <el-button type="primary" size="small" @click="handleEdit(row)">编辑</el-button>
            <el-button type="warning" size="small" @click="handleToggleStatus(row)">
              {{ row.status === 'active' ? '禁用' : '启用' }}
            </el-button>
            <el-button type="danger" size="small" @click="handleDelete(row)">删除</el-button>
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
      :title="editingSupplier ? '编辑供应商' : '新增供应商'"
      width="600px"
      @close="handleDialogClose"
    >
      <el-form
        ref="supplierFormRef"
        :model="supplierForm"
        :rules="supplierRules"
        label-width="100px"
      >
        <el-form-item label="供应商编码" prop="code">
          <el-input v-model="supplierForm.code" placeholder="请输入供应商编码" />
        </el-form-item>
        <el-form-item label="供应商名称" prop="name">
          <el-input v-model="supplierForm.name" placeholder="请输入供应商名称" />
        </el-form-item>
        <el-form-item label="联系人" prop="contact">
          <el-input v-model="supplierForm.contact" placeholder="请输入联系人" />
        </el-form-item>
        <el-form-item label="联系电话" prop="phone">
          <el-input v-model="supplierForm.phone" placeholder="请输入联系电话" />
        </el-form-item>
        <el-form-item label="邮箱" prop="email">
          <el-input v-model="supplierForm.email" placeholder="请输入邮箱" />
        </el-form-item>
        <el-form-item label="地址" prop="address">
          <el-input v-model="supplierForm.address" type="textarea" placeholder="请输入地址" />
        </el-form-item>
        <el-form-item label="状态" prop="status">
          <el-radio-group v-model="supplierForm.status">
            <el-radio label="active">启用</el-radio>
            <el-radio label="inactive">禁用</el-radio>
          </el-radio-group>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showAddDialog = false">取消</el-button>
        <el-button type="primary" @click="handleSave" :loading="saving">保存</el-button>
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
const editingSupplier = ref(null)
const supplierFormRef = ref(null)

// 搜索表单
const searchForm = reactive({
  name: '',
  contact: '',
  status: ''
})

// 供应商表单
const supplierForm = reactive({
  code: '',
  name: '',
  contact: '',
  phone: '',
  email: '',
  address: '',
  status: 'active'
})

// 表单验证规则
const supplierRules = {
  code: [{ required: true, message: '请输入供应商编码', trigger: 'blur' }],
  name: [{ required: true, message: '请输入供应商名称', trigger: 'blur' }],
  contact: [{ required: true, message: '请输入联系人', trigger: 'blur' }],
  phone: [{ required: true, message: '请输入联系电话', trigger: 'blur' }],
  email: [
    { required: true, message: '请输入邮箱', trigger: 'blur' },
    { type: 'email', message: '请输入正确的邮箱格式', trigger: 'blur' }
  ]
}

// 分页
const pagination = reactive({
  currentPage: 1,
  pageSize: 10,
  total: 0
})

// 供应商列表
const suppliers = ref([])

// 模拟数据
const mockSuppliers = [
  {
    id: 1,
    code: 'SUP001',
    name: '北京科技有限公司',
    contact: '张三',
    phone: '13800138001',
    email: 'zhangsan@example.com',
    address: '北京市朝阳区科技园区',
    status: 'active',
    createTime: '2024-01-15 10:30:00'
  },
  {
    id: 2,
    code: 'SUP002',
    name: '上海制造集团',
    contact: '李四',
    phone: '13800138002',
    email: 'lisi@example.com',
    address: '上海市浦东新区工业园',
    status: 'active',
    createTime: '2024-01-16 14:20:00'
  },
  {
    id: 3,
    code: 'SUP003',
    name: '广州贸易公司',
    contact: '王五',
    phone: '13800138003',
    email: 'wangwu@example.com',
    address: '广州市天河区商务中心',
    status: 'inactive',
    createTime: '2024-01-17 09:15:00'
  }
]

// 方法
const loadSuppliers = async () => {
  loading.value = true
  try {
    // 模拟API调用
    await new Promise(resolve => setTimeout(resolve, 500))
    suppliers.value = mockSuppliers
    pagination.total = mockSuppliers.length
  } catch (error) {
    ElMessage.error('加载供应商列表失败')
  } finally {
    loading.value = false
  }
}

const handleSearch = () => {
  loadSuppliers()
}

const handleReset = () => {
  Object.assign(searchForm, {
    name: '',
    contact: '',
    status: ''
  })
  loadSuppliers()
}

const handleEdit = (row) => {
  editingSupplier.value = row
  Object.assign(supplierForm, row)
  showAddDialog.value = true
}

const handleToggleStatus = async (row) => {
  try {
    const action = row.status === 'active' ? '禁用' : '启用'
    await ElMessageBox.confirm(`确定要${action}该供应商吗？`, '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    
    // 模拟API调用
    row.status = row.status === 'active' ? 'inactive' : 'active'
    ElMessage.success(`${action}成功`)
  } catch (error) {
    // 用户取消操作
  }
}

const handleDelete = async (row) => {
  try {
    await ElMessageBox.confirm('确定要删除该供应商吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    
    // 模拟API调用
    const index = suppliers.value.findIndex(item => item.id === row.id)
    if (index > -1) {
      suppliers.value.splice(index, 1)
      pagination.total--
    }
    ElMessage.success('删除成功')
  } catch (error) {
    // 用户取消操作
  }
}

const handleSave = async () => {
  if (!supplierFormRef.value) return
  
  try {
    await supplierFormRef.value.validate()
    saving.value = true
    
    // 模拟API调用
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    if (editingSupplier.value) {
      // 编辑
      const index = suppliers.value.findIndex(item => item.id === editingSupplier.value.id)
      if (index > -1) {
        suppliers.value[index] = { ...supplierForm, id: editingSupplier.value.id }
      }
      ElMessage.success('编辑成功')
    } else {
      // 新增
      const newSupplier = {
        ...supplierForm,
        id: Date.now(),
        createTime: new Date().toLocaleString()
      }
      suppliers.value.unshift(newSupplier)
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
  editingSupplier.value = null
  Object.assign(supplierForm, {
    code: '',
    name: '',
    contact: '',
    phone: '',
    email: '',
    address: '',
    status: 'active'
  })
  if (supplierFormRef.value) {
    supplierFormRef.value.clearValidate()
  }
}

const handleSizeChange = (size) => {
  pagination.pageSize = size
  loadSuppliers()
}

const handleCurrentChange = (page) => {
  pagination.currentPage = page
  loadSuppliers()
}

// 生命周期
onMounted(() => {
  loadSuppliers()
})
</script>

<style scoped>
.suppliers-container {
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