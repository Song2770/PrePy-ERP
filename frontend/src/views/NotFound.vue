<template>
  <div class="not-found-container">
    <div class="not-found-content">
      <div class="error-illustration">
        <div class="error-code">404</div>
        <div class="error-icon">
          <el-icon :size="120"><DocumentDelete /></el-icon>
        </div>
      </div>
      
      <div class="error-info">
        <h1 class="error-title">页面未找到</h1>
        <p class="error-description">
          抱歉，您访问的页面不存在或已被移除。
        </p>
        
        <div class="error-actions">
          <el-button type="primary" size="large" @click="goHome">
            <el-icon><HomeFilled /></el-icon>
            返回首页
          </el-button>
          
          <el-button size="large" @click="goBack">
            <el-icon><Back /></el-icon>
            返回上页
          </el-button>
        </div>
        
        <div class="help-links">
          <p class="help-text">您可以尝试：</p>
          <ul class="help-list">
            <li>
              <el-link type="primary" @click="$router.push('/dashboard')">
                访问仪表盘
              </el-link>
            </li>
            <li>
              <el-link type="primary" @click="$router.push('/sales/orders')">
                查看销售订单
              </el-link>
            </li>
            <li>
              <el-link type="primary" @click="$router.push('/master-data/products')">
                管理产品信息
              </el-link>
            </li>
            <li>
              <el-link type="primary" @click="$router.push('/warehouse/inventory')">
                查看库存状态
              </el-link>
            </li>
          </ul>
        </div>
      </div>
    </div>
    
    <!-- 装饰性背景 -->
    <div class="background-decoration">
      <div class="floating-shape shape-1"></div>
      <div class="floating-shape shape-2"></div>
      <div class="floating-shape shape-3"></div>
      <div class="floating-shape shape-4"></div>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'

const router = useRouter()

// 返回首页
const goHome = () => {
  console.log('返回首页')
  router.push('/dashboard')
  ElMessage.success('已返回首页')
}

// 返回上一页
const goBack = () => {
  console.log('返回上一页')
  if (window.history.length > 1) {
    router.go(-1)
  } else {
    router.push('/dashboard')
  }
}

console.log('404页面已加载')
</script>

<style scoped>
.not-found-container {
  position: relative;
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  overflow: hidden;
}

.not-found-content {
  position: relative;
  z-index: 2;
  text-align: center;
  max-width: 600px;
  padding: 40px;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border-radius: 20px;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.error-illustration {
  position: relative;
  margin-bottom: 40px;
}

.error-code {
  font-size: 120px;
  font-weight: 900;
  color: #5c6bc0;
  line-height: 1;
  margin-bottom: 20px;
  text-shadow: 0 4px 8px rgba(92, 107, 192, 0.3);
  background: linear-gradient(135deg, #5c6bc0 0%, #3f51b5 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.error-icon {
  color: #d9d9d9;
  opacity: 0.8;
}

.error-info {
  margin-bottom: 32px;
}

.error-title {
  font-size: 32px;
  font-weight: 700;
  color: #262626;
  margin: 0 0 16px 0;
  letter-spacing: -0.5px;
}

.error-description {
  font-size: 16px;
  color: #666;
  line-height: 1.6;
  margin: 0 0 32px 0;
}

.error-actions {
  display: flex;
  gap: 16px;
  justify-content: center;
  margin-bottom: 40px;
  flex-wrap: wrap;
}

.error-actions .el-button {
  border-radius: 8px;
  padding: 12px 24px;
  font-weight: 600;
}

.help-links {
  text-align: left;
  background-color: #f8f9fa;
  padding: 24px;
  border-radius: 12px;
  border: 1px solid #e9ecef;
}

.help-text {
  font-size: 14px;
  color: #666;
  margin: 0 0 12px 0;
  font-weight: 500;
}

.help-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.help-list li {
  margin-bottom: 8px;
  padding-left: 16px;
  position: relative;
}

.help-list li::before {
  content: '•';
  color: #5c6bc0;
  font-weight: bold;
  position: absolute;
  left: 0;
}

.help-list li:last-child {
  margin-bottom: 0;
}

/* 背景装饰 */
.background-decoration {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 1;
  overflow: hidden;
}

.floating-shape {
  position: absolute;
  border-radius: 50%;
  background: rgba(92, 107, 192, 0.1);
  animation: float 6s ease-in-out infinite;
}

.shape-1 {
  width: 80px;
  height: 80px;
  top: 10%;
  left: 10%;
  animation-delay: 0s;
}

.shape-2 {
  width: 120px;
  height: 120px;
  top: 20%;
  right: 15%;
  animation-delay: 2s;
}

.shape-3 {
  width: 60px;
  height: 60px;
  bottom: 20%;
  left: 20%;
  animation-delay: 4s;
}

.shape-4 {
  width: 100px;
  height: 100px;
  bottom: 10%;
  right: 10%;
  animation-delay: 1s;
}

@keyframes float {
  0%, 100% {
    transform: translateY(0px) rotate(0deg);
  }
  50% {
    transform: translateY(-20px) rotate(180deg);
  }
}

/* 响应式设计 */
@media (max-width: 768px) {
  .not-found-content {
    margin: 20px;
    padding: 24px;
  }
  
  .error-code {
    font-size: 80px;
  }
  
  .error-title {
    font-size: 24px;
  }
  
  .error-description {
    font-size: 14px;
  }
  
  .error-actions {
    flex-direction: column;
    align-items: center;
  }
  
  .error-actions .el-button {
    width: 100%;
    max-width: 200px;
  }
  
  .help-links {
    padding: 16px;
  }
}

@media (max-width: 480px) {
  .not-found-content {
    margin: 16px;
    padding: 20px;
  }
  
  .error-code {
    font-size: 60px;
  }
  
  .error-title {
    font-size: 20px;
  }
  
  .error-icon :deep(.el-icon) {
    font-size: 80px !important;
  }
}

/* 进入动画 */
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

.not-found-content {
  animation: fadeInUp 0.6s ease-out;
}
</style>