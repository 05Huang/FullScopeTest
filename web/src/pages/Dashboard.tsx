import { useState, useEffect } from 'react'
import { useTranslation } from 'react-i18next'
import { useNavigate } from 'react-router-dom'
import { Skeleton, Button, Modal, Checkbox, message, Space } from 'antd'
import api from '@/services/api'
import { reportService } from '@/services'
import type { DashboardStats, QualityTrendItem, ResponsePercentiles } from '@/services/reportService'
import { useProjectStore } from '@/stores/projectStore'
import {
  ApiOutlined,
  GlobalOutlined,
  ThunderboltOutlined,
  FileTextOutlined,
  ArrowUpOutlined,
  SettingOutlined,
} from '@ant-design/icons'
import DashboardWidgetGrid, { type WidgetConfig } from '@/components/widgets/DashboardWidgetGrid'

interface DailyTrend {
  date: string
  passed: number
  failed: number
}

const Dashboard = () => {
  const { t } = useTranslation()
  const navigate = useNavigate()
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

  // P26-3: 自定义仪表盘组件布局
  const [widgetModalOpen, setWidgetModalOpen] = useState(false)
  const [widgetTypes, setWidgetTypes] = useState<string[]>([])
  const [selectedWidgets, setSelectedWidgets] = useState<string[]>([])
  const [widgets, setWidgets] = useState<WidgetConfig[]>([])
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
      const data = res?.data?.data || res?.data || {}
      // API 返回的是字典对象，提取 key 作为类型列表
      if (data && typeof data === 'object' && !Array.isArray(data)) {
        setWidgetTypes(Object.keys(data))
      } else if (Array.isArray(data)) {
        setWidgetTypes(data.map((w: Record<string, unknown>) => (w.type || w.widget_type || w) as string))
      }
    } catch { /* 静默 */ }
  }

  // 获取当前用户的组件配置
  const fetchWidgets = async () => {
    try {
      const res = await api.get('/dashboard/widgets')
      const data = res?.data?.data || res?.data || []
      if (Array.isArray(data)) {
        setWidgets(data as WidgetConfig[])
        setSelectedWidgets(data.map((w: Record<string, unknown>) => (w.widget_type || w.type) as string))
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
      const res = await api.put('/dashboard/widgets', { widgets }) as { data?: { code?: number }; code?: number }
      if (res?.code === 200 || res?.data?.code === 200) {
        message.success(t('dashboard.widgetSaveSuccess') || '布局已保存')
        setWidgetModalOpen(false)
      }
    } catch {
      message.error(t('dashboard.widgetSaveFailed') || '保存失败')
    } finally {
      setWidgetLoading(false)
    }
  }

  // P26-3: 拖拽重排回调 — 保存新顺序到后端
  const handleWidgetReorder = async (reordered: WidgetConfig[]) => {
    setWidgets(reordered)
    setSelectedWidgets(reordered.map(w => w.widget_type))
    try {
      const payload = reordered.map((w, i) => ({
        widget_type: w.widget_type,
        title: w.title || w.widget_type,
        position_x: w.position_x || 0,
        position_y: i,
        width: w.width || 1,
        height: w.height || 1,
        config: w.config || {},
        is_visible: w.is_visible !== false,
      }))
      await api.put('/dashboard/widgets', { widgets: payload })
    } catch { /* 静默 */ }
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

  const statCards = [
    { label: t('dashboard.apiTestCases'), value: stats.api_tests.total.toLocaleString(), icon: <ApiOutlined style={{ fontSize: 20 }} />, iconClass: 'fst-stat-icon--primary', trend: `${getPassRate(stats.api_tests.passed, stats.api_tests.total)}%`, trendType: 'up' as const, navigateTo: '/api-test/workspace' },
    { label: t('dashboard.webTestScripts'), value: stats.web_tests.total.toLocaleString(), icon: <GlobalOutlined style={{ fontSize: 20 }} />, iconClass: 'fst-stat-icon--secondary', trend: `${getPassRate(stats.web_tests.passed, stats.web_tests.total)}%`, trendType: 'up' as const, navigateTo: '/web-test/scripts' },
    { label: t('dashboard.perfTestScenarios'), value: stats.perf_tests.total.toLocaleString(), icon: <ThunderboltOutlined style={{ fontSize: 20 }} />, iconClass: 'fst-stat-icon--tertiary', badge: `${t('dashboard.runningCount', { count: stats.perf_tests.running })}`, trendType: 'badge' as const, navigateTo: '/perf-test/scenarios' },
    { label: t('dashboard.recentTests'), value: stats.recent_runs.length.toLocaleString(), icon: <FileTextOutlined style={{ fontSize: 20 }} />, iconClass: 'fst-stat-icon--info', trend: t('dashboard.recentRuns'), trendType: 'info' as const, navigateTo: '/reports' },
  ]

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
          <div
            key={i}
            className="fst-stat-card"
            aria-label={`${card.label}: ${loading ? '加载中' : card.value}`}
            onClick={() => card.navigateTo && navigate(card.navigateTo)}
            style={{ cursor: card.navigateTo ? 'pointer' : 'default' }}
            role={card.navigateTo ? 'link' : undefined}
            tabIndex={card.navigateTo ? 0 : undefined}
            onKeyDown={(e) => { if (card.navigateTo && (e.key === 'Enter' || e.key === ' ')) { e.preventDefault(); navigate(card.navigateTo) } }}
          >
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

      {/* P26-3: 动态组件网格 — 根据用户选择的组件渲染，支持拖拽排列 */}
      <div className="fst-animate-in fst-animate-in-2" style={{ marginTop: 8 }}>
        <DashboardWidgetGrid
          widgets={widgets}
          data={{
            stats: stats as unknown as { api_tests: { total: number; passed: number; failed: number }; web_tests: { total: number; passed: number; failed: number }; perf_tests: { total: number; running: number }; recent_runs: Record<string, unknown>[] },
            dailyTrend: dailyTrend as unknown as Array<{ date: string; passed: number; failed: number }>,
            percentiles,
            qualityTrend: qualityTrend as unknown as Array<Record<string, unknown>>,
            loading,
          }}
          onReorder={handleWidgetReorder}
          onNavigate={(path) => navigate(path)}
        />
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
              'pass_rate', 'recent_runs', 'failed_top10', 'ai_usage',
              'team_activity', 'quality_gates', 'sla_rate', 'cost_overview', 'external_data',
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
