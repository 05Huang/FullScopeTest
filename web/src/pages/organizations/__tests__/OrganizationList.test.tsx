import { describe, it, expect, vi } from 'vitest'
import { render, screen } from '@testing-library/react'
import { MemoryRouter } from 'react-router-dom'
import OrganizationList from '../OrganizationList'

vi.mock('@/services/api', () => ({
  default: { get: vi.fn().mockResolvedValue({ data: { data: [] } }), post: vi.fn() },
}))

vi.mock('react-i18next', () => ({
  useTranslation: () => ({ t: (key: string) => key }),
}))

describe('OrganizationList', () => {
  it('should render organizations page', () => {
    render(<MemoryRouter><OrganizationList /></MemoryRouter>)
    expect(screen.getByText('organizations.title')).toBeInTheDocument()
  })

  it('should render create button', () => {
    render(<MemoryRouter><OrganizationList /></MemoryRouter>)
    expect(screen.getByText('organizations.create')).toBeInTheDocument()
  })

  it('should have page header', () => {
    render(<MemoryRouter><OrganizationList /></MemoryRouter>)
    expect(document.querySelector('.fst-page-header')).toBeInTheDocument()
  })

  it('should handle empty state', () => {
    render(<MemoryRouter><OrganizationList /></MemoryRouter>)
    expect(document.querySelector('.ant-empty') || document.querySelector('.ant-table')).toBeTruthy()
  })

  it('should render organization cards or list', () => {
    render(<MemoryRouter><OrganizationList /></MemoryRouter>)
    expect(document.querySelector('.fst-page')).toBeInTheDocument()
  })

  it('should render refresh button', () => {
    render(<MemoryRouter><OrganizationList /></MemoryRouter>)
    expect(screen.getByText('common.refresh')).toBeInTheDocument()
  })
})
