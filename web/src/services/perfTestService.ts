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
  step_load_enabled?: boolean
  step_users?: number
  step_duration?: number
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
  step_load_enabled?: boolean
  step_users?: number
  step_duration?: number
}): Promise<ApiResponse> => {
  return api.put(`/perf-test/scenarios/${id}`, data) as Promise<ApiResponse>
}

export const deleteScenario = (id: number): Promise<ApiResponse> => {
  return api.delete(`/perf-test/scenarios/${id}`) as Promise<ApiResponse>
}

// ==================== 执行测试 ====================

export const runScenario = (scenarioId: number, data?: {
  user_count?: number
  spawn_rate?: number
  duration?: number
  step_load_enabled?: boolean
  step_users?: number
  step_duration?: number
}): Promise<ApiResponse> => {
  return api.post(`/perf-test/scenarios/${scenarioId}/run`, data) as Promise<ApiResponse>
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

// ==================== AI ====================

// ==================== 历史测试结果 ====================

export const getPerformanceResults = (params?: {
  project_id?: number
  scenario_id?: number
  status?: string
  page?: number
  per_page?: number
}): Promise<ApiResponse> => {
  return api.get('/perf-test/results', { params }) as Promise<ApiResponse>
}

export const getPerformanceResultMetrics = (
  resultId: number,
  limit?: number
): Promise<ApiResponse> => {
  const params: Record<string, any> = {}
  if (limit) params.limit = limit
  return api.get(`/perf-test/results/${resultId}/metrics`, { params }) as Promise<ApiResponse>
}

export const comparePerformanceRuns = (runIds: number[]): Promise<ApiResponse> => {
  return api.get('/perf-test/compare', {
    params: { run_ids: runIds.join(',') },
  }) as Promise<ApiResponse>
}

// ==================== 告警规则 ====================

export const getAlertRules = (params?: {
  scenario_id?: number
}): Promise<ApiResponse> => {
  return api.get('/perf-test/alert-rules', { params }) as Promise<ApiResponse>
}

export const getAlertRule = (id: number): Promise<ApiResponse> => {
  return api.get(`/perf-test/alert-rules/${id}`) as Promise<ApiResponse>
}

export const createAlertRule = (data: {
  name: string
  description?: string
  scenario_id?: number
  p95_threshold?: number
  p99_threshold?: number
  error_rate_threshold?: number
  rps_min_threshold?: number
  relative_p95_degradation?: number
  relative_rps_degradation?: number
  relative_error_rate_degradation?: number
  notify_webhook?: string
  notify_email?: string
  enabled?: boolean
}): Promise<ApiResponse> => {
  return api.post('/perf-test/alert-rules', data) as Promise<ApiResponse>
}

export const updateAlertRule = (id: number, data: {
  name?: string
  description?: string
  scenario_id?: number
  p95_threshold?: number
  p99_threshold?: number
  error_rate_threshold?: number
  rps_min_threshold?: number
  relative_p95_degradation?: number
  relative_rps_degradation?: number
  relative_error_rate_degradation?: number
  notify_webhook?: string
  notify_email?: string
  enabled?: boolean
}): Promise<ApiResponse> => {
  return api.put(`/perf-test/alert-rules/${id}`, data) as Promise<ApiResponse>
}

export const deleteAlertRule = (id: number): Promise<ApiResponse> => {
  return api.delete(`/perf-test/alert-rules/${id}`) as Promise<ApiResponse>
}

export const evaluateAlertRule = (id: number, test_result_id: number): Promise<ApiResponse> => {
  return api.post(`/perf-test/alert-rules/${id}/evaluate`, { test_result_id }) as Promise<ApiResponse>
}

export const getAlertLogs = (params?: {
  page?: number
  per_page?: number
  rule_id?: number
  severity?: string
}): Promise<ApiResponse> => {
  return api.get('/perf-test/alert-logs', { params }) as Promise<ApiResponse>
}

// ==================== AI ====================

export const generateScriptAI = (data: {
  prompt: string
}): Promise<ApiResponse> => {
  return api.post('/perf-test/ai/generate', data) as Promise<ApiResponse>
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
  getPerformanceResults,
  getPerformanceResultMetrics,
  comparePerformanceRuns,
  getAlertRules,
  getAlertRule,
  createAlertRule,
  updateAlertRule,
  deleteAlertRule,
  evaluateAlertRule,
  getAlertLogs,
  generateScriptAI,
}
