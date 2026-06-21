/**
 * 仪表盘组件网格 — 支持拖拽排列 + 动态渲染
 *
 * 每个组件根据 widget_type 渲染对应内容，
 * 用户可通过拖拽手柄重新排列组件顺序。
 */
import React, { useState, useCallback, useRef } from 'react'
import { useTranslation } from 'react-i18next'
import {
  HolderOutlined,
  CheckCircleOutlined,
  CloseCircleOutlined,
  ClockCircleOutlined,
  FieldTimeOutlined,
  ApiOutlined,
  GlobalOutlined,
  ThunderboltOutlined,
  FileTextOutlined,
  RobotOutlined,
  TeamOutlined,
  SafetyOutlined,
  DollarOutlined,
  LinkOutlined,
} from '@ant-design/icons'
import { Skeleton } from 'antd'
import ReactECharts from 'echarts-for-react'

/* ──────────── 类型定义 ──────────── */

export interface WidgetConfig {
  id?: number
  widget_type: string
  title?: string
  position_x?: number
  position_y: number
  width?: number
  height?: number
  config?: Record<string, unknown>
  is_visible?: boolean
}

export interface DashboardWidgetData {
  stats?: {
    api_tests: { total: number; passed: number; failed: number }
    web_tests: { total: number; passed: number; failed: number }
    perf_tests: { total: number; running: number }
    recent_runs: Array<Record<string, unknown>>
  }
  dailyTrend?: Array<{ date: string; passed: number; failed: number }>
  percentiles?: {
    p50: number; p90: number; p95: number; p99: number
    avg: number; total_requests: number
  } | null
  qualityTrend?: Array<Record<string, unknown>>
  loading?: boolean
}

interface GridProps {
  widgets: WidgetConfig[]
  data: DashboardWidgetData
  onReorder: (widgets: WidgetConfig[]) => void
  onNavigate?: (path: string) => void
}

/* ──────────── 组件图标映射 ──────────── */

const WIDGET_ICONS: Record<string, React.ReactNode> = {
  pass_rate: <CheckCircleOutlined />,
  recent_runs: <ClockCircleOutlined />,
  failed_top10: <CloseCircleOutlined />,
  ai_usage: <RobotOutlined />,
  team_activity: <TeamOutlined />,
  quality_gates: <SafetyOutlined />,
  sla_rate: <FieldTimeOutlined />,
  cost_overview: <DollarOutlined />,
  external_data: <LinkOutlined />,
}

/* ──────────── 单个组件渲染 ──────────── */

