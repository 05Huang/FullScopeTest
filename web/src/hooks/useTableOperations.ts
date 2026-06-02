import { useState, useCallback } from "react"
import { message } from "antd"

interface UseTableOperationsOptions<T> {
  fetchFn: () => Promise<{ code: number; data?: T[] }>
  deleteFn?: (id: number) => Promise<{ code: number; message?: string }>
  onSuccess?: () => void
  onError?: (error: any) => void
}

export function useTableOperations<T extends { id: number }>(
  options: UseTableOperationsOptions<T>
) {
  const [loading, setLoading] = useState(false)
  const [data, setData] = useState<T[]>([])
  const [selectedRowKeys, setSelectedRowKeys] = useState<React.Key[]>([])

  const fetchData = useCallback(async () => {
    setLoading(true)
    try {
      const result = await options.fetchFn()
      if (result.code === 200) {
        setData(result.data || [])
      }
    } catch (error) {
      console.error("Failed to fetch data:", error)
      options.onError?.(error)
    } finally {
      setLoading(false)
    }
  }, [options.fetchFn])

  const deleteItem = useCallback(async (id: number) => {
    if (!options.deleteFn) return

    try {
      const result = await options.deleteFn(id)
      if (result.code === 200) {
        message.success("删除成功")
        await fetchData()
        options.onSuccess?.()
      } else {
        message.error(result.message || "删除失败")
      }
    } catch (error) {
      console.error("Failed to delete item:", error)
      message.error("删除失败")
      options.onError?.(error)
    }
  }, [options.deleteFn, fetchData])

  const deleteSelected = useCallback(async () => {
    if (!options.deleteFn || selectedRowKeys.length === 0) return

    const ids = selectedRowKeys.map(Number)
    let successCount = 0
    let failCount = 0

    for (const id of ids) {
      try {
        const result = await options.deleteFn(id)
        if (result.code === 200) {
          successCount++
        } else {
          failCount++
        }
      } catch {
        failCount++
      }
    }

    if (successCount > 0) {
      message.success("成功删除 " + successCount + " 项")
    }
    if (failCount > 0) {
      message.error("删除失败 " + failCount + " 项")
    }

    setSelectedRowKeys([])
    await fetchData()
  }, [selectedRowKeys, options.deleteFn, fetchData])

  const clearSelection = useCallback(() => {
    setSelectedRowKeys([])
  }, [])

  return {
    // State
    loading,
    data,
    selectedRowKeys,

    // Setters
    setData,
    setSelectedRowKeys,

    // Actions
    fetchData,
    deleteItem,
    deleteSelected,
    clearSelection,
  }
}
