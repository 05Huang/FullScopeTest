import { useTranslation } from 'react-i18next';
import { useState, useEffect } from 'react'
import logger from '@/utils/logger'
import {
  Layout,
  Tree,
  Input,
  Button,
  Tabs,
  Select,
  Space,
  Tag,
  Typography,
  Empty,
  Tooltip,
  message,
  Spin,
  Modal,
  Card,
  type MenuProps,
} from 'antd'
import {
  PlusOutlined,
  FolderOutlined,
  FileOutlined,
  DeleteOutlined,
  CopyOutlined,
  SearchOutlined,
  ReloadOutlined,
  CheckCircleOutlined,
  CloseCircleOutlined,
} from '@ant-design/icons'
import type { DataNode } from 'antd/es/tree'
import { apiTestService, type AiPlanOperation } from '@/services/apiTestService'
import { environmentService } from '@/services/environmentService'
import type { ApiTestCase, ApiTestCollection, Environment, TestExecutionResponse } from '@/types'
import { useProjectStore } from '@/stores/projectStore'
import CollectionManager from './CollectionManager'
import EnvironmentVariableHint from './EnvironmentVariableHint'
import ScriptTestResults from './components/ScriptTestResults'
import SaveCaseModal from './components/SaveCaseModal'
import AiSynthesizeModal from './components/AiSynthesizeModal'
import AiReviewModal from './components/AiReviewModal'
import AiAssistantDrawer from './components/AiAssistantDrawer'
import RequestHistory, { saveToHistory } from './components/RequestHistory'
import { snippetGenerators } from '@/utils/codeSnippetGenerator'
import { useAiAssistant } from './hooks/useAiAssistant'
import RequestEditor from './RequestEditor'
import ResponseViewer from './ResponseViewer'
import EnvironmentSelector from './EnvironmentSelector'
import TestRunner, { type CollectionProgress } from './TestRunner'

const { Sider, Content } = Layout
const { Text } = Typography
const { TextArea } = Input

// HTTP 方法颜色
const methodColors: Record<string, string> = {
  GET: '#52c41a',
  POST: '#1890ff',
  PUT: '#faad14',
  DELETE: '#ff4d4f',
  PATCH: '#722ed1',
}

type AiLogStatus = 'info' | 'success' | 'error'

interface AiExecutionLog {
  status: AiLogStatus
  message: string
}

