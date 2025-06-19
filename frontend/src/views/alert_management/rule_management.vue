<template>
  <div class="alert-rule-page">
    <PageHeader title="告警规则管理" description="配置和管理分部IT基础设施告警规则">
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

    <!-- 规则列表 -->
    <a-card :bordered="false">
      <template #title>
        <a-space>
          <span>告警规则配置</span>
          <a-tag color="blue">{{ ruleData.length }}条规则</a-tag>
          <a-tag color="green">{{ ruleStats.enabled }}条启用</a-tag>
        </a-space>
      </template>

      <a-table
        :columns="ruleColumns"
        :data="ruleData"
        :pagination="{ pageSize: 15, showTotal: true }"
        :scroll="{ x: '100%' }"
        :loading="tableLoading"
        row-key="id"
      >
        <template #alert_level="{ record }">
          <a-tag :color="getSeverityColor(record.alert_level)" size="small">
            {{ getSeverityText(record.alert_level) }}
          </a-tag>
        </template>

        <template #is_active="{ record }">
          <a-badge
            :status="record.is_active === 'active' ? 'success' : 'default'"
            :text="record.is_active === 'active' ? '启用' : '禁用'"
          />
        </template>

        <template #actions="{ record }">
          <a-space>
            <a-button type="text" size="small" @click="viewRule(record)">
              <template #icon>
                <icon-eye />
              </template>
              查看
            </a-button>
            <a-button type="text" size="small" @click="editRule(record)">
              <template #icon>
                <icon-edit />
              </template>
              编辑
            </a-button>
            <a-button
              type="text"
              size="small"
              status="danger"
              @click="deleteRule(record)"
              :loading="deletingRuleId === record.id"
              :disabled="deletingRuleId === record.id"
            >
              <template #icon>
                <icon-delete />
              </template>
              {{ deletingRuleId === record.id ? '删除中...' : '删除' }}
            </a-button>
          </a-space>
        </template>
      </a-table>
    </a-card>

    <!-- 添加/编辑规则弹窗 -->
    <a-modal
      v-model:visible="ruleModalVisible"
      :title="editingRule ? '编辑规则' : '添加规则'"
      @ok="handleRuleSubmit"
      @cancel="ruleModalVisible = false"
    >
      <a-form :model="ruleForm" layout="vertical">
        <a-form-item label="规则名称" required>
          <a-input v-model="ruleForm.name" placeholder="请输入规则名称" />
        </a-form-item>
        <a-form-item label="目标资产" required>
          <a-select
            v-model="ruleForm.target_asset_id"
            placeholder="请选择目标资产"
            :loading="assetsLoading"
          >
            <a-option v-for="asset in assetsList" :key="asset.id" :value="asset.id">
              {{ asset.name }} ({{ asset.ip_address }}) - ID: {{ asset.id }}
            </a-option>
          </a-select>
        </a-form-item>
        <a-form-item label="触发条件" required>
          <a-select v-model="ruleForm.trigger_condition" placeholder="请选择触发条件">
            <a-optgroup label="CPU相关">
              <a-option value="CPU使用率超过80%">CPU使用率超过80%</a-option>
              <a-option value="CPU使用率超过90%">CPU使用率超过90%</a-option>
              <a-option value="CPU负载超过系统核心数">CPU负载超过系统核心数</a-option>
            </a-optgroup>
            <a-optgroup label="内存相关">
              <a-option value="内存使用率超过85%">内存使用率超过85%</a-option>
              <a-option value="内存使用率超过95%">内存使用率超过95%</a-option>
              <a-option value="可用内存少于500MB">可用内存少于500MB</a-option>
            </a-optgroup>
            <a-optgroup label="磁盘相关">
              <a-option value="磁盘使用率超过90%">磁盘使用率超过90%</a-option>
              <a-option value="磁盘使用率超过95%">磁盘使用率超过95%</a-option>
              <a-option value="磁盘剩余空间少于1GB">磁盘剩余空间少于1GB</a-option>
            </a-optgroup>
            <a-optgroup label="网络相关">
              <a-option value="网络延迟超过100ms">网络延迟超过100ms</a-option>
              <a-option value="网络丢包率超过5%">网络丢包率超过5%</a-option>
              <a-option value="网络连接数超过1000">网络连接数超过1000</a-option>
            </a-optgroup>
            <a-optgroup label="服务相关">
              <a-option value="服务停止运行">服务停止运行</a-option>
              <a-option value="服务响应时间超过5秒">服务响应时间超过5秒</a-option>
              <a-option value="进程崩溃或异常退出">进程崩溃或异常退出</a-option>
            </a-optgroup>
            <a-optgroup label="安全相关">
              <a-option value="连续5次登录失败">连续5次登录失败</a-option>
              <a-option value="检测到恶意IP访问">检测到恶意IP访问</a-option>
              <a-option value="防火墙阻止异常流量">防火墙阻止异常流量</a-option>
            </a-optgroup>
          </a-select>
        </a-form-item>
        <a-form-item label="告警级别" required>
          <a-select v-model="ruleForm.alert_level" placeholder="请选择告警级别">
            <a-option value="CRITICAL">严重</a-option>
            <a-option value="HIGH">警告</a-option>
            <a-option value="MEDIUM">信息</a-option>
            <a-option value="LOW">低</a-option>
          </a-select>
        </a-form-item>
        <a-form-item label="状态" required>
          <a-select v-model="ruleForm.is_active" placeholder="请选择状态">
            <a-option value="active">启用</a-option>
            <a-option value="inactive">禁用</a-option>
          </a-select>
        </a-form-item>
      </a-form>
    </a-modal>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { Message, Modal } from '@arco-design/web-vue'
