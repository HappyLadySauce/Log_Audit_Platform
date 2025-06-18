import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'overview',
      component: () => import('@/views/overview/index.vue'),
      meta: {
        title: '仪表板',
      },
    },
    {
      path: '/assets',
      name: 'assets',
      component: () => import('@/views/assets_management/index.vue'),
      meta: {
        title: '资产管理',
      },
    },
    {
      path: '/log-collection',
      redirect: '/log-collection/network-device',
      meta: {
        title: '日志采集',
      },
    },
    {
      path: '/log-collection/network-device',
      name: 'network-device',
      component: () => import('@/views/log_collection/network_device.vue'),
      meta: {
        title: '网络设备日志',
      },
    },
    {
      path: '/log-collection/servers',
      name: 'servers',
      component: () => import('@/views/log_collection/servers.vue'),
      meta: {
        title: '服务器日志',
      },
    },
    {
      path: '/log-collection/server-detail',
      name: 'server-detail',
      component: () => import('@/views/log_collection/server-detail.vue'),
      meta: {
        title: '服务器详情',
      },
    },
    {
      path: '/log-collection/kubernetes',
      name: 'kubernetes',
      component: () => import('@/views/log_collection/kubernetes.vue'),
      meta: {
        title: 'K8s集群日志',
      },
    },
    {
      path: '/log-collection/internet-traffic',
      name: 'internet-traffic',
      component: () => import('@/views/log_collection/internet_traffic.vue'),
      meta: {
        title: '上网流量统计',
      },
    },
    {
      path: '/log-management',
      name: 'log-management',
      component: () => import('@/views/log_management/index.vue'),
      meta: {
        title: '日志管理',
      },
    },
    {
      path: '/alert-management',
      redirect: '/alert-management/record-query',
      meta: {
        title: '告警管理',
      },
    },
    {
      path: '/alert-management/rule-management',
      name: 'alert-rule-management',
      component: () => import('@/views/alert_management/rule_management.vue'),
      meta: {
        title: '告警规则管理',
      },
    },
    {
      path: '/alert-management/record-query',
      name: 'alert-record-query',
      component: () => import('@/views/alert_management/record_query.vue'),
      meta: {
        title: '告警记录查询',
      },
    },
    {
      path: '/ai-analysis',
      name: 'ai-analysis',
      component: () => import('@/views/ai_analysis/index.vue'),
      meta: {
        title: 'AI智能分析',
      },
    },
  ],
})

export default router
