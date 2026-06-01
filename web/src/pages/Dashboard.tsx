import { useState, useEffect } from 'react'
import { useTranslation } from 'react-i18next'
import ReactECharts from 'echarts-for-react'
import { reportService } from '@/services'
import {
  ApiOutlined,
  GlobalOutlined,
  ThunderboltOutlined,
  FileTextOutlined,
  CheckCircleOutlined,
  CloseCircleOutlined,
  ClockCircleOutlined,
  ArrowUpOutlined,
} from '@ant-design/icons'

interface DashboardStats {
  api_tests: { total: number; passed: number; failed: number }
  web_tests: { total: number; passed: number; failed: number }
  perf_tests: { total: number; running: number }
  recent_runs: any[]
}

const Dashboard = () => {
  const { t } = useTranslation()
  const [loading, setLoading] = useState(true)
  const [stats, setStats] = useState<DashboardStats>({
    api_tests: { total: 0, passed: 0, failed: 0 },
    web_tests: { total: 0, passed: 0, failed: 0 },
    perf_tests: { total: 0, running: 0 },
    recent_runs: []
  })
  const [dailyTrend, setDailyTrend] = useState<any[]>([])

  useEffect(() => {
    fetchDashboardData()
  }, [])

  const fetchDashboardData = async () => {
    setLoading(true)
    try {
      const dashboardRes = await reportService.getDashboardStats()
      if (dashboardRes.code === 200) setStats(dashboardRes.data)
      const statsRes = await reportService.getReportStatistics({ days: 7 })
      if (statsRes.code === 200) setDailyTrend(statsRes.data.daily_trend || [])
    } catch { /* silent */ } finally { setLoading(false) }
  }

  const getPassRate = (passed: number, total: number) =>
    total > 0 ? Math.round((passed / total) * 100) : 0

  const trendOption = {
    tooltip: { trigger: 'axis' },
    legend: { data: [t('common.passed'), t('common.failed')], bottom: 0, textStyle: { fontSize: 12, color: '#7C8180' } },
    grid: { left: '3%', right: '4%', bottom: '15%', containLabel: true },
    xAxis: {
      type: 'category', boundaryGap: false,
      data: dailyTrend.length > 0 ? dailyTrend.map((d: any) => d.date) : ['周一', '周二', '周三', '周四', '周五', '周六', '周日'],
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
    <div className="fst-page">
      <div className="fst-page-header fst-animate-in">
        <h1 className="fst-page-title">{t('dashboard.title')}</h1>
      </div>

      <div id="tour-step-dashboard-api" className="fst-stat-row fst-animate-in fst-animate-in-1">
        {statCards.map((card, i) => (
          <div key={i} className="fst-stat-card">
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
              <div>
                <div className="fst-stat-label">{card.label}</div>
                <div className="fst-stat-value">{loading ? '—' : card.value}</div>
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
        <div className="fst-ios-card">
          <div className="fst-ios-card-header">
            <div>
              <div className="fst-ios-card-title">{t('dashboard.testTrend')}</div>
              <div className="fst-ios-card-subtitle">过去30天的自动化任务统计</div>
            </div>
            <div className="fst-tabs" style={{ width: 'auto' }}>
              <button className="fst-tab">周</button>
              <button className="fst-tab fst-tab--active">月</button>
            </div>
          </div>
          {loading
            ? <div style={{ height: 300, display: 'grid', placeItems: 'center', color: 'var(--fst-on-surface-muted)' }}>加载中...</div>
            : <ReactECharts option={trendOption} style={{ height: 300 }} />
          }
        </div>
        <div className="fst-ios-card">
          <div className="fst-ios-card-header" style={{ flexDirection: 'column', alignItems: 'flex-start', gap: 4 }}>
            <div className="fst-ios-card-title">{t('dashboard.testDistribution')}</div>
            <div className="fst-ios-card-subtitle">各端自动化覆盖比例</div>
          </div>
          {loading
            ? <div style={{ height: 300, display: 'grid', placeItems: 'center', color: 'var(--fst-on-surface-muted)' }}>加载中...</div>
            : <ReactECharts option={distributionOption} style={{ height: 300 }} />
          }
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
            <div className="fst-empty-desc">您最近尚未启动任何测试运行，开始您的第一次自动化测试吧。</div>
          </div>
        )}
      </div>
    </div>
  )
}

export default Dashboard
