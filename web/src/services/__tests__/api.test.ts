import { describe, it, expect, vi, beforeEach } from "vitest"

vi.mock("@/stores/authStore", () => ({
  useAuthStore: {
    getState: () => ({ logout: vi.fn() }),
  },
}))

// 使用 vi.hoisted 确保变量在 mock 之前初始化
const { capturedConfig, capturedInstance } = vi.hoisted(() => {
  const cfg: any = { value: null }
  const inst: any = { value: null }
  return {
    capturedConfig: cfg,
    capturedInstance: inst,
  }
})

vi.mock("axios", () => {
  const interceptors = {
    request: { use: vi.fn() },
    response: { use: vi.fn() },
  }
  const instance = { interceptors, defaults: { baseURL: "/api/v1" } }
  capturedInstance.value = instance
  return {
    default: {
      create: vi.fn((config: any) => {
        capturedConfig.value = config
        return instance
      }),
      post: vi.fn(),
    },
  }
})

import api from "../api"

describe("api.ts axios instance", () => {
  it("should have correct baseURL", () => {
    expect(capturedConfig.value).not.toBeNull()
    expect(capturedConfig.value.baseURL).toBe("/api/v1")
  })

  it("should set timeout to 30 seconds", () => {
    expect(capturedConfig.value.timeout).toBe(30000)
  })

  it("should enable withCredentials", () => {
    expect(capturedConfig.value.withCredentials).toBe(true)
  })

  it("should set Content-Type header", () => {
    expect(capturedConfig.value.headers["Content-Type"]).toBe("application/json")
  })

  it("should register request interceptor", () => {
    expect(capturedInstance.value.interceptors.request.use).toHaveBeenCalled()
  })

  it("should register response interceptor", () => {
    expect(capturedInstance.value.interceptors.response.use).toHaveBeenCalled()
  })

  it("should export instance as default", () => {
    expect(api).toBe(capturedInstance.value)
  })
})
