import { useState, useEffect, useRef } from 'react'
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
  Upload,
  Select,
} from 'antd'
import {
  PlusOutlined,
  SearchOutlined,
  EditOutlined,
  DeleteOutlined,
  CopyOutlined,
  CheckCircleOutlined,
  ExportOutlined,
  ImportOutlined,
} from '@ant-design/icons'
import type { ColumnsType } from 'antd/es/table'
import { environmentService } from '@/services'
import { useTranslation } from 'react-i18next'
import { useRole } from '@/hooks/useRole'
import { useProjectStore } from '@/stores/projectStore'

const { Title, Text } = Typography
const { TextArea } = Input

interface Environment {
  id: number
  name: string
  base_url: string
  description: string
  is_active: boolean
  is_default?: boolean
  variables?: Record<string, any>
  updated_at: string
}

const ApiTestEnvironments = () => {
  const { t } = useTranslation();
  const { isAdmin } = useRole()
  const { currentProjectId } = useProjectStore()
  const [loading, setLoading] = useState(false)
  const [environments, setEnvironments] = useState<Environment[]>([])
  const [isModalOpen, setIsModalOpen] = useState(false)
  const [editingEnv, setEditingEnv] = useState<Environment | null>(null)
  const [searchText, setSearchText] = useState('')
  const [form] = Form.useForm()

  // P31-3: 导入/导出状态
  const [importModalOpen, setImportModalOpen] = useState(false)
  const [importData, setImportData] = useState<any>(null)
  const [importing, setImporting] = useState(false)
  const [importMode, setImportMode] = useState<'merge' | 'overwrite'>('merge')
  const fileInputRef = useRef<HTMLInputElement>(null)

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

  // 设为默认环境（使用专用端点）
  const handleSetDefault = async (id: number) => {
    try {
      const res = await environmentService.setDefaultEnvironment(id)
      if (res.code === 200) {
        message.success(t('apiTest.environments.setDefaultSuccess'))
        loadData()
      }
    } catch (error) {
      message.error(t('apiTest.environments.setFailed'))
    }
  }

  // P48-6: 导出环境为 Docker Compose 格式
  const handleDockerExport = async (id: number) => {
    try {
      const res = await environmentService.exportDockerEnvironment(id)
      if (res.code === 200) {
        const content = typeof res.data === 'string' ? res.data : JSON.stringify(res.data, null, 2)
        const blob = new Blob([content], { type: 'text/yaml' })
        const url = URL.createObjectURL(blob)
        const link = document.createElement('a')
        link.href = url
        link.download = `docker-compose-env-${id}.yml`
        document.body.appendChild(link)
        link.click()
        document.body.removeChild(link)
        URL.revokeObjectURL(url)
        message.success(t('apiTest.environments.exportSuccess'))
      }
    } catch {
      message.error(t('apiTest.environments.exportFailed'))
    }
  }

  // P31-3: 导出环境变量
  const handleExport = async (id: number) => {
    try {
      const res = await environmentService.exportEnvironment(id)
      if (res.code === 200) {
        const blob = new Blob([JSON.stringify(res.data, null, 2)], { type: 'application/json' })
        const url = URL.createObjectURL(blob)
        const link = document.createElement('a')
        link.href = url
        link.download = `environment-${id}.json`
        document.body.appendChild(link)
        link.click()
        document.body.removeChild(link)
        URL.revokeObjectURL(url)
        message.success(t('apiTest.environments.exportSuccess'))
      }
    } catch {
      message.error(t('apiTest.environments.exportFailed'))
    }
  }

  // P31-3: 解析导入文件
  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (!file) return
    const reader = new FileReader()
    reader.onload = (event) => {
      try {
        const content = event.target?.result as string
        // 支持 JSON 和 .env 格式
        if (file.name.endsWith('.json')) {
          const parsed = JSON.parse(content)
          setImportData(parsed)
        } else if (file.name.endsWith('.env')) {
          // 解析 .env 格式: KEY=VALUE
          const variables: Record<string, string> = {}
          content.split('\n').forEach(line => {
            const trimmed = line.trim()
            if (trimmed && !trimmed.startsWith('#')) {
              const eqIndex = trimmed.indexOf('=')
              if (eqIndex > 0) {
                const key = trimmed.slice(0, eqIndex).trim()
                const value = trimmed.slice(eqIndex + 1).trim().replace(/^["']|["']$/g, '')
                variables[key] = value
              }
            }
          })
          setImportData({ name: file.name.replace('.env', ''), variables })
        } else {
          message.error(t('apiTest.environments.importFormatError'))
        }
      } catch {
        message.error(t('apiTest.environments.importParseError'))
      }
    }
    reader.readAsText(file)
    // 重置 input 以便重复选择同一文件
    e.target.value = ''
  }

  // P31-3: 执行导入
  const handleImportConfirm = async () => {
    if (!importData || !currentProjectId) return
    setImporting(true)
    try {
      const payload = {
        name: importData.name || 'Imported Environment',
        base_url: importData.base_url || '',
        description: importData.description || '',
        variables: importData.variables || {},
        is_default: false,
      }
      const res = await environmentService.importEnvironment(currentProjectId, payload)
      if (res.code === 200 || res.code === 201) {
        message.success(t('apiTest.environments.importSuccess'))
        setImportModalOpen(false)
        setImportData(null)
        loadData()
      } else {
        message.error(res.message || t('apiTest.environments.importFailed'))
      }
    } catch {
      message.error(t('apiTest.environments.importFailed'))
    } finally {
      setImporting(false)
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
          {(record.is_default || record.is_active) && <Tag color="blue">{t('apiTest.environments.defaultTag')}</Tag>}
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
          {!(record.is_default || record.is_active) && (
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
                  is_default: record.is_default || record.is_active
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
                const copyValues = { ...record, name: `${record.name}${t('apiTest.environments.copyName')}`, is_default: false }
                delete (copyValues as any).id
                handleCreate(copyValues)
              }}
            />
          </Tooltip>
          <Popconfirm
            title={t('apiTest.environments.deleteConfirm')}
            onConfirm={() => handleDelete(record.id)}
            disabled={record.is_default || record.is_active || !isAdmin}
          >
            <Tooltip title={(record.is_default || record.is_active) ? t('apiTest.environments.defaultNoDelete') : (!isAdmin ? (t('common.noPermission') || 'No Permission') : t('common.delete'))}>
              <Button
                type="text"
                size="small"
                danger
                icon={<DeleteOutlined />}
                disabled={record.is_default || record.is_active || !isAdmin}
              />
            </Tooltip>
          </Popconfirm>
          <Tooltip title={t('apiTest.environments.export')}>
            <Button
              type="text"
              size="small"
              icon={<ExportOutlined />}
              onClick={() => handleExport(record.id)}
            />
          </Tooltip>
          <Tooltip title="Docker Export">
            <Button
              type="text"
              size="small"
              icon={<ExportOutlined />}
              onClick={() => handleDockerExport(record.id)}
            />
          </Tooltip>
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
            icon={<ImportOutlined />}
            onClick={() => { setImportData(null); setImportModalOpen(true); }}
          >
            {t('apiTest.environments.import')}
          </Button>
          <Button
            type="primary"
            icon={<PlusOutlined />}
            onClick={() => {
              setEditingEnv(null)
              form.resetFields()
              setIsModalOpen(true)
            }}
          >
            {t('apiTest.environments.newEnv')}
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

      {/* P31-3: 导入环境变量弹窗 */}
      <Modal
        title={t('apiTest.environments.importTitle')}
        open={importModalOpen}
        onCancel={() => { setImportModalOpen(false); setImportData(null); }}
        onOk={handleImportConfirm}
        confirmLoading={importing}
        okText={t('common.confirm')}
        cancelText={t('common.cancel')}
        okButtonProps={{ disabled: !importData }}
      >
        <div style={{ padding: '8px 0' }}>
          <input
            ref={fileInputRef}
            type="file"
            accept=".json,.env"
            style={{ display: 'none' }}
            onChange={handleFileSelect}
          />
          <Button
            icon={<ImportOutlined />}
            onClick={() => fileInputRef.current?.click()}
            style={{ marginBottom: 16 }}
          >
            {t('apiTest.environments.selectFile')}
          </Button>
          <div style={{ fontSize: 12, color: 'var(--fst-on-surface-muted, #999)', marginBottom: 16 }}>
            {t('apiTest.environments.importFormats') || '支持 .json 和 .env 格式'}
          </div>
          {importData && (
            <div style={{ padding: 12, borderRadius: 8, background: 'var(--fst-surface-variant, #f5f5f5)', border: '1px solid var(--fst-outline-soft, #e8e8e8)' }}>
              <div style={{ fontWeight: 600, marginBottom: 8 }}>{t('apiTest.environments.importPreview')}</div>
              <div><strong>{t('apiTest.environments.envName')}:</strong> {importData.name || '-'}</div>
              {importData.base_url && <div><strong>Base URL:</strong> {importData.base_url}</div>}
              {importData.variables && (
                <div>
                  <strong>{t('apiTest.environments.envVariables')}:</strong>{' '}
                  {Object.keys(importData.variables).length} {t('apiTest.environments.variableCount')}
                </div>
              )}
            </div>
          )}
        </div>
      </Modal>

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
          <Form.Item name="is_default" label={t('apiTest.environments.setAsDefault')} valuePropName="checked">
            <Switch />
          </Form.Item>
        </Form>
      </Modal>
    </div>
  )
}

export default ApiTestEnvironments
