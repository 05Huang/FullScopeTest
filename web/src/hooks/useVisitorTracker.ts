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

interface PageRecord {
  path: string
  enterTime: number
  duration: number
}

interface SessionData {
  sessionId: string
  pageRecords: PageRecord[]
  totalPageViews: number
  lastTrackTime: number
}

const SESSION_KEY = 'fst_visitor_session'
const HEARTBEAT_INTERVAL = 15000 // 15秒心跳
const PAGE_MIN_DURATION = 2000   // 最小页面停留时间 2秒

// 保存会话数据到 sessionStorage
const saveSessionData = (data: SessionData) => {
  try {
    sessionStorage.setItem(SESSION_KEY, JSON.stringify(data))
  } catch (e) {
    // 忽略存储错误
  }
}

// 加载会话数据
const loadSessionData = (sessionId: string): SessionData => {
  try {
    const stored = sessionStorage.getItem(SESSION_KEY)
    if (stored) {
      const data = JSON.parse(stored)
      if (data.sessionId === sessionId) {
        return data
      }
    }
  } catch (e) {
    // 忽略解析错误
  }
  return {
    sessionId,
    pageRecords: [],
    totalPageViews: 0,
    lastTrackTime: Date.now(),
  }
}

export const useVisitorTracker = () => {
  const sessionIdRef = useRef<string>('')
  const sessionDataRef = useRef<SessionData | null>(null)
  const currentPageRef = useRef<string>('')
  const currentPageEnterTimeRef = useRef<number>(0)
  const heartbeatIntervalRef = useRef<number | null>(null)
  const isInitializedRef = useRef(false)

  // 发送追踪数据
  const sendTrack = useCallback(async (currentPage: string, duration: number = 0) => {
    if (!sessionIdRef.current || !sessionDataRef.current) return

    const data: TrackData = {
      session_id: sessionIdRef.current,
      page_views: sessionDataRef.current.totalPageViews,
      total_duration: duration,
      current_page: currentPage,
      page_duration: duration,
      screen_width: window.screen.width,
      screen_height: window.screen.height,
      referrer: document.referrer || '',
    }

    try {
      await trackVisitor(data)
      sessionDataRef.current.lastTrackTime = Date.now()
      saveSessionData(sessionDataRef.current)
    } catch (e) {
      console.debug('Visitor tracking failed:', e)
    }
  }, [])

  // 记录页面离开
  const trackPageLeave = useCallback(() => {
    const path = currentPageRef.current
    const now = Date.now()
    const duration = Math.max(0, Math.floor((now - currentPageEnterTimeRef.current) / 1000))

    // 只有停留超过最小时间才记录
    if (path && duration >= Math.floor(PAGE_MIN_DURATION / 1000)) {
      if (sessionDataRef.current) {
        // 更新当前页面记录
        const existingRecord = sessionDataRef.current.pageRecords.find(r => r.path === path)
        if (existingRecord) {
          existingRecord.duration += duration
        } else {
          sessionDataRef.current.pageRecords.push({
            path,
            enterTime: currentPageEnterTimeRef.current,
            duration,
          })
        }
        sessionDataRef.current.totalPageViews++

        // 发送追踪数据
        sendTrack(path, duration)
      }
    }
  }, [sendTrack])

  // 记录页面进入
  const trackPageEnter = useCallback(() => {
    const path = window.location.pathname
    const now = Date.now()

    // 先记录上一个页面的离开
    if (currentPageRef.current && currentPageRef.current !== path) {
      trackPageLeave()
    }

    // 记录新页面
    currentPageRef.current = path
    currentPageEnterTimeRef.current = now
  }, [trackPageLeave])

  // 定期心跳
  const sendHeartbeat = useCallback(() => {
    const path = currentPageRef.current
    const now = Date.now()
    const duration = Math.max(0, Math.floor((now - currentPageEnterTimeRef.current) / 1000))

    if (path && sessionDataRef.current) {
      // 更新当前页面的时长
      const existingRecord = sessionDataRef.current.pageRecords.find(r => r.path === path)
      if (existingRecord) {
        existingRecord.duration = duration
      }

      // 计算总时长
      const totalDuration = sessionDataRef.current.pageRecords.reduce((sum, r) => sum + r.duration, 0)

      sendTrack(path, totalDuration)
    }
  }, [sendTrack])

  useEffect(() => {
    // 防止重复初始化
    if (isInitializedRef.current) return
    isInitializedRef.current = true

    // 初始化会话
    sessionIdRef.current = generateSessionId()
    sessionDataRef.current = loadSessionData(sessionIdRef.current)

    // 记录首次页面访问
    currentPageRef.current = window.location.pathname
    currentPageEnterTimeRef.current = Date.now()

    // 立即发送首次追踪
    sendTrack(currentPageRef.current, 0)

    // 启动心跳
    heartbeatIntervalRef.current = window.setInterval(sendHeartbeat, HEARTBEAT_INTERVAL)

    // 监听路由变化
    const handlePopstate = () => {
      trackPageEnter()
    }
    window.addEventListener('popstate', handlePopstate)

    // 监听 visibility change
    const handleVisibilityChange = () => {
      if (document.visibilityState === 'visible') {
        // 页面重新可见时，重置计时起点
        currentPageEnterTimeRef.current = Date.now()
      }
    }
    document.addEventListener('visibilitychange', handleVisibilityChange)

    // 页面离开前发送最终数据
    const handleBeforeUnload = () => {
      trackPageLeave()

      // 使用 sendBeacon 确保数据发送
      const data = {
        session_id: sessionIdRef.current,
        page_views: sessionDataRef.current?.totalPageViews || 0,
        total_duration: sessionDataRef.current?.pageRecords.reduce((sum, r) => sum + r.duration, 0) || 0,
        current_page: currentPageRef.current,
        page_duration: Math.max(0, Math.floor((Date.now() - currentPageEnterTimeRef.current) / 1000)),
        screen_width: window.screen.width,
        screen_height: window.screen.height,
        referrer: document.referrer || '',
      }

      navigator.sendBeacon('/api/v1/visitor/track', JSON.stringify(data))
    }
    window.addEventListener('beforeunload', handleBeforeUnload)

    return () => {
      trackPageLeave()
      window.removeEventListener('popstate', handlePopstate)
      document.removeEventListener('visibilitychange', handleVisibilityChange)
      window.removeEventListener('beforeunload', handleBeforeUnload)
      if (heartbeatIntervalRef.current) {
        clearInterval(heartbeatIntervalRef.current)
      }
    }
  }, [sendTrack, trackPageEnter, trackPageLeave, sendHeartbeat])

  return {
    sessionId: sessionIdRef.current,
  }
}

export default useVisitorTracker
