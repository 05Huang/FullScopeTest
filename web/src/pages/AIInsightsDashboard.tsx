import { useState, useEffect, useCallback } from 'react'
import {
  Card, Row, Col, Statistic, Typography, Table, Tag, Space, Select, Spin, Empty, Progress, Button,
} from 'antd'
import {
  RobotOutlined, CheckCircleOutlined, CloseCircleOutlined, ClockCircleOutlined,
  DollarOutlined, BarChartOutlined, ReloadOutlined, TrophyOutlined,
} from '@ant-design/icons'
import { useTranslation } from 'react-i18next'
import ReactECharts from 'echarts-for-react'
import type { ColumnsType } from 'antd/es/table'
import { aiStatsService } from '@/services/aiStatsService'

const { Title, Text } = Typography

interface AIStatsOverview {
  total_invocations: number; success_rate: number; total_tokens: number;
  total_cost: number; avg_latency_ms: number; features: Record<string, number>;
}
interface SuccessRateTrend { date: string; total: number; success: number; success_rate: number; }
interface LatencyTrend { date: string; avg_latency_ms: number; avg_tokens: number; }
interface TokenConsumption { date: string; prompt_tokens: number; completion_tokens: number; total_tokens: number; cost: number; }
interface PromptVersionComparison {
  id: number; feature: string; name: string; version: number; is_active: boolean;
  total_invocations: number; success_count: number; failure_count: number;
  success_rate: number; avg_latency_ms: number; avg_tokens: number; avg_cost: number;
}

const COLORS = { success: '#52c41a', failed: '#ff4d4f', primary: '#1890ff', warning: '#faad14', purple: '#722ed1', cyan: '#13c2c2', orange: '#fa8c16' }
const FEATURE_COLORS: Record<string, string> = { copilot: COLORS.primary, script_gen: COLORS.success, swagger_gen: COLORS.purple, dedup: COLORS.cyan, other: COLORS.orange }

