/**
 * 测试数据生成页面（AI 数据工厂前端）
 *
 * 支持配置数据 Schema，AI 自动生成测试数据。
 */
import { useState } from "react"
import { Card, Button, Input, Space, Table, Typography, Select, message, Divider } from "antd"
import { RobotOutlined, PlusOutlined, DeleteOutlined, DownloadOutlined, ExperimentOutlined } from "@ant-design/icons"
import { useTranslation } from "react-i18next"
import api from "@/services/api"

const { Text } = Typography

interface SchemaField {
  name: string; type: string; rule: string;
}

const DataFactory: React.FC = () => {
  const { t } = useTranslation()
  const [fields, setFields] = useState<SchemaField[]>([
    { name: "username", type: "string", rule: "" },
    { name: "email", type: "email", rule: "" },
    { name: "age", type: "number", rule: "18-65" },
  ])
  const [rowCount, setRowCount] = useState(10)
  const [generated, setGenerated] = useState<Record<string, unknown>[]>([])
  const [generating, setGenerating] = useState(false)

  const FIELD_TYPES = [
    { value: "string", label: t("dataFactory.types.string") },
    { value: "number", label: t("dataFactory.types.number") },
    { value: "email", label: t("dataFactory.types.email") },
    { value: "phone", label: t("dataFactory.types.phone") },
    { value: "name", label: t("dataFactory.types.name") },
    { value: "date", label: t("dataFactory.types.date") },
    { value: "boolean", label: t("dataFactory.types.boolean") },
    { value: "uuid", label: t("dataFactory.types.uuid") },
    { value: "address", label: t("dataFactory.types.address") },
    { value: "url", label: t("dataFactory.types.url") },
  ]

  const addField = () => setFields([...fields, { name: "", type: "string", rule: "" }])
  const removeField = (i: number) => setFields(fields.filter((_, idx) => idx !== i))
  const updateField = (i: number, updates: Partial<SchemaField>) => setFields(fields.map((f, idx) => idx === i ? { ...f, ...updates } : f))

  const handleGenerate = async () => {
    const validFields = fields.filter(f => f.name)
    if (validFields.length === 0) { message.warning(t("dataFactory.addOneField")); return }
    setGenerating(true)
    try {
      const res = await api.post("/ai/data-factory/generate", { schema: validFields, count: rowCount })
      if (res.data?.code === 200) { setGenerated(res.data.data || []); message.success(t("dataFactory.generateSuccess")) }
    } catch { message.error(t("dataFactory.generateFailed")) } finally { setGenerating(false) }
  }

  const handleExport = () => {
    if (generated.length === 0) return
    const headers = Object.keys(generated[0])
    const csv = [headers.join(","), ...generated.map(r => headers.map(h => JSON.stringify(r[h] ?? "")).join(","))].join('\n')
    const blob = new Blob([csv], { type: "text/csv" })
    const url = URL.createObjectURL(blob); const a = document.createElement("a")
    a.href = url; a.download = "test-data.csv"; a.click(); URL.revokeObjectURL(url)
  }

  return (
    <div className="fst-page">
      <div className="fst-page-header fst-animate-in">
        <h1 className="fst-page-title">{t("dataFactory.title")}</h1>
        <div className="fst-ios-card-subtitle">{t("dataFactory.subtitle")}</div>
      </div>
      <Card className="fst-ios-card fst-animate-in fst-animate-in-1">
        <Text strong>{t("dataFactory.schema")}</Text>
        <Table size="small" rowKey={(_, i) => String(i)} pagination={false} style={{ marginTop: 8 }}
          dataSource={fields.map((f, i) => ({ ...f, _i: i }))}
          columns={[
            { title: t("dataFactory.fieldName"), render: (_: unknown, r: SchemaField & { _i: number }) => <Input size="small" value={r.name} onChange={e => updateField(r._i, { name: e.target.value })} /> },
            { title: t("dataFactory.fieldType"), width: 120, render: (_: unknown, r: SchemaField & { _i: number }) => <Select size="small" value={r.type} style={{ width: "100%" }} onChange={v => updateField(r._i, { type: v })} options={FIELD_TYPES} /> },
            { title: t("dataFactory.fieldRule"), render: (_: unknown, r: SchemaField & { _i: number }) => <Input size="small" placeholder={t("dataFactory.fieldRule")} value={r.rule} onChange={e => updateField(r._i, { rule: e.target.value })} /> },
            { title: "", width: 40, render: (_: unknown, r: { _i: number }) => <Button type="text" size="small" danger icon={<DeleteOutlined />} onClick={() => removeField(r._i)} /> },
          ]}
          footer={() => <Button type="dashed" size="small" icon={<PlusOutlined />} block onClick={addField}>{t("dataFactory.addField")}</Button>} />
        <Divider />
        <Space>
          <Text>{t("dataFactory.rowCount")}:</Text>
          <Select value={rowCount} onChange={setRowCount} options={[5,10,20,50,100].map(n => ({ value: n, label: n + t("dataFactory.rowSuffix") }))} />
          <Button type="primary" icon={<RobotOutlined />} loading={generating} onClick={handleGenerate}>{t("dataFactory.generate")}</Button>
          {generated.length > 0 && <Button icon={<DownloadOutlined />} onClick={handleExport}>{t("dataFactory.exportCsv")}</Button>}
        </Space>
        {generated.length > 0 && (
          <div style={{ marginTop: 12 }}>
            <Text strong>{t("dataFactory.preview")}</Text>
            <Table size="small" rowKey={(_, i) => String(i)} pagination={false} style={{ marginTop: 4 }}
              dataSource={generated.slice(0, 10)}
              columns={Object.keys(generated[0]).map(k => ({ title: k, dataIndex: k, key: k, ellipsis: true }))} />
          </div>
        )}
      </Card>
    </div>
  )
}

export default DataFactory
