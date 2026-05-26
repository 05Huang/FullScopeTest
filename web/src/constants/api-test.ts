/**
 * API 测试相关常量
 */

import type { HttpMethod } from '@/types'

// HTTP 方法颜色映射
export const METHOD_COLORS: Record<HttpMethod, string> = {
  GET: '#52c41a',
  POST: '#1890ff',
  PUT: '#faad14',
  DELETE: '#ff4d4f',
  PATCH: '#722ed1',
  HEAD: '#13c2c2',
  OPTIONS: '#8c8c8c',
}

// HTTP 方法选项
export const HTTP_METHODS: { label: string; value: HttpMethod }[] = [
  { label: 'GET', value: 'GET' },
  { label: 'POST', value: 'POST' },
  { label: 'PUT', value: 'PUT' },
  { label: 'DELETE', value: 'DELETE' },
  { label: 'PATCH', value: 'PATCH' },
  { label: 'HEAD', value: 'HEAD' },
  { label: 'OPTIONS', value: 'OPTIONS' },
]

// 请求体类型选项
export const BODY_TYPE_OPTIONS = [
  { label: 'JSON', value: 'json' },
  { label: 'Form Data', value: 'form' },
  { label: 'Raw', value: 'raw' },
  { label: 'None', value: 'none' },
]

// 常用请求头
export const COMMON_HEADERS = [
  'Content-Type',
  'Authorization',
  'Accept',
  'User-Agent',
  'Cache-Control',
  'X-Requested-With',
  'X-API-Key',
  'Cookie',
]

// 常用 Content-Type
export const CONTENT_TYPES = [
  'application/json',
  'application/x-www-form-urlencoded',
  'multipart/form-data',
  'text/plain',
  'text/html',
  'application/xml',
]

// 默认空键值对
export const DEFAULT_KEY_VALUE_PAIR = { key: '', value: '' }

// 默认 Mock 配置
export const DEFAULT_MOCK_CONFIG = {
  enabled: false,
  response_code: 200,
  response_body: '{\n  "success": true,\n  "data": {}\n}',
  response_headers: [{ key: 'Content-Type', value: 'application/json' }],
  delay_ms: 0,
}

// AI 执行日志类型颜色
export const LOG_TYPE_COLORS = {
  info: '#1890ff',
  success: '#52c41a',
  error: '#ff4d4f',
  warning: '#faad14',
}

// 草稿自动保存延迟 (毫秒)
export const DRAFT_SAVE_DELAY = 2000

// 请求超时时间 (毫秒)
export const REQUEST_TIMEOUT = 30000

// AI 请求超时时间 (毫秒)
export const AI_REQUEST_TIMEOUT = 120000
