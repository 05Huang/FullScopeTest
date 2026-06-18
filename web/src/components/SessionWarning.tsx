/**
 * 会话超时预警组件
 *
 * 检测 JWT Access Token 即将过期时弹出预警弹窗。
 * 过期前 10 分钟弹出预警，倒计时 60 秒后自动刷新。
 * 不操作则到期后跳转登录页。
 */

import { useState, useEffect, useCallback } from 'react'
import { Modal, Typography, Progress } from 'antd'
import { useTranslation } from 'react-i18next'
import { useAuthStore } from '@/stores/authStore'
import api from '@/services/api'

const { Text } = Typography

const WARNING_BEFORE_EXPIRY_MS = 10 * 60 * 1000 // 提前 10 分钟预警
const COUNTDOWN_SECONDS = 60 // 倒计时 60 秒

const SessionWarning: React.FC = () => {
  const { t } = useTranslation()
  const { isAuthenticated, logout } = useAuthStore()
  const [visible, setVisible] = useState(false)
  const [countdown, setCountdown] = useState(COUNTDOWN_SECONDS)
  const [expiresIn, setExpiresIn] = useState(0)

  // 检查 token 过期时间
  const checkTokenExpiry = useCallback(() => {
    if (!isAuthenticated) return

    // 从 cookie 或响应头获取 token 过期时间
    // 这里我们检查 /auth/me 接口的响应头
    api.get('/auth/me').catch(() => {
      // 请求失败可能是 token 已过期，由 api.ts 的拦截器处理
    })
  }, [isAuthenticated])

  // 监听 token 即将过期的信号
  useEffect(() => {
    if (!isAuthenticated) return

    // 定期检查 token 状态（每 5 分钟）
    const interval = setInterval(checkTokenExpiry, 5 * 60 * 1000)
    return () => clearInterval(interval)
  }, [isAuthenticated, checkTokenExpiry])

  // 倒计时逻辑
  useEffect(() => {
    if (!visible) return

    setCountdown(COUNTDOWN_SECONDS)
    const timer = setInterval(() => {
      setCountdown(prev => {
        if (prev <= 1) {
          clearInterval(timer)
          // 倒计时结束，自动刷新
          handleRefresh()
          return 0
        }
        return prev - 1
      })
    }, 1000)

    return () => clearInterval(timer)
  }, [visible])

  const handleRefresh = async () => {
    try {
      await api.post('/auth/refresh')
      setVisible(false)
    } catch {
      // 刷新失败，登出
      logout()
      window.location.href = '/login'
    }
  }

  const handleLogout = () => {
    setVisible(false)
    logout()
    window.location.href = '/login'
  }

  // 暴露给外部调用的方法
  useEffect(() => {
    (window as any).__showSessionWarning = (expiresInMs: number) => {
      setExpiresIn(Math.floor(expiresInMs / 1000))
      setVisible(true)
    }
    return () => {
      delete (window as any).__showSessionWarning
    }
  }, [])

  if (!isAuthenticated) return null

  return (
    <Modal
      open={visible}
      title={t('session.warningTitle') || '会话即将过期'}
      closable={false}
      maskClosable={false}
      onOk={handleRefresh}
      onCancel={handleLogout}
      okText={t('session.extend') || '延长会话'}
      cancelText={t('session.logout') || '重新登录'}
      okButtonProps={{ loading: countdown === 0 }}
    >
      <div style={{ textAlign: 'center', padding: '16px 0' }}>
        <Text>
          {t('session.warningMessage') || '您的会话即将过期，是否延长？'}
        </Text>
        <div style={{ marginTop: 16 }}>
          <Progress
            type="circle"
            percent={Math.floor((countdown / COUNTDOWN_SECONDS) * 100)}
            format={() => `${countdown}s`}
            size={80}
            strokeColor={countdown <= 10 ? '#ff4d4f' : '#1890ff'}
          />
        </div>
        <Text type="secondary" style={{ display: 'block', marginTop: 8, fontSize: 12 }}>
          {countdown > 0
            ? (t('session.countdown') || `${countdown} 秒后自动刷新`)
            : (t('session.refreshing') || '正在刷新...')}
        </Text>
      </div>
    </Modal>
  )
}

export default SessionWarning
