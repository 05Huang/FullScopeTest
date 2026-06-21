import api, { ApiResponse } from './api'

// ==================== 用例集管理 ====================

export const getCollections = (projectId?: number): Promise<ApiResponse> => {
  return api.get('/app-test/collections', { params: { project_id: projectId } }) as Promise<ApiResponse>
}

export const createCollection = (data: {
  name: string
  description?: string
  project_id?: number
}): Promise<ApiResponse> => {
  return api.post('/app-test/collections', data) as Promise<ApiResponse>
}

export const updateCollection = (id: number, data: {
  name?: string
  description?: string
  sort_order?: number
}): Promise<ApiResponse> => {
  return api.put(`/app-test/collections/${id}`, data) as Promise<ApiResponse>
}

export const deleteCollection = (id: number): Promise<ApiResponse> => {
  return api.delete(`/app-test/collections/${id}`) as Promise<ApiResponse>
}

// ==================== 脚本管理 ====================

export const getScripts = (params?: {
  project_id?: number
  collection_id?: number
}): Promise<ApiResponse> => {
  return api.get('/app-test/scripts', { params }) as Promise<ApiResponse>
}

export const getScript = (id: number): Promise<ApiResponse> => {
  return api.get(`/app-test/scripts/${id}`) as Promise<ApiResponse>
}

export const createScript = (data: {
  name: string
  description?: string
  project_id?: number
  collection_id?: number
  platform?: string
  app_path?: string
  app_package?: string
  app_activity?: string
  bundle_id?: string
  device_name?: string
  platform_version?: string
  automation_name?: string
  appium_server?: string
  script_content?: string
}): Promise<ApiResponse> => {
  return api.post('/app-test/scripts', data) as Promise<ApiResponse>
}

export const updateScript = (id: number, data: {
  name?: string
  description?: string
  collection_id?: number | null
  platform?: string
  app_path?: string
  app_package?: string
  app_activity?: string
  bundle_id?: string
  device_name?: string
  platform_version?: string
  automation_name?: string
  appium_server?: string
  script_content?: string
  is_enabled?: boolean
  sort_order?: number
}): Promise<ApiResponse> => {
  return api.put(`/app-test/scripts/${id}`, data) as Promise<ApiResponse>
}

export const deleteScript = (id: number): Promise<ApiResponse> => {
  return api.delete(`/app-test/scripts/${id}`) as Promise<ApiResponse>
}

// ==================== 执行测试 ====================

export const runScript = (scriptId: number): Promise<ApiResponse> => {
  return api.post(`/app-test/scripts/${scriptId}/run`) as Promise<ApiResponse>
}

// ==================== 健康检查 ====================

export const healthCheck = (): Promise<ApiResponse> => {
  return api.get('/app-test/health') as Promise<ApiResponse>
}

// 导出服务对象
// 获取设备列表
export const getDevices = (params?: { project_id?: number; status?: string }): Promise<ApiResponse> => {
  return api.get('/app-test/devices', { params }) as Promise<ApiResponse>
}

// 获取单个设备
export const getDevice = (deviceId: number): Promise<ApiResponse> => {
  return api.get(`/app-test/devices/${deviceId}`) as Promise<ApiResponse>
}

// 更新设备
export const updateDevice = (deviceId: number, data: Record<string, unknown>): Promise<ApiResponse> => {
  return api.put(`/app-test/devices/${deviceId}`, data) as Promise<ApiResponse>
}

// 删除设备
export const deleteDevice = (deviceId: number): Promise<ApiResponse> => {
  return api.delete(`/app-test/devices/${deviceId}`) as Promise<ApiResponse>
}

export const appTestService = {
  getCollections,
  createCollection,
  updateCollection,
  deleteCollection,
  getScripts,
  getScript,
  createScript,
  updateScript,
  deleteScript,
  runScript,
  healthCheck,
  getDevices,
  getDevice,
  updateDevice,
  deleteDevice,
}
