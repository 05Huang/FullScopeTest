/**
 * 管理员 API 服务
 */
import api from './api'

export interface AdminUser {
  id: number
  username: string
  email: string
  role: string
  is_active: boolean
  avatar?: string
  created_at: string
  last_login?: string
  sso_provider?: string
}

export interface UserListResponse {
  items: AdminUser[]
  total: number
  page: number
  per_page: number
  pages: number
}

export const adminService = {
  /** 获取用户列表 */
  getUsers(params: { page?: number; per_page?: number; search?: string; role?: string } = {}) {
    return api.get('/admin/users', { params }) as Promise<any>
  },

  /** 获取单个用户 */
  getUser(userId: number) {
    return api.get(`/admin/users/${userId}`) as Promise<any>
  },

  /** 修改用户角色 */
  updateUserRole(userId: number, role: string) {
    return api.patch(`/admin/users/${userId}/role`, { role }) as Promise<any>
  },

  /** 启用/禁用用户 */
  updateUserStatus(userId: number, isActive: boolean) {
    return api.patch(`/admin/users/${userId}/status`, { is_active: isActive }) as Promise<any>
  },

  /** 重置用户密码 */
  resetPassword(userId: number, password: string) {
    return api.post(`/admin/users/${userId}/reset-password`, { password }) as Promise<any>
  },
}
