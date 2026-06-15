import { useEffect, useState, useRef } from 'react'
import { useLocation, useNavigate, Link } from 'react-router-dom'
import { Form, Input, Button, message } from 'antd'
import { useTranslation } from 'react-i18next'
import { authService } from '@/services/authService'
import { useAuthStore } from '@/stores/authStore'

interface LoginForm {
  username: string
  password: string
}

interface RegisterForm {
  username: string
  email: string
  password: string
  confirmPassword: string
}

type AuthMode = 'login' | 'register'

const getModeFromPathname = (pathname: string): AuthMode => {
  if (pathname.startsWith('/register')) return 'register'
  return 'login'
}

const IconUser = ({ className }: { className?: string }) => (
  <svg viewBox="0 0 24 24" fill="none" className={className} aria-hidden="true">
    <path
      d="M20 21a8 8 0 0 0-16 0"
      stroke="currentColor"
      strokeWidth="1.6"
      strokeLinecap="round"
    />
    <path
      d="M12 13a4.6 4.6 0 1 0 0-9.2A4.6 4.6 0 0 0 12 13Z"
      stroke="currentColor"
      strokeWidth="1.6"
      strokeLinecap="round"
    />
  </svg>
)

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
    <path
      d="M12 15.1v2.2"
      stroke="currentColor"
      strokeWidth="1.6"
      strokeLinecap="round"
    />
  </svg>
)

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

const EyeGlyph = ({ open }: { open: boolean }) => (
  <svg
    viewBox="0 0 24 24"
    fill="none"
    className={`fst-auth-eye ${open ? 'is-open' : 'is-closed'}`}
    aria-hidden="true"
  >
    <path
      d="M2.8 12s3.4-7 9.2-7 9.2 7 9.2 7-3.4 7-9.2 7-9.2-7-9.2-7Z"
      stroke="currentColor"
      strokeWidth="1.6"
      strokeLinejoin="round"
    />
    <path
      d="M12 15.3a3.3 3.3 0 1 0 0-6.6 3.3 3.3 0 0 0 0 6.6Z"
      stroke="currentColor"
      strokeWidth="1.6"
    />
    <path
      d="M5 19 19 5"
      stroke="currentColor"
      strokeWidth="1.6"
      strokeLinecap="round"
      className="fst-auth-eye-slash"
    />
  </svg>
)

/* ═══════════════════════════════════════════════════ */
/*                   LOGIN COMPONENT                   */
/* ═══════════════════════════════════════════════════ */

