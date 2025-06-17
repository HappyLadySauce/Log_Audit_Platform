<template>
  <div class="k8s-page">
    <PageHeader
      title="K8s集群日志"
      description="管理和监控Kubernetes集群的日志采集"
    >
      <template #extra>
        <a-space>
          <a-button>
            <template #icon>
              <icon-refresh />
            </template>
            刷新
          </a-button>
          <a-button type="primary">
            <template #icon>
              <icon-plus />
            </template>
            添加集群
          </a-button>
        </a-space>
      </template>
    </PageHeader>

    <!-- 集群概览 -->
    <a-row :gutter="24" class="stats-row">
      <a-col :span="6">
        <StatCard
          :icon="IconCloud"
          icon-bg-color="#1890ff"
          :value="1"
          label="集群数量"
          subtitle="K8s集群"
        />
      </a-col>
      <a-col :span="6">
        <StatCard
          :icon="IconApps"
          icon-bg-color="#52c41a"
          :value="40"
          label="Pod数量"
          subtitle="运行中"
        />
      </a-col>
      <a-col :span="6">
        <StatCard
          :icon="IconFile"
          icon-bg-color="#faad14"
          :value="596"
          label="今日日志"
          subtitle="条数统计"
        />
      </a-col>
      <a-col :span="6">
        <StatCard
          :icon="IconStorage"
          icon-bg-color="#722ed1"
          :value="3.8"
          label="存储空间(GB)"
          subtitle="日志占用"
        />
      </a-col>
    </a-row>

    <!-- 集群管理标签页 -->
    <a-tabs default-active-key="cluster-monitor" class="cluster-tabs">
      <a-tab-pane key="cluster-monitor" title="集群监控">
        <a-card :bordered="false">
          <template #title>
            <a-space>
              <span>集群监控</span>
              <a-tag color="blue">节点监控</a-tag>
              <a-tag color="green">Pod监控</a-tag>
            </a-space>
          </template>
          
          <!-- 集群列表 -->
          <a-table
            :columns="clusterColumns"
            :data="clusterData"
            :pagination="false"
            :scroll="{ x: '100%' }"
            class="cluster-table"
          >
            <template #clusterInfo="{ record }">
              <div class="cluster-info">
                <a-avatar size="small" class="cluster-avatar">
                  <icon-cloud />
                </a-avatar>
                <div class="cluster-details">
                  <div class="cluster-name">{{ record.name }}</div>
                  <div class="cluster-version">{{ record.version }}</div>
                </div>
              </div>
            </template>

            <template #status="{ record }">
              <a-badge
                :status="record.status === 'running' ? 'success' : 'error'"
                :text="record.status === 'running' ? '运行中' : '异常'"
              />
            </template>

            <template #logLevel="{ record }">
              <a-tag :color="getLogLevelColor(record.logLevel)">
                {{ record.logLevel }}
              </a-tag>
            </template>

            <template #actions="{ record }">
              <a-space>
                <a-button type="text" size="small" @click="showClusterDetail(record)">查看日志详情</a-button>
              </a-space>
            </template>
          </a-table>
        </a-card>
      </a-tab-pane>

      <a-tab-pane key="node-monitor" title="节点监控">
        <a-card title="节点监控" :bordered="false">
          <a-table
            :columns="nodeColumns"
            :data="nodeData"
            :pagination="false"
            :scroll="{ x: '100%' }"
            class="node-table"
          >
            <template #nodeName="{ record }">
              <div class="node-info">
                <a-avatar size="small" class="node-avatar">
                  <icon-desktop />
                </a-avatar>
                <div class="node-details">
                  <div class="node-name">{{ record.nodeName }}</div>
                  <div class="node-ip">{{ record.ip }}</div>
                </div>
              </div>
            </template>

            <template #nodeType="{ record }">
              <a-tag
                :color="record.nodeType === 'control-plane' ? 'blue' : 'green'"
                size="small"
              >
                {{ record.nodeType === 'control-plane' ? '控制平面节点' : '工作节点' }}
              </a-tag>
            </template>

            <template #status="{ record }">
              <a-badge
                :status="record.status === '在线' ? 'success' : 'error'"
                :text="record.status"
              />
            </template>

            <template #resources="{ record }">
              <div class="resource-info">
                <div>CPU: {{ record.cpu }}%</div>
                <div>内存: {{ record.memory }}%</div>
              </div>
            </template>

            <template #actions="{ record }">
              <a-space>
                <a-button type="text" size="small" @click="showNodeDetail(record)">查看详情</a-button>
              </a-space>
            </template>
          </a-table>
        </a-card>
      </a-tab-pane>

      <a-tab-pane key="pod-monitor" title="Pod监控">
        <a-card title="Pod监控" :bordered="false">
          <a-table
            :columns="podColumns"
            :data="podData"
            :pagination="false"
            :scroll="{ x: '100%' }"
            class="pod-table"
          >
            <template #podName="{ record }">
              <div class="pod-info">
                <a-avatar size="small" class="pod-avatar">
                  <icon-apps />
                </a-avatar>
                <div class="pod-details">
                  <div class="pod-name">{{ record.podName }}</div>
                  <div class="pod-namespace">{{ record.namespace }}</div>
                </div>
              </div>
            </template>

            <template #status="{ record }">
              <a-badge
                :status="record.status === 'Running' ? 'success' : 'error'"
                :text="record.status"
              />
            </template>

            <template #resources="{ record }">
              <div class="resource-info">
                <div>CPU: {{ record.cpu }}%</div>
                <div>内存: {{ record.memory }}%</div>
              </div>
            </template>

            <template #actions="{ record }">
              <a-space>
                <a-button type="text" size="small" @click="showPodDetail(record)">日志</a-button>
                <a-button type="text" size="small" @click="showPodDetail(record)">详情</a-button>
                <a-button type="text" size="small">重启</a-button>
              </a-space>
            </template>
          </a-table>
        </a-card>
      </a-tab-pane>
    </a-tabs>

    <!-- 集群详情模态框 -->
    <a-modal
      v-model:visible="clusterDetailVisible"
      :title="`集群详情 - ${selectedCluster?.name}`"
      width="1200px"
      :footer="false"
    >
      <a-tabs default-active-key="basic-info">
        <a-tab-pane key="basic-info" title="基本信息">
          <a-descriptions :column="2" bordered>
            <a-descriptions-item label="集群名称">{{ selectedCluster?.name }}</a-descriptions-item>
            <a-descriptions-item label="版本">{{ selectedCluster?.version }}</a-descriptions-item>
            <a-descriptions-item label="节点数">{{ selectedCluster?.nodes }}</a-descriptions-item>
            <a-descriptions-item label="Pod数">{{ selectedCluster?.pods }}</a-descriptions-item>
            <a-descriptions-item label="状态">
              <a-badge
                :status="selectedCluster?.status === 'running' ? 'success' : 'error'"
                :text="selectedCluster?.status === 'running' ? '运行中' : '异常'"
              />
            </a-descriptions-item>
            <a-descriptions-item label="API端点">{{ selectedCluster?.endpoint }}</a-descriptions-item>
          </a-descriptions>
        </a-tab-pane>
        <a-tab-pane key="real-time-logs" title="实时日志">
          <div class="log-container">
            <div class="log-header">
              <a-space>
                <a-button size="small" @click="toggleLogStream">
                  {{ logStreamActive ? '停止' : '开始' }}实时日志
                </a-button>
                <a-button size="small" @click="clearLogs">清空日志</a-button>
              </a-space>
            </div>
            <div class="log-content" ref="clusterLogRef">
              <div v-for="(log, index) in clusterLogs" :key="index" class="log-line">
                <span class="log-time">{{ log.time }}</span>
                <span :class="`log-level ${log.level.toLowerCase()}`">{{ log.level }}</span>
                <span class="log-message">{{ log.message }}</span>
              </div>
            </div>
          </div>
        </a-tab-pane>
      </a-tabs>
    </a-modal>

    <!-- 节点详情模态框 -->
    <a-modal
      v-model:visible="nodeDetailVisible"
      :title="`节点详情 - ${selectedNode?.nodeName}`"
      width="1200px"
      :footer="false"
    >
      <a-tabs default-active-key="basic-info">
        <a-tab-pane key="basic-info" title="基本信息">
          <a-descriptions :column="2" bordered>
            <a-descriptions-item label="节点名称">{{ selectedNode?.nodeName }}</a-descriptions-item>
            <a-descriptions-item label="IP地址">{{ selectedNode?.ip }}</a-descriptions-item>
            <a-descriptions-item label="节点类型">
              <a-tag :color="selectedNode?.nodeType === 'control-plane' ? 'blue' : 'green'">
                {{ selectedNode?.nodeType === 'control-plane' ? '控制平面节点' : '工作节点' }}
              </a-tag>
            </a-descriptions-item>
            <a-descriptions-item label="系统版本">{{ selectedNode?.system }}</a-descriptions-item>
            <a-descriptions-item label="状态">
              <a-badge
                :status="selectedNode?.status === '在线' ? 'success' : 'error'"
                :text="selectedNode?.status"
              />
            </a-descriptions-item>
            <a-descriptions-item label="资源使用">
              <div>CPU: {{ selectedNode?.cpu }}%, 内存: {{ selectedNode?.memory }}%</div>
            </a-descriptions-item>
          </a-descriptions>
        </a-tab-pane>
        <a-tab-pane key="real-time-logs" title="实时日志">
          <div class="log-container">
            <div class="log-header">
              <a-space>
                <a-button size="small" @click="toggleNodeLogStream">
                  {{ nodeLogStreamActive ? '停止' : '开始' }}实时日志
                </a-button>
                <a-button size="small" @click="clearNodeLogs">清空日志</a-button>
              </a-space>
            </div>
            <div class="log-content" ref="nodeLogRef">
              <div v-for="(log, index) in nodeLogs" :key="index" class="log-line">
                <span class="log-time">{{ log.time }}</span>
                <span :class="`log-level ${log.level.toLowerCase()}`">{{ log.level }}</span>
                <span class="log-message">{{ log.message }}</span>
              </div>
            </div>
          </div>
        </a-tab-pane>
      </a-tabs>
    </a-modal>

    <!-- Pod详情模态框 -->
    <a-modal
      v-model:visible="podDetailVisible"
      :title="`Pod详情 - ${selectedPod?.podName}`"
      width="1200px"
      :footer="false"
    >
      <a-tabs default-active-key="basic-info">
        <a-tab-pane key="basic-info" title="基本信息">
          <a-descriptions :column="2" bordered>
            <a-descriptions-item label="Pod名称">{{ selectedPod?.podName }}</a-descriptions-item>
            <a-descriptions-item label="命名空间">{{ selectedPod?.namespace }}</a-descriptions-item>
            <a-descriptions-item label="节点">{{ selectedPod?.node }}</a-descriptions-item>
            <a-descriptions-item label="状态">
              <a-badge
                :status="selectedPod?.status === 'Running' ? 'success' : 'error'"
                :text="selectedPod?.status"
              />
            </a-descriptions-item>
            <a-descriptions-item label="重启次数">{{ selectedPod?.restarts }}</a-descriptions-item>
            <a-descriptions-item label="创建时间">{{ selectedPod?.createdTime }}</a-descriptions-item>
            <a-descriptions-item label="UID">abc123-def456-ghi789</a-descriptions-item>
            <a-descriptions-item label="资源使用">
              <div>CPU: {{ selectedPod?.cpu }}%, 内存: {{ selectedPod?.memory }}%</div>
            </a-descriptions-item>
          </a-descriptions>
        </a-tab-pane>
        <a-tab-pane key="resource-monitor" title="资源监控">
          <div class="chart-placeholder">
            <div class="chart-content">
              <icon-settings class="chart-icon" />
              <p>CPU使用率和内存使用率监控图表</p>
            </div>
          </div>
        </a-tab-pane>
        <a-tab-pane key="event-logs" title="事件日志">
          <a-table
            :columns="eventColumns"
            :data="eventData"
            :pagination="false"
            size="small"
          >
            <template #eventType="{ record }">
              <a-tag :color="record.type === 'Normal' ? 'green' : 'red'" size="small">
                {{ record.type }}
              </a-tag>
            </template>
          </a-table>
        </a-tab-pane>
        <a-tab-pane key="real-time-logs" title="实时日志">
          <div class="log-container">
            <div class="log-header">
              <a-space>
                <a-button size="small" @click="togglePodLogStream">
                  {{ podLogStreamActive ? '停止' : '开始' }}实时日志
                </a-button>
                <a-button size="small" @click="clearPodLogs">清空日志</a-button>
              </a-space>
            </div>
            <div class="log-content" ref="podLogRef">
              <div v-for="(log, index) in podLogs" :key="index" class="log-line">
                <span class="log-time">{{ log.time }}</span>
                <span :class="`log-level ${log.level.toLowerCase()}`">{{ log.level }}</span>
                <span class="log-message">{{ log.message }}</span>
              </div>
            </div>
          </div>
        </a-tab-pane>
      </a-tabs>
    </a-modal>
  </div>
