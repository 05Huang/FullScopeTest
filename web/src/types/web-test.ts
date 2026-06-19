/**
 * Web 测试相关类型定义
 */

export type WebTestStatus = 'passed' | 'failed' | 'pending' | 'running'

export type BrowserType = 'chromium' | 'firefox' | 'webkit'

export interface WebTestScript {
  id: number
  name: string
  description: string
  collection_id?: number | null
  collection_name?: string
  target_url?: string
  browser: string
  status: WebTestStatus
  step_count: number
  last_run_at: string
  last_run_duration?: number
  updated_at: string
  script_content: string
  last_result?: WebTestResult
}

export interface WebTestResult {
  success: boolean
  stdout?: string
  stderr?: string
  return_code?: number
  duration?: number
  error?: string
  vision_results?: VisualDiffResult[]
}

export interface VisualDiffResult {
  name: string
  status: 'new' | 'passed' | 'failed'
  mismatch_ratio: number
  mismatch_pixels: number
  total_pixels: number
  baseline_id?: number
  baseline_image_path?: string
  current_image_path?: string
  diff_image_path?: string
}

export interface WebTestCollection {
  id: number
  name: string
  description?: string
  project_id?: number | null
  script_count?: number
}

export interface ExploreHistoryItem {
  id: string
  started_at: string
  start_url: string
  objective: string
  max_steps: number
  report: Record<string, unknown> | null
  console_lines: string[]
}
