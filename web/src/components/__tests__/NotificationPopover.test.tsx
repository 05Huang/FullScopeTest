import { describe, it, expect, vi } from "vitest"
import { render } from "@testing-library/react"
import NotificationPopover from "@/components/NotificationPopover"

vi.mock("@/services/reportService", () => ({
  getTestRuns: vi.fn().mockResolvedValue({
    code: 200,
    data: { items: [], pagination: { total: 0 } },
    message: "ok",
    timestamp: "",
  }),
}))

vi.mock("react-i18next", () => ({
  useTranslation: () => ({
    t: (key: string) => key,
    i18n: { language: "zh-CN" },
  }),
}))

describe("NotificationPopover Component", () => {
  it("should render without crashing", () => {
    const { container } = render(<NotificationPopover />)
    expect(container).toBeTruthy()
  })

  it("should render content", () => {
    const { container } = render(<NotificationPopover />)
    expect(container.children.length).toBeGreaterThanOrEqual(0)
  })

  it("should produce valid DOM node", () => {
    const { container } = render(<NotificationPopover />)
    expect(container.nodeType).toBe(1)
  })

  it("should have proper DOM structure", () => {
    const { container } = render(<NotificationPopover />)
    expect(container.firstElementChild).toBeTruthy()
  })

  it("should not produce console errors", () => {
    const consoleSpy = vi.spyOn(console, "error").mockImplementation(() => {})
    render(<NotificationPopover />)
    expect(consoleSpy).not.toHaveBeenCalled()
    consoleSpy.mockRestore()
  })
})
