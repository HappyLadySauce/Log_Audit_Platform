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

    <!-- 系统监控状态 -->
    <div class="monitoring-section">
      <div class="section-header">
        <h3>系统监控</h3>
        <a-switch v-model="isMonitoringEnabled" size="small">
          <template #checked>监控开启</template>
          <template #unchecked>监控关闭</template>
        </a-switch>
      </div>
      
      <a-row :gutter="16" class="monitoring-grid">
        <a-col :span="6">
          <div class="monitor-item">
            <div class="monitor-icon success">
              <icon-check />
            </div>
            <div class="monitor-info">
              <div class="monitor-title">系统异常</div>
              <div class="monitor-desc">异常总数: 0 条</div>
            </div>
            <div class="monitor-action">
              <a-button size="mini" type="outline">处理</a-button>
            </div>
          </div>
        </a-col>
        
        <a-col :span="6">
          <div class="monitor-item">
            <div class="monitor-icon success">
              <icon-check />
            </div>
            <div class="monitor-info">
              <div class="monitor-title">API调用</div>
              <div class="monitor-desc">失败响应数: 0</div>
            </div>
            <div class="monitor-action">
              <a-button size="mini" type="outline">查看</a-button>
            </div>
          </div>
        </a-col>

        <a-col :span="6">
          <div class="monitor-item">
            <div class="monitor-icon success">
              <icon-check />
            </div>
            <div class="monitor-info">
              <div class="monitor-title">日志收集</div>
              <div class="monitor-desc">正常运行中</div>
            </div>
            <div class="monitor-action">
              <a-button size="mini" type="outline">详情</a-button>
            </div>
          </div>
        </a-col>

        <a-col :span="6">
          <div class="monitor-item">
            <div class="monitor-icon info">
              <icon-info />
            </div>
            <div class="monitor-info">
              <div class="monitor-title">数据分析</div>
              <div class="monitor-desc">分析任务中</div>
            </div>
            <div class="monitor-action">
              <a-button size="mini" type="outline">进入</a-button>
            </div>
          </div>
        </a-col>
      </a-row>
    </div>

    <!-- CPU和内存使用率 -->
    <div class="resource-section">
      <a-row :gutter="16">
        <a-col :span="12">
          <a-card title="CPU使用率" :bordered="false">
            <div class="resource-chart">
              <div class="chart-container">
                <DashboardChart
                  type="line"
                  :data="cpuTrendData"
                  height="180px"
                  :smooth="true"
                  :colors="['#1890ff']"
                  :show-legend="false"
                  :show-grid="true"
                />
              </div>
              <div class="resource-text">
                <span class="resource-value">{{ currentCpuUsage }}%</span>
                <span class="resource-trend" :class="cpuTrend.type">
                  <icon-arrow-up v-if="cpuTrend.type === 'up'" />
                  <icon-arrow-down v-if="cpuTrend.type === 'down'" />
                  {{ cpuTrend.value }}
                </span>
              </div>
            </div>
          </a-card>
        </a-col>
        
        <a-col :span="12">
          <a-card title="内存使用率" :bordered="false">
            <div class="resource-chart">
              <div class="chart-container">
                <DashboardChart
                  type="line"
                  :data="memoryTrendData"
                  height="180px"
                  :smooth="true"
                  :colors="['#52c41a']"
                  :show-legend="false"
                  :show-grid="true"
                />
              </div>
              <div class="resource-text">
                <span class="resource-value">{{ currentMemoryUsage }}%</span>
                <span class="resource-trend" :class="memoryTrend.type">
                  <icon-arrow-up v-if="memoryTrend.type === 'up'" />
                  <icon-arrow-down v-if="memoryTrend.type === 'down'" />
                  {{ memoryTrend.value }}
                </span>
              </div>
            </div>
          </a-card>
        </a-col>
      </a-row>
    </div>

    <!-- 核心指标统计 -->
    <div class="stats-section">
      <h3>核心指标</h3>
      <a-row :gutter="16">
        <a-col :span="6">
          <EnhancedStatCard
            :icon="IconStorage"
            icon-bg-color="#1890ff"
            :value="19"
            label="设备监控"
            subtitle="网络设备7台 · 服务器11台"
            :trend="{ type: 'stable', value: '全部在线' }"
          />
        </a-col>
        
        <a-col :span="6">
          <EnhancedStatCard
            :icon="IconFile"
            icon-bg-color="#52c41a"
            :value="todayLogs"
            label="今日日志"
            subtitle="日志采集总量"
            :trend="{ type: 'increase', value: '82%' }"
          />
        </a-col>

        <a-col :span="6">
          <EnhancedStatCard
            :icon="IconExclamation"
            icon-bg-color="#faad14"
            :value="threatAlerts"
            label="威胁告警"
            subtitle="需要处理数量"
            :trend="{ type: 'decrease', value: '13%' }"
          />
        </a-col>

        <a-col :span="6">
          <EnhancedStatCard
            :icon="IconNotification"
            icon-bg-color="#f5222d"
            :value="'2.3G'"
            label="流量审计"
            subtitle="网络流量统计"
            :trend="{ type: 'increase', value: '32%' }"
          />
        </a-col>
      </a-row>
    </div>

    <!-- AI数据趋势预测 -->
    <div class="charts-section">
      <h3>
        <icon-robot style="margin-right: 8px; color: #722ed1;" />
        AI数据趋势预测
      </h3>
      <a-row :gutter="16">
        <a-col :span="16">
          <a-card :bordered="false">
            <template #title>
              <div class="ai-card-title">
                <icon-line-chart style="margin-right: 8px; color: #1890ff;" />
                系统性能监控预测
                <a-tag color="processing" size="small" style="margin-left: 8px;">AI预测</a-tag>
              </div>
            </template>
            <template #extra>
              <div class="chart-controls">
                <a-radio-group v-model="chartTimeRange" size="small">
                  <a-radio-button value="today">今日</a-radio-button>
                  <a-radio-button value="week">本周</a-radio-button>
                  <a-radio-button value="month">本月</a-radio-button>
                </a-radio-group>
              </div>
            </template>
            <DashboardChart
              type="area"
              :data="aiTrendData"
              :height="350"
              :smooth="true"
              :colors="['#1890ff', '#52c41a', '#faad14', '#f5222d', '#722ed1']"
            />
          </a-card>
        </a-col>

        <a-col :span="8">
          <a-card :bordered="false">
            <template #title>
              <div class="ai-card-title">
                <icon-pie-chart style="margin-right: 8px; color: #52c41a;" />
                AI分析统计
                <a-tag color="success" size="small" style="margin-left: 8px;">实时</a-tag>
              </div>
            </template>
            <DashboardChart
              type="pie"
              :data="aiAnalysisData"
              :height="350"
              :show-legend="true"
              :colors="['#1890ff', '#52c41a', '#faad14', '#f5222d', '#722ed1']"
            />
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
              :colors="['#1890ff', '#52c41a']"
            />
          </a-card>
        </a-col>
        
        <a-col :span="8">
          <a-card title="网络流量趋势" :bordered="false">
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
        >
          <template #columns>
            <a-table-column title="设备名称" data-index="name">
              <template #cell="{ record }">
                <div class="device-name">
                  <a-avatar class="device-avatar" :style="{ backgroundColor: record.color }">
                    {{ record.name.charAt(0) }}
                  </a-avatar>
                  <span>{{ record.name }}</span>
                </div>
              </template>
            </a-table-column>
            
            <a-table-column title="IP地址" data-index="ip" />
            
            <a-table-column title="状态" data-index="status">
              <template #cell="{ record }">
                <a-tag :color="getStatusColor(record.status)">
                  {{ getStatusText(record.status) }}
                </a-tag>
              </template>
            </a-table-column>
            
            <a-table-column title="最后响应" data-index="lastResponse" />
            
            <a-table-column title="操作">
              <template #cell="{ record }">
                <a-space>
                  <a-button size="mini" type="text" @click="viewDevice(record)">
                    <icon-eye />
                  </a-button>
                  <a-button size="mini" type="text" @click="editDevice(record)">
                    <icon-edit />
                  </a-button>
                  <a-button size="mini" type="text" status="danger" @click="deleteDevice(record)">
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
  IconLineChart,
  IconPieChart
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

