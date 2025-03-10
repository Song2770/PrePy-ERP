<template>
  <div class="quotation-detail-container">
    <div class="page-header">
      <div class="header-left">
        <el-button @click="goBack" plain>
          <el-icon><Back /></el-icon> 返回
        </el-button>
        <h1 class="page-title">报价单详情</h1>
        <el-tag v-if="quotation.status" class="ml-10" :type="getStatusType(quotation.status)">
          {{ getStatusText(quotation.status) }}
        </el-tag>
      </div>
      <div class="header-actions">
        <el-button @click="printQuotation">
          <el-icon><Printer /></el-icon> 打印
        </el-button>
        <el-dropdown trigger="click" @command="handleExport">
          <el-button>
            <el-icon><Download /></el-icon> 导出
            <el-icon class="ml-5"><ArrowDown /></el-icon>
          </el-button>
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item command="excel">导出 Excel</el-dropdown-item>
              <el-dropdown-item command="pdf">导出 PDF</el-dropdown-item>
              <el-dropdown-item command="word">导出 Word</el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>
        <el-button 
          type="primary" 
          @click="handleConvertToOrder" 
          v-if="quotation.status === 'approved'"
        >
          <el-icon><TopRight /></el-icon> 转换为订单
        </el-button>
        <el-button 
          type="primary" 
          @click="handleEdit"
          v-if="['draft', 'rejected'].includes(quotation.status)"
        >
          <el-icon><Edit /></el-icon> 编辑
        </el-button>
      </div>
    </div>

    <div v-loading="loading" class="main-content">
      <!-- 报价单基本信息 -->
      <el-card class="info-card">
        <el-descriptions :column="3" border size="medium">
          <el-descriptions-item label="报价单号">{{ quotation.code }}</el-descriptions-item>
          <el-descriptions-item label="客户名称">
            <el-link @click="viewCustomer(quotation.customer_id)" type="primary">
              {{ quotation.customer_name }}
            </el-link>
          </el-descriptions-item>
          <el-descriptions-item label="联系人">{{ quotation.contact_name }}</el-descriptions-item>
          <el-descriptions-item label="报价日期">{{ quotation.quotation_date }}</el-descriptions-item>
          <el-descriptions-item label="有效期至">{{ quotation.valid_until }}</el-descriptions-item>
          <el-descriptions-item label="销售代表">{{ quotation.sales_rep }}</el-descriptions-item>
          <el-descriptions-item label="支付条款">{{ quotation.payment_terms }}</el-descriptions-item>
          <el-descriptions-item label="交付方式">{{ quotation.delivery_method }}</el-descriptions-item>
          <el-descriptions-item label="运费">¥{{ quotation.shipping_fee?.toFixed(2) || '0.00' }}</el-descriptions-item>
          <el-descriptions-item label="备注" :span="3">{{ quotation.remarks || '无备注' }}</el-descriptions-item>
        </el-descriptions>
      </el-card>

      <!-- 内容选项卡 -->
      <el-tabs v-model="activeTab" class="content-tabs">
        <el-tab-pane label="报价项目" name="items">
          <el-card class="table-card">
            <template #header>
              <div class="card-header">
                <h3>报价项目</h3>
              </div>
            </template>
            <el-table
              :data="quotation.items || []"
              border
              style="width: 100%"
            >
              <el-table-column type="index" width="50" align="center" />
              <el-table-column prop="product_code" label="产品编码" min-width="120" />
              <el-table-column prop="product_name" label="产品名称" min-width="150" />
              <el-table-column prop="description" label="规格描述" min-width="200" show-overflow-tooltip />
              <el-table-column prop="quantity" label="数量" width="80" align="center" />
              <el-table-column prop="uom" label="单位" width="80" align="center" />
              <el-table-column prop="unit_price" label="单价" width="120" align="right">
                <template #default="scope">
                  ¥{{ scope.row.unit_price?.toFixed(2) }}
                </template>
              </el-table-column>
              <el-table-column prop="discount" label="折扣率" width="100" align="center">
                <template #default="scope">
                  {{ scope.row.discount ? (scope.row.discount * 100).toFixed(0) + '%' : '0%' }}
                </template>
              </el-table-column>
              <el-table-column prop="tax_rate" label="税率" width="80" align="center">
                <template #default="scope">
                  {{ scope.row.tax_rate ? (scope.row.tax_rate * 100).toFixed(0) + '%' : '0%' }}
                </template>
              </el-table-column>
              <el-table-column label="小计" width="120" align="right">
                <template #default="scope">
                  ¥{{ calculateItemTotal(scope.row).toFixed(2) }}
                </template>
              </el-table-column>
              <el-table-column label="操作" width="100" fixed="right">
                <template #default="scope">
                  <el-button
                    size="small"
                    type="primary"
                    @click="viewProduct(scope.row.product_id)"
                    text
                  >
                    <el-icon><View /></el-icon> 查看产品
                  </el-button>
                </template>
              </el-table-column>
            </el-table>

            <div class="summary-info">
              <div class="summary-item">
                <span class="label">产品总数:</span>
                <span class="value">{{ quotation.items?.length || 0 }}</span>
              </div>
              <div class="summary-item">
                <span class="label">产品总量:</span>
                <span class="value">{{ calculateTotalQuantity() }}</span>
              </div>
              <div class="summary-item cost-summary">
                <span class="label">小计:</span>
                <span class="value">¥{{ calculateSubtotal().toFixed(2) }}</span>
              </div>
              <div class="summary-item cost-summary">
                <span class="label">税额:</span>
                <span class="value">¥{{ calculateTax().toFixed(2) }}</span>
              </div>
              <div class="summary-item cost-summary">
                <span class="label">运费:</span>
                <span class="value">¥{{ quotation.shipping_fee?.toFixed(2) || '0.00' }}</span>
              </div>
              <div class="summary-item cost-summary total-cost">
                <span class="label">总计:</span>
                <span class="value cost-value">¥{{ calculateTotal().toFixed(2) }}</span>
              </div>
            </div>
          </el-card>
        </el-tab-pane>

        <el-tab-pane label="审批状态" name="approval">
          <el-card class="table-card">
            <template #header>
              <div class="card-header">
                <h3>审批流程</h3>
              </div>
            </template>
            <el-steps 
              :active="getApprovalStepIndex()" 
              finish-status="success"
              process-status="process"
              align-center
            >
              <el-step title="创建" :description="formatApprovalTime('created')" />
              <el-step title="提交审批" :description="formatApprovalTime('submitted')" />
              <el-step 
                title="审批" 
                :status="quotation.status === 'rejected' ? 'error' : ''"
                :description="formatApprovalTime(quotation.status === 'rejected' ? 'rejected' : 'approved')" 
              />
              <el-step title="确认" :description="formatApprovalTime('confirmed')" />
            </el-steps>

            <div v-if="quotation.status === 'draft'" class="approval-actions">
              <el-button type="primary" @click="submitForApproval">
                <el-icon><Top /></el-icon> 提交审批
              </el-button>
            </div>

            <div v-if="quotation.status === 'submitted' && isApprover" class="approval-actions">
              <el-input
                v-model="approvalRemarks"
                placeholder="审批意见"
                type="textarea"
                rows="2"
                class="approval-remarks"
              />
              <div class="approval-buttons">
                <el-button type="success" @click="approveQuotation">
                  <el-icon><Check /></el-icon> 批准
                </el-button>
                <el-button type="danger" @click="rejectQuotation">
                  <el-icon><Close /></el-icon> 拒绝
                </el-button>
              </div>
            </div>

            <el-empty v-if="!quotation.approval_history?.length" description="暂无审批记录" />
            <el-timeline v-else>
              <el-timeline-item
                v-for="(history, index) in quotation.approval_history"
                :key="index"
                :timestamp="history.time"
                :type="getTimelineItemType(history.action)"
                :color="getTimelineItemColor(history.action)"
              >
                <h4>{{ getActionText(history.action) }}</h4>
                <p>{{ history.remarks || '无备注' }}</p>
                <p>操作人: {{ history.user }}</p>
              </el-timeline-item>
            </el-timeline>
          </el-card>
        </el-tab-pane>

        <el-tab-pane label="操作日志" name="logs">
          <el-card class="table-card">
            <template #header>
              <div class="card-header">
                <h3>操作日志</h3>
              </div>
            </template>
            <el-table
              :data="quotation.logs || []"
              border
              style="width: 100%"
            >
              <el-table-column prop="time" label="时间" width="180" />
              <el-table-column prop="action" label="操作" width="150">
                <template #default="scope">
                  <el-tag :type="getActionTagType(scope.row.action)">
                    {{ getActionText(scope.row.action) }}
                  </el-tag>
                </template>
              </el-table-column>
              <el-table-column prop="user" label="操作人" width="150" />
              <el-table-column prop="details" label="详情" min-width="250" show-overflow-tooltip />
            </el-table>
            <el-empty v-if="!quotation.logs?.length" description="暂无操作日志" />
          </el-card>
        </el-tab-pane>
      </el-tabs>
    </div>

    <!-- 转换为订单确认对话框 -->
    <el-dialog
      v-model="convertDialogVisible"
      title="转换为销售订单"
      width="600px"
    >
      <p>您确定要将此报价单转换为销售订单吗？</p>
      <p>报价单号: {{ quotation.code }}</p>
      <p>客户: {{ quotation.customer_name }}</p>
      <p>总金额: ¥{{ calculateTotal().toFixed(2) }}</p>
      
      <el-form :model="orderForm" label-width="120px">
        <el-form-item label="预计交付日期">
          <el-date-picker
            v-model="orderForm.expected_delivery_date"
            type="date"
            placeholder="选择日期"
            :disabled-date="disabledDate"
            style="width: 100%"
          />
        </el-form-item>
        <el-form-item label="备注">
          <el-input
            v-model="orderForm.remarks"
            type="textarea"
            rows="3"
            placeholder="订单备注"
          />
        </el-form-item>
      </el-form>
      
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="convertDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="confirmConvertToOrder" :loading="convertLoading">
            确认转换
          </el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { ElMessage, ElMessageBox } from 'element-plus';