import PageHeader from '@/components/PageHeader.vue'
import StatCard from '@/components/StatCard.vue'
import { alertsApi, type AlertRule } from '@/services/alerts'
import { assetsApi, type Asset } from '@/services/assets'
import {
  IconRefresh,
  IconPlus,
  IconSearch,
  IconCheck,
  IconExclamation,
  IconSettings,
  IconClose,
  IconEye,
  IconEdit,
  IconDelete,
} from '@arco-design/web-vue/es/icon'

// 响应式数据
const refreshing = ref(false)
const tableLoading = ref(false)
const ruleModalVisible = ref(false)
const editingRule = ref(false)
const currentRule = ref<AlertRule | null>(null)
const deletingRuleId = ref<number | null>(null)

// 规则数据
const ruleData = ref<AlertRule[]>([])

// 资产数据
const assetsList = ref<Asset[]>([])
const assetsLoading = ref(false)

// 规则统计数据
const ruleStats = computed(() => {
  const total = ruleData.value.length
  const enabled = ruleData.value.filter((rule) => rule.is_active === 'active').length
  const disabled = total - enabled

  return {
    total,
    enabled,
    triggered: 0, // 暂时设为0，实际可以从告警记录中统计
    disabled,
  }
})

// 获取告警规则列表
const fetchAlertRules = async () => {
  try {
    tableLoading.value = true
    const data = await alertsApi.getAlertRules()
    ruleData.value = data
  } catch (error) {
    Message.error('获取告警规则失败，显示模拟数据')
    // 在API失败时显示模拟数据
    ruleData.value = [
      {
        id: 1,
        name: '连续5分钟未收到心跳',
        target_asset_id: 1,
        trigger_condition: '连续5分钟未收到心跳',
        alert_level: '严重',
        is_active: 'active',
        created_at: '2025-06-18T04:35:54',
      },
      {
        id: 2,
        name: 'Kube-apiserver 连接超时',
        target_asset_id: 2,
        trigger_condition: 'Kube-apiserver 连接超时',
        alert_level: '严重',
        is_active: 'active',
        created_at: '2025-06-18T04:35:54',
      },
      {
        id: 3,
        name: 'fawfwa',
        target_asset_id: 3,
        trigger_condition: 'CPU使用率超过90%',
        alert_level: '严重',
        is_active: 'active',
        created_at: '2025-06-18T12:13:43',
      },
    ]
  } finally {
    tableLoading.value = false
  }
}