</template>

<script setup lang="ts">
import { ref, nextTick, onUnmounted } from 'vue'
import PageHeader from '@/components/PageHeader.vue'
import StatCard from '@/components/StatCard.vue'
import {
  IconRefresh,
  IconPlus,
  IconCloud,
  IconApps,
  IconFile,
  IconStorage,
  IconSettings,
  IconDesktop
} from '@arco-design/web-vue/es/icon'

// 集群数据
const clusterData = ref([
  {
    key: '1',
    name: 'k8s-02',
    version: 'v1.28.2',
    nodes: 4,
    pods: 40,
    status: 'running',
    logLevel: 'INFO',
    endpoint: 'http://10.10.20.2:16443'
  }
])

// 节点数据
const nodeData = ref([
  {
    key: '1',
    nodeName: '分部K8S控制节点1',
    ip: '10.10.20.2',
    nodeType: 'control-plane',
    system: 'Ubuntu 22.04',
    status: '在线',
    cpu: 45,
    memory: 62
  },
  {
    key: '2',
    nodeName: '分部K8S控制节点2',
    ip: '10.10.20.3',
    nodeType: 'control-plane',
    system: 'Ubuntu 22.04',
    status: '在线',
    cpu: 38,
    memory: 55
  },
  {
    key: '3',
    nodeName: '分部K8S工作节点1',
    ip: '10.10.20.4',
    nodeType: 'worker',
    system: 'Ubuntu 22.04',
    status: '在线',
    cpu: 72,
    memory: 68
  },
  {
    key: '4',
    nodeName: '分部K8S工作节点2',
    ip: '10.10.20.5',
    nodeType: 'worker',
    system: 'Ubuntu 22.04',
    status: '在线',
    cpu: 58,
    memory: 71
  }
])