import { useQuotationApi } from '@/api/sales/quotation';
import { useOrderApi } from '@/api/sales/order';
import { useCustomerApi } from '@/api/sales/customer';
import { useProductApi } from '@/api/technical/product';
import { useUserStore } from '@/stores/user';

// 路由和API
const route = useRoute();
const router = useRouter();
const quotationApi = useQuotationApi();
const orderApi = useOrderApi();
const customerApi = useCustomerApi();
const productApi = useProductApi();
const userStore = useUserStore();

// 数据
const quotation = ref({});
const loading = ref(false);
const activeTab = ref('items');
const isApprover = ref(false);
const approvalRemarks = ref('');
const convertDialogVisible = ref(false);
const convertLoading = ref(false);

// 创建订单表单
const orderForm = reactive({
  expected_delivery_date: null,
  remarks: ''
});

// 组件挂载时获取数据
onMounted(async () => {
  await fetchQuotationDetail();
  checkApprovalPermission();
});

// 获取报价单详情
async function fetchQuotationDetail() {
  const quotationId = route.params.id;
  if (!quotationId) {
    ElMessage.error('报价单ID不存在');
    router.push('/sales/quotations');
    return;
  }
  
  loading.value = true;
  try {
    const { data } = await quotationApi.getQuotationDetail(quotationId);
    quotation.value = data;
  } catch (error) {
    console.error('获取报价单详情失败:', error);
    ElMessage.error('获取报价单详情失败');
  } finally {
    loading.value = false;
  }
}

