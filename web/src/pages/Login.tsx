import { useEffect, useState } from 'react'
import { useLocation, useNavigate, Link } from 'react-router-dom'
import { Form, Input, Button, Typography, message } from 'antd'
import { authService } from '@/services/authService'
import { useAuthStore } from '@/stores/authStore'

const { Title, Text } = Typography

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

const BrandMark = () => (
  <div className="fst-auth-brand" aria-hidden="true">
    <svg viewBox="0 0 64 64" className="fst-auth-brand-svg">
      <defs>
        <linearGradient id="fstBrandG" x1="10" y1="8" x2="56" y2="56" gradientUnits="userSpaceOnUse">
          <stop offset="0" stopColor="#5FA59B" />
          <stop offset="0.6" stopColor="#3D6E66" />
          <stop offset="1" stopColor="#D7B56D" />
        </linearGradient>
        <filter id="fstGlow" x="-40%" y="-40%" width="180%" height="180%">
          <feGaussianBlur stdDeviation="3.5" result="blur" />
          <feColorMatrix
            in="blur"
            type="matrix"
            values="1 0 0 0 0  0 1 0 0 0  0 0 1 0 0  0 0 0 0.9 0"
            result="glow"
          />
          <feMerge>
            <feMergeNode in="glow" />
            <feMergeNode in="SourceGraphic" />
          </feMerge>
        </filter>
      </defs>
      <path
        d="M18 16h28c1.7 0 3 1.3 3 3v7c0 1.7-1.3 3-3 3H25.2v6.2H42c1.7 0 3 1.3 3 3v7c0 1.7-1.3 3-3 3H18c-1.7 0-3-1.3-3-3V19c0-1.7 1.3-3 3-3Z"
        fill="url(#fstBrandG)"
        filter="url(#fstGlow)"
      />
      <path
        d="M22 23h24"
        stroke="rgba(255,255,255,0.55)"
        strokeWidth="2"
        strokeLinecap="round"
      />
      <path
        d="M22 45h18"
        stroke="rgba(255,255,255,0.38)"
        strokeWidth="2"
        strokeLinecap="round"
      />
    </svg>
  </div>
)

