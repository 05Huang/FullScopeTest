import { describe, it, expect, vi, beforeEach } from "vitest"
import { render, screen } from "@testing-library/react"
import { BrowserRouter } from "react-router-dom"
import Documents from "../Documents"

vi.mock("@/services/api", () => ({
  default: {
    get: vi.fn().mockResolvedValue({ data: { data: [] } }),
    post: vi.fn().mockResolvedValue({ data: { data: {} } }),
  },
}))

vi.mock("@/services/documentService", () => ({
  documentService: {
    getDocuments: vi.fn().mockResolvedValue({ data: { items: [] } }),
    createDocument: vi.fn().mockResolvedValue({ data: {} }),
  },
}))

vi.mock("@/stores/projectStore", () => ({
  useProjectStore: () => ({ currentProjectId: 1, currentProject: { id: 1 } }),
}))

vi.mock("react-i18next", () => ({
  useTranslation: () => ({ t: (key: string) => key }),
}))

const renderDocuments = () =>
  render(
    <BrowserRouter>
      <Documents />
    </BrowserRouter>
  )

describe("Documents Page", () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it("should render without crashing", () => {
    renderDocuments()
    expect(document.body).toBeTruthy()
  })

  it("should render no documents message", () => {
    renderDocuments()
    expect(screen.getByText("documents.noDocuments")).toBeTruthy()
  })

  it("should render page container", () => {
    const { container } = renderDocuments()
    expect(container.firstChild).toBeTruthy()
  })

  it("should render card elements", () => {
    const { container } = renderDocuments()
    expect(container.querySelector(".fst-ios-card")).toBeTruthy()
  })

  it("should render empty state", () => {
    renderDocuments()
    expect(screen.getByText("documents.noDocuments")).toBeTruthy()
  })

  it("should have proper page structure", () => {
    const { container } = renderDocuments()
    expect(container.innerHTML.length).toBeGreaterThan(100)
  })
})
