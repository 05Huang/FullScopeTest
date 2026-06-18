import { describe, it, expect, vi, beforeEach } from "vitest"
import { render, screen, fireEvent } from "@testing-library/react"
import { BrowserRouter } from "react-router-dom"
import ResetPassword from "../ResetPassword"

vi.mock("@/services/authService", () => ({
  authService: {
    resetPassword: vi.fn().mockResolvedValue({ code: 200, data: null, message: "ok", timestamp: "" }),
  },
}))

vi.mock("react-i18next", () => ({
  useTranslation: () => ({ t: (key: string) => key }),
}))

const renderResetPassword = () =>
  render(
    <BrowserRouter>
      <ResetPassword />
    </BrowserRouter>
  )

describe("ResetPassword Page", () => {
  beforeEach(() => {
    vi.clearAllMocks()
    window.history.pushState({}, "", "/reset-password?token=test-token")
  })

  it("should render reset password form", () => {
    renderResetPassword()
    expect(screen.getByText("resetPassword.title")).toBeTruthy()
  })

  it("should render new password input", () => {
    renderResetPassword()
    expect(screen.getByPlaceholderText("resetPassword.newPassword")).toBeTruthy()
  })

  it("should render confirm password input", () => {
    renderResetPassword()
    expect(screen.getByPlaceholderText("resetPassword.confirmPassword")).toBeTruthy()
  })

  it("should render submit button", () => {
    renderResetPassword()
    expect(screen.getByText("resetPassword.submitBtn")).toBeTruthy()
  })

  it("should render subtitle", () => {
    renderResetPassword()
    expect(screen.getByText("resetPassword.subtitle")).toBeTruthy()
  })

  it("should allow typing password", () => {
    renderResetPassword()
    const input = screen.getByPlaceholderText("resetPassword.newPassword")
    fireEvent.change(input, { target: { value: "NewPassword123!" } })
    expect(input).toBeTruthy()
  })
})
