<template>
  <div class="product-detail-container">
    <div class="page-header">
      <div class="header-left">
        <el-button @click="goBack" plain>
          <el-icon><Back /></el-icon> 返回
        </el-button>
        <h1 class="page-title">{{ product.name || '产品详情' }}</h1>
        <el-tag v-if="product.category" class="ml-10">{{ getCategoryText(product.category) }}</el-tag>
      </div>
      <div class="header-actions">
        <el-button type="primary" @click="handleEdit">
          <el-icon><Edit /></el-icon> 编辑
        </el-button>
      </div>
    </div>

    <div v-loading="loading" class="main-content">
      <el-tabs v-model="activeTab" class="product-tabs">
        <el-tab-pane label="基本信息" name="basic">
          <div class="panel-content">
            <el-row :gutter="20">
              <el-col :span="18">
                <!-- 基本信息卡片 -->
                <el-card class="info-card">
                  <template #header>
                    <div class="card-header">
                      <h3>产品信息</h3>
                    </div>
                  </template>
                  <el-descriptions :column="3" border>
                    <el-descriptions-item label="产品编码">{{ product.code }}</el-descriptions-item>
                    <el-descriptions-item label="产品名称">{{ product.name }}</el-descriptions-item>
                    <el-descriptions-item label="产品型号">{{ product.model }}</el-descriptions-item>
                    <el-descriptions-item label="产品分类">{{ getCategoryText(product.category) }}</el-descriptions-item>
                    <el-descriptions-item label="计量单位">{{ product.uom }}</el-descriptions-item>
                    <el-descriptions-item label="标准成本">
                      {{ product.standard_cost ? `¥${product.standard_cost.toFixed(2)}` : '-' }}
                    </el-descriptions-item>
                    <el-descriptions-item label="创建时间">{{ product.created_at }}</el-descriptions-item>
                    <el-descriptions-item label="更新时间">{{ product.updated_at }}</el-descriptions-item>
                    <el-descriptions-item label="状态">
                      <el-tag :type="product.is_active ? 'success' : 'danger'">
                        {{ product.is_active ? '启用' : '禁用' }}
                      </el-tag>
                    </el-descriptions-item>
                    <el-descriptions-item label="产品描述" :span="3">
                      {{ product.description || '暂无描述' }}
                    </el-descriptions-item>
                  </el-descriptions>
                </el-card>

                <!-- 技术规格卡片 -->
                <el-card class="info-card">
                  <template #header>
                    <div class="card-header">
                      <h3>技术规格</h3>
                    </div>
                  </template>
                  <el-table v-if="product.specifications && product.specifications.length > 0"
                    :data="product.specifications" border style="width: 100%">
                    <el-table-column prop="name" label="规格名称" min-width="150" />
                    <el-table-column prop="value" label="规格值" min-width="200" />
                    <el-table-column prop="unit" label="单位" width="100" />
                    <el-table-column prop="description" label="描述" min-width="250" />
                  </el-table>
                  <el-empty v-else description="暂无技术规格" />
                </el-card>

                <!-- 关联生产路线卡片 -->
                <el-card class="info-card">
                  <template #header>
                    <div class="card-header">
                      <h3>生产路线</h3>
                      <el-button type="primary" size="small" plain @click="goToCreateRoute">
                        <el-icon><Plus /></el-icon> 新建路线
                      </el-button>
                    </div>
                  </template>
                  <el-table v-if="routes && routes.length > 0"
                    :data="routes" border style="width: 100%">
                    <el-table-column prop="code" label="路线编码" min-width="120" />
                    <el-table-column prop="name" label="路线名称" min-width="150" />
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
                    <el-table-column label="操作" width="150" fixed="right">
                      <template #default="scope">
                        <el-button
                          size="small"
                          type="primary"
                          @click="viewRoute(scope.row)"
                          text
                        >
                          <el-icon><View /></el-icon> 查看
                        </el-button>
                      </template>
                    </el-table-column>
                  </el-table>
                  <el-empty v-else description="暂无关联生产路线" />
                </el-card>
              </el-col>

              <el-col :span="6">
                <!-- 产品图片卡片 -->
                <el-card class="info-card">
                  <template #header>
                    <div class="card-header">
                      <h3>产品图片</h3>
                    </div>
                  </template>
                  <div v-if="product.image_url" class="image-container">
                    <el-image
                      :src="product.image_url"
                      fit="contain"
                      :preview-src-list="[product.image_url]"
                      class="product-image"
                    />
                  </div>
                  <el-empty v-else description="暂无产品图片" />
                </el-card>

                <!-- 文档附件卡片 -->
                <el-card class="info-card">
                  <template #header>
                    <div class="card-header">
                      <h3>文档附件</h3>
                    </div>
                  </template>
                  <el-table v-if="product.documents && product.documents.length > 0"
                    :data="product.documents" border style="width: 100%">
                    <el-table-column prop="title" label="文档名称" min-width="200" />
                    <el-table-column prop="type" label="类型" width="120">
                      <template #default="scope">
                        <el-tag size="small">{{ getDocumentTypeText(scope.row.type) }}</el-tag>
                      </template>
                    </el-table-column>
                    <el-table-column label="操作" width="80" fixed="right">
                      <template #default="scope">
                        <el-link :href="scope.row.url" target="_blank" type="primary">
                          <el-icon><Download /></el-icon>
                        </el-link>
                      </template>
                    </el-table-column>
                  </el-table>
                  <el-empty v-else description="暂无文档附件" />
                </el-card>
              </el-col>
            </el-row>
          </div>
        </el-tab-pane>

        <el-tab-pane label="BOM清单" name="bom">
          <div class="panel-content">
            <el-card class="bom-card">
              <template #header>
                <div class="card-header">
                  <h3>物料清单 (BOM)</h3>
                  <div>
                    <el-button type="primary" size="small" plain @click="viewBomTree">
                      <el-icon><Connection /></el-icon> 查看BOM树
                    </el-button>
                    <el-button type="primary" size="small" plain @click="editBom">
                      <el-icon><Edit /></el-icon> 编辑BOM
                    </el-button>
                  </div>
                </div>
              </template>
              
              <el-table v-if="bom && bom.items && bom.items.length > 0"
                :data="bom.items" border style="width: 100%">
                <el-table-column type="index" width="60" align="center" />
                <el-table-column prop="material_code" label="物料编码" min-width="120" />
                <el-table-column prop="material_name" label="物料名称" min-width="150" />
                <el-table-column prop="material_type" label="物料类型" width="120">
                  <template #default="scope">
                    <el-tag size="small">{{ getCategoryText(scope.row.material_type) }}</el-tag>
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
              <el-empty v-else description="暂无BOM信息" />
              
              <div v-if="bom" class="bom-meta">
                <p><strong>BOM版本:</strong> {{ bom.version }}</p>
                <p><strong>BOM类型:</strong> {{ getBomTypeText(bom.type) }}</p>
                <p><strong>创建人:</strong> {{ bom.created_by }}</p>
                <p><strong>更新时间:</strong> {{ bom.updated_at }}</p>
              </div>
            </el-card>
          </div>
        </el-tab-pane>

        <el-tab-pane label="成本分析" name="cost">
          <div class="panel-content">
            <el-row :gutter="20">
              <el-col :span="12">
                <el-card class="info-card">
                  <template #header>
                    <div class="card-header">
                      <h3>成本构成</h3>
                    </div>
                  </template>
                  <div class="chart-container">
                    <!-- 这里将来可以放成本饼图 -->
                    <el-empty description="成本数据暂未生成" />
                  </div>
                </el-card>
              </el-col>
              <el-col :span="12">
                <el-card class="info-card">
                  <template #header>
                    <div class="card-header">
                      <h3>成本明细</h3>
                    </div>
                  </template>
                  <el-table :data="costDetails" border style="width: 100%">
                    <el-table-column prop="category" label="成本类别" min-width="150" />
                    <el-table-column prop="amount" label="金额" min-width="120">
                      <template #default="scope">
                        ¥{{ scope.row.amount.toFixed(2) }}
                      </template>
                    </el-table-column>
                    <el-table-column prop="percentage" label="占比" width="100">
                      <template #default="scope">
                        {{ scope.row.percentage.toFixed(2) }}%
                      </template>
                    </el-table-column>
                  </el-table>
                </el-card>
              </el-col>
            </el-row>
          </div>
        </el-tab-pane>
      </el-tabs>
    </div>

    <!-- BOM树对话框 -->
    <el-dialog
      v-model="bomTreeVisible"
      title="BOM结构树"
      width="80%"
    >
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
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { ElMessage, ElMessageBox } from 'element-plus';
import { useProductApi } from '@/api/technical/product';
import { useRouteApi } from '@/api/technical/productionroute';
import { useBomApi } from '@/api/technical/bom';

