<template>
  <div class="layout-container">
    <!-- 侧边栏 -->
    <el-aside :width="isCollapse ? '60px' : '240px'" class="sidebar">
      <div class="logo-container">
        <img src="/logo.png" alt="PrePy ERP" class="logo" v-if="!isCollapse" />
        <img src="/logo.png" alt="PrePy ERP" class="logo-mini" v-else />
      </div>
      
      <el-menu
        :default-active="activeMenu"
        :collapse="isCollapse"
        :unique-opened="true"
        router
        class="sidebar-menu"
      >
        <el-menu-item index="/dashboard">
          <el-icon><DataBoard /></el-icon>
          <template #title>仪表盘</template>
        </el-menu-item>
        
        <el-sub-menu index="sales">
          <template #title>
            <el-icon><ShoppingCart /></el-icon>
            <span>销售管理</span>
          </template>
          <el-menu-item index="/sales/orders">销售订单</el-menu-item>
          <el-menu-item index="/sales/quotations">销售报价</el-menu-item>
        </el-sub-menu>
        
        <el-sub-menu index="production">
          <template #title>
            <el-icon><Setting /></el-icon>
            <span>生产管理</span>
          </template>
          <el-menu-item index="/production/work-orders">生产工单</el-menu-item>
          <el-menu-item index="/production/operations">工序管理</el-menu-item>
        </el-sub-menu>
        
        <el-sub-menu index="procurement">
          <template #title>
            <el-icon><ShoppingBag /></el-icon>
            <span>采购管理</span>
          </template>
          <el-menu-item index="/procurement/purchase-orders">采购订单</el-menu-item>
          <el-menu-item index="/procurement/suppliers">供应商管理</el-menu-item>
        </el-sub-menu>
        
        <el-sub-menu index="warehouse">
          <template #title>
            <el-icon><Box /></el-icon>
            <span>仓库管理</span>
          </template>
          <el-menu-item index="/warehouse/inventory">库存管理</el-menu-item>
          <el-menu-item index="/warehouse/stock-movements">库存移动</el-menu-item>
        </el-sub-menu>
        
        <el-sub-menu index="finance">
          <template #title>
            <el-icon><Money /></el-icon>
            <span>财务管理</span>
          </template>
          <el-menu-item index="/finance/invoices">发票管理</el-menu-item>
          <el-menu-item index="/finance/payments">付款管理</el-menu-item>
        </el-sub-menu>
        
        <el-sub-menu index="master-data">
          <template #title>
            <el-icon><Files /></el-icon>
            <span>基础数据</span>
          </template>
          <el-menu-item index="/master-data/products">产品管理</el-menu-item>
          <el-menu-item index="/master-data/customers">客户管理</el-menu-item>
        </el-sub-menu>
        
        <el-sub-menu index="system">
          <template #title>
            <el-icon><Tools /></el-icon>
            <span>系统管理</span>
          </template>
          <el-menu-item index="/system/users">用户管理</el-menu-item>
          <el-menu-item index="/system/roles">角色管理</el-menu-item>
        </el-sub-menu>
      </el-menu>
    </el-aside>
    
    <!-- 主内容区域 -->
    <el-container class="main-container">
      <!-- 顶部导航栏 -->
      <el-header class="header">
        <div class="header-left">
          <el-button
            type="text"
            @click="toggleCollapse"
            class="collapse-btn"
          >
            <el-icon><Expand v-if="isCollapse" /><Fold v-else /></el-icon>
          </el-button>
          
          <el-breadcrumb separator="/" class="breadcrumb">
            <el-breadcrumb-item
              v-for="item in breadcrumbList"
              :key="item.path"
              :to="item.path"
            >
              {{ item.title }}
            </el-breadcrumb-item>
          </el-breadcrumb>
        </div>
        
        <div class="header-right">
          <!-- 全屏按钮 -->
          <el-button type="text" @click="toggleFullscreen" class="header-btn">
            <el-icon><FullScreen /></el-icon>
          </el-button>
          
          <!-- 用户菜单 -->
          <el-dropdown @command="handleUserCommand" class="user-dropdown">
            <div class="user-info">
              <el-avatar :size="32" class="user-avatar">
                <el-icon><User /></el-icon>
              </el-avatar>
              <span class="user-name">{{ userStore.userName }}</span>
              <el-icon class="dropdown-icon"><ArrowDown /></el-icon>
            </div>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item command="profile">
                  <el-icon><User /></el-icon>
                  个人资料
                </el-dropdown-item>
                <el-dropdown-item command="settings">
                  <el-icon><Setting /></el-icon>
                  系统设置
                </el-dropdown-item>
                <el-dropdown-item divided command="logout">
                  <el-icon><SwitchButton /></el-icon>
                  退出登录
                </el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
      </el-header>
      
      <!-- 主内容 -->
      <el-main class="main-content">
        <router-view v-slot="{ Component }">
          <transition name="fade-transform" mode="out-in">
            <component :is="Component" />
          </transition>
        </router-view>
      </el-main>
    </el-container>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { ElMessageBox, ElMessage } from 'element-plus'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()

