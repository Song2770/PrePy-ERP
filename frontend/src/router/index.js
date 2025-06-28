import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '@/stores/user'

console.log('正在初始化路由配置...')

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/Login.vue'),
    meta: { requiresAuth: false, title: '用户登录' }
  },
  {
    path: '/',
    name: 'Layout',
    component: () => import('@/layout/index.vue'),
    redirect: '/dashboard',
    meta: { requiresAuth: true },
    children: [
      {
        path: '/dashboard',
        name: 'Dashboard',
        component: () => import('@/views/Dashboard.vue'),
        meta: { title: '仪表盘', icon: 'DataBoard' }
      },
      {
        path: '/sales',
        name: 'Sales',
        meta: { title: '销售管理', icon: 'ShoppingCart' },
        children: [
          {
            path: '/sales/orders',
            name: 'SalesOrders',
            component: () => import('@/views/sales/Orders.vue'),
            meta: { title: '销售订单' }
          },
          {
            path: '/sales/quotations',
            name: 'SalesQuotations',
            component: () => import('@/views/sales/Quotations.vue'),
            meta: { title: '销售报价' }
          }
        ]
      },
      {
        path: '/production',
        name: 'Production',
        meta: { title: '生产管理', icon: 'Setting' },
        children: [
          {
            path: '/production/work-orders',
            name: 'WorkOrders',
            component: () => import('@/views/production/WorkOrders.vue'),
            meta: { title: '生产工单' }
          },
          {
            path: '/production/operations',
            name: 'Operations',
            component: () => import('@/views/production/Operations.vue'),
            meta: { title: '工序管理' }
          }
        ]
      },
      {
        path: '/procurement',
        name: 'Procurement',
        meta: { title: '采购管理', icon: 'ShoppingBag' },
        children: [
          {
            path: '/procurement/purchase-orders',
            name: 'PurchaseOrders',
            component: () => import('@/views/procurement/PurchaseOrders.vue'),
            meta: { title: '采购订单' }
          },
          {
            path: '/procurement/suppliers',
            name: 'Suppliers',
            component: () => import('@/views/procurement/Suppliers.vue'),
            meta: { title: '供应商管理' }
          }
        ]
      },
      {
        path: '/warehouse',
        name: 'Warehouse',
        meta: { title: '仓库管理', icon: 'Box' },
        children: [
          {
            path: '/warehouse/inventory',
            name: 'Inventory',
            component: () => import('@/views/warehouse/Inventory.vue'),
            meta: { title: '库存管理' }
          },
          {
            path: '/warehouse/stock-movements',
            name: 'StockMovements',
            component: () => import('@/views/warehouse/StockMovements.vue'),
            meta: { title: '库存移动' }
          }
        ]
      },
      {
        path: '/finance',
        name: 'Finance',
        meta: { title: '财务管理', icon: 'Money' },
        children: [
          {
            path: '/finance/invoices',
            name: 'Invoices',
            component: () => import('@/views/finance/Invoices.vue'),
            meta: { title: '发票管理' }
          },
          {
            path: '/finance/payments',
            name: 'Payments',
            component: () => import('@/views/finance/Payments.vue'),
            meta: { title: '付款管理' }
          }
        ]
      },
      {
        path: '/master-data',
        name: 'MasterData',
        meta: { title: '基础数据', icon: 'Files' },
        children: [
          {
            path: '/master-data/products',
            name: 'Products',
            component: () => import('@/views/master-data/Products.vue'),
            meta: { title: '产品管理' }
          },
          {
            path: '/master-data/customers',
            name: 'Customers',
            component: () => import('@/views/master-data/Customers.vue'),
            meta: { title: '客户管理' }
          }
        ]
      },
      {
        path: '/system',
        name: 'System',
        meta: { title: '系统管理', icon: 'Tools' },
        children: [
          {
            path: '/system/users',
            name: 'Users',
            component: () => import('@/views/system/Users.vue'),
            meta: { title: '用户管理' }
          },
          {
            path: '/system/roles',
            name: 'Roles',
            component: () => import('@/views/system/Roles.vue'),
            meta: { title: '角色管理' }
          }
        ]
      }
    ]
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: () => import('@/views/NotFound.vue'),
    meta: { title: '页面未找到' }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 路由守卫
router.beforeEach(async (to, from, next) => {
  const userStore = useUserStore()
  
  // 设置页面标题
  if (to.meta.title) {
    document.title = `${to.meta.title} - PrePy ERP`
  } else {
    document.title = 'PrePy ERP - 企业资源规划系统'
  }
  
  // 检查是否需要认证
  if (to.meta.requiresAuth !== false) {
    if (!userStore.isAuthenticated) {
      console.log('用户未登录，跳转到登录页面')
      next({ name: 'Login', query: { redirect: to.fullPath } })
      return
    }
  }
  
  // 如果已登录用户访问登录页，重定向到首页
  if (to.name === 'Login' && userStore.isAuthenticated) {
    next({ name: 'Dashboard' })
    return
  }
  
  next()
})

console.log('路由配置初始化完成')

export default router