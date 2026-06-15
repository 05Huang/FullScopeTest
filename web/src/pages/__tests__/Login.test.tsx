import { describe, it, expect, vi, beforeEach } from "vitest"
import { render, screen } from "@testing-library/react"
import { BrowserRouter } from "react-router-dom"
import Login from "../Login"

vi.mock("@/services/authService", () => ({
  authService: {
    login: vi.fn().mockResolvedValue({ code: 200, data: { user: { id: 1, username: "admin" } }, message: "ok", timestamp: "" }),
    register: vi.fn().mockResolvedValue({ code: 201, data: null, message: "ok", timestamp: "" }),
  },
}))

vi.mock("@/stores/authStore", () => ({
  useAuthStore: Object.assign(
    () => ({ setAuth: vi.fn(), isAuthenticated: false, user: null }),
    { getState: () => ({ setAuth: vi.fn(), logout: vi.fn() }) }
  ),
}))

vi.mock("react-i18next", () => ({
  useTranslation: () => ({
    t: (key: string) => key,
    i18n: { language: "zh-CN", changeLanguage: vi.fn() },
  }),
}))

const renderLogin = () =>
  render(
    <BrowserRouter>
      <Login />
    </BrowserRouter>
  )

describe("Login Page", () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it("should render login form inputs", () => {
    renderLogin()
    const inputs = document.querySelectorAll("input")
    expect(inputs.length).toBeGreaterThan(0)
  })

  it("should render submit button", () => {
    renderLogin()
    const buttons = document.querySelectorAll("button[type='submit']")
    expect(buttons.length).toBeGreaterThan(0)
  })

  it("should render username input field", () => {
    renderLogin()
    const usernameInputs = screen.getAllByPlaceholderText(/username|用户名/i)
    expect(usernameInputs.length).toBeGreaterThan(0)
  })

  it("should render password input field", () => {
    renderLogin()
    const passwordInputs = screen.getAllByPlaceholderText(/password|密码/i)
    expect(passwordInputs.length).toBeGreaterThan(0)
  })

  it("should not crash on render", () => {
    const { container } = renderLogin()
    expect(container).toBeTruthy()
  })
})
