import { get, post, put, del } from './api'

// 告警相关类型定义
export interface AlertRule {
  id: number
  name: string
  target_asset_id: number
  trigger_condition: string
  alert_level: string
  is_active: string
  created_at: string
}

export interface Alert {
  id: number
  rule_id: number
  asset_id: number
  title: string
  description?: string
  alert_level: string
  status: string
  triggered_at: string
  processed_at?: string
  resolved_at?: string
  processor?: string
  root_cause?: string
  solution?: string
  remaining_issues?: string
  asset?: any
  rule?: AlertRule
}

export interface AlertStats {
  pending: number
  resolved: number
  archived: number
}

export interface AlertProcess {
  processor: string
}

export interface AlertArchive {
  processor: string
  root_cause: string
  solution: string
  remaining_issues?: string
}

// 告警API服务
export const alertsApi = {
  // 获取告警规则列表
  getAlertRules(params?: { skip?: number; limit?: number }): Promise<AlertRule[]> {
    return get('/alert-rules', params)
  },

  // 创建告警规则
  createAlertRule(data: any): Promise<AlertRule> {
    return post('/alert-rules', data)
  },

  // 更新告警规则
  updateAlertRule(id: number, data: any): Promise<AlertRule> {
    return put(`/alert-rules/${id}`, data)
  },

  // 删除告警规则
  deleteAlertRule(id: number): Promise<void> {
    return del(`/alert-rules/${id}`)
  },

  // 获取告警记录列表
  getAlerts(params?: {
    status?: string
    alert_level?: string
    skip?: number
    limit?: number
  }): Promise<Alert[]> {
    return get('/alerts', params)
  },

  // 获取告警统计
  getAlertStats(): Promise<AlertStats> {
    return get('/alerts/stats')
  },

  // 获取单个告警详情
  getAlert(id: number): Promise<Alert> {
    return get(`/alerts/${id}`)
  },

  // 创建告警记录
  createAlert(data: any): Promise<Alert> {
    return post('/alerts', data)
  },

  // 开始处理告警
  processAlert(id: number, data: AlertProcess): Promise<Alert> {
    return post(`/alerts/${id}/process`, data)
  },

  // 解决告警
  resolveAlert(id: number): Promise<Alert> {
    return post(`/alerts/${id}/resolve`)
  },

  // 归档告警
  archiveAlert(id: number, data: AlertArchive): Promise<Alert> {
    return post(`/alerts/${id}/archive`, data)
  },

  // 忽略告警
  ignoreAlert(id: number): Promise<Alert> {
    return post(`/alerts/${id}/ignore`)
  },

  // 删除告警记录
  deleteAlert(id: number): Promise<void> {
    return del(`/alerts/${id}`)
  },
}

export default alertsApi
