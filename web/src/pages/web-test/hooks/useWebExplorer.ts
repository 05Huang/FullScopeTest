import { useState, useRef } from "react"

export interface ExploreReport {
  status?: string
  total_steps_executed?: number
  errors_found?: unknown[]
  error_summary?: { critical?: number; warning?: number; info?: number }
  actions_taken?: Array<Record<string, unknown>>
  error_message?: string
  start_url?: string
  objective?: string
  visited_urls?: string[]
  [key: string]: unknown
}

export interface ExploreHistoryItem {
  id: string
  started_at: string
  start_url: string
  objective: string
  max_steps: number
  report: ExploreReport
  console_lines: string[]
}

const EXPLORE_HISTORY_LIMIT = 20

const getExploreHistoryStorageKey = (userId?: number) => 
  "web-test-ai-explore-history-" + (userId || "guest")

const loadExploreHistory = (userId?: number): ExploreHistoryItem[] => {
  try {
    const raw = localStorage.getItem(getExploreHistoryStorageKey(userId))
    if (!raw) return []
    const parsed = JSON.parse(raw)
    return Array.isArray(parsed) ? parsed.slice(0, EXPLORE_HISTORY_LIMIT) : []
  } catch {
    return []
  }
}

const saveExploreHistory = (userId: number | undefined, history: ExploreHistoryItem[]) => {
  localStorage.setItem(
    getExploreHistoryStorageKey(userId),
    JSON.stringify(history.slice(0, EXPLORE_HISTORY_LIMIT))
  )
}

export function useWebExplorer(userId?: number) {
  const [isExploreModalOpen, setIsExploreModalOpen] = useState(false)
  const [exploreStartUrl, setExploreStartUrl] = useState("")
  const [exploreObjective, setExploreObjective] = useState("尽可能多地点击不同页面并寻找报错")
  const [exploreMaxSteps, setExploreMaxSteps] = useState(10)
  const [exploreRunning, setExploreRunning] = useState(false)
  const [exploreReport, setExploreReport] = useState<ExploreReport | null>(null)
  const [exploreConsoleLines, setExploreConsoleLines] = useState<string[]>([])
  const [exploreHistory, setExploreHistory] = useState<ExploreHistoryItem[]>(
    () => loadExploreHistory(userId)
  )
  const [exploreLivePreview, setExploreLivePreview] = useState("")
  const [exploreLiveViewUrl, setExploreLiveViewUrl] = useState("")
  const [exploreLiveUrl, setExploreLiveUrl] = useState("")
  const [exploreLiveAction, setExploreLiveAction] = useState("")
  const [exploreLiveStep, setExploreLiveStep] = useState(0)
  const [exploreLiveMaxSteps, setExploreLiveMaxSteps] = useState(0)
  const exploreAbortRef = useRef<AbortController | null>(null)

  const resetExploreState = () => {
    setExploreReport(null)
    setExploreConsoleLines([])
    setExploreLivePreview("")
    setExploreLiveViewUrl("")
    setExploreLiveUrl("")
    setExploreLiveAction("")
    setExploreLiveStep(0)
    setExploreLiveMaxSteps(0)
  }

  const addToHistory = (item: Omit<ExploreHistoryItem, "id">) => {
    const newItem: ExploreHistoryItem = {
      ...item,
      id: `${Date.now()}-${Math.random().toString(36).slice(2, 8)}`,
    }
    const updated = [newItem, ...exploreHistory].slice(0, EXPLORE_HISTORY_LIMIT)
    setExploreHistory(updated)
    saveExploreHistory(userId, updated)
  }

  const clearHistory = () => {
    setExploreHistory([])
    saveExploreHistory(userId, [])
  }

  const abortExplore = () => {
    if (exploreAbortRef.current) {
      exploreAbortRef.current.abort()
      exploreAbortRef.current = null
    }
  }

  return {
    // State
    isExploreModalOpen, setIsExploreModalOpen,
    exploreStartUrl, setExploreStartUrl,
    exploreObjective, setExploreObjective,
    exploreMaxSteps, setExploreMaxSteps,
    exploreRunning, setExploreRunning,
    exploreReport, setExploreReport,
    exploreConsoleLines, setExploreConsoleLines,
    exploreHistory,
    exploreLivePreview, setExploreLivePreview,
    exploreLiveViewUrl, setExploreLiveViewUrl,
    exploreLiveUrl, setExploreLiveUrl,
    exploreLiveAction, setExploreLiveAction,
    exploreLiveStep, setExploreLiveStep,
    exploreLiveMaxSteps, setExploreLiveMaxSteps,
    exploreAbortRef,

    // Functions
    resetExploreState,
    addToHistory,
    clearHistory,
    abortExplore,
  }
}
