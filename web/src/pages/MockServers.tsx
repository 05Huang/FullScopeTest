/**
 * 独立 Mock Server 管理页面
 *
 * 提供 Mock Server 的创建、规则配置、请求日志查看功能。
 * 支持路径匹配、方法匹配、条件响应、有状态响应。
 */
import { useState, useEffect, useCallback } from 'react'
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
  message,
  Popconfirm,
  Tooltip,
  Switch,
  Drawer,
  List,
  Empty,
  Select,
  InputNumber,
  Divider,
  Tabs,
} from 'antd'
import {
  PlusOutlined,
  DeleteOutlined,
  EditOutlined,
  ApiOutlined,
  FileTextOutlined,
  ThunderboltOutlined,
  ClearOutlined,
  ReloadOutlined,
} from '@ant-design/icons'
import type { ColumnsType } from 'antd/es/table'
import { useTranslation } from 'react-i18next'
import { useProjectStore } from '@/stores/projectStore'
import api from '@/services/api'

const { Title, Text, Paragraph } = Typography
const { TextArea } = Input

interface MockServerData {
  id: number
  project_id: number
  name: string
  description: string
  path_prefix: string
  is_enabled: boolean
  rule_count: number
  created_at: string
}

interface MockRuleData {
  id: number
  server_id: number
  name: string
  match_method: string
  match_path: string
  priority: number
  is_enabled: boolean
  response_code: number
  response_body: string
  response_headers: Record<string, string>
  response_delay_ms: number
  is_stateful: boolean
}

interface MockRequestLogData {
  id: number
  method: string
  path: string
  response_code: number
  matched_at: string
  rule_id: number | null
}

