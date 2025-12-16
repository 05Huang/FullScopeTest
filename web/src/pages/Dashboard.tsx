import { useState, useEffect } from 'react'
import { Row, Col, Card, Statistic, Typography, Progress, List, Tag, Empty, message } from 'antd'
import {
  ApiOutlined,
  GlobalOutlined,
  ThunderboltOutlined,
  FileTextOutlined,
  CheckCircleOutlined,
  CloseCircleOutlined,
  ClockCircleOutlined,
  RiseOutlined,
} from '@ant-design/icons'
import ReactECharts from 'echarts-for-react'
import { reportService } from '@/services'

const { Title, Text } = Typography

interface DashboardStats {
  api_tests: { total: number; passed: number; failed: number }
  web_tests: { total: number; passed: number; failed: number }
  perf_tests: { total: number; running: number }
  recent_runs: any[]
}

const Dashboard = () => {
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
      // 获取仪表盘统计数据
      const dashboardRes = await reportService.getDashboardStats()
      if (dashboardRes.code === 200) {
        setStats(dashboardRes.data)
      }

      // 获取趋势数据
      const statsRes = await reportService.getReportStatistics({ days: 7 })
      if (statsRes.code === 200) {
        setDailyTrend(statsRes.data.daily_trend || [])
      }
    } catch (error) {
      message.error('获取数据失败')
    } finally {
      setLoading(false)
    }
  }

  // 计算通过率
  const getPassRate = (passed: number, total: number) => {
    return total > 0 ? Math.round((passed / total) * 100) : 0
  }

  // 测试趋势图配置
  const trendOption = {
    tooltip: {
      trigger: 'axis',
    },
    legend: {
      data: ['通过', '失败'],
      bottom: 0,
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '15%',
      containLabel: true,
    },
    xAxis: {
      type: 'category',
      boundaryGap: false,
      data: dailyTrend.length > 0 
        ? dailyTrend.map(d => d.date) 
        : ['周一', '周二', '周三', '周四', '周五', '周六', '周日'],
    },
    yAxis: {
      type: 'value',
    },
    series: [
      {
        name: '通过',
        type: 'line',
        smooth: true,
        areaStyle: { opacity: 0.3 },
        data: dailyTrend.length > 0 
          ? dailyTrend.map(d => d.passed) 
          : [0, 0, 0, 0, 0, 0, 0],
        itemStyle: { color: '#52c41a' },
      },
      {
        name: '失败',
        type: 'line',
        smooth: true,
        areaStyle: { opacity: 0.3 },
        data: dailyTrend.length > 0 
          ? dailyTrend.map(d => d.failed) 
          : [0, 0, 0, 0, 0, 0, 0],
        itemStyle: { color: '#ff4d4f' },
      },
    ],
  }

  // 测试类型分布图配置
  const distributionOption = {
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
        avoidLabelOverlap: false,
        itemStyle: {
          borderRadius: 10,
          borderColor: '#fff',
          borderWidth: 2,
        },
        label: {
          show: false,
        },
        data: [
          { value: stats.api_tests.total || 0, name: 'API测试', itemStyle: { color: '#2563EB' } },
          { value: stats.web_tests.total || 0, name: 'Web测试', itemStyle: { color: '#7C3AED' } },
          { value: stats.perf_tests.total || 0, name: '性能测试', itemStyle: { color: '#F59E0B' } },
        ],
      },
    ],
  }

  // 状态标签
  const StatusTag = ({ status }: { status: string }) => {
    const config: Record<string, { color: string; icon: React.ReactNode; text: string }> = {
      success: { color: 'success', icon: <CheckCircleOutlined />, text: '成功' },
      passed: { color: 'success', icon: <CheckCircleOutlined />, text: '通过' },
      failed: { color: 'error', icon: <CloseCircleOutlined />, text: '失败' },
      running: { color: 'processing', icon: <ClockCircleOutlined />, text: '执行中' },
      pending: { color: 'default', icon: <ClockCircleOutlined />, text: '等待中' },
    }
    const { color, icon, text } = config[status] || { color: 'default', icon: null, text: status }
    return (
      <Tag color={color} icon={icon}>
        {text}
      </Tag>
    )
  }

  // 类型标签
  const TypeTag = ({ type }: { type: string }) => {
    const config: Record<string, { color: string; text: string }> = {
      api: { color: 'blue', text: 'API' },
      web: { color: 'purple', text: 'Web' },
      performance: { color: 'orange', text: '性能' },
      perf: { color: 'orange', text: '性能' },
    }
    const { color, text } = config[type] || { color: 'default', text: type }
    return <Tag color={color}>{text}</Tag>
  }

  // 格式化时间
  const formatTime = (dateStr: string) => {
    if (!dateStr) return '-'
    const date = new Date(dateStr)
    const now = new Date()
    const diff = now.getTime() - date.getTime()
    const minutes = Math.floor(diff / 60000)
    const hours = Math.floor(diff / 3600000)
    const days = Math.floor(diff / 86400000)
    
    if (minutes < 1) return '刚刚'
    if (minutes < 60) return `${minutes}分钟前`
    if (hours < 24) return `${hours}小时前`
    if (days < 7) return `${days}天前`
    return date.toLocaleDateString()
  }

  return (
    <div>
      <Title level={4} style={{ marginBottom: 24 }}>
        工作台
      </Title>

      {/* 统计卡片 */}
      <Row gutter={[16, 16]} style={{ marginBottom: 24 }}>
        <Col xs={24} sm={12} lg={6}>
          <Card loading={loading}>
            <Statistic
              title={
                <span>
                  <ApiOutlined style={{ marginRight: 8, color: '#2563EB' }} />
                  API测试用例
                </span>
              }
              value={stats.api_tests.total}
              valueStyle={{ color: '#2563EB' }}
              suffix={
                <span style={{ fontSize: 14, color: '#52c41a' }}>
                  <RiseOutlined /> {getPassRate(stats.api_tests.passed, stats.api_tests.total)}%
                </span>
              }
            />
            <Progress
              percent={getPassRate(stats.api_tests.passed, stats.api_tests.total)}
              size="small"
              status="success"
              style={{ marginTop: 8 }}
            />
            <Text type="secondary" style={{ fontSize: 12 }}>
              通过 {stats.api_tests.passed} / 失败 {stats.api_tests.failed}
            </Text>
          </Card>
        </Col>

        <Col xs={24} sm={12} lg={6}>
          <Card loading={loading}>
            <Statistic
              title={
                <span>
                  <GlobalOutlined style={{ marginRight: 8, color: '#7C3AED' }} />
                  Web测试脚本
                </span>
              }
              value={stats.web_tests.total}
              valueStyle={{ color: '#7C3AED' }}
              suffix={
                <span style={{ fontSize: 14, color: '#52c41a' }}>
                  <RiseOutlined /> {getPassRate(stats.web_tests.passed, stats.web_tests.total)}%
                </span>
              }
            />
            <Progress
              percent={getPassRate(stats.web_tests.passed, stats.web_tests.total)}
              size="small"
              status="success"
              style={{ marginTop: 8 }}
            />
            <Text type="secondary" style={{ fontSize: 12 }}>
              通过 {stats.web_tests.passed} / 失败 {stats.web_tests.failed}
            </Text>
          </Card>
        </Col>

        <Col xs={24} sm={12} lg={6}>
          <Card loading={loading}>
            <Statistic
              title={
                <span>
                  <ThunderboltOutlined style={{ marginRight: 8, color: '#F59E0B' }} />
                  性能测试场景
                </span>
              }
              value={stats.perf_tests.total}
              valueStyle={{ color: '#F59E0B' }}
            />
            <div style={{ marginTop: 8 }}>
              <Tag color="processing">{stats.perf_tests.running} 个执行中</Tag>
            </div>
          </Card>
        </Col>

        <Col xs={24} sm={12} lg={6}>
          <Card loading={loading}>
            <Statistic
              title={
                <span>
                  <FileTextOutlined style={{ marginRight: 8, color: '#10B981' }} />
                  最近测试
                </span>
              }
              value={stats.recent_runs.length}
              valueStyle={{ color: '#10B981' }}
            />
            <div style={{ marginTop: 8 }}>
              <Text type="secondary" style={{ fontSize: 12 }}>
                最近执行记录
              </Text>
            </div>
          </Card>
        </Col>
      </Row>

      {/* 图表区域 */}
      <Row gutter={[16, 16]} style={{ marginBottom: 24 }}>
        <Col xs={24} lg={16}>
          <Card title="测试执行趋势" loading={loading}>
            <ReactECharts option={trendOption} style={{ height: 300 }} />
          </Card>
        </Col>

        <Col xs={24} lg={8}>
          <Card title="测试类型分布" loading={loading}>
            <ReactECharts option={distributionOption} style={{ height: 300 }} />
          </Card>
        </Col>
      </Row>

      {/* 最近测试 */}
      <Card title="最近测试执行" loading={loading}>
        {stats.recent_runs.length > 0 ? (
          <List
            dataSource={stats.recent_runs}
            renderItem={(item: any) => (
              <List.Item
                actions={[
                  <Text type="secondary" key="time">
                    {formatTime(item.created_at)}
                  </Text>,
                ]}
              >
                <List.Item.Meta
                  title={
                    <span>
                      <TypeTag type={item.test_type} />
                      <span style={{ marginLeft: 8 }}>{item.test_object_name || `测试 #${item.id}`}</span>
                    </span>
                  }
                />
                <StatusTag status={item.status} />
              </List.Item>
            )}
          />
        ) : (
          <Empty description="暂无测试记录" />
        )}
      </Card>
    </div>
  )
}

export default Dashboard
