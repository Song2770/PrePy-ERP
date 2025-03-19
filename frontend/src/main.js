import { createApp } from 'vue';
import { createPinia } from 'pinia';
import ElementPlus from 'element-plus';
import 'element-plus/dist/index.css';
import zhCn from 'element-plus/es/locale/lang/zh-cn';
import * as ElementPlusIconsVue from '@element-plus/icons-vue';

import App from './App.vue';
import router from './router';
import { useUserStore } from './stores/user';
import './assets/styles/main.scss';

const app = createApp(App);
const pinia = createPinia();

// Register all Element Plus icons
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
  app.component(key, component);
}

app.use(pinia);
app.use(router);
app.use(ElementPlus, {
  locale: zhCn,
  size: 'default',
});

// 初始化用户状态
const userStore = useUserStore();
userStore.initializeApp();

app.mount('#app'); 