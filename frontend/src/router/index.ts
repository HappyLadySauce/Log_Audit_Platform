import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/login',
      name: 'login',
      component: () => import('@/views/login/index.vue'),
      meta: {
        title: '登录',
        requiresAuth: false,
      },
    },
    {
      path: '/',
      name: 'overview',
      component: () => import('@/views/overview/index.vue'),
      meta: {
        title: '仪表板',
        requiresAuth: true,
      },
    },
    {
      path: '/assets',
      name: 'assets',
      component: () => import('@/views/assets_management/index.vue'),
      meta: {
        title: '资产管理',
        requiresAuth: true,
      },
    },
    {
      path: '/log-collection',
      redirect: '/log-collection/network-device',
      meta: {
        title: '日志采集',
        requiresAuth: true,
      },
    },
    {
      path: '/log-collection/network-device',
      name: 'network-device',
      component: () => import('@/views/log_collection/network_device.vue'),
      meta: {
        title: '网络设备日志',
        requiresAuth: true,
      },
    },
    {
      path: '/log-collection/servers',
      name: 'servers',
      component: () => import('@/views/log_collection/servers.vue'),
      meta: {
        title: '服务器日志',
        requiresAuth: true,
      },
    },
    {
      path: '/log-collection/server-detail',
      name: 'server-detail',
      component: () => import('@/views/log_collection/server-detail.vue'),
      meta: {
        title: '服务器详情',
        requiresAuth: true,
      },
    },
    {
      path: '/log-collection/kubernetes',
      name: 'kubernetes',
      component: () => import('@/views/log_collection/kubernetes.vue'),
      meta: {
        title: 'K8s集群日志',
        requiresAuth: true,
      },
    },
    {
      path: '/log-collection/internet-traffic',
      name: 'internet-traffic',
      component: () => import('@/views/log_collection/internet_traffic.vue'),
      meta: {
        title: '上网流量统计',
        requiresAuth: true,
      },
    },
    {
      path: '/log-management',
      name: 'log-management',
      component: () => import('@/views/log_management/index.vue'),
      meta: {
        title: '日志管理',
        requiresAuth: true,
      },
    },
    {
      path: '/alert-management',
      redirect: '/alert-management/record-query',
      meta: {
        title: '告警管理',
        requiresAuth: true,
      },
    },
    {
      path: '/alert-management/rule-management',
      name: 'alert-rule-management',
      component: () => import('@/views/alert_management/rule_management.vue'),
      meta: {
        title: '告警规则管理',
        requiresAuth: true,
      },
    },
    {
      path: '/alert-management/record-query',
      name: 'alert-record-query',
      component: () => import('@/views/alert_management/record_query.vue'),
      meta: {
        title: '告警记录查询',
        requiresAuth: true,
      },
    },
    {
      path: '/ai-analysis',
      name: 'ai-analysis',
      component: () => import('@/views/ai_analysis/index.vue'),
      meta: {
        title: 'AI智能分析',
        requiresAuth: true,
      },
    },
  ],
})

// 路由守卫
router.beforeEach((to, from, next) => {
  const isLoggedIn = localStorage.getItem('isLoggedIn') === 'true'
  
  // 如果要访问的路由需要登录，但用户未登录
  if (to.meta.requiresAuth && !isLoggedIn) {
    next('/login')
  }
  // 如果用户已登录，但想访问登录页
  else if (to.path === '/login' && isLoggedIn) {
    next('/')
  }
  // 其他情况正常访问
  else {
    next()
  }
})

export default router
