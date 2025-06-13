<template>
  <div class="ai-analysis-page">
    <PageHeader
      title="AI智能分析"
      description="基于人工智能的日志分析和异常检测"
    >
      <template #extra>
        <a-space>
          <a-button @click="refreshAnalysis" :loading="analyzing">
            <template #icon>
              <icon-refresh />
            </template>
            刷新
          </a-button>
          <a-button type="primary" @click="startAnalysis" :loading="analyzing">
            <template #icon>
              <icon-robot />
            </template>
            开始分析
          </a-button>
        </a-space>
      </template>
    </PageHeader>

    <!-- AI分析统计 -->
    <a-row :gutter="[24, 24]" class="stats-row">
      <a-col :xs="24" :sm="12" :lg="6">
        <EnhancedStatCard
          :icon="IconRobot"
          icon-bg-color="linear-gradient(135deg, #667eea 0%, #764ba2 100%)"
          :value="intelligenceScore"
          label="智能得分"
          subtitle="系统健康度"
          :trend="{ type: 'increase', value: '+5.2%' }"
          :show-progress="true"
          :progress-percent="89"
          progress-color="#667eea"
          progress-text="AI置信度 89%"
        />
      </a-col>
      <a-col :xs="24" :sm="12" :lg="6">
        <EnhancedStatCard
          :icon="IconBug"
          icon-bg-color="linear-gradient(135deg, #f093fb 0%, #f5576c 100%)"
          :value="anomalyCount"
          label="异常检测"
          subtitle="发现异常"
          :trend="{ type: 'decrease', value: '-2' }"
          :show-progress="true"
          :progress-percent="25"
          progress-color="#f5576c"
          progress-text="风险等级 低"
        />
      </a-col>
      <a-col :xs="24" :sm="12" :lg="6">
        <EnhancedStatCard
          :icon="IconEye"
          icon-bg-color="linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)"
          :value="patternCount"
          label="模式识别"
          subtitle="行为模式"
          :trend="{ type: 'increase', value: '+12' }"
          :show-progress="true"
          :progress-percent="78"
          progress-color="#00f2fe"
          progress-text="识别准确率 78%"
        />
      </a-col>
      <a-col :xs="24" :sm="12" :lg="6">
        <EnhancedStatCard
          :icon="IconExclamation"
          icon-bg-color="linear-gradient(135deg, #fa709a 0%, #fee140 100%)"
          :value="predictiveAlerts"
          label="预测告警"
          subtitle="潜在风险"
          :trend="{ type: 'stable', value: '稳定' }"
          :show-progress="true"
          :progress-percent="32"
          progress-color="#fa709a"
          progress-text="预警级别 中"
        />
      </a-col>
    </a-row>

    <!-- AI分析图表 -->
    <a-row :gutter="[24, 24]" class="charts-row">
      <a-col :xs="24" :lg="16">
        <a-card title="AI异常检测趋势" :bordered="false" class="chart-card">
          <template #extra>
            <a-space>
              <a-select v-model:value="detectionModel" size="small" style="width: 120px">
                <a-option value="lstm">LSTM模型</a-option>
                <a-option value="isolation">孤立森林</a-option>
                <a-option value="autoencoder">自编码器</a-option>
              </a-select>
              <a-radio-group v-model:value="timeRange" type="button" size="small">
                <a-radio-button value="1h">1小时</a-radio-button>
                <a-radio-button value="6h">6小时</a-radio-button>
                <a-radio-button value="24h">24小时</a-radio-button>
              </a-radio-group>
            </a-space>
          </template>
          <DashboardChart
            type="line"
            :data="anomalyTrendData"
            height="350px"
            :smooth="true"
            :colors="['#f5222d', '#faad14', '#52c41a']"
          />
        </a-card>
      </a-col>
      <a-col :xs="24" :lg="8">
        <a-card title="异常类型分布" :bordered="false" class="chart-card">
          <DashboardChart
            type="pie"
            :data="anomalyTypeData"
            height="350px"
            :colors="['#f5222d', '#faad14', '#1890ff', '#722ed1', '#13c2c2']"
          />
        </a-card>
      </a-col>
    </a-row>

    <!-- 高级分析图表 -->
    <a-row :gutter="[24, 24]" class="charts-row">
      <a-col :xs="24" :lg="8">
        <a-card title="系统健康度评估" :bordered="false" class="chart-card">
          <DashboardChart
            type="gauge"
            :data="[{ value: systemHealth }]"
            height="300px"
            title="综合健康度"
          />
        </a-card>
      </a-col>
      <a-col :xs="24" :lg="8">
        <a-card title="AI模型性能对比" :bordered="false" class="chart-card">
          <DashboardChart
            type="bar"
            :data="modelPerformanceData"
            height="300px"
            :colors="['#1890ff', '#52c41a', '#faad14']"
          />
        </a-card>
      </a-col>
      <a-col :xs="24" :lg="8">
        <a-card title="威胁情报雷达" :bordered="false" class="chart-card">
          <DashboardChart
            type="radar"
            :data="threatIntelData"
            height="300px"
            :colors="['#f5222d', '#faad14']"
          />
        </a-card>
      </a-col>
    </a-row>

    <!-- AI分析结果和建议 -->
    <a-row :gutter="[24, 24]" class="analysis-row">
      <a-col :xs="24" :lg="12">
        <a-card title="实时异常检测" :bordered="false" class="analysis-card">
          <template #extra>
            <a-badge :count="anomalies.length" :number-style="{ backgroundColor: '#f5222d' }">
              <a-button size="small" type="text">
                <template #icon>
                  <icon-eye />
                </template>
                查看全部
              </a-button>
            </a-badge>
          </template>
          <div class="analysis-content">
            <div 
              class="analysis-item" 
              v-for="(item, index) in anomalies" 
              :key="item.id"
              :style="{ animationDelay: `${index * 0.1}s` }"
            >
              <div class="item-header">
                <div class="severity-indicator" :class="item.severity">
                  <component :is="getSeverityIcon(item.severity)" />
                </div>
                <div class="item-info">
                  <div class="item-title">{{ item.title }}</div>
                  <div class="item-meta">
                    <a-tag :color="getSeverityColor(item.severity)" size="small">
                      {{ getSeverityText(item.severity) }}
                    </a-tag>
                    <span class="confidence">置信度: {{ item.confidence }}%</span>
                    <span class="time">{{ item.time }}</span>
                  </div>
                </div>
              </div>
              <div class="item-description">{{ item.description }}</div>
              <div class="item-actions">
                <a-space>
                  <a-button size="mini" type="text" @click="viewAnomalyDetail(item)">
                    详情
                  </a-button>
                  <a-button size="mini" type="text" @click="ignoreAnomaly(item)">
                    忽略
                  </a-button>
                  <a-button size="mini" type="text" @click="createAlert(item)">
                    创建告警
                  </a-button>
                </a-space>
              </div>
            </div>
          </div>
        </a-card>
      </a-col>
      <a-col :xs="24" :lg="12">
        <a-card title="AI智能建议" :bordered="false" class="suggestions-card">
          <template #extra>
            <a-space>
              <a-button size="small" @click="generateSuggestions" :loading="generatingSuggestions">
                <template #icon>
                  <icon-robot />
                </template>
                重新生成
              </a-button>
            </a-space>
          </template>
          <div class="suggestions">
            <div 
              class="suggestion-item" 
              v-for="(suggestion, index) in suggestions" 
              :key="suggestion.id"
              :style="{ animationDelay: `${index * 0.15}s` }"
            >
              <div class="suggestion-icon">
                <icon-bulb />
              </div>
              <div class="suggestion-content">
                <div class="suggestion-title">{{ suggestion.title }}</div>
                <div class="suggestion-description">{{ suggestion.description }}</div>
                <div class="suggestion-meta">
                  <a-tag color="blue" size="small">{{ suggestion.category }}</a-tag>
                  <span class="priority">优先级: {{ suggestion.priority }}</span>
                </div>
              </div>
              <div class="suggestion-action">
                <a-space direction="vertical" size="mini">
                  <a-button type="outline" size="small" @click="applySuggestion(suggestion)">
                    应用建议
                  </a-button>
                  <a-button type="text" size="small" @click="viewSuggestionDetail(suggestion)">
                    查看详情
                  </a-button>
                </a-space>
              </div>
            </div>
          </div>
        </a-card>
      </a-col>
    </a-row>

    <!-- AI模型训练状态 -->
    <a-card title="AI模型训练状态" :bordered="false" class="model-status-card">
      <a-row :gutter="[24, 24]">
        <a-col :xs="24" :sm="8" v-for="model in modelStatus" :key="model.name">
          <div class="model-item">
            <div class="model-header">
              <div class="model-name">{{ model.name }}</div>
              <a-badge :status="model.status === 'training' ? 'processing' : 'success'" />
            </div>
            <div class="model-progress">
              <a-progress 
                :percent="model.progress" 
                :status="model.status === 'training' ? 'normal' : 'success'"
                :show-text="true"
              />
            </div>
            <div class="model-metrics">
              <div class="metric">
                <span class="metric-label">准确率:</span>
                <span class="metric-value">{{ model.accuracy }}%</span>
              </div>
              <div class="metric">
                <span class="metric-label">F1分数:</span>
                <span class="metric-value">{{ model.f1Score }}</span>
              </div>
            </div>
          </div>
        </a-col>
      </a-row>
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
  IconRobot,
  IconBug,
  IconEye,
  IconExclamation,
  IconBulb,
  IconCheck,
  IconClose
} from '@arco-design/web-vue/es/icon'

