/**
 * 外部数据源 Widget
 * 支持配置外部 API 数据源（Prometheus/Grafana/Jenkins）
 */
import { useState, useEffect, useCallback } from "react"
import { Card, Space, Typography, Spin, Button } from "antd"
import { ApiOutlined, ReloadOutlined, SettingOutlined } from "@ant-design/icons"
import api from "@/services/api"

const { Text } = Typography

interface Props { title?: string; apiUrl?: string; refreshInterval?: number; dataPath?: string; unit?: string; onConfigure?: () => void }

const ExternalDataWidget: React.FC<Props> = ({ title = "External", apiUrl, refreshInterval = 60, dataPath, unit, onConfigure }) => {
  const [loading, setLoading] = useState(false)
  const [value, setValue] = useState<string | null>(null)
  const [error, setError] = useState<string | null>(null)

  const fetchData = useCallback(async () => {
    if (!apiUrl) return; setLoading(true); setError(null)
    try { const res = await api.post("/dashboard/external-data", { url: apiUrl, path: dataPath }); if (res.data?.code === 200) setValue(String(res.data.data?.value ?? "-")) }
    catch (e: any) { setError(e.message || "Failed") } finally { setLoading(false) }
  }, [apiUrl, dataPath])

  useEffect(() => { fetchData(); if (refreshInterval > 0) { const t = setInterval(fetchData, refreshInterval * 1000); return () => clearInterval(t) } }, [fetchData, refreshInterval])

  return (<Card size="small" title={<Space><ApiOutlined /><Text strong>{title}</Text></Space>}
    extra={<Space><Button size="small" type="text" icon={<ReloadOutlined />} onClick={fetchData} loading={loading} />
    {onConfigure && <Button size="small" type="text" icon={<SettingOutlined />} onClick={onConfigure} />}</Space>}>
    {loading && !value ? <Spin size="small" /> : error ? <Text type="danger" style={{ fontSize: 12 }}>{error}</Text>
    : value !== null ? <div style={{ textAlign: "center" }}><Text style={{ fontSize: 28, fontWeight: 600 }}>{value}</Text>{unit && <Text type="secondary" style={{ marginLeft: 4 }}>{unit}</Text>}</div>
    : <Text type="secondary">未配置</Text>}
  </Card>)
}

export default ExternalDataWidget
