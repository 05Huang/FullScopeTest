/**
 * 角色权限 Hook
 * 基于用户 role 判断权限，用于控制菜单显示和路由守卫
 */
import { useMemo } from 'react'
import { useAuthStore } from '@/stores/authStore'

export type UserRole = 'admin' | 'member' | 'viewer'

const ROLE_HIERARCHY: Record<UserRole, number> = {
  admin: 3,
  member: 2,
  viewer: 1,
}

export function useRole() {
  const { user } = useAuthStore()
  const role = (user?.role || 'viewer') as UserRole

  const isAdmin = role === 'admin'
  const isMember = role === 'member' || role === 'admin'
  const isViewer = true

  /** 检查当前用户角色是否 >= 指定角色 */
  const hasRole = useMemo(() => {
    return (required: UserRole) => {
      return (ROLE_HIERARCHY[role] || 0) >= (ROLE_HIERARCHY[required] || 0)
    }
  }, [role])

  /** 检查是否有指定权限 */
  const hasPermission = useMemo(() => {
    return (resource: string, action: string) => {
      if (isAdmin) return true
      if (role === 'viewer') return action === 'read'
      if (role === 'member') return action !== 'delete' && action !== 'manage'
      return false
    }
  }, [role, isAdmin])

  return { role, isAdmin, isMember, isViewer, hasRole, hasPermission }
}
