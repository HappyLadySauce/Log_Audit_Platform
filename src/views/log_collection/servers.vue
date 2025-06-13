<template>
  <div class="servers-page">
    <PageHeader
      title="服务器日志采集"
      description="管理和监控服务器的日志采集，分析系统运行状态"
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

    <!-- 统计卡片 -->
    <a-row :gutter="24" class="stats-row">
      <a-col :span="6">
        <StatCard
          :icon="IconDesktop"
          icon-bg-color="#52c41a"
          :value="4"
          label="在线服务器"
          subtitle="服务器总数"
        />
      </a-col>
      <a-col :span="6">
        <StatCard
          :icon="IconDownload"
          icon-bg-color="#1890ff"
          :value="4"
          label="采集中"
          subtitle="正在采集日志"
        />
      </a-col>
      <a-col :span="6">
        <StatCard
          :icon="IconFile"
          icon-bg-color="#faad14"
          :value="16800"
          label="今日日志"
          subtitle="条数统计"
        />
      </a-col>
      <a-col :span="6">
        <StatCard
          :icon="IconCloudDownload"
          icon-bg-color="#722ed1"
          :value="2.4"
          label="存储空间(GB)"
          subtitle="日志占用"
        />
      </a-col>
    </a-row>

    <!-- 服务器管理标签页 -->
    <a-tabs default-active-key="server-config" class="server-tabs">
      <a-tab-pane key="server-config" title="服务器配置">
        <a-card :bordered="false">
          <template #title>
            <a-space>
              <span>服务器配置</span>
              <a-tag color="blue">性能监控</a-tag>
              <a-tag color="green">系统分析</a-tag>
              <a-tag color="orange">日志查看</a-tag>
              <a-tag color="purple">实时监控</a-tag>
            </a-space>
          </template>
          
          <!-- 服务器列表 -->
          <a-table
            :columns="serverColumns"
            :data="serverData"
            :pagination="false"
            :scroll="{ x: '100%' }"
            class="server-table"
          >
            <template #serverInfo="{ record }">
              <div class="server-info">
                <a-avatar size="small" class="server-avatar">
                  <icon-desktop />
                </a-avatar>
                <div class="server-details">
                  <div class="server-name">{{ record.hostname }}</div>
                  <div class="server-ip">{{ record.ip }}</div>
                </div>
              </div>
            </template>

            <template #serverType="{ record }">
              <a-tag
                :color="getServerTypeColor(record.serverType)"
                size="small"
              >
                {{ record.serverType }}
              </a-tag>
            </template>

            <template #protocol="{ record }">
              <a-tag color="blue" size="small">{{ record.protocol }}</a-tag>
            </template>

            <template #status="{ record }">
              <a-badge
                :status="record.status === '在线' ? 'success' : 'error'"
                :text="record.status"
              />
            </template>

            <template #actions="{ record }">
              <a-space>
                <a-button
                  type="text"
                  size="small"
                  status="normal"
                  @click="editServer(record)"
                >
                  编辑
                </a-button>
                <a-button
                  type="text"
                  size="small"
                  status="warning"
                  @click="stopCollection(record)"
                >
                  停止采集
                </a-button>
                <a-button
                  type="text"
                  size="small"
                  status="danger"
                  @click="deleteServer(record)"
                >
                  删除
                </a-button>
              </a-space>
            </template>
          </a-table>
        </a-card>
      </a-tab-pane>

      <a-tab-pane key="performance-monitor" title="性能监控">
        <a-card title="服务器性能监控" :bordered="false">
          <div class="chart-placeholder">
            <div class="chart-content">
              <icon-settings class="chart-icon" />
              <p>服务器性能监控图表</p>
            </div>
          </div>
        </a-card>
      </a-tab-pane>

      <a-tab-pane key="system-analysis" title="系统分析">
        <a-card title="系统运行分析" :bordered="false">
          <div class="chart-placeholder">
            <div class="chart-content">
              <icon-desktop class="chart-icon" />
              <p>系统资源使用分析报告</p>
            </div>
          </div>
        </a-card>
      </a-tab-pane>

      <a-tab-pane key="log-view" title="日志查看">
        <a-card title="服务器日志查看" :bordered="false">
          <a-textarea
            :model-value="logContent"
            :auto-size="{ minRows: 15, maxRows: 20 }"
            readonly
            placeholder="服务器日志将在这里显示..."
          />
        </a-card>
      </a-tab-pane>

      <a-tab-pane key="real-time-monitor" title="实时监控">
        <a-card title="实时监控面板" :bordered="false">
          <div class="monitor-grid">
            <a-row :gutter="16">
              <a-col :span="12">
                <div class="monitor-item">
                  <h4>平均CPU使用率</h4>
                  <a-progress :percent="avgCpuUsage" :show-text="false" />
                  <span class="monitor-value">{{ avgCpuUsage }}%</span>
                </div>
              </a-col>
              <a-col :span="12">
                <div class="monitor-item">
                  <h4>平均内存使用率</h4>
                  <a-progress :percent="avgMemoryUsage" :show-text="false" status="success" />
                  <span class="monitor-value">{{ avgMemoryUsage }}%</span>
                </div>
              </a-col>
            </a-row>
            <a-row :gutter="16" style="margin-top: 16px;">
              <a-col :span="12">
                <div class="monitor-item">
                  <h4>磁盘使用率</h4>
                  <a-progress :percent="avgDiskUsage" :show-text="false" status="warning" />
                  <span class="monitor-value">{{ avgDiskUsage }}%</span>
                </div>
              </a-col>
              <a-col :span="12">
                <div class="monitor-item">
                  <h4>网络IO</h4>
                  <a-progress :percent="networkIO" :show-text="false" status="danger" />
                  <span class="monitor-value">{{ networkIO }}%</span>
                </div>
              </a-col>
            </a-row>
          </div>
        </a-card>
      </a-tab-pane>
    </a-tabs>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import PageHeader from '@/components/PageHeader.vue'
