/**
 * APP 测试设备管理页面
 *
 * 展示已连接设备列表、设备状态、Appium Server 连接状态。
 */
import { useState, useEffect, useCallback } from "react"
import {
  Card, Table, Button, Space, Tag, Typography, Empty, Badge, Input, Row, Col, Statistic,
} from 'antd'
import {
  ReloadOutlined, MobileOutlined, AppleOutlined, AndroidOutlined, ApiOutlined,
} from '@ant-design/icons'
import { useTranslation } from "react-i18next"
import api from "@/services/api"

const { Text } = Typography

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
  const statusLabels: Record<string, string> = {
    online: t("deviceManager.online"),
    offline: t("deviceManager.offline"),
    busy: t("deviceManager.busy"),
  }
  const platformIcon = (p: string) => p === "ios" ? <AppleOutlined /> : <AndroidOutlined />;

  const columns = [
    { title: t("deviceManager.deviceName"), dataIndex: "name", render: (v: string, r: DeviceInfo) => <Space>{platformIcon(r.platform)}<Text strong>{v}</Text></Space> },
    { title: t("deviceManager.platform"), dataIndex: "platform", width: 100, render: (v: string) => <Tag color={v === "ios" ? "blue" : "green"}>{v.toUpperCase()}</Tag> },
    { title: t("deviceManager.version"), dataIndex: "version", width: 100 },
    { title: t("deviceManager.model"), dataIndex: "model", width: 120 },
    { title: t("deviceManager.resolution"), dataIndex: "screen_size", width: 100, render: (v: string) => v || "-" },
    { title: "UDID", dataIndex: "udid", width: 150, render: (v: string) => <Text code style={{ fontSize: 11 }}>{v}</Text> },
    { title: t("deviceManager.status"), dataIndex: "status", width: 80, render: (v: string) => <Tag color={statusColors[v]}>{statusLabels[v] || v}</Tag> },
  ]

  return (
    <div className="fst-page">
      <div className="fst-page-header fst-animate-in">
        <h1 className="fst-page-title">{t("deviceManager.title")}</h1>
        <div className="fst-ios-card-subtitle">{t("deviceManager.subtitle")}</div>
      </div>

      <Card className="fst-ios-card fst-animate-in fst-animate-in-1" style={{ marginBottom: 16 }}>
        <Row gutter={16} align="middle">
          <Col flex="auto">
            <Space>
              <ApiOutlined style={{ fontSize: 18 }} />
              <Text strong>{t("deviceManager.appiumServer")}</Text>
              <Input size="small" value={serverUrl} onChange={e => setServerUrl(e.target.value)} style={{ width: 250 }} placeholder="http://localhost:4723" />
              <Button size="small" icon={<ReloadOutlined />} onClick={fetchDevices} loading={loading}>{t("deviceManager.refresh")}</Button>
            </Space>
          </Col>
          <Col>
            <Space size="large">
              {appiumStatus?.connected ? (
                <Badge status="success" text={<Text type="success">{t("deviceManager.connected")}</Text>} />
              ) : (
                <Badge status="error" text={<Text type="danger">{t("deviceManager.disconnected")}</Text>} />
              )}
              {appiumStatus?.version && <Text type="secondary">v{appiumStatus.version}</Text>}
              <Statistic title={t("deviceManager.deviceList")} value={devices.length} valueStyle={{ fontSize: 16 }} />
            </Space>
          </Col>
        </Row>
      </Card>

      <Card className="fst-ios-card fst-animate-in fst-animate-in-2"
        title={<Space><MobileOutlined /><Text strong>{t("deviceManager.deviceList")}</Text></Space>}>
        {devices.length === 0 && !loading ? (
          <Empty description={t("deviceManager.noDevices")} />
        ) : (
          <Table size="small" rowKey="id" columns={columns} dataSource={devices} loading={loading} pagination={false} />
        )}
      </Card>
    </div>
  )
}

export default DeviceManager
