import api, { ApiResponse } from './api'

// ==================== 脚本管理 ====================

export const getScripts = (params?: {
  project_id?: number
  collection_id?: number
}): Promise<ApiResponse> => {
  return api.get('/web-test/scripts', { params }) as Promise<ApiResponse>
}

export const createScript = (data: {
  name: string
  description?: string
  collection_id?: number | null
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
  collection_id?: number | null
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

// ==================== 用例集管理 ====================

export const getCollections = (projectId?: number): Promise<ApiResponse> => {
  return api.get('/web-test/collections', { params: { project_id: projectId } }) as Promise<ApiResponse>
}

export const createCollection = (data: {
  name: string
  description?: string
  project_id?: number
  sort_order?: number
}): Promise<ApiResponse> => {
  return api.post('/web-test/collections', data) as Promise<ApiResponse>
}

export const updateCollection = (id: number, data: {
  name?: string
  description?: string
  sort_order?: number
}): Promise<ApiResponse> => {
  return api.put(`/web-test/collections/${id}`, data) as Promise<ApiResponse>
}

export const deleteCollection = (id: number): Promise<ApiResponse> => {
  return api.delete(`/web-test/collections/${id}`) as Promise<ApiResponse>
}

export const runCollection = (collectionId: number): Promise<ApiResponse> => {
  return api.post(`/web-test/collections/${collectionId}/run`) as Promise<ApiResponse>
}

// ==================== 执行测试 ====================

export const runScript = (scriptId: number, headless?: boolean): Promise<ApiResponse> => {
  return api.post(`/web-test/scripts/${scriptId}/run`, { headless }) as Promise<ApiResponse>
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

// ==================== AI ====================

export const generateScriptAI = (data: {
  prompt: string
  base_url?: string
  model?: string
  api_key?: string
}): Promise<ApiResponse> => {
  return api.post('/web-test/ai/generate', data) as Promise<ApiResponse>
}

export const analyzeErrorAI = (data: {
  script_id: number
  error_log: string
  base_url?: string
  model?: string
  api_key?: string
}): Promise<ApiResponse> => {
  return api.post('/web-test/ai/analyze-error', data) as Promise<ApiResponse>
}

export const exploreWebAppAI = (data: {
  start_url: string
  objective?: string
  max_steps?: number
  base_url?: string
  model?: string
  api_key?: string
}): Promise<ApiResponse> => {
  return api.post('/web-test/ai/explore', data) as Promise<ApiResponse>
}

// 导出服务对象
export const webTestService = {
  getScripts,
  createScript,
  getScript,
  updateScript,
  deleteScript,
  getCollections,
  createCollection,
  updateCollection,
  deleteCollection,
  runCollection,
  runScript,
  startRecording,
  stopRecording,
  getRecordingStatus,
  generateScriptAI,
  analyzeErrorAI,
  exploreWebAppAI,
}
