import { useState, useEffect, useRef, useCallback } from 'react'
import { apiTestService, type RunProgress } from '@/services/apiTestService'

interface UseRunProgressOptions {
  /** 轮询间隔（毫秒），默认 2000 */
  interval?: number
  /** 自动停止条件 */
  autoStop?: (progress: RunProgress) => boolean
}

/**
 * 测试执行进度轮询 Hook
 *
 * 用法：
 *   const { progress, isPolling, start, stop } = useRunProgress()
 *   start(runId) // 开始轮询
 */
export const useRunProgress = (options?: UseRunProgressOptions) => {
  const interval = options?.interval ?? 2000
  const autoStop = options?.autoStop ?? ((p) => p.status === 'success' || p.status === 'failed' || p.status === 'completed')

  const [progress, setProgress] = useState<RunProgress | null>(null)
  const [isPolling, setIsPolling] = useState(false)
  const timerRef = useRef<ReturnType<typeof setInterval> | null>(null)
  const runIdRef = useRef<number | null>(null)

  const stop = useCallback(() => {
    if (timerRef.current) {
      clearInterval(timerRef.current)
      timerRef.current = null
    }
    setIsPolling(false)
  }, [])

  const poll = useCallback(async (runId: number) => {
    try {
      const res = await apiTestService.getRunProgress(runId)
      if (res.code === 200 && res.data) {
        setProgress(res.data)
        if (autoStop(res.data)) {
          stop()
        }
      }
    } catch {
      // 静默处理轮询错误
    }
  }, [autoStop, stop])

  const start = useCallback((runId: number) => {
    stop() // 清理之前的轮询
    runIdRef.current = runId
    setIsPolling(true)
    setProgress(null)
    poll(runId) // 立即请求一次
    timerRef.current = setInterval(() => poll(runId), interval)
  }, [interval, poll, stop])

  // 组件卸载时清理
  useEffect(() => {
    return () => {
      if (timerRef.current) clearInterval(timerRef.current)
    }
  }, [])

  return { progress, isPolling, start, stop }
}
