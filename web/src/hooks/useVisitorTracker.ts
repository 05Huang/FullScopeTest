/**
 * 访客追踪 Hook
 *
 * 自动收集访客数据并发送到后端
 */
import { useEffect, useRef, useCallback } from 'react'
import { trackVisitor, TrackData } from '@/services/visitorStatsService'

// 生成唯一会话 ID
const generateSessionId = (): string => {
  const existing = sessionStorage.getItem('fst_session_id')
  if (existing) return existing

  const id = `${Date.now()}-${Math.random().toString(36).substring(2, 15)}`
  sessionStorage.setItem('fst_session_id', id)
  return id
}

// 页面停留计时器
interface PageTimer {
  startTime: number
  path: string
}

export const useVisitorTracker = () => {
  const sessionIdRef = useRef<string>('')
  const pageTimersRef = useRef<Map<string, PageTimer>>(new Map())
  const pageViewsRef = useRef(0)
  const totalDurationRef = useRef(0)
  const currentPageRef = useRef('')
  const heartbeatRef = useRef<number | null>(null)

  // 发送追踪数据
  const sendTrack = useCallback(async (pageDuration: number = 0) => {
    if (!sessionIdRef.current) return

    const data: TrackData = {
      session_id: sessionIdRef.current,
      page_views: pageViewsRef.current,
      total_duration: totalDurationRef.current,
      current_page: currentPageRef.current,
      page_duration: pageDuration,
      screen_width: window.screen.width,
      screen_height: window.screen.height,
      referrer: document.referrer || '',
    }

    try {
      await trackVisitor(data)
    } catch (e) {
      // 静默失败，不影响用户体验
      console.debug('Visitor tracking failed:', e)
    }
  }, [])

  // 记录页面访问
  const trackPageView = useCallback(() => {
    const path = window.location.pathname
    const now = Date.now()

    // 计算上一页停留时间
    if (currentPageRef.current && pageTimersRef.current.has(currentPageRef.current)) {
      const timer = pageTimersRef.current.get(currentPageRef.current)!
      const duration = Math.floor((now - timer.startTime) / 1000)
      totalDurationRef.current += duration
    }

    // 记录新页面
    currentPageRef.current = path
    pageViewsRef.current++
    pageTimersRef.current.set(path, { startTime: now, path })

    // 防抖发送
    if (heartbeatRef.current) {
      clearTimeout(heartbeatRef.current)
    }
    heartbeatRef.current = window.setTimeout(() => {
      sendTrack(0)
    }, 5000)
  }, [sendTrack])

  useEffect(() => {
    // 初始化会话
    sessionIdRef.current = generateSessionId()

    // 记录首次访问
    trackPageView()

    // 监听页面变化
    const handlePopstate = () => trackPageView()
    window.addEventListener('popstate', handlePopstate)

    // 监听页面可见性变化（用户切换标签页）
    const handleVisibilityChange = () => {
      if (document.visibilityState === 'visible') {
        // 重新进入页面，刷新计时
        if (currentPageRef.current) {
          const timer = pageTimersRef.current.get(currentPageRef.current)
          if (timer) {
            timer.startTime = Date.now()
          }
        }
      }
    }
    document.addEventListener('visibilitychange', handleVisibilityChange)

    // 定期心跳（每 30 秒）
    const heartbeatInterval = setInterval(() => {
      if (currentPageRef.current) {
        const timer = pageTimersRef.current.get(currentPageRef.current)
        if (timer) {
          const duration = Math.floor((Date.now() - timer.startTime) / 1000)
          sendTrack(duration)
        }
      }
    }, 30000)

    // 页面离开前发送最终数据
    const handleBeforeUnload = () => {
      if (currentPageRef.current) {
        const timer = pageTimersRef.current.get(currentPageRef.current)
        if (timer) {
          const duration = Math.floor((Date.now() - timer.startTime) / 1000)
          totalDurationRef.current += duration
          // 同步发送，不等待
          navigator.sendBeacon('/api/v1/visitor/track', JSON.stringify({
            session_id: sessionIdRef.current,
            page_views: pageViewsRef.current,
            total_duration: totalDurationRef.current,
            current_page: currentPageRef.current,
            page_duration: duration,
            screen_width: window.screen.width,
            screen_height: window.screen.height,
            referrer: document.referrer || '',
          }))
        }
      }
    }
    window.addEventListener('beforeunload', handleBeforeUnload)

    return () => {
      window.removeEventListener('popstate', handlePopstate)
      document.removeEventListener('visibilitychange', handleVisibilityChange)
      clearInterval(heartbeatInterval)
      window.removeEventListener('beforeunload', handleBeforeUnload)
      if (heartbeatRef.current) {
        clearTimeout(heartbeatRef.current)
      }
    }
  }, [trackPageView, sendTrack])

  return {
    sessionId: sessionIdRef.current,
  }
}

export default useVisitorTracker
