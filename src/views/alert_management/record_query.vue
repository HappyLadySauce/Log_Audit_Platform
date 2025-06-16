<template>
  <div class="alert-record-page">
    <PageHeader
      title="告警记录查询"
      description="查看和分析分部IT基础设施告警记录"
    >
      <template #extra>
        <a-space>
          <a-button @click="refreshData" :loading="refreshing">
            <template #icon>
              <icon-refresh />
            </template>
            刷新
          </a-button>
          <a-button @click="exportData">
            <template #icon>
              <icon-download />
            </template>
            导出
          </a-button>
        </a-space>
      </template>
    </PageHeader>

    <!-- 告警统计 -->
    <a-row :gutter="24" class="stats-row">
      <a-col :span="6">
        <StatCard
          :icon="IconExclamationCircle"
          icon-bg-color="#f5222d"
          :value="alertStats.error"
          label="错误告警"
          subtitle="需要立即处理"
        />
      </a-col>
      <a-col :span="6">
        <StatCard
          :icon="IconExclamation"
          icon-bg-color="#faad14"
          :value="alertStats.warning"
          label="警告告警"
          subtitle="需要关注"
        />
      </a-col>
      <a-col :span="6">
        <StatCard
          :icon="IconCheck"
          icon-bg-color="#52c41a"
          :value="alertStats.processed"
          label="已处理"
          subtitle="处理完成"
        />
      </a-col>
      <a-col :span="6">
        <StatCard
          :icon="IconSettings"
          icon-bg-color="#1890ff"
          :value="alertStats.rules"
          label="告警规则"
          subtitle="配置规则数"
        />
      </a-col>
    </a-row>



    <!-- 搜索和筛选 -->
    <a-card :bordered="false" class="search-card">
      <a-row :gutter="16">
        <a-col :span="6">
          <a-input
            v-model:value="searchKeyword"
            placeholder="搜索告警内容..."
            allow-clear
            @change="handleSearch"
          >
            <template #prefix>
              <icon-search />
            </template>
          </a-input>
        </a-col>
        <a-col :span="4">
          <a-select v-model:value="selectedLevel" placeholder="告警级别" allow-clear @change="handleSearch">
            <a-option value="error">错误</a-option>
            <a-option value="warning">警告</a-option>
            <a-option value="info">信息</a-option>
          </a-select>
        </a-col>
        <a-col :span="4">
          <a-select v-model:value="selectedStatus" placeholder="处理状态" allow-clear @change="handleSearch">
            <a-option value="pending">待处理</a-option>
            <a-option value="processing">处理中</a-option>
            <a-option value="resolved">已解决</a-option>
            <a-option value="ignored">已忽略</a-option>
          </a-select>
        </a-col>
        <a-col :span="4">
          <a-select v-model:value="selectedSource" placeholder="告警来源" allow-clear @change="handleSearch">
            <a-option value="分部防火墙">分部防火墙</a-option>
            <a-option value="分部K8S控制节点1">分部K8S控制节点1</a-option>
            <a-option value="分部彩光交换机">分部彩光交换机</a-option>
          </a-select>
        </a-col>
        <a-col :span="6">
          <a-space>
            <a-range-picker
              v-model:value="dateRange"
              format="YYYY-MM-DD"
              @change="handleSearch"
            />
            <a-button type="primary" @click="handleSearch">搜索</a-button>
            <a-button @click="clearSearch">清空</a-button>
          </a-space>
        </a-col>
      </a-row>
    </a-card>

    <!-- 告警记录列表 -->
    <a-card :bordered="false">
      <template #title>
        <a-space>
          <span>告警记录</span>
          <a-tag color="blue">{{ filteredAlertData.length }}条记录</a-tag>
          <a-tag color="orange">{{ pendingCount }}条待处理</a-tag>
          <a-badge :count="newAlertCount" :dot="newAlertCount > 0">
            <a-button size="small" @click="autoRefresh = !autoRefresh" :type="autoRefresh ? 'primary' : 'outline'">
              <template #icon>
                <icon-sync />
              </template>
              自动刷新
            </a-button>
          </a-badge>
        </a-space>
      </template>
      
      <template #extra>
        <a-space>
          <a-button size="small" @click="markAllAsRead">
            <template #icon>
              <icon-check />
            </template>
            标记已读
          </a-button>
          <a-button size="small" @click="batchProcess">
            <template #icon>
              <icon-thunderbolt />
            </template>
            批量处理
          </a-button>
        </a-space>
      </template>

      <a-table
        :columns="alertColumns"
        :data="filteredAlertData"
        :pagination="{ pageSize: 20, showTotal: true }"
        :scroll="{ x: '100%' }"
        :loading="tableLoading"
        row-key="key"
      >
        <template #level="{ record }">
          <a-tag :color="getLevelColor(record.level)" size="small">
            <template #icon>
              <component :is="getLevelIcon(record.level)" />
            </template>
            {{ getLevelText(record.level) }}
          </a-tag>
        </template>

        <template #status="{ record }">
          <a-tag :color="getStatusColor(record.status)" size="small">
            {{ getStatusText(record.status) }}
          </a-tag>
        </template>

        <template #message="{ record }">
          <div class="alert-message">
            <a-tooltip :content="record.message" placement="topLeft">
              {{ record.message }}
            </a-tooltip>
          </div>
        </template>

        <template #time="{ record }">
          <span class="time-text">{{ record.time }}</span>
        </template>

        <template #count="{ record }">
          <span class="count-badge" :class="{ 'high-count': record.count > 5 }">
            {{ record.count }}
          </span>
        </template>

        <template #actions="{ record }">
          <a-space>
            <a-button type="text" size="small" @click="viewDetail(record)">
              详情
            </a-button>
            <a-button 
              type="text" 
              size="small" 
              @click="processAlert(record)"
              :disabled="record.status === 'resolved'"
            >
              处理
            </a-button>
            <a-button 
              type="text" 
              size="small" 
              @click="ignoreAlert(record)"
              :disabled="record.status === 'ignored'"
            >
              忽略
            </a-button>
          </a-space>
        </template>
      </a-table>
    </a-card>

    <!-- 告警详情模态框 -->
    <a-modal
      v-model:visible="detailModalVisible"
      title="告警详情"
      width="800px"
      :footer="false"
    >
      <div v-if="currentAlert" class="alert-detail">
        <a-descriptions :column="2" bordered>
          <a-descriptions-item label="告警ID">
            {{ currentAlert.key }}
          </a-descriptions-item>
          <a-descriptions-item label="告警级别">
            <a-tag :color="getLevelColor(currentAlert.level)">
              {{ getLevelText(currentAlert.level) }}
            </a-tag>
          </a-descriptions-item>
          <a-descriptions-item label="告警来源" :span="2">
            {{ currentAlert.source }}
          </a-descriptions-item>
          <a-descriptions-item label="告警时间" :span="2">
            {{ currentAlert.time }}
          </a-descriptions-item>
          <a-descriptions-item label="告警消息" :span="2">
            {{ currentAlert.message }}
          </a-descriptions-item>
          <a-descriptions-item label="发生次数">
            {{ currentAlert.count }}次
          </a-descriptions-item>
          <a-descriptions-item label="处理状态">
            <a-tag :color="getStatusColor(currentAlert.status)">
              {{ getStatusText(currentAlert.status) }}
            </a-tag>
          </a-descriptions-item>
        </a-descriptions>

        <a-divider>解决建议</a-divider>
        <div class="solution-content">
          {{ currentAlert.solution }}
        </div>

        <a-divider>相关日志</a-divider>
        <div class="related-logs">
          <div v-for="log in currentAlert.relatedLogs" :key="log.id" class="log-item">
            <span class="log-time">{{ log.time }}</span>
            <span class="log-content">{{ log.content }}</span>
          </div>
        </div>
      </div>
    </a-modal>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { Message } from '@arco-design/web-vue'
