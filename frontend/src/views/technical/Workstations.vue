<template>
  <div class="workstations-container">
    <h1 class="page-title">工作站管理</h1>

    <!-- 操作区 -->
    <div class="page-actions">
      <el-button type="primary" @click="handleAddWorkstation">
        <el-icon><Plus /></el-icon> 新增工作站
      </el-button>
      <el-input
        v-model="searchQuery"
        placeholder="搜索工作站"
        class="search-input"
        clearable
        @clear="fetchWorkstations"
      >
        <template #prefix>
          <el-icon><Search /></el-icon>
        </template>
      </el-input>
    </div>

    <!-- 工作站列表 -->
    <el-card shadow="never" class="list-card">
      <el-table
        v-loading="loading"
        :data="workstations"
        border
        style="width: 100%"
        height="calc(100vh - 250px)"
      >
        <el-table-column type="index" width="60" align="center" />
        <el-table-column prop="code" label="工作站编码" min-width="120" sortable />
        <el-table-column prop="name" label="工作站名称" min-width="150" />
        <el-table-column prop="description" label="描述" min-width="200" show-overflow-tooltip />
        <el-table-column prop="work_center" label="所属工作中心" min-width="150" />
        <el-table-column prop="capacity" label="产能" min-width="100">
          <template #default="scope">
            {{ scope.row.capacity }} {{ scope.row.capacity_uom }}
          </template>
        </el-table-column>
        <el-table-column prop="efficiency" label="效率" min-width="100">
          <template #default="scope">
            {{ (scope.row.efficiency * 100).toFixed(2) }}%
          </template>
        </el-table-column>
        <el-table-column prop="is_active" label="状态" width="100" align="center">
          <template #default="scope">
            <el-tag :type="scope.row.is_active ? 'success' : 'danger'">
              {{ scope.row.is_active ? '启用' : '禁用' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200" fixed="right">
          <template #default="scope">
            <el-button
              size="small"
              type="primary"
              @click="handleEditWorkstation(scope.row)"
              text
            >
              <el-icon><Edit /></el-icon> 编辑
            </el-button>
            <el-popconfirm
              title="确定要删除此工作站吗？"
              @confirm="handleDeleteWorkstation(scope.row.id)"
            >
              <template #reference>
                <el-button
                  size="small"
                  type="danger"
                  text
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

    <!-- 新增/编辑工作站对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="isEdit ? '编辑工作站' : '新增工作站'"
      width="600px"
      @close="resetForm"
    >
      <el-form
        ref="workstationFormRef"
        :model="workstationForm"
        :rules="rules"
        label-width="120px"
      >
        <el-form-item label="工作站编码" prop="code">
          <el-input v-model="workstationForm.code" placeholder="请输入工作站编码" />
        </el-form-item>
        <el-form-item label="工作站名称" prop="name">
          <el-input v-model="workstationForm.name" placeholder="请输入工作站名称" />
        </el-form-item>
        <el-form-item label="所属工作中心" prop="work_center">
          <el-select v-model="workstationForm.work_center" placeholder="请选择工作中心" style="width: 100%">
            <el-option
              v-for="center in workCenters"
              :key="center.id"
              :label="center.name"
              :value="center.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="产能" prop="capacity">
          <el-input-number v-model="workstationForm.capacity" :min="0" style="width: 200px" />
          <el-select v-model="workstationForm.capacity_uom" style="width: 120px; margin-left: 10px">
            <el-option label="件/小时" value="piece/hour" />
            <el-option label="批次/天" value="batch/day" />
            <el-option label="公斤/小时" value="kg/hour" />
          </el-select>
        </el-form-item>
        <el-form-item label="效率" prop="efficiency">
          <el-slider
            v-model="workstationForm.efficiency"
            :min="0"
            :max="1"
            :step="0.01"
            :format-tooltip="(val) => `${(val * 100).toFixed(0)}%`"
          />
        </el-form-item>
        <el-form-item label="描述">
          <el-input
            v-model="workstationForm.description"
            type="textarea"
            rows="3"
            placeholder="请输入工作站描述"
          />
        </el-form-item>
        <el-form-item label="状态">
          <el-switch
            v-model="workstationForm.is_active"
            :active-text="workstationForm.is_active ? '启用' : '禁用'"
            inline-prompt
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="saveWorkstation" :loading="saveLoading">
            保存
          </el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue';
import { ElMessage, ElMessageBox } from 'element-plus';
import { useWorkstationApi } from '@/api/technical/workstation';
import { useWorkCenterApi } from '@/api/technical/workcenter';

// API
const workstationApi = useWorkstationApi();
const workCenterApi = useWorkCenterApi();

// 数据
const workstations = ref([]);
const workCenters = ref([]);
const loading = ref(false);
const saveLoading = ref(false);
const currentPage = ref(1);
const pageSize = ref(20);
const total = ref(0);
const searchQuery = ref('');
const dialogVisible = ref(false);
const isEdit = ref(false);
const workstationFormRef = ref(null);

// 表单数据
const workstationForm = reactive({
  id: null,
  code: '',
  name: '',
  description: '',
  work_center: '',
  capacity: 10,
  capacity_uom: 'piece/hour',
  efficiency: 0.8,
  is_active: true
});

// 表单校验规则
const rules = {
  code: [
    { required: true, message: '请输入工作站编码', trigger: 'blur' },
    { min: 2, max: 20, message: '长度在 2 到 20 个字符', trigger: 'blur' }
  ],
  name: [
    { required: true, message: '请输入工作站名称', trigger: 'blur' },
    { min: 2, max: 50, message: '长度在 2 到 50 个字符', trigger: 'blur' }
  ],
  work_center: [
    { required: true, message: '请选择所属工作中心', trigger: 'change' }
  ],
  capacity: [
    { required: true, message: '请输入产能', trigger: 'blur' },
    { type: 'number', min: 0, message: '产能必须大于等于0', trigger: 'blur' }
  ]
};

// 组件挂载时获取数据
onMounted(async () => {
  await Promise.all([fetchWorkstations(), fetchWorkCenters()]);
});

// 获取工作站列表
async function fetchWorkstations() {
  loading.value = true;
  try {
    const params = {
      page: currentPage.value,
      size: pageSize.value,
      query: searchQuery.value
    };
    const { data } = await workstationApi.getWorkstations(params);
    workstations.value = data.items;
    total.value = data.total;
  } catch (error) {
    console.error('获取工作站列表失败:', error);
    ElMessage.error('获取工作站列表失败');
  } finally {
    loading.value = false;
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

// 分页处理
function handleSizeChange(val) {
  pageSize.value = val;
  fetchWorkstations();
}

function handleCurrentChange(val) {
  currentPage.value = val;
  fetchWorkstations();
}

// 添加工作站
function handleAddWorkstation() {
  isEdit.value = false;
  dialogVisible.value = true;
}

// 编辑工作站
function handleEditWorkstation(row) {
  isEdit.value = true;
  Object.assign(workstationForm, row);
  dialogVisible.value = true;
}

// 删除工作站
async function handleDeleteWorkstation(id) {
  try {
    await workstationApi.deleteWorkstation(id);
    ElMessage.success('删除成功');
    fetchWorkstations();
  } catch (error) {
    console.error('删除工作站失败:', error);
    ElMessage.error('删除工作站失败');
  }
}

// 保存工作站
async function saveWorkstation() {
  await workstationFormRef.value.validate(async (valid) => {
    if (!valid) return;
    
    saveLoading.value = true;
    try {
      if (isEdit.value) {
        await workstationApi.updateWorkstation(workstationForm.id, workstationForm);
        ElMessage.success('更新成功');
      } else {
        await workstationApi.createWorkstation(workstationForm);
        ElMessage.success('创建成功');
      }
      dialogVisible.value = false;
      fetchWorkstations();
    } catch (error) {
      console.error('保存工作站失败:', error);
      ElMessage.error('保存工作站失败');
    } finally {
      saveLoading.value = false;
    }
  });
}

// 重置表单
function resetForm() {
  workstationFormRef.value?.resetFields();
  Object.assign(workstationForm, {
    id: null,
    code: '',
    name: '',
    description: '',
    work_center: '',
    capacity: 10,
    capacity_uom: 'piece/hour',
    efficiency: 0.8,
    is_active: true
  });
}
</script>

<style scoped>
.workstations-container {
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
</style>
