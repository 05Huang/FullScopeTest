import api from './api'

// ==================== 环境管理 ====================

export const getEnvironments = (projectId?: number) => {
  return api.get('/environments', { params: { project_id: projectId } })
}

export const createEnvironment = (data: {
  name: string
  base_url: string
  description?: string
  variables?: Record<string, any>
  project_id?: number
  is_default?: boolean
}) => {
  return api.post('/environments', data)
}

export const getEnvironment = (id: number) => {
  return api.get(`/environments/${id}`)
}

export const updateEnvironment = (id: number, data: {
  name?: string
  base_url?: string
  description?: string
  variables?: Record<string, any>
  is_default?: boolean
}) => {
  return api.put(`/environments/${id}`, data)
}

export const deleteEnvironment = (id: number) => {
  return api.delete(`/environments/${id}`)
}

export const setDefaultEnvironment = (id: number) => {
  return api.put(`/environments/${id}/default`)
}

// 导出服务对象
export const environmentService = {
  getEnvironments,
  createEnvironment,
  getEnvironment,
  updateEnvironment,
  deleteEnvironment,
  setDefaultEnvironment,
}
