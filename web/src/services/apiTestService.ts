import api, { ApiResponse } from './api'

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
  headers?: Record<string, any>
  params?: Record<string, any>
  body?: any
  body_type?: string
  pre_script?: string
  test_script?: string
  collection_id?: number
  project_id?: number
}): Promise<ApiResponse> => {
  return api.post('/api-test/cases', data) as Promise<ApiResponse>
}

export const getCase = (id: number): Promise<ApiResponse> => {
  return api.get(`/api-test/cases/${id}`) as Promise<ApiResponse>
}

export const updateCase = (id: number, data: any): Promise<ApiResponse> => {
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
}): Promise<ApiResponse> => {
  return api.post('/api-test/execute', data) as Promise<ApiResponse>
}

export const runCase = (caseId: number, envId?: number): Promise<ApiResponse> => {
  return api.post(`/api-test/cases/${caseId}/run`, null, {
    params: { env_id: envId }
  }) as Promise<ApiResponse>
}

export const runCollection = (collectionId: number): Promise<ApiResponse> => {
  return api.post(`/api-test/collections/${collectionId}/run`) as Promise<ApiResponse>
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
}
