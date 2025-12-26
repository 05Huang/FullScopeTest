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
  message,
  Popconfirm,
  Tooltip,
  Switch,
} from 'antd'
import {
  PlusOutlined,
  SearchOutlined,
  EditOutlined,
  DeleteOutlined,
  CopyOutlined,
  CheckCircleOutlined,
} from '@ant-design/icons'
import type { ColumnsType } from 'antd/es/table'
import { environmentService } from '@/services'

const { Title, Text } = Typography
const { TextArea } = Input

interface Environment {
  id: number
  name: string
  base_url: string
  description: string
  is_active: boolean
  variables?: Record<string, any>
  updated_at: string
}

const ApiTestEnvironments = () => {
  const [loading, setLoading] = useState(false)
  const [environments, setEnvironments] = useState<Environment[]>([])
  const [isModalOpen, setIsModalOpen] = useState(false)
  const [editingEnv, setEditingEnv] = useState<Environment | null>(null)
  const [searchText, setSearchText] = useState('')
  const [form] = Form.useForm()

  useEffect(() => {
    loadData()
  }, [])

  const loadData = async () => {
    setLoading(true)
    try {
      const res = await environmentService.getEnvironments()
      if (res.code === 200) {
        setEnvironments(res.data || [])
      }
    } catch (error) {
      message.error('加载环境列表失败')
    } finally {
      setLoading(false)
    }
  }

  const handleCreate = async (values: any) => {
    try {
      // 处理 variables 字段：将字符串转换为对象
      const processedValues = { ...values }
      if (typeof processedValues.variables === 'string') {
        if (processedValues.variables.trim()) {
          try {
            processedValues.variables = JSON.parse(processedValues.variables)
          } catch {
            return message.error('环境变量 JSON 格式错误')
          }
        } else {
          processedValues.variables = {}
        }
      }

      // 转换字段名：is_active -> is_default
      if (processedValues.is_active !== undefined) {
        processedValues.is_default = processedValues.is_active
        delete processedValues.is_active
      }

      const res = await environmentService.createEnvironment(processedValues)
      if (res.code === 200 || res.code === 201) {
        message.success('创建成功')
        setIsModalOpen(false)
        form.resetFields()
        loadData()
      } else {
        message.error(res.message || '创建失败')
      }
    } catch (error) {
      message.error('创建失败')
    }
  }

  const handleUpdate = async (id: number, values: any) => {
    try {
      // 处理 variables 字段：将字符串转换为对象
      const processedValues = { ...values }
      if (typeof processedValues.variables === 'string') {
        if (processedValues.variables.trim()) {
          try {
            processedValues.variables = JSON.parse(processedValues.variables)
          } catch {
            return message.error('环境变量 JSON 格式错误')
          }
        } else {
          processedValues.variables = {}
        }
      }

      // 转换字段名：is_active -> is_default
      if (processedValues.is_active !== undefined) {
        processedValues.is_default = processedValues.is_active
        delete processedValues.is_active
      }

      const res = await environmentService.updateEnvironment(id, processedValues)
      if (res.code === 200) {
        message.success('更新成功')
        setIsModalOpen(false)
        setEditingEnv(null)
        form.resetFields()
        loadData()
      } else {
        message.error(res.message || '更新失败')
      }
    } catch (error) {
      message.error('更新失败')
    }
  }

  const handleDelete = async (id: number) => {
    try {
      const res = await environmentService.deleteEnvironment(id)
      if (res.code === 200) {
        message.success('删除成功')
        loadData()
      } else {
        message.error(res.message || '删除失败')
      }
    } catch (error) {
      message.error('删除失败')
    }
  }

  // 设为默认环境
  const handleSetDefault = async (id: number) => {
    try {
      const res = await environmentService.updateEnvironment(id, { is_default: true })
      if (res.code === 200) {
        message.success('已设为默认环境')
        loadData()
      }
    } catch (error) {
      message.error('设置失败')
    }
  }

  // 表格列配置
  const columns: ColumnsType<Environment> = [
    {
      title: '环境名称',
      dataIndex: 'name',
      key: 'name',
      render: (text, record) => (
        <Space>
          <Text strong>{text}</Text>
          {record.is_active && <Tag color="blue">默认</Tag>}
        </Space>
      ),
    },
    {
      title: 'Base URL',
      dataIndex: 'base_url',
      key: 'base_url',
      render: (url) => <Text code>{url || '-'}</Text>,
    },
    {
      title: '描述',
      dataIndex: 'description',
      key: 'description',
      render: (desc) => <Text type="secondary">{desc || '-'}</Text>,
    },
    {
      title: '变量数',
      key: 'variables',
      width: 100,
      render: (_, record) => {
        const count = typeof record.variables === 'object' && record.variables !== null && !Array.isArray(record.variables)
          ? Object.keys(record.variables).length
          : 0
        return <Tag>{count} 个</Tag>
      },
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
      width: 200,
      render: (_, record) => (
        <Space>
          {!record.is_active && (
            <Tooltip title="设为默认">
              <Button
                type="text"
                size="small"
                icon={<CheckCircleOutlined style={{ color: '#52c41a' }} />}
                onClick={() => handleSetDefault(record.id)}
              />
            </Tooltip>
          )}
          <Tooltip title="编辑">
            <Button
              type="text"
              size="small"
              icon={<EditOutlined />}
              onClick={() => {
                setEditingEnv(record)
                form.setFieldsValue({
                  ...record,
                  is_active: record.is_active
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
              onClick={() => {
                const copyValues = { ...record, name: `${record.name} (副本)`, is_active: false }
                delete (copyValues as any).id
                handleCreate(copyValues)
              }}
            />
          </Tooltip>
          <Popconfirm
            title="确定删除此环境吗？"
            onConfirm={() => handleDelete(record.id)}
            disabled={record.is_active}
          >
            <Tooltip title={record.is_active ? '默认环境不可删除' : '删除'}>
              <Button
                type="text"
                size="small"
                danger
                icon={<DeleteOutlined />}
                disabled={record.is_active}
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
          环境配置
        </Title>
        <Space>
          <Input
            placeholder="搜索环境..."
            prefix={<SearchOutlined />}
            style={{ width: 250 }}
            allowClear
            value={searchText}
            onChange={(e) => setSearchText(e.target.value)}
          />
          <Button
            type="primary"
            icon={<PlusOutlined />}
            onClick={() => {
              setEditingEnv(null)
              form.resetFields()
              setIsModalOpen(true)
            }}
          >
            新建环境
          </Button>
        </Space>
      </div>

      <Card>
        <Table
          columns={columns}
          dataSource={environments.filter(env => 
            !searchText || 
            env.name.toLowerCase().includes(searchText.toLowerCase()) ||
            env.base_url?.toLowerCase().includes(searchText.toLowerCase()) ||
            env.description?.toLowerCase().includes(searchText.toLowerCase())
          )}
          rowKey="id"
          loading={loading}
          pagination={{
            total: environments.length,
            showTotal: (total) => `共 ${total} 条`,
          }}
        />
      </Card>

      {/* 新建/编辑环境弹窗 */}
      <Modal
        title={editingEnv ? '编辑环境' : '新建环境'}
        open={isModalOpen}
        onCancel={() => {
          setIsModalOpen(false)
          setEditingEnv(null)
          form.resetFields()
        }}
        onOk={() => {
          form.validateFields().then((values) => {
            if (editingEnv) {
              handleUpdate(editingEnv.id, values)
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
            label="环境名称"
            rules={[{ required: true, message: '请输入环境名称' }]}
          >
            <Input placeholder="请输入环境名称" />
          </Form.Item>
          <Form.Item
            name="base_url"
            label="Base URL"
            rules={[
              { required: true, message: '请输入 Base URL' },
              { type: 'url', message: '请输入有效的 URL' },
            ]}
          >
            <Input placeholder="https://api.example.com" />
          </Form.Item>
          <Form.Item name="description" label="描述">
            <TextArea rows={3} placeholder="请输入环境描述" />
          </Form.Item>
          <Form.Item
            name="variables"
            label="环境变量"
            tooltip='使用 JSON 格式定义变量，例如: {"bearer": "token123", "userId": "456"}'
            validateTrigger={['onChange', 'onBlur']}
            rules={[
              {
                validator: async (_, value) => {
                  // 只在提交时验证，不在输入时验证
                  if (value && typeof value === 'string' && value.trim()) {
                    try {
                      const parsed = JSON.parse(value);
                      if (!Array.isArray(parsed) && typeof parsed === 'object' && parsed !== null) {
                        return Promise.resolve();
                      }
                      return Promise.reject(new Error('variables 必须是对象类型'));
                    } catch {
                      return Promise.reject(new Error('必须是有效的 JSON 格式'));
                    }
                  }
                  return Promise.resolve();
                },
              },
            ]}
            normalize={(value) => {
              // 从后端获取的数据（对象）转换为字符串
              if (typeof value === 'object' && value !== null && !Array.isArray(value)) {
                if (Object.keys(value).length === 0) {
                  return ''; // 空对象显示为空字符串
                }
                return JSON.stringify(value, null, 2);
              }
              return value || '';
            }}
            getValueProps={(value) => {
              // 直接返回字符串值，不做额外处理
              return { value: value || '' };
            }}
          >
            <TextArea
              rows={6}
              placeholder={'{\n  "bearer": "your_token_here",\n  "userId": "123",\n  "apiKey": "abc456"\n}'}
            />
          </Form.Item>
          <Form.Item name="is_active" label="设为默认" valuePropName="checked">
            <Switch />
          </Form.Item>
        </Form>
      </Modal>
    </div>
  )
}

export default ApiTestEnvironments
