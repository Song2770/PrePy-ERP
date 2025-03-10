<template>
    <div class="users-page page-container">
      <div class="page-header">
        <h1 class="page-title">用户管理</h1>
        <el-button type="primary" @click="showAddUserDialog">
          <el-icon><Plus /></el-icon>
          添加用户
        </el-button>
      </div>
  
      <!-- Search & Filters -->
      <el-card class="table-operations">
        <el-row :gutter="20">
          <el-col :xs="24" :sm="8">
            <el-input
              v-model="searchQuery"
              placeholder="搜索用户名、邮箱或姓名"
              clearable
              @input="handleSearch"
            >
              <template #prefix>
                <el-icon><Search /></el-icon>
              </template>
            </el-input>
          </el-col>
          <el-col :xs="24" :sm="8">
            <el-select
              v-model="filterRole"
              placeholder="用户角色"
              clearable
              style="width: 100%"
              @change="handleFilter"
            >
              <el-option label="全部" value="" />
              <el-option label="管理员" value="admin" />
              <el-option label="销售" value="sales" />
              <el-option label="技术" value="technical" />
              <el-option label="计划" value="planning" />
              <el-option label="生产" value="production" />
              <el-option label="采购" value="purchasing" />
              <el-option label="库存" value="inventory" />
              <el-option label="财务" value="finance" />
              <el-option label="员工" value="employee" />
            </el-select>
          </el-col>
          <el-col :xs="24" :sm="8">
            <el-select
              v-model="filterStatus"
              placeholder="用户状态"
              clearable
              style="width: 100%"
              @change="handleFilter"
            >
              <el-option label="全部" value="" />
              <el-option label="激活" value="true" />
              <el-option label="禁用" value="false" />
            </el-select>
          </el-col>
        </el-row>
        <el-row class="mt-10">
          <el-col :span="24">
            <el-button type="primary" plain @click="handleFilter">
              <el-icon><Filter /></el-icon>
              筛选
            </el-button>
            <el-button @click="resetFilter">
              <el-icon><Refresh /></el-icon>
              重置
            </el-button>
          </el-col>
        </el-row>
      </el-card>
  
      <!-- Users Table -->
      <el-card>
        <el-table
          v-loading="loading"
          :data="users"
          border
          style="width: 100%"
          @row-click="handleRowClick"
        >
          <el-table-column prop="username" label="用户名" min-width="120" />
          <el-table-column prop="full_name" label="姓名" min-width="120" />
          <el-table-column prop="email" label="邮箱" min-width="180" />
          <el-table-column prop="department" label="部门" min-width="120" />
          <el-table-column prop="position" label="职位" min-width="120" />
          <el-table-column label="角色" min-width="100">
            <template #default="scope">
              <el-tag :type="getRoleTagType(scope.row.role)">
                {{ getRoleLabel(scope.row.role) }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column label="状态" width="80">
            <template #default="scope">
              <el-tag :type="scope.row.is_active ? 'success' : 'info'">
                {{ scope.row.is_active ? '激活' : '禁用' }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column label="最后登录" min-width="160">
            <template #default="scope">
              {{ scope.row.last_login ? formatDate(scope.row.last_login) : '从未登录' }}
            </template>
          </el-table-column>
          <el-table-column label="操作" width="200" fixed="right">
            <template #default="scope">
              <el-button
                size="small"
                type="primary"
                @click.stop="handleEdit(scope.row)"
              >
                编辑
              </el-button>
              <el-button
                size="small"
                type="danger"
                @click.stop="handleDelete(scope.row)"
                :disabled="scope.row.id === currentUser.id"
              >
                删除
              </el-button>
            </template>
          </el-table-column>
        </el-table>
  
        <!-- Pagination -->
        <div class="pagination">
          <el-pagination
            v-model:currentPage="currentPage"
            v-model:page-size="pageSize"
            :page-sizes="[10, 20, 50, 100]"
            layout="total, sizes, prev, pager, next, jumper"
            :total="totalUsers"
            @size-change="handleSizeChange"
            @current-change="handleCurrentChange"
          />
        </div>
      </el-card>
  
      <!-- Add/Edit User Dialog -->
      <el-dialog
        v-model="dialogVisible"
        :title="editMode ? '编辑用户' : '添加用户'"
        width="600px"
      >
        <el-form
          ref="userForm"
          :model="userForm"
          :rules="userRules"
          label-width="100px"
          label-position="right"
        >
          <el-row :gutter="20">
            <el-col :span="12">
              <el-form-item label="用户名" prop="username">
                <el-input v-model="userForm.username" placeholder="请输入用户名" :disabled="editMode" />
              </el-form-item>
            </el-col>
            <el-col :span="12">
              <el-form-item label="姓名" prop="full_name">
                <el-input v-model="userForm.full_name" placeholder="请输入姓名" />
              </el-form-item>
            </el-col>
          </el-row>
  
          <el-form-item label="邮箱" prop="email">
            <el-input v-model="userForm.email" placeholder="请输入邮箱" />
          </el-form-item>
  
          <el-form-item label="密码" :prop="editMode ? '' : 'password'">
            <el-input 
              v-model="userForm.password" 
              placeholder="请输入密码" 
              type="password" 
              show-password 
              :disabled="editMode && !resetPassword"
            />
            <div v-if="editMode" class="reset-password-toggle">
              <el-checkbox v-model="resetPassword">重置密码</el-checkbox>
            </div>
          </el-form-item>
  
          <el-row :gutter="20">
            <el-col :span="12">
              <el-form-item label="角色" prop="role">
                <el-select v-model="userForm.role" placeholder="请选择角色" style="width: 100%">
                  <el-option label="管理员" value="admin" />
                  <el-option label="销售" value="sales" />
                  <el-option label="技术" value="technical" />
                  <el-option label="计划" value="planning" />
                  <el-option label="生产" value="production" />
                  <el-option label="采购" value="purchasing" />
                  <el-option label="库存" value="inventory" />
                  <el-option label="财务" value="finance" />
                  <el-option label="员工" value="employee" />
                </el-select>
              </el-form-item>
            </el-col>
            <el-col :span="12">
              <el-form-item label="状态" prop="is_active">
                <el-switch
                  v-model="userForm.is_active"
                  active-text="激活"
                  inactive-text="禁用"
                />
              </el-form-item>
            </el-col>
          </el-row>
  
          <el-row :gutter="20">
            <el-col :span="12">
              <el-form-item label="部门" prop="department">
                <el-input v-model="userForm.department" placeholder="请输入部门" />
              </el-form-item>
            </el-col>
            <el-col :span="12">
              <el-form-item label="职位" prop="position">
                <el-input v-model="userForm.position" placeholder="请输入职位" />
              </el-form-item>
            </el-col>
          </el-row>
        </el-form>
  
        <template #footer>
          <span class="dialog-footer">
            <el-button @click="dialogVisible = false">取消</el-button>
            <el-button type="primary" @click="submitForm" :loading="submitting">
              {{ editMode ? '更新' : '添加' }}
            </el-button>
          </span>
        </template>
      </el-dialog>
  
      <!-- User Details Dialog -->
      <el-dialog v-model="detailsVisible" title="用户详情" width="600px">
        <el-descriptions
          v-if="selectedUser"
          :column="2"
          border
        >
          <el-descriptions-item label="用户名">{{ selectedUser.username }}</el-descriptions-item>
          <el-descriptions-item label="姓名">{{ selectedUser.full_name }}</el-descriptions-item>
          <el-descriptions-item label="邮箱">{{ selectedUser.email }}</el-descriptions-item>
          <el-descriptions-item label="角色">
            <el-tag :type="getRoleTagType(selectedUser.role)">
              {{ getRoleLabel(selectedUser.role) }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="部门">{{ selectedUser.department || '未设置' }}</el-descriptions-item>
          <el-descriptions-item label="职位">{{ selectedUser.position || '未设置' }}</el-descriptions-item>
          <el-descriptions-item label="状态">
            <el-tag :type="selectedUser.is_active ? 'success' : 'info'">
              {{ selectedUser.is_active ? '激活' : '禁用' }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="管理员">
            <el-tag :type="selectedUser.is_superuser ? 'danger' : 'info'">
              {{ selectedUser.is_superuser ? '是' : '否' }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="创建时间">{{ formatDate(selectedUser.created_at) }}</el-descriptions-item>
          <el-descriptions-item label="最后更新">{{ formatDate(selectedUser.updated_at) }}</el-descriptions-item>
          <el-descriptions-item label="最后登录" :span="2">
            {{ selectedUser.last_login ? formatDate(selectedUser.last_login) : '从未登录' }}
          </el-descriptions-item>
        </el-descriptions>
  
        <template #footer>
          <span class="dialog-footer">
            <el-button @click="detailsVisible = false">关闭</el-button>
            <el-button type="primary" @click="handleEdit(selectedUser)">编辑</el-button>
          </span>
        </template>
      </el-dialog>
    </div>
  </template>
  
  <script>
  import { defineComponent, ref, reactive, onMounted, computed } from 'vue';
  import { ElMessage, ElMessageBox } from 'element-plus';
  import { useUserStore } from '@/stores/user';
  
  export default defineComponent({
    name: 'UsersListPage',
    setup() {
      // State
      const userStore = useUserStore();
      const loading = ref(false);
      const submitting = ref(false);
      const users = ref([]);
      const totalUsers = ref(0);
      const currentPage = ref(1);
      const pageSize = ref(10);
      const searchQuery = ref('');
      const filterRole = ref('');
      const filterStatus = ref('');
      const dialogVisible = ref(false);
      const detailsVisible = ref(false);
      const editMode = ref(false);
      const selectedUser = ref(null);
      const userForm = ref(null);
      const resetPassword = ref(false);
      
      // Current logged in user (for preventing self-deletion)
      const currentUser = computed(() => userStore.user || {});
  
      // Form default values and rules
      const form = reactive({
        username: '',
        full_name: '',
        email: '',
        password: '',
        role: 'employee',
        department: '',
        position: '',
        is_active: true
      });
  
      const userRules = {
        username: [
          { required: true, message: '请输入用户名', trigger: 'blur' },
          { min: 3, max: 20, message: '长度在 3 到 20 个字符', trigger: 'blur' }
        ],
        full_name: [
          { required: true, message: '请输入姓名', trigger: 'blur' }
        ],
        email: [
          { required: true, message: '请输入邮箱', trigger: 'blur' },
          { type: 'email', message: '请输入正确的邮箱地址', trigger: 'blur' }
        ],
        password: [
          { required: true, message: '请输入密码', trigger: 'blur' },
          { min: 6, message: '密码长度至少为6个字符', trigger: 'blur' }
        ],
        role: [
          { required: true, message: '请选择角色', trigger: 'change' }
        ]
      };
  
      // Helper functions for displaying role labels
      const getRoleLabel = (role) => {
        const roleMap = {
          'admin': '管理员',
          'manager': '管理者',
          'sales': '销售',
          'technical': '技术员',
          'planning': '计划员',
          'production': '生产员',
          'purchasing': '采购员',
          'inventory': '库存管理员',
          'finance': '财务',
          'employee': '员工'
        };
        return roleMap[role] || role;
      };
  
      const getRoleTagType = (role) => {
        const typeMap = {
          'admin': 'danger',
          'manager': 'warning',
          'sales': 'success',
          'technical': 'info',
          'planning': 'primary',
          'production': 'warning',
          'purchasing': 'success',
          'inventory': 'info',
          'finance': 'primary',
          'employee': ''
        };
        return typeMap[role] || '';
      };
  
      const formatDate = (dateString) => {
        if (!dateString) return '';
        const date = new Date(dateString);
        return date.toLocaleString();
      };
  
      // Methods
      const loadUsers = async () => {
        loading.value = true;
        try {
          const params = {
            skip: (currentPage.value - 1) * pageSize.value,
            limit: pageSize.value,
            search: searchQuery.value,
            role: filterRole.value,
            is_active: filterStatus.value
          };
          
          // 在真实应用中，调用API
          // const response = await fetchUsers(params);
          // users.value = response.data;
          // totalUsers.value = response.total;
          
          // 示例数据
          users.value = [
            {
              id: 1,
              username: 'admin',
              full_name: '系统管理员',
              email: 'admin@example.com',
              role: 'admin',
              department: '信息技术部',
              position: '系统管理员',
              is_active: true,
              is_superuser: true,
              created_at: '2023-01-01T00:00:00Z',
              updated_at: '2023-01-01T00:00:00Z',
              last_login: '2023-03-01T10:30:00Z'
            },
            {
              id: 2,
              username: 'sales',
              full_name: '销售经理',
              email: 'sales@example.com',
              role: 'sales',
              department: '销售部',
              position: '销售经理',
              is_active: true,
              is_superuser: false,
              created_at: '2023-01-02T00:00:00Z',
              updated_at: '2023-01-02T00:00:00Z',
              last_login: '2023-03-02T09:15:00Z'
            },
            {
              id: 3,
              username: 'technical',
              full_name: '技术经理',
              email: 'technical@example.com',
              role: 'technical',
              department: '技术部',
              position: '技术经理',
              is_active: true,
              is_superuser: false,
              created_at: '2023-01-03T00:00:00Z',
              updated_at: '2023-01-03T00:00:00Z',
              last_login: '2023-03-03T11:45:00Z'
            },
            {
              id: 4,
              username: 'employee',
              full_name: '普通员工',
              email: 'employee@example.com',
              role: 'employee',
              department: '行政部',
              position: '文员',
              is_active: false,
              is_superuser: false,
              created_at: '2023-01-04T00:00:00Z',
              updated_at: '2023-01-04T00:00:00Z',
              last_login: null
            }
          ];
          totalUsers.value = 4;
        } catch (error) {
          console.error('Error loading users:', error);
          ElMessage.error('加载用户数据失败');
        } finally {
          loading.value = false;
        }
      };
  
      const handleSearch = () => {
        currentPage.value = 1;
        loadUsers();
      };
  
      const handleFilter = () => {
        currentPage.value = 1;
        loadUsers();
      };
  
      const resetFilter = () => {
        searchQuery.value = '';
        filterRole.value = '';
        filterStatus.value = '';
        currentPage.value = 1;
        loadUsers();
      };
  
      const handleSizeChange = (val) => {
        pageSize.value = val;
        loadUsers();
      };
  
      const handleCurrentChange = (val) => {
        currentPage.value = val;
        loadUsers();
      };
  
      const resetForm = () => {
        Object.keys(form).forEach(key => {
          if (key === 'role') {
            form[key] = 'employee';
          } else if (key === 'is_active') {
            form[key] = true;
          } else {
            form[key] = '';
          }
        });
        resetPassword.value = false;
      };
  
      const showAddUserDialog = () => {
        resetForm();
        editMode.value = false;
        dialogVisible.value = true;
      };
  
      const handleRowClick = (row) => {
        selectedUser.value = row;
        detailsVisible.value = true;
      };
  
      const handleEdit = (user) => {
        editMode.value = true;
        resetPassword.value = false;
        
        // 将用户数据复制到表单
        Object.keys(form).forEach(key => {
          if (key !== 'password' && key in user) {
            form[key] = user[key];
          } else if (key === 'password') {
            form[key] = ''; // 清空密码字段
          }
        });
        
        selectedUser.value = user;
        dialogVisible.value = true;
        detailsVisible.value = false;
      };
  
      const handleDelete = (user) => {
        // 防止删除自己
        if (user.id === userStore.user?.id) {
          ElMessage.warning('不能删除当前登录用户');
          return;
        }
        
        ElMessageBox.confirm(
          `确定要删除用户 "${user.full_name}" (${user.username}) 吗?`,
          '警告',
          {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning',
          }
        ).then(async () => {
          try {
            // 在真实应用中，调用API
            // await deleteUser(user.id);
            
            ElMessage.success('删除成功');
            loadUsers();
          } catch (error) {
            console.error('Error deleting user:', error);
            ElMessage.error('删除失败');
          }
        }).catch(() => {
          // 用户取消操作
        });
      };
  
      const submitForm = async () => {
        if (!userForm.value) return;
        
        await userForm.value.validate(async (valid) => {
          if (valid) {
            submitting.value = true;
            
            try {
              // 构建提交的数据
              const userData = { ...form };
              
              // 如果是编辑模式且没有选择重置密码，则删除密码字段
              if (editMode.value && !resetPassword.value) {
                delete userData.password;
              }
              
              if (editMode.value) {
                // 在真实应用中，调用API
                // await updateUser(selectedUser.value.id, userData);
                ElMessage.success('用户信息更新成功');
              } else {
                // 在真实应用中，调用API
                // await createUser(userData);
                ElMessage.success('用户添加成功');
              }
              
              dialogVisible.value = false;
              loadUsers();
            } catch (error) {
              console.error('Error submitting form:', error);
              ElMessage.error(editMode.value ? '更新失败' : '添加失败');
            } finally {
              submitting.value = false;
            }
          }
        });
      };
  
      // 生命周期钩子
      onMounted(() => {
        loadUsers();
      });
  
      return {
        // State
        userStore,
        loading,
        submitting,
        users,
        totalUsers,
        currentPage,
        pageSize,
        searchQuery,
        filterRole,
        filterStatus,
        dialogVisible,
        detailsVisible,
        editMode,
        selectedUser,
        userForm,
        userRules,
        resetPassword,
        currentUser,
        
        // Methods
        getRoleLabel,
        getRoleTagType,
        formatDate,
        handleSearch,
        handleFilter,
        resetFilter,
        handleSizeChange,
        handleCurrentChange,
        showAddUserDialog,
        handleRowClick,
        handleEdit,
        handleDelete,
        submitForm,
        
        // Form data
        userForm: form
      };
    }
  });
  </script>
  
  <style scoped>
  .users-page {
    min-height: calc(100vh - 200px);
  }
  
  .table-operations {
    margin-bottom: 20px;
  }
  
  .el-table {
    cursor: pointer;
  }
  
  .dialog-footer {
    display: flex;
    justify-content: flex-end;
  }
  
  .reset-password-toggle {
    margin-top: 5px;
    font-size: 14px;
    color: #606266;
  }
  
  .mt-10 {
    margin-top: 10px;
  }
  </style>