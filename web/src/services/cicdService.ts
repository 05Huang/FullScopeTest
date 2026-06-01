import api, { ApiResponse } from './api'

export interface WebhookToken {
  id: number
  project_id: number
  name: string
  token: string
  target_type: string
  target_id: number
  created_at: string
  updated_at: string
}

export interface ScheduledTask {
  id: number
  project_id: number
  name: string
  cron_expression: string
  target_type: string
  target_id: number
  is_active: boolean
  notify_webhook: string
  notify_events: string
  created_at: string
  updated_at: string
}

export const cicdService = {
  // Webhooks
  getWebhooks: (projectId: number): Promise<ApiResponse<WebhookToken[]>> => {
    return api.get('/webhooks', { params: { project_id: projectId } }) as Promise<ApiResponse<WebhookToken[]>>
  },

  createWebhook: (data: Partial<WebhookToken>): Promise<ApiResponse<WebhookToken>> => {
    return api.post('/webhooks', data) as Promise<ApiResponse<WebhookToken>>
  },

  deleteWebhook: (id: number): Promise<ApiResponse> => {
    return api.delete(`/webhooks/${id}`) as Promise<ApiResponse>
  },

  // Schedules
  getSchedules: (projectId: number): Promise<ApiResponse<ScheduledTask[]>> => {
    return api.get('/schedules', { params: { project_id: projectId } }) as Promise<ApiResponse<ScheduledTask[]>>
  },

  createSchedule: (data: Partial<ScheduledTask>): Promise<ApiResponse<ScheduledTask>> => {
    return api.post('/schedules', data) as Promise<ApiResponse<ScheduledTask>>
  },

  updateSchedule: (id: number, data: Partial<ScheduledTask>): Promise<ApiResponse<ScheduledTask>> => {
    return api.put(`/schedules/${id}`, data) as Promise<ApiResponse<ScheduledTask>>
  },

  deleteSchedule: (id: number): Promise<ApiResponse> => {
    return api.delete(`/schedules/${id}`) as Promise<ApiResponse>
  }
}