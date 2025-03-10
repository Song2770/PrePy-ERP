<template>
  <div class="bom-detail-container">
    <div class="page-header">
      <div class="header-left">
        <el-button @click="goBack" plain>
          <el-icon><Back /></el-icon> 返回
        </el-button>
        <h1 class="page-title">物料清单详情</h1>
        <el-tag v-if="bom.type" class="ml-10">{{ getBomTypeText(bom.type) }}</el-tag>
      </div>
      <div class="header-actions">
        <el-button @click="printBom">
          <el-icon><Printer /></el-icon> 打印
        </el-button>
        <el-dropdown trigger="click" @command="handleExport">
          <el-button>
            <el-icon><Download /></el-icon> 导出
            <el-icon class="ml-5"><ArrowDown /></el-icon>
          </el-button>
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item command="excel">导出 Excel</el-dropdown-item>
              <el-dropdown-item command="pdf">导出 PDF</el-dropdown-item>
              <el-dropdown-item command="csv">导出 CSV</el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>
        <el-button type="primary" @click="handleEdit">
          <el-icon><Edit /></el-icon> 编辑
        </el-button>
      </div>
    </div>

    <div v-loading="loading" class="main-content">
      <!-- BOM基本信息 -->
      <el-card class="info-card">
        <el-descriptions :column="3" border size="medium">
          <el-descriptions-item label="BOM编号">{{ bom.code }}</el-descriptions-item>
          <el-descriptions-item label="BOM名称">{{ bom.name || bom.product_name }}</el-descriptions-item>
          <el-descriptions-item label="版本">{{ bom.version }}</el-descriptions-item>
          <el-descriptions-item label="关联产品">
            <el-link @click="viewProduct(bom.product_id)" type="primary">
              {{ bom.product_name }}
            </el-link>
          </el-descriptions-item>
          <el-descriptions-item label="产品编码">{{ bom.product_code }}</el-descriptions-item>
          <el-descriptions-item label="状态">
            <el-tag :type="bom.is_active ? 'success' : 'info'">
              {{ bom.is_active ? '启用' : '禁用' }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="物料数量">{{ bom.items?.length || 0 }} 项</el-descriptions-item>
          <el-descriptions-item label="创建人">{{ bom.created_by }}</el-descriptions-item>
          <el-descriptions-item label="更新时间">{{ bom.updated_at }}</el-descriptions-item>
          <el-descriptions-item label="描述" :span="3">{{ bom.description || '无描述' }}</el-descriptions-item>
        </el-descriptions>
      </el-card>

      <!-- 内容选项卡 -->
      <el-tabs v-model="activeTab" class="content-tabs">
        <el-tab-pane label="物料清单" name="list">
          <el-card class="table-card">
            <template #header>
              <div class="card-header">
                <h3>物料清单项</h3>
                <div class="card-header-actions">
                  <el-input
                    v-model="materialFilter"
                    placeholder="搜索物料"
                    clearable
                    class="filter-input"
                  >
                    <template #prefix>
                      <el-icon><Search /></el-icon>
                    </template>
                  </el-input>
                </div>
              </div>
            </template>
            <el-table
              :data="filteredItems"
              border
              style="width: 100%"
              :default-sort="{ prop: 'sequence', order: 'ascending' }"
            >
              <el-table-column type="expand">
                <template #default="props">
                  <el-form label-position="left" inline class="expand-form">
                    <el-form-item label="物料详情">
                      <div class="material-details">
                        <p><strong>完整描述：</strong> {{ props.row.material_description || '无' }}</p>
                        <p><strong>规格型号：</strong> {{ props.row.material_spec || '无' }}</p>
                        <p><strong>安装位置：</strong> {{ props.row.position || '无' }}</p>
                        <p><strong>备注说明：</strong> {{ props.row.remarks || '无' }}</p>
                      </div>
                    </el-form-item>
                  </el-form>
                </template>
              </el-table-column>
              <el-table-column prop="sequence" label="序号" width="80" align="center" sortable />
              <el-table-column prop="material_code" label="物料编码" min-width="120" sortable />
              <el-table-column prop="material_name" label="物料名称" min-width="150" sortable />
              <el-table-column prop="material_type" label="物料类型" width="120">
                <template #default="scope">
                  <el-tag size="small">{{ getMaterialTypeText(scope.row.material_type) }}</el-tag>
                </template>
              </el-table-column>
              <el-table-column prop="quantity" label="数量" width="100" align="center" sortable />
              <el-table-column prop="uom" label="单位" width="80" align="center" />
              <el-table-column prop="is_key" label="关键件" width="80" align="center">
                <template #default="scope">
                  <el-tag v-if="scope.row.is_key" type="danger" size="small">关键</el-tag>
                  <span v-else>-</span>
                </template>
              </el-table-column>
              <el-table-column prop="cost" label="单价" width="120" align="right">
                <template #default="scope">
                  {{ scope.row.cost ? `¥${scope.row.cost.toFixed(2)}` : '-' }}
                </template>
              </el-table-column>
              <el-table-column prop="total_cost" label="合计" width="120" align="right">
                <template #default="scope">
                  {{ calculateTotalCost(scope.row) }}
                </template>
              </el-table-column>
              <el-table-column label="操作" width="150">
                <template #default="scope">
                  <el-button
                    size="small"
                    type="primary"
                    @click="viewMaterial(scope.row.material_id)"
                    text
                  >
                    <el-icon><View /></el-icon> 查看物料
                  </el-button>
                </template>
              </el-table-column>
            </el-table>

            <div class="summary-info">
              <div class="summary-block">
                <div class="summary-item">
                  <span class="label">物料总数:</span>
                  <span class="value">{{ bom.items?.length || 0 }}</span>
                </div>
                <div class="summary-item">
                  <span class="label">关键物料:</span>
                  <span class="value">{{ keyItemsCount }}</span>
                </div>
                <div class="summary-item">
                  <span class="label">原材料数:</span>
                  <span class="value">{{ rawMaterialCount }}</span>
                </div>
                <div class="summary-item">
                  <span class="label">组件数:</span>
                  <span class="value">{{ componentCount }}</span>
                </div>
              </div>
              <div class="summary-block cost-summary">
                <span class="label">物料总成本:</span>
                <span class="value cost-value">¥{{ totalCost.toFixed(2) }}</span>
              </div>
            </div>
          </el-card>
        </el-tab-pane>

        <el-tab-pane label="结构树视图" name="tree">
          <el-card class="tree-card">
            <template #header>
              <div class="card-header">
                <h3>BOM结构树</h3>
              </div>
            </template>
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
                :expand-on-click-node="false"
              >
                <template #default="{ node, data }">
                  <div class="bom-tree-node">
                    <span class="node-label">{{ data.name }}</span>
                    <span class="node-code">{{ data.code }}</span>
                    <span v-if="data.quantity" class="node-quantity">
                      {{ data.quantity }} {{ data.uom }}
                    </span>
                    <span v-if="data.cost" class="node-cost">
                      ¥{{ data.cost }}
                    </span>
                    <span v-if="data.is_key" class="node-key">
                      <el-tag size="small" type="danger">关键</el-tag>
                    </span>
                  </div>
                </template>
              </el-tree>
              <el-empty v-else description="暂无BOM结构数据" />
            </div>
          </el-card>
        </el-tab-pane>

        <el-tab-pane label="成本分析" name="cost">
          <el-card class="cost-card">
            <template #header>
              <div class="card-header">
                <h3>成本分析</h3>
              </div>
            </template>
            <el-row :gutter="20">
              <el-col :span="12">
                <div class="chart-container">
                  <div class="chart-placeholder">
                    <!-- 这里将来会展示成本分析饼图 -->
                    <el-empty description="成本分析图表暂未生成">
                      <template #description>
                        <p>此处将显示物料成本分布图</p>
                        <p>包括不同类型物料的成本占比</p>
                      </template>
                    </el-empty>
                  </div>
                </div>
              </el-col>
              <el-col :span="12">
                <div class="cost-table-container">
                  <h4>物料成本明细</h4>
                  <el-table :data="costAnalysis" border style="width: 100%">
                    <el-table-column prop="category" label="物料类型" min-width="150" />
                    <el-table-column prop="count" label="数量" width="100" align="center" />
                    <el-table-column prop="cost" label="成本" min-width="120" align="right">
                      <template #default="scope">
                        ¥{{ scope.row.cost.toFixed(2) }}
                      </template>
                    </el-table-column>
                    <el-table-column prop="percentage" label="占比" width="100" align="right">
                      <template #default="scope">
                        {{ scope.row.percentage.toFixed(2) }}%
                      </template>
                    </el-table-column>
                  </el-table>
                </div>
              </el-col>
            </el-row>
          </el-card>
        </el-tab-pane>

        <el-tab-pane label="版本历史" name="versions">
          <el-card class="versions-card">
            <template #header>
              <div class="card-header">
                <h3>版本历史记录</h3>
              </div>
            </template>
            <el-table :data="bomVersions" border style="width: 100%">
              <el-table-column prop="version" label="版本号" width="100" sortable />
              <el-table-column prop="created_at" label="创建时间" min-width="170" sortable />
              <el-table-column prop="created_by" label="创建人" min-width="120" />
              <el-table-column prop="items_count" label="物料数" width="80" align="center" />
              <el-table-column prop="is_active" label="状态" width="100" align="center">
                <template #default="scope">
                  <el-tag :type="scope.row.is_active ? 'success' : 'info'">
                    {{ scope.row.is_active ? '启用' : '禁用' }}
                  </el-tag>
                </template>
              </el-table-column>
              <el-table-column prop="remarks" label="变更说明" min-width="250" show-overflow-tooltip />
              <el-table-column label="操作" width="200">
                <template #default="scope">
                  <el-button
                    size="small"
                    type="primary"
                    @click="viewBomVersion(scope.row)"
                    text
                  >
                    <el-icon><View /></el-icon> 查看
                  </el-button>
                  <el-button
                    size="small"
                    type="info"
                    @click="compareVersions(scope.row)"
                    text
                  >
                    <el-icon><Files /></el-icon> 对比
                  </el-button>
                </template>
              </el-table-column>
            </el-table>
          </el-card>
        </el-tab-pane>
      </el-tabs>
    </div>

    <!-- 版本对比对话框 -->
    <el-dialog
      v-model="compareDialogVisible"
      title="版本对比"
      width="90%"
    >
      <el-descriptions :column="2" border size="small" class="version-compare-header">
        <el-descriptions-item label="当前版本">{{ bom.version }}</el-descriptions-item>
        <el-descriptions-item label="对比版本">{{ compareVersion?.version }}</el-descriptions-item>
        <el-descriptions-item label="创建时间">{{ bom.created_at }}</el-descriptions-item>
        <el-descriptions-item label="创建时间">{{ compareVersion?.created_at }}</el-descriptions-item>
        <el-descriptions-item label="创建人">{{ bom.created_by }}</el-descriptions-item>
        <el-descriptions-item label="创建人">{{ compareVersion?.created_by }}</el-descriptions-item>
      </el-descriptions>

      <div class="compare-content">
        <el-table :data="versionDifferences" border>
          <el-table-column prop="material_code" label="物料编码" min-width="120" />
          <el-table-column prop="material_name" label="物料名称" min-width="150" />
          <el-table-column label="变更类型" width="120" align="center">
            <template #default="scope">
              <el-tag :type="getChangeTypeTag(scope.row.change_type)">
                {{ getChangeTypeText(scope.row.change_type) }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column label="原数量" width="120" align="center">
            <template #default="scope">
              {{ scope.row.old_quantity !== undefined ? `${scope.row.old_quantity} ${scope.row.uom}` : '-' }}
            </template>
          </el-table-column>
          <el-table-column label="新数量" width="120" align="center">
            <template #default="scope">
              {{ scope.row.new_quantity !== undefined ? `${scope.row.new_quantity} ${scope.row.uom}` : '-' }}
            </template>
          </el-table-column>
          <el-table-column label="变更差值" width="120" align="center">
            <template #default="scope">
              <span :class="{ 'text-success': scope.row.quantity_diff > 0, 'text-danger': scope.row.quantity_diff < 0 }">
                {{ scope.row.quantity_diff ? (scope.row.quantity_diff > 0 ? '+' : '') + scope.row.quantity_diff : '-' }}
              </span>
            </template>
          </el-table-column>
        </el-table>
      </div>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed, watch } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { ElMessage, ElMessageBox } from 'element-plus';
import { useBomApi } from '@/api/technical/bom';
import { useProductApi } from '@/api/technical/product';
import { useMaterialApi } from '@/api/technical/material';

// 路由和API
const route = useRoute();
const router = useRouter();
const bomApi = useBomApi();
const productApi = useProductApi();
const materialApi = useMaterialApi();

// 数据
const bom = ref({});
const bomTreeData = ref([]);
const bomVersions = ref([]);
const loading = ref(false);
const activeTab = ref('list');
const materialFilter = ref('');
const compareDialogVisible = ref(false);
const compareVersion = ref(null);
const versionDifferences = ref([]);

// 计算属性 - 过滤后的物料项
const filteredItems = computed(() => {
  if (!bom.value || !bom.value.items) return [];
  
  if (!materialFilter.value) return bom.value.items;
  
  const query = materialFilter.value.toLowerCase();
  return bom.value.items.filter(item => 
    item.material_code.toLowerCase().includes(query) || 
    item.material_name.toLowerCase().includes(query)
  );
});

// 计算属性 - 关键物料数量
const keyItemsCount = computed(() => {
  if (!bom.value || !bom.value.items) return 0;
  return bom.value.items.filter(item => item.is_key).length;
});

// 计算属性 - 原材料数量
const rawMaterialCount = computed(() => {
  if (!bom.value || !bom.value.items) return 0;
  return bom.value.items.filter(item => item.material_type === 'raw_material').length;
});

// 计算属性 - 组件数量
const componentCount = computed(() => {
  if (!bom.value || !bom.value.items) return 0;
  return bom.value.items.filter(item => item.material_type === 'component').length;
});

// 计算属性 - 总成本
const totalCost = computed(() => {
  if (!bom.value || !bom.value.items) return 0;
  
  return bom.value.items.reduce((sum, item) => {
    if (item.cost && item.quantity) {
      return sum + (item.cost * item.quantity);
    }
    return sum;
  }, 0);
});

// 计算属性 - 成本分析
const costAnalysis = computed(() => {
  if (!bom.value || !bom.value.items) return [];
  
  // 按物料类型分组计算成本
  const costByType = {};
  const countByType = {};
  
  for (const item of bom.value.items) {
    const type = item.material_type || 'unknown';
    const typeCost = (item.cost || 0) * (item.quantity || 0);
    
    if (!costByType[type]) {
      costByType[type] = 0;
      countByType[type] = 0;
    }
    
    costByType[type] += typeCost;
    countByType[type] += 1;
  }
  
  const result = [];
  for (const type in costByType) {
    result.push({
      category: getMaterialTypeText(type),
      count: countByType[type],
      cost: costByType[type],
      percentage: totalCost.value ? (costByType[type] / totalCost.value * 100) : 0
    });
  }
  
  // 按成本从高到低排序
  return result.sort((a, b) => b.cost - a.cost);
});

// 组件挂载时获取数据
onMounted(async () => {
  await fetchBomDetail();
});

// 监听路由参数变化
watch(() => route.params.id, async (newId, oldId) => {
  if (newId !== oldId) {
    await fetchBomDetail();
  }
});

// 获取BOM详情
async function fetchBomDetail() {
  const bomId = route.params.id;
  if (!bomId) {
    ElMessage.error('BOM ID不存在');
    router.push('/technical/bom');
    return;
  }
  
  loading.value = true;
  try {
    // 获取完整的BOM数据
    const { data } = await bomApi.getBomDetail(bomId);
    bom.value = data;
    
    // 为物料项添加序号
    if (bom.value.items) {
      bom.value.items.forEach((item, index) => {
        item.sequence = index + 1;
      });
    }
    
    // 构建BOM树数据
    prepareBomTreeData(data);
    
    // 获取版本历史
    await fetchBomVersions(bomId);
  } catch (error) {
    console.error('获取BOM详情失败:', error);
    ElMessage.error('获取BOM详情失败');
  } finally {
    loading.value = false;
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
        uom: item.uom,
        is_key: item.is_key,
        cost: item.cost
      }))
    }
  ];
}

