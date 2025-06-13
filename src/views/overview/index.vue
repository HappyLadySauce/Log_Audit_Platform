<template>
  <div class="overview-container">
    <!-- 页面标题 -->
    <PageHeader 
      title="日志审计平台仪表盘" 
      description="实时监控系统运行状态，掌握各项关键指标"
    >
      <template #extra>
        <a-space>
          <a-button type="primary" @click="refreshData">
            <template #icon><icon-refresh /></template>
            刷新数据
          </a-button>
          <a-button @click="exportReport">
            <template #icon><icon-download /></template>
            导出报告
          </a-button>
        </a-space>
      </template>
    </PageHeader>

    <!-- 核心指标统计 -->
    <div class="stats-section">
      <h3>核心指标</h3>
      <a-row :gutter="16">
        <a-col :span="6">
          <EnhancedStatCard
            :icon="IconStorage"
            icon-bg-color="#1890ff"
            value="9"
            label="设备监控"
            subtitle="网络设备6台 · 服务器5台 · 在线总数9"
            :trend="{ type: 'stable', value: '全部在线' }"
          />
        </a-col>
        
        <a-col :span="6">
          <EnhancedStatCard
            :icon="IconFile"
            icon-bg-color="#52c41a"
            value="2.1K"
            label="今日日志"
            subtitle="日志采集总量"
            :trend="{ type: 'increase', value: '+12%' }"
          />
        </a-col>

        <a-col :span="6">
          <EnhancedStatCard
            :icon="IconExclamation"
            icon-bg-color="#faad14"
            value="0"
            label="威胁告警"
            subtitle="低风险预警信息"
            :trend="{ type: 'decrease', value: '-8%' }"
          />
        </a-col>

        <a-col :span="6">
          <EnhancedStatCard
            :icon="IconNotification"
            icon-bg-color="#f5222d"
            value="9.6G"
            label="流量审计"
            subtitle="总流量统计"
            :trend="{ type: 'increase', value: '+15%' }"
          />
        </a-col>
      </a-row>
    </div>

    <!-- AI数据趋势预测 -->
    <div class="charts-section">
      <h3 class="large-section-title">
        <icon-robot style="margin-right: 8px; color: #722ed1;" />
        AI数据趋势预测
      </h3>
      <a-row :gutter="16">
        <a-col :span="16">
          <a-card :bordered="false">
            <template #title>
              <div class="ai-card-title-large">
                <icon-file style="margin-right: 8px; color: #1890ff;" />
                日志采集概览
                <a-tag color="processing" size="medium" style="margin-left: 8px;">实时监控</a-tag>
              </div>
            </template>
            <template #extra>
              <div class="chart-controls">
                <a-space>
                  <a-radio-group v-model="logFilter" size="medium">
                    <a-radio-button value="all">全部</a-radio-button>
                    <a-radio-button value="info">信息</a-radio-button>
                    <a-radio-button value="warning">警告</a-radio-button>
                  </a-radio-group>
                  <a-button size="medium" @click="refreshLogs">
                    <template #icon><icon-refresh /></template>
                    刷新
                  </a-button>
                </a-space>
              </div>
            </template>
            
            <div class="log-overview-container">
              <a-table 
                :data="filteredLogData" 
                :pagination="{ pageSize: 8, simple: true }"
                :scroll="{ y: 300 }"
                row-key="id"
                size="medium"
                class="large-log-table"
              >
                <template #columns>
                  <a-table-column title="时间" data-index="timestamp" :width="100">
                    <template #cell="{ record }">
                      <span class="log-time-large">{{ record.timestamp }}</span>
                    </template>
                  </a-table-column>
                  
                  <a-table-column title="设备" data-index="device" :width="180">
                    <template #cell="{ record }">
                      <div class="device-info-large">
                        <a-avatar :size="28" :style="{ backgroundColor: record.deviceColor, fontSize: '14px' }">
                          {{ record.device.charAt(0) }}
                        </a-avatar>
                        <span class="device-name-large">{{ record.device }}</span>
                      </div>
                    </template>
                  </a-table-column>
                  
                  <a-table-column title="类型" data-index="type" :width="70">
                    <template #cell="{ record }">
                      <a-tag :color="getLogTypeColor(record.type)" size="medium">
                        {{ getLogTypeText(record.type) }}
                      </a-tag>
                    </template>
                  </a-table-column>
                  
                  <a-table-column title="日志信息" data-index="message" :width="320">
                    <template #cell="{ record }">
                      <div class="log-message-large" :class="'log-' + record.type">
                        <icon-info v-if="record.type === 'warning'" style="color: #faad14; margin-right: 4px;" />
                        <icon-check v-if="record.type === 'info'" style="color: #52c41a; margin-right: 4px;" />
                        {{ record.message }}
                      </div>
                    </template>
                  </a-table-column>
                </template>
              </a-table>
            </div>
          </a-card>
        </a-col>

        <a-col :span="8">
          <a-card :bordered="false">
            <template #title>
              <div class="ai-card-title-large">
                <icon-robot style="margin-right: 8px; color: #722ed1;" />
                AI预测分析
                <a-tag color="purple" size="medium" style="margin-left: 8px;">智能分析</a-tag>
              </div>
            </template>
            
            <div class="ai-analysis-container">
              <!-- 日志统计图表 -->
              <div class="log-stats-chart">
                <DashboardChart
                  type="pie"
                  :data="logStatsData"
                  :height="200"
                  :show-legend="true"
                  :colors="['#52c41a', '#faad14']"
                />
              </div>
              
              <!-- AI预测指标 -->
              <div class="ai-predictions">
                <h4 class="ai-prediction-title">
                  <icon-fire style="margin-right: 4px; color: #722ed1;" />
                  AI预测分析
                </h4>
                
                <div class="prediction-item-large" v-for="prediction in aiPredictions" :key="prediction.id">
                  <div class="prediction-header">
                    <span class="prediction-title-large">{{ prediction.title }}</span>
                    <a-tag :color="prediction.level === 'high' ? 'red' : prediction.level === 'medium' ? 'orange' : 'green'" size="medium">
                      {{ prediction.level === 'high' ? '高风险' : prediction.level === 'medium' ? '中风险' : '低风险' }}
                    </a-tag>
                  </div>
                  <div class="prediction-content-large">{{ prediction.content }}</div>
                  <div class="prediction-suggestion-large">建议: {{ prediction.suggestion }}</div>
                </div>
              </div>
            </div>
          </a-card>
        </a-col>
      </a-row>
    </div>

    <!-- 设备状态监控 -->
    <div class="devices-section">
      <h3>设备状态监控</h3>
      
      <!-- 设备状态概览 -->
      <a-row :gutter="16" class="device-overview">
        <a-col :span="8">
          <a-card title="设备状态分布" :bordered="false">
            <DashboardChart
              type="pie"
              :data="deviceStatusData"
              height="200px"
              :show-legend="true"
              legend-position="top-left"
              :colors="['#52c41a', '#f5222d', '#faad14']"
            />
          </a-card>
        </a-col>
        
        <a-col :span="8">
          <a-card title="设备类型分布" :bordered="false">
            <DashboardChart
              type="pie"
              :data="deviceTypeData"
              height="200px"
              :show-legend="true"
              legend-position="top-left"
              :colors="['#1890ff', '#52c41a']"
            />
          </a-card>
        </a-col>
        
        <a-col :span="8">
          <a-card title="网络流量趋势 (Mbps)" :bordered="false">
            <DashboardChart
              type="line"
              :data="networkTrafficData"
              height="200px"
              :smooth="true"
              :colors="['#722ed1']"
              :show-legend="false"
            />
          </a-card>
        </a-col>
      </a-row>
      
      <a-card :bordered="false" class="device-table-card">
        <template #extra>
          <a-space>
            <span>设备总数: {{ deviceList.length }} 台</span>
            <a-button size="small" @click="refreshDevices">刷新状态</a-button>
          </a-space>
        </template>
        
        <a-table 
          :data="deviceList" 
          :pagination="false"
          :scroll="{ y: 300 }"
          row-key="id"
          size="large"
          class="device-table"
        >
          <template #columns>
            <a-table-column title="设备名称" data-index="name">
              <template #cell="{ record }">
                <div class="device-name">
                  <a-avatar class="device-avatar" :style="{ backgroundColor: record.color }">
                    {{ record.name.charAt(0) }}
                  </a-avatar>
                  <span class="device-name-text">{{ record.name }}</span>
                </div>
              </template>
            </a-table-column>
            
            <a-table-column title="IP地址" data-index="ip">
              <template #cell="{ record }">
                <span class="device-ip">{{ record.ip }}</span>
              </template>
            </a-table-column>
            
            <a-table-column title="状态" data-index="status">
              <template #cell="{ record }">
                <a-tag :color="getStatusColor(record.status)" size="medium">
                  {{ getStatusText(record.status) }}
                </a-tag>
              </template>
            </a-table-column>
            
            <a-table-column title="最后响应" data-index="lastResponse">
              <template #cell="{ record }">
                <span class="device-response-time">{{ record.lastResponse }}</span>
              </template>
            </a-table-column>
            
            <a-table-column title="操作">
              <template #cell="{ record }">
                <a-space>
                  <a-button size="medium" type="text" @click="viewDevice(record)">
                    <icon-eye />
                  </a-button>
                  <a-button size="medium" type="text" @click="editDevice(record)">
                    <icon-edit />
                  </a-button>
                  <a-button size="medium" type="text" status="danger" @click="deleteDevice(record)">
                    <icon-delete />
                  </a-button>
                </a-space>
              </template>
            </a-table-column>
          </template>
        </a-table>
      </a-card>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, computed } from 'vue'
