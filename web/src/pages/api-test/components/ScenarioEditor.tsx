/**
 * 场景编排编辑器组件
 *
 * 支持多步骤链式请求编排：
 * - 步骤列表管理（添加/删除/排序）
 * - 步骤间变量提取配置
 * - 条件分支配置
 * - 场景执行与结果展示
 */
import { useState, useCallback } from "react"
import {
  Card, Button, Select, Input, Space, Table, Tag, Tooltip, Popconfirm,
  Typography, InputNumber, Collapse, Switch, Modal, message, Divider,
} from 'antd'
import {
  PlusOutlined, DeleteOutlined, PlayCircleOutlined, DragOutlined,
  SettingOutlined, BranchesOutlined, ArrowRightOutlined,
} from '@ant-design/icons'
import { useTranslation } from "react-i18next"

const { Text } = Typography


export interface ExtractorRule {
  name: string
  source: "body" | "header" | "status_code" | "response_time"
  path: string
}

export interface ScenarioStepData {
  id: string
  name: string
  method: string
  url: string
  headers: Record<string, string>
  params: Record<string, string>
  body: unknown
  body_type: string
  timeout: number
  extractors: ExtractorRule[]
  assertions: Array<{ type: string; operator: string; expected_value: string | number; body_path?: string; header_name?: string }>
  condition?: { type: string; operator: string; value: unknown; name?: string }
  on_success?: string
  on_failure?: string
  delay_ms: number
}

interface ScenarioEditorProps {
  steps: ScenarioStepData[]
  onChange: (steps: ScenarioStepData[]) => void
  onExecute: () => void
  executing: boolean
  executionResults?: {
    total: number; passed: number; failed: number; duration: number
    step_results: Array<{
      step_id: string; name: string; success: boolean; passed: boolean
      status_code?: number; response_time?: number; error?: string; skipped?: boolean
      assertions?: { total: number; passed: number; failed: number }
    }>
    variables?: Record<string, unknown>
  }
}

let stepCounter = 0
const genStepId = () => `step_${++stepCounter}_${Date.now().toString(36)}`

const METHOD_COLORS: Record<string, string> = {
  GET: "#52c41a", POST: "#1890ff", PUT: "#faad14", DELETE: "#ff4d4f", PATCH: "#722ed1",
}

