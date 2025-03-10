<template>
    <div class="products-page page-container">
      <div class="page-header">
        <h1 class="page-title">产品管理</h1>
        <el-button type="primary" @click="showAddProductDialog">
          <el-icon><Plus /></el-icon>
          添加产品
        </el-button>
      </div>
  
      <!-- Search & Filters -->
      <el-card class="table-operations">
        <el-row :gutter="20">
          <el-col :xs="24" :sm="8">
            <el-input
              v-model="searchQuery"
              placeholder="搜索产品编码或名称"
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
              v-model="filterCategory"
              placeholder="产品类别"
              clearable
              style="width: 100%"
              @change="handleFilter"
            >
              <el-option label="全部" value="" />
              <el-option label="原材料" value="raw_material" />
              <el-option label="组件" value="component" />
              <el-option label="半成品" value="semi_finished" />
              <el-option label="成品" value="finished" />
              <el-option label="服务" value="service" />
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
  
      <!-- Products Table -->
      <el-card>
        <el-table
          v-loading="loading"
          :data="products"
          border
          style="width: 100%"
          @row-click="handleRowClick"
        >
          <el-table-column prop="code" label="产品编码" min-width="120" />
          <el-table-column prop="name" label="产品名称" min-width="180" />
          <el-table-column label="类别" min-width="100">
            <template #default="scope">
              <el-tag :type="getCategoryTagType(scope.row.category)">
                {{ getCategoryLabel(scope.row.category) }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="unit" label="单位" min-width="80" />
          <el-table-column prop="current_cost" label="成本" min-width="100">
            <template #default="scope">
              {{ formatPrice(scope.row.current_cost) }}
            </template>
          </el-table-column>
          <el-table-column prop="selling_price" label="售价" min-width="100">
            <template #default="scope">
              {{ formatPrice(scope.row.selling_price) }}
            </template>
          </el-table-column>
          <el-table-column label="状态" width="100">
            <template #default="scope">
              <el-tag :type="scope.row.is_active ? 'success' : 'info'">
                {{ scope.row.is_active ? '启用' : '停用' }}
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
            :total="totalProducts"
            @size-change="handleSizeChange"
            @current-change="handleCurrentChange"
          />
        </div>
      </el-card>
  
      <!-- Add/Edit Product Dialog -->
      <el-dialog
        v-model="dialogVisible"
        :title="editMode ? '编辑产品' : '添加产品'"
        width="700px"
      >
        <el-form
          ref="productForm"
          :model="productForm"
          :rules="productRules"
          label-width="100px"
          label-position="right"
        >
          <el-tabs v-model="activeTab">
            <!-- Basic Information Tab -->
            <el-tab-pane label="基本信息" name="basic">
              <el-row :gutter="20">
                <el-col :span="12">
                  <el-form-item label="产品编码" prop="code">
                    <el-input v-model="productForm.code" placeholder="请输入产品编码" />
                  </el-form-item>
                </el-col>
                <el-col :span="12">
                  <el-form-item label="产品名称" prop="name">
                    <el-input v-model="productForm.name" placeholder="请输入产品名称" />
                  </el-form-item>
                </el-col>
              </el-row>
  
              <el-row :gutter="20">
                <el-col :span="12">
                  <el-form-item label="产品类别" prop="category">
                    <el-select v-model="productForm.category" placeholder="请选择产品类别" style="width: 100%">
                      <el-option label="原材料" value="raw_material" />
                      <el-option label="组件" value="component" />
                      <el-option label="半成品" value="semi_finished" />
                      <el-option label="成品" value="finished" />
                      <el-option label="服务" value="service" />
                    </el-select>
                  </el-form-item>
                </el-col>
                <el-col :span="12">
                  <el-form-item label="计量单位" prop="unit">
                    <el-select v-model="productForm.unit" placeholder="请选择计量单位" style="width: 100%">
                      <el-option label="件" value="piece" />
                      <el-option label="千克" value="kg" />
                      <el-option label="米" value="meter" />
                      <el-option label="升" value="liter" />
                      <el-option label="小时" value="hour" />
                      <el-option label="套" value="set" />
                      <el-option label="包" value="package" />
                    </el-select>
                  </el-form-item>
                </el-col>
              </el-row>
  
              <el-form-item label="产品描述" prop="description">
                <el-input
                  v-model="productForm.description"
                  type="textarea"
                  :rows="3"
                  placeholder="请输入产品描述"
                />
              </el-form-item>
  
              <el-row :gutter="20">
                <el-col :span="8">
                  <el-form-item label="条形码" prop="barcode">
                    <el-input v-model="productForm.barcode" placeholder="请输入条形码" />
                  </el-form-item>
                </el-col>
                <el-col :span="8">
                  <el-form-item label="规格" prop="dimensions">
                    <el-input v-model="productForm.dimensions" placeholder="请输入规格" />
                  </el-form-item>
                </el-col>
                <el-col :span="8">
                  <el-form-item label="重量" prop="weight">
                    <el-input-number v-model="productForm.weight" :min="0" style="width: 100%" />
                  </el-form-item>
                </el-col>
              </el-row>
            </el-tab-pane>
  
            <!-- Price & Cost Tab -->
            <el-tab-pane label="价格与成本" name="price">
              <el-row :gutter="20">
                <el-col :span="12">
                  <el-form-item label="标准成本" prop="standard_cost">
                    <el-input-number v-model="productForm.standard_cost" :min="0" :precision="2" style="width: 100%" />
                  </el-form-item>
                </el-col>
                <el-col :span="12">
                  <el-form-item label="当前成本" prop="current_cost">
                    <el-input-number v-model="productForm.current_cost" :min="0" :precision="2" style="width: 100%" />
                  </el-form-item>
                </el-col>
              </el-row>
  
              <el-row :gutter="20">
                <el-col :span="12">
                  <el-form-item label="销售价格" prop="selling_price">
                    <el-input-number v-model="productForm.selling_price" :min="0" :precision="2" style="width: 100%" />
                  </el-form-item>
                </el-col>
                <el-col :span="12">
                  <el-form-item label="最低价格" prop="minimum_price">
                    <el-input-number v-model="productForm.minimum_price" :min="0" :precision="2" style="width: 100%" />
                  </el-form-item>
                </el-col>
              </el-row>
  
              <el-form-item label="税率 (%)" prop="tax_rate">
                <el-input-number v-model="productForm.tax_rate" :min="0" :precision="2" style="width: 100%" />
              </el-form-item>
            </el-tab-pane>
  
            <!-- Inventory Tab -->
            <el-tab-pane label="库存设置" name="inventory">
              <el-row :gutter="20">
                <el-col :span="8">
                  <el-form-item label="最小库存" prop="min_stock_level">
                    <el-input-number v-model="productForm.min_stock_level" :min="0" style="width: 100%" />
                  </el-form-item>
                </el-col>
                <el-col :span="8">
                  <el-form-item label="最大库存" prop="max_stock_level">
                    <el-input-number v-model="productForm.max_stock_level" :min="0" style="width: 100%" />
                  </el-form-item>
                </el-col>
                <el-col :span="8">
                  <el-form-item label="再订货点" prop="reorder_level">
                    <el-input-number v-model="productForm.reorder_level" :min="0" style="width: 100%" />
                  </el-form-item>
                </el-col>
              </el-row>
  
              <el-row :gutter="20">
                <el-col :span="12">
                  <el-form-item label="采购提前期" prop="lead_time">
                    <el-input-number v-model="productForm.lead_time" :min="0" style="width: 100%" />
                    <span class="form-item-hint">天</span>
                  </el-form-item>
                </el-col>
                <el-col :span="12">
                  <el-form-item label="保质期" prop="shelf_life">
                    <el-input-number v-model="productForm.shelf_life" :min="0" style="width: 100%" />
                    <span class="form-item-hint">天</span>
                  </el-form-item>
                </el-col>
              </el-row>
  
              <el-row :gutter="20">
                <el-col :span="8">
                  <el-form-item label="可采购" prop="is_purchasable">
                    <el-switch v-model="productForm.is_purchasable" />
                  </el-form-item>
                </el-col>
                <el-col :span="8">
                  <el-form-item label="可销售" prop="is_sellable">
                    <el-switch v-model="productForm.is_sellable" />
                  </el-form-item>
                </el-col>
                <el-col :span="8">
                  <el-form-item label="可库存" prop="is_stockable">
                    <el-switch v-model="productForm.is_stockable" />
                  </el-form-item>
                </el-col>
              </el-row>
            </el-tab-pane>
  
            <!-- Other Information Tab -->
            <el-tab-pane label="其他信息" name="other">
              <el-form-item label="产品规格" prop="specifications">
                <el-input
                  v-model="productForm.specifications"
                  type="textarea"
                  :rows="3"
                  placeholder="请输入产品规格"
                />
              </el-form-item>
  
              <el-form-item label="备注" prop="notes">
                <el-input
                  v-model="productForm.notes"
                  type="textarea"
                  :rows="3"
                  placeholder="请输入备注"
                />
              </el-form-item>
  
              <el-form-item label="状态" prop="is_active">
                <el-switch
                  v-model="productForm.is_active"
                  active-text="启用"
                  inactive-text="停用"
                />
              </el-form-item>
            </el-tab-pane>
          </el-tabs>
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
  
      <!-- Product Details Dialog -->
      <el-dialog v-model="detailsVisible" title="产品详情" width="700px">
        <el-descriptions
          v-if="selectedProduct"
          :column="2"
          border
        >
          <el-descriptions-item label="产品编码">{{ selectedProduct.code }}</el-descriptions-item>
          <el-descriptions-item label="产品名称">{{ selectedProduct.name }}</el-descriptions-item>
          <el-descriptions-item label="产品类别">{{ getCategoryLabel(selectedProduct.category) }}</el-descriptions-item>
          <el-descriptions-item label="计量单位">{{ getUnitLabel(selectedProduct.unit) }}</el-descriptions-item>
          <el-descriptions-item label="标准成本">{{ formatPrice(selectedProduct.standard_cost) }}</el-descriptions-item>
          <el-descriptions-item label="当前成本">{{ formatPrice(selectedProduct.current_cost) }}</el-descriptions-item>
          <el-descriptions-item label="销售价格">{{ formatPrice(selectedProduct.selling_price) }}</el-descriptions-item>
          <el-descriptions-item label="最低价格">{{ formatPrice(selectedProduct.minimum_price) }}</el-descriptions-item>
          <el-descriptions-item label="税率">{{ selectedProduct.tax_rate }}%</el-descriptions-item>
          <el-descriptions-item label="条形码">{{ selectedProduct.barcode }}</el-descriptions-item>
          <el-descriptions-item label="规格">{{ selectedProduct.dimensions }}</el-descriptions-item>
          <el-descriptions-item label="重量">{{ selectedProduct.weight }}</el-descriptions-item>
          <el-descriptions-item label="最小库存">{{ selectedProduct.min_stock_level }}</el-descriptions-item>
          <el-descriptions-item label="最大库存">{{ selectedProduct.max_stock_level }}</el-descriptions-item>
          <el-descriptions-item label="再订货点">{{ selectedProduct.reorder_level }}</el-descriptions-item>
          <el-descriptions-item label="采购提前期">{{ selectedProduct.lead_time }} 天</el-descriptions-item>
          <el-descriptions-item label="保质期">{{ selectedProduct.shelf_life }} 天</el-descriptions-item>
          <el-descriptions-item label="状态">
            <el-tag :type="selectedProduct.is_active ? 'success' : 'info'">
              {{ selectedProduct.is_active ? '启用' : '停用' }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="可采购">
            <el-tag :type="selectedProduct.is_purchasable ? 'success' : 'info'">
              {{ selectedProduct.is_purchasable ? '是' : '否' }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="可销售">
            <el-tag :type="selectedProduct.is_sellable ? 'success' : 'info'">
              {{ selectedProduct.is_sellable ? '是' : '否' }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="可库存">
            <el-tag :type="selectedProduct.is_stockable ? 'success' : 'info'">
              {{ selectedProduct.is_stockable ? '是' : '否' }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="产品描述" :span="2">{{ selectedProduct.description }}</el-descriptions-item>
          <el-descriptions-item label="产品规格" :span="2">{{ selectedProduct.specifications }}</el-descriptions-item>
          <el-descriptions-item label="备注" :span="2">{{ selectedProduct.notes }}</el-descriptions-item>
        </el-descriptions>
  
        <template #footer>
          <span class="dialog-footer">
            <el-button @click="detailsVisible = false">关闭</el-button>
            <el-button type="primary" @click="handleEdit(selectedProduct)">编辑</el-button>
          </span>
        </template>
      </el-dialog>
    </div>
  </template>
  
  <script>
  import { defineComponent, ref, reactive, onMounted, computed } from 'vue';
  import { ElMessage, ElMessageBox } from 'element-plus';
  
  export default defineComponent({
    name: 'ProductsPage',
    setup() {
      // State
      const loading = ref(false);
      const submitting = ref(false);
      const products = ref([]);
      const totalProducts = ref(0);
      const currentPage = ref(1);
      const pageSize = ref(10);
      const searchQuery = ref('');
      const filterCategory = ref('');
      const dialogVisible = ref(false);
      const detailsVisible = ref(false);
      const editMode = ref(false);
      const selectedProduct = ref(null);
      const productForm = ref(null);
      const activeTab = ref('basic');
  
      // Form default values and rules
      const form = reactive({
        code: '',
        name: '',
        category: 'finished',
        description: '',
        unit: 'piece',
        standard_cost: 0,
        current_cost: 0,
        selling_price: 0,
        minimum_price: 0,
        tax_rate: 13.0,
        barcode: '',
        specifications: '',
        dimensions: '',
        weight: 0,
        weight_unit: 'kg',
        image_url: '',
        is_active: true,
        is_purchasable: true,
        is_sellable: true,
        is_stockable: true,
        min_stock_level: 0,
        max_stock_level: 0,
        reorder_level: 0,
        lead_time: 0,
        shelf_life: 0,
        notes: ''
      });
  
      const productRules = {
        code: [
          { required: true, message: '请输入产品编码', trigger: 'blur' },
          { min: 3, max: 20, message: '长度在 3 到 20 个字符', trigger: 'blur' }
        ],
        name: [
          { required: true, message: '请输入产品名称', trigger: 'blur' },
          { min: 2, max: 100, message: '长度在 2 到 100 个字符', trigger: 'blur' }
        ],
        category: [
          { required: true, message: '请选择产品类别', trigger: 'change' }
        ],
        unit: [
          { required: true, message: '请选择计量单位', trigger: 'change' }
        ]
      };
  
      // Helper functions for displaying category and unit labels
      const getCategoryLabel = (category) => {
        const categoryMap = {
          'raw_material': '原材料',
          'component': '组件',
          'semi_finished': '半成品',
          'finished': '成品',
          'service': '服务'
        };
        return categoryMap[category] || category;
      };
  
      const getUnitLabel = (unit) => {
        const unitMap = {
          'piece': '件',
          'kg': '千克',
          'meter': '米',
          'liter': '升',
          'hour': '小时',
          'set': '套',
          'package': '包'
        };
        return unitMap[unit] || unit;
      };
  
      const getCategoryTagType = (category) => {
        const typeMap = {
          'raw_material': 'info',
          'component': 'warning',
          'semi_finished': 'success',
          'finished': 'primary',
          'service': ''
        };
        return typeMap[category] || '';
      };
  
      const formatPrice = (price) => {
        return '¥' + parseFloat(price).toFixed(2);
      };
  
      // Methods
      const loadProducts = async () => {
        loading.value = true;
        try {
          const params = {
            skip: (currentPage.value - 1) * pageSize.value,
            limit: pageSize.value,
            search: searchQuery.value,
            category: filterCategory.value
          };
          
          // In a real app, we would call the API
          // const response = await fetchProducts(params);
          // products.value = response;
          // totalProducts.value = response.total;
          
          // For demo purposes, use dummy data
          products.value = [
            {
              id: 1,
              code: 'RM001',
              name: '钢板',
              category: 'raw_material',
              description: '高质量钢板',
              unit: 'kg',
              standard_cost: 5.0,
              current_cost: 5.5,
              selling_price: 8.0,
              minimum_price: 6.0,
              tax_rate: 13.0,
              barcode: '6901234567890',
              specifications: '优质钢板，用于各类工业产品的制造',
              dimensions: '1000x2000x3mm',
              weight: 10.5,
              weight_unit: 'kg',
              is_active: true,
              is_purchasable: true,
              is_sellable: true,
              is_stockable: true,
              min_stock_level: 100,
              max_stock_level: 1000,
              reorder_level: 200,
              lead_time: 7,
              shelf_life: 365,
              notes: '常规库存物料'
            },
            {
              id: 2,
              code: 'COMP001',
              name: '电动机',
              category: 'component',
              description: '250W电动机',
              unit: 'piece',
              standard_cost: 50.0,
              current_cost: 52.0,
              selling_price: 75.0,
              minimum_price: 60.0,
              tax_rate: 13.0,
              barcode: '6901234567891',
              specifications: '250W/220V/50Hz电动机',
              dimensions: '120x80x60mm',
              weight: 2.5,
              weight_unit: 'kg',
              is_active: true,
              is_purchasable: true,
              is_sellable: true,
              is_stockable: true,
              min_stock_level: 20,
              max_stock_level: 100,
              reorder_level: 30,
              lead_time: 14,
              shelf_life: 730,
              notes: '核心部件'
            },
            {
              id: 3,
              code: 'FP001',
              name: '工业风扇',
              category: 'finished',
              description: '工业级冷却风扇',
              unit: 'piece',
              standard_cost: 200.0,
              current_cost: 210.0,
              selling_price: 350.0,
              minimum_price: 250.0,
              tax_rate: 13.0,
              barcode: '6901234567892',
              specifications: '大功率工业冷却风扇，适用于工厂、仓库等场所',
              dimensions: '600x600x450mm',
              weight: 15.0,
              weight_unit: 'kg',
              is_active: true,
              is_purchasable: false,
              is_sellable: true,
              is_stockable: true,
              min_stock_level: 5,
              max_stock_level: 30,
              reorder_level: 10,
              lead_time: 5,
              shelf_life: 1825,
              notes: '我们的旗舰产品'
            }
          ];
          totalProducts.value = 3;
        } catch (error) {
          console.error('Error loading products:', error);
          ElMessage.error('加载产品数据失败');
        } finally {
          loading.value = false;
        }
      };
  
      const handleSearch = () => {
        currentPage.value = 1;
        loadProducts();
      };
  
      const handleFilter = () => {
        currentPage.value = 1;
        loadProducts();
      };
  
      const resetFilter = () => {
        searchQuery.value = '';
        filterCategory.value = '';
        currentPage.value = 1;
        loadProducts();
      };
  
      const handleSizeChange = (val) => {
        pageSize.value = val;
        loadProducts();
      };
  
      const handleCurrentChange = (val) => {
        currentPage.value = val;
        loadProducts();
      };
  
      const resetForm = () => {
        Object.keys(form).forEach(key => {
          switch (key) {
            case 'category':
              form[key] = 'finished';
              break;
            case 'unit':
              form[key] = 'piece';
              break;
            case 'tax_rate':
              form[key] = 13.0;
              break;
            case 'weight_unit':
              form[key] = 'kg';
              break;
            case 'is_active':
            case 'is_purchasable':
            case 'is_sellable':
            case 'is_stockable':
              form[key] = true;
              break;
            case 'standard_cost':
            case 'current_cost':
            case 'selling_price':
            case 'minimum_price':
            case 'weight':
            case 'min_stock_level':
            case 'max_stock_level':
            case 'reorder_level':
            case 'lead_time':
            case 'shelf_life':
              form[key] = 0;
              break;
            default:
              form[key] = '';
          }
        });
        activeTab.value = 'basic';
      };
  
      const showAddProductDialog = () => {
        resetForm();
        editMode.value = false;
        dialogVisible.value = true;
      };
  
      const handleRowClick = (row) => {
        selectedProduct.value = row;
        detailsVisible.value = true;
      };
  
      const handleEdit = (product) => {
        editMode.value = true;
        Object.keys(form).forEach(key => {
          if (key in product) {
            form[key] = product[key];
          }
        });
        dialogVisible.value = true;
        detailsVisible.value = false;
      };
  
      const handleDelete = (product) => {
        ElMessageBox.confirm(
          `确定要删除产品 "${product.name}" 吗?`,
          '警告',
          {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning',
          }
        ).then(async () => {
          try {
            // In a real app, we would call the API
            // await deleteProduct(product.id);
            
            ElMessage.success('删除成功');
            loadProducts();
          } catch (error) {
            console.error('Error deleting product:', error);
            ElMessage.error('删除失败');
          }
        }).catch(() => {
          // User cancelled
        });
      };
  
      const submitForm = async () => {
        if (!productForm.value) return;
        
        await productForm.value.validate(async (valid) => {
          if (valid) {
            submitting.value = true;
            
            try {
              if (editMode.value) {
                // In a real app, we would call the API
                // await updateProduct(selectedProduct.value.id, form);
                ElMessage.success('产品信息更新成功');
              } else {
                // In a real app, we would call the API
                // await createProduct(form);
                ElMessage.success('产品添加成功');
              }
              
              dialogVisible.value = false;
              loadProducts();
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
        loadProducts();
      });
  
      return {
        // State
        loading,
        submitting,
        products,
        totalProducts,
        currentPage,
        pageSize,
        searchQuery,
        filterCategory,
        dialogVisible,
        detailsVisible,
        editMode,
        selectedProduct,
        productForm,
        productRules,
        activeTab,
        
        // Methods
        getCategoryLabel,
        getUnitLabel,
        getCategoryTagType,
        formatPrice,
        handleSearch,
        handleFilter,
        resetFilter,
        handleSizeChange,
        handleCurrentChange,
        showAddProductDialog,
        handleRowClick,
        handleEdit,
        handleDelete,
        submitForm,
        
        // Form data
        productForm: form
      };
    }
  });
  </script>
  
  <style scoped>
  .products-page {
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
  
  .form-item-hint {
    margin-left: 8px;
    color: #909399;
    font-size: 12px;
  }
  </style>