import { Message } from '@arco-design/web-vue'
import PageHeader from '@/components/PageHeader.vue'
import EnhancedStatCard from '@/components/EnhancedStatCard.vue'
import DashboardChart from '@/components/DashboardChart.vue'
import {
  IconRefresh,
  IconDownload,
  IconClose,
  IconExclamation,
  IconCheck,
  IconInfo,
  IconArrowUp,
  IconArrowDown,
  IconStorage,
  IconFile,
  IconNotification,
  IconEye,
  IconEdit,
  IconDelete,
  IconRobot,
  IconBarChart,
  IconFire
} from '@arco-design/web-vue/es/icon'

// 系统监控状态
const isMonitoringEnabled = ref(true)

// CPU和内存使用率数据
const cpuTrendData = ref([])
const memoryTrendData = ref([])
const currentCpuUsage = ref(35)
const currentMemoryUsage = ref(38)
const cpuTrend = ref({ type: 'stable', value: '+2%' })
const memoryTrend = ref({ type: 'stable', value: '-1%' })

// 核心指标数据 - 保持与日志数据一致
const todayLogs = ref('2.1K')
const onlineDevices = ref(9)
const threatAlerts = ref({
  error: 0,
  warning: 280,
  info: 1820,
  total: 2100
})
const totalTraffic = ref('9.6G')

