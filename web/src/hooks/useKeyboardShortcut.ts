/**
 * 快捷键 Hook
 *
 * 注册全局或局部键盘快捷键，支持 Ctrl/Cmd + 按键组合。
 * 输入框/编辑器内不触发全局快捷键。
 *
 * 用法：
 *   useKeyboardShortcut('k', () => openSearch(), { ctrl: true })
 *   useKeyboardShortcut('Enter', () => sendRequest(), { ctrl: true })
 */
import { useEffect, useCallback } from 'react'

interface ShortcutOptions {
  /** 是否需要 Ctrl/Cmd 键 */
  ctrl?: boolean
  /** 是否需要 Shift 键 */
  shift?: boolean
  /** 是否需要 Alt 键 */
  alt?: boolean
  /** 是否在输入框中也触发（默认 false） */
  enableInInput?: boolean
}

/**
 * 判断事件目标是否为可编辑元素
 */
const isEditableElement = (target: EventTarget | null): boolean => {
  if (!target || !(target instanceof HTMLElement)) return false
  const tag = target.tagName.toLowerCase()
  if (tag === 'input' || tag === 'textarea' || tag === 'select') return true
  if (target.isContentEditable) return true
  // Monaco Editor
  if (target.closest('.monaco-editor')) return true
  return false
}

/**
 * 注册键盘快捷键
 * @param key 按键（不区分大小写）
 * @param callback 触发回调
 * @param options 快捷键选项
 */
export function useKeyboardShortcut(
  key: string,
  callback: () => void,
  options: ShortcutOptions = {}
) {
  const {
    ctrl = false,
    shift = false,
    alt = false,
    enableInInput = false,
  } = options

  const handleKeyDown = useCallback(
    (event: KeyboardEvent) => {
      // 输入框内不触发（除非显式允许）
      if (!enableInInput && isEditableElement(event.target)) return

      const isCtrlOrMeta = event.ctrlKey || event.metaKey
      const keyMatch = event.key.toLowerCase() === key.toLowerCase()
      const ctrlMatch = ctrl ? isCtrlOrMeta : !isCtrlOrMeta
      const shiftMatch = shift ? event.shiftKey : !event.shiftKey
      const altMatch = alt ? event.altKey : !event.altKey

      // 对于需要 Ctrl 的快捷键，不要求非 Ctrl 状态
      if (keyMatch && (!ctrl || isCtrlOrMeta) && (!shift || event.shiftKey) && (!alt || event.altKey)) {
        event.preventDefault()
        event.stopPropagation()
        callback()
      }
    },
    [key, callback, ctrl, shift, alt, enableInInput]
  )

  useEffect(() => {
    window.addEventListener('keydown', handleKeyDown)
    return () => window.removeEventListener('keydown', handleKeyDown)
  }, [handleKeyDown])
}

export default useKeyboardShortcut
