import api, { ApiResponse } from './api'

// ==================== 环境管理 ====================

export const getEnvironments = (projectId?: number): Promise<ApiResponse> => {
  return api.get('/environments', { params: { project_id: projectId } }) as Promise<ApiResponse>
}

export const createEnvironment = (data: {
  name: string
  base_url: string
  description?: string
  variables?: Record<string, any>
  project_id?: number
  is_default?: boolean
}): Promise<ApiResponse> => {
  return api.post('/environments', data) as Promise<ApiResponse>
}

export const getEnvironment = (id: number): Promise<ApiResponse> => {
  return api.get(`/environments/${id}`) as Promise<ApiResponse>
}

export const updateEnvironment = (id: number, data: {
  name?: string
  base_url?: string
  description?: string
  variables?: Record<string, any>
  is_default?: boolean
  is_active?: boolean
}): Promise<ApiResponse> => {
  return api.put(`/environments/${id}`, data) as Promise<ApiResponse>
}

export const deleteEnvironment = (id: number): Promise<ApiResponse> => {
  return api.delete(`/environments/${id}`) as Promise<ApiResponse>
}


// 导出服务对象
export const environmentService = {
  getEnvironments,
  createEnvironment,
  getEnvironment,
  updateEnvironment,
  deleteEnvironment,
}
