<template>
  <div class="dashboard">
    <h1 class="page-title">仪表板</h1>

    <!-- Welcome message -->
    <el-card class="welcome-card">
      <template #header>
        <div class="card-header">
          <h3>欢迎，{{ userStore.user?.full_name || '用户' }}</h3>
          <el-tag type="success">{{ roleDisplay }}</el-tag>
        </div>
      </template>
      <p>欢迎使用 PrePy ERP 系统，这是您的管理仪表板。</p>
      <p>在这里，您可以查看关键指标并访问系统的各个模块。</p>
    </el-card>

    <!-- Quick stats -->
    <div class="stat-cards">
      <el-row :gutter="20">
        <el-col :xs="24" :sm="12" :md="6">
          <el-card shadow="hover" class="stat-card">
            <div class="stat-icon">
              <el-icon><ShoppingCart /></el-icon>
            </div>
            <div class="stat-content">
              <div class="stat-title">销售订单</div>
              <div class="stat-value">{{ dashboardData.salesOrders || 0 }}</div>
              <div class="stat-footer">本月新增</div>
            </div>
          </el-card>
        </el-col>
        <el-col :xs="24" :sm="12" :md="6">
          <el-card shadow="hover" class="stat-card">
            <div class="stat-icon" style="background-color: #67C23A;">
              <el-icon><Wallet /></el-icon>
            </div>
            <div class="stat-content">
              <div class="stat-title">销售额</div>
              <div class="stat-value">¥{{ formatNumber(dashboardData.salesAmount || 0) }}</div>
              <div class="stat-footer">本月累计</div>
            </div>
          </el-card>
        </el-col>
        <el-col :xs="24" :sm="12" :md="6">
          <el-card shadow="hover" class="stat-card">
            <div class="stat-icon" style="background-color: #E6A23C;">
              <el-icon><Box /></el-icon>
            </div>
            <div class="stat-content">
              <div class="stat-title">产品总数</div>
              <div class="stat-value">{{ dashboardData.productsCount || 0 }}</div>
              <div class="stat-footer">系统内产品</div>
            </div>
          </el-card>
        </el-col>
        <el-col :xs="24" :sm="12" :md="6">
          <el-card shadow="hover" class="stat-card">
            <div class="stat-icon" style="background-color: #F56C6C;">
              <el-icon><User /></el-icon>
            </div>
            <div class="stat-content">
              <div class="stat-title">客户总数</div>
              <div class="stat-value">{{ dashboardData.customersCount || 0 }}</div>
              <div class="stat-footer">系统内客户</div>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </div>

    <!-- Recent activities -->
    <el-card class="recent-activities">
      <template #header>
        <div class="card-header">
          <h3>最近活动</h3>
          <el-button type="primary" text>查看更多</el-button>
        </div>
      </template>
      <el-table :data="dashboardData.recentActivities || []" stripe style="width: 100%">
        <el-table-column prop="date" label="日期" width="180" />
        <el-table-column prop="type" label="类型" width="180">
          <template #default="scope">
            <el-tag :type="getActivityTagType(scope.row.type)">{{ scope.row.type }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="description" label="描述" />
        <el-table-column prop="user" label="用户" width="180" />
      </el-table>
      <div v-if="!(dashboardData.recentActivities && dashboardData.recentActivities.length)" class="no-data">
        暂无活动记录
      </div>
    </el-card>

    <!-- Quick Links -->
    <el-card class="quick-links">
      <template #header>
        <div class="card-header">
          <h3>快速链接</h3>
        </div>
      </template>
      <el-row :gutter="20">
        <el-col :xs="12" :sm="8" :md="4" v-for="(link, index) in quickLinks" :key="index">
          <el-card shadow="hover" class="link-card" @click="navigateTo(link.route)">
            <el-icon :size="24" :color="link.color">
              <component :is="link.icon" />
            </el-icon>
            <div class="link-title">{{ link.title }}</div>
          </el-card>
        </el-col>
      </el-row>
    </el-card>
  </div>
</template>

<script>
import { defineComponent, ref, onMounted, computed } from 'vue';
import { useRouter } from 'vue-router';
import { useUserStore } from '@/stores/user';
import { ElMessage } from 'element-plus';
// import { fetchDashboardData } from '@/api/dashboard';

export default defineComponent({
  name: 'DashboardPage',
  setup() {
    const userStore = useUserStore();
    const router = useRouter();
    const dashboardData = ref({
      salesOrders: 12,
      salesAmount: 128500,
      productsCount: 45,
      customersCount: 18,
      recentActivities: [
        {
          date: '2023-10-01 09:30:15',
          type: '登录',
          description: '用户登录系统',
          user: '管理员'
        },
        {
          date: '2023-10-01 10:15:22',
          type: '创建',
          description: '创建了新的销售订单 #SO-2023001',
          user: '销售经理'
        },
        {
          date: '2023-10-01 11:40:50',
          type: '更新',
          description: '更新了产品"工业风扇"的价格',
          user: '产品经理'
        },
        {
          date: '2023-10-01 13:25:33',
          type: '发货',
          description: '销售订单 #SO-2023001 已发货',
          user: '仓库管理员'
        }
      ]
    });

    const quickLinks = [
      { title: '销售订单', icon: 'ShoppingCart', route: '/sales/orders', color: '#409EFF' },
      { title: '新建报价', icon: 'Document', route: '/sales/quotations/new', color: '#67C23A' },
      { title: '客户管理', icon: 'User', route: '/sales/customers', color: '#E6A23C' },
      { title: '产品目录', icon: 'Box', route: '/technical/products', color: '#F56C6C' },
      { title: '物料清单', icon: 'Files', route: '/technical/boms', color: '#909399' },
      { title: '工作站', icon: 'SetUp', route: '/technical/workstations', color: '#6610f2' }
    ];

    const roleDisplay = computed(() => {
      const roleMap = {
        admin: '系统管理员',
        manager: '管理者',
        sales: '销售',
        technical: '技术员',
        planning: '计划员',
        production: '生产员',
        purchasing: '采购员',
        inventory: '库存管理员',
        finance: '财务',
        employee: '普通用户'
      };
      return roleMap[userStore.user?.role] || '用户';
    });

    const getActivityTagType = (type) => {
      const typeMap = {
        '登录': '',
        '创建': 'success',
        '更新': 'warning',
        '删除': 'danger',
        '发货': 'info'
      };
      return typeMap[type] || '';
    };

    const formatNumber = (num) => {
      return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
    };

    const navigateTo = (route) => {
      router.push(route);
    };

    onMounted(async () => {
      try {
        // In a real application, you would fetch data from the API
        // const data = await fetchDashboardData();
        // dashboardData.value = data;
      } catch (error) {
        console.error('Error fetching dashboard data:', error);
        ElMessage.error('获取仪表板数据失败');
      }
    });

    return {
      userStore,
      dashboardData,
      quickLinks,
      roleDisplay,
      getActivityTagType,
      formatNumber,
      navigateTo
    };
  }
});
</script>

<style scoped>
.dashboard {
  padding: 0 10px;
}

.page-title {
  margin-bottom: 20px;
  font-weight: 500;
}

.welcome-card {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-header h3 {
  margin: 0;
  font-size: 16px;
  font-weight: 500;
}

.stat-cards {
  margin-bottom: 20px;
}

.stat-card {
  display: flex;
  padding: 15px;
  margin-bottom: 20px;
}

.stat-icon {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 50px;
  height: 50px;
  border-radius: 8px;
  background-color: #409EFF;
  margin-right: 15px;
  color: white;
  font-size: 24px;
}

.stat-content {
  flex: 1;
}

.stat-title {
  font-size: 14px;
  color: #909399;
  margin-bottom: 5px;
}

.stat-value {
  font-size: 20px;
  font-weight: bold;
  margin-bottom: 5px;
}

.stat-footer {
  font-size: 12px;
  color: #909399;
}

.recent-activities {
  margin-bottom: 20px;
}

.no-data {
  text-align: center;
  padding: 20px;
  color: #909399;
}

.quick-links {
  margin-bottom: 20px;
}

.link-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 15px;
  height: 100px;
  cursor: pointer;
  margin-bottom: 20px;
  transition: all 0.3s;
}

.link-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.link-title {
  margin-top: 10px;
  font-size: 14px;
  color: #606266;
}
</style> 