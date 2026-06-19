/**
 * APP 测试设备管理页面
 *
 * 展示已连接设备列表、设备状态、Appium Server 连接状态。
 */
import { useState, useEffect, useCallback } from "react"
import {
  Card, Table, Button, Space, Tag, Typography, Empty, Badge, Tooltip, message, Input, Row, Col, Statistic,
} from 'antd'
import {
  ReloadOutlined, MobileOutlined, CheckCircleOutlined, CloseCircleOutlined,
  DesktopOutlined, AppleOutlined, AndroidOutlined, ApiOutlined,
} from '@ant-design/icons'
import { useTranslation } from "react-i18next"
import api from "@/services/api"

const { Text, Title } = Typography

interface DeviceInfo {
  id: string;
  name: string;
  platform: "android" | "ios";
  version: string;
  status: "online" | "offline" | "busy";
  udid: string;
  model: string;
  screen_size?: string;
  appium_server?: string;
}

interface AppiumStatus {
  url: string;
  connected: boolean;
  version?: string;
  device_count?: number;
}

const DeviceManager: React.FC = () => {
  const { t } = useTranslation()
  const [loading, setLoading] = useState(false)
  const [devices, setDevices] = useState<DeviceInfo[]>([])
  const [appiumStatus, setAppiumStatus] = useState<AppiumStatus | null>(null)
  const [serverUrl, setServerUrl] = useState("http://localhost:4723")

  const fetchDevices = useCallback(async () => {
    setLoading(true)
    try {
      const res = await api.get("/app-test/devices", { params: { server_url: serverUrl } })
      if (res.data?.code === 200) {
        setDevices(res.data.data?.devices || [])
        setAppiumStatus(res.data.data?.server_status || null)
      }
    } catch {
      setAppiumStatus({ url: serverUrl, connected: false })
    } finally {
      setLoading(false)
    }
  }, [serverUrl])

  useEffect(() => { fetchDevices() }, [])

  const statusColors: Record<string, string> = { online: "success", offline: "default", busy: "processing" }
  const platformIcon = (p: string) => p === "ios" ? <AppleOutlined /> : <AndroidOutlined />;

  const columns = [
    { title: "设备名", dataIndex: "name", render: (v: string, r: DeviceInfo) => <Space>{platformIcon(r.platform)}<Text strong>{v}</Text></Space> },
    { title: "平台", dataIndex: "platform", width: 100, render: (v: string) => <Tag color={v === "ios" ? "blue" : "green"}>{v.toUpperCase()}</Tag> },
    { title: "系统版本", dataIndex: "version", width: 100 },
    { title: "型号", dataIndex: "model", width: 120 },
    { title: "分辨率", dataIndex: "screen_size", width: 100, render: (v: string) => v || "-" },
    { title: "UDID", dataIndex: "udid", width: 150, render: (v: string) => <Text code style={{ fontSize: 11 }}>{v}</Text> },
    { title: "状态", dataIndex: "status", width: 80, render: (v: string) => <Tag color={statusColors[v]}>{v}</Tag> },
  ]

  return (
    <div style={{ padding: 16 }}>
      {/* Appium Server 状态 */}
      <Card size="small" style={{ marginBottom: 12 }}>
        <Row gutter={16} align="middle">
          <Col flex="auto">
            <Space>
              <ApiOutlined style={{ fontSize: 18 }} />
              <Text strong>Appium Server</Text>
              <Input size="small" value={serverUrl} onChange={e => setServerUrl(e.target.value)} style={{ width: 250 }} placeholder="http://localhost:4723" />
              <Button size="small" icon={<ReloadOutlined />} onClick={fetchDevices} loading={loading}>刷新</Button>
            </Space>
          </Col>
          <Col>
            <Space size="large">
              {appiumStatus?.connected ? (
                <Badge status="success" text={<Text type="success">已连接</Text>} />
              ) : (
                <Badge status="error" text={<Text type="danger">未连接</Text>} />
              )}
              {appiumStatus?.version && <Text type="secondary">v{appiumStatus.version}</Text>}
              <Statistic title="设备数" value={devices.length} valueStyle={{ fontSize: 16 }} />
            </Space>
          </Col>
        </Row>
      </Card>

      {/* 设备列表 */}
      <Card size="small" title={<Space><MobileOutlined /><Text strong>已连接设备</Text></Space>}>
        {devices.length === 0 && !loading ? (
          <Empty description="未检测到设备。请确认 Appium Server 已启动且设备已连接。" />
        ) : (
          <Table size="small" rowKey="id" columns={columns} dataSource={devices} loading={loading} pagination={false} />
        )}
      </Card>
    </div>
  )
}

export default DeviceManager
