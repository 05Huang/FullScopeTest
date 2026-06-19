/**
 * 审计日志服务层
 *
 * 对接后端审计日志查询、详情和统计 API。
 */
import api, { ApiResponse } from './api'

// ── 类型定义 ────────────────────────────────────────────────────────────────

export interface AuditLog {
  id: number
  user_id: number | null
  organization_id: number | null
  action: string
  resource_type: string
  resource_id: number | null
  changes: Record<string, unknown> | null
  old_values: Record<string, unknown> | null
  new_values: Record<string, unknown> | null
  ip_address: string | null
  user_agent: string | null
  created_at: string
}

export interface AuditLogListParams {
  page?: number
  per_page?: number
  user_id?: number
  action?: string
  resource_type?: string
  start_time?: string
  end_time?: string
}

export interface AuditLogListResponse {
  items: AuditLog[]
  total: number
  page: number
  per_page: number
  pages: number
}

export interface AuditStats {
  period_days: number
  by_action: Record<string, number>
  by_resource: Record<string, number>
  active_users: Array<{ user_id: number; count: number }>
}

// ── API 调用 ───────────────────────────────────────────────────────────────

/** 获取审计日志列表（支持筛选/分页） */
export const getAuditLogs = (
  params?: AuditLogListParams
): Promise<ApiResponse<AuditLogListResponse>> => {
  return api.get('/audit-logs', { params }) as Promise<ApiResponse<AuditLogListResponse>>
}

/** 获取审计日志详情 */
export const getAuditLog = (logId: number): Promise<ApiResponse<AuditLog>> => {
  return api.get(`/audit-logs/${logId}`) as Promise<ApiResponse<AuditLog>>
}

/** 获取审计日志统计 */
export const getAuditStats = (days?: number): Promise<ApiResponse<AuditStats>> => {
  return api.get('/audit-logs/stats', { params: { days } }) as Promise<ApiResponse<AuditStats>>
}

/** 导出审计日志（CSV/JSON） */
export const exportAuditLogs = (params?: {
  format?: 'csv' | 'json'
  action?: string
  resource_type?: string
  days?: number
}): Promise<ApiResponse> => {
  return api.get('/audit-logs/export', { params, responseType: 'blob' as any }) as Promise<ApiResponse>
}

// ── 统一导出 ──────────────────────────────────────────────────────────────

export const auditLogService = {
  getAuditLogs,
  getAuditLog,
  getAuditStats,
  exportAuditLogs,
}

export default auditLogService
