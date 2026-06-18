import { describe, it, expect, vi, beforeEach } from "vitest"
import { render, screen } from "@testing-library/react"
import { BrowserRouter } from "react-router-dom"
import WebTestScripts from "../WebTestScripts"

vi.mock("@/services/api", () => ({
  default: {
    get: vi.fn().mockResolvedValue({ data: { data: [] } }),
    post: vi.fn().mockResolvedValue({ data: { data: {} } }),
  },
}))

vi.mock("@/services/webTestService", () => ({
  webTestService: {
    getScripts: vi.fn().mockResolvedValue({ data: [] }),
    getCollections: vi.fn().mockResolvedValue({ data: [] }),
  },
}))

vi.mock("@/stores/projectStore", () => ({
  useProjectStore: () => ({ currentProject: { id: 1 } }),
}))

vi.mock("react-i18next", () => ({
  useTranslation: () => ({ t: (key: string) => key }),
}))

const renderWebTestScripts = () =>
  render(
    <BrowserRouter>
      <WebTestScripts />
    </BrowserRouter>
  )

describe("WebTestScripts Page", () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it("should render without crashing", () => {
    renderWebTestScripts()
    expect(document.body).toBeTruthy()
  })

  it("should render script name column", () => {
    renderWebTestScripts()
    expect(screen.getByText("webTest.scriptName")).toBeTruthy()
  })

  it("should render status column", () => {
    renderWebTestScripts()
    expect(screen.getByText("webTest.status")).toBeTruthy()
  })

  it("should render browser column", () => {
    renderWebTestScripts()
    expect(screen.getByText("webTest.browser")).toBeTruthy()
  })

  it("should render last run column", () => {
    renderWebTestScripts()
    expect(screen.getByText("webTest.lastRun")).toBeTruthy()
  })

  it("should render actions column", () => {
    renderWebTestScripts()
    expect(screen.getByText("webTest.action")).toBeTruthy()
  })
})
