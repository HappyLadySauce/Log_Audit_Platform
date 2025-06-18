<template>
  <div class="server-detail-page">
    <PageHeader
      :title="`服务器详情 - ${serverInfo.hostname}`"
      :description="`查看 ${serverInfo.ip} 的实时日志和系统状态`"
    >
      <template #extra>
        <a-space>
          <a-button @click="handleBack">
            <template #icon>
              <icon-left />
            </template>
            返回
          </a-button>
          <a-button @click="toggleAutoRefresh" :type="autoRefresh ? 'primary' : 'outline'">
            <template #icon>
              <icon-refresh v-if="!autoRefresh" />
              <icon-pause v-else />
            </template>
            {{ autoRefresh ? '暂停刷新' : '自动刷新' }}
          </a-button>
          <a-button @click="clearLogs">
            <template #icon>
              <icon-delete />
            </template>
            清空日志
          </a-button>
        </a-space>
      </template>
    </PageHeader>

    <!-- 服务器基本信息 -->
    <a-card title="基本信息" :bordered="false" class="info-card">
      <a-row :gutter="24">
        <a-col :span="6">
          <div class="info-item">
            <div class="info-label">服务器名称</div>
            <div class="info-value">{{ serverInfo.hostname }}</div>
          </div>
        </a-col>
        <a-col :span="6">
          <div class="info-item">
            <div class="info-label">IP地址</div>
            <div class="info-value">{{ serverInfo.ip }}</div>
          </div>
        </a-col>
        <a-col :span="6">
          <div class="info-item">
            <div class="info-label">操作系统</div>
            <div class="info-value">{{ serverInfo.serverType }}</div>
          </div>
        </a-col>
        <a-col :span="6">
          <div class="info-item">
            <div class="info-label">连接状态</div>
            <a-badge status="success" text="已连接" />
          </div>
        </a-col>
      </a-row>
    </a-card>

    <!-- 实时日志 -->
    <a-card title="实时日志" :bordered="false" class="log-card">
      <template #extra>
        <a-space>
          <a-tag color="green">实时采集中</a-tag>
          <span class="log-count">{{ logLines.length }} 条日志</span>
        </a-space>
      </template>

      <div class="log-container" ref="logContainer">
        <div
          v-for="(log, index) in logLines"
          :key="index"
          class="log-line"
          :class="getLogLevelClass(log.level)"
        >
          <span class="log-timestamp">{{ log.timestamp }}</span>
          <span class="log-level">[{{ log.level }}]</span>
          <span class="log-content">{{ log.content }}</span>
        </div>

        <div v-if="logLines.length === 0" class="log-empty">
          <icon-file-text class="empty-icon" />
          <p>暂无日志数据</p>
        </div>
      </div>
    </a-card>

    <!-- 系统状态 -->
    <a-card title="系统状态" :bordered="false" class="status-card">
      <a-row :gutter="16">
        <a-col :span="6">
          <div class="status-item">
            <h4>CPU使用率</h4>
            <a-progress :percent="systemStats.cpu" :show-text="false" />
            <span class="status-value">{{ systemStats.cpu }}%</span>
          </div>
        </a-col>
        <a-col :span="6">
          <div class="status-item">
            <h4>内存使用率</h4>
            <a-progress :percent="systemStats.memory" :show-text="false" status="success" />
            <span class="status-value">{{ systemStats.memory }}%</span>
          </div>
        </a-col>
        <a-col :span="6">
          <div class="status-item">
            <h4>磁盘使用率</h4>
            <a-progress :percent="systemStats.disk" :show-text="false" status="warning" />
            <span class="status-value">{{ systemStats.disk }}%</span>
          </div>
        </a-col>
        <a-col :span="6">
          <div class="status-item">
            <h4>网络IO</h4>
            <a-progress :percent="systemStats.network" :show-text="false" status="danger" />
            <span class="status-value">{{ systemStats.network }} MB/s</span>
          </div>
        </a-col>
      </a-row>
    </a-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, nextTick } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { Message } from '@arco-design/web-vue'
import PageHeader from '@/components/PageHeader.vue'
import {
  IconLeft,
  IconRefresh,
  IconPause,
  IconDelete,
  IconFileText,
} from '@arco-design/web-vue/es/icon'

const route = useRoute()
const router = useRouter()

// 服务器信息
const serverInfo = ref({
  hostname: (route.query.hostname as string) || '未知服务器',
  ip: (route.query.ip as string) || '0.0.0.0',
  serverType: (route.query.serverType as string) || 'Linux Server',
})

// 日志相关
const logContainer = ref<HTMLElement>()
const logLines = ref<
  Array<{
    timestamp: string
    level: string
    content: string
  }>
>([])

// 自动刷新控制
const autoRefresh = ref(true)
let refreshTimer: number | null = null

// 系统状态
const systemStats = ref({
  cpu: 35,
  memory: 58,
  disk: 42,
  network: 128,
})

