<template>
  <div class="servers-page">
    <PageHeader title="服务器日志采集" description="管理和监控服务器的日志采集，分析系统运行状态">
      <template #extra>
        <a-space>
          <a-button @click="handleRefresh" :loading="refreshing">
            <template #icon>
              <icon-refresh />
            </template>
            刷新
          </a-button>
          <a-button type="primary" @click="startScan" :loading="scanning">
            <template #icon>
              <icon-search v-if="!scanning" />
              <icon-loading v-else />
            </template>
            {{ scanning ? '正在扫描...' : '开始扫描' }}
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
          :value="stats.online"
          label="在线服务器"
          subtitle="服务器总数"
        />
      </a-col>
      <a-col :span="6">
        <StatCard
          :icon="IconDownload"
          icon-bg-color="#1890ff"
          :value="stats.collecting"
          label="采集中"
          subtitle="正在采集日志"
        />
      </a-col>
      <a-col :span="6">
        <StatCard
          :icon="IconFile"
          icon-bg-color="#faad14"
          :value="stats.logCount"
          label="今日日志"
          subtitle="条数统计"
        />
      </a-col>
      <a-col :span="6">
        <StatCard
          :icon="IconCloudDownload"
          icon-bg-color="#722ed1"
          :value="stats.storageSize"
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
            <template #empty>
              <a-empty description="暂无服务器数据">
                <template #image>
                  <icon-desktop style="font-size: 64px; color: #86909c" />
                </template>
                <div style="margin-top: 16px">
                  <p style="color: #86909c; margin-bottom: 12px">
                    请点击上方的"开始扫描"按钮来发现网络中的服务器
                  </p>
                  <a-button type="primary" @click="startScan" :loading="scanning">
                    <template #icon>
                      <icon-search v-if="!scanning" />
                      <icon-loading v-else />
                    </template>
                    {{ scanning ? '正在扫描...' : '开始扫描' }}
                  </a-button>
                </div>
              </a-empty>
            </template>
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
              <a-tag :color="getServerTypeColor(record.serverType)" size="small">
                {{ record.serverType }}
              </a-tag>
            </template>

            <template #protocol="{ record }">
              <a-tag color="blue" size="small">{{ record.protocol }}</a-tag>
            </template>

            <template #status="{ record }">
              <a-badge :status="getStatusType(record.status)" :text="record.status" />
            </template>

            <template #collectStatus="{ record }">
              <a-badge
                :status="getCollectStatusType(record.collectStatus)"
                :text="record.collectStatus"
              />
            </template>

            <template #actions="{ record }">
              <a-space>
                <a-button type="text" size="small" @click="viewServerDetail(record)">
                  查看详情
                </a-button>
                <a-button type="text" size="small" status="warning" @click="stopCollection(record)">
                  停止采集
                </a-button>
                <a-button type="text" size="small" status="danger" @click="deleteServer(record)">
                  删除
                </a-button>
              </a-space>
            </template>
          </a-table>
        </a-card>
      </a-tab-pane>

      <a-tab-pane key="performance-monitor" title="性能监控">
        <a-card title="服务器性能监控" :bordered="false">
          <div v-if="serverData.length > 0" class="chart-placeholder">
            <div class="chart-content">
              <icon-settings class="chart-icon" />
              <p>服务器性能监控图表</p>
            </div>
          </div>
          <a-empty v-else description="暂无性能监控数据">
            <template #image>
              <icon-settings style="font-size: 64px; color: #86909c" />
            </template>
            <div style="margin-top: 16px">
              <p style="color: #86909c; margin-bottom: 12px">请先扫描服务器以开始性能监控</p>
            </div>
          </a-empty>
        </a-card>
      </a-tab-pane>

      <a-tab-pane key="system-analysis" title="系统分析">
        <a-card title="系统运行分析" :bordered="false">
          <div v-if="serverData.length > 0" class="chart-placeholder">
            <div class="chart-content">
              <icon-desktop class="chart-icon" />
              <p>系统资源使用分析报告</p>
            </div>
          </div>
          <a-empty v-else description="暂无系统分析数据">
            <template #image>
              <icon-desktop style="font-size: 64px; color: #86909c" />
            </template>
            <div style="margin-top: 16px">
              <p style="color: #86909c; margin-bottom: 12px">请先扫描服务器以获取系统分析数据</p>
            </div>
          </a-empty>
        </a-card>
      </a-tab-pane>

      <a-tab-pane key="log-view" title="日志查看">
        <a-card title="服务器日志查看" :bordered="false">
          <a-textarea
            v-if="serverData.length > 0"
            :model-value="logContent"
            :auto-size="{ minRows: 15, maxRows: 20 }"
            readonly
            placeholder="正在获取服务器日志..."
          />
          <a-empty v-else description="暂无日志数据">
            <template #image>
              <icon-file style="font-size: 64px; color: #86909c" />
            </template>
            <div style="margin-top: 16px">
              <p style="color: #86909c; margin-bottom: 12px">请先扫描服务器以获取日志数据</p>
            </div>
          </a-empty>
        </a-card>
      </a-tab-pane>

      <a-tab-pane key="real-time-monitor" title="实时监控">
        <a-card title="实时监控面板" :bordered="false">
          <div v-if="serverData.length > 0" class="monitor-grid">
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
            <a-row :gutter="16" style="margin-top: 16px">
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
          <a-empty v-else description="暂无监控数据">
            <template #image>
              <icon-cloud-download style="font-size: 64px; color: #86909c" />
            </template>
            <div style="margin-top: 16px">
              <p style="color: #86909c; margin-bottom: 12px">请先扫描服务器以开始实时监控</p>
            </div>
          </a-empty>
        </a-card>
      </a-tab-pane>
    </a-tabs>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { Message, Modal } from '@arco-design/web-vue'
