import { useTranslation } from 'react-i18next';
import React, { useState, useEffect, useRef } from 'react'
import { useWebExplorer } from './hooks/useWebExplorer'
import {
  Card,
  Table,
  Button,
  Space,
  Input,
  Tag,
  Typography,
  Modal,
  Form,
  Select,
  message,
  Popconfirm,
  Tooltip,
  Badge,
  Alert,
  Image,
  type MenuProps,
} from 'antd'
import {
  PlusOutlined,
  PlayCircleOutlined,
  EditOutlined,
  DeleteOutlined,
  CodeOutlined,
  CopyOutlined,
  ExportOutlined,
  FileTextOutlined,
  SaveOutlined,
  BugOutlined,
  CheckCircleOutlined,
  EyeOutlined,
  RobotOutlined,
  GlobalOutlined,
} from '@ant-design/icons'
import VisualDiffViewer from '@/components/VisualDiffViewer'
import LogViewerModal from './components/LogViewerModal'
import AiExploreModal from './components/AiExploreModal'
import type { ColumnsType } from 'antd/es/table'
import MonacoEditor from '@monaco-editor/react'
import { webTestService } from '@/services/webTestService'
import { runWithConcurrency } from '@/utils/runWithConcurrency'
import ScriptList from './ScriptList'

const { Title, Text } = Typography
const { TextArea } = Input

interface WebTestScript {
  id: number
  name: string
  description: string
  collection_id?: number | null
  collection_name?: string
  target_url?: string
  browser: string
  status: 'passed' | 'failed' | 'pending' | 'running'
  step_count: number
  last_run_at: string
  last_run_duration?: number
  updated_at: string
  script_content: string
  last_result?: {
    success: boolean
    stdout?: string
    stderr?: string
    return_code?: number
    duration?: number
    error?: string
    vision_results?: Array<{
      name: string
      status: 'new' | 'passed' | 'failed'
      mismatch_ratio: number
      mismatch_pixels: number
      total_pixels: number
      baseline_id?: number
      baseline_image_path?: string
      current_image_path?: string
      diff_image_path?: string
    }>
  }
}

interface WebTestCollection {
  id: number
  name: string
  description?: string
  project_id?: number | null
  script_count?: number
}

interface ExploreHistoryItem {
  id: string
  started_at: string
  start_url: string
  objective: string
  max_steps: number
  report: any
  console_lines: string[]
}

const browserConfig: Record<string, { color: string; name: string }> = {
  chromium: { color: 'blue', name: 'Chromium' },
  firefox: { color: 'orange', name: 'Firefox' },
  webkit: { color: 'purple', name: 'WebKit' },
}

const BATCH_ACTION_CONCURRENCY = 5
const EXPLORE_HISTORY_LIMIT = 20

const normalizeScriptStatus = (status?: string): WebTestScript['status'] => {
  if (status === 'success') return 'passed'
  if (status === 'timeout') return 'failed'
  if (status === 'running' || status === 'passed' || status === 'failed') return status
  return 'pending'
}

const getExploreHistoryStorageKey = (userId?: number) => `web-test-ai-explore-history-${userId || 'guest'}`

const loadExploreHistory = (userId?: number): ExploreHistoryItem[] => {
  try {
    const raw = localStorage.getItem(getExploreHistoryStorageKey(userId))
    if (!raw) return []
    const parsed = JSON.parse(raw)
    if (!Array.isArray(parsed)) return []
    return parsed.filter((item) => item && item.id && item.report)
  } catch {
    return []
  }
}

const trimExploreReport = (report: any) => {
  const safeReport = report || {}
  return {
    ...safeReport,
    errors_found: Array.isArray(safeReport.errors_found) ? safeReport.errors_found.slice(0, 200) : [],
    actions_taken: Array.isArray(safeReport.actions_taken) ? safeReport.actions_taken.slice(0, 200) : [],
  }
}

import { useAuthStore } from '@/stores/authStore'

