import api from './api'

/** Prompt 版本数据结构 */
export interface PromptVersion {
  id: number
  feature: string
  name: string
  version: number
  is_active: boolean
  system_prompt: string
  user_prompt_template: string | null
  temperature: number
  model_name: string | null
  total_invocations: number
  success_count: number
  failure_count: number
  success_rate: number
  avg_latency_ms: number
  avg_tokens: number
  avg_cost: number
  traffic_weight: number
  change_notes: string | null
  created_by: number | null
  created_at: string | null
  updated_at: string | null
  deactivated_at: string | null
}

/** 创建/更新请求参数 */
export interface PromptVersionPayload {
  feature: string
  name: string
  system_prompt: string
  user_prompt_template?: string
  temperature?: number
  model_name?: string
  is_active?: boolean
  traffic_weight?: number
  change_notes?: string
}

/** 后端分页响应 */
interface PaginatedResponse<T> {
  code: number
  message: string
  data: {
    items: T[]
    total: number
    page: number
    per_page: number
  }
}

/** 后端普通响应 */
interface ApiResponse<T> {
  code: number
  message: string
  data: T
}

/** 合法的 feature 选项 */
export const PROMPT_FEATURES = [
  { value: 'copilot', label: 'AI Copilot' },
  { value: 'script_gen', label: '脚本生成' },
  { value: 'script_gen_web', label: 'Web 脚本生成' },
  { value: 'script_gen_perf', label: '性能脚本生成' },
  { value: 'swagger_gen', label: 'Swagger 生成' },
  { value: 'dedup', label: '语义去重' },
] as const

/** Prompt 版本管理 API 服务 */
export const promptVersionService = {
  /** 获取版本列表 */
  list: (params?: {
    feature?: string
    is_active?: boolean
    page?: number
    per_page?: number
  }): Promise<PaginatedResponse<PromptVersion>> => {
    const query: Record<string, any> = {}
    if (params?.feature) query.feature = params.feature
    if (params?.is_active !== undefined) query.is_active = String(params.is_active)
    if (params?.page) query.page = params.page
    if (params?.per_page) query.per_page = params.per_page
    return api.get('/ai/prompt-versions', { params: query })
  },

  /** 获取单个版本详情 */
  get: (id: number): Promise<ApiResponse<PromptVersion>> => {
    return api.get(`/ai/prompt-versions/${id}`)
  },

  /** 创建新版本 */
  create: (payload: PromptVersionPayload): Promise<ApiResponse<PromptVersion>> => {
    return api.post('/ai/prompt-versions', payload)
  },

  /** 更新版本 */
  update: (id: number, payload: Partial<PromptVersionPayload>): Promise<ApiResponse<PromptVersion>> => {
    return api.put(`/ai/prompt-versions/${id}`, payload)
  },

  /** 停用（软删除）版本 */
  deactivate: (id: number): Promise<ApiResponse<null>> => {
    return api.delete(`/ai/prompt-versions/${id}`)
  },

  /** 激活版本（A/B 测试选择） */
  select: (feature: string): Promise<ApiResponse<PromptVersion>> => {
    return api.post('/ai/prompt-versions/select', { feature })
  },

  /** 刷新所有版本的统计数据 */
  refreshStats: (feature?: string): Promise<ApiResponse<{ refreshed_count: number }>> => {
    const params: Record<string, any> = {}
    if (feature) params.feature = feature
    return api.post('/ai/prompt-versions/refresh-stats', null, { params })
  },
}