// 核心指标数据
const todayLogs = ref(14520)
const threatAlerts = ref(3)

// 图表时间范围
const chartTimeRange = ref('today')

// 定时器引用
let cpuMemoryTimer: NodeJS.Timeout
let aiTrendTimer: NodeJS.Timeout
let networkTrafficTimer: NodeJS.Timeout

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

// AI趋势预测数据 - 模拟动态数据
const aiTrendData = ref([
  {
    name: 'CPU使用率预测',
    data: Array.from({ length: 24 }, (_, i) => ({
      name: String(i).padStart(2, '0') + ':00',
      value: Math.floor(Math.random() * 20) + 30 // 30-50% 预测范围
    }))
  },
  {
    name: '内存使用率预测',
    data: Array.from({ length: 24 }, (_, i) => ({
      name: String(i).padStart(2, '0') + ':00',
      value: Math.floor(Math.random() * 25) + 35 // 35-60% 预测范围
    }))
  },
  {
    name: '磁盘I/O预测',
    data: Array.from({ length: 24 }, (_, i) => ({
      name: String(i).padStart(2, '0') + ':00',
      value: Math.floor(Math.random() * 30) + 20 // 20-50% 预测范围
    }))
  },
  {
    name: '风扇状态预测',
    data: Array.from({ length: 24 }, (_, i) => ({
      name: String(i).padStart(2, '0') + ':00',
      value: Math.floor(Math.random() * 15) + 85 // 85-100% 正常运行
    }))
  },
  {
    name: '电源状态预测',
    data: Array.from({ length: 24 }, (_, i) => ({
      name: String(i).padStart(2, '0') + ':00',
      value: Math.floor(Math.random() * 10) + 90 // 90-100% 稳定运行
    }))
  }
])

