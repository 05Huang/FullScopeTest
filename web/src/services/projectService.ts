import api, { ApiResponse } from './api'

// ==================== 类型定义 ====================

export interface Project {
  id: number
  name: string
  description?: string
  owner_id: number
  settings?: Record<string, any>
  created_at: string
  updated_at: string
}

export interface ProjectListParams {
  page?: number
  per_page?: number
  keyword?: string
}

// ==================== 项目管理 ====================

// 获取项目列表
export const getProjects = (params?: ProjectListParams): Promise<ApiResponse> => {
  return api.get('/projects', { params }) as Promise<ApiResponse>
}

// 创建项目
export const createProject = (data: {
  name: string
  description?: string
}): Promise<ApiResponse> => {
  return api.post('/projects', data) as Promise<ApiResponse>
}

// 获取项目详情
export const getProject = (projectId: number): Promise<ApiResponse<Project>> => {
  return api.get(`/projects/${projectId}`) as Promise<ApiResponse<Project>>
}

// 更新项目
export const updateProject = (projectId: number, data: {
  name?: string
  description?: string
  settings?: Record<string, any>
}): Promise<ApiResponse> => {
  return api.put(`/projects/${projectId}`, data) as Promise<ApiResponse>
}

// 删除项目
export const deleteProject = (projectId: number): Promise<ApiResponse> => {
  return api.delete(`/projects/${projectId}`) as Promise<ApiResponse>
}

// 导出服务对象
export const projectService = {
  getProjects,
  createProject,
  getProject,
  updateProject,
  deleteProject,
}

export default projectService