const AIInsightsDashboard = () => {
  const { t } = useTranslation()

  const FEATURE_LABELS: Record<string, string> = {
    copilot: t('ai.copilot'),
    script_gen: t('ai.scriptGen'),
    swagger_gen: t('ai.swaggerGen'),
    dedup: t('ai.dedup'),
    other: t('ai.other'),
  }
  const [loading, setLoading] = useState(false)
  const [overview, setOverview] = useState<AIStatsOverview | null>(null)
  const [successTrend, setSuccessTrend] = useState<SuccessRateTrend[]>([])
  const [latencyTrend, setLatencyTrend] = useState<LatencyTrend[]>([])
  const [tokenConsumption, setTokenConsumption] = useState<TokenConsumption[]>([])
  const [promptVersions, setPromptVersions] = useState<PromptVersionComparison[]>([])
  const [days, setDays] = useState(30)
  const [featureFilter, setFeatureFilter] = useState<string | undefined>(undefined)

  const fetchData = useCallback(async () => {
    setLoading(true)
    try {
      const [o, s, l, t, v] = await Promise.all([
        aiStatsService.getOverview(), aiStatsService.getSuccessRateTrend(days, featureFilter),
        aiStatsService.getLatencyTrend(days, featureFilter), aiStatsService.getTokenConsumption(days),
        aiStatsService.getPromptVersionsComparison(featureFilter),
      ])
      if (o.code === 200) setOverview(o.data); if (s.code === 200) setSuccessTrend(s.data || []);
      if (l.code === 200) setLatencyTrend(l.data || []); if (t.code === 200) setTokenConsumption(t.data || []);
      if (v.code === 200) setPromptVersions(v.data || []);
    } catch { /* silent */ } finally { setLoading(false); }
  }, [days, featureFilter])

  useEffect(() => { fetchData() }, [fetchData])

  const successRateChartOption = {
    tooltip: { trigger: 'axis' },
    grid: { left: '3%', right: '4%', bottom: '10%', top: '10%', containLabel: true },
    xAxis: { type: 'category', data: successTrend.map(d => d.date) },
    yAxis: { type: 'value', name: '%', min: 0, max: 100 },
    series: [{ name: t('ai.successRate'), type: 'line', smooth: true, data: successTrend.map(d => d.success_rate),
      itemStyle: { color: COLORS.success }, areaStyle: { opacity: 0.1 }, lineStyle: { width: 2 },
      markLine: { silent: true, data: [{ yAxis: 95, name: 'Target 95%' }],
        lineStyle: { color: COLORS.warning, type: 'dashed', width: 1 },
        label: { formatter: 'Target: 95%', color: COLORS.warning } } }],
  }

  const latencyChartOption = {
    tooltip: { trigger: 'axis' },
    legend: { data: [t('ai.avgLatency'), 'Avg Tokens'], bottom: 0 },
    grid: { left: '3%', right: '4%', bottom: '15%', top: '8%', containLabel: true },
    xAxis: { type: 'category', data: latencyTrend.map(d => d.date) },
    yAxis: [{ type: 'value', name: 'ms', position: 'left' }, { type: 'value', name: 'tokens', position: 'right' }],
    series: [
      { name: t('ai.avgLatency'), type: 'line', smooth: true, data: latencyTrend.map(d => d.avg_latency_ms),
        itemStyle: { color: COLORS.primary }, areaStyle: { opacity: 0.08 }, lineStyle: { width: 2 } },
      { name: 'Avg Tokens', type: 'line', smooth: true, yAxisIndex: 1, data: latencyTrend.map(d => d.avg_tokens),
        itemStyle: { color: COLORS.purple }, areaStyle: { opacity: 0.05 }, lineStyle: { width: 1.5, type: 'dashed' } },
    ],
  }

  const tokenChartOption = {
    tooltip: { trigger: 'axis' },
    legend: { data: ['Prompt Tokens', 'Completion Tokens'], bottom: 0 },
    grid: { left: '3%', right: '4%', bottom: '15%', top: '8%', containLabel: true },
    xAxis: { type: 'category', data: tokenConsumption.map(d => d.date) },
    yAxis: { type: 'value', name: 'tokens' },
    series: [
      { name: 'Prompt Tokens', type: 'bar', stack: 'tokens', data: tokenConsumption.map(d => d.prompt_tokens), itemStyle: { color: COLORS.primary } },
      { name: 'Completion Tokens', type: 'bar', stack: 'tokens', data: tokenConsumption.map(d => d.completion_tokens), itemStyle: { color: COLORS.cyan } },
    ],
  }

  const featurePieOption = (() => {
    const features = overview?.features || {}
    const data = Object.entries(features).map(([key, value]) => ({ value, name: FEATURE_LABELS[key] || key, itemStyle: { color: FEATURE_COLORS[key] || FEATURE_COLORS.other } }))
    return { tooltip: { trigger: 'item', formatter: '{b}: {c} ({d}%)' }, legend: { bottom: 0, type: 'scroll' },
      series: [{ type: 'pie', radius: ['40%', '70%'], data, emphasis: { itemStyle: { shadowBlur: 10 } }, label: { show: true, formatter: '{b}: {d}%' } }] }
  })()

  const versionColumns: ColumnsType<PromptVersionComparison> = [
    { title: t('ai.featureDistribution'), dataIndex: 'feature', width: 100, render: (f: string) => <Tag color={FEATURE_COLORS[f] || 'default'}>{FEATURE_LABELS[f] || f}</Tag> },
    { title: t('ai.promptVersions'), dataIndex: 'name', width: 150, render: (name: string, r) => <Space><Text>{name}</Text><Text type="secondary" style={{ fontSize: 12 }}>v{r.version}</Text>{r.is_active && <Tag color="success" style={{ fontSize: 11 }}>Active</Tag>}</Space> },
    { title: t('ai.totalInvocations'), dataIndex: 'total_invocations', width: 100, sorter: (a: any, b: any) => a.total_invocations - b.total_invocations },
    { title: t('ai.successRate'), dataIndex: 'success_rate', width: 120, render: (rate: number) => { const c = rate >= 95 ? COLORS.success : rate >= 80 ? COLORS.warning : COLORS.failed; return <Space size={4}><Progress percent={rate} size="small" strokeColor={c} style={{ width: 60 }} showInfo={false} /><Text style={{ color: c }}>{rate}%</Text></Space> }, sorter: (a: any, b: any) => a.success_rate - b.success_rate },
    { title: t('ai.avgLatency'), dataIndex: 'avg_latency_ms', width: 100, render: (v: number) => v + ' ms', sorter: (a: any, b: any) => a.avg_latency_ms - b.avg_latency_ms },
    { title: 'Avg Tokens', dataIndex: 'avg_tokens', width: 100, render: (v: number) => v?.toFixed(0) ?? '-', sorter: (a: any, b: any) => a.avg_tokens - b.avg_tokens },
    { title: t('ai.totalCost'), dataIndex: 'avg_cost', width: 100, render: (v: number) => '$' + (v?.toFixed(4) ?? '0'), sorter: (a: any, b: any) => a.avg_cost - b.avg_cost },
  ]

  return (
    <div>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 16 }}>
        <Title level={4} style={{ margin: 0 }}><RobotOutlined style={{ marginRight: 8 }} />{t('ai.title')}</Title>
        <Space>
          <Select value={days} onChange={setDays} style={{ width: 120 }} options={[{ value: 7, label: t('ai.last7Days') }, { value: 14, label: 'Last 14 Days' }, { value: 30, label: t('ai.last30Days') }, { value: 90, label: t('ai.last90Days') }]} />
          <Select allowClear placeholder={t('ai.allFeatures')} style={{ width: 140 }} value={featureFilter} onChange={setFeatureFilter} options={Object.entries(FEATURE_LABELS).map(([k, l]) => ({ value: k, label: l }))} />
          <Button icon={<ReloadOutlined />} onClick={fetchData} loading={loading}>{t('common.refresh')}</Button>
        </Space>
      </div>
      <Spin spinning={loading}>
        <Row gutter={[16, 16]} style={{ marginBottom: 16 }}>
          <Col xs={12} sm={8} lg={4}><Card size="small"><Statistic title={t('ai.totalInvocations')} value={overview?.total_invocations ?? 0} prefix={<BarChartOutlined style={{ color: COLORS.primary }} />} /></Card></Col>
          <Col xs={12} sm={8} lg={4}><Card size="small"><Statistic title={t('ai.successRate')} value={overview?.success_rate ?? 0} suffix="%" valueStyle={{ color: (overview?.success_rate ?? 0) >= 95 ? COLORS.success : COLORS.warning }} prefix={(overview?.success_rate ?? 0) >= 95 ? <CheckCircleOutlined /> : <CloseCircleOutlined />} /></Card></Col>
          <Col xs={12} sm={8} lg={4}><Card size="small"><Statistic title={t('ai.avgLatency')} value={overview?.avg_latency_ms ?? 0} suffix="ms" prefix={<ClockCircleOutlined style={{ color: COLORS.primary }} />} /></Card></Col>
          <Col xs={12} sm={8} lg={4}><Card size="small"><Statistic title={t('ai.totalTokens')} value={overview?.total_tokens ?? 0} prefix={<BarChartOutlined style={{ color: COLORS.purple }} />} /></Card></Col>
          <Col xs={12} sm={8} lg={4}><Card size="small"><Statistic title={t('ai.totalCost')} value={overview?.total_cost ?? 0} prefix={<DollarOutlined style={{ color: COLORS.warning }} />} precision={4} /></Card></Col>
          <Col xs={12} sm={8} lg={4}><Card size="small"><Statistic title={t('ai.featureDistribution')} value={Object.keys(overview?.features ?? {}).length} prefix={<TrophyOutlined style={{ color: COLORS.cyan }} />} /></Card></Col>
        </Row>
        <Row gutter={[16, 16]} style={{ marginBottom: 16 }}>
          <Col xs={24} lg={12}><Card title={t('ai.successRateTrend')} size="small">{successTrend.length > 0 ? <ReactECharts option={successRateChartOption} style={{ height: 300 }} /> : <Empty description={t('common.noData')} />}</Card></Col>
          <Col xs={24} lg={12}><Card title={t('ai.featureDistribution')} size="small">{overview && Object.keys(overview.features).length > 0 ? <ReactECharts option={featurePieOption} style={{ height: 300 }} /> : <Empty description={t('common.noData')} />}</Card></Col>
        </Row>
        <Row gutter={[16, 16]} style={{ marginBottom: 16 }}>
          <Col xs={24} lg={12}><Card title={t('ai.latencyTrend')} size="small">{latencyTrend.length > 0 ? <ReactECharts option={latencyChartOption} style={{ height: 300 }} /> : <Empty description={t('common.noData')} />}</Card></Col>
          <Col xs={24} lg={12}><Card title={t('ai.tokenConsumption')} size="small">{tokenConsumption.length > 0 ? <ReactECharts option={tokenChartOption} style={{ height: 300 }} /> : <Empty description={t('common.noData')} />}</Card></Col>
        </Row>
        <Card title={t('ai.promptVersions')} size="small">
          {promptVersions.length > 0 ? <Table columns={versionColumns} dataSource={promptVersions} rowKey="id" size="small" pagination={{ pageSize: 10, showTotal: (total) => `${total} versions` }} scroll={{ x: 800 }} /> : <Empty description={t('common.noData')} />}
        </Card>
      </Spin>
    </div>
  )
}

export default AIInsightsDashboard
