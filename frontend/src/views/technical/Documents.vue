<template>
  <div class="documents-container">
    <h1 class="page-title">技术文档管理</h1>

    <!-- 操作区 -->
    <div class="page-actions">
      <div class="left-actions">
        <el-button type="primary" @click="handleUploadDocument">
          <el-icon><Upload /></el-icon> 上传文档
        </el-button>
        <el-button @click="handleCreateFolder">
          <el-icon><Folder /></el-icon> 新建文件夹
        </el-button>
      </div>
      <div class="right-actions">
        <el-input
          v-model="searchQuery"
          placeholder="搜索文档"
          class="search-input"
          clearable
          @clear="fetchDocuments"
          @input="handleSearch"
        >
          <template #prefix>
            <el-icon><Search /></el-icon>
          </template>
        </el-input>
        <el-select v-model="docTypeFilter" placeholder="文档类型" clearable @change="handleFilterChange">
          <el-option label="全部" value="" />
          <el-option label="规格说明" value="spec" />
          <el-option label="图纸" value="drawing" />
          <el-option label="手册" value="manual" />
          <el-option label="证书" value="certificate" />
          <el-option label="其他" value="other" />
        </el-select>
      </div>
    </div>

    <!-- 文件夹导航 -->
    <div class="folder-nav">
      <el-breadcrumb separator="/">
        <el-breadcrumb-item :to="{ path: '' }" @click="navigateToRoot">根目录</el-breadcrumb-item>
        <el-breadcrumb-item 
          v-for="(folder, index) in folderPath" 
          :key="index" 
          :to="{ path: '' }" 
          @click="navigateToFolder(index)"
        >
          {{ folder.name }}
        </el-breadcrumb-item>
      </el-breadcrumb>
    </div>

    <!-- 文档列表 -->
    <el-card shadow="never" class="list-card">
      <div v-loading="loading">
        <!-- 文件夹列表 -->
        <div v-if="folders.length > 0" class="folder-list">
          <el-row :gutter="20">
            <el-col :xs="24" :sm="12" :md="8" :lg="6" v-for="folder in folders" :key="folder.id">
              <div class="folder-item" @click="openFolder(folder)">
                <el-icon><Folder /></el-icon>
                <span class="folder-name">{{ folder.name }}</span>
                <div class="folder-actions">
                  <el-dropdown trigger="click" @click.stop>
                    <el-icon><More /></el-icon>
                    <template #dropdown>
                      <el-dropdown-menu>
                        <el-dropdown-item @click="renameFolder(folder)">
                          <el-icon><Edit /></el-icon> 重命名
                        </el-dropdown-item>
                        <el-dropdown-item @click="deleteFolder(folder)" class="danger-item">
                          <el-icon><Delete /></el-icon> 删除
                        </el-dropdown-item>
                      </el-dropdown-menu>
                    </template>
                  </el-dropdown>
                </div>
              </div>
            </el-col>
          </el-row>
        </div>

        <el-table
          :data="documents"
          border
          style="width: 100%"
        >
          <el-table-column prop="title" label="文档名称" min-width="200">
            <template #default="scope">
              <div class="doc-name-cell">
                <el-icon class="doc-icon">
                  <component :is="getDocumentIcon(scope.row.type)" />
                </el-icon>
                <span>{{ scope.row.title }}</span>
              </div>
            </template>
          </el-table-column>
          <el-table-column prop="type" label="类型" width="120">
            <template #default="scope">
              <el-tag size="small">{{ getDocumentTypeText(scope.row.type) }}</el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="related_product" label="关联产品" min-width="200">
            <template #default="scope">
              <el-link v-if="scope.row.product_id" @click="viewProduct(scope.row.product_id)" type="primary">
                {{ scope.row.product_name }}
              </el-link>
              <span v-else>-</span>
            </template>
          </el-table-column>
          <el-table-column prop="version" label="版本" width="100" />
          <el-table-column prop="created_by" label="创建人" width="120" />
          <el-table-column prop="created_at" label="创建时间" width="170" sortable />
          <el-table-column prop="file_size" label="文件大小" width="120">
            <template #default="scope">
              {{ formatFileSize(scope.row.file_size) }}
            </template>
          </el-table-column>
          <el-table-column label="操作" width="220" fixed="right">
            <template #default="scope">
              <el-button
                size="small"
                type="primary"
                @click="previewDocument(scope.row)"
                text
              >
                <el-icon><View /></el-icon> 预览
              </el-button>
              <el-button
                size="small"
                type="primary"
                @click="downloadDocument(scope.row)"
                text
              >
                <el-icon><Download /></el-icon> 下载
              </el-button>
              <el-dropdown trigger="click">
                <el-button
                  size="small"
                  text
                >
                  <el-icon><More /></el-icon>
                </el-button>
                <template #dropdown>
                  <el-dropdown-menu>
                    <el-dropdown-item @click="editDocument(scope.row)">
                      <el-icon><Edit /></el-icon> 编辑
                    </el-dropdown-item>
                    <el-dropdown-item @click="relateToProduct(scope.row)">
                      <el-icon><Link /></el-icon> 关联产品
                    </el-dropdown-item>
                    <el-dropdown-item @click="moveDocument(scope.row)">
                      <el-icon><FolderOpened /></el-icon> 移动
                    </el-dropdown-item>
                    <el-dropdown-item @click="deleteDocument(scope.row)" class="danger-item">
                      <el-icon><Delete /></el-icon> 删除
                    </el-dropdown-item>
                  </el-dropdown-menu>
                </template>
              </el-dropdown>
            </template>
          </el-table-column>
        </el-table>

        <!-- 空状态 -->
        <el-empty v-if="folders.length === 0 && documents.length === 0" description="暂无文档" />

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
      </div>
    </el-card>

    <!-- 上传文档对话框 -->
    <el-dialog
      v-model="uploadDialogVisible"
      title="上传文档"
      width="600px"
    >
      <el-form
        ref="uploadFormRef"
        :model="uploadForm"
        :rules="uploadRules"
        label-width="100px"
      >
        <el-form-item label="文档标题" prop="title">
          <el-input v-model="uploadForm.title" placeholder="请输入文档标题" />
        </el-form-item>
        <el-form-item label="文档类型" prop="type">
          <el-select v-model="uploadForm.type" placeholder="请选择文档类型" style="width: 100%">
            <el-option label="规格说明" value="spec" />
            <el-option label="图纸" value="drawing" />
            <el-option label="手册" value="manual" />
            <el-option label="证书" value="certificate" />
            <el-option label="其他" value="other" />
          </el-select>
        </el-form-item>
        <el-form-item label="版本" prop="version">
          <el-input v-model="uploadForm.version" placeholder="请输入版本号" />
        </el-form-item>
        <el-form-item label="关联产品">
          <el-select
            v-model="uploadForm.product_id"
            placeholder="请选择关联产品"
            filterable
            clearable
            style="width: 100%"
          >
            <el-option
              v-for="product in products"
              :key="product.id"
              :label="product.name"
              :value="product.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="描述">
          <el-input
            v-model="uploadForm.description"
            type="textarea"
            rows="3"
            placeholder="请输入文档描述"
          />
        </el-form-item>
        <el-form-item label="文档文件" prop="file">
          <el-upload
            ref="uploadRef"
            class="document-upload"
            action="#"
            :auto-upload="false"
            :limit="1"
            :on-change="handleFileChange"
            :on-exceed="handleExceed"
            :file-list="fileList"
          >
            <template #trigger>
              <el-button type="primary">选择文件</el-button>
            </template>
            <template #tip>
              <div class="el-upload__tip">支持的文件格式：PDF, Word, Excel, CAD, 图片等</div>
            </template>
          </el-upload>
        </el-form-item>
      </el-form>
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="uploadDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="submitUpload" :loading="uploading">
            上传
          </el-button>
        </div>
      </template>
    </el-dialog>

    <!-- 新建文件夹对话框 -->
    <el-dialog
      v-model="folderDialogVisible"
      title="新建文件夹"
      width="500px"
    >
      <el-form
        ref="folderFormRef"
        :model="folderForm"
        :rules="folderRules"
        label-width="100px"
      >
        <el-form-item label="文件夹名称" prop="name">
          <el-input v-model="folderForm.name" placeholder="请输入文件夹名称" />
        </el-form-item>
        <el-form-item label="描述">
          <el-input
            v-model="folderForm.description"
            type="textarea"
            rows="3"
            placeholder="请输入文件夹描述"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="folderDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="submitFolder" :loading="savingFolder">
            创建
          </el-button>
        </div>
      </template>
    </el-dialog>

    <!-- 文档预览对话框 -->
    <el-dialog
      v-model="previewDialogVisible"
      :title="selectedDocument ? selectedDocument.title : '文档预览'"
      width="80%"
      fullscreen
    >
      <div v-if="selectedDocument" class="preview-container">
        <div v-if="isPreviewSupported(selectedDocument.file_ext)" class="document-preview">
          <iframe :src="selectedDocument.preview_url" frameborder="0" class="preview-frame"></iframe>
        </div>
        <div v-else class="preview-not-supported">
          <el-empty description="此文件类型不支持在线预览">
            <template #extra>
              <el-button type="primary" @click="downloadDocument(selectedDocument)">
                下载文件
              </el-button>
            </template>
          </el-empty>
        </div>
      </div>
    </el-dialog>

    <!-- 关联产品对话框 -->
    <el-dialog
      v-model="relateDialogVisible"
      title="关联产品"
      width="500px"
    >
      <el-form
        ref="relateFormRef"
        :model="relateForm"
        label-width="100px"
      >
        <el-form-item label="文档">
          <el-input v-model="relateForm.document_title" disabled />
        </el-form-item>
        <el-form-item label="关联产品" prop="product_id">
          <el-select
            v-model="relateForm.product_id"
            placeholder="请选择关联产品"
            filterable
            style="width: 100%"
          >
            <el-option
              v-for="product in products"
              :key="product.id"
              :label="product.name"
              :value="product.id"
            />
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="relateDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="submitRelation" :loading="savingRelation">
            保存
          </el-button>
        </div>
      </template>
    </el-dialog>

    <!-- 移动文档对话框 -->
    <el-dialog
      v-model="moveDialogVisible"
      title="移动文档"
      width="500px"
    >
      <el-form
        ref="moveFormRef"
        :model="moveForm"
        label-width="100px"
      >
        <el-form-item label="文档">
          <el-input v-model="moveForm.document_title" disabled />
        </el-form-item>
        <el-form-item label="目标文件夹" prop="folder_id">
          <el-tree
            ref="folderTreeRef"
            :data="folderTree"
            node-key="id"
            :props="{
              label: 'name',
              children: 'children'
            }"
            highlight-current
            @node-click="handleFolderSelect"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="moveDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="submitMove" :loading="movingDocument">
            移动
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
import { 
  Document, Files, PictureRounded, Postcard, Tickets, 
  DocumentCopy, View, Download, Upload, Delete, Edit, 
  Folder, FolderOpened, More, Link, Search 
} from '@element-plus/icons-vue';
import { useDocumentApi } from '@/api/technical/document';
import { useProductApi } from '@/api/technical/product';