const WebTestScripts = () => {
  const { t } = useTranslation();
  const { user } = useAuthStore()

  const statusConfig: Record<string, { color: string; text: string }> = {
    passed: { color: 'success', text: t('common.passed') },
    failed: { color: 'error', text: t('common.failed') },
    pending: { color: 'default', text: t('webTest.notExecuted') },
    running: { color: 'processing', text: t('common.running') },
  }
  const [loading, setLoading] = useState(false)
  const [scripts, setScripts] = useState<WebTestScript[]>([])
  const [collections, setCollections] = useState<WebTestCollection[]>([])
  const [selectedRowKeys, setSelectedRowKeys] = useState<React.Key[]>([])
  const [isModalOpen, setIsModalOpen] = useState(false)
  const [isCollectionModalOpen, setIsCollectionModalOpen] = useState(false)
  const [editingCollection, setEditingCollection] = useState<WebTestCollection | null>(null)
  const [isCodeModalOpen, setIsCodeModalOpen] = useState(false)
  const [isLogModalOpen, setIsLogModalOpen] = useState(false)
  const [currentScript, setCurrentScript] = useState<WebTestScript | null>(null)
  const [editingScript, setEditingScript] = useState<WebTestScript | null>(null)
  const [runningIds, setRunningIds] = useState<number[]>([])
  const [selectedCollectionId, setSelectedCollectionId] = useState<number | undefined>(undefined)
  const [searchText, setSearchText] = useState('')
  const [form] = Form.useForm()
  const [collectionForm] = Form.useForm()
  const [isEditingCode, setIsEditingCode] = useState(false)
  const [codeContent, setCodeContent] = useState('')
  const [savingCode, setSavingCode] = useState(false)
  
  // AI Script Generation State
  const [isAiModalOpen, setIsAiModalOpen] = useState(false)
  const [aiPrompt, setAiPrompt] = useState('')
  const [aiGenerating, setAiGenerating] = useState(false)

  // AI Healing State
  const [aiHealing, setAiHealing] = useState(false)
  const [aiAnalysisResult, setAiAnalysisResult] = useState<{ analysis: string; fixed_script: string | null } | null>(null)

  // AI Web Explorer State (使用自定义 hook)
  const {
    isExploreModalOpen, setIsExploreModalOpen,
    exploreStartUrl, setExploreStartUrl,
    exploreObjective, setExploreObjective,
    exploreMaxSteps, setExploreMaxSteps,
    exploreRunning: exploring, setExploreRunning: setExploring,
    exploreReport, setExploreReport,
    exploreConsoleLines, setExploreConsoleLines,
    exploreHistory,
    exploreLivePreview, setExploreLivePreview,
    exploreLiveViewUrl, setExploreLiveViewUrl,
    exploreLiveUrl, setExploreLiveUrl,
    exploreLiveAction, setExploreLiveAction,
    exploreLiveStep, setExploreLiveStep,
    exploreLiveMaxSteps, setExploreLiveMaxSteps,
    exploreAbortRef,
    resetExploreState,
    addToHistory: addExploreHistory,
    clearHistory: clearExploreHistory,
  } = useWebExplorer(user?.id)

  // Visual Diff State
  const [isVisualDiffModalOpen, setIsVisualDiffModalOpen] = useState(false)
  const [selectedVisualDiff, setSelectedVisualDiff] = useState<any>(null)

  // 加载脚本列表
  const loadScripts = async () => {
    setLoading(true)
    try {
      const result = await webTestService.getScripts({
        collection_id: selectedCollectionId,
      })
      if (result.code === 200) {
        const rawScripts = result.data || []
        const normalizedScripts = rawScripts.map((script: any) => ({
          ...script,
          status: normalizeScriptStatus(script.status),
          last_run_duration: script.last_run_duration ?? script.last_duration,
        }))
        setScripts(normalizedScripts)
        const running = normalizedScripts
          .filter((script: WebTestScript) => script.status === 'running')
          .map((script: WebTestScript) => script.id)
        setRunningIds(running)
      } else {
        message.error(result.message || '加载失败')
      }
    } catch (error: any) {
      message.error('加载脚本列表失败')
    } finally {
      setLoading(false)
    }
  }

  const [aiBaseUrl] = useState(() => localStorage.getItem('api-test-ai-base-url') || '')
  const [aiModel] = useState(() => localStorage.getItem('api-test-ai-model') || '')
  const [aiApiKey] = useState(() => localStorage.getItem('api-test-ai-api-key') || '')
  const [aiVisionBaseUrl] = useState(() => localStorage.getItem('api-test-ai-vision-base-url') || '')
  const [aiVisionModel] = useState(() => localStorage.getItem('api-test-ai-vision-model') || '')
  const [aiVisionApiKey] = useState(() => localStorage.getItem('api-test-ai-vision-api-key') || '')

  const loadCollections = async () => {
    try {
      const result = await webTestService.getCollections()
      if (result.code === 200) {
        setCollections(result.data || [])
      }
    } catch (error) {
      console.error('加载用例集失败', error)
    }
  }

  useEffect(() => {
    loadCollections()
  }, [])

  useEffect(() => {
    loadScripts()
  }, [selectedCollectionId])

  useEffect(() => {
    return () => {
      if (exploreAbortRef.current) {
        exploreAbortRef.current.abort()
        exploreAbortRef.current = null
      }
    }
  }, [])

  const openExploreModal = () => {
    if (exploring) return
    resetExploreState()
    setIsExploreModalOpen(true)
  }

  const closeExploreModal = () => {
    if (exploring) return
    setIsExploreModalOpen(false)
    resetExploreState()
  }

  const appendExploreHistory = (payload: {
    start_url: string
    objective: string
    max_steps: number
    report: any
    console_lines: string[]
  }) => {
    addExploreHistory({
      started_at: new Date().toISOString(),
      start_url: payload.start_url,
      objective: payload.objective,
      max_steps: payload.max_steps,
      report: trimExploreReport(payload.report),
      console_lines: payload.console_lines.slice(-300),
    })
  }

  // clearExploreHistory is now from the hook

  // 创建脚本
  const handleCreate = async (values: any) => {
    try {
      const result = await webTestService.createScript({
        name: values.name,
        description: values.description,
        collection_id: values.collection_id ?? null,
        target_url: values.target_url,
        browser: values.browser,
      })
      if (result.code === 200 || result.code === 201) {
        message.success(t('webTest.createSuccess'))
        setIsModalOpen(false)
        setEditingScript(null)
        form.resetFields()
        loadScripts()
      } else {
        message.error(result.message || '创建失败')
      }
    } catch (error: any) {
      message.error('创建脚本失败')
    }
  }

  // AI 辅助生成脚本
  const handleAiGenerate = async () => {
    if (!aiPrompt.trim()) {
      message.warning('请输入描述内容')
      return
    }
    setAiGenerating(true)
    try {
      const res = await webTestService.generateScriptAI({ 
        prompt: aiPrompt,
        base_url: aiBaseUrl,
        model: aiModel,
        api_key: aiApiKey,
        vision_base_url: aiVisionBaseUrl,
        vision_model: aiVisionModel,
        vision_api_key: aiVisionApiKey
      })
      if (res.code === 200 && res.data?.script_content) {
        message.success('AI 脚本生成成功')
        setIsAiModalOpen(false)
        setAiPrompt('')
        
        // 创建一个新脚本并打开代码编辑器
        const createRes = await webTestService.createScript({
          name: t('webTest.aiGenerate') + ' - ' + new Date().toLocaleString(),
          collection_id: selectedCollectionId,
          browser: 'chromium',
          script_content: res.data.script_content,
        })
        if (createRes.code === 200 || createRes.code === 201) {
          loadScripts()
          handleViewCode(createRes.data)
        }
      } else {
        message.error(res.message || '生成失败')
      }
    } catch (e: any) {
      message.error(e.response?.data?.message || '生成失败')
    } finally {
      setAiGenerating(false)
    }
  }

  // AI 探索性测试
  const handleExplore = async () => {
    if (!exploreStartUrl) {
      message.warning('请输入起始 URL')
      return
    }
    const runtimeConsoleLines: string[] = []
    let reportForHistory: any = null
    const pushExploreLog = (line: string) => {
      const timestamp = new Date().toLocaleTimeString()
      const text = `[${timestamp}] ${line}`
      runtimeConsoleLines.push(text)
      setExploreConsoleLines((prev) => [...prev, text])
    }
    setExploreConsoleLines([])
    setExploreLivePreview('')
    setExploreLiveViewUrl('')
    setExploreLiveUrl(exploreStartUrl)
    setExploreLiveAction('初始化探索会话')
    setExploreLiveStep(0)
    setExploreLiveMaxSteps(exploreMaxSteps)
    pushExploreLog(`启动探索任务，目标 URL: ${exploreStartUrl}`)
    pushExploreLog(`探索目标: ${exploreObjective}`)
    pushExploreLog(`最大步数: ${exploreMaxSteps}`)
    setExploring(true)
    setExploreReport(null)
    if (exploreAbortRef.current) {
      exploreAbortRef.current.abort()
    }
    const controller = new AbortController()
    exploreAbortRef.current = controller
    try {
      pushExploreLog('已发送流式探索请求到后端')
      let streamError = ''
      let finalReport: any = null
      await webTestService.exploreWebAppAIStream({
        start_url: exploreStartUrl,
        objective: exploreObjective,
        max_steps: exploreMaxSteps,
        base_url: aiBaseUrl,
        model: aiModel,
        api_key: aiApiKey,
        vision_base_url: aiVisionBaseUrl,
        vision_model: aiVisionModel,
        vision_api_key: aiVisionApiKey
      }, {
        token: '',
        signal: controller.signal,
        onLog: (line) => {
          if (line) {
            pushExploreLog(line)
          }
        },
        onReport: (report) => {
          finalReport = report
          setExploreReport(report)
        },
        onProgress: (progress) => {
          if (!progress || typeof progress !== 'object') return
          const currentUrl = String(progress.current_url || '').trim()
          if (currentUrl) {
            setExploreLiveUrl(currentUrl)
          }
          const screenshot = String(progress.screenshot || '')
          if (screenshot) {
            setExploreLivePreview(screenshot)
          }
          const step = Number(progress.step || 0)
          if (Number.isFinite(step) && step >= 0) {
            setExploreLiveStep(step)
          }
          const maxSteps = Number(progress.max_steps || exploreMaxSteps)
          if (Number.isFinite(maxSteps) && maxSteps > 0) {
            setExploreLiveMaxSteps(maxSteps)
          }
          const action = String(progress.action || '').trim()
          const phase = String(progress.phase || '').trim()
          const reason = String(progress.reason || '').trim()
          const actionLabel = [phase, action, reason].filter(Boolean).join(' · ')
          if (actionLabel) {
            setExploreLiveAction(actionLabel)
          }
        },
        onLiveView: (payload) => {
          const url = String(payload?.url || '').trim()
          if (url) {
            setExploreLiveViewUrl(url)
            pushExploreLog(`已自动接入真实浏览器引擎视图: ${url}`)
          }
        },
        onError: (errMessage) => {
          streamError = errMessage || '探索任务失败'
          pushExploreLog(`服务端异常: ${streamError}`)
        }
      })
      if (streamError) {
        reportForHistory = {
          ...(finalReport || {}),
          start_url: exploreStartUrl,
          objective: exploreObjective,
          status: 'failed',
          error_message: streamError,
          total_steps_executed: finalReport?.total_steps_executed || 0,
          errors_found: finalReport?.errors_found || [],
          actions_taken: finalReport?.actions_taken || [],
          error_summary: finalReport?.error_summary || { critical: 0, warning: 0, info: 0 },
        }
        message.error(streamError)
      } else if (finalReport) {
        reportForHistory = finalReport
        pushExploreLog(`任务返回状态: ${finalReport.status || 'unknown'}`)
        pushExploreLog(`执行步数: ${finalReport.total_steps_executed || 0}`)
        pushExploreLog(`发现错误数: ${finalReport.errors_found?.length || 0}`)
        if (finalReport.error_summary) {
          pushExploreLog(
            `错误分级统计: critical=${finalReport.error_summary.critical || 0}, warning=${finalReport.error_summary.warning || 0}, info=${finalReport.error_summary.info || 0}`
          )
        }
        const actions = Array.isArray(finalReport.actions_taken) ? finalReport.actions_taken : []
        actions.slice(0, 30).forEach((item: any, index: number) => {
          const actionType = item.type || item.action || 'unknown'
          const target = item.target_id || '-'
          const reason = item.reason || ''
          pushExploreLog(`步骤 ${index + 1}: ${actionType} -> ${target} ${reason}`)
        })
        if (finalReport.status === 'failed') {
          pushExploreLog(`失败原因: ${finalReport.error_message || '未知错误'}`)
          message.error(finalReport.error_message || '探索性测试失败')
        } else {
          pushExploreLog('探索任务已完成')
          message.success('探索性测试完成')
        }
      } else {
        reportForHistory = {
          start_url: exploreStartUrl,
          objective: exploreObjective,
          total_steps_executed: 0,
          visited_urls: [],
          errors_found: [],
          error_summary: { critical: 0, warning: 0, info: 0 },
          actions_taken: [],
          status: 'failed',
          error_message: '未收到探索结果',
        }
        pushExploreLog('未收到探索结果')
        message.error('探索失败')
      }
    } catch (error: any) {
      const errorMessage = error.response?.data?.message || error.message || '探索失败'
      reportForHistory = {
        start_url: exploreStartUrl,
        objective: exploreObjective,
        total_steps_executed: 0,
        visited_urls: [],
        errors_found: [],
        error_summary: { critical: 0, warning: 0, info: 0 },
        actions_taken: [],
        status: 'failed',
        error_message: errorMessage,
      }
      pushExploreLog(`请求异常: ${errorMessage}`)
      message.error(errorMessage)
    } finally {
      if (exploreAbortRef.current === controller) {
        exploreAbortRef.current = null
      }
      appendExploreHistory({
        start_url: exploreStartUrl,
        objective: exploreObjective,
        max_steps: exploreMaxSteps,
        report: reportForHistory || {
          start_url: exploreStartUrl,
          objective: exploreObjective,
          total_steps_executed: 0,
          visited_urls: [],
          errors_found: [],
          error_summary: { critical: 0, warning: 0, info: 0 },
          actions_taken: [],
          status: 'failed',
          error_message: '任务异常结束',
        },
        console_lines: runtimeConsoleLines,
      })
      setExploring(false)
    }
  }

  // 更新脚本
  const handleUpdate = async (id: number, values: any) => {
    try {
      const result = await webTestService.updateScript(id, {
        name: values.name,
        description: values.description,
        collection_id: values.collection_id ?? null,
        target_url: values.target_url,
        browser: values.browser,
      })
      if (result.code === 200) {
        message.success(t('webTest.editSuccess'))
        setIsModalOpen(false)
        setEditingScript(null)
        form.resetFields()
        loadScripts()
      } else {
        message.error(result.message || '更新失败')
      }
    } catch (error: any) {
      message.error('更新脚本失败')
    }
  }

  // 删除脚本
  const handleDelete = async (id: number) => {
    try {
      const result = await webTestService.deleteScript(id)
      if (result.code === 200) {
        message.success(t('webTest.deleteSuccess'))
        loadScripts()
      } else {
        message.error(result.message || '删除失败')
      }
    } catch (error: any) {
      message.error('删除脚本失败')
    }
  }

  // 运行脚本
  const handleRun = async (
    id: number,
    options?: { silent?: boolean }
  ): Promise<boolean> => {
    const silent = !!options?.silent
    setRunningIds((prev) => (prev.includes(id) ? prev : [...prev, id]))
    try {
      const result = await webTestService.runScript(id, true)  // headless = true
      if (result.code === 200 && result.data?.task_id) {
        if (!silent) {
          message.success(t('webTest.scriptSubmitted'))
        }
        loadScripts()
        return true
      } else {
        if (!silent) {
          message.error(result.data?.error || result.message || '执行失败')
        }
        setRunningIds((prev) => prev.filter((i) => i !== id))
        return false
      }
    } catch (error: any) {
      if (!silent) {
        message.error('执行脚本失败')
      }
      setRunningIds((prev) => prev.filter((i) => i !== id))
      return false
    }
  }

  // 查看代码
  const handleViewCode = (script: WebTestScript) => {
    setCurrentScript(script)
    setCodeContent(script.script_content || '')
    setIsEditingCode(false)
    setIsCodeModalOpen(true)
  }

  const handleUpdateScriptContent = async () => {
    if (!currentScript) return
    setSavingCode(true)
    try {
      const result = await webTestService.updateScript(currentScript.id, {
        script_content: codeContent,
      })
      if (result.code === 200) {
        message.success('脚本代码已更新')
        const updatedScript = result.data
        if (updatedScript) {
          setScripts((prev) =>
            prev.map((s) => (s.id === updatedScript.id ? { ...s, ...updatedScript } : s))
          )
          setCurrentScript((prev) =>
            prev ? { ...prev, script_content: codeContent } : prev
          )
        } else if (currentScript) {
          setCurrentScript((prev) =>
            prev ? { ...prev, script_content: codeContent } : prev
          )
          setScripts((prev) =>
            prev.map((s) =>
              s.id === currentScript.id ? { ...s, script_content: codeContent } : s
            )
          )
        }
        setIsEditingCode(false)
      } else {
        message.error(result.message || '更新脚本代码失败')
      }
    } catch (error: any) {
      message.error('更新脚本代码失败')
    } finally {
      setSavingCode(false)
    }
  }

  // 查看执行日志
  const handleViewLog = (script: WebTestScript) => {
    setCurrentScript(script)
    setAiAnalysisResult(null)
    setIsLogModalOpen(true)
  }

  // AI 智能诊断
  const handleAiHeal = async () => {
    if (!currentScript || !currentScript.last_result) return

    const errorLog = currentScript.last_result.stderr || currentScript.last_result.error || ''
    if (!errorLog) {
      message.info('当前日志没有发现错误信息')
      return
    }

    setAiHealing(true)
    setAiAnalysisResult(null)
    try {
      const res = await webTestService.analyzeErrorAI({
        script_id: currentScript.id,
        error_log: errorLog,
        base_url: aiBaseUrl,
        model: aiModel,
        api_key: aiApiKey,
        vision_base_url: aiVisionBaseUrl,
        vision_model: aiVisionModel,
        vision_api_key: aiVisionApiKey
      })
      if (res.code === 200 && res.data) {
        setAiAnalysisResult(res.data)
        message.success('AI 诊断完成')
      } else {
        message.error(res.message || 'AI 诊断失败')
      }
    } catch (error: any) {
      message.error(error.response?.data?.message || 'AI 诊断失败')
    } finally {
      setAiHealing(false)
    }
  }

  // 应用修复脚本
  const handleApplyFix = async () => {
    if (!currentScript || !aiAnalysisResult?.fixed_script) return
    
    try {
      const result = await webTestService.updateScript(currentScript.id, {
        script_content: aiAnalysisResult.fixed_script,
      })
      if (result.code === 200) {
        message.success('已应用修复，请重新运行测试')
        setIsLogModalOpen(false)
        loadScripts()
        // 可选：直接打开代码编辑器查看修复后的代码
        handleViewCode({ ...currentScript, script_content: aiAnalysisResult.fixed_script })
      } else {
        message.error(result.message || '应用修复失败')
      }
    } catch (error) {
      message.error('应用修复失败')
    }
  }

  // 批量删除
  const handleBatchDelete = async () => {
    if (selectedRowKeys.length === 0) return
    const ids = selectedRowKeys.map((id) => id as number)
    try {
      const results = await runWithConcurrency(
        ids,
        BATCH_ACTION_CONCURRENCY,
        async (id) => {
          try {
            const result = await webTestService.deleteScript(id)
            return result.code === 200
          } catch {
            return false
          }
        }
      )
      const successCount = results.filter(Boolean).length
      const failedCount = ids.length - successCount

      if (failedCount === 0) {
        message.success(t('webTest.batchDeleteSuccess'))
      } else {
        message.warning(`批量删除完成，成功 ${successCount}，失败 ${failedCount}`)
      }
      setSelectedRowKeys([])
      loadScripts()
    } catch (error) {
      message.error(t('webTest.deleteFailed'))
    }
  }

  // 批量运行
  const handleBatchRun = async () => {
    if (selectedRowKeys.length === 0) return
    const ids = selectedRowKeys.map((id) => id as number)
    message.info(`正在执行 ${ids.length} 个脚本，并发度 ${BATCH_ACTION_CONCURRENCY}`)
    const results = await runWithConcurrency(
      ids,
      BATCH_ACTION_CONCURRENCY,
      (id) => handleRun(id, { silent: true })
    )
    const successCount = results.filter(Boolean).length
    const failedCount = ids.length - successCount

    if (failedCount === 0) {
      message.success(`批量运行已提交，成功 ${successCount} 个`)
    } else {
      message.warning(`批量运行完成，成功 ${successCount}，失败 ${failedCount}`)
    }
    setSelectedRowKeys([])
  }

  // 导出脚本
  const handleExport = () => {
    if (selectedRowKeys.length === 0) return

    const selectedScripts = scripts.filter(s => selectedRowKeys.includes(s.id))
    const exportData = {
      version: '1.0',
      export_time: new Date().toISOString(),
      scripts: selectedScripts.map(s => ({
        name: s.name,
        description: s.description,
        target_url: s.target_url,
        browser: s.browser,
        script_content: s.script_content,
        collection_id: s.collection_id,
      }))
    }

    const blob = new Blob([JSON.stringify(exportData, null, 2)], { type: 'application/json' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `web-test-scripts-${new Date().toISOString().slice(0, 10)}.json`
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    URL.revokeObjectURL(url)

    message.success(`已导出 ${selectedScripts.length} 个脚本`)
  }

  const handleRunCollection = async () => {
    if (!selectedCollectionId) {
      message.warning('请先选择用例集')
      return
    }

    try {
      const result = await webTestService.runCollection(selectedCollectionId)
      if (result.code === 200) {
        const submitted = result.data?.submitted_count ?? 0
        const skipped = (result.data?.skipped || []).length
        message.success(`批量提交完成，提交 ${submitted}，跳过 ${skipped}`)
        loadScripts()
      } else {
        message.error(result.message || '批量执行失败')
      }
    } catch (error) {
      message.error(t('webTest.batchRunComplete'))
    }
  }

  const handleCreateCollection = async (values: any) => {
    try {
      if (editingCollection) {
        const result = await webTestService.updateCollection(editingCollection.id, {
          name: values.name,
          description: values.description,
        })
        if (result.code === 200) {
          message.success(t('webTest.collectionEditSuccess'))
          setEditingCollection(null)
          collectionForm.resetFields()
          loadCollections()
        } else {
          message.error(result.message || t('webTest.collectionCreateFailed'))
        }
      } else {
        const result = await webTestService.createCollection({
          name: values.name,
          description: values.description,
        })
        if (result.code === 200 || result.code === 201) {
          message.success(t('webTest.collectionCreateSuccess'))
          collectionForm.resetFields()
          loadCollections()
        } else {
          message.error(result.message || t('webTest.collectionCreateFailed'))
        }
      }
    } catch (error) {
      message.error(t('webTest.collectionCreateFailed'))
    }
  }

  const handleDeleteCollection = async (id: number) => {
    try {
      const result = await webTestService.deleteCollection(id)
      if (result.code === 200) {
        message.success(t('webTest.collectionDeleted'))
        if (selectedCollectionId === id) {
          setSelectedCollectionId(undefined)
        }
        loadCollections()
        loadScripts()
      } else {
        message.error(result.message || t('webTest.collectionDeleteFailed'))
      }
    } catch (error) {
      message.error(t('webTest.collectionDeleteFailed'))
    }
  }

  // 表格列配置
  const columns: ColumnsType<WebTestScript> = [
    {
      title: t('webTest.scriptName'),
      dataIndex: 'name',
      key: 'name',
      render: (text, record) => (
        <div>
          <Text strong>{text}</Text>
          <br />
          <Text type="secondary" style={{ fontSize: 12 }}>
            {record.description}
          </Text>
          {record.target_url && (
            <>
              <br />
              <Text type="secondary" style={{ fontSize: 12 }}>
                🔗 {record.target_url}
              </Text>
            </>
          )}
        </div>
      ),
    },
    {
      title: t('webTest.collection'),
      dataIndex: 'collection_name',
      key: 'collection_name',
      width: 140,
      render: (value) => value ? <Tag color="geekblue">{value}</Tag> : '-',
    },
    {
      title: t('webTest.browser'),
      dataIndex: 'browser',
      key: 'browser',
      width: 110,
      render: (browser) => (
        <Tag color={browserConfig[browser]?.color || 'default'}>
          {browserConfig[browser]?.name || browser}
        </Tag>
      ),
    },
    {
      title: t('webTest.stepCount'),
      dataIndex: 'step_count',
      key: 'step_count',
      width: 80,
      render: (steps) => <Text>{steps || 0} 步</Text>,
    },
    {
      title: t('webTest.status'),
      dataIndex: 'status',
      key: 'status',
      width: 100,
      render: (status, record) => {
        const isRunning = runningIds.includes(record.id)
        const displayStatus = isRunning ? 'running' : (status || 'pending')
        return (
          <Badge
            status={
              displayStatus === 'running'
                ? 'processing'
                : displayStatus === 'passed'
                ? 'success'
                : displayStatus === 'failed'
                ? 'error'
                : 'default'
            }
            text={statusConfig[displayStatus]?.text || displayStatus}
          />
        )
      },
    },
    {
      title: t('webTest.lastRun'),
      dataIndex: 'last_run_at',
      key: 'last_run_at',
      width: 160,
      render: (text) => text || '-',
    },
    {
      title: t('apiTest.time'),
      dataIndex: 'last_run_duration',
      key: 'last_run_duration',
      width: 80,
      render: (duration) => (duration ? `${duration.toFixed(1)}s` : '-'),
    },
    {
      title: t('webTest.action'),
      key: 'action',
      width: 200,
      render: (_, record) => (
        <Space>
          <Tooltip title="运行">
            <Button
              type="text"
              size="small"
              icon={<PlayCircleOutlined style={{ color: '#52c41a' }} />}
              disabled={runningIds.includes(record.id)}
              loading={runningIds.includes(record.id)}
              onClick={() => handleRun(record.id)}
            />
          </Tooltip>
          <Tooltip title={t('webTest.viewCode')}>
            <Button
              type="text"
              size="small"
              icon={<CodeOutlined />}
              onClick={() => handleViewCode(record)}
            />
          </Tooltip>
          <Tooltip title={t('webTest.executionLog')}>
            <Button
              type="text"
              size="small"
              icon={<FileTextOutlined />}
              onClick={() => handleViewLog(record)}
              disabled={!record.last_result}
            />
          </Tooltip>
          <Tooltip title={t('common.edit')}>
            <Button 
              type="text" 
              size="small" 
              icon={<EditOutlined />}
              onClick={() => {
                setEditingScript(record)
                form.setFieldsValue({
                  name: record.name,
                  description: record.description,
                  collection_id: record.collection_id ?? undefined,
                  target_url: record.target_url,
                  browser: record.browser,
                })
                setIsModalOpen(true)
              }}
            />
          </Tooltip>
          <Popconfirm
            title={t('webTest.confirmDeleteScript')}
            onConfirm={() => handleDelete(record.id)}
          >
            <Tooltip title={t('common.delete')}>
              <Button
                type="text"
                size="small"
                danger
                icon={<DeleteOutlined />}
              />
            </Tooltip>
          </Popconfirm>
        </Space>
      ),
    },
  ]

  // 更多操作菜单
  const moreMenuItems: MenuProps['items'] = [
    { key: 'run', icon: <PlayCircleOutlined />, label: t('webTest.batchRun') },
    { key: 'export', icon: <ExportOutlined />, label: t('webTest.exportScripts') },
    { type: 'divider' },
    { key: 'delete', icon: <DeleteOutlined />, label: t('webTest.batchDelete'), danger: true },
  ]

  return (
    <div className="fst-page">
      <ScriptList
        scripts={scripts} columns={columns} loading={loading}
        searchText={searchText} setSearchText={setSearchText}
        selectedCollectionId={selectedCollectionId} setSelectedCollectionId={setSelectedCollectionId}
        collections={collections}
        selectedRowKeys={selectedRowKeys} setSelectedRowKeys={setSelectedRowKeys}
        onRefresh={loadScripts}
        onCreateCollection={() => setIsCollectionModalOpen(true)}
        onRunCollection={handleRunCollection}
        onAiGenerate={() => setIsAiModalOpen(true)}
        onExplore={openExploreModal}
        onCreateScript={() => { setEditingScript(null); form.resetFields(); form.setFieldsValue({ collection_id: selectedCollectionId }); setIsModalOpen(true) }}
        moreMenuItems={moreMenuItems}
        onMoreClick={({ key }) => {
          if (key === 'delete') handleBatchDelete()
          else if (key === 'run') handleBatchRun()
          else if (key === 'export') handleExport()
        }}
      />

      <Modal
        title={t('webTest.collectionManagement')}
        open={isCollectionModalOpen}
        onCancel={() => {
          setIsCollectionModalOpen(false)
          setEditingCollection(null)
          collectionForm.resetFields()
        }}
        footer={null}
        width={640}
      >
        <Form
          form={collectionForm}
          layout="inline"
          onFinish={handleCreateCollection}
          style={{ marginBottom: 16 }}
        >
          <Form.Item
            name="name"
            rules={[{ required: true, message: t('apiTest.collectionNameRequired') }]}
            style={{ flex: 1 }}
          >
            <Input placeholder={t('webTest.newCollectionName')} />
          </Form.Item>
          <Form.Item name="description" style={{ flex: 1 }}>
            <Input placeholder={t('webTest.collectionDescPlaceholder')} />
          </Form.Item>
          <Form.Item>
            <Button type="primary" htmlType="submit">
              {editingCollection ? t('common.save') : t('common.create')}
            </Button>
          </Form.Item>
        </Form>

        <div style={{ maxHeight: 320, overflow: 'auto' }}>
          {collections.length > 0 ? (
            collections.map((collection) => (
              <div
                key={collection.id}
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'space-between',
                  padding: '8px 12px',
                  borderBottom: '1px solid #f0f0f0',
                }}
              >
                <div>
                  <Text strong>{collection.name}</Text>
                  <Text type="secondary" style={{ marginLeft: 8 }}>
                    ({collection.script_count || 0})
                  </Text>
                  {collection.description ? (
                    <div>
                      <Text type="secondary">{collection.description}</Text>
                    </div>
                  ) : null}
                </div>
                <Space>
                  <Button
                    size="small"
                    icon={<EditOutlined />}
                    onClick={() => {
                      setEditingCollection(collection)
                      collectionForm.setFieldsValue({
                        name: collection.name,
                        description: collection.description || '',
                      })
                    }}
                  />
                  <Popconfirm
                    title={t('webTest.deleteCollectionConfirm')}
                    onConfirm={() => handleDeleteCollection(collection.id)}
                  >
                    <Button danger size="small" icon={<DeleteOutlined />} />
                  </Popconfirm>
                </Space>
              </div>
            ))
          ) : (
            <Text type="secondary">{t('webTest.noCollections')}</Text>
          )}
        </div>
      </Modal>

      {/* 新建/编辑脚本弹窗 */}
      <Modal
        title={editingScript ? "编辑脚本" : "新建脚本"}
        open={isModalOpen}
        onCancel={() => {
          setIsModalOpen(false)
          setEditingScript(null)
          form.resetFields()
        }}
        onOk={() => {
          form.validateFields().then((values) => {
            if (editingScript) {
              handleUpdate(editingScript.id, values)
            } else {
              handleCreate(values)
            }
          })
        }}
        width={600}
      >
        <Form form={form} layout="vertical">
          <Form.Item
            name="name"
            label="脚本名称"
            rules={[{ required: true, message: '请输入脚本名称' }]}
          >
            <Input placeholder="请输入脚本名称" />
          </Form.Item>
          <Form.Item name="description" label={t('common.description')}>
            <TextArea rows={2} placeholder="请输入脚本描述" />
          </Form.Item>
          <Form.Item name="collection_id" label="所属用例集">
            <Select
              allowClear
              placeholder="可选，不选则为未分组"
              options={collections.map((c) => ({
                value: c.id,
                label: c.name,
              }))}
            />
          </Form.Item>
          <Form.Item
            name="browser"
            label="目标浏览器"
            initialValue="chromium"
          >
            <Select
              options={[
                { value: 'chromium', label: 'Chromium' },
                { value: 'firefox', label: 'Firefox' },
                { value: 'webkit', label: 'WebKit (Safari)' },
              ]}
            />
          </Form.Item>
          <Form.Item name="target_url" label="目标 URL">
            <Input placeholder="https://example.com" />
          </Form.Item>
          {/* P38-3: 移动端视口测试 */}
          <Form.Item name="viewport_preset" label="视口尺寸">
            <Select
              allowClear
              placeholder="默认（桌面 1280x720）"
              options={[
                { value: 'desktop', label: '桌面 (1280x720)' },
                { value: 'iphone_se', label: 'iPhone SE (375x667)' },
                { value: 'iphone_14', label: 'iPhone 14 (390x844)' },
                { value: 'iphone_14_pro_max', label: 'iPhone 14 Pro Max (430x932)' },
                { value: 'ipad', label: 'iPad (768x1024)' },
                { value: 'ipad_pro', label: 'iPad Pro (1024x1366)' },
                { value: 'pixel_7', label: 'Pixel 7 (412x915)' },
                { value: 'galaxy_s23', label: 'Galaxy S23 (360x780)' },
                { value: 'custom', label: '自定义分辨率' },
              ]}
            />
          </Form.Item>
        </Form>
      </Modal>

      {/* AI 辅助生成弹窗 */}
      <Modal
        title={
          <Space>
            <RobotOutlined style={{ color: '#722ed1' }} />
            <span>AI 辅助生成测试脚本</span>
          </Space>
        }
        open={isAiModalOpen}
        onCancel={() => {
          if (!aiGenerating) {
            setIsAiModalOpen(false)
            setAiPrompt('')
          }
        }}
        onOk={handleAiGenerate}
        confirmLoading={aiGenerating}
        okText="生成并预览"
      >
        <div style={{ marginBottom: 16 }}>
          <Text type="secondary">
            请输入自然语言描述，AI 将自动生成对应的 Playwright Web UI 测试脚本。
          </Text>
        </div>
        <TextArea
          rows={6}
          placeholder="例如：登录系统，进入控制台，点击新增用户，填写随机生成的用户名，验证是否出现成功提示"
          value={aiPrompt}
          onChange={(e) => setAiPrompt(e.target.value)}
          disabled={aiGenerating}
        />
      </Modal>

      {/* AI 探索性测试弹窗 */}
      <Modal
        title={
          <Space>
            <GlobalOutlined style={{ color: '#3D6E66' }} />
            <span>AI 探索性测试 (Monkey Test)</span>
          </Space>
        }
        open={isExploreModalOpen}
        onCancel={closeExploreModal}
        width={1080}
        footer={
          exploreReport ? (
            <Button onClick={closeExploreModal}>{t('common.close')}</Button>
          ) : (
            <Button
              type="primary"
              onClick={handleExplore}
              loading={exploring}
            >
              开始探索
            </Button>
          )
        }
      >
        {!exploreReport ? (
          <Form layout="vertical">
            <Alert
              type="info"
              showIcon
              message="Autonomous Web Explorer"
              description="提供一个起始 URL，AI 将自动分析页面元素并决定下一步操作（点击、输入等），像真实用户一样在网站中探索并收集报错信息。"
              style={{ marginBottom: 24 }}
            />
            <Form.Item label="起始 URL" required>
              <Input
                placeholder="https://example.com"
                value={exploreStartUrl}
                onChange={(e) => setExploreStartUrl(e.target.value)}
                disabled={exploring}
              />
            </Form.Item>
            <Form.Item label="探索目标">
              <TextArea
                rows={2}
                placeholder="例如：尽可能多地点击不同页面并寻找报错，或者尝试完成下单流程"
                value={exploreObjective}
                onChange={(e) => setExploreObjective(e.target.value)}
                disabled={exploring}
              />
            </Form.Item>
            <Form.Item label="最大探索步数">
              <Select
                value={exploreMaxSteps}
                onChange={setExploreMaxSteps}
                style={{ width: 120 }}
                disabled={exploring}
                options={[
                  { value: 5, label: '5 步 (快速)' },
                  { value: 10, label: '10 步 (标准)' },
                  { value: 20, label: '20 步 (深度)' },
                ]}
              />
            </Form.Item>
            <Alert
              type="info"
              showIcon
              message="系统将自动分配真实浏览器引擎会话"
              description="点击开始探索后，系统会优先自动创建并接入 noVNC/远程浏览器视图；若后端未配置可用模板或会话服务，将自动回退为截图预览。"
              style={{ marginBottom: 16 }}
            />
            {exploreHistory.length > 0 && !exploring && (
              <Form.Item>
                <Card
                  size="small"
                  title={`历史探索记录 (${exploreHistory.length})`}
                  extra={<Button type="link" onClick={clearExploreHistory}>清空记录</Button>}
                >
                  <Table
                    size="small"
                    dataSource={exploreHistory}
                    pagination={false}
                    rowKey="id"
                    columns={[
                      {
                        title: t('common.time'),
                        dataIndex: 'started_at',
                        width: 160,
                        render: (value) => new Date(value).toLocaleString(),
                      },
                      { title: t('webTest.startUrl'), dataIndex: 'start_url', ellipsis: true },
                      {
                        title: t('common.status'),
                        width: 100,
                        render: (_, record: ExploreHistoryItem) => (
                          <Tag color={record.report?.status === 'failed' ? 'red' : 'green'}>
                            {record.report?.status || 'unknown'}
                          </Tag>
                        ),
                      },
                      {
                        title: t('webTest.errorCount'),
                        width: 80,
                        render: (_, record: ExploreHistoryItem) => String(record.report?.errors_found?.length || 0),
                      },
                      {
                        title: t('common.actions'),
                        width: 150,
                        render: (_, record: ExploreHistoryItem) => (
                          <Space size={4}>
                            <Button
                              type="link"
                              size="small"
                              onClick={() => {
                                setExploreReport(record.report)
                                setExploreConsoleLines(record.console_lines || [])
                              }}
                            >
                              查看结果
                            </Button>
                            <Button
                              type="link"
                              size="small"
                              onClick={() => {
                                setExploreStartUrl(record.start_url)
                                setExploreObjective(record.objective)
                                setExploreMaxSteps(record.max_steps)
                              }}
                            >
                              复用参数
                            </Button>
                          </Space>
                        ),
                      },
                    ]}
                  />
                </Card>
              </Form.Item>
            )}
            {(exploring || exploreConsoleLines.length > 0) && (
              <Form.Item>
                <div
                  style={{
                    display: 'grid',
                    gridTemplateColumns: '1fr 1fr',
                    gap: 12,
                  }}
                >
                  <Card size="small" title="命令窗口">
                    <div
                      style={{
                        background: '#0f172a',
                        color: '#e2e8f0',
                        borderRadius: 8,
                        border: '1px solid #1e293b',
                        padding: 12,
                        height: 260,
                        overflowY: 'auto',
                        fontFamily: 'Consolas, Menlo, Monaco, monospace',
                        fontSize: 12,
                        lineHeight: 1.6,
                        whiteSpace: 'pre-wrap',
                      }}
                    >
                      {exploreConsoleLines.length > 0 ? exploreConsoleLines.join('\n') : '等待日志输出...'}
                    </div>
                  </Card>
                  <Card
                    size="small"
                    title="浏览器 UI"
                    extra={<Tag color={exploring ? 'processing' : 'default'}>{exploring ? '探索中' : '已完成'}</Tag>}
                  >
                    <div
                      style={{
                        border: '1px solid #d9d9d9',
                        borderRadius: 8,
                        overflow: 'hidden',
                        background: '#0b1220',
                        height: 260,
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                      }}
                    >
                      {exploreLivePreview ? (
                        <img
                          src={exploreLivePreview}
                          alt="live-browser-preview"
                          style={{ width: '100%', height: '100%', objectFit: 'cover' }}
                        />
                      ) : exploreLiveViewUrl ? (
                        <iframe
                          title="live-browser-engine"
                          src={exploreLiveViewUrl}
                          style={{ width: '100%', height: '100%', border: 0, background: '#fff' }}
                        />
                      ) : (
                        <iframe
                          title="live-browser-fallback"
                          src={exploreLiveUrl || exploreStartUrl || 'about:blank'}
                          style={{ width: '100%', height: '100%', border: 0, background: '#fff' }}
                        />
                      )}
                    </div>
                    <div style={{ marginTop: 8, display: 'flex', justifyContent: 'space-between', gap: 8 }}>
                      <Text type="secondary" ellipsis style={{ maxWidth: '72%' }}>
                        {exploreLiveUrl || exploreStartUrl || '等待页面加载...'}
                      </Text>
                      <Text type="secondary">
                        {exploreLiveStep}/{exploreLiveMaxSteps || exploreMaxSteps} 步
                      </Text>
                    </div>
                    <div style={{ marginTop: 4 }}>
                      <Text type="secondary">{exploreLiveAction || '等待动作...'}</Text>
                    </div>
                  </Card>
                </div>
              </Form.Item>
            )}
          </Form>
        ) : (
          <div style={{ maxHeight: 600, overflow: 'auto' }}>
            {exploreConsoleLines.length > 0 && (
              <Card size="small" title="命令窗口" style={{ marginBottom: 16 }}>
                <div
                  style={{
                    background: '#0f172a',
                    color: '#e2e8f0',
                    borderRadius: 8,
                    border: '1px solid #1e293b',
                    padding: 12,
                    maxHeight: 220,
                    overflowY: 'auto',
                    fontFamily: 'Consolas, Menlo, Monaco, monospace',
                    fontSize: 12,
                    lineHeight: 1.6,
                    whiteSpace: 'pre-wrap',
                  }}
                >
                  {exploreConsoleLines.join('\n')}
                </div>
              </Card>
            )}
            <Alert
              type={exploreReport.status === 'failed' ? 'error' : 'success'}
              message={`探索完成 (状态: ${exploreReport.status})`}
              description={
                exploreReport.error_summary
                  ? `共执行 ${exploreReport.total_steps_executed} 步，错误统计：critical ${exploreReport.error_summary.critical || 0} / warning ${exploreReport.error_summary.warning || 0} / info ${exploreReport.error_summary.info || 0}。`
                  : `共执行 ${exploreReport.total_steps_executed} 步，发现 ${exploreReport.errors_found?.length || 0} 个错误。`
              }
              style={{ marginBottom: 16 }}
            />
            
            <Card size="small" title="发现的错误" style={{ marginBottom: 16 }}>
              {exploreReport.errors_found && exploreReport.errors_found.length > 0 ? (
                <Table
                  size="small"
                  dataSource={exploreReport.errors_found}
                  columns={[
                    { title: t('common.type'), dataIndex: 'type', width: 120, render: (t) => <Tag color="red">{t}</Tag> },
                    {
                      title: t('webTest.level'),
                      dataIndex: 'severity',
                      width: 100,
                      render: (s) => (
                        <Tag color={s === 'critical' ? 'red' : s === 'warning' ? 'orange' : 'blue'}>
                          {s || 'warning'}
                        </Tag>
                      ),
                    },
                    { title: t('webTest.category'), dataIndex: 'category', width: 120, render: (c) => <Tag>{c || '-'}</Tag> },
                    { title: t('webTest.errorMessage'), dataIndex: 'text', ellipsis: true },
                    { title: t('webTest.pageUrl'), dataIndex: 'url', ellipsis: true },
                  ]}
                  pagination={false}
                  rowKey={(_, i) => String(i)}
                />
              ) : (
                <Text type="secondary">未发现明显错误</Text>
              )}
            </Card>

            <Card size="small" title="执行动作轨迹">
              {exploreReport.actions_taken && exploreReport.actions_taken.length > 0 ? (
                <Table
                  size="small"
                  dataSource={exploreReport.actions_taken}
                  columns={[
                    { title: t('webTest.step'), dataIndex: 'step', width: 60 },
                    { title: t('webTest.action'), dataIndex: 'type', width: 80, render: (val) => <Tag color="blue">{val}</Tag> },
                    { title: t('webTest.target'), dataIndex: 'target_id' },
                    { title: t('webTest.reason'), dataIndex: 'reason', ellipsis: true },
                  ]}
                  pagination={false}
                  rowKey={(_, i) => String(i)}
                />
              ) : (
                <Text type="secondary">无动作记录</Text>
              )}
            </Card>
          </div>
        )}
      </Modal>

      {/* 查看代码弹窗 */}
      <Modal
        title={currentScript ? `脚本代码 - ${currentScript.name}` : '脚本代码'}
        open={isCodeModalOpen}
        onCancel={() => {
          setIsCodeModalOpen(false)
          setCurrentScript(null)
          setIsEditingCode(false)
        }}
        footer={
          isEditingCode
            ? [
                <Button
                  key="cancel"
                  onClick={() => {
                    if (currentScript) {
                      setCodeContent(currentScript.script_content || '')
                    }
                    setIsEditingCode(false)
                  }}
                >
                  {t('common.cancel')}
                </Button>,
                <Button
                  key="save"
                  type="primary"
                  icon={<SaveOutlined />}
                  loading={savingCode}
                  onClick={handleUpdateScriptContent}
                >
                  保存脚本
                </Button>,
              ]
            : [
                <Button
                  key="copy"
                  icon={<CopyOutlined />}
                  onClick={() => {
                    if (currentScript?.script_content) {
                      navigator.clipboard.writeText(currentScript.script_content)
                      message.success('已复制到剪贴板')
                    }
                  }}
                >
                  复制代码
                </Button>,
                <Button
                  key="edit"
                  type="primary"
                  icon={<EditOutlined />}
                  onClick={() => {
                    if (currentScript) {
                      setCodeContent(currentScript.script_content || '')
                      setIsEditingCode(true)
                    }
                  }}
                >
                  {t('webTest.editScript')}
                </Button>,
              ]
        }
        width={800}
      >
        <MonacoEditor
          height={400}
          language="python"
          theme="vs-light"
          value={
            isEditingCode
              ? codeContent
              : currentScript?.script_content || `# ${t('webTest.noScriptContent')}`
          }
          onChange={(value) => {
            if (isEditingCode) {
              setCodeContent(value || '')
            }
          }}
          options={{
            readOnly: !isEditingCode,
            minimap: { enabled: false },
            fontSize: 13,
            scrollBeyondLastLine: false,
            automaticLayout: true,
          }}
        />
      </Modal>

      {/* 执行日志模态框 */}
      <LogViewerModal
        open={isLogModalOpen}
        scriptName={currentScript?.name || ''}
        scriptId={currentScript?.id}
        scriptResult={currentScript?.last_result}
        aiHealing={aiHealing}
        aiAnalysisResult={aiAnalysisResult}
        token={''}
        onClose={() => {
          setIsLogModalOpen(false)
          setCurrentScript(null)
          setAiAnalysisResult(null)
        }}
        onAiHeal={handleAiHeal}
        onApplyFix={handleApplyFix}
        onViewVisualDiff={(diff) => {
          setSelectedVisualDiff(diff)
          setIsVisualDiffModalOpen(true)
        }}
      />

      {/* Visual Diff Viewer Modal */}
      <Modal
        title="视觉对比查看器"
        open={isVisualDiffModalOpen}
        onCancel={() => {
          setIsVisualDiffModalOpen(false)
          setSelectedVisualDiff(null)
        }}
        footer={null}
        width={1200}
      >
        {selectedVisualDiff && (
          <VisualDiffViewer
            baselineId={selectedVisualDiff.baselineId}
            baselineImagePath={selectedVisualDiff.baselineImagePath}
            currentImagePath={selectedVisualDiff.currentImagePath}
            diffPercentage={selectedVisualDiff.diffPercentage}
            status={selectedVisualDiff.status}
            onClose={() => {
              setIsVisualDiffModalOpen(false)
              setSelectedVisualDiff(null)
            }}
            onApprove={() => {
              setIsVisualDiffModalOpen(false)
              setSelectedVisualDiff(null)
              loadScripts()
            }}
          />
        )}
      </Modal>
    </div>
  )
}

export default WebTestScripts
