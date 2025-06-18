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
            <a-button type="text" size="small" status="danger" @click="deleteRule(record)">
              <template #icon>
                <icon-delete />
              </template>
              删除
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
        <a-form-item label="目标资产ID" required>
          <a-input-number v-model="ruleForm.target_asset_id" placeholder="请输入目标资产ID" />
        </a-form-item>
        <a-form-item label="触发条件" required>
          <a-textarea v-model="ruleForm.trigger_condition" placeholder="请输入触发条件" />
        </a-form-item>
        <a-form-item label="告警级别" required>
          <a-select v-model="ruleForm.alert_level" placeholder="请选择告警级别">
            <a-option value="严重">严重</a-option>
            <a-option value="警告">警告</a-option>
            <a-option value="信息">信息</a-option>
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
import { Message } from '@arco-design/web-vue'
import PageHeader from '@/components/PageHeader.vue'
import StatCard from '@/components/StatCard.vue'
import { alertsApi, type AlertRule } from '@/services/alerts'
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

// 规则数据
const ruleData = ref<AlertRule[]>([])

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
    console.error('获取告警规则失败:', error)
    Message.error('获取告警规则失败')
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
  target_asset_id: '',
  trigger_condition: '',
  alert_level: '',
  is_active: 'active',
})

// 页面挂载时获取数据
onMounted(() => {
  fetchAlertRules()
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
    title: '目标资产ID',
    dataIndex: 'target_asset_id',
    width: 120,
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

const getSeverityText = (severity: string) => {
  return severity || '未知'
}

// 事件处理函数
const showAddRule = () => {
  editingRule.value = false
  currentRule.value = null
  ruleForm.value = {
    name: '',
    target_asset_id: '',
    trigger_condition: '',
    alert_level: '',
    is_active: 'active',
  }
  ruleModalVisible.value = true
}

const viewRule = (rule: AlertRule) => {
  console.log('查看规则:', rule)
  Message.info('查看规则功能待实现')
}

const editRule = (rule: AlertRule) => {
  editingRule.value = true
  currentRule.value = rule
  ruleForm.value = {
    name: rule.name,
    target_asset_id: rule.target_asset_id.toString(),
    trigger_condition: rule.trigger_condition,
    alert_level: rule.alert_level,
    is_active: rule.is_active,
  }
  ruleModalVisible.value = true
}

const deleteRule = (rule: AlertRule) => {
  console.log('删除规则:', rule)
  Message.info('删除规则功能待实现')
}

const handleRuleSubmit = async () => {
  try {
    if (
      !ruleForm.value.name ||
      !ruleForm.value.target_asset_id ||
      !ruleForm.value.trigger_condition
    ) {
      Message.warning('请填写必填项')
      return
    }

    if (editingRule.value) {
      // TODO: 实现编辑规则API
      Message.info('编辑规则功能待实现')
    } else {
      // TODO: 实现添加规则API
      await alertsApi.createAlertRule({
        name: ruleForm.value.name,
        target_asset_id: parseInt(ruleForm.value.target_asset_id),
        trigger_condition: ruleForm.value.trigger_condition,
        alert_level: ruleForm.value.alert_level,
        is_active: ruleForm.value.is_active,
      })
      Message.success('规则添加成功')
      ruleModalVisible.value = false
      await fetchAlertRules()
    }
  } catch (error) {
    console.error('操作失败:', error)
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
