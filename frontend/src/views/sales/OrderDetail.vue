<template>
  <div class="order-detail-container">
    <el-card>
      <template #header>
        <div class="card-header">
          <h2>{{ isEdit ? '编辑订单' : '新建订单' }}</h2>
          <div class="header-actions">
            <el-button type="primary" @click="saveOrder" :loading="loading">保存</el-button>
            <el-button @click="goBack">返回</el-button>
          </div>
        </div>
      </template>

      <el-form :model="orderForm" ref="orderFormRef" :rules="rules" label-width="120px" v-loading="loading">
        <!-- 基本信息 -->
        <el-divider content-position="left">基本信息</el-divider>
        <el-row :gutter="20">
          <el-col :span="8">
            <el-form-item label="订单编号" prop="order_number" v-if="isEdit">
              <el-input v-model="orderForm.order_number" disabled></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="订单日期" prop="order_date">
              <el-date-picker v-model="orderForm.order_date" type="date" placeholder="选择日期"></el-date-picker>
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="订单状态" prop="status" v-if="isEdit">
              <el-select v-model="orderForm.status" placeholder="请选择订单状态">
                <el-option label="草稿" value="draft"></el-option>
                <el-option label="已确认" value="confirmed"></el-option>
                <el-option label="处理中" value="processing"></el-option>
                <el-option label="已发货" value="shipped"></el-option>
                <el-option label="已完成" value="completed"></el-option>
                <el-option label="已取消" value="cancelled"></el-option>
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>

        <!-- 客户信息 -->
        <el-divider content-position="left">客户信息</el-divider>
        <el-row :gutter="20">
          <el-col :span="8">
            <el-form-item label="客户" prop="customer_id">
              <el-select 
                v-model="orderForm.customer_id" 
                placeholder="请选择客户" 
                filterable 
                remote 
                :remote-method="searchCustomers"
                :loading="loadingCustomers"
                @change="handleCustomerChange"
                clearable
                :reserve-keyword="true"
                :default-first-option="true">
                <el-option 
                  v-for="item in customerOptions" 
                  :key="item.id" 
                  :label="item.name" 
                  :value="item.id">
                  <div class="customer-option">
                    <span>{{ item.name }}</span>
                    <span v-if="item.code" class="option-code">({{ item.code }})</span>
                  </div>
                </el-option>
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="联系人" prop="contact_name">
              <el-input v-model="orderForm.contact_name"></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="联系电话" prop="contact_phone">
              <el-input v-model="orderForm.contact_phone"></el-input>
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="20">
          <el-col :span="16">
            <el-form-item label="送货地址" prop="shipping_address">
              <el-input v-model="orderForm.shipping_address" type="textarea" :rows="2"></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="送货方式" prop="shipping_method">
              <el-select v-model="orderForm.shipping_method" placeholder="请选择送货方式">
                <el-option label="快递" value="express"></el-option>
                <el-option label="物流" value="logistics"></el-option>
                <el-option label="自提" value="self_pickup"></el-option>
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>

        <!-- 订单项 -->
        <el-divider content-position="left">订单项目</el-divider>
        <div class="order-items">
          <el-table :data="orderItems" border style="width: 100%">
            <el-table-column label="序号" type="index" width="50"></el-table-column>
            <el-table-column label="产品" prop="product_name">
              <template #default="scope">
                <el-select v-model="scope.row.product_id" placeholder="选择产品" filterable @change="handleProductChange($event, scope.$index)" remote :remote-method="searchProducts" :loading="loadingProducts">
                  <el-option v-for="item in productOptions" :key="item.id" :label="item.name" :value="item.id"></el-option>
                </el-select>
              </template>
            </el-table-column>
            <el-table-column label="数量" width="150">
              <template #default="scope">
                <el-input-number v-model="scope.row.quantity" :min="1" @change="calculateItemTotal(scope.$index)"></el-input-number>
              </template>
            </el-table-column>
            <el-table-column label="单价" width="150">
              <template #default="scope">
                <el-input v-model.number="scope.row.unit_price" type="number" @input="calculateItemTotal(scope.$index)"></el-input>
              </template>
            </el-table-column>
            <el-table-column label="折扣率(%)" width="120">
              <template #default="scope">
                <el-input-number v-model="scope.row.discount_percent" :min="0" :max="100" @change="calculateItemTotal(scope.$index)"></el-input-number>
              </template>
            </el-table-column>
            <el-table-column label="小计" width="150">
              <template #default="scope">
                <span>{{ formatCurrency(scope.row.total_amount) }}</span>
              </template>
            </el-table-column>
            <el-table-column label="操作" width="120">
              <template #default="scope">
                <el-button type="danger" icon="Delete" circle @click="removeOrderItem(scope.$index)"></el-button>
              </template>
            </el-table-column>
          </el-table>
          <div class="add-item-btn">
            <el-button type="primary" @click="addOrderItem" icon="Plus">添加产品</el-button>
          </div>
        </div>

        <!-- 订单汇总 -->
        <el-divider content-position="left">订单汇总</el-divider>
        <el-row :gutter="20">
          <el-col :span="8">
            <el-form-item label="商品金额">
              <el-input v-model="orderSummary.subtotal" disabled></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="税费">
              <el-input v-model.number="orderForm.tax_amount" type="number" @input="calculateOrderTotal"></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="运费">
              <el-input v-model.number="orderForm.shipping_fee" type="number" @input="calculateOrderTotal"></el-input>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="8">
            <el-form-item label="其他费用">
              <el-input v-model.number="orderForm.other_fees" type="number" @input="calculateOrderTotal"></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="折扣金额">
              <el-input v-model.number="orderForm.discount_amount" type="number" @input="calculateOrderTotal"></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="订单总额">
              <el-input v-model="orderSummary.total" disabled></el-input>
            </el-form-item>
          </el-col>
        </el-row>

        <!-- 备注 -->
        <el-divider content-position="left">备注信息</el-divider>
        <el-form-item label="备注">
          <el-input v-model="orderForm.notes" type="textarea" :rows="3"></el-input>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive, computed, watch, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { ElMessage, ElMessageBox } from 'element-plus';
