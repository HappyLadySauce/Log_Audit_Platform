<template>
  <div class="k8s-page">
    <PageHeader title="K8s集群日志" description="管理和监控Kubernetes集群的日志采集">
      <template #extra>
        <a-space>
          <a-button>
            <template #icon>
              <icon-refresh />
            </template>
            刷新
          </a-button>
          <a-button type="primary" @click="showAddClusterModal">
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
          :value="clusterCount"
          label="集群数量"
          subtitle="K8s集群"
        />
      </a-col>
      <a-col :span="6">
        <StatCard
          :icon="IconApps"
          icon-bg-color="#52c41a"
          :value="podCount"
          label="Pod数量"
          subtitle="运行中"
        />
      </a-col>
      <a-col :span="6">
        <StatCard
          :icon="IconFile"
          icon-bg-color="#faad14"
          :value="logCount"
          label="今日日志"
          subtitle="条数统计"
        />
      </a-col>
      <a-col :span="6">
        <StatCard
          :icon="IconStorage"
          icon-bg-color="#722ed1"
          :value="storageSize"
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
                <a-button type="text" size="small" @click="showClusterDetail(record)"
                  >查看日志详情</a-button
                >
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
              <a-tag :color="record.nodeType === 'control-plane' ? 'blue' : 'green'" size="small">
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
                <a-button type="text" size="small" @click="showNodeDetail(record)"
                  >查看详情</a-button
                >
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
            <a-descriptions-item label="API端点">{{
              selectedCluster?.endpoint
            }}</a-descriptions-item>
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

    <!-- Pod详情模态框 - 单页面布局 -->
    <a-modal
      v-model:visible="podDetailVisible"
      :title="`Pod详情 - ${selectedPod?.podName}`"
      width="1400px"
      :footer="false"
      :body-style="{ padding: '24px' }"
      @cancel="closePodDetail"
    >
      <div class="pod-detail-container">
        <!-- 基本信息区域 -->
        <div class="detail-section">
          <h3 class="section-title">基本信息</h3>
          <a-descriptions :column="3" bordered size="small">
            <a-descriptions-item label="Pod名称">{{ selectedPod?.podName }}</a-descriptions-item>
            <a-descriptions-item label="命名空间">{{ selectedPod?.namespace }}</a-descriptions-item>
            <a-descriptions-item label="节点IP">{{
              selectedPod?.nodeIP || selectedPod?.node
            }}</a-descriptions-item>
            <a-descriptions-item label="Pod IP">{{
              selectedPod?.podIP || 'N/A'
            }}</a-descriptions-item>
            <a-descriptions-item label="状态">
              <a-badge
                :status="selectedPod?.status === 'Running' ? 'success' : 'error'"
                :text="selectedPod?.status"
              />
            </a-descriptions-item>
            <a-descriptions-item label="重启次数">{{ selectedPod?.restarts }}</a-descriptions-item>
            <a-descriptions-item label="镜像">{{ selectedPod?.image }}</a-descriptions-item>
            <a-descriptions-item label="创建时间">{{
              selectedPod?.createdTime
            }}</a-descriptions-item>
            <a-descriptions-item label="UID">{{ selectedPod?.uid }}</a-descriptions-item>
            <a-descriptions-item label="CPU使用率">
              <!-- 变大 -->
              <span style="font-size: 40px; color: #52c41a" class="usage-text"
                >{{ selectedPod?.cpu }}%</span
              >
            </a-descriptions-item>
            <a-descriptions-item label="内存使用率">
              <span style="font-size: 40px; color: #52c41a" class="usage-text"
                >{{ selectedPod?.memory }}%</span
              >
            </a-descriptions-item>
            <a-descriptions-item label="标签">
              <div class="labels-container">
                <a-tag
                  v-for="(value, key) in selectedPod?.labels"
                  :key="key"
                  color="blue"
                  size="small"
                  class="label-tag"
                >
                  {{ key }}: {{ value }}
                </a-tag>
              </div>
            </a-descriptions-item>
          </a-descriptions>
        </div>

        <!-- 容器详情区域 -->
        <div class="detail-section">
          <h3 class="section-title">容器详情</h3>
          <a-table
            :columns="containerColumns"
            :data="selectedPod?.containers || []"
            :pagination="false"
            size="small"
            class="container-table"
          >
            <template #containerName="{ record }">
              <div class="container-info">
                <a-avatar size="small" class="container-avatar">
                  <icon-apps />
                </a-avatar>
                <div class="container-details">
                  <div class="container-name">{{ record.name }}</div>
                  <div class="container-image">{{ record.image }}</div>
                </div>
              </div>
            </template>

            <template #status="{ record }">
              <a-badge
                :status="record.status === 'Running' ? 'success' : 'error'"
                :text="record.status"
              />
            </template>

            <template #ready="{ record }">
              <a-tag :color="record.ready ? 'green' : 'red'" size="small">
                {{ record.ready ? '就绪' : '未就绪' }}
              </a-tag>
            </template>

            <template #ports="{ record }">
              <div class="ports-container">
                <a-tag
                  v-for="port in record.ports"
                  :key="port"
                  color="blue"
                  size="small"
                  class="port-tag"
                >
                  {{ port }}
                </a-tag>
                <span v-if="record.ports.length === 0" class="no-ports">无端口</span>
              </div>
            </template>

            <template #resources="{ record }">
              <div class="resource-details">
                <div class="resource-section">
                  <strong>请求:</strong>
                  <div>CPU: {{ record.resources?.requests?.cpu || 'N/A' }}</div>
                  <div>内存: {{ record.resources?.requests?.memory || 'N/A' }}</div>
                </div>
                <div class="resource-section">
                  <strong>限制:</strong>
                  <div>CPU: {{ record.resources?.limits?.cpu || 'N/A' }}</div>
                  <div>内存: {{ record.resources?.limits?.memory || 'N/A' }}</div>
                </div>
              </div>
            </template>
          </a-table>
        </div>

        <!-- 实时日志区域 -->
        <div class="detail-section">
          <h3 class="section-title">实时日志</h3>
          <div class="log-container">
            <div class="log-header">
              <a-space>
                <a-tag color="green">
                  <template #icon>
                    <icon-check-circle />
                  </template>
                  实时采集中
                </a-tag>
                <span class="log-count">日志条数: {{ podLogs.length }}</span>
              </a-space>
            </div>
            <div class="log-content" ref="podLogRef">
              <div v-for="(log, index) in podLogs" :key="index" class="log-line">
                <span class="log-time">{{ log.timestamp }}</span>
                <span :class="`log-level ${log.level.toLowerCase()}`">{{ log.level }}</span>
                <span class="log-message">{{ log.content }}</span>
              </div>
              <div v-if="podLogs.length === 0" class="log-empty">
                <icon-file style="font-size: 48px; color: #c9cdd4" />
                <p>正在初始化日志采集...</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </a-modal>

    <!-- 接入新集群模态框 -->
    <a-modal
      v-model:visible="addClusterVisible"
      title="接入新集群"
      width="650px"
      :ok-loading="connecting"
      @ok="addCluster"
      @cancel="cancelAddCluster"
    >
      <a-form ref="addClusterFormRef" :model="addClusterForm" layout="vertical">
        <a-form-item
          label="集群名称"
          field="name"
          :rules="[{ required: true, message: '请输入集群名称' }]"
        >
          <a-input
            v-model="addClusterForm.name"
            placeholder="例如：分部K8S集群"
            :disabled="connecting"
          />
        </a-form-item>

        <a-form-item
          label="Kubeconfig 配置文件"
          field="kubeconfig"
          :rules="[{ required: true, message: '请粘贴kubeconfig配置文件' }]"
        >
          <a-textarea
            v-model="addClusterForm.kubeconfig"
            placeholder="请粘贴完整的 kubeconfig 内容..."
            :rows="25"
            :disabled="connecting"
            @input="onKubeconfigInput"
            :style="{
              fontSize: '13px',
              lineHeight: '1.5',
              minHeight: '500px',
              height: '500px',
            }"
          />
        </a-form-item>

        <div v-if="connecting" class="connecting-status">
          <a-spin />
          <span>正在解析配置并验证连接...</span>
        </div>

        <div v-if="kubeconfigPreview" class="config-preview">
          <h4>配置预览</h4>
          <a-descriptions :column="1" size="small" bordered>
            <a-descriptions-item label="集群地址">{{
              kubeconfigPreview.server
            }}</a-descriptions-item>
            <a-descriptions-item label="集群名称">{{
              kubeconfigPreview.clusterName
            }}</a-descriptions-item>
            <a-descriptions-item label="用户">{{ kubeconfigPreview.user }}</a-descriptions-item>
          </a-descriptions>
        </div>
      </a-form>
    </a-modal>
  </div>
