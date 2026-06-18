import { describe, it, expect, vi, beforeEach } from "vitest"
import { render, screen, waitFor } from "@testing-library/react"
import { BrowserRouter } from "react-router-dom"
import Integrations from "../Integrations"

vi.mock("@/services/api", () => ({
  default: {
    get: vi.fn().mockResolvedValue({ data: { data: {} } }),
  },
}))

vi.mock("@/services/integrationService", () => ({
  default: {
    getGitHubConfig: vi.fn().mockResolvedValue({ code: 200, data: { configured: false } }),
    getGitHubStatus: vi.fn().mockResolvedValue({ code: 200, data: { connected: false } }),
    getGitHubAuthUrl: vi.fn().mockResolvedValue({ code: 200, data: { url: "" } }),
    unbindGitHub: vi.fn().mockResolvedValue({ code: 200, data: { message: "ok" } }),
  },
}))

vi.mock("react-i18next", () => ({
  useTranslation: () => ({ t: (key: string) => key }),
}))

const renderIntegrations = () =>
  render(
    <BrowserRouter>
      <Integrations />
    </BrowserRouter>
  )

describe("Integrations Page", () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it("should render without crashing", () => {
    renderIntegrations()
    expect(document.body).toBeTruthy()
  })

  it("should render page title", async () => {
    renderIntegrations()
    await waitFor(() => {
      expect(screen.getByText("integrations.title")).toBeTruthy()
    })
  })

  it("should render subtitle", async () => {
    renderIntegrations()
    await waitFor(() => {
      expect(screen.getByText("integrations.subtitle")).toBeTruthy()
    })
  })

  it("should render GitHub description", async () => {
    renderIntegrations()
    await waitFor(() => {
      expect(screen.getByText("integrations.github.description")).toBeTruthy()
    })
  })

  it("should render GitLab description", async () => {
    renderIntegrations()
    await waitFor(() => {
      expect(screen.getByText("integrations.gitlab.description")).toBeTruthy()
    })
  })

  it("should render Jira description", async () => {
    renderIntegrations()
    await waitFor(() => {
      expect(screen.getByText("integrations.jira.description")).toBeTruthy()
    })
  })
})
