import { useState, useEffect } from "react"
import { message } from "antd"
import { apiTestService } from "@/services/apiTestService"
import type { AiPlanOperation } from "@/services/apiTestService"

type AiLogStatus = "info" | "success" | "error"

interface AiExecutionLog {
  status: AiLogStatus
  message: string
  timestamp: number
}

interface GlobalAiConfig {
  base_url: string
  model: string
  api_key: string
  vision_base_url: string
  vision_model: string
  vision_api_key: string
}

export function useAiAssistant() {
  const [aiDrawerOpen, setAiDrawerOpen] = useState(false)
  const [aiPrompt, setAiPrompt] = useState("")
  const [aiBaseUrl, setAiBaseUrl] = useState("")
  const [aiModel, setAiModel] = useState("")
  const [aiApiKey, setAiApiKey] = useState("")
  const [aiVisionBaseUrl, setAiVisionBaseUrl] = useState("")
  const [aiVisionModel, setAiVisionModel] = useState("")
  const [aiVisionApiKey, setAiVisionApiKey] = useState("")
  const [aiAutoRun, setAiAutoRun] = useState(true)
  const [aiRunning, setAiRunning] = useState(false)
  const [aiSummary, setAiSummary] = useState("")
  const [aiPlanSource, setAiPlanSource] = useState<"llm" | "fallback" | "">("")
  const [aiPlanOperations, setAiPlanOperations] = useState<AiPlanOperation[]>([])
  const [aiExecutionLogs, setAiExecutionLogs] = useState<AiExecutionLog[]>([])

  const [globalAiConfig, setGlobalAiConfig] = useState<GlobalAiConfig | null>(null)
  const [loadingConfig, setLoadingConfig] = useState(false)

  const [aiSynthesizeModalOpen, setAiSynthesizeModalOpen] = useState(false)
  const [aiSynthesizeCount, setAiSynthesizeCount] = useState(5)
  const [aiSynthesizing, setAiSynthesizing] = useState(false)
  const [synthesizedCases, setSynthesizedCases] = useState<any[]>([])
  const [synthesizeTargetCollectionId, setSynthesizeTargetCollectionId] = useState<number | undefined>()

  const [aiReviewModalOpen, setAiReviewModalOpen] = useState(false)
  const [aiReviewing, setAiReviewing] = useState(false)
  const [reviewSummary, setReviewSummary] = useState("")
  const [reviewSuggestedCases, setReviewSuggestedCases] = useState<any[]>([])

  // 加载全局 AI 配置
  useEffect(() => {
    if (aiDrawerOpen && !globalAiConfig && !loadingConfig) {
      loadGlobalConfig()
    }
  }, [aiDrawerOpen])

  const loadGlobalConfig = async () => {
    setLoadingConfig(true)
    try {
      const res = await apiTestService.getAiConfig()
      if (res.code === 200 && res.data) {
        setGlobalAiConfig(res.data)
        setAiBaseUrl(res.data.base_url || "")
        setAiModel(res.data.model || "")
        setAiApiKey(res.data.api_key || "")
        setAiVisionBaseUrl(res.data.vision_base_url || "")
        setAiVisionModel(res.data.vision_model || "")
        setAiVisionApiKey(res.data.vision_api_key || "")
      }
    } catch (e) {
      console.error("Failed to load AI config", e)
    } finally {
      setLoadingConfig(false)
    }
  }

  const appendAiLog = (status: AiLogStatus, msg: string) => {
    setAiExecutionLogs(prev => [...prev, { status, message: msg, timestamp: Date.now() }])
  }

  const clearAiLogs = () => {
    setAiExecutionLogs([])
    setAiSummary("")
    setAiPlanSource("")
    setAiPlanOperations([])
  }

  return {
    // State
    aiDrawerOpen, setAiDrawerOpen,
    aiPrompt, setAiPrompt,
    aiBaseUrl, setAiBaseUrl,
    aiModel, setAiModel,
    aiApiKey, setAiApiKey,
    aiVisionBaseUrl, setAiVisionBaseUrl,
    aiVisionModel, setAiVisionModel,
    aiVisionApiKey, setAiVisionApiKey,
    aiAutoRun, setAiAutoRun,
    aiRunning, setAiRunning,
    aiSummary, setAiSummary,
    aiPlanSource, setAiPlanSource,
    aiPlanOperations, setAiPlanOperations,
    aiExecutionLogs, setAiExecutionLogs,
    globalAiConfig, setGlobalAiConfig,
    loadingConfig,
    aiSynthesizeModalOpen, setAiSynthesizeModalOpen,
    aiSynthesizeCount, setAiSynthesizeCount,
    aiSynthesizing, setAiSynthesizing,
    synthesizedCases, setSynthesizedCases,
    synthesizeTargetCollectionId, setSynthesizeTargetCollectionId,
    aiReviewModalOpen, setAiReviewModalOpen,
    aiReviewing, setAiReviewing,
    reviewSummary, setReviewSummary,
    reviewSuggestedCases, setReviewSuggestedCases,

    // Functions
    loadGlobalConfig,
    appendAiLog,
    clearAiLogs,
  }
}
