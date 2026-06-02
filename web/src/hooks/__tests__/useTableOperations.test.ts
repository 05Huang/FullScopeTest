import { renderHook, act } from "@testing-library/react"
import { describe, it, expect, vi } from "vitest"
import { useTableOperations } from "../useTableOperations"

describe("useTableOperations", () => {
  const mockFetchFn = vi.fn()
  const mockDeleteFn = vi.fn()

  beforeEach(() => {
    vi.clearAllMocks()
  })

  it("should initialize with default values", () => {
    const { result } = renderHook(() => useTableOperations({
      fetchFn: mockFetchFn
    }))

    expect(result.current.loading).toBe(false)
    expect(result.current.data).toEqual([])
    expect(result.current.selectedRowKeys).toEqual([])
  })

  it("should fetch data successfully", async () => {
    const mockData = [{ id: 1, name: "test" }, { id: 2, name: "test2" }]
    mockFetchFn.mockResolvedValue({ code: 200, data: mockData })

    const { result } = renderHook(() => useTableOperations({
      fetchFn: mockFetchFn
    }))

    await act(async () => {
      await result.current.fetchData()
    })

    expect(result.current.loading).toBe(false)
    expect(result.current.data).toEqual(mockData)
  })

  it("should handle fetch error", async () => {
    const mockError = new Error("Fetch failed")
    mockFetchFn.mockRejectedValue(mockError)
    const onError = vi.fn()

    const { result } = renderHook(() => useTableOperations({
      fetchFn: mockFetchFn,
      onError
    }))

    await act(async () => {
      await result.current.fetchData()
    })

    expect(result.current.loading).toBe(false)
    expect(result.current.data).toEqual([])
    expect(onError).toHaveBeenCalledWith(mockError)
  })

  it("should delete item successfully", async () => {
    mockFetchFn.mockResolvedValue({ code: 200, data: [{ id: 1 }] })
    mockDeleteFn.mockResolvedValue({ code: 200 })

    const { result } = renderHook(() => useTableOperations({
      fetchFn: mockFetchFn,
      deleteFn: mockDeleteFn
    }))

    // First fetch data
    await act(async () => {
      await result.current.fetchData()
    })

    // Then delete
    await act(async () => {
      await result.current.deleteItem(1)
    })

    expect(mockDeleteFn).toHaveBeenCalledWith(1)
    // Should fetch again after delete
    expect(mockFetchFn).toHaveBeenCalledTimes(2)
  })

  it("should update selected row keys", () => {
    const { result } = renderHook(() => useTableOperations({
      fetchFn: mockFetchFn
    }))

    act(() => {
      result.current.setSelectedRowKeys([1, 2, 3])
    })

    expect(result.current.selectedRowKeys).toEqual([1, 2, 3])
  })

  it("should clear selection", () => {
    const { result } = renderHook(() => useTableOperations({
      fetchFn: mockFetchFn
    }))

    act(() => {
      result.current.setSelectedRowKeys([1, 2])
    })
    expect(result.current.selectedRowKeys).toEqual([1, 2])

    act(() => {
      result.current.clearSelection()
    })

    expect(result.current.selectedRowKeys).toEqual([])
  })
})
