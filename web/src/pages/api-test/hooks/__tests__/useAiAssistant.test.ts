import { renderHook, act } from "@testing-library/react"
import { describe, it, expect, vi, beforeEach } from "vitest"
import { useAiAssistant } from "../useAiAssistant"

// Mock the apiTestService
vi.mock("@/services/apiTestService", () => ({
  apiTestService: {
    getAiConfig: vi.fn(),
  },
}))

describe("useAiAssistant", () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it("should initialize with default values", () => {
    const { result } = renderHook(() => useAiAssistant())

    expect(result.current.aiDrawerOpen).toBe(false)
    expect(result.current.aiPrompt).toBe("")
    expect(result.current.aiRunning).toBe(false)
    expect(result.current.aiSummary).toBe("")
    expect(result.current.aiPlanOperations).toEqual([])
    expect(result.current.aiExecutionLogs).toEqual([])
    expect(result.current.globalAiConfig).toBeNull()
    expect(result.current.loadingConfig).toBe(false)
  })

  it("should update aiDrawerOpen", () => {
    const { result } = renderHook(() => useAiAssistant())

    act(() => {
      result.current.setAiDrawerOpen(true)
    })

    expect(result.current.aiDrawerOpen).toBe(true)
  })

  it("should update aiPrompt", () => {
    const { result } = renderHook(() => useAiAssistant())

    act(() => {
      result.current.setAiPrompt("test prompt")
    })

    expect(result.current.aiPrompt).toBe("test prompt")
  })

  it("should append ai logs", () => {
    const { result } = renderHook(() => useAiAssistant())

    act(() => {
      result.current.appendAiLog("info", "test message")
    })

    expect(result.current.aiExecutionLogs).toHaveLength(1)
    expect(result.current.aiExecutionLogs[0].status).toBe("info")
    expect(result.current.aiExecutionLogs[0].message).toBe("test message")
    expect(result.current.aiExecutionLogs[0].timestamp).toBeDefined()
  })

  it("should clear ai logs", () => {
    const { result } = renderHook(() => useAiAssistant())

    // Add some logs first
    act(() => {
      result.current.appendAiLog("info", "log 1")
      result.current.appendAiLog("success", "log 2")
      result.current.setAiSummary("test summary")
    })

    expect(result.current.aiExecutionLogs).toHaveLength(2)
    expect(result.current.aiSummary).toBe("test summary")

    // Clear logs
    act(() => {
      result.current.clearAiLogs()
    })

    expect(result.current.aiExecutionLogs).toEqual([])
    expect(result.current.aiSummary).toBe("")
    expect(result.current.aiPlanSource).toBe("")
    expect(result.current.aiPlanOperations).toEqual([])
  })

  it("should update multiple ai config fields", () => {
    const { result } = renderHook(() => useAiAssistant())

    act(() => {
      result.current.setAiBaseUrl("https://api.example.com")
      result.current.setAiModel("gpt-4")
      result.current.setAiApiKey("test-key")
    })

    expect(result.current.aiBaseUrl).toBe("https://api.example.com")
    expect(result.current.aiModel).toBe("gpt-4")
    expect(result.current.aiApiKey).toBe("test-key")
  })

  it("should update synthesize state", () => {
    const { result } = renderHook(() => useAiAssistant())

    act(() => {
      result.current.setAiSynthesizeModalOpen(true)
      result.current.setAiSynthesizeCount(10)
    })

    expect(result.current.aiSynthesizeModalOpen).toBe(true)
    expect(result.current.aiSynthesizeCount).toBe(10)
  })

  it("should update review state", () => {
    const { result } = renderHook(() => useAiAssistant())

    act(() => {
      result.current.setAiReviewModalOpen(true)
      result.current.setAiReviewing(true)
      result.current.setReviewSummary("review summary")
    })

    expect(result.current.aiReviewModalOpen).toBe(true)
    expect(result.current.aiReviewing).toBe(true)
    expect(result.current.reviewSummary).toBe("review summary")
  })
})
