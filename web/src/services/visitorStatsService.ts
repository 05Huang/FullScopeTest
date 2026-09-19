/**
 * 访客统计服务层
 *
 * 对接后端访客统计 API。
 */
import api, { ApiResponse } from './api'

// ── 类型定义 ────────────────────────────────────────────────────────────────

export interface VisitedPage {
  path: string
  duration: number
  visits: number
}

export interface VisitorStat {
  id: number
  session_id: string
  ip_address: string
  ip_country: string
  ip_city: string
  ip_isp: string
  first_visit: string
  last_active: string
  total_duration: number
  page_views: number
  device_type: string
  browser: string
  browser_version: string
  os: string
  os_version: string
  screen_width: number
  screen_height: number
  referrer: string
  entry_page: string
  visited_pages: VisitedPage[]
  created_at: string
}

export interface DailyStat {
  date: string
  visitors: number
  page_views: number
}

export interface VisitorStatsOverview {
  period_days: number
  total_visitors: number
  today_visitors: number
  online_visitors: number
  avg_duration: number
  total_page_views: number
  by_device: Record<string, number>
  by_browser: Record<string, number>
  by_country: Record<string, number>
  daily_trend: DailyStat[]
}

export interface VisitorListParams {
  page?: number
  per_page?: number
  device_type?: string
  country?: string
}

export interface VisitorListResponse {
  items: VisitorStat[]
  total: number
  page: number
  per_page: number
  pages: number
}

export interface TopPage {
  path: string
  views: number
  avg_duration: number
}

// ── 追踪数据类型 ────────────────────────────────────────────────────────────

export interface TrackData {
  session_id: string
  page_views: number
  total_duration: number
  current_page: string
  page_duration: number
  screen_width: number
  screen_height: number
  referrer: string
}

// ── API 调用 ───────────────────────────────────────────────────────────────

/** 记录访客数据 */
export const trackVisitor = (data: TrackData): Promise<ApiResponse<{ tracked: boolean }>> => {
  return api.post('/visitor/track', data) as Promise<ApiResponse<{ tracked: boolean }>>
}

/** 获取访客统计概览 */
export const getVisitorStats = (days?: number): Promise<ApiResponse<VisitorStatsOverview>> => {
  return api.get('/visitor/stats', { params: { days } }) as Promise<ApiResponse<VisitorStatsOverview>>
}

/** 获取访客列表（需管理员） */
export const getVisitorList = (
  params?: VisitorListParams
): Promise<ApiResponse<VisitorListResponse>> => {
  return api.get('/visitor/list', { params }) as Promise<ApiResponse<VisitorListResponse>>
}

/** 获取访客详情 */
export const getVisitorDetail = (visitorId: number): Promise<ApiResponse<VisitorStat>> => {
  return api.get(`/visitor/${visitorId}`) as Promise<ApiResponse<VisitorStat>>
}

/** 获取最受欢迎页面排行 */
export const getTopPages = (days?: number, limit?: number): Promise<ApiResponse<TopPage[]>> => {
  return api.get('/visitor/top-pages', { params: { days, limit } }) as Promise<ApiResponse<TopPage[]>>
}

/** 清理旧访客数据 */
export const cleanupOldVisitors = (days?: number): Promise<ApiResponse<{ deleted: number }>> => {
  return api.post('/visitor/cleanup', null, { params: { days } }) as Promise<ApiResponse<{ deleted: number }>>
}

// ── 统一导出 ──────────────────────────────────────────────────────────────

export const visitorStatsService = {
  trackVisitor,
  getVisitorStats,
  getVisitorList,
  getVisitorDetail,
  getTopPages,
  cleanupOldVisitors,
}

export default visitorStatsService
