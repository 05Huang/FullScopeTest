import { create } from 'zustand'
import { devtools } from 'zustand/middleware'

interface WebTestScript {
  id: number
  name: string
  collection_id: number
  status: string
  browser?: string
  headless?: boolean
  created_at: string
  updated_at: string
}

interface WebTestCollection {
  id: number
  name: string
  description?: string
  project_id: number
  created_at: string
  updated_at: string
}

interface WebTestState {
  // 集合数据
  collections: WebTestCollection[]
  scripts: WebTestScript[]

  // 当前选中
  activeCollectionId: number | undefined
  activeScriptId: number | undefined

  // UI 状态
  loading: boolean
  error: string | undefined

  // Actions
  setCollections: (collections: WebTestCollection[]) => void
  setScripts: (scripts: WebTestScript[]) => void
  setActiveCollectionId: (id: number | undefined) => void
  setActiveScriptId: (id: number | undefined) => void
  setLoading: (loading: boolean) => void
  setError: (error: string | undefined) => void

  // 复合操作
  updateScript: (id: number, updates: Partial<WebTestScript>) => void
  removeScript: (id: number) => void
  addScript: (script: WebTestScript) => void
}

export const useWebTestStore = create<WebTestState>()(
  devtools(
    (set) => ({
      // 初始状态
      collections: [],
      scripts: [],
      activeCollectionId: undefined,
      activeScriptId: undefined,
      loading: false,
      error: undefined,

      // Actions
      setCollections: (collections) => set({ collections }),
      setScripts: (scripts) => set({ scripts }),
      setActiveCollectionId: (id) => set({ activeCollectionId: id }),
      setActiveScriptId: (id) => set({ activeScriptId: id }),
      setLoading: (loading) => set({ loading }),
      setError: (error) => set({ error }),

      // 复合操作
      updateScript: (id, updates) =>
        set((state) => ({
          scripts: state.scripts.map((s) => (s.id === id ? { ...s, ...updates } : s)),
        })),
      removeScript: (id) =>
        set((state) => ({
          scripts: state.scripts.filter((s) => s.id !== id),
          activeScriptId: state.activeScriptId === id ? undefined : state.activeScriptId,
        })),
      addScript: (script) =>
        set((state) => ({
          scripts: [...state.scripts, script],
        })),
    }),
    { name: 'web-test-store' }
  )
)
