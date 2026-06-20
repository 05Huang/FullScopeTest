/**
 * API 文档生成页面
 *
 * 从测试用例自动生成 OpenAPI 文档，在线预览和导出。
 */
import { useState, useEffect, useCallback } from "react"
import { Card, Button, Space, Typography, Select, message, Empty } from "antd"
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
  const [collections, setCollections] = useState<Record<string, unknown>[]>([])

  useEffect(() => {
    api.get("/api-test/collections").then(res => {
      if (res.data?.code === 200) setCollections(res.data.data || [])
    }).catch(() => {});
  }, [])

  const generateDoc = useCallback(async () => {
    if (!collectionId) { message.warning(t("apiDocsGen.selectCollectionWarning")); return }
    setLoading(true)
    try {
      const res = await api.post("/swagger/generate", { collection_id: collectionId, format })
      if (res.data?.code === 200) {
        setSpec(typeof res.data.data === "string" ? res.data.data : JSON.stringify(res.data.data, null, 2))
        message.success(t("apiDocsGen.generateSuccess"))
      }
    } catch { message.error(t("apiDocsGen.generateFailed")) } finally { setLoading(false) }
  }, [collectionId, format, t])

  const handleCopy = () => { navigator.clipboard.writeText(spec); message.success(t("apiDocsGen.copied")) }
  const handleDownload = () => {
    const ext = format === "yaml" ? "yaml" : "json"
    const blob = new Blob([spec], { type: "text/plain" })
    const url = URL.createObjectURL(blob); const a = document.createElement("a")
    a.href = url; a.download = "openapi." + ext; a.click(); URL.revokeObjectURL(url)
  }

  return (
    <div className="fst-page">
      <div className="fst-page-header fst-animate-in">
        <h1 className="fst-page-title">{t("apiDocsGen.title")}</h1>
        <div className="fst-ios-card-subtitle">{t("apiDocsGen.subtitle")}</div>
      </div>
      <Card className="fst-ios-card fst-animate-in fst-animate-in-1"
        title={<Space><ApiOutlined /><Text strong>{t("apiDocsGen.title")}</Text></Space>}>
        <Space style={{ marginBottom: 12 }}>
          <Select placeholder={t("apiDocsGen.selectCollection")} value={collectionId} onChange={setCollectionId} style={{ width: 200 }}
            options={collections.map(c => ({ value: c.id as number, label: c.name as string }))} />
          <Select value={format} onChange={setFormat} options={[{ value: "yaml", label: "YAML" }, { value: "json", label: "JSON" }]} />
          <Button type="primary" icon={<FileTextOutlined />} loading={loading} onClick={generateDoc}>{t("apiDocsGen.generate")}</Button>
          {spec && <>
            <Button icon={<CopyOutlined />} onClick={handleCopy}>{t("apiDocsGen.copy")}</Button>
            <Button icon={<DownloadOutlined />} onClick={handleDownload}>{t("apiDocsGen.download")}</Button>
          </>}
        </Space>
        {spec ? (
          <MonacoEditor height={500} language={format === "yaml" ? "yaml" : "json"} theme="vs-light"
            value={spec} options={{ readOnly: true, minimap: { enabled: false }, fontSize: 12 }} />
        ) : (
          <Empty description={t("apiDocsGen.selectHint")} style={{ marginTop: 60 }} />
        )}
      </Card>
    </div>
  )
}

export default ApiDocumentation
