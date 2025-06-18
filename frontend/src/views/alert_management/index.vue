<template>
  <div class="alert-management-index">
    <PageHeader title="告警管理" description="分部IT基础设施告警规则配置和记录查询" />

    <!-- 功能模块导航 -->
    <a-row :gutter="24">
      <a-col :span="12">
        <a-card hoverable class="module-card" @click="goToRuleManagement">
          <template #cover>
            <div class="card-cover">
              <icon-settings class="card-icon" />
            </div>
          </template>
          <a-card-meta
            title="告警规则管理"
            description="配置和管理分部设备的告警规则，设置监控阈值和触发条件"
          />
          <template #actions>
            <a-button type="primary" size="large" style="width: 100%">
              <template #icon>
                <icon-arrow-right />
              </template>
              进入管理
            </a-button>
          </template>
        </a-card>
      </a-col>

      <a-col :span="12">
        <a-card hoverable class="module-card" @click="goToRecordQuery">
          <template #cover>
            <div class="card-cover">
              <icon-info-circle class="card-icon" />
            </div>
          </template>
          <a-card-meta
            title="告警记录查询"
            description="查看和分析历史告警记录，跟踪告警处理状态和趋势"
          />
          <template #actions>
            <a-button type="primary" size="large" style="width: 100%">
              <template #icon>
                <icon-arrow-right />
              </template>
              进入查询
            </a-button>
          </template>
        </a-card>
      </a-col>
    </a-row>

    <!-- 快速统计 -->
    <a-row :gutter="24" style="margin-top: 24px">
      <a-col :span="6">
        <StatCard
          :icon="IconSettings"
          icon-bg-color="#1890ff"
          :value="ruleCount"
          label="配置规则"
          subtitle="已配置告警规则"
        />
      </a-col>
      <a-col :span="6">
        <StatCard
          :icon="IconExclamation"
          icon-bg-color="#faad14"
          :value="alertStats.pending"
          label="待处理"
          subtitle="待处理告警"
        />
      </a-col>
      <a-col :span="6">
        <StatCard
          :icon="IconCheck"
          icon-bg-color="#52c41a"
          :value="alertStats.resolved"
          label="已解决"
          subtitle="已解决告警"
        />
      </a-col>
      <a-col :span="6">
        <StatCard
          :icon="IconEye"
          icon-bg-color="#722ed1"
          :value="alertStats.archived"
          label="已归档"
          subtitle="已归档记录"
        />
      </a-col>
    </a-row>

    <!-- 最近告警快览 -->
    <a-card title="最近告警" style="margin-top: 24px" :bordered="false">
      <a-list :data="recentAlerts" :max-height="300">
        <template #item="{ item }">
          <a-list-item :key="item.id">
            <a-list-item-meta>
              <template #avatar>
                <a-tag :color="getLevelColor(item.alert_level)" size="small">
                  {{ getLevelText(item.alert_level) }}
                </a-tag>
              </template>
              <template #title>{{ item.title }}</template>
              <template #description>{{ item.description || '暂无描述' }}</template>
            </a-list-item-meta>
            <template #actions>
              <span class="time-text">{{ item.triggered_at }}</span>
            </template>
          </a-list-item>
        </template>
      </a-list>
    </a-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import PageHeader from '@/components/PageHeader.vue'
import StatCard from '@/components/StatCard.vue'
import { alertsApi, type Alert, type AlertStats } from '@/services/alerts'
import {
  IconSettings,
  IconInfoCircle,
  IconArrowRight,
  IconExclamation,
  IconCheck,
  IconEye,
} from '@arco-design/web-vue/es/icon'

const router = useRouter()

// 统计数据
const alertStats = ref<AlertStats>({
  pending: 0,
  processing: 0,
  resolved: 0,
  archived: 0,
})

const ruleCount = ref(0)

// 最近告警数据
const recentAlerts = ref<Alert[]>([])

// 获取数据
const fetchData = async () => {
  try {
    const [stats, alerts, rules] = await Promise.all([
      alertsApi.getAlertStats(),
      alertsApi.getAlerts({ limit: 5 }), // 只获取最近5条
      alertsApi.getAlertRules(),
    ])

    alertStats.value = stats
    recentAlerts.value = alerts
    ruleCount.value = rules.length
  } catch (error) {
    console.error('获取数据失败:', error)
  }
}

// 页面加载时获取数据
onMounted(() => {
  fetchData()
})

// 导航函数
const goToRuleManagement = () => {
  router.push('/alert-management/rule-management')
}

const goToRecordQuery = () => {
  router.push('/alert-management/record-query')
}

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
</script>

<style scoped>
.alert-management-index {
  padding: 0;
}

.module-card {
  cursor: pointer;
  transition: all 0.3s ease;
}

.module-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
}

.card-cover {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 160px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.card-icon {
  font-size: 64px;
  color: white;
}

.time-text {
  color: #666;
  font-size: 12px;
}

:deep(.arco-card) {
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

:deep(.arco-card-meta-title) {
  font-size: 18px;
  font-weight: 600;
}

:deep(.arco-card-meta-description) {
  color: #666;
  line-height: 1.6;
}
</style>
