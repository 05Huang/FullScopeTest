import api, { ApiResponse } from './api'

export type AiOperationType =
  | 'create_environment'
  | 'update_environment'
  | 'create_collection'
  | 'create_case'
  | 'run_collection'
  | 'run_case'

export interface AiPlanOperation {
  type: AiOperationType
  [key: string]: any
}

export interface AiPlanResult {
  summary: string
  source?: 'llm' | 'fallback'
  operations: AiPlanOperation[]
}

// ==================== 用例集合 ====================

export const getCollections = (projectId?: number): Promise<ApiResponse> => {
  return api.get('/api-test/collections', { params: { project_id: projectId } }) as Promise<ApiResponse>
}

export const createCollection = (data: {
  name: string
  description?: string
  project_id?: number
}): Promise<ApiResponse> => {
  return api.post('/api-test/collections', data) as Promise<ApiResponse>
}

export const updateCollection = (id: number, data: {
  name?: string
  description?: string
}): Promise<ApiResponse> => {
  return api.put(`/api-test/collections/${id}`, data) as Promise<ApiResponse>
}

export const deleteCollection = (id: number): Promise<ApiResponse> => {
  return api.delete(`/api-test/collections/${id}`) as Promise<ApiResponse>
}

// ==================== 测试用例 ====================

export const getCases = (params?: {
  collection_id?: number
  project_id?: number
}): Promise<ApiResponse> => {
  return api.get('/api-test/cases', { params }) as Promise<ApiResponse>
}

export const createCase = (data: {
  name: string
  method: string
  url: string
  description?: string
  headers?: Record<string, any>
  params?: Record<string, any>
  body?: any
  body_type?: string
  pre_script?: string
  post_script?: string
  collection_id?: number
  project_id?: number
  environment_id?: number
  mock_enabled?: boolean
  mock_response_code?: number
  mock_response_body?: string
  mock_response_headers?: Record<string, any>
  mock_delay_ms?: number
}): Promise<ApiResponse> => {
  return api.post('/api-test/cases', data) as Promise<ApiResponse>
}

export const getCase = (id: number): Promise<ApiResponse> => {
  return api.get(`/api-test/cases/${id}`) as Promise<ApiResponse>
}

export const updateCase = (id: number, data: {
  name?: string
  method?: string
  url?: string
  description?: string
  headers?: Record<string, any>
  params?: Record<string, any>
  body?: any
  body_type?: string
  pre_script?: string
  post_script?: string
  collection_id?: number | null
  environment_id?: number | null
  mock_enabled?: boolean
  mock_response_code?: number
  mock_response_body?: string
  mock_response_headers?: Record<string, any>
  mock_delay_ms?: number
}): Promise<ApiResponse> => {
  return api.put(`/api-test/cases/${id}`, data) as Promise<ApiResponse>
}

export const deleteCase = (id: number): Promise<ApiResponse> => {
  return api.delete(`/api-test/cases/${id}`) as Promise<ApiResponse>
}

// ==================== 执行测试 ====================

export const executeRequest = (data: {
  method: string
  url: string
  headers?: any
  params?: any
  body?: any
  body_type?: string
  timeout?: number
  env_id?: number
  pre_script?: string
  post_script?: string
  case_id?: number
  mock_enabled?: boolean
  mock_response_code?: number
  mock_response_body?: string
  mock_response_headers?: Record<string, any>
  mock_delay_ms?: number
}): Promise<ApiResponse> => {
  return api.post('/api-test/execute', data) as Promise<ApiResponse>
}

export const runCase = (caseId: number, envId?: number): Promise<ApiResponse> => {
  return api.post(`/api-test/cases/${caseId}/run`, null, {
    params: { env_id: envId }
  }) as Promise<ApiResponse>
}

export const runCollection = (collectionId: number, data?: { env_id?: number }): Promise<ApiResponse> => {
  return api.post(`/api-test/collections/${collectionId}/run`, data || {}) as Promise<ApiResponse>
}

// ==================== AI Assistant ====================

export const generateAiPlan = (data: {
  prompt: string
  base_url?: string
  model?: string
  api_key?: string
  project_id?: number
  collection_id?: number
  case_id?: number
  environment_id?: number
}): Promise<ApiResponse<AiPlanResult>> => {
  return api.post('/api-test/ai/plan', data) as Promise<ApiResponse<AiPlanResult>>
}

export const synthesizeCasesAI = (data: {
  base_request: any
  count?: number
  base_url?: string
  model?: string
  api_key?: string
}): Promise<ApiResponse<{ cases: any[] }>> => {
  return api.post('/api-test/ai/synthesize-cases', data) as Promise<ApiResponse<{ cases: any[] }>>
}

export const reviewCollectionAI = (data: {
  collection_id: number
  base_url?: string
  model?: string
  api_key?: string
}): Promise<ApiResponse<{ review_summary: string, suggested_cases: any[] }>> => {
  return api.post('/api-test/ai/review-collection', data) as Promise<ApiResponse<{ review_summary: string, suggested_cases: any[] }>>
}

// 导出服务对象
export const apiTestService = {
  getCollections,
  createCollection,
  updateCollection,
  deleteCollection,
  getCases,
  createCase,
  getCase,
  updateCase,
  deleteCase,
  executeRequest,
  runCase,
  runCollection,
  generateAiPlan,
  synthesizeCasesAI,
  reviewCollectionAI,
}