const ScenarioEditor: React.FC<ScenarioEditorProps> = ({
  steps, onChange, onExecute, executing, executionResults,
}) => {
  const { t } = useTranslation()
  const [editingStepId, setEditingStepId] = useState<string | null>(null)

  const addStep = () => {
    const newStep: ScenarioStepData = {
      id: genStepId(), name: `步骤 ${steps.length + 1}`, method: "GET", url: "",
      headers: {}, params: {}, body: null, body_type: "json", timeout: 30,
      extractors: [], assertions: [], delay_ms: 0,
    }
    onChange([...steps, newStep])
  }

  const removeStep = (id: string) => {
    onChange(steps.filter(s => s.id !== id))
  }

  const updateStep = (id: string, updates: Partial<ScenarioStepData>) => {
    onChange(steps.map(s => s.id === id ? { ...s, ...updates } : s))
  }

  const moveStep = (index: number, direction: -1 | 1) => {
    const next = [...steps]
    const target = index + direction
    if (target < 0 || target >= next.length) return
    [next[index], next[target]] = [next[target], next[index]]
    onChange(next)
  }

  const addExtractor = (stepId: string) => {
    const step = steps.find(s => s.id === stepId)
    if (!step) return
    updateStep(stepId, {
      extractors: [...step.extractors, { name: "", source: "body", path: "" }],
    })
  }

  const getStepResult = (stepId: string) => {
    return executionResults?.step_results?.find(r => r.step_id === stepId)
  }


  return (
    <Card size="small" title={
      <Space>
        <BranchesOutlined />
        <Text strong>场景编排</Text>
        <Text type="secondary">({steps.length} 步)</Text>
      </Space>
    } extra={
      <Space>
        <Button type="primary" icon={<PlayCircleOutlined />} loading={executing}
          onClick={onExecute} disabled={steps.length === 0}>执行场景</Button>
        <Button icon={<PlusOutlined />} onClick={addStep}>添加步骤</Button>
      </Space>
    }>
      {/* 执行结果摘要 */}
      {executionResults && (
        <div style={{
          marginBottom: 12, padding: "8px 12px", borderRadius: 6,
          background: executionResults.failed > 0 ? "#fff2f0" : "#f6ffed",
          border: `1px solid ${executionResults.failed > 0 ? "#ffccc7" : "#b7eb8f"}`,
          display: "flex", alignItems: "center", gap: 16,
        }}>
          <Text strong>执行结果</Text>
          <Tag color="blue">{executionResults.total} 步</Tag>
          <Tag color="success">{executionResults.passed} 通过</Tag>
          {executionResults.failed > 0 && <Tag color="error">{executionResults.failed} 失败</Tag>}
          <Text type="secondary">耗时 {executionResults.duration}s</Text>
        </div>
      )}

      {/* 步骤列表 */}
      {steps.length === 0 ? (
        <div style={{ textAlign: "center", padding: "40px 0", color: "#999" }}>
          <BranchesOutlined style={{ fontSize: 32, marginBottom: 8 }} />
          <div>点击「添加步骤」开始编排场景</div>
          <div style={{ fontSize: 12, marginTop: 4 }}>支持多步骤链式请求、变量提取、条件分支</div>
        </div>
      ) : (
        <Space direction="vertical" style={{ width: "100%" }} size={8}>
          {steps.map((step, index) => {
            const result = getStepResult(step.id)
            const isEditing = editingStepId === step.id
            return (
              <Card key={step.id} size="small" style={{
                border: result ? (result.passed ? "1px solid #b7eb8f" : "1px solid #ffccc7") : undefined
              }} bodyStyle={{ padding: "8px 12px" }}>
                <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
                  {/* 步骤序号 */}
                  <div style={{ width: 24, textAlign: "center" }}>
                    {result ? (
                      result.skipped ? <Tag color="default">跳过</Tag> :
                      result.passed ? <Tag color="success">{index + 1}</Tag> :
                      <Tag color="error">{index + 1}</Tag>
                    ) : (
                      <Tag color="blue">{index + 1}</Tag>
                    )}
                  </div>

                  {/* 方法标签 */}
                  <Tag color={METHOD_COLORS[step.method] || "default"} style={{ margin: 0 }}>{step.method}</Tag>
                  <Input size="small" value={step.name}
                    onChange={e => updateStep(step.id, { name: e.target.value })}
                    style={{ width: 150 }} />
                  <Input size="small" value={step.url} placeholder="请求 URL"
                    onChange={e => updateStep(step.id, { url: e.target.value })}
                    style={{ flex: 1 }} />
                  <Select size="small" value={step.method} style={{ width: 80 }}
                    onChange={v => updateStep(step.id, { method: v })}
                    options={["GET","POST","PUT","DELETE","PATCH"].map(m => ({ value: m }))} />
                  {result && !result.skipped && (
                    <Space size={4}>
                      {result.status_code && <Tag>{result.status_code}</Tag>}
                      {result.response_time && <Text type="secondary" style={{ fontSize: 11 }}>{result.response_time}ms</Text>}
                    </Space>
                  )}
                  {result?.error && <Text type="danger" style={{ fontSize: 11 }}>{result.error}</Text>}
                  <Tooltip title="配置"><Button size="small" type="text" icon={<SettingOutlined />}
                    onClick={() => setEditingStepId(isEditing ? null : step.id)} /></Tooltip>
                  <Tooltip title="上移"><Button size="small" type="text" disabled={index === 0}
                    onClick={() => moveStep(index, -1)}>{String.fromCharCode(8593)}</Button></Tooltip>
                  <Tooltip title="下移"><Button size="small" type="text" disabled={index === steps.length - 1}
                    onClick={() => moveStep(index, 1)}>{String.fromCharCode(8595)}</Button></Tooltip>
                  <Popconfirm title="确认删除？" onConfirm={() => removeStep(step.id)}>
                    <Button size="small" type="text" danger icon={<DeleteOutlined />} />
                  </Popconfirm>
                </div>
                {isEditing && (
                  <div style={{ marginTop: 8, padding: "8px 12px", background: "#fafafa", borderRadius: 4 }}>
                    <Text strong style={{ fontSize: 12, marginBottom: 4, display: "block" }}>变量提取规则</Text>
                    {step.extractors.map((ext, ei) => (
                      <Space key={ei} style={{ marginBottom: 4 }} size={4}>
                        <Input size="small" placeholder="变量名" value={ext.name} style={{ width: 100 }}
                          onChange={e => { const exts=[...step.extractors]; exts[ei]={...exts[ei],name:e.target.value}; updateStep(step.id,{extractors:exts}) }} />
                        <Select size="small" value={ext.source} style={{ width: 100 }}
                          onChange={v => { const exts=[...step.extractors]; exts[ei]={...exts[ei],source:v}; updateStep(step.id,{extractors:exts}) }}
                          options={[{value:"body",label:"响应体"},{value:"header",label:"响应头"},{value:"status_code",label:"状态码"},{value:"response_time",label:"响应时间"}]} />
                        <Input size="small" placeholder="JSONPath" value={ext.path} style={{ width: 150 }}
                          onChange={e => { const exts=[...step.extractors]; exts[ei]={...exts[ei],path:e.target.value}; updateStep(step.id,{extractors:exts}) }} />
                        <Button size="small" type="text" danger icon={<DeleteOutlined />}
                          onClick={() => { updateStep(step.id,{extractors:step.extractors.filter((_,i)=>i!==ei)}) }} />
                      </Space>
                    ))}
                    <Button size="small" type="dashed" icon={<PlusOutlined />} onClick={() => addExtractor(step.id)}>添加提取规则</Button>
                    <div style={{ marginTop: 8 }}>
                      <Space size={8}>
                        <Text style={{ fontSize: 12 }}>步骤间延迟:</Text>
                        <InputNumber size="small" value={step.delay_ms} min={0} style={{ width: 80 }}
                          onChange={v => updateStep(step.id, { delay_ms: v || 0 })} />
                        <Text type="secondary" style={{ fontSize: 11 }}>ms</Text>
                      </Space>
                    </div>
                  </div>
                )}
              </Card>
            )
          })}
        </Space>
      )}

      {executionResults?.variables && Object.keys(executionResults.variables).length > 0 && (
        <div style={{ marginTop: 12 }}>
          <Divider style={{ margin: "8px 0" }} />
          <Text strong style={{ fontSize: 12 }}>提取的变量:</Text>
          <div style={{ marginTop: 4 }}>
            {Object.entries(executionResults.variables).map(([k, v]) => (
              <Tag key={k} color="blue" style={{ marginBottom: 4 }}>{k} = {String(v).substring(0, 50)}</Tag>
            ))}
          </div>
        </div>
      )}
    </Card>
  )
}

export default ScenarioEditor
