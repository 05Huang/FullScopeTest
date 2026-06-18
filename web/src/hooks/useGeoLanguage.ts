import { useEffect, useState } from 'react'
import i18n from 'i18next'
import { detectRegion } from '@/services/geoService'

const STORAGE_KEY = 'fst-language'
const DISMISS_KEY = 'fst-geo-dismiss'
const isDEV = (import.meta as any).env?.DEV === true

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
    const env = (import.meta as any).env || {}

    // 显式禁用时跳过
    if (env.VITE_ENABLE_GEO === 'false') {
      if (isDEV) console.log('[GeoLanguage] Skipped — VITE_ENABLE_GEO=false')
      setLoading(false)
      return
    }

    // 生产环境且未显式启用时跳过
    const isProduction = env.MODE === 'production' && env.VITE_DEPLOY_ENV !== 'demo'
    if (isProduction) {
      if (isDEV) console.log('[GeoLanguage] Skipped — production')
      setLoading(false)
      return
    }

    // 用户已手动选择过语言，不再提示
    const savedLang = localStorage.getItem(STORAGE_KEY)
    if (savedLang) {
      if (isDEV) console.log('[GeoLanguage] Skipped — user already selected:', savedLang)
      setLoading(false)
      return
    }

    // 用户已关闭过提示
    const dismissed = localStorage.getItem(DISMISS_KEY)
    if (dismissed) {
      if (isDEV) console.log('[GeoLanguage] Skipped — dismissed')
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
