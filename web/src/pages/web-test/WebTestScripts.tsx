import { useState, useEffect } from 'react'
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
  Dropdown,
  Badge,
} from 'antd'
import {
  PlusOutlined,
  SearchOutlined,
  PlayCircleOutlined,
  EditOutlined,
  DeleteOutlined,
  MoreOutlined,
  CodeOutlined,
  CopyOutlined,
  ExportOutlined,
  ReloadOutlined,
} from '@ant-design/icons'
import type { ColumnsType } from 'antd/es/table'
import type { MenuProps } from 'antd'
import MonacoEditor from '@monaco-editor/react'
import { webTestService } from '@/services/webTestService'

const { Title, Text } = Typography
const { TextArea } = Input

interface WebTestScript {
  id: number
  name: string
  description: string
  browser: string
  status: 'passed' | 'failed' | 'pending' | 'running'
  step_count: number
  last_run_at: string
  last_duration: number
  updated_at: string
  script_content: string
}

const browserConfig: Record<string, { color: string; name: string }> = {
  chromium: { color: 'blue', name: 'Chromium' },
  firefox: { color: 'orange', name: 'Firefox' },
  webkit: { color: 'purple', name: 'WebKit' },
}

const statusConfig: Record<string, { color: string; text: string }> = {
  passed: { color: 'success', text: '通过' },
  failed: { color: 'error', text: '失败' },
  pending: { color: 'default', text: '未执行' },
  running: { color: 'processing', text: '执行中' },
}

