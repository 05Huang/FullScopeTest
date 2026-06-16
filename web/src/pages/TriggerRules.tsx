/**
 * 触发规则配置页面
 *
 * 展示触发规则列表，支持创建/编辑/删除和启用/禁用。
 */
import { useState, useEffect, useCallback } from 'react'
import {
  Card,
  Table,
  Button,
  Modal,
  Input,
  Select,
  Switch,
  Tag,
  message,
  Space,
  Typography,
  Popconfirm,
  Empty,
} from 'antd'
import {
  PlusOutlined,
  EditOutlined,
  DeleteOutlined,
  ThunderboltOutlined,
} from '@ant-design/icons'
import { useTranslation } from 'react-i18next'
import type { ColumnsType } from 'antd/es/table'
import { useProjectStore } from '@/stores/projectStore'
import triggerRuleService, { TriggerRule, CreateRuleRequest } from '@/services/triggerRuleService'

const { Title, Text } = Typography

const TRIGGER_EVENTS = [
  { value: 'webhook', label: 'Webhook' },
  { value: 'cron', label: 'Cron' },
  { value: 'push', label: 'Push' },
]

const TARGET_TYPES = [
  { value: 'api_collection', label: 'API Collection' },
  { value: 'web_collection', label: 'Web Collection' },
  { value: 'perf_scenario', label: 'Perf Scenario' },
]