import PageHeader from '@/components/PageHeader.vue'
import StatCard from '@/components/StatCard.vue'
import { assetsApi, type Asset } from '@/services/assets'
import { useRouter } from 'vue-router'
import {
  IconDesktop,
  IconDownload,
  IconFile,
  IconCloudDownload,
  IconRefresh,
  IconSearch,
  IconLoading,
  IconSettings,
} from '@arco-design/web-vue/es/icon'

const router = useRouter()

// 状态管理
const scanning = ref(false)
const refreshing = ref(false)

// 定时器引用，用于清理
const logCountTimer = ref<number | null>(null)
const storageSizeTimer = ref<number | null>(null)

// 服务器数据 - 初始为空，通过扫描发现
const serverData = ref<
  Array<{
    key: string
    hostname: string
    ip: string
    serverType: string
    protocol: string
    status: string
    collectStatus: string
  }>
>([])

// 统计数据
const stats = computed(() => {
  const total = serverData.value.length
  const online = serverData.value.filter((item) => item.status === '在线').length
  const collecting = serverData.value.filter((item) => item.collectStatus.includes('采集')).length

  return {
    total,
    online,
    collecting,
    logCount: logCount.value,
    storageSize: storageSize.value,
  }
})

// 表格列配置
const serverColumns = [
  {
    title: '服务器名称',
    dataIndex: 'hostname',
    slotName: 'serverInfo',
    width: 200,
  },
  {
    title: 'IP地址',
    dataIndex: 'ip',
    width: 120,
  },
  {
    title: '操作系统',
    dataIndex: 'serverType',
    slotName: 'serverType',
    width: 120,
  },
  {
    title: '协议',
    dataIndex: 'protocol',
    slotName: 'protocol',
    width: 80,
  },
  {
    title: '状态',
    dataIndex: 'status',
    slotName: 'status',
    width: 80,
  },
  {
    title: '采集状态',
    dataIndex: 'collectStatus',
    slotName: 'collectStatus',
    width: 150,
  },
  {
    title: '操作',
    slotName: 'actions',
    width: 200,
    fixed: 'right',
  },
]

// 监控数据
const avgCpuUsage = ref(35)
const avgMemoryUsage = ref(58)
const avgDiskUsage = ref(42)
const networkIO = ref(28)

