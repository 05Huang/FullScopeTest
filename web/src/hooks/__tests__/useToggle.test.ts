import { describe, it, expect } from 'vitest'
import { renderHook, act } from '@testing-library/react'
import { useToggle } from '../useToggle'

describe('useToggle', () => {
  it('should default to false', () => {
    const { result } = renderHook(() => useToggle())
    const [value] = result.current
    expect(value).toBe(false)
  })

  it('should accept initial value', () => {
    const { result } = renderHook(() => useToggle(true))
    const [value] = result.current
    expect(value).toBe(true)
  })

  it('should toggle value', () => {
    const { result } = renderHook(() => useToggle())

    act(() => {
      const [, toggle] = result.current
      toggle()
    })

    expect(result.current[0]).toBe(true)

    act(() => {
      const [, toggle] = result.current
      toggle()
    })

    expect(result.current[0]).toBe(false)
  })

  it('should set specific value', () => {
    const { result } = renderHook(() => useToggle())

    act(() => {
      const [, , setValue] = result.current
      setValue(true)
    })

    expect(result.current[0]).toBe(true)

    act(() => {
      const [, , setValue] = result.current
      setValue(false)
    })

    expect(result.current[0]).toBe(false)
  })
})
