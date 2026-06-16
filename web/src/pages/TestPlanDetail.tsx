/**
 * 测试计划详情页面
 *
 * 展示计划信息、运行历史、用例列表和通过率趋势。
 */
import { useState, useEffect, useCallback } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import {
  Card,
  Table,
  Button,
  Tabs,
  Tag,
  Space,
  Typography,
  Spin,
  Result,
  Empty,
  message,
  Progress,
} from 'antd'
import {
  ArrowLeftOutlined,
  PlayCircleOutlined,
  HistoryOutlined,
  UnorderedListOutlined,
  LineChartOutlined,
} from '@ant-design/icons'
import { useTranslation } from 'react-i18next'
import type { ColumnsType } from 'antd/es/table'
import ReactECharts from 'echarts-for-react'
import testPlanService, { TestPlan, TestPlanRun, TrendPoint } from '@/services/testPlanService'

const { Title, Text } = Typography

const TestPlanDetail = () => {
  const { planId } = useParams<{ planId: string }>()
  const navigate = useNavigate()
  const { t } = useTranslation()
  const [plan, setPlan] = useState<TestPlan | null>(null)
  const [runs, setRuns] = useState<TestPlanRun[]>([])
  const [runsTotal, setRunsTotal] = useState(0)
  const [trend, setTrend] = useState<TrendPoint[]>([])
  const [loading, setLoading] = useState(true)
  const [runsLoading, setRunsLoading] = useState(false)
  const [activeTab, setActiveTab] = useState('runs')

  const planIdNum = planId ? parseInt(planId, 10) : null

  const fetchPlan = useCallback(async () => {
    if (!planIdNum) return
    setLoading(true)
    try {
      const res = await testPlanService.getTestPlan(planIdNum)
      if (res.code === 200 && res.data) {
        setPlan(res.data)
      }
    } catch {
      message.error(t('testPlans.fetchFailed'))
    } finally {
      setLoading(false)
    }
  }, [planIdNum, t])

  const fetchRuns = useCallback(async () => {
    if (!planIdNum) return
    setRunsLoading(true)
    try {
      const res = await testPlanService.getTestPlanRuns(planIdNum, { per_page: 50 })
      if (res.code === 200 && res.data) {
        setRuns(res.data.items || [])
        setRunsTotal(res.data.total || 0)
      }
    } catch {
      message.error(t('testPlans.fetchRunsFailed'))
    } finally {
      setRunsLoading(false)
    }
  }, [planIdNum, t])

  const fetchTrend = useCallback(async () => {
    if (!planIdNum) return
    try {
      const res = await testPlanService.getPassRateTrend(planIdNum, 20)
      if (res.code === 200 && res.data) {
        setTrend(res.data || [])
      }
    } catch {
      // 趋势数据非关键，静默失败
    }
  }, [planIdNum])

  useEffect(() => {
    fetchPlan()
    fetchRuns()
    fetchTrend()
  }, [fetchPlan, fetchRuns, fetchTrend])

  const handleRun = async () => {
    if (!planIdNum) return
    try {
      const res = await testPlanService.createTestPlanRun(planIdNum)
      if (res.code === 200 || res.code === 201) {
        message.success(t('testPlans.runCreated'))
        await fetchRuns()
      } else {
        message.error(res.message || t('testPlans.runFailed'))
      }
    } catch {
      message.error(t('testPlans.runFailed'))
    }
  }

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'completed': return 'green'
      case 'running': return 'blue'
      case 'failed': return 'red'
      case 'pending': return 'default'
      default: return 'default'
    }
  }

  const runColumns: ColumnsType<TestPlanRun> = [
    {
      title: 'ID',
      dataIndex: 'id',
      key: 'id',
      width: 70,
    },
    {
      title: t('testPlans.runStatus'),
      dataIndex: 'status',
      key: 'status',
      width: 100,
      render: (status: string) => (
        <Tag color={getStatusColor(status)}>{status.toUpperCase()}</Tag>
      ),
    },
    {
      title: t('testPlans.passRate'),
      dataIndex: 'pass_rate',
      key: 'pass_rate',
      width: 200,
      render: (rate: number | null, record: TestPlanRun) => {
        if (rate === null || rate === undefined) return '-'
        const percent = Math.round(rate * 100)
        return (
          <Space>
            <Progress
              percent={percent}
              size="small"
              style={{ width: 100 }}
              strokeColor={percent >= 80 ? '#2D6A64' : percent >= 60 ? '#D4B483' : '#C75450'}
            />
            <Text style={{ fontSize: 12 }}>{percent}%</Text>
          </Space>
        )
      },
    },
    {
      title: t('testPlans.cases'),
      key: 'cases',
      width: 200,
      render: (_: unknown, record: TestPlanRun) => (
        <Space size={8}>
          <Text style={{ color: '#2D6A64' }}>{t('common.passed')}: {record.passed ?? 0}</Text>
          <Text style={{ color: '#C75450' }}>{t('common.failed')}: {record.failed ?? 0}</Text>
          <Text style={{ color: '#999' }}>{t('testPlans.skipped')}: {record.skipped ?? 0}</Text>
        </Space>
      ),
    },
    {
      title: t('common.createdAt'),
      dataIndex: 'created_at',
      key: 'created_at',
      width: 180,
      render: (val: string) => (val ? new Date(val).toLocaleString() : '-'),
    },
    {
      title: t('common.actions'),
      key: 'actions',
      width: 80,
      render: (_: unknown, record: TestPlanRun) => (
        <Button
          type="link"
          size="small"
          onClick={() => navigate(`/test-plan-runs/${record.id}`)}
        >
          {t('common.view')}
        </Button>
      ),
    },
  ]

  const caseColumns: ColumnsType = [
    {
      title: t('testPlans.caseType'),
      dataIndex: 'case_type',
      key: 'case_type',
      width: 120,
      render: (type: string) => <Tag>{type}</Tag>,
    },
    {
      title: t('testPlans.caseId'),
      dataIndex: 'case_id',
      key: 'case_id',
      width: 100,
    },
  ]

  // 趋势图配置
  const getTrendOption = () => {
    if (!trend.length) return {}
    return {
      tooltip: {
        trigger: 'axis',
        formatter: (params: any) => {
          const point = params[0]
          return `${point.name}<br/>通过率: ${Math.round(point.value * 100)}%`
        },
      },
      color: ['#2D6A64'],
      grid: { left: '3%', right: '4%', bottom: '3%', containLabel: true },
      xAxis: {
        type: 'category',
        data: trend.map((_, i) => `#${i + 1}`),
        axisLabel: { show: true },
      },
      yAxis: {
        type: 'value',
        max: 1,
        axisLabel: {
          formatter: (val: number) => `${Math.round(val * 100)}%`,
        },
      },
      series: [
        {
          type: 'line',
          data: trend.map((p) => p.pass_rate),
          smooth: true,
          areaStyle: { color: 'rgba(45, 106, 100, 0.1)' },
          lineStyle: { width: 2 },
        },
      ],
    }
  }

  if (loading) {
    return (
      <div style={{ display: 'flex', justifyContent: 'center', paddingTop: 120 }}>
        <Spin size="large" />
      </div>
    )
  }

  if (!plan) {
    return (
      <Result
        status="404"
        title={t('testPlans.notFound')}
        extra={
          <Button type="primary" onClick={() => navigate('/test-plans')}>
            {t('common.back')}
          </Button>
        }
      />
    )
  }

  return (
    <div style={{ padding: 0 }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 16 }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
          <Button
            type="text"
            icon={<ArrowLeftOutlined />}
            onClick={() => navigate('/test-plans')}
          />
          <Title level={4} style={{ margin: 0 }}>{plan.name}</Title>
          {plan.description && (
            <Text type="secondary">{plan.description}</Text>
          )}
        </div>
        <Button
          type="primary"
          icon={<PlayCircleOutlined />}
          onClick={handleRun}
        >
          {t('testPlans.run')}
        </Button>
      </div>

      <Card>
        <Tabs
          activeKey={activeTab}
          onChange={setActiveTab}
          items={[
            {
              key: 'runs',
              label: (
                <span>
                  <HistoryOutlined style={{ marginRight: 6 }} />
                  {t('testPlans.runHistory')} ({runsTotal})
                </span>
              ),
              children: (
                <Table
                  columns={runColumns}
                  dataSource={runs}
                  rowKey="id"
                  loading={runsLoading}
                  locale={{ emptyText: <Empty description={t('testPlans.noRuns')} /> }}
                  pagination={{ pageSize: 20 }}
                />
              ),
            },
            {
              key: 'cases',
              label: (
                <span>
                  <UnorderedListOutlined style={{ marginRight: 6 }} />
                  {t('testPlans.cases')} ({plan.include_cases?.length ?? 0})
                </span>
              ),
              children: (
                <Table
                  columns={caseColumns}
                  dataSource={(plan.include_cases || []).map((c, i) => ({ ...c, key: i }))}
                  rowKey="key"
                  pagination={false}
                  locale={{ emptyText: <Empty description={t('testPlans.noCasesInPlan')} /> }}
                />
              ),
            },
            {
              key: 'trend',
              label: (
                <span>
                  <LineChartOutlined style={{ marginRight: 6 }} />
                  {t('testPlans.trend')}
                </span>
              ),
              children: trend.length > 0 ? (
                <ReactECharts option={getTrendOption()} style={{ height: 350 }} />
              ) : (
                <Empty description={t('testPlans.noTrendData')} />
              ),
            },
          ]}
        />
      </Card>
    </div>
  )
}

export default TestPlanDetail