const WidgetContent: React.FC<{
  type: string
  data: DashboardWidgetData
  t: (key: string, opts?: Record<string, unknown>) => string
  onNavigate?: (path: string) => void
}> = ({ type, data, t, onNavigate }) => {
  const { stats, dailyTrend, percentiles, loading } = data

  if (loading) {
    return <Skeleton active paragraph={{ rows: 4 }} />
  }

  switch (type) {
    case 'pass_rate': {
      const apiTotal = stats?.api_tests.total || 0
      const apiPassed = stats?.api_tests.passed || 0
      const rate = apiTotal > 0 ? Math.round((apiPassed / apiTotal) * 100) : 0
      const trendData = dailyTrend?.length ? dailyTrend : []
      const option = {
        tooltip: { trigger: 'axis' as const },
        grid: { left: '3%', right: '4%', bottom: '5%', top: '10%', containLabel: true },
        xAxis: {
          type: 'category' as const, boundaryGap: false,
          data: trendData.map(d => d.date),
          axisLine: { lineStyle: { color: '#E8E8E8' } },
          axisLabel: { color: '#7C8180', fontSize: 10 },
        },
        yAxis: {
          type: 'value' as const, axisLine: { show: false },
          splitLine: { lineStyle: { color: '#F0F0F0' } },
          axisLabel: { color: '#7C8180', fontSize: 10 },
        },
        series: [{
          type: 'line' as const, smooth: true, symbol: 'circle', symbolSize: 4,
          data: trendData.map(d => d.passed),
          areaStyle: { color: { type: 'linear' as const, x: 0, y: 0, x2: 0, y2: 1, colorStops: [{ offset: 0, color: 'rgba(45,106,100,0.2)' }, { offset: 1, color: 'rgba(45,106,100,0.01)' }] } },
          itemStyle: { color: '#2D6A64' }, lineStyle: { width: 2 },
        }],
      }
      return (
        <div onClick={() => onNavigate?.('/reports')} style={{ cursor: 'pointer' }}>
          <div style={{ textAlign: 'center', marginBottom: 12 }}>
            <span style={{ fontSize: 32, fontWeight: 800, fontVariantNumeric: 'tabular-nums', color: rate >= 80 ? '#52c41a' : rate >= 60 ? '#faad14' : '#ff4d4f' }}>{rate}%</span>
            <div style={{ fontSize: 12, color: 'var(--fst-on-surface-muted)', marginTop: 4 }}>{t('dashboard.passRate') || '通过率'} · {apiPassed}/{apiTotal}</div>
          </div>
          {trendData.length > 0 && <ReactECharts option={option} style={{ height: 130 }} />}
          {trendData.length === 0 && <div style={{ height: 130, display: 'flex', alignItems: 'center', justifyContent: 'center', color: 'var(--fst-on-surface-muted)', fontSize: 13 }}>{t('dashboard.noTrendData') || '暂无趋势数据'}</div>}
        </div>
      )
    }

    case 'recent_runs': {
      const runs = stats?.recent_runs?.slice(0, 5) || []
      const statusColors: Record<string, string> = { success: '#52c41a', passed: '#52c41a', failed: '#ff4d4f', running: '#1890ff', pending: '#faad14' }
      if (runs.length === 0) return <div style={{ padding: 20, textAlign: 'center', color: 'var(--fst-on-surface-muted)' }}>{t('dashboard.noRecords')}</div>
      return (
        <div style={{ display: 'flex', flexDirection: 'column', gap: 6 }}>
          {runs.map((item: Record<string, unknown>, idx: number) => (
            <div key={idx} style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', padding: '8px 0', borderBottom: idx < runs.length - 1 ? '1px solid var(--fst-outline-soft, #f0f0f0)' : 'none' }}
              onClick={() => onNavigate?.('/reports')} role="button" tabIndex={0}>
              <div style={{ display: 'flex', alignItems: 'center', gap: 8, minWidth: 0 }}>
                <span style={{ width: 6, height: 6, borderRadius: '50%', background: statusColors[item.status as string] || '#999', flexShrink: 0 }} />
                <span style={{ fontSize: 13, overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>{(item.test_object_name as string) || `Run #${item.id}`}</span>
              </div>
              <span style={{ fontSize: 11, color: 'var(--fst-on-surface-muted)', flexShrink: 0 }}>{item.status as string}</span>
            </div>
          ))}
        </div>
      )
    }

    case 'failed_top10': {
      const runs = stats?.recent_runs || []
      const failed = runs.filter((r) => r.status === 'failed').slice(0, 10)
      if (failed.length === 0) return <div onClick={() => onNavigate?.('/reports')} style={{ padding: 20, textAlign: 'center', color: 'var(--fst-on-surface-muted)', cursor: 'pointer' }}>{t('dashboard.noRecords')}</div>
      return (
        <div onClick={() => onNavigate?.('/reports')} style={{ display: 'flex', flexDirection: 'column', gap: 4, cursor: 'pointer' }}>
          {failed.map((item: Record<string, unknown>, idx: number) => (
            <div key={idx} style={{ display: 'flex', alignItems: 'center', gap: 8, padding: '6px 0', fontSize: 13 }}>
              <span style={{ width: 18, textAlign: 'center', color: '#ff4d4f', fontWeight: 600, fontSize: 12 }}>{idx + 1}</span>
              <span style={{ overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap', flex: 1 }}>{(item.test_object_name as string) || `Run #${item.id}`}</span>
            </div>
          ))}
        </div>
      )
    }

    case 'percentiles':
    case 'response_time': {
      if (!percentiles || percentiles.total_requests === 0) {
        return <div style={{ padding: 20, textAlign: 'center', color: 'var(--fst-on-surface-muted)' }}>{t('dashboard.noPercentileData') || '暂无数据'}</div>
      }
      return (
        <div style={{ display: 'flex', flexDirection: 'column', gap: 0 }}>
          {[
            { label: 'P50', value: percentiles.p50, color: '#52c41a' },
            { label: 'P90', value: percentiles.p90, color: '#2D6A64' },
            { label: 'P95', value: percentiles.p95, color: percentiles.p95 > 2000 ? '#faad14' : '#2D6A64' },
            { label: 'P99', value: percentiles.p99, color: percentiles.p99 > 5000 ? '#ff4d4f' : '#2D6A64' },
          ].map((item) => (
            <div key={item.label} style={{ display: 'flex', justifyContent: 'space-between', padding: '8px 0', borderBottom: '1px solid var(--fst-outline-soft, #f0f0f0)' }}>
              <span style={{ fontWeight: 600, fontSize: 13, color: 'var(--fst-on-surface-variant)' }}>{item.label}</span>
              <span style={{ fontWeight: 700, fontSize: 15, color: item.color, fontVariantNumeric: 'tabular-nums' }}>
                {item.value >= 1000 ? `${(item.value / 1000).toFixed(2)}s` : `${item.value.toFixed(0)}ms`}
              </span>
            </div>
          ))}
        </div>
      )
    }

    case 'ai_usage':
      return (
        <div style={{ textAlign: 'center', padding: '16px 0' }}>
          <RobotOutlined style={{ fontSize: 32, color: 'var(--fst-primary, #2D6A64)', marginBottom: 8 }} />
          <div style={{ fontSize: 24, fontWeight: 700 }}>{stats?.api_tests.total || 0}</div>
          <div style={{ fontSize: 12, color: 'var(--fst-on-surface-muted)' }}>{t('dashboard.widgetType.ai_usage')}</div>
        </div>
      )

    case 'team_activity':
      return (
        <div onClick={() => onNavigate?.('/reports')} style={{ textAlign: 'center', padding: '16px 0', cursor: 'pointer' }}>
          <TeamOutlined style={{ fontSize: 32, color: '#629B95', marginBottom: 8 }} />
          <div style={{ fontSize: 24, fontWeight: 700 }}>{(stats?.api_tests.total || 0) + (stats?.web_tests.total || 0)}</div>
          <div style={{ fontSize: 12, color: 'var(--fst-on-surface-muted)' }}>{t('dashboard.widgetType.team_activity')}</div>
        </div>
      )

    case 'quality_gates': {
      const total = (stats?.api_tests.total || 0) + (stats?.web_tests.total || 0) + (stats?.perf_tests.total || 0)
      const passed = (stats?.api_tests.passed || 0) + (stats?.web_tests.passed || 0)
      const rate = total > 0 ? Math.round((passed / total) * 100) : 0
      return (
        <div onClick={() => onNavigate?.('/quality-gates')} style={{ textAlign: 'center', padding: '16px 0', cursor: 'pointer' }}>
          <SafetyOutlined style={{ fontSize: 32, color: rate >= 80 ? '#52c41a' : '#faad14', marginBottom: 8 }} />
          <div style={{ fontSize: 24, fontWeight: 700, color: rate >= 80 ? '#52c41a' : '#faad14' }}>{rate >= 80 ? 'PASS' : 'WARN'}</div>
          <div style={{ fontSize: 12, color: 'var(--fst-on-surface-muted)' }}>{t('dashboard.widgetType.quality_gates')}</div>
        </div>
      )
    }

    case 'sla_rate': {
      const total = (stats?.api_tests.total || 0) + (stats?.web_tests.total || 0)
      const passed = (stats?.api_tests.passed || 0) + (stats?.web_tests.passed || 0)
      const rate = total > 0 ? Math.round((passed / total) * 100) : 0
      const option = {
        series: [{
          type: 'gauge', startAngle: 200, endAngle: -20,
          min: 0, max: 100, radius: '90%',
          progress: { show: true, width: 14, itemStyle: { color: rate >= 95 ? '#52c41a' : rate >= 80 ? '#faad14' : '#ff4d4f' } },
          axisLine: { lineStyle: { width: 14, color: [[1, '#E8E8E8']] } },
          axisTick: { show: false }, splitLine: { show: false },
          axisLabel: { show: false }, pointer: { show: false },
          title: { show: false },
          detail: { valueAnimation: true, fontSize: 22, fontWeight: 700, formatter: '{value}%', color: 'inherit', offsetCenter: [0, '10%'] },
          data: [{ value: rate }],
        }],
      }
      return <div onClick={() => onNavigate?.('/reports')} style={{ cursor: 'pointer' }}><ReactECharts option={option} style={{ height: 160 }} /></div>
    }

    case 'cost_overview':
      return (
        <div onClick={() => onNavigate?.('/reports')} style={{ textAlign: 'center', padding: '16px 0', cursor: 'pointer' }}>
          <DollarOutlined style={{ fontSize: 32, color: '#D4B483', marginBottom: 8 }} />
          <div style={{ fontSize: 24, fontWeight: 700 }}>¥0</div>
          <div style={{ fontSize: 12, color: 'var(--fst-on-surface-muted)' }}>{t('dashboard.widgetType.cost_overview')}</div>
        </div>
      )

    default:
      return <div style={{ padding: 20, textAlign: 'center', color: 'var(--fst-on-surface-muted)' }}>{type.replace(/_/g, ' ')}</div>
  }
}

/* ──────────── 网格容器（带拖拽） ──────────── */

const DashboardWidgetGrid: React.FC<GridProps> = ({ widgets, data, onReorder, onNavigate }) => {
  const { t } = useTranslation()
  const [dragIndex, setDragIndex] = useState<number | null>(null)
  const [overIndex, setOverIndex] = useState<number | null>(null)
  const containerRef = useRef<HTMLDivElement>(null)

  const handleDragStart = useCallback((e: React.DragEvent, index: number) => {
    setDragIndex(index)
    e.dataTransfer.effectAllowed = 'move'
    e.dataTransfer.setData('text/plain', String(index))
    // 半透明拖拽效果
    if (e.currentTarget instanceof HTMLElement) {
      e.currentTarget.style.opacity = '0.5'
    }
  }, [])

  const handleDragOver = useCallback((e: React.DragEvent, index: number) => {
    e.preventDefault()
    e.dataTransfer.dropEffect = 'move'
    setOverIndex(index)
  }, [])

  const handleDragEnd = useCallback((e: React.DragEvent) => {
    if (e.currentTarget instanceof HTMLElement) {
      e.currentTarget.style.opacity = '1'
    }
    if (dragIndex !== null && overIndex !== null && dragIndex !== overIndex) {
      const reordered = [...widgets]
      const [moved] = reordered.splice(dragIndex, 1)
      reordered.splice(overIndex, 0, moved)
      // 更新 position_y
      const updated = reordered.map((w, i) => ({ ...w, position_y: i }))
      onReorder(updated)
    }
    setDragIndex(null)
    setOverIndex(null)
  }, [dragIndex, overIndex, widgets, onReorder])

  const handleDragLeave = useCallback(() => {
    setOverIndex(null)
  }, [])

  if (widgets.length === 0) {
    return (
      <div style={{ padding: 40, textAlign: 'center', color: 'var(--fst-on-surface-muted)' }}>
        {t('dashboard.noWidgets') || '暂无组件，请点击右上角"自定义布局"添加'}
      </div>
    )
  }

  return (
    <div
      ref={containerRef}
      style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fill, minmax(320px, 1fr))',
        gap: 16,
      }}
    >
      {widgets.map((widget, index) => {
        const icon = WIDGET_ICONS[widget.widget_type] || <ApiOutlined />
        const title = t(`dashboard.widgetType.${widget.widget_type}`) || widget.widget_type.replace(/_/g, ' ')
        const isOver = overIndex === index && dragIndex !== index

        return (
          <div
            key={widget.widget_type + '-' + index}
            draggable
            onDragStart={(e) => handleDragStart(e, index)}
            onDragOver={(e) => handleDragOver(e, index)}
            onDragEnd={handleDragEnd}
            onDragLeave={handleDragLeave}
            className="fst-ios-card"
            style={{
              gridColumn: (widget.width || 1) >= 2 ? 'span 2' : 'span 1',
              transition: 'transform 150ms ease, box-shadow 150ms ease',
              transform: isOver && dragIndex !== null && dragIndex < index ? 'translateX(4px)' : isOver ? 'translateX(-4px)' : 'none',
              boxShadow: isOver ? '0 0 0 2px var(--fst-primary, #2D6A64)' : undefined,
              cursor: 'grab',
              userSelect: 'none',
            }}
          >
            <div className="fst-ios-card-header" style={{ flexDirection: 'row', alignItems: 'center', gap: 8 }}>
              <HolderOutlined style={{ color: 'var(--fst-on-surface-muted)', cursor: 'grab', fontSize: 14 }} />
              <span style={{ color: 'var(--fst-primary, #2D6A64)', fontSize: 16 }}>{icon}</span>
              <span className="fst-ios-card-title" style={{ flex: 1, fontSize: 14 }}>{title}</span>
            </div>
            <div style={{ padding: '4px 0 0' }}>
              <WidgetContent type={widget.widget_type} data={data} t={t} onNavigate={onNavigate} />
            </div>
          </div>
        )
      })}
    </div>
  )
}

export default DashboardWidgetGrid