import PageHeader from '@/components/PageHeader.vue'
import StatCard from '@/components/StatCard.vue'
import {
  IconRefresh,
  IconDownload,
  IconSearch,
  IconCheck,
  IconExclamation,
  IconExclamationCircle,
  IconSettings,
  IconSync,
  IconThunderbolt,
  IconCloseCircle,
  IconCheckCircle,
  IconInfo
} from '@arco-design/web-vue/es/icon'

// 响应式数据
const refreshing = ref(false)
const tableLoading = ref(false)
const detailModalVisible = ref(false)
const currentAlert = ref<any>(null)
const autoRefresh = ref(true)
const newAlertCount = ref(0)
const searchKeyword = ref('')
const selectedLevel = ref('')
const selectedStatus = ref('')
const selectedSource = ref('')
const dateRange = ref([])

// 定时器
let refreshTimer: any = null

// 告警统计数据 - 根据实际数据计算
const alertStats = computed(() => {
  const errorCount = alertData.value.filter(alert => alert.level === 'error').length
  const warningCount = alertData.value.filter(alert => alert.level === 'warning').length
  const processedCount = alertData.value.filter(alert => alert.status === 'resolved').length
  const rulesCount = 45 // 来自规则管理页面的规则总数
  
  return {
    error: errorCount,
    warning: warningCount,
    processed: processedCount,
    rules: rulesCount
  }
})



