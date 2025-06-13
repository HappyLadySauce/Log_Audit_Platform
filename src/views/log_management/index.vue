<template>
  <div class="log-management-page">
    <PageHeader
      title="日志管理"
      description="统一管理和查询各类系统日志"
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
              <icon-search />
            </template>
            高级搜索
          </a-button>
        </a-space>
      </template>
    </PageHeader>

    <!-- 日志搜索栏 -->
    <a-card :bordered="false" class="search-card">
      <a-row :gutter="16">
        <a-col :span="8">
          <a-input
            placeholder="关键词搜索..."
            allow-clear
          >
            <template #prefix>
              <icon-search />
            </template>
          </a-input>
        </a-col>
        <a-col :span="4">
          <a-select placeholder="日志级别" allow-clear>
            <a-option value="INFO">INFO</a-option>
            <a-option value="WARN">WARN</a-option>
            <a-option value="ERROR">ERROR</a-option>
            <a-option value="DEBUG">DEBUG</a-option>
          </a-select>
        </a-col>
        <a-col :span="4">
          <a-select placeholder="日志来源" allow-clear>
            <a-option value="system">系统日志</a-option>
            <a-option value="application">应用日志</a-option>
            <a-option value="security">安全日志</a-option>
            <a-option value="network">网络日志</a-option>
          </a-select>
        </a-col>
        <a-col :span="6">
          <a-range-picker style="width: 100%" />
        </a-col>
        <a-col :span="2">
          <a-button type="primary" style="width: 100%">搜索</a-button>
        </a-col>
      </a-row>
    </a-card>

    <!-- 日志统计 -->
    <a-row :gutter="24" class="stats-row">
      <a-col :span="6">
        <StatCard
          :icon="IconFile"
          icon-bg-color="#1890ff"
          :value="45820"
          label="总日志数"
          subtitle="今日统计"
        />
      </a-col>
      <a-col :span="6">
        <StatCard
          :icon="IconCheck"
          icon-bg-color="#52c41a"
          :value="42156"
          label="正常日志"
          subtitle="INFO级别"
        />
      </a-col>
      <a-col :span="6">
        <StatCard
          :icon="IconExclamation"
          icon-bg-color="#faad14"
          :value="3426"
          label="警告日志"
          subtitle="WARN级别"
        />
      </a-col>
      <a-col :span="6">
        <StatCard
          :icon="IconClose"
          icon-bg-color="#f5222d"
          :value="238"
          label="错误日志"
          subtitle="ERROR级别"
        />
      </a-col>
    </a-row>

    <!-- 日志列表 -->
    <a-card title="日志记录" :bordered="false">
      <a-table
        :columns="logColumns"
        :data="logData"
        :pagination="{ pageSize: 15 }"
        :scroll="{ x: '100%' }"
      >
        <template #level="{ record }">
          <a-tag :color="getLevelColor(record.level)">
            {{ record.level }}
          </a-tag>
        </template>

        <template #source="{ record }">
          <div class="source-info">
            <component :is="getSourceIcon(record.source)" class="source-icon" />
            <span>{{ getSourceName(record.source) }}</span>
          </div>
        </template>

        <template #message="{ record }">
          <div class="log-message">
            {{ record.message }}
          </div>
        </template>

        <template #actions="{ record }">
          <a-space>
            <a-button type="text" size="small">详情</a-button>
            <a-button type="text" size="small">上下文</a-button>
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
  IconSearch,
  IconFile,
  IconCheck,
  IconExclamation,
  IconClose,
  IconDesktop,
  IconWifi,
  IconLock
} from '@arco-design/web-vue/es/icon'

// 日志数据
const logData = ref([
  {
    key: '1',
    timestamp: '2024-01-15 10:30:15',
    level: 'INFO',
    source: 'system',
    host: 'web-server-01',
    message: '用户登录成功: username=admin, ip=192.168.1.100'
  },
  {
    key: '2',
    timestamp: '2024-01-15 10:29:45',
    level: 'WARN',
    source: 'application',
    host: 'app-server-01',
    message: '数据库连接池使用率过高: current=85%, threshold=80%'
  },
  {
    key: '3',
    timestamp: '2024-01-15 10:29:30',
    level: 'ERROR',
    source: 'network',
    host: 'router-01',
    message: '网络连接超时: target=192.168.1.254, timeout=5000ms'
  }
])

// 表格列配置
const logColumns = [
  {
    title: '时间',
    dataIndex: 'timestamp',
    width: 160
  },
  {
    title: '级别',
    dataIndex: 'level',
    slotName: 'level',
    width: 80
  },
  {
    title: '来源',
    dataIndex: 'source',
    slotName: 'source',
    width: 120
  },
  {
    title: '主机',
    dataIndex: 'host',
    width: 120
  },
  {
    title: '消息',
    dataIndex: 'message',
    slotName: 'message',
    ellipsis: true
  },
  {
    title: '操作',
    slotName: 'actions',
    width: 120,
    fixed: 'right'
  }
]

// 工具函数
const getLevelColor = (level: string) => {
  switch (level) {
    case 'INFO':
      return 'blue'
    case 'WARN':
      return 'orange'
    case 'ERROR':
      return 'red'
    case 'DEBUG':
      return 'gray'
    default:
      return 'default'
  }
}

const getSourceIcon = (source: string) => {
  switch (source) {
    case 'system':
      return IconDesktop
    case 'application':
      return IconDesktop
    case 'network':
      return IconWifi
    case 'security':
      return IconLock
    default:
      return IconFile
  }
}

const getSourceName = (source: string) => {
  switch (source) {
    case 'system':
      return '系统日志'
    case 'application':
      return '应用日志'
    case 'network':
      return '网络日志'
    case 'security':
      return '安全日志'
    default:
      return '未知来源'
  }
}
</script>

<style scoped>
.log-management-page {
  padding: 0;
}

.search-card {
  margin-bottom: 24px;
}

.stats-row {
  margin-bottom: 24px;
}

.source-info {
  display: flex;
  align-items: center;
  gap: 8px;
}

.source-icon {
  font-size: 14px;
  color: #86909c;
}

.log-message {
  max-width: 400px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

:deep(.arco-card) {
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}
</style>
