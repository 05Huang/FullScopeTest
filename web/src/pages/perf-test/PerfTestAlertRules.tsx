import { useState, useEffect } from 'react'
import { useTranslation } from 'react-i18next'
import {
  Card,
  Table,
  Button,
  Space,
  Tag,
  Typography,
  Empty,
  message,
} from 'antd'
import {
  PlusOutlined,
  ReloadOutlined,
  AlertOutlined,
  BellOutlined,
} from '@ant-design/icons'
import type { ColumnsType } from 'antd/es/table'
import { perfTestService } from '@/services/perfTestService'

const { Text } = Typography

interface AlertRule {
  id: number
  scenario_id: number
  scenario_name?: string
  metric: string
  threshold: number
  operator: string
  severity: string
  is_active: boolean
  created_at: string
}

interface AlertLog {
  id: number
  rule_id: number
  scenario_name?: string
  metric: string
  value: number
  threshold: number
  severity: string
  message: string
  triggered_at: string
}

const PerfTestAlertRules = () => {
  const { t } = useTranslation()
  const [activeTab, setActiveTab] = useState<'rules' | 'logs'>('rules')
  const [loading, setLoading] = useState(false)
  const [rules, setRules] = useState<AlertRule[]>([])
  const [logs, setLogs] = useState<AlertLog[]>([])

  useEffect(() => {
    fetchData()
  }, [activeTab])

  const fetchData = async () => {
    setLoading(true)
    try {
      if (activeTab === 'rules') {
        const res = await perfTestService.getAlertRules()
        if (res.code === 200) {
          setRules(res.data?.items || res.data || [])
        }
      } else {
        const res = await perfTestService.getAlertLogs({ per_page: 50 })
        if (res.code === 200) {
          setLogs(res.data?.items || res.data || [])
        }
      }
    } catch {
      message.error(t('perfTest.loadFailed'))
    } finally {
      setLoading(false)
    }
  }

  const ruleColumns: ColumnsType<AlertRule> = [
    {
      title: t('perfTest.scenarioName'),
      dataIndex: 'scenario_name',
      key: 'scenario_name',
      render: (text) => <Text strong>{text || '-'}</Text>,
    },
    {
      title: 'Metric',
      dataIndex: 'metric',
      key: 'metric',
      width: 150,
      render: (text) => <Tag>{text}</Tag>,
    },
    {
      title: 'Condition',
      key: 'condition',
      width: 150,
      render: (_, record) => (
        <Text code>{record.operator} {record.threshold}</Text>
      ),
    },
    {
      title: t('common.status'),
      dataIndex: 'is_active',
      key: 'is_active',
      width: 100,
      render: (active) => (
        <Tag color={active ? 'success' : 'default'}>
          {active ? t('cicd.enabled') : t('cicd.disabled')}
        </Tag>
      ),
    },
    {
      title: t('common.createdAt'),
      dataIndex: 'created_at',
      key: 'created_at',
      width: 170,
      render: (time) => time ? new Date(time).toLocaleString() : '-',
    },
  ]

  const logColumns: ColumnsType<AlertLog> = [
    {
      title: t('perfTest.scenarioName'),
      dataIndex: 'scenario_name',
      key: 'scenario_name',
      render: (text) => <Text strong>{text || '-'}</Text>,
    },
    {
      title: 'Metric',
      dataIndex: 'metric',
      key: 'metric',
      width: 120,
      render: (text) => <Tag>{text}</Tag>,
    },
    {
      title: 'Value',
      dataIndex: 'value',
      key: 'value',
      width: 100,
    },
    {
      title: 'Threshold',
      dataIndex: 'threshold',
      key: 'threshold',
      width: 100,
    },
    {
      title: t('common.status'),
      dataIndex: 'severity',
      key: 'severity',
      width: 100,
      render: (severity) => (
        <Tag color={severity === 'critical' ? 'red' : severity === 'warning' ? 'orange' : 'blue'}>
          {severity}
        </Tag>
      ),
    },
    {
      title: t('common.time'),
      dataIndex: 'triggered_at',
      key: 'triggered_at',
      width: 170,
      render: (time) => time ? new Date(time).toLocaleString() : '-',
    },
  ]

  return (
    <div className="fst-page">
      <div className="fst-page-header fst-animate-in">
        <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
          <div className="fst-stat-icon fst-stat-icon--tertiary">
            <AlertOutlined style={{ fontSize: 18 }} />
          </div>
          <h1 className="fst-page-title">{t('perfTest.alertRules')}</h1>
        </div>
        <Space>
          <Button icon={<ReloadOutlined />} onClick={fetchData} loading={loading}>
            {t('common.refresh')}
          </Button>
        </Space>
      </div>

      <div className="fst-ios-card fst-animate-in fst-animate-in-1">
        <div className="fst-tabs" style={{ marginBottom: 20 }}>
          <button
            className={`fst-tab ${activeTab === 'rules' ? 'fst-tab--active' : ''}`}
            onClick={() => setActiveTab('rules')}
          >
            <AlertOutlined style={{ marginRight: 6 }} /> {t('perfTest.alertRuleManagement')}
          </button>
          <button
            className={`fst-tab ${activeTab === 'logs' ? 'fst-tab--active' : ''}`}
            onClick={() => setActiveTab('logs')}
          >
            <BellOutlined style={{ marginRight: 6 }} /> {t('perfTest.alertLogManagement')}
          </button>
        </div>

        <div className="fst-table-wrap">
          {activeTab === 'rules' ? (
            rules.length > 0 ? (
              <Table
                columns={ruleColumns}
                dataSource={rules}
                rowKey="id"
                loading={loading}
                pagination={{ pageSize: 10 }}
              />
            ) : (
              <Empty description={t('perfTest.noAlertRules')} />
            )
          ) : (
            logs.length > 0 ? (
              <Table
                columns={logColumns}
                dataSource={logs}
                rowKey="id"
                loading={loading}
                pagination={{ pageSize: 20 }}
              />
            ) : (
              <Empty description={t('perfTest.noAlertRules')} />
            )
          )}
        </div>
      </div>
    </div>
  )
}

export default PerfTestAlertRules
