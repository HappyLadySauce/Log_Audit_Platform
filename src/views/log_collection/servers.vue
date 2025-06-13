<template>
  <div class="servers-page">
    <PageHeader
      title="Linux服务器日志"
      description="管理和监控Linux服务器的日志采集"
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
            添加服务器
          </a-button>
        </a-space>
      </template>
    </PageHeader>

    <!-- 统计信息 -->
    <a-row :gutter="24" class="stats-row">
      <a-col :span="6">
        <StatCard
          :icon="IconDesktop"
          icon-bg-color="#1890ff"
          :value="24"
          label="服务器数量"
          subtitle="Linux服务器"
        />
      </a-col>
      <a-col :span="6">
        <StatCard
          :icon="IconCheck"
          icon-bg-color="#52c41a"
          :value="20"
          label="正常运行"
          subtitle="健康状态"
        />
      </a-col>
      <a-col :span="6">
        <StatCard
          :icon="IconFile"
          icon-bg-color="#faad14"
          :value="8640"
          label="今日日志"
          subtitle="条数统计"
        />
      </a-col>
      <a-col :span="6">
        <StatCard
          :icon="IconCloudDownload"
          icon-bg-color="#722ed1"
          :value="1.2"
          label="存储空间(GB)"
          subtitle="日志占用"
        />
      </a-col>
    </a-row>

    <!-- 服务器列表 -->
    <a-card title="服务器列表" :bordered="false">
      <a-table
        :columns="serverColumns"
        :data="serverData"
        :pagination="{ pageSize: 10 }"
      >
        <template #serverInfo="{ record }">
          <div class="server-info">
            <a-avatar size="small" class="server-avatar">
              <icon-server />
            </a-avatar>
            <div class="server-details">
              <div class="server-name">{{ record.hostname }}</div>
              <div class="server-ip">{{ record.ip }}</div>
            </div>
          </div>
        </template>

        <template #os="{ record }">
          <a-tag color="blue">{{ record.os }}</a-tag>
        </template>

        <template #status="{ record }">
          <a-badge
            :status="record.status === 'online' ? 'success' : 'error'"
            :text="record.status === 'online' ? '在线' : '离线'"
          />
        </template>

        <template #logStatus="{ record }">
          <a-tag
            :color="record.logStatus === 'collecting' ? 'green' : 'orange'"
          >
            {{ record.logStatus === 'collecting' ? '采集中' : '暂停' }}
          </a-tag>
        </template>

        <template #actions="{ record }">
          <a-space>
            <a-button type="text" size="small">查看日志</a-button>
            <a-button type="text" size="small">配置</a-button>
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
  IconFile,
  IconCloudDownload
} from '@arco-design/web-vue/es/icon'

// 服务器数据
const serverData = ref([
  {
    key: '1',
    hostname: 'web-server-01',
    ip: '192.168.1.101',
    os: 'Ubuntu 22.04',
    status: 'online',
    logStatus: 'collecting',
    lastLogTime: '2024-01-15 10:30:15'
  },
  {
    key: '2',
    hostname: 'db-server-01',
    ip: '192.168.1.102',
    os: 'CentOS 8',
    status: 'online',
    logStatus: 'collecting',
    lastLogTime: '2024-01-15 10:29:50'
  },
  {
    key: '3',
    hostname: 'app-server-01',
    ip: '192.168.1.103',
    os: 'RHEL 9',
    status: 'offline',
    logStatus: 'stopped',
    lastLogTime: '2024-01-15 09:15:30'
  }
])

// 表格列配置
const serverColumns = [
  {
    title: '服务器信息',
    dataIndex: 'hostname',
    slotName: 'serverInfo',
    width: 200
  },
  {
    title: '操作系统',
    dataIndex: 'os',
    slotName: 'os',
    width: 120
  },
  {
    title: '状态',
    dataIndex: 'status',
    slotName: 'status',
    width: 80
  },
  {
    title: '日志采集',
    dataIndex: 'logStatus',
    slotName: 'logStatus',
    width: 100
  },
  {
    title: '最后日志时间',
    dataIndex: 'lastLogTime',
    width: 160
  },
  {
    title: '操作',
    slotName: 'actions',
    width: 180,
    fixed: 'right'
  }
]
</script>

<style scoped>
.servers-page {
  padding: 0;
}

.stats-row {
  margin-bottom: 24px;
}

.server-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.server-avatar {
  background: #1890ff;
}

.server-details {
  flex: 1;
}

.server-name {
  font-weight: 500;
  color: #1d2129;
  margin-bottom: 2px;
}

.server-ip {
  font-size: 12px;
  color: #86909c;
}

:deep(.arco-card) {
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}
</style>