// Pod数据
const podData = ref([
  {
    key: '1',
    podName: 'nginx-deployment-7d6b5f8b4c-xmk2p',
    namespace: 'default',
    node: 'worker-node-1',
    status: 'Running',
    restarts: 0,
    cpu: 35,
    memory: 42,
    createdTime: '2024-01-15 09:30:00'
  },
  {
    key: '2',
    podName: 'mysql-statefulset-0',
    namespace: 'database',
    node: 'worker-node-2',
    status: 'Running',
    restarts: 1,
    cpu: 68,
    memory: 73,
    createdTime: '2024-01-14 15:20:00'
  },
  {
    key: '3',
    podName: 'redis-cluster-0',
    namespace: 'cache',
    node: 'worker-node-1',
    status: 'Running',
    restarts: 0,
    cpu: 25,
    memory: 38,
    createdTime: '2024-01-15 08:45:00'
  },
  {
    key: '4',
    podName: 'api-gateway-5f7c8d9b-h6k4m',
    namespace: 'default',
    node: 'worker-node-2',
    status: 'Running',
    restarts: 0,
    cpu: 52,
    memory: 61,
    createdTime: '2024-01-15 10:12:00'
  }
])

// 表格列配置
const clusterColumns = [
  {
    title: '集群信息',
    dataIndex: 'name',
    slotName: 'clusterInfo',
    width: 200
  },
  {
    title: '节点数',
    dataIndex: 'nodes',
    width: 80
  },
  {
    title: 'Pod数',
    dataIndex: 'pods',
    width: 80
  },
  {
    title: '状态',
    dataIndex: 'status',
    slotName: 'status',
    width: 100
  },
  {
    title: '日志级别',
    dataIndex: 'logLevel',
    slotName: 'logLevel',
    width: 100
  },
  {
    title: 'API端点',
    dataIndex: 'endpoint',
    width: 250
  },
  {
    title: '操作',
    slotName: 'actions',
    width: 200,
    fixed: 'right'
  }
]