const ApiTestWorkspace = () => {
  const { t } = useTranslation();
  const { currentProjectId } = useProjectStore()
  const [method, setMethod] = useState('GET')
  const [url, setUrl] = useState('')
  const [requestName, setRequestName] = useState('')  // 自定义请求名称
  const [activeTab, setActiveTab] = useState('params')
  const [responseTab, setResponseTab] = useState('body')
  const [sending, setSending] = useState(false)
  const [collectionProgress, setCollectionProgress] = useState<CollectionProgress | null>(null)
  const [response, setResponse] = useState<TestExecutionResponse | null>(null)
  const [assertionResults, setAssertionResults] = useState<{
    total: number; passed: number; failed: number
    details?: Array<{ name: string; passed: boolean; actual?: unknown; expected?: unknown; error?: string; assertion_type?: string }>
  } | undefined>(undefined)
  const [requestBody, setRequestBody] = useState('{}')
  const [bodyType, setBodyType] = useState('json')
  const [headers, setHeaders] = useState<{ key: string; value: string }[]>([{ key: '', value: '' }])
  const [params, setParams] = useState<{ key: string; value: string }[]>([{ key: '', value: '' }])
  // 新增：脚本状态
  const [preScript, setPreScript] = useState('')
  const [postScript, setPostScript] = useState('')
  
  // 新增：Mock 状态
  const [mockEnabled, setMockEnabled] = useState(false)
  const [mockResponseCode, setMockResponseCode] = useState(200)
  const [mockResponseBody, setMockResponseBody] = useState('{\n  "success": true,\n  "data": {}\n}')
  const [mockResponseHeaders, setMockResponseHeaders] = useState<{ key: string; value: string }[]>([{ key: 'Content-Type', value: 'application/json' }])
  const [mockDelayMs, setMockDelayMs] = useState(0)

  // 可视化断言状态
  const [assertions, setAssertions] = useState<Array<{
    type: 'status_code' | 'response_time' | 'header' | 'body'
    operator: string; expected_value: string | number
    header_name?: string; body_path?: string; description?: string; enabled: boolean
  }>>([])

  const [collections, setCollections] = useState<ApiTestCollection[]>([])
  const [cases, setCases] = useState<ApiTestCase[]>([])
  const [treeData, setTreeData] = useState<DataNode[]>([])
  const [selectedTreeKeys, setSelectedTreeKeys] = useState<React.Key[]>([])
  const [expandedTreeKeys, setExpandedTreeKeys] = useState<React.Key[]>([])
  const [saveModalOpen, setSaveModalOpen] = useState(false)
  const [saveCaseName, setSaveCaseName] = useState('')
  const [selectedCollectionId, setSelectedCollectionId] = useState<number | undefined>()
  const [activeCollectionId, setActiveCollectionId] = useState<number | undefined>()
  const [searchText, setSearchText] = useState('')
  const [environments, setEnvironments] = useState<Environment[]>([])
  const [selectedEnvId, setSelectedEnvId] = useState<number | undefined>()
  const [currentEnv, setCurrentEnv] = useState<Environment | null>(null)
  const [sidebarTab, setSidebarTab] = useState<string>('cases') // 侧边栏标签页
  const [hasLoadedData, setHasLoadedData] = useState(false) // 标记数据是否已加载

  // AI 助手状态（使用自定义 hook）
  const {
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
    loadGlobalConfig,
    appendAiLog,
    clearAiLogs,
  } = useAiAssistant()

  // 获取当前项目选择的环境存储键（按项目分别持久化）
  const getEnvStorageKey = (projectId?: number) => {
    return projectId ? `api-test-project-${projectId}-selected-env-id` : 'api-test-selected-env-id'
  }
  const [contextMenuState, setContextMenuState] = useState<{
    visible: boolean
    x: number
    y: number
    caseId: number | null
    caseName: string
  }>({
    visible: false,
    x: 0,
    y: 0,
    caseId: null,
    caseName: ''
  })
  const [currentCaseId, setCurrentCaseId] = useState<number | null>(null)
  const [hasUnsavedChanges, setHasUnsavedChanges] = useState(false)
  const [originalFormData, setOriginalFormData] = useState<{
    name: string; method: string; url: string; requestBody: string
    headers: { key: string; value: string }[]; params: { key: string; value: string }[]
    preScript: string; postScript: string; mockEnabled: boolean
    mockResponseCode: number; mockResponseBody: string
    mockResponseHeaders: { key: string; value: string }[]; mockDelayMs: number
  } | null>(null)

  // 加载用例数据
  useEffect(() => {
    loadData()
    // 恢复表单草稿
    restoreFormDraft()
  }, [])

  // 表单状态自动保存到localStorage
  useEffect(() => {
    const handleClick = () => {
      if (contextMenuState.visible) {
        setContextMenuState({ ...contextMenuState, visible: false })
      }
    }
    document.addEventListener('click', handleClick)
    return () => document.removeEventListener('click', handleClick)
  }, [contextMenuState])

  // 环境选择自动保存到 localStorage（按项目分别持久化）
  // 只在数据加载后执行，避免初始挂载时清除 localStorage
  useEffect(() => {
    if (!hasLoadedData) return // 跳过初始挂载

    const storageKey = getEnvStorageKey(currentProjectId)
    if (selectedEnvId) {
      localStorage.setItem(storageKey, String(selectedEnvId))
    } else {
      localStorage.removeItem(storageKey)
    }
  }, [selectedEnvId, currentProjectId, hasLoadedData])

  // 检测表单修改
  useEffect(() => {
    if (!originalFormData || !currentCaseId) return

    const currentFormData = {
      name: requestName,
      method,
      url,
      requestBody,
      headers: headers.filter(h => h.key || h.value),
      params: params.filter(p => p.key || p.value),
      preScript,
      postScript,
      mockEnabled,
      mockResponseCode,
      mockResponseBody,
      mockResponseHeaders: mockResponseHeaders.filter(h => h.key || h.value),
      mockDelayMs,
    }

    // 简单比较是否有变化
    const hasChanged =
      currentFormData.name !== originalFormData.name ||
      currentFormData.method !== originalFormData.method ||
      currentFormData.url !== originalFormData.url ||
      currentFormData.requestBody !== originalFormData.requestBody ||
      JSON.stringify(currentFormData.headers) !== JSON.stringify(originalFormData.headers) ||
      JSON.stringify(currentFormData.params) !== JSON.stringify(originalFormData.params) ||
      currentFormData.preScript !== originalFormData.preScript ||
      currentFormData.postScript !== originalFormData.postScript ||
      currentFormData.mockEnabled !== originalFormData.mockEnabled ||
      currentFormData.mockResponseCode !== originalFormData.mockResponseCode ||
      currentFormData.mockResponseBody !== originalFormData.mockResponseBody ||
      JSON.stringify(currentFormData.mockResponseHeaders) !== JSON.stringify(originalFormData.mockResponseHeaders) ||
      currentFormData.mockDelayMs !== originalFormData.mockDelayMs

    setHasUnsavedChanges(hasChanged)
  }, [method, url, requestName, requestBody, headers, params, preScript, postScript, mockEnabled, mockResponseCode, mockResponseBody, mockResponseHeaders, mockDelayMs, originalFormData, currentCaseId])

  // 从localStorage恢复表单草稿
  const restoreFormDraft = () => {
    try {
      const draftStr = localStorage.getItem('api-test-form-draft')
      if (draftStr) {
        const draft = JSON.parse(draftStr)
        if (draft.method) setMethod(draft.method)
        if (draft.url) setUrl(draft.url)
        if (draft.requestName) setRequestName(draft.requestName)
        if (draft.requestBody) setRequestBody(draft.requestBody)
        if (draft.bodyType) setBodyType(draft.bodyType)
        if (draft.headers && draft.headers.length > 0) {
          setHeaders([...draft.headers, { key: '', value: '' }])
        }
        if (draft.params && draft.params.length > 0) {
          setParams([...draft.params, { key: '', value: '' }])
        }
        message.open({
          type: 'info',
          content: '已恢复上次未保存的草稿',
          key: 'api-test-form-draft-restored',
        })
      }
    } catch (error) {
      logger.error('恢复草稿失败', error)
    }
  }

  // 新建用例
  const handleNewCase = async () => {
    await handleNewCaseV2()
    return

    // 如果当前正在编辑用例且有未保存修改，先自动保存
    if (currentCaseId && hasUnsavedChanges) {
      try {
        await saveCurrentCase()
      } catch (error) {
        // 保存失败，提示用户但仍继续清空表单
        message.warning('当前用例保存失败，但将继续创建新用例')
      }
    }

    // 清空表单状态
    setUrl('')
    setRequestName('')
    setMethod('GET')
    setRequestBody('{}')
    setHeaders([{ key: '', value: '' }])
    setParams([{ key: '', value: '' }])
    setPreScript('')
    setPostScript('')
    setResponse(null)

    // 重置用例相关状态
    setCurrentCaseId(null)
    setOriginalFormData(null)
    setHasUnsavedChanges(false)

    message.success('已创建新用例')
  }

  const handleNewCaseV2 = async () => {
    if (currentCaseId && hasUnsavedChanges) {
      const saved = await saveCurrentCaseSafely()
      if (!saved) {
        message.error('当前用例自动保存失败，已取消新建')
        return
      }
    }

    setUrl('')
    setRequestName('')
    setMethod('GET')
    setRequestBody('{}')
    setHeaders([{ key: '', value: '' }])
    setParams([{ key: '', value: '' }])
    setPreScript('')
    setPostScript('')
    setResponse(null)
    
    // 重置 Mock 状态
    setMockEnabled(false)
    setMockResponseCode(200)
    setMockResponseBody('{\n  "success": true,\n  "data": {}\n}')
    setMockResponseHeaders([{ key: 'Content-Type', value: 'application/json' }])
    setMockDelayMs(0)

    localStorage.removeItem('api-test-form-draft')

    setCurrentCaseId(null)
    setOriginalFormData(null)
    setHasUnsavedChanges(false)

    if (activeCollectionId) {
      setSelectedCollectionId(activeCollectionId)
      setSelectedTreeKeys([`collection-${activeCollectionId}`])
      setExpandedTreeKeys(prev =>
        prev.includes(`collection-${activeCollectionId}`) ? prev : [...prev, `collection-${activeCollectionId}`]
      )
    } else {
      setSelectedCollectionId(undefined)
      setSelectedTreeKeys(['ungrouped'])
    }

    message.success('已创建空白用例草稿')
  }

  const loadData = async () => {
    try {
      const [collectionsRes, casesRes, environmentsRes] = await Promise.all([
        apiTestService.getCollections(currentProjectId),
        apiTestService.getCases({}),
        environmentService.getEnvironments(currentProjectId)
      ])
      
      if (collectionsRes.code === 200) {
        setCollections(collectionsRes.data || [])
      }
      if (casesRes.code === 200) {
        setCases(casesRes.data || [])
      }
      if (environmentsRes.code === 200) {
        const envs = environmentsRes.data || []
        setEnvironments(envs)

        // 恢复之前选择的环境（按项目）
        const storageKey = getEnvStorageKey(currentProjectId)
        const savedEnvId = localStorage.getItem(storageKey)
        if (savedEnvId) {
          const envId = parseInt(savedEnvId)
          const env = envs.find((e) => e.id === envId)
          if (env) {
            setSelectedEnvId(envId)
            setCurrentEnv(env)
          }
        }
      }

      // 构建树形数据
      buildTreeData(collectionsRes.data || [], casesRes.data || [])

      // 标记数据已加载，启用 localStorage 自动保存
      setHasLoadedData(true)
    } catch (error) {
      logger.error('加载数据失败', error)
    }
  }

  const buildTreeData = (collectionsData: ApiTestCollection[], casesData: ApiTestCase[]) => {
    const tree: DataNode[] = []
    
    // 添加集合节点
    collectionsData.forEach(collection => {
      const collectionCases = casesData.filter(c => c.collection_id === collection.id)
      tree.push({
        title: collection.name,
        key: `collection-${collection.id}`,
        icon: <FolderOutlined />,
        children: collectionCases.map(c => ({
          title: `${c.method} ${c.name}`,
          key: `case-${c.id}`,
          icon: <FileOutlined />,
          isLeaf: true,
          caseData: c,
        }))
      })
    })
    
    // 添加未分组的用例
    const ungroupedCases = casesData.filter(c => !c.collection_id)
    if (ungroupedCases.length > 0) {
      tree.push({
        title: t('apiTest.ungrouped'),
        key: 'ungrouped',
        icon: <FolderOutlined />,
        children: ungroupedCases.map(c => ({
          title: `${c.method} ${c.name}`,
          key: `case-${c.id}`,
          icon: <FileOutlined />,
          isLeaf: true,
          caseData: c,
        }))
      })
    }
    
    setTreeData(tree)
  }

  // 选择用例
  const handleSelectCase = async (keys: React.Key[]) => {
    await handleTreeSelect(keys)
    return

    if (keys.length === 0) return
    const key = String(keys[0])

    if (key.startsWith('case-')) {
      const newCaseId = parseInt(key.replace('case-', ''))

      // 如果正在编辑同一个用例，不做处理
      if (newCaseId === currentCaseId) return

      // 检查是否有未保存的修改
      if (hasUnsavedChanges && currentCaseId) {
        Modal.confirm({
          title: t('apiTest.unsavedChanges'),
          content: t('apiTest.unsavedChangesContent'),
          okText: t('common.save'),
          cancelText: t('common.cancel'),
          onOk: async () => {
            await saveCurrentCase()
            loadCase(newCaseId)
          },
          onCancel: () => {
            loadCase(newCaseId)
          }
        })
        return
      }

      loadCase(newCaseId)
    }
  }

  // 加载用例数据
  const handleTreeSelect = async (keys: React.Key[]) => {
    if (keys.length === 0) return
    const key = String(keys[0])
    setSelectedTreeKeys([key])

    if (key.startsWith('collection-')) {
      const collectionId = parseInt(key.replace('collection-', ''))
      setActiveCollectionId(collectionId)
      setSelectedCollectionId(collectionId)
      setExpandedTreeKeys(prev => (prev.includes(key) ? prev : [...prev, key]))
      return
    }

    if (key === 'ungrouped') {
      setActiveCollectionId(undefined)
      setSelectedCollectionId(undefined)
      return
    }

    if (key.startsWith('case-')) {
      const newCaseId = parseInt(key.replace('case-', ''))
      const selectedCase = cases.find(c => c.id === newCaseId)
      const parentCollectionId = selectedCase?.collection_id

      setActiveCollectionId(parentCollectionId || undefined)
      setSelectedCollectionId(parentCollectionId || undefined)
      if (parentCollectionId) {
        const parentKey = `collection-${parentCollectionId}`
        setExpandedTreeKeys(prev => (prev.includes(parentKey) ? prev : [...prev, parentKey]))
      }

      if (newCaseId === currentCaseId) return

      if (hasUnsavedChanges && currentCaseId) {
        Modal.confirm({
          title: t('apiTest.unsavedChanges'),
          content: t('apiTest.unsavedChangesContent'),
          okText: t('common.save'),
          cancelText: t('common.cancel'),
          onOk: async () => {
            const saved = await saveCurrentCaseSafely()
            if (saved) {
              loadCase(newCaseId)
            }
          },
          onCancel: () => {
            loadCase(newCaseId)
          }
        })
        return
      }

      loadCase(newCaseId)
    }
  }

  const loadCase = async (caseId: number) => {
    const caseData = cases.find(c => c.id === caseId)
    if (caseData) {
      const formData = {
        name: caseData.name || '',
        method: caseData.method,
        url: caseData.url || '',
        requestBody: JSON.stringify(caseData.body || {}, null, 2),
        headers: caseData.headers
          ? Object.entries(caseData.headers).map(([k, v]) => ({ key: k, value: String(v) }))
          : [{ key: '', value: '' }],
        params: caseData.params
          ? Object.entries(caseData.params).map(([k, v]) => ({ key: k, value: String(v) }))
          : [{ key: '', value: '' }],
        preScript: caseData.pre_script || '',
        postScript: caseData.post_script || '',
        mockEnabled: caseData.mock_enabled || false,
        mockResponseCode: caseData.mock_response_code || 200,
        mockResponseBody: caseData.mock_response_body || '{\n  "success": true,\n  "data": {}\n}',
        mockResponseHeaders: caseData.mock_response_headers 
          ? Object.entries(caseData.mock_response_headers).map(([k, v]) => ({ key: k, value: String(v) }))
          : [{ key: 'Content-Type', value: 'application/json' }],
        mockDelayMs: caseData.mock_delay_ms || 0,
      }

      setRequestName(formData.name)
      setMethod(formData.method)
      setUrl(formData.url)
      setRequestBody(formData.requestBody)
      setHeaders(formData.headers)
      setParams(formData.params)
      setPreScript(formData.preScript)
      setPostScript(formData.postScript)
      setMockEnabled(formData.mockEnabled)
      setMockResponseCode(formData.mockResponseCode)
      setMockResponseBody(formData.mockResponseBody)
      setMockResponseHeaders(formData.mockResponseHeaders)
      setMockDelayMs(formData.mockDelayMs)
      // 加载可视化断言规则
      setAssertions(Array.isArray(caseData.assertions) ? caseData.assertions : [])

      // 保存原始表单数据用于比较
      setOriginalFormData(formData)
      setCurrentCaseId(caseId)
      setHasUnsavedChanges(false)
      setSelectedTreeKeys([`case-${caseId}`])

      const parentCollectionId = caseData.collection_id || undefined
      setActiveCollectionId(parentCollectionId)
      setSelectedCollectionId(parentCollectionId)
      if (parentCollectionId) {
        const parentKey = `collection-${parentCollectionId}`
        setExpandedTreeKeys(prev => (prev.includes(parentKey) ? prev : [...prev, parentKey]))
      }

      message.success(`已加载用例: ${caseData.name}`)
    }
  }

  // 保存当前用例
  const saveCurrentCase = async () => {
    if (!currentCaseId) return

    try {
      const headerObj: Record<string, string> = {}
      headers.filter(h => h.key && h.value).forEach(h => {
        headerObj[h.key] = h.value
      })

      const paramObj: Record<string, string> = {}
      params.filter(p => p.key && p.value).forEach(p => {
        paramObj[p.key] = p.value
      })

      let body = undefined
      if (['POST', 'PUT', 'PATCH'].includes(method) && requestBody) {
        try {
          body = JSON.parse(requestBody)
        } catch {
          body = requestBody
        }
      }

      const mockHeaderObj: Record<string, string> = {}
      mockResponseHeaders.filter(h => h.key && h.value).forEach(h => {
        mockHeaderObj[h.key] = h.value
      })

      const res = await apiTestService.updateCase(currentCaseId, {
        name: requestName,
        method,
        url,
        headers: headerObj,
        params: paramObj,
        body,
        body_type: bodyType,
        pre_script: preScript,
        post_script: postScript,
        assertions: assertions.filter(a => a.enabled),
        environment_id: selectedEnvId,
        mock_enabled: mockEnabled,
        mock_response_code: mockResponseCode,
        mock_response_body: mockResponseBody,
        mock_response_headers: mockHeaderObj,
        mock_delay_ms: mockDelayMs,
      })

      if (res.code === 200) {
        message.success('用例保存成功')
        setHasUnsavedChanges(false)
        // 更新原始表单数据
        setOriginalFormData({
          name: requestName,
          method,
          url,
          requestBody,
          headers: headers.filter(h => h.key || h.value),
          params: params.filter(p => p.key || p.value),
          preScript,
          postScript,
          mockEnabled,
          mockResponseCode,
          mockResponseBody,
          mockResponseHeaders: mockResponseHeaders.filter(h => h.key || h.value),
          mockDelayMs,
        })
        loadData()
      }
    } catch (error) {
      message.error(t('common.failed'))
    }
  }

  // 选择环境
  const saveCurrentCaseSafely = async (): Promise<boolean> => {
    if (!currentCaseId) return true

    try {
      const headerObj: Record<string, string> = {}
      headers.filter(h => h.key && h.value).forEach(h => {
        headerObj[h.key] = h.value
      })

      const paramObj: Record<string, string> = {}
      params.filter(p => p.key && p.value).forEach(p => {
        paramObj[p.key] = p.value
      })

      let body = undefined
      if (['POST', 'PUT', 'PATCH'].includes(method) && requestBody) {
        try {
          body = JSON.parse(requestBody)
        } catch {
          body = requestBody
        }
      }

      const mockHeaderObj: Record<string, string> = {}
      mockResponseHeaders.filter(h => h.key && h.value).forEach(h => {
        mockHeaderObj[h.key] = h.value
      })

      const res = await apiTestService.updateCase(currentCaseId, {
        name: requestName,
        method,
        url,
        headers: headerObj,
        params: paramObj,
        body,
        body_type: bodyType,
        pre_script: preScript,
        post_script: postScript,
        assertions: assertions.filter(a => a.enabled),
        environment_id: selectedEnvId,
        mock_enabled: mockEnabled,
        mock_response_code: mockResponseCode,
        mock_response_body: mockResponseBody,
        mock_response_headers: mockHeaderObj,
        mock_delay_ms: mockDelayMs,
      })

      if (res.code === 200) {
        setHasUnsavedChanges(false)
        setOriginalFormData({
          name: requestName,
          method,
          url,
          requestBody,
          headers: headers.filter(h => h.key || h.value),
          params: params.filter(p => p.key || p.value),
          preScript,
          postScript,
          mockEnabled,
          mockResponseCode,
          mockResponseBody,
          mockResponseHeaders: mockResponseHeaders.filter(h => h.key || h.value),
          mockDelayMs,
        })
        loadData()
        return true
      }

      message.error(res.message || '保存失败')
      return false
    } catch (error) {
      message.error('保存失败')
      return false
    }
  }

  const handleSelectEnv = (envId: number | undefined) => {
    setSelectedEnvId(envId)
    if (envId) {
      const env = environments.find(e => e.id === envId)
      if (env) {
        setCurrentEnv(env)
        message.success(`已选择环境: ${env.name}`)
      } else {
        // 环境不存在，清除保存
        const storageKey = getEnvStorageKey(currentProjectId)
        localStorage.removeItem(storageKey)
        message.warning('选择的环境不存在')
      }
    } else {
      setCurrentEnv(null)
      // 取消选择时清除保存的状态会由 useEffect 自动处理
      message.info('已取消环境选择')
    }
  }

  // 应用环境配置到当前请求
  const applyEnvironment = () => {
    if (!currentEnv) {
      message.warning('请先选择环境')
      return
    }

    // 应用 base_url 到 URL - 自动拼接而不是覆盖
    if (currentEnv.base_url) {
      let newUrl = currentEnv.base_url
      
      // 如果用户已输入URL，则与base_url拼接
      if (url && url.trim()) {
        // 如果用户输入的URL已经是完整URL（以http开头），则保持不变
        if (!url.startsWith('http://') && !url.startsWith('https://')) {
          // 拼接相对路径URL
          newUrl = currentEnv.base_url.replace(/\/$/, '') + (url.startsWith('/') ? url : '/' + url)
        } else {
          // 用户输入的是完整URL，保持不变
          newUrl = url
        }
      }
      
      setUrl(newUrl)
      message.success(`已拼接URL: ${newUrl}`)
    }

    // 应用环境变量到 headers
    if (currentEnv.headers && Object.keys(currentEnv.headers).length > 0) {
      const envHeaders = Object.entries(currentEnv.headers).map(([k, v]) => ({
        key: k,
        value: String(v)
      }))
      
      // 合并已有的 headers
      const existingHeaderKeys = new Set(headers.filter(h => h.key).map(h => h.key))
      const newHeaders = [...headers.filter((_, i) => i === headers.length - 1 && !headers[i].key)]
      
      envHeaders.forEach(h => {
        if (!existingHeaderKeys.has(h.key)) {
          newHeaders.push(h)
        }
      })
      
      setHeaders(newHeaders.length > 0 ? newHeaders : [{ key: '', value: '' }])
      message.success('已应用环境Headers')
    }
  }

  // 获取当前请求的所有参数（包含环境变量和Headers）
  const getRequestWithEnv = async () => {
    let finalUrl = url
    const finalHeaders: Record<string, string> = {}
    const finalParams: Record<string, string> = {}
    const envVars: Record<string, any> =
      currentEnv?.variables && typeof currentEnv.variables === 'object' && !Array.isArray(currentEnv.variables)
        ? currentEnv.variables
        : {}
    const templateVars: Record<string, any> = {
      ...envVars,
      base_url: currentEnv?.base_url,
    }

    const exactPlaceholderKey = (value: string): string | null => {
      const trimmed = value.trim()
      const doubleMatch = trimmed.match(/^\{\{\s*([a-zA-Z_][\w.-]*)\s*\}\}$/)
      if (doubleMatch) return doubleMatch[1]
      const singleMatch = trimmed.match(/^\{\s*([a-zA-Z_][\w.-]*)\s*\}$/)
      if (singleMatch) return singleMatch[1]
      return null
    }

    const resolveTemplateString = (input: string) => {
      return input.replace(
        /\{\{\s*([a-zA-Z_][\w.-]*)\s*\}\}|\{\s*([a-zA-Z_][\w.-]*)\s*\}/g,
        (match, group1, group2) => {
          const key = String(group1 || group2 || '')
          if (!Object.prototype.hasOwnProperty.call(templateVars, key)) return match
          const value = templateVars[key]
          if (value === undefined || value === null) return match
          return String(value)
        }
      )
    }

    const isPlainObject = (value: unknown): value is Record<string, unknown> => {
      if (!value || typeof value !== 'object') return false
      if (Array.isArray(value)) return false
      return Object.getPrototypeOf(value) === Object.prototype
    }

    const resolveTemplateValue = (input: unknown): unknown => {
      if (typeof input === 'string') {
        const key = exactPlaceholderKey(input)
        if (key && Object.prototype.hasOwnProperty.call(templateVars, key)) {
          const value = templateVars[key]
          if (value === undefined || value === null) return input
          if (typeof value === 'string') return value
          return value
        }
        return resolveTemplateString(input)
      }

      if (Array.isArray(input)) {
        return input.map(resolveTemplateValue)
      }

      if (isPlainObject(input)) {
        const result: Record<string, any> = {}
        Object.entries(input).forEach(([k, v]) => {
          result[k] = resolveTemplateValue(v)
        })
        return result
      }

      return input
    }

    // 应用环境配置
    if (currentEnv) {
      // 应用基础URL
      if (currentEnv.base_url && url && !url.startsWith('http')) {
        finalUrl = currentEnv.base_url.replace(/\/$/, '') + (url.startsWith('/') ? url : '/' + url)
      }

      // 应用环境headers
      if (currentEnv.headers) {
        Object.assign(finalHeaders, currentEnv.headers)
      }
    }

    // 应用当前请求的headers
    headers.filter(h => h.key && h.value).forEach(h => {
      finalHeaders[h.key] = h.value
    })

    // 应用请求参数
    params.filter(p => p.key && p.value).forEach(p => {
      finalParams[p.key] = p.value
    })

    finalUrl = resolveTemplateString(finalUrl)

    Object.keys(finalHeaders).forEach(key => {
      finalHeaders[key] = resolveTemplateString(String(finalHeaders[key]))
    })

    Object.keys(finalParams).forEach(key => {
      finalParams[key] = resolveTemplateString(String(finalParams[key]))
    })

    return { finalUrl, finalHeaders, finalParams, resolveTemplateValue }
  }

  // 生成 cURL 命令
  const generateCurl = () => {
    let curl = `curl -X ${method} '${url}'`
    
    // 添加 headers
    const headerEntries = headers.filter(h => h.key && h.value)
    headerEntries.forEach(h => {
      curl += ` \\\n  -H '${h.key}: ${h.value}'`
    })
    
    // 添加 body
    if (['POST', 'PUT', 'PATCH'].includes(method) && requestBody && requestBody !== '{}') {
      curl += ` \\\n  -d '${requestBody}'`
    }
    
    return curl
  }

  // 复制为代码片段
  const handleCopySnippet = (language: string) => {
    if (!url) {
      message.warning('请先输入请求 URL')
      return
    }
    const generator = snippetGenerators[language]
    if (!generator) return

    const snippet = generator({
      method,
      url,
      headers: headers.filter(h => h.key && h.value),
      body: ['POST', 'PUT', 'PATCH'].includes(method) ? requestBody : undefined,
    })
    navigator.clipboard.writeText(snippet)
    message.success(t('apiTest.snippetCopied', { language }))
  }

  // 保存为用例
  const handleSaveCase = async () => {
    if (!url) {
      message.warning('请先输入请求 URL')
      return
    }
    if (!saveCaseName) {
      message.warning('请输入用例名称')
      return
    }

    try {
      const headerObj: Record<string, string> = {}
      headers.filter(h => h.key && h.value).forEach(h => {
        headerObj[h.key] = h.value
      })

      const paramObj: Record<string, string> = {}
      params.filter(p => p.key && p.value).forEach(p => {
        paramObj[p.key] = p.value
      })

      let body = undefined
      if (['POST', 'PUT', 'PATCH'].includes(method) && requestBody) {
        try {
          body = JSON.parse(requestBody)
        } catch {
          body = requestBody
        }
      }

      const mockHeaderObj: Record<string, string> = {}
      mockResponseHeaders.filter(h => h.key && h.value).forEach(h => {
        mockHeaderObj[h.key] = h.value
      })

      const targetCollectionId = selectedCollectionId
      let res
      // 如果是编辑现有用例，调用更新接口
      if (currentCaseId && requestName === saveCaseName) {
        res = await apiTestService.updateCase(currentCaseId, {
          name: saveCaseName,
          method,
          url,
          headers: headerObj,
          params: paramObj,
          body,
          body_type: bodyType,
          pre_script: preScript,
          post_script: postScript,
          collection_id: selectedCollectionId,
          environment_id: selectedEnvId,
          mock_enabled: mockEnabled,
          mock_response_code: mockResponseCode,
          mock_response_body: mockResponseBody,
          mock_response_headers: mockHeaderObj,
          mock_delay_ms: mockDelayMs,
        })
      } else {
        // 新建用例
        res = await apiTestService.createCase({
          name: saveCaseName,
          method,
          url,
          headers: headerObj,
          params: paramObj,
          body,
          body_type: bodyType,
          pre_script: preScript,
          post_script: postScript,
          collection_id: selectedCollectionId,
          environment_id: selectedEnvId,
          mock_enabled: mockEnabled,
          mock_response_code: mockResponseCode,
          mock_response_body: mockResponseBody,
          mock_response_headers: mockHeaderObj,
          mock_delay_ms: mockDelayMs,
        })
      }

      if (res.code === 200 || res.code === 201) {
        message.success('用例保存成功')
        setSaveModalOpen(false)
        setSaveCaseName('')
        setActiveCollectionId(targetCollectionId)
        setSelectedCollectionId(targetCollectionId)
        if (targetCollectionId) {
          const targetKey = `collection-${targetCollectionId}`
          setSelectedTreeKeys([targetKey])
          setExpandedTreeKeys(prev => (prev.includes(targetKey) ? prev : [...prev, targetKey]))
        } else {
          setSelectedTreeKeys(['ungrouped'])
        }
        setHasUnsavedChanges(false)
        // 如果是更新当前用例，更新原始表单数据
        if (currentCaseId && requestName === saveCaseName) {
          setOriginalFormData({
            name: requestName,
            method,
            url,
            requestBody,
            headers: headers.filter(h => h.key || h.value),
            params: params.filter(p => p.key || p.value),
            preScript,
            postScript,
            mockEnabled,
            mockResponseCode,
            mockResponseBody,
            mockResponseHeaders: mockResponseHeaders.filter(h => h.key || h.value),
            mockDelayMs,
          })
        }
        loadData()
      } else {
        message.error(res.message || '保存失败')
      }
    } catch (error) {
      message.error('保存失败')
    }
  }

  const openSaveCaseModal = () => {
    // 保存时默认使用当前请求名称
    setSaveCaseName(requestName)
    setSelectedCollectionId(activeCollectionId)
    setSaveModalOpen(true)
  }

  // 删除用例
  const handleDeleteCase = async (caseId: number, caseName: string) => {
    Modal.confirm({
      title: t('common.confirm'),
      content: t('apiTest.confirmDeleteContent', { name: caseName }),
      okText: t('common.confirm'),
      cancelText: t('common.cancel'),
      okButtonProps: { danger: true },
      onOk: async () => {
        try {
          const res = await apiTestService.deleteCase(caseId)
          if (res.code === 200) {
            message.success(t('common.success'))
            setContextMenuState({ ...contextMenuState, visible: false })
            if (caseId === currentCaseId) {
              setCurrentCaseId(null)
              setOriginalFormData(null)
              setHasUnsavedChanges(false)
              setSelectedTreeKeys(activeCollectionId ? [`collection-${activeCollectionId}`] : ['ungrouped'])
              setUrl('')
              setRequestName('')
              setMethod('GET')
              setRequestBody('{}')
              setHeaders([{ key: '', value: '' }])
              setParams([{ key: '', value: '' }])
              setPreScript('')
              setPostScript('')
              setResponse(null)
              localStorage.removeItem('api-test-form-draft')
            }
            loadData()
          } else {
            message.error(res.message || '删除失败')
          }
        } catch (error) {
          message.error('删除失败')
        }
      }
    })
  }

  // AI 用例裂变
  const handleAiSynthesize = async () => {
    if (!url) {
      message.warning('请先输入有效的 URL')
      return
    }

    setAiSynthesizing(true)
    
    // 构造 base_request
    const headerObj: Record<string, string> = {}
    headers.filter(h => h.key && h.value).forEach(h => {
      headerObj[h.key] = h.value
    })
    const paramObj: Record<string, string> = {}
    params.filter(p => p.key && p.value).forEach(p => {
      paramObj[p.key] = p.value
    })
    let body = undefined
    if (['POST', 'PUT', 'PATCH'].includes(method) && requestBody) {
      try {
        body = JSON.parse(requestBody)
      } catch {
        body = requestBody
      }
    }
    
    const baseRequest = {
      method,
      url,
      headers: headerObj,
      params: paramObj,
      body,
      body_type: bodyType
    }

    try {
      const res = await apiTestService.synthesizeCasesAI({
        base_request: baseRequest,
        count: aiSynthesizeCount,
        base_url: aiBaseUrl,
        model: aiModel,
        api_key: aiApiKey,
        vision_base_url: aiVisionBaseUrl,
        vision_model: aiVisionModel,
        vision_api_key: aiVisionApiKey
      })
      if (res.code === 200 && res.data?.cases) {
        setSynthesizedCases(res.data.cases)
        message.success(`成功生成 ${res.data.cases.length} 个测试用例`)
      } else {
        message.error(res.message || '生成失败')
      }
    } catch (e: unknown) {
      message.error(e.response?.data?.message || '生成失败')
    } finally {
      setAiSynthesizing(false)
    }
  }

  // 批量保存生成的用例
  const handleSaveSynthesizedCases = async () => {
    if (!synthesizedCases.length) return
    
    let savedCount = 0
    for (const c of synthesizedCases) {
      try {
        await apiTestService.createCase({
          name: c.name || `AI Generated Case ${savedCount + 1}`,
          method: c.method,
          url: c.url,
          headers: c.headers,
          params: c.params,
          body: c.body,
          body_type: c.body_type,
          collection_id: synthesizeTargetCollectionId || undefined,
          environment_id: selectedEnvId,
        })
        savedCount++
      } catch (e) {
        logger.error('Failed to save case:', c.name, e)
      }
    }
    
    if (savedCount > 0) {
      message.success(`成功保存 ${savedCount} 个用例`)
      setAiSynthesizeModalOpen(false)
      setSynthesizedCases([])
      loadData()
    } else {
      message.error('保存失败')
    }
  }

  // 更多操作菜单

  const handleAiReviewCollection = async () => {
    const targetCollectionId = selectedCollectionId || activeCollectionId
    if (!targetCollectionId) {
      message.warning('请先在左侧选择一个用例集合')
      return
    }
    setAiReviewing(true)
    try {
      const res = await apiTestService.reviewCollectionAI({
        collection_id: targetCollectionId,
        base_url: aiBaseUrl,
        model: aiModel,
        api_key: aiApiKey,
        vision_base_url: aiVisionBaseUrl,
        vision_model: aiVisionModel,
        vision_api_key: aiVisionApiKey
      })
      if (res.code === 200 && res.data) {
        setReviewSummary(res.data.review_summary)
        setReviewSuggestedCases(res.data.suggested_cases || [])
        message.success('AI 集合评审完成')
      } else {
        message.error(res.message || '评审失败')
      }
    } catch (e: unknown) {
      message.error(e.response?.data?.message || '评审失败')
    } finally {
      setAiReviewing(false)
    }
  }

  const handleSaveReviewCases = async () => {
    const targetCollectionId = selectedCollectionId || activeCollectionId
    if (!targetCollectionId) {
      message.error('未找到目标集合')
      return
    }

    let successCount = 0
    for (const c of reviewSuggestedCases) {
      try {
        await apiTestService.createCase({
          name: c.name || 'AI 补充用例',
          description: c.description || '',
          method: c.method || 'GET',
          url: c.url || 'http://localhost',
          headers: c.headers || {},
          params: c.params || {},
          body: c.body,
          body_type: c.body_type || 'json',
          collection_id: targetCollectionId,
        })
        successCount++
      } catch (e) {
        logger.error('保存用例失败:', e)
      }
    }
    message.success(`成功保存 ${successCount} 个补充用例`)
    setAiReviewModalOpen(false)
    setReviewSuggestedCases([])
    setReviewSummary('')
    loadData() // 刷新左侧列表
  }

  const normalizeAiObject = (value: unknown): Record<string, unknown> => {
    if (value && typeof value === 'object' && !Array.isArray(value)) {
      return value as Record<string, unknown>
    }
    return {}
  }

  const handleAiExecute = async () => {
    if (!aiPrompt.trim()) {
      message.warning('Please enter a prompt')
      return
    }

    const extractAiExecutionErrorParts = (error: unknown): string[] => {
      const errObj = error as { response?: { data?: { errors?: unknown[]; message?: string; detail?: string } }; message?: string } | undefined
      const response = errObj?.response
      const data = response?.data
      const segments: string[] = []
      const pushSegment = (value: unknown) => {
        const text = String(value || '').trim()
        if (!text) return
        if (!segments.includes(text)) {
          segments.push(text.slice(0, 500))
        }
      }

      if (response?.status) {
        pushSegment(`status=${response.status}`)
      }

      pushSegment(data?.message)
      pushSegment(data?.error)
      pushSegment(data?.msg)
      pushSegment(data?.data?.message)
      pushSegment(data?.data?.error)

      if (data?.errors) {
        if (Array.isArray(data.errors)) {
          const briefErrors = data.errors.slice(0, 5).map((item: unknown) => {
            if (typeof item === 'string') return item
            return item?.message || item?.msg || JSON.stringify(item)
          })
          briefErrors.forEach((item: string) => pushSegment(item))
        } else if (typeof data.errors === 'object') {
          pushSegment(JSON.stringify(data.errors))
        } else if (typeof data.errors === 'string') {
          pushSegment(data.errors)
        }
      }

      if (data?.data && typeof data.data === 'object') {
        pushSegment(data.data.detail)
        pushSegment(data.data.traceback)
        pushSegment(data.data.response_body)
        pushSegment(data.data.body)
      }

      if (segments.length === 0) {
        pushSegment(errObj?.message)
      }
      if (segments.length === 0) {
        return ['unknown error']
      }
      return segments
    }

    setAiRunning(true)
    setAiSummary('')
    setAiPlanSource('')
    setAiPlanOperations([])
    setAiExecutionLogs([])

    try {
      const planRes = await apiTestService.generateAiPlan({
        prompt: aiPrompt,
        base_url: aiBaseUrl.trim(),
        model: aiModel.trim(),
        api_key: aiApiKey.trim(),
        vision_base_url: aiVisionBaseUrl.trim(),
        vision_model: aiVisionModel.trim(),
        vision_api_key: aiVisionApiKey.trim(),
        project_id: currentProjectId,
        collection_id: activeCollectionId,
        case_id: currentCaseId || undefined,
        environment_id: selectedEnvId,
      })

      if (planRes.code !== 200 || !planRes.data) {
        throw new Error(planRes.message || 'AI plan generation failed')
      }

      const planData = planRes.data
      const operations = Array.isArray(planData.operations) ? planData.operations : []

      setAiSummary(planData.summary || '')
      setAiPlanSource(planData.source || '')
      setAiPlanOperations(operations)
      appendAiLog('info', `AI generated ${operations.length} operation(s)`)

      const localCollections = [...collections]
      const localEnvironments = [...environments]
      const localCases = [...cases]

      const createdCollectionMap = new Map<string, number>()
      const createdEnvironmentMap = new Map<string, number>()
      const createdCaseMap = new Map<string, number>()

      const resolveCollectionId = (op: AiPlanOperation): number | undefined => {
        if (op.collection_id) return Number(op.collection_id)
        if (op.collection_name && createdCollectionMap.has(op.collection_name)) {
          return createdCollectionMap.get(op.collection_name)
        }
        if (op.collection_name) {
          const found = localCollections.find((c) => c.name === op.collection_name)
          if (found) return found.id
        }

        // Fallback: If we created a collection in this run, use the latest one
        if (createdCollectionMap.size > 0) {
           const ids = Array.from(createdCollectionMap.values())
           return ids[ids.length - 1]
        }

        return activeCollectionId
      }

      const resolveEnvironmentId = (op: AiPlanOperation): number | undefined => {
        if (op.environment_id) return Number(op.environment_id)
        if (op.environment_name && createdEnvironmentMap.has(op.environment_name)) {
          return createdEnvironmentMap.get(op.environment_name)
        }
        if (op.environment_name) {
          const found = localEnvironments.find((e) => e.name === op.environment_name)
          if (found) return found.id
        }
        return selectedEnvId
      }

      const resolveCaseId = (op: AiPlanOperation): number | undefined => {
        if (op.case_id) return Number(op.case_id)
        if (op.case_name && createdCaseMap.has(op.case_name)) {
          return createdCaseMap.get(op.case_name)
        }
        if (op.case_name) {
          const found = localCases.find((c) => c.name === op.case_name)
          if (found) return found.id
        }
        return currentCaseId || undefined
      }

      const inferAiCaseMethod = (op: AiPlanOperation): string => {
        const rawMethod = String(op.method || '').trim().toUpperCase()
        const allowedMethods = ['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'HEAD', 'OPTIONS']
        if (allowedMethods.includes(rawMethod)) return rawMethod

        const hasBody =
          op.body !== undefined &&
          op.body !== null &&
          (typeof op.body !== 'string' || op.body.trim().length > 0)
        const hintedBodyType = String(op.body_type || '').trim().toLowerCase()
        if (
          hasBody ||
          ['json', 'raw', 'form-data', 'x-www-form-urlencoded', 'multipart'].includes(hintedBodyType)
        ) {
          return 'POST'
        }

        const hint = `${op.name || ''} ${op.description || ''} ${op.url || ''}`.toLowerCase()
        if (/(login|signin|signup|register|create|add|save|submit|token)/.test(hint)) return 'POST'
        if (/(update|edit|modify)/.test(hint)) return 'PUT'
        if (/(delete|remove)/.test(hint)) return 'DELETE'
        if (/(patch)/.test(hint)) return 'PATCH'
        return 'GET'
      }

      const buildRunCaseFailureReasons = (runData: unknown): string[] => {
        if (!runData || typeof runData !== 'object') return ['unknown reason']
        const parts: string[] = []
        const pushPart = (value: unknown) => {
          const text = String(value || '').trim()
          if (!text) return
          if (!parts.includes(text)) {
            parts.push(text.slice(0, 500))
          }
        }

        if (runData.status_code !== undefined && runData.status_code !== null) {
          pushPart(`status=${runData.status_code}`)
        }
        pushPart(runData.error)

        if (runData.script_execution?.pre_script?.error) {
          pushPart(`pre_script: ${runData.script_execution.pre_script.error}`)
        }
        if (runData.script_execution?.post_script?.error) {
          pushPart(`post_script: ${runData.script_execution.post_script.error}`)
        }

        const bodyData = runData.body
        if (typeof bodyData === 'string' && bodyData.trim()) {
          pushPart(bodyData)
          try {
            const parsed = JSON.parse(bodyData)
            pushPart(parsed?.message)
            pushPart(parsed?.error)
            pushPart(parsed?.msg)
          } catch { /* ignore */ }
        } else if (bodyData && typeof bodyData === 'object') {
          pushPart(bodyData.message)
          pushPart(bodyData.msg)
          pushPart(bodyData.error)
        }

        if (parts.length === 0) return ['unknown reason']
        return parts
      }

      for (let index = 0; index < operations.length; index += 1) {
        const op = operations[index]
        const opTitle = `[${index + 1}/${operations.length}] ${op.type}`

        try {
          if (op.type === 'create_environment') {
            const envRes = await environmentService.createEnvironment({
              name: op.name || `AI Env ${Date.now()}`,
              base_url: op.base_url || '',
              description: op.description || '',
              variables: normalizeAiObject(op.variables),
              headers: normalizeAiObject(op.headers),
              project_id: op.project_id || currentProjectId,
            })
            if (envRes.code !== 200 && envRes.code !== 201) throw new Error(envRes.message || 'create environment failed')
            const envData = envRes.data
            localEnvironments.push(envData)
            if (envData?.name) createdEnvironmentMap.set(envData.name, envData.id)
            appendAiLog('success', `${opTitle} created environment #${envData?.id}`)
            continue
          }

          if (op.type === 'update_environment') {
            const envId = resolveEnvironmentId(op)
            if (!envId) throw new Error('environment id is required for update_environment')
            const updatePayload: Record<string, unknown> = {}
            if (op.name) updatePayload.name = op.name
            if (op.base_url) updatePayload.base_url = op.base_url
            if (op.variables) updatePayload.variables = normalizeAiObject(op.variables)
            if (op.headers) updatePayload.headers = normalizeAiObject(op.headers)
            const envRes = await environmentService.updateEnvironment(envId, updatePayload)
            if (envRes.code !== 200) throw new Error(envRes.message || 'update environment failed')
            appendAiLog('success', `${opTitle} updated environment #${envId}`)
            continue
          }

          if (op.type === 'create_collection') {
            const colRes = await apiTestService.createCollection({
              name: op.name || `AI Collection ${Date.now()}`,
              description: op.description || '',
              project_id: op.project_id || currentProjectId,
            })
            if (colRes.code !== 200 && colRes.code !== 201) throw new Error(colRes.message || 'create collection failed')
            const colData = colRes.data
            localCollections.push(colData)
            if (colData?.name) createdCollectionMap.set(colData.name, colData.id)
            appendAiLog('success', `${opTitle} created collection #${colData?.id}`)
            continue
          }

          if (op.type === 'create_case') {
            const methodValue = inferAiCaseMethod(op)
            const bodyValue = op.body === undefined ? undefined : op.body
            const caseRes = await apiTestService.createCase({
              name: op.name || `AI Case ${Date.now()}`,
              description: op.description || '',
              method: methodValue,
              url: op.url || '{{base_url}}/api-test/health',
              headers: normalizeAiObject(op.headers),
              params: normalizeAiObject(op.params),
              body: bodyValue,
              body_type: op.body_type || (typeof bodyValue === 'object' ? 'json' : 'raw'),
              pre_script: op.pre_script || '',
              post_script: op.post_script || '',
              collection_id: resolveCollectionId(op),
              project_id: op.project_id || currentProjectId,
              environment_id: resolveEnvironmentId(op),
            })
            if (caseRes.code !== 200 && caseRes.code !== 201) throw new Error(caseRes.message || 'create case failed')
            const caseData = caseRes.data
            localCases.push(caseData)
            if (caseData?.name) createdCaseMap.set(caseData.name, caseData.id)
            appendAiLog('success', `${opTitle} created case #${caseData?.id}`)
            continue
          }

          if (op.type === 'run_collection') {
            if (!aiAutoRun) {
              appendAiLog('info', `${opTitle} skipped (auto-run disabled)`)
              continue
            }
            const collectionId = resolveCollectionId(op)
            if (!collectionId) throw new Error('collection id is required for run_collection')
            const envId = resolveEnvironmentId(op)
            const runRes = await apiTestService.runCollection(
              collectionId,
              envId ? { env_id: envId } : {}
            )
            if (runRes.code !== 200) throw new Error(runRes.message || 'run collection failed')
            appendAiLog(
              'success',
              `${opTitle} done: passed=${runRes.data?.passed ?? 0}, failed=${runRes.data?.failed ?? 0}`
            )
            continue
          }

          if (op.type === 'run_case') {
            if (!aiAutoRun) {
              appendAiLog('info', `${opTitle} skipped (auto-run disabled)`)
              continue
            }
            const caseId = resolveCaseId(op)
            if (!caseId) throw new Error('case id is required for run_case')
            const envId = resolveEnvironmentId(op)
            const runRes = await apiTestService.runCase(caseId, envId)
            if (runRes.code !== 200) throw new Error(runRes.message || 'run case failed')
            const isPassed = runRes.data?.passed
            if (isPassed) {
              appendAiLog('success', `${opTitle} done: passed`)
            } else {
              const failureReasons = buildRunCaseFailureReasons(runRes.data)
              appendAiLog('error', `${opTitle} done: failed (${failureReasons[0]})`)
              failureReasons.slice(1).forEach((reason, detailIndex) => {
                appendAiLog('error', `${opTitle} detail ${detailIndex + 1}: ${reason}`)
              })
            }
            continue
          }

          appendAiLog('info', `${opTitle} ignored (unsupported type)`)
        } catch (error: unknown) {
          const errorParts = extractAiExecutionErrorParts(error)
          appendAiLog('error', `${opTitle} failed: ${errorParts[0]}`)
          errorParts.slice(1).forEach((part, detailIndex) => {
            appendAiLog('error', `${opTitle} detail ${detailIndex + 1}: ${part}`)
          })
        }
      }

      await loadData()
      appendAiLog('success', 'AI workflow completed')
      message.success('AI workflow completed')
    } catch (error: unknown) {
      const errorParts = extractAiExecutionErrorParts(error)
      appendAiLog('error', `AI workflow failed: ${errorParts[0]}`)
      errorParts.slice(1).forEach((part, detailIndex) => {
        appendAiLog('error', `AI workflow detail ${detailIndex + 1}: ${part}`)
      })
      message.error(errorParts[0] || 'AI workflow failed')
    } finally {
      setAiRunning(false)
    }
  }

  const moreMenuItems: MenuProps['items'] = [
    { key: 'curl', icon: <CopyOutlined />, label: 'cURL', onClick: () => handleCopySnippet('curl') },
    { key: 'python', icon: <CopyOutlined />, label: 'Python (requests)', onClick: () => handleCopySnippet('python') },
    { key: 'javascript', icon: <CopyOutlined />, label: 'JavaScript (fetch)', onClick: () => handleCopySnippet('javascript') },
    { key: 'java', icon: <CopyOutlined />, label: 'Java (OkHttp)', onClick: () => handleCopySnippet('java') },
    { key: 'go', icon: <CopyOutlined />, label: 'Go (net/http)', onClick: () => handleCopySnippet('go') },
  ]

  // 参数表格列
  const paramsColumns = [
    {
      title: t('apiTest.index'),
      key: 'index',
      width: 60,
      align: 'center' as const,
      render: (_: unknown, __: unknown, index: number) => (
        <Text type="secondary">{index + 1}</Text>
      ),
    },
    {
      title: t('apiTest.paramName'),
      dataIndex: 'key',
      key: 'key',
      render: (_: unknown, record: Record<string, unknown>, index: number) => (
        <Input
          placeholder={t('apiTest.paramName')}
          size="small"
          value={record.key}
          onChange={(e) => {
            const newParams = [...params]
            newParams[index].key = e.target.value
            setParams(newParams)
          }}
        />
      ),
    },
    {
      title: t('apiTest.paramValue'),
      dataIndex: 'value',
      key: 'value',
      render: (_: unknown, record: Record<string, unknown>, index: number) => (
        <Input
          placeholder={t('apiTest.paramValue')}
          size="small"
          value={record.value}
          onChange={(e) => {
            const newParams = [...params]
            newParams[index].value = e.target.value
            setParams(newParams)
          }}
        />
      ),
    },
    {
      title: t('common.actions'),
      key: 'action',
      width: 80,
      render: (_: unknown, __: unknown, index: number) => (
        <Button
          type="text"
          danger
          size="small"
          icon={<DeleteOutlined />}
          onClick={() => {
            const newParams = params.filter((_, i) => i !== index)
            setParams(newParams.length > 0 ? newParams : [{ key: '', value: '' }])
          }}
        />
      ),
    },
  ]

  // 请求头表格列
  const headersColumns = [
    {
      title: t('apiTest.index'),
      key: 'index',
      width: 60,
      align: 'center' as const,
      render: (_: unknown, __: unknown, index: number) => (
        <Text type="secondary">{index + 1}</Text>
      ),
    },
    {
      title: t('apiTest.headerName'),
      dataIndex: 'key',
      key: 'key',
      render: (_: unknown, record: Record<string, unknown>, index: number) => (
        <Input
          placeholder={t('apiTest.headerName')}
          size="small"
          value={record.key}
          onChange={(e) => {
            const newHeaders = [...headers]
            newHeaders[index].key = e.target.value
            setHeaders(newHeaders)
          }}
        />
      ),
    },
    {
      title: t('apiTest.headers'),
      dataIndex: 'value',
      key: 'value',
      render: (_: unknown, record: Record<string, unknown>, index: number) => (
        <Input
          placeholder={t('apiTest.headerValue')}
          size="small"
          value={record.value}
          onChange={(e) => {
            const newHeaders = [...headers]
            newHeaders[index].value = e.target.value
            setHeaders(newHeaders)
          }}
        />
      ),
    },
    {
      title: t('common.actions'),
      key: 'action',
      width: 80,
      render: (_: unknown, __: unknown, index: number) => (
        <Button
          type="text"
          danger
          size="small"
          icon={<DeleteOutlined />}
          onClick={() => {
            const newHeaders = headers.filter((_, i) => i !== index)
            setHeaders(newHeaders.length > 0 ? newHeaders : [{ key: '', value: '' }])
          }}
        />
      ),
    },
  ]

  // 发送请求
  const handleSend = async () => {
    if (sending) return // 防止重复请求
    if (!url) {
      message.warning('请输入请求URL')
      return
    }

    setSending(true)
    const startTime = Date.now()
    
    try {
      // 获取包含环境配置的请求参数
      const { finalUrl, finalHeaders, finalParams, resolveTemplateValue } = await getRequestWithEnv()

      // 准备请求头
      const reqHeaders: Record<string, string> = { ...finalHeaders }
      if (bodyType === 'json' && !reqHeaders['Content-Type']) {
        reqHeaders['Content-Type'] = 'application/json'
      } else if (bodyType === 'form' && !reqHeaders['Content-Type']) {
        reqHeaders['Content-Type'] = 'application/x-www-form-urlencoded'
      }
      
      // 准备请求体
      let body = undefined
      if (['POST', 'PUT', 'PATCH'].includes(method)) {
        if (bodyType === 'json') {
          try {
            body = JSON.parse(requestBody)
          } catch {
            message.error('JSON 格式错误')
            setSending(false)
            return
          }
        } else {
          body = requestBody
        }
      }
      body = resolveTemplateValue(body)

      // 调用后端 API 执行请求
      const result = await apiTestService.executeRequest({
        method,
        url: finalUrl,
        headers: reqHeaders,
        params: finalParams,
        body,
        body_type: bodyType,
        timeout: 30,
        env_id: selectedEnvId,
        pre_script: preScript,
        post_script: postScript,
        assertions: assertions.filter(a => a.enabled),
        case_id: currentCaseId || undefined,
        mock_enabled: mockEnabled,
        mock_response_code: mockResponseCode,
        mock_response_body: mockResponseBody,
        mock_response_headers: mockResponseHeaders.reduce((acc, curr) => {
          if (curr.key && curr.value) acc[curr.key] = curr.value
          return acc
        }, {} as Record<string, string>),
        mock_delay_ms: mockDelayMs,
      })

      const elapsed = Date.now() - startTime

      // 后端返回格式: { code: 200, data: { success: true, status_code: 200, ... } }
      if (result.code === 200 && result.data) {
        const respData = result.data
        if (respData.success) {
          setResponse({
            status: respData.status_code,
            statusText: respData.status_code < 400 ? 'OK' : 'Error',
            time: respData.response_time || elapsed,
            size: respData.response_size || '-',
            headers: respData.headers || {},
            data: respData.body,
            script_execution: respData.script_execution,
            is_mock: respData.is_mock,
          })
          // 提取可视化断言结果
          setAssertionResults(respData.script_execution?.visual_assertions || undefined)
          // 保存到请求历史
          saveToHistory({ method, url, status: respData.status_code, duration: respData.response_time || elapsed })
          message.success('请求发送成功')
        } else {
          setResponse({
            status: 0,
            statusText: 'Error',
            time: respData.response_time || elapsed,
            size: '-',
            headers: {},
            data: { error: respData.error || '请求失败' },
          })
          message.error(respData.error || '请求失败')
        }
      } else {
        setResponse({
          status: 0,
          statusText: 'Error',
          time: elapsed,
          size: '-',
          headers: {},
          data: { error: result.message || '请求失败' },
        })
        message.error(result.message || '请求失败')
      }
    } catch (error: unknown) {
      const elapsed = Date.now() - startTime
      setResponse({
        status: 0,
        statusText: 'Error',
        time: elapsed,
        size: '-',
        headers: {},
        data: { error: error.message || '请求失败' },
      })
      message.error('请求失败: ' + (error.message || '未知错误'))
    } finally {
      setSending(false)
    }
  }

  return (
    <Layout style={{ height: 'calc(100vh - 160px)', background: 'transparent' }} role="main" aria-label="接口测试工作区">
      {/* 左侧用例树和集合管理 */}
      <Sider
        width={320}
        aria-label="用例导航"
        style={{
          background: 'var(--fst-surface-card)',
          borderRadius: 'var(--fst-radius-xl)',
          border: '1px solid var(--fst-glass-border)',
          boxShadow: 'var(--fst-shadow-sm)',
          marginRight: 16,
          overflow: 'hidden',
        }}
      >
        <Tabs
          activeKey={sidebarTab}
          onChange={setSidebarTab}
          style={{ height: '100%' }}
          tabBarStyle={{ paddingLeft: 12, paddingRight: 12, marginBottom: 0 }}
          items={[
            {
              key: 'cases',
              label: '测试用例',
              children: (
                <div style={{ padding: 12, height: 'calc(100vh - 240px)', overflow: 'auto' }}>
                  <Space.Compact style={{ width: '100%', marginBottom: 12 }}>
                    <Input
                      placeholder="搜索用例..."
                      prefix={<SearchOutlined />}
                      allowClear
                      value={searchText}
                      onChange={(e) => setSearchText(e.target.value)}
                    />
                    <Tooltip title={t('common.refresh')}>
                      <Button icon={<ReloadOutlined />} onClick={loadData} />
                    </Tooltip>
                  </Space.Compact>

                  {treeData.length > 0 ? (
                    <Tree
                      showIcon
                      expandedKeys={expandedTreeKeys}
                      selectedKeys={selectedTreeKeys}
                      onExpand={(keys) => setExpandedTreeKeys(keys)}
                      treeData={treeData}
                      onSelect={handleSelectCase}
                      onRightClick={({ event, node }) => {
                        event.preventDefault()
                        // 只有测试用例节点才显示右键菜单
                        if ('caseData' in node) {
                          const caseData = (node as unknown as { caseData: { id: number; name: string } }).caseData
                          setContextMenuState({
                            visible: true,
                            x: event.clientX,
                            y: event.clientY,
                            caseId: caseData.id,
                            caseName: caseData.name
                          })
                        }
                      }}
                      style={{ background: 'transparent' }}
                    />
                  ) : (
                    <Empty description="暂无用例" style={{ marginTop: 40 }} />
                  )}
                </div>
              ),
            },
            {
              key: 'collections',
              label: '集合管理',
              children: (
                <div style={{ padding: 12, height: 'calc(100vh - 240px)', overflow: 'auto' }}>
                  <CollectionManager 
                    onCollectionChange={loadData}
                    onSelectCollection={(collectionId) => {
                      setActiveCollectionId(collectionId)
                      setSelectedCollectionId(collectionId)
                      setSidebarTab('cases')
                      setSelectedTreeKeys([`collection-${collectionId}`])
                      setExpandedTreeKeys(prev => 
                        prev.includes(`collection-${collectionId}`) ? prev : [...prev, `collection-${collectionId}`]
                      )
                    }}
                    onAiReview={(collectionId) => {
                      setActiveCollectionId(collectionId)
                      setSelectedCollectionId(collectionId)
                      setSidebarTab('cases')
                      setSelectedTreeKeys([`collection-${collectionId}`])
                      setExpandedTreeKeys(prev => 
                        prev.includes(`collection-${collectionId}`) ? prev : [...prev, `collection-${collectionId}`]
                      )
                      setAiReviewModalOpen(true)
                    }}
                  />
                </div>
              ),
            },
            {
              key: 'history',
              label: t('apiTest.history.title'),
              children: (
                <div style={{ padding: 12, height: 'calc(100vh - 240px)', overflow: 'auto' }}>
                  <RequestHistory
                    onSelect={(item) => {
                      setMethod(item.method)
                      setUrl(item.url)
                    }}
                  />
                </div>
              ),
            },
          ]}
        />
      </Sider>

      {/* 右侧工作区 */}
      <Content style={{ display: 'flex', flexDirection: 'column', gap: 16 }}>
        {/* 请求区域 — 使用提取的 RequestEditor 组件 */}
        <RequestEditor
          requestName={requestName} setRequestName={setRequestName}
          method={method} setMethod={setMethod}
          url={url} setUrl={setUrl}
          sending={sending} onSend={handleSend}
          currentCaseId={currentCaseId ?? undefined} hasUnsavedChanges={hasUnsavedChanges}
          onNewCase={handleNewCase} onSaveCase={saveCurrentCase} onOpenSaveModal={openSaveCaseModal}
          onDeleteCase={handleDeleteCase}
          environments={environments} selectedEnvId={selectedEnvId} onSelectEnv={handleSelectEnv}
          currentEnv={currentEnv} onApplyEnv={applyEnvironment}
          activeTab={activeTab} setActiveTab={setActiveTab}
          params={params} setParams={setParams} paramsColumns={paramsColumns}
          headers={headers} setHeaders={setHeaders} headersColumns={headersColumns}
          bodyType={bodyType} setBodyType={setBodyType}
          requestBody={requestBody} setRequestBody={setRequestBody}
          preScript={preScript} setPreScript={setPreScript}
          postScript={postScript} setPostScript={setPostScript}
          mockEnabled={mockEnabled} setMockEnabled={setMockEnabled}
          mockResponseCode={mockResponseCode} setMockResponseCode={setMockResponseCode}
          mockResponseBody={mockResponseBody} setMockResponseBody={setMockResponseBody}
          mockResponseHeaders={mockResponseHeaders} setMockResponseHeaders={setMockResponseHeaders}
          mockDelayMs={mockDelayMs} setMockDelayMs={setMockDelayMs}
          onOpenAiDrawer={() => setAiDrawerOpen(true)}
          onOpenSynthesize={() => { setSynthesizeTargetCollectionId(selectedCollectionId || activeCollectionId); setAiSynthesizeModalOpen(true) }}
          onOpenReview={() => setAiReviewModalOpen(true)}
          selectedCollectionId={selectedCollectionId} activeCollectionId={activeCollectionId}
          moreMenuItems={moreMenuItems}
          response={response}
          assertions={assertions} setAssertions={setAssertions}
          assertionResults={assertionResults}
        />

        {/* 响应区域 — 使用提取的 ResponseViewer 组件 */}
        <TestRunner sending={sending} onResend={handleSend} response={response} progress={collectionProgress} />
        <ResponseViewer response={response} />
      </Content>

      {/* AI Assistant 弹窗 */}
      <AiAssistantDrawer
        open={aiDrawerOpen}
        onClose={() => setAiDrawerOpen(false)}
        loadingConfig={loadingConfig}
        globalAiConfig={globalAiConfig}
        aiBaseUrl={aiBaseUrl}
        setAiBaseUrl={setAiBaseUrl}
        aiModel={aiModel}
        setAiModel={setAiModel}
        aiApiKey={aiApiKey}
        setAiApiKey={setAiApiKey}
        aiVisionBaseUrl={aiVisionBaseUrl}
        setAiVisionBaseUrl={setAiVisionBaseUrl}
        aiVisionModel={aiVisionModel}
        setAiVisionModel={setAiVisionModel}
        aiVisionApiKey={aiVisionApiKey}
        setAiVisionApiKey={setAiVisionApiKey}
        aiPrompt={aiPrompt}
        setAiPrompt={setAiPrompt}
        aiAutoRun={aiAutoRun}
        setAiAutoRun={setAiAutoRun}
        aiRunning={aiRunning}
        aiSummary={aiSummary}
        aiPlanSource={aiPlanSource}
        aiPlanOperations={aiPlanOperations}
        aiExecutionLogs={aiExecutionLogs}
        onExecute={handleAiExecute}
      />

      <SaveCaseModal
        open={saveModalOpen}
        caseName={saveCaseName}
        method={method}
        url={url}
        selectedCollectionId={selectedCollectionId}
        collections={collections}
        onCaseNameChange={setSaveCaseName}
        onCollectionChange={setSelectedCollectionId}
        onSave={handleSaveCase}
        onCancel={() => {
          setSaveModalOpen(false)
          setSaveCaseName('')
          setSelectedCollectionId(activeCollectionId)
        }}
      />

      {/* AI 扩充用例弹窗 */}
      <AiSynthesizeModal
        open={aiSynthesizeModalOpen}
        loading={aiSynthesizing}
        synthesizedCases={synthesizedCases}
        synthesizeCount={aiSynthesizeCount}
        targetCollectionId={synthesizeTargetCollectionId}
        collections={collections}
        onSynthesize={handleAiSynthesize}
        onSaveAll={handleSaveSynthesizedCases}
        onCancel={() => setAiSynthesizeModalOpen(false)}
        onCountChange={setAiSynthesizeCount}
        onTargetCollectionChange={setSynthesizeTargetCollectionId}
        onReset={() => setSynthesizedCases([])}
      />

      {/* 右键菜单 */}
      {contextMenuState.visible && (
        <div
          style={{
            position: 'fixed',
            left: contextMenuState.x,
            top: contextMenuState.y,
            zIndex: 1000,
          }}
          onClick={() => setContextMenuState({ ...contextMenuState, visible: false })}
        >
          <Card size="small" style={{ minWidth: 120 }}>
            <Space direction="vertical" style={{ width: '100%' }}>
              <Button
                type="text"
                danger
                block
                icon={<DeleteOutlined />}
                onClick={() => handleDeleteCase(contextMenuState.caseId!, contextMenuState.caseName)}
              >
                删除用例
              </Button>
            </Space>
          </Card>
        </div>
      )}

      {/* AI 集合评审弹窗 */}
      <AiReviewModal
        open={aiReviewModalOpen}
        loading={aiReviewing}
        reviewSummary={reviewSummary}
        suggestedCases={reviewSuggestedCases}
        onStartReview={handleAiReviewCollection}
        onSaveCases={handleSaveReviewCases}
        onCancel={() => setAiReviewModalOpen(false)}
        onReset={() => {
          setReviewSummary('')
          setReviewSuggestedCases([])
        }}
      />
    </Layout>
  )
}

export default ApiTestWorkspace
