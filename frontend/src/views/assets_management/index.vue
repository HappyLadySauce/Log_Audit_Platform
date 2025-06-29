<template>
  <div class="assets-page">
    <PageHeader title="资产管理" description="管理和监控所有IT资产设备">
      <template #extra>
        <a-space>
          <a-button @click="handleRefresh" :loading="loading">
            <template #icon>
              <icon-refresh />
            </template>
            刷新
          </a-button>
          <a-button @click="showAddAsset">
            <template #icon>
              <icon-plus />
            </template>
            添加资产
          </a-button>
          <a-button type="primary" @click="showContinuousAdd">
            <template #icon>
              <icon-plus />
            </template>
            连续添加
          </a-button>
        </a-space>
      </template>
    </PageHeader>

    <!-- 资产统计 -->
    <a-row :gutter="24" class="stats-row">
      <a-col :span="6">
        <StatCard
          :icon="IconDesktop"
          icon-bg-color="#1890ff"
          :value="stats.total"
          label="总资产数"
          subtitle="设备总量"
        />
      </a-col>
      <a-col :span="6">
        <StatCard
          :icon="IconCheck"
          icon-bg-color="#52c41a"
          :value="stats.online"
          label="在线设备"
          subtitle="正常运行"
        />
      </a-col>
      <a-col :span="6">
        <StatCard
          :icon="IconExclamation"
          icon-bg-color="#faad14"
          :value="stats.warning"
          label="异常设备"
          subtitle="需要关注"
        />
      </a-col>
      <a-col :span="6">
        <StatCard
          :icon="IconClose"
          icon-bg-color="#f5222d"
          :value="stats.error"
          label="离线设备"
          subtitle="失去连接"
        />
      </a-col>
    </a-row>

    <!-- 资产列表 -->
    <a-card title="资产列表" :bordered="false">
      <template #extra>
        <a-space>
          <a-input-search placeholder="搜索资产..." style="width: 200px" allow-clear />
          <a-select placeholder="设备类型" style="width: 120px" allow-clear>
            <a-option value="server">服务器</a-option>
            <a-option value="network">网络设备</a-option>
            <a-option value="storage">存储设备</a-option>
            <a-option value="security">安全设备</a-option>
          </a-select>
        </a-space>
      </template>

      <a-table
        :columns="assetColumns"
        :data="assetData"
        :pagination="{ pageSize: 10 }"
        :scroll="{ x: '100%' }"
        :loading="loading"
        row-key="id"
      >
        <template #deviceInfo="{ record }">
          <div class="device-info">
            <a-avatar size="small" class="device-avatar">
              <component :is="getDeviceIcon(record.asset_type)" />
            </a-avatar>
            <div class="device-details">
              <div class="device-name">{{ record.name }}</div>
              <div class="device-model">{{ record.security_level }}</div>
            </div>
          </div>
        </template>

        <template #type="{ record }">
          <a-tag :color="getTypeColor(record.asset_type)">
            {{ getTypeName(record.asset_type) }}
          </a-tag>
        </template>

        <template #status="{ record }">
          <a-badge :status="getStatusType(record.status)" :text="getStatusText(record.status)" />
        </template>

        <template #actions="{ record }">
          <a-space>
            <a-button type="text" size="small" @click="viewAsset(record)">查看</a-button>
            <a-button type="text" size="small" @click="editAsset(record)">编辑</a-button>
            <a-button type="text" size="small" status="danger" @click="deleteAsset(record)"
              >删除</a-button
            >
          </a-space>
        </template>
      </a-table>
    </a-card>

    <!-- 添加资产弹窗 -->
    <a-modal
      v-model:visible="showAddModal"
      title="添加资产"
      @ok="handleAddAsset"
      @cancel="resetAddForm"
      width="800px"
    >
      <a-form :model="addForm" layout="vertical">
        <a-row :gutter="16">
          <a-col :span="12">
            <a-form-item label="设备名称" required>
              <a-input v-model="addForm.name" placeholder="请输入设备名称" />
            </a-form-item>
          </a-col>
          <a-col :span="12">
            <a-form-item label="设备类型" required>
              <a-select v-model="addForm.asset_type" placeholder="请选择设备类型">
                <a-option value="linux_server">Linux服务器</a-option>
                <a-option value="windows_server">Windows服务器</a-option>
                <a-option value="network_device">网络设备</a-option>
              </a-select>
            </a-form-item>
          </a-col>
        </a-row>
        <a-row :gutter="16">
          <a-col :span="12">
            <a-form-item label="IP地址" required>
              <a-input v-model="addForm.ip_address" placeholder="请输入IP地址" />
            </a-form-item>
          </a-col>
          <a-col :span="12">
            <a-form-item label="位置" required>
              <a-input v-model="addForm.location" placeholder="请输入设备位置" />
            </a-form-item>
          </a-col>
        </a-row>
        <a-row :gutter="16">
          <a-col :span="12">
            <a-form-item required>
              <template #label>
                <span style="display: flex; align-items: center; gap: 4px;">
                  安全防护等级
                  <icon-question-circle 
                    style="color: #f53f3f; font-size: 14px; cursor: pointer;" 
                    @click="showSecurityLevelInfo"
                  />
                </span>
              </template>
              <a-select v-model="addForm.security_level" placeholder="请选择安全防护等级">
                <a-option value="低防护级别">低防护级别</a-option>
                <a-option value="中低防护级别">中低防护级别</a-option>
                <a-option value="中高防护级别">中高防护级别</a-option>
                <a-option value="高防护级别">高防护级别</a-option>
              </a-select>
            </a-form-item>
          </a-col>
          <a-col :span="12">
            <a-form-item label="管理员联系方式">
              <a-input v-model="addForm.admin_contact" placeholder="请输入联系方式" />
            </a-form-item>
          </a-col>
        </a-row>
        <a-form-item label="资产描述">
          <a-textarea
            v-model="addForm.asset_description"
            placeholder="请描述资产详细信息"
            :auto-size="{ minRows: 2, maxRows: 4 }"
          />
        </a-form-item>
        <a-form-item>
          <a-checkbox v-model="continuousAdd">
            连续添加模式（保留表单信息，方便添加相似资产）
          </a-checkbox>
        </a-form-item>
      </a-form>
      <template #footer>
        <a-space>
          <a-button @click="resetAddForm">取消</a-button>
          <a-button type="primary" @click="handleAddAsset">
            {{ continuousAdd ? '添加并继续' : '确定' }}
          </a-button>
        </a-space>
      </template>
    </a-modal>

    <!-- 编辑资产弹窗 -->
    <a-modal
      v-model:visible="showEditModal"
      title="编辑资产"
      @ok="handleEditAsset"
      @cancel="showEditModal = false"
      width="800px"
    >
      <a-form :model="editForm" layout="vertical">
        <a-row :gutter="16">
          <a-col :span="12">
            <a-form-item label="设备名称" required>
              <a-input v-model="editForm.name" placeholder="请输入设备名称" />
            </a-form-item>
          </a-col>
          <a-col :span="12">
            <a-form-item label="设备类型" required>
              <a-select v-model="editForm.asset_type" placeholder="请选择设备类型">
                <a-option value="linux_server">Linux服务器</a-option>
                <a-option value="windows_server">Windows服务器</a-option>
                <a-option value="network_device">网络设备</a-option>
                <a-option value="k8s_cluster">K8S集群</a-option>
              </a-select>
            </a-form-item>
          </a-col>
        </a-row>
        <a-row :gutter="16">
          <a-col :span="12">
            <a-form-item label="IP地址" required>
              <a-input v-model="editForm.ip_address" placeholder="请输入IP地址" />
            </a-form-item>
          </a-col>
          <a-col :span="12">
            <a-form-item label="位置" required>
              <a-input v-model="editForm.location" placeholder="请输入设备位置" />
            </a-form-item>
          </a-col>
        </a-row>
        <a-row :gutter="16">
          <a-col :span="12">
            <a-form-item required>
              <template #label>
                <span style="display: flex; align-items: center; gap: 4px;">
                  安全防护等级
                  <icon-question-circle 
                    style="color: #f53f3f; font-size: 14px; cursor: pointer;" 
                    @click="showSecurityLevelInfo"
                  />
                </span>
              </template>
              <a-select v-model="editForm.security_level" placeholder="请选择安全防护等级">
                <a-option value="低防护级别">低防护级别</a-option>
                <a-option value="中低防护级别">中低防护级别</a-option>
                <a-option value="中高防护级别">中高防护级别</a-option>
                <a-option value="高防护级别">高防护级别</a-option>
              </a-select>
            </a-form-item>
          </a-col>
          <a-col :span="12">
            <a-form-item label="管理员联系方式">
              <a-input v-model="editForm.admin_contact" placeholder="请输入联系方式" />
            </a-form-item>
          </a-col>
        </a-row>
        <a-form-item label="资产描述">
          <a-textarea
            v-model="editForm.asset_description"
            placeholder="请描述资产详细信息"
            :auto-size="{ minRows: 2, maxRows: 4 }"
          />
        </a-form-item>
      </a-form>
    </a-modal>

    <!-- 安全防护等级详情弹窗 -->
    <a-modal
      v-model:visible="showSecurityInfoModal"
      title="安全防护等级详细说明"
      @ok="showSecurityInfoModal = false"
      @cancel="showSecurityInfoModal = false"
      width="800px"
      :footer="false"
    >
      <div class="security-level-content">
        <div class="security-level-item">
          <h3 class="level-title">1. 低防护级别</h3>
          <p class="level-description">
            主要用于保护一些非常基础的信息，如一般的公开信息或无机密性的数据。这个级别的系统主要采用一些基本的安全措施，如网络防火墙、入侵检测系统等。
          </p>
        </div>

        <div class="security-level-item">
          <h3 class="level-title">2. 中低防护级别</h3>
          <p class="level-description">
            主要用于保护一些具有一定机密性或重要性的信息，但受到的风险相对较低。这个级别的系统除了基本的安全措施外，还会采用一些额外的安全措施，如加密传输、用户身份认证等。
          </p>
        </div>

        <div class="security-level-item">
          <h3 class="level-title">3. 中高防护级别</h3>
          <p class="level-description">
            主要用于保护一些具有较高机密性或重要性的信息，可能会受到一定风险的影响。这个级别的系统除了基本的安全措施外，还会采用更加复杂的安全措施，如多层防护、安全审计等。
          </p>
        </div>

        <div class="security-level-item">
          <h3 class="level-title">4. 高防护级别</h3>
          <p class="level-description">
            主要用于保护一些非常重要、具有高度机密性的信息，可能会面临严重的安全风险。这个级别的系统会采用最严格的安全措施，包括但不限于：访问控制、数据加密、安全监控、备份与恢复等多重防护机制。
          </p>
        </div>

        <div class="security-tips">
          <a-alert type="info" show-icon>
            <template #icon>
              <icon-info-circle />
            </template>
            <p><strong>选择建议：</strong></p>
            <ul>
              <li>核心业务系统、数据库服务器建议选择"高防护级别"</li>
              <li>一般业务服务器可选择"中高防护级别"</li>
              <li>办公网络设备可选择"中低防护级别"</li>
              <li>测试环境、临时设备可选择"低防护级别"</li>
            </ul>
          </a-alert>
        </div>
      </div>
    </a-modal>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { Message, Modal } from '@arco-design/web-vue'
