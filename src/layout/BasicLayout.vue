<template>
  <a-layout class="layout">
    <a-layout-sider
      v-model:collapsed="collapsed"
      :width="240"
      :collapsed-width="64"
      :trigger="null"
      collapsible
      class="layout-sider"
    >
      <div class="logo">
        <icon-desktop class="logo-icon" />
        <span v-if="!collapsed" class="logo-text">日志审计平台</span>
      </div>
      <a-menu
        v-model:selected-keys="selectedKeys"
        v-model:open-keys="openKeys"
        :style="{ width: '100%', border: 'none' }"
        theme="dark"
        mode="vertical"
        @menu-item-click="handleMenuClick"
      >
        <a-menu-item key="overview">
          <template #icon>
            <icon-dashboard />
          </template>
          <span>仪表板</span>
        </a-menu-item>
        
        <a-menu-item key="assets">
          <template #icon>
            <icon-storage />
          </template>
          <span>资产管理</span>
        </a-menu-item>

        <a-sub-menu key="log-collection">
          <template #icon>
            <icon-download />
          </template>
          <template #title>日志采集</template>
          <a-menu-item key="network-device">网络设备日志</a-menu-item>
          <a-menu-item key="servers">服务器日志</a-menu-item>
          <a-menu-item key="kubernetes">K8s集群日志</a-menu-item>
          <a-menu-item key="internet-traffic">上网流量统计</a-menu-item>
        </a-sub-menu>

        <a-menu-item key="log-management">
          <template #icon>
            <icon-file />
          </template>
          <span>日志管理</span>
        </a-menu-item>

        <a-sub-menu key="alert-management">
          <template #icon>
            <icon-notification />
          </template>
          <template #title>
            <span>告警管理</span>
          </template>
          <a-menu-item key="alert-rule-management">
            <template #icon>
              <icon-settings />
            </template>
            <span>告警规则配置</span>
          </a-menu-item>
          <a-menu-item key="alert-record-query">
            <template #icon>
              <icon-info-circle />
            </template>
            <span>告警记录查询</span>
          </a-menu-item>
        </a-sub-menu>

        <a-menu-item key="ai-analysis">
          <template #icon>
            <icon-robot />
          </template>
          <span>AI智能分析</span>
        </a-menu-item>
      </a-menu>
    </a-layout-sider>

    <a-layout>
      <a-layout-header class="layout-header">
        <div class="header-left">
          <a-button type="text" @click="collapsed = !collapsed">
            <icon-menu-fold v-if="!collapsed" />
            <icon-menu-unfold v-if="collapsed" />
          </a-button>
        </div>

        <div class="header-center">
          <a-input
            v-model="searchValue"
            placeholder="搜索日志、设备、告警..."
            style="width: 400px"
            allow-clear
          >
            <template #prefix>
              <icon-search />
            </template>
          </a-input>
        </div>

        <div class="header-right">
          <a-space>
            <a-button type="text" shape="circle">
              <icon-history />
            </a-button>
            <a-badge :count="5" dot>
              <a-button type="text" shape="circle">
                <icon-notification />
              </a-button>
            </a-badge>
            <a-dropdown>
              <a-avatar>
                <icon-user />
              </a-avatar>
              <template #content>
                <a-doption>个人中心</a-doption>
                <a-doption>退出登录</a-doption>
              </template>
            </a-dropdown>
          </a-space>
        </div>
      </a-layout-header>

      <a-layout-content class="layout-content">
        <router-view />
      </a-layout-content>
    </a-layout>
  </a-layout>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import {
  IconDesktop,
  IconDashboard,
  IconStorage,
  IconDownload,
  IconFile,
  IconNotification,
  IconRobot,
  IconMenuFold,
  IconMenuUnfold,
  IconSearch,
  IconHistory,
  IconUser,
  IconSettings,
  IconInfoCircle
} from '@arco-design/web-vue/es/icon'

const router = useRouter()
const route = useRoute()

const collapsed = ref(false)
const searchValue = ref('')

// 根据当前路由设置选中的菜单项
const selectedKeys = ref<string[]>([])
const openKeys = ref<string[]>([])

// 菜单路由映射
const menuRouteMap: Record<string, string> = {
  'overview': '/',
  'assets': '/assets',
  'network-device': '/log-collection/network-device',
  'servers': '/log-collection/servers',
  'kubernetes': '/log-collection/kubernetes',
  'internet-traffic': '/log-collection/internet-traffic',
  'log-management': '/log-management',
  'alert-rule-management': '/alert-management/rule-management',
  'alert-record-query': '/alert-management/record-query',
  'ai-analysis': '/ai-analysis'
}

// 监听路由变化更新选中状态
watch(
  () => route.path,
  (newPath) => {
    for (const [key, path] of Object.entries(menuRouteMap)) {
      if (newPath === path || newPath.startsWith(path + '/')) {
        selectedKeys.value = [key]
        
        // 如果是告警管理的子菜单，展开父菜单
        if (key.startsWith('alert-')) {
          openKeys.value = ['alert-management']
        }
        break
      }
    }
  },
  { immediate: true }
)

const handleMenuClick = (key: string) => {
  const path = menuRouteMap[key]
  if (path) {
    router.push(path)
  }
}
</script>

<style scoped>
.layout {
  height: 100vh;
}

.layout-sider {
  background: #001529;
}

.logo {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 64px;
  padding: 0 16px;
  color: #fff;
  font-size: 18px;
  font-weight: bold;
  border-bottom: 1px solid #1c2a3d;
}

.logo-icon {
  font-size: 24px;
}

.logo-text {
  margin-left: 8px;
}

.layout-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 24px;
  background: #fff;
  border-bottom: 1px solid #e5e6eb;
}

.header-left {
  display: flex;
  align-items: center;
}

.header-center {
  flex: 1;
  display: flex;
  justify-content: center;
  max-width: 600px;
}

.header-right {
  display: flex;
  align-items: center;
}

.layout-content {
  margin: 0;
  padding: 24px;
  background: #f5f5f5;
  overflow-y: auto;
}

:deep(.arco-menu-dark) {
  background: #001529;
}

:deep(.arco-menu-dark .arco-menu-item:hover) {
  background-color: #1c2a3d;
}

:deep(.arco-menu-dark .arco-menu-item.arco-menu-selected) {
  background-color: #1890ff;
}
</style> 