// 图表时间范围  
const chartTimeRange = ref('today')

// 日志过滤器
const logFilter = ref('all')

// 定时器引用
let cpuMemoryTimer: NodeJS.Timeout
let aiTrendTimer: NodeJS.Timeout
let networkTrafficTimer: NodeJS.Timeout
let aiPredictionTimer: NodeJS.Timeout

// 初始化CPU和内存趋势数据
const initResourceData = () => {
  const now = new Date()
  const cpuData = []
  const memoryData = []
  
  for (let i = 29; i >= 0; i--) {
    const time = new Date(now.getTime() - i * 60000) // 每分钟一个数据点
    const timeStr = time.toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' })
    
    cpuData.push({
      name: timeStr,
      value: Math.floor(Math.random() * 10) + 30 // 30-40之间的随机数
    })
    
    memoryData.push({
      name: timeStr,
      value: Math.floor(Math.random() * 10) + 30 // 30-40之间的随机数
    })
  }
  
  cpuTrendData.value = cpuData
  memoryTrendData.value = memoryData
  
  // 设置当前值为最新的数据点
  currentCpuUsage.value = cpuData[cpuData.length - 1].value
  currentMemoryUsage.value = memoryData[memoryData.length - 1].value
}

// 更新CPU和内存数据
const updateResourceData = () => {
  const now = new Date()
  const timeStr = now.toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' })
  
  // 移除最旧的数据点，添加新的数据点
  cpuTrendData.value.shift()
  memoryTrendData.value.shift()
  
  const newCpuValue = Math.floor(Math.random() * 10) + 30
  const newMemoryValue = Math.floor(Math.random() * 10) + 30
  
  cpuTrendData.value.push({ name: timeStr, value: newCpuValue })
  memoryTrendData.value.push({ name: timeStr, value: newMemoryValue })
  
  currentCpuUsage.value = newCpuValue
  currentMemoryUsage.value = newMemoryValue
}

