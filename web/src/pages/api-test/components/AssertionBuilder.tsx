/**
 * 可视化断言构建器组件
 *
 * 允许用户通过表单方式创建断言规则，无需编写 JavaScript 脚本。
 * 支持四种断言类型：状态码、响应时间、响应头、响应体。
 */
import { useState } from 'react'
import {
  Button, Select, Input, Space, Table, Tag, Tooltip, Popconfirm,
  Typography, InputNumber, Switch,
} from 'antd'
import {
  PlusOutlined, DeleteOutlined, CheckCircleOutlined,
  CloseCircleOutlined, InfoCircleOutlined,
} from '@ant-design/icons'
import { useTranslation } from 'react-i18next'

const { Text } = Typography

/** 单条断言规则 */
export interface AssertionRule {
  type: 'status_code' | 'response_time' | 'header' | 'body'
  operator: string
  expected_value: string | number
  header_name?: string
  body_path?: string
  description?: string
  enabled: boolean
}

interface AssertionBuilderProps {
  assertions: AssertionRule[]
  onChange: (assertions: AssertionRule[]) => void
  assertionResults?: {
    total: number; passed: number; failed: number;
    details?: Array<{
      name: string; passed: boolean; actual?: unknown;
      expected?: unknown; error?: string; assertion_type?: string;
    }>
  }
  showResults?: boolean
}

const ASSERTION_TYPES = [
  { value: "status_code", label: "状态码", color: "blue" },
  { value: "response_time", label: "响应时间", color: "orange" },
  { value: "header", label: "响应头", color: "purple" },
  { value: "body", label: "响应体", color: "green" },
]

const OPERATORS: Record<string, { value: string; label: string }[]> = {
  status_code: [
    { value: "equals", label: "等于" },
    { value: "not_equals", label: "不等于" },
    { value: "greater_than", label: "大于" },
    { value: "less_than", label: "小于" },
    { value: "greater_than_or_equals", label: "大于等于" },
    { value: "less_than_or_equals", label: "小于等于" },
  ],
  response_time: [
    { value: "less_than", label: "小于 (ms)" },
    { value: "greater_than", label: "大于 (ms)" },
    { value: "less_than_or_equals", label: "小于等于 (ms)" },
    { value: "greater_than_or_equals", label: "大于等于 (ms)" },
  ],
  header: [
    { value: "exists", label: "存在" },
    { value: "not_exists", label: "不存在" },
    { value: "equals", label: "值等于" },
    { value: "contains", label: "值包含" },
  ],
  body: [
    { value: "equals", label: "等于" },
    { value: "not_equals", label: "不等于" },
    { value: "contains", label: "包含" },
    { value: "not_contains", label: "不包含" },
    { value: "regex", label: "正则匹配" },
    { value: "type_is", label: "类型是" },
    { value: "exists", label: "存在" },
    { value: "not_exists", label: "不存在" },
    { value: "greater_than", label: "大于" },
    { value: "less_than", label: "小于" },
    { value: "length_equals", label: "长度等于" },
    { value: "is_empty", label: "为空" },
    { value: "is_not_empty", label: "不为空" },
  ],
}

const NEEDS_VALUE = new Set([
  "equals", "not_equals", "contains", "not_contains", "regex",
  "type_is", "greater_than", "less_than", "greater_than_or_equals",
  "less_than_or_equals", "length_equals",
])

const DEFAULT_OPERATORS: Record<string, string> = {
  status_code: "equals",
  response_time: "less_than",
  header: "exists",
  body: "equals",
}

