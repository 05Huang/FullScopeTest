import { create } from 'zustand'
import { devtools } from 'zustand/middleware'
import type { ApiTestCase, ApiTestCollection, Environment } from '@/types'

interface ApiTestState {
  // 集合数据
  collections: ApiTestCollection[]
  cases: ApiTestCase[]

  // 当前选中
  activeCollectionId: number | undefined
  activeCaseId: number | undefined
  activeCase: ApiTestCase | undefined

  // 环境
  environments: Environment[]
  selectedEnvId: number | undefined

  // UI 状态
  loading: boolean
  error: string | undefined

  // Actions
  setCollections: (collections: ApiTestCollection[]) => void
  setCases: (cases: ApiTestCase[]) => void
  setActiveCollectionId: (id: number | undefined) => void
  setActiveCaseId: (id: number | undefined) => void
  setActiveCase: (testCase: ApiTestCase | undefined) => void
  setEnvironments: (environments: Environment[]) => void
  setSelectedEnvId: (id: number | undefined) => void
  setLoading: (loading: boolean) => void
  setError: (error: string | undefined) => void

  // 复合操作
  updateCase: (id: number, updates: Partial<ApiTestCase>) => void
  removeCase: (id: number) => void
  addCase: (testCase: ApiTestCase) => void
}

export const useApiTestStore = create<ApiTestState>()(
  devtools(
    (set) => ({
      // 初始状态
      collections: [],
      cases: [],
      activeCollectionId: undefined,
      activeCaseId: undefined,
      activeCase: undefined,
      environments: [],
      selectedEnvId: undefined,
      loading: false,
      error: undefined,

      // Actions
      setCollections: (collections) => set({ collections }),
      setCases: (cases) => set({ cases }),
      setActiveCollectionId: (id) => set({ activeCollectionId: id }),
      setActiveCaseId: (id) => set({ activeCaseId: id }),
      setActiveCase: (testCase) => set({ activeCase: testCase }),
      setEnvironments: (environments) => set({ environments }),
      setSelectedEnvId: (id) => set({ selectedEnvId: id }),
      setLoading: (loading) => set({ loading }),
      setError: (error) => set({ error }),

      // 复合操作
      updateCase: (id, updates) =>
        set((state) => ({
          cases: state.cases.map((c) => (c.id === id ? { ...c, ...updates } : c)),
          activeCase:
            state.activeCase?.id === id
              ? { ...state.activeCase, ...updates }
              : state.activeCase,
        })),
      removeCase: (id) =>
        set((state) => ({
          cases: state.cases.filter((c) => c.id !== id),
          activeCase: state.activeCase?.id === id ? undefined : state.activeCase,
          activeCaseId: state.activeCaseId === id ? undefined : state.activeCaseId,
        })),
      addCase: (testCase) =>
        set((state) => ({
          cases: [...state.cases, testCase],
        })),
    }),
    { name: 'api-test-store' }
  )
)
