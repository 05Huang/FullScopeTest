import { useTranslation } from 'react-i18next';
import React, { useState, useEffect } from 'react'
import { Card, Table, Tag, Typography, Spin, Empty, Row, Col, Image, Button } from 'antd'
import { LineChartOutlined, ArrowLeftOutlined } from '@ant-design/icons'
import { useNavigate, useParams } from 'react-router-dom'
import { webTestService } from '@/services/webTestService'
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
  const { t } = useTranslation();
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
        const res = await webTestService.getVisualHistory(Number(testCaseId))
        setHistory((res as any).data || [])
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
      title: t('reports.executionTime'),
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
      title: t('common.actions'),
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
    <div className="fst-page">
      <div className="fst-page-header fst-animate-in">
        <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
          <button className="fst-btn fst-btn--ghost fst-btn--sm" onClick={() => navigate(-1)}><ArrowLeftOutlined /> {t('common.back')}</button>
          <h1 className="fst-page-title" style={{ fontSize: 20 }}>
            <LineChartOutlined /> 视觉回归历史趋势 - 用例 #{testCaseId}
          </h1>
        </div>
      </div>

      {history.length === 0 ? (
        <div className="fst-empty">
          <div className="fst-empty-icon"><LineChartOutlined /></div>
          <div className="fst-empty-title">暂无视觉回归历史数据</div>
        </div>
      ) : (
        <>
          <div className="fst-ios-card fst-animate-in fst-animate-in-1">
            <div className="fst-ios-card-header">
              <div className="fst-ios-card-title">差异百分比趋势</div>
            </div>
            {renderChart()}
          </div>

          <div className="fst-ios-card fst-animate-in fst-animate-in-2" style={{ marginTop: 16 }}>
            <div className="fst-ios-card-header">
              <div className="fst-ios-card-title">执行历史记录</div>
            </div>
            <div className="fst-table-wrap">
              <Table columns={columns} dataSource={history.map((h, i) => ({ ...h, key: i }))} pagination={{ pageSize: 10 }} size="small" />
            </div>
          </div>

          {selectedRecord && (
            <div className="fst-ios-card fst-animate-in fst-animate-in-3" style={{ marginTop: 16 }}>
              <div className="fst-ios-card-header">
                <div className="fst-ios-card-title">详情 - 执行 #{selectedRecord.test_run_id}</div>
                <button className="fst-btn fst-btn--ghost fst-btn--sm" onClick={() => setSelectedRecord(null)}>{t('common.close')}</button>
              </div>
              <Row gutter={16}>
                <Col span={8}>
                  <Text strong>基准截图</Text>
                  <br />
                  {selectedRecord.sample_baseline_image ? <Image src={selectedRecord.sample_baseline_image} width="100%" /> : <Empty description="无基准截图" />}
                </Col>
                <Col span={8}>
                  <Text strong>当前截图</Text>
                  <br />
                  {selectedRecord.sample_current_image ? <Image src={selectedRecord.sample_current_image} width="100%" /> : <Empty description="无当前截图" />}
                </Col>
                <Col span={8}>
                  <Text strong>差异图</Text>
                  <br />
                  {selectedRecord.sample_diff_image ? <Image src={selectedRecord.sample_diff_image} width="100%" /> : <Empty description="无差异图" />}
                </Col>
              </Row>
            </div>
          )}
        </>
      )}
    </div>
  )
}

export default VisualRegressionHistory
