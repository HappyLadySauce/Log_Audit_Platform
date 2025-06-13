<template>
  <div class="traffic-page">
    <PageHeader
      title="上网流量统计"
      description="监控和分析网络流量使用情况"
    >
      <template #extra>
        <a-space>
          <a-range-picker v-model:value="dateRange" />
          <a-button @click="refreshData" :loading="refreshing">
            <template #icon>
              <icon-refresh />
            </template>
            刷新
          </a-button>
          <a-button type="primary" @click="exportReport">
            <template #icon>
              <icon-download />
            </template>
            导出报告
          </a-button>
        </a-space>
      </template>
    </PageHeader>

    <!-- 流量统计 -->
    <a-row :gutter="[24, 24]" class="stats-row">
      <a-col :xs="24" :sm="12" :lg="6">
        <EnhancedStatCard
          :icon="IconCloudDownload"
          icon-bg-color="linear-gradient(135deg, #667eea 0%, #764ba2 100%)"
          :value="totalTraffic"
          label="总流量"
          subtitle="今日统计"
          unit="GB"
          :trend="{ type: 'increase', value: '+15.2%' }"
          :show-progress="true"
          :progress-percent="78"
          progress-color="#667eea"
          progress-text="带宽使用率 78%"
        />
      </a-col>
      <a-col :xs="24" :sm="12" :lg="6">
        <EnhancedStatCard
          :icon="IconArrowUp"
          icon-bg-color="linear-gradient(135deg, #f093fb 0%, #f5576c 100%)"
          :value="uploadTraffic"
          label="上行流量"
          subtitle="上传数据"
          unit="GB"
          :trend="{ type: 'increase', value: '+8.5%' }"
          :show-progress="true"
          :progress-percent="65"
          progress-color="#f5576c"
          progress-text="上传峰值 65%"
        />
      </a-col>
      <a-col :xs="24" :sm="12" :lg="6">
        <EnhancedStatCard
          :icon="IconArrowDown"
          icon-bg-color="linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)"
          :value="downloadTraffic"
          label="下行流量"
          subtitle="下载数据"
          unit="GB"
          :trend="{ type: 'increase', value: '+12.3%' }"
          :show-progress="true"
          :progress-percent="82"
          progress-color="#00f2fe"
          progress-text="下载峰值 82%"
        />
      </a-col>
      <a-col :xs="24" :sm="12" :lg="6">
        <EnhancedStatCard
          :icon="IconUser"
          icon-bg-color="linear-gradient(135deg, #fa709a 0%, #fee140 100%)"
          :value="activeUsers"
          label="活跃用户"
          subtitle="在线人数"
          :trend="{ type: 'stable', value: '稳定' }"
          :show-progress="true"
          :progress-percent="90"
          progress-color="#fa709a"
          progress-text="用户活跃度 90%"
        />
      </a-col>
    </a-row>

    <!-- 流量分析 -->
    <a-row :gutter="[24, 24]" class="charts-row">
      <a-col :xs="24" :lg="16">
        <a-card title="流量趋势分析" :bordered="false" class="chart-card">
          <template #extra>
            <a-radio-group v-model:value="trendPeriod" type="button" size="small">
              <a-radio-button value="24h">24小时</a-radio-button>
              <a-radio-button value="7d">7天</a-radio-button>
              <a-radio-button value="30d">30天</a-radio-button>
            </a-radio-group>
          </template>
          <DashboardChart
            type="area"
            :data="trafficTrendData"
            height="350px"
            :smooth="true"
            :colors="['#1890ff', '#52c41a', '#faad14']"
          />
        </a-card>
      </a-col>
      <a-col :xs="24" :lg="8">
        <a-card title="协议分布" :bordered="false" class="chart-card">
          <DashboardChart
            type="pie"
            :data="protocolDistributionData"
            height="350px"
            :colors="['#1890ff', '#52c41a', '#faad14', '#f5222d', '#722ed1', '#13c2c2']"
          />
        </a-card>
      </a-col>
    </a-row>

    <!-- 详细分析图表 -->
    <a-row :gutter="[24, 24]" class="charts-row">
      <a-col :xs="24" :lg="8">
        <a-card title="带宽使用率" :bordered="false" class="chart-card">
          <DashboardChart
            type="gauge"
            :data="[{ value: bandwidthUsage }]"
            height="300px"
            title="实时带宽"
          />
        </a-card>
      </a-col>
      <a-col :xs="24" :lg="8">
        <a-card title="流量类型分析" :bordered="false" class="chart-card">
          <DashboardChart
            type="bar"
            :data="trafficTypeData"
            height="300px"
            :colors="['#1890ff', '#52c41a', '#faad14', '#f5222d']"
          />
        </a-card>
      </a-col>
      <a-col :xs="24" :lg="8">
        <a-card title="网络质量监控" :bordered="false" class="chart-card">
          <DashboardChart
            type="radar"
            :data="networkQualityData"
            height="300px"
            :colors="['#1890ff', '#52c41a']"
          />
        </a-card>
      </a-col>
    </a-row>

    <!-- 用户流量排行 -->
    <a-card title="用户流量排行" :bordered="false" class="table-card">
      <template #extra>
        <a-space>
          <a-input-search
            v-model:value="searchKeyword"
            placeholder="搜索用户..."
            style="width: 200px"
            @search="handleSearch"
          />
          <a-button size="small" @click="refreshTable">
            <template #icon>
              <icon-refresh />
            </template>
          </a-button>
        </a-space>
      </template>
      <a-table
        :columns="trafficColumns"
        :data="filteredTrafficData"
        :pagination="{ pageSize: 10, showTotal: true }"
        :loading="tableLoading"
        row-key="key"
      >
        <template #userInfo="{ record }">
          <div class="user-info">
            <a-avatar 
              size="small" 
              :style="{ backgroundColor: getUserAvatarColor(record.username) }"
            >
              {{ record.username.charAt(0).toUpperCase() }}
            </a-avatar>
            <div class="user-details">
              <div class="username">{{ record.username }}</div>
              <div class="user-ip">{{ record.ip }}</div>
            </div>
          </div>
        </template>

        <template #traffic="{ record }">
          <div class="traffic-info">
            <div class="traffic-value">{{ record.totalTraffic }} GB</div>
            <a-progress
              :percent="Math.min((record.totalTraffic / 50) * 100, 100)"
              size="small"
              :show-text="false"
              :color="getProgressColor(record.totalTraffic)"
            />
          </div>
        </template>

        <template #protocol="{ record }">
          <a-space wrap>
            <a-tag 
              v-for="proto in record.protocols" 
              :key="proto" 
              size="small"
              :color="getProtocolColor(proto)"
            >
              {{ proto }}
            </a-tag>
          </a-space>
        </template>

        <template #status="{ record }">
          <a-badge 
            :status="record.isOnline ? 'processing' : 'default'" 
            :text="record.isOnline ? '在线' : '离线'"
          />
        </template>

        <template #actions="{ record }">
          <a-space>
            <a-button size="mini" type="text" @click="viewDetails(record)">
              详情
            </a-button>
            <a-button size="mini" type="text" @click="blockUser(record)">
              限制
            </a-button>
          </a-space>
        </template>
      </a-table>
    </a-card>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'
