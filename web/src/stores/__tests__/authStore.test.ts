import { describe, it, expect, beforeEach } from 'vitest'
import { useAuthStore } from '../authStore'

describe('authStore', () => {
  beforeEach(() => {
    // 每个测试前重置 store
    useAuthStore.setState({
      token: null,
      refreshToken: null,
      user: null,
      isAuthenticated: false,
    })
    localStorage.clear()
  })

  describe('setAuth', () => {
    it('should set token, refreshToken and user', () => {
      const mockUser = {
        id: 1,
        username: 'testuser',
        email: 'test@example.com',
      }

      useAuthStore.getState().setAuth(
        'access-token-123',
        'refresh-token-456',
        mockUser
      )

      const state = useAuthStore.getState()
      expect(state.token).toBe('access-token-123')
      expect(state.refreshToken).toBe('refresh-token-456')
      expect(state.user).toEqual(mockUser)
      expect(state.isAuthenticated).toBe(true)
    })

    it('should persist to localStorage', () => {
      const mockUser = {
        id: 1,
        username: 'testuser',
        email: 'test@example.com',
      }

      useAuthStore.getState().setAuth(
        'access-token-123',
        'refresh-token-456',
        mockUser
      )

      const stored = localStorage.getItem('fullscopetest-auth')
      expect(stored).toBeTruthy()

      const parsed = JSON.parse(stored!)
      expect(parsed.state.token).toBe('access-token-123')
      expect(parsed.state.user.username).toBe('testuser')
    })
  })

  describe('logout', () => {
    it('should clear token and user on logout', () => {
      const mockUser = {
        id: 1,
        username: 'testuser',
        email: 'test@example.com',
      }

      useAuthStore.getState().setAuth(
        'access-token-123',
        'refresh-token-456',
        mockUser
      )

      useAuthStore.getState().logout()

      const state = useAuthStore.getState()
      expect(state.token).toBeNull()
      expect(state.refreshToken).toBeNull()
      expect(state.user).toBeNull()
      expect(state.isAuthenticated).toBe(false)
    })
  })

  describe('updateUser', () => {
    it('should update user fields', () => {
      const mockUser = {
        id: 1,
        username: 'testuser',
        email: 'test@example.com',
      }

      useAuthStore.getState().setAuth(
        'access-token-123',
        'refresh-token-456',
        mockUser
      )

      useAuthStore.getState().updateUser({ username: 'newname' })

      expect(useAuthStore.getState().user?.username).toBe('newname')
      expect(useAuthStore.getState().user?.email).toBe('test@example.com')
    })

    it('should not update if no user', () => {
      useAuthStore.getState().updateUser({ username: 'newname' })
      expect(useAuthStore.getState().user).toBeNull()
    })
  })

  describe('isAuthenticated', () => {
    it('should be false initially', () => {
      expect(useAuthStore.getState().isAuthenticated).toBe(false)
    })

    it('should be true after setAuth', () => {
      useAuthStore.getState().setAuth(
        'token',
        'refresh',
        { id: 1, username: 'test', email: 'test@example.com' }
      )
      expect(useAuthStore.getState().isAuthenticated).toBe(true)
    })

    it('should be false after logout', () => {
      useAuthStore.getState().setAuth(
        'token',
        'refresh',
        { id: 1, username: 'test', email: 'test@example.com' }
      )
      useAuthStore.getState().logout()
      expect(useAuthStore.getState().isAuthenticated).toBe(false)
    })
  })
})
