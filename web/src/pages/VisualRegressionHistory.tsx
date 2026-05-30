import React, { useState, useEffect } from 'react'
import { Card, Table, Tag, Typography, Spin, Empty, Row, Col, Image, Button } from 'antd'
import { LineChartOutlined, ArrowLeftOutlined } from '@ant-design/icons'
import { useNavigate, useParams } from 'react-router-dom'
import api from '@/services/api'
import dayjs from 'dayjs'

const { Title, Text } = Typography

interface HistoryRecord {
  test_run_id: number
  run_time: string
  avg_diff_percentage: number
  max_diff_percentage: number
  min_diff_percentage: number
  step_count: number
  fail_count: number
  pass_count: number
  sample_diff_image: string | null
  sample_baseline_image: string | null
  sample_current_image: string | null
}

const VisualRegressionHistory: React.FC = () => {
  const navigate = useNavigate()
  const { testCaseId } = useParams<{ testCaseId: string }>()
  const [history, setHistory] = useState<HistoryRecord[]>([])
  const [loading, setLoading] = useState(true)
  const [selectedRecord, setSelectedRecord] = useState<HistoryRecord | null>(null)

  useEffect(() => {
    const fetchHistory = async () => {
      if (!testCaseId) return
      setLoading(true)
      try {
        const res = await api.get(`/visual/history/${testCaseId}`)
        setHistory(res.data || [])
      } catch (err) {
        console.error('Failed to fetch visual history:', err)
      } finally {
        setLoading(false)
      }
    }
    fetchHistory()
  }, [testCaseId])

  const columns = [
    {
      title: '测试执行',
      dataIndex: 'test_run_id',
      key: 'test_run_id',
      render: (id: number) => <Text code>#{id}</Text>,
    },
    {
      title: '执行时间',
      dataIndex: 'run_time',
      key: 'run_time',
      render: (time: string) => time ? dayjs(time).format('YYYY-MM-DD HH:mm:ss') : '-',
    },
    {
      title: '步骤数',
      dataIndex: 'step_count',
      key: 'step_count',
    },
    {
      title: '平均差异',
      dataIndex: 'avg_diff_percentage',
      key: 'avg_diff_percentage',
      render: (val: number) => (
        <Tag color={val > 5 ? 'error' : val > 1 ? 'warning' : 'success'}>
          {val.toFixed(2)}%
        </Tag>
      ),
    },
    {
      title: '最大差异',
      dataIndex: 'max_diff_percentage',
      key: 'max_diff_percentage',
      render: (val: number) => (
        <Tag color={val > 5 ? 'error' : val > 1 ? 'warning' : 'success'}>
          {val.toFixed(2)}%
        </Tag>
      ),
    },
    {
      title: '通过/失败',
      key: 'result',
      render: (_: unknown, record: HistoryRecord) => (
        <span>
          <Tag color="success">{record.pass_count} 通过</Tag>
          <Tag color="error">{record.fail_count} 失败</Tag>
        </span>
      ),
    },
    {
      title: '操作',
      key: 'action',
      render: (_: unknown, record: HistoryRecord) => (
        <Button type="link" size="small" onClick={() => setSelectedRecord(record)}>
          查看详情
        </Button>
      ),
    },
  ]

  const diffData = history.map((h, index) => ({
    time: dayjs(h.run_time).format('MM-DD HH:mm'),
    avg_diff: h.avg_diff_percentage,
    max_diff: h.max_diff_percentage,
    min_diff: h.min_diff_percentage,
    index,
  }))

  const renderChart = () => {
    if (diffData.length === 0) return null

    const maxVal = Math.max(...diffData.map(d => d.avg_diff), 1)
    const width = 600
    const height = 200
    const padding = { top: 20, right: 20, bottom: 40, left: 50 }
    const chartWidth = width - padding.left - padding.right
    const chartHeight = height - padding.top - padding.bottom

    const points = diffData.map((d, i) => ({
      x: padding.left + (i / (diffData.length - 1 || 1)) * chartWidth,
      y: padding.top + (1 - d.avg_diff / maxVal) * chartHeight,
      ...d,
    }))

    const pathD = points.map((p, i) => `${i === 0 ? 'M' : 'L'} ${p.x} ${p.y}`).join(' ')

    return (
      <svg width={width} height={height} style={{ background: '#fafafa', borderRadius: 8 }}>
        {[0, 0.25, 0.5, 0.75, 1].map(pct => {
          const y = padding.top + (1 - pct) * chartHeight
          return (
            <g key={pct}>
              <line x1={padding.left} y1={y} x2={width - padding.right} y2={y} stroke="#e8e8e8" strokeDasharray="4 2" />
              <text x={padding.left - 8} y={y + 4} textAnchor="end" fill="#888" fontSize="10">
                {(maxVal * pct).toFixed(1)}%
              </text>
            </g>
          )
        })}
        <path d={pathD} fill="none" stroke="#1677ff" strokeWidth="2" />
        {points.map((p, i) => (
          <g key={i}>
            <circle cx={p.x} cy={p.y} r="4" fill="#1677ff" />
            <text x={p.x} y={height - 8} textAnchor="middle" fill="#888" fontSize="9">
              {p.time}
            </text>
          </g>
        ))}
      </svg>
    )
  }

  if (loading) {
    return (
      <div style={{ textAlign: 'center', padding: 100 }}>
        <Spin size="large" />
      </div>
    )
  }

  return (
    <div style={{ padding: 24 }}>
      <div style={{ marginBottom: 16, display: 'flex', alignItems: 'center', gap: 12 }}>
        <Button icon={<ArrowLeftOutlined />} onClick={() => navigate(-1)}>
          返回
        </Button>
        <Title level={3} style={{ margin: 0 }}>
          <LineChartOutlined /> 视觉回归历史趋势 - 用例 #{testCaseId}
        </Title>
      </div>

      {history.length === 0 ? (
        <Empty description="暂无视觉回归历史数据" />
      ) : (
        <>
          <Card title="差异百分比趋势" style={{ marginBottom: 24 }}>
            {renderChart()}
          </Card>

          <Card title="执行历史记录">
            <Table
              columns={columns}
              dataSource={history.map((h, i) => ({ ...h, key: i }))}
              pagination={{ pageSize: 10 }}
              size="small"
            />
          </Card>

          {selectedRecord && (
            <Card
              title={`详情 - 执行 #${selectedRecord.test_run_id}`}
              style={{ marginTop: 24 }}
              extra={<Button onClick={() => setSelectedRecord(null)}>关闭</Button>}
            >
              <Row gutter={16}>
                <Col span={8}>
                  <Text strong>基准截图</Text>
                  <br />
                  {selectedRecord.sample_baseline_image ? (
                    <Image src={selectedRecord.sample_baseline_image} width="100%" />
                  ) : (
                    <Empty description="无基准截图" />
                  )}
                </Col>
                <Col span={8}>
                  <Text strong>当前截图</Text>
                  <br />
                  {selectedRecord.sample_current_image ? (
                    <Image src={selectedRecord.sample_current_image} width="100%" />
                  ) : (
                    <Empty description="无当前截图" />
                  )}
                </Col>
                <Col span={8}>
                  <Text strong>差异图</Text>
                  <br />
                  {selectedRecord.sample_diff_image ? (
                    <Image src={selectedRecord.sample_diff_image} width="100%" />
                  ) : (
                    <Empty description="无差异图" />
                  )}
                </Col>
              </Row>
            </Card>
          )}
        </>
      )}
    </div>
  )
}

export default VisualRegressionHistory
