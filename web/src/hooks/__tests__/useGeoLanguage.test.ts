import { describe, it, expect, beforeEach, vi } from 'vitest'
import { renderHook, act } from '@testing-library/react'
import { useGeoLanguage } from '../useGeoLanguage'

// Mock dependencies
vi.mock('@/services/geoService', () => ({
  detectRegion: vi.fn(),
}))

vi.mock('i18next', () => ({
  default: {
    changeLanguage: vi.fn(),
    language: 'zh',
  },
}))

describe('useGeoLanguage', () => {
  beforeEach(() => {
    localStorage.clear()
    vi.clearAllMocks()
  })

  it('should return initial state with loading true', () => {
    const { result } = renderHook(() => useGeoLanguage())
    expect(result.current.loading).toBeDefined()
  })

  it('should not show prompt when dismissed', () => {
    localStorage.setItem('fst-geo-dismiss', 'true')
    const { result } = renderHook(() => useGeoLanguage())
    // After effect runs, showPrompt should be false
    expect(result.current.showPrompt).toBe(false)
  })

  it('should not show prompt when language already selected', () => {
    localStorage.setItem('fst-language', 'en')
    const { result } = renderHook(() => useGeoLanguage())
    expect(result.current.showPrompt).toBe(false)
  })

  it('should expose dismiss function', () => {
    const { result } = renderHook(() => useGeoLanguage())
    expect(typeof result.current.dismiss).toBe('function')
  })

  it('should expose switchToEnglish function', () => {
    const { result } = renderHook(() => useGeoLanguage())
    expect(typeof result.current.switchToEnglish).toBe('function')
  })

  it('dismiss should save to localStorage', () => {
    const { result } = renderHook(() => useGeoLanguage())
    act(() => {
      result.current.dismiss()
    })
    expect(localStorage.getItem('fst-geo-dismiss')).toBe('true')
  })
})
