import { useState, useEffect } from 'react'
import {
  Layout,
  Card,
  Tree,
  Input,
  Button,
  Tabs,
  Select,
  Form,
  Space,
  Table,
  Tag,
  Dropdown,
  Typography,
  Empty,
  Tooltip,
  message,
  Modal,
  Drawer,
  Switch,
  Alert,
  Divider,
  InputNumber,
  Badge,
  Spin,
} from 'antd'
import {
  PlusOutlined,
  FolderOutlined,
  FileOutlined,
  FileAddOutlined,
  SendOutlined,
  SaveOutlined,
  DeleteOutlined,
  CopyOutlined,
  MoreOutlined,
  SearchOutlined,
  ReloadOutlined,
  InfoCircleOutlined,
  CheckCircleOutlined,
  CloseCircleOutlined,
  RobotOutlined,
  ExperimentOutlined,
} from '@ant-design/icons'
import type { DataNode } from 'antd/es/tree'
import type { MenuProps } from 'antd'
import MonacoEditor from '@monaco-editor/react'
import { apiTestService } from '@/services/apiTestService'
import type { AiPlanOperation } from '@/services/apiTestService'
import { environmentService } from '@/services/environmentService'
import CollectionManager from './CollectionManager'
import EnvironmentVariableHint from './EnvironmentVariableHint'

const { Sider, Content } = Layout
const { Text } = Typography
const { TextArea } = Input

// 脚本测试结果展示组件
interface ScriptTestResultsProps {
  scriptExecution?: {
    pre_script?: {
      executed: boolean
      passed?: boolean
      error?: string
      duration?: number
    }
    post_script?: {
      executed: boolean
      passed?: boolean
      error?: string
      duration?: number
      assertions?: {
        total: number
        passed: number
        failed: number
        details?: Array<{
          name: string
          passed: boolean
          error?: string
        }>
      }
    }
  }
}