// 生成新的日志条目
const generateNewLogEntry = () => {
  const devices = [
    { name: '分部防火墙', color: '#52c41a' },
    { name: '分部K8S控制节点1', color: '#1890ff' },
    { name: '分部K8S工作节点1', color: '#1890ff' },
    { name: '分部接入交换机', color: '#52c41a' },
    { name: 'DNS邮件服务器', color: '#1890ff' },
    { name: '分部无线控制器', color: '#52c41a' }
  ]
  
  // 85%信息日志，15%警告日志，系统运行正常
  const logTypes = ['info', 'info', 'info', 'info', 'info', 'info', 'warning']
  const logMessages = {
    info: [
      '分部系统启动完成，所有服务正常运行',
      '分部CPU使用率: 32%, 内存使用率: 38%',
      '分部网络连接正常，延迟 < 5ms',
      '分部磁盘I/O操作正常，读写速度稳定',
      '分部用户登录认证成功',
      '分部定时备份任务执行完成',
      '分部防火墙规则更新成功',
      '分部K8S集群健康检查通过',
      '分部数据同步任务完成',
      '分部系统性能监控正常',
      '分部网络流量状态稳定',
      '分部服务健康检查通过'
    ],
    warning: [
      '分部CPU使用率达到60%，建议关注',
      '分部内存使用率达到70%，状态良好',
      '分部网络延迟略微增加至12ms',
      '分部磁盘使用率达到75%，建议定期清理',
      '分部检测到轻微的负载波动',
      '分部备份任务耗时较长，建议优化',
      '分部发现少量异常访问尝试，已拦截',
      '分部系统负载略有上升，继续监控'
    ]
  }
  
  const device = devices[Math.floor(Math.random() * devices.length)]
  const type = logTypes[Math.floor(Math.random() * logTypes.length)]
  const messages = logMessages[type]
  const message = messages[Math.floor(Math.random() * messages.length)]
  
  const now = new Date()
  
  return {
    id: Date.now() + Math.random(),
    timestamp: now.toLocaleTimeString('zh-CN', { 
      hour: '2-digit', 
      minute: '2-digit',
      second: '2-digit'
    }),
    device: device.name,
    deviceColor: device.color,
    type,
    message,
    rawTimestamp: now
  }
}

// 日志数据
const logData = ref([])

// 日志统计数据 - 与实际日志类型分布保持一致
const logStatsData = ref([
  { name: '正常', value: 85 },
  { name: '警告', value: 15 },
  { name: '错误', value: 0 }
])

// AI预测分析数据 - 基于系统运行正常的前提
const aiPredictions = ref([
  {
    id: 1,
    title: '系统运行状态',
    level: 'low',
    content: '系统运行稳定，CPU和内存使用率均在正常范围内，各项服务运行良好',
    suggestion: '继续保持当前监控策略，定期检查系统性能'
  },
  {
    id: 2,
    title: '网络状态评估',
    level: 'low',
    content: '网络设备运行正常，流量稳定，延迟保持在低水平',
    suggestion: '保持当前网络配置，继续监控流量变化'
  },
  {
    id: 3,
    title: '资源使用趋势',
    level: 'medium',
    content: '磁盘使用率逐步增长，建议关注存储空间变化趋势',
    suggestion: '定期清理临时文件，制定存储管理策略'
  }
])

// 初始化日志数据
const initLogData = () => {
  const devices = [
    { name: '分部防火墙', color: '#52c41a' },
    { name: '分部K8S控制节点1', color: '#1890ff' },
    { name: '分部K8S工作节点1', color: '#1890ff' },
    { name: '分部接入交换机', color: '#52c41a' },
    { name: 'DNS邮件服务器', color: '#1890ff' },
    { name: '分部无线控制器', color: '#52c41a' }
  ]
  
  // 80%信息日志，20%警告日志，系统运行正常
  const logTypes = ['info', 'info', 'info', 'info', 'warning']
  const logMessages = {
    info: [
      '分部系统启动完成，所有服务正常运行',
      '分部CPU使用率: 32%, 内存使用率: 38%',
      '分部网络连接正常，延迟 < 5ms',
      '分部磁盘I/O操作正常，读写速度稳定',
      '分部用户登录认证成功',
      '分部定时备份任务执行完成',
      '分部防火墙规则更新成功',
      '分部K8S集群健康检查通过',
      '分部数据同步任务完成',
      '分部系统性能监控正常',
      '分部网络流量状态稳定',
      '分部服务健康检查通过'
    ],
    warning: [
      '分部CPU使用率达到60%，建议关注',
      '分部内存使用率达到70%，状态良好',
      '分部网络延迟略微增加至12ms',
      '分部磁盘使用率达到75%，建议定期清理',
      '分部检测到轻微的负载波动',
      '分部备份任务耗时较长，建议优化',
      '分部发现少量异常访问尝试，已拦截',
      '分部系统负载略有上升，继续监控'
    ]
  }
  
  const logs = []
  let id = 1
  
  // 生成最近50条日志
  for (let i = 0; i < 50; i++) {
    const device = devices[Math.floor(Math.random() * devices.length)]
    const type = logTypes[Math.floor(Math.random() * logTypes.length)]
    const messages = logMessages[type]
    const message = messages[Math.floor(Math.random() * messages.length)]
    
    const now = new Date()
    const timestamp = new Date(now.getTime() - Math.random() * 3600000) // 最近1小时内
    
    logs.push({
      id: id++,
      timestamp: timestamp.toLocaleTimeString('zh-CN', { 
        hour: '2-digit', 
        minute: '2-digit',
        second: '2-digit'
      }),
      device: device.name,
      deviceColor: device.color,
      type,
      message,
      rawTimestamp: timestamp
    })
  }
  
  // 按时间倒序排列
  logData.value = logs.sort((a, b) => b.rawTimestamp - a.rawTimestamp)
}

