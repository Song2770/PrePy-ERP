<template>
  <div class="bom-container">
    <h1 class="page-title">物料清单管理</h1>

    <!-- 操作区 -->
    <div class="page-actions">
      <el-button type="primary" @click="handleCreateBom">
        <el-icon><Plus /></el-icon> 新建物料清单
      </el-button>
      <div class="search-filter">
        <el-input
          v-model="searchQuery"
          placeholder="搜索物料清单"
          class="search-input"
          clearable
          @clear="fetchBomList"
        >
          <template #prefix>
            <el-icon><Search /></el-icon>
          </template>
        </el-input>
        <el-select v-model="bomTypeFilter" placeholder="BOM类型" clearable @change="handleFilterChange">
          <el-option label="全部" value="" />
          <el-option label="生产BOM" value="manufacturing" />
          <el-option label="工程BOM" value="engineering" />
          <el-option label="销售BOM" value="sales" />
          <el-option label="模板BOM" value="template" />
        </el-select>
      </div>
    </div>

    <!-- BOM列表 -->
    <el-card shadow="never" class="list-card">
      <el-table
        v-loading="loading"
        :data="bomList"
        border
        style="width: 100%"
        height="calc(100vh - 250px)"
      >
        <el-table-column type="index" width="60" align="center" />
        <el-table-column prop="code" label="BOM编号" min-width="120" sortable />
        <el-table-column prop="product_name" label="产品名称" min-width="150" />
        <el-table-column prop="product_code" label="产品编码" min-width="120" />
        <el-table-column prop="version" label="版本" width="100" />
        <el-table-column prop="type" label="BOM类型" width="120">
          <template #default="scope">
            <el-tag size="small">{{ getBomTypeText(scope.row.type) }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="items_count" label="物料数" width="80" align="center" />
        <el-table-column prop="is_active" label="状态" width="80" align="center">
          <template #default="scope">
            <el-tag :type="scope.row.is_active ? 'success' : 'info'">
              {{ scope.row.is_active ? '启用' : '禁用' }}
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
              @click="handleViewBom(scope.row)"
              text
            >
              <el-icon><View /></el-icon> 查看
            </el-button>
            <el-button
              size="small"
              type="primary"
              @click="handleEditBom(scope.row)"
              text
            >
              <el-icon><Edit /></el-icon> 编辑
            </el-button>
            <el-popconfirm
              title="确定要删除此物料清单吗？"
              @confirm="handleDeleteBom(scope.row.id)"
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

    <!-- 查看BOM详情对话框 -->
    <el-dialog
      v-model="viewDialogVisible"
      title="物料清单详情"
      width="80%"
    >
      <div v-if="selectedBom" class="bom-detail">
        <el-descriptions :column="3" border>
          <el-descriptions-item label="BOM编号">{{ selectedBom.code }}</el-descriptions-item>
          <el-descriptions-item label="产品名称">{{ selectedBom.product_name }}</el-descriptions-item>
          <el-descriptions-item label="产品编码">{{ selectedBom.product_code }}</el-descriptions-item>
          <el-descriptions-item label="版本">{{ selectedBom.version }}</el-descriptions-item>
          <el-descriptions-item label="BOM类型">{{ getBomTypeText(selectedBom.type) }}</el-descriptions-item>
          <el-descriptions-item label="状态">
            <el-tag :type="selectedBom.is_active ? 'success' : 'info'">
              {{ selectedBom.is_active ? '启用' : '禁用' }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="描述" :span="3">{{ selectedBom.description || '无' }}</el-descriptions-item>
        </el-descriptions>

        <el-tabs v-model="activeTab" class="bom-tabs">
          <el-tab-pane label="物料清单" name="list">
            <el-table :data="selectedBom.items || []" border style="width: 100%">
              <el-table-column type="index" width="60" align="center" />
              <el-table-column prop="material_code" label="物料编码" min-width="120" />
              <el-table-column prop="material_name" label="物料名称" min-width="150" />
              <el-table-column prop="material_type" label="物料类型" width="120">
                <template #default="scope">
                  <el-tag size="small">{{ getMaterialTypeText(scope.row.material_type) }}</el-tag>
                </template>
              </el-table-column>
              <el-table-column prop="quantity" label="数量" width="100" align="center" />
              <el-table-column prop="uom" label="单位" width="80" align="center" />
              <el-table-column prop="position" label="位置" min-width="120" />
              <el-table-column prop="is_key" label="关键件" width="80" align="center">
                <template #default="scope">
                  <el-tag v-if="scope.row.is_key" type="danger" size="small">关键</el-tag>
                  <span v-else>-</span>
                </template>
              </el-table-column>
              <el-table-column prop="remarks" label="备注" min-width="150" show-overflow-tooltip />
            </el-table>
          </el-tab-pane>
          <el-tab-pane label="结构树" name="tree">
            <div class="bom-tree-container">
              <el-tree
                v-if="bomTreeData.length > 0"
                :data="bomTreeData"
                node-key="id"
                default-expand-all
                :props="{
                  label: 'name',
                  children: 'children'
                }"
              >
                <template #default="{ node, data }">
                  <div class="bom-tree-node">
                    <span class="node-label">{{ data.name }}</span>
                    <span class="node-code">{{ data.code }}</span>
                    <span v-if="data.quantity" class="node-quantity">
                      {{ data.quantity }} {{ data.uom }}
                    </span>
                  </div>
                </template>
              </el-tree>
              <el-empty v-else description="暂无BOM结构数据" />
            </div>
          </el-tab-pane>
          <el-tab-pane label="版本历史" name="versions">
            <el-table :data="bomVersions" border style="width: 100%">
              <el-table-column prop="version" label="版本号" width="100" />
              <el-table-column prop="created_at" label="创建时间" min-width="150" />
              <el-table-column prop="created_by" label="创建人" min-width="120" />
              <el-table-column prop="items_count" label="物料数" width="80" align="center" />
              <el-table-column prop="is_active" label="状态" width="80" align="center">
                <template #default="scope">
                  <el-tag :type="scope.row.is_active ? 'success' : 'info'">
                    {{ scope.row.is_active ? '启用' : '禁用' }}
                  </el-tag>
                </template>
              </el-table-column>
              <el-table-column prop="remarks" label="变更说明" min-width="200" show-overflow-tooltip />
              <el-table-column label="操作" width="100">
                <template #default="scope">
                  <el-button
                    size="small"
                    type="primary"
                    @click="viewBomVersion(scope.row)"
                    text
                  >
                    查看
                  </el-button>
                </template>
              </el-table-column>
            </el-table>
          </el-tab-pane>
        </el-tabs>

        <div class="meta-info">
          <p>创建人: {{ selectedBom.created_by }}</p>
          <p>创建时间: {{ selectedBom.created_at }}</p>
          <p>最后更新: {{ selectedBom.updated_at }}</p>
          <p>备注: {{ selectedBom.remarks || '无' }}</p>
        </div>
      </div>
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="viewDialogVisible = false">关闭</el-button>
          <el-button 
            type="primary" 
            @click="handleEditBom(selectedBom)"
          >
            编辑
          </el-button>
        </div>
      </template>
    </el-dialog>

    <!-- 创建/编辑BOM对话框 -->
    <el-dialog
      v-model="editDialogVisible"
      :title="isEdit ? '编辑物料清单' : '新建物料清单'"
      width="80%"
      @close="resetForm"
    >
      <el-form
        ref="bomFormRef"
        :model="bomForm"
        :rules="rules"
        label-width="120px"
      >
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="BOM编号" prop="code">
              <el-input v-model="bomForm.code" placeholder="请输入BOM编号" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="版本" prop="version">
              <el-input v-model="bomForm.version" placeholder="请输入版本号" />
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="关联产品" prop="product_id">
              <el-select 
                v-model="bomForm.product_id" 
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
            <el-form-item label="BOM类型" prop="type">
              <el-select v-model="bomForm.type" placeholder="请选择BOM类型" style="width: 100%">
                <el-option label="生产BOM" value="manufacturing" />
                <el-option label="工程BOM" value="engineering" />
                <el-option label="销售BOM" value="sales" />
                <el-option label="模板BOM" value="template" />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-form-item label="描述">
          <el-input
            v-model="bomForm.description"
            type="textarea"
            rows="3"
            placeholder="请输入物料清单描述"
          />
        </el-form-item>

        <el-divider content-position="center">物料清单项</el-divider>
        
        <div class="items-container">
          <div class="items-header">
            <el-button type="primary" @click="addItem" plain size="small">
              <el-icon><Plus /></el-icon> 添加物料
            </el-button>
          </div>
          
          <el-table :data="bomForm.items" border style="width: 100%">
            <el-table-column label="序号" width="70" align="center">
              <template #default="scope">
                {{ scope.$index + 1 }}
              </template>
            </el-table-column>
            <el-table-column label="物料" min-width="300">
              <template #default="scope">
                <el-select 
                  v-model="scope.row.material_id" 
                  placeholder="选择物料"
                  filterable
                  style="width: 100%"
                  @change="(val) => handleMaterialChange(val, scope.$index)"
                >
                  <el-option
                    v-for="material in materials"
                    :key="material.id"
                    :label="`${material.code} - ${material.name}`"
                    :value="material.id"
                  />
                </el-select>
              </template>
            </el-table-column>
            <el-table-column label="数量" width="150">
              <template #default="scope">
                <el-input-number 
                  v-model="scope.row.quantity" 
                  :min="0" 
                  :precision="3"
                  :step="1"
                  style="width: 150px;"
                />
              </template>
            </el-table-column>
            <el-table-column label="单位" width="100">
              <template #default="scope">
                <el-input v-model="scope.row.uom" placeholder="单位" :disabled="true" />
              </template>
            </el-table-column>
            <el-table-column label="位置" min-width="150">
              <template #default="scope">
                <el-input v-model="scope.row.position" placeholder="安装/使用位置" />
              </template>
            </el-table-column>
            <el-table-column label="关键件" width="80" align="center">
              <template #default="scope">
                <el-checkbox v-model="scope.row.is_key" />
              </template>
            </el-table-column>
            <el-table-column label="备注" min-width="200">
              <template #default="scope">
                <el-input v-model="scope.row.remarks" placeholder="备注" />
              </template>
            </el-table-column>
            <el-table-column label="操作" width="80" align="center">
              <template #default="scope">
                <el-button 
                  type="danger" 
                  @click="removeItem(scope.$index)" 
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
            <el-form-item label="状态">
              <el-switch
                v-model="bomForm.is_active"
                :active-text="bomForm.is_active ? '启用' : '禁用'"
                inline-prompt
              />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="变更说明">
              <el-input v-model="bomForm.remarks" placeholder="版本变更说明" />
            </el-form-item>
          </el-col>
        </el-row>
      </el-form>
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="editDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="saveBom" :loading="saveLoading">
            保存
          </el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue';
import { useRouter } from 'vue-router';
import { ElMessage, ElMessageBox } from 'element-plus';
import { useBomApi } from '@/api/technical/bom';
import { useProductApi } from '@/api/technical/product';
import { useMaterialApi } from '@/api/technical/material';

// 路由和API
const router = useRouter();
const bomApi = useBomApi();
const productApi = useProductApi();
const materialApi = useMaterialApi();

// 数据
const bomList = ref([]);
const products = ref([]);
const materials = ref([]);
const bomVersions = ref([]);
const bomTreeData = ref([]);
const loading = ref(false);
const saveLoading = ref(false);
const currentPage = ref(1);
const pageSize = ref(20);
const total = ref(0);
const searchQuery = ref('');
const bomTypeFilter = ref('');

// 对话框状态
const viewDialogVisible = ref(false);
const editDialogVisible = ref(false);
const isEdit = ref(false);
const activeTab = ref('list');
const bomFormRef = ref(null);
const selectedBom = ref(null);

// 表单数据
const bomForm = reactive({
  id: null,
  code: '',
  product_id: '',
  product_name: '',
  product_code: '',
  version: '1.0',
  type: 'manufacturing',
  description: '',
  is_active: true,
  remarks: '',
  items: []
});

// 表单校验规则
const rules = {
  code: [
    { required: true, message: '请输入BOM编号', trigger: 'blur' },
    { min: 2, max: 30, message: '长度在 2 到 30 个字符', trigger: 'blur' }
  ],
  product_id: [
    { required: true, message: '请选择关联产品', trigger: 'change' }
  ],
  version: [
    { required: true, message: '请输入版本号', trigger: 'blur' }
  ],
  type: [
    { required: true, message: '请选择BOM类型', trigger: 'change' }
  ]
};

// 组件挂载时获取数据
onMounted(async () => {
  await Promise.all([
    fetchBomList(),
    fetchProducts(),
    fetchMaterials()
  ]);
});

// 获取BOM列表
async function fetchBomList() {
  loading.value = true;
  try {
    const params = {
      page: currentPage.value,
      size: pageSize.value,
      query: searchQuery.value,
      type: bomTypeFilter.value
    };
    const { data } = await bomApi.getBomList(params);
    bomList.value = data.items;
    total.value = data.total;
  } catch (error) {
    console.error('获取物料清单列表失败:', error);
    ElMessage.error('获取物料清单列表失败');
  } finally {
    loading.value = false;
  }
}

// 获取产品列表
async function fetchProducts() {
  try {
    const { data } = await productApi.getProducts({ size: 1000 });
    products.value = data.items;
  } catch (error) {
    console.error('获取产品列表失败:', error);
    ElMessage.error('获取产品列表失败');
  }
}

// 获取物料列表
async function fetchMaterials() {
  try {
    const { data } = await materialApi.getMaterials({ size: 1000 });
    materials.value = data.items;
  } catch (error) {
    console.error('获取物料列表失败:', error);
    ElMessage.error('获取物料列表失败');
  }
}

// 获取BOM版本历史
async function fetchBomVersions(bomId) {
  try {
    const { data } = await bomApi.getBomVersions(bomId);
    bomVersions.value = data;
  } catch (error) {
    console.error('获取BOM版本历史失败:', error);
    ElMessage.error('获取BOM版本历史失败');
  }
}

// 分页处理
function handleSizeChange(val) {
  pageSize.value = val;
  fetchBomList();
}

function handleCurrentChange(val) {
  currentPage.value = val;
  fetchBomList();
}

// 筛选处理
function handleFilterChange() {
  currentPage.value = 1;
  fetchBomList();
}

// 创建BOM
function handleCreateBom() {
  isEdit.value = false;
  resetForm();
  editDialogVisible.value = true;
}

// 查看BOM详情
async function handleViewBom(bom) {
  selectedBom.value = bom;
  activeTab.value = 'list';
  viewDialogVisible.value = true;
  
  try {
    // 获取完整的BOM数据，包括物料项
    const { data } = await bomApi.getBomDetail(bom.id);
    selectedBom.value = data;
    
    // 构建BOM树数据
    prepareBomTreeData(data);
    
    // 获取版本历史
    await fetchBomVersions(bom.id);
  } catch (error) {
    console.error('获取BOM详情失败:', error);
    ElMessage.error('获取BOM详情失败');
  }
}

// 编辑BOM
async function handleEditBom(bom) {
  isEdit.value = true;
  viewDialogVisible.value = false;
  
  try {
    // 获取完整的BOM数据
    const { data } = await bomApi.getBomDetail(bom.id);
    
    // 重置表单
    resetForm();
    
    // 填充表单数据
    Object.assign(bomForm, {
      id: data.id,
      code: data.code,
      product_id: data.product_id,
      product_name: data.product_name,
      product_code: data.product_code,
      version: data.version,
      type: data.type,
      description: data.description,
      is_active: data.is_active,
      remarks: data.remarks,
      items: data.items || []
    });
    
    editDialogVisible.value = true;
  } catch (error) {
    console.error('获取BOM详情失败:', error);
    ElMessage.error('获取BOM详情失败');
  }
}

// 删除BOM
async function handleDeleteBom(id) {
  try {
    await bomApi.deleteBom(id);
    ElMessage.success('删除成功');
    fetchBomList();
  } catch (error) {
    console.error('删除物料清单失败:', error);
    ElMessage.error('删除物料清单失败');
  }
}

// 查看BOM版本
async function viewBomVersion(version) {
  try {
    const { data } = await bomApi.getBomVersionDetail(version.id);
    selectedBom.value = data;
    activeTab.value = 'list';
  } catch (error) {
    console.error('获取BOM版本详情失败:', error);
    ElMessage.error('获取BOM版本详情失败');
  }
}

// 添加物料项
function addItem() {
  bomForm.items.push({
    material_id: '',
    material_code: '',
    material_name: '',
    material_type: '',
    quantity: 1,
    uom: '',
    position: '',
    is_key: false,
    remarks: ''
  });
}

// 移除物料项
function removeItem(index) {
  bomForm.items.splice(index, 1);
}

// 产品选择变更
function handleProductChange(productId) {
  const product = products.value.find(p => p.id === productId);
  if (product) {
    bomForm.product_name = product.name;
    bomForm.product_code = product.code;
    
    // 自动生成BOM编号
    if (!isEdit.value && !bomForm.code) {
      bomForm.code = `BOM-${product.code}-${bomForm.version}`;
    }
  }
}

// 物料选择变更
function handleMaterialChange(materialId, index) {
  const material = materials.value.find(m => m.id === materialId);
  if (material && bomForm.items[index]) {
    bomForm.items[index].material_code = material.code;
    bomForm.items[index].material_name = material.name;
    bomForm.items[index].material_type = material.category;
    bomForm.items[index].uom = material.uom;
  }
}

// 保存BOM
async function saveBom() {
  await bomFormRef.value.validate(async (valid) => {
    if (!valid) return;
    
    // 验证是否有物料项
    if (bomForm.items.length === 0) {
      ElMessage.warning('请至少添加一个物料项');
      return;
    }
    
    // 验证物料项有效性
    for (const item of bomForm.items) {
      if (!item.material_id) {
        ElMessage.warning('物料项信息不完整，请选择物料');
        return;
      }
    }
    
    saveLoading.value = true;
    try {
      if (isEdit.value) {
        await bomApi.updateBom(bomForm.id, bomForm);
        ElMessage.success('更新成功');
      } else {
        await bomApi.createBom(bomForm);
        ElMessage.success('创建成功');
      }
      editDialogVisible.value = false;
      fetchBomList();
    } catch (error) {
      console.error('保存物料清单失败:', error);
      ElMessage.error('保存物料清单失败');
    } finally {
      saveLoading.value = false;
    }
  });
}

// 准备BOM树数据
function prepareBomTreeData(bomData) {
  if (!bomData || !bomData.items || bomData.items.length === 0) {
    bomTreeData.value = [];
    return;
  }
  
  // 构建树结构
  bomTreeData.value = [
    {
      id: bomData.product_id,
      name: bomData.product_name,
      code: bomData.product_code,
      children: bomData.items.map(item => ({
        id: item.material_id,
        name: item.material_name,
        code: item.material_code,
        quantity: item.quantity,
        uom: item.uom
      }))
    }
  ];
}

// 重置表单
function resetForm() {
  if (bomFormRef.value) {
    bomFormRef.value.resetFields();
  }
  
  Object.assign(bomForm, {
    id: null,
    code: '',
    product_id: '',
    product_name: '',
    product_code: '',
    version: '1.0',
    type: 'manufacturing',
    description: '',
    is_active: true,
    remarks: '',
    items: []
  });
}

// 获取BOM类型文本
function getBomTypeText(type) {
  const typeMap = {
    manufacturing: '生产BOM',
    engineering: '工程BOM',
    sales: '销售BOM',
    template: '模板BOM'
  };
  return typeMap[type] || type || '未知';
}

// 获取物料类型文本
function getMaterialTypeText(type) {
  const typeMap = {
    raw_material: '原材料',
    component: '组件',
    semi_finished: '半成品',
    finished: '成品',
    service: '服务'
  };
  return typeMap[type] || type || '未分类';
}
</script>

<style scoped>
.bom-container {
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

.search-filter {
  display: flex;
  gap: 10px;
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

.items-container {
  margin: 20px 0;
}

.items-header {
  margin-bottom: 10px;
  display: flex;
  justify-content: flex-end;
}

.bom-tabs {
  margin-top: 20px;
}

.bom-tree-container {
  padding: 10px;
  max-height: 400px;
  overflow-y: auto;
}

.bom-tree-node {
  display: flex;
  align-items: center;
  font-size: 14px;
}

.node-label {
  font-weight: bold;
  margin-right: 10px;
}

.node-code {
  color: #909399;
  margin-right: 15px;
}

.node-quantity {
  color: #409EFF;
  background-color: #ecf5ff;
  padding: 0 5px;
  border-radius: 4px;
  font-size: 12px;
}

.meta-info {
  margin-top: 20px;
  padding-top: 15px;
  border-top: 1px solid #EBEEF5;
  color: #606266;
  font-size: 14px;
}

.meta-info p {
  margin: 5px 0;
}
</style>
