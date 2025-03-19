<template>
  <div class="login-container">
    <h2 class="page-title">登录系统</h2>
    
    <el-form
      ref="loginForm"
      :model="form"
      :rules="loginRules"
      label-position="top"
      @submit.prevent="handleLogin"
    >
      <el-form-item label="用户名" prop="username">
        <el-input
          v-model="form.username"
          placeholder="请输入用户名"
          prefix-icon="User"
          autocomplete="username"
        />
      </el-form-item>
      
      <el-form-item label="密码" prop="password">
        <el-input
          v-model="form.password"
          placeholder="请输入密码"
          prefix-icon="Lock"
          type="password"
          autocomplete="current-password"
          show-password
        />
      </el-form-item>
      
      <el-form-item>
        <el-row :gutter="10">
          <el-col :span="12">
            <el-checkbox v-model="rememberMe">记住我</el-checkbox>
          </el-col>
          <el-col :span="12" class="text-right">
            <router-link to="/auth/forgot-password" class="forgot-password">
              忘记密码?
            </router-link>
          </el-col>
        </el-row>
      </el-form-item>
      
      <el-form-item>
        <el-button
          type="primary"
          native-type="submit"
          :loading="loading"
          class="login-button"
        >
          登录
        </el-button>
      </el-form-item>
      
      <div class="register-link">
        <p>
          还没有账号?
          <router-link to="/auth/register">注册新账号</router-link>
        </p>
      </div>
    </el-form>
  </div>
</template>

<script>
import { defineComponent, reactive, ref } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { ElMessage } from 'element-plus';
import { useUserStore } from '@/stores/user';

export default defineComponent({
  name: 'LoginPage',
  setup() {
    const userStore = useUserStore();
    const router = useRouter();
    const route = useRoute();
    const loginForm = ref(null);
    const loading = ref(false);
    const rememberMe = ref(false);
    
    const form = reactive({
      username: '',
      password: ''
    });
    
    const rules = {
      username: [
        { required: true, message: '请输入用户名', trigger: 'blur' },
        { min: 3, message: '用户名长度至少为3个字符', trigger: 'blur' }
      ],
      password: [
        { required: true, message: '请输入密码', trigger: 'blur' },
        { min: 5, message: '密码长度至少为5个字符', trigger: 'blur' }
      ]
    };
    
    const handleLogin = async () => {
      if (!loginForm.value) return;
      
      await loginForm.value.validate(async (valid) => {
        if (valid) {
          loading.value = true;
          
          try {
            const success = await userStore.loginUser({
              username: form.username,
              password: form.password
            });
            
            if (success) {
              ElMessage({
                type: 'success',
                message: '登录成功'
              });
              
              setTimeout(() => {
                const redirectPath = route.query.redirect || '/';
                router.push(redirectPath);
              }, 300);
            } else {
              ElMessage({
                type: 'error',
                message: '用户名或密码错误'
              });
            }
          } catch (error) {
            console.error('Login error:', error);
            ElMessage({
              type: 'error',
              message: error.message || '登录失败，请稍后再试'
            });
          } finally {
            loading.value = false;
          }
        }
      });
    };
    
    return {
      loginForm,
      loginRules: rules,
      loading,
      rememberMe,
      handleLogin,
      form
    };
  }
});
</script>

<style scoped>
.login-container {
  width: 100%;
}

.page-title {
  text-align: center;
  margin-bottom: 30px;
  font-weight: 500;
  color: #303133;
}

.login-button {
  width: 100%;
}

.forgot-password {
  color: #409EFF;
  text-decoration: none;
  float: right;
}

.register-link {
  text-align: center;
  margin-top: 20px;
  font-size: 14px;
  color: #606266;
}

.text-right {
  text-align: right;
}
</style>