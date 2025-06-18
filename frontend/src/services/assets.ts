import { get, post, put, del } from './api'

// 资产相关类型定义
export interface Asset {
  id: number
  name: string
  asset_type: string
  ip_address: string
  location: string
  security_level: string
  status: string
  created_at: string
  updated_at: string
}

export interface AssetCreate {
  name: string
  asset_type: string
  ip_address: string
  location: string
  security_level: string
}

export interface AssetUpdate {
  name?: string
  asset_type?: string
  ip_address?: string
  location?: string
  security_level?: string
  status?: string
}

// 资产API服务
export const assetsApi = {
  // 获取资产列表
  getAssets(params?: {
    asset_type?: string
    status?: string
    skip?: number
    limit?: number
  }): Promise<Asset[]> {
    return get('/assets', params)
  },

  // 获取单个资产详情
  getAsset(id: number): Promise<Asset> {
    return get(`/assets/${id}`)
  },

  // 创建资产
  createAsset(data: AssetCreate): Promise<Asset> {
    return post('/assets', data)
  },

  // 更新资产
  updateAsset(id: number, data: AssetUpdate): Promise<Asset> {
    return put(`/assets/${id}`, data)
  },

  // 删除资产
  deleteAsset(id: number): Promise<{ success: boolean; message: string }> {
    return del(`/assets/${id}`)
  },
}

export default assetsApi
