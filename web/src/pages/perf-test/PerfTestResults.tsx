import { useTranslation } from 'react-i18next';
import { useState, useEffect } from 'react'
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
  DatePicker,
  Select,
  message,
} from 'antd'
import {
  BarChartOutlined,
  ClockCircleOutlined,
  ThunderboltOutlined,
  CheckCircleOutlined,
  CloseCircleOutlined,
  ReloadOutlined,
} from '@ant-design/icons'
import ReactECharts from 'echarts-for-react'
import type { ColumnsType } from 'antd/es/table'
import { perfTestService } from '@/services/perfTestService'
import dayjs from 'dayjs'

const { Title, Text } = Typography
const { RangePicker } = DatePicker

interface TestResult {
  id: number
  scenario_id: number
  scenario_name: string
  user_count: number
  duration: number
  avg_response_time: number
  p50_response_time: number
  p90_response_time: number
  p95_response_time: number
  p99_response_time: number
  min_response_time: number
  max_response_time: number
  throughput: number
  total_requests: number
  failed_requests: number
  error_rate: number
  status: 'passed' | 'failed'
  created_at: string
}

const PerfTestResults = () => {
  const { t } = useTranslation();
  const [loading, setLoading] = useState(false)
  const [results, setResults] = useState<TestResult[]>([])
  const [selectedResult, setSelectedResult] = useState<TestResult | null>(null)
  const [detailMetrics, setDetailMetrics] = useState<any[]>([])
  const [dateRange, setDateRange] = useState<[dayjs.Dayjs | null, dayjs.Dayjs | null]>([null, null])
  const [statusFilter, setStatusFilter] = useState<string | undefined>(undefined)
  const [statistics, setStatistics] = useState({
    total_tests: 0,
    avg_response_time: 0,
    avg_throughput: 0,
    avg_error_rate: 0,
  })

  useEffect(() => {
    fetchResults()
  }, [dateRange, statusFilter])

  const fetchResults = async () => {
    setLoading(true)
    try {
      const params: any = { per_page: 100 }
      if (dateRange[0]) params.start_date = dateRange[0].format('YYYY-MM-DD')
      if (dateRange[1]) params.end_date = dateRange[1].format('YYYY-MM-DD')
      if (statusFilter) params.status = statusFilter

      const result = await perfTestService.getPerformanceResults(params)
      if (result.code === 200) {
        const items = result.data?.items || result.data || []
        const testResults: TestResult[] = items.map((r: any) => ({
          id: r.id,
          scenario_id: r.scenario_id,
          scenario_name: r.scenario_name || `Scenario #${r.scenario_id}`,
          user_count: r.user_count || 0,
          duration: r.duration || 0,
          avg_response_time: r.avg_response_time || 0,
          p50_response_time: r.p50_response_time || 0,
          p90_response_time: r.p90_response_time || 0,
          p95_response_time: r.p95_response_time || 0,
          p99_response_time: r.p99_response_time || 0,
          min_response_time: r.min_response_time || 0,
          max_response_time: r.max_response_time || 0,
          throughput: r.throughput || 0,
          total_requests: r.total_requests || 0,
          failed_requests: r.failed_requests || 0,
          error_rate: r.error_rate || 0,
          status: r.status || ((r.error_rate || 0) < 5 ? 'passed' : 'failed'),
          created_at: r.created_at || new Date().toISOString(),
        }))

        setResults(testResults)

        if (testResults.length > 0) {
          setStatistics({
            total_tests: testResults.length,
            avg_response_time: Math.round(
              testResults.reduce((sum, r) => sum + r.avg_response_time, 0) / testResults.length
            ),
            avg_throughput: Math.round(
              testResults.reduce((sum, r) => sum + r.throughput, 0) / testResults.length
            ),
            avg_error_rate: parseFloat(
              (testResults.reduce((sum, r) => sum + r.error_rate, 0) / testResults.length).toFixed(2)
            ),
          })
        } else {
          setStatistics({ total_tests: 0, avg_response_time: 0, avg_throughput: 0, avg_error_rate: 0 })
        }
      }
    } catch (error) {
      // Fallback: try getScenarios if getPerformanceResults fails
      try {
        const result = await perfTestService.getScenarios()
        if (result.code === 200) {
          const scenarios = result.data || []
          const testResults: TestResult[] = scenarios
            .filter((s: any) => s.status !== 'pending')
            .map((s: any) => ({
              id: s.id, scenario_id: s.id, scenario_name: s.name,
              user_count: s.user_count || 0, duration: s.duration || 0,
              avg_response_time: s.avg_response_time || 0,
              p50_response_time: 0, p90_response_time: 0, p95_response_time: 0, p99_response_time: 0,
              min_response_time: 0, max_response_time: 0,
              throughput: s.throughput || 0, total_requests: 0, failed_requests: 0,
              error_rate: s.error_rate || 0,
              status: (s.error_rate || 0) < 5 ? 'passed' : 'failed',
              created_at: s.last_run_at || s.updated_at || new Date().toISOString(),
            }))
          setResults(testResults)
          if (testResults.length > 0) {
            setStatistics({
              total_tests: testResults.length,
              avg_response_time: Math.round(testResults.reduce((sum, r) => sum + r.avg_response_time, 0) / testResults.length),
              avg_throughput: Math.round(testResults.reduce((sum, r) => sum + r.throughput, 0) / testResults.length),
              avg_error_rate: parseFloat((testResults.reduce((sum, r) => sum + r.error_rate, 0) / testResults.length).toFixed(2)),
            })
          }
        }
      } catch {
        message.error(t('perfTest.loadFailed'))
      }
    } finally {
      setLoading(false)
    }
  }

  const fetchDetailMetrics = async (resultId: number) => {
    try {
      const res = await perfTestService.getPerformanceResultMetrics(resultId, 100)
      if (res.code === 200) {
        setDetailMetrics(res.data?.items || res.data || [])
      }
    } catch {
      setDetailMetrics([])
    }
  }

  // 响应时间分布图
  const getResponseTimeDistribution = (result: TestResult) => ({
    tooltip: {
      trigger: 'axis',
      axisPointer: { type: 'shadow' },
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      containLabel: true,
    },
    xAxis: {
      type: 'category',
      data: ['Min', 'P50', 'Avg', 'P90', 'P95', 'P99', 'Max'],
    },
    yAxis: {
      type: 'value',
      name: 'ms',
    },
    series: [
      {
        type: 'bar',
        data: [
          { value: result.min_response_time, itemStyle: { color: '#52c41a' } },
          { value: result.p50_response_time, itemStyle: { color: '#1890ff' } },
          { value: result.avg_response_time, itemStyle: { color: '#13c2c2' } },
          { value: result.p90_response_time, itemStyle: { color: '#faad14' } },
          { value: result.p95_response_time, itemStyle: { color: '#fa8c16' } },
          { value: result.p99_response_time, itemStyle: { color: '#fa541c' } },
          { value: result.max_response_time, itemStyle: { color: '#f5222d' } },
        ],
      },
    ],
  })

  // 请求统计饼图
  const getRequestsPie = (result: TestResult) => ({
    tooltip: {
      trigger: 'item',
    },
    legend: {
      bottom: 0,
    },
    series: [
      {
        type: 'pie',
        radius: ['40%', '70%'],
        data: [
          {
            value: result.total_requests - result.failed_requests,
            name: t('perfTest.successRequests'),
            itemStyle: { color: '#52c41a' },
          },
          {
            value: result.failed_requests,
            name: t('perfTest.failedRequests'),
            itemStyle: { color: '#f5222d' },
          },
        ],
      },
    ],
  })

  const columns: ColumnsType<TestResult> = [
    {
      title: t('perfTest.scenarioNameCol'),
      dataIndex: 'scenario_name',
      key: 'scenario_name',
      render: (text) => <Text strong>{text}</Text>,
    },
    {
      title: t('perfTest.userCountCol'),
      dataIndex: 'user_count',
      key: 'user_count',
      width: 100,
      render: (val) => `${val} ${t('perfTest.concurrentUsers')}`,
    },
    {
      title: t('perfTest.avgResponseTime'),
      dataIndex: 'avg_response_time',
      key: 'avg_response_time',
      width: 130,
      render: (val) => {
        const color = val < 500 ? '#52c41a' : val < 1500 ? '#faad14' : '#f5222d'
        return <Text style={{ color }}>{val} ms</Text>
      },
    },
    {
      title: t('perfTest.throughput'),
      dataIndex: 'throughput',
      key: 'throughput',
      width: 120,
      render: (val) => `${val} req/s`,
    },
    {
      title: t('perfTest.errorRate'),
      dataIndex: 'error_rate',
      key: 'error_rate',
      width: 100,
      render: (val) => {
        const color = val < 1 ? '#52c41a' : val < 5 ? '#faad14' : '#f5222d'
        return <Text style={{ color }}>{val.toFixed(2)}%</Text>
      },
    },
    {
      title: t('common.status'),
      dataIndex: 'status',
      key: 'status',
      width: 100,
      render: (status) => (
        <Tag color={status === 'passed' ? 'success' : 'error'}>
          {status === 'passed' ? (t('common.passed')) : t('common.failed')}
        </Tag>
      ),
    },
    {
      title: t('reports.executionTime'),
      dataIndex: 'created_at',
      key: 'created_at',
      width: 160,
      render: (time) => new Date(time).toLocaleString(),
    },
    {
      title: t('common.actions'),
      key: 'action',
      width: 100,
      render: (_, record) => (
        <Button type="link" onClick={() => setSelectedResult(record)}>
          {t('perfTest.viewDetail')}
        </Button>
      ),
    },
  ]

  return (
    <div className="fst-page">
      <div className="fst-page-header fst-animate-in">
        <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
          <div className="fst-stat-icon fst-stat-icon--info"><BarChartOutlined style={{ fontSize: 18 }} /></div>
          <h1 className="fst-page-title">{t('perfTest.resultAnalysis')}</h1>
        </div>
        <div style={{ display: 'flex', gap: 8, alignItems: 'center' }}>
          <Select
            placeholder={t('perfTest.allStatus')}
            size="small"
            style={{ width: 120 }}
            allowClear
            value={statusFilter}
            onChange={(val) => setStatusFilter(val)}
            options={[
              { value: 'passed', label: t('common.passed') },
              { value: 'failed', label: t('common.failed') },
            ]}
          />
          <RangePicker
            size="small"
            onChange={(dates) => {
              setDateRange(dates ? [dates[0], dates[1]] : [null, null])
            }}
          />
          <button className="fst-btn fst-btn--ghost fst-btn--sm" onClick={fetchResults}><ReloadOutlined /> {t('common.refresh')}</button>
        </div>
      </div>

      {/* 统计概览 */}
      <Row gutter={16} style={{ marginBottom: 24 }}>
        <Col span={6}>
          <Card>
            <Statistic
              title={t('perfTest.totalTests')}
              value={statistics.total_tests}
              prefix={<BarChartOutlined style={{ color: '#1890ff' }} />}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title={t('perfTest.avgResponseTime')}
              value={statistics.avg_response_time}
              suffix="ms"
              prefix={<ClockCircleOutlined style={{ color: '#faad14' }} />}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title={t('perfTest.avgThroughput')}
              value={statistics.avg_throughput}
              suffix="req/s"
              prefix={<ThunderboltOutlined style={{ color: '#52c41a' }} />}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title={t('perfTest.avgErrorRate')}
              value={statistics.avg_error_rate}
              suffix="%"
              valueStyle={{
                color: statistics.avg_error_rate > 5 ? '#f5222d' : '#52c41a',
              }}
              prefix={
                statistics.avg_error_rate > 5 ? (
                  <CloseCircleOutlined />
                ) : (
                  <CheckCircleOutlined />
                )
              }
            />
          </Card>
        </Col>
      </Row>

      {/* 测试结果列表 */}
      <Card title={t('perfTest.resultsList')} style={{ marginBottom: 24 }}>
        {results.length > 0 ? (
          <Table
            columns={columns}
            dataSource={results}
            rowKey="id"
            loading={loading}
            pagination={{
              total: results.length,
              showTotal: (total) => `${t('common.total')} ${total}`,
              showSizeChanger: true,
            }}
          />
        ) : (
          <Empty description={t('perfTest.noResults')} />
        )}
      </Card>

      {/* 详情分析 */}
      {selectedResult && (
        <Card
          title={`${t('perfTest.resultAnalysis')} - ${selectedResult.scenario_name}`}
          extra={
            <Space>
              {/* P39-4: 结果导出 */}
              <Button size="small" onClick={() => {
                try {
                  const csv = ['指标,值', ...detailMetrics.map(m => `${m.metric},${m.value}`)].join('\n')
                  const blob = new Blob([csv], { type: 'text/csv' })
                  const url = URL.createObjectURL(blob)
                  const a = document.createElement('a')
                  a.href = url; a.download = `perf-result-${selectedResult.scenario_name}.csv`; a.click()
                  URL.revokeObjectURL(url)
                  message.success('导出成功')
                } catch { message.error('导出失败') }
              }}>导出 CSV</Button>
              <Button type="text" onClick={() => { setSelectedResult(null); setDetailMetrics([]) }}>
                {t('common.close')}
              </Button>
            </Space>
          }
        >
          <Row gutter={16}>
            <Col span={16}>
              <Card title={t('perfTest.responseTimeDistribution')} size="small">
                <ReactECharts
                  option={getResponseTimeDistribution(selectedResult)}
                  style={{ height: 300 }}
                />
              </Card>
            </Col>
            <Col span={8}>
              <Card title={t('perfTest.requestStats')} size="small">
                <ReactECharts
                  option={getRequestsPie(selectedResult)}
                  style={{ height: 300 }}
                />
              </Card>
            </Col>
          </Row>

          <Card title={t('perfTest.detailedMetrics')} size="small" style={{ marginTop: 16 }}>
            <Row gutter={[16, 16]}>
              <Col span={6}>
                <Statistic title={t('perfTest.totalRequestsCol')} value={selectedResult.total_requests} />
              </Col>
              <Col span={6}>
                <Statistic title={t('perfTest.failedRequestsCol')} value={selectedResult.failed_requests} valueStyle={{ color: '#f5222d' }} />
              </Col>
              <Col span={6}>
                <Statistic title={t('perfTest.durationSec')} value={selectedResult.duration} suffix="s" />
              </Col>
              <Col span={6}>
                <Statistic title={t('perfTest.concurrentUsersCol')} value={selectedResult.user_count} />
              </Col>
              <Col span={4}>
                <Statistic title="Min" value={selectedResult.min_response_time} suffix="ms" />
              </Col>
              <Col span={4}>
                <Statistic title="P50" value={selectedResult.p50_response_time.toFixed(0)} suffix="ms" />
              </Col>
              <Col span={4}>
                <Statistic title="P90" value={selectedResult.p90_response_time.toFixed(0)} suffix="ms" />
              </Col>
              <Col span={4}>
                <Statistic title="P95" value={selectedResult.p95_response_time.toFixed(0)} suffix="ms" />
              </Col>
              <Col span={4}>
                <Statistic title="P99" value={selectedResult.p99_response_time.toFixed(0)} suffix="ms" />
              </Col>
              <Col span={4}>
                <Statistic title="Max" value={selectedResult.max_response_time.toFixed(0)} suffix="ms" />
              </Col>
            </Row>
          </Card>
        </Card>
      )}
    </div>
  )
}

export default PerfTestResults
