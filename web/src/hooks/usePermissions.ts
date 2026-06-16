/**
 * RBAC 权限 Hook
 *
 * 提供当前用户在指定组织中的权限检查能力。
 * 通过 /api/v1/organizations/:id/my-permissions 端点获取权限数据。
 *
 * 用法：
 *   const { permissions, role, hasPermission, loading } = usePermissions(orgId)
 *   if (hasPermission('project', 'create')) { ... }
 */
import { useState, useEffect, useCallback } from 'react'
import api from '@/services/api'

interface PermissionMap {
  [resource: string]: string[]
}

interface UsePermissionsResult {
  /** 完整权限映射 { resource: [actions] } */
  permissions: PermissionMap
  /** 当前用户角色名 */
  role: string | null
  /** 是否正在加载 */
  loading: boolean
  /** 错误信息 */
  error: string | null
  /**
   * 检查是否拥有指定权限
   * @param resource 资源类型（project/test_case/test_run/environment/report/ai_feature）
   * @param action 操作类型（create/read/update/delete/execute/manage）
   */
  hasPermission: (resource: string, action: string) => boolean
  /** 刷新权限数据 */
  refresh: () => void
}

export function usePermissions(orgId: number | null): UsePermissionsResult {
  const [permissions, setPermissions] = useState<PermissionMap>({})
  const [role, setRole] = useState<string | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const fetchPermissions = useCallback(async () => {
    if (!orgId) {
      setPermissions({})
      setRole(null)
      return
    }

    setLoading(true)
    setError(null)

    try {
      const res = await api.get(`/organizations/${orgId}/my-permissions`)
      const data = res.data?.data
      if (data) {
        setPermissions(data.permissions || {})
        setRole(data.role || null)
      }
    } catch (err: any) {
      // 403 表示不属于该组织，不视为异常
      if (err?.response?.status === 403) {
        setPermissions({})
        setRole(null)
      } else {
        setError(err?.message || '获取权限失败')
      }
    } finally {
      setLoading(false)
    }
  }, [orgId])

  useEffect(() => {
    fetchPermissions()
  }, [fetchPermissions])

  const hasPermission = useCallback(
    (resource: string, action: string): boolean => {
      const actions = permissions[resource]
      return Array.isArray(actions) && actions.includes(action)
    },
    [permissions],
  )

  return {
    permissions,
    role,
    loading,
    error,
    hasPermission,
    refresh: fetchPermissions,
  }
}
