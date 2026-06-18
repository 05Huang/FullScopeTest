import { describe, it, expect, vi, beforeEach } from 'vitest'

vi.mock("../api", () => ({
  default: {
    post: vi.fn(),
    get: vi.fn(),
    put: vi.fn(),
  },
}))

import { authService } from "../authService"
import api from "../api"

describe("authService", () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it("login should call POST /auth/login", async () => {
    const mockResponse = { code: 200, data: { user: { id: 1 } }, message: "ok", timestamp: "" }
    vi.mocked(api.post).mockResolvedValue(mockResponse)

    const result = await authService.login("admin", "pass123")
    expect(api.post).toHaveBeenCalledWith("/auth/login", { username: "admin", password: "pass123" })
    expect(result).toEqual(mockResponse)
  })

  it("register should call POST /auth/register", async () => {
    const mockResponse = { code: 201, data: null, message: "ok", timestamp: "" }
    vi.mocked(api.post).mockResolvedValue(mockResponse)

    const result = await authService.register("newuser", "new@example.com", "pass123")
    expect(api.post).toHaveBeenCalledWith("/auth/register", { username: "newuser", email: "new@example.com", password: "pass123" })
    expect(result).toEqual(mockResponse)
  })

  it("getCurrentUser should call GET /auth/me", async () => {
    const mockResponse = { code: 200, data: { id: 1, username: "admin" }, message: "ok", timestamp: "" }
    vi.mocked(api.get).mockResolvedValue(mockResponse)

    const result = await authService.getCurrentUser()
    expect(api.get).toHaveBeenCalledWith("/auth/me")
    expect(result).toEqual(mockResponse)
  })

  it("updateProfile should call PUT /auth/me", async () => {
    const mockResponse = { code: 200, data: null, message: "ok", timestamp: "" }
    vi.mocked(api.put).mockResolvedValue(mockResponse)

    await authService.updateProfile({ username: "newname" })
    expect(api.put).toHaveBeenCalledWith("/auth/me", { username: "newname" })
  })

  it("changePassword should call PUT /auth/password", async () => {
    const mockResponse = { code: 200, data: null, message: "ok", timestamp: "" }
    vi.mocked(api.put).mockResolvedValue(mockResponse)

    await authService.changePassword("old123", "new456")
    expect(api.put).toHaveBeenCalledWith("/auth/password", { old_password: "old123", new_password: "new456" })
  })

  it("forgotPassword should call POST /auth/forgot-password", async () => {
    const mockResponse = { code: 200, data: null, message: "如果该邮箱已注册，重置链接已发送", timestamp: "" }
    vi.mocked(api.post).mockResolvedValue(mockResponse)

    const result = await authService.forgotPassword("user@example.com")
    expect(api.post).toHaveBeenCalledWith("/auth/forgot-password", { email: "user@example.com" })
    expect(result.data).toBeNull()
    expect(result.message).toContain("重置链接已发送")
  })

  it("resetPassword should call POST /auth/reset-password", async () => {
    const mockResponse = { code: 200, data: null, message: "ok", timestamp: "" }
    vi.mocked(api.post).mockResolvedValue(mockResponse)

    await authService.resetPassword("token123", "newpass")
    expect(api.post).toHaveBeenCalledWith("/auth/reset-password", { token: "token123", new_password: "newpass" })
  })
})
