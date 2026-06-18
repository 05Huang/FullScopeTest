import { describe, it, expect, vi } from 'vitest'
import { render, screen } from '@testing-library/react'
import { MemoryRouter } from 'react-router-dom'
import QualityGates from '../QualityGates'

vi.mock('@/services/api', () => ({
  default: { get: vi.fn().mockResolvedValue({ data: { data: [] } }), post: vi.fn(), put: vi.fn(), delete: vi.fn() },
}))

vi.mock('@/stores/projectStore', () => ({
  useProjectStore: vi.fn(() => ({ currentProjectId: 1 })),
}))

vi.mock('react-i18next', () => ({
  useTranslation: () => ({ t: (key: string) => key }),
}))

describe('QualityGates', () => {
  it('should render quality gates page', () => {
    render(<MemoryRouter><QualityGates /></MemoryRouter>)
    expect(screen.getByText('qualityGates.title')).toBeInTheDocument()
  })

  it('should render create button', () => {
    render(<MemoryRouter><QualityGates /></MemoryRouter>)
    expect(screen.getByText('qualityGates.create')).toBeInTheDocument()
  })

  it('should render table', () => {
    render(<MemoryRouter><QualityGates /></MemoryRouter>)
    expect(document.querySelector('.ant-table')).toBeInTheDocument()
  })

  it('should render refresh button', () => {
    render(<MemoryRouter><QualityGates /></MemoryRouter>)
    expect(screen.getByText('common.refresh')).toBeInTheDocument()
  })

  it('should handle empty state', () => {
    render(<MemoryRouter><QualityGates /></MemoryRouter>)
    // Should show empty state or table
    expect(document.querySelector('.ant-table') || document.querySelector('.ant-empty')).toBeTruthy()
  })

  it('should have page header', () => {
    render(<MemoryRouter><QualityGates /></MemoryRouter>)
    expect(document.querySelector('.fst-page-header')).toBeInTheDocument()
  })
})