import PageHeader from '@/components/PageHeader.vue'
import StatCard from '@/components/StatCard.vue'
import { assetsApi, type Asset } from '@/services/assets'
import {
  IconRefresh,
  IconPlus,
  IconDesktop,
  IconCheck,
  IconExclamation,
  IconClose,
  IconWifi,
  IconLock,
  IconQuestionCircle,
  IconInfoCircle,
} from '@arco-design/web-vue/es/icon'

// 资产数据
const assetData = ref<Asset[]>([])
const loading = ref(false)
const showAddModal = ref(false)
const continuousAdd = ref(false) // 连续添加模式

// 添加资产表单数据
const addForm = ref({
  name: '',
  asset_type: '',
  ip_address: '',
  location: '',
  security_level: '',
  admin_contact: '',
  asset_description: '',
  last_security_scan: '',
})

// 编辑资产数据
const editForm = ref({
  id: '',
  name: '',
  asset_type: '',
  ip_address: '',
  location: '',
  security_level: '',
  admin_contact: '',
  asset_description: '',
  last_security_scan: '',
})

const showEditModal = ref(false)
const showSecurityInfoModal = ref(false)

// 统计数据计算
const stats = computed(() => {
  const total = assetData.value.length
  const online = assetData.value.filter((item) => item.status === 'normal').length
  const warning = assetData.value.filter((item) => item.status === 'warning').length
  const error = assetData.value.filter((item) => item.status === 'error').length

  return { total, online, warning, error }
})

