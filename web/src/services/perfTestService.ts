import api, { ApiResponse } from './api'

// ==================== 场景管理 ====================

export const getScenarios = (projectId?: number): Promise<ApiResponse> => {
  return api.get('/perf-test/scenarios', { params: { project_id: projectId } }) as Promise<ApiResponse>
}

export const createScenario = (data: {
  name: string
  description?: string
  target_url?: string
  method?: string
  headers?: Record<string, any>
  body?: any
  user_count?: number
  spawn_rate?: number
  duration?: number
  project_id?: number
}): Promise<ApiResponse> => {
  return api.post('/perf-test/scenarios', data) as Promise<ApiResponse>
}

export const getScenario = (id: number): Promise<ApiResponse> => {
  return api.get(`/perf-test/scenarios/${id}`) as Promise<ApiResponse>
}

export const updateScenario = (id: number, data: {
  name?: string
  description?: string
  target_url?: string
  method?: string
  headers?: Record<string, any>
  body?: any
  user_count?: number
  spawn_rate?: number
  duration?: number
}): Promise<ApiResponse> => {
  return api.put(`/perf-test/scenarios/${id}`, data) as Promise<ApiResponse>
}

export const deleteScenario = (id: number): Promise<ApiResponse> => {
  return api.delete(`/perf-test/scenarios/${id}`) as Promise<ApiResponse>
}

// ==================== 执行测试 ====================

export const runScenario = (scenarioId: number): Promise<ApiResponse> => {
  return api.post(`/perf-test/scenarios/${scenarioId}/run`) as Promise<ApiResponse>
}

export const stopScenario = (scenarioId: number): Promise<ApiResponse> => {
  return api.post(`/perf-test/scenarios/${scenarioId}/stop`) as Promise<ApiResponse>
}

export const getScenarioStatus = (scenarioId: number): Promise<ApiResponse> => {
  return api.get(`/perf-test/scenarios/${scenarioId}/status`) as Promise<ApiResponse>
}

export const getRunningTests = (): Promise<ApiResponse> => {
  return api.get('/perf-test/running') as Promise<ApiResponse>
}

// 导出服务对象
export const perfTestService = {
  getScenarios,
  createScenario,
  getScenario,
  updateScenario,
  deleteScenario,
  runScenario,
  stopScenario,
  getScenarioStatus,
  getRunningTests,
}
