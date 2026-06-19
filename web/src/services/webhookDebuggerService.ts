/**
 * Webhook 调试器服务层
 *
 * 对接后端 Webhook 调试会话和请求记录 API。
 */
import api, { ApiResponse } from './api'

export interface WebhookSession {
  id: number
  token: string
  webhook_url: string
  is_active: boolean
  request_count: number
  created_at: string
}

export interface WebhookRequest {
  id: number
  method: string
  headers: Record<string, string>
  body: string
  query_params: Record<string, string>
  source_ip: string
  received_at: string
}

export const getSessions = (): Promise<ApiResponse<WebhookSession[]>> => {
  return api.get('/webhook-debugger') as Promise<ApiResponse<WebhookSession[]>>
}

export const createSession = (): Promise<ApiResponse<WebhookSession>> => {
  return api.post('/webhook-debugger') as Promise<ApiResponse<WebhookSession>>
}

export const getRequests = (token: string): Promise<ApiResponse<WebhookRequest[]>> => {
  return api.get('/webhook-debugger/' + token + '/requests') as Promise<ApiResponse<WebhookRequest[]>>
}

export const clearRequests = (token: string): Promise<ApiResponse> => {
  return api.delete('/webhook-debugger/' + token + '/requests') as Promise<ApiResponse>
}

export const webhookDebuggerService = {
  getSessions, createSession, getRequests, clearRequests,
};

export default webhookDebuggerService