// 获取资产列表
const fetchAssets = async () => {
  try {
    loading.value = true
    const data = await assetsApi.getAssets()
    assetData.value = data
  } catch (error) {
    console.error('获取资产列表失败:', error)
    Message.error('获取资产列表失败')
  } finally {
    loading.value = false
  }
}

// 刷新数据
const handleRefresh = () => {
  fetchAssets()
}

// 显示添加资产弹窗
const showAddAsset = () => {
  showAddModal.value = true
}

// 显示连续添加模式
const showContinuousAdd = () => {
  continuousAdd.value = true
  showAddModal.value = true
}

// 显示安全防护等级详情
const showSecurityLevelInfo = () => {
  showSecurityInfoModal.value = true
}

// 添加资产
const handleAddAsset = async () => {
  try {
    if (!addForm.value.name || !addForm.value.asset_type || !addForm.value.ip_address) {
      Message.warning('请填写必填项')
      return
    }

    await assetsApi.createAsset(addForm.value)
    Message.success('资产添加成功')

    if (continuousAdd.value) {
      // 连续添加模式：只重置关键字段，保留其他信息
      const preservedData = {
        asset_type: addForm.value.asset_type,
        location: addForm.value.location,
        security_level: addForm.value.security_level,
        admin_contact: addForm.value.admin_contact,
        asset_description: addForm.value.asset_description,
      }

      addForm.value = {
        name: '',
        asset_type: preservedData.asset_type,
        ip_address: '',
        location: preservedData.location,
        security_level: preservedData.security_level,
        admin_contact: preservedData.admin_contact,
        asset_description: preservedData.asset_description,
        last_security_scan: '',
      }

      Message.info('已保留相关信息，请继续添加下一个资产')
    } else {
      // 普通模式：关闭弹窗并重置表单
      showAddModal.value = false
      resetAddForm()
    }

    // 刷新列表
    fetchAssets()
  } catch (error) {
    console.error('添加资产失败:', error)
    Message.error('添加资产失败')
  }
}

