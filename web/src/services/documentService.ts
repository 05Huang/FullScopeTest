import api, { ApiResponse } from './api'

// ==================== 类型定义 ====================

export interface TestDocument {
  id: number
  project_id: number
  title: string
  content?: string
  category: string
  version: string
  created_by: number
  updated_by?: number
  author_name?: string
  tags: string[]
  is_published: boolean
  created_at: string
  updated_at: string
}

export interface DocumentCategory {
  value: string
  label: string
  icon: string
}

export interface DocumentTemplate {
  id: string
  name: string
  category: string
  content: string
}

export interface DocumentListParams {
  category?: string
  keyword?: string
  page?: number
  per_page?: number
}

// ==================== 文档管理 ====================

// 获取文档列表
export const getDocuments = (projectId: number, params?: DocumentListParams): Promise<ApiResponse> => {
  return api.get(`/projects/${projectId}/docs`, { params }) as Promise<ApiResponse>
}

// 创建文档
export const createDocument = (projectId: number, data: {
  title: string
  content?: string
  category?: string
  tags?: string[]
}): Promise<ApiResponse> => {
  return api.post(`/projects/${projectId}/docs`, data) as Promise<ApiResponse>
}

// 获取文档详情
export const getDocument = (docId: number): Promise<ApiResponse<TestDocument>> => {
  return api.get(`/docs/${docId}`) as Promise<ApiResponse<TestDocument>>
}

// 更新文档
export const updateDocument = (docId: number, data: {
  title?: string
  content?: string
  category?: string
  tags?: string[]
  is_published?: boolean
  version?: string
}): Promise<ApiResponse> => {
  return api.put(`/docs/${docId}`, data) as Promise<ApiResponse>
}

// 删除文档
export const deleteDocument = (docId: number): Promise<ApiResponse> => {
  return api.delete(`/docs/${docId}`) as Promise<ApiResponse>
}

// ==================== 分类与模板 ====================

// 获取文档分类
export const getCategories = (): Promise<ApiResponse<DocumentCategory[]>> => {
  return api.get('/docs/categories') as Promise<ApiResponse<DocumentCategory[]>>
}

// ????????
export const getTemplates = (): Promise<ApiResponse<DocumentTemplate[]>> => {
  return api.get('/docs/templates') as Promise<ApiResponse<DocumentTemplate[]>>
}




// ==================== 导出 ====================

// 获取文档导出 URL
export const getDocExportUrl = (docId: number, format: 'md' | 'html' = 'md'): string => {
  return `/api/v1/docs/${docId}/export?format=${format}`
}

// 导出服务对象
export const documentService = {
  getDocuments,
  createDocument,
  getDocument,
  updateDocument,
  deleteDocument,
  getCategories,
  getTemplates,
  getDocExportUrl,
}

export default documentService
