<template>
  <div class="roles">
    <div class="page-header">
      <h1>角色管理</h1>
      <p>管理系统角色和权限配置</p>
    </div>
    
    <div class="content-card">
      <div class="filters">
        <el-form :inline="true" :model="filters" class="filter-form">
          <el-form-item label="角色名称">
            <el-input v-model="filters.roleName" placeholder="请输入角色名称" clearable />
          </el-form-item>
          <el-form-item label="状态">
            <el-select v-model="filters.status" placeholder="请选择状态" clearable>
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

      <div class="table-actions">
        <el-button type="primary" @click="handleAdd">新增角色</el-button>
        <el-button type="success" @click="handleBatchPermission">批量授权</el-button>
      </div>

      <el-table :data="roleList" v-loading="loading" stripe>
        <el-table-column type="selection" width="55" />
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="roleName" label="角色名称" min-width="150" />
        <el-table-column prop="roleCode" label="角色代码" width="120" />
        <el-table-column prop="description" label="描述" min-width="200" />
        <el-table-column prop="userCount" label="用户数量" width="100">
          <template #default="{ row }">
            <el-link type="primary" @click="handleViewUsers(row)">
              {{ row.userCount }}
            </el-link>
          </template>
        </el-table-column>
        <el-table-column prop="permissions" label="权限数量" width="100">
          <template #default="{ row }">
            <el-tag type="info">{{ row.permissions.length }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="status" label="状态" width="100">
          <template #default="{ row }">
            <el-switch
              v-model="row.status"
              active-value="active"
              inactive-value="inactive"
              @change="handleStatusChange(row)"
              :disabled="row.roleCode === 'admin'"
            />
          </template>
        </el-table-column>
        <el-table-column prop="createdAt" label="创建时间" width="160" />
        <el-table-column prop="updatedAt" label="更新时间" width="160" />
        <el-table-column label="操作" width="220" fixed="right">
          <template #default="{ row }">
            <el-button type="primary" size="small" @click="handleView(row)">查看</el-button>
            <el-button type="warning" size="small" @click="handleEdit(row)" :disabled="row.roleCode === 'admin'">编辑</el-button>
            <el-button type="info" size="small" @click="handlePermission(row)">权限</el-button>
            <el-button type="danger" size="small" @click="handleDelete(row)" v-if="row.roleCode !== 'admin'">删除</el-button>
          </template>
        </el-table-column>
      </el-table>

      <div class="pagination">
        <el-pagination
          v-model:current-page="pagination.page"
          v-model:page-size="pagination.size"
          :page-sizes="[10, 20, 50, 100]"
          :total="pagination.total"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="handleSizeChange"
          @current-change="handlePageChange"
        />
      </div>
    </div>

    <!-- 权限配置对话框 -->
    <el-dialog v-model="permissionDialogVisible" title="权限配置" width="60%">
      <div class="permission-config">
        <div class="role-info">
          <h3>{{ currentRole?.roleName }}</h3>
          <p>{{ currentRole?.description }}</p>
        </div>
        
        <el-tree
          ref="permissionTree"
          :data="permissionTreeData"
          :props="treeProps"
          show-checkbox
          node-key="id"
          :default-checked-keys="checkedPermissions"
          class="permission-tree"
        />
      </div>
      
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="permissionDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="handleSavePermissions">保存</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'

// 响应式数据
const loading = ref(false)
const roleList = ref([])
const permissionDialogVisible = ref(false)
const currentRole = ref(null)
const checkedPermissions = ref([])
const permissionTree = ref(null)

const filters = reactive({
  roleName: '',
  status: ''
})

const pagination = reactive({
  page: 1,
  size: 20,
  total: 0
})

const treeProps = {
  children: 'children',
  label: 'name'
}

// 模拟数据
const mockRoles = [
  {
    id: 1,
    roleName: '超级管理员',
    roleCode: 'admin',
    description: '系统超级管理员，拥有所有权限',
    userCount: 1,
    permissions: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
    status: 'active',
    createdAt: '2024-01-01 00:00:00',
    updatedAt: '2024-01-01 00:00:00'
  },
  {
    id: 2,
    roleName: '销售经理',
    roleCode: 'sales_manager',
    description: '销售部门经理，管理销售订单和客户',
    userCount: 3,
    permissions: [1, 2, 3, 4],
    status: 'active',
    createdAt: '2024-01-02 10:00:00',
    updatedAt: '2024-01-15 14:30:00'
  },
  {
    id: 3,
    roleName: '采购专员',
    roleCode: 'procurement_staff',
    description: '采购部门专员，负责采购订单管理',
    userCount: 2,
    permissions: [5, 6, 7],
    status: 'active',
    createdAt: '2024-01-03 14:30:00',
    updatedAt: '2024-01-10 09:15:00'
  },
  {
    id: 4,
    roleName: '仓库管理员',
    roleCode: 'warehouse_manager',
    description: '仓库管理员，管理库存和出入库',
    userCount: 1,
    permissions: [8, 9, 10],
    status: 'active',
    createdAt: '2024-01-04 09:15:00',
    updatedAt: '2024-01-12 16:45:00'
  },
  {
    id: 5,
    roleName: '财务专员',
    roleCode: 'finance_staff',
    description: '财务部门专员，管理财务相关业务',
    userCount: 1,
    permissions: [11, 12],
    status: 'inactive',
    createdAt: '2024-01-05 15:45:00',
    updatedAt: '2024-01-08 11:20:00'
  }
]

const permissionTreeData = [
  {
    id: 1,
    name: '销售管理',
    children: [
      { id: 2, name: '销售订单查看' },
      { id: 3, name: '销售订单创建' },
      { id: 4, name: '销售订单编辑' }
    ]
  },
  {
    id: 5,
    name: '采购管理',
    children: [
      { id: 6, name: '采购订单查看' },
      { id: 7, name: '采购订单创建' }
    ]
  },
  {
    id: 8,
    name: '库存管理',
    children: [
      { id: 9, name: '库存查看' },
      { id: 10, name: '库存调整' }
    ]
  },
  {
    id: 11,
    name: '财务管理',
    children: [
      { id: 12, name: '财务报表查看' }
    ]
  }
]

// 方法
const fetchRoles = async () => {
  loading.value = true
  try {
    // 模拟API调用
    await new Promise(resolve => setTimeout(resolve, 500))
    roleList.value = mockRoles
    pagination.total = mockRoles.length
  } catch (error) {
    ElMessage.error('获取角色列表失败')
  } finally {
    loading.value = false
  }
}

const handleSearch = () => {
  pagination.page = 1
  fetchRoles()
}

const handleReset = () => {
  Object.assign(filters, {
    roleName: '',
    status: ''
  })
  handleSearch()
}

const handleAdd = () => {
  ElMessage.info('新增角色功能开发中')
}

const handleBatchPermission = () => {
  ElMessage.info('批量授权功能开发中')
}

const handleView = (row) => {
  ElMessage.info(`查看角色: ${row.roleName}`)
}

const handleEdit = (row) => {
  ElMessage.info(`编辑角色: ${row.roleName}`)
}

const handlePermission = (row) => {
  currentRole.value = row
  checkedPermissions.value = row.permissions
  permissionDialogVisible.value = true
}

const handleViewUsers = (row) => {
  ElMessage.info(`查看角色 ${row.roleName} 的用户列表`)
}

const handleDelete = async (row) => {
  try {
    await ElMessageBox.confirm(`确定要删除角色 ${row.roleName} 吗？`, '确认删除', {
      type: 'warning'
    })
    ElMessage.success('删除成功')
    fetchRoles()
  } catch {
    // 用户取消删除
  }
}

const handleStatusChange = async (row) => {
  try {
    const action = row.status === 'active' ? '启用' : '禁用'
    ElMessage.success(`角色 ${row.roleName} ${action}成功`)
  } catch (error) {
    ElMessage.error('状态更新失败')
    // 回滚状态
    row.status = row.status === 'active' ? 'inactive' : 'active'
  }
}

const handleSavePermissions = () => {
  const checkedKeys = permissionTree.value.getCheckedKeys()
  const halfCheckedKeys = permissionTree.value.getHalfCheckedKeys()
  const allCheckedKeys = [...checkedKeys, ...halfCheckedKeys]
  
  // 更新角色权限
  currentRole.value.permissions = allCheckedKeys
  
  ElMessage.success('权限配置保存成功')
  permissionDialogVisible.value = false
}

const handleSizeChange = (size) => {
  pagination.size = size
  fetchRoles()
}

const handlePageChange = (page) => {
  pagination.page = page
  fetchRoles()
}

// 生命周期
onMounted(() => {
  fetchRoles()
})
</script>

<style scoped>
.roles {
  padding: 20px;
}

.page-header {
  margin-bottom: 20px;
}

.page-header h1 {
  margin: 0 0 8px 0;
  font-size: 24px;
  font-weight: 600;
  color: #303133;
}

.page-header p {
  margin: 0;
  color: #606266;
  font-size: 14px;
}

.content-card {
  background: white;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.filters {
  margin-bottom: 20px;
  padding: 20px;
  background: #f8f9fa;
  border-radius: 6px;
}

.filter-form .el-form-item {
  margin-bottom: 0;
}

.table-actions {
  margin-bottom: 20px;
  display: flex;
  gap: 10px;
}

.pagination {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}

.permission-config {
  padding: 20px 0;
}

.role-info {
  margin-bottom: 20px;
  padding: 15px;
  background: #f8f9fa;
  border-radius: 6px;
}

.role-info h3 {
  margin: 0 0 8px 0;
  color: #303133;
}

.role-info p {
  margin: 0;
  color: #606266;
  font-size: 14px;
}

.permission-tree {
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  padding: 10px;
  max-height: 400px;
  overflow-y: auto;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}
</style>