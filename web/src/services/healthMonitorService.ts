/**
 * API 健康监控服务层
 *
 * 对接后端健康监控配置、执行和统计 API。
 */
import api, { ApiResponse } from './api'

// ── 类型定义 ────────────────────────────────────────────────────────────────

export interface HealthMonitor {
  id: number
  name: string
  url: string
  check_interval: number
  expected_status: number
  is_active: boolean
  last_status: string | null
  last_check_at: string | null
  last_response_time: number | null
  created_at: string
}

export interface HealthCheckResult {
  status: string
  status_code: number
  response_time_ms: number
  checked_at: string
}

export interface UptimeStats {
  monitor_id: number
  days: number
  total_checks: number
  up_checks: number
  down_checks: number
  uptime_percentage: number
  avg_response_time: number
  checks: HealthCheckResult[]
}

// ── API 调用 ────────────────────────────────────────────────────────────────

/** 获取所有监控项 */
export const getMonitors = (): Promise<ApiResponse<HealthMonitor[]>> => {
  return api.get('/health-monitor') as Promise<ApiResponse<HealthMonitor[]>>
}

/** 创建监控项 */
export const createMonitor = (data: {
  name: string; url: string; check_interval?: number; expected_status?: number;
}): Promise<ApiResponse<HealthMonitor>> => {
  return api.post('/health-monitor', data) as Promise<ApiResponse<HealthMonitor>>
}

/** 获取单个监控项 */
export const getMonitor = (id: number): Promise<ApiResponse<HealthMonitor>> => {
  return api.get('/health-monitor/' + id) as Promise<ApiResponse<HealthMonitor>>
}

/** 删除监控项 */
export const deleteMonitor = (id: number): Promise<ApiResponse> => {
  return api.delete('/health-monitor/' + id) as Promise<ApiResponse>
}

/** 手动执行健康检查 */
export const runCheck = (id: number): Promise<ApiResponse<HealthCheckResult>> => {
  return api.post('/health-monitor/' + id + '/check') as Promise<ApiResponse<HealthCheckResult>>
}

/** 获取可用率统计 */
export const getUptimeStats = (id: number, days?: number): Promise<ApiResponse<UptimeStats>> => {
  return api.get('/health-monitor/' + id + '/stats', { params: { days } }) as Promise<ApiResponse<UptimeStats>>
}

// ── 统一导出 ────────────────────────────────────────────────────────────────

export const healthMonitorService = {
  getMonitors, createMonitor, getMonitor, deleteMonitor, runCheck, getUptimeStats,
};

export default healthMonitorService