// 节点表格列配置
const nodeColumns = [
  {
    title: '节点名称',
    dataIndex: 'nodeName',
    slotName: 'nodeName',
    width: 200
  },
  {
    title: '节点类型',
    dataIndex: 'nodeType',
    slotName: 'nodeType',
    width: 120
  },
  {
    title: '系统版本',
    dataIndex: 'system',
    width: 120
  },
  {
    title: '状态',
    dataIndex: 'status',
    slotName: 'status',
    width: 80
  },
  {
    title: '资源使用',
    dataIndex: 'resources',
    slotName: 'resources',
    width: 120
  },
  {
    title: '操作',
    slotName: 'actions',
    width: 120,
    fixed: 'right'
  }
]

// Pod表格列配置
const podColumns = [
  {
    title: 'Pod名称',
    dataIndex: 'podName',
    slotName: 'podName',
    width: 250
  },
  {
    title: '命名空间',
    dataIndex: 'namespace',
    width: 100
  },
  {
    title: '节点',
    dataIndex: 'node',
    width: 120
  },
  {
    title: '状态',
    dataIndex: 'status',
    slotName: 'status',
    width: 80
  },
  {
    title: '重启次数',
    dataIndex: 'restarts',
    width: 80
  },
  {
    title: '资源使用',
    dataIndex: 'resources',
    slotName: 'resources',
    width: 120
  },
  {
    title: '创建时间',
    dataIndex: 'createdTime',
    width: 150
  },
  {
    title: '操作',
    slotName: 'actions',
    width: 180,
    fixed: 'right'
  }
]

