/**
 * 通知渠道配置页面
 *
 * 管理通知渠道（Webhook/钉钉/飞书/Slack），支持创建/编辑/删除和测试发送。
 */
import { useState, useEffect, useCallback } from 'react'
import {
  Card,
  Table,
  Button,
  Modal,
  Input,
  Select,
  Tag,
  message,
  Space,
  Typography,
  Popconfirm,
  Empty,
  Tooltip,
} from 'antd'
import {
  PlusOutlined,
  EditOutlined,
  DeleteOutlined,
  SendOutlined,
  BellOutlined,
} from '@ant-design/icons'
import { useTranslation } from 'react-i18next'
import type { ColumnsType } from 'antd/es/table'
import notificationService, { NotificationConfig } from '@/services/notificationService'

const { Title } = Typography

const CHANNEL_TYPES = [
  { value: 'webhook', label: 'Webhook' },
  { value: 'dingtalk', label: 'DingTalk' },
  { value: 'feishu', label: 'Feishu' },
  { value: 'slack', label: 'Slack' },
]

const EVENTS = [
  { value: 'test_completed', label: 'Test Completed' },
  { value: 'test_failed', label: 'Test Failed' },
  { value: 'alert_triggered', label: 'Alert Triggered' },
]

const NotificationSettings = () => {
  const { t } = useTranslation()
  const [configs, setConfigs] = useState<NotificationConfig[]>([])
  const [loading, setLoading] = useState(false)
  const [modalOpen, setModalOpen] = useState(false)
  const [editingConfig, setEditingConfig] = useState<NotificationConfig | null>(null)
  const [submitLoading, setSubmitLoading] = useState(false)
  const [formName, setFormName] = useState('')
  const [formType, setFormType] = useState('webhook')
  const [formUrl, setFormUrl] = useState('')
  const [formEvents, setFormEvents] = useState<string[]>(['test_completed'])

  const fetchConfigs = useCallback(async () => {
    setLoading(true)
    try {
      const res = await notificationService.getNotificationConfigs()
      if (res.code === 200) setConfigs(res.data || [])
    } catch {
      message.error(t('notifications.fetchFailed'))
    } finally {
      setLoading(false)
    }
  }, [t])

  useEffect(() => { fetchConfigs() }, [fetchConfigs])

  const resetForm = () => {
    setFormName(''); setFormType('webhook'); setFormUrl(''); setFormEvents(['test_completed'])
  }

  const handleSubmit = async () => {
    if (!formName.trim()) return
    setSubmitLoading(true)
    try {
      const payload = { name: formName.trim(), channel_type: formType, webhook_url: formUrl.trim(), events: formEvents }
      const res = editingConfig
        ? await notificationService.updateNotificationConfig(editingConfig.id, payload)
        : await notificationService.createNotificationConfig(payload)
      if (res.code === 200 || res.code === 201) {
        message.success(editingConfig ? t('notifications.updateSuccess') : t('notifications.createSuccess'))
        setModalOpen(false); resetForm(); await fetchConfigs()
      } else {
        message.error(res.message || t('notifications.saveFailed'))
      }
    } catch {
      message.error(t('notifications.saveFailed'))
    } finally {
      setSubmitLoading(false)
    }
  }

  const handleDelete = async (id: number) => {
    try {
      const res = await notificationService.deleteNotificationConfig(id)
      if (res.code === 200) { message.success(t('notifications.deleteSuccess')); await fetchConfigs() }
      else message.error(res.message || t('notifications.deleteFailed'))
    } catch { message.error(t('notifications.deleteFailed')) }
  }

  const handleTest = async (id: number) => {
    try {
      const res = await notificationService.testNotification(id)
      if (res.code === 200) message.success(t('notifications.testSuccess'))
      else message.error(res.message || t('notifications.testFailed'))
    } catch { message.error(t('notifications.testFailed')) }
  }

  const openEdit = (config: NotificationConfig) => {
    setEditingConfig(config); setFormName(config.name); setFormType(config.channel_type)
    setFormUrl(config.webhook_url || ''); setFormEvents(config.events || []); setModalOpen(true)
  }

  const columns: ColumnsType<NotificationConfig> = [
    { title: t('common.name'), dataIndex: 'name', key: 'name', render: (n: string) => <span style={{ fontWeight: 500 }}>{n}</span> },
    { title: t('notifications.channelType'), dataIndex: 'channel_type', key: 'channel_type', width: 120, render: (ct: string) => <Tag color="blue">{ct}</Tag> },
    { title: t('notifications.webhookUrl'), dataIndex: 'webhook_url', key: 'webhook_url', ellipsis: true, render: (u: string) => u || '-' },
    { title: t('notifications.events'), dataIndex: 'events', key: 'events', render: (events: string[]) => <Space size={4} wrap>{(events || []).map((e) => <Tag key={e}>{e}</Tag>)}</Space> },
    { title: t('common.status'), dataIndex: 'is_active', key: 'is_active', width: 80, render: (a: boolean) => <Tag color={a ? 'green' : 'default'}>{a ? t('qualityGates.active') : t('qualityGates.inactive')}</Tag> },
    {
      title: t('common.actions'), key: 'actions', width: 140,
      render: (_: unknown, record: NotificationConfig) => (
        <Space>
          <Tooltip title={t('notifications.testSend')}>
            <Button type="link" size="small" icon={<SendOutlined />} onClick={() => handleTest(record.id)} />
          </Tooltip>
          <Button type="link" size="small" icon={<EditOutlined />} onClick={() => openEdit(record)} />
          <Popconfirm title={t('notifications.deleteConfirm')} onConfirm={() => handleDelete(record.id)} okText={t('common.confirm')} cancelText={t('common.cancel')}>
            <Button type="link" size="small" danger icon={<DeleteOutlined />} />
          </Popconfirm>
        </Space>
      ),
    },
  ]

  return (
    <div style={{ padding: 0 }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 16 }}>
        <Title level={4} style={{ margin: 0 }}>
          <BellOutlined style={{ marginRight: 8 }} />
          {t('notifications.title')}
        </Title>
        <Button type="primary" icon={<PlusOutlined />} onClick={() => { resetForm(); setEditingConfig(null); setModalOpen(true) }}>
          {t('notifications.create')}
        </Button>
      </div>
      <Card>
        <Table columns={columns} dataSource={configs} rowKey="id" loading={loading}
          locale={{ emptyText: <Empty description={t('notifications.noConfigs')} /> }}
          pagination={{ pageSize: 20 }} />
      </Card>
      <Modal title={editingConfig ? t('notifications.edit') : t('notifications.create')} open={modalOpen}
        onCancel={() => { setModalOpen(false); setEditingConfig(null); resetForm() }}
        onOk={handleSubmit} confirmLoading={submitLoading} okText={t('common.confirm')} cancelText={t('common.cancel')} destroyOnHidden>
        <div style={{ display: 'flex', flexDirection: 'column', gap: 16, marginTop: 8 }}>
          <div>
            <div style={{ marginBottom: 6, fontWeight: 500, fontSize: 13 }}>{t('common.name')}</div>
            <Input placeholder={t('notifications.namePlaceholder')} value={formName} onChange={(e) => setFormName(e.target.value)} maxLength={100} autoFocus />
          </div>
          <div>
            <div style={{ marginBottom: 6, fontWeight: 500, fontSize: 13 }}>{t('notifications.channelType')}</div>
            <Select value={formType} onChange={setFormType} style={{ width: '100%' }} options={CHANNEL_TYPES} />
          </div>
          <div>
            <div style={{ marginBottom: 6, fontWeight: 500, fontSize: 13 }}>{t('notifications.webhookUrl')}</div>
            <Input placeholder={t('notifications.urlPlaceholder')} value={formUrl} onChange={(e) => setFormUrl(e.target.value)} />
          </div>
          <div>
            <div style={{ marginBottom: 6, fontWeight: 500, fontSize: 13 }}>{t('notifications.events')}</div>
            <Select mode="multiple" value={formEvents} onChange={setFormEvents} style={{ width: '100%' }} options={EVENTS} />
          </div>
        </div>
      </Modal>
    </div>
  )
}

export default NotificationSettings
