import { describe, it, expect, beforeEach, vi } from 'vitest'
import { useAuthStore } from '../authStore'

// Mock axios 以避免 logout 中的网络请求
vi.mock('axios', () => ({
  default: {
    post: vi.fn().mockResolvedValue({}),
  },
}))

describe('authStore', () => {
  const mockUser = {
    id: 1,
    username: 'testuser',
    email: 'test@example.com',
  }

  beforeEach(() => {
    // 每个测试前重置 store
    useAuthStore.setState({
      user: null,
      isAuthenticated: false,
    })
    localStorage.clear()
  })

  describe('setAuth', () => {
    it('should set user and isAuthenticated', () => {
      useAuthStore.getState().setAuth(mockUser)

      const state = useAuthStore.getState()
      expect(state.user).toEqual(mockUser)
      expect(state.isAuthenticated).toBe(true)
    })

    it('should persist to localStorage', () => {
      useAuthStore.getState().setAuth(mockUser)

      const stored = localStorage.getItem('fullscopetest-auth')
      expect(stored).toBeTruthy()

      const parsed = JSON.parse(stored!)
      // Token 不应存储在 localStorage 中
      expect(parsed.state.token).toBeUndefined()
      expect(parsed.state.user.username).toBe('testuser')
    })
  })

  describe('logout', () => {
    it('should clear user on logout', () => {
      useAuthStore.getState().setAuth(mockUser)

      useAuthStore.getState().logout()

      const state = useAuthStore.getState()
      expect(state.user).toBeNull()
      expect(state.isAuthenticated).toBe(false)
    })
  })

  describe('updateUser', () => {
    it('should update user fields', () => {
      useAuthStore.getState().setAuth(mockUser)

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
      useAuthStore.getState().setAuth(mockUser)
      expect(useAuthStore.getState().isAuthenticated).toBe(true)
    })

    it('should be false after logout', () => {
      useAuthStore.getState().setAuth(mockUser)
      useAuthStore.getState().logout()
      expect(useAuthStore.getState().isAuthenticated).toBe(false)
    })
  })
})