// 重置添加表单
const resetAddForm = () => {
  addForm.value = {
    name: '',
    asset_type: '',
    ip_address: '',
    location: '',
    security_level: '',
    admin_contact: '',
    asset_description: '',
    last_security_scan: '',
  }
  continuousAdd.value = false
  showAddModal.value = false
}

// 查看资产详情
const viewAsset = (record: Asset) => {
  // 可以导航到详情页或显示详情弹窗
  console.log('查看资产:', record)
}

// 编辑资产
const editAsset = (record: Asset) => {
  editForm.value = {
    id: record.id.toString(),
    name: record.name,
    asset_type: record.asset_type,
    ip_address: record.ip_address,
    location: record.location,
    security_level: record.security_level,
    admin_contact: record.admin_contact || '',
    asset_description: record.asset_description || '',
    last_security_scan: record.last_security_scan || '',
  }
  showEditModal.value = true
}

// 处理编辑资产
const handleEditAsset = async () => {
  try {
    if (!editForm.value.name || !editForm.value.asset_type || !editForm.value.ip_address) {
      Message.warning('请填写必填项')
      return
    }

    await assetsApi.updateAsset(Number(editForm.value.id), editForm.value)
    Message.success('资产更新成功')
    showEditModal.value = false

    // 刷新列表
    fetchAssets()
  } catch (error) {
    console.error('更新资产失败:', error)
    Message.error('更新资产失败')
  }
}

