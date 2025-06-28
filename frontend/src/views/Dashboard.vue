<template>
  <div class="dashboard-container">
    <!-- 页面标题 -->
    <div class="page-header">
      <h1 class="page-title">仪表盘</h1>
      <div class="header-actions">
        <el-button type="primary" @click="refreshData">
          <el-icon><Refresh /></el-icon>
          刷新数据
        </el-button>
      </div>
    </div>
    
    <!-- 统计卡片 -->
    <div class="stats-grid">
      <div class="stat-card" v-for="stat in statsData" :key="stat.key">
        <div class="stat-icon" :style="{ backgroundColor: stat.color }">
          <el-icon :size="24">
            <component :is="stat.icon" />
          </el-icon>
        </div>
        <div class="stat-content">
          <div class="stat-value">{{ stat.value }}</div>
          <div class="stat-label">{{ stat.label }}</div>
          <div class="stat-change" :class="stat.changeType">
            <el-icon><component :is="stat.changeIcon" /></el-icon>
            {{ stat.change }}
          </div>
        </div>
      </div>
    </div>
    
    <!-- 图表区域 -->
    <div class="charts-grid">
      <!-- 销售趋势图 -->
      <div class="chart-card">
        <div class="chart-header">
          <h3>销售趋势</h3>
          <el-select v-model="salesPeriod" size="small" style="width: 120px">
            <el-option label="最近7天" value="7d" />
            <el-option label="最近30天" value="30d" />
            <el-option label="最近90天" value="90d" />
          </el-select>
        </div>
        <div class="chart-content">
          <v-chart :option="salesChartOption" style="height: 300px" />
        </div>
      </div>
      
      <!-- 产品分类饼图 -->
      <div class="chart-card">
        <div class="chart-header">
          <h3>产品分类分布</h3>
        </div>
        <div class="chart-content">
          <v-chart :option="categoryChartOption" style="height: 300px" />
        </div>
      </div>
    </div>
    
    <!-- 数据表格区域 -->
    <div class="tables-grid">
      <!-- 最近订单 -->
      <div class="table-card">
        <div class="table-header">
          <h3>最近订单</h3>
          <el-link type="primary" @click="$router.push('/sales/orders')">
            查看全部
          </el-link>
        </div>
        <el-table :data="recentOrders" style="width: 100%" size="small">
          <el-table-column prop="number" label="订单号" width="120" />
          <el-table-column prop="customer" label="客户" />
          <el-table-column prop="amount" label="金额" width="100">
            <template #default="{ row }">
              ¥{{ row.amount.toLocaleString() }}
            </template>
          </el-table-column>
          <el-table-column prop="status" label="状态" width="80">
            <template #default="{ row }">
              <el-tag :type="getStatusType(row.status)" size="small">
                {{ row.status }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="date" label="日期" width="100" />
        </el-table>
      </div>
      
      <!-- 库存预警 -->
      <div class="table-card">
        <div class="table-header">
          <h3>库存预警</h3>
          <el-link type="primary" @click="$router.push('/warehouse/inventory')">
            查看全部
          </el-link>
        </div>
        <el-table :data="lowStockItems" style="width: 100%" size="small">
          <el-table-column prop="code" label="产品编码" width="120" />
          <el-table-column prop="name" label="产品名称" />
          <el-table-column prop="stock" label="库存" width="80">
            <template #default="{ row }">
              <span :class="{ 'text-danger': row.stock < row.minStock }">
                {{ row.stock }}
              </span>
            </template>
          </el-table-column>
          <el-table-column prop="minStock" label="最低库存" width="80" />
          <el-table-column prop="unit" label="单位" width="60" />
        </el-table>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue'
import { use } from 'echarts/core'
import { CanvasRenderer } from 'echarts/renderers'
import { LineChart, PieChart } from 'echarts/charts'
import {
  TitleComponent,
  TooltipComponent,
  LegendComponent,
  GridComponent
} from 'echarts/components'
import VChart from 'vue-echarts'

// 注册 ECharts 组件
use([
  CanvasRenderer,
  LineChart,
  PieChart,
  TitleComponent,
  TooltipComponent,
  LegendComponent,
  GridComponent
])

// 响应式数据
const salesPeriod = ref('30d')
const loading = ref(false)

// 统计数据
const statsData = reactive([
  {
    key: 'sales',
    label: '本月销售额',
    value: '¥1,234,567',
    change: '+12.5%',
    changeType: 'positive',
    changeIcon: 'ArrowUp',
    icon: 'Money',
    color: '#3f51b5'
  },
  {
    key: 'orders',
    label: '待处理订单',
    value: '156',
    change: '+8',
    changeType: 'positive',
    changeIcon: 'ArrowUp',
    icon: 'Document',
    color: '#52c41a'
  },
  {
    key: 'products',
    label: '产品总数',
    value: '2,345',
    change: '+23',
    changeType: 'positive',
    changeIcon: 'ArrowUp',
    icon: 'Box',
    color: '#fa8c16'
  },
  {
    key: 'alerts',
    label: '库存预警',
    value: '12',
    change: '-3',
    changeType: 'negative',
    changeIcon: 'ArrowDown',
    icon: 'Warning',
    color: '#f5222d'
  }
])

// 最近订单数据
const recentOrders = reactive([
  {
    number: 'SO-2024-001',
    customer: '华为技术有限公司',
    amount: 125000,
    status: '已确认',
    date: '2024-01-15'
  },
  {
    number: 'SO-2024-002',
    customer: '腾讯科技有限公司',
    amount: 89000,
    status: '待确认',
    date: '2024-01-14'
  },
  {
    number: 'SO-2024-003',
    customer: '阿里巴巴集团',
    amount: 156000,
    status: '已发货',
    date: '2024-01-13'
  },
  {
    number: 'SO-2024-004',
    customer: '百度在线网络技术',
    amount: 67000,
    status: '已完成',
    date: '2024-01-12'
  }
])

// 库存预警数据
const lowStockItems = reactive([
  {
    code: 'P001',
    name: '高精度传感器',
    stock: 5,
    minStock: 10,
    unit: '个'
  },
  {
    code: 'P002',
    name: '工业控制器',
    stock: 8,
    minStock: 15,
    unit: '台'
  },
  {
    code: 'P003',
    name: '电机驱动模块',
    stock: 12,
    minStock: 20,
    unit: '个'
  },
  {
    code: 'P004',
    name: '通信接口卡',
    stock: 3,
    minStock: 8,
    unit: '张'
  }
])

// 销售趋势图配置
const salesChartOption = computed(() => ({
  tooltip: {
    trigger: 'axis',
    axisPointer: {
      type: 'cross'
    }
  },
  grid: {
    left: '3%',
    right: '4%',
    bottom: '3%',
    containLabel: true
  },
  xAxis: {
    type: 'category',
    data: ['1月', '2月', '3月', '4月', '5月', '6月', '7月', '8月', '9月', '10月', '11月', '12月']
  },
  yAxis: {
    type: 'value',
    axisLabel: {
      formatter: '{value}万'
    }
  },
  series: [
    {
      name: '销售额',
      type: 'line',
      smooth: true,
      data: [120, 132, 101, 134, 90, 230, 210, 182, 191, 234, 290, 330],
      itemStyle: {
        color: '#3f51b5'
      },
      areaStyle: {
        color: {
          type: 'linear',
          x: 0,
          y: 0,
          x2: 0,
          y2: 1,
          colorStops: [
            { offset: 0, color: 'rgba(24, 144, 255, 0.3)' },
            { offset: 1, color: 'rgba(24, 144, 255, 0.1)' }
          ]
        }
      }
    }
  ]
}))

// 产品分类饼图配置
const categoryChartOption = computed(() => ({
  tooltip: {
    trigger: 'item',
    formatter: '{a} <br/>{b}: {c} ({d}%)'
  },
  legend: {
    orient: 'vertical',
    left: 'left'
  },
  series: [
    {
      name: '产品分类',
      type: 'pie',
      radius: ['40%', '70%'],
      avoidLabelOverlap: false,
      label: {
        show: false,
        position: 'center'
      },
      emphasis: {
        label: {
          show: true,
          fontSize: '18',
          fontWeight: 'bold'
        }
      },
      labelLine: {
        show: false
      },
      data: [
        { value: 335, name: '电子产品' },
        { value: 310, name: '机械设备' },
        { value: 234, name: '化工原料' },
        { value: 135, name: '纺织材料' },
        { value: 148, name: '其他' }
      ]
    }
  ]
}))

// 获取状态类型
const getStatusType = (status) => {
  const statusMap = {
    '已确认': 'success',
    '待确认': 'warning',
    '已发货': 'info',
    '已完成': 'success',
    '已取消': 'danger'
  }
  return statusMap[status] || 'info'
}

// 刷新数据
const refreshData = async () => {
  loading.value = true
  console.log('刷新仪表盘数据...')
  
  try {
    // 模拟API调用
    await new Promise(resolve => setTimeout(resolve, 1000))
    console.log('仪表盘数据刷新完成')
  } catch (error) {
    console.error('刷新数据失败:', error)
  } finally {
    loading.value = false
  }
}

// 组件挂载时加载数据
onMounted(() => {
  console.log('仪表盘页面已加载')
  refreshData()
})
</script>

<style scoped>
.dashboard-container {
  padding: 24px;
  background-color: #f5f5f5;
  min-height: 100vh;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.page-title {
  font-size: 24px;
  font-weight: 600;
  color: #262626;
  margin: 0;
}

.header-actions {
  display: flex;
  gap: 12px;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 20px;
  margin-bottom: 24px;
}

.stat-card {
  background: #fff;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  display: flex;
  align-items: center;
  gap: 16px;
  transition: transform 0.3s, box-shadow 0.3s;
}

.stat-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
}

.stat-icon {
  width: 56px;
  height: 56px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
}

.stat-content {
  flex: 1;
}

.stat-value {
  font-size: 28px;
  font-weight: 700;
  color: #262626;
  line-height: 1;
  margin-bottom: 4px;
}

.stat-label {
  font-size: 14px;
  color: #8c8c8c;
  margin-bottom: 8px;
}

.stat-change {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 12px;
  font-weight: 500;
}

.stat-change.positive {
  color: #52c41a;
}

.stat-change.negative {
  color: #f5222d;
}

.charts-grid {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 20px;
  margin-bottom: 24px;
}

.chart-card {
  background: #fff;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.chart-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.chart-header h3 {
  font-size: 16px;
  font-weight: 600;
  color: #262626;
  margin: 0;
}

.chart-content {
  width: 100%;
}

.tables-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
}

.table-card {
  background: #fff;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.table-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.table-header h3 {
  font-size: 16px;
  font-weight: 600;
  color: #262626;
  margin: 0;
}

.text-danger {
  color: #f5222d;
  font-weight: 600;
}

/* 响应式设计 */
@media (max-width: 1200px) {
  .charts-grid {
    grid-template-columns: 1fr;
  }
  
  .tables-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .dashboard-container {
    padding: 16px;
  }
  
  .stats-grid {
    grid-template-columns: 1fr;
  }
  
  .page-header {
    flex-direction: column;
    gap: 16px;
    align-items: flex-start;
  }
  
  .stat-card {
    padding: 16px;
  }
  
  .chart-card,
  .table-card {
    padding: 16px;
  }
}
</style>