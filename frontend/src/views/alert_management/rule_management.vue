<template>
  <div class="alert-rule-page">
    <PageHeader
      title="告警规则管理"
      description="配置和管理分部IT基础设施告警规则"
    >
      <template #extra>
        <a-space>
          <a-button @click="refreshRules" :loading="refreshing">
            <template #icon>
              <icon-refresh />
            </template>
            刷新
          </a-button>
          <a-button type="primary" @click="showAddRule">
            <template #icon>
              <icon-plus />
            </template>
            添加规则
          </a-button>
          <a-button @click="exportRules">
            <template #icon>
              <icon-download />
            </template>
            导出配置
          </a-button>
        </a-space>
      </template>
    </PageHeader>

    <!-- 规则统计 -->
    <a-row :gutter="24" class="stats-row">
      <a-col :span="6">
        <StatCard
          :icon="IconSettings"
          icon-bg-color="#1890ff"
          :value="ruleStats.total"
          label="总规则数"
          subtitle="全部配置规则"
        />
      </a-col>
      <a-col :span="6">
        <StatCard
          :icon="IconCheck"
          icon-bg-color="#52c41a"
          :value="ruleStats.enabled"
          label="启用规则"
          subtitle="正在监控中"
        />
      </a-col>
      <a-col :span="6">
        <StatCard
          :icon="IconExclamation"
          icon-bg-color="#faad14"
          :value="ruleStats.triggered"
          label="触发规则"
          subtitle="今日触发次数"
        />
      </a-col>
      <a-col :span="6">
        <StatCard
          :icon="IconClose"
          icon-bg-color="#f5222d"
          :value="ruleStats.disabled"
          label="禁用规则"
          subtitle="已停用规则"
        />
      </a-col>
    </a-row>



    <!-- 规则搜索和筛选 -->
    <a-card :bordered="false" class="search-card">
      <a-row :gutter="16">
        <a-col :span="6">
          <a-input
            v-model:value="searchKeyword"
            placeholder="搜索规则名称..."
            allow-clear
            @change="handleSearch"
          >
            <template #prefix>
              <icon-search />
            </template>
          </a-input>
        </a-col>
        <a-col :span="4">
          <a-select v-model:value="selectedCategory" placeholder="规则类型" allow-clear @change="handleSearch">
            <a-option value="resource">资源监控</a-option>
            <a-option value="network">网络监控</a-option>
            <a-option value="security">安全监控</a-option>
            <a-option value="performance">性能监控</a-option>
          </a-select>
        </a-col>
        <a-col :span="3">
          <a-select v-model:value="selectedSeverity" placeholder="告警级别" allow-clear @change="handleSearch">
            <a-option value="critical">严重</a-option>
            <a-option value="warning">警告</a-option>
            <a-option value="info">信息</a-option>
          </a-select>
        </a-col>
        <a-col :span="3">
          <a-select v-model:value="selectedStatus" placeholder="状态" allow-clear @change="handleSearch">
            <a-option value="enabled">启用</a-option>
            <a-option value="disabled">禁用</a-option>
          </a-select>
        </a-col>
        <a-col :span="4">
          <a-select v-model:value="selectedTarget" placeholder="监控目标" allow-clear @change="handleSearch">
            <a-option value="分部防火墙">分部防火墙</a-option>
            <a-option value="分部K8S控制节点1">分部K8S控制节点1</a-option>
            <a-option value="分部彩光交换机">分部彩光交换机</a-option>
          </a-select>
        </a-col>
        <a-col :span="4">
          <a-space>
            <a-button type="primary" @click="handleSearch">搜索</a-button>
            <a-button @click="clearSearch">清空</a-button>
          </a-space>
        </a-col>
      </a-row>
    </a-card>

    <!-- 规则列表 -->
    <a-card :bordered="false">
      <template #title>
        <a-space>
          <span>告警规则配置</span>
          <a-tag color="blue">{{ filteredRuleData.length }}条规则</a-tag>
          <a-tag color="green">{{ enabledRules }}条启用</a-tag>
        </a-space>
      </template>
      
      <template #extra>
        <a-space>
          <a-button size="small" @click="enableAllRules">
            <template #icon>
              <icon-check />
            </template>
            批量启用
          </a-button>
          <a-button size="small" @click="disableAllRules">
            <template #icon>
              <icon-close />
            </template>
            批量禁用
          </a-button>
        </a-space>
      </template>

      <a-table
        :columns="ruleColumns"
        :data="filteredRuleData"
        :pagination="{ pageSize: 15, showTotal: true }"
        :scroll="{ x: '100%' }"
        :loading="tableLoading"
        row-key="key"
      >
        <template #category="{ record }">
          <a-tag :color="getCategoryColor(record.category)" size="small">
            <template #icon>
              <component :is="getCategoryIcon(record.category)" />
            </template>
            {{ getCategoryText(record.category) }}
          </a-tag>
        </template>

        <template #severity="{ record }">
          <a-tag :color="getSeverityColor(record.severity)" size="small">
            {{ getSeverityText(record.severity) }}
          </a-tag>
        </template>

        <template #status="{ record }">
          <a-switch
            v-model:checked="record.enabled"
            :checked-text="'启用'"
            :unchecked-text="'禁用'"
            @change="toggleRuleStatus(record)"
          />
        </template>

        <template #condition="{ record }">
          <div class="rule-condition">
            <a-tooltip :content="record.condition" placement="topLeft">
              {{ record.condition }}
            </a-tooltip>
          </div>
        </template>

        <template #triggerCount="{ record }">
          <span class="trigger-count" :class="{ 'high-trigger': record.triggerCount > 10 }">
            {{ record.triggerCount }}次
          </span>
        </template>

        <template #actions="{ record }">
          <a-space>
            <a-button type="text" size="small" @click="editRule(record)">
              编辑
            </a-button>
            <a-button type="text" size="small" @click="copyRule(record)">
              复制
            </a-button>
            <a-button type="text" size="small" @click="testRule(record)">
              测试
            </a-button>
            <a-button type="text" size="small" status="danger" @click="deleteRule(record)">
              删除
            </a-button>
          </a-space>
        </template>
      </a-table>
    </a-card>

    <!-- 添加/编辑规则模态框 -->
    <a-modal
      v-model:visible="ruleModalVisible"
      :title="editingRule ? '编辑告警规则' : '添加告警规则'"
      width="800px"
      @ok="saveRule"
      @cancel="cancelRule"
    >
      <a-form :model="ruleForm" layout="vertical">
        <a-row :gutter="16">
          <a-col :span="12">
            <a-form-item label="规则名称" required>
              <a-input v-model:value="ruleForm.name" placeholder="请输入规则名称" />
            </a-form-item>
          </a-col>
          <a-col :span="12">
            <a-form-item label="规则类型" required>
              <a-select v-model:value="ruleForm.category" placeholder="请选择规则类型">
                <a-option value="resource">资源监控</a-option>
                <a-option value="network">网络监控</a-option>
                <a-option value="security">安全监控</a-option>
                <a-option value="performance">性能监控</a-option>
              </a-select>
            </a-form-item>
          </a-col>
        </a-row>
        
        <a-row :gutter="16">
          <a-col :span="12">
            <a-form-item label="告警级别" required>
              <a-select v-model:value="ruleForm.severity" placeholder="请选择告警级别">
                <a-option value="critical">严重</a-option>
                <a-option value="warning">警告</a-option>
                <a-option value="info">信息</a-option>
              </a-select>
            </a-form-item>
          </a-col>
          <a-col :span="12">
            <a-form-item label="监控目标" required>
              <a-select v-model:value="ruleForm.target" placeholder="请选择监控目标">
                <a-option value="分部防火墙">分部防火墙</a-option>
                <a-option value="分部K8S控制节点1">分部K8S控制节点1</a-option>
                <a-option value="分部K8S工作节点1">分部K8S工作节点1</a-option>
                <a-option value="分部彩光交换机">分部彩光交换机</a-option>
                <a-option value="分部无线控制器">分部无线控制器</a-option>
              </a-select>
            </a-form-item>
          </a-col>
        </a-row>

        <a-form-item label="触发条件" required>
          <a-textarea
            v-model:value="ruleForm.condition"
            placeholder="请输入触发条件，如：CPU使用率 > 80%"
            :rows="3"
          />
        </a-form-item>

        <a-form-item label="规则描述">
          <a-textarea
            v-model:value="ruleForm.description"
            placeholder="请输入规则描述"
            :rows="2"
          />
        </a-form-item>

        <a-row :gutter="16">
          <a-col :span="12">
            <a-form-item label="检查间隔">
              <a-select v-model:value="ruleForm.interval" placeholder="检查间隔">
                <a-option value="1分钟">1分钟</a-option>
                <a-option value="5分钟">5分钟</a-option>
                <a-option value="10分钟">10分钟</a-option>
                <a-option value="30分钟">30分钟</a-option>
              </a-select>
            </a-form-item>
          </a-col>
          <a-col :span="12">
            <a-form-item label="规则状态">
              <a-switch
                v-model:checked="ruleForm.enabled"
                checked-text="启用"
                unchecked-text="禁用"
              />
            </a-form-item>
          </a-col>
        </a-row>
      </a-form>
    </a-modal>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { Message } from '@arco-design/web-vue'
