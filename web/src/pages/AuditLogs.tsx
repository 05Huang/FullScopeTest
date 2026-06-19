/**
 * 审计日志页面
 *
 * 展示审计日志列表，支持筛选、详情查看和统计图表。
 * 日志只读，不可编辑/删除。
 */
import { useState, useEffect, useCallback, useRef } from 'react'
import {
  Card,
  Table,
  Button,
  Modal,
  Select,
  DatePicker,
  Space,
  Typography,
  Tag,
  Empty,
  Spin,
  Row,
  Col,
  Statistic,
  message,
  Descriptions,
} from 'antd'
import {
  ReloadOutlined,
  EyeOutlined,
  FileSearchOutlined,
  PieChartOutlined,
  DownloadOutlined,
} from '@ant-design/icons'
import { useTranslation } from 'react-i18next'
import type { ColumnsType } from 'antd/es/table'
import ReactECharts from 'echarts-for-react'
import auditLogService, {
  AuditLog,
  AuditLogListParams,
  AuditStats,
} from '@/services/auditLogService'

const { Title, Text } = Typography
const { RangePicker } = DatePicker

// 操作类型颜色映射
const ACTION_COLORS: Record<string, string> = {
  create: 'green',
  update: 'blue',
  delete: 'red',
  login: 'cyan',
  logout: 'orange',
  execute: 'purple',
}

// 资源类型标签
const RESOURCE_LABELS: Record<string, string> = {
  project: 'Project',
  test_case: 'TestCase',
  test_run: 'TestRun',
  organization: 'Organization',
  user: 'User',
  environment: 'Environment',
  test_plan: 'TestPlan',
  api_token: 'ApiToken',
}

