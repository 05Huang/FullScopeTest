/**
 * 测试数据生成页面（AI 数据工厂前端）
 *
 * 支持配置数据 Schema，AI 自动生成测试数据。
 */
import { useState } from "react"
import { Card, Button, Input, Space, Table, Tag, Typography, Select, message, Divider } from "antd"
import { RobotOutlined, PlusOutlined, DeleteOutlined, DownloadOutlined, ExperimentOutlined } from "@ant-design/icons"
import { useTranslation } from "react-i18next"
import api from "@/services/api"

const { Text } = Typography
const { TextArea } = Input

interface SchemaField {
  name: string; type: string; rule: string;
}

const FIELD_TYPES = [
  { value: "string", label: "字符串" },
  { value: "number", label: "数字" },
  { value: "email", label: "邮箱" },
  { value: "phone", label: "手机号" },
  { value: "name", label: "姓名" },
  { value: "date", label: "日期" },
  { value: "boolean", label: "布尔值" },
  { value: "uuid", label: "UUID" },
  { value: "address", label: "地址" },
  { value: "url", label: "URL" },
]

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

  const addField = () => setFields([...fields, { name: "", type: "string", rule: "" }])
  const removeField = (i: number) => setFields(fields.filter((_, idx) => idx !== i))
  const updateField = (i: number, updates: Partial<SchemaField>) => setFields(fields.map((f, idx) => idx === i ? { ...f, ...updates } : f))

  const handleGenerate = async () => {
    const validFields = fields.filter(f => f.name)
    if (validFields.length === 0) { message.warning("请至少添加一个字段"); return }
    setGenerating(true)
    try {
      const res = await api.post("/ai/data-factory/generate", { schema: validFields, count: rowCount })
      if (res.data?.code === 200) { setGenerated(res.data.data || []); message.success("生成完成") }
    } catch { message.error("生成失败") } finally { setGenerating(false) }
  }

  const handleExport = () => {
    if (generated.length === 0) return
    const headers = Object.keys(generated[0])
    const csv = [headers.join(","), ...generated.map(r => headers.map(h => JSON.stringify(r[h] ?? "")).join(","))].join("
")
    const blob = new Blob([csv], { type: "text/csv" })
    const url = URL.createObjectURL(blob); const a = document.createElement("a")
    a.href = url; a.download = "test-data.csv"; a.click(); URL.revokeObjectURL(url)
  }

  return (
    <div style={{ padding: 16 }}>
      <Card title={<Space><ExperimentOutlined /><Text strong>AI 数据工厂</Text></Space>}>
        {/* Schema 配置 */}
        <Text strong>数据 Schema</Text>
        <Table size="small" rowKey={(_, i) => String(i)} pagination={false} style={{ marginTop: 8 }}
          dataSource={fields.map((f, i) => ({ ...f, _i: i }))}
          columns={[
            { title: "字段名", render: (_: any, r: SchemaField & { _i: number }) => <Input size="small" value={r.name} onChange={e => updateField(r._i, { name: e.target.value })} /> },
            { title: "类型", width: 120, render: (_: any, r: SchemaField & { _i: number }) => <Select size="small" value={r.type} style={{ width: "100%" }} onChange={v => updateField(r._i, { type: v })} options={FIELD_TYPES} /> },
            { title: "规则", render: (_: any, r: SchemaField & { _i: number }) => <Input size="small" placeholder="如 18-65" value={r.rule} onChange={e => updateField(r._i, { rule: e.target.value })} /> },
            { title: "", width: 40, render: (_: any, r: { _i: number }) => <Button type="text" size="small" danger icon={<DeleteOutlined />} onClick={() => removeField(r._i)} /> },
          ]}
          footer={() => <Button type="dashed" size="small" icon={<PlusOutlined />} block onClick={addField}>添加字段</Button>} />
        <Divider />
        <Space>
          <Text>生成行数:</Text>
          <Select value={rowCount} onChange={setRowCount} options={[5,10,20,50,100].map(n => ({ value: n, label: n + " 行" }))} />
          <Button type="primary" icon={<RobotOutlined />} loading={generating} onClick={handleGenerate}>AI 生成</Button>
          {generated.length > 0 && <Button icon={<DownloadOutlined />} onClick={handleExport}>导出 CSV</Button>}
        </Space>
        {/* 生成结果预览 */}
        {generated.length > 0 && (
          <div style={{ marginTop: 12 }}>
            <Text strong>预览 (前 10 行)</Text>
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
