import api, { ApiResponse } from './api'

export interface Project {
  id: number
  name: string
  description?: string
  is_pinned?: boolean
  pinned_at?: string | null
  created_at: string
  updated_at: string
}

export const getProjects = (params?: { page?: number; per_page?: number; keyword?: string }): Promise<ApiResponse> => {
  return api.get('/projects', { params: { per_page: 100, ...params } }) as Promise<ApiResponse>
}

export const getProject = (id: number): Promise<ApiResponse> => {
  return api.get(`/projects/${id}`) as Promise<ApiResponse>
}

export const createProject = (data: {
  name: string
  description?: string
}): Promise<ApiResponse> => {
  return api.post('/projects', data) as Promise<ApiResponse>
}

export const updateProject = (id: number, data: {
  name?: string
  description?: string
}): Promise<ApiResponse> => {
  return api.put(`/projects/${id}`, data) as Promise<ApiResponse>
}

export const deleteProject = (id: number): Promise<ApiResponse> => {
  return api.delete(`/projects/${id}`) as Promise<ApiResponse>
}

/** 置顶/取消置顶项目 */
export const togglePinProject = (id: number): Promise<ApiResponse> => {
  return api.put(`/projects/${id}/pin`) as Promise<ApiResponse>
}

export const projectService = {
  getProjects,
  getProject,
  createProject,
  updateProject,
  deleteProject,
  togglePinProject,
}