const AuditLogs = () => {
  const { t } = useTranslation()
  const [logs, setLogs] = useState<AuditLog[]>([])
  const [total, setTotal] = useState(0)
  const [loading, setLoading] = useState(false)
  const [page, setPage] = useState(1)
  const [pageSize, setPageSize] = useState(20)
  const [filters, setFilters] = useState<AuditLogListParams>({})
  const [detailModalOpen, setDetailModalOpen] = useState(false)
  const [selectedLog, setSelectedLog] = useState<AuditLog | null>(null)
  const [stats, setStats] = useState<AuditStats | null>(null)
  const [statsLoading, setStatsLoading] = useState(false)
  const [showStats, setShowStats] = useState(false)
  const [statsDays, setStatsDays] = useState(30)

  const fetchLogs = useCallback(async () => {
    setLoading(true)
    try {
      const res = await auditLogService.getAuditLogs({
        page,
        per_page: pageSize,
        ...filters,
      })
      if (res.code === 200 && res.data) {
        setLogs(res.data.items || [])
        setTotal(res.data.total || 0)
      }
    } catch {
      message.error(t('auditLogs.fetchFailed'))
    } finally {
      setLoading(false)
    }
  }, [page, pageSize, filters, t])

  const fetchStats = useCallback(async () => {
    setStatsLoading(true)
    try {
      const res = await auditLogService.getAuditStats(statsDays)
      if (res.code === 200 && res.data) {
        setStats(res.data)
      }
    } catch {
      message.error(t('auditLogs.statsFailed'))
    } finally {
      setStatsLoading(false)
    }
  }, [statsDays, t])

  useEffect(() => {
    fetchLogs()
  }, [fetchLogs])

  useEffect(() => {
    if (showStats) {
      fetchStats()
    }
  }, [showStats, fetchStats])

  const handleViewDetail = (log: AuditLog) => {
    setSelectedLog(log)
    setDetailModalOpen(true)
  }

  // 操作类型饼图配置
  const getPieOption = () => {
    if (!stats) return {}
    const data = Object.entries(stats.by_action).map(([name, value]) => ({
      name,
      value,
    }))
    return {
      tooltip: { trigger: 'item', formatter: '{b}: {c} ({d}%)' },
      color: ['#2D6A64', '#629B95', '#D4B483', '#5B8FB9', '#C75450', '#4A9E96'],
      series: [
        {
          type: 'pie',
          radius: ['40%', '70%'],
          avoidLabelOverlap: false,
          itemStyle: { borderRadius: 6, borderColor: '#fff', borderWidth: 2 },
          label: { show: true, formatter: '{b}\n{c}' },
          data,
        },
      ],
    }
  }

  // 资源类型柱状图配置
  const getBarOption = () => {
    if (!stats) return {}
    const entries = Object.entries(stats.by_resource)
    return {
      tooltip: { trigger: 'axis' },
      color: ['#2D6A64'],
      grid: { left: '3%', right: '4%', bottom: '3%', containLabel: true },
      xAxis: {
        type: 'category',
        data: entries.map(([k]) => k),
        axisLabel: { rotate: 30 },
      },
      yAxis: { type: 'value' },
      series: [
        {
          type: 'bar',
          data: entries.map(([, v]) => v),
          barWidth: '60%',
          itemStyle: { borderRadius: [4, 4, 0, 0] },
        },
      ],
    }
  }

  const columns: ColumnsType<AuditLog> = [
    {
      title: 'ID',
      dataIndex: 'id',
      key: 'id',
      width: 70,
    },
    {
      title: t('auditLogs.operator'),
      dataIndex: 'user_id',
      key: 'user_id',
      width: 100,
      render: (uid: number | null) => (uid ? `User #${uid}` : '-'),
    },
    {
      title: t('auditLogs.action'),
      dataIndex: 'action',
      key: 'action',
      width: 100,
      render: (action: string) => (
        <Tag color={ACTION_COLORS[action] || 'default'}>
          {action.toUpperCase()}
        </Tag>
      ),
    },
    {
      title: t('auditLogs.resourceType'),
      dataIndex: 'resource_type',
      key: 'resource_type',
      width: 120,
      render: (type: string) => RESOURCE_LABELS[type] || type,
    },
    {
      title: t('auditLogs.resourceId'),
      dataIndex: 'resource_id',
      key: 'resource_id',
      width: 80,
      render: (id: number | null) => id ?? '-',
    },
    {
      title: t('auditLogs.ipAddress'),
      dataIndex: 'ip_address',
      key: 'ip_address',
      width: 140,
      render: (ip: string | null) => ip || '-',
    },
    {
      title: t('common.createdAt'),
      dataIndex: 'created_at',
      key: 'created_at',
      width: 180,
      render: (val: string) => (val ? new Date(val).toLocaleString() : '-'),
      sorter: true,
    },
    {
      title: t('common.actions'),
      key: 'actions',
      width: 80,
      render: (_: unknown, record: AuditLog) => (
        <Button
          type="link"
          size="small"
          icon={<EyeOutlined />}
          onClick={() => handleViewDetail(record)}
        >
          {t('auditLogs.detail')}
        </Button>
      ),
    },
  ]

  // 渲染 JSON diff 区域
  const renderChanges = (log: AuditLog) => {
    if (log.changes) {
      return (
        <pre style={{
          background: '#f6f8f8',
          padding: 12,
          borderRadius: 8,
          fontSize: 12,
          maxHeight: 300,
          overflow: 'auto',
        }}>
          {JSON.stringify(log.changes, null, 2)}
        </pre>
      )
    }
    if (log.old_values || log.new_values) {
      return (
        <Row gutter={16}>
          <Col span={12}>
            <Text strong style={{ fontSize: 12, color: '#C75450' }}>{t('auditLogs.oldValues')}</Text>
            <pre style={{
              background: '#fff2f0',
              padding: 12,
              borderRadius: 8,
              fontSize: 12,
              maxHeight: 250,
              overflow: 'auto',
              marginTop: 4,
            }}>
              {JSON.stringify(log.old_values || {}, null, 2)}
            </pre>
          </Col>
          <Col span={12}>
            <Text strong style={{ fontSize: 12, color: '#2D6A64' }}>{t('auditLogs.newValues')}</Text>
            <pre style={{
              background: '#f6ffed',
              padding: 12,
              borderRadius: 8,
              fontSize: 12,
              maxHeight: 250,
              overflow: 'auto',
              marginTop: 4,
            }}>
              {JSON.stringify(log.new_values || {}, null, 2)}
            </pre>
          </Col>
        </Row>
      )
    }
    return <Text type="secondary">{t('auditLogs.noChanges')}</Text>
  }

  return (
    <div style={{ padding: 0 }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 16 }}>
        <Title level={4} style={{ margin: 0 }}>
          <FileSearchOutlined style={{ marginRight: 8 }} />
          {t('auditLogs.title')}
        </Title>
        <Space>
          <Button
            icon={<PieChartOutlined />}
            onClick={() => setShowStats(!showStats)}
          >
            {showStats ? t('auditLogs.hideStats') : t('auditLogs.showStats')}
          </Button>
          <Button icon={<ReloadOutlined />} onClick={fetchLogs}>
            {t('common.refresh')}
          </Button>
          <Button
            icon={<DownloadOutlined />}
            onClick={async () => {
              try {
                const res = await auditLogService.exportAuditLogs({ format: 'csv', days: 30 })
                if (res.code === 200 && res.data) {
                  const blob = new Blob([res.data], { type: 'text/csv' })
                  const url = URL.createObjectURL(blob)
                  const link = document.createElement('a')
                  link.href = url
                  link.download = `audit-logs-${new Date().toISOString().slice(0, 10)}.csv`
                  document.body.appendChild(link)
                  link.click()
                  document.body.removeChild(link)
                  URL.revokeObjectURL(url)
                  message.success('导出成功')
                }
              } catch {
                message.error('导出失败')
              }
            }}
          >
            {t('common.export') || '导出'}
          </Button>
        </Space>
      </div>

      {/* 统计图表 */}
      {showStats && (
        <Card style={{ marginBottom: 16 }} loading={statsLoading}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 16 }}>
            <Title level={5} style={{ margin: 0 }}>{t('auditLogs.statistics')}</Title>
            <Select
              value={statsDays}
              onChange={setStatsDays}
              style={{ width: 120 }}
              options={[
                { value: 7, label: t('auditLogs.last7Days') },
                { value: 30, label: t('auditLogs.last30Days') },
                { value: 90, label: t('auditLogs.last90Days') },
              ]}
            />
          </div>
          {stats && (
            <Row gutter={16}>
              <Col span={6}>
                <Statistic
                  title={t('auditLogs.totalOperations')}
                  value={Object.values(stats.by_action).reduce((a, b) => a + b, 0)}
                />
              </Col>
              <Col span={6}>
                <Statistic
                  title={t('auditLogs.activeUsers')}
                  value={stats.active_users.length}
                />
              </Col>
              <Col span={6}>
                <ReactECharts option={getPieOption()} style={{ height: 200 }} />
              </Col>
              <Col span={6}>
                <ReactECharts option={getBarOption()} style={{ height: 200 }} />
              </Col>
            </Row>
          )}
        </Card>
      )}

      {/* 筛选条件 */}
      <Card style={{ marginBottom: 16 }}>
        <Space wrap>
          <Select
            placeholder={t('auditLogs.filterAction')}
            allowClear
            style={{ width: 140 }}
            value={filters.action}
            onChange={(val) => setFilters((prev) => ({ ...prev, action: val }))}
            options={[
              { value: 'create', label: 'Create' },
              { value: 'update', label: 'Update' },
              { value: 'delete', label: 'Delete' },
              { value: 'login', label: 'Login' },
              { value: 'logout', label: 'Logout' },
              { value: 'execute', label: 'Execute' },
            ]}
          />
          <Select
            placeholder={t('auditLogs.filterResourceType')}
            allowClear
            style={{ width: 160 }}
            value={filters.resource_type}
            onChange={(val) => setFilters((prev) => ({ ...prev, resource_type: val }))}
            options={Object.entries(RESOURCE_LABELS).map(([value, label]) => ({
              value,
              label,
            }))}
          />
          <Button
            onClick={() => {
              setFilters({})
              setPage(1)
            }}
          >
            {t('common.reset')}
          </Button>
        </Space>
      </Card>

      {/* 日志列表 */}
      <Card>
        <Table
          columns={columns}
          dataSource={logs}
          rowKey="id"
          loading={loading}
          locale={{ emptyText: <Empty description={t('auditLogs.noLogs')} /> }}
          pagination={{
            current: page,
            pageSize,
            total,
            showSizeChanger: true,
            showTotal: (totalVal) => `${totalVal} ${t('common.count')}`,
            onChange: (p, ps) => {
              setPage(p)
              setPageSize(ps)
            },
          }}
        />
      </Card>

      {/* 日志详情弹窗 */}
      <Modal
        title={t('auditLogs.logDetail')}
        open={detailModalOpen}
        onCancel={() => { setDetailModalOpen(false); setSelectedLog(null) }}
        footer={null}
        width={720}
        destroyOnHidden
      >
        {selectedLog && (
          <div>
            <Descriptions bordered column={2} size="small" style={{ marginBottom: 16 }}>
              <Descriptions.Item label="ID">{selectedLog.id}</Descriptions.Item>
              <Descriptions.Item label={t('auditLogs.operator')}>
                {selectedLog.user_id ? `User #${selectedLog.user_id}` : '-'}
              </Descriptions.Item>
              <Descriptions.Item label={t('auditLogs.action')}>
                <Tag color={ACTION_COLORS[selectedLog.action] || 'default'}>
                  {selectedLog.action.toUpperCase()}
                </Tag>
              </Descriptions.Item>
              <Descriptions.Item label={t('auditLogs.resourceType')}>
                {RESOURCE_LABELS[selectedLog.resource_type] || selectedLog.resource_type}
              </Descriptions.Item>
              <Descriptions.Item label={t('auditLogs.resourceId')}>
                {selectedLog.resource_id ?? '-'}
              </Descriptions.Item>
              <Descriptions.Item label={t('auditLogs.ipAddress')}>
                {selectedLog.ip_address || '-'}
              </Descriptions.Item>
              <Descriptions.Item label={t('common.createdAt')} span={2}>
                {selectedLog.created_at ? new Date(selectedLog.created_at).toLocaleString() : '-'}
              </Descriptions.Item>
            </Descriptions>

            <div style={{ marginBottom: 8, fontWeight: 500, fontSize: 13 }}>
              {t('auditLogs.changeDetails')}
            </div>
            {renderChanges(selectedLog)}
          </div>
        )}
      </Modal>
    </div>
  )
}

export default AuditLogs
