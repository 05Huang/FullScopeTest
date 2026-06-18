import { describe, it, expect, beforeEach, vi } from 'vitest'
import { renderHook } from '@testing-library/react'
import { useRole } from '../useRole'
import { useAuthStore } from '@/stores/authStore'

describe('useRole', () => {
  beforeEach(() => {
    useAuthStore.setState({ user: null, isAuthenticated: false })
  })

  it('should default to viewer when no user', () => {
    const { result } = renderHook(() => useRole())
    expect(result.current.role).toBe('viewer')
    expect(result.current.isAdmin).toBe(false)
    expect(result.current.isMember).toBe(false)
    expect(result.current.isViewer).toBe(true)
  })

  it('should detect admin role', () => {
    useAuthStore.getState().setAuth({ id: 1, username: 'admin', role: 'admin' } as any)
    const { result } = renderHook(() => useRole())
    expect(result.current.role).toBe('admin')
    expect(result.current.isAdmin).toBe(true)
    expect(result.current.isMember).toBe(true)
  })

  it('should detect member role', () => {
    useAuthStore.getState().setAuth({ id: 2, username: 'member', role: 'member' } as any)
    const { result } = renderHook(() => useRole())
    expect(result.current.role).toBe('member')
    expect(result.current.isAdmin).toBe(false)
    expect(result.current.isMember).toBe(true)
  })

  it('should check role hierarchy with hasRole', () => {
    useAuthStore.getState().setAuth({ id: 2, username: 'member', role: 'member' } as any)
    const { result } = renderHook(() => useRole())
    expect(result.current.hasRole('viewer')).toBe(true)
    expect(result.current.hasRole('member')).toBe(true)
    expect(result.current.hasRole('admin')).toBe(false)
  })

  it('should check permissions for viewer', () => {
    useAuthStore.getState().setAuth({ id: 3, username: 'viewer', role: 'viewer' } as any)
    const { result } = renderHook(() => useRole())
    expect(result.current.hasPermission('project', 'read')).toBe(true)
    expect(result.current.hasPermission('project', 'write')).toBe(false)
    expect(result.current.hasPermission('project', 'delete')).toBe(false)
  })

  it('should grant all permissions to admin', () => {
    useAuthStore.getState().setAuth({ id: 1, username: 'admin', role: 'admin' } as any)
    const { result } = renderHook(() => useRole())
    expect(result.current.hasPermission('project', 'read')).toBe(true)
    expect(result.current.hasPermission('project', 'write')).toBe(true)
    expect(result.current.hasPermission('project', 'delete')).toBe(true)
    expect(result.current.hasPermission('project', 'manage')).toBe(true)
  })
})
