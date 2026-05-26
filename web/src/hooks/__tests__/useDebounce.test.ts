import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest'
import { renderHook, act } from '@testing-library/react'
import { useDebounce } from '../useDebounce'

describe('useDebounce', () => {
  beforeEach(() => {
    vi.useFakeTimers()
  })

  afterEach(() => {
    vi.useRealTimers()
  })

  it('should return initial value immediately', () => {
    const { result } = renderHook(() => useDebounce('initial', 500))
    expect(result.current).toBe('initial')
  })

  it('should debounce value update', () => {
    const { result, rerender } = renderHook(
      ({ value, delay }) => useDebounce(value, delay),
      { initialProps: { value: 'initial', delay: 500 } }
    )

    // Update value
    rerender({ value: 'updated', delay: 500 })

    // Value should not change yet
    expect(result.current).toBe('initial')

    // Fast forward time
    act(() => {
      vi.advanceTimersByTime(500)
    })

    // Now value should be updated
    expect(result.current).toBe('updated')
  })

  it('should reset timer on rapid updates', () => {
    const { result, rerender } = renderHook(
      ({ value, delay }) => useDebounce(value, delay),
      { initialProps: { value: 'initial', delay: 500 } }
    )

    // Rapid updates
    rerender({ value: 'update1', delay: 500 })
    act(() => {
      vi.advanceTimersByTime(200)
    })

    rerender({ value: 'update2', delay: 500 })
    act(() => {
      vi.advanceTimersByTime(200)
    })

    rerender({ value: 'final', delay: 500 })

    // Should still be initial
    expect(result.current).toBe('initial')

    // Complete the debounce
    act(() => {
      vi.advanceTimersByTime(500)
    })

    // Should be the final value
    expect(result.current).toBe('final')
  })

  it('should work with different delay values', () => {
    const { result, rerender } = renderHook(
      ({ value, delay }) => useDebounce(value, delay),
      { initialProps: { value: 'initial', delay: 1000 } }
    )

    rerender({ value: 'updated', delay: 1000 })

    act(() => {
      vi.advanceTimersByTime(1000)
    })

    expect(result.current).toBe('updated')
  })
})
