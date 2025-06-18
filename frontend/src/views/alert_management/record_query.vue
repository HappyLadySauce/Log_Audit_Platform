<template>
  <div class="alert-record-page">
    <PageHeader title="告警记录查询" description="查看和分析历史告警记录，跟踪告警处理状态和趋势">
      <template #extra>
        <a-space>
          <a-tag color="green">
            <template #icon>
              <icon-sync />
            </template>
            自动刷新中
          </a-tag>
          <a-button type="primary" @click="exportData">
            <template #icon>
              <icon-download />
            </template>
            导出数据
          </a-button>
        </a-space>
      </template>
    </PageHeader>

    <!-- 告警统计 -->
    <a-row :gutter="24" class="stats-row">
      <a-col :span="8">
        <StatCard
          :icon="IconExclamationCircle"
          icon-bg-color="#faad14"
          :value="stats.pending"
          label="待处理"
          subtitle="需要立即关注"
          :active="activeTab === 'pending'"
          @click="setActiveTab('pending')"
        />
      </a-col>
      <a-col :span="8">
        <StatCard
          :icon="IconCheckCircle"
          icon-bg-color="#52c41a"
          :value="stats.resolved"
          label="已处理"
          subtitle="问题已解决"
          :active="activeTab === 'resolved'"
          @click="setActiveTab('resolved')"
        />
      </a-col>
      <a-col :span="8">
        <StatCard
          :icon="IconFolder"
          icon-bg-color="#722ed1"
          :value="stats.archived"
          label="已归档"
          subtitle="完成归档"
          :active="activeTab === 'archived'"
          @click="setActiveTab('archived')"
        />
      </a-col>
    </a-row>

    <!-- 告警列表 -->
    <a-card :bordered="false">
      <template #title>
        <a-space>
          <span>告警记录</span>
          <a-tag color="blue">{{ filteredAlerts.length }}条记录</a-tag>
          <a-tag v-if="activeTab !== 'all'" color="green">{{ getStatusText(activeTab) }}</a-tag>
        </a-space>
      </template>

      <template #extra>
        <a-space>
          <a-input
            v-model:value="searchKeyword"
            placeholder="搜索告警名称、描述..."
            style="width: 250px"
            allow-clear
          >
            <template #prefix>
              <icon-search />
            </template>
          </a-input>
          <a-select
            v-model:value="filterLevel"
            placeholder="告警等级"
            style="width: 120px"
            allow-clear
          >
            <a-option value="">全部等级</a-option>
            <a-option value="CRITICAL">严重</a-option>
            <a-option value="HIGH">高</a-option>
            <a-option value="MEDIUM">中</a-option>
            <a-option value="LOW">低</a-option>
          </a-select>
        </a-space>
      </template>

      <a-table
        :columns="alertColumns"
        :data="filteredAlerts"
        :pagination="{ pageSize: 15, showTotal: true }"
        :scroll="{ x: '100%' }"
        :loading="loading"
        row-key="id"
      >
        <template #alert_level="{ record }">
          <a-tag :color="getLevelTagColor(record.alert_level)" size="small">
            {{ getLevelText(record.alert_level) }}
          </a-tag>
        </template>

        <template #status="{ record }">
          <a-badge
            :status="getStatusBadgeType(record.status)"
            :text="getStatusText(record.status)"
          />
        </template>

        <template #asset_info="{ record }">
          <div v-if="record.asset">
            <div class="asset-name">{{ record.asset.name }}</div>
            <div class="asset-ip">{{ record.asset.ip_address }}</div>
          </div>
          <span v-else>-</span>
        </template>

        <template #rule_info="{ record }">
          <div v-if="record.rule">
            <div class="rule-name">{{ record.rule.name }}</div>
            <div class="trigger-condition">{{ record.rule.trigger_condition }}</div>
          </div>
          <span v-else>-</span>
        </template>

        <template #processor_info="{ record }">
          <div v-if="record.processor">
            <div class="processor-name">{{ record.processor }}</div>
            <div class="process-time" v-if="record.processed_at">
              {{ formatDateTime(record.processed_at) }}
            </div>
          </div>
          <span v-else>-</span>
        </template>

        <template #actions="{ record }">
          <a-space>
            <a-button type="text" size="small" @click="viewAlert(record)">
              <template #icon>
                <icon-eye />
              </template>
              查看
            </a-button>
            <a-button
              v-if="record.status === 'PENDING' || record.status === 'pending'"
              type="text"
              size="small"
              @click="processAlert(record)"
            >
              <template #icon>
                <icon-play-arrow />
              </template>
              处理
            </a-button>
            <a-button
              v-if="record.status === 'RESOLVED' || record.status === 'resolved'"
              type="text"
              size="small"
              @click="archiveAlert(record)"
            >
              <template #icon>
                <icon-folder />
              </template>
              归档
            </a-button>
          </a-space>
        </template>
      </a-table>
    </a-card>

    <!-- 告警详情弹窗 -->
    <a-modal v-model:visible="detailModalVisible" title="告警详情" :width="900" :footer="false">
      <div v-if="selectedAlert" class="alert-detail">
        <a-descriptions :column="2" bordered size="medium">
          <a-descriptions-item label="告警ID">{{ selectedAlert.id }}</a-descriptions-item>
          <a-descriptions-item label="告警标题">{{ selectedAlert.title }}</a-descriptions-item>
          <a-descriptions-item label="告警等级">
            <a-tag :color="getLevelTagColor(selectedAlert.alert_level)">
              {{ getLevelText(selectedAlert.alert_level) }}
            </a-tag>
          </a-descriptions-item>
          <a-descriptions-item label="状态">
            <a-badge
              :status="getStatusBadgeType(selectedAlert.status)"
              :text="getStatusText(selectedAlert.status)"
            />
          </a-descriptions-item>
          <a-descriptions-item label="触发时间">
            {{ formatDateTime(selectedAlert.triggered_at) }}
          </a-descriptions-item>
          <a-descriptions-item label="处理时间">
            {{ selectedAlert.processed_at ? formatDateTime(selectedAlert.processed_at) : '-' }}
          </a-descriptions-item>
          <a-descriptions-item label="解决时间">
            {{ selectedAlert.resolved_at ? formatDateTime(selectedAlert.resolved_at) : '-' }}
          </a-descriptions-item>
          <a-descriptions-item label="处理人">
            {{ selectedAlert.processor || '-' }}
          </a-descriptions-item>
          <a-descriptions-item label="监控对象" :span="2">
            <div v-if="selectedAlert.asset">
              <a-tag color="blue">{{ selectedAlert.asset.name }}</a-tag>
              <a-tag color="green">{{ selectedAlert.asset.ip_address }}</a-tag>
              <a-tag color="orange">{{ selectedAlert.asset.location }}</a-tag>
            </div>
            <span v-else>-</span>
          </a-descriptions-item>
          <a-descriptions-item label="告警规则" :span="2">
            <div v-if="selectedAlert.rule">
              <div><strong>规则名称：</strong>{{ selectedAlert.rule.name }}</div>
              <div><strong>触发条件：</strong>{{ selectedAlert.rule.trigger_condition }}</div>
            </div>
            <span v-else>-</span>
          </a-descriptions-item>
          <a-descriptions-item label="描述" :span="2">
            {{ selectedAlert.description || '-' }}
          </a-descriptions-item>
          <a-descriptions-item label="根本原因分析" :span="2" v-if="selectedAlert.root_cause">
            {{ selectedAlert.root_cause }}
          </a-descriptions-item>
          <a-descriptions-item label="解决方案" :span="2" v-if="selectedAlert.solution">
            {{ selectedAlert.solution }}
          </a-descriptions-item>
          <a-descriptions-item label="遗留问题" :span="2" v-if="selectedAlert.remaining_issues">
            {{ selectedAlert.remaining_issues }}
          </a-descriptions-item>
        </a-descriptions>
      </div>
    </a-modal>

    <!-- 归档对话框 -->
    <a-modal
      v-model:visible="archiveModalVisible"
      title="告警处理归档"
      :width="600"
      @ok="submitArchive"
      :ok-loading="archiveLoading"
    >
      <a-form :model="archiveForm" layout="vertical">
        <a-form-item label="处理人" required>
          <a-input
            v-model="archiveForm.processor"
            placeholder="请输入处理人真实姓名（至少2个字符）"
          />
        </a-form-item>
        <a-form-item label="根本原因分析" required>
          <a-textarea
            v-model="archiveForm.root_cause"
            :rows="4"
            placeholder="请详细分析告警的根本原因，包括故障发生的技术细节和原因（至少10个字符）..."
            :show-word-limit="true"
            :max-length="500"
          />
          <div style="font-size: 12px; color: #999; margin-top: 4px">
            当前字符数: {{ archiveForm.root_cause?.length || 0 }} / 至少10个字符
          </div>
        </a-form-item>
        <a-form-item label="解决方案" required>
          <a-textarea
            v-model="archiveForm.solution"
            :rows="4"
            placeholder="请描述具体的解决方案，包括操作步骤和修复过程（至少10个字符）..."
            :show-word-limit="true"
            :max-length="500"
          />
          <div style="font-size: 12px; color: #999; margin-top: 4px">
            当前字符数: {{ archiveForm.solution?.length || 0 }} / 至少10个字符
          </div>
        </a-form-item>
        <a-form-item label="遗留问题">
          <a-textarea
            v-model="archiveForm.remaining_issues"
            :rows="3"
            placeholder="如有遗留问题请详细说明，可以留空..."
          />
        </a-form-item>
      </a-form>
    </a-modal>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted, onUnmounted } from 'vue'
