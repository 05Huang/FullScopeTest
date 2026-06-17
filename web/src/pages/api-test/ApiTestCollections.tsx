import { useState, useEffect } from 'react'
import {
  Card,
  Table,
  Button,
  Space,
  Input,
  Tag,
  Typography,
  Dropdown,
  Modal,
  Form,
  Select,
  message,
  Popconfirm,
  Tooltip,
  type MenuProps,
} from 'antd'
import {
  PlusOutlined,
  SearchOutlined,
  PlayCircleOutlined,
  EditOutlined,
  DeleteOutlined,
  MoreOutlined,
  FolderOutlined,
  FileOutlined,
  CopyOutlined,
  ExportOutlined,
} from '@ant-design/icons'
import type { ColumnsType } from 'antd/es/table'
import { apiTestService } from '@/services'
import { useTranslation } from 'react-i18next'
import { useProjectStore } from '@/stores/projectStore'

const { Title, Text } = Typography

interface TestCase {
  id: number
  name: string
  method: string
  url: string
  collection_id?: number
  collection_name?: string
  description?: string
  headers?: any
  params?: any
  body?: any
  assertions?: any[]
  updated_at: string
}

interface Collection {
  id: number
  name: string
  description?: string
}

const methodColors: Record<string, string> = {
  GET: 'green',
  POST: 'blue',
  PUT: 'orange',
  DELETE: 'red',
  PATCH: 'purple',
}

