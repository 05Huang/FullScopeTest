import { describe, it, expect, beforeEach } from "vitest"
import { useProjectStore } from "../projectStore"

describe("projectStore", () => {
  beforeEach(() => {
    // Reset store state
    useProjectStore.setState({
      currentProjectId: undefined,
      projects: [],
    })
    localStorage.clear()
  })

  it("should initialize with default values", () => {
    const state = useProjectStore.getState()
    expect(state.currentProjectId).toBeUndefined()
    expect(state.projects).toEqual([])
  })

  it("should set current project", () => {
    const { setCurrentProject } = useProjectStore.getState()

    setCurrentProject(123)

    const state = useProjectStore.getState()
    expect(state.currentProjectId).toBe(123)
  })

  it("should clear current project", () => {
    const { setCurrentProject } = useProjectStore.getState()

    // First set a project
    setCurrentProject(123)
    expect(useProjectStore.getState().currentProjectId).toBe(123)

    // Then clear it
    setCurrentProject(undefined)

    const state = useProjectStore.getState()
    expect(state.currentProjectId).toBeUndefined()
  })

  it("should update project id", () => {
    const { setCurrentProject } = useProjectStore.getState()

    setCurrentProject(123)
    expect(useProjectStore.getState().currentProjectId).toBe(123)

    setCurrentProject(456)
    expect(useProjectStore.getState().currentProjectId).toBe(456)
  })
})
