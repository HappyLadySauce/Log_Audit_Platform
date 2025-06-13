<template>
  <div class="alert-page">
    <PageHeader
      title="告警管理"
      description="管理和处理系统告警信息"
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
            添加规则
          </a-button>
        </a-space>
      </template>
    </PageHeader>

    <!-- 告警统计 -->
    <a-row :gutter="24" class="stats-row">
      <a-col :span="6">
        <StatCard
          :icon="IconNotification"
          icon-bg-color="#f5222d"
          :value="23"
          label="活跃告警"
          subtitle="待处理"
        />
      </a-col>
      <a-col :span="6">
        <StatCard
          :icon="IconExclamation"
          icon-bg-color="#faad14"
          :value="156"
          label="今日告警"
          subtitle="总数统计"
        />
      </a-col>
      <a-col :span="6">
        <StatCard
          :icon="IconCheck"
          icon-bg-color="#52c41a"
          :value="98"
          label="已处理"
          subtitle="处理完成"
        />
      </a-col>
      <a-col :span="6">
        <StatCard
          :icon="IconSettings"
          icon-bg-color="#1890ff"
          :value="45"
          label="告警规则"
          subtitle="配置数量"
        />
      </a-col>
    </a-row>

    <!-- 告警列表 -->
    <a-card title="告警记录" :bordered="false">
      <template #extra>
        <a-space>
          <a-select placeholder="告警级别" style="width: 120px" allow-clear>
            <a-option value="critical">严重</a-option>
            <a-option value="warning">警告</a-option>
            <a-option value="info">信息</a-option>
          </a-select>
          <a-select placeholder="处理状态" style="width: 120px" allow-clear>
            <a-option value="pending">待处理</a-option>
            <a-option value="processing">处理中</a-option>
            <a-option value="resolved">已解决</a-option>
          </a-select>
        </a-space>
      </template>

      <a-table
        :columns="alertColumns"
        :data="alertData"
        :pagination="{ pageSize: 10 }"
      >
        <template #severity="{ record }">
          <a-tag :color="getSeverityColor(record.severity)">
            {{ getSeverityText(record.severity) }}
          </a-tag>
        </template>

        <template #status="{ record }">
          <a-badge
            :status="getStatusType(record.status)"
            :text="getStatusText(record.status)"
          />
        </template>

        <template #actions="{ record }">
          <a-space>
            <a-button type="text" size="small">处理</a-button>
            <a-button type="text" size="small">详情</a-button>
            <a-button type="text" size="small" status="danger">忽略</a-button>
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
  IconNotification,
  IconExclamation,
  IconCheck,
  IconSettings
} from '@arco-design/web-vue/es/icon'

// 告警数据
const alertData = ref([
  {
    key: '1',
    title: 'CPU使用率过高',
    description: '服务器 web-01 CPU使用率达到 95%',
    severity: 'critical',
    status: 'pending',
    source: 'web-server-01',
    timestamp: '2024-01-15 10:30:00'
  },
  {
    key: '2',
    title: '磁盘空间不足',
    description: '磁盘 /dev/sda1 剩余空间仅 5%',
    severity: 'warning',
    status: 'processing',
    source: 'db-server-01',
    timestamp: '2024-01-15 10:25:00'
  },
  {
    key: '3',
    title: '网络连接异常',
    description: '网络设备连接中断',
    severity: 'critical',
    status: 'resolved',
    source: 'router-01',
    timestamp: '2024-01-15 10:20:00'
  }
])

// 表格列配置
const alertColumns = [
  {
    title: '告警标题',
    dataIndex: 'title',
    width: 200
  },
  {
    title: '描述',
    dataIndex: 'description',
    ellipsis: true
  },
  {
    title: '级别',
    dataIndex: 'severity',
    slotName: 'severity',
    width: 80
  },
  {
    title: '状态',
    dataIndex: 'status',
    slotName: 'status',
    width: 100
  },
  {
    title: '来源',
    dataIndex: 'source',
    width: 120
  },
  {
    title: '时间',
    dataIndex: 'timestamp',
    width: 160
  },
  {
    title: '操作',
    slotName: 'actions',
    width: 180,
    fixed: 'right'
  }
]

// 工具函数
const getSeverityColor = (severity: string) => {
  switch (severity) {
    case 'critical':
      return 'red'
    case 'warning':
      return 'orange'
    case 'info':
      return 'blue'
    default:
      return 'gray'
  }
}

const getSeverityText = (severity: string) => {
  switch (severity) {
    case 'critical':
      return '严重'
    case 'warning':
      return '警告'
    case 'info':
      return '信息'
    default:
      return '未知'
  }
}

const getStatusType = (status: string) => {
  switch (status) {
    case 'pending':
      return 'danger'
    case 'processing':
      return 'warning'
    case 'resolved':
      return 'success'
    default:
      return 'default'
  }
}

const getStatusText = (status: string) => {
  switch (status) {
    case 'pending':
      return '待处理'
    case 'processing':
      return '处理中'
    case 'resolved':
      return '已解决'
    default:
      return '未知'
  }
}
</script>

<style scoped>
.alert-page {
  padding: 0;
}

.stats-row {
  margin-bottom: 24px;
}

:deep(.arco-card) {
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}
</style> 