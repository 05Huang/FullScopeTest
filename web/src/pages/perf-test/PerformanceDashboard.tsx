import { useState, useEffect, useCallback, useRef } from 'react'
import {
  Card,
  Row,
  Col,
  Statistic,
  Typography,
  Table,
  Tag,
  Space,
  Empty,
  Button,
  Select,
  Checkbox,
  Spin,
  Tooltip,
} from 'antd'
import {
  DashboardOutlined,
  ClockCircleOutlined,
  ThunderboltOutlined,
  CheckCircleOutlined,
  CloseCircleOutlined,
  ReloadOutlined,
  SwapOutlined,
  WarningOutlined,
  ApartmentOutlined,
} from '@ant-design/icons'
import ReactECharts from 'echarts-for-react'
import type { ColumnsType } from 'antd/es/table'
import { perfTestService } from '@/services/perfTestService'

const { Title, Text } = Typography

/* ================================================================
   类型定义
   ================================================================ */

interface PerformanceTestResultItem {
  id: number
  scenario_id: number
  scenario_name?: string
  user_count: number
  spawn_rate: number
  duration: number
  target_url?: string
  status: string
  started_at?: string
  finished_at?: string
  total_requests: number
  total_failures: number
  error_rate: number
  rps: number
  avg_response_time: number
  min_response_time: number
  max_response_time: number
  p50_response_time: number
  p75_response_time: number
  p95_response_time: number
  p99_response_time: number
  created_at?: string
}

interface MetricSample {
  id: number
  test_result_id: number
  timestamp: string
  elapsed_seconds: number
  rps: number
  active_users: number
  avg_response_time: number
  min_response_time: number
  max_response_time: number
  p95_response_time: number
  p99_response_time: number
  request_count: number
  failure_count: number
  error_rate: number
}

/* ================================================================
   颜色常量
   ================================================================ */

const COLORS = {
  rps: '#1890ff',
  avgRT: '#52c41a',
  p95: '#faad14',
  p99: '#fa541c',
  errorRate: '#ff4d4f',
  users: '#722ed1',
  success: '#52c41a',
  failed: '#ff4d4f',
  stopped: '#faad14',
  running: '#1890ff',
}

const RUN_COLOR_PALETTE = [
  '#1890ff', '#52c41a', '#faad14', '#fa541c', '#722ed1',
  '#13c2c2', '#eb2f96', '#a0d911', '#2f54eb', '#fa8c16',
]

/* ================================================================
   主组件
   ================================================================ */