// 响应式数据
const analyzing = ref(false)
const generatingSuggestions = ref(false)
const detectionModel = ref('lstm')
const timeRange = ref('24h')

// 统计数据
const intelligenceScore = ref(89)
const anomalyCount = ref(12)
const patternCount = ref(156)
const predictiveAlerts = ref(8)
const systemHealth = ref(85)

// 异常趋势数据
const anomalyTrendData = ref([
  { name: '00:00', value: 2 },
  { name: '04:00', value: 1 },
  { name: '08:00', value: 5 },
  { name: '12:00', value: 8 },
  { name: '16:00', value: 12 },
  { name: '20:00', value: 6 },
  { name: '24:00', value: 3 }
])

// 异常类型数据
const anomalyTypeData = ref([
  { name: 'CPU异常', value: 35 },
  { name: '内存泄漏', value: 25 },
  { name: '网络异常', value: 20 },
  { name: '磁盘IO', value: 12 },
  { name: '其他', value: 8 }
])

// 模型性能数据
const modelPerformanceData = ref([
  { name: 'LSTM', value: 94.2 },
  { name: '孤立森林', value: 87.6 },
  { name: '自编码器', value: 91.3 },
  { name: 'SVM', value: 83.8 },
  { name: '随机森林', value: 89.1 }
])

