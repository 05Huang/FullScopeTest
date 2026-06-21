import logger from "@/utils/logger"
import { useTranslation } from 'react-i18next';
import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAiScriptGenerator } from './hooks/useAiScriptGenerator'
import ScenarioStepEditor, { type PerfScenarioStep } from './ScenarioStepEditor'
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
  InputNumber,
  Select,
  message,
  Popconfirm,
  Tooltip,
  Dropdown,
  Progress,
  Row,
  Col,
  Switch,
  type MenuProps,
} from 'antd'
import {
  PlusOutlined,
  SearchOutlined,
  PlayCircleOutlined,
  PauseCircleOutlined,
  EditOutlined,
  DeleteOutlined,
  MoreOutlined,
  ExportOutlined,
  LineChartOutlined,
  UserOutlined,
  ClockCircleOutlined,
  ReloadOutlined,
  CodeOutlined,
  CopyOutlined,
  SaveOutlined,
  RobotOutlined,
} from '@ant-design/icons'
import type { ColumnsType } from 'antd/es/table'
import MonacoEditor from '@monaco-editor/react'
import { perfTestService } from '@/services/perfTestService'
import { runWithConcurrency } from '@/utils/runWithConcurrency'

const { Title, Text } = Typography
const { TextArea } = Input

interface PerfTestScenario {
  id: number
  name: string
  description: string
  target_url: string
  method: string
  headers?: Record<string, any>
  body?: Record<string, unknown> | string | null
  user_count: number
  spawn_rate: number
  duration: number
  ramp_up: number
  step_load_enabled: boolean
  step_users: number
  step_duration: number
  status: 'passed' | 'failed' | 'pending' | 'running'
  script_content?: string
  avg_response_time: number
  throughput: number
  error_rate: number
  last_run_at: string
  updated_at: string
}

const BATCH_ACTION_CONCURRENCY = 5
const PERF_MAX_USERS = 2000