// 刷新规则数据
const refreshRules = async () => {
  refreshing.value = true
  try {
    await fetchAlertRules()
    Message.success('规则数据刷新成功')
  } catch (error) {
    Message.error('刷新失败')
  } finally {
    refreshing.value = false
  }
}

// 规则表单数据
const ruleForm = ref({
  name: '',
  target_asset_id: null as number | null,
  trigger_condition: '',
  alert_level: '',
  is_active: 'active',
})

// 获取资产列表
const fetchAssets = async () => {
  try {
    assetsLoading.value = true
    const data = await assetsApi.getAssets()
    assetsList.value = data
  } catch (error) {
    Message.error('获取资产列表失败，显示模拟数据')
    // 在API失败时显示模拟资产数据
    assetsList.value = [
      {
        id: 1,
        name: '分部集群接入交换机',
        asset_type: 'network_device',
        ip_address: '192.168.10.1',
        location: '分部机房',
        security_level: '等级二',
        status: 'normal',
        created_at: '2025-06-18T04:35:54Z',
        updated_at: '2025-06-18T04:35:54Z',
      },
      {
        id: 2,
        name: '分部K8S集群',
        asset_type: 'k8s_cluster',
        ip_address: '192.168.20.1',
        location: '数据中心B栋',
        security_level: '等级三',
        status: 'normal',
        created_at: '2025-06-18T04:35:54Z',
        updated_at: '2025-06-18T04:35:54Z',
      },
      {
        id: 3,
        name: '分部服务器1',
        asset_type: 'linux_server',
        ip_address: '192.168.30.1',
        location: '分部机房',
        security_level: '等级二',
        status: 'normal',
        created_at: '2025-06-18T04:35:54Z',
        updated_at: '2025-06-18T04:35:54Z',
      },
    ] as Asset[]
  } finally {
    assetsLoading.value = false
  }
}

// 页面挂载时获取数据
onMounted(() => {
  fetchAlertRules()
  fetchAssets()
})

// 表格列配置
const ruleColumns = [
  {
    title: '规则ID',
    dataIndex: 'id',
    width: 80,
  },
  {
    title: '规则名称',
    dataIndex: 'name',
    width: 200,
    ellipsis: true,
    tooltip: true,
  },
  {
    title: '目标资产',
    dataIndex: 'target_asset_id',
    width: 200,
    render: ({ record }: { record: AlertRule }) => {
      const asset = assetsList.value.find((a) => a.id === record.target_asset_id)
      return asset ? `${asset.name} (ID: ${asset.id})` : `ID: ${record.target_asset_id}`
    },
  },
  {
    title: '触发条件',
    dataIndex: 'trigger_condition',
    width: 200,
    ellipsis: true,
    tooltip: true,
  },
  {
    title: '告警级别',
    dataIndex: 'alert_level',
    slotName: 'alert_level',
    width: 100,
  },
  {
    title: '状态',
    dataIndex: 'is_active',
    slotName: 'is_active',
    width: 100,
  },
  {
    title: '创建时间',
    dataIndex: 'created_at',
    width: 150,
  },
  {
    title: '操作',
    slotName: 'actions',
    width: 200,
    fixed: 'right',
  },
]

// 工具函数
const getSeverityColor = (severity: string) => {
  switch (severity) {
    case 'CRITICAL':
      return 'red'
    case 'HIGH':
      return 'orange'
    case 'MEDIUM':
      return 'blue'
    case 'LOW':
      return 'green'
    default:
      return 'gray'
  }
}

const getSeverityText = (severity: string) => {
  switch (severity) {
    case 'CRITICAL':
      return '严重'
    case 'HIGH':
      return '警告'
    case 'MEDIUM':
      return '信息'
    case 'LOW':
      return '低'
    default:
      return '未知'
  }
}

// 事件处理函数
const showAddRule = () => {
  editingRule.value = false
  currentRule.value = null
  ruleForm.value = {
    name: '',
    target_asset_id: null,
    trigger_condition: '',
    alert_level: '',
    is_active: 'active',
  }
  ruleModalVisible.value = true
}

