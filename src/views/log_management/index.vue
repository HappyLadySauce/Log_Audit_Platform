<template>
  <div class="log-management-page">
    <PageHeader
      title="日志管理"
      description="统一管理和查询各类系统日志，监控分部IT基础设施运行状态"
    >
      <template #extra>
        <a-space>
          <a-button @click="refreshLogs" :loading="refreshing">
            <template #icon>
              <icon-refresh />
            </template>
            刷新
          </a-button>
          <a-button type="primary" @click="showAdvancedSearch">
            <template #icon>
              <icon-search />
            </template>
            高级搜索
          </a-button>
          <a-button @click="exportLogs">
            <template #icon>
              <icon-download />
            </template>
            导出日志
          </a-button>
        </a-space>
      </template>
    </PageHeader>

    <!-- 日志搜索栏 -->
    <a-card :bordered="false" class="search-card">
      <a-row :gutter="16">
        <a-col :span="6">
          <a-input
            v-model:value="searchKeyword"
            placeholder="关键词搜索..."
            allow-clear
            @change="handleSearch"
          >
            <template #prefix>
              <icon-search />
            </template>
          </a-input>
        </a-col>
        <a-col :span="3">
          <a-select v-model:value="selectedLevel" placeholder="日志级别" allow-clear @change="handleSearch">
            <a-option value="INFO">INFO</a-option>
            <a-option value="WARN">WARN</a-option>
            <a-option value="ERROR">ERROR</a-option>
            <a-option value="DEBUG">DEBUG</a-option>
          </a-select>
        </a-col>
        <a-col :span="4">
          <a-select v-model:value="selectedSource" placeholder="日志来源" allow-clear @change="handleSearch">
            <a-option value="network">网络设备</a-option>
            <a-option value="server">服务器</a-option>
            <a-option value="k8s">K8s集群</a-option>
            <a-option value="security">安全审计</a-option>
            <a-option value="system">系统日志</a-option>
          </a-select>
        </a-col>
        <a-col :span="5">
          <a-select v-model:value="selectedHost" placeholder="设备/主机" allow-clear @change="handleSearch">
            <a-option value="分部防火墙">分部防火墙</a-option>
            <a-option value="分部集群接入交换机">分部集群接入交换机</a-option>
            <a-option value="分部彩光交换机">分部彩光交换机</a-option>
            <a-option value="分部无线控制器">分部无线控制器</a-option>
            <a-option value="分部用户接入交换机">分部用户接入交换机</a-option>
            <a-option value="分部AP">分部AP</a-option>
            <a-option value="分部K8S控制节点1">分部K8S控制节点1</a-option>
            <a-option value="分部K8S控制节点2">分部K8S控制节点2</a-option>
            <a-option value="分部K8S工作节点1">分部K8S工作节点1</a-option>
            <a-option value="分部K8S工作节点2">分部K8S工作节点2</a-option>
          </a-select>
        </a-col>
        <a-col :span="4">
          <a-range-picker v-model:value="dateRange" style="width: 100%" @change="handleSearch" />
        </a-col>
        <a-col :span="2">
          <a-button type="primary" style="width: 100%" @click="handleSearch">搜索</a-button>
        </a-col>
      </a-row>
    </a-card>

    <!-- 日志统计 -->
    <a-row :gutter="24" class="stats-row">
      <a-col :span="6">
        <StatCard
          :icon="IconFile"
          icon-bg-color="#1890ff"
          :value="todayStats.total"
          label="今日日志总数"
          subtitle="所有设备"
        />
      </a-col>
      <a-col :span="6">
        <StatCard
          :icon="IconCheck"
          icon-bg-color="#52c41a"
          :value="todayStats.info"
          label="正常日志"
          subtitle="INFO级别"
        />
      </a-col>
      <a-col :span="6">
        <StatCard
          :icon="IconExclamation"
          icon-bg-color="#faad14"
          :value="todayStats.warn"
          label="警告日志"
          subtitle="WARN级别"
        />
      </a-col>
      <a-col :span="6">
        <StatCard
          :icon="IconClose"
          icon-bg-color="#f5222d"
          :value="todayStats.error"
          label="错误日志"
          subtitle="ERROR级别"
        />
      </a-col>
    </a-row>

    <!-- 日志分类标签页 -->
    <a-tabs default-active-key="all-logs" class="log-tabs">
      <a-tab-pane key="all-logs" title="全部日志">
        <a-card :bordered="false">
          <template #title>
            <a-space>
              <span>日志记录</span>
              <a-tag color="blue">{{ currentLogCount.toLocaleString() }}条</a-tag>
              <a-badge :count="onlineDevices" :number-style="{ backgroundColor: '#52c41a' }">
                <a-tag color="green">在线设备</a-tag>
              </a-badge>
            </a-space>
          </template>
          
          <template #extra>
            <a-space>
              <a-checkbox v-model:checked="autoRefresh" @change="toggleAutoRefresh">
                自动刷新({{ autoRefreshInterval }}s)
              </a-checkbox>
                             <a-button size="small" @click="clearSearch">
                 <template #icon>
                   <icon-delete />
                 </template>
                 清空筛选
               </a-button>
            </a-space>
          </template>

          <a-table
            :columns="logColumns"
            :data="filteredLogData"
            :pagination="{ 
              pageSize: 15, 
              total: 56842,
              showTotal: true,
              showSizeChanger: true,
              pageSizeOptions: ['15', '30', '50', '100']
            }"
            :scroll="{ x: '100%' }"
            :loading="tableLoading"
            row-key="key"
          >
            <template #level="{ record }">
              <a-tag :color="getLevelColor(record.level)" size="small">
                <template #icon>
                  <component :is="getLevelIcon(record.level)" />
                </template>
                {{ record.level }}
              </a-tag>
            </template>

            <template #source="{ record }">
              <div class="source-info">
                <component :is="getSourceIcon(record.source)" class="source-icon" />
                <span>{{ getSourceName(record.source) }}</span>
              </div>
            </template>

            <template #host="{ record }">
              <div class="host-info">
                <a-badge :status="record.online ? 'processing' : 'default'" />
                <span>{{ record.host }}</span>
              </div>
            </template>

            <template #message="{ record }">
              <div class="log-message">
                <a-tooltip :content="record.message" placement="topLeft">
                  {{ record.message }}
                </a-tooltip>
              </div>
            </template>

            <template #actions="{ record }">
              <a-space>
                <a-button type="text" size="small" @click="showLogDetail(record)">详情</a-button>
                <a-button type="text" size="small" @click="showContext(record)">上下文</a-button>
                <a-button type="text" size="small" @click="addToWatch(record)">监控</a-button>
              </a-space>
            </template>
          </a-table>
        </a-card>
      </a-tab-pane>

      <a-tab-pane key="network-logs" title="网络设备日志">
        <a-card title="网络设备日志" :bordered="false">
          <div class="device-stats">
            <a-row :gutter="16">
              <a-col :span="6">
                <a-statistic title="设备数量" :value="6" suffix="台" />
              </a-col>
              <a-col :span="6">
                <a-statistic title="在线设备" :value="6" suffix="台" />
              </a-col>
              <a-col :span="6">
                <a-statistic title="今日日志" :value="15680" suffix="条" />
              </a-col>
              <a-col :span="6">
                <a-statistic title="异常事件" :value="12" suffix="个" />
              </a-col>
            </a-row>
          </div>
        </a-card>
      </a-tab-pane>

      <a-tab-pane key="server-logs" title="服务器日志">
        <a-card title="服务器日志" :bordered="false">
          <div class="device-stats">
            <a-row :gutter="16">
              <a-col :span="6">
                <a-statistic title="服务器数量" :value="4" suffix="台" />
              </a-col>
              <a-col :span="6">
                <a-statistic title="在线服务器" :value="4" suffix="台" />
              </a-col>
              <a-col :span="6">
                <a-statistic title="今日日志" :value="28560" suffix="条" />
              </a-col>
              <a-col :span="6">
                <a-statistic title="系统告警" :value="8" suffix="个" />
              </a-col>
            </a-row>
          </div>
        </a-card>
      </a-tab-pane>

      <a-tab-pane key="k8s-logs" title="K8s集群日志">
        <a-card title="K8s集群日志" :bordered="false">
          <div class="device-stats">
            <a-row :gutter="16">
              <a-col :span="6">
                <a-statistic title="集群数量" :value="1" suffix="个" />
              </a-col>
              <a-col :span="6">
                <a-statistic title="Pod数量" :value="40" suffix="个" />
              </a-col>
              <a-col :span="6">
                <a-statistic title="今日日志" :value="12560" suffix="条" />
              </a-col>
              <a-col :span="6">
                <a-statistic title="容器重启" :value="3" suffix="次" />
              </a-col>
            </a-row>
          </div>
        </a-card>
      </a-tab-pane>
    </a-tabs>

    <!-- 日志详情模态框 -->
    <a-modal
      v-model:visible="logDetailVisible"
      :title="`日志详情 - ${selectedLog?.timestamp}`"
      width="800px"
      :footer="false"
    >
      <a-descriptions v-if="selectedLog" :column="2" bordered>
        <a-descriptions-item label="时间">{{ selectedLog.timestamp }}</a-descriptions-item>
        <a-descriptions-item label="级别">
          <a-tag :color="getLevelColor(selectedLog.level)">{{ selectedLog.level }}</a-tag>
        </a-descriptions-item>
        <a-descriptions-item label="来源">{{ getSourceName(selectedLog.source) }}</a-descriptions-item>
        <a-descriptions-item label="主机">{{ selectedLog.host }}</a-descriptions-item>
        <a-descriptions-item label="IP地址">{{ selectedLog.ip }}</a-descriptions-item>
        <a-descriptions-item label="进程ID">{{ selectedLog.pid }}</a-descriptions-item>
        <a-descriptions-item label="完整消息" :span="2">
          <div class="full-message">{{ selectedLog.message }}</div>
        </a-descriptions-item>
        <a-descriptions-item label="原始日志" :span="2">
          <pre class="raw-log">{{ selectedLog.rawLog }}</pre>
        </a-descriptions-item>
      </a-descriptions>
    </a-modal>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'
