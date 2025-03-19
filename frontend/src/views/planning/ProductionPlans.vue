<template>
  <div class="production-plans-container">
    <div class="header">
      <h1>生产计划管理</h1>
      <el-button type="primary" @click="handleCreatePlan">创建生产计划</el-button>
    </div>
    
    <el-card class="filter-container">
      <el-form :inline="true" :model="filterForm" class="filter-form">
        <el-form-item label="计划名称">
          <el-input v-model="filterForm.name" placeholder="请输入计划名称" clearable />
        </el-form-item>
        <el-form-item label="状态">
          <el-select v-model="filterForm.status" placeholder="请选择状态" clearable>
            <el-option v-for="item in statusOptions" :key="item.value" :label="item.label" :value="item.value" />
          </el-select>
        </el-form-item>
        <el-form-item label="日期范围">
          <el-date-picker
            v-model="dateRange"
            type="daterange"
            range-separator="至"
            start-placeholder="开始日期"
            end-placeholder="结束日期"
            value-format="YYYY-MM-DD"
          />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch">搜索</el-button>
          <el-button @click="resetFilter">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>
    
    <el-card class="table-container">
      <el-table
        v-loading="loading"
        :data="productionPlans"
        border
        style="width: 100%"
      >
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="name" label="计划名称" min-width="150" />
        <el-table-column prop="planned_start_date" label="计划开始日期" width="120" />
        <el-table-column prop="planned_end_date" label="计划结束日期" width="120" />
        <el-table-column label="状态" width="100">
          <template #default="scope">
            <el-tag :type="getStatusType(scope.row.status)">
              {{ getStatusText(scope.row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="responsible_person" label="负责人" width="120" />
        <el-table-column prop="created_at" label="创建时间" width="180" />
        <el-table-column label="操作" width="220" fixed="right">
          <template #default="scope">
            <el-button size="small" @click="handleViewPlan(scope.row.id)">查看</el-button>
            <el-button size="small" type="primary" @click="handleEditPlan(scope.row.id)">编辑</el-button>
            <el-popconfirm
              title="确定删除此生产计划吗？"
              @confirm="handleDeletePlan(scope.row.id)"
            >
              <template #reference>
                <el-button size="small" type="danger">删除</el-button>
              </template>
            </el-popconfirm>
          </template>
        </el-table-column>
      </el-table>
      
      <div class="pagination-container">
        <el-pagination
          background
          layout="total, sizes, prev, pager, next"
          :current-page="page"
          :page-size="pageSize"
          :page-sizes="[10, 20, 50, 100]"
          :total="total"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        />
      </div>
    </el-card>
  </div>
</template>

<script>
import { ref, reactive, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { getProductionPlans, deleteProductionPlan } from '@/api/planning'

export default {
  name: 'ProductionPlans',
  setup() {
    const router = useRouter()
    const loading = ref(false)
    const productionPlans = ref([])
    const page = ref(1)
    const pageSize = ref(10)
    const total = ref(0)
    const dateRange = ref([])
    
    const filterForm = reactive({
      name: '',
      status: '',
      start_date: '',
      end_date: ''
    })
    
    const statusOptions = [
      { value: 'draft', label: '草稿' },
      { value: 'confirmed', label: '已确认' },
      { value: 'in_progress', label: '进行中' },
      { value: 'completed', label: '已完成' },
      { value: 'cancelled', label: '已取消' }
    ]
    
    // 监听日期范围变化
    const watchDateRange = computed(() => {
      if (dateRange.value && dateRange.value.length === 2) {
        filterForm.start_date = dateRange.value[0]
        filterForm.end_date = dateRange.value[1]
      } else {
        filterForm.start_date = ''
        filterForm.end_date = ''
      }
      return dateRange.value
    })
    
    // 获取状态文本
    const getStatusText = (status) => {
      const statusMap = {
        'draft': '草稿',
        'confirmed': '已确认',
        'in_progress': '进行中',
        'completed': '已完成',
        'cancelled': '已取消'
      }
      return statusMap[status] || status
    }
    
    // 获取状态类型
    const getStatusType = (status) => {
      const statusMap = {
        'draft': 'info',
        'confirmed': 'primary',
        'in_progress': 'warning',
        'completed': 'success',
        'cancelled': 'danger'
      }
      return statusMap[status] || ''
    }
    
    // 加载生产计划数据
    const loadProductionPlans = async () => {
      try {
        loading.value = true
        const params = {
          page: page.value,
          size: pageSize.value,
          ...filterForm
        }
        
        const response = await getProductionPlans(params)
        productionPlans.value = response.items
        total.value = response.total
      } catch (error) {
        console.error('获取生产计划失败:', error)
        ElMessage.error('获取生产计划失败')
      } finally {
        loading.value = false
      }
    }
    
    // 搜索
    const handleSearch = () => {
      page.value = 1
      loadProductionPlans()
    }
    
    // 重置筛选条件
    const resetFilter = () => {
      Object.keys(filterForm).forEach(key => {
        filterForm[key] = ''
      })
      dateRange.value = []
      page.value = 1
      loadProductionPlans()
    }
    
    // 查看生产计划
    const handleViewPlan = (id) => {
      router.push(`/planning/production-plans/${id}`)
    }
    
    // 创建生产计划
    const handleCreatePlan = () => {
      router.push('/planning/production-plans/create')
    }
    
    // 编辑生产计划
    const handleEditPlan = (id) => {
      router.push(`/planning/production-plans/${id}/edit`)
    }
    
    // 删除生产计划
    const handleDeletePlan = async (id) => {
      try {
        await deleteProductionPlan(id)
        ElMessage.success('删除生产计划成功')
        loadProductionPlans()
      } catch (error) {
        console.error('删除生产计划失败:', error)
        ElMessage.error('删除生产计划失败')
      }
    }
    
    // 页码改变
    const handleCurrentChange = (val) => {
      page.value = val
      loadProductionPlans()
    }
    
    // 每页数量改变
    const handleSizeChange = (val) => {
      pageSize.value = val
      page.value = 1
      loadProductionPlans()
    }
    
    onMounted(() => {
      loadProductionPlans()
    })
    
    return {
      loading,
      productionPlans,
      page,
      pageSize,
      total,
      filterForm,
      dateRange,
      statusOptions,
      watchDateRange,
      handleSearch,
      resetFilter,
      handleViewPlan,
      handleCreatePlan,
      handleEditPlan,
      handleDeletePlan,
      handleCurrentChange,
      handleSizeChange,
      getStatusText,
      getStatusType
    }
  }
}
</script>

<style scoped>
.production-plans-container {
  padding: 20px;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.filter-container {
  margin-bottom: 20px;
}

.filter-form {
  display: flex;
  flex-wrap: wrap;
}

.table-container {
  margin-bottom: 20px;
}

.pagination-container {
  display: flex;
  justify-content: flex-end;
  margin-top: 20px;
}
</style> 