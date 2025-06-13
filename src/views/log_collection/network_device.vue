<template>
  <div class="network-device-page">
    <PageHeader
      title="网络设备日志采集"
      description="配置并监控网络设备日志采集，分析上网流量统计"
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
            添加网络设备
          </a-button>
        </a-space>
      </template>
    </PageHeader>

    <!-- 统计卡片 -->
    <a-row :gutter="24" class="stats-row">
      <a-col :span="6">
        <StatCard
          :icon="IconDesktop"
          icon-bg-color="#52c41a"
          :value="12"
          label="在线设备"
          subtitle="网络设备总数"
        />
      </a-col>
      <a-col :span="6">
        <StatCard
          :icon="IconDownload"
          icon-bg-color="#1890ff"
          :value="8"
          label="采集中"
          subtitle="正在采集日志"
        />
      </a-col>
      <a-col :span="6">
        <StatCard
          :icon="IconFile"
          icon-bg-color="#faad14"
          :value="15420"
          label="今日日志"
          subtitle="条数统计"
        />
      </a-col>
      <a-col :span="6">
        <StatCard
          :icon="IconCloudDownload"
          icon-bg-color="#722ed1"
          :value="2.8"
          label="今日流量(GB)"
          subtitle="网络流量统计"
        />
      </a-col>
    </a-row>

    <!-- 设备管理标签页 -->
    <a-tabs default-active-key="device-config" class="device-tabs">
      <a-tab-pane key="device-config" title="设备配置">
        <a-card :bordered="false">
          <template #title>
            <a-space>
              <span>设备配置</span>
              <a-tag color="blue">流量监控</a-tag>
              <a-tag color="green">行为分析</a-tag>
              <a-tag color="orange">日志查看</a-tag>
              <a-tag color="purple">实时监控</a-tag>
            </a-space>
          </template>
          
          <!-- 设备列表 -->
          <a-table
            :columns="deviceColumns"
            :data="deviceData"
            :pagination="false"
            :scroll="{ x: '100%' }"
            class="device-table"
          >
            <template #deviceName="{ record }">
              <div class="device-info">
                <a-avatar size="small" class="device-avatar">
                  <icon-desktop />
                </a-avatar>
                <div class="device-details">
                  <div class="device-name">{{ record.deviceName }}</div>
                  <div class="device-ip">{{ record.ip }}</div>
                </div>
              </div>
            </template>

            <template #deviceType="{ record }">
              <a-tag
                :color="getDeviceTypeColor(record.deviceType)"
                size="small"
              >
                {{ record.deviceType }}
              </a-tag>
            </template>

            <template #protocol="{ record }">
              <a-tag color="blue" size="small">{{ record.protocol }}</a-tag>
            </template>

            <template #status="{ record }">
              <a-badge
                :status="record.status === '在线' ? 'success' : 'error'"
                :text="record.status"
              />
            </template>

            <template #actions="{ record }">
              <a-space>
                <a-button
                  type="text"
                  size="small"
                  status="normal"
                  @click="editDevice(record)"
                >
                  编辑
                </a-button>
                <a-button
                  type="text"
                  size="small"
                  status="warning"
                  @click="stopCollection(record)"
                >
                  停止采集
                </a-button>
                <a-button
                  type="text"
                  size="small"
                  status="danger"
                  @click="deleteDevice(record)"
                >
                  删除
                </a-button>
              </a-space>
            </template>
          </a-table>
        </a-card>
      </a-tab-pane>

      <a-tab-pane key="flow-monitor" title="流量监控">
        <a-card title="网络流量监控" :bordered="false">
          <div class="chart-placeholder">
            <div class="chart-content">
              <icon-settings class="chart-icon" />
              <p>实时网络流量监控图表</p>
            </div>
          </div>
        </a-card>
      </a-tab-pane>

      <a-tab-pane key="behavior-analysis" title="行为分析">
        <a-card title="用户行为分析" :bordered="false">
          <div class="chart-placeholder">
            <div class="chart-content">
              <icon-desktop class="chart-icon" />
              <p>用户上网行为分析报告</p>
            </div>
          </div>
        </a-card>
      </a-tab-pane>

      <a-tab-pane key="log-view" title="日志查看">
        <a-card title="设备日志查看" :bordered="false">
          <a-textarea
            :model-value="logContent"
            :auto-size="{ minRows: 15, maxRows: 20 }"
            readonly
            placeholder="设备日志将在这里显示..."
          />
        </a-card>
      </a-tab-pane>

      <a-tab-pane key="real-time-monitor" title="实时监控">
        <a-card title="实时监控面板" :bordered="false">
          <div class="monitor-grid">
            <a-row :gutter="16">
              <a-col :span="12">
                <div class="monitor-item">
                  <h4>CPU 使用率</h4>
                  <a-progress :percent="cpuUsage" :show-text="false" />
                  <span class="monitor-value">{{ cpuUsage }}%</span>
                </div>
              </a-col>
              <a-col :span="12">
                <div class="monitor-item">
                  <h4>内存使用率</h4>
                  <a-progress :percent="memoryUsage" :show-text="false" status="success" />
                  <span class="monitor-value">{{ memoryUsage }}%</span>
                </div>
              </a-col>
            </a-row>
            <a-row :gutter="16" style="margin-top: 16px;">
              <a-col :span="12">
                <div class="monitor-item">
                  <h4>网络流入</h4>
                  <a-progress :percent="networkIn" :show-text="false" status="warning" />
                  <span class="monitor-value">{{ networkIn }}%</span>
                </div>
              </a-col>
              <a-col :span="12">
                <div class="monitor-item">
                  <h4>网络流出</h4>
                  <a-progress :percent="networkOut" :show-text="false" status="danger" />
                  <span class="monitor-value">{{ networkOut }}%</span>
                </div>
              </a-col>
            </a-row>
          </div>
        </a-card>
      </a-tab-pane>
    </a-tabs>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import PageHeader from '@/components/PageHeader.vue'
