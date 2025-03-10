<template>
    <div class="profile-page page-container">
      <div class="page-header">
        <h1 class="page-title">个人资料</h1>
      </div>
      
      <el-row :gutter="20">
        <!-- 左侧个人信息卡片 -->
        <el-col :span="8">
          <el-card class="profile-card">
            <div class="profile-header">
              <div class="avatar-container">
                <el-avatar :size="120" :src="avatarUrl">
                  {{ userInitials }}
                </el-avatar>
                <div class="avatar-upload">
                  <el-upload
                    class="avatar-uploader"
                    action="#"
                    :auto-upload="false"
                    :show-file-list="false"
                    :on-change="handleAvatarChange"
                  >
                    <el-button class="upload-button" size="small" type="primary">
                      <el-icon><EditPen /></el-icon>
                      更换头像
                    </el-button>
                  </el-upload>
                </div>
              </div>
              
              <div class="user-info">
                <h2 class="user-name">{{ userStore.user?.full_name || '用户名' }}</h2>
                <div class="user-role">
                  <el-tag :type="getRoleTagType(userStore.user?.role)">
                    {{ getRoleLabel(userStore.user?.role) }}
                  </el-tag>
                </div>
              </div>
            </div>
            
            <el-divider />
            
            <div class="info-section">
              <div class="info-item">
                <div class="info-label">
                  <el-icon><User /></el-icon>
                  用户名
                </div>
                <div class="info-value">{{ userStore.user?.username }}</div>
              </div>
              
              <div class="info-item">
                <div class="info-label">
                  <el-icon><Message /></el-icon>
                  邮箱
                </div>
                <div class="info-value">{{ userStore.user?.email }}</div>
              </div>
              
              <div class="info-item">
                <div class="info-label">
                  <el-icon><OfficeBuilding /></el-icon>
                  部门
                </div>
                <div class="info-value">{{ userStore.user?.department || '未设置' }}</div>
              </div>
              
              <div class="info-item">
                <div class="info-label">
                  <el-icon><Position /></el-icon>
                  职位
                </div>
                <div class="info-value">{{ userStore.user?.position || '未设置' }}</div>
              </div>
            </div>
            
            <el-divider />
            
            <div class="account-info">
              <div class="info-item">
                <div class="info-label">账户状态</div>
                <div class="info-value">
                  <el-tag :type="userStore.user?.is_active ? 'success' : 'danger'">
                    {{ userStore.user?.is_active ? '激活' : '已禁用' }}
                  </el-tag>
                </div>
              </div>
              
              <div class="info-item">
                <div class="info-label">创建时间</div>
                <div class="info-value">{{ formatDate(userStore.user?.created_at) }}</div>
              </div>
              
              <div class="info-item">
                <div class="info-label">最后登录</div>
                <div class="info-value">{{ formatDate(userStore.user?.last_login) || '从未登录' }}</div>
              </div>
            </div>
          </el-card>
        </el-col>
        
        <!-- 右侧编辑表单 -->
        <el-col :span="16">
          <el-card class="edit-card">
            <template #header>
              <div class="card-header">
                <h2 class="section-title">编辑个人资料</h2>
                <div class="last-updated">
                  上次更新: {{ formatDate(userStore.user?.updated_at) }}
                </div>
              </div>
            </template>
            
            <el-form
              ref="profileForm"
              :model="profileForm"
              :rules="profileRules"
              label-width="100px"
              label-position="top"
              @submit.prevent="updateProfile"
            >
              <el-row :gutter="20">
                <el-col :span="12">
                  <el-form-item label="姓名" prop="full_name">
                    <el-input v-model="profileForm.full_name" placeholder="请输入姓名" />
                  </el-form-item>
                </el-col>
                
                <el-col :span="12">
                  <el-form-item label="用户名" prop="username">
                    <el-input v-model="profileForm.username" placeholder="请输入用户名" disabled />
                    <div class="form-hint">用户名不可修改</div>
                  </el-form-item>
                </el-col>
              </el-row>
              
              <el-form-item label="邮箱" prop="email">
                <el-input v-model="profileForm.email" placeholder="请输入邮箱" />
              </el-form-item>
              
              <el-row :gutter="20">
                <el-col :span="12">
                  <el-form-item label="部门" prop="department">
                    <el-input v-model="profileForm.department" placeholder="请输入部门" />
                  </el-form-item>
                </el-col>
                
                <el-col :span="12">
                  <el-form-item label="职位" prop="position">
                    <el-input v-model="profileForm.position" placeholder="请输入职位" />
                  </el-form-item>
                </el-col>
              </el-row>
              
              <el-divider content-position="left">联系信息</el-divider>
              
              <el-row :gutter="20">
                <el-col :span="12">
                  <el-form-item label="手机号码" prop="phone">
                    <el-input v-model="profileForm.phone" placeholder="请输入手机号码" />
                  </el-form-item>
                </el-col>
                
                <el-col :span="12">
                  <el-form-item label="办公电话" prop="office_phone">
                    <el-input v-model="profileForm.office_phone" placeholder="请输入办公电话" />
                  </el-form-item>
                </el-col>
              </el-row>
              
              <el-form-item label="地址" prop="address">
                <el-input v-model="profileForm.address" placeholder="请输入地址" />
              </el-form-item>
              
              <el-divider content-position="left">个人信息</el-divider>
              
              <el-form-item label="个人简介" prop="bio">
                <el-input
                  v-model="profileForm.bio"
                  type="textarea"
                  :rows="4"
                  placeholder="请输入个人简介"
                />
              </el-form-item>
              
              <el-row :gutter="20">
                <el-col :span="12">
                  <el-form-item label="入职日期" prop="hire_date">
                    <el-date-picker
                      v-model="profileForm.hire_date"
                      type="date"
                      placeholder="选择入职日期"
                      style="width: 100%"
                    />
                  </el-form-item>
                </el-col>
                
                <el-col :span="12">
                  <el-form-item label="生日" prop="birthday">
                    <el-date-picker
                      v-model="profileForm.birthday"
                      type="date"
                      placeholder="选择生日"
                      style="width: 100%"
                    />
                  </el-form-item>
                </el-col>
              </el-row>
              
              <el-form-item>
                <el-button
                  type="primary"
                  native-type="submit"
                  :loading="loading"
                >
                  保存修改
                </el-button>
                <el-button @click="resetForm">重置</el-button>
              </el-form-item>
            </el-form>
          </el-card>
          
          <!-- 社交媒体与联系方式 -->
          <el-card class="social-card">
            <template #header>
              <div class="card-header">
                <h2 class="section-title">社交媒体</h2>
              </div>
            </template>
            
            <el-form
              ref="socialForm"
              :model="socialForm"
              label-width="100px"
              @submit.prevent="updateSocial"
            >
              <el-row :gutter="20">
                <el-col :xs="24" :sm="12">
                  <el-form-item label="微信">
                    <el-input v-model="socialForm.wechat" placeholder="微信号">
                      <template #prefix>
                        <i class="social-icon wechat-icon"></i>
                      </template>
                    </el-input>
                  </el-form-item>
                </el-col>
                
                <el-col :xs="24" :sm="12">
                  <el-form-item label="钉钉">
                    <el-input v-model="socialForm.dingtalk" placeholder="钉钉号">
                      <template #prefix>
                        <i class="social-icon dingtalk-icon"></i>
                      </template>
                    </el-input>
                  </el-form-item>
                </el-col>
              </el-row>
              
              <el-row :gutter="20">
                <el-col :xs="24" :sm="12">
                  <el-form-item label="GitHub">
                    <el-input v-model="socialForm.github" placeholder="GitHub用户名">
                      <template #prefix>
                        <el-icon><Link /></el-icon>
                      </template>
                    </el-input>
                  </el-form-item>
                </el-col>
                
                <el-col :xs="24" :sm="12">
                  <el-form-item label="个人网站">
                    <el-input v-model="socialForm.website" placeholder="个人网站URL">
                      <template #prefix>
                        <el-icon><House /></el-icon>
                      </template>
                    </el-input>
                  </el-form-item>
                </el-col>
              </el-row>
              
              <el-form-item>
                <el-button
                  type="primary"
                  native-type="submit"
                  :loading="socialLoading"
                >
                  保存信息
                </el-button>
              </el-form-item>
            </el-form>
          </el-card>
        </el-col>
      </el-row>
    </div>
  </template>
  
  <script>
  import { defineComponent, ref, reactive, computed, onMounted } from 'vue';
  import { ElMessage } from 'element-plus';
  import { useUserStore } from '@/stores/user';
  
  export default defineComponent({
    name: 'UserProfilePage',
    setup() {
      const userStore = useUserStore();
      const profileForm = ref(null);
      const socialForm = ref(null);
      const loading = ref(false);
      const socialLoading = ref(false);
      const avatarUrl = ref('');
      
      // 计算用户首字母作为头像默认显示
      const userInitials = computed(() => {
        const fullName = userStore.user?.full_name || '';
        if (!fullName) return '';
        
        const names = fullName.split(' ');
        if (names.length === 1) {
          return fullName.charAt(0).toUpperCase();
        } else {
          return (names[0].charAt(0) + names[names.length - 1].charAt(0)).toUpperCase();
        }
      });
      
      // 个人资料表单数据
      const form = reactive({
        username: '',
        full_name: '',
        email: '',
        department: '',
        position: '',
        phone: '',
        office_phone: '',
        address: '',
        bio: '',
        hire_date: '',
        birthday: ''
      });
      
      // 社交媒体表单数据
      const social = reactive({
        wechat: '',
        dingtalk: '',
        github: '',
        website: ''
      });
      
      // 表单验证规则
      const profileRules = {
        full_name: [
          { required: true, message: '请输入姓名', trigger: 'blur' }
        ],
        email: [
          { required: true, message: '请输入邮箱', trigger: 'blur' },
          { type: 'email', message: '请输入正确的邮箱地址', trigger: 'blur' }
        ],
        phone: [
          { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号码', trigger: 'blur' }
        ]
      };
      
      // 获取用户角色标签类型
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
      
      // 获取用户角色显示文本
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
        return roleMap[role] || role || '未知角色';
      };
      
      // 格式化日期
      const formatDate = (dateString) => {
        if (!dateString) return '';
        const date = new Date(dateString);
        return date.toLocaleString();
      };
      
      // 加载用户资料
      const loadUserProfile = () => {
        // 在真实应用中，可能需要从API获取更详细的用户资料
        // 这里简单使用store中的用户数据
        if (userStore.user) {
          form.username = userStore.user.username || '';
          form.full_name = userStore.user.full_name || '';
          form.email = userStore.user.email || '';
          form.department = userStore.user.department || '';
          form.position = userStore.user.position || '';
          
          // 模拟一些额外数据
          form.phone = '13800138000';
          form.office_phone = '010-12345678';
          form.address = '北京市海淀区中关村';
          form.bio = '这是一段个人简介，描述了用户的背景、专长和兴趣等信息。';
          form.hire_date = new Date('2022-01-15');
          
          // 模拟社交账号数据
          social.wechat = 'wx_username';
          social.dingtalk = 'dt_username';
          social.github = 'github_username';
          social.website = 'https://example.com';
        }
      };
      
      // 更新个人资料
      const updateProfile = async () => {
        if (!profileForm.value) return;
        
        await profileForm.value.validate(async (valid) => {
          if (valid) {
            loading.value = true;
            
            try {
              // 在真实应用中，调用API更新用户资料
              // const updatedUser = await updateUserProfile(form);
              
              // 模拟API延迟
              await new Promise(resolve => setTimeout(resolve, 800));
              
              // 更新本地状态
              userStore.setUser({
                ...userStore.user,
                full_name: form.full_name,
                email: form.email,
                department: form.department,
                position: form.position
              });
              
              ElMessage.success('个人资料已更新');
            } catch (error) {
              console.error('Error updating profile:', error);
              ElMessage.error('更新失败，请稍后重试');
            } finally {
              loading.value = false;
            }
          }
        });
      };
      
      // 更新社交媒体信息
      const updateSocial = async () => {
        socialLoading.value = true;
        
        try {
          // 在真实应用中，调用API更新社交媒体信息
          // await updateUserSocialMedia(social);
          
          // 模拟API延迟
          await new Promise(resolve => setTimeout(resolve, 800));
          
          ElMessage.success('社交媒体信息已更新');
        } catch (error) {
          console.error('Error updating social media:', error);
          ElMessage.error('更新失败，请稍后重试');
        } finally {
          socialLoading.value = false;
        }
      };
      
      // 处理头像上传
      const handleAvatarChange = (file) => {
        // 在真实应用中，上传头像文件到服务器
        // 这里只是简单预览
        avatarUrl.value = URL.createObjectURL(file.raw);
        
        // 模拟上传成功
        ElMessage.success('头像已更新');
      };
      
      // 重置表单
      const resetForm = () => {
        loadUserProfile();
      };
      
      // 生命周期钩子
      onMounted(() => {
        loadUserProfile();
      });
      
      return {
        userStore,
        profileForm,
        socialForm,
        profileForm: form,
        socialForm: social,
        loading,
        socialLoading,
        avatarUrl,
        userInitials,
        profileRules,
        getRoleTagType,
        getRoleLabel,
        formatDate,
        updateProfile,
        updateSocial,
        handleAvatarChange,
        resetForm
      };
    }
  });
  </script>
  
  <style scoped>
  .profile-page {
    margin-bottom: 40px;
  }
  
  .profile-card,
  .edit-card,
  .social-card {
    margin-bottom: 20px;
  }
  
  .profile-header {
    display: flex;
    flex-direction: column;
    align-items: center;
    margin-bottom: 20px;
  }
  
  .avatar-container {
    position: relative;
    margin-bottom: 20px;
  }
  
  .avatar-upload {
    margin-top: 10px;
    text-align: center;
  }
  
  .upload-button {
    display: inline-flex;
    align-items: center;
  }
  
  .upload-button .el-icon {
    margin-right: 4px;
  }
  
  .user-info {
    text-align: center;
  }
  
  .user-name {
    margin: 0 0 10px;
    font-size: 18px;
    font-weight: 500;
  }
  
  .user-role {
    margin-bottom: 10px;
  }
  
  .info-section,
  .account-info {
    margin-bottom: 20px;
  }
  
  .info-item {
    display: flex;
    justify-content: space-between;
    margin-bottom: 12px;
  }
  
  .info-label {
    color: #909399;
    display: flex;
    align-items: center;
  }
  
  .info-label .el-icon {
    margin-right: 6px;
  }
  
  .info-value {
    font-weight: 500;
    text-align: right;
  }
  
  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  
  .section-title {
    margin: 0;
    font-size: 16px;
    font-weight: 500;
  }
  
  .last-updated {
    font-size: 12px;
    color: #909399;
  }
  
  .form-hint {
    font-size: 12px;
    color: #909399;
    margin-top: 4px;
  }
  
  .social-icon {
    display: inline-block;
    width: 16px;
    height: 16px;
    background-size: contain;
    background-repeat: no-repeat;
    background-position: center;
  }
  
  .wechat-icon {
    background-image: url('data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCI+PHBhdGggZmlsbD0iIzA5QjgzQSIgZD0iTTkuNSwxMC4zQzkuNSwxMSw4LjksMTEuNSw4LjMsMTEuNWMtMC43LDAtMS4yLTAuNi0xLjItMS4yYzAtMC43LDAuNi0xLjIsMS4yLTEuMkM4LjksOS4xLDkuNSw5LjcsOS41LDEwLjNNMTMuNywxNi4zYy0wLjYsMC0xLjEtMC41LTEuMS0xLjFjMC0wLjYsMC41LTEuMSwxLjEtMS4xczEuMSwwLjUsMS4xLDEuMUMxNC44LDE1LjgsMTQuMywxNi4zLDEzLjcsMTYuM00xNi43LDExLjVjLTAuNiwwLTEuMi0wLjYtMS4yLTEuMmMwLTAuNywwLjYtMS4yLDEuMi0xLjJjMC43LDAsMS4yLDAuNiwxLjIsMS4yQzE3LjksMTEsMTcuMywxMS41LDE2LjcsMTEuNU0xMS4zLDE2LjNjLTAuNiwwLTEuMS0wLjUtMS4xLTEuMWMwLTAuNiwwLjUtMS4xLDEuMS0xLjFjMC42LDAsMS4xLDAuNSwxLjEsMS4xQzEyLjQsMTUuOCwxMS45LDE2LjMsMTEuMywxNi4zTTIzLjksMTUuNEMyNCwxNSwyNCwxNC42LDI0LDE0LjJoMGMwLTQuNCwwLTguOCwwLTEzLjNjMC0wLjMtMC4xLTAuNi0wLjMtMC44Yy0wLjItMC4yLTAuNC0wLjItMC43LTAuMkMxNS40LDAsMy4yLDAsMi45LDBDMi42LDAsMi4zLDAuMSwyLjEsMC4zQzIsMC41LDEuOSwwLjcsMS45LDFjMCw0LjUsMCw5LDAsMTMuNWMwLDAuMywwLjEsMC41LDAuMiwwLjhjMC4yLDAuMiwwLjQsMC4zLDAuNywwLjNjMS41LDAsMywwLDQuNSwwYzAuMSwwLjcsMC4zLDEuMywwLjYsMS45YzAuMywwLjcsMC44LDEuMywxLjMsMS45YzEsMS4xLDIuMiwxLjgsMy42LDIuM2MwLjgsMC4zLDEuNiwwLjQsMi40LDAuM2MwLjcsMCwxLjMtMC4yLDEuOS0wLjRjMC4xLDAsMC4yLTAuMSwwLjMtMC4xYzAuNCwwLjEsMC44LDAuMiwxLjMsMC4yYzAuMSwwLDAuMiwwLjEsMC4zLDAuMWMwLjQsMC4xLDAuOCwwLjEsMS4yLDAuMWMwLjMsMCwwLjYtMC4yLDAuNy0wLjVjMC4xLTAuMywwLTAuNS0wLjItMC43Yy0wLjEtMC4xLTAuMi0wLjEtMC4zLTAuMmMtMC42LTAuNC0xLTEtMS4yLTEuN2MwLTAuMSwwLTAuMSwwLjEtMC4yYzAuMi0wLjIsMC40LTAuNCwwLjYtMC42YzAuNi0wLjYsMS4xLTEuMiwxLjUtMmMwLjMtMC42LDAuNi0xLjMsMC43LTJDMjEsMTUuNCwyMi41LDE1LjQsMjMuOSwxNS40eiIvPjwvc3ZnPg==');
  }
  
  .dingtalk-icon {
    background-image: url('data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCI+PHBhdGggZmlsbD0iIzEyOTZkYiIgZD0iTTEyLjUsMEM2LjUsMC4xLDEuNiw1LjIsMS41LDExLjJjMCw2LjEsNC45LDExLjEsMTEsMTEuMWM2LjEsMCwxMS01LDExLjEtMTEuMUMyMy42LDUsMTguNiwwLDEyLjUsMHogTTE4LjEsOS44bC0xLjIsMC4zYy0wLjIsMC43LTAuNCwxLjQtMC43LDIuMWgtMi40YzAuMy0wLjYsMC41LTEuMywwLjctMkgxMWMtMC4xLDAuNC0wLjMsMC45LTAuNSwxLjNjLTAuMSwwLjMtMC4zLDAuNi0wLjQsMC43SDcuN2MtMC4yLDAtMC4zLDAtMC41LTAuMWMtMC4xLTAuMS0wLjEtMC4zLTAuMS0wLjRjMC0wLjEsMC4xLTAuMywwLjItMC40YzAuMi0wLjIsMC4zLTAuMywwLjUtMC40YzAuNy0wLjQsMS4zLTEsMi0xLjdjMC4zLTAuMywyLTIuMSwyLTIuMUg3LjJjLTAuMSwwLTAuMywwLTAuNS0wLjFjLTAuMi0wLjEtMC4yLTAuMy0wLjItMC40YzAtMC4yLDAtMC4zLDAuMi0wLjRjMC4xLTAuMSwwLjMtMC4xLDAuNS0wLjFoNi4yYzAuMiwwLDAuMywwLDAuNSwwLjFjMC4xLDAuMSwwLjIsMC4zLDAuMiwwLjRjMCwwLjItMC4xLDAuMy0wLjIsMC40Yy0wLjEsMC4xLTAuMywwLjEtMC41LDAuMWgtMmMwLjEsMC4xLDAuMiwwLjQsMC4zLDAuN0MxMSw2LjcsMTAuOSw2LjksMTAuNyw3SDEyYzAuMiwwLDAuMywwLDAuNSwwLjFjMC4xLDAuMSwwLjIsMC4zLDAuMiwwLjRjMCwwLjItMC4xLDAuMy0wLjIsMC40Yy0wLjEsMC4xLTAuMywwLjEtMC41LDAuMWgtMS43YzAsMC4xLDAsMC4xLTAuMSwwLjJjMCwwLjMtMC4yLDAuNi0wLjQsMUgxM2MwLjIsMCwwLjMsMCwwLjUsMC4xYzAuMSwwLjEsMC4yLDAuMywwLjIsMC40YzAsMC4yLTAuMSwwLjMtMC4yLDAuNGMtMC4xLDAuMS0wLjMsMC4xLTAuNSwwLjFoLTMuOGMxLDEuNywyLjQsMi43LDQsMy4xYzAuMi0wLjcsMC40LTEuMywwLjUtMmMwLjEtMC4zLDAuNC0wLjUsMC43LTAuNWMwLjEsMCwwLjMsMCwwLjQsMC4xYzAuMiwwLjEsMC4zLDAuMiwwLjQsMC40YzAuMSwwLjIsMC4xLDAuMywwLDAuNWMtMC40LDEuMy0wLjksMi41LTEuNywzLjVDMTguMSwxNy4yLDE5LjcsMTMuOCwxOC4xLDkuOHoiLz48L3N2Zz4=');
  }
  
  /* 响应式调整 */
  @media (max-width: 768px) {
    .info-item {
      flex-direction: column;
    }
    
    .info-value {
      text-align: left;
      margin-top: 4px;
    }
  }
  </style>