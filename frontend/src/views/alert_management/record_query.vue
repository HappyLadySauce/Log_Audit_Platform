<template>
  <div class="alert-record-page">
    <PageHeader title="告警记录查询" description="查看和分析分部IT基础设施告警记录">
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
          :value="alertStats.pending"
          label="待处理"
          subtitle="需要立即处理"
        />
      </a-col>
      <a-col :span="6">
        <StatCard
          :icon="IconExclamation"
          icon-bg-color="#faad14"
          :value="alertStats.processing"
          label="处理中"
          subtitle="正在处理"
        />
      </a-col>
      <a-col :span="6">
        <StatCard
          :icon="IconCheck"
          icon-bg-color="#52c41a"
          :value="alertStats.resolved"
          label="已解决"
          subtitle="处理完成"
        />
      </a-col>
      <a-col :span="6">
        <StatCard
          :icon="IconSettings"
          icon-bg-color="#1890ff"
          :value="alertStats.archived"
          label="已归档"
          subtitle="已归档记录"
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
          <a-select
            v-model:value="selectedLevel"
            placeholder="告警级别"
            allow-clear
            @change="handleSearch"
          >
            <a-option value="严重">严重</a-option>
            <a-option value="警告">警告</a-option>
            <a-option value="信息">信息</a-option>
          </a-select>
        </a-col>
        <a-col :span="4">
          <a-select
            v-model:value="selectedStatus"
            placeholder="处理状态"
            allow-clear
            @change="handleSearch"
          >
            <a-option value="pending">待处理</a-option>
            <a-option value="processing">处理中</a-option>
            <a-option value="resolved">已解决</a-option>
            <a-option value="ignored">已忽略</a-option>
          </a-select>
        </a-col>
        <a-col :span="4">
          <a-select
            v-model:value="selectedSource"
            placeholder="告警来源"
            allow-clear
            @change="handleSearch"
          >
            <a-option value="分部防火墙">分部防火墙</a-option>
            <a-option value="分部K8S控制节点1">分部K8S控制节点1</a-option>
            <a-option value="分部彩光交换机">分部彩光交换机</a-option>
          </a-select>
        </a-col>
        <a-col :span="6">
          <a-space>
            <a-range-picker v-model:value="dateRange" format="YYYY-MM-DD" @change="handleSearch" />
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
            <a-button
              size="small"
              @click="autoRefresh = !autoRefresh"
              :type="autoRefresh ? 'primary' : 'outline'"
            >
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
            <a-button type="text" size="small" @click="viewDetail(record)"> 详情 </a-button>
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
    <a-modal v-model:visible="detailModalVisible" title="告警详情" width="800px" :footer="false">
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
          <a-descriptions-item label="发生次数"> {{ currentAlert.count }}次 </a-descriptions-item>
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
import { alertsApi, type Alert, type AlertStats } from '@/services/alerts'
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
  IconInfo,
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

// 告警数据
const alertData = ref<Alert[]>([])

// 告警统计数据
const alertStats = ref<AlertStats>({
  pending: 0,
  processing: 0,
  resolved: 0,
  archived: 0,
})

// 获取告警记录列表
const fetchAlerts = async () => {
  try {
    tableLoading.value = true
    const data = await alertsApi.getAlerts()
    alertData.value = data
  } catch (error) {
    console.error('获取告警记录失败:', error)
    Message.error('获取告警记录失败')
  } finally {
    tableLoading.value = false
  }
}

// 获取告警统计
const fetchAlertStats = async () => {
  try {
    const stats = await alertsApi.getAlertStats()
    alertStats.value = stats
  } catch (error) {
    console.error('获取告警统计失败:', error)
  }
}

// 页面加载时获取数据
onMounted(async () => {
  await Promise.all([fetchAlerts(), fetchAlertStats()])

  // 设置自动刷新
  if (autoRefresh.value) {
    refreshTimer = setInterval(async () => {
      await Promise.all([fetchAlerts(), fetchAlertStats()])
    }, 30000) // 30秒刷新一次
  }
})

// 页面卸载时清理定时器
onUnmounted(() => {
  if (refreshTimer) {
    clearInterval(refreshTimer)
  }
})

// 过滤后的告警数据
const filteredAlertData = computed(() => {
  let filtered = alertData.value

  if (searchKeyword.value) {
    filtered = filtered.filter(
      (alert) =>
        (alert.title && alert.title.toLowerCase().includes(searchKeyword.value.toLowerCase())) ||
        (alert.description &&
          alert.description.toLowerCase().includes(searchKeyword.value.toLowerCase())),
    )
  }

  if (selectedLevel.value) {
    filtered = filtered.filter((alert) => alert.alert_level === selectedLevel.value)
  }

  if (selectedStatus.value) {
    filtered = filtered.filter((alert) => alert.status === selectedStatus.value)
  }

  // 暂时移除来源过滤，因为后端数据结构不同
  // if (selectedSource.value) {
  //   filtered = filtered.filter((alert) => alert.asset?.name === selectedSource.value)
  // }

  return filtered
})

// 待处理告警数量
const pendingCount = computed(() => {
  return alertStats.value.pending
})

// 表格列配置
const alertColumns = [
  {
    title: 'ID',
    dataIndex: 'id',
    width: 80,
  },
  {
    title: '级别',
    dataIndex: 'alert_level',
    slotName: 'level',
    width: 80,
  },
  {
    title: '资产ID',
    dataIndex: 'asset_id',
    width: 100,
  },
  {
    title: '告警标题',
    dataIndex: 'title',
    slotName: 'message',
    ellipsis: true,
    tooltip: true,
  },
  {
    title: '时间',
    dataIndex: 'triggered_at',
    slotName: 'time',
    width: 150,
  },
  {
    title: '状态',
    dataIndex: 'status',
    slotName: 'status',
    width: 100,
  },
  {
    title: '操作',
    slotName: 'actions',
    width: 150,
    fixed: 'right',
  },
]

// 工具函数
const getLevelColor = (level: string) => {
  switch (level) {
    case '严重':
      return 'red'
    case '警告':
      return 'orange'
    case '信息':
      return 'blue'
    default:
      return 'gray'
  }
}

const getLevelText = (level: string) => {
  return level || '未知'
}

const getLevelIcon = (level: string) => {
  switch (level) {
    case '严重':
      return IconExclamationCircle
    case '警告':
      return IconExclamation
    case '信息':
      return IconInfo
    default:
      return IconInfo
  }
}

const getStatusColor = (status: string) => {
  switch (status) {
    case 'pending':
      return 'red'
    case 'processing':
      return 'orange'
    case 'resolved':
      return 'green'
    case 'ignored':
      return 'gray'
    default:
      return 'gray'
  }
}

const getStatusText = (status: string) => {
  switch (status) {
    case 'pending':
      return '待处理'
    case 'processing':
      return '处理中'
    case 'resolved':
      return '已解决'
    case 'ignored':
      return '已忽略'
    default:
      return '未知'
  }
}

// 事件处理函数
const refreshData = async () => {
  refreshing.value = true
  try {
    await Promise.all([fetchAlerts(), fetchAlertStats()])
    newAlertCount.value = 0
    Message.success('数据刷新成功')
  } catch (error) {
    Message.error('刷新失败')
  } finally {
    refreshing.value = false
  }
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
