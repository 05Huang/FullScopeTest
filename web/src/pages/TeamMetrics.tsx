/**
 * 团队效能指标页面
 *
 * 展示团队成员的测试效能指标，支持时间范围选择。
 */
import { useState, useEffect, useCallback } from 'react'
import {
  Card,
  Table,
  Select,
  Row,
  Col,
  Statistic,
  Typography,
  Space,
  Empty,
  Spin,
  message,
} from 'antd'
import {
  TeamOutlined,
  FileTextOutlined,
  ThunderboltOutlined,
  CheckCircleOutlined,
} from '@ant-design/icons'
import { useTranslation } from 'react-i18next'
import type { ColumnsType } from 'antd/es/table'
import ReactECharts from 'echarts-for-react'
import { useProjectStore } from '@/stores/projectStore'
import teamMetricsService, { TeamMemberMetric, TeamMetricsData } from '@/services/teamMetricsService'

const { Title } = Typography

const TeamMetrics = () => {
  const { t } = useTranslation()
  const { currentProjectId } = useProjectStore()
  const [data, setData] = useState<TeamMetricsData | null>(null)
  const [loading, setLoading] = useState(false)
  const [days, setDays] = useState(30)

  const fetchData = useCallback(async () => {
    setLoading(true)
    try {
      const res = await teamMetricsService.getTeamMetrics({
        project_id: currentProjectId || undefined,
        days,
      })
      if (res.code === 200 && res.data) {
        setData(res.data)
      }
    } catch {
      message.error(t('teamMetrics.fetchFailed'))
    } finally {
      setLoading(false)
    }
  }, [currentProjectId, days, t])

  useEffect(() => { fetchData() }, [fetchData])

  const columns: ColumnsType<TeamMemberMetric> = [
    {
      title: t('teamMetrics.member'),
      dataIndex: 'username',
      key: 'username',
      render: (name: string) => <span style={{ fontWeight: 500 }}>{name}</span>,
    },
    {
      title: t('teamMetrics.casesCreated'),
      dataIndex: 'cases_created',
      key: 'cases_created',
      sorter: (a, b) => a.cases_created - b.cases_created,
    },
    {
      title: t('teamMetrics.casesExecuted'),
      dataIndex: 'cases_executed',
      key: 'cases_executed',
      sorter: (a, b) => a.cases_executed - b.cases_executed,
    },
    {
      title: t('teamMetrics.bugsFound'),
      dataIndex: 'bugs_found',
      key: 'bugs_found',
      sorter: (a, b) => a.bugs_found - b.bugs_found,
    },
    {
      title: t('teamMetrics.avgPassRate'),
      dataIndex: 'avg_pass_rate',
      key: 'avg_pass_rate',
      render: (rate: number) => rate !== null && rate !== undefined ? `${Math.round(rate * 100)}%` : '-',
      sorter: (a, b) => (a.avg_pass_rate || 0) - (b.avg_pass_rate || 0),
    },
  ]

  // 柱状图配置
  const getBarOption = () => {
    if (!data?.members?.length) return {}
    return {
      tooltip: { trigger: 'axis' },
      color: ['#2D6A64', '#D4B483'],
      legend: { data: [t('teamMetrics.casesCreated'), t('teamMetrics.casesExecuted')] },
      grid: { left: '3%', right: '4%', bottom: '3%', containLabel: true },
      xAxis: {
        type: 'category',
        data: data.members.map((m) => m.username),
        axisLabel: { rotate: 30 },
      },
      yAxis: { type: 'value' },
      series: [
        {
          name: t('teamMetrics.casesCreated'),
          type: 'bar',
          data: data.members.map((m) => m.cases_created),
          itemStyle: { borderRadius: [4, 4, 0, 0] },
        },
        {
          name: t('teamMetrics.casesExecuted'),
          type: 'bar',
          data: data.members.map((m) => m.cases_executed),
          itemStyle: { borderRadius: [4, 4, 0, 0] },
        },
      ],
    }
  }

  return (
    <div style={{ padding: 0 }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 16 }}>
        <Title level={4} style={{ margin: 0 }}>
          <TeamOutlined style={{ marginRight: 8 }} />
          {t('teamMetrics.title')}
        </Title>
        <Select
          value={days}
          onChange={setDays}
          style={{ width: 140 }}
          options={[
            { value: 7, label: t('teamMetrics.last7Days') },
            { value: 30, label: t('teamMetrics.last30Days') },
            { value: 90, label: t('teamMetrics.last90Days') },
          ]}
        />
      </div>

      {loading ? (
        <div style={{ display: 'flex', justifyContent: 'center', paddingTop: 80 }}>
          <Spin size="large" />
        </div>
      ) : data ? (
        <>
          {/* 概览卡片 */}
          <Row gutter={16} style={{ marginBottom: 16 }}>
            <Col span={6}>
              <Card>
                <Statistic title={t('teamMetrics.totalCases')} value={data.summary?.total_cases ?? 0} prefix={<FileTextOutlined />} />
              </Card>
            </Col>
            <Col span={6}>
              <Card>
                <Statistic title={t('teamMetrics.totalExecutions')} value={data.summary?.total_executions ?? 0} prefix={<ThunderboltOutlined />} />
              </Card>
            </Col>
            <Col span={6}>
              <Card>
                <Statistic
                  title={t('teamMetrics.avgPassRate')}
                  value={data.summary?.avg_pass_rate !== null && data.summary?.avg_pass_rate !== undefined ? `${Math.round(data.summary.avg_pass_rate * 100)}%` : '-'}
                  prefix={<CheckCircleOutlined />}
                  valueStyle={{ color: '#2D6A64' }}
                />
              </Card>
            </Col>
            <Col span={6}>
              <Card>
                <Statistic title={t('teamMetrics.activeMembers')} value={data.summary?.active_members ?? 0} prefix={<TeamOutlined />} />
              </Card>
            </Col>
          </Row>

          {/* 柱状图 */}
          {data.members?.length > 0 && (
            <Card style={{ marginBottom: 16 }}>
              <ReactECharts option={getBarOption()} style={{ height: 350 }} />
            </Card>
          )}

          {/* 成员排行表格 */}
          <Card>
            <Table
              columns={columns}
              dataSource={data.members || []}
              rowKey="user_id"
              pagination={false}
              locale={{ emptyText: <Empty description={t('teamMetrics.noData')} /> }}
            />
          </Card>
        </>
      ) : (
        <Card>
          <Empty description={t('teamMetrics.noData')} />
        </Card>
      )}
    </div>
  )
}

export default TeamMetrics