import PageHeader from '@/components/PageHeader.vue'
import EnhancedStatCard from '@/components/EnhancedStatCard.vue'
import DashboardChart from '@/components/DashboardChart.vue'
import {
  IconRefresh,
  IconDownload,
  IconUser,
  IconCloudDownload,
  IconArrowUp,
  IconArrowDown
} from '@arco-design/web-vue/es/icon'

// 响应式数据
const refreshing = ref(false)
const tableLoading = ref(false)
const dateRange = ref([])
const trendPeriod = ref('24h')
const searchKeyword = ref('')

// 统计数据
const totalTraffic = ref(1234.5)
const uploadTraffic = ref(456.8)
const downloadTraffic = ref(777.7)
const activeUsers = ref(245)
const bandwidthUsage = ref(78)

// 流量趋势数据
const trafficTrendData = ref([
  { name: '00:00', value: 120 },
  { name: '02:00', value: 80 },
  { name: '04:00', value: 60 },
  { name: '06:00', value: 150 },
  { name: '08:00', value: 300 },
  { name: '10:00', value: 450 },
  { name: '12:00', value: 600 },
  { name: '14:00', value: 550 },
  { name: '16:00', value: 480 },
  { name: '18:00', value: 520 },
  { name: '20:00', value: 380 },
  { name: '22:00', value: 280 }
])

