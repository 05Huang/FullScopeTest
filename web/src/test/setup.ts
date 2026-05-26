import '@testing-library/jest-dom'
import { vi } from 'vitest'

// Mock window.matchMedia for antd
Object.defineProperty(window, 'matchMedia', {
  writable: true,
  value: vi.fn().mockImplementation((query) => ({
    matches: false,
    media: query,
    onchange: null,
    addListener: vi.fn(), // deprecated
    removeListener: vi.fn(), // deprecated
    addEventListener: vi.fn(),
    removeEventListener: vi.fn(),
    dispatchEvent: vi.fn(),
  })),
})

// Mock window.getComputedStyle
window.getComputedStyle = () =>
  ({
    getPropertyValue: () => '',
  }) as any

// Mock antd message/notification/modal static methods
// These use antd's internal static function API which isn't available in jsdom
vi.mock('antd', async (importOriginal) => {
  const antd = await importOriginal<typeof import('antd')>()
  const noop = vi.fn()
  noop.success = vi.fn()
  noop.error = vi.fn()
  noop.warning = vi.fn()
  noop.info = vi.fn()
  noop.loading = vi.fn()
  noop.open = vi.fn()
  noop.config = vi.fn()
  noop.destroy = vi.fn()

  return {
    ...antd,
    message: noop,
    notification: {
      ...antd.notification,
      open: vi.fn(),
      success: vi.fn(),
      error: vi.fn(),
      info: vi.fn(),
      warning: vi.fn(),
    },
  }
})
