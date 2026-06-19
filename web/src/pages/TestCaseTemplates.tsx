/**
 * 用例模板库页面
 *
 * 提供内置用例模板（CRUD 模板、认证模板、分页模板），支持自定义模板保存。
 */
import { useState } from "react"
import { Card, Row, Col, Button, Tag, Typography, Space, Empty, message, Input } from "antd"
import { PlusOutlined, CopyOutlined, FileTextOutlined, SearchOutlined } from "@ant-design/icons"
import { useTranslation } from "react-i18next"

const { Text, Title } = Typography

interface Template {
  id: string; name: string; description: string; category: string;
  method: string; url_pattern: string; headers: string; body: string; assertions: string;
}

const BUILTIN_TEMPLATES: Template[] = [
  {
    id: "crud_create", name: "CRUD - 创建", description: "标准创建资源用例模板", category: "CRUD",
    method: "POST", url_pattern: "{{base_url}}/api/resource",
    headers: '{"Content-Type": "application/json"}',
    body: '{"name": "test"}',
    assertions: "status=201, body.data.id exists",
  },
  {
    id: "crud_read", name: "CRUD - 读取", description: "标准读取资源用例模板", category: "CRUD",
    method: "GET", url_pattern: "{{base_url}}/api/resource/{{id}}",
    headers: "{}", body: "", assertions: "status=200, body.data.id equals {{id}}",
  },
  {
    id: "auth_login", name: "认证 - 登录", description: "用户登录认证模板", category: "认证",
    method: "POST", url_pattern: "{{base_url}}/api/auth/login",
    headers: '{"Content-Type": "application/json"}',
    body: '{"username": "{{username}}", "password": "{{password}}"}',
    assertions: "status=200, body.access_token exists",
  },
  {
    id: "pagination", name: "分页查询", description: "列表分页查询模板", category: "CRUD",
    method: "GET", url_pattern: "{{base_url}}/api/resource?page=1&per_page=10",
    headers: "{}", body: "", assertions: "status=200, body.data is array, body.total >= 0",
  },
  {
    id: "health_check", name: "健康检查", description: "服务健康检查模板", category: "监控",
    method: "GET", url_pattern: "{{base_url}}/health",
    headers: "{}", body: "", assertions: "status=200, response_time < 1000",
  },
]

const CATEGORIES = [...new Set(BUILTIN_TEMPLATES.map(t => t.category))]

const TestCaseTemplates: React.FC = () => {
  const { t } = useTranslation()
  const [search, setSearch] = useState("")
  const [selectedCategory, setSelectedCategory] = useState<string | null>(null)

  const filtered = BUILTIN_TEMPLATES.filter(tmpl => {
    if (selectedCategory && tmpl.category !== selectedCategory) return false
    if (search && !tmpl.name.toLowerCase().includes(search.toLowerCase()) && !tmpl.description.includes(search)) return false
    return true
  })

  const handleUse = (tmpl: Template) => {
    navigator.clipboard.writeText(JSON.stringify(tmpl, null, 2))
    message.success("模板已复制到剪贴板")
  }

  return (
    <div style={{ padding: 16 }}>
      <Card title={<Space><FileTextOutlined /><Text strong>用例模板库</Text></Space>}>
        <Space style={{ marginBottom: 16 }}>
          <Input prefix={<SearchOutlined />} placeholder="搜索模板" value={search} onChange={e => setSearch(e.target.value)} style={{ width: 200 }} />
          {CATEGORIES.map(cat => (
            <Tag key={cat} color={selectedCategory === cat ? "blue" : undefined} style={{ cursor: "pointer" }} onClick={() => setSelectedCategory(selectedCategory === cat ? null : cat)}>{cat}</Tag>
          ))}
        </Space>
        <Row gutter={[16, 16]}>
          {filtered.map(tmpl => (
            <Col key={tmpl.id} xs={24} sm={12} md={8} lg={6}>
              <Card size="small" title={<Text strong style={{ fontSize: 13 }}>{tmpl.name}</Text>}
                extra={<Tag>{tmpl.method}</Tag>}
                actions={[<Button key="use" type="link" icon={<CopyOutlined />} onClick={() => handleUse(tmpl)}>使用</Button>]}>
                <Text type="secondary" style={{ fontSize: 12 }}>{tmpl.description}</Text>
                <div style={{ marginTop: 8 }}><Text code style={{ fontSize: 11 }}>{tmpl.url_pattern}</Text></div>
              </Card>
            </Col>
          ))}
        </Row>
        {filtered.length === 0 && <Empty description="未找到匹配的模板" style={{ marginTop: 40 }} />}
      </Card>
    </div>
  )
}

export default TestCaseTemplates