// 路由和API
const route = useRoute();
const router = useRouter();
const productApi = useProductApi();
const routeApi = useRouteApi();
const bomApi = useBomApi();

// 数据
const loading = ref(false);
const product = ref({});
const routes = ref([]);
const bom = ref(null);
const bomTreeData = ref([]);
const activeTab = ref('basic');
const bomTreeVisible = ref(false);

// 成本明细模拟数据
const costDetails = ref([
  { category: '材料成本', amount: 120.5, percentage: 60.25 },
  { category: '人工成本', amount: 45.3, percentage: 22.65 },
  { category: '制造费用', amount: 30.2, percentage: 15.10 },
  { category: '其他成本', amount: 4.0, percentage: 2.00 },
]);

// 获取产品信息
async function fetchProduct() {
  loading.value = true;
  try {
    const productId = route.params.id;
    if (!productId) {
      ElMessage.error('产品ID不存在');
      return;
    }
    
    const { data } = await productApi.getProduct(productId);
    product.value = data;
    
    // 获取关联数据
    await Promise.all([
      fetchProductRoutes(productId),
      fetchProductBom(productId)
    ]);
  } catch (error) {
    console.error('获取产品详情失败:', error);
    ElMessage.error('获取产品详情失败');
  } finally {
    loading.value = false;
  }
}