// 检查当前用户是否有审批权限
function checkApprovalPermission() {
  // 根据实际业务逻辑检查权限
  // 这里仅作示例，可根据用户角色或特定权限判断
  const userRoles = userStore.roles || [];
  isApprover.value = userRoles.includes('sales_manager') || userRoles.includes('admin');
}

// 计算每项的总价
function calculateItemTotal(item) {
  if (!item.unit_price || !item.quantity) return 0;
  
  const priceAfterDiscount = item.unit_price * (1 - (item.discount || 0));
  const amount = priceAfterDiscount * item.quantity;
  const tax = amount * (item.tax_rate || 0);
  
  return amount + tax;
}

// 计算产品总量
function calculateTotalQuantity() {
  if (!quotation.value.items || !quotation.value.items.length) return 0;
  
  return quotation.value.items.reduce((sum, item) => sum + (item.quantity || 0), 0);
}

// 计算小计金额
function calculateSubtotal() {
  if (!quotation.value.items || !quotation.value.items.length) return 0;
  
  return quotation.value.items.reduce((sum, item) => {
    const priceAfterDiscount = item.unit_price * (1 - (item.discount || 0));
    return sum + (priceAfterDiscount * item.quantity);
  }, 0);
}

// 计算税额
function calculateTax() {
  if (!quotation.value.items || !quotation.value.items.length) return 0;
  
  return quotation.value.items.reduce((sum, item) => {
    const priceAfterDiscount = item.unit_price * (1 - (item.discount || 0));
    const amount = priceAfterDiscount * item.quantity;
    return sum + (amount * (item.tax_rate || 0));
  }, 0);
}

