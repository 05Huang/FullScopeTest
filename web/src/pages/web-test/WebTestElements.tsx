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
} from 'antd'
import {
  PlusOutlined,
  SearchOutlined,
  EditOutlined,
  DeleteOutlined,
  CopyOutlined,
  AimOutlined,
  ReloadOutlined,
} from '@ant-design/icons'
import type { ColumnsType } from 'antd/es/table'

const { Title, Text } = Typography

interface Element {
  id: number
  name: string
  description: string
  locator_type: 'css' | 'xpath' | 'id' | 'name' | 'text'
  locator_value: string
  page_url?: string
  category?: string
  created_at: string
  updated_at: string
}

const locatorTypeConfig: Record<string, { color: string; label: string }> = {
  css: { color: 'blue', label: 'CSS' },
  xpath: { color: 'purple', label: 'XPath' },
  id: { color: 'green', label: 'ID' },
  name: { color: 'orange', label: 'Name' },
  text: { color: 'cyan', label: 'Text' },
}

const WebTestElements = () => {
  const [loading, setLoading] = useState(false)
  const [elements, setElements] = useState<Element[]>([])
  const [isModalOpen, setIsModalOpen] = useState(false)
  const [editingElement, setEditingElement] = useState<Element | null>(null)
  const [searchText, setSearchText] = useState('')
  const [form] = Form.useForm()

  // 模拟数据
  useEffect(() => {
    loadElements()
  }, [])

  const loadElements = () => {
    setLoading(true)
    // 模拟加载数据
    setTimeout(() => {
      setElements([
        {
          id: 1,
          name: '登录按钮',
          description: '登录页面的登录按钮',
          locator_type: 'css',
          locator_value: 'button[type="submit"]',
          page_url: '/login',
          category: '登录模块',
          created_at: '2025-12-24 10:00:00',
          updated_at: '2025-12-24 10:00:00',
        },
        {
          id: 2,
          name: '用户名输入框',
          description: '登录页面的用户名输入框',
          locator_type: 'id',
          locator_value: 'username',
          page_url: '/login',
          category: '登录模块',
          created_at: '2025-12-24 10:00:00',
          updated_at: '2025-12-24 10:00:00',
        },
        {
          id: 3,
          name: '搜索框',
          description: '页面顶部搜索框',
          locator_type: 'xpath',
          locator_value: '//input[@placeholder="搜索"]',
          page_url: '/home',
          category: '通用',
          created_at: '2025-12-24 10:00:00',
          updated_at: '2025-12-24 10:00:00',
        },
      ])
      setLoading(false)
    }, 500)
  }

  const handleCreate = (values: any) => {
    const newElement: Element = {
      id: Date.now(),
      ...values,
      created_at: new Date().toLocaleString(),
      updated_at: new Date().toLocaleString(),
    }
    setElements([newElement, ...elements])
    message.success('创建成功')
    setIsModalOpen(false)
    form.resetFields()
  }

  const handleUpdate = (values: any) => {
    if (!editingElement) return
    
    setElements(elements.map(el => 
      el.id === editingElement.id
        ? { ...el, ...values, updated_at: new Date().toLocaleString() }
        : el
    ))
    message.success('更新成功')
    setIsModalOpen(false)
    setEditingElement(null)
    form.resetFields()
  }

  const handleDelete = (id: number) => {
    setElements(elements.filter(el => el.id !== id))
    message.success('删除成功')
  }

  const handleCopy = (element: Element) => {
    navigator.clipboard.writeText(element.locator_value)
    message.success('已复制到剪贴板')
  }

  const openEditModal = (element: Element) => {
    setEditingElement(element)
    form.setFieldsValue(element)
    setIsModalOpen(true)
  }

  // 过滤搜索
  const filteredElements = elements.filter(el =>
    el.name.toLowerCase().includes(searchText.toLowerCase()) ||
    el.locator_value.toLowerCase().includes(searchText.toLowerCase()) ||
    el.description?.toLowerCase().includes(searchText.toLowerCase())
  )

  const columns: ColumnsType<Element> = [
    {
      title: '元素名称',
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
      title: '定位类型',
      dataIndex: 'locator_type',
      key: 'locator_type',
      width: 100,
      render: (type) => (
        <Tag color={locatorTypeConfig[type]?.color}>
          {locatorTypeConfig[type]?.label || type}
        </Tag>
      ),
    },
    {
      title: '定位表达式',
      dataIndex: 'locator_value',
      key: 'locator_value',
      render: (value) => (
        <Text code style={{ fontSize: 12 }}>
          {value}
        </Text>
      ),
    },
    {
      title: '所属页面',
      dataIndex: 'page_url',
      key: 'page_url',
      width: 120,
      render: (url) => url || '-',
    },
    {
      title: '分类',
      dataIndex: 'category',
      key: 'category',
      width: 100,
      render: (cat) => cat ? <Tag>{cat}</Tag> : '-',
    },
    {
      title: '更新时间',
      dataIndex: 'updated_at',
      key: 'updated_at',
      width: 160,
    },
    {
      title: '操作',
      key: 'action',
      width: 150,
      render: (_, record) => (
        <Space>
          <Tooltip title="复制表达式">
            <Button
              type="text"
              size="small"
              icon={<CopyOutlined />}
              onClick={() => handleCopy(record)}
            />
          </Tooltip>
          <Tooltip title="编辑">
            <Button
              type="text"
              size="small"
              icon={<EditOutlined />}
              onClick={() => openEditModal(record)}
            />
          </Tooltip>
          <Popconfirm
            title="确定删除此元素吗？"
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
          <AimOutlined style={{ marginRight: 8 }} />
          元素库
        </Title>
        <Space>
          <Input
            placeholder="搜索元素..."
            prefix={<SearchOutlined />}
            style={{ width: 250 }}
            allowClear
            value={searchText}
            onChange={(e) => setSearchText(e.target.value)}
          />
          <Button
            icon={<ReloadOutlined />}
            onClick={loadElements}
            loading={loading}
          >
            刷新
          </Button>
          <Button
            type="primary"
            icon={<PlusOutlined />}
            onClick={() => {
              setEditingElement(null)
              form.resetFields()
              setIsModalOpen(true)
            }}
          >
            添加元素
          </Button>
        </Space>
      </div>

      <Card>
        <Table
          columns={columns}
          dataSource={filteredElements}
          rowKey="id"
          loading={loading}
          pagination={{
            total: filteredElements.length,
            showTotal: (total) => `共 ${total} 个元素`,
            showSizeChanger: true,
            showQuickJumper: true,
          }}
        />
      </Card>

      {/* 新建/编辑元素弹窗 */}
      <Modal
        title={editingElement ? '编辑元素' : '添加元素'}
        open={isModalOpen}
        onCancel={() => {
          setIsModalOpen(false)
          setEditingElement(null)
          form.resetFields()
        }}
        onOk={() => {
          form.validateFields().then((values) => {
            if (editingElement) {
              handleUpdate(values)
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
            label="元素名称"
            rules={[{ required: true, message: '请输入元素名称' }]}
          >
            <Input placeholder="请输入元素名称" />
          </Form.Item>
          <Form.Item name="description" label="描述">
            <Input.TextArea rows={2} placeholder="请输入元素描述" />
          </Form.Item>
          <Form.Item
            name="locator_type"
            label="定位类型"
            initialValue="css"
            rules={[{ required: true }]}
          >
            <Select
              options={[
                { value: 'css', label: 'CSS 选择器' },
                { value: 'xpath', label: 'XPath' },
                { value: 'id', label: 'ID' },
                { value: 'name', label: 'Name' },
                { value: 'text', label: 'Text' },
              ]}
            />
          </Form.Item>
          <Form.Item
            name="locator_value"
            label="定位表达式"
            rules={[{ required: true, message: '请输入定位表达式' }]}
          >
            <Input.TextArea rows={2} placeholder="请输入定位表达式" />
          </Form.Item>
          <Form.Item name="page_url" label="所属页面">
            <Input placeholder="页面 URL 路径，如 /login" />
          </Form.Item>
          <Form.Item name="category" label="分类">
            <Input placeholder="元素分类，如 登录模块" />
          </Form.Item>
        </Form>
      </Modal>
    </div>
  )
}

export default WebTestElements
