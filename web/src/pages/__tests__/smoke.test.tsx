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
  it('should render without crashing', () => {
    renderWithRouter(<Login />)
    // Login page should render form inputs
    const inputs = document.querySelectorAll('input')
    expect(inputs.length).toBeGreaterThan(0)
  })

  it('should render username and password inputs', () => {
    renderWithRouter(<Login />)
    // Look for input fields by placeholder text (i18n keys)
    const usernameInputs = screen.getAllByPlaceholderText(/username|用户名/i)
    const passwordInputs = screen.getAllByPlaceholderText(/password|密码/i)
    expect(usernameInputs.length).toBeGreaterThan(0)
    expect(passwordInputs.length).toBeGreaterThan(0)
  })

  it('should render submit buttons', () => {
    renderWithRouter(<Login />)
    // Should have at least one button element
    const buttons = document.querySelectorAll('button[type="submit"]')
    expect(buttons.length).toBeGreaterThan(0)
  })
})
