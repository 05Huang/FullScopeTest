import { create } from 'zustand'
import { persist } from 'zustand/middleware'
import { projectService, Project } from '@/services/projectService'

interface ProjectState {
  currentProjectId: number | undefined
  projects: Project[]

  setCurrentProject: (id: number | undefined) => void
  fetchProjects: () => Promise<void>
}

export const useProjectStore = create<ProjectState>()(
  persist(
    (set, get) => ({
      currentProjectId: undefined,
      projects: [],

      setCurrentProject: (id) => {
        set({ currentProjectId: id })
      },

      fetchProjects: async () => {
        try {
          const res = await projectService.getProjects()
          if (res.code === 200) {
            const projects = res.data?.items || []
            set({ projects })

            // 如果当前选中的项目不在列表中，自动选择第一个
            const { currentProjectId } = get()
            if (projects.length > 0 && !projects.find((p: Project) => p.id === currentProjectId)) {
              set({ currentProjectId: projects[0].id })
            }
          }
        } catch {
          // 静默失败，不影响主流程
        }
      },
    }),
    {
      name: 'fullscopetest-project',
    }
  )
)