// 告警数据
const alertData = ref([
  {
    key: 'AL001',
    level: 'warning',
    source: '分部K8S工作节点1',
    message: '磁盘使用率达到85%，建议清理日志文件',
    time: '2024-01-15 10:45:22',
    status: 'pending',
    count: 3,
    solution: '1. 检查/var/log目录下的日志文件大小\n2. 清理过期的日志文件\n3. 配置日志轮转策略\n4. 监控磁盘使用情况',
    relatedLogs: [
      { id: 1, time: '2024-01-15 10:45:22', content: 'Disk usage warning: /dev/sda1 85% used' },
      { id: 2, time: '2024-01-15 10:44:18', content: 'Log rotation failed for /var/log/syslog' },
      { id: 3, time: '2024-01-15 10:43:45', content: 'Available disk space: 2.3GB remaining' }
    ]
  },
  {
    key: 'AL002',
    level: 'warning',
    source: '分部K8S工作节点1',
    message: '内存使用率持续超过80%，可能影响服务性能',
    time: '2024-01-15 10:42:15',
    status: 'processing',
    count: 8,
    solution: '1. 检查内存消耗最高的进程\n2. 重启占用内存过多的服务\n3. 考虑增加内存容量\n4. 优化应用程序内存使用',
    relatedLogs: [
      { id: 1, time: '2024-01-15 10:42:15', content: 'Memory usage: 82.5% (6.6GB/8GB)' },
      { id: 2, time: '2024-01-15 10:41:30', content: 'High memory consumption detected in kubelet process' }
    ]
  },
  {
    key: 'AL003',
    level: 'warning',
    source: '分部彩光交换机',
    message: '端口 Gi0/1 利用率达到90%，可能出现网络拥塞',
    time: '2024-01-15 10:38:45',
    status: 'pending',
    count: 2,
    solution: '1. 检查端口流量统计\n2. 分析流量来源和目的\n3. 考虑链路聚合或升级带宽\n4. 监控网络延迟',
    relatedLogs: [
      { id: 1, time: '2024-01-15 10:38:45', content: 'Interface Gi0/1: Input rate 90.2% of capacity' },
      { id: 2, time: '2024-01-15 10:37:20', content: 'High bandwidth utilization on uplink port' }
    ]
  },
  {
    key: 'AL004',
    level: 'info',
    source: '分部用户接入交换机',
    message: '端口 Gi0/5 链路状态变化：up -> down -> up',
    time: '2024-01-15 10:35:12',
    status: 'resolved',
    count: 1,
    solution: '1. 检查网线连接是否松动\n2. 测试端口和网线质量\n3. 查看对端设备状态\n4. 更换网线或检查端口配置',
    relatedLogs: [
      { id: 1, time: '2024-01-15 10:35:12', content: 'Interface Gi0/5: Link state changed to UP' },
      { id: 2, time: '2024-01-15 10:34:58', content: 'Interface Gi0/5: Link state changed to DOWN' }
    ]
  },
  {
    key: 'AL005',
    level: 'info',
    source: '分部防火墙',
    message: 'VPN隧道连接数增长至25个，接近预警阈值',
    time: '2024-01-15 10:32:33',
    status: 'pending',
    count: 1,
    solution: '1. 监控VPN连接使用情况\n2. 检查VPN许可证数量\n3. 优化VPN连接策略\n4. 考虑升级VPN容量',
    relatedLogs: [
      { id: 1, time: '2024-01-15 10:32:33', content: 'Active VPN tunnels: 25 (threshold: 30)' },
      { id: 2, time: '2024-01-15 10:30:15', content: 'New VPN connection established from 192.168.1.100' }
    ]
  },
  {
    key: 'AL006',
    level: 'warning',
    source: '分部K8S控制节点1',
    message: 'etcd集群延迟超过100ms，可能影响集群响应',
    time: '2024-01-15 10:28:21',
    status: 'processing',
    count: 5,
    solution: '1. 检查etcd集群健康状态\n2. 分析网络延迟原因\n3. 优化etcd配置参数\n4. 监控磁盘I/O性能',
    relatedLogs: [
      { id: 1, time: '2024-01-15 10:28:21', content: 'etcd cluster latency: 125ms (threshold: 100ms)' },
      { id: 2, time: '2024-01-15 10:27:45', content: 'Slow etcd request detected: PUT /registry/pods' }
    ]
  },
  {
    key: 'AL007',
    level: 'info',
    source: '分部AP',
    message: '无线客户端连接数增长至32个，网络使用活跃',
    time: '2024-01-15 10:25:18',
    status: 'resolved',
    count: 1,
    solution: '1. 监控无线网络性能\n2. 检查客户端连接质量\n3. 优化无线信道配置\n4. 考虑增加AP数量',
    relatedLogs: [
      { id: 1, time: '2024-01-15 10:25:18', content: 'Wireless clients connected: 32' },
      { id: 2, time: '2024-01-15 10:24:30', content: 'New client connected: MAC 00:1A:2B:3C:4D:5E' }
    ]
  },
  {
    key: 'AL008',
    level: 'info',
    source: '分部集群接入交换机',
    message: '检测到配置变更：VLAN 100新增端口配置',
    time: '2024-01-15 10:22:45',
    status: 'resolved',
    count: 1,
    solution: '1. 验证配置变更是否符合预期\n2. 检查VLAN配置一致性\n3. 测试网络连通性\n4. 更新配置文档',
    relatedLogs: [
      { id: 1, time: '2024-01-15 10:22:45', content: 'Configuration change: VLAN 100 added to interface Gi0/10' },
      { id: 2, time: '2024-01-15 10:22:30', content: 'Admin user performed configuration save' }
    ]
  }
])

