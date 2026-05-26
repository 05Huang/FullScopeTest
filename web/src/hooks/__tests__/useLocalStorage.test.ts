import { describe, it, expect, beforeEach } from 'vitest'
import { renderHook, act } from '@testing-library/react'
import { useLocalStorage } from '../useLocalStorage'

describe('useLocalStorage', () => {
  beforeEach(() => {
    localStorage.clear()
  })

  it('should return initial value when no stored value', () => {
    const { result } = renderHook(() => useLocalStorage('test-key', 'initial'))
    const [value] = result.current
    expect(value).toBe('initial')
  })

  it('should store and retrieve string value', () => {
    const { result } = renderHook(() => useLocalStorage('test-key', ''))

    act(() => {
      const [, setValue] = result.current
      setValue('new value')
    })

    const [value] = result.current
    expect(value).toBe('new value')
    expect(localStorage.getItem('test-key')).toBe('"new value"')
  })

  it('should store and retrieve object value', () => {
    const initialValue = { name: 'test', count: 0 }
    const { result } = renderHook(() => useLocalStorage('test-key', initialValue))

    act(() => {
      const [, setValue] = result.current
      setValue({ name: 'updated', count: 5 })
    })

    const [value] = result.current
    expect(value).toEqual({ name: 'updated', count: 5 })
  })

  it('should update value with function updater', () => {
    const { result } = renderHook(() => useLocalStorage('test-key', 0))

    act(() => {
      const [, setValue] = result.current
      setValue((prev) => prev + 1)
    })

    const [value] = result.current
    expect(value).toBe(1)
  })

  it('should remove value', () => {
    const { result } = renderHook(() => useLocalStorage('test-key', 'initial'))

    act(() => {
      const [, setValue] = result.current
      setValue('stored')
    })

    act(() => {
      const [, , removeValue] = result.current
      removeValue()
    })

    const [value] = result.current
    expect(value).toBe('initial')
    expect(localStorage.getItem('test-key')).toBeNull()
  })

  it('should read from existing localStorage', () => {
    localStorage.setItem('existing-key', '"stored value"')

    const { result } = renderHook(() => useLocalStorage('existing-key', 'default'))
    const [value] = result.current
    expect(value).toBe('stored value')
  })
})
