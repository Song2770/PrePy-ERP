<template>
  <div class="users">
    <div class="page-header">
      <h1>用户管理</h1>
      <p>管理系统用户账户和权限</p>
    </div>
    
    <div class="content-card">
      <div class="filters">
        <el-form :inline="true" :model="filters" class="filter-form">
          <el-form-item label="用户名">
            <el-input v-model="filters.username" placeholder="请输入用户名" clearable />
          </el-form-item>
          <el-form-item label="邮箱">
            <el-input v-model="filters.email" placeholder="请输入邮箱" clearable />
          </el-form-item>
          <el-form-item label="角色">
            <el-select v-model="filters.role" placeholder="请选择角色" clearable>
              <el-option label="管理员" value="admin" />
              <el-option label="销售" value="sales" />
              <el-option label="采购" value="procurement" />
              <el-option label="仓库" value="warehouse" />
              <el-option label="财务" value="finance" />
            </el-select>
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
        <el-button type="primary" @click="handleAdd">新增用户</el-button>
        <el-button type="success" @click="handleImport">批量导入</el-button>
        <el-button type="warning" @click="handleExport">导出用户</el-button>
      </div>

      <el-table :data="userList" v-loading="loading" stripe>
        <el-table-column type="selection" width="55" />
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="avatar" label="头像" width="80">
          <template #default="{ row }">
            <el-avatar :src="row.avatar" :size="40">
              <el-icon><User /></el-icon>
            </el-avatar>
          </template>
        </el-table-column>
        <el-table-column prop="username" label="用户名" min-width="120" />
        <el-table-column prop="realName" label="真实姓名" min-width="120" />
        <el-table-column prop="email" label="邮箱" min-width="180" />
        <el-table-column prop="phone" label="手机号" width="130" />
        <el-table-column prop="role" label="角色" width="100">
          <template #default="{ row }">
            <el-tag :type="getRoleTag(row.role)">
              {{ getRoleText(row.role) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="department" label="部门" width="120" />
        <el-table-column prop="status" label="状态" width="100">
          <template #default="{ row }">
            <el-switch
              v-model="row.status"
              active-value="active"
              inactive-value="inactive"
              @change="handleStatusChange(row)"
            />
          </template>
        </el-table-column>
        <el-table-column prop="lastLogin" label="最后登录" width="160" />
        <el-table-column prop="createdAt" label="创建时间" width="160" />
        <el-table-column label="操作" width="200" fixed="right">
          <template #default="{ row }">
            <el-button type="primary" size="small" @click="handleView(row)">查看</el-button>
            <el-button type="warning" size="small" @click="handleEdit(row)">编辑</el-button>
            <el-button type="info" size="small" @click="handleResetPassword(row)">重置密码</el-button>
            <el-button type="danger" size="small" @click="handleDelete(row)" v-if="row.username !== 'admin'">删除</el-button>
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

    <!-- 用户统计卡片 -->
    <div class="stats-cards">
      <el-row :gutter="20">
        <el-col :span="6">
          <div class="stat-card">
            <div class="stat-icon total">
              <el-icon><User /></el-icon>
            </div>
            <div class="stat-content">
              <div class="stat-value">{{ stats.totalUsers }}</div>
              <div class="stat-label">总用户数</div>
            </div>
          </div>
        </el-col>
        <el-col :span="6">
          <div class="stat-card">
            <div class="stat-icon active">
              <el-icon><Check /></el-icon>
            </div>
            <div class="stat-content">
              <div class="stat-value">{{ stats.activeUsers }}</div>
              <div class="stat-label">活跃用户</div>
            </div>
          </div>
        </el-col>
        <el-col :span="6">
          <div class="stat-card">
            <div class="stat-icon online">
              <el-icon><Connection /></el-icon>
            </div>
            <div class="stat-content">
              <div class="stat-value">{{ stats.onlineUsers }}</div>
              <div class="stat-label">在线用户</div>
            </div>
          </div>
        </el-col>
        <el-col :span="6">
          <div class="stat-card">
            <div class="stat-icon new">
              <el-icon><Plus /></el-icon>
            </div>
            <div class="stat-content">
              <div class="stat-value">{{ stats.newUsers }}</div>
              <div class="stat-label">本月新增</div>
            </div>
          </div>
        </el-col>
      </el-row>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { User, Check, Connection, Plus } from '@element-plus/icons-vue'

// 响应式数据
const loading = ref(false)
const userList = ref([])

const filters = reactive({
  username: '',
  email: '',
  role: '',
  status: ''
})

const pagination = reactive({
  page: 1,
  size: 20,
  total: 0
})

// 模拟数据
const mockData = [
  {
    id: 1,
    username: 'admin',
    realName: '系统管理员',
    email: 'admin@example.com',
    phone: '13800138000',
    role: 'admin',
    department: 'IT部',
    status: 'active',
    avatar: '',
    lastLogin: '2024-01-15 10:30:00',
    createdAt: '2024-01-01 00:00:00'
  },
  {
    id: 2,
    username: 'sales001',
    realName: '张三',
    email: 'zhangsan@example.com',
    phone: '13800138001',
    role: 'sales',
    department: '销售部',
    status: 'active',
    avatar: '',
    lastLogin: '2024-01-15 09:15:00',
    createdAt: '2024-01-02 10:00:00'
  },
  {
    id: 3,
    username: 'procurement001',
    realName: '李四',
    email: 'lisi@example.com',
    phone: '13800138002',
    role: 'procurement',
    department: '采购部',
    status: 'active',
    avatar: '',
    lastLogin: '2024-01-14 16:45:00',
    createdAt: '2024-01-03 14:30:00'
  },
  {
    id: 4,
    username: 'warehouse001',
    realName: '王五',
    email: 'wangwu@example.com',
    phone: '13800138003',
    role: 'warehouse',
    department: '仓储部',
    status: 'inactive',
    avatar: '',
    lastLogin: '2024-01-10 11:20:00',
    createdAt: '2024-01-04 09:15:00'
  },
  {
    id: 5,
    username: 'finance001',
    realName: '赵六',
    email: 'zhaoliu@example.com',
    phone: '13800138004',
    role: 'finance',
    department: '财务部',
    status: 'active',
    avatar: '',
    lastLogin: '2024-01-15 08:30:00',
    createdAt: '2024-01-05 15:45:00'
  }
]

// 计算属性
const stats = computed(() => {
  const total = userList.value.length
  const active = userList.value.filter(user => user.status === 'active').length
  const online = Math.floor(active * 0.6) // 模拟在线用户数
  const newUsers = userList.value.filter(user => {
    const createDate = new Date(user.createdAt)
    const now = new Date()
    return createDate.getMonth() === now.getMonth() && createDate.getFullYear() === now.getFullYear()
  }).length
  
  return {
    totalUsers: total,
    activeUsers: active,
    onlineUsers: online,
    newUsers: newUsers
  }
})

// 方法
const fetchUsers = async () => {
  loading.value = true
  try {
    // 模拟API调用
    await new Promise(resolve => setTimeout(resolve, 500))
    userList.value = mockData
    pagination.total = mockData.length
  } catch (error) {
    ElMessage.error('获取用户列表失败')
  } finally {
    loading.value = false
  }
}

const handleSearch = () => {
  pagination.page = 1
  fetchUsers()
}

const handleReset = () => {
  Object.assign(filters, {
    username: '',
    email: '',
    role: '',
    status: ''
  })
  handleSearch()
}

const handleAdd = () => {
  ElMessage.info('新增用户功能开发中')
}

const handleImport = () => {
  ElMessage.info('批量导入功能开发中')
}

const handleExport = () => {
  ElMessage.info('导出功能开发中')
}

const handleView = (row) => {
  ElMessage.info(`查看用户: ${row.username}`)
}

const handleEdit = (row) => {
  ElMessage.info(`编辑用户: ${row.username}`)
}

const handleResetPassword = async (row) => {
  try {
    await ElMessageBox.confirm(`确定要重置用户 ${row.username} 的密码吗？`, '确认重置', {
      type: 'warning'
    })
    ElMessage.success('密码重置成功，新密码已发送到用户邮箱')
  } catch {
    // 用户取消操作
  }
}

const handleDelete = async (row) => {
  try {
    await ElMessageBox.confirm(`确定要删除用户 ${row.username} 吗？`, '确认删除', {
      type: 'warning'
    })
    ElMessage.success('删除成功')
    fetchUsers()
  } catch {
    // 用户取消删除
  }
}

const handleStatusChange = async (row) => {
  try {
    const action = row.status === 'active' ? '启用' : '禁用'
    ElMessage.success(`用户 ${row.username} ${action}成功`)
  } catch (error) {
    ElMessage.error('状态更新失败')
    // 回滚状态
    row.status = row.status === 'active' ? 'inactive' : 'active'
  }
}

const handleSizeChange = (size) => {
  pagination.size = size
  fetchUsers()
}

const handlePageChange = (page) => {
  pagination.page = page
  fetchUsers()
}

const getRoleTag = (role) => {
  const tagMap = {
    admin: 'danger',
    sales: 'success',
    procurement: 'warning',
    warehouse: 'info',
    finance: 'primary'
  }
  return tagMap[role] || 'info'
}

const getRoleText = (role) => {
  const textMap = {
    admin: '管理员',
    sales: '销售',
    procurement: '采购',
    warehouse: '仓库',
    finance: '财务'
  }
  return textMap[role] || '未知'
}

// 生命周期
onMounted(() => {
  fetchUsers()
})
</script>

<style scoped>
.users {
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
  margin-bottom: 20px;
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

.stats-cards {
  margin-top: 20px;
}

.stat-card {
  background: white;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  display: flex;
  align-items: center;
  gap: 15px;
}

.stat-icon {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
  color: white;
}

.stat-icon.total {
  background: #5c6bc0;
}

.stat-icon.active {
  background: #67c23a;
}

.stat-icon.online {
  background: #e6a23c;
}

.stat-icon.new {
  background: #f56c6c;
}

.stat-content {
  flex: 1;
}

.stat-value {
  font-size: 24px;
  font-weight: 600;
  color: #303133;
  margin-bottom: 4px;
}

.stat-label {
  font-size: 14px;
  color: #606266;
}
</style>