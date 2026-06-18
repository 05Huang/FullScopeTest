import { describe, it, expect, vi, beforeEach } from "vitest"
import { render, screen } from "@testing-library/react"
import { BrowserRouter } from "react-router-dom"
import QualityGates from "../QualityGates"

vi.mock("@/services/api", () => ({
  default: {
    get: vi.fn().mockResolvedValue({ data: { data: [] } }),
    post: vi.fn().mockResolvedValue({ data: { data: {} } }),
    delete: vi.fn().mockResolvedValue({ data: { message: "ok" } }),
  },
}))

vi.mock("@/stores/projectStore", () => ({
  useProjectStore: () => ({ currentProject: { id: 1 } }),
}))

vi.mock("react-i18next", () => ({
  useTranslation: () => ({ t: (key: string) => key }),
}))

const renderQualityGates = () =>
  render(
    <BrowserRouter>
      <QualityGates />
    </BrowserRouter>
  )

describe("QualityGates Page", () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it("should render without crashing", () => {
    renderQualityGates()
    expect(document.body).toBeTruthy()
  })

  it("should render page title", () => {
    renderQualityGates()
    expect(screen.getByText("qualityGates.title")).toBeTruthy()
  })

  it("should render create button", () => {
    renderQualityGates()
    expect(screen.getByText("qualityGates.create")).toBeTruthy()
  })

  it("should render name column", () => {
    renderQualityGates()
    expect(screen.getByText("common.name")).toBeTruthy()
  })

  it("should render status column", () => {
    renderQualityGates()
    expect(screen.getByText("common.status")).toBeTruthy()
  })

  it("should render empty state", () => {
    renderQualityGates()
    expect(screen.getByText("qualityGates.noGates")).toBeTruthy()
  })
})