// 威胁情报数据
const threatIntelData = ref([
  { name: '恶意IP', value: 85, max: 100 },
  { name: '异常端口', value: 72, max: 100 },
  { name: '可疑域名', value: 68, max: 100 },
  { name: '文件哈希', value: 91, max: 100 },
  { name: '行为模式', value: 79, max: 100 }
])

// 异常检测数据
const anomalies = ref([
  {
    id: 1,
    title: 'CPU使用率异常波动',
    description: '检测到服务器CPU使用率存在异常波动模式，可能存在资源竞争问题或恶意进程',
    severity: 'high',
    confidence: 95,
    time: '2024-01-15 10:30:00'
  },
  {
    id: 2,
    title: '网络流量异常',
    description: '发现异常的网络流量模式，流量突增且目标地址可疑，建议立即检查',
    severity: 'high',
    confidence: 87,
    time: '2024-01-15 10:25:00'
  },
  {
    id: 3,
    title: '数据库连接异常',
    description: '数据库连接数存在异常增长，可能影响系统性能，建议优化连接池配置',
    severity: 'medium',
    confidence: 92,
    time: '2024-01-15 10:20:00'
  },
  {
    id: 4,
    title: '内存使用异常',
    description: '检测到内存使用模式异常，可能存在内存泄漏风险',
    severity: 'medium',
    confidence: 78,
    time: '2024-01-15 10:15:00'
  }
])

