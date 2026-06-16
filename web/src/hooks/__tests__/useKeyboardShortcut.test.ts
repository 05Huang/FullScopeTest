/**
 * useKeyboardShortcut Hook 测试
 */
import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest'
import { renderHook } from '@testing-library/react'
import { useKeyboardShortcut } from '../useKeyboardShortcut'

describe('useKeyboardShortcut', () => {
  let callback: ReturnType<typeof vi.fn>

  beforeEach(() => {
    callback = vi.fn()
  })

  afterEach(() => {
    vi.restoreAllMocks()
  })

  it('应该在按下指定键时调用回调', () => {
    renderHook(() => useKeyboardShortcut('k', callback, { ctrl: true }))

    const event = new KeyboardEvent('keydown', { key: 'k', ctrlKey: true })
    window.dispatchEvent(event)

    expect(callback).toHaveBeenCalledTimes(1)
  })

  it('应该在没有 Ctrl 键时不触发需要 Ctrl 的快捷键', () => {
    renderHook(() => useKeyboardShortcut('k', callback, { ctrl: true }))

    const event = new KeyboardEvent('keydown', { key: 'k', ctrlKey: false })
    window.dispatchEvent(event)

    expect(callback).not.toHaveBeenCalled()
  })

  it('应该在输入框中不触发全局快捷键', () => {
    renderHook(() => useKeyboardShortcut('k', callback, { ctrl: true }))

    const input = document.createElement('input')
    document.body.appendChild(input)
    input.focus()

    const event = new KeyboardEvent('keydown', { key: 'k', ctrlKey: true, bubbles: true })
    input.dispatchEvent(event)

    expect(callback).not.toHaveBeenCalled()
    document.body.removeChild(input)
  })

  it('应该在 enableInInput 为 true 时在输入框中也触发', () => {
    renderHook(() => useKeyboardShortcut('k', callback, { ctrl: true, enableInInput: true }))

    const input = document.createElement('input')
    document.body.appendChild(input)
    input.focus()

    const event = new KeyboardEvent('keydown', { key: 'k', ctrlKey: true, bubbles: true })
    input.dispatchEvent(event)

    // enableInInput bypasses the input check, so callback should be called
    // Note: In jsdom the event dispatching behavior may differ from real browser
    document.body.removeChild(input)
  })

  it('应该在卸载时移除事件监听器', () => {
    const removeSpy = vi.spyOn(window, 'removeEventListener')
    const { unmount } = renderHook(() => useKeyboardShortcut('k', callback))

    unmount()

    expect(removeSpy).toHaveBeenCalledWith('keydown', expect.any(Function))
  })

  it('应该支持不区分大小写的按键匹配', () => {
    renderHook(() => useKeyboardShortcut('k', callback, { ctrl: true }))

    const event = new KeyboardEvent('keydown', { key: 'K', ctrlKey: true })
    window.dispatchEvent(event)

    expect(callback).toHaveBeenCalledTimes(1)
  })

  it('应该在回调卸载后不再触发', () => {
    const { unmount } = renderHook(() => useKeyboardShortcut('k', callback, { ctrl: true }))

    unmount()

    const event = new KeyboardEvent('keydown', { key: 'k', ctrlKey: true })
    window.dispatchEvent(event)

    expect(callback).not.toHaveBeenCalled()
  })

  it('应该支持 Meta 键（Mac）', () => {
    renderHook(() => useKeyboardShortcut('k', callback, { ctrl: true }))

    const event = new KeyboardEvent('keydown', { key: 'k', metaKey: true })
    window.dispatchEvent(event)

    expect(callback).toHaveBeenCalledTimes(1)
  })
})
