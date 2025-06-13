<template>
  <div class="k8s-page">
    <PageHeader
      title="K8s集群日志"
      description="管理和监控Kubernetes集群的日志采集"
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
            添加集群
          </a-button>
        </a-space>
      </template>
    </PageHeader>

    <!-- 集群概览 -->
    <a-row :gutter="24" class="stats-row">
      <a-col :span="6">
        <StatCard
          :icon="IconCloud"
          icon-bg-color="#1890ff"
          :value="3"
          label="集群数量"
          subtitle="K8s集群"
        />
      </a-col>
      <a-col :span="6">
        <StatCard
          :icon="IconApps"
          icon-bg-color="#52c41a"
          :value="48"
          label="Pod数量"
          subtitle="运行中"
        />
      </a-col>
      <a-col :span="6">
        <StatCard
          :icon="IconFile"
          icon-bg-color="#faad14"
          :value="12560"
          label="今日日志"
          subtitle="条数统计"
        />
      </a-col>
      <a-col :span="6">
        <StatCard
          :icon="IconStorage"
          icon-bg-color="#722ed1"
          :value="3.8"
          label="存储空间(GB)"
          subtitle="日志占用"
        />
      </a-col>
    </a-row>

    <!-- 集群管理 -->
    <a-card title="集群管理" :bordered="false">
      <a-table
        :columns="clusterColumns"
        :data="clusterData"
        :pagination="false"
      >
        <template #clusterInfo="{ record }">
          <div class="cluster-info">
            <a-avatar size="small" class="cluster-avatar">
              <icon-cloud />
            </a-avatar>
            <div class="cluster-details">
              <div class="cluster-name">{{ record.name }}</div>
              <div class="cluster-version">{{ record.version }}</div>
            </div>
          </div>
        </template>

        <template #status="{ record }">
          <a-badge
            :status="record.status === 'running' ? 'success' : 'error'"
            :text="record.status === 'running' ? '运行中' : '异常'"
          />
        </template>

        <template #logLevel="{ record }">
          <a-tag :color="getLogLevelColor(record.logLevel)">
            {{ record.logLevel }}
          </a-tag>
        </template>

        <template #actions="{ record }">
          <a-space>
            <a-button type="text" size="small">查看Pods</a-button>
            <a-button type="text" size="small">查看日志</a-button>
            <a-button type="text" size="small">配置</a-button>
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
  IconCloud,
  IconApps,
  IconFile,
  IconStorage
} from '@arco-design/web-vue/es/icon'

// 集群数据
const clusterData = ref([
  {
    key: '1',
    name: 'prod-cluster-01',
    version: 'v1.28.2',
    nodes: 5,
    pods: 24,
    status: 'running',
    logLevel: 'INFO',
    endpoint: 'https://k8s-api.example.com'
  },
  {
    key: '2',
    name: 'dev-cluster-01',
    version: 'v1.27.8',
    nodes: 3,
    pods: 16,
    status: 'running',
    logLevel: 'DEBUG',
    endpoint: 'https://k8s-dev.example.com'
  }
])

// 表格列配置
const clusterColumns = [
  {
    title: '集群信息',
    dataIndex: 'name',
    slotName: 'clusterInfo',
    width: 200
  },
  {
    title: '节点数',
    dataIndex: 'nodes',
    width: 80
  },
  {
    title: 'Pod数',
    dataIndex: 'pods',
    width: 80
  },
  {
    title: '状态',
    dataIndex: 'status',
    slotName: 'status',
    width: 100
  },
  {
    title: '日志级别',
    dataIndex: 'logLevel',
    slotName: 'logLevel',
    width: 100
  },
  {
    title: 'API端点',
    dataIndex: 'endpoint',
    width: 250
  },
  {
    title: '操作',
    slotName: 'actions',
    width: 200,
    fixed: 'right'
  }
]

const getLogLevelColor = (level: string) => {
  switch (level) {
    case 'DEBUG':
      return 'blue'
    case 'INFO':
      return 'green'
    case 'WARN':
      return 'orange'
    case 'ERROR':
      return 'red'
    default:
      return 'gray'
  }
}
</script>

<style scoped>
.k8s-page {
  padding: 0;
}

.stats-row {
  margin-bottom: 24px;
}

.cluster-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.cluster-avatar {
  background: #1890ff;
}

.cluster-details {
  flex: 1;
}

.cluster-name {
  font-weight: 500;
  color: #1d2129;
  margin-bottom: 2px;
}

.cluster-version {
  font-size: 12px;
  color: #86909c;
}

:deep(.arco-card) {
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}
</style>