import PageHeader from '@/components/PageHeader.vue'
import StatCard from '@/components/StatCard.vue'
import {
  IconRefresh,
  IconPlus,
  IconDownload,
  IconSearch,
  IconCheck,
  IconExclamation,
  IconSettings,
  IconClose,
  IconDesktop,
  IconWifi,
  IconLock,
  IconCloud
} from '@arco-design/web-vue/es/icon'

// 响应式数据
const refreshing = ref(false)
const tableLoading = ref(false)
const ruleModalVisible = ref(false)
const editingRule = ref(false)
const searchKeyword = ref('')
const selectedCategory = ref('')
const selectedSeverity = ref('')
const selectedStatus = ref('')
const selectedTarget = ref('')

// 规则统计数据
const ruleStats = ref({
  total: 45,
  enabled: 45,
  triggered: 127,
  disabled: 0
})



// 规则表单数据
const ruleForm = ref({
  key: '',
  name: '',
  category: '',
  severity: '',
  target: '',
  condition: '',
  description: '',
  interval: '5分钟',
  enabled: true,
  triggerCount: 0,
  lastTrigger: '-'
})

// 规则数据 - 45条规则数据
const ruleData = ref([
  // 安全监控规则 (8条)
  {
    key: '1',
    name: '系统登录失败告警',
    category: 'security',
    severity: 'warning',
    target: '分部防火墙',
    condition: 'Failed password > 5次/10分钟',
    description: '监控系统登录失败次数',
    interval: '5分钟',
    triggerCount: 12,
    enabled: true,
    lastTrigger: '2024-01-15 10:30:00'
  },
  {
    key: '2',
    name: '系统错误告警',
    category: 'security',
    severity: 'error',
    target: '分部K8S控制节点1',
    condition: 'error|critical|panic',
    description: '监控系统关键错误日志',
    interval: '1分钟',
    triggerCount: 3,
    enabled: true,
    lastTrigger: '2024-01-15 10:25:00'
  },
  {
    key: '3',
    name: '防火墙入侵检测',
    category: 'security',
    severity: 'critical',
    target: '分部防火墙',
    condition: '入侵尝试 > 3次/分钟',
    description: '检测恶意入侵尝试',
    interval: '1分钟',
    triggerCount: 0,
    enabled: true,
    lastTrigger: '-'
  },
  {
    key: '4',
    name: 'SSH暴力破解检测',
    category: 'security',
    severity: 'warning',
    target: '分部K8S控制节点1',
    condition: 'SSH失败 > 10次/小时',
    description: '检测SSH暴力破解攻击',
    interval: '10分钟',
    triggerCount: 0,
    enabled: true,
    lastTrigger: '-'
  },
  {
    key: '5',
    name: '异常访问模式检测',
    category: 'security',
    severity: 'info',
    target: '分部防火墙',
    condition: '异常流量模式检测',
    description: '检测异常网络访问模式',
    interval: '15分钟',
    triggerCount: 5,
    enabled: true,
    lastTrigger: '2024-01-15 09:45:00'
  },
  {
    key: '6',
    name: '端口扫描检测',
    category: 'security',
    severity: 'warning',
    target: '分部防火墙',
    condition: '端口扫描 > 100次/分钟',
    description: '检测恶意端口扫描行为',
    interval: '5分钟',
    triggerCount: 2,
    enabled: true,
    lastTrigger: '2024-01-15 09:30:00'
  },
  {
    key: '7',
    name: '恶意IP访问',
    category: 'security',
    severity: 'critical',
    target: '分部防火墙',
    condition: '黑名单IP访问检测',
    description: '检测已知恶意IP的访问尝试',
    interval: '1分钟',
    triggerCount: 0,
    enabled: true,
    lastTrigger: '-'
  },
  {
    key: '8',
    name: '权限提升检测',
    category: 'security',
    severity: 'warning',
    target: '分部K8S控制节点1',
    condition: 'sudo使用异常检测',
    description: '检测异常的权限提升操作',
    interval: '5分钟',
    triggerCount: 1,
    enabled: true,
    lastTrigger: '2024-01-15 08:15:00'
  },

  // 资源监控规则 (18条)
  {
    key: '9',
    name: '磁盘空间不足告警',
    category: 'resource',
    severity: 'critical',
    target: '分部K8S工作节点1',
    condition: 'disk space|no space left > 1次/60分钟',
    description: '监控磁盘空间不足警告',
    interval: '10分钟',
    triggerCount: 8,
    enabled: true,
    lastTrigger: '2024-01-15 10:20:00'
  },
  {
    key: '10',
    name: '磁盘使用率监控',
    category: 'resource',
    severity: 'warning',
    target: '分部K8S控制节点1',
    condition: '磁盘使用率 > 85%',
    description: '监控磁盘使用率过高',
    interval: '10分钟',
    triggerCount: 15,
    enabled: true,
    lastTrigger: '2024-01-15 10:00:00'
  },
  {
    key: '11',
    name: '磁盘I/O监控',
    category: 'resource',
    severity: 'info',
    target: '分部K8S工作节点1',
    condition: '磁盘I/O > 90%',
    description: '监控磁盘I/O使用率',
    interval: '5分钟',
    triggerCount: 3,
    enabled: true,
    lastTrigger: '2024-01-15 09:45:00'
  },
  {
    key: '12',
    name: '文件系统只读检测',
    category: 'resource',
    severity: 'critical',
    target: '分部K8S控制节点1',
    condition: '文件系统只读错误',
    description: '检测文件系统变为只读状态',
    interval: '5分钟',
    triggerCount: 0,
    enabled: true,
    lastTrigger: '-'
  },
  {
    key: '13',
    name: 'inode使用率监控',
    category: 'resource',
    severity: 'warning',
    target: '分部K8S工作节点1',
    condition: 'inode使用率 > 90%',
    description: '监控文件系统inode使用率',
    interval: '15分钟',
    triggerCount: 0,
    enabled: true,
    lastTrigger: '-'
  },
  {
    key: '14',
    name: '交换空间使用监控',
    category: 'resource',
    severity: 'warning',
    target: '分部K8S控制节点1',
    condition: 'Swap使用率 > 50%',
    description: '监控交换空间使用情况',
    interval: '10分钟',
    triggerCount: 2,
    enabled: true,
    lastTrigger: '2024-01-15 08:30:00'
  },
  {
    key: '15',
    name: '文件描述符监控',
    category: 'resource',
    severity: 'warning',
    target: '分部K8S控制节点1',
    condition: '文件描述符使用率 > 80%',
    description: '监控系统文件描述符使用情况',
    interval: '10分钟',
    triggerCount: 0,
    enabled: true,
    lastTrigger: '-'
  },
  {
    key: '16',
    name: '进程数量监控',
    category: 'resource',
    severity: 'info',
    target: '分部K8S控制节点1',
    condition: '进程数量 > 500',
    description: '监控系统进程数量',
    interval: '15分钟',
    triggerCount: 10,
    enabled: true,
    lastTrigger: '2024-01-15 09:30:00'
  },
  {
    key: '17',
    name: '僵尸进程检测',
    category: 'resource',
    severity: 'warning',
    target: '分部K8S控制节点1',
    condition: '僵尸进程 > 5个',
    description: '检测系统中的僵尸进程',
    interval: '10分钟',
    triggerCount: 0,
    enabled: true,
    lastTrigger: '-'
  },
  {
    key: '18',
    name: '负载平均值监控',
    category: 'resource',
    severity: 'warning',
    target: '分部K8S控制节点1',
    condition: '15分钟负载 > 4.0',
    description: '监控系统负载平均值',
    interval: '5分钟',
    triggerCount: 8,
    enabled: true,
    lastTrigger: '2024-01-15 09:15:00'
  },
  {
    key: '19',
    name: '内存碎片监控',
    category: 'resource',
    severity: 'info',
    target: '分部K8S工作节点1',
    condition: '内存碎片率 > 30%',
    description: '监控内存碎片化程度',
    interval: '30分钟',
    triggerCount: 2,
    enabled: true,
    lastTrigger: '2024-01-15 08:00:00'
  },
  {
    key: '20',
    name: '缓存命中率监控',
    category: 'resource',
    severity: 'info',
    target: '分部K8S控制节点1',
    condition: '缓存命中率 < 70%',
    description: '监控系统缓存效率',
    interval: '20分钟',
    triggerCount: 1,
    enabled: true,
    lastTrigger: '2024-01-15 07:40:00'
  },
  {
    key: '21',
    name: '磁盘错误监控',
    category: 'resource',
    severity: 'critical',
    target: '分部K8S工作节点1',
    condition: '磁盘硬件错误检测',
    description: '检测磁盘硬件故障',
    interval: '10分钟',
    triggerCount: 0,
    enabled: true,
    lastTrigger: '-'
  },
  {
    key: '22',
    name: '温度监控',
    category: 'resource',
    severity: 'warning',
    target: '分部K8S控制节点1',
    condition: 'CPU温度 > 70°C',
    description: '监控硬件温度',
    interval: '15分钟',
    triggerCount: 0,
    enabled: true,
    lastTrigger: '-'
  },
  {
    key: '23',
    name: '电源状态监控',
    category: 'resource',
    severity: 'critical',
    target: '分部K8S控制节点1',
    condition: '电源故障检测',
    description: '监控服务器电源状态',
    interval: '5分钟',
    triggerCount: 0,
    enabled: true,
    lastTrigger: '-'
  },
  {
    key: '24',
    name: '网卡流量监控',
    category: 'resource',
    severity: 'info',
    target: '分部K8S控制节点1',
    condition: '网卡流量 > 800Mbps',
    description: '监控网络接口流量',
    interval: '5分钟',
    triggerCount: 12,
    enabled: true,
    lastTrigger: '2024-01-15 10:10:00'
  },
  {
    key: '25',
    name: '内存泄漏检测',
    category: 'resource',
    severity: 'warning',
    target: '分部K8S工作节点1',
    condition: '内存使用持续增长检测',
    description: '检测应用程序内存泄漏',
    interval: '30分钟',
    triggerCount: 1,
    enabled: true,
    lastTrigger: '2024-01-15 07:30:00'
  },
  {
    key: '26',
    name: '存储阵列监控',
    category: 'resource',
    severity: 'critical',
    target: '分部K8S控制节点1',
    condition: 'RAID状态异常检测',
    description: '监控存储阵列健康状态',
    interval: '10分钟',
    triggerCount: 0,
    enabled: true,
    lastTrigger: '-'
  },

  // 性能监控规则 (7条)
  {
    key: '27',
    name: 'CPU使用率监控',
    category: 'performance',
    severity: 'warning',
    target: '分部K8S控制节点1',
    condition: 'CPU使用率 > 80%',
    description: '监控CPU使用率过高',
    interval: '5分钟',
    triggerCount: 25,
    enabled: true,
    lastTrigger: '2024-01-15 10:15:00'
  },
  {
    key: '28',
    name: '内存使用率监控',
    category: 'performance',
    severity: 'warning',
    target: '分部K8S工作节点1',
    condition: '内存使用率 > 75%',
    description: '监控内存使用率过高',
    interval: '5分钟',
    triggerCount: 18,
    enabled: true,
    lastTrigger: '2024-01-15 10:10:00'
  },
  {
    key: '29',
    name: '响应时间监控',
    category: 'performance',
    severity: 'warning',
    target: '分部K8S控制节点1',
    condition: 'API响应时间 > 2秒',
    description: '监控服务响应时间',
    interval: '5分钟',
    triggerCount: 5,
    enabled: true,
    lastTrigger: '2024-01-15 09:50:00'
  },
  {
    key: '30',
    name: '数据库性能监控',
    category: 'performance',
    severity: 'info',
    target: '分部K8S控制节点1',
    condition: '数据库查询时间 > 5秒',
    description: '监控数据库查询性能',
    interval: '10分钟',
    triggerCount: 3,
    enabled: true,
    lastTrigger: '2024-01-15 09:20:00'
  },
  {
    key: '31',
    name: '吞吐量监控',
    category: 'performance',
    severity: 'info',
    target: '分部K8S控制节点1',
    condition: '请求吞吐量 < 100/秒',
    description: '监控系统处理能力',
    interval: '10分钟',
    triggerCount: 2,
    enabled: true,
    lastTrigger: '2024-01-15 08:45:00'
  },
  {
    key: '32',
    name: '并发连接监控',
    category: 'performance',
    severity: 'warning',
    target: '分部K8S控制节点1',
    condition: '并发连接数 > 1000',
    description: '监控系统并发连接数',
    interval: '5分钟',
    triggerCount: 8,
    enabled: true,
    lastTrigger: '2024-01-15 09:35:00'
  },
  {
    key: '33',
    name: '服务可用性监控',
    category: 'performance',
    severity: 'critical',
    target: '分部K8S控制节点1',
    condition: '服务可用性 < 99%',
    description: '监控服务可用性指标',
    interval: '5分钟',
    triggerCount: 0,
    enabled: true,
    lastTrigger: '-'
  },

  // 网络监控规则 (12条)
  {
    key: '34',
    name: '网络端口利用率告警',
    category: 'network',
    severity: 'warning',
    target: '分部彩光交换机',
    condition: '端口利用率 > 85%',
    description: '监控交换机端口利用率',
    interval: '10分钟',
    triggerCount: 6,
    enabled: true,
    lastTrigger: '2024-01-15 10:05:00'
  },
  {
    key: '35',
    name: '无线客户端连接数监控',
    category: 'network',
    severity: 'info',
    target: '分部AP',
    condition: '无线客户端 > 30个',
    description: '监控AP连接数',
    interval: '15分钟',
    triggerCount: 2,
    enabled: true,
    lastTrigger: '2024-01-15 09:50:00'
  },
  {
    key: '36',
    name: '网络延迟监控',
    category: 'network',
    severity: 'warning',
    target: '分部彩光交换机',
    condition: '网络延迟 > 100ms',
    description: '监控网络延迟情况',
    interval: '5分钟',
    triggerCount: 4,
    enabled: true,
    lastTrigger: '2024-01-15 09:25:00'
  },
  {
    key: '37',
    name: '丢包率监控',
    category: 'network',
    severity: 'warning',
    target: '分部集群接入交换机',
    condition: '丢包率 > 1%',
    description: '监控网络丢包情况',
    interval: '5分钟',
    triggerCount: 1,
    enabled: true,
    lastTrigger: '2024-01-15 08:40:00'
  },
  {
    key: '38',
    name: 'VLAN配置监控',
    category: 'network',
    severity: 'info',
    target: '分部集群接入交换机',
    condition: 'VLAN配置变更检测',
    description: '监控VLAN配置变更',
    interval: '30分钟',
    triggerCount: 3,
    enabled: true,
    lastTrigger: '2024-01-15 08:00:00'
  },
  {
    key: '39',
    name: '端口状态监控',
    category: 'network',
    severity: 'warning',
    target: '分部用户接入交换机',
    condition: '端口状态变更检测',
    description: '监控交换机端口状态',
    interval: '5分钟',
    triggerCount: 8,
    enabled: true,
    lastTrigger: '2024-01-15 09:40:00'
  },
  {
    key: '40',
    name: '生成树协议监控',
    category: 'network',
    severity: 'warning',
    target: '分部彩光交换机',
    condition: 'STP拓扑变更检测',
    description: '监控生成树协议状态',
    interval: '15分钟',
    triggerCount: 0,
    enabled: true,
    lastTrigger: '-'
  },
  {
    key: '41',
    name: 'DHCP池使用监控',
    category: 'network',
    severity: 'info',
    target: '分部防火墙',
    condition: 'DHCP池使用率 > 80%',
    description: '监控DHCP地址池使用情况',
    interval: '20分钟',
    triggerCount: 2,
    enabled: true,
    lastTrigger: '2024-01-15 08:20:00'
  },
  {
    key: '42',
    name: 'VPN连接监控',
    category: 'network',
    severity: 'info',
    target: '分部防火墙',
    condition: 'VPN连接数 > 25',
    description: '监控VPN连接数量',
    interval: '10分钟',
    triggerCount: 4,
    enabled: true,
    lastTrigger: '2024-01-15 09:10:00'
  },
  {
    key: '43',
    name: '带宽使用监控',
    category: 'network',
    severity: 'warning',
    target: '分部防火墙',
    condition: '带宽使用率 > 90%',
    description: '监控网络带宽使用情况',
    interval: '5分钟',
    triggerCount: 3,
    enabled: true,
    lastTrigger: '2024-01-15 09:05:00'
  },
  {
    key: '44',
    name: 'DNS查询监控',
    category: 'network',
    severity: 'info',
    target: '分部防火墙',
    condition: 'DNS查询失败率 > 5%',
    description: '监控DNS查询成功率',
    interval: '10分钟',
    triggerCount: 1,
    enabled: true,
    lastTrigger: '2024-01-15 08:30:00'
  },
  {
    key: '45',
    name: '无线信号强度监控',
    category: 'network',
    severity: 'info',
    target: '分部AP',
    condition: '信号强度 < -70dBm',
    description: '监控无线信号强度',
    interval: '15分钟',
    triggerCount: 0,
    enabled: true,
    lastTrigger: '-'
  }
])

