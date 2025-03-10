<template>
    <div class="register-container">
      <h2 class="page-title">注册账号</h2>
      
      <el-form
        ref="registerForm"
        :model="form"
        :rules="registerRules"
        label-position="top"
        @submit.prevent="handleRegister"
      >
        <el-form-item label="用户名" prop="username">
          <el-input
            v-model="form.username"
            placeholder="请输入用户名"
            prefix-icon="User"
            autocomplete="username"
          />
        </el-form-item>
        
        <el-form-item label="真实姓名" prop="full_name">
          <el-input
            v-model="form.full_name"
            placeholder="请输入真实姓名"
            prefix-icon="User"
          />
        </el-form-item>
        
        <el-form-item label="邮箱" prop="email">
          <el-input
            v-model="form.email"
            placeholder="请输入邮箱"
            prefix-icon="Message"
            autocomplete="email"
          />
        </el-form-item>
        
        <el-form-item label="密码" prop="password">
          <el-input
            v-model="form.password"
            placeholder="请输入密码"
            prefix-icon="Lock"
            type="password"
            autocomplete="new-password"
            show-password
          />
        </el-form-item>
        
        <el-form-item label="确认密码" prop="confirmPassword">
          <el-input
            v-model="form.confirmPassword"
            placeholder="请确认密码"
            prefix-icon="Lock"
            type="password"
            autocomplete="new-password"
            show-password
          />
        </el-form-item>
        
        <el-form-item>
          <el-button
            type="primary"
            native-type="submit"
            :loading="loading"
            class="register-button"
          >
            注册
          </el-button>
        </el-form-item>
        
        <div class="login-link">
          <p>
            已有账号?
            <router-link to="/auth/login">立即登录</router-link>
          </p>
        </div>
      </el-form>
    </div>
  </template>
  
  <script>
  import { defineComponent, reactive, ref } from 'vue';
  import { useRouter } from 'vue-router';
  import { ElMessage } from 'element-plus';
  import { useUserStore } from '@/stores/user';
  
  export default defineComponent({
    name: 'RegisterPage',
    setup() {
      const userStore = useUserStore();
      const router = useRouter();
      const registerForm = ref(null);
      const loading = ref(false);
      
      const form = reactive({
        username: '',
        full_name: '',
        email: '',
        password: '',
        confirmPassword: ''
      });
      
      const validatePass = (rule, value, callback) => {
        if (value === '') {
          callback(new Error('请输入密码'));
        } else {
          if (form.confirmPassword !== '') {
            registerForm.value.validateField('confirmPassword');
          }
          callback();
        }
      };
      
      const validatePass2 = (rule, value, callback) => {
        if (value === '') {
          callback(new Error('请再次输入密码'));
        } else if (value !== form.password) {
          callback(new Error('两次输入密码不一致!'));
        } else {
          callback();
        }
      };
      
      const rules = {
        username: [
          { required: true, message: '请输入用户名', trigger: 'blur' },
          { min: 3, message: '用户名长度至少为3个字符', trigger: 'blur' }
        ],
        full_name: [
          { required: true, message: '请输入真实姓名', trigger: 'blur' }
        ],
        email: [
          { required: true, message: '请输入邮箱地址', trigger: 'blur' },
          { type: 'email', message: '请输入正确的邮箱地址', trigger: 'blur' }
        ],
        password: [
          { required: true, message: '请输入密码', trigger: 'blur' },
          { min: 6, message: '密码长度至少为6个字符', trigger: 'blur' },
          { validator: validatePass, trigger: 'blur' }
        ],
        confirmPassword: [
          { required: true, message: '请再次输入密码', trigger: 'blur' },
          { validator: validatePass2, trigger: 'blur' }
        ]
      };
      
      const handleRegister = async () => {
        if (!registerForm.value) return;
        
        await registerForm.value.validate(async (valid) => {
          if (valid) {
            loading.value = true;
            
            try {
              // Remove confirmPassword before sending to API
              const userData = {
                username: form.username,
                full_name: form.full_name,
                email: form.email,
                password: form.password
              };
              
              await userStore.registerUser(userData);
              
              ElMessage({
                type: 'success',
                message: '注册成功，请登录'
              });
              
              router.push('/auth/login');
            } catch (error) {
              console.error('Registration error:', error);
              ElMessage({
                type: 'error',
                message: error.response?.data?.detail || '注册失败，请稍后再试'
              });
            } finally {
              loading.value = false;
            }
          }
        });
      };
      
      return {
        registerForm,
        registerRules: rules,
        loading,
        handleRegister,
        form
      };
    }
  });
  </script>
  
  <style scoped>
  .register-container {
    width: 100%;
  }
  
  .page-title {
    text-align: center;
    margin-bottom: 30px;
    font-weight: 500;
    color: #303133;
  }
  
  .register-button {
    width: 100%;
  }
  
  .login-link {
    text-align: center;
    margin-top: 20px;
    font-size: 14px;
    color: #606266;
  }
  </style>