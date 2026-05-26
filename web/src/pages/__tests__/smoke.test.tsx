import { describe, it, expect, vi } from 'vitest'
import { render, screen, within } from '@testing-library/react'
import { BrowserRouter } from 'react-router-dom'
import Login from '../Login'

// Mock antd 的 message 组件
vi.mock('antd', async () => {
  const actual = await vi.importActual('antd')
  return {
    ...actual,
    message: {
      open: vi.fn(),
      success: vi.fn(),
      error: vi.fn(),
      warning: vi.fn(),
      info: vi.fn(),
      loading: vi.fn(),
      config: vi.fn(),
      destroy: vi.fn(),
    },
  }
})

// Mock authService
vi.mock('@/services/authService', () => ({
  authService: {
    login: vi.fn(),
    register: vi.fn(),
  },
}))

const renderWithRouter = (component: React.ReactElement) => {
  return render(
    <BrowserRouter>
      {component}
    </BrowserRouter>
  )
}

describe('Login Page Smoke Tests', () => {
  it('should render login form', () => {
    renderWithRouter(<Login />)

    // 使用 aria-label 限定在登录表单内查找
    const loginForm = screen.getByLabelText('登录表单')
    expect(within(loginForm).getByPlaceholderText(/用户名/i)).toBeInTheDocument()
    expect(within(loginForm).getByPlaceholderText(/密码/i)).toBeInTheDocument()
  })

  it('should render login button', () => {
    renderWithRouter(<Login />)

    // 登录按钮使用 aria-label="登录表单" 区域内查找
    const loginForm = screen.getByLabelText('登录表单')
    expect(within(loginForm).getByText(/登\s*录/)).toBeInTheDocument()
  })

  it('should render register link', () => {
    renderWithRouter(<Login />)

    // 查找"立即注册"链接（使用精确文本避免匹配多个元素）
    expect(screen.getByText('立即注册')).toBeInTheDocument()
  })
})