import StatCard from '@/components/StatCard.vue'
import {
  IconDesktop,
  IconDownload,
  IconFile,
  IconCloudDownload,
  IconRefresh,
  IconPlus,
  IconSettings
} from '@arco-design/web-vue/es/icon'

// 设备数据
const deviceData = ref([
  {
    key: '1',
    deviceName: '核心路由器-01',
    ip: '192.168.1.1',
    deviceType: 'router',
    protocol: 'snmp',
    status: '在线'
  },
  {
    key: '2',
    deviceName: '汇聚交换机-01',
    ip: '192.168.1.10',
    deviceType: 'switch',
    protocol: 'syslog',
    status: '在线'
  }
])

// 表格列配置
const deviceColumns = [
  {
    title: '设备名称',
    dataIndex: 'deviceName',
    slotName: 'deviceName',
    width: 200
  },
  {
    title: 'IP地址',
    dataIndex: 'ip',
    width: 120
  },
  {
    title: '设备类型',
    dataIndex: 'deviceType',
    slotName: 'deviceType',
    width: 100
  },
  {
    title: '协议',
    dataIndex: 'protocol',
    slotName: 'protocol',
    width: 80
  },
  {
    title: '状态',
    dataIndex: 'status',
    slotName: 'status',
    width: 80
  },
  {
    title: '操作',
    slotName: 'actions',
    width: 180,
    fixed: 'right'
  }
]

// 监控数据
const cpuUsage = ref(45)
const memoryUsage = ref(62)
const networkIn = ref(78)
const networkOut = ref(23)

// 日志内容
const logContent = ref(`[2024-01-15 10:30:15] INFO: 设备连接正常
[2024-01-15 10:29:45] DEBUG: 开始日志采集任务
[2024-01-15 10:29:30] INFO: SNMP连接建立成功
[2024-01-15 10:29:15] INFO: 设备认证通过`)

// 获取设备类型颜色
const getDeviceTypeColor = (type: string) => {
  switch (type) {
    case 'router':
      return 'blue'
    case 'switch':
      return 'green'
    case 'firewall':
      return 'red'
    default:
      return 'gray'
  }
}

// 操作方法
const editDevice = (record: any) => {
  console.log('编辑设备:', record)
}

const stopCollection = (record: any) => {
  console.log('停止采集:', record)
}

const deleteDevice = (record: any) => {
  console.log('删除设备:', record)
}
</script>

<style scoped>
.network-device-page {
  padding: 0;
}

.stats-row {
  margin-bottom: 24px;
}

.device-tabs {
  margin-bottom: 0;
}

.device-table {
  margin-top: 16px;
}

.device-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.device-avatar {
  background: #1890ff;
}

.device-details {
  flex: 1;
}

.device-name {
  font-weight: 500;
  color: #1d2129;
  margin-bottom: 2px;
}

.device-ip {
  font-size: 12px;
  color: #86909c;
}

.chart-placeholder {
  height: 300px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #fafafa;
  border-radius: 6px;
}

.chart-content {
  text-align: center;
  color: #86909c;
}

.chart-icon {
  font-size: 48px;
  margin-bottom: 16px;
}

.monitor-grid {
  padding: 16px 0;
}

.monitor-item {
  padding: 16px;
  background: #fafafa;
  border-radius: 6px;
  position: relative;
}

.monitor-item h4 {
  margin: 0 0 12px 0;
  font-size: 14px;
  color: #1d2129;
}

.monitor-value {
  position: absolute;
  right: 16px;
  top: 16px;
  font-weight: 500;
  color: #1d2129;
}

:deep(.arco-card) {
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

:deep(.arco-tabs-content) {
  padding-top: 0;
}
</style>
