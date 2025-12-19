import api, { ApiResponse } from './api'

// ==================== 脚本管理 ====================

export const getScripts = (projectId?: number): Promise<ApiResponse> => {
  return api.get('/web-test/scripts', { params: { project_id: projectId } }) as Promise<ApiResponse>
}

export const createScript = (data: {
  name: string
  description?: string
  target_url?: string
  browser?: string
  script_content?: string
  config?: Record<string, any>
  project_id?: number
}): Promise<ApiResponse> => {
  return api.post('/web-test/scripts', data) as Promise<ApiResponse>
}

export const getScript = (id: number): Promise<ApiResponse> => {
  return api.get(`/web-test/scripts/${id}`) as Promise<ApiResponse>
}

export const updateScript = (id: number, data: {
  name?: string
  description?: string
  target_url?: string
  browser?: string
  script_content?: string
  config?: Record<string, any>
}): Promise<ApiResponse> => {
  return api.put(`/web-test/scripts/${id}`, data) as Promise<ApiResponse>
}

export const deleteScript = (id: number): Promise<ApiResponse> => {
  return api.delete(`/web-test/scripts/${id}`) as Promise<ApiResponse>
}

// ==================== 执行测试 ====================

export const runScript = (scriptId: number, headless?: boolean): Promise<ApiResponse> => {
  return api.post(`/web-test/scripts/${scriptId}/run`, { headless }) as Promise<ApiResponse>
}

export const executeWebCode = (data: {
  code: string
  headless?: boolean
}): Promise<ApiResponse> => {
  return api.post('/web-test/execute', data) as Promise<ApiResponse>
}

// ==================== 录制功能 ====================

export const startRecording = (data: {
  url: string
  browser?: string
}): Promise<ApiResponse> => {
  return api.post('/web-test/record/start', data) as Promise<ApiResponse>
}

export const stopRecording = (): Promise<ApiResponse> => {
  return api.post('/web-test/record/stop') as Promise<ApiResponse>
}

export const getRecordingStatus = (): Promise<ApiResponse> => {
  return api.get('/web-test/record/status') as Promise<ApiResponse>
}

// 导出服务对象
export const webTestService = {
  getScripts,
  createScript,
  getScript,
  updateScript,
  deleteScript,
  runScript,
  executeWebCode,
  startRecording,
  stopRecording,
  getRecordingStatus,
}
