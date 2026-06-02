import { renderHook, act } from "@testing-library/react"
import { describe, it, expect } from "vitest"
import { useAiScriptGenerator } from "../useAiScriptGenerator"

describe("useAiScriptGenerator", () => {
  it("should initialize with default values", () => {
    const { result } = renderHook(() => useAiScriptGenerator())

    expect(result.current.isAiModalOpen).toBe(false)
    expect(result.current.aiPrompt).toBe("")
    expect(result.current.aiGenerating).toBe(false)
    expect(result.current.generatedScript).toBeNull()
  })

  it("should open modal", () => {
    const { result } = renderHook(() => useAiScriptGenerator())

    act(() => {
      result.current.openModal("test prompt")
    })

    expect(result.current.isAiModalOpen).toBe(true)
    expect(result.current.aiPrompt).toBe("test prompt")
    expect(result.current.generatedScript).toBeNull()
  })

  it("should close modal", () => {
    const { result } = renderHook(() => useAiScriptGenerator())

    // Open modal first
    act(() => {
      result.current.openModal("test")
    })
    expect(result.current.isAiModalOpen).toBe(true)

    // Close modal
    act(() => {
      result.current.closeModal()
    })

    expect(result.current.isAiModalOpen).toBe(false)
    expect(result.current.aiPrompt).toBe("")
    expect(result.current.generatedScript).toBeNull()
  })

  it("should start generation", () => {
    const { result } = renderHook(() => useAiScriptGenerator())

    act(() => {
      result.current.startGeneration()
    })

    expect(result.current.aiGenerating).toBe(true)
    expect(result.current.generatedScript).toBeNull()
  })

  it("should complete generation", () => {
    const { result } = renderHook(() => useAiScriptGenerator())

    // Start generation
    act(() => {
      result.current.startGeneration()
    })
    expect(result.current.aiGenerating).toBe(true)

    // Complete generation
    act(() => {
      result.current.completeGeneration("generated script content")
    })

    expect(result.current.aiGenerating).toBe(false)
    expect(result.current.generatedScript).toBe("generated script content")
  })

  it("should fail generation", () => {
    const { result } = renderHook(() => useAiScriptGenerator())

    // Start generation
    act(() => {
      result.current.startGeneration()
    })
    expect(result.current.aiGenerating).toBe(true)

    // Fail generation
    act(() => {
      result.current.failGeneration()
    })

    expect(result.current.aiGenerating).toBe(false)
    expect(result.current.generatedScript).toBeNull()
  })

  it("should update prompt", () => {
    const { result } = renderHook(() => useAiScriptGenerator())

    act(() => {
      result.current.setAiPrompt("new prompt")
    })

    expect(result.current.aiPrompt).toBe("new prompt")
  })
})