const PerfTestScenarios = () => {
  const { t } = useTranslation();

  const statusConfig: Record<string, { color: string; text: string }> = {
    passed: { color: 'success', text: t('common.passed') },
    failed: { color: 'error', text: t('common.failed') },
    pending: { color: 'default', text: t('perfTest.notExecuted') },
    running: { color: 'processing', text: t('common.running') },
  }
  const navigate = useNavigate()
  const [loading, setLoading] = useState(false)
  const [scenarios, setScenarios] = useState<PerfTestScenario[]>([])
  const [selectedRowKeys, setSelectedRowKeys] = useState<React.Key[]>([])
  const [isModalOpen, setIsModalOpen] = useState(false)
  const [editingScenario, setEditingScenario] = useState<PerfTestScenario | null>(null)
  const [runningIds, setRunningIds] = useState<number[]>([])
  const [searchText, setSearchText] = useState('')
  const [form] = Form.useForm()

  // Code Editor State
  const [scenarioSteps, setScenarioSteps] = useState<PerfScenarioStep[]>([])
  const [isCodeModalOpen, setIsCodeModalOpen] = useState(false)
  const [currentScenario, setCurrentScenario] = useState<PerfTestScenario | null>(null)
  const [isEditingCode, setIsEditingCode] = useState(false)
  const [codeContent, setCodeContent] = useState('')
  const [savingCode, setSavingCode] = useState(false)

  // AI Script Generation State (使用自定义 hook)
  const {
    isAiModalOpen,
    aiPrompt,
    aiGenerating,
    generatedScript,
    setIsAiModalOpen,
    setAiPrompt,
    openModal: openAiModal,
    closeModal: closeAiModal,
    startGeneration,
    completeGeneration,
    failGeneration,
  } = useAiScriptGenerator()

  // 加载场景列表
  const loadScenarios = async () => {
    setLoading(true)
    try {
      const result = await perfTestService.getScenarios()
      if (result.code === 200) {
        const data = result.data || []
        setScenarios(data)
        // 从数据库状态同步运行中的场景 ID
        const running = data.filter((s: PerfTestScenario) => s.status === 'running').map((s: PerfTestScenario) => s.id)
        setRunningIds(running)
      } else {
        message.error(result.message || '加载失败')
      }
    } catch (error: unknown) {
      message.error(t('perfTest.loadScenariosFailed'))
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    loadScenarios()
    // 定时刷新状态（每5秒）
    const interval = setInterval(loadScenarios, 5000)
    return () => clearInterval(interval)
  }, [])

  // 创建场景
  const handleCreate = async (values: Record<string, unknown>) => {
    try {
      // 解析 headers 和 body JSON
      let headers: Record<string, any> | undefined = undefined
      let body: Record<string, unknown> | string | undefined = undefined

      if (values.headers) {
        try {
          headers = JSON.parse(values.headers)
        } catch (e) {
          message.error(t('perfTest.headersFormatError'))
          return
        }
      }

      if (values.body) {
        try {
          body = JSON.parse(values.body as string)
        } catch (e) {
          message.error(t('perfTest.bodyFormatError'))
          return
        }
      }

      const result = await perfTestService.createScenario({
        name: values.name,
        description: values.description,
        target_url: values.targetUrl,
        method: values.method,
        headers: headers,
        body: body,
        user_count: values.users,
        duration: values.duration,
        spawn_rate: values.spawnRate,
        step_load_enabled: !!values.stepLoadEnabled,
        step_users: values.stepUsers,
        step_duration: values.stepDuration,
      })
      if (result.code === 200 || result.code === 201) {
        message.success(t('perfTest.createSuccess'))
        setIsModalOpen(false)
        setEditingScenario(null)
        form.resetFields()
        loadScenarios()
      } else {
        message.error(result.message || '创建失败')
      }
    } catch (error: unknown) {
      message.error(t('perfTest.createScenarioFailed'))
    }
  }

  // AI 辅助生成脚本
  const handleAiGenerate = async () => {
    if (!aiPrompt.trim()) {
      message.warning('请输入描述内容')
      return
    }
    startGeneration()
    try {
      const res = await perfTestService.generateScriptAI({ prompt: aiPrompt })
      if (res.code === 200 && res.data?.script_content) {
        message.success('AI 脚本生成成功')
        completeGeneration(res.data.script_content)
        closeAiModal()
        
        const createRes = await perfTestService.createScenario({
          name: t('perfTest.aiGenerate') + ' - ' + new Date().toLocaleString(),
          target_url: 'http://localhost',
          method: 'GET',
          user_count: 10,
          duration: 60,
          spawn_rate: 1,
          step_load_enabled: false,
          script_content: res.data.script_content,
        } as Record<string, unknown>)
        
        if (createRes.code === 200 || createRes.code === 201) {
          loadScenarios()
          handleViewCode(createRes.data)
        }
      } else {
        message.error(res.message || t('perfTest.aiGenerateFailed'))
      }
    } catch (e: unknown) {
      message.error(e.response?.data?.message || t('perfTest.aiGenerateFailed'))
      failGeneration()
    }
  }

  // 查看/编辑代码
  const handleViewCode = (scenario: PerfTestScenario) => {
    setCurrentScenario(scenario)
    setCodeContent(scenario.script_content || '')
    setIsEditingCode(false)
    setIsCodeModalOpen(true)
  }

  const handleUpdateScriptContent = async () => {
    if (!currentScenario) return
    setSavingCode(true)
    try {
      const result = await perfTestService.updateScenario(currentScenario.id, {
        script_content: codeContent,
      } as Record<string, unknown>)
      if (result.code === 200) {
        message.success(t('perfTest.scriptUpdated'))
        const updatedScenario = result.data
        if (updatedScenario) {
          setScenarios((prev) =>
            prev.map((s) => (s.id === updatedScenario.id ? { ...s, ...updatedScenario } : s))
          )
          setCurrentScenario((prev) =>
            prev ? { ...prev, script_content: codeContent } : prev
          )
        }
        setIsEditingCode(false)
      } else {
        message.error(result.message || t('perfTest.scriptUpdateFailed'))
      }
    } catch (error: unknown) {
      message.error(t('perfTest.scriptUpdateFailed'))
    } finally {
      setSavingCode(false)
    }
  }

  // 更新场景
  const handleUpdate = async (id: number, values: Record<string, unknown>) => {
    try {
      // 解析 headers 和 body JSON
      let headers: Record<string, any> | undefined = undefined
      let body: Record<string, unknown> | string | undefined = undefined

      if (values.headers) {
        try {
          headers = JSON.parse(values.headers as string)
        } catch (e) {
          message.error(t('perfTest.headersFormatError'))
          return
        }
      }

      if (values.body) {
        try {
          body = JSON.parse(values.body as string)
        } catch (e) {
          message.error(t('perfTest.bodyFormatError'))
          return
        }
      }

      const result = await perfTestService.updateScenario(id, {
        name: values.name as string,
        description: values.description as string,
        target_url: values.targetUrl as string,
        method: values.method as string,
        headers: headers,
        body: body,
        user_count: values.users as number,
        duration: values.duration as number,
        spawn_rate: values.spawnRate as number,
        step_load_enabled: !!values.stepLoadEnabled,
        step_users: values.stepUsers as number,
        step_duration: values.stepDuration as number,
      })
      if (result.code === 200) {
        message.success(t('perfTest.editSuccess'))
        setIsModalOpen(false)
        setEditingScenario(null)
        form.resetFields()
        loadScenarios()
      } else {
        message.error(result.message || '更新失败')
      }
    } catch (error: unknown) {
      message.error(t('perfTest.updateScenarioFailed'))
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
            const result = await perfTestService.deleteScenario(id)
            return result.code === 200
          } catch {
            return false
          }
        }
      )
      const successCount = results.filter(Boolean).length
      const failedCount = ids.length - successCount

      if (failedCount === 0) {
        message.success(t('perfTest.batchDeleteSuccess'))
      } else {
        message.warning(`批量删除完成，成功 ${successCount}，失败 ${failedCount}`)
      }
      setSelectedRowKeys([])
      loadScenarios()
    } catch (error) {
      message.error(t('perfTest.deleteFailed'))
    }
  }

  // 导出场景配置
  const handleExport = () => {
    if (selectedRowKeys.length === 0) return

    const selectedScenarios = scenarios.filter(s => selectedRowKeys.includes(s.id))
    const exportData = {
      version: '1.0',
      export_time: new Date().toISOString(),
      scenarios: selectedScenarios.map(s => ({
        name: s.name,
        description: s.description,
        target_url: s.target_url,
        method: s.method,
        headers: s.headers,
        body: s.body,
        user_count: s.user_count,
        spawn_rate: s.spawn_rate,
        duration: s.duration,
        ramp_up: s.ramp_up,
        step_load_enabled: s.step_load_enabled,
        step_users: s.step_users,
        step_duration: s.step_duration,
        script_content: s.script_content,
      }))
    }

    const blob = new Blob([JSON.stringify(exportData, null, 2)], { type: 'application/json' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `perf-test-scenarios-${new Date().toISOString().slice(0, 10)}.json`
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    URL.revokeObjectURL(url)

    message.success(`已导出 ${selectedScenarios.length} 个场景配置`)
  }

  // 删除场景
  const handleDelete = async (id: number) => {
    try {
      const result = await perfTestService.deleteScenario(id)
      if (result.code === 200) {
        message.success(t('perfTest.deleteSuccess'))
        loadScenarios()
      } else {
        message.error(result.message || '删除失败')
      }
    } catch (error: unknown) {
      logger.error('删除场景失败:', error)
      const err = error as { response?: { data?: { message?: string } }; message?: string }
      const errorMsg = err?.response?.data?.message || err?.message || '删除场景失败'
      message.error(errorMsg)
    }
  }

  // 运行场景
  const handleRun = async (
    record: PerfTestScenario,
    options?: { silent?: boolean }
  ): Promise<boolean> => {
    const silent = !!options?.silent
    const id = record.id
    setRunningIds((prev) => (prev.includes(id) ? prev : [...prev, id]))
    try {
      const result = await perfTestService.runScenario(id, {
        user_count: record.user_count,
        spawn_rate: record.spawn_rate,
        duration: record.duration,
        step_load_enabled: record.step_load_enabled,
        step_users: record.step_users,
        step_duration: record.step_duration,
      })
      if (result.code === 200) {
        if (!silent) {
          message.success(t('perfTest.testStarted'))
        }
        loadScenarios()
        return true
      } else {
        if (!silent) {
          message.error(result.message || t('perfTest.startFailed'))
        }
        setRunningIds((prev) => prev.filter((i) => i !== id))
        return false
      }
    } catch (error: unknown) {
      logger.error('启动测试失败:', error)
      const err = error as { response?: { data?: { message?: string } }; message?: string }
      const errorMsg = err?.response?.data?.message || err?.message || '启动测试失败'
      if (!silent) {
        message.error(errorMsg)
      }
      setRunningIds((prev) => prev.filter((i) => i !== id))
      return false
    }
  }

  const handleBatchRun = async () => {
    if (selectedRowKeys.length === 0) return
    const ids = selectedRowKeys.map((id) => id as number)
    const scenarioMap = new Map(scenarios.map((scenario) => [scenario.id, scenario]))

    message.info(`${t('perfTest.batchRun')}: ${ids.length}`)
    const results = await runWithConcurrency(
      ids,
      BATCH_ACTION_CONCURRENCY,
      async (id) => {
        const scenario = scenarioMap.get(id)
        if (!scenario) {
          return false
        }
        return handleRun(scenario, { silent: true })
      }
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

  // 停止场景
  const handleStop = async (id: number) => {
    try {
      const result = await perfTestService.stopScenario(id)
      if (result.code === 200) {
        message.success(t('perfTest.testStopped'))
        setRunningIds((prev) => prev.filter((i) => i !== id))
        loadScenarios()
      } else {
        message.error(result.message || '停止失败')
      }
    } catch (error: unknown) {
      message.error(t('perfTest.stopFailed'))
    }
  }

  // 格式化持续时间
  const formatDuration = (seconds: number) => {
    if (seconds < 60) return `${seconds}秒`
    if (seconds < 3600) return `${Math.floor(seconds / 60)}分钟`
    return `${Math.floor(seconds / 3600)}小时`
  }

  // 表格列配置
  const columns: ColumnsType<PerfTestScenario> = [
    {
      title: t('perfTest.scenarioName'),
      dataIndex: 'name',
      key: 'name',
      render: (text, record) => (
        <div>
          <Text strong>{text}</Text>
          <br />
          <Text type="secondary" style={{ fontSize: 12 }}>
            {record.description}
          </Text>
        </div>
      ),
    },
    {
      title: t('perfTest.configuration'),
      key: 'config',
      width: 180,
      render: (_, record) => (
        <Space direction="vertical" size={0}>
          <Text>
            <UserOutlined style={{ marginRight: 4 }} />
            {record.user_count} {t('perfTest.concurrency')}
          </Text>
          <Text type="secondary" style={{ fontSize: 12 }}>
            <ClockCircleOutlined style={{ marginRight: 4 }} />
            {formatDuration(record.duration)}
          </Text>
          {record.step_load_enabled && (
            <Text type="secondary" style={{ fontSize: 12 }}>
              {t('perfTest.stepLoad')}: +{record.step_users} / {record.step_duration}s
            </Text>
          )}
        </Space>
      ),
    },
    {
      title: t('perfTest.status'),
      dataIndex: 'status',
      key: 'status',
      width: 100,
      render: (status, record) => {
        const isRunning = runningIds.includes(record.id)
        const displayStatus = isRunning ? 'running' : (status || 'pending')
        return (
          <Tag color={statusConfig[displayStatus]?.color || 'default'}>
            {statusConfig[displayStatus]?.text || displayStatus}
          </Tag>
        )
      },
    },
    {
      title: t('perfTest.responseTime'),
      dataIndex: 'avg_response_time',
      key: 'avg_response_time',
      width: 120,
      render: (time, record) => {
        if (record.status === 'pending' || !time) return '-'
        const color = time < 500 ? '#52c41a' : time < 1500 ? '#faad14' : '#ff4d4f'
        return <Text style={{ color }}>{Number(time).toFixed(2)} ms</Text>
      },
    },
    {
      title: t('perfTest.throughput'),
      dataIndex: 'throughput',
      key: 'throughput',
      width: 120,
      render: (throughput, record) => {
        if (record.status === 'pending' || !throughput) return '-'
        return <Text>{Number(throughput).toFixed(2)} req/s</Text>
      },
    },
    {
      title: t('perfTest.errorRate'),
      dataIndex: 'error_rate',
      key: 'error_rate',
      width: 120,
      render: (rate, record) => {
        if (record.status === 'pending' || rate === null || rate === undefined) return '-'
        const color = rate < 1 ? '#52c41a' : rate < 5 ? '#faad14' : '#ff4d4f'
        return (
          <Progress
            percent={rate}
            size="small"
            strokeColor={color}
            format={(p) => `${p?.toFixed(1)}%`}
          />
        )
      },
    },
    {
      title: t('perfTest.lastRun'),
      dataIndex: 'last_run_at',
      key: 'last_run_at',
      width: 160,
      render: (text) => text || '-',
    },
    {
      title: t('perfTest.action'),
      key: 'action',
      width: 180,
      render: (_, record) => {
        const isRunning = runningIds.includes(record.id) || record.status === 'running'
        return (
          <Space>
            {isRunning ? (
              <Tooltip title={t('perfTest.stop')}>
                <Button
                  type="text"
                  size="small"
                  danger
                  icon={<PauseCircleOutlined />}
                  onClick={() => handleStop(record.id)}
                />
              </Tooltip>
            ) : (
              <Tooltip title={t('perfTest.run')}>
                <Button
                  type="text"
                  size="small"
                  icon={<PlayCircleOutlined style={{ color: '#52c41a' }} />}
                  onClick={() => handleRun(record)}
                />
              </Tooltip>
            )}
            <Tooltip title={t('reports.viewReport')}>
              <Button
                type="text"
                size="small"
                icon={<LineChartOutlined />}
                disabled={record.status === 'pending'}
                onClick={() => navigate('/perf-test/results')}
              />
            </Tooltip>
            <Tooltip title={t('common.edit')}>
              <Button
                type="text"
                size="small"
                icon={<EditOutlined />}
                onClick={() => {
                  setEditingScenario(record)
                  form.setFieldsValue({
                    name: record.name,
                    description: record.description,
                    targetUrl: record.target_url,
                    method: record.method,
                    users: record.user_count,
                    duration: record.duration,
                    spawnRate: record.spawn_rate,
                    stepLoadEnabled: record.step_load_enabled,
                    stepUsers: record.step_users,
                    stepDuration: record.step_duration,
                    headers: record.headers ? JSON.stringify(record.headers, null, 2) : undefined,
                    body: record.body ? JSON.stringify(record.body, null, 2) : undefined,
                  })
                  setIsModalOpen(true)
                }}
              />
            </Tooltip>
            <Tooltip title={t('perfTest.viewCode')}>
              <Button
                type="text"
                size="small"
                icon={<CodeOutlined />}
                onClick={() => handleViewCode(record)}
              />
            </Tooltip>
            <Popconfirm
              title={t('perfTest.confirmDeleteScenario')}
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
        )
      },
    },
  ]

  // 更多操作菜单
  const moreMenuItems: MenuProps['items'] = [
    { key: 'run', icon: <PlayCircleOutlined />, label: t('perfTest.batchRun') },
    { key: 'export', icon: <ExportOutlined />, label: t('perfTest.exportConfig') },
    { type: 'divider' },
    { key: 'delete', icon: <DeleteOutlined />, label: t('perfTest.batchDelete'), danger: true },
  ]

  return (
    <div className="fst-page">
      <div className="fst-page-header fst-animate-in">
        <h1 className="fst-page-title">{t('perfTest.scenarioManagement')}</h1>
        <Space>
          <Input
            placeholder={t('perfTest.searchScenarios')}
            prefix={<SearchOutlined />}
            style={{ width: 250 }}
            allowClear
            value={searchText}
            onChange={(e) => setSearchText(e.target.value)}
          />
          <Button
            icon={<ReloadOutlined />}
            onClick={loadScenarios}
            loading={loading}
          >
            {t('common.refresh')}
          </Button>
          <Button
            type="primary"
            icon={<RobotOutlined />}
            onClick={() => setIsAiModalOpen(true)}
          >
            {t('perfTest.aiGenerate')}
          </Button>
          <Button
            type="primary"
            icon={<PlusOutlined />}
            onClick={() => {
              setEditingScenario(null)
              form.resetFields()
              setScenarioSteps([])
              setIsModalOpen(true)
            }}
          >
            {t('perfTest.createScenario')}
          </Button>
          <Dropdown
            menu={{ 
              items: moreMenuItems,
              onClick: ({ key }) => {
                if (key === 'delete') {
                  handleBatchDelete()
                } else if (key === 'run') {
                  handleBatchRun()
                } else if (key === 'export') {
                  handleExport()
                }
              }
            }}
            disabled={selectedRowKeys.length === 0}
          >
            <Button icon={<MoreOutlined />}>{t('common.more')}</Button>
          </Dropdown>
        </Space>
      </div>

      <div className="fst-ios-card fst-animate-in fst-animate-in-1">
        <div className="fst-table-wrap">
          <Table
            rowSelection={{
              selectedRowKeys,
              onChange: setSelectedRowKeys,
            }}
            columns={columns}
            dataSource={scenarios.filter(s =>
              !searchText ||
              s.name.toLowerCase().includes(searchText.toLowerCase()) ||
              s.description?.toLowerCase().includes(searchText.toLowerCase()) ||
              s.target_url?.toLowerCase().includes(searchText.toLowerCase())
            )}
            rowKey="id"
            loading={loading}
            pagination={{
              total: scenarios.length,
              showTotal: (total) => `共 ${total} 条`,
              showSizeChanger: true,
              showQuickJumper: true,
            }}
          />
        </div>
      </div>

      {/* 新建/编辑场景弹窗 */}
      <Modal
        title={editingScenario ? t('perfTest.editScenarioTitle') : t('perfTest.newScenarioTitle')}
        open={isModalOpen}
        onCancel={() => {
          setIsModalOpen(false)
          setEditingScenario(null)
          form.resetFields()
        }}
        onOk={() => {
          form.validateFields().then((values) => {
            if (editingScenario) {
              handleUpdate(editingScenario.id, values)
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
            label={t('perfTest.scenarioName')}
            rules={[{ required: true, message: t('perfTest.scenarioName') }]}
          >
            <Input placeholder={t('perfTest.scenarioName')} />
          </Form.Item>
          <Form.Item name="description" label={t('perfTest.scenarioDesc')}>
            <TextArea rows={2} placeholder={t('perfTest.scenarioDesc')} />
          </Form.Item>
          <Form.Item
            name="targetUrl"
            label={t('perfTest.targetUrl')}
            rules={[
              { required: true, message: t('perfTest.targetUrlRequired') },
              { type: 'url', message: t('perfTest.targetUrlRequired') },
            ]}
          >
            <Input placeholder={t('perfTest.targetUrlPlaceholder')} />
          </Form.Item>
          <Row gutter={16}>
            <Col span={8}>
              <Form.Item
                name="users"
                label={t('perfTest.concurrentUsers')}
                initialValue={10}
                rules={[{ required: true }]}
              >
                <InputNumber min={1} max={PERF_MAX_USERS} style={{ width: '100%' }} />
              </Form.Item>
            </Col>
            <Col span={8}>
              <Form.Item
                name="duration"
                label={t('perfTest.duration')}
                initialValue={60}
                rules={[{ required: true }]}
              >
                <InputNumber min={10} max={3600} style={{ width: '100%' }} />
              </Form.Item>
            </Col>
            <Col span={8}>
              <Form.Item
                name="spawnRate"
                label={t('perfTest.rps')}
                initialValue={1}
                rules={[{ required: true }]}
                tooltip="每秒启动多少个用户"
              >
                <InputNumber min={1} max={50} style={{ width: '100%' }} />
              </Form.Item>
            </Col>
          </Row>
          <Form.Item
            name="stepLoadEnabled"
            label={t('perfTest.rampUp')}
            valuePropName="checked"
            initialValue={false}
          >
            <Switch />
          </Form.Item>
          <Form.Item noStyle shouldUpdate={(prev, curr) => prev.stepLoadEnabled !== curr.stepLoadEnabled}>
            {({ getFieldValue }) => {
              if (!getFieldValue('stepLoadEnabled')) {
                return null
              }

              return (
                <Row gutter={16}>
                  <Col span={12}>
                    <Form.Item
                      name="stepUsers"
                      label={t('perfTest.stepUsers')}
                      initialValue={10}
                      rules={[{ required: true, message: t('perfTest.stepUsers') }]}
                    >
                      <InputNumber min={1} max={PERF_MAX_USERS} style={{ width: '100%' }} />
                    </Form.Item>
                  </Col>
                  <Col span={12}>
                    <Form.Item
                      name="stepDuration"
                      label={t('perfTest.stepDuration')}
                      initialValue={30}
                      rules={[{ required: true, message: t('perfTest.stepDuration') }]}
                    >
                      <InputNumber min={1} max={3600} style={{ width: '100%' }} />
                    </Form.Item>
                  </Col>
                </Row>
              )
            }}
          </Form.Item>
          <Form.Item name="method" label={t('apiTest.method')} initialValue="GET">
            <Select
              options={['GET', 'POST', 'PUT', 'DELETE'].map((m) => ({
                value: m,
                label: m,
              }))}
            />
          </Form.Item>
          <Form.Item name="headers" label={t('perfTest.requestHeaders')}>
            <TextArea
              rows={3}
              placeholder='{"Authorization": "Bearer token", "Content-Type": "application/json"}'
            />
          </Form.Item>
          <Form.Item noStyle shouldUpdate={(prev, curr) => prev.method !== curr.method}>
            {({ getFieldValue }) => {
              const method = getFieldValue('method')
              if (['POST', 'PUT', 'PATCH'].includes(method)) {
                return (
                  <Form.Item name="body" label={t('perfTest.requestBody')}>
                    <TextArea
                      rows={4}
                      placeholder='{"username": "test", "password": "REDACTED_PASSWORD"}'
                    />
                  </Form.Item>
                )
              }
              return null
            }}
          </Form.Item>
        </Form>
        {/* 多步骤用户旅程编辑器 */}
        <div style={{ marginTop: 16 }}>
          <ScenarioStepEditor steps={scenarioSteps} onChange={setScenarioSteps} />
        </div>
      </Modal>

      {/* AI 辅助生成弹窗 */}
      <Modal
        title={
          <Space>
            <RobotOutlined style={{ color: '#722ed1' }} />
            <span>{t('perfTest.aiGenerateTitle')}</span>
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
        okText={t('perfTest.generateAndPreview')}
      >
        <div style={{ marginBottom: 16 }}>
          <Text type="secondary">
            {t('perfTest.aiGenerateDesc')}
          </Text>
        </div>
        <TextArea
          rows={6}
          placeholder={t('perfTest.aiGeneratePlaceholder')}
          value={aiPrompt}
          onChange={(e) => setAiPrompt(e.target.value)}
          disabled={aiGenerating}
        />
      </Modal>

      {/* 查看代码弹窗 */}
      <Modal
        title={currentScenario ? `${t('perfTest.scriptCode')} - ${currentScenario.name}` : t('perfTest.scriptCode')}
        open={isCodeModalOpen}
        onCancel={() => {
          setIsCodeModalOpen(false)
          setCurrentScenario(null)
          setIsEditingCode(false)
        }}
        footer={
          isEditingCode
            ? [
                <Button
                  key="cancel"
                  onClick={() => {
                    if (currentScenario) {
                      setCodeContent(currentScenario.script_content || '')
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
                  {t('perfTest.saveScript')}
                </Button>,
              ]
            : [
                <Button
                  key="copy"
                  icon={<CopyOutlined />}
                  onClick={() => {
                    if (currentScenario?.script_content) {
                      navigator.clipboard.writeText(currentScenario.script_content)
                      message.success(t('perfTest.copiedToClipboard'))
                    }
                  }}
                >
                  {t('perfTest.copyCode')}
                </Button>,
                <Button
                  key="edit"
                  type="primary"
                  icon={<EditOutlined />}
                  onClick={() => {
                    if (currentScenario) {
                      setCodeContent(currentScenario.script_content || '')
                      setIsEditingCode(true)
                    }
                  }}
                >
                  {t('common.edit')}
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
              : currentScenario?.script_content || `# ${t('perfTest.noScriptContent')}`
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
    </div>
  )
}

export default PerfTestScenarios
