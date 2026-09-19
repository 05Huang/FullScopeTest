/**
 * 访客统计页面
 *
 * 隐藏页面，展示网站访客的详细统计数据。
 * 访问路径: /hidden/visitor-stats
 * 需要管理员权限。
 */
import { useState, useEffect, useCallback } from 'react'
import {
  Card,
  Table,
  Row,
  Col,
  Statistic,
  Typography,
  Select,
  Space,
  Tag,
  message,
  Modal,
  Button,
} from 'antd'
import {
  UserOutlined,
  EyeOutlined,
  ClockCircleOutlined,
  GlobalOutlined,
  DesktopOutlined,
  MobileOutlined,
  TabletOutlined,
  ReloadOutlined,
  FireOutlined,
} from '@ant-design/icons'
import { useTranslation } from 'react-i18next'
import type { ColumnsType } from 'antd/es/table'
import ReactECharts from 'echarts-for-react'
import visitorStatsService, {
  VisitorStat,
  VisitorStatsOverview,
  TopPage,
  VisitorListParams,
} from '@/services/visitorStatsService'

const { Title, Text } = Typography

// 设备图标映射
const DeviceIcon: Record<string, React.ReactNode> = {
  desktop: <DesktopOutlined />,
  mobile: <MobileOutlined />,
  tablet: <TabletOutlined />,
}

// 设备颜色
const DeviceColors: Record<string, string> = {
  desktop: '#1890ff',
  mobile: '#52c41a',
  tablet: '#faad14',
}