// 设备状态统计数据
const deviceStatusData = ref([
  { name: '在线', value: 9 },
  { name: '离线', value: 0 },
  { name: '告警', value: 0 }
])

// 设备类型统计数据
const deviceTypeData = ref([
  { name: '网络设备', value: 6 },
  { name: '服务器', value: 5 }
])

// 网络流量趋势数据 (Mbps) - 初始化30个数据点，保留历史数据
const networkTrafficData = ref([])

// 初始化网络流量数据
const initNetworkTrafficData = () => {
  const now = new Date()
  const data = []
  
  for (let i = 29; i >= 0; i--) {
    const time = new Date(now.getTime() - i * 5000) // 每5秒一个数据点
    const timeStr = time.toLocaleTimeString('zh-CN', { 
      hour: '2-digit', 
      minute: '2-digit',
      second: '2-digit'
    })
    
    data.push({
      name: timeStr,
      value: Math.floor(Math.random() * 100) + 200 // 200-300 Mbps 范围
    })
  }
  
  networkTrafficData.value = data
}

// 设备列表 - 使用分部设备数据
const deviceList = ref([
  // 网络设备
  {
    id: 1,
    name: '分部防火墙',
    ip: '10.10.20.1',
    status: 'online',
    lastResponse: formatTime(new Date()),
    color: '#52c41a'
  },
  {
    id: 2,
    name: '分部集群接入交换机',
    ip: '10.10.10.150',
    status: 'online',
    lastResponse: formatTime(new Date()),
    color: '#52c41a'
  },
  {
    id: 3,
    name: '分部彩光交换机',
    ip: '192.168.100.1',
    status: 'online',
    lastResponse: formatTime(new Date()),
    color: '#52c41a'
  },
  {
    id: 4,
    name: '分部无线控制器',
    ip: '192.168.100.2',
    status: 'online',
    lastResponse: formatTime(new Date()),
    color: '#52c41a'
  },
  {
    id: 5,
    name: '分部用户接入交换机',
    ip: '192.168.100.3',
    status: 'online',
    lastResponse: formatTime(new Date()),
    color: '#52c41a'
  },
  {
    id: 6,
    name: '分部AP',
    ip: '192.168.30.2',
    status: 'online',
    lastResponse: formatTime(new Date()),
    color: '#52c41a'
  },
  // 服务器设备
  {
    id: 7,
    name: '分部K8S控制节点1',
    ip: '10.10.20.2',
    status: 'online',
    lastResponse: formatTime(new Date()),
    color: '#1890ff'
  },
  {
    id: 8,
    name: '分部K8S控制节点2',
    ip: '10.10.20.3',
    status: 'online',
    lastResponse: formatTime(new Date()),
    color: '#1890ff'
  },
  {
    id: 9,
    name: '分部K8S工作节点1',
    ip: '10.10.20.4',
    status: 'online',
    lastResponse: formatTime(new Date()),
    color: '#1890ff'
  },
  {
    id: 10,
    name: '分部K8S工作节点2',
    ip: '10.10.20.5',
    status: 'online',
    lastResponse: formatTime(new Date()),
    color: '#1890ff'
  },
  {
    id: 11,
    name: 'DNS邮件服务器',
    ip: '10.10.20.254',
    status: 'online',
    lastResponse: formatTime(new Date()),
    color: '#1890ff'
  }
])

// 格式化时间
function formatTime(date: Date): string {
  return date.toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit'
  })
}

// 获取状态颜色
const getStatusColor = (status: string) => {
  switch (status) {
    case 'online': return 'green'
    case 'offline': return 'red'  
    case 'warning': return 'orange'
    default: return 'gray'
  }
}

// 获取状态文本
const getStatusText = (status: string) => {
  switch (status) {
    case 'online': return '在线'
    case 'offline': return '离线'
    case 'warning': return '告警'
    default: return '未知'
  }
}

