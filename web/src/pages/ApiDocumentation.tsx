/**
 * API 文档生成页面
 *
 * 从测试用例自动生成 OpenAPI 文档，在线预览和导出。
 */
import { useState, useEffect, useCallback } from "react"
import { Card, Button, Space, Typography, Select, message, Tabs, Empty } from "antd"
import { FileTextOutlined, DownloadOutlined, ApiOutlined, CopyOutlined } from "@ant-design/icons"
import { useTranslation } from "react-i18next"
import MonacoEditor from "@monaco-editor/react"
import api from "@/services/api"

const { Text } = Typography

const ApiDocumentation: React.FC = () => {
  const { t } = useTranslation()
  const [spec, setSpec] = useState("")
  const [format, setFormat] = useState("yaml")
  const [loading, setLoading] = useState(false)
  const [collectionId, setCollectionId] = useState<number | undefined>()
  const [collections, setCollections] = useState<any[]>([])

  useEffect(() => {
    api.get("/api-test/collections").then(res => {
      if (res.data?.code === 200) setCollections(res.data.data || [])
    }).catch(() => {});
  }, [])

  const generateDoc = useCallback(async () => {
    if (!collectionId) { message.warning("请选择用例集"); return }
    setLoading(true)
    try {
      const res = await api.post("/swagger/generate", { collection_id: collectionId, format })
      if (res.data?.code === 200) {
        setSpec(typeof res.data.data === "string" ? res.data.data : JSON.stringify(res.data.data, null, 2))
        message.success("文档生成完成")
      }
    } catch { message.error("生成失败") } finally { setLoading(false) }
  }, [collectionId, format])

  const handleCopy = () => { navigator.clipboard.writeText(spec); message.success("已复制") }
  const handleDownload = () => {
    const ext = format === "yaml" ? "yaml" : "json"
    const blob = new Blob([spec], { type: "text/plain" })
    const url = URL.createObjectURL(blob); const a = document.createElement("a")
    a.href = url; a.download = "openapi." + ext; a.click(); URL.revokeObjectURL(url)
  }

  return (
    <div style={{ padding: 16 }}>
      <Card title={<Space><ApiOutlined /><Text strong>API 文档生成</Text></Space>}>
        <Space style={{ marginBottom: 12 }}>
          <Select placeholder="选择用例集" value={collectionId} onChange={setCollectionId} style={{ width: 200 }}
            options={collections.map(c => ({ value: c.id, label: c.name }))} />
          <Select value={format} onChange={setFormat} options={[{ value: "yaml", label: "YAML" }, { value: "json", label: "JSON" }]} />
          <Button type="primary" icon={<FileTextOutlined />} loading={loading} onClick={generateDoc}>生成文档</Button>
          {spec && <><Button icon={<CopyOutlined />} onClick={handleCopy}>复制</Button><Button icon={<DownloadOutlined />} onClick={handleDownload}>下载</Button></>}
        </Space>
        {spec ? (
          <MonacoEditor height={500} language={format === "yaml" ? "yaml" : "json"} theme="vs-light"
            value={spec} options={{ readOnly: true, minimap: { enabled: false }, fontSize: 12 }} />
        ) : (
          <Empty description="选择用例集后点击生成" style={{ marginTop: 60 }} />
        )}
      </Card>
    </div>
  )
}

export default ApiDocumentation
