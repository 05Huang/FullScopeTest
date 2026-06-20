import api, { ApiResponse } from './api'

export type AiOperationType =
  | 'create_environment'
  | 'update_environment'
  | 'create_collection'
  | 'create_case'
  | 'run_collection'
  | 'run_case'

export interface AiPlanOperation {
  type: AiOperationType
  collection_id?: number | string
  collection_name?: string
  environment_id?: number | string
  environment_name?: string
  case_id?: number | string
  case_name?: string
  name?: string
  description?: string
  method?: string
  url?: string
  body?: unknown
  body_type?: string
  base_url?: string
  variables?: unknown
  headers?: unknown
  [key: string]: unknown
}

export interface AiPlanResult {
  summary: string
  source?: 'llm' | 'fallback'
  operations: AiPlanOperation[]
}

// ==================== 用例集合 ====================

export const getCollections = (projectId?: number): Promise<ApiResponse> => {
  return api.get('/api-test/collections', { params: { project_id: projectId } }) as Promise<ApiResponse>
}

export const createCollection = (data: {
  name: string
  description?: string
  project_id?: number
}): Promise<ApiResponse> => {
  return api.post('/api-test/collections', data) as Promise<ApiResponse>
}

export const updateCollection = (id: number, data: {
  name?: string
  description?: string
}): Promise<ApiResponse> => {
  return api.put(`/api-test/collections/${id}`, data) as Promise<ApiResponse>
}

export const deleteCollection = (id: number): Promise<ApiResponse> => {
  return api.delete(`/api-test/collections/${id}`) as Promise<ApiResponse>
}

// ==================== 测试用例 ====================

export const getCases = (params?: {
  collection_id?: number
  project_id?: number
}): Promise<ApiResponse> => {
  return api.get('/api-test/cases', { params }) as Promise<ApiResponse>
}

export const createCase = (data: {
  name: string
  method: string
  url: string
  description?: string
  headers?: Record<string, string>
  params?: Record<string, string>
  body?: Record<string, unknown> | string | null
  body_type?: string
  pre_script?: string
  post_script?: string
  assertions?: Array<Record<string, unknown>>
  collection_id?: number
  project_id?: number
  environment_id?: number
  mock_enabled?: boolean
  mock_response_code?: number
  mock_response_body?: string
  mock_response_headers?: Record<string, string>
  mock_delay_ms?: number
}): Promise<ApiResponse> => {
  return api.post('/api-test/cases', data) as Promise<ApiResponse>
}

export const getCase = (id: number): Promise<ApiResponse> => {
  return api.get(`/api-test/cases/${id}`) as Promise<ApiResponse>
}

export const updateCase = (id: number, data: {
  name?: string
  method?: string
  url?: string
  description?: string
  headers?: Record<string, string>
  params?: Record<string, string>
  body?: Record<string, unknown> | string | null
  body_type?: string
  pre_script?: string
  post_script?: string
  assertions?: Array<Record<string, unknown>>
  collection_id?: number | null
  environment_id?: number | null
  mock_enabled?: boolean
  mock_response_code?: number
  mock_response_body?: string
  mock_response_headers?: Record<string, string>
  mock_delay_ms?: number
}): Promise<ApiResponse> => {
  return api.put(`/api-test/cases/${id}`, data) as Promise<ApiResponse>
}

export const deleteCase = (id: number): Promise<ApiResponse> => {
  return api.delete(`/api-test/cases/${id}`) as Promise<ApiResponse>
}

// ==================== 执行测试 ====================

export const executeRequest = (data: {
  method: string
  url: string
  headers?: Record<string, string>
  params?: Record<string, string>
  body?: Record<string, unknown> | string | null
  body_type?: string
  timeout?: number
  env_id?: number
  pre_script?: string
  post_script?: string
  assertions?: Array<Record<string, unknown>>
  case_id?: number
  mock_enabled?: boolean
  mock_response_code?: number
  mock_response_body?: string
  mock_response_headers?: Record<string, string>
  mock_delay_ms?: number
}): Promise<ApiResponse> => {
  return api.post('/api-test/execute', data) as Promise<ApiResponse>
}

export const runCase = (caseId: number, envId?: number): Promise<ApiResponse> => {
  return api.post(`/api-test/cases/${caseId}/run`, null, {
    params: { env_id: envId }
  }) as Promise<ApiResponse>
}

export const runCollection = (collectionId: number, data?: { env_id?: number }): Promise<ApiResponse> => {
  return api.post(`/api-test/collections/${collectionId}/run`, data || {}) as Promise<ApiResponse>
}

/** 获取测试执行进度 */
export interface RunProgress {
  current: number
  total: number
  passed: number
  failed: number
  status: string
}

