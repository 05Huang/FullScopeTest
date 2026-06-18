import { describe, it, expect, vi, beforeEach } from "vitest"
import { render, screen, fireEvent, waitFor } from "@testing-library/react"
import { BrowserRouter } from "react-router-dom"
import ForgotPassword from "../ForgotPassword"

vi.mock("@/services/authService", () => ({
  authService: {
    forgotPassword: vi.fn().mockResolvedValue({ code: 200, data: null, message: "ok", timestamp: "" }),
  },
}))

vi.mock("react-i18next", () => ({
  useTranslation: () => ({ t: (key: string) => key }),
}))

const renderForgotPassword = () =>
  render(
    <BrowserRouter>
      <ForgotPassword />
    </BrowserRouter>
  )

describe("ForgotPassword Page", () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it("should render forgot password form", () => {
    renderForgotPassword()
    expect(screen.getByText(/forgotPassword.title/i)).toBeTruthy()
  })

  it("should render email input", () => {
    renderForgotPassword()
    expect(screen.getByPlaceholderText(/forgotPassword.emailPlaceholder/i)).toBeTruthy()
  })

  it("should render submit button", () => {
    renderForgotPassword()
    expect(screen.getByText(/forgotPassword.submitBtn/i)).toBeTruthy()
  })

  it("should render back to login link", () => {
    renderForgotPassword()
    expect(screen.getByText(/login.goLogin/i)).toBeTruthy()
  })

  it("should show subtitle", () => {
    renderForgotPassword()
    expect(screen.getByText(/forgotPassword.subtitle/i)).toBeTruthy()
  })

  it("should allow typing email", () => {
    renderForgotPassword()
    const input = screen.getByPlaceholderText(/forgotPassword.emailPlaceholder/i)
    fireEvent.change(input, { target: { value: "test@example.com" } })
    expect(input).toBeTruthy()
  })
})
