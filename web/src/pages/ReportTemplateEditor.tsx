/**
 * 报告模板编辑器页面
 *
 * 支持自定义报告模板：选择展示模块、排序、配色。
 */
import { useState } from "react"
import { Card, Checkbox, Space, Typography, Button, Input, Select, message, Divider, Tag } from "antd"
import { SaveOutlined, FileTextOutlined } from "@ant-design/icons"
import { useTranslation } from "react-i18next"
import api from "@/services/api"

const { Text } = Typography

interface TemplateModule {
  id: string; name: string; enabled: boolean; order: number;
}

const ReportTemplateEditor: React.FC = () => {
  const { t } = useTranslation()
  const [templateName, setTemplateName] = useState(t("reportTemplates.title"))
  const [modules, setModules] = useState<TemplateModule[]>([
    { id: "summary", name: t("reportTemplates.modules.summary"), enabled: true, order: 1 },
    { id: "pass_rate", name: t("reportTemplates.modules.passRate"), enabled: true, order: 2 },
    { id: "duration", name: t("reportTemplates.modules.duration"), enabled: true, order: 3 },
    { id: "failed_cases", name: t("reportTemplates.modules.failedCases"), enabled: true, order: 4 },
    { id: "trend", name: t("reportTemplates.modules.trend"), enabled: false, order: 5 },
    { id: "env_info", name: t("reportTemplates.modules.envInfo"), enabled: true, order: 6 },
    { id: "ai_analysis", name: t("reportTemplates.modules.aiAnalysis"), enabled: false, order: 7 },
    { id: "screenshots", name: t("reportTemplates.modules.screenshots"), enabled: false, order: 8 },
  ])
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
      message.success(t("reportTemplates.saveSuccess"))
    } catch { message.error(t("reportTemplates.saveFailed")) }
  }

  return (
    <div className="fst-page" style={{ maxWidth: 800, margin: "0 auto" }}>
      <div className="fst-page-header fst-animate-in">
        <h1 className="fst-page-title">{t("reportTemplates.title")}</h1>
        <div className="fst-ios-card-subtitle">{t("reportTemplates.subtitle")}</div>
      </div>
      <Card className="fst-ios-card fst-animate-in fst-animate-in-1"
        title={<Space><FileTextOutlined /><Text strong>{t("reportTemplates.title")}</Text></Space>}
        extra={<Button icon={<SaveOutlined />} type="primary" onClick={handleSave}>{t("reportTemplates.save")}</Button>}>
        <Space direction="vertical" style={{ width: "100%" }} size="large">
          <div>
            <Text strong>{t("reportTemplates.templateName")}</Text>
            <Input value={templateName} onChange={e => setTemplateName(e.target.value)} style={{ marginTop: 4 }} />
          </div>
          <div>
            <Text strong>{t("reportTemplates.themeColor")}</Text>
            <Select value={theme} onChange={setTheme} style={{ width: "100%", marginTop: 4 }}
              options={[
                { value: "default", label: t("reportTemplates.themes.default") },
                { value: "green", label: t("reportTemplates.themes.green") },
                { value: "dark", label: t("reportTemplates.themes.dark") },
                { value: "warm", label: t("reportTemplates.themes.warm") },
              ]} />
          </div>
          <Divider style={{ margin: 0 }} />
          <div>
            <Text strong>{t("reportTemplates.reportModules")}</Text>
            <Text type="secondary" style={{ marginLeft: 8, fontSize: 12 }}>{t("reportTemplates.moduleHint")}</Text>
            <div style={{ marginTop: 8 }}>
              {modules.map(m => (
                <div key={m.id} style={{ padding: "8px 12px", marginBottom: 4, background: m.enabled ? "rgba(45,106,100,0.06)" : "var(--fst-surface-dim)", borderRadius: 8, display: "flex", alignItems: "center", gap: 8 }}>
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