// 过滤后的规则数据
const filteredRuleData = computed(() => {
  let filtered = ruleData.value
  
  if (searchKeyword.value) {
    filtered = filtered.filter(rule => 
      rule.name.toLowerCase().includes(searchKeyword.value.toLowerCase()) ||
      rule.description.toLowerCase().includes(searchKeyword.value.toLowerCase())
    )
  }
  
  if (selectedCategory.value) {
    filtered = filtered.filter(rule => rule.category === selectedCategory.value)
  }
  
  if (selectedSeverity.value) {
    filtered = filtered.filter(rule => rule.severity === selectedSeverity.value)
  }
  
  if (selectedStatus.value) {
    filtered = filtered.filter(rule => 
      selectedStatus.value === 'enabled' ? rule.enabled : !rule.enabled
    )
  }
  
  if (selectedTarget.value) {
    filtered = filtered.filter(rule => rule.target === selectedTarget.value)
  }
  
  return filtered
})

// 启用规则数量
const enabledRules = computed(() => {
  return ruleData.value.filter(rule => rule.enabled).length
})

// 禁用规则数量
const disabledRules = computed(() => {
  return ruleData.value.filter(rule => !rule.enabled).length
})

// 触发的规则数量
const triggeredRules = computed(() => {
  return ruleData.value.filter(rule => rule.triggerCount > 0).length
})

