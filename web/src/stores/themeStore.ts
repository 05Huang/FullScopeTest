/**
 * 主题状态管理
 *
 * 管理亮色/暗色主题切换，支持跟随系统设置。
 * 主题偏好持久化到 localStorage。
 */
import { create } from 'zustand'

type ThemeMode = 'light' | 'dark' | 'system'

interface ThemeState {
  /** 当前实际应用的主题（light 或 dark） */
  resolvedTheme: 'light' | 'dark'
  /** 用户选择的主题模式 */
  mode: ThemeMode
  /** 设置主题模式 */
  setMode: (mode: ThemeMode) => void
  /** 切换亮暗 */
  toggle: () => void
  /** 初始化主题 */
  init: () => void
}

const STORAGE_KEY = 'fst-theme'

/** 获取系统主题偏好 */
const getSystemTheme = (): 'light' | 'dark' => {
  if (typeof window === 'undefined') return 'light'
  return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light'
}

/** 解析实际主题 */
const resolveTheme = (mode: ThemeMode): 'light' | 'dark' => {
  if (mode === 'system') return getSystemTheme()
  return mode
}

/** 应用主题到 DOM */
const applyTheme = (theme: 'light' | 'dark') => {
  document.documentElement.setAttribute('data-theme', theme)
  if (theme === 'dark') {
    document.documentElement.classList.add('dark')
  } else {
    document.documentElement.classList.remove('dark')
  }
}

export const useThemeStore = create<ThemeState>((set, get) => ({
  resolvedTheme: 'light',
  mode: 'system',

  setMode: (mode: ThemeMode) => {
    const resolved = resolveTheme(mode)
    localStorage.setItem(STORAGE_KEY, mode)
    applyTheme(resolved)
    set({ mode, resolvedTheme: resolved })
  },

  toggle: () => {
    const current = get().resolvedTheme
    const next = current === 'light' ? 'dark' : 'light'
    get().setMode(next)
  },

  init: () => {
    const stored = localStorage.getItem(STORAGE_KEY) as ThemeMode | null
    const mode = stored || 'system'
    const resolved = resolveTheme(mode)
    applyTheme(resolved)
    set({ mode, resolvedTheme: resolved })

    // 监听系统主题变化
    const mq = window.matchMedia('(prefers-color-scheme: dark)')
    mq.addEventListener('change', () => {
      if (get().mode === 'system') {
        const resolvedNow = getSystemTheme()
        applyTheme(resolvedNow)
        set({ resolvedTheme: resolvedNow })
      }
    })
  },
}))

export default useThemeStore
