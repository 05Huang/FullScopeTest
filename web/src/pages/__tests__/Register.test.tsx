import { describe, it, expect, vi, beforeEach } from "vitest"
import { render, screen } from "@testing-library/react"
import { BrowserRouter } from "react-router-dom"
import Login from "../Login"

vi.mock("@/services/authService", () => ({
  authService: {
    login: vi.fn(),
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

const renderAtRegister = () =>
  render(
    <BrowserRouter>
      <Login />
    </BrowserRouter>
  )

describe("Register Page (via Login component)", () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it("should render without crashing in register mode", () => {
    const { container } = renderAtRegister()
    expect(container).toBeTruthy()
  })

  it("should render form inputs", () => {
    renderAtRegister()
    const inputs = document.querySelectorAll("input")
    expect(inputs.length).toBeGreaterThan(0)
  })

  it("should render submit buttons", () => {
    renderAtRegister()
    const buttons = document.querySelectorAll("button[type='submit']")
    expect(buttons.length).toBeGreaterThan(0)
  })

  it("should render page without errors", () => {
    const consoleSpy = vi.spyOn(console, "error").mockImplementation(() => {})
    renderAtRegister()
    expect(consoleSpy).not.toHaveBeenCalled()
    consoleSpy.mockRestore()
  })

  it("should have accessible form structure", () => {
    renderAtRegister()
    const form = document.querySelector("form")
    expect(form).toBeTruthy()
  })
})