// 路由和API
const router = useRouter();
const documentApi = useDocumentApi();
const productApi = useProductApi();

// 数据
const loading = ref(false);
const documents = ref([]);
const folders = ref([]);
const folderPath = ref([]);
const folderTree = ref([]);
const products = ref([]);
const currentPage = ref(1);
const pageSize = ref(20);
const total = ref(0);
const searchQuery = ref('');
const docTypeFilter = ref('');
const currentFolderId = ref(null);

// 对话框状态
const uploadDialogVisible = ref(false);
const folderDialogVisible = ref(false);
const previewDialogVisible = ref(false);
const relateDialogVisible = ref(false);
const moveDialogVisible = ref(false);
const uploading = ref(false);
const savingFolder = ref(false);
const savingRelation = ref(false);
const movingDocument = ref(false);

// 选中的文档
const selectedDocument = ref(null);

// 文件上传
const uploadRef = ref(null);
const uploadFormRef = ref(null);
const fileList = ref([]);
const uploadForm = reactive({
  title: '',
  type: '',
  version: '1.0',
  product_id: '',
  description: '',
  folder_id: null,
  file: null
});

// 文件夹表单
const folderFormRef = ref(null);
const folderForm = reactive({
  name: '',
  description: '',
  parent_id: null
});

// 关联产品表单
const relateFormRef = ref(null);
const relateForm = reactive({
  document_id: '',
  document_title: '',
  product_id: ''
});

