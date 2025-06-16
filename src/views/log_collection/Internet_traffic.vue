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
          :value="1234.5"
          label="总流量(GB)"
          subtitle="今日统计"
        />
      </a-col>
      <a-col :span="6">
        <StatCard
          :icon="IconUser"
          icon-bg-color="#52c41a"
          :value="156"
          label="活跃用户"
          subtitle="在线人数"
        />
      </a-col>
      <a-col :span="6">
        <StatCard
          :icon="IconLink"
          icon-bg-color="#faad14"
          :value="2346"
          label="访问网站"
          subtitle="网站数量"
        />
      </a-col>
      <a-col :span="6">
        <StatCard
          :icon="IconExclamationCircle"
          icon-bg-color="#f5222d"
          :value="23"
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
              <div class="chart-container">
                <div class="chart-placeholder">
                  <div class="chart-content">
                    <icon-line-chart class="chart-icon" />
                    <p>流量趋势分析图表</p>
                  </div>
                </div>
              </div>
            </a-card>
          </a-col>
          <a-col :span="8">
            <a-card title="协议分布" :bordered="false" class="chart-card">
              <div class="chart-container">
                <div class="chart-placeholder">
                  <div class="chart-content">
                    <icon-pie-chart class="chart-icon" />
                    <p>协议类型分布图</p>
                  </div>
                </div>
              </div>
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
        :pagination="{ pageSize: 10, showTotal: true }"
        :loading="tableLoading"
        row-key="key"
        size="small"
      >
        <template #user="{ record }">
          <span class="user-name">{{ record.user }}</span>
        </template>

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

        <template #browser="{ record }">
          <span class="browser-text">{{ record.browser }}</span>
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
import {
  IconRefresh,
  IconUser,
  IconCloudDownload,
  IconLink,
  IconExclamationCircle,
  IconFile,
  IconThunderbolt
} from '@arco-design/web-vue/es/icon'

// 响应式数据
const refreshing = ref(false)
const tableLoading = ref(false)
const startTime = ref('')
const endTime = ref('')

// 流量数据
const trafficData = ref([
  {
    key: '1',
    time: '2024-01-15 10:30:01',
    user: '张三',
    srcIp: '192.168.1.100',
    mac: '00:1B:44:11:3A:B7',
    dstIp: '8.8.8.8',
    url: 'https://google.com/search?q=test',
    srcPort: '192.168.1.100',
    dstPort: '8.8.8.8',
    port: 443,
    browser: 'Chrome',
    protocol: 'HTTPS',
    status: '允许'
  },
  {
    key: '2',
    time: '2024-01-15 10:30:02',
    user: '李四',
    srcIp: '192.168.1.101',
    mac: '00:1B:44:11:3A:B8',
    dstIp: '114.114.114.114',
    url: 'https://baidu.com',
    srcPort: '192.168.1.101',
    dstPort: '114.114.114.114',
    port: 443,
    browser: 'Chrome',
    protocol: 'HTTPS',
    status: '允许'
  },
  {
    key: '3',
    time: '2024-01-15 10:30:03',
    user: '王五',
    srcIp: '192.168.1.102',
    mac: '00:1B:44:11:3A:B9',
    dstIp: '123.45.67.89',
    url: 'https://suspicious-site.com',
    srcPort: '192.168.1.102',
    dstPort: '123.45.67.89',
    port: 443,
    browser: 'Chrome',
    protocol: 'HTTPS',
    status: '拒绝'
  }
])

// 表格列配置
const trafficColumns = [
  {
    title: '时间',
    dataIndex: 'time',
    width: 150
  },
  {
    title: '用户',
    dataIndex: 'user',
    slotName: 'user',
    width: 80
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
    title: '浏览器',
    dataIndex: 'browser',
    slotName: 'browser',
    width: 80
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
    'UDP': 'purple',
    'FTP': 'red',
    'DNS': 'cyan'
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
  // 初始化
})

onUnmounted(() => {
  // 清理
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

.user-name {
  font-weight: 500;
  color: #1d2129;
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

.browser-text {
  color: #52c41a;
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