const Login = () => {
  const { t } = useTranslation()
  const [loginLoading, setLoginLoading] = useState(false)
  const [registerLoading, setRegisterLoading] = useState(false)
  const navigate = useNavigate()
  const location = useLocation()
  const { setAuth } = useAuthStore()
  const [loginForm] = Form.useForm<LoginForm>()
  const [registerForm] = Form.useForm<RegisterForm>()
  const [loginError, setLoginError] = useState<string | null>(null)
  const [loginPwdVisible, setLoginPwdVisible] = useState(false)
  const [registerPwdVisible, setRegisterPwdVisible] = useState(false)
  const [registerConfirmPwdVisible, setRegisterConfirmPwdVisible] = useState(false)

  const [mode, setMode] = useState<AuthMode>(() => getModeFromPathname(location.pathname))
  const autoFilled = useRef(false)

  useEffect(() => {
    setMode(getModeFromPathname(location.pathname))
  }, [location.pathname])

  const isRegister = mode === 'register'

  useEffect(() => {
    // 移动端检测
    const isMobile = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent)
    if (isMobile) {
      message.warning({
        content: <span style={{ color: '#3D6E66', fontWeight: 500 }}>{t('login.mobileHint')}</span>,
        icon: (
          <svg viewBox="0 0 24 24" fill="none" style={{ width: 18, height: 18, marginRight: 8, verticalAlign: '-4px', color: '#D7B56D' }} aria-hidden="true">
            <path d="M12 22C6.477 22 2 17.523 2 12S6.477 2 12 2s10 4.477 10 10-4.477 10-10 10zm-1-7v2h2v-2h-2zm0-8v6h2V7h-2z" fill="currentColor" />
          </svg>
        ),
        duration: 5
      })
    }

    if (!isRegister && !autoFilled.current) {
      loginForm.setFieldsValue({
        username: 'huangxuan',
        password: 'Test@123456'
      })

      message.open({
        content: <span style={{ color: '#3D6E66', fontWeight: 500 }}>{t('login.autoFillHint')}</span>,
        icon: (
          <svg viewBox="0 0 24 24" fill="none" style={{ width: 18, height: 18, marginRight: 8, verticalAlign: '-4px', color: '#5FA59B' }} aria-hidden="true">
            <path d="M20 21a8 8 0 0 0-16 0" stroke="currentColor" strokeWidth="1.6" strokeLinecap="round" />
            <path d="M12 13a4.6 4.6 0 1 0 0-9.2A4.6 4.6 0 0 0 12 13Z" stroke="currentColor" strokeWidth="1.6" strokeLinecap="round" />
          </svg>
        )
      })
      autoFilled.current = true
    }
  }, [isRegister, loginForm])

  const onLoginFinish = async (values: LoginForm) => {
    setLoginLoading(true)
    setLoginError(null)
    loginForm.setFields([
      { name: 'username', errors: [] },
      { name: 'password', errors: [] },
    ])
    try {
      const response = await authService.login(values.username, values.password)
      if (response.code !== 200) {
        throw new Error(response.message || t('login.loginFailed'))
      }
      const { user } = response.data
      setAuth(user || { id: 0, username: values.username, email: '' })
      message.success(t('login.loginSuccess'))
      navigate('/dashboard')
    } catch (error: any) {
      const msg = error?.response?.data?.message || error?.message || t('login.loginFailed')
      loginForm.setFields([{ name: 'password', errors: [msg] }])
      setLoginError(msg)
      message.error(msg)
    } finally {
      setLoginLoading(false)
    }
  }

  const onRegisterFinish = async (values: RegisterForm) => {
    setRegisterLoading(true)
    registerForm.setFields([
      { name: 'username', errors: [] },
      { name: 'email', errors: [] },
      { name: 'password', errors: [] },
      { name: 'confirmPassword', errors: [] },
    ])
    try {
      await authService.register(values.username, values.email, values.password)
      message.success(t('login.register.registerSuccess'))
      navigate('/login')
    } catch (error: any) {
      message.error(error.response?.data?.message || t('login.register.registerFailed'))
    } finally {
      setRegisterLoading(false)
    }
  }

  return (
    <div className="fst-login-split" role="main" aria-label={isRegister ? t('login.registerBtn') : t('login.loginBtn')}>
      {/* ─── Left: Product showcase image ─── */}
      <div className="fst-login-left">
        <img
          className="fst-login-left-img"
          src="/login-left.webp"
          alt="FullScopeTest Dashboard"
          draggable={false}
        />
      </div>

      {/* ─── Right: Login form ─── */}
      <div className="fst-login-right">
        <div className="fst-login-right-inner">
          {/* Logo + brand */}
          <div className="fst-login-right-brand">
            <img
              className="fst-login-right-logo"
              src="/logo-full.webp"
              alt="FullScopeTest"
              draggable={false}
            />
          </div>

          <div className="fst-login-right-card">
            <div className={`fst-auth-flip ${isRegister ? 'is-flipped' : ''}`}>
              {/* ─── Login face ─── */}
              <section className="fst-auth-face fst-auth-front" aria-label={t('login.loginForm')}>
                <h3 className="fst-login-right-title">{t('login.accountLogin')}</h3>

                <Form<LoginForm>
                  form={loginForm}
                  name="login"
                  onFinish={onLoginFinish}
                  onValuesChange={(changed) => {
                    const keys = Object.keys(changed) as Array<keyof LoginForm>
                    keys.forEach((k) => loginForm.setFields([{ name: k, errors: [] }]))
                    if ('username' in changed || 'password' in changed) setLoginError(null)
                  }}
                  autoComplete="off"
                  size="large"
                  layout="vertical"
                >
                  <Form.Item name="username" rules={[{ required: true, message: t('login.validation.usernameRequired') }]}>
                    <Input
                      className="fst-auth-input"
                      prefix={<IconUser className="fst-auth-icon" />}
                      placeholder={t('login.username')}
                      aria-label={t('login.username')}
                    />
                  </Form.Item>

                  <Form.Item
                    name="password"
                    rules={[{ required: true, message: t('login.validation.passwordRequired') }]}
                    validateStatus={loginError ? 'error' : undefined}
                    help={loginError || undefined}
                  >
                    <Input
                      className="fst-auth-input"
                      prefix={<IconLock className="fst-auth-icon" />}
                      type={loginPwdVisible ? 'text' : 'password'}
                      placeholder={t('login.password')}
                      aria-label={t('login.password')}
                      suffix={
                        <button
                          type="button"
                          className="fst-auth-eye-btn"
                          aria-label={loginPwdVisible ? t('login.hidePassword') : t('login.showPassword')}
                          onMouseDown={(e) => e.preventDefault()}
                          onClick={() => setLoginPwdVisible((v) => !v)}
                        >
                          <EyeGlyph open={loginPwdVisible} />
                        </button>
                      }
                    />
                  </Form.Item>

                  {loginError ? (
                    <div className="fst-auth-error" role="alert" aria-live="polite">
                      {loginError}
                    </div>
                  ) : null}

                  <Form.Item style={{ marginBottom: 16 }}>
                    <Button htmlType="submit" loading={loginLoading} block className="fst-auth-submit">
                      {t('login.loginBtn')}
                    </Button>
                  </Form.Item>
                </Form>

              </section>

              {/* ─── Register face ─── */}
              <section className="fst-auth-face fst-auth-back" aria-label={t('login.registerForm')}>
                <h3 className="fst-login-right-title">{t('login.register.title')}</h3>

                <Form<RegisterForm>
                  form={registerForm}
                  name="register"
                  onFinish={onRegisterFinish}
                  onValuesChange={(changed) => {
                    const keys = Object.keys(changed) as Array<keyof RegisterForm>
                    keys.forEach((k) => registerForm.setFields([{ name: k, errors: [] }]))
                  }}
                  autoComplete="off"
                  size="large"
                  layout="vertical"
                >
                  <Form.Item
                    name="username"
                    rules={[
                      { required: true, message: t('login.validation.usernameRequired') },
                      { min: 3, message: t('login.validation.usernameMin') },
                      { max: 20, message: t('login.validation.usernameMax') },
                    ]}
                  >
                    <Input
                      className="fst-auth-input"
                      prefix={<IconUser className="fst-auth-icon" />}
                      placeholder={t('login.username')}
                      aria-label={t('login.username')}
                    />
                  </Form.Item>

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
                      placeholder={t('login.register.email')}
                      aria-label={t('login.register.email')}
                    />
                  </Form.Item>

                  <Form.Item
                    name="password"
                    rules={[
                      { required: true, message: t('login.validation.passwordRequired') },
                      { min: 8, message: t('login.validation.passwordMin') },
                    ]}
                  >
                    <Input
                      className="fst-auth-input"
                      prefix={<IconLock className="fst-auth-icon" />}
                      type={registerPwdVisible ? 'text' : 'password'}
                      placeholder={t('login.password')}
                      aria-label={t('login.password')}
                      suffix={
                        <button
                          type="button"
                          className="fst-auth-eye-btn"
                          aria-label={registerPwdVisible ? t('login.hidePassword') : t('login.showPassword')}
                          onMouseDown={(e) => e.preventDefault()}
                          onClick={() => setRegisterPwdVisible((v) => !v)}
                        >
                          <EyeGlyph open={registerPwdVisible} />
                        </button>
                      }
                    />
                  </Form.Item>

                  <Form.Item
                    name="confirmPassword"
                    dependencies={['password']}
                    rules={[
                      { required: true, message: t('login.validation.confirmRequired') },
                      ({ getFieldValue }) => ({
                        validator(_, value) {
                          if (!value || getFieldValue('password') === value) return Promise.resolve()
                          return Promise.reject(new Error(t('login.validation.passwordMismatch')))
                        },
                      }),
                    ]}
                  >
                    <Input
                      className="fst-auth-input"
                      prefix={<IconLock className="fst-auth-icon" />}
                      type={registerConfirmPwdVisible ? 'text' : 'password'}
                      placeholder={t('login.register.confirmPassword')}
                      aria-label={t('login.register.confirmPassword')}
                      suffix={
                        <button
                          type="button"
                          className="fst-auth-eye-btn"
                          aria-label={registerConfirmPwdVisible ? t('login.hidePassword') : t('login.showPassword')}
                          onMouseDown={(e) => e.preventDefault()}
                          onClick={() => setRegisterConfirmPwdVisible((v) => !v)}
                        >
                          <EyeGlyph open={registerConfirmPwdVisible} />
                        </button>
                      }
                    />
                  </Form.Item>

                  <Form.Item style={{ marginBottom: 16 }}>
                    <Button htmlType="submit" loading={registerLoading} block className="fst-auth-submit">
                      {t('login.registerBtn')}
                    </Button>
                  </Form.Item>
                </Form>

                <div className="fst-login-right-footer">
                  <span className="fst-auth-footer-muted">{t('login.hasAccount')}</span>
                  <Link to="/login" className="fst-auth-link">
                    {t('login.goLogin')}
                  </Link>
                </div>
              </section>
            </div>
          </div>
        </div>

        <footer className="fst-login-right-copyright">
          © 2024 FullScopeTest. All rights reserved.
        </footer>
      </div>
    </div>
  )
}

export default Login
