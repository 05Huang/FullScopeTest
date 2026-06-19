import axios, { AxiosError, InternalAxiosRequestConfig } from 'axios'
import { message } from 'antd'
import { useAuthStore } from '@/stores/authStore'

// API 响应类型定义
export interface ApiResponse<T = any> {
  code: number
  data: T
  message: string
  timestamp: string
  errors?: any
  request_id?: string
}

/**
 * 获取最近一次请求的 Request ID（用于错误日志和 Bug 报告）
 */
let lastRequestId = ''
export const getLastRequestId = () => lastRequestId

// 创建 axios 实例
// withCredentials: true 使浏览器自动携带 httpOnly Cookie
const api = axios.create({
  baseURL: '/api/v1',
  timeout: 30000,
  withCredentials: true,
  headers: {
    'Content-Type': 'application/json',
  },
})

let refreshPromise: Promise<void> | null = null

/**
 * 刷新 Access Token
 * 后端通过 httpOnly Cookie 设置新的 access_token，前端无需处理 token 明文
 */
const refreshAccessToken = () => {
  if (!refreshPromise) {
    refreshPromise = axios
      .post('/api/v1/auth/refresh', null, {
        withCredentials: true,
      })
      .then(() => {
        // 后端已通过 Set-Cookie 更新 access_token_cookie
      })
      .finally(() => {
        refreshPromise = null
      })
  }

  return refreshPromise
}

// 请求拦截器（httpOnly Cookie 由浏览器自动携带，无需手动添加 Authorization header）
api.interceptors.request.use(
  (config: InternalAxiosRequestConfig) => {
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// 响应拦截器 - 返回类型为 ApiResponse
api.interceptors.response.use(
  (response) => {
    // 捕获后端返回的 X-Request-ID（用于错误排查）
    const requestId = response.headers['x-request-id']
    if (requestId) {
      lastRequestId = requestId
    }
    // 如果响应类型是 text 或 blob，直接返回整个 response 对象
    // 让调用方自行处理
    if (response.config.responseType === 'text' || response.config.responseType === 'blob') {
      return response
    }
    // JSON 响应，返回 data 部分
    return response.data
  },
  async (error: AxiosError) => {
    // 捕获错误响应中的 X-Request-ID
    const errorRequestId = error.response?.headers?.['x-request-id']
    if (errorRequestId) {
      lastRequestId = errorRequestId
    }

    // 网络错误检测（断网或服务器无响应）
    if (!error.response && error.code === 'ERR_NETWORK') {
      message.error({
        content: '网络连接已断开，请检查网络后重试',
        duration: 5,
        key: 'network-error',
      })
    }

    // 500 错误提示
    if (error.response?.status === 500) {
      const rid = errorRequestId || lastRequestId
      message.error({
        content: `服务器错误${rid ? ` (ID: ${rid})` : ''}，请稍后重试`,
        duration: 5,
        key: 'server-error',
      })
    }

    const originalRequest = error.config as (InternalAxiosRequestConfig & { _retry?: boolean }) | undefined

    // 401 错误，尝试刷新 token（通过 httpOnly Cookie）
    if (error.response?.status === 401 && originalRequest && !originalRequest._retry) {
      // 如果刷新接口本身返回 401，说明 refresh token 也已失效
      if (originalRequest.url?.includes('/auth/refresh')) {
        useAuthStore.getState().logout()
        window.location.href = '/login'
        return Promise.reject(error)
      }

      originalRequest._retry = true
      try {
        await refreshAccessToken()
        // 刷新成功，重试原请求（新的 access_token_cookie 已由浏览器自动携带）
        return api(originalRequest)
      } catch (refreshError) {
        // 刷新失败，登出并明确拒绝原请求
        useAuthStore.getState().logout()
        window.location.href = '/login'
        return Promise.reject(refreshError)
      }
    }

    return Promise.reject(error)
  }
)

export default api
