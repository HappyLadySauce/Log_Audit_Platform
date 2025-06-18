<template>
  <div class="traffic-page">
    <PageHeader
      title="上网流量审计分析"
      description="审计网络流量使用情况，监控用户上网行为，分析网络活动"
    >
      <template #extra>
        <a-space>
          <a-button @click="refreshData" :loading="refreshing">
            <template #icon>
              <icon-refresh />
            </template>
            刷新状态
          </a-button>
        </a-space>
      </template>
    </PageHeader>

    <!-- 流量统计 -->
    <a-row :gutter="24" class="stats-row">
      <a-col :span="6">
        <StatCard
          :icon="IconCloudDownload"
          icon-bg-color="#1890ff"
          :value="currentTraffic"
          label="总流量(Mbps)"
          subtitle="实时流量"
        />
      </a-col>
      <a-col :span="6">
        <StatCard
          :icon="IconUser"
          icon-bg-color="#52c41a"
          :value="13"
          label="活跃设备"
          subtitle="集群+数据库节点"
        />
      </a-col>
      <a-col :span="6">
        <StatCard
          :icon="IconLink"
          icon-bg-color="#faad14"
          :value="12"
          label="服务端点"
          subtitle="API/DNS/DB同步"
        />
      </a-col>
      <a-col :span="6">
        <StatCard
          :icon="IconExclamationCircle"
          icon-bg-color="#f5222d"
          :value="0"
          label="异常告警"
          subtitle="安全事件"
        />
      </a-col>
    </a-row>

    <!-- 流量分析标签页 -->
    <a-tabs default-active-key="trend-analysis" class="analysis-tabs">
      <a-tab-pane key="trend-analysis" title="流量分析">
        <a-row :gutter="24">
          <a-col :span="16">
            <a-card title="流量趋势" :bordered="false" class="chart-card">
              <DashboardChart
                type="line"
                :data="trafficTrendData"
                height="280px"
                :smooth="true"
                :colors="['#1890ff', '#52c41a', '#faad14']"
                :showLegend="true"
              />
            </a-card>
          </a-col>
          <a-col :span="8">
            <a-card title="协议分布" :bordered="false" class="chart-card protocol-chart">
              <DashboardChart
                type="pie"
                :data="protocolData"
                height="300px"
                :showLegend="true"
                legendPosition="bottom"
                :colors="['#52c41a', '#1890ff', '#faad14', '#722ed1']"
              />
            </a-card>
          </a-col>
        </a-row>
      </a-tab-pane>

      <a-tab-pane key="behavior-analysis" title="行为分析">
        <a-card title="用户行为分析" :bordered="false">
          <div class="chart-placeholder">
            <div class="chart-content">
              <icon-bar-chart class="chart-icon" />
              <p>用户上网行为分析图表</p>
            </div>
          </div>
        </a-card>
      </a-tab-pane>

      <a-tab-pane key="abnormal-detection" title="异常检测">
        <a-card title="异常行为检测" :bordered="false">
          <div class="chart-placeholder">
            <div class="chart-content">
              <icon-thunder class="chart-icon" />
              <p>异常流量检测分析</p>
            </div>
          </div>
        </a-card>
      </a-tab-pane>

      <a-tab-pane key="statistical-reports" title="统计报表">
        <a-card title="流量统计报表" :bordered="false">
          <div class="chart-placeholder">
            <div class="chart-content">
              <icon-file-text class="chart-icon" />
              <p>详细统计报表</p>
            </div>
          </div>
        </a-card>
      </a-tab-pane>
    </a-tabs>

    <!-- 时间筛选 -->
    <a-card :bordered="false" class="filter-card">
      <a-row align="center" justify="space-between">
        <a-col>
          <a-space>
            <span>开始时间</span>
            <a-date-picker v-model:value="startTime" placeholder="开始时间" />
            <span>至</span>
            <a-date-picker v-model:value="endTime" placeholder="结束时间" />
            <span>截止5小时</span>
            <a-button type="primary" size="small" @click="queryData">查询</a-button>
          </a-space>
        </a-col>
      </a-row>
    </a-card>

    <!-- 详细流量记录表格 -->
    <a-card :bordered="false" class="table-card">
      <a-table
        :columns="trafficColumns"
        :data="trafficData"
        :pagination="{ 
          pageSize: 15, 
          showTotal: true,
          showSizeChanger: true,
          pageSizeOptions: ['15', '30', '50']
        }"
        :loading="tableLoading"
        row-key="key"
        size="small"
      >
        <template #srcIp="{ record }">
          <span class="ip-address">{{ record.srcIp }}</span>
        </template>

        <template #dstIp="{ record }">
          <span class="ip-address">{{ record.dstIp }}</span>
        </template>

        <template #url="{ record }">
          <a-tooltip :content="record.url">
            <span class="url-text">{{ record.url }}</span>
          </a-tooltip>
        </template>

        <template #protocol="{ record }">
          <a-tag :color="getProtocolColor(record.protocol)" size="small">
            {{ record.protocol }}
          </a-tag>
        </template>

        <template #status="{ record }">
          <a-tag :color="getStatusColor(record.status)" size="small">
            {{ record.status }}
          </a-tag>
        </template>
      </a-table>
    </a-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import PageHeader from '@/components/PageHeader.vue'
