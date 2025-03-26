<template>
  <div class="main-layout">
    <el-container>
      <!-- Sidebar -->
      <el-aside width="220px" class="sidebar">
        <div class="logo-container">
          <h1 class="logo">PrePy ERP</h1>
          <h2 class="logo-sub">轻量化企业资源规划系统</h2>
        </div>
        
        <el-menu
          :router="true"
          :default-active="activeMenu"
          class="el-menu-vertical"
          background-color="#001529"
          text-color="#fff"
          active-text-color="#409EFF"
        >
          <!-- Dashboard -->
          <el-menu-item index="/" route="/">
            <el-icon><Odometer /></el-icon>
            <span>仪表板</span>
          </el-menu-item>
          
          <!-- Sales Management -->
          <el-sub-menu index="/sales">
            <template #title>
              <el-icon><ShoppingCart /></el-icon>
              <span>销售管理</span>
            </template>
            <el-menu-item index="/sales/quotations" route="/sales/quotations">报价单</el-menu-item>
            <el-menu-item index="/sales/orders" route="/sales/orders">销售订单</el-menu-item>
            <el-menu-item index="/sales/deliveries" route="/sales/deliveries">销售出库</el-menu-item>
            <el-menu-item index="/sales/invoices" route="/sales/invoices">销售发票</el-menu-item>
            <el-menu-item index="/sales/customers" route="/sales/customers">客户管理</el-menu-item>
          </el-sub-menu>
          
          <!-- Technical Management -->
          <el-sub-menu index="/technical">
            <template #title>
              <el-icon><SetUp /></el-icon>
              <span>技术管理</span>
            </template>
            <el-menu-item index="/technical/products" route="/technical/products">产品管理</el-menu-item>
            <el-menu-item index="/technical/boms" route="/technical/boms">物料清单</el-menu-item>
            <el-menu-item index="/technical/workstations" route="/technical/workstations">工作站</el-menu-item>
            <el-menu-item index="/technical/routes" route="/technical/routes">生产路线</el-menu-item>
            <el-menu-item index="/technical/documents" route="/technical/documents">技术文档</el-menu-item>
          </el-sub-menu>
          
          <!-- User Management (Admin only) -->
          <el-sub-menu index="/users" v-if="userStore.isAdmin">
            <template #title>
              <el-icon><UserFilled /></el-icon>
              <span>用户管理</span>
            </template>
            <el-menu-item index="/users/list" route="/users/list">用户列表</el-menu-item>
          </el-sub-menu>
        </el-menu>
      </el-aside>
      
      <!-- Main Content -->
      <el-container>
        <!-- Header -->
        <el-header class="header">
          <div class="header-left">
            <el-breadcrumb separator="/">
              <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
              <el-breadcrumb-item v-for="(item, index) in breadcrumbs" :key="index">
                {{ item.title }}
              </el-breadcrumb-item>
            </el-breadcrumb>
          </div>
          
          <div class="header-right">
            <el-dropdown trigger="click" @command="handleCommand">
              <span class="user-dropdown">
                {{ userStore.user?.full_name }}
                <el-icon><CaretBottom /></el-icon>
              </span>
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item command="profile">个人资料</el-dropdown-item>
                  <el-dropdown-item command="settings">设置</el-dropdown-item>
                  <el-dropdown-item divided command="logout">退出登录</el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
          </div>
        </el-header>
        
        <!-- Main Content -->
        <el-main>
          <router-view />
        </el-main>
        
        <!-- Footer -->
        <el-footer class="footer">
          <div>PrePy ERP &copy; {{ currentYear }} - 企业资源规划系统</div>
        </el-footer>
      </el-container>
    </el-container>
  </div>
</template>

<script>
import { computed, ref } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { useUserStore } from '@/stores/user';
import { ElMessage, ElMessageBox } from 'element-plus';

export default {
  name: 'MainLayout',
  setup() {
    const router = useRouter();
    const route = useRoute();
    const userStore = useUserStore();
    
    // Get current year for footer
    const currentYear = new Date().getFullYear();
    
    // Computed property to get active menu based on current route
    const activeMenu = computed(() => {
      return route.path;
    });
    
    // Computed property to generate breadcrumbs based on current route
    const breadcrumbs = computed(() => {
      const breadcrumbItems = [];
      const matched = route.matched;
      
      // Skip first route (MainLayout)
      for (let i = 1; i < matched.length; i++) {
        if (matched[i].meta && matched[i].meta.title) {
          breadcrumbItems.push({
            path: matched[i].path,
            title: matched[i].meta.title
          });
        }
      }
      
      return breadcrumbItems;
    });
    
    // Handle dropdown menu commands
    const handleCommand = (command) => {
      switch (command) {
        case 'profile':
          router.push('/users/profile');
          break;
        case 'settings':
          router.push('/users/settings');
          break;
        case 'logout':
          ElMessageBox.confirm('确定要退出登录吗?', '提示', {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning',
          }).then(async () => {
            await userStore.logoutUser();
            ElMessage({
              type: 'success',
              message: '您已成功退出登录'
            });
            router.push('/auth/login');
          }).catch(() => {
            // User cancelled logout
          });
          break;
      }
    };
    
    return {
      userStore,
      activeMenu,
      breadcrumbs,
      currentYear,
      handleCommand,
    };
  }
};
</script>

<style scoped>
.main-layout {
  height: 100%;
}

.sidebar {
  background-color: #001529;
  color: white;
  height: 100vh;
  overflow-y: auto;
  position: fixed;
  left: 0;
  top: 0;
  bottom: 0;
  z-index: 100;
}

.logo-container {
  height: 80px;
  padding: 0 20px;
  display: flex;
  align-items: center;
  display: table-cell;
  overflow: hidden;
  justify-content: center;
  padding: 12px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.2);
}

.logo {
  color: white;
  font-size: 23px;
  ;
}

.logo-sub {
  color: #eee;
  margin: 0;
  font-size: 13px;
  font-weight: 400;
}

.el-menu-vertical {
  border-right: none;
}

.el-container {
  margin-left: 150px;
  height: 100vh;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.header {
  height: 9vh;
  background-color: whibte;
  border-bottom: 2px solid #eee;
  border-radius: 4px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 22px;
  padding-top: 5px;
}

.user-dropdown {
  cursor: pointer;
  display: flex;
  align-items: center;
  font-weight: bold;
}

.el-main {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
  background-color: #f5f7fa;
}

.footer {
  padding: 15px 20px;
  text-align: center;
  color: #666;
  font-size: 12px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  border-top: 1px solid #eee;
  background-color: white;
}
</style> 