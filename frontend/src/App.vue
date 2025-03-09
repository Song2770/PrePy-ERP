<template>
  <router-view />
</template>

<script>
import { defineComponent } from 'vue';
import { useUserStore } from '@/stores/user';

export default defineComponent({
  name: 'App',
  setup() {
    const userStore = useUserStore();
    
    // Try to load user from localStorage on app start
    userStore.initializeFromStorage();
    
    return {};
  }
});
</script>

<style>
html, body {
  margin: 0;
  padding: 0;
  height: 100%;
  font-family: 'Helvetica Neue', Helvetica, 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', '微软雅黑', Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

#app {
  height: 100%;
}

.page-container {
  padding: 20px;
}

.el-table {
  width: 100%;
}

.table-operations {
  margin-bottom: 20px;
}

.pagination {
  margin-top: 20px;
  text-align: right;
}
</style> 