const PerformanceDashboard = () => {
  /* ---------- 状态 ---------- */
  const [resultsLoading, setResultsLoading] = useState(false)
  const [metricsLoading, setMetricsLoading] = useState(false)
  const [results, setResults] = useState<PerformanceTestResultItem[]>([])
  const [selectedResultId, setSelectedResultId] = useState<number | null>(null)
  const [currentMetrics, setCurrentMetrics] = useState<MetricSample[]>([])
  const [currentResult, setCurrentResult] = useState<PerformanceTestResultItem | null>(null)

  /* 历史对比 */
  const [compareMode, setCompareMode] = useState(false)
  const [compareIds, setCompareIds] = useState<number[]>([])
  const [compareData, setCompareData] = useState<PerformanceTestResultItem[]>([])
  const [compareMetricsMap, setCompareMetricsMap] = useState<Record<number, MetricSample[]>>({})

  /* 筛选 */
  const [scenarioFilter, setScenarioFilter] = useState<number | undefined>(undefined)
  const [statusFilter, setStatusFilter] = useState<string | undefined>(undefined)
  const [currentPage, setCurrentPage] = useState(1)
  const [totalResults, setTotalResults] = useState(0)

  /* 实时轮询 */
  const pollingRef = useRef<ReturnType<typeof setInterval> | null>(null)

  /* ---------- 获取历史结果列表 ---------- */
  const fetchResults = useCallback(async (page = 1) => {
    setResultsLoading(true)
    try {
      const params: Record<string, any> = { page, per_page: 15 }
      if (scenarioFilter) params.scenario_id = scenarioFilter
      if (statusFilter) params.status = statusFilter

      const res = await perfTestService.getPerformanceResults(params)
      if (res.code === 200) {
        const items = res.data?.items || []
        const total = res.data?.pagination?.total || 0
        setResults(items)
        setTotalResults(total)
        setCurrentPage(page)
      }
    } catch {
      /* 静默 */
    } finally {
      setResultsLoading(false)
    }
  }, [scenarioFilter, statusFilter])

  /* ---------- 获取某个结果的指标采样 ---------- */
  const fetchMetrics = useCallback(async (resultId: number) => {
    setMetricsLoading(true)
    try {
      const res = await perfTestService.getPerformanceResultMetrics(resultId)
      if (res.code === 200) {
        setCurrentResult(res.data?.result || null)
        setCurrentMetrics(res.data?.metrics || [])
      }
    } catch {
      /* 静默 */
    } finally {
      setMetricsLoading(false)
    }
  }, [])

  /* ---------- 选择测试结果 ---------- */
  const handleSelectResult = useCallback((resultId: number) => {
    setSelectedResultId(resultId)
    setCompareMode(false)
    setCompareIds([])
    setCompareData([])
    setCompareMetricsMap({})
    fetchMetrics(resultId)
  }, [fetchMetrics])

  /* ---------- 对比模式 ---------- */
  const toggleCompareMode = useCallback(() => {
    setCompareMode(prev => !prev)
    if (compareMode) {
      setCompareIds([])
      setCompareData([])
      setCompareMetricsMap({})
      if (selectedResultId) {
        fetchMetrics(selectedResultId)
      }
    } else {
      setCurrentMetrics([])
      setCurrentResult(null)
    }
  }, [compareMode, selectedResultId, fetchMetrics])

  const handleCompareSelect = useCallback(async (resultIds: number[]) => {
    if (resultIds.length < 1) {
      setCompareIds([])
      setCompareData([])
      setCompareMetricsMap({})
      return
    }
    setCompareIds(resultIds)

    /* 获取每个结果的指标 */
    const allData: PerformanceTestResultItem[] = []
    const metricsMap: Record<number, MetricSample[]> = {}

    await Promise.all(
      resultIds.map(async (id) => {
        try {
          const res = await perfTestService.getPerformanceResultMetrics(id)
          if (res.code === 200) {
            allData.push(res.data?.result)
            metricsMap[id] = res.data?.metrics || []
          }
        } catch {
          /* 静默 */
        }
      })
    )

    /* 按创建时间排序 */
    allData.sort((a, b) => {
      const ta = a.created_at ? new Date(a.created_at).getTime() : 0
      const tb = b.created_at ? new Date(b.created_at).getTime() : 0
      return ta - tb
    })

    setCompareData(allData)
    setCompareMetricsMap(metricsMap)
  }, [])

  /* ---------- 初始化 & 轮询 ---------- */
  useEffect(() => {
    fetchResults(1)
  }, [fetchResults])

  /* 自动刷新运行中状态的结果 */
  useEffect(() => {
    pollingRef.current = setInterval(() => {
      fetchResults(currentPage)
    }, 10000)
    return () => {
      if (pollingRef.current) clearInterval(pollingRef.current)
    }
  }, [fetchResults, currentPage])

  /* ================================================================
     图表配置
     ================================================================ */

  /** 实时 RPS 折线图 */
  const rpsChartOption = {
    tooltip: { trigger: 'axis' },
    legend: { data: ['RPS', '活跃用户'], bottom: 0 },
    grid: { left: '3%', right: '4%', bottom: '15%', top: '8%', containLabel: true },
    xAxis: {
      type: 'category',
      data: currentMetrics.map(m => `${m.elapsed_seconds}s`),
      axisLabel: { rotate: 0 },
    },
    yAxis: [
      { type: 'value', name: 'req/s', position: 'left' },
      { type: 'value', name: 'users', position: 'right' },
    ],
    series: [
      {
        name: 'RPS',
        type: 'line',
        smooth: true,
        data: currentMetrics.map(m => m.rps),
        itemStyle: { color: COLORS.rps },
        areaStyle: { opacity: 0.1 },
        lineStyle: { width: 2 },
      },
      {
        name: '活跃用户',
        type: 'line',
        smooth: true,
        yAxisIndex: 1,
        data: currentMetrics.map(m => m.active_users),
        itemStyle: { color: COLORS.users },
        areaStyle: { opacity: 0.05 },
        lineStyle: { width: 1.5, type: 'dashed' },
      },
    ],
  }

  /** 响应时间折线图（含 P95/P99 高亮） */
  const responseTimeChartOption = {
    tooltip: {
      trigger: 'axis',
      formatter: (params: any[]) => {
        if (!params || params.length === 0) return ''
        let html = `<b>${params[0].axisValue}</b><br/>`
        params.forEach((p: any) => {
          html += `${p.marker} ${p.seriesName}: <b>${p.value?.toFixed(1) ?? '-'} ms</b><br/>`
        })
        return html
      },
    },
    legend: {
      data: ['平均响应时间', 'P95', 'P99', '最小', '最大'],
      bottom: 0,
    },
    grid: { left: '3%', right: '4%', bottom: '15%', top: '8%', containLabel: true },
    xAxis: {
      type: 'category',
      data: currentMetrics.map(m => `${m.elapsed_seconds}s`),
    },
    yAxis: { type: 'value', name: 'ms' },
    series: [
      {
        name: '平均响应时间',
        type: 'line',
        smooth: true,
        data: currentMetrics.map(m => m.avg_response_time),
        itemStyle: { color: COLORS.avgRT },
        areaStyle: { opacity: 0.08 },
        lineStyle: { width: 2 },
      },
      {
        name: 'P95',
        type: 'line',
        smooth: true,
        data: currentMetrics.map(m => m.p95_response_time),
        itemStyle: { color: COLORS.p95 },
        lineStyle: { width: 2.5, type: 'solid' },
        symbol: 'circle',
        symbolSize: 4,
        markLine: currentResult?.p95_response_time
          ? {
              silent: true,
              data: [{ yAxis: currentResult.p95_response_time, name: 'P95 汇总' }],
              lineStyle: { color: COLORS.p95, type: 'dashed', width: 1 },
              label: { formatter: 'P95: {c} ms', color: COLORS.p95 },
            }
          : undefined,
      },
      {
        name: 'P99',
        type: 'line',
        smooth: true,
        data: currentMetrics.map(m => m.p99_response_time),
        itemStyle: { color: COLORS.p99 },
        lineStyle: { width: 2.5, type: 'solid' },
        symbol: 'diamond',
        symbolSize: 5,
        markLine: currentResult?.p99_response_time
          ? {
              silent: true,
              data: [{ yAxis: currentResult.p99_response_time, name: 'P99 汇总' }],
              lineStyle: { color: COLORS.p99, type: 'dashed', width: 1 },
              label: { formatter: 'P99: {c} ms', color: COLORS.p99 },
            }
          : undefined,
      },
      {
        name: '最小',
        type: 'line',
        smooth: true,
        data: currentMetrics.map(m => m.min_response_time),
        itemStyle: { color: '#bfbfbf' },
        lineStyle: { width: 1, type: 'dotted' },
      },
      {
        name: '最大',
        type: 'line',
        smooth: true,
        data: currentMetrics.map(m => m.max_response_time),
        itemStyle: { color: '#ff7a45' },
        lineStyle: { width: 1, type: 'dotted' },
      },
    ],
  }

  /** 错误率折线图 */
  const errorRateChartOption = {
    tooltip: { trigger: 'axis' },
    legend: { data: ['错误率 (%)'], bottom: 0 },
    grid: { left: '3%', right: '4%', bottom: '15%', top: '8%', containLabel: true },
    xAxis: {
      type: 'category',
      data: currentMetrics.map(m => `${m.elapsed_seconds}s`),
    },
    yAxis: {
      type: 'value',
      name: '%',
      min: 0,
    },
    series: [
      {
        name: '错误率 (%)',
        type: 'line',
        smooth: true,
        data: currentMetrics.map(m => m.error_rate),
        itemStyle: { color: COLORS.errorRate },
        areaStyle: { opacity: 0.12 },
        lineStyle: { width: 2 },
        markArea: {
          silent: true,
          data: [[{ yAxis: 5, itemStyle: { color: 'rgba(255,77,79,0.06)' } }, { yAxis: 100 }]],
        },
      },
    ],
  }

  /** 历史对比折线图（多条曲线叠加） */
  const buildCompareChart = (
    label: string,
    field: keyof MetricSample,
    color?: string,
  ) => ({
    tooltip: { trigger: 'axis' },
    legend: {
      data: compareData.map(d => `#${d.id}`),
      bottom: 0,
    },
    grid: { left: '3%', right: '4%', bottom: '15%', top: '10%', containLabel: true },
    xAxis: { type: 'category', data: ['0s'] },
    yAxis: { type: 'value', name: label },
    series: compareData.map((d, i) => {
      const metrics = compareMetricsMap[d.id] || []
      return {
        name: `#${d.id}`,
        type: 'line',
        smooth: true,
        data: metrics.map((m: any) => m[field]),
        itemStyle: { color: color || RUN_COLOR_PALETTE[i % RUN_COLOR_PALETTE.length] },
        lineStyle: { width: 2 },
        areaStyle: { opacity: 0.05 },
      }
    }),
  })

  const compareRpsOption = (() => {
    const opt = buildCompareChart('req/s', 'rps')
    if (compareData.length > 0) {
      const maxLen = Math.max(...compareData.map(d => (compareMetricsMap[d.id] || []).length))
      const ticks = Array.from({ length: maxLen }, (_, i) => `${i}s`)
      opt.xAxis.data = ticks
    }
    return opt
  })()

  const compareResponseTimeOption = (() => {
    const opt = buildCompareChart('ms', 'avg_response_time')
    if (compareData.length > 0) {
      const maxLen = Math.max(...compareData.map(d => (compareMetricsMap[d.id] || []).length))
      opt.xAxis.data = Array.from({ length: maxLen }, (_, i) => `${i}s`)
    }
    /* 添加 P95/P99 作为额外 series */
    compareData.forEach((d, i) => {
      const metrics = compareMetricsMap[d.id] || []
      const baseColor = RUN_COLOR_PALETTE[i % RUN_COLOR_PALETTE.length]
      opt.series.push({
        name: `#${d.id} P95`,
        type: 'line',
        smooth: true,
        data: metrics.map((m: any) => m.p95_response_time),
        itemStyle: { color: baseColor },
        lineStyle: { width: 1.5, type: 'dashed' },
        symbol: 'circle',
        symbolSize: 3,
      } as any)
      opt.series.push({
        name: `#${d.id} P99`,
        type: 'line',
        smooth: true,
        data: metrics.map((m: any) => m.p99_response_time),
        itemStyle: { color: baseColor },
        lineStyle: { width: 1, type: 'dotted' },
        symbol: 'diamond',
        symbolSize: 3,
      } as any)
    })
    opt.legend.data = compareData.flatMap(d => [`#${d.id}`, `#${d.id} P95`, `#${d.id} P99`])
    return opt
  })()

  const compareErrorRateOption = (() => {
    const opt = buildCompareChart('%', 'error_rate')
    if (compareData.length > 0) {
      const maxLen = Math.max(...compareData.map(d => (compareMetricsMap[d.id] || []).length))
      opt.xAxis.data = Array.from({ length: maxLen }, (_, i) => `${i}s`)
    }
    return opt
  })()

  /* ================================================================
     汇总统计
     ================================================================ */

  const summaryStats = (() => {
    if (!currentMetrics.length && !currentResult) {
      return { avgRps: 0, avgRT: 0, p95: 0, p99: 0, errorRate: 0 }
    }
    if (currentResult && !currentMetrics.length) {
      return {
        avgRps: currentResult.rps || 0,
        avgRT: currentResult.avg_response_time || 0,
        p95: currentResult.p95_response_time || 0,
        p99: currentResult.p99_response_time || 0,
        errorRate: currentResult.error_rate || 0,
      }
    }
    const n = currentMetrics.length
    return {
      avgRps: Math.round(currentMetrics.reduce((s, m) => s + m.rps, 0) / n),
      avgRT: Math.round(currentMetrics.reduce((s, m) => s + m.avg_response_time, 0) / n),
      p95: Math.round(currentMetrics.reduce((s, m) => s + m.p95_response_time, 0) / n),
      p99: Math.round(currentMetrics.reduce((s, m) => s + m.p99_response_time, 0) / n),
      errorRate: parseFloat((currentMetrics.reduce((s, m) => s + m.error_rate, 0) / n).toFixed(2)),
    }
  })()

  /* ================================================================
     表格列
     ================================================================ */

  const resultColumns: ColumnsType<PerformanceTestResultItem> = [
    {
      title: 'ID',
      dataIndex: 'id',
      key: 'id',
      width: 60,
      render: (id: number) => (
        <Text code>{id}</Text>
      ),
    },
    {
      title: '场景 ID',
      dataIndex: 'scenario_id',
      key: 'scenario_id',
      width: 80,
    },
    {
      title: '并发数',
      dataIndex: 'user_count',
      key: 'user_count',
      width: 80,
      render: (val: number) => `${val}`,
    },
    {
      title: 'RPS',
      dataIndex: 'rps',
      key: 'rps',
      width: 80,
      render: (val: number) => val?.toFixed(1) ?? '-',
    },
    {
      title: '平均 RT',
      dataIndex: 'avg_response_time',
      key: 'avg_response_time',
      width: 100,
      render: (val: number) => {
        if (!val) return '-'
        const color = val < 500 ? COLORS.success : val < 1500 ? COLORS.stopped : COLORS.failed
        return <Text style={{ color }}>{val.toFixed(0)} ms</Text>
      },
    },
    {
      title: 'P95',
      dataIndex: 'p95_response_time',
      key: 'p95_response_time',
      width: 80,
      render: (val: number) => val ? <Text style={{ color: COLORS.p95 }}>{val.toFixed(0)} ms</Text> : '-',
    },
    {
      title: 'P99',
      dataIndex: 'p99_response_time',
      key: 'p99_response_time',
      width: 80,
      render: (val: number) => val ? <Text style={{ color: COLORS.p99 }}>{val.toFixed(0)} ms</Text> : '-',
    },
    {
      title: '错误率',
      dataIndex: 'error_rate',
      key: 'error_rate',
      width: 80,
      render: (val: number) => {
        if (!val && val !== 0) return '-'
        const color = val < 1 ? COLORS.success : val < 5 ? COLORS.stopped : COLORS.failed
        return <Text style={{ color }}>{val.toFixed(2)}%</Text>
      },
    },
    {
      title: '状态',
      dataIndex: 'status',
      key: 'status',
      width: 90,
      render: (status: string) => {
        const map: Record<string, { color: string; text: string }> = {
          completed: { color: 'success', text: '完成' },
          failed: { color: 'error', text: '失败' },
          stopped: { color: 'warning', text: '已停止' },
          running: { color: 'processing', text: '运行中' },
        }
        const info = map[status] || { color: 'default', text: status }
        return <Tag color={info.color}>{info.text}</Tag>
      },
    },
    {
      title: '时间',
      dataIndex: 'created_at',
      key: 'created_at',
      width: 140,
      render: (t: string) => t ? new Date(t).toLocaleString() : '-',
    },
  ]

  /* ================================================================
     渲染
     ================================================================ */

  return (
    <div className="fst-page">
      {/* 标题栏 */}
      <div className="fst-page-header fst-animate-in">
        <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
          <div className="fst-stat-icon fst-stat-icon--tertiary"><DashboardOutlined style={{ fontSize: 18 }} /></div>
          <h1 className="fst-page-title">性能测试大盘</h1>
        </div>
        <div style={{ display: 'flex', gap: 8 }}>
          <button className={`fst-btn fst-btn--sm ${compareMode ? 'fst-btn--primary' : 'fst-btn--ghost'}`} onClick={toggleCompareMode}>
            <SwapOutlined /> {compareMode ? '退出对比' : '历史对比'}
          </button>
          <button className="fst-btn fst-btn--ghost fst-btn--sm" onClick={() => {
            fetchResults(currentPage)
            if (selectedResultId && !compareMode) fetchMetrics(selectedResultId)
          }}>
            <ReloadOutlined /> 刷新
          </button>
        </div>
      </div>

      {/* 筛选栏 */}
      <Card size="small" style={{ marginBottom: 16 }}>
        <Space wrap>
          <span>状态：</span>
          <Select
            allowClear
            placeholder="全部状态"
            style={{ width: 140 }}
            value={statusFilter}
            onChange={(v) => setStatusFilter(v)}
            options={[
              { value: 'completed', label: '完成' },
              { value: 'failed', label: '失败' },
              { value: 'stopped', label: '已停止' },
              { value: 'running', label: '运行中' },
            ]}
          />
          <Button
            size="small"
            onClick={() => {
              setStatusFilter(undefined)
              setScenarioFilter(undefined)
            }}
          >
            重置筛选
          </Button>
        </Space>
      </Card>

      <Row gutter={[16, 16]}>
        {/* ====== 左侧：测试结果列表 ====== */}
        <Col xs={24} lg={compareMode ? 24 : 10} xl={compareMode ? 24 : 8}>
          <Card
            title={compareMode ? '选择要对比的测试结果（多选）' : '测试结果历史'}
            size="small"
            style={{ marginBottom: 16 }}
            bodyStyle={{ padding: 0 }}
          >
            {compareMode ? (
              <div style={{ padding: 12 }}>
                <Checkbox.Group
                  style={{ width: '100%' }}
                  value={compareIds}
                  onChange={(checkedValues) => {
                    handleCompareSelect(checkedValues as number[])
                  }}
                >
                  <div style={{ maxHeight: 480, overflowY: 'auto' }}>
                    {results.map(r => (
                      <div
                        key={r.id}
                        style={{
                          padding: '6px 0',
                          borderBottom: '1px solid #f0f0f0',
                        }}
                      >
                        <Checkbox value={r.id}>
                          <Space size={4}>
                            <Text code style={{ fontSize: 12 }}>#{r.id}</Text>
                            <Text style={{ fontSize: 12 }}>
                              {r.user_count}用户 | {r.rps?.toFixed(0) ?? '-'} RPS | {r.avg_response_time?.toFixed(0) ?? '-'}ms
                            </Text>
                            <Tag
                              color={r.status === 'completed' ? 'success' : r.status === 'failed' ? 'error' : 'warning'}
                              style={{ fontSize: 11, lineHeight: '16px', padding: '0 4px' }}
                            >
                              {r.status === 'completed' ? '完成' : r.status === 'failed' ? '失败' : r.status}
                            </Tag>
                          </Space>
                        </Checkbox>
                      </div>
                    ))}
                  </div>
                </Checkbox.Group>
                {compareIds.length > 0 && (
                  <div style={{ marginTop: 8, textAlign: 'center' }}>
                    <Text type="secondary" style={{ fontSize: 12 }}>
                      已选择 {compareIds.length} 个结果进行对比
                    </Text>
                  </div>
                )}
              </div>
            ) : (
              <Table
                columns={resultColumns.filter(c => c.key !== 'scenario_id')}
                dataSource={results}
                rowKey="id"
                size="small"
                loading={resultsLoading}
                pagination={{
                  current: currentPage,
                  total: totalResults,
                  pageSize: 15,
                  showTotal: (total) => `共 ${total} 条`,
                  onChange: (page) => fetchResults(page),
                  size: 'small',
                }}
                onRow={(record) => ({
                  onClick: () => handleSelectResult(record.id),
                  style: {
                    cursor: 'pointer',
                    background: selectedResultId === record.id ? '#e6f7ff' : undefined,
                  },
                })}
                scroll={{ x: 700 }}
              />
            )}
          </Card>
        </Col>

        {/* ====== 右侧：图表区域 ====== */}
        <Col xs={24} lg={compareMode ? 24 : 14} xl={compareMode ? 24 : 16}>
          {compareMode ? (
            /* ---- 历史对比视图 ---- */
            <div>
              {compareData.length === 0 ? (
                <Card>
                  <Empty description="请在左侧选择至少 1 个测试结果进行对比" />
                </Card>
              ) : (
                <>
                  {/* 对比汇总表 */}
                  <Card title={`对比汇总（${compareData.length} 次运行）`} size="small" style={{ marginBottom: 16 }}>
                    <Table
                      dataSource={compareData}
                      rowKey="id"
                      size="small"
                      pagination={false}
                      scroll={{ x: 800 }}
                      columns={[
                        {
                          title: 'ID',
                          dataIndex: 'id',
                          width: 60,
                          render: (id: number) => <Text code>#{id}</Text>,
                        },
                        {
                          title: '并发',
                          dataIndex: 'user_count',
                          width: 60,
                        },
                        {
                          title: 'RPS',
                          dataIndex: 'rps',
                          width: 80,
                          render: (v: number) => v?.toFixed(1) ?? '-',
                        },
                        {
                          title: '平均 RT (ms)',
                          dataIndex: 'avg_response_time',
                          width: 100,
                          render: (v: number) => v?.toFixed(0) ?? '-',
                        },
                        {
                          title: 'P95 (ms)',
                          dataIndex: 'p95_response_time',
                          width: 80,
                          render: (v: number) => <Text style={{ color: COLORS.p95 }}>{v?.toFixed(0) ?? '-'}</Text>,
                        },
                        {
                          title: 'P99 (ms)',
                          dataIndex: 'p99_response_time',
                          width: 80,
                          render: (v: number) => <Text style={{ color: COLORS.p99 }}>{v?.toFixed(0) ?? '-'}</Text>,
                        },
                        {
                          title: '错误率',
                          dataIndex: 'error_rate',
                          width: 80,
                          render: (v: number) => {
                            const color = v < 1 ? COLORS.success : v < 5 ? COLORS.stopped : COLORS.failed
                            return <Text style={{ color }}>{v?.toFixed(2) ?? '-'}%</Text>
                          },
                        },
                        {
                          title: '状态',
                          dataIndex: 'status',
                          width: 70,
                          render: (s: string) => (
                            <Tag color={s === 'completed' ? 'success' : s === 'failed' ? 'error' : 'warning'}>
                              {s === 'completed' ? '完成' : s === 'failed' ? '失败' : s}
                            </Tag>
                          ),
                        },
                        {
                          title: '时间',
                          dataIndex: 'created_at',
                          width: 130,
                          render: (t: string) => t ? new Date(t).toLocaleString() : '-',
                        },
                      ]}
                    />
                  </Card>

                  <Row gutter={[16, 16]}>
                    <Col xs={24} lg={12}>
                      <Card title="RPS 对比" size="small">
                        <ReactECharts option={compareRpsOption} style={{ height: 280 }} />
                      </Card>
                    </Col>
                    <Col xs={24} lg={12}>
                      <Card title="响应时间对比 (含 P95/P99)" size="small">
                        <ReactECharts option={compareResponseTimeOption} style={{ height: 280 }} />
                      </Card>
                    </Col>
                    <Col span={24}>
                      <Card title="错误率对比" size="small">
                        <ReactECharts option={compareErrorRateOption} style={{ height: 240 }} />
                      </Card>
                    </Col>
                  </Row>
                </>
              )}
            </div>
          ) : (
            /* ---- 单次运行详情 ---- */
            <div>
              {!selectedResultId ? (
                <Card>
                  <Empty description="请在左侧选择一个测试结果查看详细大盘" />
                </Card>
              ) : metricsLoading ? (
                <Card>
                  <div style={{ textAlign: 'center', padding: 40 }}>
                    <Spin size="large" tip="加载指标数据..." />
                  </div>
                </Card>
              ) : (
                <>
                  {/* 汇总指标卡片 */}
                  <Row gutter={[12, 12]} style={{ marginBottom: 16 }}>
                    <Col xs={12} sm={8} lg={4}>
                      <Card size="small">
                        <Statistic
                          title="RPS"
                          value={summaryStats.avgRps}
                          prefix={<ThunderboltOutlined style={{ color: COLORS.rps }} />}
                        />
                      </Card>
                    </Col>
                    <Col xs={12} sm={8} lg={4}>
                      <Card size="small">
                        <Statistic
                          title="平均响应"
                          value={summaryStats.avgRT}
                          suffix="ms"
                          prefix={<ClockCircleOutlined style={{ color: COLORS.avgRT }} />}
                        />
                      </Card>
                    </Col>
                    <Col xs={12} sm={8} lg={4}>
                      <Card size="small">
                        <Statistic
                          title="P95"
                          value={summaryStats.p95}
                          suffix="ms"
                          valueStyle={{ color: COLORS.p95 }}
                          prefix={<WarningOutlined style={{ color: COLORS.p95 }} />}
                        />
                      </Card>
                    </Col>
                    <Col xs={12} sm={8} lg={4}>
                      <Card size="small">
                        <Statistic
                          title="P99"
                          value={summaryStats.p99}
                          suffix="ms"
                          valueStyle={{ color: COLORS.p99 }}
                          prefix={<WarningOutlined style={{ color: COLORS.p99 }} />}
                        />
                      </Card>
                    </Col>
                    <Col xs={12} sm={8} lg={4}>
                      <Card size="small">
                        <Statistic
                          title="错误率"
                          value={summaryStats.errorRate}
                          suffix="%"
                          valueStyle={{ color: summaryStats.errorRate > 5 ? COLORS.failed : COLORS.success }}
                          prefix={
                            summaryStats.errorRate > 5
                              ? <CloseCircleOutlined />
                              : <CheckCircleOutlined />
                          }
                        />
                      </Card>
                    </Col>
                    <Col xs={12} sm={8} lg={4}>
                      <Card size="small">
                        <Statistic
                          title="采样点"
                          value={currentMetrics.length}
                          prefix={<ApartmentOutlined style={{ color: '#722ed1' }} />}
                        />
                      </Card>
                    </Col>
                  </Row>

                  {/* 图表 */}
                  <Row gutter={[16, 16]}>
                    <Col xs={24} lg={12}>
                      <Card title="RPS & 并发用户" size="small">
                        <ReactECharts option={rpsChartOption} style={{ height: 300 }} />
                      </Card>
                    </Col>
                    <Col xs={24} lg={12}>
                      <Card
                        title={
                          <Space>
                            <span>响应时间趋势</span>
                            <Tooltip title="P95/P99 汇总线来自测试结果的最终统计值">
                              <Text type="secondary" style={{ fontSize: 12 }}>(含 P95/P99)</Text>
                            </Tooltip>
                          </Space>
                        }
                        size="small"
                      >
                        <ReactECharts option={responseTimeChartOption} style={{ height: 300 }} />
                      </Card>
                    </Col>
                    <Col span={24}>
                      <Card title="错误率趋势" size="small">
                        <ReactECharts option={errorRateChartOption} style={{ height: 240 }} />
                      </Card>
                    </Col>
                  </Row>

                  {/* 详细指标表格 */}
                  {currentResult && (
                    <Card title="测试结果详情" size="small" style={{ marginTop: 16 }}>
                      <Row gutter={[16, 16]}>
                        <Col span={4}><Statistic title="总请求数" value={currentResult.total_requests} /></Col>
                        <Col span={4}><Statistic title="失败请求数" value={currentResult.total_failures} valueStyle={{ color: COLORS.failed }} /></Col>
                        <Col span={4}><Statistic title="持续时间" value={currentResult.duration} suffix="秒" /></Col>
                        <Col span={4}><Statistic title="并发用户" value={currentResult.user_count} /></Col>
                        <Col span={4}><Statistic title="Min RT" value={currentResult.min_response_time?.toFixed(0)} suffix="ms" /></Col>
                        <Col span={4}><Statistic title="Max RT" value={currentResult.max_response_time?.toFixed(0)} suffix="ms" /></Col>
                        <Col span={4}><Statistic title="P50" value={currentResult.p50_response_time?.toFixed(0)} suffix="ms" /></Col>
                        <Col span={4}><Statistic title="P75" value={currentResult.p75_response_time?.toFixed(0)} suffix="ms" /></Col>
                        <Col span={4}><Statistic title="P95" value={currentResult.p95_response_time?.toFixed(0)} suffix="ms" valueStyle={{ color: COLORS.p95 }} /></Col>
                        <Col span={4}><Statistic title="P99" value={currentResult.p99_response_time?.toFixed(0)} suffix="ms" valueStyle={{ color: COLORS.p99 }} /></Col>
                        <Col span={4}>
                          <Statistic
                            title="状态"
                            value={currentResult.status === 'completed' ? '完成' : currentResult.status === 'failed' ? '失败' : currentResult.status}
                            valueStyle={{ color: currentResult.status === 'completed' ? COLORS.success : currentResult.status === 'failed' ? COLORS.failed : COLORS.stopped }}
                          />
                        </Col>
                        <Col span={4}>
                          <Statistic
                            title="完成时间"
                            value={currentResult.finished_at ? new Date(currentResult.finished_at).toLocaleString() : '-'}
                            valueStyle={{ fontSize: 14 }}
                          />
                        </Col>
                      </Row>
                    </Card>
                  )}
                </>
              )}
            </div>
          )}
        </Col>
      </Row>
    </div>
  )
}

export default PerformanceDashboard