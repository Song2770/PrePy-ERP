<template>
    <div class="not-found-container">
      <div class="not-found-content">
        <h1 class="error-code">404</h1>
        <div class="error-divider"></div>
        <h2 class="error-message">页面未找到</h2>
        <p class="error-description">
          抱歉，您访问的页面不存在或已被移除。
        </p>
        <div class="action-buttons">
          <el-button type="primary" @click="goHome">
            <el-icon><Back /></el-icon>
            返回首页
          </el-button>
          <el-button @click="goBack">返回上一页</el-button>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import { defineComponent } from 'vue';
  import { useRouter } from 'vue-router';
  
  export default defineComponent({
    name: 'NotFoundPage',
    setup() {
      const router = useRouter();
      
      const goHome = () => {
        router.push('/');
      };
      
      const goBack = () => {
        router.back();
      };
      
      return {
        goHome,
        goBack
      };
    }
  });
  </script>
  
  <style scoped>
  .not-found-container {
    height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
    background-color: #f5f7fa;
  }
  
  .not-found-content {
    text-align: center;
    padding: 50px;
    background-color: white;
    border-radius: 4px;
    box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
    max-width: 500px;
    width: 100%;
  }
  
  .error-code {
    font-size: 80px;
    color: #409EFF;
    margin: 0;
    font-weight: 600;
  }
  
  .error-divider {
    width: 80px;
    height: 4px;
    background-color: #409EFF;
    margin: 20px auto;
    border-radius: 2px;
  }
  
  .error-message {
    font-size: 24px;
    color: #303133;
    margin: 0 0 20px;
  }
  
  .error-description {
    color: #606266;
    margin-bottom: 30px;
  }
  
  .action-buttons {
    display: flex;
    justify-content: center;
    gap: 16px;
  }
  
  @media (max-width: 576px) {
    .not-found-content {
      padding: 30px;
    }
    
    .error-code {
      font-size: 60px;
    }
    
    .error-message {
      font-size: 20px;
    }
    
    .action-buttons {
      flex-direction: column;
    }
  }
  </style>