// 移动文档表单
const moveFormRef = ref(null);
const folderTreeRef = ref(null);
const moveForm = reactive({
  document_id: '',
  document_title: '',
  folder_id: null
});

// 表单校验规则
const uploadRules = {
  title: [
    { required: true, message: '请输入文档标题', trigger: 'blur' },
    { min: 2, max: 100, message: '长度在 2 到 100 个字符', trigger: 'blur' }
  ],
  type: [
    { required: true, message: '请选择文档类型', trigger: 'change' }
  ],
  version: [
    { required: true, message: '请输入版本号', trigger: 'blur' }
  ],
  file: [
    { required: true, message: '请选择要上传的文件', trigger: 'change' }
  ]
};

const folderRules = {
  name: [
    { required: true, message: '请输入文件夹名称', trigger: 'blur' },
    { min: 2, max: 50, message: '长度在 2 到 50 个字符', trigger: 'blur' }
  ]
};

// 组件挂载时获取数据
onMounted(async () => {
  await Promise.all([
    fetchDocuments(),
    fetchFolders(),
    fetchFolderTree(),
    fetchProducts()
  ]);
});

// 获取文档列表
async function fetchDocuments() {
  loading.value = true;
  try {
    const params = {
      page: currentPage.value,
      size: pageSize.value,
      query: searchQuery.value,
      type: docTypeFilter.value,
      folder_id: currentFolderId.value
    };
    const { data } = await documentApi.getDocuments(params);
    documents.value = data.items;
    total.value = data.total;
  } catch (error) {
    console.error('获取文档列表失败:', error);
    ElMessage.error('获取文档列表失败');
  } finally {
    loading.value = false;
  }
}

