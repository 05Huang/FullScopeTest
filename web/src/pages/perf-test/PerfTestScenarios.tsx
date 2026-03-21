import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
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
} from '@ant-design/icons'
import type { ColumnsType } from 'antd/es/table'
import type { MenuProps } from 'antd'
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
  body?: any
  user_count: number
  spawn_rate: number
  duration: number
  ramp_up: number
  step_load_enabled: boolean
  step_users: number
  step_duration: number
  status: 'passed' | 'failed' | 'pending' | 'running'
  avg_response_time: number
  throughput: number
  error_rate: number
  last_run_at: string
  updated_at: string
}

const statusConfig: Record<string, { color: string; text: string }> = {
  passed: { color: 'success', text: '通过' },
  failed: { color: 'error', text: '失败' },
  pending: { color: 'default', text: '未执行' },
  running: { color: 'processing', text: '执行中' },
}

const BATCH_ACTION_CONCURRENCY = 5
const PERF_MAX_USERS = 2000

const PerfTestScenarios = () => {
  const navigate = useNavigate()
  const [loading, setLoading] = useState(false)
  const [scenarios, setScenarios] = useState<PerfTestScenario[]>([])
  const [selectedRowKeys, setSelectedRowKeys] = useState<React.Key[]>([])
  const [isModalOpen, setIsModalOpen] = useState(false)
  const [editingScenario, setEditingScenario] = useState<PerfTestScenario | null>(null)
  const [runningIds, setRunningIds] = useState<number[]>([])
  const [searchText, setSearchText] = useState('')
  const [form] = Form.useForm()

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
    } catch (error: any) {
      message.error('加载场景列表失败')
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
  const handleCreate = async (values: any) => {
    try {
      // 解析 headers 和 body JSON
      let headers: Record<string, any> | undefined = undefined
      let body: any = undefined

      if (values.headers) {
        try {
          headers = JSON.parse(values.headers)
        } catch (e) {
          message.error('Headers 格式错误，请输入有效的 JSON')
          return
        }
      }

      if (values.body) {
        try {
          body = JSON.parse(values.body)
        } catch (e) {
          message.error('Body 格式错误，请输入有效的 JSON')
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
        message.success('创建成功')
        setIsModalOpen(false)
        setEditingScenario(null)
        form.resetFields()
        loadScenarios()
      } else {
        message.error(result.message || '创建失败')
      }
    } catch (error: any) {
      message.error('创建场景失败')
    }
  }

  // 更新场景
  const handleUpdate = async (id: number, values: any) => {
    try {
      // 解析 headers 和 body JSON
      let headers: Record<string, any> | undefined = undefined
      let body: any = undefined

      if (values.headers) {
        try {
          headers = JSON.parse(values.headers)
        } catch (e) {
          message.error('Headers 格式错误，请输入有效的 JSON')
          return
        }
      }

      if (values.body) {
        try {
          body = JSON.parse(values.body)
        } catch (e) {
          message.error('Body 格式错误，请输入有效的 JSON')
          return
        }
      }

      const result = await perfTestService.updateScenario(id, {
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
      if (result.code === 200) {
        message.success('更新成功')
        setIsModalOpen(false)
        setEditingScenario(null)
        form.resetFields()
        loadScenarios()
      } else {
        message.error(result.message || '更新失败')
      }
    } catch (error: any) {
      message.error('更新场景失败')
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
        message.success('批量删除成功')
      } else {
        message.warning(`批量删除完成，成功 ${successCount}，失败 ${failedCount}`)
      }
      setSelectedRowKeys([])
      loadScenarios()
    } catch (error) {
      message.error('删除失败')
    }
  }

  // 删除场景
  const handleDelete = async (id: number) => {
    try {
      const result = await perfTestService.deleteScenario(id)
      if (result.code === 200) {
        message.success('删除成功')
        loadScenarios()
      } else {
        message.error(result.message || '删除失败')
      }
    } catch (error: any) {
      console.error('删除场景失败:', error)
      const errorMsg = error?.response?.data?.message || error?.message || '删除场景失败'
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
          message.success('性能测试已启动')
        }
        loadScenarios()
        return true
      } else {
        if (!silent) {
          message.error(result.message || '启动失败')
        }
        setRunningIds((prev) => prev.filter((i) => i !== id))
        return false
      }
    } catch (error: any) {
      console.error('启动测试失败:', error)
      const errorMsg = error?.response?.data?.message || error?.message || '启动测试失败'
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

    message.info(`正在执行 ${ids.length} 个场景，并发度 ${BATCH_ACTION_CONCURRENCY}`)
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
        message.success('测试已停止')
        setRunningIds((prev) => prev.filter((i) => i !== id))
        loadScenarios()
      } else {
        message.error(result.message || '停止失败')
      }
    } catch (error: any) {
      message.error('停止测试失败')
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
      title: '场景名称',
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
      title: '配置',
      key: 'config',
      width: 180,
      render: (_, record) => (
        <Space direction="vertical" size={0}>
          <Text>
            <UserOutlined style={{ marginRight: 4 }} />
            {record.user_count} 并发
          </Text>
          <Text type="secondary" style={{ fontSize: 12 }}>
            <ClockCircleOutlined style={{ marginRight: 4 }} />
            {formatDuration(record.duration)}
          </Text>
          {record.step_load_enabled && (
            <Text type="secondary" style={{ fontSize: 12 }}>
              阶梯: +{record.step_users} / {record.step_duration}s
            </Text>
          )}
        </Space>
      ),
    },
    {
      title: '状态',
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
      title: '响应时间',
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
      title: '吞吐量',
      dataIndex: 'throughput',
      key: 'throughput',
      width: 120,
      render: (throughput, record) => {
        if (record.status === 'pending' || !throughput) return '-'
        return <Text>{Number(throughput).toFixed(2)} req/s</Text>
      },
    },
    {
      title: '错误率',
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
      title: '最后执行',
      dataIndex: 'last_run_at',
      key: 'last_run_at',
      width: 160,
      render: (text) => text || '-',
    },
    {
      title: '操作',
      key: 'action',
      width: 180,
      render: (_, record) => {
        const isRunning = runningIds.includes(record.id) || record.status === 'running'
        return (
          <Space>
            {isRunning ? (
              <Tooltip title="停止">
                <Button
                  type="text"
                  size="small"
                  danger
                  icon={<PauseCircleOutlined />}
                  onClick={() => handleStop(record.id)}
                />
              </Tooltip>
            ) : (
              <Tooltip title="运行">
                <Button
                  type="text"
                  size="small"
                  icon={<PlayCircleOutlined style={{ color: '#52c41a' }} />}
                  onClick={() => handleRun(record)}
                />
              </Tooltip>
            )}
            <Tooltip title="查看报告">
              <Button
                type="text"
                size="small"
                icon={<LineChartOutlined />}
                disabled={record.status === 'pending'}
                onClick={() => navigate('/perf-test/results')}
              />
            </Tooltip>
            <Tooltip title="编辑">
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
            <Popconfirm
              title="确定删除此场景吗？"
              onConfirm={() => handleDelete(record.id)}
            >
              <Tooltip title="删除">
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
    { key: 'run', icon: <PlayCircleOutlined />, label: '批量执行' },
    { key: 'export', icon: <ExportOutlined />, label: '导出配置' },
    { type: 'divider' },
    { key: 'delete', icon: <DeleteOutlined />, label: '批量删除', danger: true },
  ]

  return (
    <div>
      <div
        style={{
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
          marginBottom: 16,
        }}
      >
        <Title level={4} style={{ margin: 0 }}>
          场景管理
        </Title>
        <Space>
          <Input
            placeholder="搜索场景..."
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
            刷新
          </Button>
          <Button
            type="primary"
            icon={<PlusOutlined />}
            onClick={() => {
              setEditingScenario(null)
              form.resetFields()
              setIsModalOpen(true)
            }}
          >
            新建场景
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
                  message.info('导出功能开发中')
                }
              }
            }}
            disabled={selectedRowKeys.length === 0}
          >
            <Button icon={<MoreOutlined />}>更多</Button>
          </Dropdown>
        </Space>
      </div>

      <Card>
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
      </Card>

      {/* 新建/编辑场景弹窗 */}
      <Modal
        title={editingScenario ? "编辑性能测试场景" : "新建性能测试场景"}
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
            label="场景名称"
            rules={[{ required: true, message: '请输入场景名称' }]}
          >
            <Input placeholder="请输入场景名称" />
          </Form.Item>
          <Form.Item name="description" label="描述">
            <TextArea rows={2} placeholder="请输入场景描述" />
          </Form.Item>
          <Form.Item
            name="targetUrl"
            label="目标 URL"
            rules={[
              { required: true, message: '请输入目标 URL' },
              { type: 'url', message: '请输入有效的 URL（需包含 http/https）' },
            ]}
          >
            <Input placeholder="https://api.example.com/endpoint" />
          </Form.Item>
          <Row gutter={16}>
            <Col span={8}>
              <Form.Item
                name="users"
                label="并发用户数"
                initialValue={10}
                rules={[{ required: true }]}
              >
                <InputNumber min={1} max={PERF_MAX_USERS} style={{ width: '100%' }} />
              </Form.Item>
            </Col>
            <Col span={8}>
              <Form.Item
                name="duration"
                label="持续时间（秒）"
                initialValue={60}
                rules={[{ required: true }]}
              >
                <InputNumber min={10} max={3600} style={{ width: '100%' }} />
              </Form.Item>
            </Col>
            <Col span={8}>
              <Form.Item
                name="spawnRate"
                label="用户生成速率（用户/秒）"
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
            label="开启阶梯加压"
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
                      label="每步新增用户数"
                      initialValue={10}
                      rules={[{ required: true, message: '请输入每步新增用户数' }]}
                    >
                      <InputNumber min={1} max={PERF_MAX_USERS} style={{ width: '100%' }} />
                    </Form.Item>
                  </Col>
                  <Col span={12}>
                    <Form.Item
                      name="stepDuration"
                      label="每步时长（秒）"
                      initialValue={30}
                      rules={[{ required: true, message: '请输入每步时长' }]}
                    >
                      <InputNumber min={1} max={3600} style={{ width: '100%' }} />
                    </Form.Item>
                  </Col>
                </Row>
              )
            }}
          </Form.Item>
          <Form.Item name="method" label="请求方法" initialValue="GET">
            <Select
              options={['GET', 'POST', 'PUT', 'DELETE'].map((m) => ({
                value: m,
                label: m,
              }))}
            />
          </Form.Item>
          <Form.Item name="headers" label="请求 Headers (可选)">
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
                  <Form.Item name="body" label="请求 Body (可选)">
                    <TextArea
                      rows={4}
                      placeholder='{"username": "test", "password": "123456"}'
                    />
                  </Form.Item>
                )
              }
              return null
            }}
          </Form.Item>
        </Form>
      </Modal>
    </div>
  )
}

export default PerfTestScenarios
