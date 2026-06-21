import { renderHook, act } from "@testing-library/react"
import { describe, it, expect, vi, beforeEach } from "vitest"
import { useWebExplorer } from "../useWebExplorer"

describe("useWebExplorer", () => {
  beforeEach(() => {
    localStorage.clear()
  })

  it("should initialize with default values", () => {
    const { result } = renderHook(() => useWebExplorer())

    expect(result.current.isExploreModalOpen).toBe(false)
    expect(result.current.exploreStartUrl).toBe("")
    expect(result.current.exploreObjective).toBe("尽可能多地点击不同页面并寻找报错")
    expect(result.current.exploreMaxSteps).toBe(10)
    expect(result.current.exploreRunning).toBe(false)
    expect(result.current.exploreReport).toBeNull()
    expect(result.current.exploreConsoleLines).toEqual([])
    expect(result.current.exploreHistory).toEqual([])
  })

  it("should update explore modal state", () => {
    const { result } = renderHook(() => useWebExplorer())

    act(() => {
      result.current.setIsExploreModalOpen(true)
    })

    expect(result.current.isExploreModalOpen).toBe(true)
  })

  it("should update explore settings", () => {
    const { result } = renderHook(() => useWebExplorer())

    act(() => {
      result.current.setExploreStartUrl("https://example.com")
      result.current.setExploreObjective("Test objective")
      result.current.setExploreMaxSteps(20)
    })

    expect(result.current.exploreStartUrl).toBe("https://example.com")
    expect(result.current.exploreObjective).toBe("Test objective")
    expect(result.current.exploreMaxSteps).toBe(20)
  })

  it("should add to history", () => {
    const { result } = renderHook(() => useWebExplorer(123))

    act(() => {
      result.current.addToHistory({
        started_at: new Date().toISOString(),
        start_url: "https://example.com",
        objective: "Test",
        max_steps: 10,
        report: { summary: "test" },
        console_lines: ["log1", "log2"]
      })
    })

    expect(result.current.exploreHistory).toHaveLength(1)
    expect(result.current.exploreHistory[0].start_url).toBe("https://example.com")
    expect(result.current.exploreHistory[0].objective).toBe("Test")
  })

  it("should clear history", () => {
    const { result } = renderHook(() => useWebExplorer(123))

    // Add some history first
    act(() => {
      result.current.addToHistory({
        started_at: new Date().toISOString(),
        start_url: "https://example.com",
        objective: "Test",
        max_steps: 10,
        report: undefined,
        console_lines: []
      })
    })

    expect(result.current.exploreHistory).toHaveLength(1)

    // Clear history
    act(() => {
      result.current.clearHistory()
    })

    expect(result.current.exploreHistory).toEqual([])
  })

  it("should reset explore state", () => {
    const { result } = renderHook(() => useWebExplorer())

    // Set some state
    act(() => {
      result.current.setExploreReport({ test: true })
      result.current.setExploreConsoleLines(["log1"])
      result.current.setExploreLivePreview("preview")
    })

    expect(result.current.exploreReport).toEqual({ test: true })

    // Reset state
    act(() => {
      result.current.resetExploreState()
    })

    expect(result.current.exploreReport).toBeNull()
    expect(result.current.exploreConsoleLines).toEqual([])
    expect(result.current.exploreLivePreview).toBe("")
  })

  it("should limit history to EXPLORE_HISTORY_LIMIT", () => {
    const { result } = renderHook(() => useWebExplorer(123))

    // Add 25 items one at a time (more than limit of 20)
    for (let i = 0; i < 25; i++) {
      act(() => {
        result.current.addToHistory({
          started_at: new Date().toISOString(),
          start_url: "https://example.com/" + i,
          objective: "Test " + i,
          max_steps: 10,
          report: undefined,
          console_lines: []
        })
      })
    }

    expect(result.current.exploreHistory).toHaveLength(20)
    // Most recent should be first
    expect(result.current.exploreHistory[0].start_url).toBe("https://example.com/24")
  })
})