const WebTestScripts = () => {
  const [loading, setLoading] = useState(false)
  const [scripts, setScripts] = useState<WebTestScript[]>([])
  const [selectedRowKeys, setSelectedRowKeys] = useState<React.Key[]>([])
  const [isModalOpen, setIsModalOpen] = useState(false)
  const [isCodeModalOpen, setIsCodeModalOpen] = useState(false)
  const [currentScript, setCurrentScript] = useState<WebTestScript | null>(null)
  const [editingScript, setEditingScript] = useState<WebTestScript | null>(null)
  const [runningIds, setRunningIds] = useState<number[]>([])
  const [searchText, setSearchText] = useState('')
  const [form] = Form.useForm()

  // 加载脚本列表
  const loadScripts = async () => {
    setLoading(true)
    try {
      const result = await webTestService.getScripts()
      if (result.code === 200) {
        setScripts(result.data || [])
      } else {
        message.error(result.message || '加载失败')
      }
    } catch (error: any) {
      message.error('加载脚本列表失败')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    loadScripts()
  }, [])

  // 创建脚本
  const handleCreate = async (values: any) => {
    try {
      const result = await webTestService.createScript({
        name: values.name,
        description: values.description,
        browser: values.browser,
      })
      if (result.code === 200 || result.code === 201) {
        message.success('创建成功')
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

  // 更新脚本
  const handleUpdate = async (id: number, values: any) => {
    try {
      const result = await webTestService.updateScript(id, {
        name: values.name,
        description: values.description,
        browser: values.browser,
      })
      if (result.code === 200) {
        message.success('更新成功')
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
        message.success('删除成功')
        loadScripts()
      } else {
        message.error(result.message || '删除失败')
      }
    } catch (error: any) {
      message.error('删除脚本失败')
    }
  }

  // 运行脚本
  const handleRun = async (id: number) => {
    setRunningIds((prev) => [...prev, id])
    try {
      const result = await webTestService.runScript(id, true)  // headless = true
      if (result.code === 200 && result.data?.success) {
        message.success('脚本执行完成')
        loadScripts()
      } else {
        message.error(result.data?.error || result.message || '执行失败')
      }
    } catch (error: any) {
      message.error('执行脚本失败')
    } finally {
      setRunningIds((prev) => prev.filter((i) => i !== id))
    }
  }

  // 查看代码
  const handleViewCode = (script: WebTestScript) => {
    setCurrentScript(script)
    setIsCodeModalOpen(true)
  }

  // 批量删除
  const handleBatchDelete = async () => {
    if (selectedRowKeys.length === 0) return
    try {
      for (const id of selectedRowKeys) {
        await webTestService.deleteScript(id as number)
      }
      message.success('批量删除成功')
      setSelectedRowKeys([])
      loadScripts()
    } catch (error) {
      message.error('删除失败')
    }
  }

  // 批量运行
  const handleBatchRun = async () => {
    if (selectedRowKeys.length === 0) return
    message.info(`正在执行 ${selectedRowKeys.length} 个脚本...`)
    for (const id of selectedRowKeys) {
      await handleRun(id as number)
    }
    setSelectedRowKeys([])
  }

  // 表格列配置
  const columns: ColumnsType<WebTestScript> = [
    {
      title: '脚本名称',
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
      title: '浏览器',
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
      title: '步骤数',
      dataIndex: 'step_count',
      key: 'step_count',
      width: 80,
      render: (steps) => <Text>{steps || 0} 步</Text>,
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
      title: '最后执行',
      dataIndex: 'last_run_at',
      key: 'last_run_at',
      width: 160,
      render: (text) => text || '-',
    },
    {
      title: '耗时',
      dataIndex: 'last_duration',
      key: 'last_duration',
      width: 80,
      render: (duration) => (duration ? `${duration.toFixed(1)}s` : '-'),
    },
    {
      title: '操作',
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
          <Tooltip title="查看代码">
            <Button
              type="text"
              size="small"
              icon={<CodeOutlined />}
              onClick={() => handleViewCode(record)}
            />
          </Tooltip>
          <Tooltip title="编辑">
            <Button 
              type="text" 
              size="small" 
              icon={<EditOutlined />}
              onClick={() => {
                setEditingScript(record)
                form.setFieldsValue({
                  name: record.name,
                  description: record.description,
                  browser: record.browser,
                })
                setIsModalOpen(true)
              }}
            />
          </Tooltip>
          <Popconfirm
            title="确定删除此脚本吗？"
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
      ),
    },
  ]

  // 更多操作菜单
  const moreMenuItems: MenuProps['items'] = [
    { key: 'run', icon: <PlayCircleOutlined />, label: '批量执行' },
    { key: 'export', icon: <ExportOutlined />, label: '导出脚本' },
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
          脚本管理
        </Title>
        <Space>
          <Input
            placeholder="搜索脚本..."
            prefix={<SearchOutlined />}
            style={{ width: 250 }}
            allowClear
            value={searchText}
            onChange={(e) => setSearchText(e.target.value)}
          />
          <Button
            icon={<ReloadOutlined />}
            onClick={loadScripts}
            loading={loading}
          >
            刷新
          </Button>
          <Button
            type="primary"
            icon={<PlusOutlined />}
            onClick={() => {
              setEditingScript(null)
              form.resetFields()
              setIsModalOpen(true)
            }}
          >
            新建脚本
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
          dataSource={scripts.filter(s => 
            !searchText || 
            s.name.toLowerCase().includes(searchText.toLowerCase()) ||
            s.description?.toLowerCase().includes(searchText.toLowerCase())
          )}
          rowKey="id"
          loading={loading}
          pagination={{
            total: scripts.length,
            showTotal: (total) => `共 ${total} 条`,
            showSizeChanger: true,
            showQuickJumper: true,
          }}
        />
      </Card>

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
          <Form.Item name="description" label="描述">
            <TextArea rows={2} placeholder="请输入脚本描述" />
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
          <Form.Item name="baseUrl" label="测试基础 URL">
            <Input placeholder="https://example.com" />
          </Form.Item>
        </Form>
      </Modal>

      {/* 查看代码弹窗 */}
      <Modal
        title={currentScript ? `脚本代码 - ${currentScript.name}` : '脚本代码'}
        open={isCodeModalOpen}
        onCancel={() => {
          setIsCodeModalOpen(false)
          setCurrentScript(null)
        }}
        footer={[
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
          <Button key="edit" type="primary" icon={<EditOutlined />}>
            编辑脚本
          </Button>,
        ]}
        width={800}
      >
        <MonacoEditor
          height={400}
          language="python"
          theme="vs-light"
          value={currentScript?.script_content || '# 暂无脚本内容'}
          options={{
            readOnly: true,
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

export default WebTestScripts