// 删除资产
const deleteAsset = (record: Asset) => {
  Modal.confirm({
    title: '确认删除',
    content: `确定要删除资产 "${record.name}" 吗？此操作不可恢复。`,
    onOk: async () => {
      try {
        await assetsApi.deleteAsset(record.id)
        Message.success('资产删除成功')
        // 刷新列表
        fetchAssets()
      } catch (error) {
        console.error('删除资产失败:', error)
        Message.error('删除资产失败')
      }
    },
  })
}

// 页面加载时获取数据
onMounted(() => {
  fetchAssets()
})

// 表格列配置
const assetColumns = [
  {
    title: '设备信息',
    dataIndex: 'name',
    slotName: 'deviceInfo',
    width: 250,
  },
  {
    title: '设备类型',
    dataIndex: 'asset_type',
    slotName: 'type',
    width: 100,
  },
  {
    title: 'IP地址',
    dataIndex: 'ip_address',
    width: 120,
  },
  {
    title: '位置',
    dataIndex: 'location',
    width: 120,
  },
  {
    title: '状态',
    dataIndex: 'status',
    slotName: 'status',
    width: 100,
  },
  {
    title: '最后更新',
    dataIndex: 'updated_at',
    width: 160,
  },
  {
    title: '操作',
    slotName: 'actions',
    width: 150,
    fixed: 'right',
  },
]

// 工具函数
const getDeviceIcon = (type: string) => {
  switch (type) {
    case 'linux_server':
    case 'windows_server':
      return IconDesktop
    case 'network_device':
      return IconWifi
    case 'k8s_cluster':
      return IconLock
    default:
      return IconDesktop
  }
}

const getTypeColor = (type: string) => {
  switch (type) {
    case 'linux_server':
    case 'windows_server':
      return 'blue'
    case 'network_device':
      return 'green'
    case 'k8s_cluster':
      return 'red'
    default:
      return 'gray'
  }
}

const getTypeName = (type: string) => {
  switch (type) {
    case 'linux_server':
      return 'Linux服务器'
    case 'windows_server':
      return 'Windows服务器'
    case 'network_device':
      return '网络设备'
    case 'k8s_cluster':
      return 'K8S集群'
    default:
      return '未知'
  }
}

const getStatusType = (status: string) => {
  switch (status) {
    case 'normal':
      return 'success'
    case 'warning':
      return 'warning'
    case 'error':
      return 'error'
    default:
      return 'default'
  }
}

const getStatusText = (status: string) => {
  switch (status) {
    case 'normal':
      return '在线'
    case 'warning':
      return '异常'
    case 'error':
      return '离线'
    default:
      return '未知'
  }
}
</script>

<style scoped>
.assets-page {
  padding: 0;
}

.stats-row {
  margin-bottom: 24px;
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

.device-model {
  font-size: 12px;
  color: #86909c;
}

:deep(.arco-card) {
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

/* 安全防护等级详情样式 */
.security-level-content {
  padding: 8px 0;
}

.security-level-item {
  margin-bottom: 24px;
  padding: 16px;
  background: #f8f9fa;
  border-radius: 8px;
  border-left: 4px solid #1890ff;
}

.level-title {
  margin: 0 0 12px 0;
  font-size: 16px;
  font-weight: 600;
  color: #1d2129;
}

.level-description {
  margin: 0;
  font-size: 14px;
  line-height: 1.6;
  color: #4e5969;
}

.security-tips {
  margin-top: 20px;
}

.security-tips ul {
  margin: 8px 0 0 0;
  padding-left: 20px;
}

.security-tips li {
  margin-bottom: 4px;
  font-size: 14px;
  color: #4e5969;
}
</style>
