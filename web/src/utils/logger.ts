/**
 * 前端日志工具
 *
 * 开发环境输出到控制台，生产环境静默或上报错误追踪服务。
 */

const isDev = import.meta.env.DEV

export const logger = {
  info: (...args: unknown[]) => {
    if (isDev) {
      console.log('[INFO]', ...args)
    }
  },

  warn: (...args: unknown[]) => {
    if (isDev) {
      console.warn('[WARN]', ...args)
    }
  },

  error: (...args: unknown[]) => {
    if (isDev) {
      console.error('[ERROR]', ...args)
    }
    // 生产环境可接入 Sentry 等错误追踪服务
    // if (!isDev && window.Sentry) {
    //   window.Sentry.captureException(args[0])
    // }
  },

  debug: (...args: unknown[]) => {
    if (isDev) {
      console.debug('[DEBUG]', ...args)
    }
  },
}

export default logger