// 更新AI趋势预测数据
const updateAiTrendData = () => {
  aiTrendData.value.forEach((series, index) => {
    series.data.forEach(point => {
      let baseValue, variation
      
      switch (index) {
        case 0: // CPU
          baseValue = 35
          variation = 15
          break
        case 1: // 内存
          baseValue = 45
          variation = 20
          break
        case 2: // 磁盘I/O
          baseValue = 30
          variation = 25
          break
        case 3: // 风扇状态
          baseValue = 92
          variation = 8
          break
        case 4: // 电源状态
          baseValue = 95
          variation = 5
          break
        default:
          baseValue = 50
          variation = 20
      }
      
      // 添加平滑的随机变化
      const change = (Math.random() - 0.5) * variation * 0.3
      point.value = Math.max(
        baseValue - variation / 2,
        Math.min(baseValue + variation / 2, Math.floor(point.value + change))
      )
    })
  })
}

// AI分析统计数据
const aiAnalysisData = ref([
  { name: 'CPU性能', value: 28 },
  { name: '内存优化', value: 22 },
  { name: '磁盘I/O', value: 18 },
  { name: '风扇运行', value: 16 },
  { name: '电源稳定', value: 16 }
])

// 设备状态统计数据
const deviceStatusData = ref([
  { name: '在线', value: 18 },
  { name: '离线', value: 0 },
  { name: '告警', value: 0 }
])

// 设备类型统计数据
const deviceTypeData = ref([
  { name: '网络设备', value: 7 },
  { name: '服务器', value: 11 }
])