const MockServers = () => {
  const { t } = useTranslation()
  const currentProjectId = useProjectStore((s) => s.currentProjectId)
  const [servers, setServers] = useState<MockServerData[]>([])
  const [loading, setLoading] = useState(false)
  const [serverModalOpen, setServerModalOpen] = useState(false)
  const [editingServer, setEditingServer] = useState<MockServerData | null>(null)
  const [ruleDrawerOpen, setRuleDrawerOpen] = useState(false)
  const [currentServerId, setCurrentServerId] = useState<number | null>(null)
  const [currentServerDetail, setCurrentServerDetail] = useState<MockServerData & { rules: MockRuleData[] } | null>(null)
  const [ruleModalOpen, setRuleModalOpen] = useState(false)
  const [editingRule, setEditingRule] = useState<MockRuleData | null>(null)
  const [logDrawerOpen, setLogDrawerOpen] = useState(false)
  const [logs, setLogs] = useState<MockRequestLogData[]>([])
  const [form] = Form.useForm()
  const [ruleForm] = Form.useForm()

  const fetchServers = useCallback(async () => {
    if (!currentProjectId) return
    setLoading(true)
    try {
      const res = await api.get('/mock-servers', { params: { project_id: currentProjectId } })
      setServers((res as any).data || [])
    } catch {
      message.error('获取 Mock 服务器列表失败')
    } finally {
      setLoading(false)
    }
  }, [currentProjectId])

  useEffect(() => {
    fetchServers()
  }, [fetchServers])

  const handleCreateOrEdit = async () => {
    try {
      const values = await form.validateFields()
      if (editingServer) {
        await api.put(`/mock-servers/${editingServer.id}`, values)
        message.success('Mock 服务器已更新')
      } else {
        await api.post('/mock-servers', { ...values, project_id: currentProjectId })
        message.success('Mock 服务器已创建')
      }
      setServerModalOpen(false)
      form.resetFields()
      setEditingServer(null)
      fetchServers()
    } catch {
      message.error('操作失败')
    }
  }

  const handleDelete = async (id: number) => {
    try {
      await api.delete(`/mock-servers/${id}`)
      message.success('已删除')
      fetchServers()
    } catch {
      message.error('删除失败')
    }
  }

  const openRuleDrawer = async (serverId: number) => {
    setCurrentServerId(serverId)
    setRuleDrawerOpen(true)
    try {
      const res = await api.get(`/mock-servers/${serverId}`)
      setCurrentServerDetail((res as any).data)
    } catch {
      message.error('获取详情失败')
    }
  }

  const handleCreateOrEditRule = async () => {
    try {
      const values = await ruleForm.validateFields()
      if (editingRule) {
        await api.put(`/mock-rules/${editingRule.id}`, values)
        message.success('规则已更新')
      } else {
        await api.post(`/mock-servers/${currentServerId}/rules`, values)
        message.success('规则已创建')
      }
      setRuleModalOpen(false)
      ruleForm.resetFields()
      setEditingRule(null)
      // 刷新详情
      if (currentServerId) {
        const res = await api.get(`/mock-servers/${currentServerId}`)
        setCurrentServerDetail((res as any).data)
      }
    } catch {
      message.error('操作失败')
    }
  }

  const handleDeleteRule = async (ruleId: number) => {
    try {
      await api.delete(`/mock-rules/${ruleId}`)
      message.success('规则已删除')
      if (currentServerId) {
        const res = await api.get(`/mock-servers/${currentServerId}`)
        setCurrentServerDetail((res as any).data)
      }
    } catch {
      message.error('删除失败')
    }
  }

  const openLogs = async (serverId: number) => {
    setLogDrawerOpen(true)
    try {
      const res = await api.get(`/mock-servers/${serverId}/logs`)
      setLogs((res as any).data || [])
    } catch {
      message.error('获取日志失败')
    }
  }

  const clearLogs = async () => {
    if (!currentServerId) return
    try {
      await api.delete(`/mock-servers/${currentServerId}/logs`)
      message.success('日志已清空')
      setLogs([])
    } catch {
      message.error('清空失败')
    }
  }

  const methodColors: Record<string, string> = {
    GET: '#61affe', POST: '#49cc90', PUT: '#fca130',
    DELETE: '#f93e3e', PATCH: '#50e3c2', '*': '#999',
  }

  const serverColumns: ColumnsType<MockServerData> = [
    {
      title: '名称',
      dataIndex: 'name',
      key: 'name',
      render: (text, record) => (
        <Space>
          <ApiOutlined style={{ color: record.is_enabled ? '#52c41a' : '#d9d9d9' }} />
          <Text strong>{text}</Text>
        </Space>
      ),
    },
    {
      title: '路径前缀',
      dataIndex: 'path_prefix',
      key: 'path_prefix',
      render: (text) => <Tag color="blue">{text}</Tag>,
    },
    {
      title: '规则数',
      dataIndex: 'rule_count',
      key: 'rule_count',
      render: (count) => <Tag>{count}</Tag>,
    },
    {
      title: '状态',
      dataIndex: 'is_enabled',
      key: 'is_enabled',
      render: (enabled) => (
        <Tag color={enabled ? 'green' : 'default'}>{enabled ? '启用' : '禁用'}</Tag>
      ),
    },
    {
      title: 'Mock URL',
      key: 'mock_url',
      render: (_, record) => (
        <Tooltip title="点击复制">
          <Text
            code
            style={{ cursor: 'pointer' }}
            onClick={() => {
              const url = `${window.location.origin}/api/v1/mock/${record.id}/`
              navigator.clipboard.writeText(url)
              message.success('已复制 Mock URL')
            }}
          >
            /api/v1/mock/{record.id}/...
          </Text>
        </Tooltip>
      ),
    },
    {
      title: '操作',
      key: 'action',
      render: (_, record) => (
        <Space>
          <Tooltip title="规则管理">
            <Button size="small" icon={<FileTextOutlined />} onClick={() => openRuleDrawer(record.id)} />
          </Tooltip>
          <Tooltip title="请求日志">
            <Button size="small" icon={<ThunderboltOutlined />} onClick={() => openLogs(record.id)} />
          </Tooltip>
          <Tooltip title="编辑">
            <Button size="small" icon={<EditOutlined />} onClick={() => {
              setEditingServer(record)
              form.setFieldsValue(record)
              setServerModalOpen(true)
            }} />
          </Tooltip>
          <Popconfirm title="确认删除？" onConfirm={() => handleDelete(record.id)}>
            <Button size="small" danger icon={<DeleteOutlined />} />
          </Popconfirm>
        </Space>
      ),
    },
  ]

  const ruleColumns: ColumnsType<MockRuleData> = [
    {
      title: '规则名称',
      dataIndex: 'name',
      key: 'name',
      render: (text) => <Text strong>{text}</Text>,
    },
    {
      title: '方法',
      dataIndex: 'match_method',
      key: 'match_method',
      render: (method) => (
        <Tag color={methodColors[method] || '#999'} style={{ fontFamily: 'monospace' }}>
          {method || '*'}
        </Tag>
      ),
    },
    {
      title: '路径',
      dataIndex: 'match_path',
      key: 'match_path',
      render: (path) => <Text code>{path}</Text>,
    },
    {
      title: '状态码',
      dataIndex: 'response_code',
      key: 'response_code',
      render: (code) => <Tag color={code < 400 ? 'green' : 'red'}>{code}</Tag>,
    },
    {
      title: '优先级',
      dataIndex: 'priority',
      key: 'priority',
    },
    {
      title: '状态',
      dataIndex: 'is_enabled',
      key: 'is_enabled',
      render: (enabled) => <Tag color={enabled ? 'green' : 'default'}>{enabled ? '启用' : '禁用'}</Tag>,
    },
    {
      title: '操作',
      key: 'action',
      render: (_, record) => (
        <Space>
          <Button size="small" icon={<EditOutlined />} onClick={() => {
            setEditingRule(record)
            ruleForm.setFieldsValue(record)
            setRuleModalOpen(true)
          }} />
          <Popconfirm title="确认删除？" onConfirm={() => handleDeleteRule(record.id)}>
            <Button size="small" danger icon={<DeleteOutlined />} />
          </Popconfirm>
        </Space>
      ),
    },
  ]

  return (
    <div style={{ padding: 24 }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 16 }}>
        <Title level={4}>
          <ApiOutlined /> {t('mockServer.title')}
        </Title>
        <Button
          type="primary"
          icon={<PlusOutlined />}
          onClick={() => {
            setEditingServer(null)
            form.resetFields()
            setServerModalOpen(true)
          }}
        >
          {t('mockServer.create')}
        </Button>
      </div>

      <Card>
        <Table
          columns={serverColumns}
          dataSource={servers}
          rowKey="id"
          loading={loading}
          locale={{ emptyText: <Empty description="暂无 Mock 服务器" /> }}
        />
      </Card>

      {/* 创建/编辑服务器 Modal */}
      <Modal
        title={editingServer ? '编辑 Mock 服务器' : '创建 Mock 服务器'}
        open={serverModalOpen}
        onOk={handleCreateOrEdit}
        onCancel={() => {
          setServerModalOpen(false)
          setEditingServer(null)
          form.resetFields()
        }}
      >
        <Form form={form} layout="vertical">
          <Form.Item name="name" label={t('mockServer.name')} rules={[{ required: true }]}>
            <Input placeholder="如：订单 API Mock" />
          </Form.Item>
          <Form.Item name="description" label={t('mockServer.description')}>
            <TextArea rows={2} placeholder="描述这个 Mock 服务器的用途" />
          </Form.Item>
          <Form.Item name="path_prefix" label={t('mockServer.path')} initialValue="/">
            <Input placeholder="/api/v1/orders" />
          </Form.Item>
          <Form.Item name="is_enabled" label={t('mockServer.enabled')} valuePropName="checked" initialValue={true}>
            <Switch />
          </Form.Item>
        </Form>
      </Modal>

      {/* 规则管理 Drawer */}
      <Drawer
        title={`规则管理 — ${currentServerDetail?.name || ''}`}
        open={ruleDrawerOpen}
        onClose={() => setRuleDrawerOpen(false)}
        width={800}
        extra={
          <Button
            type="primary"
            icon={<PlusOutlined />}
            onClick={() => {
              setEditingRule(null)
              ruleForm.resetFields()
              setRuleModalOpen(true)
            }}
          >
            {t('mockServer.addRule')}
          </Button>
        }
      >
        <Table
          columns={ruleColumns}
          dataSource={currentServerDetail?.rules || []}
          rowKey="id"
          size="small"
        />
      </Drawer>

      {/* 创建/编辑规则 Modal */}
      <Modal
        title={editingRule ? '编辑规则' : '添加规则'}
        open={ruleModalOpen}
        onOk={handleCreateOrEditRule}
        onCancel={() => {
          setRuleModalOpen(false)
          setEditingRule(null)
          ruleForm.resetFields()
        }}
        width={640}
      >
        <Form form={ruleForm} layout="vertical">
          <Form.Item name="name" label="规则名称" rules={[{ required: true }]}>
            <Input placeholder="如：获取订单列表" />
          </Form.Item>
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 2fr', gap: 16 }}>
            <Form.Item name="match_method" label={t('mockServer.matchMethod')} initialValue="*">
              <Select>
                <Select.Option value="*">全部 (*)</Select.Option>
                <Select.Option value="GET">GET</Select.Option>
                <Select.Option value="POST">POST</Select.Option>
                <Select.Option value="PUT">PUT</Select.Option>
                <Select.Option value="DELETE">DELETE</Select.Option>
                <Select.Option value="PATCH">PATCH</Select.Option>
              </Select>
            </Form.Item>
            <Form.Item name="match_path" label={t('mockServer.matchPath')} rules={[{ required: true }]}>
              <Input placeholder="/orders 或 /orders/*" style={{ fontFamily: 'monospace' }} />
            </Form.Item>
          </div>
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: 16 }}>
            <Form.Item name="response_code" label={t('mockServer.statusCode')} initialValue={200}>
              <InputNumber min={100} max={599} style={{ width: '100%' }} />
            </Form.Item>
            <Form.Item name="response_delay_ms" label={t('mockServer.delay')} initialValue={0}>
              <InputNumber min={0} max={30000} style={{ width: '100%' }} />
            </Form.Item>
            <Form.Item name="priority" label="优先级" initialValue={0}>
              <InputNumber min={0} max={100} style={{ width: '100%' }} />
            </Form.Item>
          </div>
          <Form.Item name="response_body" label={t('mockServer.responseBody')}>
            <TextArea
              rows={6}
              placeholder={'{\n  "code": 200,\n  "data": []\n}'}
              style={{ fontFamily: 'monospace', fontSize: 13 }}
            />
          </Form.Item>
        </Form>
      </Modal>

      {/* 请求日志 Drawer */}
      <Drawer
        title="Mock 请求日志"
        open={logDrawerOpen}
        onClose={() => setLogDrawerOpen(false)}
        width={600}
        extra={
          <Space>
            <Button icon={<ClearOutlined />} onClick={clearLogs}>清空日志</Button>
            <Button icon={<ReloadOutlined />} onClick={() => currentServerId && openLogs(currentServerId)} />
          </Space>
        }
      >
        <List
          dataSource={logs}
          locale={{ emptyText: <Empty description={t('mockServer.noRequests')} /> }}
          renderItem={(log) => (
            <List.Item>
              <div style={{ width: '100%' }}>
                <Space style={{ marginBottom: 4 }}>
                  <Tag color={methodColors[log.method] || '#999'}>{log.method}</Tag>
                  <Text code>{log.path}</Text>
                  <Tag color={log.response_code < 400 ? 'green' : 'red'}>
                    {log.response_code}
                  </Tag>
                </Space>
                <Text type="secondary" style={{ fontSize: 12 }}>
                  {log.matched_at ? new Date(log.matched_at).toLocaleString() : ''}
                </Text>
              </div>
            </List.Item>
          )}
        />
      </Drawer>
    </div>
  )
}

export default MockServers