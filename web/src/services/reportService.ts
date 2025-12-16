import api, { ApiResponse } from './api'

// ==================== 测试执行记录 ====================

export interface TestRun {
  id: number
  project_id: number
  test_type: 'api' | 'web' | 'performance'
  test_object_id?: number
  test_object_name?: string
  status: 'pending' | 'running' | 'success' | 'failed' | 'cancelled'
  total_cases: number
  passed: number
  failed: number
  skipped: number
  error: number
  pass_rate: number
  duration?: number
  started_at?: string
  finished_at?: string
  environment_id?: number
  environment_name?: string
  report_path?: string
  allure_report_path?: string
  triggered_by: 'manual' | 'schedule' | 'ci'
  triggered_user_id?: number
  error_message?: string
  created_at: string
}

export interface TestRunListParams {
  project_id?: number
  test_type?: string
  status?: string
  page?: number
  per_page?: number
  start_date?: string
  end_date?: string
}

export interface DashboardStats {
  api_tests: { total: number; passed: number; failed: number }
  web_tests: { total: number; passed: number; failed: number }
  perf_tests: { total: number; running: number }
  recent_runs: TestRun[]
}

export interface ReportStatistics {
  summary: {
    total_runs: number
    success_runs: number
    failed_runs: number
    running_runs: number
    success_rate: number
  }
  by_type: Array<{
    type: string
    count: number
    passed: number
    failed: number
  }>
  daily_trend: Array<{
    date: string
    passed: number
    failed: number
    total: number
  }>
}

// 获取测试执行记录列表
export const getTestRuns = (params?: TestRunListParams): Promise<ApiResponse> => {
  return api.get('/test-runs', { params }) as Promise<ApiResponse>
}

// 创建测试执行记录
export const createTestRun = (data: {
  project_id: number
  test_type: string
  test_object_id?: number
  test_object_name?: string
  total_cases?: number
  environment_id?: number
  environment_name?: string
  triggered_by?: string
}): Promise<ApiResponse> => {
  return api.post('/test-runs', data) as Promise<ApiResponse>
}

// 获取测试执行记录详情
export const getTestRun = (runId: number): Promise<ApiResponse> => {
  return api.get(`/test-runs/${runId}`) as Promise<ApiResponse>
}

// 更新测试执行记录
export const updateTestRun = (runId: number, data: Partial<TestRun>): Promise<ApiResponse> => {
  return api.put(`/test-runs/${runId}`, data) as Promise<ApiResponse>
}

// 删除测试执行记录
export const deleteTestRun = (runId: number): Promise<ApiResponse> => {
  return api.delete(`/test-runs/${runId}`) as Promise<ApiResponse>
}

// ==================== 统计数据 ====================

// 获取报告统计数据
export const getReportStatistics = (params?: {
  project_id?: number
  days?: number
}): Promise<ApiResponse<ReportStatistics>> => {
  return api.get('/reports/statistics', { params }) as Promise<ApiResponse<ReportStatistics>>
}

// 获取仪表盘统计数据
export const getDashboardStats = (): Promise<ApiResponse<DashboardStats>> => {
  return api.get('/reports/dashboard') as Promise<ApiResponse<DashboardStats>>
}

// ==================== 报告导出 ====================

// 导出报告 (JSON)
export const exportReportJson = (runId: number): Promise<ApiResponse> => {
  return api.get(`/reports/${runId}/export`, { params: { format: 'json' } }) as Promise<ApiResponse>
}

// 导出报告 (HTML) - 返回下载链接
export const getReportExportUrl = (runId: number, format: 'json' | 'html' = 'html'): string => {
  return `/api/v1/reports/${runId}/export?format=${format}`
}

// 导出服务对象
export const reportService = {
  getTestRuns,
  createTestRun,
  getTestRun,
  updateTestRun,
  deleteTestRun,
  getReportStatistics,
  getDashboardStats,
  exportReportJson,
  getReportExportUrl,
}

export default reportService
