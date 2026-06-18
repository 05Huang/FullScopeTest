import { describe, it, expect, vi } from "vitest"
import { render, screen } from "@testing-library/react"
import { BrowserRouter } from "react-router-dom"
import ServerError from "../ServerError"

const renderServerError = (props = {}) =>
  render(
    <BrowserRouter>
      <ServerError {...props} />
    </BrowserRouter>
  )

describe("ServerError Page", () => {
  it("should render 500 error page", () => {
    renderServerError()
    expect(screen.getByText("服务器错误")).toBeTruthy()
  })

  it("should render error message", () => {
    renderServerError()
    expect(screen.getByText(/服务器处理请求时发生错误/)).toBeTruthy()
  })

  it("should render buttons", () => {
    renderServerError()
    const buttons = screen.getAllByRole("button")
    expect(buttons.length).toBeGreaterThanOrEqual(2)
  })

  it("should render back to home button", () => {
    renderServerError()
    const buttons = screen.getAllByRole("button")
    const homeBtn = buttons.find(b => b.textContent?.includes("返回首页"))
    expect(homeBtn).toBeTruthy()
  })

  it("should display request ID when provided", () => {
    renderServerError({ requestId: "req-abc123" })
    expect(screen.getByText(/req-abc123/)).toBeTruthy()
  })

  it("should not display request ID when not provided", () => {
    renderServerError()
    expect(screen.queryByText(/Request ID/)).toBeNull()
  })
})
