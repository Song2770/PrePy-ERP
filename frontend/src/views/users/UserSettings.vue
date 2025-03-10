<template>
    <div class="settings-page page-container">
      <div class="page-header">
        <h1 class="page-title">账户设置</h1>
      </div>
      
      <el-card class="settings-card">
        <el-tabs v-model="activeTab" tab-position="left" style="min-height: 400px;">
          <!-- 密码修改 -->
          <el-tab-pane label="密码修改" name="password">
            <h2 class="section-title">修改密码</h2>
            <div class="section-description">定期更改密码有助于保护您的账户安全。</div>
            
            <el-form 
              ref="passwordForm" 
              :model="passwordForm" 
              :rules="passwordRules" 
              label-width="120px" 
              class="settings-form"
              @submit.prevent="updatePassword"
            >
              <el-form-item label="当前密码" prop="currentPassword">
                <el-input 
                  v-model="passwordForm.currentPassword"
                  type="password"
                  show-password
                  placeholder="请输入当前密码"
                />
              </el-form-item>
              
              <el-form-item label="新密码" prop="newPassword">
                <el-input 
                  v-model="passwordForm.newPassword"
                  type="password" 
                  show-password
                  placeholder="请输入新密码"
                />
                <div class="form-tip">密码长度应至少为8个字符，并包含字母和数字。</div>
              </el-form-item>
              
              <el-form-item label="确认新密码" prop="confirmPassword">
                <el-input 
                  v-model="passwordForm.confirmPassword"
                  type="password" 
                  show-password
                  placeholder="请再次输入新密码"
                />
              </el-form-item>
              
              <el-form-item>
                <el-button 
                  type="primary" 
                  native-type="submit" 
                  :loading="passwordLoading"
                >
                  更新密码
                </el-button>
              </el-form-item>
            </el-form>
          </el-tab-pane>
          
          <!-- 界面设置 -->
          <el-tab-pane label="界面设置" name="ui">
            <h2 class="section-title">界面设置</h2>
            <div class="section-description">自定义系统界面以获得更好的使用体验。</div>
            
            <el-form 
              ref="uiForm" 
              :model="uiForm" 
              label-width="120px" 
              class="settings-form"
              @submit.prevent="updateUiSettings"
            >
              <el-form-item label="语言">
                <el-select v-model="uiForm.language" style="width: 100%">
                  <el-option label="简体中文" value="zh-CN" />
                  <el-option label="English" value="en-US" />
                </el-select>
              </el-form-item>
              
              <el-form-item label="主题">
                <el-select v-model="uiForm.theme" style="width: 100%">
                  <el-option label="默认主题" value="default" />
                  <el-option label="深色主题" value="dark" />
                  <el-option label="蓝色主题" value="blue" />
                </el-select>
              </el-form-item>
              
              <el-form-item label="表格密度">
                <el-radio-group v-model="uiForm.tableDensity">
                  <el-radio label="compact">紧凑</el-radio>
                  <el-radio label="default">默认</el-radio>
                  <el-radio label="loose">宽松</el-radio>
                </el-radio-group>
              </el-form-item>
              
              <el-form-item label="显示欢迎页">
                <el-switch v-model="uiForm.showWelcome" />
              </el-form-item>
              
              <el-form-item>
                <el-button 
                  type="primary" 
                  native-type="submit" 
                  :loading="uiLoading"
                >
                  保存设置
                </el-button>
              </el-form-item>
            </el-form>
          </el-tab-pane>
          
          <!-- 通知设置 -->
          <el-tab-pane label="通知设置" name="notifications">
            <h2 class="section-title">通知设置</h2>
            <div class="section-description">管理您接收的系统通知。</div>
            
            <el-form 
              ref="notificationForm" 
              :model="notificationForm" 
              label-width="120px" 
              class="settings-form"
              @submit.prevent="updateNotificationSettings"
            >
              <el-form-item label="邮件通知">
                <el-switch v-model="notificationForm.emailEnabled" />
                <div class="form-tip">通过邮件接收系统通知。</div>
              </el-form-item>
              
              <div class="sub-settings" v-if="notificationForm.emailEnabled">
                <el-form-item label="订单通知">
                  <el-checkbox v-model="notificationForm.orderNotifications">接收订单状态变更通知</el-checkbox>
                </el-form-item>
                
                <el-form-item label="系统通知">
                  <el-checkbox v-model="notificationForm.systemNotifications">接收系统更新和公告</el-checkbox>
                </el-form-item>
                
                <el-form-item label="任务提醒">
                  <el-checkbox v-model="notificationForm.taskReminders">接收待办任务提醒</el-checkbox>
                </el-form-item>
              </div>
              
              <el-form-item label="应用内通知">
                <el-switch v-model="notificationForm.inAppEnabled" />
                <div class="form-tip">在系统界面内接收通知。</div>
              </el-form-item>
              
              <el-form-item>
                <el-button 
                  type="primary" 
                  native-type="submit" 
                  :loading="notificationLoading"
                >
                  保存设置
                </el-button>
              </el-form-item>
            </el-form>
          </el-tab-pane>
          
          <!-- 账户安全 -->
          <el-tab-pane label="账户安全" name="security">
            <h2 class="section-title">账户安全</h2>
            <div class="section-description">管理您的账户安全设置。</div>
            
            <!-- 登录会话 -->
            <div class="security-section">
              <h3 class="subsection-title">活跃会话</h3>
              <div class="session-list">
                <el-card class="session-item current-session">
                  <div class="session-info">
                    <div class="session-device">
                      <el-icon><Monitor /></el-icon>
                      <span>当前设备 - Windows</span>
                    </div>
                    <div class="session-details">
                      <div class="session-location">IP: 192.168.1.1 · 上海</div>
                      <div class="session-time">最后活动: 刚刚</div>
                    </div>
                  </div>
                  <div class="session-status">
                    <el-tag type="success">当前会话</el-tag>
                  </div>
                </el-card>
                
                <el-card class="session-item">
                  <div class="session-info">
                    <div class="session-device">
                      <el-icon><Iphone /></el-icon>
                      <span>移动设备 - iOS</span>
                    </div>
                    <div class="session-details">
                      <div class="session-location">IP: 114.88.XX.XX · 北京</div>
                      <div class="session-time">最后活动: 3小时前</div>
                    </div>
                  </div>
                  <div class="session-actions">
                    <el-button type="danger" size="small" @click="logoutSession(2)">注销</el-button>
                  </div>
                </el-card>
              </div>
              
              <div class="section-actions">
                <el-button type="danger" @click="logoutAllSessions">
                  <el-icon><CircleClose /></el-icon>
                  注销所有其他会话
                </el-button>
              </div>
            </div>
            
            <!-- 账户验证 -->
            <div class="security-section">
              <h3 class="subsection-title">两步验证</h3>
              <div class="security-option">
                <div class="security-option-content">
                  <div class="security-option-title">
                    启用两步验证
                  </div>
                  <div class="security-option-description">
                    使用身份验证应用程序或短信验证码提高账户安全性。
                  </div>
                </div>
                <div class="security-option-action">
                  <el-switch v-model="securityForm.twoFactorEnabled" @change="toggle2FA" />
                </div>
              </div>
            </div>
          </el-tab-pane>
        </el-tabs>
      </el-card>
    </div>
  </template>
  
  <script>
  import { defineComponent, ref, reactive, onMounted } from 'vue';
  import { ElMessage, ElMessageBox } from 'element-plus';
  import { useUserStore } from '@/stores/user';
  
  export default defineComponent({
    name: 'UserSettingsPage',
    setup() {
      const userStore = useUserStore();
      const activeTab = ref('password');
      
      // 密码修改表单
      const passwordForm = ref(null);
      const passwordLoading = ref(false);
      const passwordData = reactive({
        currentPassword: '',
        newPassword: '',
        confirmPassword: ''
      });
      
      // 密码验证规则
      const validatePass = (rule, value, callback) => {
        if (value === '') {
          callback(new Error('请输入新密码'));
        } else {
          if (value.length < 8) {
            callback(new Error('密码长度至少为8个字符'));
          } else if (!/\d/.test(value) || !/[a-zA-Z]/.test(value)) {
            callback(new Error('密码必须包含字母和数字'));
          } else if (passwordData.confirmPassword !== '') {
            passwordForm.value.validateField('confirmPassword');
          }
          callback();
        }
      };
      
      const validateConfirmPass = (rule, value, callback) => {
        if (value === '') {
          callback(new Error('请再次输入新密码'));
        } else if (value !== passwordData.newPassword) {
          callback(new Error('两次输入密码不一致!'));
        } else {
          callback();
        }
      };
      
      const passwordRules = {
        currentPassword: [
          { required: true, message: '请输入当前密码', trigger: 'blur' }
        ],
        newPassword: [
          { required: true, trigger: 'blur', validator: validatePass }
        ],
        confirmPassword: [
          { required: true, trigger: 'blur', validator: validateConfirmPass }
        ]
      };
      
      // 更新密码
      const updatePassword = async () => {
        if (!passwordForm.value) return;
        
        await passwordForm.value.validate(async (valid) => {
          if (valid) {
            passwordLoading.value = true;
            
            try {
              // 在真实应用中，调用API更新密码
              // await updateUserPassword({
              //   currentPassword: passwordData.currentPassword,
              //   newPassword: passwordData.newPassword
              // });
              
              // 模拟API调用
              await new Promise(resolve => setTimeout(resolve, 800));
              
              ElMessage.success('密码已成功更新');
              
              // 清空表单
              passwordData.currentPassword = '';
              passwordData.newPassword = '';
              passwordData.confirmPassword = '';
            } catch (error) {
              console.error('Error updating password:', error);
              ElMessage.error('密码更新失败，请确认当前密码正确');
            } finally {
              passwordLoading.value = false;
            }
          }
        });
      };
      
      // 界面设置表单
      const uiForm = ref(null);
      const uiLoading = ref(false);
      const uiData = reactive({
        language: 'zh-CN',
        theme: 'default',
        tableDensity: 'default',
        showWelcome: true
      });
      
      // 更新界面设置
      const updateUiSettings = async () => {
        uiLoading.value = true;
        
        try {
          // 在真实应用中，调用API保存设置
          // await updateUserUiSettings(uiData);
          
          // 模拟API调用
          await new Promise(resolve => setTimeout(resolve, 800));
          
          ElMessage.success('界面设置已保存');
          
          // 可以在这里应用一些设置，如主题切换
          // applyTheme(uiData.theme);
        } catch (error) {
          console.error('Error updating UI settings:', error);
          ElMessage.error('保存设置失败');
        } finally {
          uiLoading.value = false;
        }
      };
      
      // 通知设置表单
      const notificationForm = ref(null);
      const notificationLoading = ref(false);
      const notificationData = reactive({
        emailEnabled: true,
        orderNotifications: true,
        systemNotifications: true,
        taskReminders: false,
        inAppEnabled: true
      });
      
      // 更新通知设置
      const updateNotificationSettings = async () => {
        notificationLoading.value = true;
        
        try {
          // 在真实应用中，调用API保存设置
          // await updateUserNotificationSettings(notificationData);
          
          // 模拟API调用
          await new Promise(resolve => setTimeout(resolve, 800));
          
          ElMessage.success('通知设置已保存');
        } catch (error) {
          console.error('Error updating notification settings:', error);
          ElMessage.error('保存设置失败');
        } finally {
          notificationLoading.value = false;
        }
      };
      
      // 安全设置
      const securityForm = reactive({
        twoFactorEnabled: false
      });
      
      // 切换两步验证
      const toggle2FA = (value) => {
        if (value) {
          // 显示两步验证设置向导
          ElMessageBox.confirm(
            '启用两步验证将增强您的账户安全性。您需要设置身份验证应用程序或手机短信验证。是否继续?',
            '启用两步验证',
            {
              confirmButtonText: '继续设置',
              cancelButtonText: '取消',
              type: 'info'
            }
          ).then(() => {
            // 在真实应用中，跳转到两步验证设置页面或显示设置模态框
            ElMessage.info('两步验证设置功能尚未实现，敬请期待');
          }).catch(() => {
            // 用户取消，恢复开关状态
            securityForm.twoFactorEnabled = false;
          });
        } else {
          // 确认关闭两步验证
          ElMessageBox.confirm(
            '关闭两步验证将降低您的账户安全性。确定要继续吗?',
            '关闭两步验证',
            {
              confirmButtonText: '确定',
              cancelButtonText: '取消',
              type: 'warning'
            }
          ).then(() => {
            // 在真实应用中，调用API关闭两步验证
            ElMessage.success('两步验证已关闭');
          }).catch(() => {
            // 用户取消，恢复开关状态
            securityForm.twoFactorEnabled = true;
          });
        }
      };
      
      // 注销会话
      const logoutSession = (sessionId) => {
        ElMessageBox.confirm(
          '确定要注销此会话吗?',
          '注销会话',
          {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning'
          }
        ).then(() => {
          // 在真实应用中，调用API注销会话
          // await logoutUserSession(sessionId);
          
          ElMessage.success('会话已注销');
        });
      };
      
      // 注销所有其他会话
      const logoutAllSessions = () => {
        ElMessageBox.confirm(
          '确定要注销所有其他设备的会话吗?',
          '注销所有会话',
          {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning'
          }
        ).then(() => {
          // 在真实应用中，调用API注销所有其他会话
          // await logoutAllUserSessions();
          
          ElMessage.success('所有其他会话已注销');
        });
      };
      
      // 加载用户设置
      const loadUserSettings = async () => {
        try {
          // 在真实应用中，从API获取用户设置
          // const settings = await getUserSettings();
          // 
          // 应用设置到表单
          // uiData.language = settings.language || 'zh-CN';
          // uiData.theme = settings.theme || 'default';
          // ...
          
          // 使用模拟数据
          // 设置已经在reactive对象中设置了默认值
        } catch (error) {
          console.error('Error loading user settings:', error);
          ElMessage.error('加载设置失败');
        }
      };
      
      // 生命周期钩子
      onMounted(() => {
        loadUserSettings();
      });
      
      return {
        userStore,
        activeTab,
        
        // 密码修改
        passwordForm,
        passwordLoading,
        passwordRules,
        passwordForm: passwordData,
        updatePassword,
        
        // 界面设置
        uiForm,
        uiLoading,
        uiForm: uiData,
        updateUiSettings,
        
        // 通知设置
        notificationForm,
        notificationLoading,
        notificationForm: notificationData,
        updateNotificationSettings,
        
        // 安全设置
        securityForm,
        toggle2FA,
        logoutSession,
        logoutAllSessions
      };
    }
  });
  </script>
  
  <style scoped>
  .settings-page {
    min-height: calc(100vh - 200px);
  }
  
  .settings-card {
    margin-bottom: 20px;
  }
  
  .section-title {
    margin-top: 0;
    margin-bottom: 10px;
    font-size: 18px;
    color: #303133;
  }
  
  .section-description {
    margin-bottom: 25px;
    color: #909399;
    font-size: 14px;
  }
  
  .settings-form {
    max-width: 500px;
  }
  
  .form-tip {
    font-size: 12px;
    color: #909399;
    margin-top: 4px;
    line-height: 1.4;
  }
  
  .sub-settings {
    padding-left: 20px;
    margin-bottom: 20px;
    border-left: 2px solid #ebeef5;
  }
  
  .security-section {
    margin-bottom: 30px;
  }
  
  .subsection-title {
    margin-top: 0;
    margin-bottom: 15px;
    font-size: 16px;
    font-weight: 500;
    color: #303133;
  }
  
  .session-list {
    margin-bottom: 20px;
  }
  
  .session-item {
    margin-bottom: 15px;
    padding: 15px;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  
  .current-session {
    border-left: 3px solid #67C23A;
  }
  
  .session-info {
    flex: 1;
  }
  
  .session-device {
    display: flex;
    align-items: center;
    font-size: 16px;
    margin-bottom: 5px;
  }
  
  .session-device .el-icon {
    margin-right: 10px;
    font-size: 18px;
  }
  
  .session-details {
    margin-left: 28px;
    color: #909399;
    font-size: 13px;
  }
  
  .security-option {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 15px;
    background-color: #f5f7fa;
    border-radius: 4px;
    margin-bottom: 15px;
  }
  
  .security-option-title {
    font-weight: 500;
    margin-bottom: 5px;
  }
  
  .security-option-description {
    color: #909399;
    font-size: 13px;
  }
  
  .section-actions {
    margin-top: 20px;
  }
  </style>