import { Message, Modal } from '@arco-design/web-vue'
import PageHeader from '@/components/PageHeader.vue'
import StatCard from '@/components/StatCard.vue'
import alertsApi from '@/services/alerts'
import type { Alert } from '@/services/alerts'
import {
  IconSync,
  IconDownload,
  IconExclamationCircle,
  IconCheckCircle,
  IconFolder,
  IconSearch,
  IconEye,
  IconPlayArrow,
} from '@arco-design/web-vue/es/icon'

// 响应式数据
const loading = ref(false)
const activeTab = ref('pending')
const searchKeyword = ref('')
const filterLevel = ref('')

// 自动刷新相关
const autoRefreshInterval = ref<number | null>(null)
const REFRESH_INTERVAL = 5000 // 5秒刷新一次

const stats = reactive({
  pending: 0,
  resolved: 0,
  archived: 0,
})

const alerts = ref<Alert[]>([])
const selectedAlert = ref<Alert | null>(null)

// 对话框状态
const detailModalVisible = ref(false)
const archiveModalVisible = ref(false)
const archiveLoading = ref(false)

// 归档表单
const archiveForm = reactive({
  processor: '系统分析师',
  root_cause: '',
  solution: '',
  remaining_issues: '',
})

// 表格列配置
const alertColumns = [
  {
    title: 'ID',
    dataIndex: 'id',
    width: 80,
  },
  {
    title: '告警名称',
    dataIndex: 'title',
    minWidth: 200,
  },
  {
    title: '等级',
    dataIndex: 'alert_level',
    width: 100,
    slotName: 'alert_level',
  },
  {
    title: '状态',
    dataIndex: 'status',
    width: 100,
    slotName: 'status',
  },
  {
    title: '监控对象',
    width: 160,
    slotName: 'asset_info',
  },
  {
    title: '告警规则',
    width: 200,
    slotName: 'rule_info',
  },
  {
    title: '触发时间',
    dataIndex: 'triggered_at',
    width: 160,
    render: ({ record }: any) => formatDateTime(record.triggered_at),
  },
  {
    title: '处理信息',
    width: 160,
    slotName: 'processor_info',
  },
  {
    title: '操作',
    width: 200,
    fixed: 'right',
    slotName: 'actions',
  },
]

