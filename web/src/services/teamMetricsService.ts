/**
 * 团队效能指标服务层
 */
import api, { ApiResponse } from './api'

export interface TeamMemberMetric {
  user_id: number
  username: string
  cases_created: number
  cases_executed: number
  bugs_found: number
  avg_pass_rate: number
}

export interface TeamMetricsData {
  period_days: number
  summary: {
    total_cases: number
    total_executions: number
    avg_pass_rate: number
    active_members: number
  }
  members: TeamMemberMetric[]
}

export const getTeamMetrics = (
  params?: { project_id?: number; days?: number }
): Promise<ApiResponse<TeamMetricsData>> => {
  return api.get('/reports/team-metrics', { params }) as Promise<ApiResponse<TeamMetricsData>>
}

export const teamMetricsService = { getTeamMetrics }
export default teamMetricsService