// 过滤后的告警数据
const filteredAlertData = computed(() => {
  let filtered = alertData.value
  
  if (searchKeyword.value) {
    filtered = filtered.filter(alert => 
      alert.message.toLowerCase().includes(searchKeyword.value.toLowerCase()) ||
      alert.source.toLowerCase().includes(searchKeyword.value.toLowerCase())
    )
  }
  
  if (selectedLevel.value) {
    filtered = filtered.filter(alert => alert.level === selectedLevel.value)
  }
  
  if (selectedStatus.value) {
    filtered = filtered.filter(alert => alert.status === selectedStatus.value)
  }
  
  if (selectedSource.value) {
    filtered = filtered.filter(alert => alert.source === selectedSource.value)
  }
  
  return filtered
})

// 待处理告警数量
const pendingCount = computed(() => {
  return alertData.value.filter(alert => alert.status === 'pending').length
})

// 表格列配置
const alertColumns = [
  {
    title: 'ID',
    dataIndex: 'key',
    width: 80
  },
  {
    title: '级别',
    dataIndex: 'level',
    slotName: 'level',
    width: 80
  },
  {
    title: '来源',
    dataIndex: 'source',
    width: 150
  },
  {
    title: '告警消息',
    dataIndex: 'message',
    slotName: 'message',
    ellipsis: true,
    tooltip: true
  },
  {
    title: '时间',
    dataIndex: 'time',
    slotName: 'time',
    width: 150
  },
  {
    title: '次数',
    dataIndex: 'count',
    slotName: 'count',
    width: 80
  },
  {
    title: '状态',
    dataIndex: 'status',
    slotName: 'status',
    width: 100
  },
  {
    title: '操作',
    slotName: 'actions',
    width: 150,
    fixed: 'right'
  }
]