// 协议分布数据
const protocolDistributionData = ref([
  { name: 'HTTPS', value: 45.2 },
  { name: 'HTTP', value: 28.6 },
  { name: 'TCP', value: 12.8 },
  { name: 'UDP', value: 8.4 },
  { name: 'DNS', value: 3.2 },
  { name: '其他', value: 1.8 }
])

// 流量类型数据
const trafficTypeData = ref([
  { name: '视频流媒体', value: 35.2 },
  { name: '文件下载', value: 28.6 },
  { name: '网页浏览', value: 18.4 },
  { name: '游戏娱乐', value: 12.8 },
  { name: '社交通讯', value: 5.0 }
])

// 网络质量数据
const networkQualityData = ref([
  { name: '延迟', value: 85, max: 100 },
  { name: '丢包率', value: 95, max: 100 },
  { name: '带宽利用率', value: 78, max: 100 },
  { name: '连接稳定性', value: 92, max: 100 },
  { name: '服务质量', value: 88, max: 100 }
])

// 流量数据
const trafficData = ref([
  {
    key: '1',
    username: 'zhangsan',
    ip: '192.168.1.100',
    totalTraffic: 45.2,
    uploadTraffic: 12.3,
    downloadTraffic: 32.9,
    protocols: ['HTTPS', 'HTTP', 'FTP'],
    lastActive: '2024-01-15 10:30:00',
    isOnline: true
  },
  {
    key: '2',
    username: 'lisi',
    ip: '192.168.1.101',
    totalTraffic: 38.7,
    uploadTraffic: 8.9,
    downloadTraffic: 29.8,
    protocols: ['HTTPS', 'HTTP'],
    lastActive: '2024-01-15 10:25:00',
    isOnline: true
  },
  {
    key: '3',
    username: 'wangwu',
    ip: '192.168.1.102',
    totalTraffic: 52.1,
    uploadTraffic: 15.6,
    downloadTraffic: 36.5,
    protocols: ['HTTPS', 'TCP', 'UDP'],
    lastActive: '2024-01-15 10:20:00',
    isOnline: false
  },
  {
    key: '4',
    username: 'zhaoliu',
    ip: '192.168.1.103',
    totalTraffic: 29.8,
    uploadTraffic: 7.2,
    downloadTraffic: 22.6,
    protocols: ['HTTPS', 'HTTP', 'DNS'],
    lastActive: '2024-01-15 10:15:00',
    isOnline: true
  },
  {
    key: '5',
    username: 'sunqi',
    ip: '192.168.1.104',
    totalTraffic: 41.3,
    uploadTraffic: 11.8,
    downloadTraffic: 29.5,
    protocols: ['HTTPS', 'TCP'],
    lastActive: '2024-01-15 10:10:00',
    isOnline: true
  }
])

// 过滤后的流量数据
const filteredTrafficData = computed(() => {
  if (!searchKeyword.value) {
    return trafficData.value
  }
  return trafficData.value.filter(item => 
    item.username.toLowerCase().includes(searchKeyword.value.toLowerCase()) ||
    item.ip.includes(searchKeyword.value)
  )
})

// 表格列配置
const trafficColumns = [
  {
    title: '用户信息',
    dataIndex: 'username',
    slotName: 'userInfo',
    width: 200
  },
  {
    title: '总流量',
    dataIndex: 'totalTraffic',
    slotName: 'traffic',
    width: 150,
    sortable: {
      sortDirections: ['ascend', 'descend']
    }
  },
  {
    title: '上传(GB)',
    dataIndex: 'uploadTraffic',
    width: 100,
    sortable: {
      sortDirections: ['ascend', 'descend']
    }
  },
  {
    title: '下载(GB)',
    dataIndex: 'downloadTraffic',
    width: 100,
    sortable: {
      sortDirections: ['ascend', 'descend']
    }
  },
  {
    title: '协议',
    dataIndex: 'protocols',
    slotName: 'protocol',
    width: 150
  },
  {
    title: '状态',
    dataIndex: 'isOnline',
    slotName: 'status',
    width: 80
  },
  {
    title: '最后活跃',
    dataIndex: 'lastActive',
    width: 160
  },
  {
    title: '操作',
    slotName: 'actions',
    width: 120,
    fixed: 'right'
  }
]

