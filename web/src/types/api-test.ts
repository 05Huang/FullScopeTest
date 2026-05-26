/**
 * API 测试相关类型定义
 */

// HTTP 方法
export type HttpMethod = 'GET' | 'POST' | 'PUT' | 'DELETE' | 'PATCH' | 'HEAD' | 'OPTIONS'

// 请求体类型
export type BodyType = 'json' | 'form' | 'raw' | 'none'

// 键值对
export interface KeyValuePair {
  key: string
  value: string
}

// API 测试用例
export interface ApiTestCase {
  id: number
  name: string
  method: HttpMethod
  url: string
  description?: string
  headers: Record<string, string>
  params: Record<string, string>
  body?: any
  body_type: BodyType
  pre_script?: string
  post_script?: string
  collection_id?: number
  project_id?: number
  environment_id?: number
  mock_enabled: boolean
  mock_response_code?: number
  mock_response_body?: string
  mock_response_headers?: Record<string, string>
  mock_delay_ms?: number
  created_at: string
  updated_at: string
}

// API 测试集合
export interface ApiTestCollection {
  id: number
  name: string
  description?: string
  project_id: number
  parent_id?: number
  created_at: string
  updated_at: string
  children?: ApiTestCollection[]
  cases?: ApiTestCase[]
}

// 测试执行响应
export interface TestExecutionResponse {
  success: boolean
  status_code: number
  headers: Record<string, string>
  body: any
  response_time: number
  size: number
  script_execution?: ScriptExecutionResult
}

// 脚本执行结果
export interface ScriptExecutionResult {
  pre_script?: {
    executed: boolean
    passed?: boolean
    error?: string
    duration?: number
  }
  post_script?: {
    executed: boolean
    passed?: boolean
    error?: string
    duration?: number
    assertions?: AssertionResult
  }
}

// 断言结果
export interface AssertionResult {
  total: number
  passed: number
  failed: number
  details?: AssertionDetail[]
}

// 断言详情
export interface AssertionDetail {
  name: string
  passed: boolean
  error?: string
}

// 环境变量
export interface Environment {
  id: number
  name: string
  project_id: number
  variables: Record<string, string>
  headers: Record<string, string>
  created_at: string
  updated_at: string
}

// AI 配置
export interface AiConfig {
  base_url: string
  model: string
  api_key: string
  vision_base_url: string
  vision_model: string
  vision_api_key: string
  enabled: boolean
}

// AI 计划操作类型
export type AiOperationType =
  | 'create_environment'
  | 'update_environment'
  | 'create_collection'
  | 'create_case'
  | 'run_collection'
  | 'run_case'

// AI 计划操作
export interface AiPlanOperation {
  type: AiOperationType
  [key: string]: any
}

// AI 计划结果
export interface AiPlanResult {
  summary: string
  source?: 'llm' | 'fallback'
  operations: AiPlanOperation[]
}

// AI 执行日志
export interface AiExecutionLog {
  id: string
  timestamp: number
  type: 'info' | 'success' | 'error' | 'warning'
  message: string
  details?: any
}

// Mock 配置
export interface MockConfig {
  enabled: boolean
  response_code: number
  response_body: string
  response_headers: KeyValuePair[]
  delay_ms: number
}

// 树节点数据
export interface ApiTestTreeNode {
  key: string
  title: string
  type: 'collection' | 'case'
  id: number
  method?: HttpMethod
  isLeaf?: boolean
  children?: ApiTestTreeNode[]
}

// 侧边栏标签页
export type SidebarTab = 'cases' | 'environments' | 'ai'

// 响应标签页
export type ResponseTab = 'body' | 'headers' | 'scripts' | 'timeline'
