/**
 * 项目相关类型定义
 */

export interface Project {
  id: number
  name: string
  description?: string
  user_id: number
  settings: Record<string, unknown>
  created_at: string
  updated_at: string
}

export interface ProjectCreateParams {
  name: string
  description?: string
  settings?: Record<string, unknown>
}

export interface ProjectUpdateParams {
  name?: string
  description?: string
  settings?: Record<string, unknown>
}
