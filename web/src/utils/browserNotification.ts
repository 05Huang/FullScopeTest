/**
 * 浏览器通知工具
 *
 * 提供浏览器原生通知功能，用于测试完成提醒等场景。
 * 首次使用时请求 Notification.requestPermission() 权限。
 */

const SETTINGS_KEY = 'fst-browser-notifications-enabled'

/**
 * 检查浏览器是否支持通知
 */
export function isNotificationSupported(): boolean {
  return 'Notification' in window
}

/**
 * 获取通知权限状态
 */
export function getNotificationPermission(): NotificationPermission | 'unsupported' {
  if (!isNotificationSupported()) return 'unsupported'
  return Notification.permission
}

/**
 * 请求通知权限
 */
export async function requestNotificationPermission(): Promise<NotificationPermission> {
  if (!isNotificationSupported()) {
    return 'denied'
  }

  if (Notification.permission === 'granted') {
    return 'granted'
  }

  if (Notification.permission !== 'denied') {
    return await Notification.requestPermission()
  }

  return 'denied'
}

/**
 * 检查用户是否启用了浏览器通知
 */
export function isBrowserNotificationEnabled(): boolean {
  const stored = localStorage.getItem(SETTINGS_KEY)
  if (stored === null) return true // 默认启用
  return stored === 'true'
}

/**
 * 设置浏览器通知开关
 */
export function setBrowserNotificationEnabled(enabled: boolean): void {
  localStorage.setItem(SETTINGS_KEY, String(enabled))
}

/**
 * 发送浏览器通知
 *
 * @param title 通知标题
 * @param options 通知选项
 * @param onClick 点击通知时的回调
 */
export async function sendBrowserNotification(
  title: string,
  options?: NotificationOptions,
  onClick?: () => void,
): Promise<void> {
  // 检查用户是否启用了通知
  if (!isBrowserNotificationEnabled()) return

  // 检查浏览器支持
  if (!isNotificationSupported()) return

  // 请求权限（如果尚未授权）
  const permission = await requestNotificationPermission()
  if (permission !== 'granted') return

  const notification = new Notification(title, {
    icon: '/logo-icon.webp',
    badge: '/logo-icon.webp',
    ...options,
  })

  if (onClick) {
    notification.onclick = () => {
      window.focus()
      onClick()
      notification.close()
    }
  }

  // 5 秒后自动关闭
  setTimeout(() => notification.close(), 5000)
}

/**
 * 发送测试完成通知
 */
export async function sendTestCompleteNotification(
  testName: string,
  passRate: number,
  passed: number,
  total: number,
  reportId?: number,
): Promise<void> {
  await sendBrowserNotification(
    `测试完成：${testName}`,
    {
      body: `通过率 ${passRate}% (${passed}/${total})`,
      tag: `test-complete-${reportId || Date.now()}`,
    },
    () => {
      if (reportId) {
        window.location.href = `/reports?run=${reportId}`
      }
    },
  )
}
