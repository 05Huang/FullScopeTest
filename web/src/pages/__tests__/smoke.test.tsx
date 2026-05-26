import { describe, it, expect, vi } from 'vitest'
import { render, screen } from '@testing-library/react'
import { BrowserRouter } from 'react-router-dom'
import Login from '../Login'

// Mock antd 的 message 组件
vi.mock('antd', async () => {
  const actual = await vi.importActual('antd')
  return {
    ...actual,
    message: {
      success: vi.fn(),
      error: vi.fn(),
      loading: vi.fn(),
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

    // 检查是否有用户名和密码输入框
    expect(screen.getByPlaceholderText(/用户名/i)).toBeInTheDocument()
    expect(screen.getByPlaceholderText(/密码/i)).toBeInTheDocument()
  })

  it('should render login button', () => {
    renderWithRouter(<Login />)

    // 检查是否有登录按钮
    expect(screen.getByRole('button', { name: /登录/i })).toBeInTheDocument()
  })

  it('should render register link', () => {
    renderWithRouter(<Login />)

    // 检查是否有注册链接
    expect(screen.getByText(/注册/i)).toBeInTheDocument()
  })
})