import PageHeader from '@/components/PageHeader.vue'
import StatCard from '@/components/StatCard.vue'
import {
  IconRefresh,
  IconSearch,
  IconDownload,
  IconFile,
  IconCheck,
  IconExclamation,
  IconClose,
  IconDesktop,
  IconWifi,
  IconLock,
  IconCloud,
  IconCheckCircle,
  IconExclamationCircle,
  IconCloseCircle,
  IconBug,
  IconDelete
} from '@arco-design/web-vue/es/icon'

// 响应式数据
const refreshing = ref(false)
const tableLoading = ref(false)
const searchKeyword = ref('')
const selectedLevel = ref('')
const selectedSource = ref('')
const selectedHost = ref('')
const dateRange = ref([])
const autoRefresh = ref(true)
const autoRefreshInterval = ref(30)
const logDetailVisible = ref(false)
const selectedLog = ref<any>(null)

// 统计数据
const todayStats = ref({
  total: 56842,
  info: 52198,
  warn: 4226,
  error: 418
})

const onlineDevices = ref(10)

// 基础日志数据（前两页30条）
const baseLogData = ref([
  {
    key: '1',
    timestamp: '2024-01-15 10:35:18',
    level: 'INFO',
    source: 'network',
    host: '分部防火墙',
    ip: '10.10.20.1',
    pid: '1234',
    message: '分部防火墙(10.10.20.1) - 流量监控正常，当前带宽: 850Mbps',
    rawLog: '[2024-01-15 10:35:18] INFO: Firewall traffic monitoring normal, bandwidth: 850Mbps',
    online: true
  },
  {
    key: '2',
    timestamp: '2024-01-15 10:35:15',
    level: 'DEBUG',
    source: 'network',
    host: '分部集群接入交换机',
    ip: '10.10.10.150',
    pid: '5678',
    message: '分部集群接入交换机(10.10.10.150) - 端口状态检查完成，24端口全部在线',
    rawLog: '[2024-01-15 10:35:15] DEBUG: Switch port status check completed, all 24 ports online',
    online: true
  },
  {
    key: '3',
    timestamp: '2024-01-15 10:35:12',
    level: 'INFO',
    source: 'server',
    host: '分部K8S控制节点1',
    ip: '10.10.20.2',
    pid: '9012',
    message: '分部K8S控制节点1(10.10.20.2) - 节点状态正常，CPU使用率: 45%，内存使用率: 62%',
    rawLog: '[2024-01-15 10:35:12] INFO: K8s control node status normal, CPU: 45%, Memory: 62%',
    online: true
  },
  {
    key: '4',
    timestamp: '2024-01-15 10:35:08',
    level: 'WARN',
    source: 'k8s',
    host: '分部K8S工作节点1',
    ip: '10.10.20.4',
    pid: '3456',
    message: '分部K8S工作节点1(10.10.20.4) - Pod重启检测到，nginx-deployment重启1次',
    rawLog: '[2024-01-15 10:35:08] WARN: Pod restart detected, nginx-deployment restarted 1 time',
    online: true
  },
  {
    key: '5',
    timestamp: '2024-01-15 10:35:05',
    level: 'ERROR',
    source: 'network',
    host: '分部无线控制器',
    ip: '192.168.100.2',
    pid: '7890',
    message: '分部无线控制器(192.168.100.2) - 连接超时，部分AP离线',
    rawLog: '[2024-01-15 10:35:05] ERROR: Connection timeout, some APs offline',
    online: false
  },
  {
    key: '6',
    timestamp: '2024-01-15 10:35:02',
    level: 'INFO',
    source: 'security',
    host: '分部防火墙',
    ip: '10.10.20.1',
    pid: '1234',
    message: '分部防火墙安全策略更新完成，新增安全规则5条',
    rawLog: '[2024-01-15 10:35:02] INFO: Firewall security policy updated, added 5 new rules',
    online: true
  },
  {
    key: '7',
    timestamp: '2024-01-15 10:35:00',
    level: 'INFO',
    source: 'system',
    host: '分部K8S控制节点2',
    ip: '10.10.20.3',
    pid: '2468',
    message: '分部K8S控制节点2系统备份任务完成，备份大小: 2.5GB',
    rawLog: '[2024-01-15 10:35:00] INFO: System backup task completed, backup size: 2.5GB',
    online: true
  },
  {
    key: '8',
    timestamp: '2024-01-15 10:34:58',
    level: 'INFO',
    source: 'network',
    host: '分部彩光交换机',
    ip: '192.168.100.1',
    pid: '3421',
    message: '分部彩光交换机(192.168.100.1) - 光纤链路状态正常，信号强度: -5.2dBm',
    rawLog: '[2024-01-15 10:34:58] INFO: Fiber link status normal, signal strength: -5.2dBm',
    online: true
  },
  {
    key: '9',
    timestamp: '2024-01-15 10:34:55',
    level: 'INFO',
    source: 'server',
    host: '分部K8S工作节点2',
    ip: '10.10.20.5',
    pid: '7654',
    message: '分部K8S工作节点2(10.10.20.5) - 容器健康检查通过，运行Pod数量: 12',
    rawLog: '[2024-01-15 10:34:55] INFO: Container health check passed, running pods: 12',
    online: true
  },
  {
    key: '10',
    timestamp: '2024-01-15 10:34:52',
    level: 'DEBUG',
    source: 'network',
    host: '分部用户接入交换机',
    ip: '192.168.100.3',
    pid: '8765',
    message: '分部用户接入交换机(192.168.100.3) - VLAN配置更新，用户VLAN100激活',
    rawLog: '[2024-01-15 10:34:52] DEBUG: VLAN configuration updated, user VLAN100 activated',
    online: true
  },
  {
    key: '11',
    timestamp: '2024-01-15 10:34:50',
    level: 'INFO',
    source: 'network',
    host: '分部AP',
    ip: '192.168.30.2',
    pid: '4321',
    message: '分部AP(192.168.30.2) - 无线客户端连接数: 28，信号覆盖正常',
    rawLog: '[2024-01-15 10:34:50] INFO: Wireless clients: 28, signal coverage normal',
    online: true
  },
  {
    key: '12',
    timestamp: '2024-01-15 10:34:48',
    level: 'INFO',
    source: 'system',
    host: '分部K8S控制节点1',
    ip: '10.10.20.2',
    pid: '9012',
    message: '分部K8S控制节点1 - etcd数据库状态健康，延迟: 2.1ms',
    rawLog: '[2024-01-15 10:34:48] INFO: etcd database healthy, latency: 2.1ms',
    online: true
  },
  {
    key: '13',
    timestamp: '2024-01-15 10:34:45',
    level: 'WARN',
    source: 'server',
    host: '分部K8S工作节点1',
    ip: '10.10.20.4',
    pid: '3456',
    message: '分部K8S工作节点1 - 磁盘使用率达到78%，建议清理临时文件',
    rawLog: '[2024-01-15 10:34:45] WARN: Disk usage reached 78%, recommend cleanup',
    online: true
  },
  {
    key: '14',
    timestamp: '2024-01-15 10:34:42',
    level: 'INFO',
    source: 'security',
    host: '分部防火墙',
    ip: '10.10.20.1',
    pid: '1234',
    message: '分部防火墙 - IPS检测到0个威胁，阻止恶意IP: 0个',
    rawLog: '[2024-01-15 10:34:42] INFO: IPS detected 0 threats, blocked malicious IPs: 0',
    online: true
  },
  {
    key: '15',
    timestamp: '2024-01-15 10:34:40',
    level: 'INFO',
    source: 'network',
    host: '分部集群接入交换机',
    ip: '10.10.10.150',
    pid: '5678',
    message: '分部集群接入交换机 - 端口镜像配置更新，监控端口激活',
    rawLog: '[2024-01-15 10:34:40] INFO: Port mirroring config updated, monitor port activated',
    online: true
  },
  {
    key: '16',
    timestamp: '2024-01-15 10:34:38',
    level: 'DEBUG',
    source: 'k8s',
    host: '分部K8S控制节点2',
    ip: '10.10.20.3',
    pid: '2468',
    message: '分部K8S控制节点2 - API服务器响应时间: 15ms，请求处理正常',
    rawLog: '[2024-01-15 10:34:38] DEBUG: API server response time: 15ms, request processing normal',
    online: true
  },
  {
    key: '17',
    timestamp: '2024-01-15 10:34:35',
    level: 'INFO',
    source: 'system',
    host: '分部K8S工作节点2',
    ip: '10.10.20.5',
    pid: '7654',
    message: '分部K8S工作节点2 - 系统负载均衡，当前负载: 1.2',
    rawLog: '[2024-01-15 10:34:35] INFO: System load balanced, current load: 1.2',
    online: true
  },
  {
    key: '18',
    timestamp: '2024-01-15 10:34:32',
    level: 'WARN',
    source: 'network',
    host: '分部彩光交换机',
    ip: '192.168.100.1',
    pid: '3421',
    message: '分部彩光交换机 - 端口利用率达到85%，建议关注流量分布',
    rawLog: '[2024-01-15 10:34:32] WARN: Port utilization reached 85%, monitor traffic distribution',
    online: true
  },
  {
    key: '19',
    timestamp: '2024-01-15 10:34:30',
    level: 'INFO',
    source: 'network',
    host: '分部无线控制器',
    ip: '192.168.100.2',
    pid: '7890',
    message: '分部无线控制器 - 漫游策略更新，支持快速切换',
    rawLog: '[2024-01-15 10:34:30] INFO: Roaming policy updated, fast handoff supported',
    online: true
  },
  {
    key: '20',
    timestamp: '2024-01-15 10:34:28',
    level: 'INFO',
    source: 'system',
    host: '分部K8S控制节点1',
    ip: '10.10.20.2',
    pid: '9012',
    message: '分部K8S控制节点1 - 调度器工作正常，Pod分配策略生效',
    rawLog: '[2024-01-15 10:34:28] INFO: Scheduler working normally, pod allocation policy active',
    online: true
  },
  {
    key: '21',
    timestamp: '2024-01-15 10:34:25',
    level: 'DEBUG',
    source: 'network',
    host: '分部用户接入交换机',
    ip: '192.168.100.3',
    pid: '8765',
    message: '分部用户接入交换机 - STP收敛完成，网络拓扑稳定',
    rawLog: '[2024-01-15 10:34:25] DEBUG: STP convergence completed, network topology stable',
    online: true
  },
  {
    key: '22',
    timestamp: '2024-01-15 10:34:22',
    level: 'INFO',
    source: 'security',
    host: '分部防火墙',
    ip: '10.10.20.1',
    pid: '1234',
    message: '分部防火墙 - SSL VPN连接数: 15，用户认证通过率: 100%',
    rawLog: '[2024-01-15 10:34:22] INFO: SSL VPN connections: 15, user auth success rate: 100%',
    online: true
  },
  {
    key: '23',
    timestamp: '2024-01-15 10:34:20',
    level: 'WARN',
    source: 'k8s',
    host: '分部K8S工作节点1',
    ip: '10.10.20.4',
    pid: '3456',
    message: '分部K8S工作节点1 - 内存使用率达到75%，建议监控应用内存泄漏',
    rawLog: '[2024-01-15 10:34:20] WARN: Memory usage reached 75%, monitor app memory leaks',
    online: true
  },
  {
    key: '24',
    timestamp: '2024-01-15 10:34:18',
    level: 'INFO',
    source: 'network',
    host: '分部AP',
    ip: '192.168.30.2',
    pid: '4321',
    message: '分部AP - 频谱分析完成，干扰水平: 低',
    rawLog: '[2024-01-15 10:34:18] INFO: Spectrum analysis completed, interference level: low',
    online: true
  },
  {
    key: '25',
    timestamp: '2024-01-15 10:34:15',
    level: 'INFO',
    source: 'system',
    host: '分部K8S控制节点2',
    ip: '10.10.20.3',
    pid: '2468',
    message: '分部K8S控制节点2 - 证书自动更新完成，有效期延长至2025年',
    rawLog: '[2024-01-15 10:34:15] INFO: Certificate auto-renewal completed, valid until 2025',
    online: true
  },
  {
    key: '26',
    timestamp: '2024-01-15 10:34:12',
    level: 'INFO',
    source: 'network',
    host: '分部彩光交换机',
    ip: '192.168.100.1',
    pid: '3421',
    message: '分部彩光交换机 - 交换机温度正常，CPU温度: 45°C',
    rawLog: '[2024-01-15 10:34:12] INFO: Switch temperature normal, CPU temp: 45°C',
    online: true
  },
  {
    key: '27',
    timestamp: '2024-01-15 10:34:10',
    level: 'DEBUG',
    source: 'server',
    host: '分部K8S工作节点2',
    ip: '10.10.20.5',
    pid: '7654',
    message: '分部K8S工作节点2 - 网络接口状态检查，eth0: UP, eth1: UP',
    rawLog: '[2024-01-15 10:34:10] DEBUG: Network interface check, eth0: UP, eth1: UP',
    online: true
  },
  {
    key: '28',
    timestamp: '2024-01-15 10:34:08',
    level: 'INFO',
    source: 'security',
    host: '分部防火墙',
    ip: '10.10.20.1',
    pid: '1234',
    message: '分部防火墙 - 防病毒引擎更新完成，病毒库版本: 2024.01.15',
    rawLog: '[2024-01-15 10:34:08] INFO: Antivirus engine updated, virus DB version: 2024.01.15',
    online: true
  },
  {
    key: '29',
    timestamp: '2024-01-15 10:34:05',
    level: 'WARN',
    source: 'network',
    host: '分部用户接入交换机',
    ip: '192.168.100.3',
    pid: '8765',
    message: '分部用户接入交换机 - 端口16流量异常，建议检查连接设备',
    rawLog: '[2024-01-15 10:34:05] WARN: Port 16 traffic anomaly, check connected device',
    online: true
  },
  {
    key: '30',
    timestamp: '2024-01-15 10:34:02',
    level: 'INFO',
    source: 'k8s',
    host: '分部K8S控制节点1',
    ip: '10.10.20.2',
    pid: '9012',
    message: '分部K8S控制节点1 - 集群节点心跳检测正常，所有节点Ready',
    rawLog: '[2024-01-15 10:34:02] INFO: Cluster node heartbeat normal, all nodes Ready',
    online: true
  }
])