// 更新统计数据
const updateStats = () => {
  ruleStats.value.total = ruleData.value.length
  ruleStats.value.enabled = enabledRules.value
  ruleStats.value.disabled = disabledRules.value
  ruleStats.value.triggered = triggeredRules.value
}

// 表格列配置
const ruleColumns = [
  {
    title: '规则名称',
    dataIndex: 'name',
    width: 200,
    ellipsis: true,
    tooltip: true
  },
  {
    title: '类型',
    dataIndex: 'category',
    slotName: 'category',
    width: 120
  },
  {
    title: '级别',
    dataIndex: 'severity',
    slotName: 'severity',
    width: 80
  },
  {
    title: '监控目标',
    dataIndex: 'target',
    width: 150
  },
  {
    title: '触发条件',
    dataIndex: 'condition',
    slotName: 'condition',
    ellipsis: true,
    tooltip: true
  },
  {
    title: '检查间隔',
    dataIndex: 'interval',
    width: 100
  },
  {
    title: '触发次数',
    dataIndex: 'triggerCount',
    slotName: 'triggerCount',
    width: 100
  },
  {
    title: '状态',
    dataIndex: 'enabled',
    slotName: 'status',
    width: 80
  },
  {
    title: '操作',
    slotName: 'actions',
    width: 200,
    fixed: 'right'
  }
]