// 更新网络流量数据 (Mbps) - 保留历史数据，添加新数据点
const updateNetworkTrafficData = () => {
  // 移除最旧的数据点
  networkTrafficData.value.shift()
  
  // 生成新数据点，基于上一个数据点进行小幅波动，保持连续性
  const lastValue = networkTrafficData.value[networkTrafficData.value.length - 1]?.value || 250
  const change = (Math.random() - 0.5) * 20 // -10 到 +10 的变化
  let newValue = lastValue + change
  
  // 确保数值在200-300范围内
  newValue = Math.max(200, Math.min(300, newValue))
  
  const now = new Date()
  const timeStr = now.toLocaleTimeString('zh-CN', { 
    hour: '2-digit', 
    minute: '2-digit',
    second: '2-digit'
  })
  
  networkTrafficData.value.push({
    name: timeStr,
    value: Math.round(newValue)
  })
}

// 过滤后的日志数据
const filteredLogData = computed(() => {
  if (logFilter.value === 'all') {
    return logData.value
  }
  return logData.value.filter(log => log.type === logFilter.value)
})

// 获取日志类型颜色 - 系统运行正常，只有警告和信息
const getLogTypeColor = (type: string) => {
  switch (type) {
    case 'warning': return 'orange'
    case 'info': return 'green'
    default: return 'green'
  }
}

// 获取日志类型文本 - 系统运行正常，只有警告和信息
const getLogTypeText = (type: string) => {
  switch (type) {
    case 'warning': return '警告'
    case 'info': return '信息'
    default: return '信息'
  }
}

// 刷新日志
const refreshLogs = () => {
  Message.success('日志数据已刷新')
  initLogData()
  updateAiPredictions()
}

// 更新AI预测分析 - 保持系统正常运行状态
const updateAiPredictions = () => {
  const total = logData.value.length
  const infoCount = logData.value.filter(log => log.type === 'info').length
  const warningCount = logData.value.filter(log => log.type === 'warning').length
  const errorCount = 0 // 系统运行正常，无错误日志
  
  // 根据日志情况动态更新预测 - 保持正面评估
  if (warningCount > total * 0.25) {
    aiPredictions.value[0].level = 'medium'
    aiPredictions.value[0].content = `检测到${warningCount}个警告信息，系统整体运行良好，建议持续关注`
    aiPredictions.value[0].suggestion = '继续监控系统状态，适时进行性能优化'
  } else {
    aiPredictions.value[0].level = 'low'
    aiPredictions.value[0].content = '系统运行稳定，各项指标正常，服务响应良好'
    aiPredictions.value[0].suggestion = '保持当前配置，继续常规监控'
  }
  
  // 更新网络状态评估
  aiPredictions.value[1].content = '网络设备运行正常，流量稳定，平均延迟保持在5ms以下'
  
  // 更新资源使用趋势
  const cpuUsage = currentCpuUsage.value
  const memoryUsage = currentMemoryUsage.value
  
  if (cpuUsage > 50 || memoryUsage > 60) {
    aiPredictions.value[2].level = 'medium'
    aiPredictions.value[2].content = `CPU使用率${cpuUsage}%，内存使用率${memoryUsage}%，资源使用较为活跃`
  } else {
    aiPredictions.value[2].level = 'low'
    aiPredictions.value[2].content = `CPU使用率${cpuUsage}%，内存使用率${memoryUsage}%，资源使用正常`
  }
  
  // 更新统计数据 - 保持85%正常，15%警告，0%错误
  logStatsData.value = [
    { name: '正常', value: total > 0 ? Math.round((infoCount / total) * 100) : 85 },
    { name: '警告', value: total > 0 ? Math.round((warningCount / total) * 100) : 15 },
    { name: '错误', value: 0 }
  ]
}

// 添加新日志条目到列表顶部
const addNewLogEntry = () => {
  const newLog = generateNewLogEntry()
  logData.value.unshift(newLog)
  
  // 保持最多100条日志
  if (logData.value.length > 100) {
    logData.value = logData.value.slice(0, 100)
  }
  
  updateAiPredictions()
}

// 刷新数据
const refreshData = () => {
  Message.success('数据刷新成功')
  updateResourceData()
  updateNetworkTrafficData()
  updateCoreMetrics()
  refreshLogs()
  
  // 更新设备最后响应时间
  deviceList.value.forEach(device => {
    device.lastResponse = formatTime(new Date())
  })
}

// 导出报告
const exportReport = () => {
  Message.info('正在生成报告...')
}

