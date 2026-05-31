import { useState } from 'react'
import { useNavigate, useLocation, Link } from 'react-router-dom'
import { Form, Input, Button, Typography, message, Result } from 'antd'
import { useTranslation } from 'react-i18next'
import { authService } from '@/services/authService'

const { Title, Text } = Typography

const IconLock = ({ className }: { className?: string }) => (
  <svg viewBox="0 0 24 24" fill="none" className={className} aria-hidden="true">
    <path
      d="M7.5 11V8.6a4.5 4.5 0 1 1 9 0V11"
      stroke="currentColor"
      strokeWidth="1.6"
      strokeLinecap="round"
    />
    <path
      d="M6.6 11h10.8c.9 0 1.6.7 1.6 1.6v6.9c0 .9-.7 1.6-1.6 1.6H6.6c-.9 0-1.6-.7-1.6-1.6v-6.9c0-.9.7-1.6 1.6-1.6Z"
      stroke="currentColor"
      strokeWidth="1.6"
      strokeLinejoin="round"
    />
    <path d="M12 15.1v2.2" stroke="currentColor" strokeWidth="1.6" strokeLinecap="round" />
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

interface ResetForm {
  token: string
  newPassword: string
  confirmPassword: string
}

const ResetPassword = () => {
  const { t } = useTranslation()
  const [loading, setLoading] = useState(false)
  const [success, setSuccess] = useState(false)
  const navigate = useNavigate()
  const location = useLocation()
  const initialToken = (location.state as { token?: string })?.token || ''

  const onFinish = async (values: ResetForm) => {
    setLoading(true)
    try {
      await authService.resetPassword(values.token, values.newPassword)
      setSuccess(true)
      message.success(t('resetPassword.success'))
    } catch (error: any) {
      message.error(error.response?.data?.message || t('resetPassword.failed'))
    } finally {
      setLoading(false)
    }
  }

  if (success) {
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
              title={t('resetPassword.successTitle')}
              subTitle={t('resetPassword.successMessage')}
              extra={
                <Button type="primary" onClick={() => navigate('/login')}>
                  {t('resetPassword.goLogin')}
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
                {t('resetPassword.title')}
              </Title>
              <Text className="fst-auth-subtitle">{t('resetPassword.subtitle')}</Text>
            </div>
          </div>

          <Form<ResetForm>
            onFinish={onFinish}
            autoComplete="off"
            size="large"
            layout="vertical"
            initialValues={{ token: initialToken }}
          >
            <Form.Item
              name="token"
              rules={[{ required: true, message: t('resetPassword.tokenRequired') }]}
              hidden={!!initialToken}
            >
              <Input
                className="fst-auth-input"
                placeholder={t('resetPassword.tokenPlaceholder')}
                aria-label={t('resetPassword.tokenPlaceholder')}
              />
            </Form.Item>

            <Form.Item
              name="newPassword"
              rules={[
                { required: true, message: t('login.validation.passwordRequired') },
                { min: 8, message: t('resetPassword.passwordMin') },
              ]}
            >
              <Input.Password
                className="fst-auth-input"
                prefix={<IconLock className="fst-auth-icon" />}
                placeholder={t('resetPassword.newPassword')}
                aria-label={t('resetPassword.newPassword')}
              />
            </Form.Item>

            <Form.Item
              name="confirmPassword"
              dependencies={['newPassword']}
              rules={[
                { required: true, message: t('login.validation.confirmRequired') },
                ({ getFieldValue }) => ({
                  validator(_, value) {
                    if (!value || getFieldValue('newPassword') === value) return Promise.resolve()
                    return Promise.reject(new Error(t('login.validation.passwordMismatch')))
                  },
                }),
              ]}
            >
              <Input.Password
                className="fst-auth-input"
                prefix={<IconLock className="fst-auth-icon" />}
                placeholder={t('resetPassword.confirmPassword')}
                aria-label={t('resetPassword.confirmPassword')}
              />
            </Form.Item>

            <Form.Item style={{ marginBottom: 14 }}>
              <Button htmlType="submit" loading={loading} block className="fst-auth-submit">
                {t('resetPassword.submitBtn')}
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

export default ResetPassword
