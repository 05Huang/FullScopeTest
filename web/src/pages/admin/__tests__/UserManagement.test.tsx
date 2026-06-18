import { describe, it, expect, vi } from 'vitest'
import { render, screen } from '@testing-library/react'
import { MemoryRouter } from 'react-router-dom'
import UserManagement from '../UserManagement'

vi.mock('@/services/api', () => ({
  default: {
    get: vi.fn().mockResolvedValue({ data: { data: { items: [], total: 0 } } }),
    put: vi.fn(),
    post: vi.fn(),
  },
}))

vi.mock('react-i18next', () => ({
  useTranslation: () => ({ t: (key: string) => key }),
}))

describe('UserManagement', () => {
  it('should render user management page', () => {
    render(<MemoryRouter><UserManagement /></MemoryRouter>)
    expect(screen.getByText('admin.userManagement')).toBeInTheDocument()
  })

  it('should render user table', () => {
    render(<MemoryRouter><UserManagement /></MemoryRouter>)
    expect(document.querySelector('.ant-table')).toBeInTheDocument()
  })

  it('should render search input', () => {
    render(<MemoryRouter><UserManagement /></MemoryRouter>)
    expect(document.querySelector('input')).toBeInTheDocument()
  })

  it('should have page header', () => {
    render(<MemoryRouter><UserManagement /></MemoryRouter>)
    expect(document.querySelector('.fst-page-header')).toBeInTheDocument()
  })

  it('should render subtitle', () => {
    render(<MemoryRouter><UserManagement /></MemoryRouter>)
    expect(screen.getByText('admin.userManagementSubtitle')).toBeInTheDocument()
  })

  it('should render role filter', () => {
    render(<MemoryRouter><UserManagement /></MemoryRouter>)
    expect(document.querySelector('.ant-select')).toBeInTheDocument()
  })
})
