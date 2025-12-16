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
  ReloadOutlined,
} from '@ant-design/icons'
import type { ColumnsType } from 'antd/es/table'
import type { MenuProps } from 'antd'
import { apiTestService } from '@/services'

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
  const [loading, setLoading] = useState(false)
  const [cases, setCases] = useState<TestCase[]>([])
  const [collections, setCollections] = useState<Collection[]>([])
  const [selectedRowKeys, setSelectedRowKeys] = useState<React.Key[]>([])
  const [isModalOpen, setIsModalOpen] = useState(false)
  const [editingCase, setEditingCase] = useState<TestCase | null>(null)
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
      const collectionsRes = await apiTestService.getCollections()
      if (collectionsRes.code === 200) {
        setCollections(collectionsRes.data || [])
      }
    } catch (error) {
      message.error('加载数据失败')
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
        message.success('创建成功')
        setIsModalOpen(false)
        setEditingCase(null)
        form.resetFields()
        loadData()
      }
    } catch (error) {
      message.error('创建失败')
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
        message.success('更新成功')
        setIsModalOpen(false)
        setEditingCase(null)
        form.resetFields()
        loadData()
      }
    } catch (error) {
      message.error('更新失败')
    }
  }

  const handleCopy = async (record: TestCase) => {
    try {
      const res = await apiTestService.createCase({
        name: `${record.name} (副本)`,
        method: record.method,
        url: record.url || '',
        collection_id: record.collection_id,
        description: record.description,
        headers: record.headers,
        params: record.params,
        body: record.body,
      })
      if (res.code === 200 || res.code === 201) {
        message.success('复制成功')
        loadData()
      }
    } catch (error) {
      message.error('复制失败')
    }
  }

  const handleDelete = async (id: number) => {
    try {
      const res = await apiTestService.deleteCase(id)
      if (res.code === 200) {
        message.success('删除成功')
        loadData()
      }
    } catch (error) {
      message.error('删除失败')
    }
  }

  const handleBatchDelete = async () => {
    if (selectedRowKeys.length === 0) return
    
    try {
      for (const id of selectedRowKeys) {
        await apiTestService.deleteCase(id as number)
      }
      message.success('批量删除成功')
      setSelectedRowKeys([])
      loadData()
    } catch (error) {
      message.error('删除失败')
    }
  }

  const handleRun = async (id: number) => {
    try {
      const res = await apiTestService.runCase(id)
      if (res.code === 200) {
        message.success('执行完成')
        loadData()
      }
    } catch (error) {
      message.error('执行失败')
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
      title: '用例名称',
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
      title: '方法',
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
      title: '请求路径',
      dataIndex: 'url',
      key: 'url',
      render: (url) => <Text code>{url || '-'}</Text>,
    },
    {
      title: '所属集合',
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
      title: '更新时间',
      dataIndex: 'updated_at',
      key: 'updated_at',
      width: 160,
      render: (time) => time ? new Date(time).toLocaleString() : '-'
    },
    {
      title: '操作',
      key: 'action',
      width: 180,
      render: (_, record) => (
        <Space>
          <Tooltip title="运行">
            <Button
              type="text"
              size="small"
              icon={<PlayCircleOutlined style={{ color: '#52c41a' }} />}
              onClick={() => handleRun(record.id)}
            />
          </Tooltip>
          <Tooltip title="编辑">
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
          <Tooltip title="复制">
            <Button
              type="text"
              size="small"
              icon={<CopyOutlined />}
              onClick={() => handleCopy(record)}
            />
          </Tooltip>
          <Popconfirm
            title="确定删除此用例吗？"
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
    { key: 'export', icon: <ExportOutlined />, label: '导出用例' },
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
          用例管理
        </Title>
        <Space>
          <Input
            placeholder="搜索用例..."
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
                message.info('批量执行功能开发中')
              } else if (key === 'export') {
                message.info('导出功能开发中')
              }
            }
          }} disabled={selectedRowKeys.length === 0}>
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
          dataSource={cases.filter(c => 
            !searchText || 
            c.name.toLowerCase().includes(searchText.toLowerCase()) ||
            c.url?.toLowerCase().includes(searchText.toLowerCase())
          )}
          rowKey="id"
          loading={loading}
          pagination={{
            total: cases.length,
            showTotal: (total) => `共 ${total} 条`,
            showSizeChanger: true,
            showQuickJumper: true,
          }}
        />
      </Card>

      {/* 新建/编辑用例弹窗 */}
      <Modal
        title={editingCase ? "编辑用例" : "新建用例"}
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
            label="用例名称"
            rules={[{ required: true, message: '请输入用例名称' }]}
          >
            <Input placeholder="请输入用例名称" />
          </Form.Item>
          <Form.Item
            name="collection_id"
            label="所属集合"
          >
            <Select
              placeholder="请选择所属集合"
              allowClear
              options={collections.map(c => ({
                value: c.id,
                label: c.name
              }))}
            />
          </Form.Item>
          <Form.Item name="method" label="请求方法" initialValue="GET">
            <Select
              options={['GET', 'POST', 'PUT', 'DELETE', 'PATCH'].map((m) => ({
                value: m,
                label: m,
              }))}
            />
          </Form.Item>
          <Form.Item name="url" label="请求路径">
            <Input placeholder="请输入请求路径" />
          </Form.Item>
          <Form.Item name="description" label="描述">
            <Input.TextArea placeholder="请输入用例描述" rows={3} />
          </Form.Item>
        </Form>
      </Modal>
    </div>
  )
}

export default ApiTestCollections