// 工具函数
const getCategoryColor = (category: string) => {
  switch (category) {
    case 'resource': return 'blue'
    case 'network': return 'green'
    case 'security': return 'red'
    case 'performance': return 'orange'
    default: return 'gray'
  }
}

const getCategoryText = (category: string) => {
  switch (category) {
    case 'resource': return '资源监控'
    case 'network': return '网络监控'
    case 'security': return '安全监控'
    case 'performance': return '性能监控'
    default: return '未知'
  }
}

const getCategoryIcon = (category: string) => {
  switch (category) {
    case 'resource': return IconDesktop
    case 'network': return IconWifi
    case 'security': return IconLock
    case 'performance': return IconCloud
    default: return IconSettings
  }
}

const getSeverityColor = (severity: string) => {
  switch (severity) {
    case 'critical': return 'red'
    case 'warning': return 'orange'
    case 'info': return 'blue'
    default: return 'gray'
  }
}

const getSeverityText = (severity: string) => {
  switch (severity) {
    case 'critical': return '严重'
    case 'warning': return '警告'
    case 'info': return '信息'
    default: return '未知'
  }
}

// 事件处理函数
const refreshRules = async () => {
  refreshing.value = true
  await new Promise(resolve => setTimeout(resolve, 1500))
  refreshing.value = false
  Message.success('规则数据刷新成功')
}

