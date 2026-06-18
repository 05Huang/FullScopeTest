import { describe, it, expect, vi, beforeEach } from "vitest"
import { render, screen } from "@testing-library/react"
import { BrowserRouter } from "react-router-dom"
import UserManagement from "../UserManagement"

vi.mock("@/services/api", () => ({
  default: {
    get: vi.fn().mockResolvedValue({ data: { data: { users: [], total: 0 } } }),
    put: vi.fn().mockResolvedValue({ data: { message: "ok" } }),
  },
}))

vi.mock("@/services/adminService", () => ({
  adminService: {
    getUsers: vi.fn().mockResolvedValue({ data: { users: [], total: 0 } }),
    updateUserStatus: vi.fn().mockResolvedValue({ data: { message: "ok" } }),
    updateUserRole: vi.fn().mockResolvedValue({ data: { message: "ok" } }),
    resetPassword: vi.fn().mockResolvedValue({ data: { message: "ok" } }),
  },
}))

vi.mock("@/hooks/useRole", () => ({
  useRole: () => ({ isAdmin: true, role: "admin" }),
}))

vi.mock("react-i18next", () => ({
  useTranslation: () => ({ t: (key: string) => key }),
}))

const renderUserManagement = () =>
  render(
    <BrowserRouter>
      <UserManagement />
    </BrowserRouter>
  )

describe("UserManagement Page", () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it("should render without crashing", () => {
    renderUserManagement()
    expect(document.body).toBeTruthy()
  })

  it("should render page title", () => {
    renderUserManagement()
    expect(screen.getByText("admin.userManagement")).toBeTruthy()
  })

  it("should render subtitle", () => {
    renderUserManagement()
    expect(screen.getByText("admin.userManagementSubtitle")).toBeTruthy()
  })

  it("should render search input", () => {
    renderUserManagement()
    expect(screen.getByPlaceholderText("admin.searchPlaceholder")).toBeTruthy()
  })

  it("should render filter role select", () => {
    const { container } = renderUserManagement()
    expect(container.querySelector(".ant-select")).toBeTruthy()
  })

  it("should render refresh button", () => {
    renderUserManagement()
    expect(screen.getByText("Refresh")).toBeTruthy()
  })
})
