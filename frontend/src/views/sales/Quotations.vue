<template>
  <div class="quotations-container">
    <div class="header">
      <h1>报价单列表</h1>
      <el-button type="primary" @click="handleCreate">新建报价单</el-button>
    </div>

    <el-table :data="quotations" style="width: 100%" v-loading="loading">
      <el-table-column prop="quotation_number" label="报价单号" width="180" />
      <el-table-column prop="customer.name" label="客户名称" width="200" />
      <el-table-column prop="subject" label="主题" width="200" />
      <el-table-column prop="quotation_date" label="报价日期" width="120">
        <template #default="scope">
          {{ formatDate(scope.row.quotation_date) }}
        </template>
      </el-table-column>
      <el-table-column prop="valid_until" label="有效期至" width="120">
        <template #default="scope">
          {{ formatDate(scope.row.valid_until) }}
        </template>
      </el-table-column>
      <el-table-column prop="status" label="状态" width="120">
        <template #default="scope">
          <el-tag :type="getStatusType(scope.row.status)">
            {{ getStatusText(scope.row.status) }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="grand_total" label="总金额" width="120">
        <template #default="scope">
          {{ formatCurrency(scope.row.grand_total, scope.row.currency) }}
        </template>
      </el-table-column>
      <el-table-column label="操作" width="250">
        <template #default="scope">
          <el-button-group>
            <el-button size="small" @click="handleView(scope.row)">查看</el-button>
            <el-button size="small" type="primary" @click="handleEdit(scope.row)">编辑</el-button>
            <el-button size="small" type="success" @click="handleConvert(scope.row)">转为订单</el-button>
            <el-button size="small" type="danger" @click="handleDelete(scope.row)">删除</el-button>
          </el-button-group>
        </template>
      </el-table-column>
    </el-table>

    <!-- 分页 -->
    <div class="pagination">
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
  </div>
</template>

<script>
import { defineComponent, ref, onMounted } from 'vue';
import { ElMessage, ElMessageBox } from 'element-plus';
import { formatDate, formatCurrency } from '@/utils/format';
import { getQuotations, deleteQuotation } from '@/api/sales';

export default defineComponent({
  name: 'QuotationsPage',
  setup() {
    const quotations = ref([]);
    const loading = ref(false);
    const currentPage = ref(1);
    const pageSize = ref(10);
    const total = ref(0);

    const fetchQuotations = async () => {
      loading.value = true;
      try {
        const response = await getQuotations({
          page: currentPage.value,
          page_size: pageSize.value
        });
        quotations.value = response.data;
        total.value = response.total;
      } catch (error) {
        ElMessage.error('获取报价单列表失败');
      } finally {
        loading.value = false;
      }
    };

    const handleCreate = () => {
      // TODO: 跳转到创建报价单页面
    };

    const handleView = (row) => {
      // TODO: 跳转到查看报价单详情页面
    };

    const handleEdit = (row) => {
      // TODO: 跳转到编辑报价单页面
    };

    const handleConvert = (row) => {
      // TODO: 实现转换为订单的功能
    };

    const handleDelete = async (row) => {
      try {
        await ElMessageBox.confirm('确定要删除该报价单吗？', '提示', {
          type: 'warning'
        });
        await deleteQuotation(row.id);
        ElMessage.success('删除成功');
        fetchQuotations();
      } catch (error) {
        if (error !== 'cancel') {
          ElMessage.error('删除失败');
        }
      }
    };

    const handleSizeChange = (val) => {
      pageSize.value = val;
      fetchQuotations();
    };

    const handleCurrentChange = (val) => {
      currentPage.value = val;
      fetchQuotations();
    };

    const getStatusType = (status) => {
      const statusMap = {
        draft: 'info',
        sent: 'warning',
        approved: 'success',
        rejected: 'danger',
        expired: 'info',
        converted: 'success'
      };
      return statusMap[status] || 'info';
    };

    const getStatusText = (status) => {
      const statusMap = {
        draft: '草稿',
        sent: '已发送',
        approved: '已批准',
        rejected: '已拒绝',
        expired: '已过期',
        converted: '已转换'
      };
      return statusMap[status] || status;
    };

    onMounted(() => {
      fetchQuotations();
    });

    return {
      quotations,
      loading,
      currentPage,
      pageSize,
      total,
      handleCreate,
      handleView,
      handleEdit,
      handleConvert,
      handleDelete,
      handleSizeChange,
      handleCurrentChange,
      formatDate,
      formatCurrency,
      getStatusType,
      getStatusText
    };
  }
});
</script>

<style scoped>
.quotations-container {
  padding: 20px;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.pagination {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}
</style>