// 网络流量趋势数据
const networkTrafficData = ref([
  { name: '08:00', value: 1.2 },
  { name: '09:00', value: 1.8 },
  { name: '10:00', value: 2.1 },
  { name: '11:00', value: 2.3 },
  { name: '12:00', value: 1.9 },
  { name: '13:00', value: 1.5 },
  { name: '14:00', value: 2.0 },
  { name: '15:00', value: 2.4 },
  { name: '16:00', value: 2.2 },
  { name: '17:00', value: 1.8 },
  { name: '18:00', value: 1.3 },
  { name: '现在', value: 2.3 }
])

// 设备列表 - 使用真实的设备数据
const deviceList = ref([
  // 网络设备
  {
    id: 1,
    name: '总部防火墙',
    ip: '10.10.10.1',
    status: 'online',
    lastResponse: formatTime(new Date()),
    color: '#52c41a'
  },
  {
    id: 2,
    name: '分部防火墙',
    ip: '10.10.20.1',
    status: 'online',
    lastResponse: formatTime(new Date()),
    color: '#52c41a'
  },
  {
    id: 3,
    name: '分部集群接入交换机',
    ip: '10.10.10.150',
    status: 'online',
    lastResponse: formatTime(new Date()),
    color: '#52c41a'
  },
  {
    id: 4,
    name: '分部彩光交换机',
    ip: '192.168.100.1',
    status: 'online',
    lastResponse: formatTime(new Date()),
    color: '#52c41a'
  },
  {
    id: 5,
    name: '分部无线控制器',
    ip: '192.168.100.2',
    status: 'online',
    lastResponse: formatTime(new Date()),
    color: '#52c41a'
  },
  {
    id: 6,
    name: '分部用户接入交换机',
    ip: '192.168.100.3',
    status: 'online',
    lastResponse: formatTime(new Date()),
    color: '#52c41a'
  },
  {
    id: 7,
    name: '分部AP',
    ip: '192.168.30.2',
    status: 'online',
    lastResponse: formatTime(new Date()),
    color: '#52c41a'
  },
  // 服务器设备
  {
    id: 8,
    name: '总部Karmada控制服务器',
    ip: '10.10.10.6',
    status: 'online',
    lastResponse: formatTime(new Date()),
    color: '#1890ff'
  },
  {
    id: 9,
    name: '总部Karmada节点服务器',
    ip: '10.10.10.7',
    status: 'online',
    lastResponse: formatTime(new Date()),
    color: '#1890ff'
  },
  {
    id: 10,
    name: '总部K8S控制节点1',
    ip: '10.10.10.2',
    status: 'online',
    lastResponse: formatTime(new Date()),
    color: '#1890ff'
  },
  {
    id: 11,
    name: '总部K8S控制节点2',
    ip: '10.10.10.3',
    status: 'online',
    lastResponse: formatTime(new Date()),
    color: '#1890ff'
  },
  {
    id: 12,
    name: '总部K8S工作节点1',
    ip: '10.10.10.4',
    status: 'online',
    lastResponse: formatTime(new Date()),
    color: '#1890ff'
  },
  {
    id: 13,
    name: '总部K8S工作节点2',
    ip: '10.10.10.5',
    status: 'online',
    lastResponse: formatTime(new Date()),
    color: '#1890ff'
  },
  {
    id: 14,
    name: '分部K8S控制节点1',
    ip: '10.10.20.2',
    status: 'online',
    lastResponse: formatTime(new Date()),
    color: '#1890ff'
  },
  {
    id: 15,
    name: '分部K8S控制节点2',
    ip: '10.10.20.3',
    status: 'online',
    lastResponse: formatTime(new Date()),
    color: '#1890ff'
  },
  {
    id: 16,
    name: '分部K8S工作节点1',
    ip: '10.10.20.4',
    status: 'online',
    lastResponse: formatTime(new Date()),
    color: '#1890ff'
  },
  {
    id: 17,
    name: '分部K8S工作节点2',
    ip: '10.10.20.5',
    status: 'online',
    lastResponse: formatTime(new Date()),
    color: '#1890ff'
  },
  {
    id: 18,
    name: 'DNS邮件服务器',
    ip: '10.10.10.254',
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

// 更新网络流量数据
const updateNetworkTrafficData = () => {
  // 移除最旧的数据点，添加新的数据点
  networkTrafficData.value.shift()
  const newValue = Math.random() * 1.5 + 1.5 // 1.5-3.0G 范围
  const now = new Date()
  const timeStr = now.toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' })
  
  networkTrafficData.value.push({
    name: timeStr,
    value: parseFloat(newValue.toFixed(1))
  })
}

// 刷新数据
const refreshData = () => {
  Message.success('数据刷新成功')
  updateResourceData()
  updateAiTrendData()
  updateNetworkTrafficData()
  
  // 更新核心指标数据
  todayLogs.value += Math.floor(Math.random() * 100)
  threatAlerts.value = Math.floor(Math.random() * 5)
  
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

// 组件挂载时初始化数据和定时器
onMounted(() => {
  // 初始化资源数据
  initResourceData()
  
  // CPU和内存数据每3秒更新一次，增加数据流动感  
  cpuMemoryTimer = setInterval(() => {
    if (isMonitoringEnabled.value) {
      updateResourceData()
    }
  }, 3000)
  
  // AI趋势预测数据每3秒更新一次
  aiTrendTimer = setInterval(() => {
    if (isMonitoringEnabled.value) {
      updateAiTrendData()
    }
  }, 3000)
  
  // 网络流量数据每3秒更新一次
  networkTrafficTimer = setInterval(() => {
    if (isMonitoringEnabled.value) {
      updateNetworkTrafficData()
    }
  }, 3000)
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

/* 系统监控样式 */
.monitoring-section {
  margin-bottom: 24px;
}

.monitoring-grid {
  margin-top: 16px;
}

.monitor-item {
  display: flex;
  align-items: center;
  padding: 16px;
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  transition: all 0.3s;
}

.monitor-item:hover {
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.12);
  transform: translateY(-2px);
}

.monitor-icon {
  width: 40px;
  height: 40px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 12px;
  color: #fff;
  font-size: 18px;
}

.monitor-icon.error {
  background: #f5222d;
}

.monitor-icon.warning {
  background: #faad14;
}

.monitor-icon.success {
  background: #52c41a;
}

.monitor-icon.info {
  background: #1890ff;
}

.monitor-info {
  flex: 1;
}

.monitor-title {
  font-size: 14px;
  font-weight: 600;
  color: #262626;
  margin-bottom: 4px;
}

.monitor-desc {
  font-size: 12px;
  color: #8c8c8c;
}

/* 资源使用率样式 */
.resource-section {
  margin-bottom: 24px;
}

.resource-chart {
  padding: 16px 0;
}

.chart-container {
  height: 200px;
  margin-bottom: 16px;
}

.resource-progress {
  position: relative;
  margin-bottom: 16px;
}

.resource-text {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 12px;
  padding: 0 8px;
}

.resource-value {
  font-size: 24px;
  font-weight: bold;
  color: #262626;
}

.resource-trend {
  display: flex;
  align-items: center;
  font-size: 12px;
  font-weight: 600;
}

.resource-trend.up {
  color: #f5222d;
}

.resource-trend.down {
  color: #52c41a;
}

.resource-trend.stable {
  color: #1890ff;
}

/* 统计卡片样式 */
.stats-section {
  margin-bottom: 24px;
}

.stats-section h3 {
  margin-bottom: 16px;
  font-size: 18px;
  font-weight: 600;
  color: #262626;
}

/* 图表区域样式 */
.charts-section {
  margin-bottom: 24px;
}

.charts-section h3 {
  margin-bottom: 16px;
  font-size: 18px;
  font-weight: 600;
  color: #262626;
  display: flex;
  align-items: center;
}

.ai-card-title {
  display: flex;
  align-items: center;
  font-size: 16px;
  font-weight: 600;
  color: #262626;
}

.chart-controls {
  display: flex;
  align-items: center;
  gap: 8px;
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
  gap: 8px;
}

.device-avatar {
  width: 32px;
  height: 32px;
  font-size: 14px;
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
</style>