// 计算总计金额
function calculateTotal() {
  const subtotal = calculateSubtotal();
  const tax = calculateTax();
  const shipping = quotation.value.shipping_fee || 0;
  
  return subtotal + tax + shipping;
}

// 返回上一页
function goBack() {
  router.go(-1);
}

// 编辑报价单
function handleEdit() {
  router.push(`/sales/quotations/edit/${quotation.value.id}`);
}

// 查看客户
function viewCustomer(customerId) {
  router.push(`/sales/customers/${customerId}`);
}

// 查看产品
function viewProduct(productId) {
  router.push(`/technical/products/${productId}`);
}

// 打印报价单
function printQuotation() {
  ElMessage.info('正在准备打印报价单...');
  window.print();
}

// 导出报价单
function handleExport(type) {
  ElMessage.success(`正在导出报价单为 ${type.toUpperCase()} 格式`);
  
  // 这里是导出功能的模拟实现
  // 实际项目中应调用后端API执行导出
  setTimeout(() => {
    const filename = `报价单_${quotation.value.code}_${new Date().getTime()}.${type}`;
    ElMessage.success(`导出成功: ${filename}`);
  }, 1500);
}

// 提交审批
async function submitForApproval() {
  try {
    await quotationApi.submitForApproval(quotation.value.id);
    ElMessage.success('提交审批成功');
    await fetchQuotationDetail();
  } catch (error) {
    console.error('提交审批失败:', error);
    ElMessage.error('提交审批失败');
  }
}

// 批准报价单
async function approveQuotation() {
  try {
    await quotationApi.approveQuotation(quotation.value.id, { remarks: approvalRemarks.value });
    ElMessage.success('批准成功');
    approvalRemarks.value = '';
    await fetchQuotationDetail();
  } catch (error) {
    console.error('批准失败:', error);
    ElMessage.error('批准失败');
  }
}

// 拒绝报价单
async function rejectQuotation() {
  try {
    await quotationApi.rejectQuotation(quotation.value.id, { remarks: approvalRemarks.value });
    ElMessage.success('已拒绝此报价单');
    approvalRemarks.value = '';
    await fetchQuotationDetail();
  } catch (error) {
    console.error('操作失败:', error);
    ElMessage.error('操作失败');
  }
}

// 转换为订单
function handleConvertToOrder() {
  // 设置默认预计交付日期为30天后
  const today = new Date();
  today.setDate(today.getDate() + 30);
  orderForm.expected_delivery_date = today;
  
  convertDialogVisible.value = true;
}

// 确认转换为订单
async function confirmConvertToOrder() {
  if (!orderForm.expected_delivery_date) {
    ElMessage.warning('请选择预计交付日期');
    return;
  }
  
  convertLoading.value = true;
  try {
    const orderData = {
      quotation_id: quotation.value.id,
      expected_delivery_date: orderForm.expected_delivery_date,
      remarks: orderForm.remarks
    };
    
    const { data } = await orderApi.createOrderFromQuotation(orderData);
    
    ElMessage.success('转换为订单成功');
    convertDialogVisible.value = false;
    
    // 跳转到新创建的订单详情页
    router.push(`/sales/orders/${data.id}`);
  } catch (error) {
    console.error('转换为订单失败:', error);
    ElMessage.error('转换为订单失败');
  } finally {
    convertLoading.value = false;
  }
}

// 禁用过去的日期
function disabledDate(time) {
  return time.getTime() < Date.now() - 8.64e7; // 禁用昨天及之前的日期
}

// 格式化审批时间
function formatApprovalTime(step) {
  if (!quotation.value.approval_history) return '';
  
  const history = quotation.value.approval_history.find(h => h.action === step);
  return history ? history.time : '';
}

