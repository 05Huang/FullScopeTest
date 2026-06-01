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
  Tabs,
  Row,
  Col,
} from 'antd'
import {
  PlusOutlined,
  SearchOutlined,
  PlayCircleOutlined,
  EditOutlined,
  DeleteOutlined,
  MoreOutlined,
  MobileOutlined,
  CopyOutlined,
  ExportOutlined,
  ReloadOutlined,
  SettingOutlined,
  SaveOutlined,
} from '@ant-design/icons'
import type { ColumnsType } from 'antd/es/table'
import type { MenuProps } from 'antd'
import MonacoEditor from '@monaco-editor/react'
import { appTestService } from '@/services/appTestService'
import { useProjectStore } from '@/stores/projectStore'

const { Title, Text } = Typography
const { TextArea } = Input
const { TabPane } = Tabs

interface AppTestScript {
  id: number
  name: string
  description: string
  collection_id?: number | null
  collection_name?: string
  platform: string
  app_path?: string
  app_package?: string
  app_activity?: string
  bundle_id?: string
  device_name?: string
  platform_version?: string
  automation_name: string
  appium_server: string
  script_content: string
  status: string
  last_result?: any
  last_run_at?: string
  is_enabled: boolean
  updated_at: string
}

interface Collection {
  id: number
  name: string
  description?: string
  script_count: number
}

const statusConfig: Record<string, { color: string; text: string }> = {
  passed: { color: 'success', text: '通过' },
  failed: { color: 'error', text: '失败' },
  pending: { color: 'default', text: '未执行' },
  running: { color: 'processing', text: '执行中' },
}

const platformOptions = [
  { value: 'android', label: 'Android' },
  { value: 'ios', label: 'iOS' },
]

const automationOptions = [
  { value: 'UiAutomator2', label: 'UiAutomator2 (Android)' },
  { value: 'XCUITest', label: 'XCUITest (iOS)' },
  { value: 'Espresso', label: 'Espresso (Android)' },
]