// 获取产品的生产路线
async function fetchProductRoutes(productId) {
  try {
    const { data } = await routeApi.getRoutes({ product_id: productId });
    routes.value = data.items || [];
  } catch (error) {
    console.error('获取生产路线失败:', error);
  }
}

// 获取产品的BOM信息
async function fetchProductBom(productId) {
  try {
    const { data } = await bomApi.getProductBom(productId);
    bom.value = data;
    
    // 如果有BOM数据，准备BOM树数据
    if (data && data.items) {
      prepareBomTreeData(data);
    }
  } catch (error) {
    console.error('获取BOM信息失败:', error);
  }
}

// 准备BOM树数据
function prepareBomTreeData(bomData) {
  // 这里假设API返回的数据中包含了层次结构信息
  // 实际应用中可能需要根据API返回的数据结构进行调整
  if (bomData.tree) {
    bomTreeData.value = bomData.tree;
  } else {
    // 如果没有现成的树结构，可以根据BOM items创建简单的树结构
    bomTreeData.value = [
      {
        id: product.value.id,
        name: product.value.name,
        code: product.value.code,
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
}

// 返回上一页
function goBack() {
  router.go(-1);
}

// 编辑产品
function handleEdit() {
  router.push(`/technical/products/edit/${product.value.id}`);
}

// 查看生产路线
function viewRoute(route) {
  router.push(`/technical/routes/view/${route.id}`);
}

// 新建生产路线
function goToCreateRoute() {
  router.push({
    path: '/technical/routes/create',
    query: { product_id: product.value.id }
  });
}

// 查看BOM树
function viewBomTree() {
  bomTreeVisible.value = true;
}

// 编辑BOM
function editBom() {
  router.push(`/technical/bom/edit/${product.value.id}`);
}

// 获取产品分类文本
function getCategoryText(category) {
  const categoryMap = {
    raw_material: '原材料',
    component: '组件',
    semi_finished: '半成品',
    finished: '成品',
    service: '服务'
  };
  return categoryMap[category] || category || '未分类';
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

// 获取文档类型文本
function getDocumentTypeText(type) {
  const typeMap = {
    spec: '规格说明',
    drawing: '图纸',
    manual: '手册',
    certificate: '证书',
    other: '其他'
  };
  return typeMap[type] || type || '其他';
}

// 获取路线状态类型
function getStatusType(status) {
  const statusMap = {
    draft: 'warning',
    active: 'success',
    inactive: 'info'
  };
  return statusMap[status] || 'info';
}

// 获取路线状态文本
function getStatusText(status) {
  const statusMap = {
    draft: '草稿',
    active: '活跃',
    inactive: '非活跃'
  };
  return statusMap[status] || '未知';
}

// 组件挂载时获取数据
onMounted(() => {
  fetchProduct();
});
</script>

<style scoped>
.product-detail-container {
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

.ml-10 {
  margin-left: 10px;
}

.info-card, .bom-card {
  margin-bottom: 20px;
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

.image-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 200px;
}

.product-image {
  max-height: 100%;
  max-width: 100%;
}

.panel-content {
  padding: 20px 0;
}

.bom-meta {
  margin-top: 20px;
  padding-top: 15px;
  border-top: 1px solid #EBEEF5;
  color: #606266;
  font-size: 14px;
}

.bom-meta p {
  margin: 5px 0;
}

.chart-container {
  height: 300px;
  display: flex;
  justify-content: center;
  align-items: center;
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
}
</style> 