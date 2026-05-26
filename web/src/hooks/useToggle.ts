import { useState, useCallback } from 'react'

/**
 * 布尔值切换 Hook
 */
export function useToggle(
  initialValue: boolean = false
): [boolean, () => void, (value: boolean) => void] {
  const [value, setValue] = useState(initialValue)

  const toggle = useCallback(() => {
    setValue((prev) => !prev)
  }, [])

  return [value, toggle, setValue]
}
