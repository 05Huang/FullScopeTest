import { useState, useEffect } from 'react'
import { useTranslation } from 'react-i18next'
import { Skeleton, Tooltip, Button, Modal, Checkbox, message, Space } from 'antd'
import ReactECharts from 'echarts-for-react'
import api from '@/services/api'
import { reportService } from '@/services'
import type { DashboardStats, QualityTrendItem, ResponsePercentiles } from '@/services/reportService'
import { useProjectStore } from '@/stores/projectStore'
import {
  ApiOutlined,
  GlobalOutlined,
  ThunderboltOutlined,
  FileTextOutlined,
  CheckCircleOutlined,
  CloseCircleOutlined,
  ClockCircleOutlined,
  ArrowUpOutlined,
  ArrowDownOutlined,
  FieldTimeOutlined,
  SettingOutlined,
} from '@ant-design/icons'

interface DailyTrend {
  date: string
  passed: number
  failed: number
}

const Dashboard = () => {
  const { t } = useTranslation()
  const { currentProjectId } = useProjectStore()
  const [loading, setLoading] = useState(true)
  const [stats, setStats] = useState<DashboardStats>({
    api_tests: { total: 0, passed: 0, failed: 0 },
    web_tests: { total: 0, passed: 0, failed: 0 },
    perf_tests: { total: 0, running: 0 },
    recent_runs: []
  })
  const [dailyTrend, setDailyTrend] = useState<DailyTrend[]>([])
  const [trendPeriod, setTrendPeriod] = useState<'week' | 'month'>('month')
  const trendDays = trendPeriod === 'week' ? 7 : 30

  // P31-2: 响应时间分位数与质量趋势
  const [percentiles, setPercentiles] = useState<ResponsePercentiles | null>(null)
  const [qualityTrend, setQualityTrend] = useState<QualityTrendItem[]>([])
  const [qualityDays, setQualityDays] = useState(30)

  // P32-2: 自定义仪表盘组件布局
  const [widgetModalOpen, setWidgetModalOpen] = useState(false)
  const [widgetTypes, setWidgetTypes] = useState<string[]>([])
  const [selectedWidgets, setSelectedWidgets] = useState<string[]>([])
  const [widgetLoading, setWidgetLoading] = useState(false)

  useEffect(() => {
    fetchDashboardData()
  }, [currentProjectId])

  useEffect(() => {
    fetchTrend()
  }, [trendPeriod])

  useEffect(() => {
    fetchQualityTrend()
  }, [qualityDays, currentProjectId])

  useEffect(() => {
    fetchPercentiles()
  }, [currentProjectId])

  useEffect(() => {
    fetchWidgetTypes()
    fetchWidgets()
  }, [])

  const fetchDashboardData = async () => {
    setLoading(true)
    try {
      const dashboardRes = await reportService.getDashboardStats(currentProjectId)
      if (dashboardRes.code === 200) setStats(dashboardRes.data)
      await fetchTrend()
    } catch { /* silent */ } finally { setLoading(false) }
  }

  const fetchTrend = async () => {
    try {
      const statsRes = await reportService.getReportStatistics({ days: trendDays, project_id: currentProjectId })
      if (statsRes.code === 200) setDailyTrend(statsRes.data.daily_trend || [])
    } catch { /* silent */ }
  }

  const fetchPercentiles = async () => {
    try {
      const res = await reportService.getResponsePercentiles({ project_id: currentProjectId, days: 7 })
      if (res.code === 200) setPercentiles(res.data)
    } catch { /* silent */ }
  }

  const fetchQualityTrend = async () => {
    try {
      const res = await reportService.getQualityTrend({ project_id: currentProjectId, days: qualityDays, granularity: 'week' })
      if (res.code === 200) setQualityTrend(res.data || [])
    } catch { /* silent */ }
  }

  // P32-2: 获取组件类型列表
  const fetchWidgetTypes = async () => {
    try {
      const res = await api.get('/dashboard/widget-types')
      const data = (res as any)?.data?.data || (res as any)?.data || []
      if (Array.isArray(data)) {
        setWidgetTypes(data.map((w: any) => w.type || w.widget_type || w))
      }
    } catch { /* 静默 */ }
  }

  // 获取当前用户的组件配置
  const fetchWidgets = async () => {
    try {
      const res = await api.get('/dashboard/widgets')
      const data = (res as any)?.data?.data || (res as any)?.data || []
      if (Array.isArray(data)) {
        setSelectedWidgets(data.map((w: any) => w.widget_type || w.type))
      }
    } catch { /* 静默 */ }
  }

  // 保存组件布局
  const handleSaveWidgets = async () => {
    setWidgetLoading(true)
    try {
      const widgets = selectedWidgets.map((type, index) => ({
        widget_type: type,
        title: type,
        position_x: 0,
        position_y: index,
        width: 1,
        height: 1,
        config: {},
      }))
      const res = await api.put('/dashboard/widgets', { widgets })
      if ((res as any).code === 200 || (res as any).data?.code === 200) {
        message.success(t('dashboard.widgetSaveSuccess') || '布局已保存')
        setWidgetModalOpen(false)
      }
    } catch {
      message.error(t('dashboard.widgetSaveFailed') || '保存失败')
    } finally {
      setWidgetLoading(false)
    }
  }

  // 重置为默认布局
  const handleResetWidgets = async () => {
    try {
      await api.post('/dashboard/widgets/reset')
      message.success(t('dashboard.widgetResetSuccess') || '已恢复默认布局')
      fetchWidgets()
      setWidgetModalOpen(false)
    } catch {
      message.error(t('common.failed') || '重置失败')
    }
  }

  const getPassRate = (passed: number, total: number) =>
    total > 0 ? Math.round((passed / total) * 100) : 0

  const trendOption = {
    tooltip: { trigger: 'axis' },
    legend: { data: [t('common.passed'), t('common.failed')], bottom: 0, textStyle: { fontSize: 12, color: '#7C8180' } },
    grid: { left: '3%', right: '4%', bottom: '15%', containLabel: true },
    xAxis: {
      type: 'category', boundaryGap: false,
      data: dailyTrend.length > 0 ? dailyTrend.map((d: any) => d.date) : [t('dashboard.weekdays.mon'), t('dashboard.weekdays.tue'), t('dashboard.weekdays.wed'), t('dashboard.weekdays.thu'), t('dashboard.weekdays.fri'), t('dashboard.weekdays.sat'), t('dashboard.weekdays.sun')],
      axisLine: { lineStyle: { color: '#E8E8E8' } }, axisLabel: { color: '#7C8180', fontSize: 11 },
    },
    yAxis: { type: 'value', axisLine: { show: false }, splitLine: { lineStyle: { color: '#F0F0F0' } }, axisLabel: { color: '#7C8180', fontSize: 11 } },
    series: [
      {
        name: t('common.passed'), type: 'line', smooth: true, symbol: 'circle', symbolSize: 6,
        areaStyle: { color: { type: 'linear', x: 0, y: 0, x2: 0, y2: 1, colorStops: [{ offset: 0, color: 'rgba(45,106,100,0.25)' }, { offset: 1, color: 'rgba(45,106,100,0.02)' }] } },
        data: dailyTrend.length > 0 ? dailyTrend.map((d: any) => d.passed) : [0, 0, 0, 0, 0, 0, 0],
        itemStyle: { color: '#2D6A64' }, lineStyle: { width: 2.5 },
      },
      {
        name: t('common.failed'), type: 'line', smooth: true, symbol: 'circle', symbolSize: 6,
        areaStyle: { color: { type: 'linear', x: 0, y: 0, x2: 0, y2: 1, colorStops: [{ offset: 0, color: 'rgba(199,84,80,0.15)' }, { offset: 1, color: 'rgba(199,84,80,0.02)' }] } },
        data: dailyTrend.length > 0 ? dailyTrend.map((d: any) => d.failed) : [0, 0, 0, 0, 0, 0, 0],
        itemStyle: { color: '#C75450' }, lineStyle: { width: 2.5 },
      },
    ],
  }

  const distributionOption = {
    tooltip: { trigger: 'item', backgroundColor: 'rgba(255,255,255,0.96)', borderColor: '#E8E8E8', borderRadius: 12, textStyle: { fontSize: 13 } },
    legend: { bottom: 0, textStyle: { fontSize: 12, color: '#7C8180' } },
    series: [{
      type: 'pie', radius: ['42%', '72%'], center: ['50%', '45%'],
      avoidLabelOverlap: false, itemStyle: { borderRadius: 10, borderColor: '#fff', borderWidth: 3 }, label: { show: false },
      data: [
        { value: stats.api_tests.total || 0, name: t('dashboard.apiTest'), itemStyle: { color: '#2D6A64' } },
        { value: stats.web_tests.total || 0, name: t('dashboard.webTest'), itemStyle: { color: '#629B95' } },
        { value: stats.perf_tests.total || 0, name: t('dashboard.perfTest'), itemStyle: { color: '#D4B483' } },
      ],
    }],
  }

  // P31-2: 质量趋势图选项（调用 /reports/trend 接口）
  const qualityTrendOption = {
    tooltip: { trigger: 'axis' },
    legend: { data: [t('dashboard.qualityTrendModules.api') || 'API', t('dashboard.qualityTrendModules.web') || 'Web', t('dashboard.qualityTrendModules.perf') || '性能'], bottom: 0, textStyle: { fontSize: 12, color: '#7C8180' } },
    grid: { left: '3%', right: '4%', bottom: '15%', containLabel: true },
    xAxis: {
      type: 'category', boundaryGap: false,
      data: qualityTrend.map(d => d.date),
      axisLine: { lineStyle: { color: '#E8E8E8' } }, axisLabel: { color: '#7C8180', fontSize: 11 },
    },
    yAxis: { type: 'value', axisLine: { show: false }, splitLine: { lineStyle: { color: '#F0F0F0' } }, axisLabel: { color: '#7C8180', fontSize: 11 } },
    series: [
      { name: 'API', type: 'line', smooth: true, symbol: 'circle', symbolSize: 6, data: qualityTrend.map(d => d.api || 0), itemStyle: { color: '#2D6A64' }, lineStyle: { width: 2 } },
      { name: 'Web', type: 'line', smooth: true, symbol: 'circle', symbolSize: 6, data: qualityTrend.map(d => d.web || 0), itemStyle: { color: '#629B95' }, lineStyle: { width: 2 } },
      { name: '性能', type: 'line', smooth: true, symbol: 'circle', symbolSize: 6, data: qualityTrend.map(d => d.perf || 0), itemStyle: { color: '#D4B483' }, lineStyle: { width: 2 } },
    ],
  }

  const formatTime = (dateStr: string) => {
    if (!dateStr) return '-'
    const diff = Date.now() - new Date(dateStr).getTime()
    const m = Math.floor(diff / 60000), h = Math.floor(diff / 3600000), d = Math.floor(diff / 86400000)
    if (m < 1) return t('dashboard.time.justNow')
    if (m < 60) return t('dashboard.time.minutesAgo', { minutes: m })
    if (h < 24) return t('dashboard.time.hoursAgo', { hours: h })
    if (d < 7) return t('dashboard.time.daysAgo', { days: d })
    return new Date(dateStr).toLocaleDateString()
  }

  const statCards = [
    { label: t('dashboard.apiTestCases'), value: stats.api_tests.total.toLocaleString(), icon: <ApiOutlined style={{ fontSize: 20 }} />, iconClass: 'fst-stat-icon--primary', trend: `${getPassRate(stats.api_tests.passed, stats.api_tests.total)}%`, trendType: 'up' as const },
    { label: t('dashboard.webTestScripts'), value: stats.web_tests.total.toLocaleString(), icon: <GlobalOutlined style={{ fontSize: 20 }} />, iconClass: 'fst-stat-icon--secondary', trend: `${getPassRate(stats.web_tests.passed, stats.web_tests.total)}%`, trendType: 'up' as const },
    { label: t('dashboard.perfTestScenarios'), value: stats.perf_tests.total.toLocaleString(), icon: <ThunderboltOutlined style={{ fontSize: 20 }} />, iconClass: 'fst-stat-icon--tertiary', badge: `${t('dashboard.runningCount', { count: stats.perf_tests.running })}`, trendType: 'badge' as const },
    { label: t('dashboard.recentTests'), value: stats.recent_runs.length.toLocaleString(), icon: <FileTextOutlined style={{ fontSize: 20 }} />, iconClass: 'fst-stat-icon--info', trend: t('dashboard.recentRuns'), trendType: 'info' as const },
  ]

  const statusConfig: Record<string, { cls: string; icon: React.ReactNode; text: string }> = {
    success: { cls: 'fst-badge--success', icon: <CheckCircleOutlined />, text: t('common.success') },
    passed: { cls: 'fst-badge--success', icon: <CheckCircleOutlined />, text: t('common.passed') },
    failed: { cls: 'fst-badge--error', icon: <CloseCircleOutlined />, text: t('common.failed') },
    running: { cls: 'fst-badge--primary', icon: <ClockCircleOutlined />, text: t('common.running') },
    pending: { cls: 'fst-badge--warning', icon: <ClockCircleOutlined />, text: t('common.pending') },
  }

  const typeColors: Record<string, string> = { api: '#2D6A64', web: '#629B95', performance: '#D4B483', perf: '#D4B483' }
  const typeLabels: Record<string, string> = { api: 'API', web: 'Web', performance: t('dashboard.perfTest'), perf: t('dashboard.perfTest') }

  return (
    <div className="fst-page" role="main" aria-label={t('dashboard.title')}>
      <div className="fst-page-header fst-animate-in" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <h1 className="fst-page-title">{t('dashboard.title')}</h1>
        <Button icon={<SettingOutlined />} onClick={() => { fetchWidgetTypes(); fetchWidgets(); setWidgetModalOpen(true) }}>
          {t('dashboard.customizeLayout') || '自定义布局'}
        </Button>
      </div>

      <div id="tour-step-dashboard-api" className="fst-stat-row fst-animate-in fst-animate-in-1"
           role="region" aria-label={t('dashboard.title') + ' - 统计概览'} aria-live="polite">
        {statCards.map((card, i) => (
          <div key={i} className="fst-stat-card" aria-label={`${card.label}: ${loading ? '加载中' : card.value}`}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
              <div>
                <div className="fst-stat-label">{card.label}</div>
                <div className="fst-stat-value">{loading ? <Skeleton.Input active size="small" style={{ width: 60, height: 28 }} /> : card.value}</div>
              </div>
              <div className={`fst-stat-icon ${card.iconClass}`}>{card.icon}</div>
            </div>
            <div style={{ marginTop: 'auto', paddingTop: 4 }}>
              {card.trendType === 'up' && <span className="fst-stat-trend fst-stat-trend--up"><ArrowUpOutlined /> {card.trend}</span>}
              {card.trendType === 'badge' && <span className="fst-badge fst-badge--primary">{card.badge}</span>}
              {card.trendType === 'info' && <span className="fst-stat-trend" style={{ color: 'var(--fst-on-surface-muted)', background: 'var(--fst-surface-dim)' }}>{card.trend}</span>}
            </div>
          </div>
        ))}
      </div>

      <div className="fst-grid fst-animate-in fst-animate-in-2" style={{ gridTemplateColumns: '2fr 1fr' }}>
        <div className="fst-ios-card" role="region" aria-label={t('dashboard.testTrend')}>
          <div className="fst-ios-card-header">
            <div>
              <div className="fst-ios-card-title">{t('dashboard.testTrend')}</div>
              <div className="fst-ios-card-subtitle">{t('dashboard.trendSubtitle')}</div>
            </div>
            <div className="fst-tabs" style={{ width: 'auto' }}>
              <button
                className={`fst-tab ${trendPeriod === 'week' ? 'fst-tab--active' : ''}`}
                onClick={() => setTrendPeriod('week')}
              >
                {t('dashboard.week')}
              </button>
              <button
                className={`fst-tab ${trendPeriod === 'month' ? 'fst-tab--active' : ''}`}
                onClick={() => setTrendPeriod('month')}
              >
                {t('dashboard.month')}
              </button>
            </div>
          </div>
          {loading
            ? <Skeleton active paragraph={{ rows: 8 }} />
            : <ReactECharts option={trendOption} style={{ height: 300 }} />
          }
        </div>
        <div className="fst-ios-card">
          <div className="fst-ios-card-header" style={{ flexDirection: 'column', alignItems: 'flex-start', gap: 4 }}>
            <div className="fst-ios-card-title">{t('dashboard.testDistribution')}</div>
            <div className="fst-ios-card-subtitle">{t('dashboard.distributionSubtitle')}</div>
          </div>
          {loading
            ? <Skeleton active paragraph={{ rows: 8 }} />
            : <ReactECharts option={distributionOption} style={{ height: 300 }} />
          }
        </div>
      </div>

      {/* P31-2: 响应时间分位数 + 质量趋势 */}
      <div className="fst-grid fst-animate-in fst-animate-in-2" style={{ gridTemplateColumns: '1fr 2fr' }}>
        {/* 响应时间分位数卡片 */}
        <div className="fst-ios-card">
          <div className="fst-ios-card-header" style={{ flexDirection: 'column', alignItems: 'flex-start', gap: 4 }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
              <FieldTimeOutlined style={{ color: 'var(--fst-primary, #2D6A64)' }} />
              <div className="fst-ios-card-title">{t('dashboard.percentiles') || '响应时间分位数'}</div>
            </div>
            <div className="fst-ios-card-subtitle">{t('dashboard.percentilesSubtitle') || '近 7 天 API 测试 P50/P90/P95/P99'}</div>
          </div>
          {loading ? (
            <Skeleton active paragraph={{ rows: 4 }} />
          ) : percentiles && percentiles.total_requests > 0 ? (
            <div style={{ padding: '8px 0' }}>
              {[
                { label: 'P50', value: percentiles.p50, color: '#52c41a' },
                { label: 'P90', value: percentiles.p90, color: '#2D6A64' },
                { label: 'P95', value: percentiles.p95, color: percentiles.p95 > 2000 ? '#faad14' : '#2D6A64' },
                { label: 'P99', value: percentiles.p99, color: percentiles.p99 > 5000 ? '#ff4d4f' : percentiles.p99 > 2000 ? '#faad14' : '#2D6A64' },
              ].map((item) => (
                <div key={item.label} style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', padding: '10px 0', borderBottom: '1px solid var(--fst-outline-soft, #f0f0f0)' }}>
                  <span style={{ fontWeight: 600, fontSize: 13, color: 'var(--fst-on-surface-variant, #666)' }}>{item.label}</span>
                  <span style={{ fontWeight: 700, fontSize: 16, color: item.color, fontVariantNumeric: 'tabular-nums' }}>
                    {item.value >= 1000 ? `${(item.value / 1000).toFixed(2)}s` : `${item.value.toFixed(0)}ms`}
                  </span>
                </div>
              ))}
              <div style={{ marginTop: 12, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <span style={{ fontSize: 12, color: 'var(--fst-on-surface-muted, #999)' }}>
                  {t('dashboard.totalRequests') || '总请求数'}: {percentiles.total_requests.toLocaleString()}
                </span>
                <span style={{ fontSize: 12, color: 'var(--fst-on-surface-muted, #999)' }}>
                  {t('dashboard.avgLatency') || '平均'}: {percentiles.avg >= 1000 ? `${(percentiles.avg / 1000).toFixed(2)}s` : `${percentiles.avg.toFixed(0)}ms`}
                </span>
              </div>
            </div>
          ) : (
            <div className="fst-empty" style={{ padding: '30px 0' }}>
              <div className="fst-empty-icon"><FieldTimeOutlined /></div>
              <div className="fst-empty-title">{t('dashboard.noPercentileData') || '暂无响应时间数据'}</div>
              <div className="fst-empty-desc">{t('dashboard.noPercentileDataDesc') || '运行 API 测试后可查看分位数统计'}</div>
            </div>
          )}
        </div>

        {/* 质量趋势图 */}
        <div className="fst-ios-card" role="region" aria-label={t('dashboard.qualityTrend') || '质量趋势'}>
          <div className="fst-ios-card-header">
            <div>
              <div className="fst-ios-card-title">{t('dashboard.qualityTrend') || '质量趋势'}</div>
              <div className="fst-ios-card-subtitle">{t('dashboard.qualityTrendSubtitle') || '按模块统计用例通过数量趋势'}</div>
            </div>
            <div className="fst-tabs" style={{ width: 'auto' }}>
              <button className={`fst-tab ${qualityDays === 7 ? 'fst-tab--active' : ''}`} onClick={() => setQualityDays(7)}>
                {t('dashboard.week') || '7天'}
              </button>
              <button className={`fst-tab ${qualityDays === 30 ? 'fst-tab--active' : ''}`} onClick={() => setQualityDays(30)}>
                {t('dashboard.month') || '30天'}
              </button>
              <button className={`fst-tab ${qualityDays === 90 ? 'fst-tab--active' : ''}`} onClick={() => setQualityDays(90)}>
                {t('dashboard.quarter') || '90天'}
              </button>
            </div>
          </div>
          {loading ? (
            <Skeleton active paragraph={{ rows: 8 }} />
          ) : qualityTrend.length > 0 ? (
            <ReactECharts option={qualityTrendOption} style={{ height: 300 }} />
          ) : (
            <div className="fst-empty" style={{ padding: '60px 0' }}>
              <div className="fst-empty-title">{t('dashboard.noQualityTrendData') || '暂无质量趋势数据'}</div>
              <div className="fst-empty-desc">{t('dashboard.noQualityTrendDataDesc') || '运行测试后自动展示趋势图'}</div>
            </div>
          )}
        </div>
      </div>

      <div className="fst-ios-card fst-animate-in fst-animate-in-3" style={{ overflow: 'hidden' }}>
        <div className="fst-ios-card-header">
          <div className="fst-ios-card-title">{t('dashboard.recentExecutions')}</div>
        </div>
        {stats.recent_runs.length > 0 ? (
          <div style={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
            {stats.recent_runs.map((item: any, idx: number) => {
              const st = statusConfig[item.status] || { cls: '', icon: null, text: item.status }
              const color = typeColors[item.test_type] || '#999'
              return (
                <div key={idx} style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', padding: '14px 16px', borderRadius: 12, transition: 'background 150ms ease' }}
                  onMouseEnter={e => e.currentTarget.style.background = 'var(--fst-surface-dim)'}
                  onMouseLeave={e => e.currentTarget.style.background = 'transparent'}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: 12, minWidth: 0 }}>
                    <span style={{ width: 8, height: 8, borderRadius: '50%', background: color, flexShrink: 0 }} />
                    <div style={{ minWidth: 0 }}>
                      <div style={{ fontWeight: 600, fontSize: 14, color: 'var(--fst-on-surface)', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
                        {item.test_object_name || `Test #${item.id}`}
                      </div>
                      <div style={{ fontSize: 12, color: 'var(--fst-on-surface-muted)' }}>
                        {typeLabels[item.test_type] || item.test_type} · {formatTime(item.created_at)}
                      </div>
                    </div>
                  </div>
                  <span className={`fst-badge ${st.cls}`} style={{ flexShrink: 0 }}>{st.icon} {st.text}</span>
                </div>
              )
            })}
          </div>
        ) : (
          <div className="fst-empty">
            <div className="fst-empty-icon"><ClockCircleOutlined /></div>
            <div className="fst-empty-title">{t('dashboard.noRecords')}</div>
            <div className="fst-empty-desc">{t('dashboard.noRecordsDesc')}</div>
          </div>
        )}
      </div>
      {/* P32-2: 自定义仪表盘组件布局弹窗 */}
      <Modal
        title={t('dashboard.customizeLayout') || '自定义仪表盘布局'}
        open={widgetModalOpen}
        onCancel={() => setWidgetModalOpen(false)}
        onOk={handleSaveWidgets}
        confirmLoading={widgetLoading}
        okText={t('common.save') || '保存'}
        cancelText={t('common.cancel') || '取消'}
        footer={
          <div style={{ display: 'flex', justifyContent: 'space-between' }}>
            <Button onClick={handleResetWidgets}>{t('dashboard.resetLayout') || '恢复默认'}</Button>
            <Space>
              <Button onClick={() => setWidgetModalOpen(false)}>{t('common.cancel') || '取消'}</Button>
              <Button type="primary" onClick={handleSaveWidgets} loading={widgetLoading}>{t('common.save') || '保存'}</Button>
            </Space>
          </div>
        }
      >
        <div style={{ padding: '8px 0' }}>
          <div style={{ marginBottom: 12, fontSize: 13, color: 'var(--fst-on-surface-muted, #999)' }}>
            {t('dashboard.selectWidgets') || '选择要在仪表盘中显示的组件：'}
          </div>
          <Checkbox.Group
            value={selectedWidgets}
            onChange={(values) => setSelectedWidgets(values as string[])}
            style={{ display: 'flex', flexDirection: 'column', gap: 8 }}
          >
            {(widgetTypes.length > 0 ? widgetTypes : [
              'pass_rate', 'recent_runs', 'top_failures', 'ai_usage',
              'team_activity', 'quality_gate', 'sla', 'cost_overview',
            ]).map((type) => (
              <Checkbox key={type} value={type} style={{ marginLeft: 0 }}>
                {t('dashboard.widgetType.' + type) || type.replace(/_/g, ' ')}
              </Checkbox>
            ))}
          </Checkbox.Group>
        </div>
      </Modal>
    </div>
  )
}

export default Dashboard
