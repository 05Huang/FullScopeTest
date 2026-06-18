import api, { ApiResponse } from './api'

export interface LoginParams {
  username: string
  password: string
}

export interface RegisterParams {
  username: string
  email: string
  password: string
}

export interface AuthData {
  user?: {
    id: number
    username: string
    email: string
    avatar?: string
  }
}

// 用户登录
export const login = (username: string, password: string): Promise<ApiResponse<AuthData>> => {
  return api.post('/auth/login', { username, password }) as Promise<ApiResponse<AuthData>>
}

// 用户注册
export const register = (username: string, email: string, password: string, invite_code?: string): Promise<ApiResponse> => {
  return api.post('/auth/register', { username, email, password, invite_code: invite_code || undefined }) as Promise<ApiResponse>
}

// 获取当前用户信息
export const getCurrentUser = (): Promise<ApiResponse> => {
  return api.get('/auth/me') as Promise<ApiResponse>
}

// 修改个人信息
export const updateProfile = (data: { username?: string; email?: string; avatar?: string }): Promise<ApiResponse> => {
  return api.put('/auth/me', data) as Promise<ApiResponse>
}

// 上传个人头像
export const uploadAvatar = (file: File): Promise<ApiResponse<{ avatar: string }>> => {
  const formData = new FormData()
  formData.append('file', file)
  return api.post('/auth/me/avatar', formData, {
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  }) as Promise<ApiResponse<{ avatar: string }>>
}

// 修改密码
export const changePassword = (oldPassword: string, newPassword: string): Promise<ApiResponse> => {
  return api.put('/auth/password', { old_password: oldPassword, new_password: newPassword }) as Promise<ApiResponse>
}

// 忘记密码 - 发送重置链接（安全规范：不再返回 reset_token）
export const forgotPassword = (email: string): Promise<ApiResponse<null>> => {
  return api.post('/auth/forgot-password', { email }) as Promise<ApiResponse<null>>
}

// 重置密码
export const resetPassword = (token: string, newPassword: string): Promise<ApiResponse> => {
  return api.post('/auth/reset-password', { token, new_password: newPassword }) as Promise<ApiResponse>
}

// 导出服务对象
export const authService = {
  login,
  register,
  getCurrentUser,
  updateProfile,
  uploadAvatar,
  changePassword,
  forgotPassword,
  resetPassword,
}
