/**
 * 性能测试相关类型定义
 */

export type PerfTestStatus = 'passed' | 'failed' | 'pending' | 'running'

export interface PerfTestScenario {
  id: number
  name: string
  description: string
  target_url: string
  method: string
  headers?: Record<string, string>
  body?: Record<string, unknown> | string | null
  user_count: number
  spawn_rate: number
  duration: number
  ramp_up: number
  step_load_enabled: boolean
  step_users: number
  step_duration: number
  status: PerfTestStatus
  script_content?: string
  avg_response_time: number
  throughput: number
  error_rate: number
  last_run_at: string
  updated_at: string
}

export interface PerfTestResult {
  id: number
  scenario_id: number
  status: PerfTestStatus
  user_count: number
  duration: number
  avg_response_time: number
  p90_response_time: number
  p95_response_time: number
  p99_response_time: number
  throughput: number
  error_rate: number
  created_at: string
}

export interface PerfTestAlert {
  id: number
  scenario_id: number
  metric: string
  threshold: number
  operator: '>' | '<' | '>=' | '<=' | '=='
  enabled: boolean
  created_at: string
}