// 计算属性
const filteredAlerts = computed(() => {
  let result = alerts.value

  // 按状态筛选
  if (activeTab.value !== 'all') {
    const statusMap: Record<string, string> = {
      pending: 'PENDING',
      resolved: 'RESOLVED',
      archived: 'ARCHIVED',
    }
    const dbStatus = statusMap[activeTab.value] || activeTab.value.toUpperCase()
    result = result.filter((alert) => alert.status === dbStatus || alert.status === activeTab.value)
  }

  // 按关键词搜索
  if (searchKeyword.value) {
    const keyword = searchKeyword.value.toLowerCase()
    result = result.filter(
      (alert) =>
        (alert.title || '').toLowerCase().includes(keyword) ||
        (alert.description || '').toLowerCase().includes(keyword) ||
        (alert.asset?.name || '').toLowerCase().includes(keyword),
    )
  }

  // 按等级筛选
  if (filterLevel.value) {
    result = result.filter((alert) => alert.alert_level === filterLevel.value)
  }

  return result
})

// 方法
const setActiveTab = (tab: string) => {
  activeTab.value = tab
}

const refreshData = async () => {
  await Promise.all([loadAlerts(), loadStats()])
}

const loadStats = async () => {
  try {
    const response = await alertsApi.getAlertStats()
    Object.assign(stats, response)
  } catch (error) {
    console.error('获取统计数据失败:', error)
    // 提供默认数据
    Object.assign(stats, {
      pending: 2,
      resolved: 3,
      archived: 1,
    })
  }
}

