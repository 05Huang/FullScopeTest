import { describe, it, expect, vi } from "vitest"
import { render } from "@testing-library/react"
import { BrowserRouter } from "react-router-dom"
import GlobalSearch from "@/components/GlobalSearch"

vi.mock("@/services/aiSearchService", () => ({
  globalSearchAI: vi.fn().mockResolvedValue({ results: [] }),
}))

vi.mock("react-i18next", () => ({
  useTranslation: () => ({
    t: (key: string) => key,
    i18n: { language: "zh-CN" },
  }),
}))

const renderGlobalSearch = () =>
  render(
    <BrowserRouter>
      <GlobalSearch />
    </BrowserRouter>
  )

describe("GlobalSearch Component", () => {
  it("should render without crashing", () => {
    const { container } = renderGlobalSearch()
    expect(container).toBeTruthy()
  })

  it("should render at least one child element", () => {
    const { container } = renderGlobalSearch()
    expect(container.children.length).toBeGreaterThan(0)
  })

  it("should produce valid DOM node", () => {
    const { container } = renderGlobalSearch()
    expect(container.nodeType).toBe(1)
  })

  it("should not produce console errors on render", () => {
    const consoleSpy = vi.spyOn(console, "error").mockImplementation(() => {})
    renderGlobalSearch()
    expect(consoleSpy).not.toHaveBeenCalled()
    consoleSpy.mockRestore()
  })

  it("should render with proper DOM structure", () => {
    const { container } = renderGlobalSearch()
    expect(container.firstElementChild).toBeTruthy()
  })
})
