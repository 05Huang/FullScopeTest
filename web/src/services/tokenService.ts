/**
 * API Token 管理服务层
 *
 * 对接后端 Token 创建/删除/验证 API。
 */
import api, { ApiResponse } from './api'

// ── 类型定义 ────────────────────────────────────────────────────────────────

export interface ApiToken {
  id: number
  name: string
  actions: string[]
  project_ids: number[]
  permissions: string[]
  expires_at: string | null
  created_at?: string
  last_used_at?: string
}

export interface CreateTokenRequest {
  name: string
  actions?: string[]
  project_ids?: number[]
  expires_in_days?: number | null
}

export interface CreateTokenResponse {
  id: number
  token: string  // 仅在创建时返回明文
  name: string
  actions: string[]
  project_ids: number[]
  permissions: string[]
  expires_at: string | null
}

// ── API 调用 ───────────────────────────────────────────────────────────────

/** 获取当前用户的 Token 列表 */
export const getTokens = (params?: {
  page?: number
  per_page?: number
}): Promise<ApiResponse<{ items: ApiToken[]; pagination: { total: number; page: number; per_page: number; pages: number } }>> => {
  return api.get('/tokens', { params }) as Promise<ApiResponse<any>>
}

/** 创建新 Token */
export const createToken = (
  data: CreateTokenRequest
): Promise<ApiResponse<CreateTokenResponse>> => {
  return api.post('/tokens', data) as Promise<ApiResponse<CreateTokenResponse>>
}

/** 删除 Token */
export const deleteToken = (tokenId: number): Promise<ApiResponse> => {
  return api.delete(`/tokens/${tokenId}`) as Promise<ApiResponse>
}

/** 验证 Token */
export const validateToken = (data: {
  action: string
  project_id?: number
}): Promise<ApiResponse<{ has_permission: boolean; token_name: string }>> => {
  return api.post('/tokens/validate', data) as Promise<ApiResponse<any>>
}

// ── 统一导出 ──────────────────────────────────────────────────────────────

export const tokenService = {
  getTokens,
  createToken,
  deleteToken,
  validateToken,
}

export default tokenService
