import api, { ApiResponse } from './api'

export interface Project {
  id: number
  name: string
  description?: string
  created_at: string
  updated_at: string
}

export const getProjects = (): Promise<ApiResponse> => {
  return api.get('/projects') as Promise<ApiResponse>
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

export const projectService = {
  getProjects,
  getProject,
  createProject,
  updateProject,
  deleteProject,
}
