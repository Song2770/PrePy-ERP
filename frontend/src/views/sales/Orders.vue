<template>
  <div class="orders-container">
    <h1 class="page-title">销售订单管理</h1>

    <!-- 操作区 -->
    <div class="page-actions">
      <el-button type="primary" @click="handleCreateOrder">
        <el-icon><Plus /></el-icon> 新建订单
      </el-button>
      <div class="search-filter">
        <el-input
          v-model="searchQuery"
          placeholder="搜索订单号/客户"
          class="search-input"
          clearable
          @clear="fetchOrders"
        >
          <template #prefix>
            <el-icon><Search /></el-icon>
          </template>
        </el-input>
        <el-select v-model="statusFilter" placeholder="订单状态" clearable @change="handleFilterChange">
          <el-option label="全部" value="" />
          <el-option label="待确认" value="pending" />
          <el-option label="已确认" value="confirmed" />
          <el-option label="生产中" value="in_production" />
          <el-option label="已发货" value="shipped" />
          <el-option label="已完成" value="completed" />
          <el-option label="已取消" value="cancelled" />
        </el-select>
        <el-date-picker
          v-model="dateRange"
          type="daterange"
          range-separator="至"
          start-placeholder="开始日期"
          end-placeholder="结束日期"
          @change="handleFilterChange"
          value-format="YYYY-MM-DD"
          style="width: 260px"
        />
      </div>
    </div>

    <!-- 订单列表 -->
    <el-card shadow="never" class="list-card">
      <el-table
        v-loading="loading"
        :data="orders"
        border
        style="width: 100%"
        height="calc(100vh - 250px)"
      >
        <el-table-column type="index" width="60" align="center" />
        <el-table-column prop="code" label="订单编号" min-width="130" sortable />
        <el-table-column prop="customer_name" label="客户名称" min-width="150" />
        <el-table-column prop="order_date" label="订单日期" min-width="120" sortable />
        <el-table-column prop="expected_delivery_date" label="预计交付日期" min-width="120" sortable />
        <el-table-column prop="total_amount" label="订单金额" min-width="120" align="right" sortable>
          <template #default="scope">
            ¥{{ scope.row.total_amount?.toFixed(2) }}
          </template>
        </el-table-column>
        <el-table-column prop="status" label="状态" width="100" align="center">
          <template #default="scope">
            <el-tag :type="getStatusType(scope.row.status)">
              {{ getStatusText(scope.row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="payment_status" label="付款状态" width="100" align="center">
          <template #default="scope">
            <el-tag :type="getPaymentStatusType(scope.row.payment_status)">
              {{ getPaymentStatusText(scope.row.payment_status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="delivery_status" label="发货状态" width="100" align="center">
          <template #default="scope">
            <el-tag :type="getDeliveryStatusType(scope.row.delivery_status)">
              {{ getDeliveryStatusText(scope.row.delivery_status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="sales_rep" label="销售员" min-width="120" />
        <el-table-column label="操作" width="250" fixed="right">
          <template #default="scope">
            <el-button
              size="small"
              type="primary"
              @click="handleViewOrder(scope.row)"
              text
            >
              <el-icon><View /></el-icon> 查看
            </el-button>
            <el-button
              size="small"
              type="primary"
              @click="handleEditOrder(scope.row)"
              text
              v-if="canEdit(scope.row)"
            >
              <el-icon><Edit /></el-icon> 编辑
            </el-button>
            <el-dropdown trigger="click" @command="(cmd) => handleOrderActions(cmd, scope.row)">
              <el-button size="small" text>
                <el-icon><MoreFilled /></el-icon> 更多
              </el-button>
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item command="confirm" v-if="scope.row.status === 'pending'">确认订单</el-dropdown-item>
                  <el-dropdown-item command="deliver" v-if="['confirmed', 'in_production'].includes(scope.row.status)">安排发货</el-dropdown-item>
                  <el-dropdown-item command="invoice" v-if="['confirmed', 'in_production', 'shipped'].includes(scope.row.status)">创建发票</el-dropdown-item>
                  <el-dropdown-item command="cancel" v-if="['pending', 'confirmed'].includes(scope.row.status)">取消订单</el-dropdown-item>
                  <el-dropdown-item command="print">打印订单</el-dropdown-item>
                  <el-dropdown-item command="export">导出订单</el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
          </template>
        </el-table-column>
      </el-table>

      <!-- 分页 -->
      <div class="pagination-container">
        <el-pagination
          v-model:current-page="currentPage"
          v-model:page-size="pageSize"
          :page-sizes="[10, 20, 50, 100]"
          :total="total"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        />
      </div>
    </el-card>

    <!-- 取消订单确认对话框 -->
    <el-dialog
      v-model="cancelDialogVisible"
      title="取消订单"
      width="500px"
    >
      <p>您确定要取消此订单吗？</p>
      <p>订单号: {{ selectedOrder?.code }}</p>
      <p>客户: {{ selectedOrder?.customer_name }}</p>
      <el-input
        v-model="cancelReason"
        type="textarea"
        rows="3"
        placeholder="请输入取消原因"
      />
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="cancelDialogVisible = false">关闭</el-button>
          <el-button type="danger" @click="confirmCancelOrder" :loading="actionLoading">
            确认取消
          </el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue';
import { useRouter } from 'vue-router';
import { ElMessage, ElMessageBox } from 'element-plus';
import { useOrderApi } from '@/api/sales/order.js';
import { useInvoiceApi } from '@/api/sales/invoice';
import { useDeliveryApi } from '@/api/sales/delivery';

// 路由和API
const router = useRouter();
const orderApi = useOrderApi();
const invoiceApi = useInvoiceApi();
const deliveryApi = useDeliveryApi();

// 数据
const orders = ref([]);
const loading = ref(false);
const currentPage = ref(1);
const pageSize = ref(20);
const total = ref(0);
const searchQuery = ref('');
const statusFilter = ref('');
const dateRange = ref([]);
const cancelDialogVisible = ref(false);
const selectedOrder = ref(null);
const cancelReason = ref('');
const actionLoading = ref(false);

// 组件挂载时获取数据
onMounted(() => {
  fetchOrders();
});

// 获取订单列表
async function fetchOrders() {
  loading.value = true;
  try {
    const params = {
      page: currentPage.value,
      size: pageSize.value,
      query: searchQuery.value,
      status: statusFilter.value,
      start_date: dateRange.value ? dateRange.value[0] : undefined,
      end_date: dateRange.value ? dateRange.value[1] : undefined
    };
    const { data } = await orderApi.getOrders(params);
    orders.value = data.items;
    total.value = data.total;
  } catch (error) {
    console.error('获取订单列表失败:', error);
    ElMessage.error('获取订单列表失败');
  } finally {
    loading.value = false;
  }
}

// 分页处理
function handleSizeChange(val) {
  pageSize.value = val;
  fetchOrders();
}

function handleCurrentChange(val) {
  currentPage.value = val;
  fetchOrders();
}

// 筛选处理
function handleFilterChange() {
  currentPage.value = 1;
  fetchOrders();
}

// 创建订单
function handleCreateOrder() {
  router.push('/sales/orders/create');
}

// 查看订单
function handleViewOrder(order) {
  router.push(`/sales/orders/${order.id}`);
}

// 编辑订单
function handleEditOrder(order) {
  router.push(`/sales/orders/edit/${order.id}`);
}

// 订单其他操作
function handleOrderActions(action, order) {
  selectedOrder.value = order;
  
  switch (action) {
    case 'confirm':
      confirmOrder(order);
      break;
    case 'deliver':
      createDelivery(order);
      break;
    case 'invoice':
      createInvoice(order);
      break;
    case 'cancel':
      showCancelDialog(order);
      break;
    case 'print':
      printOrder(order);
      break;
    case 'export':
      exportOrder(order);
      break;
  }
}

// 确认订单
async function confirmOrder(order) {
  try {
    await ElMessageBox.confirm(
      `确定要确认订单 ${order.code} 吗？确认后将无法修改订单基本信息。`,
      '确认订单',
      {
        confirmButtonText: '确认',
        cancelButtonText: '取消',
        type: 'warning'
      }
    );
    
    actionLoading.value = true;
    await orderApi.confirmOrder(order.id);
    ElMessage.success('订单确认成功');
    fetchOrders();
  } catch (error) {
    if (error !== 'cancel') {
      console.error('确认订单失败:', error);
      ElMessage.error('确认订单失败');
    }
  } finally {
    actionLoading.value = false;
  }
}

// 创建发货单
function createDelivery(order) {
  router.push({
    path: '/sales/deliveries/create',
    query: { order_id: order.id }
  });
}

// 创建发票
function createInvoice(order) {
  router.push({
    path: '/sales/invoices/create',
    query: { order_id: order.id }
  });
}

// 显示取消订单对话框
function showCancelDialog(order) {
  selectedOrder.value = order;
  cancelReason.value = '';
  cancelDialogVisible.value = true;
}

// 确认取消订单
async function confirmCancelOrder() {
  if (!cancelReason.value.trim()) {
    ElMessage.warning('请输入取消原因');
    return;
  }
  
  actionLoading.value = true;
  try {
    await orderApi.cancelOrder(selectedOrder.value.id, { reason: cancelReason.value });
    ElMessage.success('订单已取消');
    cancelDialogVisible.value = false;
    fetchOrders();
  } catch (error) {
    console.error('取消订单失败:', error);
    ElMessage.error('取消订单失败');
  } finally {
    actionLoading.value = false;
  }
}

// 打印订单
function printOrder(order) {
  ElMessage.info('准备打印订单: ' + order.code);
  router.push({
    path: `/sales/orders/${order.id}`,
    query: { print: true }
  });
}

// 导出订单
function exportOrder(order) {
  ElMessage.success(`正在导出订单 ${order.code}`);
  // 这里是导出功能的模拟实现
  // 实际项目中应调用后端API执行导出
  setTimeout(() => {
    const filename = `订单_${order.code}_${new Date().getTime()}.xlsx`;
    ElMessage.success(`导出成功: ${filename}`);
  }, 1500);
}

// 判断订单是否可编辑
function canEdit(order) {
  return ['pending'].includes(order.status);
}

// 获取订单状态类型
function getStatusType(status) {
  const statusMap = {
    pending: 'warning',
    confirmed: 'primary',
    in_production: 'info',
    shipped: 'success',
    completed: 'success',
    cancelled: 'danger'
  };
  
  return statusMap[status] || 'info';
}

// 获取订单状态文本
function getStatusText(status) {
  const statusMap = {
    pending: '待确认',
    confirmed: '已确认',
    in_production: '生产中',
    shipped: '已发货',
    completed: '已完成',
    cancelled: '已取消'
  };
  
  return statusMap[status] || '未知';
}

// 获取付款状态类型
function getPaymentStatusType(status) {
  const statusMap = {
    unpaid: 'danger',
    partial: 'warning',
    paid: 'success'
  };
  
  return statusMap[status] || 'info';
}

// 获取付款状态文本
function getPaymentStatusText(status) {
  const statusMap = {
    unpaid: '未付款',
    partial: '部分付款',
    paid: '已付款'
  };
  
  return statusMap[status] || '未知';
}

// 获取发货状态类型
function getDeliveryStatusType(status) {
  const statusMap = {
    pending: 'info',
    partial: 'warning',
    completed: 'success'
  };
  
  return statusMap[status] || 'info';
}

// 获取发货状态文本
function getDeliveryStatusText(status) {
  const statusMap = {
    pending: '待发货',
    partial: '部分发货',
    completed: '已发货'
  };
  
  return statusMap[status] || '未知';
}
</script>

<style scoped>
.orders-container {
  padding: 20px;
}

.page-title {
  margin-bottom: 20px;
  font-size: 24px;
  font-weight: 600;
  color: #303133;
}

.page-actions {
  display: flex;
  justify-content: space-between;
  margin-bottom: 20px;
}

.search-filter {
  display: flex;
  gap: 10px;
}

.search-input {
  width: 300px;
}

.list-card {
  margin-bottom: 20px;
}

.pagination-container {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
}
</style>
