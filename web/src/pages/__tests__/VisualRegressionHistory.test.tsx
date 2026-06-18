import { describe, it, expect, vi, beforeEach } from "vitest"
import { render, screen, waitFor } from "@testing-library/react"
import { MemoryRouter, Route, Routes } from "react-router-dom"
import VisualRegressionHistory from "../VisualRegressionHistory"

vi.mock("@/services/api", () => ({
  default: {
    get: vi.fn().mockResolvedValue({ data: [] }),
  },
}))

vi.mock("react-i18next", () => ({
  useTranslation: () => ({ t: (key: string) => key }),
}))

const renderVisualRegressionHistory = () =>
  render(
    <MemoryRouter initialEntries={["/visual-regression/history/123"]}>
      <Routes>
        <Route path="/visual-regression/history/:testCaseId" element={<VisualRegressionHistory />} />
      </Routes>
    </MemoryRouter>
  )

describe("VisualRegressionHistory Page", () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it("should render without crashing", () => {
    renderVisualRegressionHistory()
    expect(document.body).toBeTruthy()
  })

  it("should render page title with case ID", async () => {
    renderVisualRegressionHistory()
    await waitFor(() => {
      expect(screen.getByText(/视觉回归历史趋势/)).toBeTruthy()
    }, { timeout: 3000 })
  })

  it("should render case ID in title", async () => {
    renderVisualRegressionHistory()
    await waitFor(() => {
      expect(screen.getByText(/123/)).toBeTruthy()
    }, { timeout: 3000 })
  })

  it("should render back button", async () => {
    renderVisualRegressionHistory()
    await waitFor(() => {
      expect(screen.getByText("common.back")).toBeTruthy()
    }, { timeout: 3000 })
  })

  it("should render empty state", async () => {
    renderVisualRegressionHistory()
    await waitFor(() => {
      expect(screen.getByText("暂无视觉回归历史数据")).toBeTruthy()
    }, { timeout: 3000 })
  })

  it("should render page structure", async () => {
    const { container } = renderVisualRegressionHistory()
    await waitFor(() => {
      expect(container.querySelector(".fst-page")).toBeTruthy()
    }, { timeout: 3000 })
  })
})
