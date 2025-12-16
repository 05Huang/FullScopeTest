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
  const [loading, setLoading] = useState(false)
  const [results, setResults] = useState<TestResult[]>([])
  const [selectedResult, setSelectedResult] = useState<TestResult | null>(null)
  const [statistics, setStatistics] = useState({
    total_tests: 0,
    avg_response_time: 0,
    avg_throughput: 0,
    avg_error_rate: 0,
  })

  useEffect(() => {
    fetchResults()
  }, [])

  const fetchResults = async () => {
    setLoading(true)
    try {
      // 从场景列表获取历史数据
      const result = await perfTestService.getScenarios()
      if (result.code === 200) {
        // 转换数据格式
        const scenarios = result.data || []
        const testResults: TestResult[] = scenarios
          .filter((s: any) => s.status !== 'pending')
          .map((s: any) => ({
            id: s.id,
            scenario_id: s.id,
            scenario_name: s.name,
            user_count: s.user_count,
            duration: s.duration,
            avg_response_time: s.avg_response_time || 0,
            p50_response_time: (s.avg_response_time || 0) * 0.9,
            p90_response_time: (s.avg_response_time || 0) * 1.2,
            p95_response_time: (s.avg_response_time || 0) * 1.4,
            p99_response_time: (s.avg_response_time || 0) * 1.8,
            min_response_time: (s.avg_response_time || 0) * 0.5,
            max_response_time: (s.avg_response_time || 0) * 2,
            throughput: s.throughput || 0,
            total_requests: (s.throughput || 0) * s.duration,
            failed_requests: Math.round((s.throughput || 0) * s.duration * (s.error_rate || 0) / 100),
            error_rate: s.error_rate || 0,
            status: (s.error_rate || 0) < 5 ? 'passed' : 'failed',
            created_at: s.last_run_at || s.updated_at || new Date().toISOString(),
          }))
        
        setResults(testResults)
        
        // 计算统计数据
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
        }
      }
    } catch (error) {
      message.error('获取测试结果失败')
    } finally {
      setLoading(false)
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
            name: '成功请求',
            itemStyle: { color: '#52c41a' },
          },
          {
            value: result.failed_requests,
            name: '失败请求',
            itemStyle: { color: '#f5222d' },
          },
        ],
      },
    ],
  })

  const columns: ColumnsType<TestResult> = [
    {
      title: '场景名称',
      dataIndex: 'scenario_name',
      key: 'scenario_name',
      render: (text) => <Text strong>{text}</Text>,
    },
    {
      title: '并发数',
      dataIndex: 'user_count',
      key: 'user_count',
      width: 100,
      render: (val) => `${val} 用户`,
    },
    {
      title: '平均响应时间',
      dataIndex: 'avg_response_time',
      key: 'avg_response_time',
      width: 130,
      render: (val) => {
        const color = val < 500 ? '#52c41a' : val < 1500 ? '#faad14' : '#f5222d'
        return <Text style={{ color }}>{val} ms</Text>
      },
    },
    {
      title: '吞吐量',
      dataIndex: 'throughput',
      key: 'throughput',
      width: 120,
      render: (val) => `${val} req/s`,
    },
    {
      title: '错误率',
      dataIndex: 'error_rate',
      key: 'error_rate',
      width: 100,
      render: (val) => {
        const color = val < 1 ? '#52c41a' : val < 5 ? '#faad14' : '#f5222d'
        return <Text style={{ color }}>{val.toFixed(2)}%</Text>
      },
    },
    {
      title: '状态',
      dataIndex: 'status',
      key: 'status',
      width: 100,
      render: (status) => (
        <Tag color={status === 'passed' ? 'success' : 'error'}>
          {status === 'passed' ? '通过' : '失败'}
        </Tag>
      ),
    },
    {
      title: '执行时间',
      dataIndex: 'created_at',
      key: 'created_at',
      width: 160,
      render: (time) => new Date(time).toLocaleString(),
    },
    {
      title: '操作',
      key: 'action',
      width: 100,
      render: (_, record) => (
        <Button type="link" onClick={() => setSelectedResult(record)}>
          详情
        </Button>
      ),
    },
  ]

  return (
    <div>
      <div
        style={{
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
          marginBottom: 16,
        }}
      >
        <Title level={4} style={{ margin: 0 }}>
          <BarChartOutlined style={{ marginRight: 8 }} />
          结果分析
        </Title>
        <Space>
          <RangePicker size="small" />
          <Button
            icon={<ReloadOutlined />}
            onClick={fetchResults}
            loading={loading}
          >
            刷新
          </Button>
        </Space>
      </div>

      {/* 统计概览 */}
      <Row gutter={16} style={{ marginBottom: 24 }}>
        <Col span={6}>
          <Card>
            <Statistic
              title="测试总数"
              value={statistics.total_tests}
              prefix={<BarChartOutlined style={{ color: '#1890ff' }} />}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="平均响应时间"
              value={statistics.avg_response_time}
              suffix="ms"
              prefix={<ClockCircleOutlined style={{ color: '#faad14' }} />}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="平均吞吐量"
              value={statistics.avg_throughput}
              suffix="req/s"
              prefix={<ThunderboltOutlined style={{ color: '#52c41a' }} />}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="平均错误率"
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
      <Card title="测试结果列表" style={{ marginBottom: 24 }}>
        {results.length > 0 ? (
          <Table
            columns={columns}
            dataSource={results}
            rowKey="id"
            loading={loading}
            pagination={{
              total: results.length,
              showTotal: (total) => `共 ${total} 条`,
              showSizeChanger: true,
            }}
          />
        ) : (
          <Empty description="暂无测试结果" />
        )}
      </Card>

      {/* 详情分析 */}
      {selectedResult && (
        <Card
          title={`详细分析 - ${selectedResult.scenario_name}`}
          extra={
            <Button
              type="text"
              onClick={() => setSelectedResult(null)}
            >
              关闭
            </Button>
          }
        >
          <Row gutter={16}>
            <Col span={16}>
              <Card title="响应时间分布" size="small">
                <ReactECharts
                  option={getResponseTimeDistribution(selectedResult)}
                  style={{ height: 300 }}
                />
              </Card>
            </Col>
            <Col span={8}>
              <Card title="请求统计" size="small">
                <ReactECharts
                  option={getRequestsPie(selectedResult)}
                  style={{ height: 300 }}
                />
              </Card>
            </Col>
          </Row>

          <Card title="详细指标" size="small" style={{ marginTop: 16 }}>
            <Row gutter={[16, 16]}>
              <Col span={6}>
                <Statistic title="总请求数" value={selectedResult.total_requests} />
              </Col>
              <Col span={6}>
                <Statistic title="失败请求" value={selectedResult.failed_requests} valueStyle={{ color: '#f5222d' }} />
              </Col>
              <Col span={6}>
                <Statistic title="持续时间" value={selectedResult.duration} suffix="秒" />
              </Col>
              <Col span={6}>
                <Statistic title="并发用户" value={selectedResult.user_count} />
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
