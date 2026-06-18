import { describe, it, expect, vi, beforeEach } from "vitest"
import { render, screen } from "@testing-library/react"
import { BrowserRouter } from "react-router-dom"
import ApiTestEnvironments from "../ApiTestEnvironments"

vi.mock("@/services/api", () => ({
  default: {
    get: vi.fn().mockResolvedValue({ data: { data: [] } }),
    post: vi.fn().mockResolvedValue({ data: { data: {} } }),
  },
}))

vi.mock("@/services/environmentService", () => ({
  environmentService: {
    getEnvironments: vi.fn().mockResolvedValue({ data: [] }),
    createEnvironment: vi.fn().mockResolvedValue({ data: {} }),
  },
}))

vi.mock("@/stores/projectStore", () => ({
  useProjectStore: () => ({ currentProjectId: 1, currentProject: { id: 1 } }),
}))

vi.mock("react-i18next", () => ({
  useTranslation: () => ({ t: (key: string) => key }),
}))

const renderEnvironments = () =>
  render(
    <BrowserRouter>
      <ApiTestEnvironments />
    </BrowserRouter>
  )

describe("ApiTestEnvironments Page", () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it("should render without crashing", () => {
    renderEnvironments()
    expect(document.body).toBeTruthy()
  })

  it("should render env name column", () => {
    renderEnvironments()
    expect(screen.getByText("apiTest.environments.envName")).toBeTruthy()
  })

  it("should render env variables column", () => {
    renderEnvironments()
    expect(screen.getByText("apiTest.environments.envVariables")).toBeTruthy()
  })

  it("should render create button", () => {
    renderEnvironments()
    expect(screen.getByText("新建环境")).toBeTruthy()
  })

  it("should render updated at column", () => {
    renderEnvironments()
    expect(screen.getByText("common.updatedAt")).toBeTruthy()
  })

  it("should render actions column", () => {
    renderEnvironments()
    expect(screen.getByText("common.actions")).toBeTruthy()
  })
})