import StatCard from '@/components/StatCard.vue'
import DashboardChart from '@/components/DashboardChart.vue'
import {
  IconRefresh,
  IconUser,
  IconCloudDownload,
  IconLink,
  IconExclamationCircle,
  IconFile,
  IconThunderbolt
} from '@arco-design/web-vue/es/icon'

// 定义流量记录类型
interface TrafficRecord {
  key: string
  time: string
  srcIp: string
  mac: string
  dstIp: string
  url: string
  srcPort: string
  dstPort: string
  port: number
  protocol: string
  status: string
}

// 响应式数据
const refreshing = ref(false)
const tableLoading = ref(false)
const startTime = ref('')
const endTime = ref('')

// 定时器
let trafficTimer: number | null = null
let trendTimer: number | null = null

// 实时流量值
const currentTraffic = ref(245)

// 时间更新计数器
let timeUpdateCounter = 0

// 流量趋势数据
const trafficTrendData = ref<Array<{name: string, value: number}>>([])

// 生成实时时间点
const generateTimePoints = () => {
  const now = new Date()
  const points = []
  
  // 生成最近8个时间点，每15分钟一个间隔
  for (let i = 7; i >= 0; i--) {
    const time = new Date(now)
    time.setMinutes(time.getMinutes() - (i * 15))
    const timeStr = `${String(time.getHours()).padStart(2, '0')}:${String(time.getMinutes()).padStart(2, '0')}`
    points.push({
      name: timeStr,
      value: Math.floor(Math.random() * 100) + 200 // 200-300 范围
    })
  }
  
  return points
}

// 初始化时间数据
const initTimeData = () => {
  trafficTrendData.value = generateTimePoints()
}

// 协议分布数据
const protocolData = ref([
  { name: 'HTTPS', value: 45 },
  { name: 'HTTP', value: 25 },
  { name: 'TCP', value: 20 },
  { name: 'UDP', value: 10 }
])

// 流量数据
const trafficData = ref<TrafficRecord[]>([])