import { 
  getOrder, 
  createOrder, 
  updateOrder, 
  getOrderItems, 
  addOrderItem as apiAddOrderItem, 
  updateOrderItem,
  deleteOrderItem
} from '@/api/sales/order';
import { searchCustomers as searchCustomersApi } from '@/api/sales/customer';
import { searchProducts as searchProductsApi } from '@/api/technical/product';

// 路由信息
const route = useRoute();
const router = useRouter();
const orderId = computed(() => {
  const id = route.params.id;
  return id ? parseInt(id) : null;
});
const isEdit = computed(() => !!orderId.value);

// 加载状态
const loading = ref(false);
const loadingCustomers = ref(false);
const loadingProducts = ref(false);

// 表单引用
const orderFormRef = ref(null);

// 表单数据
const orderForm = reactive({
  order_date: new Date(),
  customer_id: undefined,
  contact_name: '',
  contact_phone: '',
  shipping_address: '',
  shipping_method: 'express',
  tax_amount: 0,
  shipping_fee: 0,
  other_fees: 0,
  discount_amount: 0,
  notes: '',
  status: 'draft'
});

// 表单验证规则
const rules = {
  customer_id: [{ required: true, message: '请选择客户', trigger: 'change' }],
  order_date: [{ required: true, message: '请选择订单日期', trigger: 'change' }],
  shipping_method: [{ required: true, message: '请选择送货方式', trigger: 'change' }]
};

// 订单项列表
const orderItems = ref([]);
const defaultOrderItem = {
  product_id: null,
  product_name: '',
  quantity: 1,
  unit_price: 0,
  discount_percent: 0,
  total_amount: 0
};

// 订单汇总
const orderSummary = reactive({
  subtotal: '0.00',
  total: '0.00'
});

// 下拉选项
const customerOptions = ref([]);
const productOptions = ref([]);

// 格式化货币
const formatCurrency = (value) => {
  return new Intl.NumberFormat('zh-CN', { style: 'currency', currency: 'CNY' }).format(value || 0);
};

// 搜索客户
const searchCustomers = async (query) => {
  if (!query) {
    customerOptions.value = [];
    return;
  }

  loadingCustomers.value = true;
  try {
    const response = await searchCustomersApi({ query });
    // 确保response.data存在，否则使用空数组
    const customers = response?.data?.items || response?.items || response || [];
    customerOptions.value = customers.map(customer => ({
      id: customer.id,
      name: customer.name,
      code: customer.code,
      contact_person: customer.contact_person,
      phone: customer.phone,
      address: customer.address
    }));
  } catch (error) {
    console.error('搜索客户失败:', error);
    ElMessage.error('搜索客户失败');
    customerOptions.value = [];
  } finally {
    loadingCustomers.value = false;
  }
};