// 事件表格列配置
const eventColumns = [
  {
    title: '类型',
    dataIndex: 'type',
    slotName: 'eventType',
    width: 80
  },
  {
    title: '原因',
    dataIndex: 'reason',
    width: 120
  },
  {
    title: '消息',
    dataIndex: 'message',
    width: 400
  },
  {
    title: '时间',
    dataIndex: 'time',
    width: 150
  }
]

// 事件数据
const eventData = ref([
  {
    key: '1',
    type: 'Normal',
    reason: 'Scheduled',
    message: 'Successfully assigned default/nginx-deployment-xxx to worker-node-1',
    time: '2024-01-15 09:30:00'
  },
  {
    key: '2',
    type: 'Normal',
    reason: 'Pulled',
    message: 'Container image "nginx:1.20" already present on machine',
    time: '2024-01-15 09:30:05'
  }
])

// 模态框显示状态
const clusterDetailVisible = ref(false)
const nodeDetailVisible = ref(false)
const podDetailVisible = ref(false)

// 选中的数据
const selectedCluster = ref<any>(null)
const selectedNode = ref<any>(null)
const selectedPod = ref<any>(null)

// 实时日志相关
const clusterLogs = ref<any[]>([])
const nodeLogs = ref<any[]>([])
const podLogs = ref<any[]>([])

