/**
 * 性能测试多步骤场景编辑器
 * 支持配置多步骤用户旅程（登录 -> 浏览 -> 下单）
 */
import { useState } from "react"
import { Card, Button, Select, Input, Space, Table, Tag, Popconfirm, Typography, InputNumber, Tooltip } from "antd"
import { PlusOutlined, DeleteOutlined, ClockCircleOutlined, ArrowRightOutlined } from "@ant-design/icons"
import { useTranslation } from "react-i18next"

const { Text } = Typography

export interface PerfScenarioStep {
  id: string; name: string; method: string; url: string;
  headers: Record<string, string>; body: string;
  think_time_ms: number; weight: number;
  extract_vars: Array<{ name: string; path: string }>; enabled: boolean;
}

interface ScenarioStepEditorProps { steps: PerfScenarioStep[]; onChange: (steps: PerfScenarioStep[]) => void }

let counter = 0
const genId = () => "perf_step_" + (++counter)

const ScenarioStepEditor: React.FC<ScenarioStepEditorProps> = ({ steps, onChange }) => {
  const { t } = useTranslation()
  const addStep = () => onChange([...steps, {
    id: genId(), name: "步骤 " + (steps.length + 1), method: "GET", url: "",
    headers: {}, body: "", think_time_ms: 1000, weight: 1, extract_vars: [], enabled: true,
  }])
  const updateStep = (id: string, u: Partial<PerfScenarioStep>) => onChange(steps.map(s => s.id === id ? { ...s, ...u } : s))
  const removeStep = (id: string) => onChange(steps.filter(s => s.id !== id))

  const columns = [
    { title: "#", width: 30, render: (_: any, __: any, i: number) => <Text type="secondary" style={{ fontSize: 11 }}>{i + 1}</Text> },
    { title: "步骤名", width: 120, render: (_: any, r: PerfScenarioStep) => <Input size="small" value={r.name} onChange={e => updateStep(r.id, { name: e.target.value })} /> },
    { title: "方法", width: 80, render: (_: any, r: PerfScenarioStep) => <Select size="small" value={r.method} style={{ width: "100%" }} onChange={v => updateStep(r.id, { method: v })} options={["GET","POST","PUT","DELETE"].map(m => ({ value: m }))} /> },
    { title: "URL", render: (_: any, r: PerfScenarioStep) => <Input size="small" placeholder="请求 URL" value={r.url} onChange={e => updateStep(r.id, { url: e.target.value })} /> },
    { title: "思考时间", width: 100, render: (_: any, r: PerfScenarioStep) => <Tooltip title="ms"><InputNumber size="small" value={r.think_time_ms} min={0} step={500} style={{ width: 80 }} onChange={v => updateStep(r.id, { think_time_ms: v || 0 })} /></Tooltip> },
    { title: "权重", width: 70, render: (_: any, r: PerfScenarioStep) => <InputNumber size="small" value={r.weight} min={1} max={100} style={{ width: 60 }} onChange={v => updateStep(r.id, { weight: v || 1 })} /> },
    { title: "", width: 50, render: (_: any, r: PerfScenarioStep) => <Popconfirm title="删除？" onConfirm={() => removeStep(r.id)}><Button type="text" size="small" danger icon={<DeleteOutlined />} /></Popconfirm> },
  ]

  return (
    <Card size="small" title={<Space><ClockCircleOutlined /><Text strong>用户旅程步骤</Text></Space>}
      extra={<Button size="small" icon={<PlusOutlined />} onClick={addStep}>添加步骤</Button>}>
      {steps.length === 0 ? (
        <div style={{ textAlign: "center", padding: "20px 0", color: "#999" }}>点击「添加步骤」配置用户旅程</div>
      ) : (
        <Table size="small" rowKey="id" pagination={false}
          dataSource={steps.map((s, i) => ({ ...s, _index: i }))} columns={columns} />
      )}
      {steps.length > 1 && <div style={{ marginTop: 8 }}><Text type="secondary" style={{ fontSize: 11 }}><ArrowRightOutlined /> 步骤按顺序执行，每步之间插入「思考时间」模拟真实用户</Text></div>}
    </Card>
  )
}

export default ScenarioStepEditor
