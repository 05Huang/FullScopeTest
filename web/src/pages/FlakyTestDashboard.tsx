/**
 * Flaky Test 检测仪表盘
 *
 * 展示不稳定测试用例列表、失败模式分析、稳定性评分。
 */
import { useState, useEffect, useCallback } from "react"
import { Card, Table, Tag, Typography, Space, Progress, Tooltip, Button, message } from "antd"
import { WarningOutlined, ReloadOutlined, BugOutlined, CheckCircleOutlined } from "@ant-design/icons"
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
    { title: "用例名", dataIndex: "case_name", ellipsis: true },
    { title: "稳定性评分", dataIndex: "stability_score", width: 150, render: (v: number) => (
      <Tooltip title={v + "/100"><Progress percent={v} size="small" strokeColor={getScoreColor(v)} format={p => p + "%"} /></Tooltip>
    )},
    { title: "总执行", dataIndex: "total_runs", width: 80 },
    { title: "Flaky 次数", dataIndex: "flaky_count", width: 100, render: (v: number) => <Tag color={v > 5 ? "error" : v > 2 ? "warning" : "default"}>{v}</Tag> },
    { title: "失败模式", dataIndex: "pattern", width: 120, ellipsis: true },
    { title: "修复建议", dataIndex: "suggestion", ellipsis: true, render: (v: string) => <Text type="secondary" style={{ fontSize: 12 }}>{v}</Text> },
  ]

  return (
    <div style={{ padding: 16 }}>
      <Card title={<Space><BugOutlined /><Text strong>Flaky Test 检测</Text><Text type="secondary">({cases.length})</Text></Space>}
        extra={<Button icon={<ReloadOutlined />} onClick={fetchData} loading={loading}>刷新</Button>}>
        <Table size="small" rowKey="case_id" loading={loading} dataSource={cases} columns={columns} pagination={{ pageSize: 20 }} />
      </Card>
    </div>
  )
}

export default FlakyTestDashboard