export const getRunProgress = (runId: number): Promise<ApiResponse<RunProgress>> => {
  return api.get(`/api-test/runs/${runId}/progress`) as Promise<ApiResponse<RunProgress>>
}

// ==================== AI Assistant ====================

export const getAiConfig = (): Promise<ApiResponse<{
  base_url: string
  model: string
  api_key: string
  vision_base_url: string
  vision_model: string
  vision_api_key: string
}>> => {
  return api.get('/api-test/ai/config') as Promise<ApiResponse<{
    base_url: string
    model: string
    api_key: string
    vision_base_url: string
    vision_model: string
    vision_api_key: string
  }>>
}

export const saveAiConfig = (data: {
  base_url: string
  model: string
  api_key: string
  vision_base_url: string
  vision_model: string
  vision_api_key: string
}): Promise<ApiResponse<{
  base_url: string
  model: string
  api_key: string
  vision_base_url: string
  vision_model: string
  vision_api_key: string
}>> => {
  return api.post('/api-test/ai/config', data) as Promise<ApiResponse<{
    base_url: string
    model: string
    api_key: string
    vision_base_url: string
    vision_model: string
    vision_api_key: string
  }>>
}

export const generateAiPlan = (data: {
  prompt: string
  base_url?: string
  model?: string
  api_key?: string
  vision_base_url?: string
  vision_model?: string
  vision_api_key?: string
  project_id?: number
  collection_id?: number
  case_id?: number
  environment_id?: number
}): Promise<ApiResponse<AiPlanResult>> => {
  return api.post('/api-test/ai/plan', data, { timeout: 120000 }) as Promise<ApiResponse<AiPlanResult>>
}

export const synthesizeCasesAI = (data: {
  base_request: Record<string, unknown>
  count?: number
  base_url?: string
  model?: string
  api_key?: string
  vision_base_url?: string
  vision_model?: string
  vision_api_key?: string
}): Promise<ApiResponse<{ cases: Array<Record<string, unknown>> }>> => {
  return api.post('/api-test/ai/synthesize-cases', data, { timeout: 120000 }) as Promise<ApiResponse<{ cases: Array<Record<string, unknown>> }>>
}

export const reviewCollectionAI = (data: {
  collection_id: number
  base_url?: string
  model?: string
  api_key?: string
  vision_base_url?: string
  vision_model?: string
  vision_api_key?: string
}): Promise<ApiResponse<{ review_summary: string, suggested_cases: Array<Record<string, unknown>> }>> => {
  return api.post('/api-test/ai/review-collection', data, { timeout: 120000 }) as Promise<ApiResponse<{ review_summary: string, suggested_cases: Array<Record<string, unknown>> }>>
}

// ==================== 智能测试选择 ====================

export interface SmartSelectResult {
  cases: Array<{
    case: Record<string, unknown>
    match_reason: string
    estimated_time: number
    score: number
    history_bonus?: string
  }>
  reasoning: string
  total_estimated_time: number
  affected_paths: string[]
}

/** 智能测试选择 — 根据变更文件推荐用例 */
export const smartTestSelect = (data: {
  changed_files: string[]
  project_id?: number
  tags?: string[]
  max_cases?: number
}): Promise<ApiResponse<SmartSelectResult>> => {
  return api.post('/api-test/smart-select', data) as Promise<ApiResponse<SmartSelectResult>>
}

// ==================== AI 用例自愈 ====================

export interface HealSuggestion {
  case_id: number
  failure_reason: string
  analysis: string
  fixes: Array<{
    field: string
    current: string
    suggested: string
    reason: string
  }>
  confidence: number
  can_auto_apply: boolean
  original_case?: Record<string, unknown>
}

/** AI 用例自愈 — 获取修复建议 */
export const healTestCase = (data: {
  case_id: number
  failure_info?: Record<string, unknown>
}): Promise<ApiResponse<HealSuggestion>> => {
  return api.post('/api-test/heal-case', data, { timeout: 120000 }) as Promise<ApiResponse<HealSuggestion>>
}

/** 应用 AI 自愈修复 */
export const applyHealFix = (data: {
  case_id: number
  fixes: Array<{
    field: string
    current: string
    suggested: string
    reason: string
  }>
}): Promise<ApiResponse> => {
  return api.post('/api-test/apply-heal', data) as Promise<ApiResponse>
}

// ==================== 标签管理 ====================

export interface TagStat {
  tag: string
  count: number
  percentage: number
}

/** 获取标签统计 */
export const getTagStats = (projectId?: number): Promise<ApiResponse<TagStat[]>> => {
  return api.get('/api-test/tags/stats', {
    params: { project_id: projectId },
  }) as Promise<ApiResponse<TagStat[]>>
}