</template>

<script setup lang="ts">
import { ref, nextTick, onUnmounted, computed } from 'vue'
import { Message } from '@arco-design/web-vue'
import PageHeader from '@/components/PageHeader.vue'
import StatCard from '@/components/StatCard.vue'
import DashboardChart from '@/components/DashboardChart.vue'
import {
  IconRefresh,
  IconPlus,
  IconCloud,
  IconApps,
  IconFile,
  IconStorage,
  IconSettings,
  IconDesktop,
  IconCheckCircle,
  IconInfo,
} from '@arco-design/web-vue/es/icon'

// 集群数据 - 初始为空
const clusterData = ref<any[]>([])

// 统计数据
const clusterCount = computed(() => clusterData.value.length)
const podCount = computed(() =>
  clusterData.value.reduce((sum, cluster) => sum + (cluster.pods || 0), 0),
)
const logCount = ref(0)
const storageSize = ref(0)

// 接入新集群相关
const addClusterVisible = ref(false)
const connecting = ref(false)
const addClusterForm = ref({
  name: '',
  kubeconfig: '',
})
const addClusterFormRef = ref()
const kubeconfigPreview = ref<any>(null)

// 节点数据 - 初始为空
const nodeData = ref<any[]>([])

// Pod数据 - 初始为空
const podData = ref<any[]>([])

// 表格列配置
const clusterColumns = [
  {
    title: '集群信息',
    dataIndex: 'name',
    slotName: 'clusterInfo',
    width: 200,
  },
  {
    title: '节点数',
    dataIndex: 'nodes',
    width: 80,
  },
  {
    title: 'Pod数',
    dataIndex: 'pods',
    width: 80,
  },
  {
    title: '状态',
    dataIndex: 'status',
    slotName: 'status',
    width: 100,
  },
  {
    title: '日志级别',
    dataIndex: 'logLevel',
    slotName: 'logLevel',
    width: 100,
  },
  {
    title: 'API端点',
    dataIndex: 'endpoint',
    width: 250,
  },
  {
    title: '操作',
    slotName: 'actions',
    width: 200,
    fixed: 'right',
  },
]

// 节点表格列配置
const nodeColumns = [
  {
    title: '节点名称',
    dataIndex: 'nodeName',
    slotName: 'nodeName',
    width: 200,
  },
  {
    title: '节点类型',
    dataIndex: 'nodeType',
    slotName: 'nodeType',
    width: 120,
  },
  {
    title: '系统版本',
    dataIndex: 'system',
    width: 120,
  },
  {
    title: '状态',
    dataIndex: 'status',
    slotName: 'status',
    width: 80,
  },
  {
    title: '资源使用',
    dataIndex: 'resources',
    slotName: 'resources',
    width: 120,
  },
  {
    title: '操作',
    slotName: 'actions',
    width: 120,
    fixed: 'right',
  },
]

// Pod表格列配置
const podColumns = [
  {
    title: 'Pod名称',
    dataIndex: 'podName',
    slotName: 'podName',
    width: 250,
  },
  {
    title: '命名空间',
    dataIndex: 'namespace',
    width: 100,
  },
  {
    title: '节点',
    dataIndex: 'node',
    width: 120,
  },
  {
    title: '状态',
    dataIndex: 'status',
    slotName: 'status',
    width: 80,
  },
  {
    title: '重启次数',
    dataIndex: 'restarts',
    width: 80,
  },
  {
    title: '资源使用',
    dataIndex: 'resources',
    slotName: 'resources',
    width: 120,
  },
  {
    title: '创建时间',
    dataIndex: 'createdTime',
    width: 150,
  },
  {
    title: '操作',
    slotName: 'actions',
    width: 180,
    fixed: 'right',
  },
]

