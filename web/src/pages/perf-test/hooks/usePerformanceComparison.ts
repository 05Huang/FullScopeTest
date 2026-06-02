import { useState, useCallback } from "react"

interface MetricSample {
  timestamp: string
  current_rps: number
  avg_response_time: number
  error_rate: number
  active_users: number
  [key: string]: any
}

export function usePerformanceComparison() {
  const [compareMode, setCompareMode] = useState(false)
  const [compareIds, setCompareIds] = useState<number[]>([])
  const [compareData, setCompareData] = useState<any[]>([])
  const [compareMetricsMap, setCompareMetricsMap] = useState<Record<number, MetricSample[]>>({})

  const toggleCompareMode = useCallback(() => {
    setCompareMode(prev => !prev)
    if (compareMode) {
      // 退出对比模式时清空选择
      setCompareIds([])
      setCompareData([])
      setCompareMetricsMap({})
    }
  }, [compareMode])

  const toggleCompareId = useCallback((id: number) => {
    setCompareIds(prev => {
      if (prev.includes(id)) {
        return prev.filter(i => i !== id)
      }
      // 最多对比 5 个
      if (prev.length >= 5) {
        return prev
      }
      return [...prev, id]
    })
  }, [])

  const addCompareData = useCallback((data: any) => {
    setCompareData(prev => {
      if (prev.find(d => d.id === data.id)) return prev
      return [...prev, data]
    })
  }, [])

  const addCompareMetrics = useCallback((id: number, metrics: MetricSample[]) => {
    setCompareMetricsMap(prev => ({
      ...prev,
      [id]: metrics
    }))
  }, [])

  const clearCompare = useCallback(() => {
    setCompareIds([])
    setCompareData([])
    setCompareMetricsMap({})
  }, [])

  return {
    // State
    compareMode,
    compareIds,
    compareData,
    compareMetricsMap,

    // Actions
    toggleCompareMode,
    toggleCompareId,
    addCompareData,
    addCompareMetrics,
    clearCompare,
    setCompareMode,
  }
}
