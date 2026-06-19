/**
 * 报告模板编辑器页面
 *
 * 支持自定义报告模板：选择展示模块、排序、配色。
 */
import { useState } from "react"
import { Card, Checkbox, Space, Typography, Button, Input, Select, message, Divider, Tag } from "antd"
import { SaveOutlined, EyeOutlined, FileTextOutlined } from "@ant-design/icons"
import { useTranslation } from "react-i18next"
import api from "@/services/api"

const { Text, Title } = Typography

interface TemplateModule {
  id: string; name: string; enabled: boolean; order: number;
}

const DEFAULT_MODULES: TemplateModule[] = [
  { id: "summary", name: "执行摘要", enabled: true, order: 1 },
  { id: "pass_rate", name: "通过率统计", enabled: true, order: 2 },
  { id: "duration", name: "执行时长", enabled: true, order: 3 },
  { id: "failed_cases", name: "失败用例详情", enabled: true, order: 4 },
  { id: "trend", name: "质量趋势", enabled: false, order: 5 },
  { id: "env_info", name: "环境信息", enabled: true, order: 6 },
  { id: "ai_analysis", name: "AI 分析", enabled: false, order: 7 },
  { id: "screenshots", name: "截图附件", enabled: false, order: 8 },
]

const ReportTemplateEditor: React.FC = () => {
  const { t } = useTranslation()
  const [templateName, setTemplateName] = useState("默认模板")
  const [modules, setModules] = useState<TemplateModule[]>(DEFAULT_MODULES)
  const [theme, setTheme] = useState("default")

  const toggleModule = (id: string) => {
    setModules(prev => prev.map(m => m.id === id ? { ...m, enabled: !m.enabled } : m))
  }

  const handleSave = async () => {
    try {
      await api.post("/report-templates", {
        name: templateName,
        modules: modules.filter(m => m.enabled).sort((a, b) => a.order - b.order),
        theme,
      })
      message.success("模板已保存")
    } catch { message.error("保存失败") }
  }

  return (
    <div style={{ padding: 16, maxWidth: 800, margin: "0 auto" }}>
      <Card title={<Space><FileTextOutlined /><Text strong>报告模板编辑器</Text></Space>}
        extra={<Space>
          <Button icon={<SaveOutlined />} type="primary" onClick={handleSave}>保存模板</Button>
        </Space>}>
        <Space direction="vertical" style={{ width: "100%" }} size="large">
          <div>
            <Text strong>模板名称</Text>
            <Input value={templateName} onChange={e => setTemplateName(e.target.value)} style={{ marginTop: 4 }} />
          </div>
          <div>
            <Text strong>主题配色</Text>
            <Select value={theme} onChange={setTheme} style={{ width: "100%", marginTop: 4 }}
              options={[{ value: "default", label: "默认蓝" }, { value: "green", label: "清新绿" }, { value: "dark", label: "暗夜黑" }, { value: "warm", label: "暖橙" }]} />
          </div>
          <Divider style={{ margin: 0 }} />
          <div>
            <Text strong>报告模块</Text>
            <Text type="secondary" style={{ marginLeft: 8, fontSize: 12 }}>勾选要包含的模块，按顺序展示</Text>
            <div style={{ marginTop: 8 }}>
              {modules.map(m => (
                <div key={m.id} style={{ padding: "8px 12px", marginBottom: 4, background: m.enabled ? "#f6ffed" : "#fafafa", borderRadius: 4, display: "flex", alignItems: "center", gap: 8 }}>
                  <Checkbox checked={m.enabled} onChange={() => toggleModule(m.id)} />
                  <Text style={{ flex: 1 }}>{m.name}</Text>
                  <Tag>{m.order}</Tag>
                </div>
              ))}
            </div>
          </div>
        </Space>
      </Card>
    </div>
  )
}

export default ReportTemplateEditor
