import { describe, it, expect, vi } from 'vitest'
import { render, screen } from '@testing-library/react'
import { MemoryRouter } from 'react-router-dom'
import Documents from '../Documents'

vi.mock('@/services/api', () => ({
  default: { get: vi.fn().mockResolvedValue({ data: { data: [] } }), post: vi.fn(), put: vi.fn(), delete: vi.fn() },
}))

vi.mock('@/stores/projectStore', () => ({
  useProjectStore: vi.fn(() => ({ currentProjectId: 1 })),
}))

vi.mock('react-i18next', () => ({
  useTranslation: () => ({ t: (key: string) => key }),
}))

describe('Documents', () => {
  it('should render documents page', () => {
    render(<MemoryRouter><Documents /></MemoryRouter>)
    expect(screen.getByText('documents.title')).toBeInTheDocument()
  })

  it('should render create button', () => {
    render(<MemoryRouter><Documents /></MemoryRouter>)
    expect(screen.getByText('documents.create')).toBeInTheDocument()
  })

  it('should have page header', () => {
    render(<MemoryRouter><Documents /></MemoryRouter>)
    expect(document.querySelector('.fst-page-header')).toBeInTheDocument()
  })

  it('should render search', () => {
    render(<MemoryRouter><Documents /></MemoryRouter>)
    expect(document.querySelector('input')).toBeInTheDocument()
  })

  it('should handle empty state', () => {
    render(<MemoryRouter><Documents /></MemoryRouter>)
    expect(document.querySelector('.fst-page')).toBeInTheDocument()
  })

  it('should render table or list', () => {
    render(<MemoryRouter><Documents /></MemoryRouter>)
    expect(document.querySelector('.ant-table') || document.querySelector('.ant-list')).toBeTruthy()
  })
})
