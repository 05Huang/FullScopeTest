import { describe, it, expect, vi, beforeEach } from "vitest"
import { render, screen } from "@testing-library/react"
import { BrowserRouter } from "react-router-dom"
import NotificationSettings from "../NotificationSettings"

vi.mock("@/services/api", () => ({
  default: {
    get: vi.fn().mockResolvedValue({ data: { data: [] } }),
    post: vi.fn().mockResolvedValue({ data: { data: {} } }),
    put: vi.fn().mockResolvedValue({ data: { message: "ok" } }),
    delete: vi.fn().mockResolvedValue({ data: { message: "ok" } }),
  },
}))

vi.mock("react-i18next", () => ({
  useTranslation: () => ({ t: (key: string) => key }),
}))

const renderNotificationSettings = () =>
  render(
    <BrowserRouter>
      <NotificationSettings />
    </BrowserRouter>
  )

describe("NotificationSettings Page", () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it("should render without crashing", () => {
    renderNotificationSettings()
    expect(document.body).toBeTruthy()
  })

  it("should render page title", () => {
    renderNotificationSettings()
    expect(screen.getByText("notifications.title")).toBeTruthy()
  })

  it("should render create button", () => {
    renderNotificationSettings()
    expect(screen.getByText("notifications.create")).toBeTruthy()
  })

  it("should render channel type column", () => {
    renderNotificationSettings()
    expect(screen.getByText("notifications.channelType")).toBeTruthy()
  })

  it("should render webhook URL column", () => {
    renderNotificationSettings()
    expect(screen.getByText("notifications.webhookUrl")).toBeTruthy()
  })

  it("should render empty state", () => {
    renderNotificationSettings()
    expect(screen.getByText("notifications.noConfigs")).toBeTruthy()
  })
})
