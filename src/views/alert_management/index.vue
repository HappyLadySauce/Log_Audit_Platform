<template>
  <div class="alert-management-index">
    <PageHeader
      title="告警管理"
      description="分部IT基础设施告警规则配置和记录查询"
    />

    <!-- 功能模块导航 -->
    <a-row :gutter="24">
      <a-col :span="12">
        <a-card 
          hoverable 
          class="module-card"
          @click="goToRuleManagement"
        >
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
        <a-card 
          hoverable 
          class="module-card"
          @click="goToRecordQuery"
        >
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
    <a-row :gutter="24" style="margin-top: 24px;">
      <a-col :span="6">
        <StatCard
          :icon="IconSettings"
          icon-bg-color="#1890ff"
          :value="45"
          label="配置规则"
          subtitle="已配置告警规则"
        />
      </a-col>
      <a-col :span="6">
        <StatCard
          :icon="IconExclamation"
          icon-bg-color="#faad14"
          :value="4226"
          label="活跃告警"
          subtitle="待处理告警"
        />
      </a-col>
      <a-col :span="6">
        <StatCard
          :icon="IconCheck"
          icon-bg-color="#52c41a"
          :value="1650"
          label="已处理"
          subtitle="历史处理总数"
        />
      </a-col>
      <a-col :span="6">
        <StatCard
          :icon="IconEye"
          icon-bg-color="#722ed1"
          :value="10"
          label="监控设备"
          subtitle="分部监控设备"
        />
      </a-col>
    </a-row>

    <!-- 最近告警快览 -->
    <a-card title="最近告警" style="margin-top: 24px;" :bordered="false">
      <a-list :data="recentAlerts" :max-height="300">
        <template #item="{ item }">
          <a-list-item :key="item.id">
            <a-list-item-meta>
              <template #avatar>
                <a-tag :color="getLevelColor(item.level)" size="small">
                  {{ getLevelText(item.level) }}
                </a-tag>
              </template>
              <template #title>{{ item.source }}</template>
              <template #description>{{ item.message }}</template>
            </a-list-item-meta>
            <template #actions>
              <span class="time-text">{{ item.time }}</span>
            </template>
          </a-list-item>
        </template>
      </a-list>
    </a-card>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import PageHeader from '@/components/PageHeader.vue'
import StatCard from '@/components/StatCard.vue'
import {
  IconSettings,
  IconInfoCircle,
  IconArrowRight,
  IconExclamation,
  IconCheck,
  IconEye
} from '@arco-design/web-vue/es/icon'

const router = useRouter()

// 最近告警数据
const recentAlerts = ref([
  {
    id: 1,
    level: 'warning',
    source: '分部K8S工作节点1',
    message: '磁盘使用率达到85%，建议清理日志文件',
    time: '2024-01-15 10:45:22'
  },
  {
    id: 2,
    level: 'warning',
    source: '分部彩光交换机',
    message: '端口 Gi0/1 利用率达到90%，可能出现网络拥塞',
    time: '2024-01-15 10:38:45'
  },
  {
    id: 3,
    level: 'info',
    source: '分部防火墙',
    message: 'VPN隧道连接数增长至25个，接近预警阈值',
    time: '2024-01-15 10:32:33'
  },
  {
    id: 4,
    level: 'warning',
    source: '分部K8S控制节点1',
    message: 'etcd集群延迟超过100ms，可能影响集群响应',
    time: '2024-01-15 10:28:21'
  }
])

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