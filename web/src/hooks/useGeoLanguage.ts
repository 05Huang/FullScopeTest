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
    console.log('[GeoLanguage] Initializing...')

    // 仅在演示/非生产环境触发
    const isProduction = (import.meta as any).env?.MODE === 'production' || (import.meta as any).env?.VITE_DEPLOY_ENV === 'prod'
    console.log('[GeoLanguage] isProduction:', isProduction, '| MODE:', (import.meta as any).env?.MODE, '| VITE_DEPLOY_ENV:', (import.meta as any).env?.VITE_DEPLOY_ENV)
    if (isProduction) {
      console.log('[GeoLanguage] Skipped — production environment')
      setLoading(false)
      return
    }

    // 用户已手动选择过语言，不再提示
    const savedLang = localStorage.getItem(STORAGE_KEY)
    if (savedLang) {
      console.log('[GeoLanguage] Skipped — user already selected language:', savedLang)
      setLoading(false)
      return
    }

    // 用户已关闭过提示
    const dismissed = localStorage.getItem(DISMISS_KEY)
    if (dismissed) {
      console.log('[GeoLanguage] Skipped — user previously dismissed prompt')
      setLoading(false)
      return
    }

    console.log('[GeoLanguage] Calling detectRegion API...')
    detectRegion().then((geo) => {
      console.log('[GeoLanguage] API response:', geo)
      if (geo && !geo.is_china) {
        console.log('[GeoLanguage] ✅ Non-China user detected → showing prompt')
        setShowPrompt(true)
      } else {
        console.log('[GeoLanguage] ℹ️ China user or no data → no prompt')
      }
      setLoading(false)
    }).catch((err) => {
      console.error('[GeoLanguage] ❌ API error:', err)
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