const Login = () => {
  const [loginLoading, setLoginLoading] = useState(false)
  const [registerLoading, setRegisterLoading] = useState(false)
  const navigate = useNavigate()
  const location = useLocation()
  const { setAuth } = useAuthStore()
  const [loginForm] = Form.useForm<LoginForm>()
  const [registerForm] = Form.useForm<RegisterForm>()
  const [loginError, setLoginError] = useState<string | null>(null)

  const [mode, setMode] = useState<AuthMode>(() => getModeFromPathname(location.pathname))

  useEffect(() => {
    setMode(getModeFromPathname(location.pathname))
  }, [location.pathname])

  const isRegister = mode === 'register'

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
        throw new Error(response.message || '用户名或密码错误')
      }
      const { user, access_token, refresh_token } = response.data
      setAuth(access_token, refresh_token, user || { id: 0, username: values.username, email: '' })
      message.success('登录成功！')
      navigate('/dashboard')
    } catch (error: any) {
      const msg = error?.response?.data?.message || error?.message || '登录失败，请检查用户名和密码'
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
      message.success('注册成功！请登录')
      navigate('/login')
    } catch (error: any) {
      message.error(error.response?.data?.message || '注册失败，请稍后重试')
    } finally {
      setRegisterLoading(false)
    }
  }

  return (
    <div className="fst-auth-root">
      <div className="fst-auth-bg" aria-hidden="true">
        <div className="fst-auth-bg-blob fst-auth-bg-blob-a" />
        <div className="fst-auth-bg-blob fst-auth-bg-blob-b" />
        <div className="fst-auth-bg-grid" />
        <div className="fst-auth-bg-particles" />
      </div>

      <div className="fst-auth-shell">
        <div className="fst-auth-card">
          <div className={`fst-auth-flip ${isRegister ? 'is-flipped' : ''}`}>
            <section className="fst-auth-face fst-auth-front" aria-label="登录表单">
              <div className="fst-auth-header">
                <BrandMark />
                <div className="fst-auth-heading">
                  <Title level={3} className="fst-auth-title">
                    欢迎使用 FullScopeTest
                  </Title>
                  <Text className="fst-auth-subtitle">简单高效的自动化测试平台</Text>
                </div>
              </div>

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
                <Form.Item name="username" rules={[{ required: true, message: '请输入用户名' }]}>
                  <Input
                    className="fst-auth-input"
                    prefix={<IconUser className="fst-auth-icon" />}
                    placeholder="用户名"
                    aria-label="用户名"
                  />
                </Form.Item>

                <Form.Item
                  name="password"
                  rules={[{ required: true, message: '请输入密码' }]}
                  validateStatus={loginError ? 'error' : undefined}
                  help={loginError || undefined}
                >
                  <Input.Password
                    className="fst-auth-input"
                    prefix={<IconLock className="fst-auth-icon" />}
                    placeholder="密码"
                    aria-label="密码"
                    iconRender={(open) => <EyeGlyph open={open} />}
                  />
                </Form.Item>

                {loginError ? (
                  <div className="fst-auth-error" role="alert" aria-live="polite">
                    {loginError}
                  </div>
                ) : null}

                <Form.Item style={{ marginBottom: 14 }}>
                  <Button htmlType="submit" loading={loginLoading} block className="fst-auth-submit">
                    登录
                  </Button>
                </Form.Item>
              </Form>

              <div className="fst-auth-meta" aria-label="登录提示">
                <div className="fst-auth-slogan">
                  <div className="fst-auth-slogan-line">把测试覆盖看得见，把风险收得住</div>
                  <div className="fst-auth-slogan-line">一套平台，连接接口 / Web / 性能全链路</div>
                </div>
                <div className="fst-auth-slogan-sub">更清晰的质量视野，更稳定的交付节奏</div>
                <div className="fst-auth-chips" aria-label="平台特性">
                  <span className="fst-auth-chip">低延迟会话</span>
                  <span className="fst-auth-chip">细粒度权限</span>
                  <span className="fst-auth-chip">可追溯审计</span>
                </div>
              </div>

              <div className="fst-auth-footer">
                <span className="fst-auth-footer-muted">还没有账号？</span>
                <Link to="/register" className="fst-auth-link">
                  立即注册
                </Link>
              </div>
            </section>

            <section className="fst-auth-face fst-auth-back" aria-label="注册表单">
              <div className="fst-auth-header">
                <BrandMark />
                <div className="fst-auth-heading">
                  <Title level={3} className="fst-auth-title">
                    创建账户
                  </Title>
                  <Text className="fst-auth-subtitle">开启你的自动化测试之旅</Text>
                </div>
              </div>

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
                    { required: true, message: '请输入用户名' },
                    { min: 3, message: '用户名至少3个字符' },
                    { max: 20, message: '用户名最多20个字符' },
                  ]}
                >
                  <Input
                    className="fst-auth-input"
                    prefix={<IconUser className="fst-auth-icon" />}
                    placeholder="用户名"
                    aria-label="用户名"
                  />
                </Form.Item>

                <Form.Item
                  name="email"
                  rules={[
                    { required: true, message: '请输入邮箱' },
                    { type: 'email', message: '请输入有效的邮箱地址' },
                  ]}
                >
                  <Input
                    className="fst-auth-input"
                    prefix={<IconMail className="fst-auth-icon" />}
                    placeholder="邮箱"
                    aria-label="邮箱"
                  />
                </Form.Item>

                <Form.Item
                  name="password"
                  rules={[
                    { required: true, message: '请输入密码' },
                    { min: 6, message: '密码至少6个字符' },
                  ]}
                >
                  <Input.Password
                    className="fst-auth-input"
                    prefix={<IconLock className="fst-auth-icon" />}
                    placeholder="密码"
                    aria-label="密码"
                    iconRender={(open) => <EyeGlyph open={open} />}
                  />
                </Form.Item>

                <Form.Item
                  name="confirmPassword"
                  dependencies={['password']}
                  rules={[
                    { required: true, message: '请确认密码' },
                    ({ getFieldValue }) => ({
                      validator(_, value) {
                        if (!value || getFieldValue('password') === value) return Promise.resolve()
                        return Promise.reject(new Error('两次输入的密码不一致'))
                      },
                    }),
                  ]}
                >
                  <Input.Password
                    className="fst-auth-input"
                    prefix={<IconLock className="fst-auth-icon" />}
                    placeholder="确认密码"
                    aria-label="确认密码"
                    iconRender={(open) => <EyeGlyph open={open} />}
                  />
                </Form.Item>

                <Form.Item style={{ marginBottom: 14 }}>
                  <Button htmlType="submit" loading={registerLoading} block className="fst-auth-submit">
                    注册
                  </Button>
                </Form.Item>
              </Form>

              <div className="fst-auth-meta" aria-label="注册提示">
                <div className="fst-auth-meta-line">
                  <span className="fst-auth-meta-text">注册后可创建项目并管理用例</span>
                  <span className="fst-auth-dot" />
                  <span className="fst-auth-meta-text">支持团队协作</span>
                </div>
                <div className="fst-auth-chips" aria-label="平台特性">
                  <span className="fst-auth-chip">统一鉴权</span>
                  <span className="fst-auth-chip">自动化工作流</span>
                  <span className="fst-auth-chip">安全合规</span>
                </div>
              </div>

              <div className="fst-auth-footer">
                <span className="fst-auth-footer-muted">已有账号？</span>
                <Link to="/login" className="fst-auth-link">
                  去登录
                </Link>
              </div>
            </section>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Login
