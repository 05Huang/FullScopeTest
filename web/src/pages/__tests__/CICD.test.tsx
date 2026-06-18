import { describe, it, expect, vi, beforeEach } from "vitest"
import { render, screen } from "@testing-library/react"
import { BrowserRouter } from "react-router-dom"
import CICD from "../CICD"

vi.mock("@/services/api", () => ({
  default: {
    get: vi.fn().mockResolvedValue({ data: { data: [] } }),
    post: vi.fn().mockResolvedValue({ data: { data: {} } }),
    delete: vi.fn().mockResolvedValue({ data: { message: "ok" } }),
  },
}))

vi.mock("@/services/cicdService", () => ({
  cicdService: {
    getWebhooks: vi.fn().mockResolvedValue({ data: [] }),
    getSchedules: vi.fn().mockResolvedValue({ data: [] }),
    getTargetOptions: vi.fn().mockResolvedValue({ data: [] }),
  },
}))

vi.mock("@/stores/projectStore", () => ({
  useProjectStore: () => ({ currentProjectId: 1, currentProject: { id: 1 } }),
}))

vi.mock("react-i18next", () => ({
  useTranslation: () => ({ t: (key: string) => key }),
}))

const renderCICD = () =>
  render(
    <BrowserRouter>
      <CICD />
    </BrowserRouter>
  )

describe("CICD Page", () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it("should render without crashing", () => {
    renderCICD()
    expect(document.body).toBeTruthy()
  })

  it("should render page title", () => {
    renderCICD()
    expect(screen.getByText("sidebar.cicd")).toBeTruthy()
  })

  it("should render webhook tab", () => {
    renderCICD()
    expect(screen.getByText(/cicd.webhookTab/)).toBeTruthy()
  })

  it("should render schedule tab", () => {
    renderCICD()
    expect(screen.getByText(/cicd.scheduleTab/)).toBeTruthy()
  })

  it("should render new webhook button", () => {
    renderCICD()
    expect(screen.getByText("cicd.newWebhook")).toBeTruthy()
  })

  it("should render task name column", () => {
    renderCICD()
    expect(screen.getByText("cicd.taskName")).toBeTruthy()
  })
})
