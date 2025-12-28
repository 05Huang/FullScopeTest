import axios, { AxiosError, InternalAxiosRequestConfig } from 'axios'
import { useAuthStore } from '@/stores/authStore'

// API 响应类型定义
export interface ApiResponse<T = any> {
  code: number
  data: T
  message: string
  timestamp: string
  errors?: any
}

// 创建 axios 实例
const api = axios.create({
  baseURL: '/api/v1',
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
})

// 请求拦截器
api.interceptors.request.use(
  (config: InternalAxiosRequestConfig) => {
    const token = useAuthStore.getState().token
    if (token && config.headers) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// 响应拦截器 - 返回类型为 ApiResponse
api.interceptors.response.use(
  (response) => {
    // 如果响应类型是 text 或 blob，直接返回整个 response 对象
    // 让调用方自行处理
    if (response.config.responseType === 'text' || response.config.responseType === 'blob') {
      return response
    }
    // JSON 响应，返回 data 部分
    return response.data
  },
  async (error: AxiosError) => {
    const originalRequest = error.config

    // 401 错误，尝试刷新 token
    if (error.response?.status === 401 && originalRequest) {
      const refreshToken = useAuthStore.getState().refreshToken

      if (refreshToken) {
        try {
          const response = await axios.post('/api/v1/auth/refresh', null, {
            headers: { Authorization: `Bearer ${refreshToken}` },
          })

          const { access_token } = response.data.data
          useAuthStore.getState().setAuth(
            access_token,
            refreshToken,
            useAuthStore.getState().user!
          )

          // 重试原请求
          if (originalRequest.headers) {
            originalRequest.headers.Authorization = `Bearer ${access_token}`
          }
          return api(originalRequest)
        } catch {
          // 刷新失败，登出
          useAuthStore.getState().logout()
          window.location.href = '/login'
        }
      } else {
        useAuthStore.getState().logout()
        window.location.href = '/login'
      }
    }

    return Promise.reject(error)
  }
)

export default api
