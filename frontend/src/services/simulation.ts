import { post } from './api'

// 模拟控制API服务
export const simulationApi = {
  // 触发故障
  triggerFault(): Promise<{ success: boolean; message: string }> {
    return post('/simulation/trigger-fault')
  },

  // 修复故障
  fixFault(): Promise<{ success: boolean; message: string }> {
    return post('/simulation/fix-fault')
  },

  // 初始化演示数据
  initDemoData(): Promise<{ success: boolean; message: string }> {
    return post('/simulation/init-data')
  },
}

export default simulationApi