const showAddRule = () => {
  editingRule.value = false
  ruleForm.value = {
    key: '',
    name: '',
    category: '',
    severity: '',
    target: '',
    condition: '',
    description: '',
    interval: '5分钟',
    enabled: true,
    triggerCount: 0,
    lastTrigger: '-'
  }
  ruleModalVisible.value = true
}

const exportRules = () => {
  Message.info('正在导出规则配置...')
}

const handleSearch = () => {
  console.log('搜索规则')
}

const clearSearch = () => {
  searchKeyword.value = ''
  selectedCategory.value = ''
  selectedSeverity.value = ''
  selectedStatus.value = ''
  selectedTarget.value = ''
}

const toggleRuleStatus = (record: any) => {
  const status = record.enabled ? '启用' : '禁用'
  Message.success(`规则 "${record.name}" 已${status}`)
}

const editRule = (record: any) => {
  editingRule.value = true
  ruleForm.value = { ...record }
  ruleModalVisible.value = true
}

const copyRule = (record: any) => {
  const newRule = {
    ...record,
    key: Date.now().toString(),
    name: record.name + ' (副本)',
    enabled: false
  }
  ruleData.value.push(newRule)
  Message.success(`规则 "${record.name}" 复制成功`)
}

const testRule = (record: any) => {
  Message.info(`正在测试规则 "${record.name}"...`)
}

