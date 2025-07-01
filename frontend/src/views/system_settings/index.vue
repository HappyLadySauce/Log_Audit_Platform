<template>
  <div class="system-settings">
    <div class="page-header">
      <h1>系统设置</h1>
      <p>管理系统配置和参数设置</p>
    </div>

    <div class="settings-content">
      <a-row :gutter="24">
        <a-col :span="16">
          <a-card title="基本设置" class="settings-card">
            <a-form :model="systemSettings" layout="vertical">
              <a-row :gutter="16">
                <a-col :span="12">
                  <a-form-item label="系统名称">
                    <a-input v-model="systemSettings.systemName" placeholder="输入系统名称" />
                  </a-form-item>
                </a-col>
                <a-col :span="12">
                  <a-form-item label="系统版本">
                    <a-input v-model="systemSettings.systemVersion" placeholder="输入系统版本" disabled />
                  </a-form-item>
                </a-col>
                <a-col :span="12">
                  <a-form-item label="管理员邮箱">
                    <a-input v-model="systemSettings.adminEmail" placeholder="输入管理员邮箱" />
                  </a-form-item>
                </a-col>
                <a-col :span="12">
                  <a-form-item label="系统时区">
                    <a-select v-model="systemSettings.timezone" placeholder="选择时区">
                      <a-option value="Asia/Shanghai">Asia/Shanghai (UTC+8)</a-option>
                      <a-option value="UTC">UTC (UTC+0)</a-option>
                      <a-option value="America/New_York">America/New_York (UTC-5)</a-option>
                    </a-select>
                  </a-form-item>
                </a-col>
                <a-col :span="24">
                  <a-form-item label="系统描述">
                    <a-textarea v-model="systemSettings.description" placeholder="输入系统描述" :rows="4" />
                  </a-form-item>
                </a-col>
              </a-row>
            </a-form>
          </a-card>

          <a-card title="日志设置" class="settings-card" style="margin-top: 16px;">
            <a-form :model="logSettings" layout="vertical">
              <a-row :gutter="16">
                <a-col :span="12">
                  <a-form-item label="日志保留天数">
                    <a-input-number v-model="logSettings.retentionDays" :min="1" :max="365" />
                  </a-form-item>
                </a-col>
                <a-col :span="12">
                  <a-form-item label="最大日志文件大小 (MB)">
                    <a-input-number v-model="logSettings.maxFileSize" :min="1" :max="1024" />
                  </a-form-item>
                </a-col>
                <a-col :span="12">
                  <a-form-item label="日志级别">
                    <a-select v-model="logSettings.logLevel" placeholder="选择日志级别">
                      <a-option value="DEBUG">DEBUG</a-option>
                      <a-option value="INFO">INFO</a-option>
                      <a-option value="WARNING">WARNING</a-option>
                      <a-option value="ERROR">ERROR</a-option>
                    </a-select>
                  </a-form-item>
                </a-col>
                <a-col :span="12">
                  <a-form-item label="自动备份">
                    <a-switch v-model="logSettings.autoBackup" />
                  </a-form-item>
                </a-col>
              </a-row>
            </a-form>
          </a-card>

          <a-card title="安全设置" class="settings-card" style="margin-top: 16px;">
            <a-form :model="securitySettings" layout="vertical">
              <a-row :gutter="16">
                <a-col :span="12">
                  <a-form-item label="会话超时时间 (分钟)">
                    <a-input-number v-model="securitySettings.sessionTimeout" :min="5" :max="1440" />
                  </a-form-item>
                </a-col>
                <a-col :span="12">
                  <a-form-item label="密码最小长度">
                    <a-input-number v-model="securitySettings.minPasswordLength" :min="6" :max="32" />
                  </a-form-item>
                </a-col>
                <a-col :span="12">
                  <a-form-item label="启用双因素认证">
                    <a-switch v-model="securitySettings.enableTwoFactor" />
                  </a-form-item>
                </a-col>
                <a-col :span="12">
                  <a-form-item label="登录失败锁定">
                    <a-switch v-model="securitySettings.lockoutEnabled" />
                  </a-form-item>
                </a-col>
              </a-row>
            </a-form>
          </a-card>

          <div class="settings-actions" style="margin-top: 24px;">
            <a-space>
              <a-button type="primary" @click="saveSettings" :loading="saveLoading">
                保存设置
              </a-button>
              <a-button @click="resetSettings">重置设置</a-button>
              <a-button @click="exportSettings">导出配置</a-button>
            </a-space>
          </div>
        </a-col>

        <a-col :span="8">
          <a-card title="系统状态" class="status-card">
            <a-descriptions :column="1" size="small">
              <a-descriptions-item label="系统运行时间">
                <a-tag color="green">{{ systemStatus.uptime }}</a-tag>
              </a-descriptions-item>
              <a-descriptions-item label="CPU 使用率">
                <a-progress
                  :percent="systemStatus.cpuUsage"
                  :color="systemStatus.cpuUsage > 80 ? '#f53f3f' : '#00b42a'"
                  size="small"
                />
              </a-descriptions-item>
              <a-descriptions-item label="内存使用率">
                <a-progress
                  :percent="systemStatus.memoryUsage"
                  :color="systemStatus.memoryUsage > 80 ? '#f53f3f' : '#00b42a'"
                  size="small"
                />
              </a-descriptions-item>
              <a-descriptions-item label="磁盘使用率">
                <a-progress
                  :percent="systemStatus.diskUsage"
                  :color="systemStatus.diskUsage > 80 ? '#f53f3f' : '#00b42a'"
                  size="small"
                />
              </a-descriptions-item>
              <a-descriptions-item label="网络状态">
                <a-badge
                  :status="systemStatus.networkStatus === 'online' ? 'success' : 'error'"
                  :text="systemStatus.networkStatus === 'online' ? '正常' : '异常'"
                />
              </a-descriptions-item>
              <a-descriptions-item label="数据库状态">
                <a-badge
                  :status="systemStatus.databaseStatus === 'connected' ? 'success' : 'error'"
                  :text="systemStatus.databaseStatus === 'connected' ? '已连接' : '连接异常'"
                />
              </a-descriptions-item>
            </a-descriptions>
          </a-card>

          <a-card title="最近操作" class="recent-actions-card" style="margin-top: 16px;">
            <a-timeline>
              <a-timeline-item
                v-for="(action, index) in recentActions"
                :key="index"
              >
                <div class="timeline-content">
                  <div class="action-description">{{ action.description }}</div>
                  <div class="action-time">{{ action.time }}</div>
                </div>
              </a-timeline-item>
            </a-timeline>
          </a-card>
        </a-col>
      </a-row>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { Message } from '@arco-design/web-vue'

