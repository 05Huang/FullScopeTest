import api from './api'

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
  getWebhooks: (projectId: number) => {
    return api.get<any, WebhookToken[]>('/webhooks', { params: { project_id: projectId } })
  },
  
  createWebhook: (data: Partial<WebhookToken>) => {
    return api.post<any, WebhookToken>('/webhooks', data)
  },
  
  deleteWebhook: (id: number) => {
    return api.delete(`/webhooks/${id}`)
  },
  
  // Schedules
  getSchedules: (projectId: number) => {
    return api.get<any, ScheduledTask[]>('/schedules', { params: { project_id: projectId } })
  },
  
  createSchedule: (data: Partial<ScheduledTask>) => {
    return api.post<any, ScheduledTask>('/schedules', data)
  },
  
  updateSchedule: (id: number, data: Partial<ScheduledTask>) => {
    return api.put<any, ScheduledTask>(`/schedules/${id}`, data)
  },
  
  deleteSchedule: (id: number) => {
    return api.delete(`/schedules/${id}`)
  }
}