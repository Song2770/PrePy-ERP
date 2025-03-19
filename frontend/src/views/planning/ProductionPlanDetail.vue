<template>
  <div class="production-plan-detail-container">
    <el-card v-loading="loading">
      <template #header>
        <div class="card-header">
          <h2>生产计划详情</h2>
          <div class="header-actions">
            <el-button @click="goBack">返回</el-button>
            <el-button 
              type="primary" 
              @click="handleEdit" 
              v-if="planData.status === 'draft'"
            >
              编辑
            </el-button>
            <el-button 
              type="success" 
              @click="handleConfirm" 
              v-if="planData.status === 'draft'"
              :loading="confirming"
            >
              确认计划
            </el-button>
            <el-button 
              type="warning" 
              @click="handleMRP" 
              v-if="planData.status === 'confirmed'"
              :loading="mrpLoading"
            >
              运行MRP
            </el-button>
          </div>
        </div>
      </template>
      
      <div v-if="!loading">
        <!-- 基本信息 -->
        <div class="section">
          <div class="section-title">基本信息</div>
          <el-descriptions :column="2" border>
            <el-descriptions-item label="计划名称">{{ planData.name }}</el-descriptions-item>
            <el-descriptions-item label="计划ID">{{ planData.id }}</el-descriptions-item>
            <el-descriptions-item label="负责人">{{ planData.responsible_person }}</el-descriptions-item>
            <el-descriptions-item label="状态">
              <el-tag :type="getStatusType(planData.status)">
                {{ getStatusText(planData.status) }}
              </el-tag>
            </el-descriptions-item>
            <el-descriptions-item label="计划开始日期">{{ planData.planned_start_date }}</el-descriptions-item>
            <el-descriptions-item label="计划结束日期">{{ planData.planned_end_date }}</el-descriptions-item>
            <el-descriptions-item label="优先级">
              <el-tag :type="getPriorityType(planData.priority)">
                {{ getPriorityText(planData.priority) }}
              </el-tag>
            </el-descriptions-item>
            <el-descriptions-item label="创建时间">{{ planData.created_at }}</el-descriptions-item>
            <el-descriptions-item label="备注" :span="2">{{ planData.notes || '无' }}</el-descriptions-item>
          </el-descriptions>
        </div>
        
        <!-- 产品清单 -->
        <div class="section">
          <div class="section-title">产品清单</div>
          <el-table
            :data="planData.plan_items || []"
            border
            style="width: 100%"
          >
            <el-table-column type="index" width="50" label="#" />
            <el-table-column prop="product_name" label="产品名称" min-width="200" />
            <el-table-column prop="product_code" label="产品编码" width="150" />
            <el-table-column prop="planned_quantity" label="计划数量" width="120" />
            <el-table-column prop="completed_quantity" label="已完成数量" width="120" />
            <el-table-column label="完成率" width="150">
              <template #default="scope">
                <el-progress 
                  :percentage="calculateCompletionRate(scope.row)" 
                  :status="getCompletionStatus(scope.row)"
                />
              </template>
            </el-table-column>
          </el-table>
        </div>
        
        <!-- MRP结果 -->
        <div class="section" v-if="mrpResults.length > 0">
          <div class="section-title">物料需求计划 (MRP)</div>
          <el-table
            :data="mrpResults"
            border
            style="width: 100%"
          >
            <el-table-column type="index" width="50" label="#" />
            <el-table-column prop="material_name" label="物料名称" min-width="200" />
            <el-table-column prop="material_code" label="物料编码" width="150" />
            <el-table-column prop="required_quantity" label="需求数量" width="120" />
            <el-table-column prop="available_quantity" label="库存数量" width="120" />
            <el-table-column prop="net_quantity" label="净需求数量" width="120" />
            <el-table-column prop="required_date" label="需求日期" width="120" />
            <el-table-column prop="source_type" label="来源" width="100">
              <template #default="scope">
                {{ getMaterialSourceText(scope.row.source_type) }}
              </template>
            </el-table-column>
            <el-table-column prop="source_name" label="来源详情" min-width="150" />
          </el-table>
        </div>
        
        <!-- 工作单 -->
        <div class="section" v-if="workOrders.length > 0">
          <div class="section-title">关联工作单</div>
          <el-table
            :data="workOrders"
            border
            style="width: 100%"
          >
            <el-table-column type="index" width="50" label="#" />
            <el-table-column prop="work_order_number" label="工单编号" min-width="150" />
            <el-table-column prop="product_name" label="产品名称" min-width="200" />
            <el-table-column prop="planned_quantity" label="计划数量" width="120" />
            <el-table-column prop="status" label="状态" width="100">
              <template #default="scope">
                <el-tag :type="getWorkOrderStatusType(scope.row.status)">
                  {{ getWorkOrderStatusText(scope.row.status) }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="planned_start_date" label="计划开始日期" width="120" />
            <el-table-column prop="planned_end_date" label="计划结束日期" width="120" />
            <el-table-column label="操作" width="120">
              <template #default="scope">
                <el-button size="small" @click="viewWorkOrder(scope.row.id)">查看</el-button>
              </template>
            </el-table-column>
          </el-table>
        </div>
      </div>
    </el-card>
  </div>
</template>

<script>
import { ref, reactive, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { 
  getProductionPlan, 
  updateProductionPlan,
  runMRP,
  getWorkOrdersByPlan
} from '@/api/planning'

export default {
  name: 'ProductionPlanDetail',
  setup() {
    const route = useRoute()
    const router = useRouter()
    const loading = ref(true)
    const confirming = ref(false)
    const mrpLoading = ref(false)
    const planData = reactive({
      id: '',
      name: '',
      responsible_person: '',
      planned_start_date: '',
      planned_end_date: '',
      status: '',
      priority: '',
      notes: '',
      created_at: '',
      plan_items: []
    })
    const mrpResults = ref([])
    const workOrders = ref([])
    
    // 加载生产计划详情
    const loadProductionPlan = async () => {
      try {
        loading.value = true
        const data = await getProductionPlan(route.params.id)
        
        // 填充计划数据
        Object.keys(planData).forEach(key => {
          if (key in data) {
            planData[key] = data[key]
          }
        })
        
        // 加载关联的工作单
        await loadWorkOrders()
        
        // 如果状态为已确认或进行中，尝试获取MRP结果
        if (['confirmed', 'in_progress'].includes(planData.status)) {
          await loadMRPResults()
        }
      } catch (error) {
        console.error('加载生产计划详情失败:', error)
        ElMessage.error('加载生产计划详情失败')
      } finally {
        loading.value = false
      }
    }
    
    // 加载关联的工作单
    const loadWorkOrders = async () => {
      try {
        const response = await getWorkOrdersByPlan(route.params.id)
        workOrders.value = response.items || []
      } catch (error) {
        console.error('加载关联工作单失败:', error)
      }
    }
    
    // 加载MRP结果
    const loadMRPResults = async () => {
      try {
        const response = await runMRP(route.params.id, { dry_run: true })
        mrpResults.value = response.items || []
      } catch (error) {
        console.error('加载MRP结果失败:', error)
      }
    }
    
    // 确认生产计划
    const handleConfirm = async () => {
      try {
        await ElMessageBox.confirm(
          '确认后，计划状态将更改为"已确认"，确定要继续吗？',
          '确认计划',
          {
            confirmButtonText: '确认',
            cancelButtonText: '取消',
            type: 'warning'
          }
        )
        
        confirming.value = true
        await updateProductionPlan(route.params.id, { status: 'confirmed' })
        ElMessage.success('生产计划已确认')
        planData.status = 'confirmed'
        
        // 自动运行MRP
        await handleMRP()
      } catch (error) {
        if (error !== 'cancel') {
          console.error('确认计划失败:', error)
          ElMessage.error('确认计划失败')
        }
      } finally {
        confirming.value = false
      }
    }
    
    // 运行MRP
    const handleMRP = async () => {
      try {
        mrpLoading.value = true
        const response = await runMRP(route.params.id, { dry_run: false })
        mrpResults.value = response.items || []
        ElMessage.success('MRP运行成功')
        
        // 重新加载工作单数据
        await loadWorkOrders()
      } catch (error) {
        console.error('运行MRP失败:', error)
        ElMessage.error('运行MRP失败')
      } finally {
        mrpLoading.value = false
      }
    }
    
    // 查看工作单
    const viewWorkOrder = (id) => {
      router.push(`/production/work-orders/${id}`)
    }
    
    // 编辑计划
    const handleEdit = () => {
      router.push(`/planning/production-plans/${route.params.id}/edit`)
    }
    
    // 返回列表
    const goBack = () => {
      router.push('/planning/production-plans')
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
    
    // 获取优先级类型
    const getPriorityType = (priority) => {
      const priorityMap = {
        'low': 'info',
        'medium': 'primary',
        'high': 'warning',
        'urgent': 'danger'
      }
      return priorityMap[priority] || 'info'
    }
    
    // 获取优先级文本
    const getPriorityText = (priority) => {
      const priorityMap = {
        'low': '低',
        'medium': '中',
        'high': '高',
        'urgent': '紧急'
      }
      return priorityMap[priority] || priority
    }
    
    // 获取工作单状态类型
    const getWorkOrderStatusType = (status) => {
      const statusMap = {
        'draft': 'info',
        'scheduled': 'primary',
        'in_progress': 'warning',
        'completed': 'success',
        'cancelled': 'danger'
      }
      return statusMap[status] || ''
    }
    
    // 获取工作单状态文本
    const getWorkOrderStatusText = (status) => {
      const statusMap = {
        'draft': '草稿',
        'scheduled': '已安排',
        'in_progress': '进行中',
        'completed': '已完成',
        'cancelled': '已取消'
      }
      return statusMap[status] || status
    }
    
    // 获取物料来源类型文本
    const getMaterialSourceText = (sourceType) => {
      const sourceMap = {
        'bom': 'BOM',
        'product': '产品',
        'work_order': '工单'
      }
      return sourceMap[sourceType] || sourceType
    }
    
    // 计算完成率
    const calculateCompletionRate = (item) => {
      if (!item.planned_quantity || item.planned_quantity <= 0) {
        return 0
      }
      
      const completed = item.completed_quantity || 0
      const rate = (completed / item.planned_quantity) * 100
      return Math.min(100, Math.round(rate))
    }
    
    // 获取完成状态
    const getCompletionStatus = (item) => {
      const rate = calculateCompletionRate(item)
      if (rate >= 100) {
        return 'success'
      } else if (rate > 0) {
        return ''
      }
      return 'exception'
    }
    
    onMounted(() => {
      loadProductionPlan()
    })
    
    return {
      loading,
      confirming,
      mrpLoading,
      planData,
      mrpResults,
      workOrders,
      handleConfirm,
      handleMRP,
      handleEdit,
      viewWorkOrder,
      goBack,
      getStatusType,
      getStatusText,
      getPriorityType,
      getPriorityText,
      getWorkOrderStatusType,
      getWorkOrderStatusText,
      getMaterialSourceText,
      calculateCompletionRate,
      getCompletionStatus
    }
  }
}
</script>

<style scoped>
.production-plan-detail-container {
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

.section {
  margin-bottom: 30px;
}

.section-title {
  font-size: 16px;
  font-weight: bold;
  margin-bottom: 15px;
  padding-bottom: 10px;
  border-bottom: 1px solid #ebeef5;
}
</style> 