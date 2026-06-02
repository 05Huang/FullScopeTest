import api from './api'

// 通用 API 响应类型
export interface ApiResponse<T = any> {
  code: number
  message: string
  data: T
  timestamp?: string
}

// AI 统计相关类型定义
export interface AIStatsOverview {
  total_invocations: number
  success_rate: number
  total_tokens: number
  total_cost: number
  avg_latency_ms: number
  features: Record<string, number>
}

export interface SuccessRateTrend {
  date: string
  total: number
  success: number
  success_rate: number
}

export interface LatencyTrend {
  date: string
  avg_latency_ms: number
  avg_tokens: number
}

export interface TokenConsumption {
  date: string
  prompt_tokens: number
  completion_tokens: number
  total_tokens: number
  cost: number
}

export interface PromptVersionComparison {
  id: number
  feature: string
  name: string
  version: number
  is_active: boolean
  total_invocations: number
  success_count: number
  failure_count: number
  success_rate: number
  avg_latency_ms: number
  avg_tokens: number
  avg_cost: number
}

// AI 统计服务
export const aiStatsService = {
  // 获取概览统计
  getOverview: (): Promise<ApiResponse<AIStatsOverview>> => {
    return api.get('/ai/stats/overview') as Promise<ApiResponse<AIStatsOverview>>
  },

  // 获取成功率趋势
  getSuccessRateTrend: (days: number = 30, feature?: string): Promise<ApiResponse<SuccessRateTrend[]>> => {
    const params: any = { days }
    if (feature) params.feature = feature
    return api.get('/ai/stats/success-rate-trend', { params }) as Promise<ApiResponse<SuccessRateTrend[]>>
  },

  // 获取延迟趋势
  getLatencyTrend: (days: number = 30, feature?: string): Promise<ApiResponse<LatencyTrend[]>> => {
    const params: any = { days }
    if (feature) params.feature = feature
    return api.get('/ai/stats/latency-trend', { params }) as Promise<ApiResponse<LatencyTrend[]>>
  },

  // 获取 Token 消耗统计
  getTokenConsumption: (days: number = 30): Promise<ApiResponse<TokenConsumption[]>> => {
    return api.get('/ai/stats/token-consumption', { params: { days } }) as Promise<ApiResponse<TokenConsumption[]>>
  },

  // 获取 Prompt 版本效果对比
  getPromptVersionsComparison: (feature?: string): Promise<ApiResponse<PromptVersionComparison[]>> => {
    const params: any = {}
    if (feature) params.feature = feature
    return api.get('/ai/stats/prompt-versions-comparison', { params }) as Promise<ApiResponse<PromptVersionComparison[]>>
  },
}
