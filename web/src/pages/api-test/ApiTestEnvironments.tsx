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
import { useTranslation } from 'react-i18next'
import { useProjectStore } from '@/stores/projectStore'

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
  const { t } = useTranslation();
  const { currentProjectId } = useProjectStore()
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
      const res = await environmentService.getEnvironments(currentProjectId)
      if (res.code === 200) {
        setEnvironments(res.data || [])
      }
    } catch (error) {
      message.error(t('apiTest.environments.loadFailed'))
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
            return message.error(t('apiTest.environments.jsonError'))
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
        message.success(t('apiTest.environments.createSuccess'))
        setIsModalOpen(false)
        form.resetFields()
        loadData()
      } else {
        message.error(res.message || t('apiTest.environments.createFailed'))
      }
    } catch (error) {
      message.error(t('apiTest.environments.createFailed'))
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
            return message.error(t('apiTest.environments.jsonError'))
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
        message.success(t('apiTest.environments.updateSuccess'))
        setIsModalOpen(false)
        setEditingEnv(null)
        form.resetFields()
        loadData()
      } else {
        message.error(res.message || t('apiTest.environments.updateFailed'))
      }
    } catch (error) {
      message.error(t('apiTest.environments.updateFailed'))
    }
  }

  const handleDelete = async (id: number) => {
    try {
      const res = await environmentService.deleteEnvironment(id)
      if (res.code === 200) {
        message.success(t('apiTest.environments.deleteSuccess'))
        loadData()
      } else {
        message.error(res.message || t('apiTest.environments.deleteFailed'))
      }
    } catch (error) {
      message.error(t('apiTest.environments.deleteFailed'))
    }
  }

  // 设为默认环境
  const handleSetDefault = async (id: number) => {
    try {
      const res = await environmentService.updateEnvironment(id, { is_default: true })
      if (res.code === 200) {
        message.success(t('apiTest.environments.setDefaultSuccess'))
        loadData()
      }
    } catch (error) {
      message.error(t('apiTest.environments.setFailed'))
    }
  }

  // 表格列配置
  const columns: ColumnsType<Environment> = [
    {
      title: t('apiTest.environments.envName'),
      dataIndex: 'name',
      key: 'name',
      render: (text, record) => (
        <Space>
          <Text strong>{text}</Text>
          {record.is_active && <Tag color="blue">{t('apiTest.environments.defaultTag')}</Tag>}
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
      title: t('apiTest.environments.envDescription'),
      dataIndex: 'description',
      key: 'description',
      render: (desc) => <Text type="secondary">{desc || '-'}</Text>,
    },
    {
      title: t('apiTest.environments.envVariables'),
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
      title: t('common.updatedAt'),
      dataIndex: 'updated_at',
      key: 'updated_at',
      width: 160,
      render: (time) => time ? new Date(time).toLocaleString() : '-'
    },
    {
      title: t('common.actions'),
      key: 'action',
      width: 200,
      render: (_, record) => (
        <Space>
          {!record.is_active && (
            <Tooltip title={t('apiTest.environments.setDefault')}>
              <Button
                type="text"
                size="small"
                icon={<CheckCircleOutlined style={{ color: '#52c41a' }} />}
                onClick={() => handleSetDefault(record.id)}
              />
            </Tooltip>
          )}
          <Tooltip title={t('common.edit')}>
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
          <Tooltip title={t('common.copy')}>
            <Button
              type="text"
              size="small"
              icon={<CopyOutlined />}
              onClick={() => {
                const copyValues = { ...record, name: `${record.name}${t('apiTest.environments.copyName')}`, is_active: false }
                delete (copyValues as any).id
                handleCreate(copyValues)
              }}
            />
          </Tooltip>
          <Popconfirm
            title={t('apiTest.environments.deleteConfirm')}
            onConfirm={() => handleDelete(record.id)}
            disabled={record.is_active}
          >
            <Tooltip title={record.is_active ? t('apiTest.environments.defaultNoDelete') : t('common.delete')}>
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
    <div className="fst-page">
      <div className="fst-page-header fst-animate-in">
        <h1 className="fst-page-title">{t("apiTest.environments.title")}</h1>
      </div>
      <div style={{ display: 'flex', gap: 8, marginBottom: 16 }}>
        <Input
          placeholder={t("apiTest.environments.searchEnv")}
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
        </div>

      <div className="fst-ios-card fst-animate-in fst-animate-in-1">
        <div className="fst-table-wrap">
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
            showTotal: (total) => `${t('common.total')} ${total}`,
          }}
        />
        </div>
      </div>

      {/* 新建/编辑环境弹窗 */}
      <Modal
        title={editingEnv ? t('apiTest.environments.editEnv') : t('apiTest.environments.newEnv')}
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
            label={t('apiTest.environments.envName')}
            rules={[{ required: true, message: t('apiTest.environments.envNameRequired') }]}
          >
            <Input placeholder={t("apiTest.environments.envNamePlaceholder")} />
          </Form.Item>
          <Form.Item
            name="base_url"
            label="Base URL"
            rules={[
              { required: true, message: t('apiTest.environments.envUrlRequired') },
              { type: 'url', message: t('apiTest.environments.envUrlInvalid') },
            ]}
          >
            <Input placeholder="https://api.example.com" />
          </Form.Item>
          <Form.Item name="description" label={t('apiTest.environments.envDescription')}>
            <TextArea rows={3} placeholder={t("apiTest.environments.envDescriptionPlaceholder")} />
          </Form.Item>
          <Form.Item
            name="variables"
            label={t('apiTest.environments.envVariables')}
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
              if (typeof value === 'object' && value !== null && !Array.isArray(value)) {
                if (Object.keys(value).length === 0) {
                  return { value: '' }
                }
                return { value: JSON.stringify(value, null, 2) }
              }
              return { value: value || '' }
            }}
          >
            <TextArea
              rows={6}
              placeholder={'{\n  "bearer": "your_token_here",\n  "userId": "123",\n  "apiKey": "abc456"\n}'}
            />
          </Form.Item>
          <Form.Item name="is_active" label={t('apiTest.environments.setAsDefault')} valuePropName="checked">
            <Switch />
          </Form.Item>
        </Form>
      </Modal>
    </div>
  )
}

export default ApiTestEnvironments
