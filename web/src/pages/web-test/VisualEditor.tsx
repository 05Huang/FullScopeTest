/**
 * Web 测试无代码可视化编排器
 *
 * 提供拖拽式步骤编排面板：
 * - 拖拽添加「点击/输入/等待/断言/截图」步骤
 * - 每步配置参数（选择器、输入值、等待时间）
 * - 实时预览生成的 Playwright 脚本
 */
import { useState, useCallback } from "react"
import {
  Card, Button, Select, Input, Space, Table, Tag, Tooltip, Popconfirm,
  Typography, InputNumber, Switch, Collapse, Divider, message,
} from 'antd'
import {
  PlusOutlined, DeleteOutlined, PlayCircleOutlined, CodeOutlined,
  DragOutlined, MousePointerOutlined, EditOutlined, ClockCircleOutlined,
  CheckCircleOutlined, CameraOutlined, EyeOutlined, ReloadOutlined,
} from '@ant-design/icons'
import { useTranslation } from "react-i18next"
import MonacoEditor from "@monaco-editor/react"

const { Text } = Typography

export interface WebTestStep {
  id: string
  action: "click" | "fill" | "select" | "wait" | "assert" | "screenshot" | "navigate" | "hover" | "press" | "scroll"
  selector: string
  value: string
  description: string
  timeout: number
  enabled: boolean
}

interface VisualEditorProps {
  steps: WebTestStep[]
  onChange: (steps: WebTestStep[]) => void
  onExecute?: () => void
  executing?: boolean
}

const ACTION_OPTIONS = [
  { value: "navigate", label: "导航", icon: <EyeOutlined />, color: "blue" },
  { value: "click", label: "点击", icon: <MousePointerOutlined />, color: "green" },
  { value: "fill", label: "输入", icon: <EditOutlined />, color: "cyan" },
  { value: "select", label: "选择", icon: <DragOutlined />, color: "purple" },
  { value: "wait", label: "等待", icon: <ClockCircleOutlined />, color: "orange" },
  { value: "assert", label: "断言", icon: <CheckCircleOutlined />, color: "red" },
  { value: "screenshot", label: "截图", icon: <CameraOutlined />, color: "magenta" },
  { value: "hover", label: "悬停", icon: <MousePointerOutlined />, color: "geekblue" },
  { value: "press", label: "按键", icon: <DragOutlined />, color: "volcano" },
  { value: "scroll", label: "滚动", icon: <DragOutlined />, color: "gold" },
]

let idCounter = 0
const genId = () => "step_" + (++idCounter) + "_" + Date.now().toString(36)

