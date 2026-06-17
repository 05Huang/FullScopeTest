import { useEffect, useState } from 'react'
import i18n from 'i18next'
import { detectRegion } from '@/services/geoService'

const STORAGE_KEY = 'fst-language'
const DISMISS_KEY = 'fst-geo-dismiss'

/**
 * 演示系统智能语言检测 Hook
 *
 * 检测用户 IP 所在地区，非中国用户自动提示切换英文。
 * 仅在演示模式（非生产环境）下生效。
 * 用户关闭提示后不再显示（localStorage 记录）。
 */
export function useGeoLanguage() {
  const [showPrompt, setShowPrompt] = useState(false)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    // 仅在演示/非生产环境触发
    const isProduction = (import.meta as any).env?.MODE === 'production' || (import.meta as any).env?.VITE_DEPLOY_ENV === 'prod'
    if (isProduction) {
      setLoading(false)
      return
    }

    // 用户已手动选择过语言，不再提示
    if (localStorage.getItem(STORAGE_KEY)) {
      setLoading(false)
      return
    }

    // 用户已关闭过提示
    if (localStorage.getItem(DISMISS_KEY)) {
      setLoading(false)
      return
    }

    detectRegion().then((geo) => {
      if (geo && !geo.is_china) {
        setShowPrompt(true)
      }
      setLoading(false)
    }).catch(() => {
      setLoading(false)
    })
  }, [])

  const switchToEnglish = () => {
    i18n.changeLanguage('en')
    localStorage.setItem(STORAGE_KEY, 'en')
    setShowPrompt(false)
  }

  const dismiss = () => {
    localStorage.setItem(DISMISS_KEY, '1')
    setShowPrompt(false)
  }

  return { showPrompt, loading, switchToEnglish, dismiss }
}