// 统计数据 - 初始为0，扫描后增长
const logCount = ref(0)
const storageSize = ref(0)

// 日志内容 - 初始为空，扫描后显示
const logContent = ref('')

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

// 状态类型函数
const getStatusType = (status: string) => {
  switch (status) {
    case '在线':
      return 'success'
    case '离线':
      return 'error'
    case '异常':
      return 'warning'
    default:
      return 'default'
  }
}

const getCollectStatusType = (status: string) => {
  if (status.includes('实时采集')) return 'success'
  if (status.includes('采集中')) return 'processing'
  if (status.includes('停止')) return 'error'
  return 'default'
}

// 扫描功能
const startScan = async () => {
  try {
    scanning.value = true
    Message.loading({ content: '正在扫描网络中的服务器...', duration: 1000 })

    // 模拟扫描过程
    await new Promise((resolve) => setTimeout(resolve, 2000))

    let discoveredCount = 0

    // 首先添加预设的K8S集群服务器（模拟已存在的基础设施）
    const presetServers = [
      {
        key: '1',
        hostname: '分部K8S控制节点1',
        ip: '10.10.20.2',
        serverType: 'Ubuntu 22.04',
        protocol: 'syslog',
        status: '在线',
        collectStatus: '采集中...',
      },
      {
        key: '2',
        hostname: '分部K8S控制节点2',
        ip: '10.10.20.3',
        serverType: 'Ubuntu 22.04',
        protocol: 'syslog',
        status: '在线',
        collectStatus: '采集中...',
      },
      {
        key: '3',
        hostname: '分部K8S工作节点1',
        ip: '10.10.20.4',
        serverType: 'Ubuntu 22.04',
        protocol: 'syslog',
        status: '在线',
        collectStatus: '采集中...',
      },
      {
        key: '4',
        hostname: '分部K8S工作节点2',
        ip: '10.10.20.5',
        serverType: 'Ubuntu 22.04',
        protocol: 'syslog',
        status: '在线',
        collectStatus: '采集中...',
      },
    ]

    // 添加预设服务器
    serverData.value.push(...presetServers)
    discoveredCount += presetServers.length

    // 模拟预设服务器采集状态变化
    presetServers.forEach((server, index) => {
      setTimeout(
        () => {
          const foundServer = serverData.value.find((s) => s.key === server.key)
          if (foundServer) {
            foundServer.collectStatus = '已连接 - 实时采集中'
          }
        },
        1000 + index * 500,
      )
    })

    // 然后获取资产管理中的服务器资产
    try {
      const assets = await assetsApi.getAssets()
      const servers = assets.filter(
        (asset) => asset.asset_type === 'linux_server' || asset.asset_type === 'windows_server',
      )

      // 将新发现的服务器添加到列表中
      for (const asset of servers) {
        const existingServer = serverData.value.find((server) => server.ip === asset.ip_address)
        if (!existingServer) {
          const newServer = {
            key: (serverData.value.length + 1).toString(),
            hostname: asset.name,
            ip: asset.ip_address,
            serverType: asset.asset_type === 'linux_server' ? 'Linux Server' : 'Windows Server',
            protocol: asset.asset_type === 'linux_server' ? 'syslog' : 'winlog',
            status: asset.status === 'normal' ? '在线' : '离线',
            collectStatus: '采集中...',
          }

          serverData.value.push(newServer)
          discoveredCount++

          // 模拟采集状态变化
          setTimeout(() => {
            newServer.collectStatus = '已连接 - 实时采集中'
          }, 3000)
        }
      }
    } catch (apiError) {
      console.warn('无法获取资产管理数据，仅显示预设服务器:', apiError)
    }

    // 扫描完成后开始数据增长
    if (discoveredCount > 0) {
      // 开始日志计数增长
      startLogCountIncrement()

      // 开始存储空间增长
      startStorageSizeIncrement()

      // 生成日志内容
      setTimeout(() => {
        logContent.value = `[2024-01-15 10:35:05] INFO: 分部K8S控制节点1(10.10.20.2) - 集群网络通信正常，CNI插件工作正常
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
[2024-01-15 10:34:22] INFO: 系统日志采集完成，共采集${discoveredCount}台分部服务器数据
[2024-01-15 10:34:18] INFO: 分部网络连接稳定，集群间通信正常
[2024-01-15 10:34:15] DEBUG: Pod调度策略优化，资源利用率提升
[2024-01-15 10:34:12] INFO: 分部K8S集群扩容完成，新节点加入成功`
      }, 2000)
    }

    Message.success(`扫描完成！发现 ${discoveredCount} 台服务器`)
  } catch (error) {
    console.error('扫描失败:', error)
    Message.error('扫描失败，请重试')
  } finally {
    scanning.value = false
  }
}