// 搜索产品
const searchProducts = async (query) => {
  if (query) {
    loadingProducts.value = true;
    try {
      const response = await searchProductsApi({ query });
      productOptions.value = response;
    } catch (error) {
      console.error('搜索产品失败:', error);
      ElMessage.error('搜索产品失败');
    } finally {
      loadingProducts.value = false;
    }
  } else {
    productOptions.value = [];
  }
};

// 添加订单项
const addOrderItem = () => {
  orderItems.value.push({ ...defaultOrderItem });
};

// 移除订单项
const removeOrderItem = (index) => {
  orderItems.value.splice(index, 1);
  calculateOrderTotal();
};

// 产品选择变更
const handleProductChange = (productId, index) => {
  const product = productOptions.value.find(p => p.id === productId);
  if (product) {
    orderItems.value[index].product_name = product.name;
    orderItems.value[index].unit_price = product.price || 0;
    calculateItemTotal(index);
  }
};

// 计算订单项总额
const calculateItemTotal = (index) => {
  const item = orderItems.value[index];
  const discount = 1 - (item.discount_percent || 0) / 100;
  item.total_amount = (item.quantity || 0) * (item.unit_price || 0) * discount;
  calculateOrderTotal();
};

// 计算订单总额
const calculateOrderTotal = () => {
  const subtotal = orderItems.value.reduce((sum, item) => sum + (item.total_amount || 0), 0);
  orderSummary.subtotal = formatCurrency(subtotal);
  
  const totalAmount = subtotal + 
    (orderForm.tax_amount || 0) + 
    (orderForm.shipping_fee || 0) + 
    (orderForm.other_fees || 0) - 
    (orderForm.discount_amount || 0);
  
  orderSummary.total = formatCurrency(totalAmount);
  orderForm.total_amount = totalAmount;
};

// 返回列表
const goBack = () => {
  router.push('/sales/orders');
};

// 保存订单
const saveOrder = async () => {
  await orderFormRef.value.validate(async (valid) => {
    if (!valid) {
      ElMessage.error('请填写必填项');
      return;
    }
    
    if (orderItems.value.length === 0) {
      ElMessage.error('请至少添加一个订单项');
      return;
    }
    
    for (const item of orderItems.value) {
      if (!item.product_id) {
        ElMessage.error('请为所有订单项选择产品');
        return;
      }
    }
    
    loading.value = true;
    
    try {
      // 准备提交的数据
      const formData = {
        ...orderForm,
        order_items: orderItems.value.map(item => ({
          product_id: item.product_id,
          quantity: item.quantity,
          unit_price: item.unit_price,
          discount_percent: item.discount_percent,
          total_amount: item.total_amount
        }))
      };
      
      let response;
      if (isEdit.value) {
        // 更新订单
        response = await updateOrder(orderId.value, formData);
        ElMessage.success('订单更新成功');
      } else {
        // 创建订单
        response = await createOrder(formData);
        ElMessage.success('订单创建成功');
      }
      
      // 导航到订单列表
      router.push('/sales/orders');
    } catch (error) {
      console.error('保存订单失败', error);
      ElMessage.error('保存订单失败: ' + (error.message || '未知错误'));
    } finally {
      loading.value = false;
    }
  });
};

// 加载订单数据
const loadOrderData = async () => {
  loading.value = true;
  try {
    const response = await getOrder(orderId.value);
    Object.assign(orderForm, response);
    if (response.items) {
      orderItems.value = response.items;
    }
    calculateOrderTotal();
  } catch (error) {
    console.error('加载订单数据失败:', error);
    ElMessage.error('加载订单数据失败');
  } finally {
    loading.value = false;
  }
};

// 客户选择变更处理
const handleCustomerChange = (customerId) => {
  if (!customerId) {
    orderForm.contact_name = '';
    orderForm.contact_phone = '';
    orderForm.shipping_address = '';
    return;
  }

  const customer = customerOptions.value.find(c => c.id === customerId);
  if (customer) {
    orderForm.contact_name = customer.contact_person || '';
    orderForm.contact_phone = customer.phone || '';
    orderForm.shipping_address = customer.address || '';
  }
};

// 初始化数据
onMounted(async () => {
  if (isEdit.value) {
    await loadOrderData();
  }
});
</script>

<style scoped>
.order-detail-container {
  padding: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-actions {
  display: flex;
  gap: 10px;
}

.add-item-btn {
  margin-top: 15px;
  text-align: center;
}

.order-items {
  margin-bottom: 20px;
}

.el-divider {
  margin: 24px 0;
}

.customer-option {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.option-code {
  color: #909399;
  font-size: 13px;
  margin-left: 8px;
}
</style>