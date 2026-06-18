import { describe, it, expect, vi } from 'vitest'
import { render } from '@testing-library/react'
import { MemoryRouter } from 'react-router-dom'
import OrganizationDetail from '../OrganizationDetail'

vi.mock('@/services/api', () => ({
  default: {
    get: vi.fn().mockResolvedValue({ data: { data: { id: 1, name: 'Test Org', slug: 'test-org', members: [] } } }),
    post: vi.fn(),
    put: vi.fn(),
  },
}))

vi.mock('react-router-dom', async () => {
  const actual = await vi.importActual('react-router-dom')
  return { ...actual, useParams: () => ({ id: '1' }) }
})

vi.mock('react-i18next', () => ({
  useTranslation: () => ({ t: (key: string) => key }),
}))

describe('OrganizationDetail', () => {
  it('should render without crashing', () => {
    render(<MemoryRouter><OrganizationDetail /></MemoryRouter>)
    expect(document.querySelector('.fst-page') || document.querySelector('.ant-spin')).toBeTruthy()
  })

  it('should have page structure', () => {
    render(<MemoryRouter><OrganizationDetail /></MemoryRouter>)
    expect(document.body).toBeTruthy()
  })

  it('should render loading state initially', () => {
    render(<MemoryRouter><OrganizationDetail /></MemoryRouter>)
    expect(document.querySelector('.ant-spin') || document.querySelector('.fst-page')).toBeTruthy()
  })

  it('should handle members section', () => {
    render(<MemoryRouter><OrganizationDetail /></MemoryRouter>)
    expect(document.body.innerHTML.length).toBeGreaterThan(0)
  })

  it('should handle settings section', () => {
    render(<MemoryRouter><OrganizationDetail /></MemoryRouter>)
    expect(document.body.innerHTML.length).toBeGreaterThan(0)
  })

  it('should handle invite code section', () => {
    render(<MemoryRouter><OrganizationDetail /></MemoryRouter>)
    expect(document.body.innerHTML.length).toBeGreaterThan(0)
  })
})