const viewRule = (rule: AlertRule) => {
  // 可以在这里实现查看规则详情的功能
  Modal.info({
    title: `规则详情 - ${rule.name}`,
    content: `
      规则ID: ${rule.id}
      目标资产: ${rule.target_asset_id}
      触发条件: ${rule.trigger_condition}
      告警级别: ${rule.alert_level}
      状态: ${rule.is_active === 'active' ? '启用' : '禁用'}
      创建时间: ${rule.created_at}
    `,
    width: 500,
  })
}

const editRule = (rule: AlertRule) => {
  editingRule.value = true
  currentRule.value = rule
  ruleForm.value = {
    name: rule.name,
    target_asset_id: rule.target_asset_id,
    trigger_condition: rule.trigger_condition,
    alert_level: rule.alert_level,
    is_active: rule.is_active,
  }
  ruleModalVisible.value = true
}

const deleteRule = (rule: AlertRule) => {
  // 获取关联的资产信息
  const asset = assetsList.value.find((a) => a.id === rule.target_asset_id)
  const assetInfo = asset ? `${asset.name} (${asset.ip_address})` : `ID: ${rule.target_asset_id}`

  // 显示确认对话框
  const modal = Modal.confirm({
    title: '确认删除告警规则',
    content: `即将删除以下告警规则，此操作不可恢复：
    
• 规则名称：${rule.name}
• 目标资产：${assetInfo}
• 触发条件：${rule.trigger_condition}
• 告警级别：${getSeverityText(rule.alert_level)}

注意：如果该规则下存在关联的告警记录，将无法删除。`,
    okText: '确定删除',
    cancelText: '取消',
    okButtonProps: { status: 'danger' },
    onOk: async () => {
      try {
        deletingRuleId.value = rule.id
        await alertsApi.deleteAlertRule(rule.id)
        Message.success('规则删除成功')
        await fetchAlertRules()
      } catch (error: any) {
        console.error('删除规则失败:', error)

        // 根据错误类型显示不同的提示信息
        if (
          error.message &&
          error.message.includes('存在') &&
          error.message.includes('条关联的告警记录')
        ) {
          Modal.error({
            title: '删除失败',
            content: `无法删除该规则：${error.message}。

建议：请先处理或删除相关的告警记录，然后再删除该规则。

您可以前往"告警记录查询"页面查看和处理相关告警。`,
            width: 500,
          })
        } else if (error.message && error.message.includes('404')) {
          Message.error('告警规则不存在，可能已被删除')
          await fetchAlertRules() // 刷新列表
        } else {
          Message.error(`删除规则失败：${error.message || '未知错误'}`)
        }
      } finally {
        deletingRuleId.value = null
      }
    },
  })
}

const handleRuleSubmit = async () => {
  try {
    if (
      !ruleForm.value.name ||
      !ruleForm.value.target_asset_id ||
      !ruleForm.value.trigger_condition ||
      !ruleForm.value.alert_level
    ) {
      Message.warning('请填写所有必填项')
      return
    }

    if (editingRule.value && currentRule.value) {
      // 编辑规则
      await alertsApi.updateAlertRule(currentRule.value.id, {
        name: ruleForm.value.name,
        target_asset_id: ruleForm.value.target_asset_id!,
        trigger_condition: ruleForm.value.trigger_condition,
        alert_level: ruleForm.value.alert_level,
        is_active: ruleForm.value.is_active,
      })
      Message.success('规则更新成功')
      ruleModalVisible.value = false
      await fetchAlertRules()
    } else {
      // 添加新规则
      await alertsApi.createAlertRule({
        name: ruleForm.value.name,
        target_asset_id: ruleForm.value.target_asset_id!,
        trigger_condition: ruleForm.value.trigger_condition,
        alert_level: ruleForm.value.alert_level,
        is_active: ruleForm.value.is_active,
      })
      Message.success('规则添加成功')
      ruleModalVisible.value = false
      await fetchAlertRules()
    }
  } catch (error) {
    Message.error('操作失败')
  }
}
</script>

<style scoped>
.alert-rule-page {
  padding: 0;
}

.stats-row {
  margin-bottom: 24px;
}

:deep(.arco-card) {
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}
</style>
