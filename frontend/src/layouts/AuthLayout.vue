<template>
  <div class="auth-container">
    <div class="auth-card">
      <div class="logo-container">
        <h1 class="logo">PrePy ERP</h1>
        <p class="subtitle">企业资源规划系统</p>
      </div>
      
      <router-view />
      
      <div class="footer">
        <p>&copy; {{ currentYear }} PrePy ERP</p>
      </div>
    </div>
  </div>
</template>

<script>
import { defineComponent } from 'vue';

export default defineComponent({
  name: 'AuthLayout',
  setup() {
    const currentYear = new Date().getFullYear();
    
    return {
      currentYear
    };
  }
});
</script>

<style scoped>
.auth-container {
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: #f0f2f5;
}

.auth-card {
  width: 400px;
  background-color: white;
  border-radius: 4px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  padding: 40px;
}

.logo-container {
  text-align: center;
  margin-bottom: 30px;
}

.logo {
  margin: 0;
  font-size: 28px;
  color: #409EFF;
}

.subtitle {
  margin: 10px 0 0;
  font-size: 14px;
  color: #909399;
}

.footer {
  margin-top: 30px;
  text-align: center;
  color: #909399;
  font-size: 12px;
}
</style> 