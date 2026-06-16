/**
 * ThemeStore 测试
 */
import { describe, it, expect, beforeEach, vi } from 'vitest'
import { useThemeStore } from '../themeStore'

describe('themeStore', () => {
  beforeEach(() => {
    // 重置 store 状态
    useThemeStore.setState({ mode: 'system', resolvedTheme: 'light' })
    localStorage.clear()
    document.documentElement.removeAttribute('data-theme')
    document.documentElement.classList.remove('dark')
  })

  it('应该有默认状态', () => {
    const state = useThemeStore.getState()
    expect(state.mode).toBe('system')
    expect(state.resolvedTheme).toBe('light')
  })

  it('应该能设置亮色模式', () => {
    useThemeStore.getState().setMode('light')
    const state = useThemeStore.getState()
    expect(state.mode).toBe('light')
    expect(state.resolvedTheme).toBe('light')
    expect(localStorage.getItem('fst-theme')).toBe('light')
  })

  it('应该能设置暗色模式', () => {
    useThemeStore.getState().setMode('dark')
    const state = useThemeStore.getState()
    expect(state.mode).toBe('dark')
    expect(state.resolvedTheme).toBe('dark')
    expect(localStorage.getItem('fst-theme')).toBe('dark')
    expect(document.documentElement.getAttribute('data-theme')).toBe('dark')
    expect(document.documentElement.classList.contains('dark')).toBe(true)
  })

  it('应该能切换主题', () => {
    useThemeStore.setState({ resolvedTheme: 'light' })
    useThemeStore.getState().toggle()
    expect(useThemeStore.getState().resolvedTheme).toBe('dark')

    useThemeStore.getState().toggle()
    expect(useThemeStore.getState().resolvedTheme).toBe('light')
  })

  it('应该能从 localStorage 读取主题偏好', () => {
    localStorage.setItem('fst-theme', 'dark')
    useThemeStore.getState().init()
    expect(useThemeStore.getState().mode).toBe('dark')
    expect(useThemeStore.getState().resolvedTheme).toBe('dark')
  })

  it('应该持久化主题到 localStorage', () => {
    useThemeStore.getState().setMode('dark')
    expect(localStorage.getItem('fst-theme')).toBe('dark')

    useThemeStore.getState().setMode('light')
    expect(localStorage.getItem('fst-theme')).toBe('light')
  })
})
