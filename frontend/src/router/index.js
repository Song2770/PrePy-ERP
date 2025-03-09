import { createRouter, createWebHistory } from 'vue-router';
import { useUserStore } from '@/stores/user';

// Layouts
import MainLayout from '@/layouts/MainLayout.vue';
import AuthLayout from '@/layouts/AuthLayout.vue';

// Auth pages
const Login = () => import('@/views/auth/Login.vue');
const Register = () => import('@/views/auth/Register.vue');
const ForgotPassword = () => import('@/views/auth/ForgotPassword.vue');

// Dashboard
const Dashboard = () => import('@/views/Dashboard.vue');

// Sales Management
const SalesQuotations = () => import('@/views/sales/Quotations.vue');
const SalesQuotationDetail = () => import('@/views/sales/QuotationDetail.vue');
const SalesOrders = () => import('@/views/sales/Orders.vue');
const SalesOrderDetail = () => import('@/views/sales/OrderDetail.vue');
const SalesDeliveries = () => import('@/views/sales/Deliveries.vue');
const SalesInvoices = () => import('@/views/sales/Invoices.vue');
const Customers = () => import('@/views/sales/Customers.vue');
const CustomerDetail = () => import('@/views/sales/CustomerDetail.vue');

// Technical Management
const Products = () => import('@/views/technical/Products.vue');
const ProductDetail = () => import('@/views/technical/ProductDetail.vue');
const BillOfMaterials = () => import('@/views/technical/BillOfMaterials.vue');
const BOMDetail = () => import('@/views/technical/BOMDetail.vue');
const Workstations = () => import('@/views/technical/Workstations.vue');
const ProductionRoutes = () => import('@/views/technical/ProductionRoutes.vue');
const TechnicalDocuments = () => import('@/views/technical/Documents.vue');

// User Management
const UserProfile = () => import('@/views/users/UserProfile.vue');
const UserSettings = () => import('@/views/users/UserSettings.vue');
const UsersList = () => import('@/views/users/UsersList.vue');

// Error Pages
const NotFound = () => import('@/views/errors/NotFound.vue');
const Forbidden = () => import('@/views/errors/Forbidden.vue');

const routes = [
  {
    path: '/',
    component: MainLayout,
    meta: { requiresAuth: true },
    children: [
      {
        path: '',
        name: 'Dashboard',
        component: Dashboard,
        meta: { title: '仪表板' }
      },
      // Sales Management Routes
      {
        path: 'sales',
        name: 'Sales',
        meta: { title: '销售管理' },
        children: [
          {
            path: 'quotations',
            name: 'SalesQuotations',
            component: SalesQuotations,
            meta: { title: '报价单' }
          },
          {
            path: 'quotations/:id',
            name: 'SalesQuotationDetail',
            component: SalesQuotationDetail,
            props: true,
            meta: { title: '报价单详情' }
          },
          {
            path: 'orders',
            name: 'SalesOrders',
            component: SalesOrders,
            meta: { title: '销售订单' }
          },
          {
            path: 'orders/:id',
            name: 'SalesOrderDetail',
            component: SalesOrderDetail,
            props: true,
            meta: { title: '销售订单详情' }
          },
          {
            path: 'deliveries',
            name: 'SalesDeliveries',
            component: SalesDeliveries,
            meta: { title: '销售出库' }
          },
          {
            path: 'invoices',
            name: 'SalesInvoices',
            component: SalesInvoices,
            meta: { title: '销售发票' }
          },
          {
            path: 'customers',
            name: 'Customers',
            component: Customers,
            meta: { title: '客户管理' }
          },
          {
            path: 'customers/:id',
            name: 'CustomerDetail',
            component: CustomerDetail,
            props: true,
            meta: { title: '客户详情' }
          }
        ]
      },
      // Technical Management Routes
      {
        path: 'technical',
        name: 'Technical',
        meta: { title: '技术管理' },
        children: [
          {
            path: 'products',
            name: 'Products',
            component: Products,
            meta: { title: '产品管理' }
          },
          {
            path: 'products/:id',
            name: 'ProductDetail',
            component: ProductDetail,
            props: true,
            meta: { title: '产品详情' }
          },
          {
            path: 'boms',
            name: 'BillOfMaterials',
            component: BillOfMaterials,
            meta: { title: '物料清单管理' }
          },
          {
            path: 'boms/:id',
            name: 'BOMDetail',
            component: BOMDetail,
            props: true,
            meta: { title: '物料清单详情' }
          },
          {
            path: 'workstations',
            name: 'Workstations',
            component: Workstations,
            meta: { title: '工作站管理' }
          },
          {
            path: 'routes',
            name: 'ProductionRoutes',
            component: ProductionRoutes,
            meta: { title: '生产路线管理' }
          },
          {
            path: 'documents',
            name: 'TechnicalDocuments',
            component: TechnicalDocuments,
            meta: { title: '技术文档管理' }
          }
        ]
      },
      // User Management Routes
      {
        path: 'users',
        name: 'Users',
        meta: { title: '用户管理' },
        children: [
          {
            path: 'profile',
            name: 'UserProfile',
            component: UserProfile,
            meta: { title: '用户资料' }
          },
          {
            path: 'settings',
            name: 'UserSettings',
            component: UserSettings,
            meta: { title: '用户设置' }
          },
          {
            path: 'list',
            name: 'UsersList',
            component: UsersList,
            meta: { title: '用户列表', requiresAdmin: true }
          }
        ]
      }
    ]
  },
  {
    path: '/auth',
    component: AuthLayout,
    meta: { guest: true },
    children: [
      {
        path: 'login',
        name: 'Login',
        component: Login,
        meta: { title: '登录' }
      },
      {
        path: 'register',
        name: 'Register',
        component: Register,
        meta: { title: '注册' }
      },
      {
        path: 'forgot-password',
        name: 'ForgotPassword',
        component: ForgotPassword,
        meta: { title: '忘记密码' }
      }
    ]
  },
  {
    path: '/forbidden',
    name: 'Forbidden',
    component: Forbidden,
    meta: { title: '访问被拒绝' }
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: NotFound,
    meta: { title: '页面未找到' }
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

// Global navigation guard
router.beforeEach((to, from, next) => {
  // Set document title
  document.title = to.meta.title ? `${to.meta.title} - PrePy ERP` : 'PrePy ERP';
  
  const userStore = useUserStore();
  const isLoggedIn = userStore.isLoggedIn;
  const requiresAuth = to.matched.some(record => record.meta.requiresAuth);
  const requiresAdmin = to.matched.some(record => record.meta.requiresAdmin);
  const isAdmin = userStore.isAdmin;
  const isGuestRoute = to.matched.some(record => record.meta.guest);
  
  // Check if route requires authentication
  if (requiresAuth && !isLoggedIn) {
    next({ name: 'Login', query: { redirect: to.fullPath } });
  }
  // Check if route requires admin privileges
  else if (requiresAdmin && !isAdmin) {
    next({ name: 'Forbidden' });
  }
  // Redirect authenticated users away from guest routes (like Login)
  else if (isLoggedIn && isGuestRoute) {
    next({ name: 'Dashboard' });
  }
  else {
    next();
  }
});

export default router; 