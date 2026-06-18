import { describe, it, expect, vi, beforeEach } from "vitest"
import { render, screen } from "@testing-library/react"
import { BrowserRouter } from "react-router-dom"
import ApiTokens from "../ApiTokens"

vi.mock("@/services/api", () => ({
  default: {
    get: vi.fn().mockResolvedValue({ data: { data: [], total: 0 } }),
    post: vi.fn().mockResolvedValue({ data: { data: { token: "test" } } }),
    delete: vi.fn().mockResolvedValue({ data: { message: "ok" } }),
  },
}))

vi.mock("@/services/tokenService", () => ({
  default: {
    getTokens: vi.fn().mockResolvedValue({ data: [], total: 0 }),
    createToken: vi.fn().mockResolvedValue({ data: { token: "test-token" } }),
    deleteToken: vi.fn().mockResolvedValue({ message: "ok" }),
  },
}))

vi.mock("react-i18next", () => ({
  useTranslation: () => ({ t: (key: string) => key }),
}))

const renderApiTokens = () =>
  render(
    <BrowserRouter>
      <ApiTokens />
    </BrowserRouter>
  )

describe("ApiTokens Page", () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it("should render without crashing", () => {
    renderApiTokens()
    expect(document.body).toBeTruthy()
  })

  it("should render page title", () => {
    renderApiTokens()
    expect(screen.getByText("tokens.title")).toBeTruthy()
  })

  it("should render create button", () => {
    renderApiTokens()
    expect(screen.getByText("tokens.create")).toBeTruthy()
  })

  it("should render name column", () => {
    renderApiTokens()
    expect(screen.getByText("common.name")).toBeTruthy()
  })

  it("should render project scope column", () => {
    renderApiTokens()
    expect(screen.getByText("tokens.projectScope")).toBeTruthy()
  })

  it("should render empty state", () => {
    renderApiTokens()
    expect(screen.getByText("tokens.noTokens")).toBeTruthy()
  })
})