// 日志流状态
const logStreamActive = ref(false)
const nodeLogStreamActive = ref(false)
const podLogStreamActive = ref(false)

// 日志容器引用
const clusterLogRef = ref<HTMLElement>()
const nodeLogRef = ref<HTMLElement>()
const podLogRef = ref<HTMLElement>()

// 定时器
let clusterLogTimer: any = null
let nodeLogTimer: any = null
let podLogTimer: any = null

// 显示集群详情
const showClusterDetail = (cluster: any) => {
  selectedCluster.value = cluster
  clusterDetailVisible.value = true
  initClusterLogs()
}

// 显示节点详情
const showNodeDetail = (node: any) => {
  selectedNode.value = node
  nodeDetailVisible.value = true
  initNodeLogs()
}

// 显示Pod详情
const showPodDetail = (pod: any) => {
  selectedPod.value = pod
  podDetailVisible.value = true
  initPodLogs()
}

// 初始化集群日志
const initClusterLogs = () => {
  clusterLogs.value = [
    {
      time: '2024-01-15 10:35:18',
      level: 'INFO',
      message: '分部k8s-02集群(10.10.20.2) - 集群状态正常，40个Pod全部运行中'
    },
    {
      time: '2024-01-15 10:35:15',
      level: 'DEBUG',
      message: '分部k8s-02节点状态检查完成，4个节点全部在线'
    },
    {
      time: '2024-01-15 10:35:12',
      level: 'INFO',
      message: '分部k8s-02 Pod调度成功，新增服务实例3个'
    }
  ]
}

// 初始化节点日志
const initNodeLogs = () => {
  nodeLogs.value = [
    {
      time: '2024-01-15 10:35:18',
      level: 'INFO',
      message: `${selectedNode.value?.nodeName}(${selectedNode.value?.ip}) - 节点状态正常，资源充足`
    },
    {
      time: '2024-01-15 10:35:15',
      level: 'DEBUG',
      message: `${selectedNode.value?.nodeName} - 系统资源检查完成，CPU使用率: ${selectedNode.value?.cpu}%`
    },
    {
      time: '2024-01-15 10:35:12',
      level: 'INFO',
      message: `${selectedNode.value?.nodeName} - kubelet服务运行正常，网络连接稳定`
    }
  ]
}

// 初始化Pod日志
const initPodLogs = () => {
  podLogs.value = [
    {
      time: '2024-01-15 10:35:18',
      level: 'INFO',
      message: `${selectedPod.value?.podName} - 容器启动成功，服务正常运行`
    },
    {
      time: '2024-01-15 10:35:15',
      level: 'DEBUG',
      message: `${selectedPod.value?.podName} - 健康检查通过，CPU: ${selectedPod.value?.cpu}%, 内存: ${selectedPod.value?.memory}%`
    },
    {
      time: '2024-01-15 10:35:12',
      level: 'INFO',
      message: `${selectedPod.value?.podName} - 网络连接正常，存储卷挂载成功`
    }
  ]
}

// 切换集群日志流
const toggleLogStream = () => {
  logStreamActive.value = !logStreamActive.value
  if (logStreamActive.value) {
    startClusterLogStream()
  } else {
    stopClusterLogStream()
  }
}

// 切换节点日志流
const toggleNodeLogStream = () => {
  nodeLogStreamActive.value = !nodeLogStreamActive.value
  if (nodeLogStreamActive.value) {
    startNodeLogStream()
  } else {
    stopNodeLogStream()
  }
}