// 定时器
let dataUpdateTimer: NodeJS.Timeout | null = null

// 获取用户头像颜色
const getUserAvatarColor = (username: string) => {
  const colors = ['#1890ff', '#52c41a', '#faad14', '#f5222d', '#722ed1', '#13c2c2']
  const index = username.charCodeAt(0) % colors.length
  return colors[index]
}

// 获取进度条颜色
const getProgressColor = (traffic: number) => {
  if (traffic > 40) return '#f5222d'
  if (traffic > 25) return '#faad14'
  return '#52c41a'
}

// 获取协议颜色
const getProtocolColor = (protocol: string) => {
  const colorMap: Record<string, string> = {
    'HTTPS': 'green',
    'HTTP': 'blue',
    'TCP': 'orange',
    'UDP': 'purple',
    'FTP': 'red',
    'DNS': 'cyan'
  }
  return colorMap[protocol] || 'gray'
}

// 刷新数据
const refreshData = async () => {
  refreshing.value = true
  
  // 模拟API调用
  await new Promise(resolve => setTimeout(resolve, 1500))
  
  // 更新模拟数据
  totalTraffic.value = Math.round((Math.random() * 500 + 1000) * 10) / 10
  uploadTraffic.value = Math.round((Math.random() * 200 + 300) * 10) / 10
  downloadTraffic.value = Math.round((Math.random() * 300 + 500) * 10) / 10
  activeUsers.value = Math.floor(Math.random() * 100) + 200
  bandwidthUsage.value = Math.floor(Math.random() * 40) + 60
  
  refreshing.value = false
}

// 导出报告
const exportReport = () => {
  console.log('导出流量报告')
}

// 刷新表格
const refreshTable = async () => {
  tableLoading.value = true
  await new Promise(resolve => setTimeout(resolve, 1000))
  tableLoading.value = false
}

// 搜索处理
const handleSearch = (value: string) => {
  console.log('搜索:', value)
}

// 查看详情
const viewDetails = (record: any) => {
  console.log('查看详情:', record)
}

// 限制用户
const blockUser = (record: any) => {
  console.log('限制用户:', record)
}

// 实时数据更新
const startDataUpdate = () => {
  dataUpdateTimer = setInterval(() => {
    // 模拟实时数据更新
    bandwidthUsage.value = Math.floor(Math.random() * 40) + 60
    
    // 随机更新流量趋势数据
    const lastValue = trafficTrendData.value[trafficTrendData.value.length - 1].value
    const newValue = Math.max(0, lastValue + (Math.random() - 0.5) * 100)
    
    trafficTrendData.value.shift()
    trafficTrendData.value.push({
      name: new Date().toLocaleTimeString().slice(0, 5),
      value: Math.floor(newValue)
    })
  }, 5000)
}

// 生命周期
onMounted(() => {
  startDataUpdate()
})

onUnmounted(() => {
  if (dataUpdateTimer) {
    clearInterval(dataUpdateTimer)
  }
})
</script>

<style scoped>
.traffic-page {
  padding: 0;
  min-height: 100vh;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
}

.stats-row {
  margin-bottom: 24px;
}

.charts-row {
  margin-bottom: 24px;
}

.chart-card {
  height: 100%;
  transition: all 0.3s ease;
}

.chart-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.12);
}

.table-card {
  margin-bottom: 24px;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.user-details {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.username {
  font-weight: 600;
  color: #262626;
}

.user-ip {
  font-size: 12px;
  color: #8c8c8c;
}

.traffic-info {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.traffic-value {
  font-weight: 600;
  color: #262626;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .user-info {
    flex-direction: column;
    align-items: flex-start;
    gap: 8px;
  }
  
  .traffic-info {
    gap: 4px;
  }
}

:deep(.arco-card) {
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  border: 1px solid rgba(255, 255, 255, 0.8);
  backdrop-filter: blur(10px);
}

:deep(.arco-card-header) {
  border-bottom: 1px solid rgba(240, 240, 240, 0.8);
}

:deep(.arco-card-body) {
  padding: 20px;
}

:deep(.arco-table-th) {
  background: rgba(250, 250, 250, 0.8);
}

:deep(.arco-table-tr:hover) {
  background: rgba(24, 144, 255, 0.04);
}
</style>
