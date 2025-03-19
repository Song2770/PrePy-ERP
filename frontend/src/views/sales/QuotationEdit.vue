<template>
  <div class="quotation-edit">
    <div class="header">
      <h1>{{ isEdit ? '编辑报价单' : '新建报价单' }}</h1>
      <el-button-group>
        <el-button @click="handleCancel">取消</el-button>
        <el-button type="primary" @click="handleSave">保存</el-button>
        <el-button type="success" @click="handleSubmit">提交</el-button>
      </el-button-group>
    </div>

    <el-form ref="formRef" :model="form" :rules="rules" label-width="120px">
      <!-- 基本信息 -->
      <el-card class="form-card">
        <template #header>
          <div class="card-header">
            <span>基本信息</span>
          </div>
        </template>
        
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="客户" prop="customer_id">
              <el-select
                v-model="form.customer_id"
                filterable
                remote
                :remote-method="searchCustomers"
                :loading="customerLoading"
                placeholder="请选择客户"
                @change="handleCustomerChange"
              >
                <el-option
                  v-for="item in customers"
                  :key="item.id"
                  :label="item.name"
                  :value="item.id"
                />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="联系人" prop="contact_id">
              <el-select
                v-model="form.contact_id"
                filterable
                placeholder="请选择联系人"
                :disabled="!form.customer_id"
              >
                <el-option
                  v-for="item in contacts"
                  :key="item.id"
                  :label="item.name"
                  :value="item.id"
                />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="报价单号" prop="quotation_number">
              <el-input v-model="form.quotation_number" placeholder="请输入报价单号" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="主题" prop="subject">
              <el-input v-model="form.subject" placeholder="请输入主题" />
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="报价日期" prop="quotation_date">
              <el-date-picker
                v-model="form.quotation_date"
                type="date"
                placeholder="选择日期"
                format="YYYY-MM-DD"
                value-format="YYYY-MM-DD"
              />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="有效期至" prop="valid_until">
              <el-date-picker
                v-model="form.valid_until"
                type="date"
                placeholder="选择日期"
                format="YYYY-MM-DD"
                value-format="YYYY-MM-DD"
              />
            </el-form-item>
          </el-col>
        </el-row>
      </el-card>

      <!-- 报价明细 -->
      <el-card class="form-card">
        <template #header>
          <div class="card-header">
            <span>报价明细</span>
            <el-button type="primary" @click="handleAddItem">添加明细</el-button>
          </div>
        </template>

        <el-table :data="form.items" border>
          <el-table-column label="产品" width="300">
            <template #default="scope">
              <el-select
                v-model="scope.row.product_id"
                filterable
                remote
                :remote-method="searchProducts"
                :loading="productLoading"
                placeholder="请选择产品"
                @change="(val) => handleProductChange(val, scope.$index)"
              >
                <el-option
                  v-for="item in products"
                  :key="item.id"
                  :label="item.name"
                  :value="item.id"
                />
              </el-select>
            </template>
          </el-table-column>
          <el-table-column label="描述" width="300">
            <template #default="scope">
              <el-input v-model="scope.row.description" placeholder="请输入描述" />
            </template>
          </el-table-column>
          <el-table-column label="数量" width="120">
            <template #default="scope">
              <el-input-number
                v-model="scope.row.quantity"
                :min="0"
                :precision="2"
                @change="(val) => calculateItemTotal(val, scope.$index)"
              />
            </template>
          </el-table-column>
          <el-table-column label="单位" width="120">
            <template #default="scope">
              <el-input v-model="scope.row.unit" placeholder="单位" />
            </template>
          </el-table-column>
          <el-table-column label="单价" width="120">
            <template #default="scope">
              <el-input-number
                v-model="scope.row.unit_price"
                :min="0"
                :precision="2"
                @change="(val) => calculateItemTotal(val, scope.$index)"
              />
            </template>
          </el-table-column>
          <el-table-column label="税率" width="120">
            <template #default="scope">
              <el-input-number
                v-model="scope.row.tax_rate"
                :min="0"
                :max="100"
                :precision="2"
                @change="(val) => calculateItemTotal(val, scope.$index)"
              />
            </template>
          </el-table-column>
          <el-table-column label="折扣" width="120">
            <template #default="scope">
              <el-input-number
                v-model="scope.row.discount_percent"
                :min="0"
                :max="100"
                :precision="2"
                @change="(val) => calculateItemTotal(val, scope.$index)"
              />
            </template>
          </el-table-column>
          <el-table-column label="金额" width="120">
            <template #default="scope">
              {{ formatCurrency(scope.row.total_price) }}
            </template>
          </el-table-column>
          <el-table-column label="操作" width="100">
            <template #default="scope">
              <el-button
                type="danger"
                size="small"
                @click="handleRemoveItem(scope.$index)"
              >
                删除
              </el-button>
            </template>
          </el-table-column>
        </el-table>
      </el-card>

      <!-- 其他信息 -->
      <el-card class="form-card">
        <template #header>
          <div class="card-header">
            <span>其他信息</span>
          </div>
        </template>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="付款条件" prop="payment_terms">
              <el-input
                v-model="form.payment_terms"
                type="textarea"
                :rows="3"
                placeholder="请输入付款条件"
              />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="交货条件" prop="delivery_terms">
              <el-input
                v-model="form.delivery_terms"
                type="textarea"
                :rows="3"
                placeholder="请输入交货条件"
              />
            </el-form-item>
          </el-col>
        </el-row>

        <el-form-item label="备注" prop="notes">
          <el-input
            v-model="form.notes"
            type="textarea"
            :rows="3"
            placeholder="请输入备注"
          />
        </el-form-item>

        <el-form-item label="条款和条件" prop="terms_and_conditions">
          <el-input
            v-model="form.terms_and_conditions"
            type="textarea"
            :rows="3"
            placeholder="请输入条款和条件"
          />
        </el-form-item>
      </el-card>

      <!-- 合计信息 -->
      <el-card class="form-card">
        <template #header>
          <div class="card-header">
            <span>合计信息</span>
          </div>
        </template>

        <el-row :gutter="20">
          <el-col :span="8">
            <div class="total-item">
              <span class="label">总金额：</span>
              <span class="value">{{ formatCurrency(form.total_amount) }}</span>
            </div>
          </el-col>
          <el-col :span="8">
            <div class="total-item">
              <span class="label">税额：</span>
              <span class="value">{{ formatCurrency(form.tax_amount) }}</span>
            </div>
          </el-col>
          <el-col :span="8">
            <div class="total-item">
              <span class="label">折扣：</span>
              <span class="value">{{ formatCurrency(form.discount_amount) }}</span>
            </div>
          </el-col>
        </el-row>
        <el-row>
          <el-col :span="24">
            <div class="total-item grand-total">
              <span class="label">总计：</span>
              <span class="value">{{ formatCurrency(form.grand_total) }}</span>
            </div>
          </el-col>
        </el-row>
      </el-card>
    </el-form>
  </div>