// 容器表格列配置
const containerColumns = [
  {
    title: '容器名称',
    dataIndex: 'name',
    slotName: 'containerName',
    width: 200,
  },
  {
    title: '状态',
    dataIndex: 'status',
    slotName: 'status',
    width: 80,
  },
  {
    title: '就绪状态',
    dataIndex: 'ready',
    slotName: 'ready',
    width: 80,
  },
  {
    title: '重启次数',
    dataIndex: 'restarts',
    width: 80,
  },
  {
    title: '端口',
    dataIndex: 'ports',
    slotName: 'ports',
    width: 120,
  },
  {
    title: '资源配置',
    dataIndex: 'resources',
    slotName: 'resources',
    width: 200,
  },
]

// 事件表格列配置
const eventColumns = [
  {
    title: '类型',
    dataIndex: 'type',
    slotName: 'eventType',
    width: 80,
  },
  {
    title: '原因',
    dataIndex: 'reason',
    width: 120,
  },
  {
    title: '消息',
    dataIndex: 'message',
    width: 400,
  },
  {
    title: '时间',
    dataIndex: 'time',
    width: 150,
  },
]

// 事件数据
const eventData = ref([
  {
    key: '1',
    type: 'Normal',
    reason: 'Scheduled',
    message: 'Successfully assigned kubesphere-system/extensions-museum-xxx to control-plane-1',
    time: '2025-06-17 19:03:15',
  },
  {
    key: '2',
    type: 'Normal',
    reason: 'Pulled',
    message: 'Container image "kubesphere/extensions-museum:v3.4.1" already present on machine',
    time: '2025-06-17 19:03:18',
  },
  {
    key: '3',
    type: 'Normal',
    reason: 'Created',
    message: 'Created container extensions-museum',
    time: '2025-06-17 19:03:19',
  },
  {
    key: '4',
    type: 'Normal',
    reason: 'Started',
    message: 'Started container extensions-museum',
    time: '2025-06-17 19:03:20',
  },
  {
    key: '5',
    type: 'Normal',
    reason: 'Killing',
    message: 'Stopping container extensions-museum',
    time: '2025-06-17 15:22:10',
  },
  {
    key: '6',
    type: 'Warning',
    reason: 'BackOff',
    message: 'Back-off restarting failed container',
    time: '2025-06-17 12:15:30',
  },
  {
    key: '7',
    type: 'Normal',
    reason: 'SuccessfulMountVolume',
    message: 'MountVolume.SetUp succeeded for volume "kube-api-access-token"',
    time: '2025-06-17 19:03:16',
  },
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
const podLogs = ref<
  Array<{
    timestamp: string
    level: string
    content: string
  }>
>([])

// 日志流状态
const logStreamActive = ref(false)
const nodeLogStreamActive = ref(false)
const podLogStreamActive = ref(false)
const podLogInitialized = ref(false)

// 日志容器引用
const clusterLogRef = ref<HTMLElement>()
const nodeLogRef = ref<HTMLElement>()
const podLogRef = ref<HTMLElement>()

// 定时器
let clusterLogTimer: any = null
let nodeLogTimer: any = null
let podLogTimer: any = null

// Pod资源监控数据
const cpuChartData = computed(() =>
  ['14:30', '14:35', '14:40', '14:45', '14:50', '14:55'].map((time, index) => ({
    name: time,
    value: [45, 52, 48, 65, 78, 82][index],
  })),
)

const memoryChartData = computed(() =>
  ['14:30', '14:35', '14:40', '14:45', '14:50', '14:55'].map((time, index) => ({
    name: time,
    value: [62, 68, 71, 75, 80, 82][index],
  })),
)

const networkChartData = computed(() =>
  ['14:30', '14:35', '14:40', '14:45', '14:50', '14:55'].map((time, index) => ({
    name: time,
    value: [120, 135, 142, 158, 165, 172][index], // 入站流量 KB/s
  })),
)

const diskChartData = computed(() =>
  ['14:30', '14:35', '14:40', '14:45', '14:50', '14:55'].map((time, index) => ({
    name: time,
    value: [25, 32, 28, 35, 42, 38][index], // 磁盘读取 MB/s
  })),
)

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

  // 自动开始实时日志流
  podLogStreamActive.value = true
  startPodLogStream()
}

// 关闭Pod详情
const closePodDetail = () => {
  podDetailVisible.value = false
  podLogStreamActive.value = false
  stopPodLogStream()
}

// 初始化集群日志
const initClusterLogs = () => {
  clusterLogs.value = [
    {
      time: '2024-01-15 10:35:18',
      level: 'INFO',
      message: '分部k8s-02集群(10.10.20.2) - 集群状态正常，40个Pod全部运行中',
    },
    {
      time: '2024-01-15 10:35:15',
      level: 'DEBUG',
      message: '分部k8s-02节点状态检查完成，4个节点全部在线',
    },
    {
      time: '2024-01-15 10:35:12',
      level: 'INFO',
      message: '分部k8s-02 Pod调度成功，新增服务实例3个',
    },
  ]
}

// 初始化节点日志
const initNodeLogs = () => {
  nodeLogs.value = [
    {
      time: '2024-01-15 10:35:18',
      level: 'INFO',
      message: `${selectedNode.value?.nodeName}(${selectedNode.value?.ip}) - 节点状态正常，资源充足`,
    },
    {
      time: '2024-01-15 10:35:15',
      level: 'DEBUG',
      message: `${selectedNode.value?.nodeName} - 系统资源检查完成，CPU使用率: ${selectedNode.value?.cpu}%`,
    },
    {
      time: '2024-01-15 10:35:12',
      level: 'INFO',
      message: `${selectedNode.value?.nodeName} - kubelet服务运行正常，网络连接稳定`,
    },
  ]
}

// 生成Pod初始化日志（仿servers.vue）
const generatePodInitLogs = (): Array<{ timestamp: string; level: string; content: string }> => {
  const now = new Date()
  const baseTime = now.getTime()
  const logs: Array<{ timestamp: string; level: string; content: string }> = []

  // 模拟应用启动过程的时间间隔
  const intervals = [0, 500, 800, 1200, 1500, 2000, 2200, 2500]

  const initContents = [
    `time="${new Date(baseTime).toLocaleString('zh-CN').replace(/\//g, '-')}+08:00" level=info msg="[Database] 尝试连接应用数据库"`,
    `[3.566ms] [rows:-] SELECT DATABASE()`,
    `[7.568ms] [rows:1] SELECT SCHEMA_NAME from Information_schema.SCHEMATA`,
    `time="${new Date(baseTime + 1000).toLocaleString('zh-CN').replace(/\//g, '-')}+08:00" level=info msg="[Database] 应用数据库已连接"`,
    `time="${new Date(baseTime + 1200).toLocaleString('zh-CN').replace(/\//g, '-')}+08:00" level=info msg="[Session Cache] 尝试连接redis服务器"`,
    `time="${new Date(baseTime + 1500).toLocaleString('zh-CN').replace(/\//g, '-')}+08:00" level=info msg="[Session Cache] redis已连接"`,
    `[GIN-debug] [WARNING] Running in "debug" mode. Switch to "release" mode in production.`,
    `[GIN-debug] Listening and serving HTTP on :20000`,
  ]

  initContents.forEach((content, index) => {
    const logTime = new Date(baseTime + intervals[index])
    logs.push({
      timestamp: logTime.toLocaleString('zh-CN', {
        hour12: false,
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit',
      }),
      level: content.includes('level=info') ? 'INFO' : 'DEBUG',
      content,
    })
  })

  return logs
}

// 初始化Pod日志
const initPodLogs = () => {
  podLogs.value = []
  podLogInitialized.value = false

  // 先显示初始化日志
  const initLogs = generatePodInitLogs()
  podLogs.value.push(...initLogs)
  podLogInitialized.value = true
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
    const time = now
      .toLocaleString('zh-CN', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit',
      })
      .replace(/\//g, '-')

    const messages = [
      '集群健康检查通过，所有组件运行正常',
      'etcd集群状态健康，数据同步完成',
      'API Server响应正常，延迟8ms',
      'Scheduler调度器工作正常',
      'Controller Manager状态良好',
    ]

    const levels = ['INFO', 'DEBUG', 'WARN']
    const randomMessage = messages[Math.floor(Math.random() * messages.length)]
    const randomLevel = levels[Math.floor(Math.random() * levels.length)]

    clusterLogs.value.push({
      time,
      level: randomLevel,
      message: `分部k8s-02集群 - ${randomMessage}`,
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
    const time = now
      .toLocaleString('zh-CN', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit',
      })
      .replace(/\//g, '-')

    const messages = [
      'kubelet服务运行正常',
      '容器运行时状态良好',
      '网络插件工作正常',
      '磁盘空间充足',
      '系统负载正常',
    ]

    const levels = ['INFO', 'DEBUG']
    const randomMessage = messages[Math.floor(Math.random() * messages.length)]
    const randomLevel = levels[Math.floor(Math.random() * levels.length)]

    nodeLogs.value.push({
      time,
      level: randomLevel,
      message: `${selectedNode.value?.nodeName} - ${randomMessage}`,
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

// 生成Pod运行时日志（仿servers.vue）
const generatePodMockLog = (): { timestamp: string; level: string; content: string } => {
  const now = new Date()
  const timestamp = now.toLocaleString('zh-CN', {
    hour12: false,
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit',
  })

  const levels = ['INFO', 'DEBUG']
  const level = levels[Math.floor(Math.random() * levels.length)]

  const httpRequests = [
    `GET    /api/v1/ping`,
    `GET    /api/v1/user/list`,
    `GET    /api/v1/user/info`,
    `GET    /api/v1/user/captcha`,
    `GET    /api/v1/assets`,
    `GET    /api/v1/logs`,
    `GET    /health`,
  ]

  const mockContents = [
    `[GIN] ${timestamp.replace(/\//g, '-')} - ${timestamp.split(' ')[1]} | 200 | ${Math.floor(Math.random() * 30 + 5)}.${Math.floor(Math.random() * 999)}ms | 172.17.0.1 | ${httpRequests[Math.floor(Math.random() * httpRequests.length)]}`,
  ]

  const content = mockContents[Math.floor(Math.random() * mockContents.length)]
  return { timestamp, level, content }
}

// 添加新的Pod日志
const addPodNewLog = () => {
  if (!podLogStreamActive.value) return

  const newLog = generatePodMockLog()
  podLogs.value.push(newLog)

  // 限制日志行数，避免过多日志影响性能
  if (podLogs.value.length > 200) {
    podLogs.value.shift()
  }

  // 自动滚动到底部
  nextTick(() => {
    if (podLogRef.value) {
      podLogRef.value.scrollTop = podLogRef.value.scrollHeight
    }
  })
}

// 开始Pod日志流
const startPodLogStream = () => {
  podLogTimer = setInterval(() => {
    addPodNewLog()
  }, 2000)
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
  podLogInitialized.value = false

  // 重新显示初始化日志
  const initLogs = generatePodInitLogs()
  podLogs.value.push(...initLogs)
  podLogInitialized.value = true
}

// 接入新集群相关方法
const showAddClusterModal = () => {
  console.log('点击了添加集群按钮')
  addClusterVisible.value = true
  addClusterForm.value = {
    name: '',
    kubeconfig: '',
  }
  kubeconfigPreview.value = null
}

// kubeconfig输入处理
const onKubeconfigInput = () => {
  if (addClusterForm.value.kubeconfig.trim()) {
    parseKubeconfig(addClusterForm.value.kubeconfig)
  } else {
    kubeconfigPreview.value = null
  }
}

// 解析kubeconfig配置
const parseKubeconfig = (kubeconfigContent: string) => {
  try {
    // 模拟解析kubeconfig内容
    const lines = kubeconfigContent.split('\n')
    let server = 'https://10.10.20.2:6443'
    let clusterName = '分部K8S集群'
    let user = 'kubernetes-admin'

    // 简单解析server地址
    for (const line of lines) {
      if (line.includes('server:')) {
        const match = line.match(/server:\s*(.+)/)
        if (match) {
          server = match[1].trim()
        }
      } else if (line.includes('name:') && line.includes('cluster')) {
        const match = line.match(/name:\s*(.+)/)
        if (match) {
          clusterName = match[1].trim()
        }
      } else if (line.includes('name:') && line.includes('user')) {
        const match = line.match(/name:\s*(.+)/)
        if (match) {
          user = match[1].trim()
        }
      }
    }

    kubeconfigPreview.value = {
      server,
      clusterName,
      user,
    }
  } catch (error) {
    console.error('解析kubeconfig失败:', error)
  }
}

const cancelAddCluster = () => {
  addClusterVisible.value = false
  connecting.value = false
  kubeconfigPreview.value = null
  if (addClusterFormRef.value) {
    addClusterFormRef.value.resetFields()
  }
}

const addCluster = async () => {
  if (!addClusterFormRef.value) return

  const errors = await addClusterFormRef.value.validate()
  if (errors) return

  // 开始连接过程
  connecting.value = true

  try {
    // 模拟连接验证过程
    await new Promise((resolve) => setTimeout(resolve, 3000))

    // 添加新集群到列表
    const endpoint = kubeconfigPreview.value?.server || 'https://10.10.20.2:6443'
    const newCluster = {
      key: Date.now().toString(),
      name: addClusterForm.value.name,
      version: 'v1.28.2',
      nodes: 4,
      pods: 13, // 实际添加的Pod数量
      status: 'running',
      logLevel: 'INFO',
      endpoint: endpoint,
    }

    clusterData.value.push(newCluster)

    // 添加对应的节点数据
    let baseIP = '10.10.20.2'
    try {
      const url = new URL(endpoint)
      baseIP = url.hostname
    } catch (e) {
      // 如果URL解析失败，使用默认IP
      console.warn('URL解析失败，使用默认IP', e)
    }

    const nodeList = [
      {
        key: `${newCluster.key}-node-1`,
        nodeName: `${addClusterForm.value.name}控制节点1`,
        ip: baseIP,
        nodeType: 'control-plane',
        system: 'Ubuntu 22.04',
        status: '在线',
        cpu: 45,
        memory: 62,
      },
      {
        key: `${newCluster.key}-node-2`,
        nodeName: `${addClusterForm.value.name}控制节点2`,
        ip: getNextIP(baseIP),
        nodeType: 'control-plane',
        system: 'Ubuntu 22.04',
        status: '在线',
        cpu: 38,
        memory: 55,
      },
      {
        key: `${newCluster.key}-node-3`,
        nodeName: `${addClusterForm.value.name}工作节点1`,
        ip: getNextIP(baseIP, 2),
        nodeType: 'worker',
        system: 'Ubuntu 22.04',
        status: '在线',
        cpu: 72,
        memory: 68,
      },
      {
        key: `${newCluster.key}-node-4`,
        nodeName: `${addClusterForm.value.name}工作节点2`,
        ip: getNextIP(baseIP, 3),
        nodeType: 'worker',
        system: 'Ubuntu 22.04',
        status: '在线',
        cpu: 58,
        memory: 71,
      },
    ]

    nodeData.value.push(...nodeList)

    // 添加一些Pod数据 - 基于真实数据
    const podList = [
      // app-deployment 金融审批平台的两个副本
      {
        key: `${newCluster.key}-pod-1`,
        podName: 'app-deployment-c958c4d7b-r8wr2',
        namespace: 'default',
        node: 'k8s2-node01.k8s.cn',
        status: 'Running',
        restarts: 0,
        cpu: 15,
        memory: 35,
        createdTime: '2025-06-19 02:48:50',
        image: 'app:v4',
        uid: 'a1b2c3d4-e5f6-7890-abcd-ef1234567890',
        podIP: '10.244.20.77',
        nodeIP: '10.10.20.4',
        containers: [
          {
            name: 'app-deployment',
            image: 'app:v4',
            status: 'Running',
            ready: true,
            restarts: 0,
            ports: [8080, 9090],
            resources: {
              requests: { cpu: '200m', memory: '256Mi' },
              limits: { cpu: '1000m', memory: '1Gi' },
            },
          },
        ],
        labels: {
          app: 'app-deployment',
          version: 'v1.2.3',
          tier: 'frontend',
          'app.kubernetes.io/name': 'finance-approval-platform',
        },
        annotations: {
          'deployment.kubernetes.io/revision': '1',
          'kubesphere.io/creator': 'admin',
          'kubesphere.io/description': '金融审批平台',
        },
      },
      {
        key: `${newCluster.key}-pod-2`,
        podName: 'app-deployment-c958c4d7b-csz4g',
        namespace: 'default',
        node: 'k8s2-node02.k8s.cn',
        status: 'Running',
        restarts: 0,
        cpu: 18,
        memory: 42,
        createdTime: '2025-06-19 02:48:50',
        image: 'app:v4',
        uid: 'b2c3d4e5-f6g7-8901-bcde-fg2345678901',
        podIP: '10.244.87.161',
        nodeIP: '10.10.20.5',
        containers: [
          {
            name: 'app-deployment',
            image: 'app:v4',
            status: 'Running',
            ready: true,
            restarts: 0,
            ports: [8080, 9090],
            resources: {
              requests: { cpu: '200m', memory: '256Mi' },
              limits: { cpu: '1000m', memory: '1Gi' },
            },
          },
        ],
        labels: {
          app: 'app-deployment',
          version: 'v1.2.3',
          tier: 'frontend',
          'app.kubernetes.io/name': 'finance-approval-platform',
        },
        annotations: {
          'deployment.kubernetes.io/revision': '1',
          'kubesphere.io/creator': 'admin',
          'kubesphere.io/description': '金融审批平台',
        },
      },
      // ks-controller-manager
      {
        key: `${newCluster.key}-pod-3`,
        podName: 'ks-controller-manager-7f8b9c6d4e-xm9w3',
        namespace: 'kubesphere-system',
        node: 'k8s2-node01.k8s.cn',
        status: 'Running',
        restarts: 0,
        cpu: 25,
        memory: 80,
        createdTime: '2025-06-18 17:19:01',
        image: 'kubesphere/ks-controller-manager:v3.4.1',
        uid: 'c3d4e5f6-g7h8-9012-cdef-gh3456789012',
        podIP: '10.244.20.78',
        nodeIP: '10.10.20.4',
        containers: [
          {
            name: 'ks-controller-manager',
            image: 'kubesphere/ks-controller-manager:v3.4.1',
            status: 'Running',
            ready: true,
            restarts: 0,
            ports: [8080, 8443],
            resources: {
              requests: { cpu: '100m', memory: '128Mi' },
              limits: { cpu: '1000m', memory: '1Gi' },
            },
          },
        ],
        labels: {
          app: 'ks-controller-manager',
          tier: 'control-plane',
          version: 'v3.4.1',
        },
        annotations: {
          'deployment.kubernetes.io/revision': '1',
          'kubesphere.io/creator': 'system',
        },
      },
      // tigera-operator
      {
        key: `${newCluster.key}-pod-4`,
        podName: 'tigera-operator-6b8c9d7e5f-yn4x8',
        namespace: 'tigera-operator',
        node: 'k8s2-node01.k8s.cn',
        status: 'Running',
        restarts: 0,
        cpu: 12,
        memory: 85,
        createdTime: '2025-06-18 17:18:21',
        image: 'quay.io/tigera/operator:v1.30.4',
        uid: 'd4e5f6g7-h8i9-0123-defg-hi4567890123',
        podIP: '10.244.20.79',
        nodeIP: '10.10.20.4',
        containers: [
          {
            name: 'tigera-operator',
            image: 'quay.io/tigera/operator:v1.30.4',
            status: 'Running',
            ready: true,
            restarts: 0,
            ports: [9443],
            resources: {
              requests: { cpu: '100m', memory: '128Mi' },
              limits: { cpu: '500m', memory: '512Mi' },
            },
          },
        ],
        labels: {
          'k8s-app': 'tigera-operator',
          version: 'v1.30.4',
        },
        annotations: {
          'deployment.kubernetes.io/revision': '1',
        },
      },
      // calico-apiserver
      {
        key: `${newCluster.key}-pod-5`,
        podName: 'calico-apiserver-7c9d8e6f4a-zp5y9',
        namespace: 'calico-apiserver',
        node: 'k8s2-node02.k8s.cn',
        status: 'Running',
        restarts: 0,
        cpu: 20,
        memory: 95,
        createdTime: '2025-06-18 17:18:18',
        image: 'calico/apiserver:v3.26.1',
        uid: 'e5f6g7h8-i9j0-1234-efgh-ij5678901234',
        podIP: '10.244.87.162',
        nodeIP: '10.10.20.5',
        containers: [
          {
            name: 'calico-apiserver',
            image: 'calico/apiserver:v3.26.1',
            status: 'Running',
            ready: true,
            restarts: 0,
            ports: [5443],
            resources: {
              requests: { cpu: '100m', memory: '128Mi' },
              limits: { cpu: '500m', memory: '512Mi' },
            },
          },
        ],
        labels: {
          'k8s-app': 'calico-apiserver',
          version: 'v3.26.1',
        },
        annotations: {
          'deployment.kubernetes.io/revision': '1',
        },
      },
      // ingress-nginx-controller
      {
        key: `${newCluster.key}-pod-6`,
        podName: 'ingress-nginx-controller-8a0e9f7d5b-aq6z0',
        namespace: 'ingress-nginx',
        node: 'k8s2-node01.k8s.cn',
        status: 'Running',
        restarts: 0,
        cpu: 35,
        memory: 40,
        createdTime: '2025-06-18 10:08:40',
        image: 'registry.k8s.io/ingress-nginx/controller:v1.8.1',
        uid: 'f6g7h8i9-j0k1-2345-fghi-jk6789012345',
        podIP: '10.244.20.80',
        nodeIP: '10.10.20.4',
        containers: [
          {
            name: 'controller',
            image: 'registry.k8s.io/ingress-nginx/controller:v1.8.1',
            status: 'Running',
            ready: true,
            restarts: 0,
            ports: [80, 443, 8443],
            resources: {
              requests: { cpu: '100m', memory: '90Mi' },
              limits: { cpu: '1000m', memory: '1Gi' },
            },
          },
        ],
        labels: {
          app: 'ingress-nginx-controller',
          version: 'v1.8.1',
        },
        annotations: {
          'deployment.kubernetes.io/revision': '1',
        },
      },
      // extensions-museum
      {
        key: `${newCluster.key}-pod-7`,
        podName: 'extensions-museum-5f7b8c6d9b-xk8v2',
        namespace: 'kubesphere-system',
        node: 'k8s2-node02.k8s.cn',
        status: 'Running',
        restarts: 0,
        cpu: 8,
        memory: 65,
        createdTime: '2025-06-18 09:38:00',
        image: 'kubesphere/extensions-museum:v3.4.1',
        uid: 'g7h8i9j0-k1l2-3456-ghij-kl7890123456',
        podIP: '10.244.87.163',
        nodeIP: '10.10.20.5',
        containers: [
          {
            name: 'extensions-museum',
            image: 'kubesphere/extensions-museum:v3.4.1',
            status: 'Running',
            ready: true,
            restarts: 0,
            ports: [8080],
            resources: {
              requests: { cpu: '100m', memory: '128Mi' },
              limits: { cpu: '500m', memory: '512Mi' },
            },
          },
        ],
        labels: {
          app: 'extensions-museum',
          version: 'v3.4.1',
          tier: 'backend',
        },
        annotations: {
          'deployment.kubernetes.io/revision': '1',
          'kubesphere.io/creator': 'admin',
        },
      },
      // karmada-agent
      {
        key: `${newCluster.key}-pod-8`,
        podName: 'karmada-agent-6d8f7e5c4a-bq7w1',
        namespace: 'karmada-system',
        node: 'k8s2-node02.k8s.cn',
        status: 'Running',
        restarts: 0,
        cpu: 15,
        memory: 75,
        createdTime: '2025-06-18 09:37:59',
        image: 'karmada/karmada-agent:v1.7.0',
        uid: 'h8i9j0k1-l2m3-4567-hijk-lm8901234567',
        podIP: '10.244.87.164',
        nodeIP: '10.10.20.5',
        containers: [
          {
            name: 'karmada-agent',
            image: 'karmada/karmada-agent:v1.7.0',
            status: 'Running',
            ready: true,
            restarts: 0,
            ports: [10357],
            resources: {
              requests: { cpu: '100m', memory: '128Mi' },
              limits: { cpu: '500m', memory: '512Mi' },
            },
          },
        ],
        labels: {
          app: 'karmada-agent',
          version: 'v1.7.0',
        },
        annotations: {
          'deployment.kubernetes.io/revision': '1',
        },
      },
      // coredns
      {
        key: `${newCluster.key}-pod-9`,
        podName: 'coredns-5d78c9d6bb-mx2n4',
        namespace: 'kube-system',
        node: 'k8s2-node01.k8s.cn',
        status: 'Running',
        restarts: 0,
        cpu: 5,
        memory: 45,
        createdTime: '2025-06-18 08:22:46',
        image: 'registry.k8s.io/coredns/coredns:v1.10.1',
        uid: 'i9j0k1l2-m3n4-5678-ijkl-mn9012345678',
        podIP: '10.244.20.81',
        nodeIP: '10.10.20.4',
        containers: [
          {
            name: 'coredns',
            image: 'registry.k8s.io/coredns/coredns:v1.10.1',
            status: 'Running',
            ready: true,
            restarts: 0,
            ports: [53],
            resources: {
              requests: { cpu: '100m', memory: '70Mi' },
              limits: { cpu: '500m', memory: '170Mi' },
            },
          },
        ],
        labels: {
          'k8s-app': 'kube-dns',
          version: 'v1.10.1',
        },
        annotations: {
          'deployment.kubernetes.io/revision': '1',
        },
      },
      // calico-kube-controllers
      {
        key: `${newCluster.key}-pod-10`,
        podName: 'calico-kube-controllers-6b7c8d5e4f-cr8s3',
        namespace: 'calico-system',
        node: 'k8s2-node01.k8s.cn',
        status: 'Running',
        restarts: 0,
        cpu: 10,
        memory: 55,
        createdTime: '2025-06-18 08:17:01',
        image: 'calico/kube-controllers:v3.26.1',
        uid: 'j0k1l2m3-n4o5-6789-jklm-no0123456789',
        podIP: '10.244.20.82',
        nodeIP: '10.10.20.4',
        containers: [
          {
            name: 'calico-kube-controllers',
            image: 'calico/kube-controllers:v3.26.1',
            status: 'Running',
            ready: true,
            restarts: 0,
            ports: [9094],
            resources: {
              requests: { cpu: '30m', memory: '64Mi' },
              limits: { cpu: '500m', memory: '512Mi' },
            },
          },
        ],
        labels: {
          'k8s-app': 'calico-kube-controllers',
          version: 'v3.26.1',
        },
        annotations: {
          'deployment.kubernetes.io/revision': '1',
        },
      },
      // calico-typha
      {
        key: `${newCluster.key}-pod-11`,
        podName: 'calico-typha-7c8d9e6f5a-ds9t4',
        namespace: 'calico-system',
        node: 'k8s2-node02.k8s.cn',
        status: 'Running',
        restarts: 0,
        cpu: 12,
        memory: 68,
        createdTime: '2025-06-17 03:37:22',
        image: 'calico/typha:v3.26.1',
        uid: 'k1l2m3n4-o5p6-7890-klmn-op1234567890',
        podIP: '10.244.87.165',
        nodeIP: '10.10.20.5',
        containers: [
          {
            name: 'calico-typha',
            image: 'calico/typha:v3.26.1',
            status: 'Running',
            ready: true,
            restarts: 0,
            ports: [5473],
            resources: {
              requests: { cpu: '100m', memory: '128Mi' },
              limits: { cpu: '500m', memory: '512Mi' },
            },
          },
        ],
        labels: {
          'k8s-app': 'calico-typha',
          version: 'v3.26.1',
        },
        annotations: {
          'deployment.kubernetes.io/revision': '1',
        },
      },
      // ks-apiserver (工作负载)
      {
        key: `${newCluster.key}-pod-12`,
        podName: 'ks-apiserver-8d9e0f7g6h-et0u5',
        namespace: 'kubesphere-system',
        node: 'k8s2-node01.k8s.cn',
        status: 'Running',
        restarts: 0,
        cpu: 22,
        memory: 25,
        createdTime: '2025-06-16 16:01:09',
        image: 'kubesphere/ks-apiserver:v3.4.1',
        uid: 'l2m3n4o5-p6q7-8901-lmno-pq2345678901',
        podIP: '10.244.20.83',
        nodeIP: '10.10.20.4',
        containers: [
          {
            name: 'ks-apiserver',
            image: 'kubesphere/ks-apiserver:v3.4.1',
            status: 'Running',
            ready: true,
            restarts: 0,
            ports: [9090],
            resources: {
              requests: { cpu: '100m', memory: '128Mi' },
              limits: { cpu: '1000m', memory: '1Gi' },
            },
          },
        ],
        labels: {
          app: 'ks-apiserver',
          tier: 'backend',
          version: 'v3.4.1',
        },
        annotations: {
          'deployment.kubernetes.io/revision': '1',
          'kubesphere.io/creator': 'system',
        },
      },
      // ks-console (工作负载)
      {
        key: `${newCluster.key}-pod-13`,
        podName: 'ks-console-9e0f1g8h7i-fu1v6',
        namespace: 'kubesphere-system',
        node: 'k8s2-node02.k8s.cn',
        status: 'Running',
        restarts: 0,
        cpu: 18,
        memory: 95,
        createdTime: '2025-06-16 16:01:09',
        image: 'kubesphere/ks-console:v3.4.1',
        uid: 'm3n4o5p6-q7r8-9012-mnop-qr3456789012',
        podIP: '10.244.87.166',
        nodeIP: '10.10.20.5',
        containers: [
          {
            name: 'ks-console',
            image: 'kubesphere/ks-console:v3.4.1',
            status: 'Running',
            ready: true,
            restarts: 0,
            ports: [8000],
            resources: {
              requests: { cpu: '100m', memory: '128Mi' },
              limits: { cpu: '1000m', memory: '1Gi' },
            },
          },
        ],
        labels: {
          app: 'ks-console',
          tier: 'frontend',
          version: 'v3.4.1',
        },
        annotations: {
          'deployment.kubernetes.io/revision': '1',
          'kubesphere.io/creator': 'system',
        },
      },
    ]

    podData.value.push(...podList)

    // 开始统计数据增长
    startStatisticsGrowth()

    Message.success(`集群 ${addClusterForm.value.name} 接入成功`)
    addClusterVisible.value = false
  } catch (error) {
    Message.error('集群接入失败，请检查连接配置')
  } finally {
    connecting.value = false
  }
}

// 辅助函数：生成下一个IP
const getNextIP = (baseIP: string, offset: number = 1) => {
  const parts = baseIP.split('.')
  const lastPart = parseInt(parts[3]) + offset
  return `${parts[0]}.${parts[1]}.${parts[2]}.${lastPart}`
}

// 开始统计数据增长
const startStatisticsGrowth = () => {
  // 日志数量增长
  const logInterval = setInterval(() => {
    if (logCount.value < 596) {
      logCount.value += Math.floor(Math.random() * 5) + 1
    } else {
      clearInterval(logInterval)
    }
  }, 200)

  // 存储大小增长
  const storageInterval = setInterval(() => {
    if (storageSize.value < 3.8) {
      const increment = 0.01 // 每秒固定增长0.01
      storageSize.value = Math.round((storageSize.value + increment) * 100) / 100 // 保留2位小数
      storageSize.value = Math.min(storageSize.value, 3.8)
    } else {
      clearInterval(storageInterval)
    }
  }, 1000) // 每秒更新一次
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

.chart-placeholder.small {
  height: 180px;
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

/* 标签和注解样式 */
.labels-container,
.annotations-container {
  min-height: 100px;
  padding: 12px;
  background: #fafafa;
  border-radius: 6px;
  border: 1px solid #f0f0f0;
}

.label-tag,
.annotation-tag {
  margin: 4px;
  font-size: 12px;
}

/* 容器信息样式 */
.container-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.container-avatar {
  background: #52c41a;
}

.container-details {
  flex: 1;
}

.container-name {
  font-weight: 500;
  color: #1d2129;
  margin-bottom: 2px;
}

.container-image {
  font-size: 12px;
  color: #86909c;
}

.ports-container {
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
}

.port-tag {
  font-size: 11px;
}

.no-ports {
  color: #86909c;
  font-size: 12px;
}

/* 空状态样式 */
.empty-state {
  padding: 60px 20px;
  text-align: center;
}

.empty-content {
  max-width: 300px;
  margin: 0 auto;
}

.empty-icon {
  font-size: 64px;
  color: #c9cdd4;
  margin-bottom: 16px;
}

.empty-content h3 {
  color: #1d2129;
  margin-bottom: 8px;
  font-weight: 500;
}

.empty-content p {
  color: #86909c;
  margin-bottom: 24px;
  line-height: 1.5;
}

/* 连接状态样式 */
.connecting-status {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px;
  background: #f7f8fa;
  border-radius: 6px;
  margin-top: 16px;
  color: #1d2129;
}

.resource-details {
  font-size: 12px;
}

.resource-section {
  margin-bottom: 8px;
}

.resource-section:last-child {
  margin-bottom: 0;
}

.resource-section strong {
  color: #1d2129;
  display: block;
  margin-bottom: 4px;
}

.resource-section div {
  color: #86909c;
  margin-left: 8px;
}

/* 资源使用率样式 */
.resource-usage {
  display: flex;
  align-items: center;
  gap: 12px;
}

.usage-text {
  font-weight: 500;
  color: #1d2129;
  min-width: 40px;
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
  line-height: 1.4;
  padding: 12px;
  border-radius: 6px;
  overflow-y: auto;
  max-height: 350px;
}

.log-line {
  margin-bottom: 3px;
  word-wrap: break-word;
}

.log-time {
  color: #86909c;
  margin-right: 6px;
}

.log-level {
  margin-right: 6px;
  font-weight: bold;
}

.log-level.info {
  color: #52c41a;
}

.log-level.debug {
  color: #1890ff;
}

.log-level.warn {
  color: #faad14;
}

.log-level.error {
  color: #f5222d;
}

.log-message {
  color: #f0f0f0;
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

/* kubeconfig文本区域样式 */
:deep(.arco-textarea) {
  font-family: 'Courier New', 'Monaco', 'Menlo', monospace;
  font-size: 13px;
  line-height: 1.5;
  resize: vertical;
  min-height: 500px !important;
  height: 500px !important;
}

:deep(.arco-textarea-wrapper) {
  min-height: 500px !important;
  height: auto !important;
}

.config-preview {
  margin-top: 16px;
  padding: 16px;
  background: #f5f5f5;
  border-radius: 6px;
}

.config-preview h4 {
  margin: 0 0 12px 0;
  font-size: 14px;
  color: #333;
}

/* Pod详情页样式 */
.pod-detail-container {
  max-height: 80vh;
  overflow-y: auto;
}

.detail-section {
  margin-bottom: 32px;
}

.detail-section:last-child {
  margin-bottom: 0;
}

.section-title {
  margin: 0 0 16px 0;
  font-size: 16px;
  font-weight: 600;
  color: #1d2129;
  border-left: 4px solid #1890ff;
  padding-left: 12px;
  background: #f7f8fa;
  padding: 8px 12px;
  border-radius: 4px;
}

.labels-container {
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
  max-width: 200px;
}

.label-tag {
  font-size: 11px;
  margin: 0;
}

.log-count {
  font-size: 12px;
  color: #86909c;
}

.log-empty {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 200px;
  color: #86909c;
  background: #f7f8fa;
  border-radius: 4px;
}

.log-empty p {
  margin: 12px 0 0 0;
  font-size: 14px;
}

:deep(.arco-descriptions-item-value) {
  word-break: break-all;
}

:deep(.arco-modal-body) {
  padding: 24px !important;
}

/* 资源使用率样式 */
.resource-usage {
  display: flex;
  align-items: center;
  gap: 8px;
  min-width: 150px;
}

.usage-text {
  font-weight: 500;
  color: #1d2129;
  min-width: 35px;
  text-align: right;
}

/* 容器表格样式 */
.container-table {
  margin-top: 8px;
}

.container-info {
  display: flex;
  align-items: center;
  gap: 8px;
}

.container-avatar {
  background: #1890ff;
}

.container-details {
  flex: 1;
}

.container-name {
  font-weight: 500;
  color: #1d2129;
  margin-bottom: 2px;
}

.container-image {
  font-size: 12px;
  color: #86909c;
}

.ports-container {
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
}

.port-tag {
  margin: 0;
  font-size: 11px;
}

.no-ports {
  color: #86909c;
  font-size: 12px;
}

.resource-details {
  font-size: 12px;
}

.resource-section {
  margin-bottom: 4px;
}

.resource-section:last-child {
  margin-bottom: 0;
}
</style>
