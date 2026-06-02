import { renderHook, act } from "@testing-library/react"
import { describe, it, expect } from "vitest"
import { useSearchFilter } from "../useSearchFilter"

interface TestItem {
  id: number
  name: string
  category: string
}

describe("useSearchFilter", () => {
  const testData: TestItem[] = [
    { id: 1, name: "Apple", category: "fruit" },
    { id: 2, name: "Banana", category: "fruit" },
    { id: 3, name: "Carrot", category: "vegetable" },
    { id: 4, name: "Avocado", category: "fruit" },
  ]

  it("should initialize with default values", () => {
    const { result } = renderHook(() => useSearchFilter({
      data: testData,
      searchFields: ["name"]
    }))

    expect(result.current.searchText).toBe("")
    expect(result.current.filters).toEqual({})
    expect(result.current.filteredData).toEqual(testData)
    expect(result.current.hasActiveFilters).toBe(false)
  })

  it("should filter by search text", () => {
    const { result } = renderHook(() => useSearchFilter({
      data: testData,
      searchFields: ["name"]
    }))

    act(() => {
      result.current.setSearchText("ana")
    })

    expect(result.current.filteredData).toHaveLength(1)
    expect(result.current.filteredData[0].name).toBe("Banana")
    expect(result.current.hasActiveFilters).toBe(true)
  })

  it("should filter case insensitively", () => {
    const { result } = renderHook(() => useSearchFilter({
      data: testData,
      searchFields: ["name"]
    }))

    act(() => {
      result.current.setSearchText("APPLE")
    })

    expect(result.current.filteredData).toHaveLength(1)
    expect(result.current.filteredData[0].name).toBe("Apple")
  })

  it("should search across multiple fields", () => {
    const { result } = renderHook(() => useSearchFilter({
      data: testData,
      searchFields: ["name", "category"]
    }))

    act(() => {
      result.current.setSearchText("fruit")
    })

    expect(result.current.filteredData).toHaveLength(3)
  })

  it("should apply custom filter", () => {
    const { result } = renderHook(() => useSearchFilter({
      data: testData,
      searchFields: ["name"],
      filterFn: (item, filters) => {
        if (filters.category) {
          return item.category === filters.category
        }
        return true
      }
    }))

    act(() => {
      result.current.updateFilter("category", "vegetable")
    })

    expect(result.current.filteredData).toHaveLength(1)
    expect(result.current.filteredData[0].name).toBe("Carrot")
  })

  it("should clear filters", () => {
    const { result } = renderHook(() => useSearchFilter({
      data: testData,
      searchFields: ["name"]
    }))

    act(() => {
      result.current.setSearchText("test")
    })
    expect(result.current.hasActiveFilters).toBe(true)

    act(() => {
      result.current.clearFilters()
    })

    expect(result.current.searchText).toBe("")
    expect(result.current.filters).toEqual({})
    expect(result.current.filteredData).toEqual(testData)
    expect(result.current.hasActiveFilters).toBe(false)
  })
})