/** 按标签过滤用例 */
export const filterByTags = (data: {
  tags: string[]
  project_id?: number
  match_all?: boolean
}): Promise<ApiResponse> => {
  return api.post('/api-test/tags/filter', data) as Promise<ApiResponse>
}

// ==================== Schema 校验 ====================

export interface SchemaValidationResult {
  valid: boolean
  errors: Array<{ path: string; message: string; type: string }>
  warnings: Array<{ path: string; message: string; type: string }>
  summary: string
  total_issues: number
}

/** 校验响应是否符合 Schema */
export const validateResponseSchema = (data: {
  schema: Record<string, unknown>
  response_body: string
  status_code?: number
}): Promise<ApiResponse<SchemaValidationResult>> => {
  return api.post('/api-test/validate-schema', data) as Promise<ApiResponse<SchemaValidationResult>>
}

/** 从响应自动生成 JSON Schema */
export const generateResponseSchema = (data: {
  response_body: string
  max_depth?: number
}): Promise<ApiResponse<Record<string, unknown>>> => {
  return api.post('/api-test/generate-schema', data) as Promise<ApiResponse<Record<string, unknown>>>
}

// ==================== HAR 导入 ====================

export interface HarParseResult {
  entries: Array<{
    name: string
    method: string
    url: string
    headers: Record<string, string>
    body: string
    body_type: string
    description: string
  }>
  summary: {
    total_entries: number
    parsed: number
    skipped: number
    methods: Record<string, number>
    domains: string[]
  }
}

/** 解析 HAR 文件预览（不导入） */
export const parseHarPreview = (data: {
  har_content: string
}): Promise<ApiResponse<HarParseResult>> => {
  return api.post('/api-test/parse-har', data) as Promise<ApiResponse<HarParseResult>>
}

/** 导入 HAR 文件生成测试用例 */
export const importHar = (data: {
  har_content: string
  project_id: number
  collection_id?: number
  collection_name?: string
}): Promise<ApiResponse> => {
  return api.post('/api-test/import-har', data) as Promise<ApiResponse>
}

// ==================== API 变更检测 ====================

export interface ChangeDetectionResult {
  has_changes: boolean
  is_first_record: boolean
  changes: Array<{
    type: 'added' | 'removed' | 'type_changed'
    path: string
    old_type?: string
    new_type?: string
    severity: 'info' | 'warning' | 'breaking'
  }>
  summary: string
  previous_recorded_at?: string
}

/** 检测 API 响应结构变更 */
export const detectApiChanges = (data: {
  case_id: number
  response_body: string
  status_code?: number
}): Promise<ApiResponse<ChangeDetectionResult>> => {
  return api.post('/api-test/detect-changes', data) as Promise<ApiResponse<ChangeDetectionResult>>
}

// ==================== BDD/Gherkin ====================

/** 解析 Gherkin 文本为结构化数据 */
export const parseBdd = (data: {
  content: string
  collection_id?: number
}): Promise<ApiResponse> => {
  return api.post('/api-test/bdd/parse', data) as Promise<ApiResponse>
}

/** 将解析结果导入为测试用例 */
export const importBdd = (data: {
  feature: string
  scenarios: Array<{
    name: string
    steps: Array<{ keyword: string; text: string }>
  }>
  collection_id?: number
}): Promise<ApiResponse> => {
  return api.post('/api-test/bdd/import', data) as Promise<ApiResponse>
}

// ==================== 多步骤场景执行 ====================

/** 执行多步骤场景 */
export const executeScenario = (data: {
  steps: Array<{
    case_id?: number
    name: string
    method: string
    url: string
    headers?: Record<string, string>
    body?: string
    extract?: Array<{ variable: string; path: string }>
    condition?: { field: string; operator: string; value: string }
  }>
  environment_id?: number
  variables?: Record<string, string>
}): Promise<ApiResponse> => {
  return api.post('/api-test/execute-scenario', data) as Promise<ApiResponse>
}

// 导出服务对象
export const apiTestService = {
  getCollections,
  createCollection,
  updateCollection,
  deleteCollection,
  getCases,
  createCase,
  getCase,
  updateCase,
  deleteCase,
  executeRequest,
  runCase,
  runCollection,
  getRunProgress,
  getAiConfig,
  saveAiConfig,
  generateAiPlan,
  synthesizeCasesAI,
  reviewCollectionAI,
  smartTestSelect,
  healTestCase,
  applyHealFix,
  getTagStats,
  filterByTags,
  validateResponseSchema,
  generateResponseSchema,
  parseHarPreview,
  importHar,
  detectApiChanges,
  parseBdd,
  importBdd,
  executeScenario,
}
