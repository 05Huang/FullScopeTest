import { create } from 'zustand'
import { devtools } from 'zustand/middleware'

interface PerfTestScenario {
  id: number
  name: string
  description?: string
  project_id: number
  target_url: string
  method: string
  status: string
  created_at: string
  updated_at: string
}

interface PerfTestState {
  // 场景数据
  scenarios: PerfTestScenario[]

  // 当前选中
  activeScenarioId: number | undefined

  // 执行状态
  runningTaskId: string | undefined
  realtimeStats: Record<string, any> | undefined

  // UI 状态
  loading: boolean
  error: string | undefined

  // Actions
  setScenarios: (scenarios: PerfTestScenario[]) => void
  setActiveScenarioId: (id: number | undefined) => void
  setRunningTaskId: (taskId: string | undefined) => void
  setRealtimeStats: (stats: Record<string, any> | undefined) => void
  setLoading: (loading: boolean) => void
  setError: (error: string | undefined) => void

  // 复合操作
  updateScenario: (id: number, updates: Partial<PerfTestScenario>) => void
  removeScenario: (id: number) => void
  addScenario: (scenario: PerfTestScenario) => void
}

export const usePerfTestStore = create<PerfTestState>()(
  devtools(
    (set) => ({
      // 初始状态
      scenarios: [],
      activeScenarioId: undefined,
      runningTaskId: undefined,
      realtimeStats: undefined,
      loading: false,
      error: undefined,

      // Actions
      setScenarios: (scenarios) => set({ scenarios }),
      setActiveScenarioId: (id) => set({ activeScenarioId: id }),
      setRunningTaskId: (taskId) => set({ runningTaskId: taskId }),
      setRealtimeStats: (stats) => set({ realtimeStats: stats }),
      setLoading: (loading) => set({ loading }),
      setError: (error) => set({ error }),

      // 复合操作
      updateScenario: (id, updates) =>
        set((state) => ({
          scenarios: state.scenarios.map((s) =>
            s.id === id ? { ...s, ...updates } : s
          ),
        })),
      removeScenario: (id) =>
        set((state) => ({
          scenarios: state.scenarios.filter((s) => s.id !== id),
          activeScenarioId:
            state.activeScenarioId === id ? undefined : state.activeScenarioId,
        })),
      addScenario: (scenario) =>
        set((state) => ({
          scenarios: [...state.scenarios, scenario],
        })),
    }),
    { name: 'perf-test-store' }
  )
)