// 系统设置数据
const systemSettings = ref({
  systemName: '综合日志审计分析平台',
  systemVersion: 'v1.0.0',
  adminEmail: 'admin@example.com',
  timezone: 'Asia/Shanghai',
  description: '基于AI的综合日志审计分析平台，提供全面的日志收集、分析和告警功能。'
})

// 日志设置数据
const logSettings = ref({
  retentionDays: 30,
  maxFileSize: 100,
  logLevel: 'INFO',
  autoBackup: true
})

// 安全设置数据
const securitySettings = ref({
  sessionTimeout: 60,
  minPasswordLength: 8,
  enableTwoFactor: false,
  lockoutEnabled: true
})

// 系统状态数据
const systemStatus = ref({
  uptime: '7天 12小时 30分钟',
  cpuUsage: 35,
  memoryUsage: 68,
  diskUsage: 45,
  networkStatus: 'online',
  databaseStatus: 'connected'
})

// 最近操作记录
const recentActions = ref([
  {
    description: '修改了系统时区设置',
    time: '2025-01-19 14:30:00'
  },
  {
    description: '更新了日志保留策略',
    time: '2025-01-19 10:15:00'
  },
  {
    description: '启用了自动备份功能',
    time: '2025-01-18 16:45:00'
  },
  {
    description: '修改了管理员邮箱',
    time: '2025-01-18 09:20:00'
  }
])

