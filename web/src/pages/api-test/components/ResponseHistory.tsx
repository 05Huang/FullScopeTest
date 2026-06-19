/**
 * 响应历史面板组件
 *
 * 展示同一接口的历史响应列表和响应时间趋势图。
 */
import { useState, useEffect, useCallback } from "react"
import { Card, Table, Tag, Space, Typography, Empty, Button, Tooltip, Spin } from "antd"
import { HistoryOutlined, LineChartOutlined, ReloadOutlined } from "@ant-design/icons"
import { useTranslation } from "react-i18next"
import api from "@/services/api"

const { Text } = Typography

interface HistoryItem {
  id: number; url: string; method: string; status_code: number | null;
  response_time: number | null; created_at: string | null;
}

interface ResponseHistoryProps {
  caseId?: number;
  onSelectHistory?: (item: HistoryItem) => void;
}

const METHOD_COLORS: Record<string, string> = {
  GET: "#52c41a", POST: "#1890ff", PUT: "#faad14", DELETE: "#ff4d4f", PATCH: "#722ed1",
};

const ResponseHistory: React.FC<ResponseHistoryProps> = ({ caseId, onSelectHistory }) => {
  const { t } = useTranslation()
  const [loading, setLoading] = useState(false)
  const [history, setHistory] = useState<HistoryItem[]>([])

  const fetchHistory = useCallback(async () => {
    if (!caseId) { setHistory([]); return }
    setLoading(true)
    try {
      const res = await api.get("/api-test/history", { params: { case_id: caseId, limit: 30 } })
      if (res.data?.code === 200) {
        setHistory(res.data.data || [])
      }
    } catch (err) {
      // 静默处理
    } finally {
      setLoading(false)
    }
  }, [caseId])

  useEffect(() => { fetchHistory() }, [fetchHistory])

  const columns = [
    {
      title: "状态", width: 60,
      render: (_: unknown, record: HistoryItem) => record.status_code ? (
        <Tag color={record.status_code < 400 ? "success" : "error"}>{record.status_code}</Tag>
      ) : <Tag color="default">-</Tag>,
    },
    {
      title: "耗时", width: 80, dataIndex: "response_time",
      render: (v: number | null) => v !== null ? <Text>{Math.round(v)}ms</Text> : <Text type="secondary">-</Text>,
    },
    {
      title: "时间", width: 140, dataIndex: "created_at",
      render: (v: string | null) => v ? <Text type="secondary" style={{ fontSize: 12 }}>{new Date(v).toLocaleString("zh-CN")}</Text> : null,
    },
    {
      title: "", width: 40,
      render: (_: unknown, record: HistoryItem) => (
        <Tooltip title="查看详情">
          <Button type="text" size="small" onClick={() => onSelectHistory?.(record)}>查看</Button>
        </Tooltip>
      ),
    },
  ]

  return (
    <Card size="small" title={<Space><HistoryOutlined /><Text strong>响应历史</Text><Text type="secondary">({history.length})</Text></Space>}
      extra={<Button size="small" icon={<ReloadOutlined />} onClick={fetchHistory} loading={loading} />}>
      {!caseId ? (
        <Empty description="保存用例后可查看响应历史" image={Empty.PRESENTED_IMAGE_SIMPLE} />
      ) : loading ? (
        <Spin size="small" />
      ) : history.length === 0 ? (
        <Empty description="暂无响应历史" image={Empty.PRESENTED_IMAGE_SIMPLE} />
      ) : (
        <Table size="small" rowKey="id" columns={columns} dataSource={history} pagination={false} />
      )}
    </Card>
  )
}

export default ResponseHistory