// 智能建议数据
const suggestions = ref([
  {
    id: 1,
    title: '优化数据库连接池配置',
    description: '建议将数据库连接池大小调整为当前的1.5倍，并启用连接池监控',
    category: '性能优化',
    priority: '高'
  },
  {
    id: 2,
    title: '增强网络安全监控',
    description: '建议部署DPI深度包检测，加强对异常流量的实时监控和拦截',
    category: '安全加固',
    priority: '高'
  },
  {
    id: 3,
    title: '部署自动化运维',
    description: '建议引入自动化运维工具，提高系统响应速度和故障恢复能力',
    category: '运维优化',
    priority: '中'
  },
  {
    id: 4,
    title: '优化AI模型参数',
    description: '根据最新数据重新训练LSTM模型，提高异常检测准确率',
    category: 'AI优化',
    priority: '中'
  }
])

// AI模型状态
const modelStatus = ref([
  {
    name: 'LSTM异常检测',
    status: 'completed',
    progress: 100,
    accuracy: 94.2,
    f1Score: 0.91
  },
  {
    name: '孤立森林模型',
    status: 'training',
    progress: 75,
    accuracy: 87.6,
    f1Score: 0.84
  },
  {
    name: '自编码器模型',
    status: 'completed',
    progress: 100,
    accuracy: 91.3,
    f1Score: 0.88
  }
])

// 定时器
let dataUpdateTimer: NodeJS.Timeout | null = null

// 获取严重程度图标
const getSeverityIcon = (severity: string) => {
  switch (severity) {
    case 'high':
      return IconClose
    case 'medium':
      return IconExclamation
    case 'low':
      return IconCheck
    default:
      return IconExclamation
  }
}

// 获取严重程度颜色
const getSeverityColor = (severity: string) => {
  switch (severity) {
    case 'high':
      return 'red'
    case 'medium':
      return 'orange'
    case 'low':
      return 'green'
    default:
      return 'gray'
  }
}

// 获取严重程度文本
const getSeverityText = (severity: string) => {
  switch (severity) {
    case 'high':
      return '高风险'
    case 'medium':
      return '中风险'
    case 'low':
      return '低风险'
    default:
      return '未知'
  }
}

// 刷新分析
const refreshAnalysis = async () => {
  analyzing.value = true
  
  // 模拟AI分析过程
  await new Promise(resolve => setTimeout(resolve, 2000))
  
  // 更新数据
  intelligenceScore.value = Math.floor(Math.random() * 20) + 80
  anomalyCount.value = Math.floor(Math.random() * 10) + 5
  patternCount.value = Math.floor(Math.random() * 50) + 120
  systemHealth.value = Math.floor(Math.random() * 30) + 70
  
  analyzing.value = false
}

// 开始分析
const startAnalysis = async () => {
  analyzing.value = true
  
  // 模拟深度AI分析
  await new Promise(resolve => setTimeout(resolve, 3000))
  
  analyzing.value = false
}

// 生成建议
const generateSuggestions = async () => {
  generatingSuggestions.value = true
  await new Promise(resolve => setTimeout(resolve, 1500))
  generatingSuggestions.value = false
}

// 查看异常详情
const viewAnomalyDetail = (item: any) => {
  console.log('查看异常详情:', item)
}

// 忽略异常
const ignoreAnomaly = (item: any) => {
  console.log('忽略异常:', item)
}

// 创建告警
const createAlert = (item: any) => {
  console.log('创建告警:', item)
}

// 应用建议
const applySuggestion = (suggestion: any) => {
  console.log('应用建议:', suggestion)
}

