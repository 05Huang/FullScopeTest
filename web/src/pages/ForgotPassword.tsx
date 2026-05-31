import { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { Form, Input, Button, Typography, message, Result } from 'antd'
import { useTranslation } from 'react-i18next'
import { authService } from '@/services/authService'

const { Title, Text } = Typography

const IconMail = ({ className }: { className?: string }) => (
  <svg viewBox="0 0 24 24" fill="none" className={className} aria-hidden="true">
    <path
      d="M5.5 7.6h13c.9 0 1.6.7 1.6 1.6v8.9c0 .9-.7 1.6-1.6 1.6h-13c-.9 0-1.6-.7-1.6-1.6V9.2c0-.9.7-1.6 1.6-1.6Z"
      stroke="currentColor"
      strokeWidth="1.6"
      strokeLinejoin="round"
    />
    <path
      d="m5.9 9 6.1 4.7a1.6 1.6 0 0 0 2 0L20.1 9"
      stroke="currentColor"
      strokeWidth="1.6"
      strokeLinecap="round"
      strokeLinejoin="round"
    />
  </svg>
)

const BrandMark = () => (
  <div className="fst-auth-brand" aria-hidden="true">
    <svg viewBox="0 0 64 64" className="fst-auth-brand-svg">
      <defs>
        <linearGradient id="fstBrandG" x1="10" y1="8" x2="56" y2="56" gradientUnits="userSpaceOnUse">
          <stop offset="0" stopColor="#5FA59B" />
          <stop offset="0.6" stopColor="#3D6E66" />
          <stop offset="1" stopColor="#D7B56D" />
        </linearGradient>
      </defs>
      <path
        d="M18 16h28c1.7 0 3 1.3 3 3v7c0 1.7-1.3 3-3 3H25.2v6.2H42c1.7 0 3 1.3 3 3v7c0 1.7-1.3 3-3 3H18c-1.7 0-3-1.3-3-3V19c0-1.7 1.3-3 3-3Z"
        fill="url(#fstBrandG)"
      />
      <path d="M22 23h24" stroke="rgba(255,255,255,0.55)" strokeWidth="2" strokeLinecap="round" />
      <path d="M22 45h18" stroke="rgba(255,255,255,0.38)" strokeWidth="2" strokeLinecap="round" />
    </svg>
  </div>
)

const ForgotPassword = () => {
  const { t } = useTranslation()
  const [loading, setLoading] = useState(false)
  const [sent, setSent] = useState(false)
  const [resetToken, setResetToken] = useState('')
  const navigate = useNavigate()

  const onFinish = async (values: { email: string }) => {
    setLoading(true)
    try {
      const response = await authService.forgotPassword(values.email)
      if (response.data?.reset_token) {
        setResetToken(response.data.reset_token)
      }
      setSent(true)
      message.success(t('forgotPassword.success'))
    } catch (error: any) {
      message.error(error.response?.data?.message || t('forgotPassword.failed'))
    } finally {
      setLoading(false)
    }
  }

  if (sent) {
    return (
      <div className="fst-auth-root">
        <div className="fst-auth-bg" aria-hidden="true">
          <div className="fst-auth-bg-blob fst-auth-bg-blob-a" />
          <div className="fst-auth-bg-blob fst-auth-bg-blob-b" />
          <div className="fst-auth-bg-grid" />
        </div>
        <div className="fst-auth-shell">
          <div className="fst-auth-card" style={{ maxWidth: 480 }}>
            <Result
              status="success"
              title={t('forgotPassword.sentTitle')}
              subTitle={
                <div>
                  <Text>{t('forgotPassword.sentMessage')}</Text>
                  {resetToken && (
                    <div style={{ marginTop: 16 }}>
                      <Text type="secondary" style={{ fontSize: 12 }}>
                        {t('forgotPassword.tokenHint')}
                      </Text>
                      <Input.TextArea
                        value={resetToken}
                        readOnly
                        autoSize
                        style={{ marginTop: 8, fontFamily: 'monospace', fontSize: 12 }}
                        onClick={(e) => (e.target as HTMLTextAreaElement).select()}
                      />
                    </div>
                  )}
                </div>
              }
              extra={
                <Button type="primary" onClick={() => navigate('/reset-password', { state: { token: resetToken } })}>
                  {t('forgotPassword.goReset')}
                </Button>
              }
            />
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="fst-auth-root">
      <div className="fst-auth-bg" aria-hidden="true">
        <div className="fst-auth-bg-blob fst-auth-bg-blob-a" />
        <div className="fst-auth-bg-blob fst-auth-bg-blob-b" />
        <div className="fst-auth-bg-grid" />
      </div>
      <div className="fst-auth-shell">
        <div className="fst-auth-card" style={{ maxWidth: 480 }}>
          <div className="fst-auth-header">
            <BrandMark />
            <div className="fst-auth-heading">
              <Title level={3} className="fst-auth-title">
                {t('forgotPassword.title')}
              </Title>
              <Text className="fst-auth-subtitle">{t('forgotPassword.subtitle')}</Text>
            </div>
          </div>

          <Form onFinish={onFinish} autoComplete="off" size="large" layout="vertical">
            <Form.Item
              name="email"
              rules={[
                { required: true, message: t('login.validation.emailRequired') },
                { type: 'email', message: t('login.validation.emailInvalid') },
              ]}
            >
              <Input
                className="fst-auth-input"
                prefix={<IconMail className="fst-auth-icon" />}
                placeholder={t('forgotPassword.emailPlaceholder')}
                aria-label={t('forgotPassword.emailPlaceholder')}
              />
            </Form.Item>

            <Form.Item style={{ marginBottom: 14 }}>
              <Button htmlType="submit" loading={loading} block className="fst-auth-submit">
                {t('forgotPassword.submitBtn')}
              </Button>
            </Form.Item>
          </Form>

          <div className="fst-auth-footer">
            <span className="fst-auth-footer-muted">{t('forgotPassword.rememberPassword')}</span>
            <Link to="/login" className="fst-auth-link">
              {t('login.goLogin')}
            </Link>
          </div>
        </div>
      </div>
    </div>
  )
}

export default ForgotPassword
