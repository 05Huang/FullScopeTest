/**
 * 测试计划服务层
 *
 * 对接后端测试计划 CRUD、运行管理、结果查询和趋势 API。
 */
import api, { ApiResponse } from './api'

// ── 类型定义 ────────────────────────────────────────────────────────────────

export interface TestPlan {
  id: number
  name: string
  description: string
  project_id: number
  include_cases: Array<{ case_type: string; case_id: number }>
  tags: string[]
  status: string
  created_by: number
  created_at: string
  updated_at?: string
  recent_runs?: TestPlanRun[]
  case_count?: number
}

export interface TestPlanRun {
  id: number
  plan_id: number
  status: 'pending' | 'running' | 'completed' | 'failed'
  pass_rate: number | null
  total_cases: number
  passed: number
  failed: number
  skipped: number
  started_at: string | null
  finished_at: string | null
  notes: string
  created_by: number
  created_at: string
}

export interface CaseResult {
  id: number
  run_id: number
  case_type: string
  case_id: number
  status: 'passed' | 'failed' | 'skipped' | 'error'
  duration: number | null
  error_message: string | null
  result_detail: Record<string, unknown> | null
  created_at: string
}

export interface TrendPoint {
  run_id: number
  pass_rate: number
  created_at: string
}

export interface CreatePlanRequest {
  name: string
  project_id: number
  description?: string
  include_cases?: Array<{ case_type: string; case_id: number }>
  tags?: string[]
}

export interface CreateRunRequest {
  environment_id?: number
  environment_name?: string
  notes?: string
}

// ── API 调用 ───────────────────────────────────────────────────────────────

/** 获取测试计划列表 */
export const getTestPlans = (params: {
  project_id: number
  page?: number
  per_page?: number
  status?: string
}): Promise<ApiResponse<{ items: TestPlan[]; total: number; page: number; per_page: number }>> => {
  return api.get('/test-plans', { params }) as Promise<ApiResponse<any>>
}

/** 获取测试计划详情 */
export const getTestPlan = (planId: number): Promise<ApiResponse<TestPlan>> => {
  return api.get(`/test-plans/${planId}`) as Promise<ApiResponse<TestPlan>>
}

/** 创建测试计划 */
export const createTestPlan = (
  data: CreatePlanRequest
): Promise<ApiResponse<TestPlan>> => {
  return api.post('/test-plans', data) as Promise<ApiResponse<TestPlan>>
}

/** 更新测试计划 */
export const updateTestPlan = (
  planId: number,
  data: Partial<CreatePlanRequest>
): Promise<ApiResponse<TestPlan>> => {
  return api.put(`/test-plans/${planId}`, data) as Promise<ApiResponse<TestPlan>>
}

/** 删除测试计划 */
export const deleteTestPlan = (planId: number): Promise<ApiResponse> => {
  return api.delete(`/test-plans/${planId}`) as Promise<ApiResponse>
}

/** 创建执行轮次 */
export const createTestPlanRun = (
  planId: number,
  data?: CreateRunRequest
): Promise<ApiResponse<TestPlanRun>> => {
  return api.post(`/test-plans/${planId}/runs`, data) as Promise<ApiResponse<TestPlanRun>>
}

/** 获取计划的执行轮次列表 */
export const getTestPlanRuns = (
  planId: number,
  params?: { page?: number; per_page?: number }
): Promise<ApiResponse<{ items: TestPlanRun[]; total: number }>> => {
  return api.get(`/test-plans/${planId}/runs`, { params }) as Promise<ApiResponse<any>>
}

/** 获取执行轮次详情 */
export const getTestPlanRun = (runId: number): Promise<ApiResponse<TestPlanRun>> => {
  return api.get(`/test-plan-runs/${runId}`) as Promise<ApiResponse<TestPlanRun>>
}

/** 更新用例执行结果 */
export const updateCaseResult = (
  runId: number,
  data: {
    case_type: string
    case_id: number
    status: string
    duration?: number
    error_message?: string
    result_detail?: Record<string, unknown>
    test_run_id?: number
  }
): Promise<ApiResponse> => {
  return api.patch(`/test-plan-runs/${runId}/case-results`, data) as Promise<ApiResponse>
}

/** 标记轮次完成 */
export const completeTestPlanRun = (runId: number): Promise<ApiResponse> => {
  return api.post(`/test-plan-runs/${runId}/complete`) as Promise<ApiResponse>
}

/** 获取通过率趋势 */
export const getPassRateTrend = (
  planId: number,
  limit?: number
): Promise<ApiResponse<TrendPoint[]>> => {
  return api.get(`/test-plans/${planId}/trend`, { params: { limit } }) as Promise<ApiResponse<TrendPoint[]>>
}

// ── 统一导出 ──────────────────────────────────────────────────────────────

export const testPlanService = {
  getTestPlans,
  getTestPlan,
  createTestPlan,
  updateTestPlan,
  deleteTestPlan,
  createTestPlanRun,
  getTestPlanRuns,
  getTestPlanRun,
  updateCaseResult,
  completeTestPlanRun,
  getPassRateTrend,
}

export default testPlanService
