import { describe, it, expect, vi, beforeEach } from "vitest"
import { render, screen } from "@testing-library/react"
import { BrowserRouter } from "react-router-dom"
import ApiTestCollections from "../ApiTestCollections"

vi.mock("@/services/api", () => ({
  default: {
    get: vi.fn().mockResolvedValue({ data: { data: [] } }),
    post: vi.fn().mockResolvedValue({ data: { data: {} } }),
  },
}))

vi.mock("@/services/apiTestService", () => ({
  apiTestService: {
    getCollections: vi.fn().mockResolvedValue({ data: [] }),
    getCases: vi.fn().mockResolvedValue({ data: [] }),
    deleteCase: vi.fn().mockResolvedValue({ message: "ok" }),
  },
}))

vi.mock("@/stores/projectStore", () => ({
  useProjectStore: () => ({ currentProject: { id: 1 } }),
}))

vi.mock("react-i18next", () => ({
  useTranslation: () => ({ t: (key: string) => key }),
}))

const renderCollections = () =>
  render(
    <BrowserRouter>
      <ApiTestCollections />
    </BrowserRouter>
  )

describe("ApiTestCollections Page", () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it("should render without crashing", () => {
    renderCollections()
    expect(document.body).toBeTruthy()
  })

  it("should render case name column", () => {
    renderCollections()
    expect(screen.getByText("apiTest.caseName")).toBeTruthy()
  })

  it("should render request method column", () => {
    renderCollections()
    expect(screen.getByText("apiTest.requestMethod")).toBeTruthy()
  })

  it("should render request path column", () => {
    renderCollections()
    expect(screen.getByText("apiTest.requestPath")).toBeTruthy()
  })

  it("should render collection column", () => {
    renderCollections()
    expect(screen.getByText("apiTest.collection")).toBeTruthy()
  })

  it("should render updated at column", () => {
    renderCollections()
    expect(screen.getByText("common.updatedAt")).toBeTruthy()
  })
})