// 生成随机流量记录
const generateRandomTrafficRecord = (index: number) => {
  const protocols = ['HTTPS', 'HTTP', 'TCP', 'UDP']
  const srcIps = ['10.10.10.2', '10.10.10.3', '10.10.10.4', '10.10.10.5', '10.10.20.2', '10.10.20.3', '10.10.20.4']
  const dstIps = ['10.10.10.6', '10.10.10.7', '10.10.20.5', '192.168.1.100', '8.8.8.8', '114.114.114.114']
  const urls = [
    'https://api.server.com/data',
    'http://web.service.com/api',
    'tcp://database.local:3306',
    'udp://dns.server.com:53',
    'https://auth.service.com/login',
    'http://monitor.local/health',
    'tcp://cache.server.com:6379',
    'udp://ntp.server.com:123'
  ]
  
  const protocol = protocols[Math.floor(Math.random() * protocols.length)]
  const srcIp = srcIps[Math.floor(Math.random() * srcIps.length)]
  const dstIp = dstIps[Math.floor(Math.random() * dstIps.length)]
  const url = urls[Math.floor(Math.random() * urls.length)]
  
  const portMap = {
    'HTTPS': 443,
    'HTTP': 80,
    'TCP': Math.floor(Math.random() * 9000) + 1000,
    'UDP': Math.floor(Math.random() * 9000) + 1000
  }
  
  const now = new Date()
  const time = `${now.getFullYear()}-${String(now.getMonth() + 1).padStart(2, '0')}-${String(now.getDate()).padStart(2, '0')} ${String(now.getHours()).padStart(2, '0')}:${String(now.getMinutes()).padStart(2, '0')}:${String(now.getSeconds()).padStart(2, '0')}`
  
  return {
    key: String(index),
    time,
    srcIp,
    mac: `00:50:56:C0:00:${String(Math.floor(Math.random() * 256)).padStart(2, '0')}`,
    dstIp,
    url,
    srcPort: srcIp,
    dstPort: dstIp,
    port: portMap[protocol as keyof typeof portMap],
    protocol,
    status: Math.random() > 0.1 ? '允许' : '拒绝'
  }
}

// 初始化流量数据
const initTrafficData = () => {
  const data = []
  for (let i = 1; i <= 15; i++) {
    data.push(generateRandomTrafficRecord(i))
  }
  trafficData.value = data
}

// 更新流量趋势数据
const updateTrafficTrend = () => {
  const now = new Date()
  const currentData = [...trafficTrendData.value]
  
  // 每次更新都滚动时间点（每2秒），模拟实时数据流
  timeUpdateCounter++
  
  if (currentData.length > 0) {
    // 移除第一个时间点，添加新的最新时间点
    currentData.shift()
    
    // 计算新的时间点（基于当前时间和更新次数）
    const newTime = new Date(now)
    newTime.setSeconds(newTime.getSeconds() - (8 - timeUpdateCounter) * 2) // 每2秒一个点
    const latestTimeStr = `${String(newTime.getHours()).padStart(2, '0')}:${String(newTime.getMinutes()).padStart(2, '0')}`
    
    // 基于上一个时间点的值进行小幅变化
    const lastValue = currentData[currentData.length - 1]?.value || 250
    const change = (Math.random() - 0.5) * 30 // -15 到 +15
    let newValue = lastValue + change
    newValue = Math.max(200, Math.min(300, newValue))
    
    currentData.push({
      name: latestTimeStr,
      value: Math.round(newValue)
    })
    
    // 同时对其他点进行小幅数值更新
    currentData.slice(0, -1).forEach((item) => {
      const change = (Math.random() - 0.5) * 10 // 较小的变化 ±5
      let newValue = item.value + change
      newValue = Math.max(200, Math.min(300, newValue))
      item.value = Math.round(newValue)
    })
  }
  
  trafficTrendData.value = currentData
  
  // 更新当前流量统计值（取最新时间点的值）
  const latestValue = currentData[currentData.length - 1]?.value || 245
  currentTraffic.value = latestValue
}

// 更新协议分布数据
const updateProtocolData = () => {
  const newData = protocolData.value.map(item => {
    // 在当前值基础上小幅度变化 ±1-3%
    const change = (Math.random() - 0.5) * 6 // -3% 到 +3%
    let newValue = item.value + change
    // 确保值在合理范围内（5%-60%）
    newValue = Math.max(5, Math.min(60, newValue))
    return {
      ...item,
      value: Math.round(newValue)
    }
  })
  
  // 重新归一化到100%
  const total = newData.reduce((sum, item) => sum + item.value, 0)
  const normalizedData = newData.map(item => ({
    ...item,
    value: Math.round((item.value / total) * 100)
  }))
  
  protocolData.value = normalizedData
}

