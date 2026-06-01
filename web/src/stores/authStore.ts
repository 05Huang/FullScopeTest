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
  token: string | null
  refreshToken: string | null
  user: User | null
  isAuthenticated: boolean

  // Actions
  setAuth: (token: string, refreshToken: string, user: User) => void
  logout: () => void
  updateUser: (user: Partial<User>) => void
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      token: null,
      refreshToken: null,
      user: null,
      isAuthenticated: false,

      setAuth: (token, refreshToken, user) => {
        set({
          token,
          refreshToken,
          user,
          isAuthenticated: true,
        })
      },

      logout: () => {
        // 通知后端注销 Token（异步，不阻塞本地清理）
        // 使用独立 axios 实例避免与 api.ts 的循环依赖
        const token = useAuthStore.getState().token
        if (token) {
          axios.post('/api/v1/auth/logout', null, {
            headers: { Authorization: `Bearer ${token}` },
          }).catch(() => {})
        }
        set({
          token: null,
          refreshToken: null,
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
    }
  )
)
