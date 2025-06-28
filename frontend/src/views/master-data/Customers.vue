<template>
  <div class="customers">
    <div class="page-header">
      <h1>客户管理</h1>
      <p>管理客户信息、联系方式和交易记录</p>
    </div>
    
    <div class="content-card">
      <div class="filters">
        <el-form :inline="true" :model="filters" class="filter-form">
          <el-form-item label="客户名称">
            <el-input v-model="filters.customerName" placeholder="请输入客户名称" clearable />
          </el-form-item>
          <el-form-item label="客户编码">
            <el-input v-model="filters.customerCode" placeholder="请输入客户编码" clearable />
          </el-form-item>
          <el-form-item label="客户类型">
            <el-select v-model="filters.customerType" placeholder="请选择类型" clearable>
              <el-option label="企业客户" value="enterprise" />
              <el-option label="个人客户" value="individual" />
              <el-option label="政府机构" value="government" />
              <el-option label="合作伙伴" value="partner" />
            </el-select>
          </el-form-item>
          <el-form-item label="客户等级">
            <el-select v-model="filters.customerLevel" placeholder="请选择等级" clearable>
              <el-option label="VIP客户" value="vip" />
              <el-option label="重要客户" value="important" />
              <el-option label="普通客户" value="normal" />
              <el-option label="潜在客户" value="potential" />
            </el-select>
          </el-form-item>
          <el-form-item label="状态">
            <el-select v-model="filters.status" placeholder="请选择状态" clearable>
              <el-option label="活跃" value="active" />
              <el-option label="非活跃" value="inactive" />
              <el-option label="黑名单" value="blacklist" />
            </el-select>
          </el-form-item>
          <el-form-item label="所在地区">
            <el-input v-model="filters.region" placeholder="请输入地区" clearable />
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="handleSearch">搜索</el-button>
            <el-button @click="handleReset">重置</el-button>
          </el-form-item>
        </el-form>
      </div>

      <div class="table-actions">
        <el-button type="primary" @click="handleAdd">新增客户</el-button>
        <el-button type="success" @click="handleBatchImport">批量导入</el-button>
        <el-button type="warning" @click="handleExport">导出客户</el-button>
        <el-button type="info" @click="handleAssignSales">分配销售</el-button>
      </div>

      <el-table :data="customerList" v-loading="loading" stripe>
        <el-table-column type="selection" width="55" />
        <el-table-column label="客户头像" width="80">
          <template #default="{ row }">
            <el-avatar :size="50" :src="row.avatar">
              <el-icon><User /></el-icon>
            </el-avatar>
          </template>
        </el-table-column>
        <el-table-column prop="customerCode" label="客户编码" width="120" />
        <el-table-column prop="customerName" label="客户名称" min-width="150" />
        <el-table-column prop="customerType" label="客户类型" width="100">
          <template #default="{ row }">
            <el-tag size="small" :type="getTypeTag(row.customerType)">
              {{ getTypeText(row.customerType) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="customerLevel" label="客户等级" width="100">
          <template #default="{ row }">
            <el-tag size="small" :type="getLevelTag(row.customerLevel)">
              {{ getLevelText(row.customerLevel) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="contactPerson" label="联系人" width="100" />
        <el-table-column prop="phone" label="联系电话" width="130" />
        <el-table-column prop="email" label="邮箱" width="180" />
        <el-table-column prop="region" label="所在地区" width="120" />
        <el-table-column prop="totalOrders" label="订单数量" width="100">
          <template #default="{ row }">
            <span class="order-count">{{ row.totalOrders }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="totalAmount" label="交易金额" width="120">
          <template #default="{ row }">
            <span class="amount">¥{{ row.totalAmount.toFixed(2) }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="lastOrderDate" label="最后交易" width="120" />
        <el-table-column prop="salesPerson" label="负责销售" width="100" />
        <el-table-column prop="status" label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="getStatusTag(row.status)">
              {{ getStatusText(row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="createdAt" label="创建时间" width="160" />
        <el-table-column label="操作" width="200" fixed="right">
          <template #default="{ row }">
            <el-button type="primary" size="small" @click="handleView(row)">查看</el-button>
            <el-button type="warning" size="small" @click="handleEdit(row)">编辑</el-button>
            <el-button type="info" size="small" @click="handleOrders(row)">订单</el-button>
            <el-dropdown trigger="click">
              <el-button type="info" size="small">
                更多<el-icon class="el-icon--right"><arrow-down /></el-icon>
              </el-button>
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item @click="handleContact(row)">联系记录</el-dropdown-item>
                  <el-dropdown-item @click="handleQuotation(row)">创建报价</el-dropdown-item>
                  <el-dropdown-item @click="handleContract(row)">合同管理</el-dropdown-item>
                  <el-dropdown-item @click="handleCredit(row)">信用管理</el-dropdown-item>
                  <el-dropdown-item divided @click="handleBlacklist(row)" v-if="row.status !== 'blacklist'">加入黑名单</el-dropdown-item>
                  <el-dropdown-item @click="handleRemoveBlacklist(row)" v-if="row.status === 'blacklist'">移出黑名单</el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
          </template>
        </el-table-column>
      </el-table>

      <div class="pagination">
        <el-pagination
          v-model:current-page="pagination.page"
          v-model:page-size="pagination.size"
          :page-sizes="[10, 20, 50, 100]"
          :total="pagination.total"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="handleSizeChange"
          @current-change="handlePageChange"
        />
      </div>
    </div>

    <!-- 客户统计卡片 -->
    <div class="stats-cards">
      <el-row :gutter="20">
        <el-col :span="6">
          <div class="stat-card">
            <div class="stat-icon total">
              <el-icon><User /></el-icon>
            </div>
            <div class="stat-content">
              <div class="stat-value">{{ stats.totalCustomers }}</div>
              <div class="stat-label">总客户数</div>
            </div>
          </div>
        </el-col>
        <el-col :span="6">
          <div class="stat-card">
            <div class="stat-icon active">
              <el-icon><Check /></el-icon>
            </div>
            <div class="stat-content">
              <div class="stat-value">{{ stats.activeCustomers }}</div>
              <div class="stat-label">活跃客户</div>
            </div>
          </div>
        </el-col>
        <el-col :span="6">
          <div class="stat-card">
            <div class="stat-icon vip">
              <el-icon><Star /></el-icon>
            </div>
            <div class="stat-content">
              <div class="stat-value">{{ stats.vipCustomers }}</div>
              <div class="stat-label">VIP客户</div>
            </div>
          </div>
        </el-col>
        <el-col :span="6">
          <div class="stat-card">
            <div class="stat-icon revenue">
              <el-icon><Money /></el-icon>
            </div>
            <div class="stat-content">
              <div class="stat-value">¥{{ stats.totalRevenue.toFixed(0) }}</div>
              <div class="stat-label">总交易额</div>
            </div>
          </div>
        </el-col>
      </el-row>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { User, Check, Star, Money, ArrowDown } from '@element-plus/icons-vue'

// 响应式数据
const loading = ref(false)
const customerList = ref([])

const filters = reactive({
  customerName: '',
  customerCode: '',
  customerType: '',
  customerLevel: '',
  status: '',
  region: ''
})

const pagination = reactive({
  page: 1,
  size: 20,
  total: 0
})

// 模拟数据
const mockData = [
  {
    id: 1,
    customerCode: 'C001',
    customerName: '深圳科技有限公司',
    customerType: 'enterprise',
    customerLevel: 'vip',
    contactPerson: '张经理',
    phone: '13800138001',
    email: 'zhang@sztech.com',
    region: '深圳市',
    totalOrders: 25,
    totalAmount: 125000.00,
    lastOrderDate: '2024-01-15',
    salesPerson: '李销售',
    status: 'active',
    avatar: '',
    createdAt: '2023-06-15 10:30:00'
  },
  {
    id: 2,
    customerCode: 'C002',
    customerName: '上海制造集团',
    customerType: 'enterprise',
    customerLevel: 'important',
    contactPerson: '王总监',
    phone: '13800138002',
    email: 'wang@shmanuf.com',
    region: '上海市',
    totalOrders: 18,
    totalAmount: 89000.00,
    lastOrderDate: '2024-01-12',
    salesPerson: '赵销售',
    status: 'active',
    avatar: '',
    createdAt: '2023-08-20 14:20:00'
  },
  {
    id: 3,
    customerCode: 'C003',
    customerName: '北京电子商务公司',
    customerType: 'enterprise',
    customerLevel: 'normal',
    contactPerson: '刘主管',
    phone: '13800138003',
    email: 'liu@bjecom.com',
    region: '北京市',
    totalOrders: 12,
    totalAmount: 45000.00,
    lastOrderDate: '2024-01-10',
    salesPerson: '钱销售',
    status: 'active',
    avatar: '',
    createdAt: '2023-09-10 16:45:00'
  },
  {
    id: 4,
    customerCode: 'C004',
    customerName: '广州贸易公司',
    customerType: 'enterprise',
    customerLevel: 'normal',
    contactPerson: '陈经理',
    phone: '13800138004',
    email: 'chen@gztrade.com',
    region: '广州市',
    totalOrders: 8,
    totalAmount: 32000.00,
    lastOrderDate: '2023-12-28',
    salesPerson: '孙销售',
    status: 'inactive',
    avatar: '',
    createdAt: '2023-10-05 11:20:00'
  },
  {
    id: 5,
    customerCode: 'C005',
    customerName: '杭州创新科技',
    customerType: 'enterprise',
    customerLevel: 'potential',
    contactPerson: '周工程师',
    phone: '13800138005',
    email: 'zhou@hzinno.com',
    region: '杭州市',
    totalOrders: 3,
    totalAmount: 15000.00,
    lastOrderDate: '2023-11-15',
    salesPerson: '吴销售',
    status: 'active',
    avatar: '',
    createdAt: '2023-11-01 08:30:00'
  },
  {
    id: 6,
    customerCode: 'C006',
    customerName: '成都智能制造',
    customerType: 'enterprise',
    customerLevel: 'important',
    contactPerson: '郑总',
    phone: '13800138006',
    email: 'zheng@cdsmart.com',
    region: '成都市',
    totalOrders: 15,
    totalAmount: 67000.00,
    lastOrderDate: '2024-01-08',
    salesPerson: '郑销售',
    status: 'active',
    avatar: '',
    createdAt: '2023-07-12 15:45:00'
  },
  {
    id: 7,
    customerCode: 'C007',
    customerName: '问题客户公司',
    customerType: 'enterprise',
    customerLevel: 'normal',
    contactPerson: '黑名单',
    phone: '13800138007',
    email: 'bad@problem.com',
    region: '其他',
    totalOrders: 2,
    totalAmount: 5000.00,
    lastOrderDate: '2023-08-15',
    salesPerson: '无',
    status: 'blacklist',
    avatar: '',
    createdAt: '2023-08-01 10:00:00'
  }
]

// 计算属性
const stats = computed(() => {
  const total = customerList.value.length
  const active = customerList.value.filter(c => c.status === 'active').length
  const vip = customerList.value.filter(c => c.customerLevel === 'vip').length
  const totalRevenue = customerList.value.reduce((sum, c) => sum + c.totalAmount, 0)
  
  return {
    totalCustomers: total,
    activeCustomers: active,
    vipCustomers: vip,
    totalRevenue: totalRevenue
  }
})

// 方法
const fetchCustomers = async () => {
  loading.value = true
  try {
    // 模拟API调用
    await new Promise(resolve => setTimeout(resolve, 500))
    customerList.value = mockData
    pagination.total = mockData.length
  } catch (error) {
    ElMessage.error('获取客户列表失败')
  } finally {
    loading.value = false
  }
}

const handleSearch = () => {
  pagination.page = 1
  fetchCustomers()
}

const handleReset = () => {
  Object.assign(filters, {
    customerName: '',
    customerCode: '',
    customerType: '',
    customerLevel: '',
    status: '',
    region: ''
  })
  handleSearch()
}

const handleAdd = () => {
  ElMessage.info('新增客户功能开发中')
}

const handleBatchImport = () => {
  ElMessage.info('批量导入功能开发中')
}

const handleExport = () => {
  ElMessage.info('导出功能开发中')
}

const handleAssignSales = () => {
  ElMessage.info('分配销售功能开发中')
}

const handleView = (row) => {
  ElMessage.info(`查看客户: ${row.customerName}`)
}

const handleEdit = (row) => {
  ElMessage.info(`编辑客户: ${row.customerName}`)
}

const handleOrders = (row) => {
  ElMessage.info(`查看订单: ${row.customerName}`)
}

const handleContact = (row) => {
  ElMessage.info(`联系记录: ${row.customerName}`)
}

const handleQuotation = (row) => {
  ElMessage.info(`创建报价: ${row.customerName}`)
}

const handleContract = (row) => {
  ElMessage.info(`合同管理: ${row.customerName}`)
}

const handleCredit = (row) => {
  ElMessage.info(`信用管理: ${row.customerName}`)
}

const handleBlacklist = async (row) => {
  try {
    await ElMessageBox.confirm(`确定要将客户 ${row.customerName} 加入黑名单吗？`, '加入黑名单', {
      type: 'warning'
    })
    row.status = 'blacklist'
    ElMessage.success('客户已加入黑名单')
  } catch {
    // 用户取消操作
  }
}

const handleRemoveBlacklist = async (row) => {
  try {
    await ElMessageBox.confirm(`确定要将客户 ${row.customerName} 移出黑名单吗？`, '移出黑名单', {
      type: 'warning'
    })
    row.status = 'active'
    ElMessage.success('客户已移出黑名单')
  } catch {
    // 用户取消操作
  }
}

const handleSizeChange = (size) => {
  pagination.size = size
  fetchCustomers()
}

const handlePageChange = (page) => {
  pagination.page = page
  fetchCustomers()
}

const getTypeTag = (type) => {
  const tagMap = {
    enterprise: 'primary',
    individual: 'success',
    government: 'warning',
    partner: 'info'
  }
  return tagMap[type] || 'info'
}

const getTypeText = (type) => {
  const textMap = {
    enterprise: '企业客户',
    individual: '个人客户',
    government: '政府机构',
    partner: '合作伙伴'
  }
  return textMap[type] || '未知'
}

const getLevelTag = (level) => {
  const tagMap = {
    vip: 'danger',
    important: 'warning',
    normal: 'primary',
    potential: 'info'
  }
  return tagMap[level] || 'info'
}

const getLevelText = (level) => {
  const textMap = {
    vip: 'VIP客户',
    important: '重要客户',
    normal: '普通客户',
    potential: '潜在客户'
  }
  return textMap[level] || '未知'
}

const getStatusTag = (status) => {
  const tagMap = {
    active: 'success',
    inactive: 'info',
    blacklist: 'danger'
  }
  return tagMap[status] || 'info'
}

const getStatusText = (status) => {
  const textMap = {
    active: '活跃',
    inactive: '非活跃',
    blacklist: '黑名单'
  }
  return textMap[status] || '未知'
}

// 生命周期
onMounted(() => {
  fetchCustomers()
})
</script>

<style scoped>
.customers {
  padding: 20px;
}

.page-header {
  margin-bottom: 20px;
}

.page-header h1 {
  margin: 0 0 8px 0;
  font-size: 24px;
  font-weight: 600;
  color: #303133;
}

.page-header p {
  margin: 0;
  color: #606266;
  font-size: 14px;
}

.content-card {
  background: white;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  margin-bottom: 20px;
}

.filters {
  margin-bottom: 20px;
  padding: 20px;
  background: #f8f9fa;
  border-radius: 6px;
}

.filter-form .el-form-item {
  margin-bottom: 0;
}

.table-actions {
  margin-bottom: 20px;
  display: flex;
  gap: 10px;
}

.pagination {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}

.order-count {
  font-weight: 600;
  color: #5c6bc0;
}

.amount {
  font-weight: 600;
  color: #67c23a;
}

.stats-cards {
  margin-top: 20px;
}

.stat-card {
  background: white;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  display: flex;
  align-items: center;
  gap: 15px;
}

.stat-icon {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
  color: white;
}

.stat-icon.total {
  background: #5c6bc0;
}

.stat-icon.active {
  background: #67c23a;
}

.stat-icon.vip {
  background: #f56c6c;
}

.stat-icon.revenue {
  background: #e6a23c;
}

.stat-content {
  flex: 1;
}

.stat-value {
  font-size: 24px;
  font-weight: 600;
  color: #303133;
  margin-bottom: 4px;
}

.stat-label {
  font-size: 14px;
  color: #606266;
}
</style>