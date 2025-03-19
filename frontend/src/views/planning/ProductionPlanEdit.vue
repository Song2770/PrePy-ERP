<template>
  <div class="production-plan-edit-container">
    <el-card>
      <template #header>
        <div class="card-header">
          <h2>{{ isEdit ? '编辑生产计划' : '创建生产计划' }}</h2>
        </div>
      </template>
      
      <el-form
        ref="formRef"
        :model="formData"
        :rules="rules"
        label-width="120px"
        label-position="right"
        v-loading="loading"
      >
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="计划名称" prop="name">
              <el-input v-model="formData.name" placeholder="请输入计划名称" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="负责人" prop="responsible_person">
              <el-input v-model="formData.responsible_person" placeholder="请输入负责人姓名" />
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="计划开始日期" prop="planned_start_date">
              <el-date-picker
                v-model="formData.planned_start_date"
                type="date"
                placeholder="选择开始日期"
                value-format="YYYY-MM-DD"
                style="width: 100%"
              />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="计划结束日期" prop="planned_end_date">
              <el-date-picker
                v-model="formData.planned_end_date"
                type="date"
                placeholder="选择结束日期"
                value-format="YYYY-MM-DD"
                style="width: 100%"
              />
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="状态" prop="status">
              <el-select v-model="formData.status" placeholder="请选择状态" style="width: 100%">
                <el-option
                  v-for="item in statusOptions"
                  :key="item.value"
                  :label="item.label"
                  :value="item.value"
                />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="优先级" prop="priority">
              <el-select v-model="formData.priority" placeholder="请选择优先级" style="width: 100%">
                <el-option label="低" value="low" />
                <el-option label="中" value="medium" />
                <el-option label="高" value="high" />
                <el-option label="紧急" value="urgent" />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-form-item label="备注" prop="notes">
          <el-input
            v-model="formData.notes"
            type="textarea"
            :rows="3"
            placeholder="请输入备注信息"
          />
        </el-form-item>
        
        <!-- 计划产品清单 -->
        <div class="section-title">产品清单</div>
        <el-table
          :data="formData.plan_items"
          border
          style="width: 100%"
          class="plan-items-table"
        >
          <el-table-column type="index" width="50" label="#" />
          <el-table-column label="产品" min-width="200">
            <template #default="scope">
              <el-select
                v-model="scope.row.product_id"
                filterable
                remote
                placeholder="搜索产品"
                :remote-method="searchProducts"
                :loading="productLoading"
                @change="(val) => handleProductChange(val, scope.$index)"
                style="width: 100%"
              >
                <el-option
                  v-for="item in productOptions"
                  :key="item.id"
                  :label="item.name"
                  :value="item.id"
                >
                  <div style="display: flex; justify-content: space-between">
                    <span>{{ item.name }}</span>
                    <span class="text-gray">{{ item.code }}</span>
                  </div>
                </el-option>
              </el-select>
            </template>
          </el-table-column>
          <el-table-column prop="product_name" label="产品名称" width="200" />
          <el-table-column prop="product_code" label="产品编码" width="120" />
          <el-table-column label="计划数量" width="150">
            <template #default="{ row }">
              <el-input-number v-model="row.planned_quantity" :min="1" />
            </template>
          </el-table-column>
          <el-table-column label="操作" width="120">
            <template #default="scope">
              <el-button
                type="danger"
                circle
                plain
                size="small"
                icon="Delete"
                @click="removePlanItem(scope.$index)"
              />
            </template>
          </el-table-column>
        </el-table>
        
        <div class="add-item-btn">
          <el-button type="primary" plain icon="Plus" @click="addPlanItem">添加产品</el-button>
        </div>
        
        <div class="form-actions">
          <el-button @click="handleCancel">取消</el-button>
          <el-button type="primary" @click="handleSubmit" :loading="submitting">保存</el-button>
          <el-button
            v-if="isEdit && formData.status === 'draft'"
            type="success"
            @click="handleConfirm"
            :loading="confirming"
          >
            确认计划
          </el-button>
        </div>
      </el-form>
    </el-card>
  </div>
</template>

<script>
import { ref, reactive, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  getProductionPlan,
  createProductionPlan,
  updateProductionPlan
} from '@/api/planning'
import { searchProductsList } from '@/api/technical'

