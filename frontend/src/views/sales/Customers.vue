<template>
  <div class="customers-page page-container">
    <div class="page-header">
      <h1 class="page-title">客户管理</h1>
      <el-button type="primary" @click="showAddCustomerDialog">
        <el-icon><Plus /></el-icon>
        添加客户
      </el-button>
    </div>

    <!-- Search & Filters -->
    <el-card class="table-operations">
      <el-row :gutter="20">
        <el-col :xs="24" :sm="8">
          <el-input
            v-model="searchQuery"
            placeholder="搜索客户名称、代码或联系人"
            clearable
            @input="handleSearch"
          >
            <template #prefix>
              <el-icon><Search /></el-icon>
            </template>
          </el-input>
        </el-col>
        <el-col :xs="24" :sm="8">
          <el-select
            v-model="filterStatus"
            placeholder="客户状态"
            clearable
            style="width: 100%"
            @change="handleFilter"
          >
            <el-option label="全部" value="" />
            <el-option label="活跃" value="true" />
            <el-option label="非活跃" value="false" />
          </el-select>
        </el-col>
        <el-col :xs="24" :sm="8">
          <el-button type="primary" plain @click="handleFilter">
            <el-icon><Filter /></el-icon>
            筛选
          </el-button>
          <el-button @click="resetFilter">
            <el-icon><Refresh /></el-icon>
            重置
          </el-button>
        </el-col>
      </el-row>
    </el-card>

    <!-- Customers Table -->
    <el-card>
      <el-table
        v-loading="loading"
        :data="customers"
        border
        style="width: 100%"
        @row-click="handleRowClick"
      >
        <el-table-column prop="code" label="客户代码" min-width="120" />
        <el-table-column prop="name" label="客户名称" min-width="200" />
        <el-table-column prop="contact_person" label="联系人" min-width="150" />
        <el-table-column prop="phone" label="电话" min-width="150" />
        <el-table-column prop="city" label="城市" min-width="120" />
        <el-table-column label="状态" width="100">
          <template #default="scope">
            <el-tag :type="scope.row.is_active ? 'success' : 'info'">
              {{ scope.row.is_active ? '活跃' : '非活跃' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200" fixed="right">
          <template #default="scope">
            <el-button
              size="small"
              type="primary"
              @click.stop="handleEdit(scope.row)"
            >
              编辑
            </el-button>
            <el-button
              size="small"
              type="danger"
              @click.stop="handleDelete(scope.row)"
            >
              删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <!-- Pagination -->
      <div class="pagination">
        <el-pagination
          v-model:currentPage="currentPage"
          v-model:page-size="pageSize"
          :page-sizes="[10, 20, 50, 100]"
          layout="total, sizes, prev, pager, next, jumper"
          :total="totalCustomers"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        />
      </div>
    </el-card>

    <!-- Add/Edit Customer Dialog -->
    <el-dialog
      v-model="dialogVisible"
      :title="editMode ? '编辑客户' : '添加客户'"
      width="600px"
    >
      <el-form
        ref="customerForm"
        :model="customerForm"
        :rules="customerRules"
        label-width="100px"
        label-position="right"
      >
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="客户代码" prop="code">
              <el-input v-model="customerForm.code" placeholder="请输入客户代码" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="客户名称" prop="name">
              <el-input v-model="customerForm.name" placeholder="请输入客户名称" />
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="联系人" prop="contact_person">
              <el-input v-model="customerForm.contact_person" placeholder="请输入联系人" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="电话" prop="phone">
              <el-input v-model="customerForm.phone" placeholder="请输入电话" />
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="邮箱" prop="email">
              <el-input v-model="customerForm.email" placeholder="请输入邮箱" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="税号" prop="tax_id">
              <el-input v-model="customerForm.tax_id" placeholder="请输入税号" />
            </el-form-item>
          </el-col>
        </el-row>

        <el-form-item label="地址" prop="address">
          <el-input v-model="customerForm.address" placeholder="请输入地址" />
        </el-form-item>

        <el-row :gutter="20">
          <el-col :span="8">
            <el-form-item label="城市" prop="city">
              <el-input v-model="customerForm.city" placeholder="请输入城市" />
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="省份/州" prop="state">
              <el-input v-model="customerForm.state" placeholder="请输入省份/州" />
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="邮编" prop="postal_code">
              <el-input v-model="customerForm.postal_code" placeholder="请输入邮编" />
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="国家" prop="country">
              <el-input v-model="customerForm.country" placeholder="请输入国家" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="行业" prop="industry">
              <el-input v-model="customerForm.industry" placeholder="请输入行业" />
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="客户类型" prop="customer_type">
              <el-select v-model="customerForm.customer_type" placeholder="请选择客户类型" style="width: 100%">
                <el-option label="个人" value="个人" />
                <el-option label="企业" value="企业" />
                <el-option label="政府" value="政府" />
                <el-option label="非营利组织" value="非营利组织" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="信用额度" prop="credit_limit">
              <el-input-number
                v-model="customerForm.credit_limit"
                :min="0"
                :precision="2"
                style="width: 100%"
              />
            </el-form-item>
          </el-col>
        </el-row>

        <el-form-item label="支付条款" prop="payment_terms">
          <el-input v-model="customerForm.payment_terms" placeholder="请输入支付条款" />
        </el-form-item>

        <el-form-item label="备注" prop="notes">
          <el-input
            v-model="customerForm.notes"
            type="textarea"
            :rows="3"
            placeholder="请输入备注"
          />
        </el-form-item>

        <el-form-item label="状态" prop="is_active">
          <el-switch
            v-model="customerForm.is_active"
            active-text="活跃"
            inactive-text="非活跃"
          />
        </el-form-item>
      </el-form>

      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="submitForm" :loading="submitting">
            {{ editMode ? '更新' : '添加' }}
          </el-button>
        </span>
      </template>
    </el-dialog>

    <!-- Customer Details Dialog -->
    <el-dialog v-model="detailsVisible" title="客户详情" width="700px">
      <el-descriptions
        v-if="selectedCustomer"
        :column="2"
        border
      >
        <el-descriptions-item label="客户代码">{{ selectedCustomer.code }}</el-descriptions-item>
        <el-descriptions-item label="客户名称">{{ selectedCustomer.name }}</el-descriptions-item>
        <el-descriptions-item label="联系人">{{ selectedCustomer.contact_person }}</el-descriptions-item>
        <el-descriptions-item label="电话">{{ selectedCustomer.phone }}</el-descriptions-item>
        <el-descriptions-item label="邮箱">{{ selectedCustomer.email }}</el-descriptions-item>
        <el-descriptions-item label="税号">{{ selectedCustomer.tax_id }}</el-descriptions-item>
        <el-descriptions-item label="地址" :span="2">{{ selectedCustomer.address }}</el-descriptions-item>
        <el-descriptions-item label="城市">{{ selectedCustomer.city }}</el-descriptions-item>
        <el-descriptions-item label="省份/州">{{ selectedCustomer.state }}</el-descriptions-item>
        <el-descriptions-item label="国家">{{ selectedCustomer.country }}</el-descriptions-item>
        <el-descriptions-item label="邮编">{{ selectedCustomer.postal_code }}</el-descriptions-item>
        <el-descriptions-item label="行业">{{ selectedCustomer.industry }}</el-descriptions-item>
        <el-descriptions-item label="客户类型">{{ selectedCustomer.customer_type }}</el-descriptions-item>
        <el-descriptions-item label="信用额度">{{ selectedCustomer.credit_limit }}</el-descriptions-item>
        <el-descriptions-item label="支付条款">{{ selectedCustomer.payment_terms }}</el-descriptions-item>
        <el-descriptions-item label="状态">
          <el-tag :type="selectedCustomer.is_active ? 'success' : 'info'">
            {{ selectedCustomer.is_active ? '活跃' : '非活跃' }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="创建时间">
          {{ new Date(selectedCustomer.created_at).toLocaleString() }}
        </el-descriptions-item>
        <el-descriptions-item label="备注" :span="2">{{ selectedCustomer.notes }}</el-descriptions-item>
      </el-descriptions>

      <template #footer>
        <span class="dialog-footer">
          <el-button @click="detailsVisible = false">关闭</el-button>
          <el-button type="primary" @click="handleEdit(selectedCustomer)">编辑</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import { defineComponent, ref, reactive, onMounted, computed } from 'vue';
import { ElMessage, ElMessageBox } from 'element-plus';
import { fetchCustomers, createCustomer, updateCustomer, deleteCustomer } from '@/api/sales';

export default defineComponent({
  name: 'CustomersPage',
  setup() {
    // State
    const loading = ref(false);
    const submitting = ref(false);
    const customers = ref([]);
    const totalCustomers = ref(0);
    const currentPage = ref(1);
    const pageSize = ref(10);
    const searchQuery = ref('');
    const filterStatus = ref('');
    const dialogVisible = ref(false);
    const detailsVisible = ref(false);
    const editMode = ref(false);
    const selectedCustomer = ref(null);
    const customerForm = ref(null);

    // Form default values and rules
    const form = reactive({
      code: '',
      name: '',
      contact_person: '',
      phone: '',
      email: '',
      address: '',
      city: '',
      state: '',
      country: '',
      postal_code: '',
      tax_id: '',
      industry: '',
      customer_type: '',
      credit_limit: 0,
      payment_terms: '',
      notes: '',
      is_active: true
    });

    const customerRules = {
      code: [
        { required: true, message: '请输入客户代码', trigger: 'blur' },
        { min: 3, max: 20, message: '长度在 3 到 20 个字符', trigger: 'blur' }
      ],
      name: [
        { required: true, message: '请输入客户名称', trigger: 'blur' },
        { min: 2, max: 100, message: '长度在 2 到 100 个字符', trigger: 'blur' }
      ],
      email: [
        { type: 'email', message: '请输入正确的邮箱地址', trigger: 'blur' }
      ]
    };

    // Methods
    const loadCustomers = async () => {
      loading.value = true;
      try {
        const params = {
          skip: (currentPage.value - 1) * pageSize.value,
          limit: pageSize.value,
          search: searchQuery.value,
          is_active: filterStatus.value
        };
        
        // In a real app, we would call the API
        // const response = await fetchCustomers(params);
        // customers.value = response;
        // totalCustomers.value = response.total;
        
        // For demo purposes, use dummy data
        customers.value = [
          {
            id: 1,
            code: 'CUST001',
            name: 'ABC Electronics',
            contact_person: 'John Smith',
            phone: '1234567890',
            email: 'john@abcelectronics.com',
            address: '123 Main St',
            city: 'Shanghai',
            state: '',
            country: 'China',
            postal_code: '200000',
            tax_id: 'TAX123456',
            industry: 'Electronics',
            customer_type: '企业',
            credit_limit: 100000,
            payment_terms: '30 days',
            notes: 'Important customer',
            is_active: true,
            created_at: '2023-01-15T08:30:00Z',
            updated_at: '2023-01-15T08:30:00Z'
          },
          {
            id: 2,
            code: 'CUST002',
            name: 'XYZ Manufacturing',
            contact_person: 'Jane Doe',
            phone: '9876543210',
            email: 'jane@xyzmanufacturing.com',
            address: '456 Broad St',
            city: 'Beijing',
            state: '',
            country: 'China',
            postal_code: '100000',
            tax_id: 'TAX654321',
            industry: 'Manufacturing',
            customer_type: '企业',
            credit_limit: 200000,
            payment_terms: '45 days',
            notes: 'Long-term partner',
            is_active: true,
            created_at: '2023-02-20T10:15:00Z',
            updated_at: '2023-02-20T10:15:00Z'
          }
        ];
        totalCustomers.value = 2;
      } catch (error) {
        console.error('Error loading customers:', error);
        ElMessage.error('加载客户数据失败');
      } finally {
        loading.value = false;
      }
    };

    const handleSearch = () => {
      currentPage.value = 1;
      loadCustomers();
    };

    const handleFilter = () => {
      currentPage.value = 1;
      loadCustomers();
    };

    const resetFilter = () => {
      searchQuery.value = '';
      filterStatus.value = '';
      currentPage.value = 1;
      loadCustomers();
    };

    const handleSizeChange = (val) => {
      pageSize.value = val;
      loadCustomers();
    };

    const handleCurrentChange = (val) => {
      currentPage.value = val;
      loadCustomers();
    };

    const resetForm = () => {
      Object.keys(form).forEach(key => {
        form[key] = '';
      });
      form.credit_limit = 0;
      form.is_active = true;
    };

    const showAddCustomerDialog = () => {
      resetForm();
      editMode.value = false;
      dialogVisible.value = true;
    };

    const handleRowClick = (row) => {
      selectedCustomer.value = row;
      detailsVisible.value = true;
    };

    const handleEdit = (customer) => {
      editMode.value = true;
      Object.keys(form).forEach(key => {
        form[key] = customer[key];
      });
      dialogVisible.value = true;
      detailsVisible.value = false;
    };

    const handleDelete = (customer) => {
      ElMessageBox.confirm(
        `确定要删除客户 "${customer.name}" 吗?`,
        '警告',
        {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning',
        }
      ).then(async () => {
        try {
          // In a real app, we would call the API
          // await deleteCustomer(customer.id);
          
          ElMessage.success('删除成功');
          loadCustomers();
        } catch (error) {
          console.error('Error deleting customer:', error);
          ElMessage.error('删除失败');
        }
      }).catch(() => {
        // User cancelled
      });
    };

    const submitForm = async () => {
      if (!customerForm.value) return;
      
      await customerForm.value.validate(async (valid) => {
        if (valid) {
          submitting.value = true;
          
          try {
            if (editMode.value) {
              // In a real app, we would call the API
              // await updateCustomer(selectedCustomer.value.id, form);
              ElMessage.success('客户信息更新成功');
            } else {
              // In a real app, we would call the API
              // await createCustomer(form);
              ElMessage.success('客户添加成功');
            }
            
            dialogVisible.value = false;
            loadCustomers();
          } catch (error) {
            console.error('Error submitting form:', error);
            ElMessage.error(editMode.value ? '更新失败' : '添加失败');
          } finally {
            submitting.value = false;
          }
        }
      });
    };

    // Lifecycle hooks
    onMounted(() => {
      loadCustomers();
    });

    return {
      // State
      loading,
      submitting,
      customers,
      totalCustomers,
      currentPage,
      pageSize,
      searchQuery,
      filterStatus,
      dialogVisible,
      detailsVisible,
      editMode,
      selectedCustomer,
      customerForm,
      customerRules,
      
      // Methods
      handleSearch,
      handleFilter,
      resetFilter,
      handleSizeChange,
      handleCurrentChange,
      showAddCustomerDialog,
      handleRowClick,
      handleEdit,
      handleDelete,
      submitForm,
      
      // Form data
      customerForm: form
    };
  }
});
</script>

<style scoped>
.customers-page {
  min-height: calc(100vh - 200px);
}

.table-operations {
  margin-bottom: 20px;
}

.el-table {
  cursor: pointer;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
}
</style> 