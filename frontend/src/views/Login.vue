<template>
  <div class="login-container">
    <div class="login-background">
      <div class="background-overlay"></div>
    </div>
    
    <div class="login-content">
      <div class="login-card">
        <div class="login-header">
          <img src="/logo.png" alt="PrePy ERP" class="login-logo" />
          <p class="login-subtitle">企业资源规划系统</p>
        </div>
        
        <el-form
          ref="loginFormRef"
          :model="loginForm"
          :rules="loginRules"
          class="login-form"
          @submit.prevent="handleLogin"
        >
          <el-form-item prop="username">
            <el-input
              v-model="loginForm.username"
              placeholder="请输入用户名"
              size="large"
              prefix-icon="User"
              clearable
              @keyup.enter="handleLogin"
            />
          </el-form-item>
          
          <el-form-item prop="password">
            <el-input
              v-model="loginForm.password"
              type="password"
              placeholder="请输入密码"
              size="large"
              prefix-icon="Lock"
              show-password
              clearable
              @keyup.enter="handleLogin"
            />
          </el-form-item>
          
          <el-form-item>
            <div class="login-options">
              <el-checkbox v-model="loginForm.remember">记住密码</el-checkbox>
              <el-link type="primary" :underline="false">忘记密码？</el-link>
            </div>
          </el-form-item>
          
          <el-form-item>
            <el-button
              type="primary"
              size="large"
              class="login-button"
              :loading="userStore.loading"
              @click="handleLogin"
            >
              {{ userStore.loading ? '登录中...' : '登录' }}
            </el-button>
          </el-form-item>
        </el-form>
        
        <div class="login-footer">
          <p class="demo-info">
            <el-icon><InfoFilled /></el-icon>
            演示账号：admin / admin123
          </p>
        </div>
      </div>
    </div>
    
    <!-- 版权信息 -->
    <div class="copyright">
      <p>&copy; 2024 PrePy ERP. All rights reserved.</p>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { ElMessage } from 'element-plus'

const router = useRouter()
const route = useRoute()
const userStore = useUserStore()

// 表单引用
const loginFormRef = ref()

// 登录表单数据
const loginForm = reactive({
  username: 'admin',
  password: '123456',
  remember: false
})

// 表单验证规则
const loginRules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 2, max: 50, message: '用户名长度在 2 到 50 个字符', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, max: 100, message: '密码长度在 6 到 100 个字符', trigger: 'blur' }
  ]
}

// 处理登录
const handleLogin = async () => {
  if (!loginFormRef.value) return
  
  try {
    // 验证表单
    await loginFormRef.value.validate()
    
    console.log('开始登录流程:', loginForm.username)
    
    // 调用登录接口
    const result = await userStore.login({
      username: loginForm.username,
      password: loginForm.password
    })
    
    if (result.success) {
      // 保存记住密码设置
      if (loginForm.remember) {
        localStorage.setItem('rememberedUsername', loginForm.username)
      } else {
        localStorage.removeItem('rememberedUsername')
      }
      
      // 登录成功，跳转到目标页面
      const redirectPath = route.query.redirect || '/dashboard'
      console.log('登录成功，跳转到:', redirectPath)
      
      await router.push(redirectPath)
    }
  } catch (error) {
    console.error('登录表单验证失败:', error)
  }
}

// 加载记住的用户名
const loadRememberedUsername = () => {
  const rememberedUsername = localStorage.getItem('rememberedUsername')
  if (rememberedUsername) {
    loginForm.username = rememberedUsername
    loginForm.remember = true
    console.log('加载记住的用户名:', rememberedUsername)
  }
}

// 组件挂载时执行
onMounted(() => {
  console.log('登录页面已加载')
  loadRememberedUsername()
  
  // 如果已经登录，直接跳转
  if (userStore.isAuthenticated) {
    console.log('用户已登录，跳转到首页')
    router.push('/dashboard')
  }
})
</script>

<style scoped>
.login-container {
  position: relative;
  width: 100vw;
  height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}

.login-background {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  z-index: 1;
}

.background-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><pattern id="grain" width="100" height="100" patternUnits="userSpaceOnUse"><circle cx="50" cy="50" r="1" fill="%23ffffff" opacity="0.1"/></pattern></defs><rect width="100" height="100" fill="url(%23grain)"/></svg>') repeat;
  opacity: 0.3;
}

.login-content {
  position: relative;
  z-index: 2;
  width: 100%;
  max-width: 400px;
  padding: 20px;
}

.login-card {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border-radius: 16px;
  padding: 40px;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.login-header {
  text-align: center;
  margin-bottom: 32px;
}

.login-logo {
  width: 200px;
  height: auto;
  aspect-ratio: 800/430;
  object-fit: contain;
}

.login-subtitle {
  font-size: 14px;
  color: #666;
  margin: 0;
  font-weight: 400;
}

.login-form {
  margin-bottom: 24px;
}

.login-form :deep(.el-form-item) {
  margin-bottom: 20px;
}

.login-form :deep(.el-input__wrapper) {
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  border: 1px solid #e1e5e9;
  transition: all 0.3s;
}

.login-form :deep(.el-input__wrapper:hover) {
  border-color: #5c6bc0;
  box-shadow: 0 2px 12px rgba(92, 107, 192, 0.2);
}

.login-form :deep(.el-input__wrapper.is-focus) {
  border-color: #5c6bc0;
  box-shadow: 0 2px 12px rgba(92, 107, 192, 0.3);
}

.login-options {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
}

.login-button {
  width: 100%;
  height: 48px;
  font-size: 16px;
  font-weight: 600;
  border-radius: 8px;
  background: linear-gradient(135deg, #5c6bc0 0%, #3f51b5 100%);
  border: none;
  box-shadow: 0 4px 12px rgba(92, 107, 192, 0.3);
  transition: all 0.3s;
}

.login-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(92, 107, 192, 0.4);
}

.login-button:active {
  transform: translateY(0);
}

.login-footer {
  text-align: center;
}

.demo-info {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  font-size: 13px;
  color: #666;
  background-color: #f8f9fa;
  padding: 12px 16px;
  border-radius: 8px;
  margin: 0;
  border: 1px solid #e9ecef;
}

.copyright {
  position: absolute;
  bottom: 20px;
  left: 50%;
  transform: translateX(-50%);
  z-index: 2;
  color: rgba(255, 255, 255, 0.8);
  font-size: 12px;
  text-align: center;
}

/* 响应式设计 */
@media (max-width: 480px) {
  .login-content {
    padding: 16px;
  }
  
  .login-card {
    padding: 24px;
    border-radius: 12px;
  }
  
  .login-title {
    font-size: 24px;
  }
  
  .login-logo {
    width: 160px;
    height: auto;
  }
}

/* 加载动画 */
@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.login-card {
  animation: fadeInUp 0.6s ease-out;
}
</style>