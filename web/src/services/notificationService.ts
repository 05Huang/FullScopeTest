/**
 * 通知服务层
 *
 * 对接后端通知配置和通知发送 API。
 */
import api, { ApiResponse } from './api'

export interface NotificationConfig {
  id: number
  name: string
  channel_type: string
  webhook_url?: string
  is_active: boolean
  events: string[]
  config?: Record<string, unknown>
  created_at: string
}

export const getNotificationConfigs = (): Promise<ApiResponse<NotificationConfig[]>> => {
  return api.get('/notifications/configs') as Promise<ApiResponse<NotificationConfig[]>>
}

export const createNotificationConfig = (data: {
  name: string
  channel_type: string
  webhook_url?: string
  events?: string[]
}): Promise<ApiResponse<NotificationConfig>> => {
  return api.post('/notifications/configs', data) as Promise<ApiResponse<NotificationConfig>>
}

export const updateNotificationConfig = (
  configId: number,
  data: Partial<NotificationConfig>
): Promise<ApiResponse<NotificationConfig>> => {
  return api.put(`/notifications/configs/${configId}`, data) as Promise<ApiResponse<NotificationConfig>>
}

export const deleteNotificationConfig = (configId: number): Promise<ApiResponse> => {
  return api.delete(`/notifications/configs/${configId}`) as Promise<ApiResponse>
}

export const testNotification = (configId: number): Promise<ApiResponse> => {
  return api.post(`/notifications/configs/${configId}/test`) as Promise<ApiResponse>
}

export const notificationService = {
  getNotificationConfigs,
  createNotificationConfig,
  updateNotificationConfig,
  deleteNotificationConfig,
  testNotification,
}

export default notificationService