import StatCard from '@/components/StatCard.vue'
import {
  IconDesktop,
  IconDownload,
  IconFile,
  IconCloudDownload,
  IconRefresh,
  IconPlus,
  IconSettings
} from '@arco-design/web-vue/es/icon'

// 服务器数据
const serverData = ref([
  {
    key: '1',
    hostname: '分部K8S控制节点1',
    ip: '10.10.20.2',
    serverType: 'Ubuntu 22.04',
    protocol: 'syslog',
    status: '在线'
  },
  {
    key: '2',
    hostname: '分部K8S控制节点2',
    ip: '10.10.20.3',
    serverType: 'Ubuntu 22.04',
    protocol: 'syslog',
    status: '在线'
  },
  {
    key: '3',
    hostname: '分部K8S工作节点1',
    ip: '10.10.20.4',
    serverType: 'Ubuntu 22.04',
    protocol: 'syslog',
    status: '在线'
  },
  {
    key: '4',
    hostname: '分部K8S工作节点2',
    ip: '10.10.20.5',
    serverType: 'Ubuntu 22.04',
    protocol: 'syslog',
    status: '在线'
  }
])

// 表格列配置
const serverColumns = [
  {
    title: '服务器名称',
    dataIndex: 'hostname',
    slotName: 'serverInfo',
    width: 250
  },
  {
    title: 'IP地址',
    dataIndex: 'ip',
    width: 120
  },
  {
    title: '操作系统',
    dataIndex: 'serverType',
    slotName: 'serverType',
    width: 120
  },
  {
    title: '协议',
    dataIndex: 'protocol',
    slotName: 'protocol',
    width: 80
  },
  {
    title: '状态',
    dataIndex: 'status',
    slotName: 'status',
    width: 80
  },
  {
    title: '操作',
    slotName: 'actions',
    width: 180,
    fixed: 'right'
  }
]

// 监控数据
const avgCpuUsage = ref(35)
const avgMemoryUsage = ref(58)
const avgDiskUsage = ref(42)
const networkIO = ref(28)

// 日志内容
const logContent = ref(`[2024-01-15 10:35:05] INFO: 分部K8S控制节点1(10.10.20.2) - 集群网络通信正常，CNI插件工作正常
[2024-01-15 10:35:02] INFO: 分部K8S控制节点2(10.10.20.3) - 负载均衡器工作正常，Service状态: Active
[2024-01-15 10:34:58] DEBUG: 分部K8S工作节点1(10.10.20.4) - 内存使用率: 45%，可用内存: 12GB
[2024-01-15 10:34:55] INFO: 分部K8S工作节点2(10.10.20.5) - 磁盘I/O性能正常，IOPS: 2500
[2024-01-15 10:34:48] DEBUG: 分部Kubernetes集群状态检查完成，所有节点健康
[2024-01-15 10:34:45] INFO: 容器镜像拉取正常，镜像仓库连接稳定
[2024-01-15 10:34:42] INFO: 服务发现功能正常，Ingress控制器工作正常
[2024-01-15 10:34:38] DEBUG: 持久化存储检查完成，StorageClass配置正确
[2024-01-15 10:34:35] INFO: 集群安全策略更新，RBAC权限配置生效
[2024-01-15 10:34:32] INFO: 监控指标收集正常，Prometheus采集成功
[2024-01-15 10:34:28] DEBUG: 日志聚合服务正常，ElasticSearch索引更新
[2024-01-15 10:34:25] INFO: 备份任务执行完成，数据完整性检查通过
[2024-01-15 10:34:22] INFO: 系统日志采集完成，共采集4台分部服务器数据
[2024-01-15 10:34:18] INFO: 分部网络连接稳定，集群间通信正常
[2024-01-15 10:34:15] DEBUG: Pod调度策略优化，资源利用率提升
[2024-01-15 10:34:12] INFO: 分部K8S集群扩容完成，新节点加入成功`)

// 获取服务器类型颜色
const getServerTypeColor = (type: string) => {
  switch (type) {
    case 'Ubuntu 22.04':
      return 'orange'
    case 'CentOS 8':
      return 'red'
    case 'RHEL 9':
      return 'blue'
    case 'Windows Server':
      return 'purple'
    default:
      return 'gray'
  }
}

// 操作方法
const editServer = (record: any) => {
  console.log('编辑服务器:', record)
}

const stopCollection = (record: any) => {
  console.log('停止采集:', record)
}

const deleteServer = (record: any) => {
  console.log('删除服务器:', record)
}
</script>

<style scoped>
.servers-page {
  padding: 0;
}

.stats-row {
  margin-bottom: 24px;
}

.server-tabs {
  margin-bottom: 0;
}

.server-table {
  margin-top: 16px;
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

.chart-placeholder {
  height: 300px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #fafafa;
  border-radius: 6px;
}

.chart-content {
  text-align: center;
  color: #86909c;
}

.chart-icon {
  font-size: 48px;
  margin-bottom: 16px;
}

.monitor-grid {
  padding: 16px 0;
}

.monitor-item {
  padding: 16px;
  background: #fafafa;
  border-radius: 6px;
  position: relative;
}

.monitor-item h4 {
  margin: 0 0 12px 0;
  font-size: 14px;
  color: #1d2129;
}

.monitor-value {
  position: absolute;
  right: 16px;
  top: 16px;
  font-weight: 500;
  color: #1d2129;
}

:deep(.arco-card) {
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

:deep(.arco-tabs-content) {
  padding-top: 0;
}
</style>
