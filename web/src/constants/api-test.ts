/**
 * API 测试共享常量
 */

/** HTTP 方法颜色映射 */
export const HTTP_METHOD_COLORS: Record<string, string> = {
  GET: '#52c41a',
  POST: '#1890ff',
  PUT: '#faad14',
  DELETE: '#ff4d4f',
  PATCH: '#722ed1',
  HEAD: '#13c2c2',
  OPTIONS: '#8c8c8c',
}

/** 浏览器配置 */
export const BROWSER_CONFIG: Record<string, { color: string; name: string }> = {
  chromium: { color: 'blue', name: 'Chromium' },
  firefox: { color: 'orange', name: 'Firefox' },
  webkit: { color: 'purple', name: 'WebKit' },
}

/** 批量操作并发数 */
export const BATCH_ACTION_CONCURRENCY = 5

/** AI 探索历史存储键前缀 */
export const EXPLORE_HISTORY_STORAGE_PREFIX = 'web-test-ai-explore-history'

/** 性能测试最大用户数 */
export const PERF_MAX_USERS = 2000

/** 探索历史上限 */
export const EXPLORE_HISTORY_LIMIT = 20
