import { describe, it, expect, vi, beforeEach } from "vitest"
import { render, screen, waitFor } from "@testing-library/react"
import { BrowserRouter } from "react-router-dom"
import TeamMetrics from "../TeamMetrics"

vi.mock("@/services/api", () => ({
  default: {
    get: vi.fn().mockResolvedValue({ data: { data: {} } }),
  },
}))

vi.mock("@/services/teamMetricsService", () => ({
  default: {
    getTeamMetrics: vi.fn().mockResolvedValue({
      code: 200,
      data: {
        members: [],
        summary: {
          total_cases: 10,
          total_executions: 50,
          active_members: 3,
          avg_pass_rate: 0.95,
        },
      },
    }),
  },
}))

vi.mock("react-i18next", () => ({
  useTranslation: () => ({ t: (key: string) => key }),
}))

vi.mock("@/stores/projectStore", () => ({
  useProjectStore: () => ({ currentProjectId: 1, currentProject: { id: 1 } }),
}))

const renderTeamMetrics = () =>
  render(
    <BrowserRouter>
      <TeamMetrics />
    </BrowserRouter>
  )

describe("TeamMetrics Page", () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it("should render without crashing", () => {
    renderTeamMetrics()
    expect(document.body).toBeTruthy()
  })

  it("should render page title", async () => {
    renderTeamMetrics()
    await waitFor(() => {
      expect(screen.getByText("teamMetrics.title")).toBeTruthy()
    })
  })

  it("should render total cases metric", async () => {
    renderTeamMetrics()
    await waitFor(() => {
      expect(screen.getByText("teamMetrics.totalCases")).toBeTruthy()
    })
  })

  it("should render active members metric", async () => {
    renderTeamMetrics()
    await waitFor(() => {
      expect(screen.getByText("teamMetrics.activeMembers")).toBeTruthy()
    })
  })

  it("should render avg pass rate metric", async () => {
    renderTeamMetrics()
    await waitFor(() => {
      const elements = screen.getAllByText(/teamMetrics\.avgPassRate/)
      expect(elements.length).toBeGreaterThan(0)
    })
  })

  it("should render no data message when members empty", async () => {
    renderTeamMetrics()
    await waitFor(() => {
      expect(screen.getByText("teamMetrics.noData")).toBeTruthy()
    })
  })
})