// 获取审批步骤索引
function getApprovalStepIndex() {
  const statusMap = {
    draft: 0,
    submitted: 1,
    approved: 2,
    rejected: 2,
    confirmed: 3
  };
  
  return statusMap[quotation.value.status] || 0;
}

// 获取状态标签类型
function getStatusType(status) {
  const statusMap = {
    draft: 'info',
    submitted: 'warning',
    approved: 'success',
    rejected: 'danger',
    confirmed: 'success',
    expired: 'info',
    converted: 'primary'
  };
  
  return statusMap[status] || 'info';
}

// 获取状态文本
function getStatusText(status) {
  const statusMap = {
    draft: '草稿',
    submitted: '审批中',
    approved: '已批准',
    rejected: '已拒绝',
    confirmed: '已确认',
    expired: '已过期',
    converted: '已转订单'
  };
  
  return statusMap[status] || '未知';
}

// 获取时间线项目类型
function getTimelineItemType(action) {
  const actionMap = {
    created: 'primary',
    submitted: 'warning',
    approved: 'success',
    rejected: 'danger',
    confirmed: 'success',
    modified: 'info',
    expired: 'info',
    converted: 'primary'
  };
  
  return actionMap[action] || 'info';
}

// 获取时间线项目颜色
function getTimelineItemColor(action) {
  const colorMap = {
    created: '#409EFF',
    submitted: '#E6A23C',
    approved: '#67C23A',
    rejected: '#F56C6C',
    confirmed: '#67C23A',
    modified: '#909399',
    expired: '#909399',
    converted: '#409EFF'
  };
  
  return colorMap[action] || '#909399';
}

// 获取操作标签类型
function getActionTagType(action) {
  const actionMap = {
    created: 'info',
    submitted: 'warning',
    approved: 'success',
    rejected: 'danger',
    confirmed: 'success',
    modified: 'info',
    exported: 'info',
    viewed: '',
    printed: 'info',
    expired: 'info',
    converted: 'primary'
  };
  
  return actionMap[action] || '';
}

// 获取操作文本
function getActionText(action) {
  const actionMap = {
    created: '创建',
    submitted: '提交审批',
    approved: '批准',
    rejected: '拒绝',
    confirmed: '确认',
    modified: '修改',
    exported: '导出',
    viewed: '查看',
    printed: '打印',
    expired: '过期',
    converted: '转订单'
  };
  
  return actionMap[action] || action;
}
</script>

<style scoped>
.quotation-detail-container {
  padding: 20px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.header-left {
  display: flex;
  align-items: center;
}

.page-title {
  margin: 0 10px;
  font-size: 24px;
  font-weight: 600;
  color: #303133;
}

.ml-5 {
  margin-left: 5px;
}

.ml-10 {
  margin-left: 10px;
}

.header-actions {
  display: flex;
  gap: 10px;
}

.info-card {
  margin-bottom: 20px;
}

.content-tabs {
  margin-top: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-header h3 {
  margin: 0;
  font-size: 18px;
  font-weight: 600;
  color: #303133;
}

.table-card {
  margin-bottom: 20px;
}

.summary-info {
  margin-top: 20px;
  display: flex;
  flex-wrap: wrap;
  justify-content: flex-end;
  align-items: center;
  padding: 15px;
  border-top: 1px solid #EBEEF5;
  gap: 20px;
}

.summary-item {
  display: flex;
  align-items: center;
}

.summary-item .label {
  color: #606266;
  margin-right: 5px;
}

.summary-item .value {
  font-weight: bold;
  color: #303133;
}

.cost-summary {
  margin-left: auto;
}

.total-cost {
  margin-left: 0;
}

.cost-value {
  font-size: 18px;
  color: #F56C6C;
}

.approval-actions {
  margin: 20px 0;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.approval-remarks {
  width: 500px;
  max-width: 100%;
  margin-bottom: 15px;
}

.approval-buttons {
  display: flex;
  gap: 20px;
}

@media print {
  .header-actions, .el-tabs__header, .page-header button {
    display: none;
  }
  
  .quotation-detail-container {
    padding: 0;
  }
  
  .info-card, .table-card {
    box-shadow: none;
    border: none;
  }
}
</style>
