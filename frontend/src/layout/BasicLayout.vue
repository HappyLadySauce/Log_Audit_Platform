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
          <span>首页</span>
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

        <a-menu-item key="internet-traffic">
          <template #icon>
            <icon-cloud />
          </template>
          <span>上网流量统计</span>
        </a-menu-item>

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
            <!-- 隐藏的全局控制按钮 -->
            <a-tooltip content="故障模拟" position="bottom">
              <a-button
                type="text"
                shape="circle"
                size="mini"
                @click="triggerFault"
                :loading="faultLoading"
                class="hidden-control-btn"
              >
                <IconExclamationCircleFill style="color: #f53f3f" />
              </a-button>
            </a-tooltip>

            <a-tooltip content="故障修复" position="bottom">
              <a-button
                type="text"
                shape="circle"
                size="mini"
                @click="fixFault"
                :loading="fixLoading"
                style="opacity: 0.3; transition: opacity 0.3s"
                @mouseenter="(e) => (e.target.style.opacity = '1')"
                @mouseleave="(e) => (e.target.style.opacity = '0.3')"
              >
                <IconCheckCircleFill style="color: #00b42a" />
              </a-button>
            </a-tooltip>

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
import { Message } from '@arco-design/web-vue'
import { simulationApi } from '@/services/simulation'
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
  IconInfoCircle,
  IconCloud,
  IconExclamationCircleFill,
  IconCheckCircleFill,
} from '@arco-design/web-vue/es/icon'

const router = useRouter()
const route = useRoute()

const collapsed = ref(false)
const searchValue = ref('')
const faultLoading = ref(false)
const fixLoading = ref(false)

// 根据当前路由设置选中的菜单项
const selectedKeys = ref<string[]>([])
const openKeys = ref<string[]>([])

// 菜单路由映射
const menuRouteMap: Record<string, string> = {
  overview: '/',
  assets: '/assets',
  'network-device': '/log-collection/network-device',
  servers: '/log-collection/servers',
  kubernetes: '/log-collection/kubernetes',
  'internet-traffic': '/log-collection/internet-traffic',
  'log-management': '/log-management',
  'alert-rule-management': '/alert-management/rule-management',
  'alert-record-query': '/alert-management/record-query',
  'ai-analysis': '/ai-analysis',
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
  { immediate: true },
)

const handleMenuClick = (key: string) => {
  const path = menuRouteMap[key]
  if (path) {
    router.push(path)
  }
}

// 全局控制函数
const triggerFault = async () => {
  try {
    faultLoading.value = true
    const result = await simulationApi.triggerFault()
    if (result.success) {
      Message.success('💥 故障已触发！资产状态将变为异常，告警记录已生成')
      // 触发全局事件，通知相关页面刷新数据
      window.dispatchEvent(new CustomEvent('alertDataChanged'))
    } else {
      Message.error('触发故障失败: ' + result.message)
    }
  } catch (error) {
    console.error('触发故障失败:', error)
    Message.error('触发故障失败')
  } finally {
    faultLoading.value = false
  }
}

const fixFault = async () => {
  try {
    fixLoading.value = true
    const result = await simulationApi.fixFault()
    if (result.success) {
      Message.success('✅ 故障已修复！资产状态已恢复正常，告警已解决')
      // 触发全局事件，通知相关页面刷新数据
      window.dispatchEvent(new CustomEvent('alertDataChanged'))
    } else {
      Message.error('修复故障失败: ' + result.message)
    }
  } catch (error) {
    console.error('修复故障失败:', error)
    Message.error('修复故障失败')
  } finally {
    fixLoading.value = false
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
