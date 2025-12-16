import { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { Form, Input, Button, Card, Typography, message, Divider } from 'antd'
import {
  UserOutlined,
  LockOutlined,
  GithubOutlined,
} from '@ant-design/icons'
import { authService } from '@/services/authService'
import { useAuthStore } from '@/stores/authStore'

const { Title, Text } = Typography

interface LoginForm {
  username: string
  password: string
}

const Login = () => {
  const [loading, setLoading] = useState(false)
  const navigate = useNavigate()
  const { setAuth } = useAuthStore()

  const onFinish = async (values: LoginForm) => {
    setLoading(true)
    try {
      const response = await authService.login(values.username, values.password)
      // 后端返回: { code: 200, data: { user: {...}, access_token: "...", refresh_token: "..." } }
      const { user, access_token, refresh_token } = response.data
      setAuth(access_token, refresh_token, user || { id: 0, username: values.username, email: '' })
      message.success('登录成功！')
      navigate('/dashboard')
    } catch (error: any) {
      message.error(error.response?.data?.message || '登录失败，请检查用户名和密码')
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
            欢迎使用 EasyTest
          </Title>
          <Text type="secondary">简单高效的自动化测试平台</Text>
        </div>

        <Form
          name="login"
          onFinish={onFinish}
          autoComplete="off"
          size="large"
          layout="vertical"
        >
          <Form.Item
            name="username"
            rules={[{ required: true, message: '请输入用户名' }]}
          >
            <Input
              prefix={<UserOutlined style={{ color: '#bfbfbf' }} />}
              placeholder="用户名"
              style={{ height: 48, borderRadius: 8 }}
            />
          </Form.Item>

          <Form.Item
            name="password"
            rules={[{ required: true, message: '请输入密码' }]}
          >
            <Input.Password
              prefix={<LockOutlined style={{ color: '#bfbfbf' }} />}
              placeholder="密码"
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
              登录
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
          使用 GitHub 登录
        </Button>

        <div style={{ textAlign: 'center' }}>
          <Text type="secondary">还没有账号？</Text>
          <Link to="/register" style={{ marginLeft: 8, fontWeight: 500 }}>
            立即注册
          </Link>
        </div>
      </Card>
    </div>
  )
}

export default Login