const AssertionBuilder: React.FC<AssertionBuilderProps> = ({
  assertions, onChange, assertionResults, showResults = false,
}) => {
  const { t } = useTranslation()

  const addAssertion = () => {
    onChange([
      ...assertions,
      { type: "status_code", operator: "equals", expected_value: 200, description: "", enabled: true },
    ])
  }

  const updateAssertion = (index: number, updates: Partial<AssertionRule>) => {
    const next = assertions.map((a, i) => {
      if (i !== index) return a
      const merged = { ...a, ...updates }
      if (updates.type && updates.type !== a.type) {
        merged.operator = DEFAULT_OPERATORS[updates.type] || "equals"
        if (updates.type === "status_code") merged.expected_value = 200
        else if (updates.type === "response_time") merged.expected_value = 1000
        else merged.expected_value = ""
        merged.header_name = undefined
        merged.body_path = undefined
      }
      return merged
    })
    onChange(next)
  }

  const removeAssertion = (index: number) => {
    onChange(assertions.filter((_, i) => i !== index))
  }

  const needsValue = (rule: AssertionRule) => NEEDS_VALUE.has(rule.operator)

  const getPathPlaceholder = (type: string) => {
    if (type === "header") return "Header 名称 (如 content-type)"
    return "JSONPath (如 data.items[0].id)"
  }

  const getValuePlaceholder = (rule: AssertionRule) => {
    if (rule.type === "status_code") return "200"
    if (rule.type === "response_time") return "1000"
    if (rule.operator === "type_is") return "string / number / array / object"
    return "期望值"
  }

  const getResult = (index: number) => {
    if (!assertionResults?.details) return undefined
    return assertionResults.details[index]
  }

  const columns = [
    {
      title: "#", width: 40,
      render: (_: unknown, __: unknown, index: number) => <Text type="secondary" style={{ fontSize: 12 }}>{index + 1}</Text>,
    },
    {
      title: "类型", width: 120,
      render: (_: unknown, record: AssertionRule, index: number) => (
        <Select size="small" value={record.type} style={{ width: "100%" }}
          onChange={(v) => updateAssertion(index, { type: v as AssertionRule["type"] })}
          options={ASSERTION_TYPES.map((tp) => ({
            value: tp.value,
            label: <Tag color={tp.color} style={{ margin: 0 }}>{tp.label}</Tag>,
          }))} />
      ),
    },
    {
      title: "条件", width: 200,
      render: (_: unknown, record: AssertionRule, index: number) => {
        const parts: React.ReactNode[] = []
        if (record.type === "header" || record.type === "body") {
          parts.push(
            <Input key="path" size="small"
              placeholder={getPathPlaceholder(record.type)}
              value={record.type === "header" ? record.header_name || "" : record.body_path || ""}
              onChange={(e) => updateAssertion(index, record.type === "header"
                ? { header_name: e.target.value } : { body_path: e.target.value })}
              style={{ width: "100%", marginBottom: 4 }} />
          )
        }
        parts.push(
          <Select key="op" size="small" value={record.operator} style={{ width: "100%" }}
            onChange={(v) => updateAssertion(index, { operator: v })}
            options={(OPERATORS[record.type] || []).map((o) => ({ value: o.value, label: o.label }))} />
        )
        return <Space direction="vertical" size={2} style={{ width: "100%" }}>{parts}</Space>
      },
    },
    {
      title: "期望值", width: 180,
      render: (_: unknown, record: AssertionRule, index: number) => {
        if (!needsValue(record)) return <Text type="secondary" style={{ fontSize: 12 }}>-</Text>
        if (record.type === "status_code" || record.type === "response_time") {
          return <InputNumber size="small" value={record.expected_value as number}
            onChange={(v) => updateAssertion(index, { expected_value: v ?? 0 })}
            placeholder={getValuePlaceholder(record)} style={{ width: "100%" }} />
        }
        return <Input size="small" value={String(record.expected_value || "")}
          onChange={(e) => updateAssertion(index, { expected_value: e.target.value })}
          placeholder={getValuePlaceholder(record)} style={{ width: "100%" }} />
      },
    },
    {
      title: "说明", width: 150,
      render: (_: unknown, record: AssertionRule, index: number) => (
        <Input size="small" placeholder="可选说明" value={record.description || ""}
          onChange={(e) => updateAssertion(index, { description: e.target.value })} />
      ),
    },
    ...(showResults
      ? [{
          title: "结果", width: 100,
          render: (_: unknown, __: AssertionRule, index: number) => {
            const result = getResult(index)
            if (!result) return <Text type="secondary">-</Text>
            return result.passed ? (
              <Tag icon={<CheckCircleOutlined />} color="success">通过</Tag>
            ) : (
              <Tooltip title={result.error || `实际值: ${String(result.actual ?? '-')}`}>
                <Tag icon={<CloseCircleOutlined />} color="error">失败</Tag>
              </Tooltip>
            )
          },
        }]
      : []),
    {
      title: "", width: 80,
      render: (_: unknown, record: AssertionRule, index: number) => (
        <Space size={2}>
          <Switch size="small" checked={record.enabled}
            onChange={(checked) => updateAssertion(index, { enabled: checked })} />
          <Popconfirm title="确认删除此断言？" onConfirm={() => removeAssertion(index)} okText="删除" cancelText="取消">
            <Button type="text" size="small" danger icon={<DeleteOutlined />} />
          </Popconfirm>
        </Space>
      ),
    },
  ]

  return (
    <div>
      {showResults && assertionResults && assertionResults.total > 0 && (
        <div style={{
          marginBottom: 12, padding: "8px 12px", borderRadius: 6,
          background: assertionResults.failed > 0 ? "#fff2f0" : "#f6ffed",
          border: `1px solid ${assertionResults.failed > 0 ? '#ffccc7' : '#b7eb8f'}`,
          display: "flex", alignItems: "center", gap: 12,
        }}>
          {assertionResults.failed > 0 ? (
            <CloseCircleOutlined style={{ color: "#ff4d4f", fontSize: 16 }} />
          ) : (
            <CheckCircleOutlined style={{ color: "#52c41a", fontSize: 16 }} />
          )}
          <Text strong>断言结果：{assertionResults.passed}/{assertionResults.total} 通过</Text>
          {assertionResults.failed > 0 && <Text type="danger">{assertionResults.failed} 条失败</Text>}
        </div>
      )}
      <Table size="small" rowKey={(_, i) => String(i)} columns={columns}
        dataSource={assertions.map((a, i) => ({ ...a, _index: i }))}
        pagination={false}
        locale={{ emptyText: "暂无断言规则，点击下方按钮添加" }}
        footer={() => (
          <Button type="dashed" size="small" icon={<PlusOutlined />} block onClick={addAssertion}>
            添加断言规则
          </Button>
        )} style={{ fontSize: 13 }} />
      <div style={{ marginTop: 8 }}>
        <Text type="secondary" style={{ fontSize: 11 }}>
          <InfoCircleOutlined /> 提示：可视化断言在后置脚本之外独立执行，支持状态码、响应时间、响应头和响应体四种断言类型。
        </Text>
      </div>
    </div>
  )
}

export default AssertionBuilder
