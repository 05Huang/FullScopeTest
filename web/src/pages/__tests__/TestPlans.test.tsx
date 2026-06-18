import { describe, it, expect, vi } from 'vitest'
import { render, screen } from '@testing-library/react'
import { MemoryRouter } from 'react-router-dom'
import TestPlans from '../TestPlans'

vi.mock('@/services/api', () => ({
  default: { get: vi.fn().mockResolvedValue({ data: { data: [] } }), post: vi.fn(), put: vi.fn(), delete: vi.fn() },
}))

vi.mock('@/stores/projectStore', () => ({
  useProjectStore: vi.fn(() => ({ currentProjectId: 1 })),
}))

vi.mock('react-i18next', () => ({
  useTranslation: () => ({ t: (key: string) => key }),
}))

describe('TestPlans', () => {
  it('should render test plans page', () => {
    render(<MemoryRouter><TestPlans /></MemoryRouter>)
    expect(screen.getByText('testPlans.title')).toBeInTheDocument()
  })

  it('should render create button', () => {
    render(<MemoryRouter><TestPlans /></MemoryRouter>)
    expect(screen.getByText('testPlans.create')).toBeInTheDocument()
  })

  it('should render table', () => {
    render(<MemoryRouter><TestPlans /></MemoryRouter>)
    expect(document.querySelector('.ant-table')).toBeInTheDocument()
  })

  it('should have page header', () => {
    render(<MemoryRouter><TestPlans /></MemoryRouter>)
    expect(document.querySelector('.fst-page-header')).toBeInTheDocument()
  })

  it('should render search input', () => {
    render(<MemoryRouter><TestPlans /></MemoryRouter>)
    expect(document.querySelector('input')).toBeInTheDocument()
  })

  it('should handle empty list', () => {
    render(<MemoryRouter><TestPlans /></MemoryRouter>)
    expect(document.querySelector('.ant-table') || document.querySelector('.ant-empty')).toBeTruthy()
  })
})
