/**
 * 用例模板库页面
 *
 * 提供内置用例模板（CRUD 模板、认证模板、分页模板），支持自定义模板保存。
 */
import { Card, Row, Col, Button, Tag, Typography, Space, Empty, message, Input } from "antd"
import { CopyOutlined, SearchOutlined } from "@ant-design/icons"
import { useTranslation } from "react-i18next"
import { useSearchFilter } from "@/hooks/useSearchFilter"

const { Text } = Typography

interface Template {
  id: string; name: string; description: string; category: string;
  method: string; url_pattern: string; headers: string; body: string; assertions: string;
}

const TestCaseTemplates: React.FC = () => {
  const { t } = useTranslation()

  const BUILTIN_TEMPLATES: Template[] = [
    {
      id: "crud_create", name: "CRUD - Create", description: "Standard create resource template", category: t("testTemplates.categories.crud"),
      method: "POST", url_pattern: "{{base_url}}/api/resource",
      headers: '{"Content-Type": "application/json"}',
      body: '{"name": "test"}',
      assertions: "status=201, body.data.id exists",
    },
    {
      id: "crud_read", name: "CRUD - Read", description: "Standard read resource template", category: t("testTemplates.categories.crud"),
      method: "GET", url_pattern: "{{base_url}}/api/resource/{{id}}",
      headers: "{}", body: "", assertions: "status=200, body.data.id equals {{id}}",
    },
    {
      id: "auth_login", name: "Auth - Login", description: "User login authentication template", category: t("testTemplates.categories.auth"),
      method: "POST", url_pattern: "{{base_url}}/api/auth/login",
      headers: '{"Content-Type": "application/json"}',
      body: '{"username": "{{username}}", "password": "{{password}}"}',
      assertions: "status=200, body.access_token exists",
    },
    {
      id: "pagination", name: "Pagination", description: "List pagination query template", category: t("testTemplates.categories.crud"),
      method: "GET", url_pattern: "{{base_url}}/api/resource?page=1&per_page=10",
      headers: "{}", body: "", assertions: "status=200, body.data is array, body.total >= 0",
    },
    {
      id: "health_check", name: "Health Check", description: "Service health check template", category: t("testTemplates.categories.monitor"),
      method: "GET", url_pattern: "{{base_url}}/health",
      headers: "{}", body: "", assertions: "status=200, response_time < 1000",
    },
  ]

  const CATEGORIES = [...new Set(BUILTIN_TEMPLATES.map(tmpl => tmpl.category))]

  const {
    searchText, setSearchText, filters, updateFilter, filteredData, hasActiveFilters, clearFilters,
  } = useSearchFilter<Template>({
    data: BUILTIN_TEMPLATES,
    searchFields: ['name', 'description'],
    filterFn: (item, f) => !f.category || item.category === f.category,
  })

  const handleUse = (tmpl: Template) => {
    navigator.clipboard.writeText(JSON.stringify(tmpl, null, 2))
    message.success(t("testTemplates.copied"))
  }

  return (
    <div className="fst-page">
      <div className="fst-page-header fst-animate-in">
        <h1 className="fst-page-title">{t("testTemplates.title")}</h1>
        <div className="fst-ios-card-subtitle">{t("testTemplates.subtitle")}</div>
      </div>
      <Card className="fst-ios-card fst-animate-in fst-animate-in-1">
        <Space style={{ marginBottom: 16 }}>
          <Input prefix={<SearchOutlined />} placeholder={t("testTemplates.searchPlaceholder")} value={searchText} onChange={e => setSearchText(e.target.value)} style={{ width: 200 }} />
          {CATEGORIES.map(cat => (
            <Tag key={cat} color={filters.category === cat ? "blue" : undefined} style={{ cursor: "pointer" }} onClick={() => updateFilter('category', filters.category === cat ? undefined : cat)}>{cat}</Tag>
          ))}
          {hasActiveFilters && <Button size="small" type="link" onClick={clearFilters}>{t('common.clear') || '清除'}</Button>}
        </Space>
        <Row gutter={[16, 16]}>
          {filteredData.map(tmpl => (
            <Col key={tmpl.id} xs={24} sm={12} md={8} lg={6}>
              <Card size="small" title={<Text strong style={{ fontSize: 13 }}>{tmpl.name}</Text>}
                extra={<Tag>{tmpl.method}</Tag>}
                actions={[<Button key="use" type="link" icon={<CopyOutlined />} onClick={() => handleUse(tmpl)}>{t("testTemplates.use")}</Button>]}>
                <Text type="secondary" style={{ fontSize: 12 }}>{tmpl.description}</Text>
                <div style={{ marginTop: 8 }}><Text code style={{ fontSize: 11 }}>{tmpl.url_pattern}</Text></div>
              </Card>
            </Col>
          ))}
        </Row>
        {filteredData.length === 0 && <Empty description={t("testTemplates.noTemplates")} style={{ marginTop: 40 }} />}
      </Card>
    </div>
  )
}

export default TestCaseTemplates
