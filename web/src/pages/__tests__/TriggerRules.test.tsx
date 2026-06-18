import { describe, it, expect, vi, beforeEach } from "vitest"
import { render, screen } from "@testing-library/react"
import { BrowserRouter } from "react-router-dom"
import TriggerRules from "../TriggerRules"

vi.mock("@/services/api", () => ({
  default: {
    get: vi.fn().mockResolvedValue({ data: { data: [] } }),
    post: vi.fn().mockResolvedValue({ data: { data: {} } }),
    delete: vi.fn().mockResolvedValue({ data: { message: "ok" } }),
  },
}))

vi.mock("react-i18next", () => ({
  useTranslation: () => ({ t: (key: string) => key }),
}))

vi.mock("@/stores/projectStore", () => ({
  useProjectStore: () => ({ currentProject: { id: 1 } }),
}))

const renderTriggerRules = () =>
  render(
    <BrowserRouter>
      <TriggerRules />
    </BrowserRouter>
  )

describe("TriggerRules Page", () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it("should render without crashing", () => {
    renderTriggerRules()
    expect(document.body).toBeTruthy()
  })

  it("should render page title", () => {
    renderTriggerRules()
    expect(screen.getByText("triggerRules.title")).toBeTruthy()
  })

  it("should render create button", () => {
    renderTriggerRules()
    expect(screen.getByText("triggerRules.create")).toBeTruthy()
  })

  it("should render name column", () => {
    renderTriggerRules()
    expect(screen.getByText("common.name")).toBeTruthy()
  })

  it("should render trigger event column", () => {
    renderTriggerRules()
    expect(screen.getByText("triggerRules.triggerEvent")).toBeTruthy()
  })

  it("should render empty state", () => {
    renderTriggerRules()
    expect(screen.getByText("triggerRules.noRules")).toBeTruthy()
  })
})