const deleteRule = (record: any) => {
  const index = ruleData.value.findIndex(rule => rule.key === record.key)
  if (index > -1) {
    ruleData.value.splice(index, 1)
    Message.success(`规则 "${record.name}" 删除成功`)
  }
}

const enableAllRules = () => {
  filteredRuleData.value.forEach(rule => {
    rule.enabled = true
  })
  Message.success('批量启用规则成功')
}

const disableAllRules = () => {
  filteredRuleData.value.forEach(rule => {
    rule.enabled = false
  })
  Message.success('批量禁用规则成功')
}

const saveRule = () => {
  if (!ruleForm.value.name || !ruleForm.value.category || !ruleForm.value.condition) {
    Message.error('请填写必填项')
    return
  }

  if (editingRule.value) {
    // 编辑现有规则
    const index = ruleData.value.findIndex(rule => rule.key === ruleForm.value.key)
    if (index > -1) {
      ruleData.value[index] = { 
        ...ruleForm.value,
        triggerCount: ruleData.value[index].triggerCount,
        lastTrigger: ruleData.value[index].lastTrigger
      }
      Message.success('规则编辑成功')
    }
  } else {
    // 添加新规则
    const newRule = {
      ...ruleForm.value,
      key: Date.now().toString(),
      triggerCount: 0,
      lastTrigger: '-'
    }
    ruleData.value.push(newRule)
    Message.success('规则添加成功')
  }
  
  ruleModalVisible.value = false
}

const cancelRule = () => {
  ruleModalVisible.value = false
}

onMounted(() => {
  // 初始化统计数据
  updateStats()
})
</script>

<style scoped>
.alert-rule-page {
  padding: 0;
}

.stats-row {
  margin-bottom: 24px;
}

.search-card {
  margin-bottom: 24px;
}

.rule-condition {
  max-width: 200px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.trigger-count {
  font-weight: 500;
}

.trigger-count.high-trigger {
  color: #f5222d;
  font-weight: 600;
}

:deep(.arco-card) {
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

:deep(.arco-switch-checked) {
  background-color: #52c41a;
}
</style> 