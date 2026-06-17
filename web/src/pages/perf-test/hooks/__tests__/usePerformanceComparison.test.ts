import { renderHook, act } from "@testing-library/react"
import { describe, it, expect } from "vitest"
import { usePerformanceComparison } from "../usePerformanceComparison"

describe("usePerformanceComparison", () => {
  it("should initialize with default values", () => {
    const { result } = renderHook(() => usePerformanceComparison())

    expect(result.current.compareMode).toBe(false)
    expect(result.current.compareIds).toEqual([])
    expect(result.current.compareData).toEqual([])
    expect(result.current.compareMetricsMap).toEqual({})
  })

  it("should toggle compare mode", () => {
    const { result } = renderHook(() => usePerformanceComparison())

    act(() => {
      result.current.toggleCompareMode()
    })
    expect(result.current.compareMode).toBe(true)

    act(() => {
      result.current.toggleCompareMode()
    })
    expect(result.current.compareMode).toBe(false)
  })

  it("should toggle compare id", () => {
    const { result } = renderHook(() => usePerformanceComparison())

    act(() => {
      result.current.toggleCompareId(1)
    })
    expect(result.current.compareIds).toEqual([1])

    act(() => {
      result.current.toggleCompareId(2)
    })
    expect(result.current.compareIds).toEqual([1, 2])

    // Toggle off
    act(() => {
      result.current.toggleCompareId(1)
    })
    expect(result.current.compareIds).toEqual([2])
  })

  it("should limit compare ids to 5", () => {
    const { result } = renderHook(() => usePerformanceComparison())

    act(() => {
      for (let i = 1; i <= 6; i++) {
        result.current.toggleCompareId(i)
      }
    })

    expect(result.current.compareIds).toHaveLength(5)
    expect(result.current.compareIds).toEqual([1, 2, 3, 4, 5])
  })

  it("should add compare data", () => {
    const { result } = renderHook(() => usePerformanceComparison())

    act(() => {
      result.current.addCompareData({ id: 1, name: "test1" })
    })
    expect(result.current.compareData).toHaveLength(1)
    expect(result.current.compareData[0].id).toBe(1)

    // Should not add duplicate
    act(() => {
      result.current.addCompareData({ id: 1, name: "test1" })
    })
    expect(result.current.compareData).toHaveLength(1)
  })

  it("should add compare metrics", () => {
    const { result } = renderHook(() => usePerformanceComparison())

    const metrics = [{ timestamp: "2024-01-01", current_rps: 100, avg_response_time: 200, error_rate: 0.01, active_users: 10 }]

    act(() => {
      result.current.addCompareMetrics(1, metrics)
    })

    expect(result.current.compareMetricsMap[1]).toEqual(metrics)
  })

  it("should clear compare", () => {
    const { result } = renderHook(() => usePerformanceComparison())

    // Add some data first
    act(() => {
      result.current.toggleCompareId(1)
      result.current.addCompareData({ id: 1 })
      result.current.addCompareMetrics(1, [])
    })

    expect(result.current.compareIds).toHaveLength(1)

    // Clear
    act(() => {
      result.current.clearCompare()
    })

    expect(result.current.compareIds).toEqual([])
    expect(result.current.compareData).toEqual([])
    expect(result.current.compareMetricsMap).toEqual({})
  })
})