// 刷新设备状态
const refreshDevices = () => {
  Message.success('设备状态已刷新')
  deviceList.value.forEach(device => {
    device.lastResponse = formatTime(new Date())
  })
}

// 查看设备
const viewDevice = (device: any) => {
  Message.info(`查看设备: ${device.name}`)
}

// 编辑设备
const editDevice = (device: any) => {
  Message.info(`编辑设备: ${device.name}`)
}

// 删除设备
const deleteDevice = (device: any) => {
  Message.warning(`删除设备: ${device.name}`)
}

// 更新核心指标数据
const updateCoreMetrics = () => {
  // 今日日志数量实时增长
  const currentLogs = parseFloat(todayLogs.value.replace('K', '')) * 1000
  const newLogs = currentLogs + Math.floor(Math.random() * 30) + 5
  todayLogs.value = (newLogs / 1000).toFixed(1) + 'K'
  
  // 威胁告警数据轻微波动 - 分部规模较小
  if (Math.random() > 0.8) {
    threatAlerts.value.warning += Math.floor(Math.random() * 2) - 1
    threatAlerts.value.info += Math.floor(Math.random() * 8) + 3
    threatAlerts.value.total = threatAlerts.value.error + threatAlerts.value.warning + threatAlerts.value.info
  }
  
  // 流量审计数据增长
  const currentTraffic = parseFloat(totalTraffic.value.replace('G', ''))
  const newTraffic = currentTraffic + (Math.random() * 0.08)
  totalTraffic.value = newTraffic.toFixed(1) + 'G'
  
  // 设备在线数量保持稳定
  onlineDevices.value = 9
}

// 组件挂载时初始化数据和定时器
onMounted(() => {
  // 初始化资源数据
  initResourceData()
  // 初始化网络流量数据
  initNetworkTrafficData()
  // 初始化日志数据
  initLogData()
  updateAiPredictions()
  
  // CPU和内存数据每3秒更新一次，增加数据流动感  
  cpuMemoryTimer = setInterval(() => {
    if (isMonitoringEnabled.value) {
      updateResourceData()
    }
  }, 3000)
  
  // 日志数据每3秒更新一次
  aiTrendTimer = setInterval(() => {
    if (isMonitoringEnabled.value) {
      // 30%概率生成新日志条目
      if (Math.random() > 0.7) {
        addNewLogEntry()
      }
      // 更新核心指标
      updateCoreMetrics()
    }
  }, 3000)
  
  // 网络流量数据每5秒更新一次，保持连续性
  networkTrafficTimer = setInterval(() => {
    if (isMonitoringEnabled.value) {
      updateNetworkTrafficData()
    }
  }, 5000)
  
  // AI预测分析每1小时更新一次
  aiPredictionTimer = setInterval(() => {
    if (isMonitoringEnabled.value) {
      updateAiPredictions()
    }
  }, 3600000) // 1小时 = 3600000毫秒
})

// 组件卸载时清理定时器
onUnmounted(() => {
  if (cpuMemoryTimer) {
    clearInterval(cpuMemoryTimer)
  }
  if (aiTrendTimer) {
    clearInterval(aiTrendTimer)
  }
  if (networkTrafficTimer) {
    clearInterval(networkTrafficTimer)
  }
  if (aiPredictionTimer) {
    clearInterval(aiPredictionTimer)
  }
})
</script>

