/**
 * 质量门禁服务层
 *
 * 对接后端质量门禁 CRUD、评估和评估历史 API。
 */
import api, { ApiResponse } from './api'

// ── 类型定义 ────────────────────────────────────────────────────────────────

export interface QualityGate {
  id: number
  project_id: number
  name: string
  description: string
  is_active: boolean
  min_pass_rate: number | null
  max_p95_response_time: number | null
  max_visual_diff_percentage: number | null
  created_by: number
  created_at: string
  updated_at?: string
}

export interface EvaluationResult {
  passed: boolean
  details: Record<string, { threshold: number; actual: number; passed: boolean }>
  gate_id: number
  test_run_id: number
}

export interface CreateGateRequest {
  name: string
  project_id: number
  description?: string
  is_active?: boolean
  min_pass_rate?: number
  max_p95_response_time?: number
  max_visual_diff_percentage?: number
}

// ── API 调用 ───────────────────────────────────────────────────────────────

/** 获取质量门禁列表 */
export const getQualityGates = (projectId?: number): Promise<ApiResponse<QualityGate[]>> => {
  return api.get('/quality-gates', { params: { project_id: projectId } }) as Promise<ApiResponse<QualityGate[]>>
}

/** 获取质量门禁详情 */
export const getQualityGate = (gateId: number): Promise<ApiResponse<QualityGate>> => {
  return api.get(`/quality-gates/${gateId}`) as Promise<ApiResponse<QualityGate>>
}

/** 创建质量门禁 */
export const createQualityGate = (
  data: CreateGateRequest
): Promise<ApiResponse<QualityGate>> => {
  return api.post('/quality-gates', data) as Promise<ApiResponse<QualityGate>>
}

/** 更新质量门禁 */
export const updateQualityGate = (
  gateId: number,
  data: Partial<CreateGateRequest>
): Promise<ApiResponse<QualityGate>> => {
  return api.put(`/quality-gates/${gateId}`, data) as Promise<ApiResponse<QualityGate>>
}

/** 删除质量门禁 */
export const deleteQualityGate = (gateId: number): Promise<ApiResponse> => {
  return api.delete(`/quality-gates/${gateId}`) as Promise<ApiResponse>
}

/** 触发评估 */
export const evaluateQualityGate = (
  gateId: number,
  testRunId: number
): Promise<ApiResponse<EvaluationResult>> => {
  return api.post(`/quality-gates/${gateId}/evaluate`, {
    test_run_id: testRunId,
  }) as Promise<ApiResponse<EvaluationResult>>
}

/** 获取评估历史 */
export const getEvaluations = (
  gateId: number,
  params?: { page?: number; per_page?: number }
): Promise<ApiResponse<{ items: any[]; total: number }>> => {
  return api.get(`/quality-gates/${gateId}/evaluations`, { params }) as Promise<ApiResponse<any>>
}

// ── 统一导出 ──────────────────────────────────────────────────────────────

export const qualityGateService = {
  getQualityGates,
  getQualityGate,
  createQualityGate,
  updateQualityGate,
  deleteQualityGate,
  evaluateQualityGate,
  getEvaluations,
}

export default qualityGateService