const VisitorStats = () => {
  const { t } = useTranslation()
  const [overview, setOverview] = useState<VisitorStatsOverview | null>(null)
  const [visitors, setVisitors] = useState<VisitorStat[]>([])
  const [topPages, setTopPages] = useState<TopPage[]>([])
  const [total, setTotal] = useState(0)
  const [page, setPage] = useState(1)
  const [pageSize, setPageSize] = useState(20)
  const [loading, setLoading] = useState(false)
  const [statsDays, setStatsDays] = useState(7)
  const [filters, setFilters] = useState<VisitorListParams>({})
  const [selectedVisitor, setSelectedVisitor] = useState<VisitorStat | null>(null)
  const [detailModalOpen, setDetailModalOpen] = useState(false)

  // 获取统计概览
  const fetchOverview = useCallback(async () => {
    try {
      const res = await visitorStatsService.getVisitorStats(statsDays)
      if (res.code === 200 && res.data) {
        setOverview(res.data)
      }
    } catch {
      message.error(t('visitorStats.fetchFailed'))
    }
  }, [statsDays, t])

  // 获取访客列表
  const fetchVisitors = useCallback(async () => {
    setLoading(true)
    try {
      const res = await visitorStatsService.getVisitorList({
        page,
        per_page: pageSize,
        ...filters,
      })
      if (res.code === 200 && res.data) {
        setVisitors(res.data.items || [])
        setTotal(res.data.total || 0)
      }
    } catch {
      message.error(t('visitorStats.fetchFailed'))
    } finally {
      setLoading(false)
    }
  }, [page, pageSize, filters])

  // 获取页面排行
  const fetchTopPages = useCallback(async () => {
    try {
      const res = await visitorStatsService.getTopPages(statsDays, 10)
      if (res.code === 200 && res.data) {
        setTopPages(res.data)
      }
    } catch {
      message.error(t('visitorStats.fetchFailed'))
    }
  }, [statsDays])

  useEffect(() => {
    fetchOverview()
    fetchTopPages()
  }, [fetchOverview, fetchTopPages])

  useEffect(() => {
    fetchVisitors()
  }, [fetchVisitors])

  // 格式化时长
  const formatDuration = (seconds: number) => {
    if (seconds < 60) return `${seconds}s`
    if (seconds < 3600) return `${Math.floor(seconds / 60)}m ${seconds % 60}s`
    return `${Math.floor(seconds / 3600)}h ${Math.floor((seconds % 3600) / 60)}m`
  }

  // 格式化日期
  const formatDate = (isoString: string) => {
    const date = new Date(isoString)
    return date.toLocaleString('zh-CN', {
      month: '2-digit',
      day: '2-digit',
      hour: '2-digit',
      minute: '2-digit',
    })
  }

  // 访客列表列定义
  const visitorColumns: ColumnsType<VisitorStat> = [
    {
      title: t('visitorStats.columns.session'),
      dataIndex: 'session_id',
      key: 'session_id',
      width: 120,
      render: (id: string) => <Text code copyable={{ text: id }}>{id.slice(0, 8)}...</Text>,
    },
    {
      title: t('visitorStats.columns.location'),
      key: 'location',
      width: 150,
      render: (_, record) => (
        <Space direction="vertical" size={0}>
          <Text>{record.ip_country || 'Unknown'}</Text>
          <Text type="secondary" style={{ fontSize: 12 }}>{record.ip_city}</Text>
        </Space>
      ),
    },
    {
      title: t('visitorStats.columns.device'),
      key: 'device',
      width: 120,
      render: (_, record) => (
        <Space size="small">
          <Tag icon={DeviceIcon[record.device_type || 'desktop']} color={DeviceColors[record.device_type || 'desktop']}>
            {record.device_type || 'desktop'}
          </Tag>
          <Text type="secondary" style={{ fontSize: 12 }}>{record.browser}</Text>
        </Space>
      ),
    },
    {
      title: t('visitorStats.columns.os'),
      dataIndex: 'os',
      key: 'os',
      width: 100,
      render: (os: string) => os || 'Unknown',
    },
    {
      title: t('visitorStats.columns.pageViews'),
      dataIndex: 'page_views',
      key: 'page_views',
      width: 80,
      sorter: (a, b) => a.page_views - b.page_views,
      render: (views: number) => <Tag color="blue">{views}</Tag>,
    },
    {
      title: t('visitorStats.columns.duration'),
      dataIndex: 'total_duration',
      key: 'total_duration',
      width: 100,
      sorter: (a, b) => a.total_duration - b.total_duration,
      render: (duration: number) => formatDuration(duration),
    },
    {
      title: t('visitorStats.columns.entry'),
      dataIndex: 'entry_page',
      key: 'entry_page',
      width: 150,
      ellipsis: true,
      render: (path: string) => <Text code>{path || '/'}</Text>,
    },
    {
      title: t('visitorStats.columns.lastActive'),
      dataIndex: 'last_active',
      key: 'last_active',
      width: 140,
      sorter: (a, b) => new Date(b.last_active).getTime() - new Date(a.last_active).getTime(),
      render: (date: string) => formatDate(date),
    },
    {
      title: t('visitorStats.columns.actions'),
      key: 'actions',
      width: 80,
      render: (_, record) => (
        <Button type="link" size="small" onClick={() => {
          setSelectedVisitor(record)
          setDetailModalOpen(true)
        }}>
          {t('common.view')}
        </Button>
      ),
    },
  ]

  // 趋势图配置
  const trendOption = {
    title: { text: t('visitorStats.trendTitle'), left: 'center' },
    tooltip: { trigger: 'axis' },
    legend: { data: [t('visitorStats.visitors'), t('visitorStats.pageViews')], bottom: 0 },
    xAxis: {
      type: 'category',
      data: overview?.daily_trend.map(d => d.date) || [],
    },
    yAxis: [
      { type: 'value', name: t('visitorStats.visitors') },
      { type: 'value', name: t('visitorStats.pageViews') },
    ],
    series: [
      {
        name: t('visitorStats.visitors'),
        type: 'bar',
        data: overview?.daily_trend.map(d => d.visitors) || [],
        itemStyle: { color: '#1890ff' },
      },
      {
        name: t('visitorStats.pageViews'),
        type: 'line',
        yAxisIndex: 1,
        data: overview?.daily_trend.map(d => d.page_views) || [],
        itemStyle: { color: '#52c41a' },
        smooth: true,
      },
    ],
  }

  // 设备分布图配置
  const deviceOption = {
    title: { text: t('visitorStats.deviceTitle'), left: 'center' },
    tooltip: { trigger: 'item' },
    legend: { bottom: 0 },
    series: [{
      type: 'pie',
      radius: ['40%', '70%'],
      data: Object.entries(overview?.by_device || {}).map(([name, value]) => ({
        name,
        value,
        itemStyle: { color: DeviceColors[name] || '#999' },
      })),
    }],
  }

  // 浏览器分布图配置
  const browserOption = {
    title: { text: t('visitorStats.browserTitle'), left: 'center' },
    tooltip: { trigger: 'item' },
    legend: { bottom: 0 },
    series: [{
      type: 'pie',
      radius: ['40%', '70%'],
      data: Object.entries(overview?.by_browser || {}).map(([name, value]) => ({
        name,
        value,
      })),
    }],
  }

  // 国家分布图配置
  const countryOption = {
    title: { text: t('visitorStats.countryTitle'), left: 'center' },
    tooltip: { trigger: 'axis' },
    xAxis: { type: 'value' },
    yAxis: {
      type: 'category',
      data: Object.keys(overview?.by_country || {}).slice(0, 10).reverse(),
    },
    series: [{
      type: 'bar',
      data: Object.values(overview?.by_country || {}).slice(0, 10).reverse(),
      itemStyle: { color: '#722ed1' },
    }],
  }

  return (
    <div className="fst-page" role="main" aria-label={t('visitorStats.title')}>
      {/* 页面头部 */}
      <div className="fst-page-header fst-animate-in">
        <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
          <GlobalOutlined style={{ fontSize: 20, color: 'var(--fst-primary)' }} />
          <h1 className="fst-page-title">{t('visitorStats.title')}</h1>
        </div>
        <Text type="secondary">{t('visitorStats.subtitle')}</Text>
      </div>

      {/* 概览统计卡片 */}
      <div className="fst-stat-row fst-animate-in fst-animate-in-1" style={{ marginTop: 16 }}>
        <div className="fst-stat-card">
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
            <div>
              <div className="fst-stat-label">{t('visitorStats.totalVisitors')}</div>
              <div className="fst-stat-value">
                {loading ? '—' : (overview?.total_visitors || 0)}
              </div>
            </div>
            <div className="fst-stat-icon fst-stat-icon--primary">
              <UserOutlined style={{ fontSize: 20 }} />
            </div>
          </div>
          <div style={{ marginTop: 'auto', paddingTop: 4 }}>
            <span className="fst-stat-trend" style={{ color: 'var(--fst-on-surface-muted)', background: 'var(--fst-surface-dim)' }}>
              / {statsDays}d
            </span>
          </div>
        </div>

        <div className="fst-stat-card">
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
            <div>
              <div className="fst-stat-label">{t('visitorStats.todayVisitors')}</div>
              <div className="fst-stat-value" style={{ color: '#f5222d' }}>
                {loading ? '—' : (overview?.today_visitors || 0)}
              </div>
            </div>
            <div className="fst-stat-icon fst-stat-icon--danger">
              <FireOutlined style={{ fontSize: 20 }} />
            </div>
          </div>
        </div>

        <div className="fst-stat-card">
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
            <div>
              <div className="fst-stat-label">{t('visitorStats.onlineVisitors')}</div>
              <div className="fst-stat-value" style={{ color: '#52c41a' }}>
                {loading ? '—' : (overview?.online_visitors || 0)}
              </div>
            </div>
            <div className="fst-stat-icon fst-stat-icon--success">
              <EyeOutlined style={{ fontSize: 20 }} />
            </div>
          </div>
        </div>

        <div className="fst-stat-card">
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
            <div>
              <div className="fst-stat-label">{t('visitorStats.avgDuration')}</div>
              <div className="fst-stat-value">
                {loading ? '—' : formatDuration(overview?.avg_duration || 0)}
              </div>
            </div>
            <div className="fst-stat-icon fst-stat-icon--info">
              <ClockCircleOutlined style={{ fontSize: 20 }} />
            </div>
          </div>
        </div>
      </div>

      {/* 趋势图和分布图 */}
      <Row gutter={16} style={{ marginTop: 16 }} className="fst-animate-in fst-animate-in-2">
        <Col span={12}>
          <Card className="fst-card">
            <ReactECharts option={trendOption} style={{ height: 280 }} />
          </Card>
        </Col>
        <Col span={12}>
          <Row gutter={16}>
            <Col span={12}>
              <Card className="fst-card fst-card--small">
                <ReactECharts option={deviceOption} style={{ height: 130 }} />
              </Card>
            </Col>
            <Col span={12}>
              <Card className="fst-card fst-card--small">
                <ReactECharts option={browserOption} style={{ height: 130 }} />
              </Card>
            </Col>
          </Row>
        </Col>
      </Row>

      {/* 页面排行和地区分布 */}
      <Row gutter={16} style={{ marginTop: 16 }} className="fst-animate-in fst-animate-in-3">
        <Col span={12}>
          <Card className="fst-card" title={t('visitorStats.topPages')}>
            {topPages.length === 0 ? (
              <div style={{ textAlign: 'center', padding: '40px 0', color: 'var(--fst-on-surface-muted)' }}>
                {t('visitorStats.noData')}
              </div>
            ) : (
              topPages.map((p, i) => (
                <div key={p.path} style={{ display: 'flex', alignItems: 'center', marginBottom: 8 }}>
                  <Text strong style={{ width: 24 }}>{i + 1}</Text>
                  <Text code style={{ flex: 1 }} ellipsis>{p.path}</Text>
                  <Text type="secondary">{p.views} {t('visitorStats.views')}</Text>
                </div>
              ))
            )}
          </Card>
        </Col>
        <Col span={12}>
          <Card className="fst-card">
            <ReactECharts option={countryOption} style={{ height: 180 }} />
          </Card>
        </Col>
      </Row>

      {/* 访客列表 */}
      <Card
        className="fst-card"
        style={{ marginTop: 16 }}
        title={t('visitorStats.visitorList')}
        extra={
          <Space size="small">
            <Select
              placeholder={t('visitorStats.filterDevice')}
              style={{ width: 110 }}
              allowClear
              size="small"
              onChange={(v) => setFilters({ ...filters, device_type: v })}
            >
              <Select.Option value="desktop">{t('visitorStats.deviceDesktop')}</Select.Option>
              <Select.Option value="mobile">{t('visitorStats.deviceMobile')}</Select.Option>
              <Select.Option value="tablet">{t('visitorStats.deviceTablet')}</Select.Option>
            </Select>
            <Select
              placeholder={t('visitorStats.filterCountry')}
              style={{ width: 110 }}
              allowClear
              size="small"
              onChange={(v) => setFilters({ ...filters, country: v })}
              options={Object.entries(overview?.by_country || {}).map(([k, v]) => ({
                label: `${k} (${v})`,
                value: k,
              }))}
            />
            <Button icon={<ReloadOutlined />} size="small" onClick={() => { fetchOverview(); fetchVisitors(); fetchTopPages(); }}>
              {t('common.refresh')}
            </Button>
          </Space>
        }
      >
        <Table
          columns={visitorColumns}
          dataSource={visitors}
          rowKey="id"
          loading={loading}
          size="small"
          pagination={{
            current: page,
            pageSize,
            total,
            showSizeChanger: true,
            showTotal: (total) => `${t('common.total')}: ${total}`,
            onChange: (p, ps) => {
              setPage(p)
              setPageSize(ps)
            },
          }}
        />
      </Card>

      {/* 访客详情弹窗 */}
      <Modal
        title={t('visitorStats.visitorDetail')}
        open={detailModalOpen}
        onCancel={() => setDetailModalOpen(false)}
        footer={null}
        width={650}
      >
        {selectedVisitor && (
          <Row gutter={[16, 16]}>
            <Col span={12}>
              <Text type="secondary">{t('visitorStats.columns.session')}</Text>
              <div><Text code copyable>{selectedVisitor.session_id}</Text></div>
            </Col>
            <Col span={12}>
              <Text type="secondary">{t('visitorStats.columns.location')}</Text>
              <div>{selectedVisitor.ip_country} {selectedVisitor.ip_city}</div>
            </Col>
            <Col span={12}>
              <Text type="secondary">{t('visitorStats.columns.device')}</Text>
              <div>
                <Tag color={DeviceColors[selectedVisitor.device_type || 'desktop']}>
                  {selectedVisitor.device_type}
                </Tag>
                {selectedVisitor.browser} {selectedVisitor.browser_version}
              </div>
            </Col>
            <Col span={12}>
              <Text type="secondary">{t('visitorStats.columns.os')}</Text>
              <div>{selectedVisitor.os} {selectedVisitor.os_version}</div>
            </Col>
            <Col span={12}>
              <Text type="secondary">{t('visitorStats.columns.screen')}</Text>
              <div>{selectedVisitor.screen_width} x {selectedVisitor.screen_height}</div>
            </Col>
            <Col span={12}>
              <Text type="secondary">{t('visitorStats.columns.referrer')}</Text>
              <div><Text ellipsis>{selectedVisitor.referrer || '-'}</Text></div>
            </Col>
            <Col span={24}>
              <Text type="secondary">{t('visitorStats.visitedPages')}</Text>
              <div style={{ marginTop: 8 }}>
                {selectedVisitor.visited_pages?.map((p, i) => (
                  <Tag key={i} style={{ marginBottom: 4 }}>
                    {p.path} ({formatDuration(p.duration)}, {p.visits} {t('visitorStats.visits')})
                  </Tag>
                ))}
              </div>
            </Col>
          </Row>
        )}
      </Modal>
    </div>
  )
}

export default VisitorStats
