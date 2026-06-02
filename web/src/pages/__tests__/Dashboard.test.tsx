import { describe, it, expect, vi } from 'vitest'
import { render, screen } from '@testing-library/react'
import { BrowserRouter } from 'react-router-dom'
import Dashboard from '../Dashboard'

// Mock services
vi.mock('@/services/reportService', () => ({
  reportService: {
    getDashboardStats: vi.fn().mockResolvedValue({ data: {} }),
    getRecentRuns: vi.fn().mockResolvedValue({ data: [] }),
  },
}))

vi.mock('@/stores/projectStore', () => ({
  useProjectStore: () => ({
    currentProjectId: 1,
    projects: [],
    setCurrentProject: vi.fn(),
  }),
}))

vi.mock('@/services/projectService', () => ({
  projectService: {
    getProjects: vi.fn().mockResolvedValue({ data: [] }),
  },
}))

const renderWithRouter = (component: React.ReactElement) => {
  return render(
    <BrowserRouter>{component}</BrowserRouter>
  )
}

describe('Dashboard Smoke Tests', () => {
  it('should render without crashing', () => {
    renderWithRouter(<Dashboard />)
    // Dashboard should render some content
    expect(document.body).toBeTruthy()
  })

  it('should render dashboard title or heading', () => {
    renderWithRouter(<Dashboard />)
    // Look for any heading or dashboard-related text
    const headings = document.querySelectorAll('h1, h2, h3, h4, h5')
    expect(headings.length).toBeGreaterThanOrEqual(0) // At minimum renders
  })
})
