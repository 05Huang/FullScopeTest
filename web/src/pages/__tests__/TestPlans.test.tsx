import { describe, it, expect, vi, beforeEach } from "vitest"
import { render, screen } from "@testing-library/react"
import { BrowserRouter } from "react-router-dom"
import TestPlans from "../TestPlans"

vi.mock("@/services/api", () => ({
  default: {
    get: vi.fn().mockResolvedValue({ data: { data: [] } }),
    post: vi.fn().mockResolvedValue({ data: { data: {} } }),
    delete: vi.fn().mockResolvedValue({ data: { message: "ok" } }),
  },
}))

vi.mock("@/services/testPlanService", () => ({
  testPlanService: {
    getTestPlans: vi.fn().mockResolvedValue({ data: [] }),
    createTestPlan: vi.fn().mockResolvedValue({ data: {} }),
  },
}))

vi.mock("@/stores/projectStore", () => ({
  useProjectStore: () => ({ currentProjectId: 1, currentProject: { id: 1 } }),
}))

vi.mock("react-i18next", () => ({
  useTranslation: () => ({ t: (key: string) => key }),
}))

const renderTestPlans = () =>
  render(
    <BrowserRouter>
      <TestPlans />
    </BrowserRouter>
  )

describe("TestPlans Page", () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it("should render without crashing", () => {
    renderTestPlans()
    expect(document.body).toBeTruthy()
  })

  it("should render page title", () => {
    renderTestPlans()
    expect(screen.getByText("testPlans.title")).toBeTruthy()
  })

  it("should render create button", () => {
    renderTestPlans()
    expect(screen.getByText("testPlans.create")).toBeTruthy()
  })

  it("should render name column", () => {
    renderTestPlans()
    expect(screen.getByText("common.name")).toBeTruthy()
  })

  it("should render status column", () => {
    renderTestPlans()
    expect(screen.getByText("testPlans.status")).toBeTruthy()
  })

  it("should render empty state", () => {
    renderTestPlans()
    expect(screen.getByText("testPlans.noPlans")).toBeTruthy()
  })
})