</template>

<script>
import { defineComponent, ref, computed, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { ElMessage } from 'element-plus';
import { formatCurrency } from '@/utils/format';
import {
  getQuotation,
  createQuotation,
  updateQuotation,
  getCustomers,
  getCustomerContacts,
  getProducts
} from '@/api/sales';

export default defineComponent({
  name: 'QuotationEdit',
  setup() {
    const route = useRoute();
    const router = useRouter();
    const formRef = ref(null);
    const isEdit = computed(() => route.params.id);

    // 表单数据
    const form = ref({
      customer_id: null,
      contact_id: null,
      quotation_number: '',
      subject: '',
      quotation_date: '',
      valid_until: '',
      items: [],
      payment_terms: '',
      delivery_terms: '',
      notes: '',
      terms_and_conditions: '',
      total_amount: 0,
      tax_amount: 0,
      discount_amount: 0,
      grand_total: 0,
      currency: 'CNY'
    });

    // 表单验证规则
    const rules = {
      customer_id: [{ required: true, message: '请选择客户', trigger: 'change' }],
      quotation_number: [{ required: true, message: '请输入报价单号', trigger: 'blur' }],
      subject: [{ required: true, message: '请输入主题', trigger: 'blur' }],
      quotation_date: [{ required: true, message: '请选择报价日期', trigger: 'change' }]
    };

    // 客户和联系人数据
    const customers = ref([]);
    const contacts = ref([]);
    const customerLoading = ref(false);

    // 产品数据
    const products = ref([]);
    const productLoading = ref(false);

    // 获取客户列表
    const searchCustomers = async (query) => {
      if (query) {
        customerLoading.value = true;
        try {
          const response = await getCustomers({ search: query });
          customers.value = response.data;
        } catch (error) {
          ElMessage.error('获取客户列表失败');
        } finally {
          customerLoading.value = false;
        }
      }
    };

    // 获取联系人列表
    const getContacts = async (customerId) => {
      try {
        const response = await getCustomerContacts(customerId);
        contacts.value = response.data;
        form.value.contact_id = null;
      } catch (error) {
        ElMessage.error('获取联系人列表失败');
      }
    };

    // 客户变更处理
    const handleCustomerChange = (customerId) => {
      if (customerId) {
        getContacts(customerId);
      } else {
        contacts.value = [];
        form.value.contact_id = null;
      }
    };

    // 获取产品列表
    const searchProducts = async (query) => {
      if (query) {
        productLoading.value = true;
        try {
          const response = await getProducts({ search: query });
          products.value = response.data;
        } catch (error) {
          ElMessage.error('获取产品列表失败');
        } finally {
          productLoading.value = false;
        }
      }
    };

    // 添加明细行
    const handleAddItem = () => {
      form.value.items.push({
        product_id: null,
        description: '',
        quantity: 1,
        unit: '',
        unit_price: 0,
        tax_rate: 0,
        discount_percent: 0,
        total_price: 0
      });
    };

    // 删除明细行
    const handleRemoveItem = (index) => {
      form.value.items.splice(index, 1);
      calculateTotals();
    };

    // 产品变更处理
    const handleProductChange = (productId, index) => {
      const product = products.value.find(p => p.id === productId);
      if (product) {
        form.value.items[index].unit = product.unit || '';
        form.value.items[index].unit_price = product.price || 0;
        calculateItemTotal(form.value.items[index].quantity, index);
      }
    };

    // 计算明细行总金额
    const calculateItemTotal = (value, index) => {
      const item = form.value.items[index];
      const quantity = item.quantity || 0;
      const unitPrice = item.unit_price || 0;
      const taxRate = item.tax_rate || 0;
      const discountPercent = item.discount_percent || 0;

      const subtotal = quantity * unitPrice;
      const discount = subtotal * (discountPercent / 100);
      const afterDiscount = subtotal - discount;
      const tax = afterDiscount * (taxRate / 100);

      item.total_price = afterDiscount + tax;
      calculateTotals();
    };

    // 计算合计金额
    const calculateTotals = () => {
      let totalAmount = 0;
      let taxAmount = 0;
      let discountAmount = 0;

      form.value.items.forEach(item => {
        const quantity = item.quantity || 0;
        const unitPrice = item.unit_price || 0;
        const taxRate = item.tax_rate || 0;
        const discountPercent = item.discount_percent || 0;

        const subtotal = quantity * unitPrice;
        const discount = subtotal * (discountPercent / 100);
        const afterDiscount = subtotal - discount;
        const tax = afterDiscount * (taxRate / 100);

        totalAmount += subtotal;
        taxAmount += tax;
        discountAmount += discount;
      });

      form.value.total_amount = totalAmount;
      form.value.tax_amount = taxAmount;
      form.value.discount_amount = discountAmount;
      form.value.grand_total = totalAmount - discountAmount + taxAmount;
    };

    // 获取报价单详情
    const getQuotationDetail = async (id) => {
      try {
        const response = await getQuotation(id);
        form.value = response.data;
      } catch (error) {
        ElMessage.error('获取报价单详情失败');
      }
    };

    // 保存报价单
    const handleSave = async () => {
      if (!formRef.value) return;
      
      try {
        await formRef.value.validate();
        if (isEdit.value) {
          await updateQuotation(route.params.id, form.value);
          ElMessage.success('更新成功');
        } else {
          await createQuotation(form.value);
          ElMessage.success('创建成功');
        }
        router.push('/sales/quotations');
      } catch (error) {
        ElMessage.error('保存失败');
      }
    };

    // 提交报价单
    const handleSubmit = async () => {
      if (!formRef.value) return;
      
      try {
        await formRef.value.validate();
        form.value.status = 'sent';
        if (isEdit.value) {
          await updateQuotation(route.params.id, form.value);
          ElMessage.success('提交成功');
        } else {
          await createQuotation(form.value);
          ElMessage.success('提交成功');
        }
        router.push('/sales/quotations');
      } catch (error) {
        ElMessage.error('提交失败');
      }
    };

    // 取消
    const handleCancel = () => {
      router.back();
    };

    onMounted(() => {
      if (isEdit.value) {
        getQuotationDetail(route.params.id);
      }
    });

    return {
      formRef,
      form,
      rules,
      isEdit,
      customers,
      contacts,
      products,
      customerLoading,
      productLoading,
      searchCustomers,
      handleCustomerChange,
      searchProducts,
      handleAddItem,
      handleRemoveItem,
      handleProductChange,
      calculateItemTotal,
      formatCurrency,
      handleSave,
      handleSubmit,
      handleCancel
    };
  }
});
</script>

<style scoped>
.quotation-edit {
  padding: 20px;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.form-card {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.total-item {
  display: flex;
  justify-content: flex-end;
  align-items: center;
  margin-bottom: 10px;
}

.total-item .label {
  margin-right: 10px;
  font-weight: bold;
}

.total-item .value {
  font-size: 16px;
  color: #409EFF;
}

.grand-total {
  margin-top: 20px;
  padding-top: 20px;
  border-top: 1px solid #EBEEF5;
}

.grand-total .label {
  font-size: 18px;
}

.grand-total .value {
  font-size: 24px;
  color: #F56C6C;
}
</style> 