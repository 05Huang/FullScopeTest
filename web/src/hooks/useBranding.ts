/**
 * 品牌配置 Hook
 *
 * 前端启动时获取品牌配置，动态应用到 CSS 变量和页面标题。
 */
import { useState, useEffect } from 'react'
import api from '@/services/api'

interface BrandingConfig {
  platform_name: string
  logo_url: string | null
  favicon_url: string | null
  primary_color: string
  login_background_url: string | null
  footer_text: string
  custom_css: string
}

const DEFAULT_BRANDING: BrandingConfig = {
  platform_name: 'FullScopeTest',
  logo_url: null,
  favicon_url: null,
  primary_color: '#5FA59B',
  login_background_url: null,
  footer_text: '',
  custom_css: '',
}

export function useBranding() {
  const [branding, setBranding] = useState<BrandingConfig>(DEFAULT_BRANDING)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetchBranding = async () => {
      try {
        const res = await api.get('/branding/config')
        if (res.data?.code === 200 && res.data?.data) {
          const config = res.data.data as BrandingConfig
          setBranding(config)
          applyBranding(config)
        }
      } catch {
        // 品牌配置获取失败时使用默认值
      } finally {
        setLoading(false)
      }
    }

    fetchBranding()
  }, [])

  return { branding, loading }
}

/**
 * 将品牌配置应用到 CSS 变量和页面元素
 */
function applyBranding(config: BrandingConfig) {
  // 应用主色调到 CSS 变量
  if (config.primary_color) {
    document.documentElement.style.setProperty('--fst-primary', config.primary_color)
  }

  // 更新页面标题
  if (config.platform_name) {
    document.title = config.platform_name
  }

  // 更新 Favicon
  if (config.favicon_url) {
    let link = document.querySelector("link[rel~='icon']") as HTMLLinkElement
    if (!link) {
      link = document.createElement('link')
      link.rel = 'icon'
      document.head.appendChild(link)
    }
    link.href = config.favicon_url
  }

  // 注入自定义 CSS
  if (config.custom_css) {
    let style = document.getElementById('fst-branding-css')
    if (!style) {
      style = document.createElement('style')
      style.id = 'fst-branding-css'
      document.head.appendChild(style)
    }
    style.textContent = config.custom_css
  }
}
