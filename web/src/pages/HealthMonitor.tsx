import { useState, useEffect, useCallback } from 'react'
import {
  Card, Table, Button, Modal, Form, Input, InputNumber, Select, Space,
  Typography, Tag, message, Progress, Row, Col, Statistic, Empty, Tooltip,
} from 'antd'
import {
  PlusOutlined, DeleteOutlined, ReloadOutlined, CheckCircleOutlined,
  CloseCircleOutlined, DashboardOutlined, ThunderboltOutlined,
} from '@ant-design/icons'
import { useTranslation } from 'react-i18next'
import type { ColumnsType } from 'antd/es/table'
import healthMonitorService, { HealthMonitor, UptimeStats } from '@/services/healthMonitorService'

const { Title, Text } = Typography

const HealthMonitorPage = () => {
  const { t } = useTranslation()
  const [loading, setLoading] = useState(true)
  const [monitors, setMonitors] = useState<HealthMonitor[]>([])
  const [createModalOpen, setCreateModalOpen] = useState(false)
  const [creating, setCreating] = useState(false)
  const [statsModalOpen, setStatsModalOpen] = useState(false)
  const [statsData, setStatsData] = useState<UptimeStats | null>(null)
  const [statsLoading, setStatsLoading] = useState(false)
  const [form] = Form.useForm()

  const loadMonitors = useCallback(async () => {
    setLoading(true)
    try {
      const res = await healthMonitorService.getMonitors()
      if (res.code === 200) setMonitors(res.data || [])
    } catch {} finally { setLoading(false) }
  }, [])

  useEffect(() => { loadMonitors() }, [loadMonitors])

  const handleCreate = async () => {
    try {
      const values = await form.validateFields()
      setCreating(true)
      const res = await healthMonitorService.createMonitor(values)
      if (res.code === 200 || res.code === 201) {
        message.success(t('healthMonitor.addSuccess'))
        setCreateModalOpen(false)
        form.resetFields()
        await loadMonitors()
      } else { message.error(res.message || t('healthMonitor.addFailed')) }
    } catch {} finally { setCreating(false) }
  }

  const handleDelete = (id: number) => {
    Modal.confirm({
      title: t('common.confirm'),
      okText: t('common.confirm'), cancelText: t('common.cancel'),
      okButtonProps: { danger: true },
      onOk: async () => {
        try {
          const res = await healthMonitorService.deleteMonitor(id)
          if (res.code === 200) { message.success(t('healthMonitor.deleteSuccess')); await loadMonitors() }
          else { message.error(res.message || t('healthMonitor.deleteFailed')) }
        } catch { message.error(t('healthMonitor.deleteFailed')) }
      },
    })
  }

  const handleManualCheck = async (id: number) => {
    try {
      const res = await healthMonitorService.runCheck(id)
      if (res.code === 200) { message.success(t('healthMonitor.checkSuccess')); await loadMonitors() }
      else { message.error(res.message || t('healthMonitor.checkFailed')) }
    } catch { message.error(t('healthMonitor.checkFailed')) }
  }

  const handleViewStats = async (id: number) => {
    setStatsLoading(true)
    setStatsModalOpen(true)
    try {
      const res = await healthMonitorService.getUptimeStats(id, 7)
      if (res.code === 200) setStatsData(res.data)
    } catch {} finally { setStatsLoading(false) }
  }

  const columns: ColumnsType<HealthMonitor> = [
    { title: t('healthMonitor.name'), dataIndex: 'name', key: 'name', render: (v: string) => <Text strong>{v}</Text> },
    { title: 'URL', dataIndex: 'url', key: 'url', ellipsis: true, render: (v: string) => <Text code style={{ fontSize: 12 }}>{v}</Text> },
    { title: t('healthMonitor.currentStatus'), dataIndex: 'last_status', key: 'last_status', width: 100,
      render: (v: string | null) => {
        if (!v) return <Tag>'-'</Tag>
        return v === 'up' ? <Tag color='green' icon={<CheckCircleOutlined />}>{t('healthMonitor.statusUp')}</Tag>
          : <Tag color='red' icon={<CloseCircleOutlined />}>{t('healthMonitor.statusDown')}</Tag>
      }
    },
    { title: t('healthMonitor.uptime'), key: 'uptime', width: 120,
      render: (_: unknown, record: HealthMonitor) => {
        if (!record.last_status) return <Tag>'-'</Tag>
        const isUp = record.last_status === 'up'
        return <Progress percent={isUp ? 100 : 0} size='small' strokeColor={isUp ? '#52c41a' : '#ff4d4f'} />
      }
    },
    { title: t('healthMonitor.avgResponseTime'), dataIndex: 'last_response_time', key: 'response_time', width: 140,
      render: (v: number | null) => v !== null ? <Statistic value={v} suffix='ms' valueStyle={{ fontSize: 14 }} /> : '-'
    },
    { title: t('healthMonitor.lastCheck'), dataIndex: 'last_check_at', key: 'last_check', width: 160,
      render: (v: string | null) => v ? new Date(v).toLocaleString() : '-'
    },
    { title: t('common.actions') || 'Actions', key: 'actions', width: 200,
      render: (_: unknown, record: HealthMonitor) => (
        <Space>
          <Tooltip title={t('healthMonitor.manualCheck')}>
            <Button size='small' icon={<ReloadOutlined />} onClick={() => handleManualCheck(record.id)} />
          </Tooltip>
          <Button size='small' icon={<DashboardOutlined />} onClick={() => handleViewStats(record.id)}>{t('healthMonitor.uptime')}</Button>
          <Button size='small' danger icon={<DeleteOutlined />} onClick={() => handleDelete(record.id)} />
        </Space>
      )
    },
  ];

  // 区间选择选项
  const intervalOptions = [
    { label: '1 min', value: 60 },
    { label: '5 min', value: 300 },
    { label: '15 min', value: 900 },
    { label: '60 min', value: 3600 },
  ];

  return (
    <div style={{ padding: 24 }}>
      <div style={{ marginBottom: 24, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <div>
          <Title level={3} style={{ marginBottom: 4 }}>{t('healthMonitor.title')}</Title>
          <Text type='secondary'>{t('healthMonitor.subtitle')}</Text>
        </div>
        <Button type='primary' icon={<PlusOutlined />} onClick={() => setCreateModalOpen(true)}>{t('healthMonitor.addMonitor')}</Button>
      </div>

      {monitors.length === 0 && !loading ? (
        <Empty description={t('healthMonitor.noMonitors')}>
          <Button type='primary' onClick={() => setCreateModalOpen(true)}>{t('healthMonitor.addMonitor')}</Button>
        </Empty>
      ) : (
        <Card>
          <Table
            columns={columns}
            dataSource={monitors}
            rowKey='id'
            loading={loading}
            pagination={false}
          />
        </Card>
      )}

      {/* 创建监控项弹窗 */}
      <Modal
        title={t('healthMonitor.createTitle')}
        open={createModalOpen}
        onCancel={() => { setCreateModalOpen(false); form.resetFields() }}
        onOk={handleCreate}
        confirmLoading={creating}
      >
        <Form form={form} layout='vertical'>
          <Form.Item name='name' label={t('healthMonitor.name')} rules={[{ required: true }]}>
            <Input placeholder={t('healthMonitor.name')} />
          </Form.Item>
          <Form.Item name='url' label={t('healthMonitor.url')} rules={[{ required: true, type: 'url' }]}>
            <Input placeholder='https://api.example.com/health' />
          </Form.Item>
          <Row gutter={16}>
            <Col span={12}>
              <Form.Item name='check_interval' label={t('healthMonitor.interval')} initialValue={300}>
                <Select options={intervalOptions} />
              </Form.Item>
            </Col>
            <Col span={12}>
              <Form.Item name='expected_status' label={t('healthMonitor.expectedStatus')} initialValue={200}>
                <InputNumber min={100} max={599} style={{ width: '100%' }} />
              </Form.Item>
            </Col>
          </Row>
        </Form>
      </Modal>

      {/* 统计弹窗 */}
      <Modal
        title={t('healthMonitor.uptime')}
        open={statsModalOpen}
        onCancel={() => { setStatsModalOpen(false); setStatsData(null) }}
        footer={null}
        width={600}
      >
        {statsLoading ? <div style={{ textAlign: 'center', padding: 40 }}><ThunderboltOutlined spin style={{ fontSize: 32 }} /></div> :
        statsData ? (
          <Row gutter={[16, 16]}>
            <Col span={8}><Statistic title={t('healthMonitor.uptime')} value={statsData.uptime_percentage} suffix='%' precision={1} /></Col>
            <Col span={8}><Statistic title={t('healthMonitor.avgResponseTime')} value={statsData.avg_response_time} suffix='ms' precision={0} /></Col>
            <Col span={8}><Statistic title={t('healthMonitor.total') || 'Total'} value={statsData.total_checks} /></Col>
          </Row>
        ) : <Empty />}
      </Modal>
    </div>
  )
}

export default HealthMonitorPage