// 获取文件夹列表
async function fetchFolders() {
  try {
    const params = {
      parent_id: currentFolderId.value
    };
    const { data } = await documentApi.getFolders(params);
    folders.value = data;
  } catch (error) {
    console.error('获取文件夹列表失败:', error);
    ElMessage.error('获取文件夹列表失败');
  }
}

// 获取文件夹树
async function fetchFolderTree() {
  try {
    const { data } = await documentApi.getFolderTree();
    folderTree.value = [
      {
        id: null,
        name: '根目录',
        children: data
      }
    ];
  } catch (error) {
    console.error('获取文件夹树失败:', error);
  }
}

// 获取产品列表
async function fetchProducts() {
  try {
    const { data } = await productApi.getProducts({ size: 1000 });
    products.value = data.items;
  } catch (error) {
    console.error('获取产品列表失败:', error);
  }
}

// 分页处理
function handleSizeChange(val) {
  pageSize.value = val;
  fetchDocuments();
}

function handleCurrentChange(val) {
  currentPage.value = val;
  fetchDocuments();
}

// 搜索和筛选
function handleSearch() {
  currentPage.value = 1;
  fetchDocuments();
}

function handleFilterChange() {
  currentPage.value = 1;
  fetchDocuments();
}

// 文件夹导航
function navigateToRoot() {
  currentFolderId.value = null;
  folderPath.value = [];
  fetchDocuments();
  fetchFolders();
}

function navigateToFolder(index) {
  if (index < folderPath.value.length - 1) {
    const targetFolder = folderPath.value[index];
    currentFolderId.value = targetFolder.id;
    folderPath.value = folderPath.value.slice(0, index + 1);
    fetchDocuments();
    fetchFolders();
  }
}

function openFolder(folder) {
  currentFolderId.value = folder.id;
  folderPath.value.push({ id: folder.id, name: folder.name });
  fetchDocuments();
  fetchFolders();
}

// 文件操作
function handleUploadDocument() {
  resetUploadForm();
  uploadForm.folder_id = currentFolderId.value;
  uploadDialogVisible.value = true;
}

function handleCreateFolder() {
  resetFolderForm();
  folderForm.parent_id = currentFolderId.value;
  folderDialogVisible.value = true;
}

function handleFileChange(file) {
  uploadForm.file = file.raw;
}

function handleExceed() {
  ElMessage.warning('只能上传一个文件');
}

function resetUploadForm() {
  if (uploadFormRef.value) {
    uploadFormRef.value.resetFields();
  }
  fileList.value = [];
  Object.assign(uploadForm, {
    title: '',
    type: '',
    version: '1.0',
    product_id: '',
    description: '',
    folder_id: null,
    file: null
  });
}

