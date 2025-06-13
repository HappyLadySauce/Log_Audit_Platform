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
            <div class="monitor-icon error">
              <icon-close />
            </div>
            <div class="monitor-info">
              <div class="monitor-title">系统异常</div>
              <div class="monitor-desc">异常总数: 17 条</div>
            </div>
            <div class="monitor-action">
              <a-button size="mini" type="outline">处理</a-button>
            </div>
          </div>
        </a-col>
        
        <a-col :span="6">
          <div class="monitor-item">
            <div class="monitor-icon warning">
              <icon-exclamation />
            </div>
            <div class="monitor-info">
              <div class="monitor-title">API调用</div>
              <div class="monitor-desc">失败响应数</div>
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
              <div class="resource-progress">
                <a-progress 
                  :percent="cpuUsage" 
                  :color="getProgressColor(cpuUsage)"
                  :show-text="false"
                  size="large"
                />
                <div class="resource-text">
                  <span class="resource-value">{{ cpuUsage }}%</span>
                  <span class="resource-trend" :class="cpuTrend.type">
                    <icon-arrow-up v-if="cpuTrend.type === 'up'" />
                    <icon-arrow-down v-if="cpuTrend.type === 'down'" />
                    {{ cpuTrend.value }}
                  </span>
                </div>
              </div>
            </div>
          </a-card>
        </a-col>
        
        <a-col :span="12">
          <a-card title="内存使用率" :bordered="false">
            <div class="resource-chart">
              <div class="resource-progress">
                <a-progress 
                  :percent="memoryUsage" 
                  :color="getProgressColor(memoryUsage)"
                  :show-text="false"
                  size="large"
                />
                <div class="resource-text">
                  <span class="resource-value">{{ memoryUsage }}%</span>
                  <span class="resource-trend" :class="memoryTrend.type">
                    <icon-arrow-up v-if="memoryTrend.type === 'up'" />
                    <icon-arrow-down v-if="memoryTrend.type === 'down'" />
                    {{ memoryTrend.value }}
                  </span>
                </div>
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
             :value="18"
             label="网络设备"
             subtitle="在线监控数量"
             :trend="{ type: 'stable', value: '12%' }"
           />
         </a-col>
        
        <a-col :span="6">
          <EnhancedStatCard
            :icon="IconFile"
            icon-bg-color="#52c41a"
            :value="4500"
            label="今日日志"
            subtitle="日志采集总量"
            :trend="{ type: 'increase', value: '82%' }"
          />
        </a-col>

                 <a-col :span="6">
           <EnhancedStatCard
             :icon="IconExclamation"
             icon-bg-color="#faad14"
             :value="10"
             label="威胁告警"
             subtitle="需要处理数量"
             :trend="{ type: 'decrease', value: '13%' }"
           />
         </a-col>

         <a-col :span="6">
           <EnhancedStatCard
             :icon="IconNotification"
             icon-bg-color="#f5222d"
             :value="933"
             label="今日请求"
             subtitle="API调用统计"
             :trend="{ type: 'increase', value: '32%' }"
           />
         </a-col>
      </a-row>
    </div>

    <!-- 数据趋势和分布 -->
    <div class="charts-section">
      <h3>数据趋势</h3>
      <a-row :gutter="16">
        <a-col :span="16">
          <a-card title="日志分类分析" :bordered="false">
            <div class="chart-controls">
              <a-radio-group v-model="chartTimeRange" size="small">
                <a-radio-button value="day">天</a-radio-button>
                <a-radio-button value="week">周</a-radio-button>
                <a-radio-button value="month">月</a-radio-button>
              </a-radio-group>
            </div>
            <DashboardChart
              type="area"
              :data="logTrendData"
              :height="350"
              :smooth="true"
              :colors="['#1890ff', '#52c41a', '#faad14', '#f5222d']"
            />
          </a-card>
        </a-col>

        <a-col :span="8">
          <a-card title="分析统计" :bordered="false">
            <DashboardChart
              type="pie"
              :data="logDistributionData"
              :height="350"
              :show-legend="false"
            />
          </a-card>
        </a-col>
      </a-row>
    </div>

    <!-- 设备状态监控 -->
    <div class="devices-section">
      <h3>设备状态监控</h3>
      <a-card :bordered="false">
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
import { ref, onMounted, computed } from 'vue'
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
  IconDelete
} from '@arco-design/web-vue/es/icon'

// 系统监控状态
const isMonitoringEnabled = ref(true)

// 资源使用率
const cpuUsage = ref(54)
const memoryUsage = ref(82)
const cpuTrend = ref({ type: 'up', value: '+10%' })
const memoryTrend = ref({ type: 'down', value: '-3%' })

// 图表时间范围
const chartTimeRange = ref('day')

// 日志趋势数据
const logTrendData = ref([
  { name: '00:00', value: 820 },
  { name: '02:00', value: 932 },
  { name: '04:00', value: 901 },
  { name: '06:00', value: 934 },
  { name: '08:00', value: 1290 },
  { name: '10:00', value: 1330 },
  { name: '12:00', value: 1320 },
  { name: '14:00', value: 1200 },
  { name: '16:00', value: 1100 },
  { name: '18:00', value: 1400 },
  { name: '20:00', value: 1300 },
  { name: '22:00', value: 1000 }
])

// 日志分布数据
const logDistributionData = ref([
  { name: '网络设备', value: 35 },
  { name: '应用日志', value: 25 },
  { name: '系统日志', value: 20 },
  { name: 'SNMP日志', value: 20 }
])

// 设备列表
const deviceList = ref([
  {
    id: 1,
    name: '交换机1',
    ip: '192.168.1.10',
    status: 'online',
    lastResponse: '2024-01-15 22:40:37',
    color: '#52c41a'
  },
  {
    id: 2,
    name: '交换机2',
    ip: '192.168.1.11',
    status: 'online',
    lastResponse: '2024-01-15 23:47:32',
    color: '#52c41a'
  },
  {
    id: 3,
    name: '交换机3',
    ip: '192.168.1.12',
    status: 'offline',
    lastResponse: '2024-01-15 22:07:46',
    color: '#f5222d'
  }
])

// 获取进度条颜色
const getProgressColor = (value: number) => {
  if (value < 50) return '#52c41a'
  if (value < 80) return '#faad14'  
  return '#f5222d'
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

// 刷新数据
const refreshData = () => {
  Message.success('数据刷新成功')
  // 模拟数据更新
  cpuUsage.value = Math.floor(Math.random() * 100)
  memoryUsage.value = Math.floor(Math.random() * 100)
}

// 导出报告
const exportReport = () => {
  Message.info('正在生成报告...')
}

// 刷新设备状态
const refreshDevices = () => {
  Message.success('设备状态已刷新')
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

// 模拟数据定时更新
onMounted(() => {
  setInterval(() => {
    if (isMonitoringEnabled.value) {
      cpuUsage.value = Math.floor(Math.random() * 100)
      memoryUsage.value = Math.floor(Math.random() * 100)
    }
  }, 30000) // 30秒更新一次
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
  padding: 20px 0;
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
}

.chart-controls {
  position: absolute;
  top: 16px;
  right: 16px;
  z-index: 10;
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
