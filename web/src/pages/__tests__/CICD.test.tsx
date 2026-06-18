import { describe, it, expect, vi } from 'vitest'
import { render, screen } from '@testing-library/react'
import { MemoryRouter } from 'react-router-dom'
import CICD from '../CICD'

vi.mock('@/services/api', () => ({
  default: { get: vi.fn().mockResolvedValue({ data: { data: [] } }), post: vi.fn(), put: vi.fn(), delete: vi.fn() },
}))

vi.mock('@/stores/projectStore', () => ({
  useProjectStore: vi.fn(() => ({ currentProjectId: 1 })),
}))

vi.mock('react-i18next', () => ({
  useTranslation: () => ({ t: (key: string) => key }),
}))

describe('CICD', () => {
  it('should render CI/CD page', () => {
    render(<MemoryRouter><CICD /></MemoryRouter>)
    expect(screen.getByText('cicd.title')).toBeInTheDocument()
  })

  it('should have page header', () => {
    render(<MemoryRouter><CICD /></MemoryRouter>)
    expect(document.querySelector('.fst-page-header')).toBeInTheDocument()
  })

  it('should render tabs', () => {
    render(<MemoryRouter><CICD /></MemoryRouter>)
    expect(document.querySelector('.ant-tabs')).toBeInTheDocument()
  })

  it('should render scheduled tasks tab', () => {
    render(<MemoryRouter><CICD /></MemoryRouter>)
    expect(screen.getByText('cicd.scheduledTasks')).toBeInTheDocument()
  })

  it('should render triggers tab', () => {
    render(<MemoryRouter><CICD /></MemoryRouter>)
    expect(screen.getByText('cicd.triggerRules')).toBeInTheDocument()
  })

  it('should render create button', () => {
    render(<MemoryRouter><CICD /></MemoryRouter>)
    expect(screen.getByText('cicd.create')).toBeInTheDocument()
  })
})
