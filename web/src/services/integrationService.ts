/**
 * 集成管理服务层
 *
 * 对接后端 GitHub 集成 API：授权、状态查询、解绑、配置。
 */
import api, { ApiResponse } from './api'

export interface GitHubIntegration {
  id: number
  github_username: string
  github_avatar?: string
  repo_full_name?: string
  is_active: boolean
  check_run_enabled?: boolean
  created_at: string
}

export interface GitHubStatus {
  connected: boolean
  integration: GitHubIntegration | null
}

export interface GitHubConfig {
  client_id?: string
  configured: boolean
}

/** 获取 GitHub 绑定状态 */
export const getGitHubStatus = (): Promise<ApiResponse<GitHubStatus>> => {
  return api.get('/integrations/github/status') as Promise<ApiResponse<GitHubStatus>>
}

/** 获取 GitHub OAuth 授权 URL */
export const getGitHubAuthUrl = (): Promise<ApiResponse<{ authorize_url: string; state: string }>> => {
  return api.get('/integrations/github/auth') as Promise<ApiResponse<any>>
}

/** 获取 GitHub 配置 */
export const getGitHubConfig = (): Promise<ApiResponse<GitHubConfig>> => {
  return api.get('/integrations/github/config') as Promise<ApiResponse<GitHubConfig>>
}

/** 解绑 GitHub */
export const unbindGitHub = (): Promise<ApiResponse> => {
  return api.post('/integrations/github/unbind') as Promise<ApiResponse>
}

export const integrationService = {
  getGitHubStatus,
  getGitHubAuthUrl,
  getGitHubConfig,
  unbindGitHub,
}

export default integrationService