const TriggerRules = () => {
  const { t } = useTranslation()
  const { currentProjectId } = useProjectStore()
  const [rules, setRules] = useState<TriggerRule[]>([])
  const [loading, setLoading] = useState(false)
  const [modalOpen, setModalOpen] = useState(false)
  const [editingRule, setEditingRule] = useState<TriggerRule | null>(null)
  const [submitLoading, setSubmitLoading] = useState(false)
  const [formName, setFormName] = useState('')
  const [formDesc, setFormDesc] = useState('')
  const [formEvent, setFormEvent] = useState('webhook')
  const [formTargetType, setFormTargetType] = useState('api_collection')

  const fetchRules = useCallback(async () => {
    if (!currentProjectId) return
    setLoading(true)
    try {
      const res = await triggerRuleService.getTriggerRules(currentProjectId)
      if (res.code === 200) setRules(res.data || [])
    } catch {
      message.error(t('triggerRules.fetchFailed'))
    } finally {
      setLoading(false)
    }
  }, [currentProjectId, t])

  useEffect(() => { fetchRules() }, [fetchRules])

  const resetForm = () => {
    setFormName(''); setFormDesc(''); setFormEvent('webhook'); setFormTargetType('api_collection')
  }

  const handleSubmit = async () => {
    if (!formName.trim() || !currentProjectId) return
    setSubmitLoading(true)
    try {
      const payload: CreateRuleRequest = {
        project_id: currentProjectId,
        name: formName.trim(),
        trigger_event: formEvent,
        target_type: formTargetType,
        description: formDesc.trim(),
      }
      const res = editingRule
        ? await triggerRuleService.updateTriggerRule(editingRule.id, payload)
        : await triggerRuleService.createTriggerRule(payload)
      if (res.code === 200 || res.code === 201) {
        message.success(editingRule ? t('triggerRules.updateSuccess') : t('triggerRules.createSuccess'))
        setModalOpen(false); resetForm(); await fetchRules()
      } else {
        message.error(res.message || t('triggerRules.saveFailed'))
      }
    } catch {
      message.error(t('triggerRules.saveFailed'))
    } finally {
      setSubmitLoading(false)
    }
  }

  const handleDelete = async (id: number) => {
    try {
      const res = await triggerRuleService.deleteTriggerRule(id)
      if (res.code === 200) { message.success(t('triggerRules.deleteSuccess')); await fetchRules() }
      else message.error(res.message || t('triggerRules.deleteFailed'))
    } catch { message.error(t('triggerRules.deleteFailed')) }
  }

  const openEdit = (rule: TriggerRule) => {
    setEditingRule(rule); setFormName(rule.name); setFormDesc(rule.description || '')
    setFormEvent(rule.trigger_event); setFormTargetType(rule.target_type); setModalOpen(true)
  }

  const columns: ColumnsType<TriggerRule> = [
    { title: t('common.name'), dataIndex: 'name', key: 'name', render: (n: string) => <span style={{ fontWeight: 500 }}>{n}</span> },
    { title: t('common.description'), dataIndex: 'description', key: 'description', ellipsis: true, render: (d: string) => d || '-' },
    { title: t('triggerRules.triggerEvent'), dataIndex: 'trigger_event', key: 'trigger_event', width: 120, render: (e: string) => <Tag color="blue">{e}</Tag> },
    { title: t('triggerRules.targetType'), dataIndex: 'target_type', key: 'target_type', width: 150, render: (tt: string) => <Tag>{tt}</Tag> },
    { title: t('common.status'), dataIndex: 'is_active', key: 'is_active', width: 80, render: (a: boolean) => <Tag color={a ? 'green' : 'default'}>{a ? t('qualityGates.active') : t('qualityGates.inactive')}</Tag> },
    { title: t('common.createdAt'), dataIndex: 'created_at', key: 'created_at', width: 180, render: (v: string) => v ? new Date(v).toLocaleString() : '-' },
    {
      title: t('common.actions'), key: 'actions', width: 120,
      render: (_: unknown, record: TriggerRule) => (
        <Space>
          <Button type="link" size="small" icon={<EditOutlined />} onClick={() => openEdit(record)} />
          <Popconfirm title={t('triggerRules.deleteConfirm')} onConfirm={() => handleDelete(record.id)} okText={t('common.confirm')} cancelText={t('common.cancel')}>
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
          <ThunderboltOutlined style={{ marginRight: 8 }} />
          {t('triggerRules.title')}
        </Title>
        <Button type="primary" icon={<PlusOutlined />} onClick={() => { resetForm(); setEditingRule(null); setModalOpen(true) }} disabled={!currentProjectId}>
          {t('triggerRules.create')}
        </Button>
      </div>
      <Card>
        <Table columns={columns} dataSource={rules} rowKey="id" loading={loading}
          locale={{ emptyText: <Empty description={t('triggerRules.noRules')} /> }}
          pagination={{ pageSize: 20, showSizeChanger: true }} />
      </Card>
      <Modal title={editingRule ? t('triggerRules.edit') : t('triggerRules.create')} open={modalOpen}
        onCancel={() => { setModalOpen(false); setEditingRule(null); resetForm() }}
        onOk={handleSubmit} confirmLoading={submitLoading} okText={t('common.confirm')} cancelText={t('common.cancel')} destroyOnHidden>
        <div style={{ display: 'flex', flexDirection: 'column', gap: 16, marginTop: 8 }}>
          <div>
            <div style={{ marginBottom: 6, fontWeight: 500, fontSize: 13 }}>{t('common.name')}</div>
            <Input placeholder={t('triggerRules.namePlaceholder')} value={formName} onChange={(e) => setFormName(e.target.value)} maxLength={100} autoFocus />
          </div>
          <div>
            <div style={{ marginBottom: 6, fontWeight: 500, fontSize: 13 }}>{t('common.description')}</div>
            <Input.TextArea placeholder={t('triggerRules.descPlaceholder')} value={formDesc} onChange={(e) => setFormDesc(e.target.value)} rows={2} maxLength={500} />
          </div>
          <div style={{ display: 'flex', gap: 16 }}>
            <div style={{ flex: 1 }}>
              <div style={{ marginBottom: 6, fontWeight: 500, fontSize: 13 }}>{t('triggerRules.triggerEvent')}</div>
              <Select value={formEvent} onChange={setFormEvent} style={{ width: '100%' }} options={TRIGGER_EVENTS} />
            </div>
            <div style={{ flex: 1 }}>
              <div style={{ marginBottom: 6, fontWeight: 500, fontSize: 13 }}>{t('triggerRules.targetType')}</div>
              <Select value={formTargetType} onChange={setFormTargetType} style={{ width: '100%' }} options={TARGET_TYPES} />
            </div>
          </div>
        </div>
      </Modal>
    </div>
  )
}

export default TriggerRules
