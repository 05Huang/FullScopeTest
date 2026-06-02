import { describe, it, expect, vi } from 'vitest'
import { render, screen } from '@testing-library/react'
import { BrowserRouter } from 'react-router-dom'
import Settings from '../Settings'

vi.mock('@/stores/authStore', () => ({
  useAuthStore: () => ({
    user: { id: 1, username: 'testuser', role: 'admin' },
    token: 'test-token',
  }),
}))

vi.mock('@/services/authService', () => ({
  authService: {
    updateProfile: vi.fn(),
  },
}))

const renderWithRouter = (component: React.ReactElement) => {
  return render(
    <BrowserRouter>{component}</BrowserRouter>
  )
}

describe('Settings Smoke Tests', () => {
  it('should render without crashing', () => {
    renderWithRouter(<Settings />)
    expect(document.body).toBeTruthy()
  })
})
