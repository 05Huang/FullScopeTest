/**
 * 质量门禁管理页面
 *
 * 展示质量门禁列表，支持创建/编辑/删除和手动触发评估。
 */
import { useState, useEffect, useCallback } from 'react'
import {
  Card,
  Table,
  Button,
  Modal,
  Input,
  InputNumber,
  Switch,
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
  PlayCircleOutlined,
  CheckCircleOutlined,
  CloseCircleOutlined,
  SafetyOutlined,
} from '@ant-design/icons'
import { useTranslation } from 'react-i18next'
import type { ColumnsType } from 'antd/es/table'
import { useProjectStore } from '@/stores/projectStore'
import qualityGateService, { QualityGate } from '@/services/qualityGateService'

const { Title, Text } = Typography

const QualityGates = () => {
  const { t } = useTranslation()
  const { currentProjectId } = useProjectStore()
  const [gates, setGates] = useState<QualityGate[]>([])
  const [loading, setLoading] = useState(false)
  const [modalOpen, setModalOpen] = useState(false)
  const [editingGate, setEditingGate] = useState<QualityGate | null>(null)
  const [submitLoading, setSubmitLoading] = useState(false)

  // 表单状态
  const [formName, setFormName] = useState('')
  const [formDesc, setFormDesc] = useState('')
  const [formPassRate, setFormPassRate] = useState<number | null>(100)
  const [formP95, setFormP95] = useState<number | null>(null)
  const [formVisualDiff, setFormVisualDiff] = useState<number | null>(null)
  const [formActive, setFormActive] = useState(true)

  const fetchGates = useCallback(async () => {
    setLoading(true)
    try {
      const res = await qualityGateService.getQualityGates(currentProjectId || undefined)
      if (res.code === 200) {
        setGates(res.data || [])
      }
    } catch {
      message.error(t('qualityGates.fetchFailed'))
    } finally {
      setLoading(false)
    }
  }, [currentProjectId, t])

  useEffect(() => {
    fetchGates()
  }, [fetchGates])

  const resetForm = () => {
    setFormName('')
    setFormDesc('')
    setFormPassRate(100)
    setFormP95(null)
    setFormVisualDiff(null)
    setFormActive(true)
  }

  const openCreateModal = () => {
    resetForm()
    setEditingGate(null)
    setModalOpen(true)
  }

  const openEditModal = (gate: QualityGate) => {
    setEditingGate(gate)
    setFormName(gate.name)
    setFormDesc(gate.description || '')
    setFormPassRate(gate.min_pass_rate)
    setFormP95(gate.max_p95_response_time)
    setFormVisualDiff(gate.max_visual_diff_percentage)
    setFormActive(gate.is_active)
    setModalOpen(true)
  }

  const handleSubmit = async () => {
    if (!formName.trim() || !currentProjectId) return
    setSubmitLoading(true)
    try {
      const payload = {
        name: formName.trim(),
        project_id: currentProjectId,
        description: formDesc.trim(),
        is_active: formActive,
        min_pass_rate: formPassRate,
        max_p95_response_time: formP95,
        max_visual_diff_percentage: formVisualDiff,
      }

      let res
      if (editingGate) {
        res = await qualityGateService.updateQualityGate(editingGate.id, payload)
      } else {
        res = await qualityGateService.createQualityGate(payload)
      }

      if (res.code === 200 || res.code === 201) {
        message.success(editingGate ? t('qualityGates.updateSuccess') : t('qualityGates.createSuccess'))
        setModalOpen(false)
        resetForm()
        await fetchGates()
      } else {
        message.error(res.message || t('qualityGates.saveFailed'))
      }
    } catch {
      message.error(t('qualityGates.saveFailed'))
    } finally {
      setSubmitLoading(false)
    }
  }

  const handleDelete = async (gateId: number) => {
    try {
      const res = await qualityGateService.deleteQualityGate(gateId)
      if (res.code === 200) {
        message.success(t('qualityGates.deleteSuccess'))
        await fetchGates()
      } else {
        message.error(res.message || t('qualityGates.deleteFailed'))
      }
    } catch {
      message.error(t('qualityGates.deleteFailed'))
    }
  }

  const columns: ColumnsType<QualityGate> = [
    {
      title: t('common.name'),
      dataIndex: 'name',
      key: 'name',
      render: (name: string) => <span style={{ fontWeight: 500 }}>{name}</span>,
    },
    {
      title: t('common.description'),
      dataIndex: 'description',
      key: 'description',
      ellipsis: true,
      render: (desc: string) => desc || '-',
    },
    {
      title: t('qualityGates.minPassRate'),
      dataIndex: 'min_pass_rate',
      key: 'min_pass_rate',
      width: 130,
      render: (val: number | null) => val !== null ? `${val}%` : '-',
    },
    {
      title: t('qualityGates.maxP95'),
      dataIndex: 'max_p95_response_time',
      key: 'max_p95_response_time',
      width: 140,
      render: (val: number | null) => val !== null ? `${val}ms` : '-',
    },
    {
      title: t('qualityGates.maxVisualDiff'),
      dataIndex: 'max_visual_diff_percentage',
      key: 'max_visual_diff_percentage',
      width: 140,
      render: (val: number | null) => val !== null ? `${val}%` : '-',
    },
    {
      title: t('common.status'),
      dataIndex: 'is_active',
      key: 'is_active',
      width: 80,
      render: (active: boolean) => (
        <Tag color={active ? 'green' : 'default'}>
          {active ? t('qualityGates.active') : t('qualityGates.inactive')}
        </Tag>
      ),
    },
    {
      title: t('common.createdAt'),
      dataIndex: 'created_at',
      key: 'created_at',
      width: 180,
      render: (val: string) => (val ? new Date(val).toLocaleString() : '-'),
    },
    {
      title: t('common.actions'),
      key: 'actions',
      width: 160,
      render: (_: unknown, record: QualityGate) => (
        <Space>
          <Tooltip title={t('qualityGates.evaluate')}>
            <Button
              type="link"
              size="small"
              icon={<PlayCircleOutlined />}
              onClick={() => message.info(t('qualityGates.evaluateHint'))}
            />
          </Tooltip>
          <Button
            type="link"
            size="small"
            icon={<EditOutlined />}
            onClick={() => openEditModal(record)}
          />
          <Popconfirm
            title={t('qualityGates.deleteConfirm')}
            onConfirm={() => handleDelete(record.id)}
            okText={t('common.confirm')}
            cancelText={t('common.cancel')}
          >
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
          <SafetyOutlined style={{ marginRight: 8 }} />
          {t('qualityGates.title')}
        </Title>
        <Button
          type="primary"
          icon={<PlusOutlined />}
          onClick={openCreateModal}
          disabled={!currentProjectId}
        >
          {t('qualityGates.create')}
        </Button>
      </div>

      <Card>
        <Table
          columns={columns}
          dataSource={gates}
          rowKey="id"
          loading={loading}
          locale={{ emptyText: <Empty description={t('qualityGates.noGates')} /> }}
          pagination={{ pageSize: 20, showSizeChanger: true }}
        />
      </Card>

      {/* 创建/编辑弹窗 */}
      <Modal
        title={editingGate ? t('qualityGates.edit') : t('qualityGates.create')}
        open={modalOpen}
        onCancel={() => { setModalOpen(false); setEditingGate(null); resetForm() }}
        onOk={handleSubmit}
        confirmLoading={submitLoading}
        okText={t('common.confirm')}
        cancelText={t('common.cancel')}
        width={600}
        destroyOnHidden
      >
        <div style={{ display: 'flex', flexDirection: 'column', gap: 16, marginTop: 8 }}>
          <div>
            <div style={{ marginBottom: 6, fontWeight: 500, fontSize: 13 }}>{t('common.name')}</div>
            <Input
              placeholder={t('qualityGates.namePlaceholder')}
              value={formName}
              onChange={(e) => setFormName(e.target.value)}
              maxLength={100}
              autoFocus
            />
          </div>
          <div>
            <div style={{ marginBottom: 6, fontWeight: 500, fontSize: 13 }}>{t('common.description')}</div>
            <Input.TextArea
              placeholder={t('qualityGates.descPlaceholder')}
              value={formDesc}
              onChange={(e) => setFormDesc(e.target.value)}
              rows={2}
              maxLength={500}
            />
          </div>
          <div style={{ display: 'flex', gap: 16 }}>
            <div style={{ flex: 1 }}>
              <div style={{ marginBottom: 6, fontWeight: 500, fontSize: 13 }}>
                {t('qualityGates.minPassRate')} (%)
              </div>
              <InputNumber
                value={formPassRate}
                onChange={setFormPassRate}
                min={0}
                max={100}
                style={{ width: '100%' }}
                placeholder="100"
              />
            </div>
            <div style={{ flex: 1 }}>
              <div style={{ marginBottom: 6, fontWeight: 500, fontSize: 13 }}>
                {t('qualityGates.maxP95')} (ms)
              </div>
              <InputNumber
                value={formP95}
                onChange={setFormP95}
                min={0}
                style={{ width: '100%' }}
                placeholder={t('qualityGates.optional')}
              />
            </div>
            <div style={{ flex: 1 }}>
              <div style={{ marginBottom: 6, fontWeight: 500, fontSize: 13 }}>
                {t('qualityGates.maxVisualDiff')} (%)
              </div>
              <InputNumber
                value={formVisualDiff}
                onChange={setFormVisualDiff}
                min={0}
                max={100}
                style={{ width: '100%' }}
                placeholder={t('qualityGates.optional')}
              />
            </div>
          </div>
          <div>
            <Space>
              <Switch checked={formActive} onChange={setFormActive} />
              <Text>{t('qualityGates.enabled')}</Text>
            </Space>
          </div>
        </div>
      </Modal>
    </div>
  )
}

export default QualityGates