// 侧边栏折叠状态
const isCollapse = ref(false)

// 当前激活的菜单
const activeMenu = computed(() => {
  return route.path
})

// 面包屑导航
const breadcrumbList = computed(() => {
  const matched = route.matched.filter(item => item.meta && item.meta.title)
  const breadcrumbs = []
  
  matched.forEach(item => {
    if (item.meta.title) {
      breadcrumbs.push({
        path: item.path,
        title: item.meta.title
      })
    }
  })
  
  return breadcrumbs
})

// 切换侧边栏折叠状态
const toggleCollapse = () => {
  isCollapse.value = !isCollapse.value
  console.log('切换侧边栏状态:', isCollapse.value ? '折叠' : '展开')
}

// 全屏切换
const toggleFullscreen = () => {
  if (!document.fullscreenElement) {
    document.documentElement.requestFullscreen()
    console.log('进入全屏模式')
  } else {
    document.exitFullscreen()
    console.log('退出全屏模式')
  }
}

// 处理用户菜单命令
const handleUserCommand = async (command) => {
  console.log('用户菜单命令:', command)
  
  switch (command) {
    case 'profile':
      ElMessage.info('个人资料功能开发中...')
      break
      
    case 'settings':
      ElMessage.info('系统设置功能开发中...')
      break
      
    case 'logout':
      try {
        await ElMessageBox.confirm(
          '确定要退出登录吗？',
          '退出确认',
          {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning'
          }
        )
        
        await userStore.logout()
        router.push({ name: 'Login' })
      } catch {
        console.log('取消退出登录')
      }
      break
  }
}

// 监听路由变化
watch(
  () => route.path,
  (newPath) => {
    console.log('路由变化:', newPath)
  }
)

console.log('主布局组件已加载')
</script>

<style scoped>
.layout-container {
  display: flex;
  height: 100vh;
  background-color: #f5f5f5;
}

.sidebar {
  background-color: #ffffff;
  transition: width 0.3s;
  overflow: hidden;
  border-right: 1px solid #e0e0e0;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
}

.logo-container {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 64px;
  padding: 0 16px;
  background-color: #ffffff;
  border-bottom: 1px solid #e0e0e0;
}

/* 折叠状态下的logo容器 */
.sidebar[style*="width: 80px"] .logo-container {
  padding: 0;
}

.logo {
  height: 100px;
  max-width: 300px;
  object-fit: contain;
}

.logo-mini {
  height: 32px;
  width: 32px;
  object-fit: contain;
}



.sidebar-menu {
  border-right: none;
  background-color: #ffffff;
}

.sidebar-menu :deep(.el-menu-item) {
  color: rgba(0, 0, 0, 0.87);
  margin: 4px 8px;
  border-radius: 8px;
  transition: all 0.2s ease;
}

/* 折叠状态下的菜单样式重置 */
.sidebar-menu.el-menu--collapse {
  width: 80px;
}

.sidebar-menu.el-menu--collapse :deep(.el-menu-item),
.sidebar-menu.el-menu--collapse :deep(.el-sub-menu__title) {
  height: 56px !important;
  line-height: 56px !important;
  padding: 0 !important;
  margin: 0 !important;
  text-align: center !important;
  position: relative !important;
}

