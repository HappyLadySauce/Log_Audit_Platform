<template>
  <div class="assets-page">
    <PageHeader
      title="资产管理"
      description="管理和监控所有IT资产设备"
    >
      <template #extra>
        <a-space>
          <a-button>
            <template #icon>
              <icon-refresh />
            </template>
            刷新
          </a-button>
          <a-button type="primary">
            <template #icon>
              <icon-plus />
            </template>
            添加资产
          </a-button>
        </a-space>
      </template>
    </PageHeader>

    <!-- 资产统计 -->
    <a-row :gutter="24" class="stats-row">
      <a-col :span="6">
        <StatCard
          :icon="IconDesktop"
          icon-bg-color="#1890ff"
          :value="156"
          label="总资产数"
          subtitle="设备总量"
        />
      </a-col>
      <a-col :span="6">
        <StatCard
          :icon="IconCheck"
          icon-bg-color="#52c41a"
          :value="142"
          label="在线设备"
          subtitle="正常运行"
        />
      </a-col>
      <a-col :span="6">
        <StatCard
          :icon="IconExclamation"
          icon-bg-color="#faad14"
          :value="8"
          label="异常设备"
          subtitle="需要关注"
        />
      </a-col>
      <a-col :span="6">
        <StatCard
          :icon="IconClose"
          icon-bg-color="#f5222d"
          :value="6"
          label="离线设备"
          subtitle="失去连接"
        />
      </a-col>
    </a-row>

    <!-- 资产列表 -->
    <a-card title="资产列表" :bordered="false">
      <template #extra>
        <a-space>
          <a-input-search
            placeholder="搜索资产..."
            style="width: 200px"
            allow-clear
          />
          <a-select
            placeholder="设备类型"
            style="width: 120px"
            allow-clear
          >
            <a-option value="server">服务器</a-option>
            <a-option value="network">网络设备</a-option>
            <a-option value="storage">存储设备</a-option>
            <a-option value="security">安全设备</a-option>
          </a-select>
        </a-space>
      </template>

      <a-table
        :columns="assetColumns"
        :data="assetData"
        :pagination="{ pageSize: 10 }"
        :scroll="{ x: '100%' }"
      >
        <template #deviceInfo="{ record }">
          <div class="device-info">
            <a-avatar size="small" class="device-avatar">
              <component :is="getDeviceIcon(record.type)" />
            </a-avatar>
            <div class="device-details">
              <div class="device-name">{{ record.name }}</div>
              <div class="device-model">{{ record.model }}</div>
            </div>
          </div>
        </template>

        <template #type="{ record }">
          <a-tag :color="getTypeColor(record.type)">
            {{ getTypeName(record.type) }}
          </a-tag>
        </template>

        <template #status="{ record }">
          <a-badge
            :status="getStatusType(record.status)"
            :text="record.status"
          />
        </template>

        <template #actions="{ record }">
          <a-space>
            <a-button type="text" size="small">查看</a-button>
            <a-button type="text" size="small">编辑</a-button>
            <a-button type="text" size="small" status="danger">删除</a-button>
          </a-space>
        </template>
      </a-table>
    </a-card>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import PageHeader from '@/components/PageHeader.vue'
import StatCard from '@/components/StatCard.vue'
import {
  IconRefresh,
  IconPlus,
  IconDesktop,
  IconCheck,
  IconExclamation,
  IconClose,
  IconWifi,
  IconLock
} from '@arco-design/web-vue/es/icon'

// 资产数据
const assetData = ref([
  {
    key: '1',
    name: '核心服务器-01',
    model: 'Dell PowerEdge R750',
    type: 'server',
    ip: '192.168.1.100',
    location: '机房A-01',
    status: '在线',
    lastUpdate: '2024-01-15 10:30:00'
  },
  {
    key: '2',
    name: '核心路由器-01',
    model: 'Cisco ISR 4431',
    type: 'network',
    ip: '192.168.1.1',
    location: '机房A-02',
    status: '在线',
    lastUpdate: '2024-01-15 10:25:00'
  },
  {
    key: '3',
    name: '防火墙-01',
    model: 'Fortinet FortiGate 200F',
    type: 'security',
    ip: '192.168.1.254',
    location: '机房A-03',
    status: '异常',
    lastUpdate: '2024-01-15 09:45:00'
  }
])

// 表格列配置
const assetColumns = [
  {
    title: '设备信息',
    dataIndex: 'name',
    slotName: 'deviceInfo',
    width: 250
  },
  {
    title: '设备类型',
    dataIndex: 'type',
    slotName: 'type',
    width: 100
  },
  {
    title: 'IP地址',
    dataIndex: 'ip',
    width: 120
  },
  {
    title: '位置',
    dataIndex: 'location',
    width: 120
  },
  {
    title: '状态',
    dataIndex: 'status',
    slotName: 'status',
    width: 100
  },
  {
    title: '最后更新',
    dataIndex: 'lastUpdate',
    width: 160
  },
  {
    title: '操作',
    slotName: 'actions',
    width: 150,
    fixed: 'right'
  }
]

// 工具函数
const getDeviceIcon = (type: string) => {
  switch (type) {
    case 'server':
      return IconDesktop
    case 'network':
      return IconWifi
    case 'security':
      return IconLock
    default:
      return IconDesktop
  }
}

const getTypeColor = (type: string) => {
  switch (type) {
    case 'server':
      return 'blue'
    case 'network':
      return 'green'
    case 'security':
      return 'red'
    case 'storage':
      return 'orange'
    default:
      return 'gray'
  }
}

const getTypeName = (type: string) => {
  switch (type) {
    case 'server':
      return '服务器'
    case 'network':
      return '网络设备'
    case 'security':
      return '安全设备'
    case 'storage':
      return '存储设备'
    default:
      return '未知'
  }
}

const getStatusType = (status: string) => {
  switch (status) {
    case '在线':
      return 'success'
    case '异常':
      return 'warning'
    case '离线':
      return 'error'
    default:
      return 'default'
  }
}
</script>

<style scoped>
.assets-page {
  padding: 0;
}

.stats-row {
  margin-bottom: 24px;
}

.device-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.device-avatar {
  background: #1890ff;
}

.device-details {
  flex: 1;
}

.device-name {
  font-weight: 500;
  color: #1d2129;
  margin-bottom: 2px;
}

.device-model {
  font-size: 12px;
  color: #86909c;
}

:deep(.arco-card) {
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}
</style>
