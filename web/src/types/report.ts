/**
 * 测试报告相关类型定义
 */

export type TestType = 'api' | 'web' | 'performance'
export type TestStatus = 'pending' | 'running' | 'success' | 'failed' | 'cancelled'

export interface TestRun {
  id: number
  project_id: number
  test_type: TestType
  test_object_id: number
  test_object_name: string
  status: TestStatus
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
  triggered_by: string
  triggered_user_id?: number
  error_message?: string
  created_at: string
}

export interface TestReport {
  id: number
  test_run_id: number
  project_id: number
  test_type: TestType
  summary: ReportSummary
  html_path?: string
  created_at: string
}

export interface ReportSummary {
  total: number
  passed: number
  failed: number
  skipped: number
  error: number
  duration: number
  pass_rate: number
  start_time: string
  end_time: string
}

export interface ReportStatistics {
  total_runs: number
  success_runs: number
  failed_runs: number
  avg_duration: number
  pass_rate: number
  trend: TrendData[]
}

export interface TrendData {
  date: string
  total: number
  passed: number
  failed: number
}

export interface DashboardStats {
  total_projects: number
  total_test_cases: number
  total_runs_today: number
  pass_rate_today: number
  recent_runs: TestRun[]
}
