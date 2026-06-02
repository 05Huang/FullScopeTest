import { useState, useCallback, useMemo } from "react"

interface UseSearchFilterOptions<T> {
  data: T[]
  searchFields: (keyof T)[]
  filterFn?: (item: T, filters: Record<string, any>) => boolean
}

export function useSearchFilter<T>(options: UseSearchFilterOptions<T>) {
  const [searchText, setSearchText] = useState("")
  const [filters, setFilters] = useState<Record<string, any>>({})

  const filteredData = useMemo(() => {
    let result = options.data

    // 应用搜索
    if (searchText.trim()) {
      const searchLower = searchText.toLowerCase()
      result = result.filter(item =>
        options.searchFields.some(field => {
          const value = item[field]
          if (typeof value === "string") {
            return value.toLowerCase().includes(searchLower)
          }
          if (typeof value === "number") {
            return value.toString().includes(searchLower)
          }
          return false
        })
      )
    }

    // 应用自定义筛选
    if (options.filterFn && Object.keys(filters).length > 0) {
      result = result.filter(item => options.filterFn!(item, filters))
    }

    return result
  }, [options.data, searchText, filters, options.searchFields, options.filterFn])

  const updateFilter = useCallback((key: string, value: any) => {
    setFilters(prev => ({
      ...prev,
      [key]: value
    }))
  }, [])

  const clearFilters = useCallback(() => {
    setSearchText("")
    setFilters({})
  }, [])

  const hasActiveFilters = searchText.trim() !== "" || Object.values(filters).some(v => v !== undefined && v !== null && v !== "")

  return {
    // State
    searchText,
    filters,
    filteredData,
    hasActiveFilters,

    // Setters
    setSearchText,
    setFilters,
    updateFilter,

    // Actions
    clearFilters,
  }
}