const ScriptTestResults: React.FC<ScriptTestResultsProps> = ({ scriptExecution }) => {
  if (!scriptExecution) {
    return <Empty description="暂无脚本执行结果" />
  }

  const { pre_script, post_script } = scriptExecution

  // 检查是否有任何脚本被执行
  const hasExecutedScript = (pre_script?.executed || post_script?.executed)

  if (!hasExecutedScript) {
    return <Empty description="未配置前置/后置脚本" />
  }

  return (
    <Space direction="vertical" style={{ width: '100%' }} size="large">
      {/* 前置脚本结果 */}
      {pre_script?.executed && (
        <Card size="small" title={<Space><Text strong>前置脚本</Text></Space>}>
          <Space direction="vertical" style={{ width: '100%' }} size="small">
            <Space>
              {pre_script.passed ? (
                <Tag icon={<CheckCircleOutlined />} color="success">执行成功</Tag>
              ) : (
                <Tag icon={<CloseCircleOutlined />} color="error">执行失败</Tag>
              )}
              {pre_script.duration !== undefined && (
                <Text type="secondary">耗时: {pre_script.duration}ms</Text>
              )}
            </Space>
            {pre_script.error && (
              <Text type="danger">{pre_script.error}</Text>
            )}
          </Space>
        </Card>
      )}

      {/* 后置脚本结果 */}
      {post_script?.executed && (
        <Card size="small" title={<Space><Text strong>后置断言</Text></Space>}>
          <Space direction="vertical" style={{ width: '100%' }} size="small">
            <Space>
              {post_script.passed ? (
                <Tag icon={<CheckCircleOutlined />} color="success">全部通过</Tag>
              ) : (
                <Tag icon={<CloseCircleOutlined />} color="error">存在失败</Tag>
              )}
              {post_script.duration !== undefined && (
                <Text type="secondary">耗时: {post_script.duration}ms</Text>
              )}
            </Space>

            {/* 断言统计 */}
            {post_script.assertions && (
              <Space>
                <Text>总计: <Text strong>{post_script.assertions.total}</Text></Text>
                <Text type="success">通过: <Text strong>{post_script.assertions.passed}</Text></Text>
                {post_script.assertions.failed > 0 && (
                  <Text type="danger">失败: <Text strong>{post_script.assertions.failed}</Text></Text>
                )}
              </Space>
            )}

            {/* 断言详情 */}
            {post_script.assertions?.details && post_script.assertions.details.length > 0 && (
              <Table
                size="small"
                dataSource={post_script.assertions.details.map((d, i) => ({ ...d, key: i }))}
                columns={[
                  {
                    title: '状态',
                    dataIndex: 'passed',
                    width: 60,
                    render: (passed) => passed ? (
                      <CheckCircleOutlined style={{ color: '#52c41a' }} />
                    ) : (
                      <CloseCircleOutlined style={{ color: '#ff4d4f' }} />
                    ),
                  },
                  {
                    title: '断言描述',
                    dataIndex: 'name',
                    ellipsis: true,
                  },
                  {
                    title: '错误信息',
                    dataIndex: 'error',
                    render: (error) => error ? (
                      <Text type="danger" style={{ fontSize: 12 }}>{error}</Text>
                    ) : (
                      <Text type="secondary">-</Text>
                    ),
                  },
                ]}
                pagination={false}
                showHeader={false}
              />
            )}

            {post_script.error && (
              <Text type="danger">{post_script.error}</Text>
            )}
          </Space>
        </Card>
      )}
    </Space>
  )
}

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
  const [method, setMethod] = useState('GET')
  const [url, setUrl] = useState('')
  const [requestName, setRequestName] = useState('')  // 自定义请求名称
  const [activeTab, setActiveTab] = useState('params')
  const [responseTab, setResponseTab] = useState('body')
  const [sending, setSending] = useState(false)
  const [response, setResponse] = useState<any>(null)
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

  const [collections, setCollections] = useState<any[]>([])
  const [cases, setCases] = useState<any[]>([])
  const [treeData, setTreeData] = useState<DataNode[]>([])
  const [selectedTreeKeys, setSelectedTreeKeys] = useState<React.Key[]>([])
  const [expandedTreeKeys, setExpandedTreeKeys] = useState<React.Key[]>([])
  const [saveModalOpen, setSaveModalOpen] = useState(false)
  const [saveCaseName, setSaveCaseName] = useState('')
  const [selectedCollectionId, setSelectedCollectionId] = useState<number | undefined>()
  const [activeCollectionId, setActiveCollectionId] = useState<number | undefined>()
  const [searchText, setSearchText] = useState('')
  const [environments, setEnvironments] = useState<any[]>([])
  const [selectedEnvId, setSelectedEnvId] = useState<number | undefined>()
  const [currentEnv, setCurrentEnv] = useState<any>(null)
  const [sidebarTab, setSidebarTab] = useState<string>('cases') // 侧边栏标签页
  const [hasLoadedData, setHasLoadedData] = useState(false) // 标记数据是否已加载
  const [aiDrawerOpen, setAiDrawerOpen] = useState(false)
  const [aiPrompt, setAiPrompt] = useState('')
  const [aiBaseUrl, setAiBaseUrl] = useState('')
  const [aiModel, setAiModel] = useState('')
  const [aiApiKey, setAiApiKey] = useState('')
  const [aiAutoRun, setAiAutoRun] = useState(true)
  const [aiRunning, setAiRunning] = useState(false)
  const [aiSummary, setAiSummary] = useState('')
  const [aiPlanSource, setAiPlanSource] = useState<'llm' | 'fallback' | ''>('')
  const [aiPlanOperations, setAiPlanOperations] = useState<AiPlanOperation[]>([])
  const [aiExecutionLogs, setAiExecutionLogs] = useState<AiExecutionLog[]>([])

  // 全局配置加载
  const [globalAiConfig, setGlobalAiConfig] = useState<{base_url: string, model: string, api_key: string} | null>(null)
  const [loadingConfig, setLoadingConfig] = useState(false)

  // Fetch global AI config when drawer opens
  useEffect(() => {
    if (aiDrawerOpen && !globalAiConfig && !loadingConfig) {
      setLoadingConfig(true)
      apiTestService.getAiConfig()
        .then(res => {
          if (res.code === 200 && res.data) {
            setGlobalAiConfig(res.data)
          }
        })
        .catch(err => console.error('Failed to load global AI config', err))
        .finally(() => setLoadingConfig(false))
    }
  }, [aiDrawerOpen])

  // AI Synthesizer State
  const [aiSynthesizeModalOpen, setAiSynthesizeModalOpen] = useState(false)
  const [aiSynthesizeCount, setAiSynthesizeCount] = useState(5)
  const [aiSynthesizing, setAiSynthesizing] = useState(false)
  const [synthesizedCases, setSynthesizedCases] = useState<any[]>([])
  const [synthesizeTargetCollectionId, setSynthesizeTargetCollectionId] = useState<number | undefined>()

  // AI Reviewer State
  const [aiReviewModalOpen, setAiReviewModalOpen] = useState(false)
  const [aiReviewing, setAiReviewing] = useState(false)
  const [reviewSummary, setReviewSummary] = useState('')
  const [reviewSuggestedCases, setReviewSuggestedCases] = useState<any[]>([])

  // 获取当前项目选择的环境存储键（按项目分别持久化）
  // TODO: 从路由参数或上下文获取当前项目 ID
  const getEnvStorageKey = (projectId?: number) => {
    return projectId ? `api-test-project-${projectId}-selected-env-id` : 'api-test-selected-env-id'
  }
  const currentProjectId = undefined // 待实现：从 URL 或上下文获取
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
  const [originalFormData, setOriginalFormData] = useState<any>(null)

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
      console.error('恢复草稿失败', error)
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
        apiTestService.getCollections(),
        apiTestService.getCases({}),
        environmentService.getEnvironments()
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
          const env = envs.find((e: any) => e.id === envId)
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
      console.error('加载数据失败', error)
    }
  }

  const buildTreeData = (collectionsData: any[], casesData: any[]) => {
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
        title: '未分组',
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
          title: '未保存的修改',
          content: '当前用例有未保存的修改，是否保存后切换？',
          okText: '保存并切换',
          cancelText: '放弃修改',
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
          title: '未保存的修改',
          content: '当前用例有未保存的修改，是否保存后切换？',
          okText: '保存并切换',
          cancelText: '放弃修改',
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
      message.error('保存失败')
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
    let finalHeaders: Record<string, string> = {}
    let finalParams: Record<string, string> = {}
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

    const isPlainObject = (value: any) => {
      if (!value || typeof value !== 'object') return false
      if (Array.isArray(value)) return false
      return Object.getPrototypeOf(value) === Object.prototype
    }

    const resolveTemplateValue = (input: any): any => {
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

  // 复制为 cURL
  const handleCopyCurl = () => {
    if (!url) {
      message.warning('请先输入请求 URL')
      return
    }
    const curlCommand = generateCurl()
    navigator.clipboard.writeText(curlCommand)
    message.success('已复制 cURL 命令到剪贴板')
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
      title: '确认删除',
      content: `确定要删除用例 "${caseName}" 吗？此操作不可恢复。`,
      okText: '确认删除',
      cancelText: '取消',
      okButtonProps: { danger: true },
      onOk: async () => {
        try {
          const res = await apiTestService.deleteCase(caseId)
          if (res.code === 200) {
            message.success('用例删除成功')
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
        api_key: aiApiKey
      })
      if (res.code === 200 && res.data?.cases) {
        setSynthesizedCases(res.data.cases)
        message.success(`成功生成 ${res.data.cases.length} 个测试用例`)
      } else {
        message.error(res.message || '生成失败')
      }
    } catch (e: any) {
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
        console.error('Failed to save case:', c.name, e)
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
        api_key: aiApiKey
      })
      if (res.code === 200 && res.data) {
        setReviewSummary(res.data.review_summary)
        setReviewSuggestedCases(res.data.suggested_cases || [])
        message.success('AI 集合评审完成')
      } else {
        message.error(res.message || '评审失败')
      }
    } catch (e: any) {
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
        console.error('保存用例失败:', e)
      }
    }
    message.success(`成功保存 ${successCount} 个补充用例`)
    setAiReviewModalOpen(false)
    setReviewSuggestedCases([])
    setReviewSummary('')
    loadData() // 刷新左侧列表
  }

  const appendAiLog = (status: AiLogStatus, logMessage: string) => {
    setAiExecutionLogs(prev => [...prev, { status, message: logMessage }])
  }

  const normalizeAiObject = (value: any): Record<string, any> => {
    if (value && typeof value === 'object' && !Array.isArray(value)) {
      return value
    }
    return {}
  }

  const handleAiExecute = async () => {
    if (!aiPrompt.trim()) {
      message.warning('Please enter a prompt')
      return
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

      const resolveCollectionId = (op: any): number | undefined => {
        if (op.collection_id) return Number(op.collection_id)
        if (op.collection_name && createdCollectionMap.has(op.collection_name)) {
          return createdCollectionMap.get(op.collection_name)
        }
        if (op.collection_name) {
          const found = localCollections.find((c: any) => c.name === op.collection_name)
          if (found) return found.id
        }
        
        // Fallback: If we created a collection in this run, use the latest one
        if (createdCollectionMap.size > 0) {
           const ids = Array.from(createdCollectionMap.values())
           return ids[ids.length - 1]
        }

        return activeCollectionId
      }

      const resolveEnvironmentId = (op: any): number | undefined => {
        if (op.environment_id) return Number(op.environment_id)
        if (op.environment_name && createdEnvironmentMap.has(op.environment_name)) {
          return createdEnvironmentMap.get(op.environment_name)
        }
        if (op.environment_name) {
          const found = localEnvironments.find((e: any) => e.name === op.environment_name)
          if (found) return found.id
        }
        return selectedEnvId
      }

      const resolveCaseId = (op: any): number | undefined => {
        if (op.case_id) return Number(op.case_id)
        if (op.case_name && createdCaseMap.has(op.case_name)) {
          return createdCaseMap.get(op.case_name)
        }
        if (op.case_name) {
          const found = localCases.find((c: any) => c.name === op.case_name)
          if (found) return found.id
        }
        return currentCaseId || undefined
      }

      for (let index = 0; index < operations.length; index += 1) {
        const op = operations[index]
        const opTitle = `[${index + 1}/${operations.length}] ${op.type}`

        try {
          if (op.type === 'create_environment') {
            const envRes = await environmentService.createEnvironment({
              name: op.name || `AI Env ${Date.now()}`,
              base_url: op.base_url || 'http://127.0.0.1:5211/api/v1',
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
            const updatePayload: any = {}
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
            const methodValue = String(op.method || 'GET').toUpperCase()
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
            const passedText = isPassed ? 'passed' : 'failed'
            appendAiLog(isPassed ? 'success' : 'error', `${opTitle} done: ${passedText}`)
            continue
          }

          appendAiLog('info', `${opTitle} ignored (unsupported type)`)
        } catch (error: any) {
          appendAiLog('error', `${opTitle} failed: ${error?.message || 'unknown error'}`)
        }
      }

      await loadData()
      appendAiLog('success', 'AI workflow completed')
      message.success('AI workflow completed')
    } catch (error: any) {
      appendAiLog('error', error?.message || 'AI workflow failed')
      message.error(error?.message || 'AI workflow failed')
    } finally {
      setAiRunning(false)
    }
  }

  const moreMenuItems: MenuProps['items'] = [
    { key: 'copy', icon: <CopyOutlined />, label: '复制为 cURL', onClick: handleCopyCurl },
  ]

  // 参数表格列
  const paramsColumns = [
    {
      title: '序号',
      key: 'index',
      width: 60,
      align: 'center' as const,
      render: (_: any, __: any, index: number) => (
        <Text type="secondary">{index + 1}</Text>
      ),
    },
    {
      title: '参数名',
      dataIndex: 'key',
      key: 'key',
      render: (_: any, record: any, index: number) => (
        <Input
          placeholder="参数名"
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
      title: '参数值',
      dataIndex: 'value',
      key: 'value',
      render: (_: any, record: any, index: number) => (
        <Input
          placeholder="参数值"
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
      title: '操作',
      key: 'action',
      width: 80,
      render: (_: any, __: any, index: number) => (
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
      title: '序号',
      key: 'index',
      width: 60,
      align: 'center' as const,
      render: (_: any, __: any, index: number) => (
        <Text type="secondary">{index + 1}</Text>
      ),
    },
    {
      title: 'Header 名',
      dataIndex: 'key',
      key: 'key',
      render: (_: any, record: any, index: number) => (
        <Input
          placeholder="Header 名"
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
      title: 'Header 值',
      dataIndex: 'value',
      key: 'value',
      render: (_: any, record: any, index: number) => (
        <Input
          placeholder="Header 值"
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
      title: '操作',
      key: 'action',
      width: 80,
      render: (_: any, __: any, index: number) => (
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
    } catch (error: any) {
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
    <Layout style={{ height: 'calc(100vh - 160px)', background: 'transparent' }}>
      {/* 左侧用例树和集合管理 */}
      <Sider
        width={320}
        style={{
          background: '#fff',
          borderRadius: 8,
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
                    <Tooltip title="刷新">
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
                          const caseData = (node as any).caseData
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
          ]}
        />
      </Sider>

      {/* 右侧工作区 */}
      <Content style={{ display: 'flex', flexDirection: 'column', gap: 16 }}>
        {/* 请求区域 */}
        <Card
          size="small"
          style={{ borderRadius: 8 }}
          bodyStyle={{ padding: 12 }}
        >
          {/* 请求名称输入栏 */}
          <div style={{ marginBottom: 12, display: 'flex', alignItems: 'center', gap: 8 }}>
            <Input
              placeholder="请输入请求名称（可选）"
              value={requestName}
              onChange={(e) => setRequestName(e.target.value)}
              prefix={<Text type="secondary" style={{ fontSize: 12 }}>名称:</Text>}
              allowClear
              style={{ flex: 1 }}
            />
            <Tooltip title="表单内容会自动保存为草稿，切换页面不会丢失">
              <Text type="secondary" style={{ fontSize: 12, whiteSpace: 'nowrap' }}>
                <InfoCircleOutlined /> 自动保存草稿
              </Text>
            </Tooltip>
          </div>
          {/* URL 输入栏 */}
          <div style={{ display: 'flex', gap: 8, marginBottom: 12 }}>
            <Select
              value={method}
              onChange={setMethod}
              style={{ width: 100 }}
              options={['GET', 'POST', 'PUT', 'DELETE', 'PATCH'].map((m) => ({
                value: m,
                label: (
                  <span style={{ color: methodColors[m], fontWeight: 600 }}>
                    {m}
                  </span>
                ),
              }))}
            />
            <Input
              placeholder="请输入请求 URL，例如：https://api.example.com/users"
              value={url}
              onChange={(e) => setUrl(e.target.value)}
              style={{ flex: 1 }}
            />
            <Button
              type="primary"
              icon={<SendOutlined />}
              loading={sending}
              onClick={handleSend}
            >
              发送
            </Button>
            <Tooltip title="新建用例（自动保存当前用例）">
              <Button
                icon={<FileAddOutlined />}
                onClick={handleNewCase}
              >
                新建用例
              </Button>
            </Tooltip>
            <Tooltip title={currentCaseId ? (hasUnsavedChanges ? "保存修改" : "保存") : "保存到用例"}>
              <Button
                type={currentCaseId && hasUnsavedChanges ? "primary" : "default"}
                icon={<SaveOutlined />}
                onClick={currentCaseId ? saveCurrentCase : openSaveCaseModal}
              >
                保存
              </Button>
            </Tooltip>
            <Tooltip title={currentCaseId ? "删除当前用例" : "请先选择一个已保存用例"}>
              <Button
                danger
                disabled={!currentCaseId}
                icon={<DeleteOutlined />}
                onClick={() => currentCaseId && handleDeleteCase(currentCaseId, requestName || `ID:${currentCaseId}`)}
              >
                删除用例
              </Button>
            </Tooltip>
            <Tooltip title="AI Assistant">
              <Button
                icon={<RobotOutlined />}
                onClick={() => setAiDrawerOpen(true)}
              >
                AI Assistant
              </Button>
            </Tooltip>
            <Tooltip title="AI 扩充用例">
              <Button
                type="default"
                icon={<ExperimentOutlined />}
                onClick={() => {
                  setSynthesizeTargetCollectionId(selectedCollectionId || activeCollectionId)
                  setAiSynthesizeModalOpen(true)
                }}
              >
                AI 扩充用例
              </Button>
            </Tooltip>
            <Tooltip title="AI 集合评审">
              <Button
                type="dashed"
                icon={<RobotOutlined />}
                onClick={() => {
                  if (!(selectedCollectionId || activeCollectionId)) {
                    message.warning('请先在左侧选择一个用例集合')
                    return
                  }
                  setAiReviewModalOpen(true)
                }}
              >
                AI 集合评审
              </Button>
            </Tooltip>
            <Dropdown menu={{ items: moreMenuItems }}>
              <Button icon={<MoreOutlined />} />
            </Dropdown>
          </div>

          {/* 环境选择栏 */}
          <div style={{ display: 'flex', gap: 8, marginBottom: 12, alignItems: 'center' }}>
            <Text type="secondary" style={{ fontSize: 12, minWidth: 50 }}>环境:</Text>
            <Select
              placeholder="选择测试环境"
              allowClear
              style={{ flex: 1, maxWidth: 300 }}
              value={selectedEnvId}
              onChange={handleSelectEnv}
              options={environments.map(env => ({
                value: env.id,
                label: env.name
              }))}
            />
            {currentEnv && (
              <>
                <Tag color="blue">{currentEnv.name}</Tag>
                <Button
                  type="dashed"
                  size="small"
                  onClick={applyEnvironment}
                >
                  应用配置
                </Button>
              </>
            )}
          </div>

          {/* 环境变量提示 */}
          {selectedEnvId && (
            <div style={{ marginBottom: 12 }}>
              <EnvironmentVariableHint envId={selectedEnvId} showUsage={true} />
            </div>
          )}

          {/* 请求配置 Tabs */}
          <Tabs
            activeKey={activeTab}
            onChange={setActiveTab}
            size="small"
            items={[
              {
                key: 'params',
                label: 'Params',
                children: (
                  <Table
                    size="small"
                    rowKey="rowKey"
                    columns={paramsColumns}
                    dataSource={params.map((p, i) => ({ ...p, rowKey: String(i) }))}
                    pagination={false}
                    footer={() => (
                      <Button
                        type="dashed"
                        size="small"
                        icon={<PlusOutlined />}
                        block
                        onClick={() => setParams([...params, { key: '', value: '' }])}
                      >
                        添加参数
                      </Button>
                    )}
                  />
                ),
              },
              {
                key: 'headers',
                label: 'Headers',
                children: (
                  <Table
                    size="small"
                    rowKey="rowKey"
                    columns={headersColumns}
                    dataSource={headers.map((h, i) => ({ ...h, rowKey: String(i) }))}
                    pagination={false}
                    footer={() => (
                      <Button
                        type="dashed"
                        size="small"
                        icon={<PlusOutlined />}
                        block
                        onClick={() => setHeaders([...headers, { key: '', value: '' }])}
                      >
                        添加请求头
                      </Button>
                    )}
                  />
                ),
              },
              {
                key: 'body',
                label: 'Body',
                children: (
                  <div>
                    <Space style={{ marginBottom: 8 }}>
                      <Select
                        value={bodyType}
                        onChange={setBodyType}
                        size="small"
                        options={[
                          { value: 'none', label: 'none' },
                          { value: 'json', label: 'JSON' },
                          { value: 'form', label: 'form-data' },
                          { value: 'urlencoded', label: 'x-www-form-urlencoded' },
                          { value: 'raw', label: 'raw' },
                        ]}
                  />
                  {response?.is_mock && (
                    <Tag color="purple" style={{ marginLeft: 8 }}>Mock 数据</Tag>
                  )}
                </Space>
                <MonacoEditor
                      height={150}
                      language={bodyType === 'json' ? 'json' : 'plaintext'}
                      theme="vs-light"
                      value={requestBody}
                      onChange={(value) => setRequestBody(value || '{}')}
                      options={{
                        minimap: { enabled: false },
                        fontSize: 13,
                        lineNumbers: 'on',
                        scrollBeyondLastLine: false,
                        automaticLayout: true,
                      }}
                    />
                  </div>
                ),
              },
              {
                key: 'pre-script',
                label: '前置脚本',
                children: (
                  <MonacoEditor
                    height={150}
                    language="javascript"
                    theme="vs-light"
                    value={preScript}
                    onChange={(value) => setPreScript(value || '')}
                    options={{
                      minimap: { enabled: false },
                      fontSize: 13,
                      scrollBeyondLastLine: false,
                      automaticLayout: true,
                    }}
                  />
                ),
              },
              {
                key: 'tests',
                label: '断言脚本',
                children: (
                  <MonacoEditor
                    height={150}
                    language="javascript"
                    theme="vs-light"
                    value={postScript}
                    onChange={(value) => setPostScript(value || '')}
                    options={{
                      minimap: { enabled: false },
                      fontSize: 13,
                      scrollBeyondLastLine: false,
                      automaticLayout: true,
                    }}
                  />
                ),
              },
              {
                key: 'mock',
                label: (
                  <Space size={4}>
                    <span>Mock</span>
                    {mockEnabled && <Badge status="success" />}
                  </Space>
                ),
                children: (
                  <div style={{ padding: '8px 0' }}>
                    <Space direction="vertical" style={{ width: '100%' }} size="middle">
                      <div style={{ display: 'flex', alignItems: 'center', gap: 16 }}>
                        <Space>
                          <Text>启用 Mock:</Text>
                          <Switch checked={mockEnabled} onChange={setMockEnabled} size="small" />
                        </Space>
                        <Space>
                          <Text>状态码:</Text>
                          <InputNumber 
                            value={mockResponseCode} 
                            onChange={(val) => setMockResponseCode(val || 200)} 
                            size="small" 
                            style={{ width: 80 }} 
                          />
                        </Space>
                        <Space>
                          <Text>延迟(ms):</Text>
                          <InputNumber 
                            value={mockDelayMs} 
                            onChange={(val) => setMockDelayMs(val || 0)} 
                            size="small" 
                            style={{ width: 80 }} 
                            min={0}
                          />
                        </Space>
                        {currentCaseId && (
                          <Text type="secondary" style={{ fontSize: 12 }}>
                            Mock 地址: <Text code copyable>{`${window.location.origin}/api/v1/api-test/mock/${currentCaseId}`}</Text>
                          </Text>
                        )}
                      </div>
                      
                      <div style={{ display: 'flex', gap: 16, height: 200 }}>
                        <div style={{ flex: 1, display: 'flex', flexDirection: 'column' }}>
                          <Text type="secondary" style={{ marginBottom: 4 }}>响应头 (Headers):</Text>
                          <div style={{ flex: 1, overflow: 'auto', border: '1px solid #d9d9d9', borderRadius: 4 }}>
                            <Table
                              size="small"
                              rowKey="rowKey"
                              columns={[
                                {
                                  title: 'Header 名',
                                  dataIndex: 'key',
                                  render: (_: any, record: any, index: number) => (
                                    <Input
                                      placeholder="Content-Type"
                                      size="small"
                                      value={record.key}
                                      onChange={(e) => {
                                        const newHeaders = [...mockResponseHeaders]
                                        newHeaders[index].key = e.target.value
                                        setMockResponseHeaders(newHeaders)
                                      }}
                                    />
                                  ),
                                },
                                {
                                  title: 'Header 值',
                                  dataIndex: 'value',
                                  render: (_: any, record: any, index: number) => (
                                    <Input
                                      placeholder="application/json"
                                      size="small"
                                      value={record.value}
                                      onChange={(e) => {
                                        const newHeaders = [...mockResponseHeaders]
                                        newHeaders[index].value = e.target.value
                                        setMockResponseHeaders(newHeaders)
                                      }}
                                    />
                                  ),
                                },
                                {
                                  title: '操作',
                                  width: 50,
                                  render: (_: any, __: any, index: number) => (
                                    <Button
                                      type="text"
                                      danger
                                      size="small"
                                      icon={<DeleteOutlined />}
                                      onClick={() => {
                                        const newHeaders = mockResponseHeaders.filter((_, i) => i !== index)
                                        setMockResponseHeaders(newHeaders.length > 0 ? newHeaders : [{ key: '', value: '' }])
                                      }}
                                    />
                                  ),
                                },
                              ]}
                              dataSource={mockResponseHeaders.map((h, i) => ({ ...h, rowKey: String(i) }))}
                              pagination={false}
                              footer={() => (
                                <Button
                                  type="dashed"
                                  size="small"
                                  icon={<PlusOutlined />}
                                  block
                                  onClick={() => setMockResponseHeaders([...mockResponseHeaders, { key: '', value: '' }])}
                                >
                                  添加 Header
                                </Button>
                              )}
                            />
                          </div>
                        </div>
                        
                        <div style={{ flex: 2, display: 'flex', flexDirection: 'column' }}>
                          <Text type="secondary" style={{ marginBottom: 4 }}>响应体 (Body):</Text>
                          <div style={{ flex: 1, border: '1px solid #d9d9d9', borderRadius: 4, overflow: 'hidden' }}>
                            <MonacoEditor
                              language="json"
                              theme="vs-light"
                              value={mockResponseBody}
                              onChange={(value) => setMockResponseBody(value || '')}
                              options={{
                                minimap: { enabled: false },
                                fontSize: 13,
                                scrollBeyondLastLine: false,
                                automaticLayout: true,
                              }}
                            />
                          </div>
                        </div>
                      </div>
                    </Space>
                {response?.is_mock && (
                  <Tag color="purple" style={{ marginLeft: 16 }}>Mock 数据</Tag>
                )}
              </div>
                ),
              },
            ]}
          />
        </Card>

        {/* 响应区域 */}
        <Card
          size="small"
          style={{ borderRadius: 8, flex: 1 }}
          bodyStyle={{ padding: 12, height: '100%' }}
          title={
            response ? (
              <Space>
                <Tag color={response.status < 400 ? 'success' : 'error'}>
                  {response.status} {response.statusText}
                </Tag>
                <Text type="secondary">Time: {response.time}ms</Text>
                <Text type="secondary">Size: {response.size}</Text>
              </Space>
            ) : (
              '响应'
            )
          }
        >
          {response ? (
            <Tabs
              activeKey={responseTab}
              onChange={setResponseTab}
              size="small"
              items={[
                {
                  key: 'body',
                  label: 'Body',
                  children: (
                    <MonacoEditor
                      height={250}
                      language="json"
                      theme="vs-light"
                      value={JSON.stringify(response.data, null, 2)}
                      options={{
                        readOnly: true,
                        minimap: { enabled: false },
                        fontSize: 13,
                        scrollBeyondLastLine: false,
                        automaticLayout: true,
                      }}
                    />
                  ),
                },
                {
                  key: 'headers',
                  label: 'Headers',
                  children: (
                    <Table
                      size="small"
                      dataSource={Object.entries(response.headers).map(
                        ([key, value]) => ({ key, value })
                      )}
                      columns={[
                        { title: 'Key', dataIndex: 'key', key: 'key' },
                        { title: 'Value', dataIndex: 'value', key: 'value' },
                      ]}
                      pagination={false}
                    />
                  ),
                },
                {
                  key: 'cookies',
                  label: 'Cookies',
                  children: <Empty description="暂无 Cookie" />,
                },
                {
                  key: 'test-results',
                  label: '测试结果',
                  children: (
                    <ScriptTestResults
                      scriptExecution={response?.script_execution}
                    />
                  ),
                },
              ]}
            />
          ) : (
            <Empty
              description="发送请求查看响应"
              style={{ marginTop: 60 }}
            />
          )}
        </Card>
      </Content>

      {/* AI Assistant 弹窗 */}
      <Drawer
        title={
          <Space>
            <RobotOutlined style={{ color: '#3D6E66' }} />
            <span style={{ color: '#3D6E66', fontWeight: 600 }}>AI Assistant (依赖全局系统设置)</span>
          </Space>
        }
        placement="right"
        width={520}
        open={aiDrawerOpen}
        onClose={() => setAiDrawerOpen(false)}
      >
        <Space direction="vertical" style={{ width: '100%' }} size="middle">
          <Alert
            type="info"
            showIcon
            message="AI 将通过调用平台现有的 API 来创建或更新环境、集合、用例，并执行测试。"
          />

          <Card size="small" title="模型配置" loading={loadingConfig}>
            <Form layout="vertical">
              <Form.Item label="Base URL" style={{ marginBottom: 12 }}>
                <Input
                  placeholder={globalAiConfig?.base_url || "https://api.openai.com/v1"}
                  value={aiBaseUrl}
                  onChange={(e) => setAiBaseUrl(e.target.value)}
                />
              </Form.Item>
              <Form.Item label="Model" style={{ marginBottom: 12 }}>
                <Input
                  placeholder={globalAiConfig?.model || "gpt-4o-mini"}
                  value={aiModel}
                  onChange={(e) => setAiModel(e.target.value)}
                />
              </Form.Item>
              <Form.Item label="API Key" style={{ marginBottom: 0 }}>
                <Input.Password
                  placeholder={globalAiConfig?.api_key || "请输入模型提供商的 API Key"}
                  value={aiApiKey}
                  onChange={(e) => setAiApiKey(e.target.value)}
                />
              </Form.Item>
            </Form>
          </Card>

          <TextArea
            rows={8}
            placeholder="请用自然语言描述您的需求。例如：创建一个登录接口集合，包含3个测试用例，创建对应的测试环境，然后运行该集合。"
            value={aiPrompt}
            onChange={(e) => setAiPrompt(e.target.value)}
          />

          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <Space>
              <Text type="secondary">自动运行测试</Text>
              <Switch checked={aiAutoRun} onChange={setAiAutoRun} />
            </Space>
            <Button type="primary" icon={<RobotOutlined />} loading={aiRunning} onClick={handleAiExecute}>
              执行 AI 指令
            </Button>
          </div>

          {aiSummary && <Alert type="success" showIcon message={aiSummary} />}

          {aiPlanSource && (
            <Tag color={aiPlanSource === 'llm' ? 'blue' : 'orange'}>
              来源: {aiPlanSource}
            </Tag>
          )}

          {aiPlanOperations.length > 0 && (
            <Card size="small" title={`计划执行的操作 (${aiPlanOperations.length})`}>
              <div style={{ maxHeight: 180, overflow: 'auto' }}>
                {aiPlanOperations.map((op, index) => (
                  <div key={`${op.type}-${index}`} style={{ marginBottom: 6 }}>
                    <Text code>{`${index + 1}. ${op.type}`}</Text>
                  </div>
                ))}
              </div>
            </Card>
          )}

          <Divider style={{ margin: '8px 0' }} />

          <Card size="small" title="执行日志">
            {aiExecutionLogs.length === 0 ? (
              <Empty description="暂无日志" image={Empty.PRESENTED_IMAGE_SIMPLE} />
            ) : (
              <div style={{ maxHeight: 220, overflow: 'auto' }}>
                {aiExecutionLogs.map((log, index) => (
                  <div key={`${log.status}-${index}`} style={{ marginBottom: 8 }}>
                    <Tag
                      color={
                        log.status === 'success'
                          ? 'success'
                          : log.status === 'error'
                            ? 'error'
                            : 'default'
                      }
                    >
                      {log.status.toUpperCase()}
                    </Tag>
                    <Text>{log.message}</Text>
                  </div>
                ))}
              </div>
            )}
          </Card>
        </Space>
      </Drawer>

      <Modal
        title="保存到用例"
        open={saveModalOpen}
        onCancel={() => {
          setSaveModalOpen(false)
          setSaveCaseName('')
          setSelectedCollectionId(activeCollectionId)
        }}
        onOk={handleSaveCase}
      >
        <Form layout="vertical">
          <Form.Item label="用例名称" required>
            <Input
              placeholder="请输入用例名称"
              value={saveCaseName}
              onChange={(e) => setSaveCaseName(e.target.value)}
            />
          </Form.Item>
          <Form.Item label="所属集合">
            <Select
              placeholder="选择集合（可选）"
              allowClear
              value={selectedCollectionId}
              onChange={setSelectedCollectionId}
              options={collections.map(c => ({
                value: c.id,
                label: c.name
              }))}
            />
          </Form.Item>
          <Form.Item label="请求信息">
            <Card size="small">
              <Space direction="vertical" style={{ width: '100%' }}>
                <div>
                  <Text type="secondary">方法:</Text> <Tag color={methodColors[method]}>{method}</Tag>
                </div>
                <div>
                  <Text type="secondary">URL:</Text> <Text code>{url || '未设置'}</Text>
                </div>
              </Space>
            </Card>
          </Form.Item>
        </Form>
      </Modal>

      {/* AI 扩充用例弹窗 */}
      <Modal
        title={
          <Space>
            <ExperimentOutlined style={{ color: '#3D6E66' }} />
            <span>AI 智能测试数据生成与用例裂变</span>
          </Space>
        }
        open={aiSynthesizeModalOpen}
        onCancel={() => {
          if (!aiSynthesizing) {
            setAiSynthesizeModalOpen(false)
            setSynthesizedCases([])
          }
        }}
        width={800}
        footer={
          synthesizedCases.length > 0 ? (
            <Space>
              <Button onClick={() => setSynthesizedCases([])}>重新生成</Button>
              <Button type="primary" onClick={handleSaveSynthesizedCases}>
                保存全部用例
              </Button>
            </Space>
          ) : (
            <Button
              type="primary"
              onClick={handleAiSynthesize}
              loading={aiSynthesizing}
            >
              生成测试用例
            </Button>
          )
        }
      >
        {!synthesizedCases.length ? (
          <div style={{ padding: '20px 0' }}>
            <Alert
              type="info"
              showIcon
              message="基于当前 API 定义自动生成异常和边界测试用例"
              description="AI 将自动分析当前的请求 URL、Headers、Params 和 Body，并生成包含边界值、非法注入、空值等异常测试用例，极大提升测试覆盖率。"
              style={{ marginBottom: 24 }}
            />
            <Form layout="vertical">
              <Form.Item label="生成数量">
                <Select
                  value={aiSynthesizeCount}
                  onChange={setAiSynthesizeCount}
                  style={{ width: 120 }}
                  options={[
                    { value: 3, label: '3 个' },
                    { value: 5, label: '5 个' },
                    { value: 10, label: '10 个' },
                  ]}
                />
              </Form.Item>
              <Form.Item label="保存目标分组">
                <Select
                  value={synthesizeTargetCollectionId}
                  onChange={setSynthesizeTargetCollectionId}
                  placeholder="选择用例集合（默认未分组）"
                  allowClear
                  options={collections.map(c => ({
                    value: c.id,
                    label: c.name
                  }))}
                />
              </Form.Item>
            </Form>
          </div>
        ) : (
          <div style={{ maxHeight: 500, overflow: 'auto' }}>
            <Alert 
              type="success" 
              message={`成功生成 ${synthesizedCases.length} 个测试用例，您可以预览并一键保存到左侧用例树中。`} 
              style={{ marginBottom: 16 }}
            />
            {synthesizedCases.map((c, idx) => (
              <Card 
                key={idx} 
                size="small" 
                title={<Space><Tag color={methodColors[c.method] || 'blue'}>{c.method}</Tag><Text strong>{c.name}</Text></Space>}
                style={{ marginBottom: 16 }}
              >
                <div style={{ marginBottom: 8 }}>
                  <Text type="secondary" style={{ width: 60, display: 'inline-block' }}>URL:</Text>
                  <Text code>{c.url}</Text>
                </div>
                {c.params && Object.keys(c.params).length > 0 && (
                  <div style={{ marginBottom: 8 }}>
                    <Text type="secondary" style={{ width: 60, display: 'inline-block' }}>Params:</Text>
                    <Text code>{JSON.stringify(c.params)}</Text>
                  </div>
                )}
                {c.body && Object.keys(c.body).length > 0 && (
                  <div style={{ marginBottom: 8 }}>
                    <Text type="secondary" style={{ width: 60, display: 'inline-block', verticalAlign: 'top' }}>Body:</Text>
                    <pre style={{ 
                      display: 'inline-block', 
                      margin: 0, 
                      padding: '4px 8px', 
                      background: '#f5f5f5', 
                      borderRadius: 4,
                      width: 'calc(100% - 70px)'
                    }}>
                      {JSON.stringify(c.body, null, 2)}
                    </pre>
                  </div>
                )}
              </Card>
            ))}
          </div>
        )}
      </Modal>

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
      <Modal
        title={
          <Space>
            <RobotOutlined style={{ color: '#1890ff' }} />
            <span>AI 智能用例评审与补全</span>
          </Space>
        }
        open={aiReviewModalOpen}
        onCancel={() => {
          if (!aiReviewing) {
            setAiReviewModalOpen(false)
            setReviewSummary('')
            setReviewSuggestedCases([])
          }
        }}
        width={900}
        footer={
          reviewSuggestedCases.length > 0 ? (
            <Space>
              <Button onClick={() => {
                setReviewSummary('')
                setReviewSuggestedCases([])
              }}>重新评审</Button>
              <Button type="primary" onClick={handleSaveReviewCases}>
                一键保存所有补充用例
              </Button>
            </Space>
          ) : (
            <Button
              type="primary"
              onClick={handleAiReviewCollection}
              loading={aiReviewing}
            >
              开始智能评审
            </Button>
          )
        }
      >
        {!reviewSummary && !aiReviewing ? (
          <div style={{ padding: '20px 0' }}>
            <Alert
              type="info"
              showIcon
              message="基于当前集合自动评审并补充用例"
              description="AI 将自动分析当前集合内的所有用例，指出哪些边界条件、异常场景或安全漏洞没有被覆盖，并提供一键生成补充用例的功能。"
              style={{ marginBottom: 24 }}
            />
          </div>
        ) : (
          <Spin spinning={aiReviewing} tip="AI 正在深度评审当前集合...">
            {reviewSummary && (
              <div style={{ padding: '10px 0' }}>
                <Alert
                  type="success"
                  showIcon
                  message="评审总结"
                  description={<div style={{ whiteSpace: 'pre-wrap' }}>{reviewSummary}</div>}
                  style={{ marginBottom: 24 }}
                />
                
                {reviewSuggestedCases.length > 0 && (
                  <div>
                    <div style={{ marginBottom: 12, fontWeight: 500 }}>
                      AI 建议补充的测试用例 ({reviewSuggestedCases.length} 个):
                    </div>
                    <div style={{ maxHeight: 400, overflow: 'auto', paddingRight: 8 }}>
                      {reviewSuggestedCases.map((c, i) => (
                        <Card key={i} size="small" style={{ marginBottom: 12 }}>
                          <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 8 }}>
                            <Space>
                              <Tag color={methodColors[c.method] || 'default'}>{c.method}</Tag>
                              <Text strong>{c.name}</Text>
                            </Space>
                          </div>
                          <div style={{ marginBottom: 8 }}>
                            <Text type="secondary" style={{ fontSize: 13 }}>URL: </Text>
                            <Text code>{c.url}</Text>
                          </div>
                          <div style={{ fontSize: 13, color: 'rgba(0,0,0,0.65)' }}>
                            {c.description}
                          </div>
                        </Card>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            )}
          </Spin>
        )}
      </Modal>
    </Layout>
  )
}

export default ApiTestWorkspace