// 工具函数
const getLevelColor = (level: string) => {
  switch (level) {
    case 'error': return 'red'
    case 'warning': return 'orange'
    case 'info': return 'blue'
    default: return 'gray'
  }
}

const getLevelText = (level: string) => {
  switch (level) {
    case 'error': return '错误'
    case 'warning': return '警告'
    case 'info': return '信息'
    default: return '未知'
  }
}

const getLevelIcon = (level: string) => {
  switch (level) {
    case 'error': return IconExclamationCircle
    case 'warning': return IconExclamation
    case 'info': return IconInfo
    default: return IconInfo
  }
}

const getStatusColor = (status: string) => {
  switch (status) {
    case 'pending': return 'red'
    case 'processing': return 'orange'
    case 'resolved': return 'green'
    case 'ignored': return 'gray'
    default: return 'gray'
  }
}

const getStatusText = (status: string) => {
  switch (status) {
    case 'pending': return '待处理'
    case 'processing': return '处理中'
    case 'resolved': return '已解决'
    case 'ignored': return '已忽略'
    default: return '未知'
  }
}

// 事件处理函数
const refreshData = async () => {
  refreshing.value = true
  await new Promise(resolve => setTimeout(resolve, 1500))
  refreshing.value = false
  newAlertCount.value = 0
  Message.success('告警数据刷新成功')
}

const exportData = () => {
  Message.info('正在导出告警记录...')
}

const handleSearch = () => {
  console.log('搜索告警记录')
}

const clearSearch = () => {
  searchKeyword.value = ''
  selectedLevel.value = ''
  selectedStatus.value = ''
  selectedSource.value = ''
  dateRange.value = []
}

const viewDetail = (record: any) => {
  currentAlert.value = record
  detailModalVisible.value = true
}

const processAlert = (record: any) => {
  record.status = 'processing'
  Message.success(`告警 ${record.key} 已标记为处理中`)
}

const ignoreAlert = (record: any) => {
  record.status = 'ignored'
  Message.success(`告警 ${record.key} 已忽略`)
}

const markAllAsRead = () => {
  newAlertCount.value = 0
  Message.success('所有告警已标记为已读')
}

const batchProcess = () => {
  Message.info('批量处理功能开发中...')
}

// 自动刷新功能
const startAutoRefresh = () => {
  if (refreshTimer) return
  
  refreshTimer = setInterval(() => {
    if (autoRefresh.value) {
      // 模拟新告警
      if (Math.random() > 0.7) {
        newAlertCount.value++
      }
    }
  }, 30000) // 30秒检查一次
}

const stopAutoRefresh = () => {
  if (refreshTimer) {
    clearInterval(refreshTimer)
    refreshTimer = null
  }
}

onMounted(() => {
  startAutoRefresh()
})

onUnmounted(() => {
  stopAutoRefresh()
})
</script>

<style scoped>
.alert-record-page {
  padding: 0;
}

.stats-row {
  margin-bottom: 24px;
}

.search-card {
  margin-bottom: 24px;
}

.alert-message {
  max-width: 300px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.time-text {
  color: #666;
  font-size: 12px;
}

.count-badge {
  background: #f0f0f0;
  padding: 2px 6px;
  border-radius: 10px;
  font-size: 12px;
  font-weight: 500;
}

.count-badge.high-count {
  background: #fff2e8;
  color: #fa8c16;
}

.alert-detail {
  padding: 16px 0;
}

.solution-content {
  background: #f6ffed;
  border: 1px solid #b7eb8f;
  border-radius: 6px;
  padding: 12px;
  white-space: pre-line;
  line-height: 1.6;
}

.related-logs {
  max-height: 200px;
  overflow-y: auto;
  background: #fafafa;
  border-radius: 6px;
  padding: 8px;
}

.log-item {
  display: flex;
  margin-bottom: 8px;
  padding: 8px;
  background: white;
  border-radius: 4px;
  font-family: 'Courier New', monospace;
  font-size: 12px;
}

.log-time {
  color: #666;
  margin-right: 12px;
  min-width: 130px;
}

.log-content {
  color: #333;
  flex: 1;
}

:deep(.arco-card) {
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}
</style> 