.sidebar-menu.el-menu--collapse :deep(.el-menu-item .el-icon),
.sidebar-menu.el-menu--collapse :deep(.el-sub-menu__title .el-icon) {
  position: absolute !important;
  left: 50% !important;
  top: 50% !important;
  transform: translate(-50%, -50%) !important;
  margin: 0 !important;
  font-size: 18px !important;
}

.sidebar-menu.el-menu--collapse :deep(.el-sub-menu__icon-arrow) {
  display: none !important;
}

.sidebar-menu.el-menu--collapse :deep(.el-menu-item span),
.sidebar-menu.el-menu--collapse :deep(.el-sub-menu__title span) {
  display: none !important;
}

.sidebar-menu :deep(.el-menu-item:hover) {
  background-color: rgba(63, 81, 181, 0.08);
  color: #3f51b5;
}

.sidebar-menu :deep(.el-menu-item.is-active) {
  background-color: rgba(63, 81, 181, 0.12);
  color: #3f51b5;
  font-weight: 500;
}

.sidebar-menu :deep(.el-sub-menu__title) {
  color: rgba(0, 0, 0, 0.87);
  margin: 4px 8px;
  border-radius: 8px;
  transition: all 0.2s ease;
}

.sidebar-menu :deep(.el-sub-menu__title:hover) {
  background-color: rgba(63, 81, 181, 0.08);
  color: #3f51b5;
}

.sidebar-menu :deep(.el-sub-menu .el-menu-item) {
  color: rgba(0, 0, 0, 0.6);
  margin: 2px 16px;
  border-radius: 6px;
  font-size: 14px;
}

.sidebar-menu :deep(.el-sub-menu .el-menu-item:hover) {
  background-color: rgba(63, 81, 181, 0.06);
  color: #3f51b5;
}

.sidebar-menu :deep(.el-sub-menu .el-menu-item.is-active) {
  background-color: rgba(63, 81, 181, 0.1);
  color: #3f51b5;
  font-weight: 500;
}

.sidebar-menu :deep(.el-icon) {
  color: rgba(0, 0, 0, 0.54);
}

.sidebar-menu :deep(.el-menu-item:hover .el-icon),
.sidebar-menu :deep(.el-sub-menu__title:hover .el-icon),
.sidebar-menu :deep(.el-menu-item.is-active .el-icon) {
  color: #3f51b5;
}

.main-container {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.header {
  background-color: #fff;
  border-bottom: 1px solid #e8e8e8;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.header-left {
  display: flex;
  align-items: center;
}

.collapse-btn {
  margin-right: 20px;
  font-size: 18px;
  color: #666;
}

.breadcrumb {
  font-size: 14px;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 16px;
}

.header-btn {
  font-size: 16px;
  color: #666;
}

.user-dropdown {
  cursor: pointer;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 12px;
  border-radius: 6px;
  transition: background-color 0.3s;
}

.user-info:hover {
  background-color: #f5f5f5;
}

.user-avatar {
  background-color: #3f51b5;
}

.user-name {
  font-size: 14px;
  color: #333;
  font-weight: 500;
}

.dropdown-icon {
  font-size: 12px;
  color: #999;
  transition: transform 0.3s;
}

.main-content {
  padding: 0;
  background-color: #f5f5f5;
  overflow-y: auto;
}

/* 页面切换动画 */
.fade-transform-enter-active,
.fade-transform-leave-active {
  transition: all 0.3s;
}

.fade-transform-enter-from {
  opacity: 0;
  transform: translateX(30px);
}

.fade-transform-leave-to {
  opacity: 0;
  transform: translateX(-30px);
}

/* 响应式设计 */
@media (max-width: 768px) {
  .layout-container {
    flex-direction: column;
  }
  
  .sidebar {
    width: 100% !important;
    height: auto;
  }
  
  .header {
    padding: 0 16px;
  }
  
  .breadcrumb {
    display: none;
  }
  
  .user-name {
    display: none;
  }
}
</style>