 // API基础配置和请求封装
const API_BASE_URL = 'http://localhost:8000/api'

interface ApiResponse<T = any> {
  success: boolean
  message: string
  data?: T
}

// 请求封装
async function request<T = any>(
  url: string,
  options: RequestInit = {}
): Promise<T> {
  const config: RequestInit = {
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
    ...options,
  }

  try {
    const response = await fetch(`${API_BASE_URL}${url}`, config)
    
    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}))
      throw new Error(errorData.detail || `HTTP ${response.status}: ${response.statusText}`)
    }

    const data = await response.json()
    return data
  } catch (error) {
    console.error('API请求失败:', error)
    throw error
  }
}

// GET请求
export function get<T = any>(url: string, params?: Record<string, any>): Promise<T> {
  const searchParams = params ? new URLSearchParams(params).toString() : ''
  const fullUrl = searchParams ? `${url}?${searchParams}` : url
  
  return request<T>(fullUrl, {
    method: 'GET',
  })
}

// POST请求
export function post<T = any>(url: string, data?: any): Promise<T> {
  return request<T>(url, {
    method: 'POST',
    body: data ? JSON.stringify(data) : undefined,
  })
}

// PUT请求
export function put<T = any>(url: string, data?: any): Promise<T> {
  return request<T>(url, {
    method: 'PUT',
    body: data ? JSON.stringify(data) : undefined,
  })
}

// DELETE请求
export function del<T = any>(url: string): Promise<T> {
  return request<T>(url, {
    method: 'DELETE',
  })
}

export default {
  get,
  post,
  put,
  delete: del,
}