// 查看建议详情
const viewSuggestionDetail = (suggestion: any) => {
  console.log('查看建议详情:', suggestion)
}

// 实时数据更新
const startDataUpdate = () => {
  dataUpdateTimer = setInterval(() => {
    // 模拟实时数据更新
    systemHealth.value = Math.floor(Math.random() * 30) + 70
    
    // 随机更新异常趋势数据
    const lastValue = anomalyTrendData.value[anomalyTrendData.value.length - 1].value
    const newValue = Math.max(0, lastValue + (Math.random() - 0.5) * 5)
    
    anomalyTrendData.value.shift()
    anomalyTrendData.value.push({
      name: new Date().toLocaleTimeString().slice(0, 5),
      value: Math.floor(newValue)
    })
  }, 8000)
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
.ai-analysis-page {
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

.analysis-row {
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

.analysis-card,
.suggestions-card {
  height: 100%;
}

.analysis-content {
  max-height: 500px;
  overflow-y: auto;
}

.analysis-item {
  padding: 16px;
  border: 1px solid #f0f0f0;
  border-radius: 8px;
  margin-bottom: 12px;
  background: #fafafa;
  transition: all 0.3s ease;
  animation: slideInUp 0.6s ease-out;
}

.analysis-item:hover {
  background: #ffffff;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.item-header {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  margin-bottom: 8px;
}

.severity-indicator {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 14px;
  flex-shrink: 0;
}

.severity-indicator.high {
  background: #f5222d;
}

.severity-indicator.medium {
  background: #faad14;
}

.severity-indicator.low {
  background: #52c41a;
}

.item-info {
  flex: 1;
}

.item-title {
  font-weight: 600;
  color: #262626;
  margin-bottom: 4px;
}

.item-meta {
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 12px;
  color: #8c8c8c;
}

.confidence {
  font-weight: 500;
}

.item-description {
  color: #595959;
  line-height: 1.5;
  margin-bottom: 12px;
}

.item-actions {
  display: flex;
  justify-content: flex-end;
}

.suggestions {
  max-height: 500px;
  overflow-y: auto;
}

.suggestion-item {
  display: flex;
  align-items: flex-start;
  gap: 16px;
  padding: 16px;
  border: 1px solid #f0f0f0;
  border-radius: 8px;
  margin-bottom: 12px;
  background: #fafafa;
  transition: all 0.3s ease;
  animation: slideInUp 0.6s ease-out;
}

.suggestion-item:hover {
  background: #ffffff;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.suggestion-icon {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: linear-gradient(135deg, #faad14, #fee140);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 18px;
  flex-shrink: 0;
}

.suggestion-content {
  flex: 1;
}

.suggestion-title {
  font-weight: 600;
  color: #262626;
  margin-bottom: 8px;
}

.suggestion-description {
  color: #595959;
  line-height: 1.5;
  margin-bottom: 8px;
}

.suggestion-meta {
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 12px;
  color: #8c8c8c;
}

.priority {
  font-weight: 500;
}

.suggestion-action {
  flex-shrink: 0;
}

.model-status-card {
  margin-bottom: 24px;
}

.model-item {
  padding: 20px;
  border: 1px solid #f0f0f0;
  border-radius: 12px;
  background: #fafafa;
  transition: all 0.3s ease;
}

.model-item:hover {
  background: #ffffff;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.model-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.model-name {
  font-weight: 600;
  color: #262626;
}

.model-progress {
  margin-bottom: 16px;
}

.model-metrics {
  display: flex;
  justify-content: space-between;
}

.metric {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
}

.metric-label {
  font-size: 12px;
  color: #8c8c8c;
}

.metric-value {
  font-weight: 600;
  color: #262626;
}

@keyframes slideInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* 响应式设计 */
@media (max-width: 768px) {
  .suggestion-item {
    flex-direction: column;
    gap: 12px;
  }
  
  .suggestion-action {
    align-self: stretch;
  }
  
  .model-metrics {
    flex-direction: column;
    gap: 12px;
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
</style> 