function resetFolderForm() {
  if (folderFormRef.value) {
    folderFormRef.value.resetFields();
  }
  Object.assign(folderForm, {
    name: '',
    description: '',
    parent_id: null
  });
}

// 提交上传
async function submitUpload() {
  if (!uploadForm.file) {
    ElMessage.warning('请选择要上传的文件');
    return;
  }
  
  await uploadFormRef.value.validate(async (valid) => {
    if (!valid) return;
    
    uploading.value = true;
    try {
      const formData = new FormData();
      formData.append('file', uploadForm.file);
      formData.append('title', uploadForm.title);
      formData.append('type', uploadForm.type);
      formData.append('version', uploadForm.version);
      
      if (uploadForm.description) {
        formData.append('description', uploadForm.description);
      }
      
      if (uploadForm.product_id) {
        formData.append('product_id', uploadForm.product_id);
      }
      
      if (uploadForm.folder_id) {
        formData.append('folder_id', uploadForm.folder_id);
      }
      
      await documentApi.uploadDocument(formData);
      ElMessage.success('文档上传成功');
      uploadDialogVisible.value = false;
      fetchDocuments();
    } catch (error) {
      console.error('上传文档失败:', error);
      ElMessage.error('上传文档失败');
    } finally {
      uploading.value = false;
    }
  });
}

// 提交文件夹
async function submitFolder() {
  await folderFormRef.value.validate(async (valid) => {
    if (!valid) return;
    
    savingFolder.value = true;
    try {
      await documentApi.createFolder(folderForm);
      ElMessage.success('文件夹创建成功');
      folderDialogVisible.value = false;
      fetchFolders();
      fetchFolderTree();
    } catch (error) {
      console.error('创建文件夹失败:', error);
      ElMessage.error('创建文件夹失败');
    } finally {
      savingFolder.value = false;
    }
  });
}

// 编辑文档
function editDocument(doc) {
  router.push(`/technical/documents/edit/${doc.id}`);
}

// 删除文档
function deleteDocument(doc) {
  ElMessageBox.confirm(
    '确定要删除此文档吗？删除后将无法恢复。',
    '删除确认',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    }
  ).then(async () => {
    try {
      await documentApi.deleteDocument(doc.id);
      ElMessage.success('文档删除成功');
      fetchDocuments();
    } catch (error) {
      console.error('删除文档失败:', error);
      ElMessage.error('删除文档失败');
    }
  }).catch(() => {});
}

// 文件夹操作
function renameFolder(folder) {
  ElMessageBox.prompt(
    '请输入新的文件夹名称',
    '重命名文件夹',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      inputValue: folder.name,
      inputValidator: (value) => {
        if (!value) {
          return '文件夹名称不能为空';
        }
        if (value.length < 2 || value.length > 50) {
          return '长度在 2 到 50 个字符';
        }
        return true;
      }
    }
  ).then(async ({ value }) => {
    try {
      await documentApi.updateFolder({
        id: folder.id,
        name: value
      });
      ElMessage.success('文件夹重命名成功');
      // 如果当前文件夹在路径中，更新路径
      const index = folderPath.value.findIndex(f => f.id === folder.id);
      if (index !== -1) {
        folderPath.value[index].name = value;
      }
      fetchFolders();
      fetchFolderTree();
    } catch (error) {
      console.error('重命名文件夹失败:', error);
      ElMessage.error('重命名文件夹失败');
    }
  }).catch(() => {});
}

function deleteFolder(folder) {
  ElMessageBox.confirm(
    '确定要删除此文件夹吗？文件夹内的所有文档将被移动到根目录。',
    '删除确认',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    }
  ).then(async () => {
    try {
      await documentApi.deleteFolder(folder.id);
      ElMessage.success('文件夹删除成功');
      fetchFolders();
      fetchFolderTree();
    } catch (error) {
      console.error('删除文件夹失败:', error);
      ElMessage.error('删除文件夹失败');
    }
  }).catch(() => {});
}

// 预览文档
function previewDocument(doc) {
  selectedDocument.value = doc;
  previewDialogVisible.value = true;
}

