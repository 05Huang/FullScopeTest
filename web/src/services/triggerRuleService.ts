/**
 * 触发规则服务层
 *
 * 对接后端触发规则 CRUD 和 Webhook 触发 API。
 */
import api, { ApiResponse } from './api'

export interface TriggerRule {
  id: number
  project_id: number
  name: string
  description?: string
  trigger_event: string
  target_type: string
  target_id?: number
  target_branches?: string[]
  target_tags?: string[]
  include_paths?: string[]
  exclude_paths?: string[]
  test_types?: string[]
  tags?: string[]
  is_active: boolean
  created_by: number
  created_at: string
  updated_at?: string
}

export interface CreateRuleRequest {
  project_id: number
  name: string
  trigger_event: string
  target_type: string
  description?: string
  target_branches?: string[]
  target_tags?: string[]
  include_paths?: string[]
  exclude_paths?: string[]
  test_types?: string[]
  tags?: string[]
  target_id?: number
}

export const getTriggerRules = (projectId: number): Promise<ApiResponse<TriggerRule[]>> => {
  return api.get('/trigger-rules', { params: { project_id: projectId } }) as Promise<ApiResponse<TriggerRule[]>>
}

export const createTriggerRule = (data: CreateRuleRequest): Promise<ApiResponse<TriggerRule>> => {
  return api.post('/trigger-rules', data) as Promise<ApiResponse<TriggerRule>>
}

export const updateTriggerRule = (
  ruleId: number,
  data: Partial<CreateRuleRequest>
): Promise<ApiResponse<TriggerRule>> => {
  return api.put(`/trigger-rules/${ruleId}`, data) as Promise<ApiResponse<TriggerRule>>
}

export const deleteTriggerRule = (ruleId: number): Promise<ApiResponse> => {
  return api.delete(`/trigger-rules/${ruleId}`) as Promise<ApiResponse>
}

export const triggerRuleService = {
  getTriggerRules,
  createTriggerRule,
  updateTriggerRule,
  deleteTriggerRule,
}

export default triggerRuleService