const saveLoading = ref(false)

// 保存设置
const saveSettings = async () => {
  saveLoading.value = true
  try {
    // 模拟API调用
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    Message.success('设置保存成功！')
    
    // 添加到最近操作记录
    recentActions.value.unshift({
      description: '保存了系统设置',
      time: new Date().toLocaleString('zh-CN')
    })
    
    // 只保留最近5条记录
    if (recentActions.value.length > 5) {
      recentActions.value = recentActions.value.slice(0, 5)
    }
  } catch (error) {
    Message.error('保存设置失败！')
  } finally {
    saveLoading.value = false
  }
}

// 重置设置
const resetSettings = () => {
  systemSettings.value = {
    systemName: '综合日志审计分析平台',
    systemVersion: 'v1.0.0',
    adminEmail: 'admin@example.com',
    timezone: 'Asia/Shanghai',
    description: '基于AI的综合日志审计分析平台，提供全面的日志收集、分析和告警功能。'
  }
  
  logSettings.value = {
    retentionDays: 30,
    maxFileSize: 100,
    logLevel: 'INFO',
    autoBackup: true
  }
  
  securitySettings.value = {
    sessionTimeout: 60,
    minPasswordLength: 8,
    enableTwoFactor: false,
    lockoutEnabled: true
  }
  
  Message.info('设置已重置为默认值')
}

// 导出配置
const exportSettings = () => {
  const config = {
    system: systemSettings.value,
    log: logSettings.value,
    security: securitySettings.value,
    exportTime: new Date().toLocaleString('zh-CN')
  }
  
  const dataStr = JSON.stringify(config, null, 2)
  const dataBlob = new Blob([dataStr], { type: 'application/json' })
  const url = URL.createObjectURL(dataBlob)
  
  const link = document.createElement('a')
  link.href = url
  link.download = `system-settings-${Date.now()}.json`
  link.click()
  
  URL.revokeObjectURL(url)
  Message.success('配置文件已导出')
}

// 定时更新系统状态
const updateSystemStatus = () => {
  // 模拟系统状态更新
  systemStatus.value.cpuUsage = Math.floor(Math.random() * 100)
  systemStatus.value.memoryUsage = Math.floor(Math.random() * 100)
  systemStatus.value.diskUsage = Math.floor(Math.random() * 100)
}

onMounted(() => {
  // 每30秒更新一次系统状态
  setInterval(updateSystemStatus, 30000)
})
</script>

<style scoped>
.system-settings {
  padding: 24px;
  background: #f7f8fa;
  min-height: 100vh;
}

.page-header {
  margin-bottom: 24px;
}

.page-header h1 {
  font-size: 24px;
  font-weight: 600;
  color: #1d2129;
  margin: 0 0 8px 0;
}

.page-header p {
  color: #86909c;
  margin: 0;
}

.settings-content {
  max-width: 1400px;
}

.settings-card {
  margin-bottom: 16px;
}

.settings-card :deep(.arco-card-header) {
  border-bottom: 1px solid #e5e6eb;
  padding: 16px 20px;
}

.settings-card :deep(.arco-card-header-title) {
  font-size: 16px;
  font-weight: 600;
  color: #1d2129;
}

.settings-card :deep(.arco-card-body) {
  padding: 20px;
}

.status-card {
  height: fit-content;
}

.status-card :deep(.arco-card-header) {
  border-bottom: 1px solid #e5e6eb;
}

.recent-actions-card {
  height: fit-content;
}

.timeline-content {
  padding-left: 8px;
}

.action-description {
  font-size: 14px;
  color: #1d2129;
  margin-bottom: 4px;
}

.action-time {
  font-size: 12px;
  color: #86909c;
}

.settings-actions {
  display: flex;
  justify-content: flex-start;
  padding: 16px 0;
}

:deep(.arco-form-item-label) {
  font-weight: 500;
  color: #1d2129;
}

:deep(.arco-descriptions-item-label) {
  font-weight: 500;
  color: #4e5969;
}

:deep(.arco-timeline-item-content) {
  min-height: auto;
}
</style> 