const loadAlerts = async () => {
  loading.value = true
  try {
    const response = await alertsApi.getAlerts()
    alerts.value = response || []
  } catch (error) {
    console.error('获取告警数据失败:', error)
    // 提供模拟数据
    alerts.value = [
      {
        id: 1,
        rule_id: 1,
        asset_id: 1,
        title: '核心网络设备离线告警',
        description: 'Access-Switch-Branch 连续5分钟未收到心跳信号，设备可能已离线',
        alert_level: 'critical',
        status: 'pending',
        triggered_at: new Date(Date.now() - 3600000).toISOString(),
        processed_at: null,
        resolved_at: null,
        processor: null,
        root_cause: null,
        solution: null,
        remaining_issues: null,
        asset: {
          id: 1,
          name: 'Access-Switch-Branch',
          ip_address: '192.168.10.1',
          location: '分部机房',
          asset_type: 'network_device',
        },
        rule: {
          id: 1,
          name: '核心网络设备离线告警',
          trigger_condition: '连续5分钟未收到心跳',
          alert_level: 'critical',
        },
      },
      {
        id: 2,
        rule_id: 2,
        asset_id: 2,
        title: 'K8S集群API Server无响应',
        description: 'Kubernetes API Server 连接超时，集群管理功能受影响',
        alert_level: 'critical',
        status: 'pending',
        triggered_at: new Date(Date.now() - 1800000).toISOString(),
        processed_at: null,
        resolved_at: null,
        processor: null,
        root_cause: null,
        solution: null,
        remaining_issues: null,
        asset: {
          id: 2,
          name: '分部K8S集群',
          ip_address: '192.168.20.10',
          location: '数据中心B栋',
          asset_type: 'k8s_cluster',
        },
        rule: {
          id: 2,
          name: 'K8S集群API Server无响应',
          trigger_condition: 'Kube-apiserver 连接超时',
          alert_level: 'critical',
        },
      },
      {
        id: 3,
        rule_id: 3,
        asset_id: 3,
        title: '服务器CPU使用率过高',
        description: 'Web服务器CPU使用率持续超过85%，性能下降',
        alert_level: 'warning',
        status: 'resolved',
        triggered_at: new Date(Date.now() - 7200000).toISOString(),
        processed_at: new Date(Date.now() - 5400000).toISOString(),
        resolved_at: new Date(Date.now() - 3600000).toISOString(),
        processor: '运维工程师',
        root_cause: '应用程序内存泄漏导致CPU占用过高',
        solution: '重启应用服务，优化代码逻辑',
        remaining_issues: '需要进一步监控应用性能',
        asset: {
          id: 3,
          name: 'Web-Server-01',
          ip_address: '192.168.1.100',
          location: '数据中心A栋',
          asset_type: 'linux_server',
        },
        rule: {
          id: 3,
          name: 'CPU使用率过高告警',
          trigger_condition: 'CPU使用率超过80%持续5分钟',
          alert_level: 'warning',
        },
      },
    ] as Alert[]
  } finally {
    loading.value = false
  }
}

const viewAlert = (alert: Alert) => {
  selectedAlert.value = alert
  detailModalVisible.value = true
}

const processAlert = async (alert: Alert) => {
  try {
    await Modal.confirm({
      title: '确认处理',
      content: `确定要开始处理告警"${alert.title}"吗？`,
    })

    await alertsApi.processAlert(alert.id, { processor: '系统分析师' })
    Message.success('告警已开始处理')
    await refreshData()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('处理告警失败:', error)
      Message.error('处理告警失败')
    }
  }
}

const archiveAlert = (alert: Alert) => {
  selectedAlert.value = alert
  // 重置表单所有字段
  Object.assign(archiveForm, {
    processor: '系统分析师',
    root_cause: '',
    solution: '',
    remaining_issues: '',
  })
  archiveModalVisible.value = true
}

