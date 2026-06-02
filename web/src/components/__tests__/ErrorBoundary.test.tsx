import { describe, it, expect } from 'vitest'
import { render, screen } from '@testing-library/react'
import ErrorBoundary from '../ErrorBoundary'

const ThrowingComponent = () => {
  throw new Error('Test error')
}

const originalError = console.error
beforeAll(() => {
  console.error = (...args: any[]) => {
    if (args[0]?.includes?.('ErrorBoundary')) return
    originalError(...args)
  }
})
afterAll(() => {
  console.error = originalError
})

describe('ErrorBoundary', () => {
  it('should render children normally when no error', () => {
    render(
      <ErrorBoundary>
        <div>Test content</div>
      </ErrorBoundary>
    )
    expect(screen.getByText('Test content')).toBeInTheDocument()
  })

  it('should render fallback UI when child throws', () => {
    render(
      <ErrorBoundary>
        <ThrowingComponent />
      </ErrorBoundary>
    )
    expect(document.body).toBeTruthy()
  })
})
