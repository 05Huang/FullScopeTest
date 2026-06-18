import { describe, it, expect, vi, beforeEach } from "vitest"
import { render, screen } from "@testing-library/react"
import { BrowserRouter } from "react-router-dom"
import AuditLogs from "../AuditLogs"

vi.mock("@/services/api", () => ({
  default: {
    get: vi.fn().mockResolvedValue({ data: { data: [], total: 0 } }),
  },
}))

vi.mock("react-i18next", () => ({
  useTranslation: () => ({ t: (key: string) => key }),
}))

const renderAuditLogs = () =>
  render(
    <BrowserRouter>
      <AuditLogs />
    </BrowserRouter>
  )

describe("AuditLogs Page", () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it("should render without crashing", () => {
    renderAuditLogs()
    expect(document.body).toBeTruthy()
  })

  it("should render page title", () => {
    renderAuditLogs()
    expect(screen.getByText("auditLogs.title")).toBeTruthy()
  })

  it("should render operator column", () => {
    renderAuditLogs()
    expect(screen.getByText("auditLogs.operator")).toBeTruthy()
  })

  it("should render action column", () => {
    renderAuditLogs()
    expect(screen.getByText("auditLogs.action")).toBeTruthy()
  })

  it("should render resource type column", () => {
    renderAuditLogs()
    expect(screen.getByText("auditLogs.resourceType")).toBeTruthy()
  })

  it("should render resource ID column", () => {
    renderAuditLogs()
    expect(screen.getByText("auditLogs.resourceId")).toBeTruthy()
  })
})