const submitArchive = async () => {
  if (!selectedAlert.value) return

  // 表单验证 - 检查字段是否为空或只包含空白字符
  const processor = (archiveForm.processor || '').trim()
  const rootCause = (archiveForm.root_cause || '').trim()
  const solution = (archiveForm.solution || '').trim()

  if (!processor || !rootCause || !solution) {
    Message.warning('请填写必填字段：处理人、根本原因分析、解决方案')
    return
  }

  // 验证内容长度
  if (processor.length < 2) {
    Message.warning(`处理人姓名至少需要2个字符，当前${processor.length}个字符`)
    return
  }
  if (rootCause.length < 10) {
    Message.warning(`根本原因分析至少需要10个字符，当前${rootCause.length}个字符`)
    return
  }
  if (solution.length < 10) {
    Message.warning(`解决方案至少需要10个字符，当前${solution.length}个字符`)
    return
  }

  archiveLoading.value = true
  try {
    await alertsApi.archiveAlert(selectedAlert.value.id, {
      processor: processor,
      root_cause: rootCause,
      solution: solution,
      remaining_issues: (archiveForm.remaining_issues || '').trim(),
    })

    Message.success('告警归档成功')
    archiveModalVisible.value = false
    resetArchiveForm()
    await refreshData()
  } catch (error) {
    console.error('归档告警失败:', error)
    Message.error('归档告警失败')
  } finally {
    archiveLoading.value = false
  }
}

const resetArchiveForm = () => {
  Object.assign(archiveForm, {
    processor: '系统分析师',
    root_cause: '',
    solution: '',
    remaining_issues: '',
  })
  selectedAlert.value = null
}

const exportData = () => {
  Message.info('导出功能开发中...')
}

// 辅助方法
const getLevelTagColor = (level: string) => {
  const colorMap: Record<string, string> = {
    CRITICAL: 'red',
    HIGH: 'red',
    MEDIUM: 'orange',
    LOW: 'blue',
    critical: 'red',
    warning: 'orange',
    info: 'blue',
  }
  return colorMap[level] || 'gray'
}

const getLevelText = (level: string) => {
  const textMap: Record<string, string> = {
    CRITICAL: '严重',
    HIGH: '高',
    MEDIUM: '中',
    LOW: '低',
    critical: '严重',
    warning: '警告',
    info: '信息',
  }
  return textMap[level] || level || '未知'
}

const getStatusBadgeType = (status: string) => {
  const typeMap: Record<string, string> = {
    PENDING: 'warning',
    RESOLVED: 'success',
    ARCHIVED: 'default',
    pending: 'warning',
    resolved: 'success',
    archived: 'default',
  }
  return typeMap[status] || 'default'
}

const getStatusText = (status: string) => {
  const textMap: Record<string, string> = {
    PENDING: '待处理',
    RESOLVED: '已处理',
    ARCHIVED: '已归档',
    pending: '待处理',
    resolved: '已处理',
    archived: '已归档',
  }
  return textMap[status] || status || '未知'
}

const formatDateTime = (dateTime: string | Date) => {
  if (!dateTime) return '-'
  const date = new Date(dateTime)
  return date.toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
  })
}

// 自动刷新功能
const startAutoRefresh = () => {
  // 先清除可能存在的定时器
  if (autoRefreshInterval.value) {
    clearInterval(autoRefreshInterval.value)
  }

  // 设置新的定时器
  autoRefreshInterval.value = setInterval(() => {
    refreshData()
  }, REFRESH_INTERVAL)
}

const stopAutoRefresh = () => {
  if (autoRefreshInterval.value) {
    clearInterval(autoRefreshInterval.value)
    autoRefreshInterval.value = null
  }
}

// 监听全局事件（触发故障/修复故障）
const handleGlobalRefresh = () => {
  // 立即刷新数据
  refreshData()
  // 重启自动刷新
  startAutoRefresh()
}

// 生命周期
onMounted(() => {
  refreshData()
  startAutoRefresh()

  // 监听全局刷新事件
  window.addEventListener('alertDataChanged', handleGlobalRefresh)
})

onUnmounted(() => {
  stopAutoRefresh()
  window.removeEventListener('alertDataChanged', handleGlobalRefresh)
})
</script>

<style scoped>
.alert-record-page {
  padding: 0;
}

.stats-row {
  margin-bottom: 24px;
}

.asset-name {
  font-weight: 500;
  color: #1890ff;
}

.asset-ip {
  font-size: 12px;
  color: #999;
}

.rule-name {
  font-weight: 500;
  color: #333;
  margin-bottom: 2px;
}

.trigger-condition {
  font-size: 12px;
  color: #666;
}

.processor-name {
  font-weight: 500;
  color: #52c41a;
}

.process-time {
  font-size: 12px;
  color: #999;
}

.alert-detail {
  margin: 16px 0;
}

.alert-detail strong {
  color: #333;
}
</style>
