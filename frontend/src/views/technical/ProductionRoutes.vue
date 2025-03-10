<template>
  <div class="routes-container">
    <h1 class="page-title">生产路线管理</h1>

    <!-- 操作区 -->
    <div class="page-actions">
      <el-button type="primary" @click="handleAddRoute">
        <el-icon><Plus /></el-icon> 新增生产路线
      </el-button>
      <el-input
        v-model="searchQuery"
        placeholder="搜索生产路线"
        class="search-input"
        clearable
        @clear="fetchRoutes"
      >
        <template #prefix>
          <el-icon><Search /></el-icon>
        </template>
      </el-input>
    </div>

    <!-- 生产路线列表 -->
    <el-card shadow="never" class="list-card">
      <el-table
        v-loading="loading"
        :data="routes"
        border
        style="width: 100%"
        height="calc(100vh - 250px)"
      >
        <el-table-column type="index" width="60" align="center" />
        <el-table-column prop="code" label="路线编码" min-width="120" sortable />
        <el-table-column prop="name" label="路线名称" min-width="150" />
        <el-table-column prop="product_name" label="适用产品" min-width="150" />
        <el-table-column prop="version" label="版本" width="80" align="center" />
        <el-table-column prop="steps_count" label="工序数" width="80" align="center" />
        <el-table-column prop="total_time" label="标准工时" min-width="120">
          <template #default="scope">
            {{ scope.row.total_time }} 分钟
          </template>
        </el-table-column>
        <el-table-column prop="status" label="状态" width="100" align="center">
          <template #default="scope">
            <el-tag :type="getStatusType(scope.row.status)">
              {{ getStatusText(scope.row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="created_by" label="创建人" min-width="120" />
        <el-table-column prop="updated_at" label="更新时间" min-width="150" sortable />
        <el-table-column label="操作" width="250" fixed="right">
          <template #default="scope">
            <el-button
              size="small"
              type="primary"
              @click="handleViewRoute(scope.row)"
              text
            >
              <el-icon><View /></el-icon> 查看
            </el-button>
            <el-button
              size="small"
              type="primary"
              @click="handleEditRoute(scope.row)"
              text
              :disabled="scope.row.status === 'active'"
            >
              <el-icon><Edit /></el-icon> 编辑
            </el-button>
            <el-popconfirm
              title="确定要删除此生产路线吗？"
              @confirm="handleDeleteRoute(scope.row.id)"
            >
              <template #reference>
                <el-button
                  size="small"
                  type="danger"
                  text
                  :disabled="scope.row.status === 'active'"
                >
                  <el-icon><Delete /></el-icon> 删除
                </el-button>
              </template>
            </el-popconfirm>
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

    <!-- 新增/编辑生产路线对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="isEdit ? '编辑生产路线' : '新增生产路线'"
      width="80%"
      @close="resetForm"
    >
      <el-form
        ref="routeFormRef"
        :model="routeForm"
        :rules="rules"
        label-width="120px"
      >
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="路线编码" prop="code">
              <el-input v-model="routeForm.code" placeholder="请输入路线编码" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="路线名称" prop="name">
              <el-input v-model="routeForm.name" placeholder="请输入路线名称" />
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="适用产品" prop="product_id">
              <el-select 
                v-model="routeForm.product_id" 
                placeholder="请选择产品" 
                filterable 
                style="width: 100%"
                @change="handleProductChange"
              >
                <el-option
                  v-for="product in products"
                  :key="product.id"
                  :label="product.name"
                  :value="product.id"
                />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="版本" prop="version">
              <el-input v-model="routeForm.version" placeholder="请输入版本号" />
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-form-item label="描述">
          <el-input
            v-model="routeForm.description"
            type="textarea"
            rows="3"
            placeholder="请输入生产路线描述"
          />
        </el-form-item>

        <el-divider content-position="center">工序步骤</el-divider>
        
        <div class="steps-container">
          <div class="steps-header">
            <el-button type="primary" @click="addStep" plain size="small">
              <el-icon><Plus /></el-icon> 添加工序
            </el-button>
          </div>
          
          <el-table :data="routeForm.steps" border style="width: 100%">
            <el-table-column label="序号" width="70" align="center">
              <template #default="scope">
                <el-input-number 
                  v-model="scope.row.sequence" 
                  :min="1" 
                  controls-position="right"
                  size="small"
                  style="width: 80px;"
                />
              </template>
            </el-table-column>
            <el-table-column label="工序名称" min-width="150">
              <template #default="scope">
                <el-input v-model="scope.row.name" placeholder="工序名称" />
              </template>
            </el-table-column>
            <el-table-column label="工作中心" min-width="150">
              <template #default="scope">
                <el-select 
                  v-model="scope.row.work_center_id" 
                  placeholder="选择工作中心"
                  style="width: 100%"
                  @change="(val) => handleWorkCenterChange(val, scope.$index)"
                >
                  <el-option
                    v-for="center in workCenters"
                    :key="center.id"
                    :label="center.name"
                    :value="center.id"
                  />
                </el-select>
              </template>
            </el-table-column>
            <el-table-column label="工作站" min-width="150">
              <template #default="scope">
                <el-select 
                  v-model="scope.row.workstation_id" 
                  placeholder="选择工作站"
                  style="width: 100%"
                >
                  <el-option
                    v-for="station in scope.row.available_workstations || []"
                    :key="station.id"
                    :label="station.name"
                    :value="station.id"
                  />
                </el-select>
              </template>
            </el-table-column>
            <el-table-column label="标准工时(分钟)" width="150">
              <template #default="scope">
                <el-input-number 
                  v-model="scope.row.standard_time" 
                  :min="0" 
                  :precision="1"
                  style="width: 130px;"
                />
              </template>
            </el-table-column>
            <el-table-column label="操作说明" min-width="200">
              <template #default="scope">
                <el-input 
                  v-model="scope.row.instructions" 
                  type="textarea" 
                  rows="2"
                  placeholder="操作说明"
                />
              </template>
            </el-table-column>
            <el-table-column label="操作" width="100" align="center">
              <template #default="scope">
                <el-button 
                  type="danger" 
                  @click="removeStep(scope.$index)" 
                  circle
                  size="small"
                >
                  <el-icon><Delete /></el-icon>
                </el-button>
              </template>
            </el-table-column>
          </el-table>
        </div>
        
        <el-divider />
        
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="状态" prop="status">
              <el-select v-model="routeForm.status" style="width: 100%">
                <el-option label="草稿" value="draft" />
                <el-option label="活跃" value="active" />
                <el-option label="非活跃" value="inactive" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="备注">
              <el-input v-model="routeForm.notes" placeholder="备注信息" />
            </el-form-item>
          </el-col>
        </el-row>
      </el-form>
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="saveRoute" :loading="saveLoading">
            保存
          </el-button>
        </div>
      </template>
    </el-dialog>

    <!-- 查看生产路线详情对话框 -->
    <el-dialog
      v-model="viewDialogVisible"
      title="生产路线详情"
      width="80%"
    >
      <div v-if="selectedRoute" class="route-detail">
        <el-descriptions :column="3" border>
          <el-descriptions-item label="路线编码">{{ selectedRoute.code }}</el-descriptions-item>
          <el-descriptions-item label="路线名称">{{ selectedRoute.name }}</el-descriptions-item>
          <el-descriptions-item label="版本">{{ selectedRoute.version }}</el-descriptions-item>
          <el-descriptions-item label="适用产品">{{ selectedRoute.product_name }}</el-descriptions-item>
          <el-descriptions-item label="总工时">{{ selectedRoute.total_time }} 分钟</el-descriptions-item>
          <el-descriptions-item label="状态">
            <el-tag :type="getStatusType(selectedRoute.status)">
              {{ getStatusText(selectedRoute.status) }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="描述" :span="3">{{ selectedRoute.description }}</el-descriptions-item>
        </el-descriptions>

        <h3 class="section-title">工序步骤</h3>
        <el-table :data="selectedRoute.steps || []" border style="width: 100%">
          <el-table-column prop="sequence" label="序号" width="80" align="center" />
          <el-table-column prop="name" label="工序名称" min-width="150" />
          <el-table-column prop="work_center_name" label="工作中心" min-width="150" />
          <el-table-column prop="workstation_name" label="工作站" min-width="150" />
          <el-table-column prop="standard_time" label="标准工时(分钟)" width="150" align="center" />
          <el-table-column prop="instructions" label="操作说明" min-width="200" show-overflow-tooltip />
        </el-table>

        <div class="meta-info">
          <p>创建人: {{ selectedRoute.created_by }}</p>
          <p>创建时间: {{ selectedRoute.created_at }}</p>
          <p>最后更新: {{ selectedRoute.updated_at }}</p>
          <p>备注: {{ selectedRoute.notes }}</p>
        </div>
      </div>
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="viewDialogVisible = false">关闭</el-button>
          <el-button 
            type="primary" 
            @click="handleEditRoute(selectedRoute)"
            :disabled="selectedRoute && selectedRoute.status === 'active'"
          >
            编辑
          </el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue';
import { ElMessage, ElMessageBox } from 'element-plus';
import { useRouteApi } from '@/api/technical/productionroute';
import { useProductApi } from '@/api/technical/product';
import { useWorkCenterApi } from '@/api/technical/workcenter';
import { useWorkstationApi } from '@/api/technical/workstation';

// API
const routeApi = useRouteApi();
const productApi = useProductApi();
const workCenterApi = useWorkCenterApi();
const workstationApi = useWorkstationApi();

// 数据
const routes = ref([]);
const products = ref([]);
const workCenters = ref([]);
const loading = ref(false);
const saveLoading = ref(false);
const currentPage = ref(1);
const pageSize = ref(20);
const total = ref(0);
const searchQuery = ref('');
const dialogVisible = ref(false);
const viewDialogVisible = ref(false);
const isEdit = ref(false);
const routeFormRef = ref(null);
const selectedRoute = ref(null);

// 表单数据
const routeForm = reactive({
  id: null,
  code: '',
  name: '',
  product_id: '',
  product_name: '',
  version: '1.0',
  description: '',
  status: 'draft',
  notes: '',
  steps: []
});

// 表单校验规则
const rules = {
  code: [
    { required: true, message: '请输入路线编码', trigger: 'blur' },
    { min: 2, max: 20, message: '长度在 2 到 20 个字符', trigger: 'blur' }
  ],
  name: [
    { required: true, message: '请输入路线名称', trigger: 'blur' },
    { min: 2, max: 50, message: '长度在 2 到 50 个字符', trigger: 'blur' }
  ],
  product_id: [
    { required: true, message: '请选择适用产品', trigger: 'change' }
  ],
  version: [
    { required: true, message: '请输入版本号', trigger: 'blur' }
  ],
  status: [
    { required: true, message: '请选择状态', trigger: 'change' }
  ]
};

// 组件挂载时获取数据
onMounted(async () => {
  await Promise.all([fetchRoutes(), fetchProducts(), fetchWorkCenters()]);
});

// 获取生产路线列表
async function fetchRoutes() {
  loading.value = true;
  try {
    const params = {
      page: currentPage.value,
      size: pageSize.value,
      query: searchQuery.value
    };
    const { data } = await routeApi.getRoutes(params);
    routes.value = data.items;
    total.value = data.total;
  } catch (error) {
    console.error('获取生产路线列表失败:', error);
    ElMessage.error('获取生产路线列表失败');
  } finally {
    loading.value = false;
  }
}

// 获取产品列表
async function fetchProducts() {
  try {
    const { data } = await productApi.getProducts({ size: 100 });
    products.value = data.items;
  } catch (error) {
    console.error('获取产品列表失败:', error);
    ElMessage.error('获取产品列表失败');
  }
}

// 获取工作中心列表
async function fetchWorkCenters() {
  try {
    const { data } = await workCenterApi.getWorkCenters({ size: 100 });
    workCenters.value = data.items;
  } catch (error) {
    console.error('获取工作中心列表失败:', error);
    ElMessage.error('获取工作中心列表失败');
  }
}

// 根据工作中心获取工作站列表
async function fetchWorkstations(workCenterId, stepIndex) {
  try {
    const { data } = await workstationApi.getWorkstations({ 
      work_center: workCenterId,
      is_active: true,
      size: 100
    });
    
    if (stepIndex !== undefined) {
      routeForm.steps[stepIndex].available_workstations = data.items;
    }
    
    return data.items;
  } catch (error) {
    console.error('获取工作站列表失败:', error);
    ElMessage.error('获取工作站列表失败');
    return [];
  }
}

// 分页处理
function handleSizeChange(val) {
  pageSize.value = val;
  fetchRoutes();
}

function handleCurrentChange(val) {
  currentPage.value = val;
  fetchRoutes();
}

// 添加生产路线
function handleAddRoute() {
  isEdit.value = false;
  dialogVisible.value = true;
}

// 查看生产路线详情
function handleViewRoute(row) {
  selectedRoute.value = row;
  viewDialogVisible.value = true;
}

// 编辑生产路线
function handleEditRoute(row) {
  isEdit.value = true;
  viewDialogVisible.value = false;
  
  // 克隆数据以防止直接修改原始数据
  const routeData = JSON.parse(JSON.stringify(row));
  
  // 处理步骤数据
  if (routeData.steps) {
    // 确保每个步骤都有available_workstations属性
    routeData.steps.forEach(async (step, index) => {
      if (step.work_center_id) {
        const workstations = await fetchWorkstations(step.work_center_id);
        step.available_workstations = workstations;
      } else {
        step.available_workstations = [];
      }
    });
  }
  
  Object.assign(routeForm, routeData);
  dialogVisible.value = true;
}

// 删除生产路线
async function handleDeleteRoute(id) {
  try {
    await routeApi.deleteRoute(id);
    ElMessage.success('删除成功');
    fetchRoutes();
  } catch (error) {
    console.error('删除生产路线失败:', error);
    ElMessage.error('删除生产路线失败');
  }
}

// 添加工序步骤
function addStep() {
  routeForm.steps.push({
    sequence: routeForm.steps.length + 1,
    name: '',
    work_center_id: '',
    workstation_id: '',
    standard_time: 10,
    instructions: '',
    available_workstations: []
  });
}

// 移除工序步骤
function removeStep(index) {
  routeForm.steps.splice(index, 1);
  
  // 重新排列序号
  routeForm.steps.forEach((step, idx) => {
    step.sequence = idx + 1;
  });
}

// 产品选择变更
function handleProductChange(productId) {
  const product = products.value.find(p => p.id === productId);
  if (product) {
    routeForm.product_name = product.name;
  }
}

// 工作中心变更
async function handleWorkCenterChange(workCenterId, stepIndex) {
  // 重置当前步骤的工作站
  routeForm.steps[stepIndex].workstation_id = '';
  
  // 加载该工作中心下的工作站
  await fetchWorkstations(workCenterId, stepIndex);
}

// 保存生产路线
async function saveRoute() {
  await routeFormRef.value.validate(async (valid) => {
    if (!valid) return;
    
    // 验证是否有工序步骤
    if (routeForm.steps.length === 0) {
      ElMessage.warning('请至少添加一个工序步骤');
      return;
    }
    
    // 验证工序步骤有效性
    for (const step of routeForm.steps) {
      if (!step.name || !step.work_center_id || !step.workstation_id) {
        ElMessage.warning('工序步骤信息不完整');
        return;
      }
    }
    
    saveLoading.value = true;
    try {
      // 计算总工时
      const totalTime = routeForm.steps.reduce((sum, step) => sum + (step.standard_time || 0), 0);
      
      // 准备要提交的数据
      const routeData = { ...routeForm, total_time: totalTime };
      
      if (isEdit.value) {
        await routeApi.updateRoute(routeForm.id, routeData);
        ElMessage.success('更新成功');
      } else {
        await routeApi.createRoute(routeData);
        ElMessage.success('创建成功');
      }
      dialogVisible.value = false;
      fetchRoutes();
    } catch (error) {
      console.error('保存生产路线失败:', error);
      ElMessage.error('保存生产路线失败');
    } finally {
      saveLoading.value = false;
    }
  });
}

// 重置表单
function resetForm() {
  routeFormRef.value?.resetFields();
  Object.assign(routeForm, {
    id: null,
    code: '',
    name: '',
    product_id: '',
    product_name: '',
    version: '1.0',
    description: '',
    status: 'draft',
    notes: '',
    steps: []
  });
}

// 获取状态类型
function getStatusType(status) {
  const statusMap = {
    draft: 'warning',
    active: 'success',
    inactive: 'info'
  };
  return statusMap[status] || 'info';
}

// 获取状态文本
function getStatusText(status) {
  const statusMap = {
    draft: '草稿',
    active: '活跃',
    inactive: '非活跃'
  };
  return statusMap[status] || '未知';
}
</script>

<style scoped>
.routes-container {
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

.steps-container {
  margin: 20px 0;
}

.steps-header {
  margin-bottom: 10px;
  display: flex;
  justify-content: flex-end;
}

.section-title {
  margin: 20px 0 10px;
  font-size: 18px;
  font-weight: 600;
  color: #303133;
}

.meta-info {
  margin-top: 20px;
  color: #606266;
  font-size: 14px;
}

.meta-info p {
  margin: 5px 0;
}
</style> 