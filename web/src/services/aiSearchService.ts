import api, { ApiResponse } from './api'

export interface GlobalSearchResult {
  id: number
  type: string
  title: string
  description: string
  url: string
}

export const globalSearchAI = (data: {
  query: string
  base_url?: string
  model?: string
  api_key?: string
}): Promise<ApiResponse<{ results: GlobalSearchResult[] }>> => {
  return api.post('/ai/global-search', data) as Promise<ApiResponse<{ results: GlobalSearchResult[] }>>
}
