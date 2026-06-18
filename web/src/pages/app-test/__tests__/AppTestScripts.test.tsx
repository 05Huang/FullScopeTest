import { describe, it, expect, vi, beforeEach } from "vitest"
import { render, screen } from "@testing-library/react"
import { BrowserRouter } from "react-router-dom"
import AppTestScripts from "../AppTestScripts"

vi.mock("@/services/api", () => ({
  default: {
    get: vi.fn().mockResolvedValue({ data: { data: [] } }),
    post: vi.fn().mockResolvedValue({ data: { data: {} } }),
  },
}))

vi.mock("@/services/appTestService", () => ({
  appTestService: {
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

const renderAppTestScripts = () =>
  render(
    <BrowserRouter>
      <AppTestScripts />
    </BrowserRouter>
  )

describe("AppTestScripts Page", () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it("should render without crashing", () => {
    renderAppTestScripts()
    expect(document.body).toBeTruthy()
  })

  it("should render page title", () => {
    renderAppTestScripts()
    expect(screen.getByText("appTest.title")).toBeTruthy()
  })

  it("should render script name column", () => {
    renderAppTestScripts()
    expect(screen.getByText("appTest.scriptName")).toBeTruthy()
  })

  it("should render platform column", () => {
    renderAppTestScripts()
    expect(screen.getByText("appTest.platformLabel")).toBeTruthy()
  })

  it("should render status column", () => {
    renderAppTestScripts()
    expect(screen.getByText("appTest.status")).toBeTruthy()
  })

  it("should render device label column", () => {
    renderAppTestScripts()
    expect(screen.getByText("appTest.deviceLabel")).toBeTruthy()
  })
})