// 切换Pod日志流
const togglePodLogStream = () => {
  podLogStreamActive.value = !podLogStreamActive.value
  if (podLogStreamActive.value) {
    startPodLogStream()
  } else {
    stopPodLogStream()
  }
}

// 开始集群日志流
const startClusterLogStream = () => {
  clusterLogTimer = setInterval(() => {
    const now = new Date()
    const time = now.toLocaleString('zh-CN', { 
      year: 'numeric', 
      month: '2-digit', 
      day: '2-digit', 
      hour: '2-digit', 
      minute: '2-digit', 
      second: '2-digit' 
    }).replace(/\//g, '-')
    
    const messages = [
      '集群健康检查通过，所有组件运行正常',
      'etcd集群状态健康，数据同步完成',
      'API Server响应正常，延迟8ms',
      'Scheduler调度器工作正常',
      'Controller Manager状态良好'
    ]
    
    const levels = ['INFO', 'DEBUG', 'WARN']
    const randomMessage = messages[Math.floor(Math.random() * messages.length)]
    const randomLevel = levels[Math.floor(Math.random() * levels.length)]
    
    clusterLogs.value.push({
      time,
      level: randomLevel,
      message: `分部k8s-02集群 - ${randomMessage}`
    })
    
    // 限制日志条数
    if (clusterLogs.value.length > 100) {
      clusterLogs.value.shift()
    }
    
    // 自动滚动到底部
    nextTick(() => {
      if (clusterLogRef.value) {
        clusterLogRef.value.scrollTop = clusterLogRef.value.scrollHeight
      }
    })
  }, 2000)
}

// 开始节点日志流
const startNodeLogStream = () => {
  nodeLogTimer = setInterval(() => {
    const now = new Date()
    const time = now.toLocaleString('zh-CN', { 
      year: 'numeric', 
      month: '2-digit', 
      day: '2-digit', 
      hour: '2-digit', 
      minute: '2-digit', 
      second: '2-digit' 
    }).replace(/\//g, '-')
    
    const messages = [
      'kubelet服务运行正常',
      '容器运行时状态良好',
      '网络插件工作正常',
      '磁盘空间充足',
      '系统负载正常'
    ]
    
    const levels = ['INFO', 'DEBUG']
    const randomMessage = messages[Math.floor(Math.random() * messages.length)]
    const randomLevel = levels[Math.floor(Math.random() * levels.length)]
    
    nodeLogs.value.push({
      time,
      level: randomLevel,
      message: `${selectedNode.value?.nodeName} - ${randomMessage}`
    })
    
    if (nodeLogs.value.length > 100) {
      nodeLogs.value.shift()
    }
    
    nextTick(() => {
      if (nodeLogRef.value) {
        nodeLogRef.value.scrollTop = nodeLogRef.value.scrollHeight
      }
    })
  }, 3000)
}

// 开始Pod日志流
const startPodLogStream = () => {
  podLogTimer = setInterval(() => {
    const now = new Date()
    const time = now.toLocaleString('zh-CN', { 
      year: 'numeric', 
      month: '2-digit', 
      day: '2-digit', 
      hour: '2-digit', 
      minute: '2-digit', 
      second: '2-digit' 
    }).replace(/\//g, '-')
    
    const messages = [
      '接收到新的请求',
      '处理业务逻辑',
      '数据库连接正常',
      '缓存命中率: 95%',
      '响应时间: 120ms'
    ]
    
    const levels = ['INFO', 'DEBUG']
    const randomMessage = messages[Math.floor(Math.random() * messages.length)]
    const randomLevel = levels[Math.floor(Math.random() * levels.length)]
    
    podLogs.value.push({
      time,
      level: randomLevel,
      message: `${selectedPod.value?.podName} - ${randomMessage}`
    })
    
    if (podLogs.value.length > 100) {
      podLogs.value.shift()
    }
    
    nextTick(() => {
      if (podLogRef.value) {
        podLogRef.value.scrollTop = podLogRef.value.scrollHeight
      }
    })
  }, 1500)
}

// 停止日志流
const stopClusterLogStream = () => {
  if (clusterLogTimer) {
    clearInterval(clusterLogTimer)
    clusterLogTimer = null
  }
}

const stopNodeLogStream = () => {
  if (nodeLogTimer) {
    clearInterval(nodeLogTimer)
    nodeLogTimer = null
  }
}

const stopPodLogStream = () => {
  if (podLogTimer) {
    clearInterval(podLogTimer)
    podLogTimer = null
  }
}

// 清空日志
const clearLogs = () => {
  clusterLogs.value = []
}

const clearNodeLogs = () => {
  nodeLogs.value = []
}

const clearPodLogs = () => {
  podLogs.value = []
}

// 组件卸载时清理定时器
onUnmounted(() => {
  stopClusterLogStream()
  stopNodeLogStream()
  stopPodLogStream()
})

const getLogLevelColor = (level: string) => {
  switch (level) {
    case 'DEBUG':
      return 'blue'
    case 'INFO':
      return 'green'
    case 'WARN':
      return 'orange'
    case 'ERROR':
      return 'red'
    default:
      return 'gray'
  }
}
</script>

<style scoped>
.k8s-page {
  padding: 0;
}

.stats-row {
  margin-bottom: 24px;
}

.cluster-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.cluster-avatar {
  background: #1890ff;
}

.cluster-details {
  flex: 1;
}

.cluster-name {
  font-weight: 500;
  color: #1d2129;
  margin-bottom: 2px;
}

.cluster-version {
  font-size: 12px;
  color: #86909c;
}

.cluster-tabs {
  margin-top: 0;
}

.cluster-table {
  margin-top: 16px;
}

.node-table,
.pod-table {
  margin-top: 16px;
}

.node-info,
.pod-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.node-avatar {
  background: #52c41a;
}

.pod-avatar {
  background: #1890ff;
}

.node-details,
.pod-details {
  flex: 1;
}

.node-name,
.pod-name {
  font-weight: 500;
  color: #1d2129;
  margin-bottom: 2px;
}

.node-ip,
.pod-namespace {
  font-size: 12px;
  color: #86909c;
}

.resource-info {
  font-size: 12px;
  line-height: 1.4;
}

.resource-info div {
  margin-bottom: 2px;
}

.chart-placeholder {
  height: 300px;
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

.log-container {
  height: 400px;
  display: flex;
  flex-direction: column;
}

.log-header {
  padding: 12px 0;
  border-bottom: 1px solid #e5e6eb;
  margin-bottom: 12px;
}

.log-content {
  flex: 1;
  background: #1e1e1e;
  color: #ffffff;
  font-family: 'Courier New', monospace;
  font-size: 12px;
  line-height: 1.5;
  padding: 12px;
  border-radius: 4px;
  overflow-y: auto;
  max-height: 350px;
}

.log-line {
  margin-bottom: 4px;
  word-wrap: break-word;
}

.log-time {
  color: #86909c;
  margin-right: 8px;
}

.log-level {
  font-weight: bold;
  margin-right: 8px;
  padding: 2px 6px;
  border-radius: 2px;
  font-size: 11px;
}

.log-level.info {
  background: #52c41a;
  color: white;
}

.log-level.debug {
  background: #1890ff;
  color: white;
}

.log-level.warn {
  background: #faad14;
  color: white;
}

.log-level.error {
  background: #ff4d4f;
  color: white;
}

.log-message {
  color: #ffffff;
}

:deep(.arco-modal-body) {
  max-height: 70vh;
  overflow-y: auto;
}

:deep(.arco-descriptions-item-label) {
  background: #f7f8fa;
}

:deep(.arco-card) {
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

:deep(.arco-tabs-content) {
  padding-top: 0;
}
</style>
