import { describe, it, expect, vi } from 'vitest'
import { render } from '@testing-library/react'
import { BrowserRouter } from 'react-router-dom'
import Reports from '../Reports'

vi.mock('@/services/reportService', () => ({
  reportService: {
    getReports: vi.fn().mockResolvedValue({ data: [], total: 0 }),
    getTestRuns: vi.fn().mockResolvedValue({ data: [], total: 0 }),
  },
}))

vi.mock('@/stores/projectStore', () => ({
  useProjectStore: () => ({
    currentProjectId: 1,
  }),
}))

vi.mock('@/stores/authStore', () => ({
  useAuthStore: () => ({
    user: { id: 1, username: 'testuser' },
    token: 'test-token',
  }),
}))

const renderWithRouter = (component: React.ReactElement) => {
  return render(
    <BrowserRouter>{component}</BrowserRouter>
  )
}

describe('Reports Smoke Tests', () => {
  it('should render without crashing', () => {
    renderWithRouter(<Reports />)
    expect(document.body).toBeTruthy()
  })
})
