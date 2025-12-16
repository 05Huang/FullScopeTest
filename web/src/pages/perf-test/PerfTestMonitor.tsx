import { useState, useEffect } from 'react'
import {
  Card,
  Row,
  Col,
  Statistic,
  Typography,
  Progress,
  Table,
  Tag,
  Empty,
  Button,
} from 'antd'
import {
  DashboardOutlined,
  UserOutlined,
  ClockCircleOutlined,
  ThunderboltOutlined,
  CheckCircleOutlined,
  CloseCircleOutlined,
  SyncOutlined,
  ReloadOutlined,
} from '@ant-design/icons'
import ReactECharts from 'echarts-for-react'
import { perfTestService } from '@/services/perfTestService'

const { Title, Text } = Typography

interface RunningTest {
  id: number
  name: string
  user_count: number
  duration: number
  elapsed: number
  status: string
  avg_response_time: number
  throughput: number
  error_rate: number
}

const PerfTestMonitor = () => {
  const [loading, setLoading] = useState(false)
  const [runningTests, setRunningTests] = useState<RunningTest[]>([])
  const [selectedTest, setSelectedTest] = useState<RunningTest | null>(null)
  const [realtimeData] = useState<any[]>([])

  useEffect(() => {
    fetchRunningTests()
    
    // 定时刷新
    const interval = setInterval(fetchRunningTests, 5000)
    return () => clearInterval(interval)
  }, [])

  const fetchRunningTests = async () => {
    setLoading(true)
    try {
      const result = await perfTestService.getRunningTests()
      if (result.code === 200) {
        setRunningTests(result.data || [])
        // 如果有运行中的测试且未选择，默认选择第一个
        if (result.data?.length > 0 && !selectedTest) {
          setSelectedTest(result.data[0])
        }
      }
    } catch (error) {
      console.error('获取运行中测试失败', error)
    } finally {
      setLoading(false)
    }
  }

  // 响应时间趋势图配置
  const responseTimeOption = {
    tooltip: {
      trigger: 'axis',
    },
    legend: {
      data: ['平均响应时间', 'P95响应时间'],
      bottom: 0,
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '15%',
      top: '10%',
      containLabel: true,
    },
    xAxis: {
      type: 'category',
      data: realtimeData.length > 0
        ? realtimeData.map((_, i) => `${i * 5}s`)
        : ['0s', '5s', '10s', '15s', '20s', '25s', '30s'],
    },
    yAxis: {
      type: 'value',
      name: 'ms',
    },
    series: [
      {
        name: '平均响应时间',
        type: 'line',
        smooth: true,
        data: realtimeData.length > 0
          ? realtimeData.map(d => d.avg_response_time)
          : [0, 0, 0, 0, 0, 0, 0],
        itemStyle: { color: '#1890ff' },
        areaStyle: { opacity: 0.1 },
      },
      {
        name: 'P95响应时间',
        type: 'line',
        smooth: true,
        data: realtimeData.length > 0
          ? realtimeData.map(d => d.p95_response_time)
          : [0, 0, 0, 0, 0, 0, 0],
        itemStyle: { color: '#faad14' },
        areaStyle: { opacity: 0.1 },
      },
    ],
  }

  // 吞吐量趋势图配置
  const throughputOption = {
    tooltip: {
      trigger: 'axis',
    },
    legend: {
      data: ['吞吐量', '错误率'],
      bottom: 0,
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '15%',
      top: '10%',
      containLabel: true,
    },
    xAxis: {
      type: 'category',
      data: realtimeData.length > 0
        ? realtimeData.map((_, i) => `${i * 5}s`)
        : ['0s', '5s', '10s', '15s', '20s', '25s', '30s'],
    },
    yAxis: [
      {
        type: 'value',
        name: 'req/s',
        position: 'left',
      },
      {
        type: 'value',
        name: '%',
        position: 'right',
        max: 100,
      },
    ],
    series: [
      {
        name: '吞吐量',
        type: 'bar',
        data: realtimeData.length > 0
          ? realtimeData.map(d => d.throughput)
          : [0, 0, 0, 0, 0, 0, 0],
        itemStyle: { color: '#52c41a' },
      },
      {
        name: '错误率',
        type: 'line',
        yAxisIndex: 1,
        data: realtimeData.length > 0
          ? realtimeData.map(d => d.error_rate)
          : [0, 0, 0, 0, 0, 0, 0],
        itemStyle: { color: '#ff4d4f' },
      },
    ],
  }

  // 运行中测试表格列
  const columns = [
    {
      title: '场景名称',
      dataIndex: 'name',
      key: 'name',
    },
    {
      title: '并发数',
      dataIndex: 'user_count',
      key: 'user_count',
      render: (val: number) => `${val} 用户`,
    },
    {
      title: '进度',
      key: 'progress',
      render: (_: any, record: RunningTest) => (
        <Progress
          percent={Math.round((record.elapsed / record.duration) * 100)}
          size="small"
          status="active"
        />
      ),
    },
    {
      title: '状态',
      dataIndex: 'status',
      key: 'status',
      render: () => (
        <Tag color="processing" icon={<SyncOutlined spin />}>
          执行中
        </Tag>
      ),
    },
    {
      title: '操作',
      key: 'action',
      render: (_: any, record: RunningTest) => (
        <Button
          type="link"
          size="small"
          onClick={() => setSelectedTest(record)}
        >
          查看详情
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
          <DashboardOutlined style={{ marginRight: 8 }} />
          实时监控
        </Title>
        <Button
          icon={<ReloadOutlined />}
          onClick={fetchRunningTests}
          loading={loading}
        >
          刷新
        </Button>
      </div>

      {runningTests.length === 0 ? (
        <Card>
          <Empty
            description={
              <span>
                暂无运行中的性能测试
                <br />
                <Text type="secondary">在"场景管理"中启动测试后，可在此查看实时监控数据</Text>
              </span>
            }
          />
        </Card>
      ) : (
        <>
          {/* 运行中的测试列表 */}
          <Card title="运行中的测试" style={{ marginBottom: 24 }}>
            <Table
              columns={columns}
              dataSource={runningTests}
              rowKey="id"
              pagination={false}
            />
          </Card>

          {selectedTest && (
            <>
              {/* 实时统计 */}
              <Row gutter={16} style={{ marginBottom: 24 }}>
                <Col span={6}>
                  <Card>
                    <Statistic
                      title="当前并发用户"
                      value={selectedTest.user_count}
                      prefix={<UserOutlined style={{ color: '#1890ff' }} />}
                    />
                  </Card>
                </Col>
                <Col span={6}>
                  <Card>
                    <Statistic
                      title="平均响应时间"
                      value={selectedTest.avg_response_time || 0}
                      suffix="ms"
                      prefix={<ClockCircleOutlined style={{ color: '#faad14' }} />}
                    />
                  </Card>
                </Col>
                <Col span={6}>
                  <Card>
                    <Statistic
                      title="吞吐量"
                      value={selectedTest.throughput || 0}
                      suffix="req/s"
                      prefix={<ThunderboltOutlined style={{ color: '#52c41a' }} />}
                    />
                  </Card>
                </Col>
                <Col span={6}>
                  <Card>
                    <Statistic
                      title="错误率"
                      value={selectedTest.error_rate || 0}
                      suffix="%"
                      valueStyle={{
                        color: (selectedTest.error_rate || 0) > 5 ? '#ff4d4f' : '#52c41a',
                      }}
                      prefix={
                        (selectedTest.error_rate || 0) > 5 ? (
                          <CloseCircleOutlined />
                        ) : (
                          <CheckCircleOutlined />
                        )
                      }
                    />
                  </Card>
                </Col>
              </Row>

              {/* 实时图表 */}
              <Row gutter={16}>
                <Col span={12}>
                  <Card title="响应时间趋势">
                    <ReactECharts option={responseTimeOption} style={{ height: 300 }} />
                  </Card>
                </Col>
                <Col span={12}>
                  <Card title="吞吐量与错误率">
                    <ReactECharts option={throughputOption} style={{ height: 300 }} />
                  </Card>
                </Col>
              </Row>
            </>
          )}
        </>
      )}
    </div>
  )
}

export default PerfTestMonitor