const ApiTestCollections = () => {
  const { t } = useTranslation();
  const { currentProjectId } = useProjectStore()
  const [loading, setLoading] = useState(false)
  const [cases, setCases] = useState<TestCase[]>([])
  const [collections, setCollections] = useState<Collection[]>([])
  const [selectedRowKeys, setSelectedRowKeys] = useState<React.Key[]>([])
  const [isModalOpen, setIsModalOpen] = useState(false)
  const [editingCase, setEditingCase] = useState<TestCase | null>(null)
  const [searchText, setSearchText] = useState('')
  const [form] = Form.useForm()

  useEffect(() => {
    loadData()
  }, [])

  const loadData = async () => {
    setLoading(true)
    try {
      // 加载用例列表
      const casesRes = await apiTestService.getCases({})
      if (casesRes.code === 200) {
        setCases(casesRes.data || [])
      }

      // 加载集合列表
      const collectionsRes = await apiTestService.getCollections(currentProjectId)
      if (collectionsRes.code === 200) {
        setCollections(collectionsRes.data || [])
      }
    } catch (error) {
      message.error(t('apiTest.loadFailed'))
    } finally {
      setLoading(false)
    }
  }

  const handleCreate = async (values: any) => {
    try {
      const res = await apiTestService.createCase({
        name: values.name,
        method: values.method,
        url: values.url || '',
        collection_id: values.collection_id,
        description: values.description,
      })
      if (res.code === 200 || res.code === 201) {
        message.success(t('common.success'))
        setIsModalOpen(false)
        setEditingCase(null)
        form.resetFields()
        loadData()
      }
    } catch (error) {
      message.error(t('common.failed'))
    }
  }

  const handleUpdate = async (id: number, values: any) => {
    try {
      const res = await apiTestService.updateCase(id, {
        name: values.name,
        method: values.method,
        url: values.url || '',
        collection_id: values.collection_id,
        description: values.description,
      })
      if (res.code === 200) {
        message.success(t('common.success'))
        setIsModalOpen(false)
        setEditingCase(null)
        form.resetFields()
        loadData()
      }
    } catch (error) {
      message.error(t('common.failed'))
    }
  }

  const handleCopy = async (record: TestCase) => {
    try {
      const res = await apiTestService.createCase({
        name: `${record.name}${t('apiTest.copyName')}`,
        method: record.method,
        url: record.url || '',
        collection_id: record.collection_id,
        description: record.description,
        headers: record.headers,
        params: record.params,
        body: record.body,
      })
      if (res.code === 200 || res.code === 201) {
        message.success(t('common.success'))
        loadData()
      }
    } catch (error) {
      message.error(t('common.failed'))
    }
  }

  const handleDelete = async (id: number) => {
    try {
      const res = await apiTestService.deleteCase(id)
      if (res.code === 200) {
        message.success(t('common.success'))
        loadData()
      }
    } catch (error) {
      message.error(t('common.failed'))
    }
  }

  const handleBatchDelete = async () => {
    if (selectedRowKeys.length === 0) return

    try {
      for (const id of selectedRowKeys) {
        await apiTestService.deleteCase(id as number)
      }
      message.success(t('common.success'))
      setSelectedRowKeys([])
      loadData()
    } catch (error) {
      message.error(t('common.failed'))
    }
  }

  // 批量执行用例
  const handleBatchRun = async () => {
    if (selectedRowKeys.length === 0) return

    const total = selectedRowKeys.length
    let successCount = 0
    let failCount = 0

    message.loading(`正在执行 ${total} 个用例...`)

    for (const id of selectedRowKeys) {
      try {
        const res = await apiTestService.runCase(id as number)
        if (res.code === 200) {
          successCount++
        } else {
          failCount++
        }
      } catch {
        failCount++
      }
    }

    message.destroy()
    if (failCount === 0) {
      message.success(`批量执行完成，${successCount} 个用例全部成功`)
    } else {
      message.warning(`批量执行完成，成功 ${successCount} 个，失败 ${failCount} 个`)
    }
    loadData()
  }

  // 导出用例
  const handleExport = () => {
    if (selectedRowKeys.length === 0) return

    const selectedCases = cases.filter(c => selectedRowKeys.includes(c.id))
    const exportData = {
      version: '1.0',
      export_time: new Date().toISOString(),
      cases: selectedCases.map(c => ({
        name: c.name,
        method: c.method,
        url: c.url,
        description: c.description,
        headers: c.headers,
        params: c.params,
        body: c.body,
        assertions: c.assertions,
        collection_id: c.collection_id,
      }))
    }

    const blob = new Blob([JSON.stringify(exportData, null, 2)], { type: 'application/json' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `api-test-cases-${new Date().toISOString().slice(0, 10)}.json`
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    URL.revokeObjectURL(url)

    message.success(t('apiTest.exportedCount', {count: selectedCases.length}))
  }

  const handleRun = async (id: number) => {
    try {
      const res = await apiTestService.runCase(id)
      if (res.code === 200) {
        message.success(t('common.success'))
        loadData()
      }
    } catch (error) {
      message.error(t('common.failed'))
    }
  }

  // 获取集合名称
  const getCollectionName = (collectionId?: number) => {
    if (!collectionId) return '-'
    const collection = collections.find(c => c.id === collectionId)
    return collection?.name || '-'
  }

  // 表格列配置
  const columns: ColumnsType<TestCase> = [
    {
      title: t('apiTest.caseName'),
      dataIndex: 'name',
      key: 'name',
      render: (text) => (
        <Space>
          <FileOutlined style={{ color: '#1890ff' }} />
          <Text strong>{text}</Text>
        </Space>
      ),
    },
    {
      title: t('apiTest.requestMethod'),
      dataIndex: 'method',
      key: 'method',
      width: 100,
      render: (method) => (
        <Tag color={methodColors[method]} style={{ fontWeight: 600 }}>
          {method}
        </Tag>
      ),
    },
    {
      title: t('apiTest.requestPath'),
      dataIndex: 'url',
      key: 'url',
      render: (url) => <Text code>{url || '-'}</Text>,
    },
    {
      title: t('apiTest.collection'),
      dataIndex: 'collection_id',
      key: 'collection_id',
      render: (collectionId) => (
        <Space>
          <FolderOutlined />
          {getCollectionName(collectionId)}
        </Space>
      ),
    },
    {
      title: t('common.updatedAt'),
      dataIndex: 'updated_at',
      key: 'updated_at',
      width: 160,
      render: (time) => time ? new Date(time).toLocaleString() : '-'
    },
    {
      title: t('common.actions'),
      key: 'action',
      width: 180,
      render: (_, record) => (
        <Space>
          <Tooltip title={t("apiTest.runScript")}>
            <Button
              type="text"
              size="small"
              icon={<PlayCircleOutlined style={{ color: '#52c41a' }} />}
              onClick={() => handleRun(record.id)}
            />
          </Tooltip>
          <Tooltip title={t("common.edit")}>
            <Button
              type="text"
              size="small"
              icon={<EditOutlined />}
              onClick={() => {
                setEditingCase(record)
                form.setFieldsValue({
                  name: record.name,
                  method: record.method,
                  url: record.url,
                  collection_id: record.collection_id,
                  description: record.description,
                })
                setIsModalOpen(true)
              }}
            />
          </Tooltip>
          <Tooltip title={t("common.copy")}>
            <Button
              type="text"
              size="small"
              icon={<CopyOutlined />}
              onClick={() => handleCopy(record)}
            />
          </Tooltip>
          <Popconfirm
            title={t('apiTest.confirmDeleteCase')}
            onConfirm={() => handleDelete(record.id)}
          >
            <Tooltip title={t("common.delete")}>
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
    { key: 'run', icon: <PlayCircleOutlined />, label: t('apiTest.batchRun') },
    { key: 'export', icon: <ExportOutlined />, label: t('apiTest.exportCases') },
    { type: 'divider' },
    { key: 'delete', icon: <DeleteOutlined />, label: t('apiTest.batchDelete'), danger: true },
  ]

  return (
    <div className="fst-page">
      <div className="fst-page-header fst-animate-in">
        <h1 className="fst-page-title">{t("apiTest.casesManagement")}</h1>
      </div>
      <div style={{ display: 'flex', gap: 8, marginBottom: 16 }}>
        <Input
          placeholder={t("apiTest.searchCases")}
          prefix={<SearchOutlined />}
          style={{ width: 250 }}
          allowClear
          value={searchText}
          onChange={(e) => setSearchText(e.target.value)}
        />
        <Button type="primary" icon={<PlusOutlined />} onClick={() => {
          setEditingCase(null)
          form.resetFields()
          setIsModalOpen(true)
        }}>
          新建用例
        </Button>
        <Dropdown menu={{
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
          }} disabled={selectedRowKeys.length === 0}>
            <Button icon={<MoreOutlined />}>{t("common.more")}</Button>
          </Dropdown>
        </div>

      <div className="fst-ios-card fst-animate-in fst-animate-in-1">
        <div className="fst-table-wrap">
        <Table
          rowSelection={{
            selectedRowKeys,
            onChange: setSelectedRowKeys,
          }}
          columns={columns}
          dataSource={cases.filter(c =>
            !searchText ||
            c.name.toLowerCase().includes(searchText.toLowerCase()) ||
            c.url?.toLowerCase().includes(searchText.toLowerCase())
          )}
          rowKey="id"
          loading={loading}
          pagination={{
            total: cases.length,
            showTotal: (total) => `${t('common.total')} ${total}`,
            showSizeChanger: true,
            showQuickJumper: true,
          }}
        />
        </div>
      </div>

      {/* 新建/编辑用例弹窗 */}
      <Modal
        title={editingCase ? t('apiTest.editCase') : t('apiTest.newCase')}
        open={isModalOpen}
        onCancel={() => {
          setIsModalOpen(false)
          setEditingCase(null)
          form.resetFields()
        }}
        onOk={() => {
          form.validateFields().then((values) => {
            if (editingCase) {
              handleUpdate(editingCase.id, values)
            } else {
              handleCreate(values)
            }
          })
        }}
      >
        <Form form={form} layout="vertical">
          <Form.Item
            name="name"
            label={t("apiTest.caseName")}
            rules={[{ required: true, message: t('apiTest.caseRequired') }]}
          >
            <Input placeholder={t("apiTest.caseName")} />
          </Form.Item>
          <Form.Item
            name="collection_id"
            label={t("apiTest.collection")}
          >
            <Select
              placeholder={t("apiTest.collectionPlaceholder")}
              allowClear
              options={collections.map(c => ({
                value: c.id,
                label: c.name
              }))}
            />
          </Form.Item>
          <Form.Item name="method" label={t("apiTest.requestMethod")} initialValue="GET">
            <Select
              options={['GET', 'POST', 'PUT', 'DELETE', 'PATCH'].map((m) => ({
                value: m,
                label: m,
              }))}
            />
          </Form.Item>
          <Form.Item name="url" label={t("apiTest.requestPath")}>
            <Input placeholder={t("apiTest.pathPlaceholder")} />
          </Form.Item>
          <Form.Item name="description" label={t("common.description")}>
            <Input.TextArea placeholder={t("apiTest.descriptionPlaceholder")} rows={3} />
          </Form.Item>
        </Form>
      </Modal>
    </div>
  )
}

export default ApiTestCollections