<style scoped>
.overview-container {
  padding: 0;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.section-header h3 {
  margin: 0;
  font-size: 18px;
  font-weight: 600;
  color: #262626;
}

/* 统计卡片样式 */
.stats-section {
  margin-bottom: 24px;
}

.stats-section h3 {
  margin-bottom: 20px;
  font-size: 24px;
  font-weight: 600;
  color: #262626;
}

/* 图表区域样式 */
.charts-section {
  margin-bottom: 24px;
}

.charts-section h3 {
  margin-bottom: 20px;
  font-size: 24px;
  font-weight: 600;
  color: #262626;
  display: flex;
  align-items: center;
}

.large-section-title {
  font-size: 26px !important;
  font-weight: 700 !important;
  margin-bottom: 24px !important;
}

.ai-card-title {
  display: flex;
  align-items: center;
  font-size: 16px;
  font-weight: 600;
  color: #262626;
}

.ai-card-title-large {
  display: flex;
  align-items: center;
  font-size: 20px;
  font-weight: 600;
  color: #262626;
}

.chart-controls {
  display: flex;
  align-items: center;
  gap: 8px;
}

/* 大字体日志表格样式 */
.large-log-table {
  font-size: 16px;
}

.large-log-table .arco-table-th {
  font-size: 16px;
  font-weight: 600;
  padding: 14px 16px;
}

.large-log-table .arco-table-td {
  padding: 14px 16px;
}

.log-time-large {
  font-family: 'Courier New', monospace;
  font-size: 14px;
  color: #8c8c8c;
  font-weight: 500;
}

.device-info-large {
  display: flex;
  align-items: center;
  gap: 10px;
}

.device-name-large {
  font-size: 14px;
  color: #262626;
  font-weight: 500;
}

.log-message-large {
  display: flex;
  align-items: center;
  font-size: 14px;
  line-height: 1.5;
  font-weight: 400;
}

/* AI预测分析大字体样式 */
.ai-prediction-title {
  margin: 20px 0 16px 0;
  color: #262626;
  font-size: 18px;
  font-weight: 600;
  display: flex;
  align-items: center;
}

.prediction-item-large {
  margin-bottom: 16px;
  padding: 12px 16px;
  background: #f8f9fa;
  border-radius: 8px;
  border-left: 4px solid #722ed1;
}

.prediction-title-large {
  font-weight: 600;
  font-size: 16px;
  color: #262626;
}

.prediction-content-large {
  font-size: 14px;
  color: #595959;
  margin: 8px 0;
  line-height: 1.5;
}

.prediction-suggestion-large {
  font-size: 13px;
  color: #8c8c8c;
  font-style: italic;
  line-height: 1.4;
}

/* 设备监控样式 */
.devices-section {
  margin-bottom: 24px;
}

.devices-section h3 {
  margin-bottom: 16px;
  font-size: 18px;
  font-weight: 600;
  color: #262626;
}

.device-overview {
  margin-bottom: 24px;
}

.device-table-card {
  margin-top: 16px;
}

.device-name {
  display: flex;
  align-items: center;
  gap: 12px;
}

.device-avatar {
  width: 32px;
  height: 32px;
  font-size: 14px;
  font-weight: 500;
}

/* 日志概览样式 */
.log-overview-container {
  margin-top: 8px;
}

.log-time {
  font-family: 'Courier New', monospace;
  font-size: 12px;
  color: #8c8c8c;
}

.device-info {
  display: flex;
  align-items: center;
  gap: 8px;
}

.device-info .device-name {
  font-size: 12px;
  color: #262626;
}

.log-message {
  display: flex;
  align-items: center;
  font-size: 12px;
  line-height: 1.4;
}

.log-message.log-error {
  color: #f5222d;
}

.log-message.log-warning {
  color: #faad14;
}

.log-message.log-info {
  color: #52c41a;
}

/* AI分析容器样式 */
.ai-analysis-container {
  display: flex;
  flex-direction: column;
  height: 350px;
}

.log-stats-chart {
  flex-shrink: 0;
}

.ai-predictions {
  flex: 1;
  overflow-y: auto;
  padding: 0 8px;
}

.prediction-item {
  margin-bottom: 12px;
  padding: 8px 12px;
  background: #f8f9fa;
  border-radius: 6px;
  border-left: 3px solid #722ed1;
}

.prediction-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 4px;
}

.prediction-title {
  font-weight: 600;
  font-size: 13px;
  color: #262626;
}

.prediction-content {
  font-size: 12px;
  color: #595959;
  margin-bottom: 4px;
  line-height: 1.4;
}

.prediction-suggestion {
  font-size: 11px;
  color: #8c8c8c;
  font-style: italic;
}

/* 响应式设计 */
@media (max-width: 1200px) {
  .overview-container {
    padding: 0 12px;
  }
}

@media (max-width: 768px) {
  .monitoring-grid .arco-col {
    margin-bottom: 16px;
  }
  
  .resource-value {
    font-size: 20px;
  }
  
  .chart-controls {
    position: static;
    margin-bottom: 16px;
  }
}

/* 设备表格样式 */
.device-table {
  font-size: 14px;
}

.device-table .arco-table-td {
  padding: 12px 16px;
}

.device-name {
  display: flex;
  align-items: center;
  gap: 12px;
}

.device-name-text {
  font-size: 14px;
  font-weight: 500;
  color: #262626;
}

.device-avatar {
  width: 32px;
  height: 32px;
  font-size: 14px;
  font-weight: 500;
}

.device-ip {
  font-size: 14px;
  color: #595959;
  font-weight: 500;
}

.device-response-time {
  font-size: 13px;
  color: #8c8c8c;
}

.device-table .arco-btn {
  padding: 8px;
  font-size: 16px;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.device-table .arco-btn .arco-icon {
  font-size: 18px;
}
</style>