// 计算物料项总成本
function calculateTotalCost(item) {
  if (!item.cost || !item.quantity) return '-';
  return `¥${(item.cost * item.quantity).toFixed(2)}`;
}

// 返回上一页
function goBack() {
  router.go(-1);
}

// 编辑BOM
function handleEdit() {
  router.push(`/technical/bom/edit/${bom.value.id}`);
}

// 查看产品
function viewProduct(productId) {
  router.push(`/technical/products/${productId}`);
}

// 查看物料
function viewMaterial(materialId) {
  router.push(`/technical/materials/${materialId}`);
}

// 查看BOM版本
async function viewBomVersion(version) {
  try {
    const { data } = await bomApi.getBomVersionDetail(version.id);
    bom.value = data;
    activeTab.value = 'list';
  } catch (error) {
    console.error('获取BOM版本详情失败:', error);
    ElMessage.error('获取BOM版本详情失败');
  }
}

// 对比版本
async function compareVersions(versionData) {
  compareVersion.value = versionData;
  
  try {
    const { data } = await bomApi.getBomVersionDetail(versionData.id);
    compareVersion.value = data;
    
    // 计算版本差异
    calculateVersionDifferences(bom.value, data);
    
    compareDialogVisible.value = true;
  } catch (error) {
    console.error('获取对比版本失败:', error);
    ElMessage.error('获取对比版本失败');
  }
}