// 更新流量列表数据
const updateTrafficData = () => {
  // 移除最后几条记录，添加新记录到开头
  const currentData = [...trafficData.value]
  const newRecordsCount = Math.floor(Math.random() * 3) + 1 // 1-3条新记录
  
  // 生成新记录
  const newRecords = []
  for (let i = 0; i < newRecordsCount; i++) {
    const newIndex = Date.now() + i
    newRecords.push(generateRandomTrafficRecord(newIndex))
  }
  
  // 保持总记录数在15条左右
  const updatedData = [...newRecords, ...currentData.slice(0, 15 - newRecordsCount)]
  trafficData.value = updatedData
}

// 开始实时更新
const startRealTimeUpdates = () => {
  // 每2秒更新流量数据
  trafficTimer = setInterval(() => {
    updateTrafficData()
    updateProtocolData()
  }, 2000)
  
  // 每2秒更新趋势图
  trendTimer = setInterval(() => {
    updateTrafficTrend()
  }, 2000)
}

// 停止实时更新
const stopRealTimeUpdates = () => {
  if (trafficTimer) {
    clearInterval(trafficTimer)
    trafficTimer = null
  }
  if (trendTimer) {
    clearInterval(trendTimer)
    trendTimer = null
  }
}

// 表格列配置
const trafficColumns = [
  {
    title: '时间',
    dataIndex: 'time',
    width: 150
  },
  {
    title: '源IP',
    dataIndex: 'srcIp',
    slotName: 'srcIp',
    width: 120
  },
  {
    title: 'MAC',
    dataIndex: 'mac',
    width: 130
  },
  {
    title: '目标IP',
    dataIndex: 'dstIp',
    slotName: 'dstIp',
    width: 120
  },
  {
    title: 'URL',
    dataIndex: 'url',
    slotName: 'url',
    width: 250
  },
  {
    title: '源端口',
    dataIndex: 'srcPort',
    width: 120
  },
  {
    title: '目标端口',
    dataIndex: 'dstPort',
    width: 120
  },
  {
    title: '端口',
    dataIndex: 'port',
    width: 60
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
  }
]

// 获取协议颜色
const getProtocolColor = (protocol: string) => {
  const colorMap: Record<string, string> = {
    'HTTPS': 'green',
    'HTTP': 'blue',
    'TCP': 'orange',
    'UDP': 'purple'
  }
  return colorMap[protocol] || 'gray'
}

// 获取状态颜色
const getStatusColor = (status: string) => {
  return status === '允许' ? 'green' : 'red'
}

// 刷新数据
const refreshData = async () => {
  refreshing.value = true
  await new Promise(resolve => setTimeout(resolve, 1000))
  refreshing.value = false
}

// 查询数据
const queryData = () => {
  console.log('查询数据:', startTime.value, endTime.value)
}

// 生命周期
onMounted(() => {
  // 初始化数据
  initTimeData()
  initTrafficData()
  // 启动实时更新
  startRealTimeUpdates()
})

onUnmounted(() => {
  // 清理定时器
  stopRealTimeUpdates()
})
</script>

<style scoped>
.traffic-page {
  padding: 0;
}

.stats-row {
  margin-bottom: 24px;
}

.analysis-tabs {
  margin-bottom: 24px;
}

.chart-card {
  height: 100%;
}

.protocol-chart {
  height: 350px; /* 增加协议分布卡片高度，为图例留出空间 */
}

.protocol-chart :deep(.arco-card-body) {
  padding: 16px;
  height: calc(100% - 60px);
  display: flex;
  flex-direction: column;
}

.chart-container {
  height: 300px;
}

.chart-placeholder {
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f7f8fa;
  border-radius: 6px;
}

.chart-content {
  text-align: center;
  color: #86909c;
}

.chart-icon {
  font-size: 48px;
  margin-bottom: 16px;
  color: #c9cdd4;
}

.filter-card {
  margin-bottom: 16px;
}

.table-card {
  margin-bottom: 24px;
}

.ip-address {
  font-family: monospace;
  color: #1890ff;
}

.url-text {
  max-width: 200px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  display: inline-block;
  vertical-align: middle;
}

:deep(.arco-card) {
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

:deep(.arco-tabs-content) {
  padding-top: 0;
}

:deep(.arco-table) {
  font-size: 12px;
}

:deep(.arco-table-th) {
  background: #fafafa;
  font-weight: 600;
}
</style>
