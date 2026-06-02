import { useState } from "react"

interface AiGeneratorState {
  isModalOpen: boolean
  prompt: string
  generating: boolean
  generatedScript: string | null
}

export function useAiScriptGenerator() {
  const [isAiModalOpen, setIsAiModalOpen] = useState(false)
  const [aiPrompt, setAiPrompt] = useState("")
  const [aiGenerating, setAiGenerating] = useState(false)
  const [generatedScript, setGeneratedScript] = useState<string | null>(null)

  const openModal = (initialPrompt?: string) => {
    setAiPrompt(initialPrompt || "")
    setGeneratedScript(null)
    setIsAiModalOpen(true)
  }

  const closeModal = () => {
    setIsAiModalOpen(false)
    setAiPrompt("")
    setGeneratedScript(null)
  }

  const startGeneration = () => {
    setAiGenerating(true)
    setGeneratedScript(null)
  }

  const completeGeneration = (script: string) => {
    setAiGenerating(false)
    setGeneratedScript(script)
  }

  const failGeneration = () => {
    setAiGenerating(false)
  }

  return {
    // State
    isAiModalOpen,
    aiPrompt,
    aiGenerating,
    generatedScript,

    // Setters
    setIsAiModalOpen,
    setAiPrompt,

    // Actions
    openModal,
    closeModal,
    startGeneration,
    completeGeneration,
    failGeneration,
  }
}