// 生成完整的日志数据（56842条）
const generateLogData = () => {
  const totalLogs = 56842
  const pageSize = 15
  const baseLogs = baseLogData.value
  const totalPages = Math.ceil(totalLogs / pageSize)
  
  const allLogs = []
  
  for (let page = 0; page < totalPages; page++) {
    for (let i = 0; i < pageSize && allLogs.length < totalLogs; i++) {
      // 使用前30条数据循环
      const baseIndex = i % baseLogs.length
      const baseLog = baseLogs[baseIndex]
      
      // 为每条日志生成唯一的key
      const uniqueKey = (page * pageSize + i + 1).toString()
      
      // 调整时间戳，使其看起来更真实
      const baseTime = new Date('2024-01-15 10:35:18')
      const offsetMinutes = Math.floor(allLogs.length / 10) // 每10条日志时间往前推1分钟
      const adjustedTime = new Date(baseTime.getTime() - offsetMinutes * 60000)
      
      const logEntry = {
        ...baseLog,
        key: uniqueKey,
        timestamp: adjustedTime.toLocaleString('zh-CN', {
          year: 'numeric',
          month: '2-digit',
          day: '2-digit',
          hour: '2-digit',
          minute: '2-digit',
          second: '2-digit'
        }).replace(/\//g, '-')
      }
      
      allLogs.push(logEntry)
    }
  }
  
  return allLogs
}

// 日志数据
const logData = ref(generateLogData())

// 过滤后的日志数据
const filteredLogData = computed(() => {
  let filtered = logData.value
  
  if (searchKeyword.value) {
    filtered = filtered.filter(log => 
      log.message.toLowerCase().includes(searchKeyword.value.toLowerCase()) ||
      log.host.toLowerCase().includes(searchKeyword.value.toLowerCase())
    )
  }
  
  if (selectedLevel.value) {
    filtered = filtered.filter(log => log.level === selectedLevel.value)
  }
  
  if (selectedSource.value) {
    filtered = filtered.filter(log => log.source === selectedSource.value)
  }
  
  if (selectedHost.value) {
    filtered = filtered.filter(log => log.host === selectedHost.value)
  }
  
  return filtered
})

// 当前显示的日志数量
const currentLogCount = computed(() => filteredLogData.value.length)

// 表格列配置
const logColumns = [
  {
    title: '时间',
    dataIndex: 'timestamp',
    width: 160,
    sortable: {
      sortDirections: ['ascend', 'descend']
    }
  },
  {
    title: '级别',
    dataIndex: 'level',
    slotName: 'level',
    width: 90
  },
  {
    title: '来源',
    dataIndex: 'source',
    slotName: 'source',
    width: 120
  },
  {
    title: '主机/设备',
    dataIndex: 'host',
    slotName: 'host',
    width: 180
  },
  {
    title: 'IP地址',
    dataIndex: 'ip',
    width: 120
  },
  {
    title: '消息',
    dataIndex: 'message',
    slotName: 'message',
    ellipsis: true,
    tooltip: true
  },
  {
    title: '操作',
    slotName: 'actions',
    width: 180,
    fixed: 'right'
  }
]

// 定时器
let refreshTimer: any = null

// 工具函数
const getLevelColor = (level: string) => {
  switch (level) {
    case 'INFO':
      return 'blue'
    case 'WARN':
      return 'orange'
    case 'ERROR':
      return 'red'
    case 'DEBUG':
      return 'gray'
    default:
      return 'default'
  }
}

const getLevelIcon = (level: string) => {
  switch (level) {
    case 'INFO':
      return IconCheckCircle
    case 'WARN':
      return IconExclamationCircle
    case 'ERROR':
      return IconCloseCircle
    case 'DEBUG':
      return IconBug
    default:
      return IconFile
  }
}

const getSourceIcon = (source: string) => {
  switch (source) {
    case 'network':
      return IconWifi
    case 'server':
      return IconDesktop
    case 'k8s':
      return IconCloud
    case 'security':
      return IconLock
    case 'system':
      return IconDesktop
    default:
      return IconFile
  }
}

const getSourceName = (source: string) => {
  switch (source) {
    case 'network':
      return '网络设备'
    case 'server':
      return '服务器'
    case 'k8s':
      return 'K8s集群'
    case 'security':
      return '安全审计'
    case 'system':
      return '系统日志'
    default:
      return '未知来源'
  }
}

// 事件处理函数
const refreshLogs = async () => {
  refreshing.value = true
  await new Promise(resolve => setTimeout(resolve, 1500))
  refreshing.value = false
}

const handleSearch = () => {
  console.log('搜索日志')
}

const showAdvancedSearch = () => {
  console.log('显示高级搜索')
}

const exportLogs = () => {
  console.log('导出日志')
}

const clearSearch = () => {
  searchKeyword.value = ''
  selectedLevel.value = ''
  selectedSource.value = ''
  selectedHost.value = ''
  dateRange.value = []
}

const showLogDetail = (record: any) => {
  selectedLog.value = record
  logDetailVisible.value = true
}

const showContext = (record: any) => {
  console.log('显示上下文:', record)
}

const addToWatch = (record: any) => {
  console.log('添加到监控:', record)
}

const toggleAutoRefresh = (checked: boolean) => {
  if (checked) {
    startAutoRefresh()
  } else {
    stopAutoRefresh()
  }
}

const startAutoRefresh = () => {
  refreshTimer = setInterval(() => {
    // 模拟新日志数据
    console.log('自动刷新日志')
  }, autoRefreshInterval.value * 1000)
}

const stopAutoRefresh = () => {
  if (refreshTimer) {
    clearInterval(refreshTimer)
    refreshTimer = null
  }
}

// 生命周期
onMounted(() => {
  if (autoRefresh.value) {
    startAutoRefresh()
  }
})

onUnmounted(() => {
  stopAutoRefresh()
})
</script>

<style scoped>
.log-management-page {
  padding: 0;
}

.search-card {
  margin-bottom: 24px;
}

.stats-row {
  margin-bottom: 24px;
}

.log-tabs {
  margin-bottom: 24px;
}

.device-stats {
  padding: 20px;
  background: #fafbfc;
  border-radius: 6px;
  margin-bottom: 16px;
}

.source-info {
  display: flex;
  align-items: center;
  gap: 8px;
}

.source-icon {
  font-size: 14px;
  color: #86909c;
}

.host-info {
  display: flex;
  align-items: center;
  gap: 8px;
}

.log-message {
  max-width: 400px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.full-message {
  padding: 8px 12px;
  background: #f7f8fa;
  border-radius: 4px;
  word-break: break-all;
}

.raw-log {
  background: #1e1e1e;
  color: #ffffff;
  padding: 12px;
  border-radius: 4px;
  font-family: 'Courier New', monospace;
  font-size: 12px;
  line-height: 1.5;
  white-space: pre-wrap;
  word-break: break-all;
}

:deep(.arco-card) {
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

:deep(.arco-tabs-content) {
  padding-top: 0;
}

:deep(.arco-statistic-title) {
  font-size: 14px;
  color: #86909c;
}

:deep(.arco-statistic-value) {
  font-size: 20px;
  font-weight: 600;
  color: #1d2129;
}
</style>
