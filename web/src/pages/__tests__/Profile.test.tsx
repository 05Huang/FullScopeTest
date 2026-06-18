import { describe, it, expect, vi, beforeEach } from "vitest"
import { render, screen } from "@testing-library/react"
import { BrowserRouter } from "react-router-dom"
import Profile from "../Profile"

vi.mock("@/services/api", () => ({
  default: {
    get: vi.fn().mockResolvedValue({ data: { data: { username: "test", email: "test@test.com" } } }),
    put: vi.fn().mockResolvedValue({ data: { message: "ok" } }),
  },
}))

vi.mock("@/stores/authStore", () => ({
  useAuthStore: () => ({ user: { id: 1, username: "test", email: "test@test.com" } }),
}))

vi.mock("react-i18next", () => ({
  useTranslation: () => ({ t: (key: string) => key }),
}))

const renderProfile = () =>
  render(
    <BrowserRouter>
      <Profile />
    </BrowserRouter>
  )

describe("Profile Page", () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it("should render without crashing", () => {
    renderProfile()
    expect(document.body).toBeTruthy()
  })

  it("should render page title", () => {
    renderProfile()
    expect(screen.getByText("profile.title")).toBeTruthy()
  })

  it("should render basic info title", () => {
    renderProfile()
    expect(screen.getByText("profile.basicInfoTitle")).toBeTruthy()
  })

  it("should render password title", () => {
    renderProfile()
    expect(screen.getByText("profile.passwordTitle")).toBeTruthy()
  })

  it("should render username label", () => {
    renderProfile()
    expect(screen.getByText("profile.usernameLabel")).toBeTruthy()
  })

  it("should render email label", () => {
    renderProfile()
    expect(screen.getByText("profile.emailLabel")).toBeTruthy()
  })
})