// 计算版本差异
function calculateVersionDifferences(currentBom, oldBom) {
  if (!currentBom.items || !oldBom.items) {
    versionDifferences.value = [];
    return;
  }
  
  const currentItems = {};
  const oldItems = {};
  const differences = [];
  
  // 构建当前版本物料映射
  currentBom.items.forEach(item => {
    currentItems[item.material_id] = item;
  });
  
  // 构建旧版本物料映射
  oldBom.items.forEach(item => {
    oldItems[item.material_id] = item;
  });
  
  // 查找新增和修改的物料
  for (const materialId in currentItems) {
    const current = currentItems[materialId];
    const old = oldItems[materialId];
    
    if (!old) {
      // 新增物料
      differences.push({
        material_id: materialId,
        material_code: current.material_code,
        material_name: current.material_name,
        uom: current.uom,
        change_type: 'added',
        new_quantity: current.quantity
      });
    } else if (current.quantity !== old.quantity) {
      // 数量变更
      differences.push({
        material_id: materialId,
        material_code: current.material_code,
        material_name: current.material_name,
        uom: current.uom,
        change_type: 'modified',
        old_quantity: old.quantity,
        new_quantity: current.quantity,
        quantity_diff: current.quantity - old.quantity
      });
    }
  }
  
  // 查找删除的物料
  for (const materialId in oldItems) {
    if (!currentItems[materialId]) {
      const old = oldItems[materialId];
      differences.push({
        material_id: materialId,
        material_code: old.material_code,
        material_name: old.material_name,
        uom: old.uom,
        change_type: 'removed',
        old_quantity: old.quantity
      });
    }
  }
  
  versionDifferences.value = differences;
}

