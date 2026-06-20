/**
 * Flaky Test 检测仪表盘
 *
 * 展示不稳定测试用例列表、失败模式分析、稳定性评分。
 */
import { useState, useEffect, useCallback } from "react"
import { Card, Table, Tag, Typography, Space, Progress, Tooltip, Button } from "antd"
import { ReloadOutlined, BugOutlined } from "@ant-design/icons"
import { useTranslation } from "react-i18next"
import api from "@/services/api"

const { Text } = Typography

interface FlakyCase {
  case_id: number; case_name: string; stability_score: number;
  total_runs: number; flaky_count: number; last_status: string;
  pattern: string; suggestion: string;
}

const FlakyTestDashboard: React.FC = () => {
  const { t } = useTranslation()
  const [loading, setLoading] = useState(false)
  const [cases, setCases] = useState<FlakyCase[]>([])

  const fetchData = useCallback(async () => {
    setLoading(true)
    try {
      const res = await api.get("/flaky-detector/analyze")
      if (res.data?.code === 200) setCases(res.data.data || [])
    } catch {} finally { setLoading(false) }
  }, [])

  useEffect(() => { fetchData() }, [fetchData])

  const getScoreColor = (score: number) => score >= 80 ? "#52c41a" : score >= 50 ? "#faad14" : "#ff4d4f"

  const columns = [
    { title: t("flakyTests.caseName"), dataIndex: "case_name", ellipsis: true },
    { title: t("flakyTests.stabilityScore"), dataIndex: "stability_score", width: 150, render: (v: number) => (
      <Tooltip title={v + '/100'}><Progress percent={v} size="small" strokeColor={getScoreColor(v)} format={p => p + '%'} /></Tooltip>
    )},
    { title: t("flakyTests.totalRuns"), dataIndex: "total_runs", width: 80 },
    { title: t("flakyTests.flakyCount"), dataIndex: "flaky_count", width: 100, render: (v: number) => <Tag color={v > 5 ? "error" : v > 2 ? "warning" : "default"}>{v}</Tag> },
    { title: t("flakyTests.failurePattern"), dataIndex: "pattern", width: 120, ellipsis: true },
    { title: t("flakyTests.suggestion"), dataIndex: "suggestion", ellipsis: true, render: (v: string) => <Text type="secondary" style={{ fontSize: 12 }}>{v}</Text> },
  ]

  return (
    <div className="fst-page">
      <div className="fst-page-header fst-animate-in">
        <h1 className="fst-page-title">{t("flakyTests.title")}</h1>
        <div className="fst-ios-card-subtitle">{t("flakyTests.subtitle")}</div>
      </div>
      <Card className="fst-ios-card fst-animate-in fst-animate-in-1"
        title={<Space><BugOutlined /><Text strong>{t("flakyTests.title")}</Text><Text type="secondary">({cases.length})</Text></Space>}
        extra={<Button icon={<ReloadOutlined />} onClick={fetchData} loading={loading}>{t("flakyTests.refresh")}</Button>}>
        <Table size="small" rowKey="case_id" loading={loading} dataSource={cases} columns={columns} pagination={{ pageSize: 20 }} />
      </Card>
    </div>
  )
}

export default FlakyTestDashboard
