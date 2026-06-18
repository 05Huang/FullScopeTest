import { describe, it, expect, beforeEach, vi } from 'vitest'
import { render, screen } from '@testing-library/react'
import { MemoryRouter } from 'react-router-dom'
import Profile from '../Profile'

vi.mock('@/services/api', () => ({
  default: { get: vi.fn().mockResolvedValue({ data: { data: {} } }), put: vi.fn().mockResolvedValue({ data: { data: {} } }) },
}))

vi.mock('@/stores/authStore', () => ({
  useAuthStore: vi.fn(() => ({
    user: { id: 1, username: 'testuser', email: 'test@example.com', role: 'member' },
    setAuth: vi.fn(),
  })),
}))

vi.mock('react-i18next', () => ({
  useTranslation: () => ({ t: (key: string) => key }),
}))

describe('Profile', () => {
  it('should render profile page', () => {
    render(<MemoryRouter><Profile /></MemoryRouter>)
    expect(screen.getByText('profile.title')).toBeInTheDocument()
  })

  it('should display username', () => {
    render(<MemoryRouter><Profile /></MemoryRouter>)
    expect(screen.getByDisplayValue('testuser')).toBeInTheDocument()
  })

  it('should display email', () => {
    render(<MemoryRouter><Profile /></MemoryRouter>)
    expect(screen.getByDisplayValue('test@example.com')).toBeInTheDocument()
  })

  it('should render save button', () => {
    render(<MemoryRouter><Profile /></MemoryRouter>)
    expect(screen.getByText('profile.save')).toBeInTheDocument()
  })

  it('should render change password section', () => {
    render(<MemoryRouter><Profile /></MemoryRouter>)
    expect(screen.getByText('profile.changePassword')).toBeInTheDocument()
  })

  it('should have form fields', () => {
    render(<MemoryRouter><Profile /></MemoryRouter>)
    const inputs = document.querySelectorAll('input')
    expect(inputs.length).toBeGreaterThan(0)
  })
})
