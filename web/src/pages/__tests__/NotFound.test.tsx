import { describe, it, expect, vi } from "vitest"
import { render, screen, fireEvent } from "@testing-library/react"
import { BrowserRouter } from "react-router-dom"
import NotFound from "../NotFound"

vi.mock("react-i18next", () => ({
  useTranslation: () => ({ t: (key: string) => key }),
}))

const renderNotFound = () =>
  render(
    <BrowserRouter>
      <NotFound />
    </BrowserRouter>
  )

describe("NotFound Page", () => {
  it("should render 404 title", () => {
    renderNotFound()
    expect(screen.getByText("404")).toBeTruthy()
  })

  it("should render not found message", () => {
    renderNotFound()
    expect(screen.getByText("notFound.message")).toBeTruthy()
  })

  it("should render back to home button", () => {
    renderNotFound()
    expect(screen.getByText("notFound.backHome")).toBeTruthy()
  })

  it("should have clickable button", () => {
    renderNotFound()
    const btn = screen.getByText("notFound.backHome")
    expect(btn.tagName).toMatch(/BUTTON|SPAN/i)
  })

  it("should render with centered layout", () => {
    const { container } = renderNotFound()
    const wrapper = container.firstChild as HTMLElement
    expect(wrapper.style.display).toBe("flex")
  })

  it("should contain 404 in content", () => {
    const { container } = renderNotFound()
    expect(container.textContent).toContain("404")
  })
})
