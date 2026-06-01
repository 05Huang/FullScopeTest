import { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { Form, Input, Button, Card, Typography, message, Divider } from 'antd'
import {
  UserOutlined,
  LockOutlined,
  MailOutlined,
  GithubOutlined,
} from '@ant-design/icons'
import { useTranslation } from 'react-i18next'
import { authService } from '@/services/authService'

const { Title, Text } = Typography

interface RegisterForm {
  username: string
  email: string
  password: string
  confirmPassword: string
}

const Register = () => {
  const { t } = useTranslation();
  const [loading, setLoading] = useState(false)
  const navigate = useNavigate()

  const onFinish = async (values: RegisterForm) => {
    setLoading(true)
    try {
      await authService.register(values.username, values.email, values.password)
      message.success(t('login.register.registerSuccess'))
      navigate('/login')
    } catch (error: any) {
      message.error(error.response?.data?.message || t('login.register.registerFailed'))
    } finally {
      setLoading(false)
    }
  }

  return (
    <div
      style={{
        minHeight: '100vh',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
        padding: 24,
      }}
    >
      <Card
        style={{
          width: '100%',
          maxWidth: 420,
          borderRadius: 16,
          boxShadow: '0 20px 60px rgba(0, 0, 0, 0.3)',
        }}
        bodyStyle={{ padding: '40px 40px 32px' }}
      >
        {/* Logo */}
        <div style={{ textAlign: 'center', marginBottom: 32 }}>
          <div
            style={{
              width: 64,
              height: 64,
              borderRadius: 16,
              background: 'linear-gradient(135deg, #2563EB 0%, #7C3AED 100%)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              margin: '0 auto 16px',
              color: '#fff',
              fontWeight: 'bold',
              fontSize: 28,
            }}
          >
            E
          </div>
          <Title level={3} style={{ margin: 0 }}>
            创建账户
          </Title>
          <Text type="secondary">{t("login.register.subtitle")}</Text>
        </div>

        <Form
          name="register"
          onFinish={onFinish}
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
              prefix={<UserOutlined style={{ color: '#bfbfbf' }} />}
              placeholder={t("login.username")}
              style={{ height: 48, borderRadius: 8 }}
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
              prefix={<MailOutlined style={{ color: '#bfbfbf' }} />}
              placeholder={t("login.register.email")}
              style={{ height: 48, borderRadius: 8 }}
            />
          </Form.Item>

          <Form.Item
            name="password"
            rules={[
              { required: true, message: t('login.validation.passwordRequired') },
              { min: 8, message: t('login.validation.passwordMin') },
            ]}
          >
            <Input.Password
              prefix={<LockOutlined style={{ color: '#bfbfbf' }} />}
              placeholder={t("login.password")}
              style={{ height: 48, borderRadius: 8 }}
            />
          </Form.Item>

          <Form.Item
            name="confirmPassword"
            dependencies={['password']}
            rules={[
              { required: true, message: t('login.validation.confirmRequired') },
              ({ getFieldValue }) => ({
                validator(_, value) {
                  if (!value || getFieldValue('password') === value) {
                    return Promise.resolve()
                  }
                  return Promise.reject(new Error(t('login.validation.passwordMismatch')))
                },
              }),
            ]}
          >
            <Input.Password
              prefix={<LockOutlined style={{ color: '#bfbfbf' }} />}
              placeholder={t("login.register.confirmPassword")}
              style={{ height: 48, borderRadius: 8 }}
            />
          </Form.Item>

          <Form.Item style={{ marginBottom: 16 }}>
            <Button
              type="primary"
              htmlType="submit"
              loading={loading}
              block
              style={{
                height: 48,
                borderRadius: 8,
                fontSize: 16,
                fontWeight: 500,
              }}
            >
              注册
            </Button>
          </Form.Item>
        </Form>

        <Divider plain>
          <Text type="secondary" style={{ fontSize: 12 }}>
            或者
          </Text>
        </Divider>

        <Button
          icon={<GithubOutlined />}
          block
          size="large"
          style={{
            height: 48,
            borderRadius: 8,
            marginBottom: 24,
          }}
        >
          使用 GitHub 注册
        </Button>

        <div style={{ textAlign: 'center' }}>
          <Text type="secondary">{t("login.hasAccount")}</Text>
          <Link to="/login" style={{ marginLeft: 8, fontWeight: 500 }}>
            立即登录
          </Link>
        </div>
      </Card>
    </div>
  )
}

export default Register