export default {
  name: 'ProductionPlanEdit',
  setup() {
    const route = useRoute()
    const router = useRouter()
    const formRef = ref(null)
    const loading = ref(false)
    const submitting = ref(false)
    const confirming = ref(false)
    const productLoading = ref(false)
    const productOptions = ref([])
    
    // 判断是否为编辑模式
    const isEdit = computed(() => {
      return !!route.params.id
    })
    
    // 表单数据
    const formData = reactive({
      name: '',
      responsible_person: '',
      planned_start_date: '',
      planned_end_date: '',
      status: 'draft',
      priority: 'medium',
      notes: '',
      plan_items: []
    })
    
    // 状态选项
    const statusOptions = [
      { value: 'draft', label: '草稿' },
      { value: 'confirmed', label: '已确认' },
      { value: 'in_progress', label: '进行中' },
      { value: 'completed', label: '已完成' },
      { value: 'cancelled', label: '已取消' }
    ]
    
    // 表单验证规则
    const rules = {
      name: [
        { required: true, message: '请输入计划名称', trigger: 'blur' }
      ],
      responsible_person: [
        { required: true, message: '请输入负责人', trigger: 'blur' }
      ],
      planned_start_date: [
        { required: true, message: '请选择计划开始日期', trigger: 'change' }
      ],
      planned_end_date: [
        { required: true, message: '请选择计划结束日期', trigger: 'change' }
      ],
      status: [
        { required: true, message: '请选择状态', trigger: 'change' }
      ]
    }
    
    // 加载生产计划数据
    const loadProductionPlan = async (id) => {
      try {
        loading.value = true
        const data = await getProductionPlan(id)
        // 填充表单数据
        Object.keys(formData).forEach(key => {
          if (key in data && key !== 'plan_items') {
            formData[key] = data[key]
          }
        })
        
        // 处理计划产品项
        if (data.plan_items && Array.isArray(data.plan_items)) {
          formData.plan_items = data.plan_items.map(item => ({
            id: item.id,
            product_id: item.product_id,
            product_name: item.product_name,
            product_code: item.product_code,
            planned_quantity: item.planned_quantity
          }))
        }
      } catch (error) {
        console.error('加载生产计划失败:', error)
        ElMessage.error('加载生产计划数据失败')
      } finally {
        loading.value = false
      }
    }
    
    // 搜索产品
    const searchProducts = async (query) => {
      if (query === '') {
        productOptions.value = []
        return
      }
      
      try {
        productLoading.value = true
        const response = await searchProductsList({ query })
        productOptions.value = response.items || []
      } catch (error) {
        console.error('搜索产品失败:', error)
        ElMessage.error('搜索产品失败')
      } finally {
        productLoading.value = false
      }
    }
    
    // 处理产品选择变更
    const handleProductChange = (productId, index) => {
      const selectedProduct = productOptions.value.find(p => p.id === productId)
      if (selectedProduct) {
        formData.plan_items[index].product_name = selectedProduct.name
        formData.plan_items[index].product_code = selectedProduct.code
      }
    }
    
    // 添加计划产品项
    const addPlanItem = () => {
      formData.plan_items.push({
        product_id: null,
        product_name: '',
        product_code: '',
        planned_quantity: 1
      })
    }
    
    // 移除计划产品项
    const removePlanItem = (index) => {
      formData.plan_items.splice(index, 1)
    }
    
    // 提交表单
    const handleSubmit = async () => {
      // 表单验证
      await formRef.value.validate(async (valid, fields) => {
        if (!valid) {
          console.error('表单验证失败:', fields)
          return
        }
        
        if (formData.plan_items.length === 0) {
          ElMessage.warning('请至少添加一个产品')
          return
        }
        
        // 检查产品是否都已选择
        const invalidItems = formData.plan_items.filter(item => !item.product_id)
        if (invalidItems.length > 0) {
          ElMessage.warning('有产品未选择，请检查')
          return
        }
        
        try {
          submitting.value = true
          
          // 准备提交数据
          const submitData = {
            name: formData.name,
            responsible_person: formData.responsible_person,
            planned_start_date: formData.planned_start_date,
            planned_end_date: formData.planned_end_date,
            status: formData.status,
            priority: formData.priority,
            notes: formData.notes,
            plan_items: formData.plan_items.map(item => ({
              product_id: item.product_id,
              planned_quantity: item.planned_quantity,
              id: item.id || undefined
            }))
          }
          
          if (isEdit.value) {
            // 更新生产计划
            await updateProductionPlan(route.params.id, submitData)
            ElMessage.success('更新生产计划成功')
          } else {
            // 创建生产计划
            await createProductionPlan(submitData)
            ElMessage.success('创建生产计划成功')
          }
          
          // 返回列表页
          router.push('/planning/production-plans')
        } catch (error) {
          console.error('保存生产计划失败:', error)
          ElMessage.error('保存生产计划失败')
        } finally {
          submitting.value = false
        }
      })
    }
    
    // 确认计划
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
        router.push('/planning/production-plans')
      } catch (error) {
        if (error !== 'cancel') {
          console.error('确认计划失败:', error)
          ElMessage.error('确认计划失败')
        }
      } finally {
        confirming.value = false
      }
    }
    
    // 取消操作
    const handleCancel = () => {
      router.push('/planning/production-plans')
    }
    
    onMounted(async () => {
      if (isEdit.value) {
        await loadProductionPlan(route.params.id)
      } else {
        // 新建模式，添加一个空的产品项
        addPlanItem()
      }
    })
    
    return {
      formRef,
      formData,
      rules,
      loading,
      submitting,
      confirming,
      isEdit,
      statusOptions,
      productOptions,
      productLoading,
      searchProducts,
      handleProductChange,
      addPlanItem,
      removePlanItem,
      handleSubmit,
      handleConfirm,
      handleCancel
    }
  }
}
</script>

<style scoped>
.production-plan-edit-container {
  padding: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.section-title {
  font-size: 16px;
  font-weight: bold;
  margin: 20px 0 10px;
  padding-bottom: 10px;
  border-bottom: 1px solid #ebeef5;
}

.plan-items-table {
  margin-bottom: 10px;
}

.add-item-btn {
  margin: 15px 0;
  display: flex;
  justify-content: center;
}

.form-actions {
  margin-top: 30px;
  display: flex;
  justify-content: center;
  gap: 10px;
}

.text-gray {
  color: #909399;
}
</style> 