// 刷新功能
const handleRefresh = () => {
  refreshing.value = true

  // 清理定时器
  clearTimers()

  // 重置所有数据
  serverData.value = []
  logContent.value = ''
  logCount.value = 0
  storageSize.value = 0

  setTimeout(() => {
    refreshing.value = false
    Message.success('刷新完成')
  }, 1000)
}

// 查看服务器详情
const viewServerDetail = (record: any) => {
  router.push({
    path: '/log-collection/server-detail',
    query: {
      hostname: record.hostname,
      ip: record.ip,
      serverType: record.serverType,
    },
  })
}

// 停止采集
const stopCollection = (record: any) => {
  Modal.confirm({
    title: '确认停止',
    content: `确定要停止服务器 "${record.hostname}" 的日志采集吗？`,
    onOk: () => {
      const server = serverData.value.find((s) => s.key === record.key)
      if (server) {
        server.collectStatus = '已停止采集'
        Message.success('日志采集已停止')
      }
    },
  })
}

// 删除服务器
const deleteServer = (record: any) => {
  Modal.confirm({
    title: '确认删除',
    content: `确定要删除服务器 "${record.hostname}" 吗？此操作不可恢复。`,
    onOk: () => {
      const index = serverData.value.findIndex((s) => s.key === record.key)
      if (index > -1) {
        serverData.value.splice(index, 1)
        Message.success('服务器删除成功')
      }
    },
  })
}

// 清理定时器函数
const clearTimers = () => {
  if (logCountTimer.value) {
    clearTimeout(logCountTimer.value)
    logCountTimer.value = null
  }
  if (storageSizeTimer.value) {
    clearTimeout(storageSizeTimer.value)
    storageSizeTimer.value = null
  }
}

// 日志计数增长函数
const startLogCountIncrement = () => {
  clearTimers() // 先清理之前的定时器

  const targetLogCount = 642
  const increment = () => {
    if (logCount.value < targetLogCount) {
      const randomIncrement = Math.floor(Math.random() * 15) + 5 // 5-19 随机增长
      logCount.value = Math.min(logCount.value + randomIncrement, targetLogCount)
      logCountTimer.value = window.setTimeout(increment, 1000 + Math.random() * 2000) // 1-3秒随机间隔
    }
  }
  // 延迟1秒开始增长
  logCountTimer.value = window.setTimeout(increment, 1000)
}

// 存储空间增长函数
const startStorageSizeIncrement = () => {
  const targetStorageSize = 2.4
  const increment = () => {
    if (storageSize.value < targetStorageSize) {
      const randomIncrement = Math.random() * 0.1 + 0.05 // 0.05-0.15 随机增长
      storageSize.value = Math.min(
        Math.round((storageSize.value + randomIncrement) * 10) / 10, // 保留1位小数
        targetStorageSize,
      )
      storageSizeTimer.value = window.setTimeout(increment, 1500 + Math.random() * 2000) // 1.5-3.5秒随机间隔
    }
  }
  // 延迟1.5秒开始增长
  storageSizeTimer.value = window.setTimeout(increment, 1500)
}

// 组件销毁时清理定时器
onUnmounted(() => {
  clearTimers()
})
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
