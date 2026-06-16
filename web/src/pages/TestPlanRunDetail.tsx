/**
 * 测试计划运行详情页面
 *
 * 展示单次运行的详细信息，包括每个用例的执行结果。
 */
import { useState, useEffect, useCallback } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import {
  Card,
  Table,
  Button,
  Tag,
  Space,
  Typography,
  Spin,
  Result,
  Statistic,
  Row,
  Col,
  Empty,
  message,
  Progress,
} from 'antd'
import {
  ArrowLeftOutlined,
  CheckCircleOutlined,
  CloseCircleOutlined,
  MinusCircleOutlined,
  ExclamationCircleOutlined,
} from '@ant-design/icons'
import { useTranslation } from 'react-i18next'
import type { ColumnsType } from 'antd/es/table'
import testPlanService, { TestPlanRun } from '@/services/testPlanService'

const { Title, Text } = Typography

const TestPlanRunDetail = () => {
  const { runId } = useParams<{ runId: string }>()
  const navigate = useNavigate()
  const { t } = useTranslation()
  const [run, setRun] = useState<TestPlanRun | null>(null)
  const [loading, setLoading] = useState(true)

  const runIdNum = runId ? parseInt(runId, 10) : null

  const fetchRun = useCallback(async () => {
    if (!runIdNum) return
    setLoading(true)
    try {
      const res = await testPlanService.getTestPlanRun(runIdNum)
      if (res.code === 200 && res.data) {
        setRun(res.data)
      }
    } catch {
      message.error(t('testPlans.fetchRunFailed'))
    } finally {
      setLoading(false)
    }
  }, [runIdNum, t])

  useEffect(() => {
    fetchRun()
  }, [fetchRun])

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'passed': return <CheckCircleOutlined style={{ color: '#2D6A64' }} />
      case 'failed': return <CloseCircleOutlined style={{ color: '#C75450' }} />
      case 'skipped': return <MinusCircleOutlined style={{ color: '#999' }} />
      case 'error': return <ExclamationCircleOutlined style={{ color: '#D4B483' }} />
      default: return null
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

  if (loading) {
    return (
      <div style={{ display: 'flex', justifyContent: 'center', paddingTop: 120 }}>
        <Spin size="large" />
      </div>
    )
  }

  if (!run) {
    return (
      <Result
        status="404"
        title={t('testPlans.runNotFound')}
        extra={
          <Button type="primary" onClick={() => navigate(-1)}>
            {t('common.back')}
          </Button>
        }
      />
    )
  }

  const passRate = run.pass_rate !== null && run.pass_rate !== undefined
    ? Math.round(run.pass_rate * 100)
    : null

  return (
    <div style={{ padding: 0 }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: 12, marginBottom: 16 }}>
        <Button
          type="text"
          icon={<ArrowLeftOutlined />}
          onClick={() => navigate(-1)}
        />
        <Title level={4} style={{ margin: 0 }}>
          {t('testPlans.runDetail')} #{run.id}
        </Title>
        <Tag color={getStatusColor(run.status)}>{run.status.toUpperCase()}</Tag>
      </div>

      {/* 概览统计 */}
      <Card style={{ marginBottom: 16 }}>
        <Row gutter={24}>
          <Col span={4}>
            <Statistic title={t('testPlans.status')} value={run.status.toUpperCase()} />
          </Col>
          <Col span={5}>
            <Statistic
              title={t('testPlans.passRate')}
              value={passRate !== null ? `${passRate}%` : '-'}
              valueStyle={{ color: passRate !== null && passRate >= 80 ? '#2D6A64' : passRate !== null && passRate >= 60 ? '#D4B483' : '#C75450' }}
            />
          </Col>
          <Col span={5}>
            <Statistic title={t('common.total')} value={run.total_cases ?? 0} />
          </Col>
          <Col span={5}>
            <Statistic title={t('common.passed')} value={run.passed ?? 0} valueStyle={{ color: '#2D6A64' }} />
          </Col>
          <Col span={5}>
            <Statistic title={t('common.failed')} value={run.failed ?? 0} valueStyle={{ color: '#C75450' }} />
          </Col>
        </Row>
        {passRate !== null && (
          <Progress
            percent={passRate}
            strokeColor={passRate >= 80 ? '#2D6A64' : passRate >= 60 ? '#D4B483' : '#C75450'}
            style={{ marginTop: 16 }}
          />
        )}
      </Card>

      {/* 运行信息 */}
      <Card title={t('testPlans.runInfo')} style={{ marginBottom: 16 }}>
        <Row gutter={16}>
          <Col span={8}>
            <Text type="secondary">{t('common.createdAt')}:</Text>
            <br />
            <Text>{run.created_at ? new Date(run.created_at).toLocaleString() : '-'}</Text>
          </Col>
          <Col span={8}>
            <Text type="secondary">{t('testPlans.startedAt')}:</Text>
            <br />
            <Text>{run.started_at ? new Date(run.started_at).toLocaleString() : '-'}</Text>
          </Col>
          <Col span={8}>
            <Text type="secondary">{t('testPlans.finishedAt')}:</Text>
            <br />
            <Text>{run.finished_at ? new Date(run.finished_at).toLocaleString() : '-'}</Text>
          </Col>
        </Row>
        {run.notes && (
          <div style={{ marginTop: 12 }}>
            <Text type="secondary">{t('common.description')}:</Text>
            <br />
            <Text>{run.notes}</Text>
          </div>
        )}
      </Card>
    </div>
  )
}

export default TestPlanRunDetail