/** 将步骤列表转换为 Playwright 脚本 */
function generateScript(steps: WebTestStep[]): string {
  const lines: string[] = ["const { test, expect } = require("@playwright/test");", "", "test("录制的测试", async ({ page }) => {"];
  steps.filter(s => s.enabled).forEach(step => {
    const timeout = step.timeout !== 30000 ? ", { timeout: " + step.timeout + " }" : "";
    const desc = step.description ? " // " + step.description : "";
    switch (step.action) {
      case "navigate": lines.push("  await page.goto("" + step.value + "");" + desc); break;
      case "click": lines.push("  await page.click("" + step.selector + """ + timeout + ");" + desc); break;
      case "fill": lines.push("  await page.fill("" + step.selector + "", "" + step.value + """ + timeout + ");" + desc); break;
      case "select": lines.push("  await page.selectOption("" + step.selector + "", "" + step.value + "");" + desc); break;
      case "wait":
        if (step.selector) lines.push("  await page.waitForSelector("" + step.selector + """ + timeout + ");" + desc);
        else lines.push("  await page.waitForTimeout(" + (parseInt(step.value) || 1000) + ");" + desc);
        break;
      case "assert":
        if (step.value === "visible") lines.push("  await expect(page.locator("" + step.selector + "")).toBeVisible();" + desc);
        else if (step.value === "hidden") lines.push("  await expect(page.locator("" + step.selector + "")).toBeHidden();" + desc);
        else if (step.value === "enabled") lines.push("  await expect(page.locator("" + step.selector + "")).toBeEnabled();" + desc);
        else lines.push("  await expect(page.locator("" + step.selector + "")).toContainText("" + step.value + "");" + desc);
        break;
      case "screenshot": lines.push("  await page.screenshot({ path: "" + (step.value || "screenshot.png") + "" });" + desc); break;
      case "hover": lines.push("  await page.hover("" + step.selector + "");" + desc); break;
      case "press": lines.push("  await page.press("" + step.selector + "", "" + step.value + "");" + desc); break;
      case "scroll": lines.push("  await page.evaluate(() => window.scrollBy(0, " + (parseInt(step.value) || 500) + "));" + desc); break;
    }
  });
  lines.push("});");
  return lines.join("
");
}


const VisualEditor: React.FC<VisualEditorProps> = ({ steps, onChange, onExecute, executing }) => {
  const { t } = useTranslation()
  const [showScript, setShowScript] = useState(false)

  const addStep = (action: WebTestStep["action"] = "click") => {
    const actionInfo = ACTION_OPTIONS.find(a => a.value === action)
    onChange([...steps, {
      id: genId(), action, selector: "", value: "", description: "", timeout: 30000, enabled: true,
    }])
  }

  const updateStep = (id: string, updates: Partial<WebTestStep>) => {
    onChange(steps.map(s => s.id === id ? { ...s, ...updates } : s))
  }

  const removeStep = (id: string) => { onChange(steps.filter(s => s.id !== id)) }
  const moveStep = (index: number, dir: -1 | 1) => {
    const next = [...steps]; const t = index + dir;
    if (t < 0 || t >= next.length) return;
    [next[index], next[t]] = [next[t], next[index]]; onChange(next)
  }

  const getActionInfo = (action: string) => ACTION_OPTIONS.find(a => a.value === action) || ACTION_OPTIONS[0]

  return (
    <Card size="small" title={<Space><CodeOutlined /><Text strong>可视化编排</Text><Text type="secondary">({steps.length} 步)</Text></Space>}
      extra={<Space>
        <Button icon={<PlusOutlined />} onClick={() => addStep()}>添加步骤</Button>
        <Button type={showScript ? "primary" : "default"} onClick={() => setShowScript(!showScript)}>生成脚本</Button>
        {onExecute && <Button type="primary" icon={<PlayCircleOutlined />} loading={executing} onClick={onExecute}>执行</Button>}
      </Space>}>
      {/* 快速添加栏 */}
      <div style={{ marginBottom: 8 }}>
        <Space wrap>
          {ACTION_OPTIONS.map(opt => (
            <Button key={opt.value} size="small" icon={opt.icon} onClick={() => addStep(opt.value as WebTestStep["action"])}>
              {opt.label}
            </Button>
          ))}
        </Space>
      </div>

      {/* 步骤列表 */}
      {steps.length === 0 ? (
        <div style={{ textAlign: "center", padding: "30px 0", color: "#999" }}>
          <CodeOutlined style={{ fontSize: 28, marginBottom: 8 }} />
          <div>点击上方按钮或「添加步骤」开始编排</div>
        </div>
      ) : (
        <Table size="small" rowKey="id" pagination={false}
          dataSource={steps.map((s, i) => ({ ...s, _index: i }))}
          columns={[
            { title: "#", width: 35, render: (_: any, __: any, i: number) => <Text type="secondary" style={{ fontSize: 11 }}>{i + 1}</Text> },
            { title: "操作", width: 100, render: (_: any, r: WebTestStep & { _index: number }) => (
              <Select size="small" value={r.action} style={{ width: "100%" }}
                onChange={v => updateStep(r.id, { action: v })}
                options={ACTION_OPTIONS.map(a => ({ value: a.value, label: <Space size={4}>{a.icon}<span>{a.label}</span></Space> }))} />
            )},
            { title: "选择器", render: (_: any, r: WebTestStep) => (
              <Input size="small" placeholder="CSS 选择器 / URL" value={r.selector}
                onChange={e => updateStep(r.id, { selector: e.target.value })} />
            )},
            { title: "值", width: 180, render: (_: any, r: WebTestStep) => (
              <Input size="small" placeholder={r.action === "fill" ? "输入内容" : r.action === "navigate" ? "URL" : r.action === "assert" ? "visible / 文本" : "值"}
                value={r.value} onChange={e => updateStep(r.id, { value: e.target.value })} />
            )},
            { title: "说明", width: 120, render: (_: any, r: WebTestStep) => (
              <Input size="small" placeholder="可选" value={r.description}
                onChange={e => updateStep(r.id, { description: e.target.value })} />
            )},
            { title: "", width: 60, render: (_: any, r: WebTestStep & { _index: number }) => (
              <Space size={0}>
                <Switch size="small" checked={r.enabled} onChange={v => updateStep(r.id, { enabled: v })} />
                <Popconfirm title="删除？" onConfirm={() => removeStep(r.id)}><Button type="text" size="small" danger icon={<DeleteOutlined />} /></Popconfirm>
              </Space>
            )},
          ]} />
      )}

      {/* 生成的脚本预览 */}
      {showScript && (
        <div style={{ marginTop: 12 }}>
          <MonacoEditor height={250} language="javascript" theme="vs-light"
            value={generateScript(steps)} options={{ readOnly: true, minimap: { enabled: false }, fontSize: 12 }} />
        </div>
      )}
    </Card>
  )
}

export default VisualEditor