// 模拟日志数据生成器
const generateMockLog = (): { timestamp: string; level: string; content: string } => {
  const now = new Date()
  const timestamp = now.toLocaleString('zh-CN', {
    hour12: false,
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit',
  })

  const levels = ['INFO', 'DEBUG', 'WARN', 'ERROR']
  const level = levels[Math.floor(Math.random() * levels.length)]

  const mockContents = [
    `${serverInfo.value.hostname} - 系统运行正常，CPU使用率: ${systemStats.value.cpu}%`,
    `${serverInfo.value.hostname} - 网络连接稳定，延迟: ${Math.floor(Math.random() * 10 + 5)}ms`,
    `${serverInfo.value.hostname} - 磁盘I/O操作完成，处理 ${Math.floor(Math.random() * 1000 + 100)} 个请求`,
    `${serverInfo.value.hostname} - 内存清理完成，释放 ${Math.floor(Math.random() * 500 + 50)}MB 空间`,
    `${serverInfo.value.hostname} - 服务进程检查完成，所有服务运行正常`,
    `${serverInfo.value.hostname} - 安全扫描完成，未发现威胁`,
    `${serverInfo.value.hostname} - 备份任务执行中，进度: ${Math.floor(Math.random() * 100)}%`,
    `${serverInfo.value.hostname} - 日志轮转完成，归档 ${Math.floor(Math.random() * 10 + 1)} 个文件`,
    `${serverInfo.value.hostname} - 监控指标更新，所有指标正常`,
    `${serverInfo.value.hostname} - 用户会话管理，当前活跃用户: ${Math.floor(Math.random() * 20 + 1)}`,
  ]

  const content = mockContents[Math.floor(Math.random() * mockContents.length)]

  return { timestamp, level, content }
}

// 添加新日志
const addNewLog = () => {
  if (!autoRefresh.value) return

  const newLog = generateMockLog()
  logLines.value.push(newLog)

  // 限制日志行数，避免过多日志影响性能
  if (logLines.value.length > 200) {
    logLines.value.shift()
  }

  // 自动滚动到底部
  nextTick(() => {
    if (logContainer.value) {
      logContainer.value.scrollTop = logContainer.value.scrollHeight
    }
  })
}

// 更新系统状态
const updateSystemStats = () => {
  systemStats.value = {
    cpu: Math.floor(Math.random() * 40 + 20), // 20-60%
    memory: Math.floor(Math.random() * 30 + 40), // 40-70%
    disk: Math.floor(Math.random() * 20 + 30), // 30-50%
    network: Math.floor(Math.random() * 200 + 50), // 50-250 MB/s
  }
}

// 获取日志级别样式类
const getLogLevelClass = (level: string) => {
  switch (level) {
    case 'ERROR':
      return 'log-error'
    case 'WARN':
      return 'log-warn'
    case 'DEBUG':
      return 'log-debug'
    default:
      return 'log-info'
  }
}

// 切换自动刷新
const toggleAutoRefresh = () => {
  autoRefresh.value = !autoRefresh.value
  Message.info(autoRefresh.value ? '已开启自动刷新' : '已暂停自动刷新')
}

// 清空日志
const clearLogs = () => {
  logLines.value = []
  Message.success('日志已清空')
}

// 返回
const handleBack = () => {
  router.back()
}

// 生命周期
onMounted(() => {
  // 初始化日志
  for (let i = 0; i < 10; i++) {
    logLines.value.push(generateMockLog())
  }

  // 启动定时器
  refreshTimer = setInterval(() => {
    addNewLog()
    updateSystemStats()
  }, 2000) // 每2秒添加新日志
})

onUnmounted(() => {
  if (refreshTimer) {
    clearInterval(refreshTimer)
  }
})
</script>

<style scoped>
.server-detail-page {
  padding: 0;
}

.info-card,
.log-card,
.status-card {
  margin-bottom: 24px;
}

.info-item {
  text-align: center;
  padding: 16px;
  background: #fafafa;
  border-radius: 6px;
}

.info-label {
  font-size: 12px;
  color: #86909c;
  margin-bottom: 8px;
}

.info-value {
  font-size: 16px;
  font-weight: 500;
  color: #1d2129;
}

.log-container {
  height: 500px;
  overflow-y: auto;
  background: #1e1e1e;
  border-radius: 6px;
  padding: 16px;
  font-family: 'Courier New', monospace;
  font-size: 12px;
  line-height: 1.5;
}

.log-line {
  margin-bottom: 4px;
  word-wrap: break-word;
}

.log-timestamp {
  color: #86909c;
  margin-right: 8px;
}

.log-level {
  margin-right: 8px;
  font-weight: bold;
}

.log-content {
  color: #f0f0f0;
}

.log-info .log-level {
  color: #52c41a;
}

.log-debug .log-level {
  color: #1890ff;
}

.log-warn .log-level {
  color: #faad14;
}

.log-error .log-level {
  color: #f5222d;
}

.log-empty {
  text-align: center;
  color: #86909c;
  padding: 50px 0;
}

.empty-icon {
  font-size: 48px;
  margin-bottom: 16px;
}

.log-count {
  color: #86909c;
  font-size: 12px;
}

.status-item {
  padding: 16px;
  background: #fafafa;
  border-radius: 6px;
  position: relative;
}

.status-item h4 {
  margin: 0 0 12px 0;
  font-size: 14px;
  color: #1d2129;
}

.status-value {
  position: absolute;
  right: 16px;
  top: 50%;
  transform: translateY(-50%);
  font-weight: 500;
  color: #1d2129;
}
</style>