const AppTestScripts = () => {
  const { currentProjectId } = useProjectStore()
  const [loading, setLoading] = useState(false)
  const [scripts, setScripts] = useState<AppTestScript[]>([])
  const [collections, setCollections] = useState<Collection[]>([])
  const [selectedRowKeys, setSelectedRowKeys] = useState<React.Key[]>([])
  const [searchText, setSearchText] = useState('')
  const [selectedCollectionId, setSelectedCollectionId] = useState<number | undefined>()
  const [isModalOpen, setIsModalOpen] = useState(false)
  const [editingScript, setEditingScript] = useState<AppTestScript | null>(null)
  const [form] = Form.useForm()

  // 编辑器状态
  const [editorScript, setEditorScript] = useState<AppTestScript | null>(null)
  const [scriptContent, setScriptContent] = useState('')
  const [configForm] = Form.useForm()

  useEffect(() => {
    loadData()
  }, [currentProjectId])

  const loadData = async () => {
    setLoading(true)
    try {
      const [scriptsRes, collectionsRes] = await Promise.all([
        appTestService.getScripts({ project_id: currentProjectId }),
        appTestService.getCollections(currentProjectId),
      ])

      if (scriptsRes.code === 200) {
        setScripts(scriptsRes.data || [])
      }
      if (collectionsRes.code === 200) {
        setCollections(collectionsRes.data || [])
      }
    } catch {
      message.error('加载数据失败')
    } finally {
      setLoading(false)
    }
  }

  // 创建脚本
  const handleCreate = async (values: any) => {
    try {
      const res = await appTestService.createScript({
        ...values,
        project_id: currentProjectId,
      })
      if (res.code === 200 || res.code === 201) {
        message.success('创建成功')
        setIsModalOpen(false)
        form.resetFields()
        loadData()
      }
    } catch {
      message.error('创建失败')
    }
  }

  // 更新脚本
  const handleUpdate = async (id: number, values: any) => {
    try {
      const res = await appTestService.updateScript(id, values)
      if (res.code === 200) {
        message.success('更新成功')
        setIsModalOpen(false)
        setEditingScript(null)
        form.resetFields()
        loadData()
      }
    } catch {
      message.error('更新失败')
    }
  }

  // 删除脚本
  const handleDelete = async (id: number) => {
    try {
      const res = await appTestService.deleteScript(id)
      if (res.code === 200) {
        message.success('删除成功')
        loadData()
      }
    } catch {
      message.error('删除失败')
    }
  }

  // 复制脚本
  const handleCopy = async (record: AppTestScript) => {
    try {
      const res = await appTestService.createScript({
        name: `${record.name} (副本)`,
        description: record.description,
        collection_id: record.collection_id ?? undefined,
        platform: record.platform,
        app_path: record.app_path,
        app_package: record.app_package,
        app_activity: record.app_activity,
        bundle_id: record.bundle_id,
        device_name: record.device_name,
        platform_version: record.platform_version,
        automation_name: record.automation_name,
        appium_server: record.appium_server,
        script_content: record.script_content,
        project_id: currentProjectId,
      })
      if (res.code === 200 || res.code === 201) {
        message.success('复制成功')
        loadData()
      }
    } catch {
      message.error('复制失败')
    }
  }

  // 执行脚本
  const handleRun = async (id: number) => {
    try {
      const res = await appTestService.runScript(id)
      if (res.code === 200) {
        message.success('脚本已提交执行')
        loadData()
      }
    } catch {
      message.error('执行失败')
    }
  }

  // 批量删除
  const handleBatchDelete = async () => {
    if (selectedRowKeys.length === 0) return

    try {
      for (const id of selectedRowKeys) {
        await appTestService.deleteScript(id as number)
      }
      message.success('批量删除成功')
      setSelectedRowKeys([])
      loadData()
    } catch {
      message.error('删除失败')
    }
  }

  // 打开编辑器
  const handleOpenEditor = (script: AppTestScript) => {
    setEditorScript(script)
    setScriptContent(script.script_content || '')
    configForm.setFieldsValue({
      platform: script.platform,
      app_path: script.app_path,
      app_package: script.app_package,
      app_activity: script.app_activity,
      bundle_id: script.bundle_id,
      device_name: script.device_name,
      platform_version: script.platform_version,
      automation_name: script.automation_name,
      appium_server: script.appium_server,
    })
  }

  // 保存脚本内容
  const handleSaveScript = async () => {
    if (!editorScript) return

    try {
      const configValues = configForm.getFieldsValue()
      const res = await appTestService.updateScript(editorScript.id, {
        script_content: scriptContent,
        ...configValues,
      })
      if (res.code === 200) {
        message.success('保存成功')
        loadData()
      }
    } catch {
      message.error('保存失败')
    }
  }

  // 表格列配置
  const columns: ColumnsType<AppTestScript> = [
    {
      title: '脚本名称',
      dataIndex: 'name',
      key: 'name',
      render: (text, record) => (
        <Space>
          <MobileOutlined style={{ color: '#1890ff' }} />
          <Text strong>{text}</Text>
          {!record.is_enabled && <Tag color="default">已禁用</Tag>}
        </Space>
      ),
    },
    {
      title: '平台',
      dataIndex: 'platform',
      key: 'platform',
      width: 100,
      render: (platform) => (
        <Tag color={platform === 'android' ? 'green' : 'blue'}>
          {platform === 'android' ? 'Android' : 'iOS'}
        </Tag>
      ),
    },
    {
      title: '设备',
      dataIndex: 'device_name',
      key: 'device_name',
      width: 150,
      render: (text) => text || '-',
    },
    {
      title: '状态',
      dataIndex: 'status',
      key: 'status',
      width: 100,
      render: (status) => {
        const config = statusConfig[status] || statusConfig.pending
        return <Badge status={config.color as any} text={config.text} />
      },
    },
    {
      title: '最后执行',
      dataIndex: 'last_run_at',
      key: 'last_run_at',
      width: 180,
      render: (text) => text ? new Date(text).toLocaleString('zh-CN') : '-',
    },
    {
      title: '操作',
      key: 'action',
      width: 200,
      render: (_, record) => (
        <Space size="small">
          <Tooltip title="编辑">
            <Button
              type="text"
              size="small"
              icon={<EditOutlined />}
              onClick={() => {
                setEditingScript(record)
                form.setFieldsValue(record)
                setIsModalOpen(true)
              }}
            />
          </Tooltip>
          <Tooltip title="脚本编辑器">
            <Button
              type="text"
              size="small"
              icon={<SettingOutlined />}
              onClick={() => handleOpenEditor(record)}
            />
          </Tooltip>
          <Tooltip title="执行">
            <Button
              type="text"
              size="small"
              icon={<PlayCircleOutlined style={{ color: '#52c41a' }} />}
              onClick={() => handleRun(record.id)}
              disabled={record.status === 'running'}
            />
          </Tooltip>
          <Tooltip title="复制">
            <Button
              type="text"
              size="small"
              icon={<CopyOutlined />}
              onClick={() => handleCopy(record)}
            />
          </Tooltip>
          <Popconfirm
            title="确定删除此脚本？"
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
    { key: 'export', icon: <ExportOutlined />, label: '导出脚本' },
    { type: 'divider' },
    { key: 'delete', icon: <DeleteOutlined />, label: '批量删除', danger: true },
  ]

  // 筛选后的脚本列表
  const filteredScripts = scripts.filter(s => {
    const matchSearch = !searchText ||
      s.name.toLowerCase().includes(searchText.toLowerCase()) ||
      s.description?.toLowerCase().includes(searchText.toLowerCase())
    const matchCollection = !selectedCollectionId || s.collection_id === selectedCollectionId
    return matchSearch && matchCollection
  })

  return (
    <div className="fst-page">
      <div className="fst-page-header fst-animate-in">
        <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
          <div className="fst-stat-icon fst-stat-icon--primary"><MobileOutlined style={{ fontSize: 18 }} /></div>
          <h1 className="fst-page-title">APP 自动化测试</h1>
        </div>
        <div style={{ display: 'flex', gap: 8 }}>
          <button className="fst-btn fst-btn--ghost fst-btn--sm" onClick={loadData}><ReloadOutlined /> 刷新</button>
          <button className="fst-btn fst-btn--primary fst-btn--sm" onClick={() => {
            setEditingScript(null)
            form.resetFields()
            setIsModalOpen(true)
          }}>
            新建脚本
          </button>
          <Dropdown
            menu={{
              items: moreMenuItems,
              onClick: ({ key }) => {
                if (key === 'delete') {
                  handleBatchDelete()
                } else if (key === 'export') {
                  message.info('导出功能开发中')
                }
              }
            }}
            disabled={selectedRowKeys.length === 0}
          >
            <Button icon={<MoreOutlined />}>更多</Button>
          </Dropdown>
        </div>
      </div>

      <div className="fst-ios-card fst-animate-in fst-animate-in-1">
        <div style={{ marginBottom: 16, display: 'flex', gap: 16 }}>
          <Input
            placeholder="搜索脚本名称"
            prefix={<SearchOutlined />}
            value={searchText}
            onChange={e => setSearchText(e.target.value)}
            style={{ width: 250 }}
            allowClear
          />
          <Select
            placeholder="按用例集筛选"
            value={selectedCollectionId}
            onChange={setSelectedCollectionId}
            style={{ width: 200 }}
            allowClear
            options={collections.map(c => ({ value: c.id, label: `${c.name} (${c.script_count})` }))}
          />
        </div>

        <Table
          rowSelection={{
            selectedRowKeys,
            onChange: setSelectedRowKeys,
          }}
          columns={columns}
          dataSource={filteredScripts}
          rowKey="id"
          loading={loading}
          pagination={{
            total: filteredScripts.length,
            showTotal: (total) => `共 ${total} 条`,
            showSizeChanger: true,
            defaultPageSize: 20,
          }}
        />
      </div>

      {/* 创建/编辑模态框 */}
      <Modal
        title={editingScript ? '编辑脚本' : '新建脚本'}
        open={isModalOpen}
        onCancel={() => {
          setIsModalOpen(false)
          setEditingScript(null)
          form.resetFields()
        }}
        onOk={() => form.submit()}
        width={600}
      >
        <Form
          form={form}
          layout="vertical"
          onFinish={editingScript ? (values) => handleUpdate(editingScript.id, values) : handleCreate}
        >
          <Form.Item name="name" label="脚本名称" rules={[{ required: true, message: '请输入脚本名称' }]}>
            <Input placeholder="请输入脚本名称" />
          </Form.Item>
          <Form.Item name="description" label="描述">
            <TextArea rows={2} placeholder="请输入描述" />
          </Form.Item>
          <Row gutter={16}>
            <Col span={12}>
              <Form.Item name="platform" label="平台" initialValue="android">
                <Select options={platformOptions} />
              </Form.Item>
            </Col>
            <Col span={12}>
              <Form.Item name="automation_name" label="自动化引擎" initialValue="UiAutomator2">
                <Select options={automationOptions} />
              </Form.Item>
            </Col>
          </Row>
          <Form.Item name="collection_id" label="所属用例集">
            <Select
              placeholder="选择用例集"
              allowClear
              options={collections.map(c => ({ value: c.id, label: c.name }))}
            />
          </Form.Item>
        </Form>
      </Modal>

      {/* 脚本编辑器模态框 */}
      <Modal
        title={
          <Space>
            <SettingOutlined />
            <span>脚本编辑器 - {editorScript?.name}</span>
          </Space>
        }
        open={!!editorScript}
        onCancel={() => setEditorScript(null)}
        width={1000}
        footer={
          <Space>
            <Button onClick={() => setEditorScript(null)}>关闭</Button>
            <Button type="primary" icon={<SaveOutlined />} onClick={handleSaveScript}>
              保存
            </Button>
          </Space>
        }
      >
        <Tabs defaultActiveKey="script">
          <TabPane tab="脚本代码" key="script">
            <MonacoEditor
              height="500px"
              language="python"
              value={scriptContent}
              onChange={(value) => setScriptContent(value || '')}
              options={{
                minimap: { enabled: false },
                fontSize: 14,
                lineNumbers: 'on',
                scrollBeyondLastLine: false,
                automaticLayout: true,
              }}
            />
          </TabPane>
          <TabPane tab="Appium 配置" key="config">
            <Form form={configForm} layout="vertical" style={{ maxWidth: 600 }}>
              <Form.Item name="appium_server" label="Appium Server">
                <Input placeholder="http://localhost:4723" />
              </Form.Item>
              <Form.Item name="app_path" label="APP 路径">
                <Input placeholder="APK/IPA 文件路径或 URL" />
              </Form.Item>
              <Form.Item name="device_name" label="设备名称">
                <Input placeholder="emulator-5554 或 iPhone Simulator" />
              </Form.Item>
              <Form.Item name="platform_version" label="系统版本">
                <Input placeholder="13.0" />
              </Form.Item>
              <Form.Item name="app_package" label="Android 包名">
                <Input placeholder="com.example.app" />
              </Form.Item>
              <Form.Item name="app_activity" label="Android Activity">
                <Input placeholder=".MainActivity" />
              </Form.Item>
              <Form.Item name="bundle_id" label="iOS Bundle ID">
                <Input placeholder="com.example.app" />
              </Form.Item>
            </Form>
          </TabPane>
        </Tabs>
      </Modal>
    </div>
  )
}

export default AppTestScripts
