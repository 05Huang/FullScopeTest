import { create } from 'zustand'
import { persist } from 'zustand/middleware'
import axios from 'axios'

interface User {
  id: number
  username: string
  email: string
  avatar?: string
}

interface AuthState {
  user: User | null
  isAuthenticated: boolean

  // Actions
  setAuth: (user: User) => void
  logout: () => void
  updateUser: (user: Partial<User>) => void
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      user: null,
      isAuthenticated: false,

      setAuth: (user) => {
        set({
          user,
          isAuthenticated: true,
        })
      },

      logout: () => {
        // 通知后端注销 Token（通过 httpOnly Cookie 认证）
        // 使用独立 axios 实例避免与 api.ts 的循环依赖
        axios.post('/api/v1/auth/logout', null, {
          withCredentials: true,
        }).catch(() => {})
        set({
          user: null,
          isAuthenticated: false,
        })
      },

      updateUser: (userData) => {
        set((state) => ({
          user: state.user ? { ...state.user, ...userData } : null,
        }))
      },
    }),
    {
      name: 'fullscopetest-auth',
      // 仅持久化 user 和 isAuthenticated，不存储 token
      partialize: (state) => ({
        user: state.user,
        isAuthenticated: state.isAuthenticated,
      }),
    }
  )
)