// 获取变更类型标签类型
function getChangeTypeTag(changeType) {
  const typeMap = {
    added: 'success',
    removed: 'danger',
    modified: 'warning'
  };
  return typeMap[changeType] || 'info';
}

// 获取变更类型文本
function getChangeTypeText(changeType) {
  const typeMap = {
    added: '新增',
    removed: '删除',
    modified: '修改'
  };
  return typeMap[changeType] || '未知';
}

// 打印BOM
function printBom() {
  ElMessage.info('即将打印物料清单');
  window.print();
}

// 导出BOM
function handleExport(type) {
  ElMessage.success(`正在导出物料清单为 ${type.toUpperCase()} 格式`);
  
  // 这里是导出功能的模拟实现
  // 实际项目中应调用后端API执行导出
  setTimeout(() => {
    const filename = `BOM_${bom.value.code}_${new Date().getTime()}.${type}`;
    ElMessage.success(`导出成功: ${filename}`);
  }, 1500);
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
.bom-detail-container {
  padding: 20px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.header-left {
  display: flex;
  align-items: center;
}

.page-title {
  margin: 0 10px;
  font-size: 24px;
  font-weight: 600;
  color: #303133;
}

.ml-5 {
  margin-left: 5px;
}

.ml-10 {
  margin-left: 10px;
}

.header-actions {
  display: flex;
  gap: 10px;
}

.info-card {
  margin-bottom: 20px;
}

.content-tabs {
  margin-top: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-header h3 {
  margin: 0;
  font-size: 18px;
  font-weight: 600;
  color: #303133;
}

.card-header-actions {
  display: flex;
  align-items: center;
}

.filter-input {
  width: 200px;
}

.table-card, .tree-card, .cost-card, .versions-card {
  margin-bottom: 20px;
}

.expand-form {
  padding: 10px 20px;
}

.material-details p {
  margin: 5px 0;
  line-height: 1.5;
}

.bom-tree-container {
  padding: 10px;
  max-height: 600px;
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
  margin-right: 10px;
}

.node-cost {
  color: #F56C6C;
  margin-right: 10px;
}

.node-key {
  margin-left: 5px;
}

.summary-info {
  margin-top: 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px;
  border-top: 1px solid #EBEEF5;
}

.summary-block {
  display: flex;
  gap: 20px;
}

.summary-item {
  display: flex;
  align-items: center;
}

.summary-item .label {
  color: #606266;
  margin-right: 5px;
}

.summary-item .value {
  font-weight: bold;
  color: #303133;
}

.cost-summary .label {
  font-size: 16px;
  font-weight: bold;
}

.cost-value {
  font-size: 18px;
  color: #F56C6C;
}

.chart-container {
  height: 400px;
  display: flex;
  justify-content: center;
  align-items: center;
}

.chart-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
}

.cost-table-container {
  height: 400px;
  display: flex;
  flex-direction: column;
}

.cost-table-container h4 {
  margin: 0 0 15px 0;
  color: #303133;
}

.version-compare-header {
  margin-bottom: 20px;
}

.compare-content {
  margin-top: 20px;
  max-height: 500px;
  overflow-y: auto;
}

.text-success {
  color: #67C23A;
}

.text-danger {
  color: #F56C6C;
}

@media print {
  .header-actions, .el-tabs__header, .page-header button {
    display: none;
  }
  
  .bom-detail-container {
    padding: 0;
  }
  
  .info-card, .table-card {
    box-shadow: none;
    border: none;
  }
}
</style>
