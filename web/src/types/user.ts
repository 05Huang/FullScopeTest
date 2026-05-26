/**
 * 用户相关类型定义
 */

export interface User {
  id: number
  username: string
  email: string
  avatar?: string
  is_active: boolean
  created_at: string
  updated_at: string
}

export interface LoginParams {
  username: string
  password: string
}

export interface RegisterParams {
  username: string
  email: string
  password: string
}

export interface AuthResponse {
  access_token: string
  refresh_token: string
  user: User
}

export interface UpdateProfileParams {
  email?: string
  avatar?: string
}

export interface ChangePasswordParams {
  old_password: string
  new_password: string
}