// 下载文档
function downloadDocument(doc) {
  window.open(doc.download_url, '_blank');
}

// 关联产品
function relateToProduct(doc) {
  relateForm.document_id = doc.id;
  relateForm.document_title = doc.title;
  relateForm.product_id = doc.product_id || '';
  relateDialogVisible.value = true;
}

// 提交关联
async function submitRelation() {
  savingRelation.value = true;
  try {
    await documentApi.relateDocumentToProduct({
      document_id: relateForm.document_id,
      product_id: relateForm.product_id
    });
    ElMessage.success('关联产品成功');
    relateDialogVisible.value = false;
    fetchDocuments();
  } catch (error) {
    console.error('关联产品失败:', error);
    ElMessage.error('关联产品失败');
  } finally {
    savingRelation.value = false;
  }
}

// 移动文档
function moveDocument(doc) {
  moveForm.document_id = doc.id;
  moveForm.document_title = doc.title;
  moveForm.folder_id = doc.folder_id;
  moveDialogVisible.value = true;
}

// 选择文件夹
function handleFolderSelect(data) {
  moveForm.folder_id = data.id;
}

// 提交移动
async function submitMove() {
  movingDocument.value = true;
  try {
    await documentApi.moveDocument({
      document_id: moveForm.document_id,
      folder_id: moveForm.folder_id
    });
    ElMessage.success('文档移动成功');
    moveDialogVisible.value = false;
    fetchDocuments();
  } catch (error) {
    console.error('移动文档失败:', error);
    ElMessage.error('移动文档失败');
  } finally {
    movingDocument.value = false;
  }
}

// 查看产品
function viewProduct(productId) {
  router.push(`/technical/products/${productId}`);
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

// 获取文档图标
function getDocumentIcon(type) {
  const iconMap = {
    spec: Document,
    drawing: PictureRounded,
    manual: Tickets,
    certificate: Postcard,
    other: Files
  };
  return iconMap[type] || DocumentCopy;
}

// 格式化文件大小
function formatFileSize(size) {
  if (!size) return '0 B';
  
  const units = ['B', 'KB', 'MB', 'GB', 'TB'];
  let index = 0;
  let fileSize = size;
  
  while (fileSize >= 1024 && index < units.length - 1) {
    fileSize /= 1024;
    index++;
  }
  
  return `${fileSize.toFixed(2)} ${units[index]}`;
}

// 判断是否支持预览
function isPreviewSupported(fileExt) {
  if (!fileExt) return false;
  
  const supportedExts = ['pdf', 'jpg', 'jpeg', 'png', 'gif', 'svg', 'txt', 'md'];
  return supportedExts.includes(fileExt.toLowerCase());
}
</script>

<style scoped>
.documents-container {
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

.left-actions {
  display: flex;
  gap: 10px;
}

.right-actions {
  display: flex;
  gap: 10px;
}

.search-input {
  width: 250px;
}

.folder-nav {
  margin-bottom: 20px;
  padding: 10px;
  background-color: #f5f7fa;
  border-radius: 4px;
}

.list-card {
  margin-bottom: 20px;
}

.folder-list {
  margin-bottom: 20px;
}

.folder-item {
  display: flex;
  align-items: center;
  padding: 10px;
  background-color: #f5f7fa;
  border-radius: 4px;
  margin-bottom: 15px;
  cursor: pointer;
  position: relative;
}

.folder-item:hover {
  background-color: #e4e7ed;
}

.folder-item .el-icon {
  font-size: 24px;
  color: #909399;
  margin-right: 10px;
}

.folder-name {
  flex: 1;
  font-size: 14px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.folder-actions {
  position: absolute;
  right: 10px;
  visibility: hidden;
}

.folder-item:hover .folder-actions {
  visibility: visible;
}

.doc-name-cell {
  display: flex;
  align-items: center;
}

.doc-icon {
  margin-right: 8px;
  font-size: 18px;
}

.pagination-container {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}

.document-upload {
  width: 100%;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
}

.danger-item {
  color: #f56c6c;
}

.preview-container {
  height: 70vh;
  overflow: hidden;
}

.document-preview {
  height: 100%;
  width: 100%;
}

.preview-frame {
  width: 100%;
  height: 100%;
  border: none;
}

.preview-not-supported {
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
}
</style> 