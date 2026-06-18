/**
 * 面包屑导航组件
 *
 * 根据当前路由自动生成面包屑：首页 > 模块 > 子页面
 * 使用 Ant Design Breadcrumb 组件，支持 i18n。
 */

import { Breadcrumb } from 'antd'
import { HomeOutlined } from '@ant-design/icons'
import { useLocation, useNavigate } from 'react-router-dom'
import { useTranslation } from 'react-i18next'

// 路由段到 i18n key 的映射
const ROUTE_LABEL_MAP: Record<string, string> = {
  dashboard: 'sidebar.dashboard',
  'api-test': 'sidebar.apiTest',
  workspace: 'apiTest.workspace',
  collections: 'apiTest.collections',
  environments: 'apiTest.environments',
  'web-test': 'sidebar.webTest',
  scripts: 'webTest.scripts',
  'app-test': 'sidebar.appTest',
  'perf-test': 'sidebar.perfTest',
  scenarios: 'perfTest.scenarios',
  monitor: 'perfTest.monitor',
  results: 'perfTest.results',
  'perf-dashboard': 'perfTest.dashboard',
  'alert-rules': 'perfTest.alertRules',
  reports: 'sidebar.reports',
  settings: 'sidebar.settings',
  profile: 'sidebar.profile',
  organizations: 'sidebar.organizations',
  'audit-logs': 'sidebar.auditLogs',
  'user-management': 'admin.userManagement',
  documents: 'sidebar.documents',
  'quality-gates': 'sidebar.qualityGates',
  'test-plans': 'sidebar.testPlans',
  'ai-insights': 'sidebar.aiInsights',
  'visual-regression': 'sidebar.visualRegression',
  integrations: 'sidebar.integrations',
  tokens: 'sidebar.apiTokens',
  notifications: 'sidebar.notifications',
  'team-metrics': 'sidebar.teamMetrics',
}

const PageBreadcrumb: React.FC = () => {
  const { t } = useTranslation()
  const location = useLocation()
  const navigate = useNavigate()

  const pathSegments = location.pathname.split('/').filter(Boolean)

  if (pathSegments.length === 0 || (pathSegments.length === 1 && pathSegments[0] === 'dashboard')) {
    return null
  }

  const items = [
    {
      title: (
        <span onClick={() => navigate('/dashboard')} style={{ cursor: 'pointer' }}>
          <HomeOutlined style={{ marginRight: 4 }} />
          {t('sidebar.dashboard')}
        </span>
      ),
    },
    ...pathSegments.map((segment, index) => {
      const path = '/' + pathSegments.slice(0, index + 1).join('/')
      const isLast = index === pathSegments.length - 1
      const labelKey = ROUTE_LABEL_MAP[segment]
      const label = labelKey ? t(labelKey) : segment

      return {
        title: isLast ? (
          <span>{label}</span>
        ) : (
          <span onClick={() => navigate(path)} style={{ cursor: 'pointer' }}>
            {label}
          </span>
        ),
      }
    }),
  ]

  return (
    <Breadcrumb
      items={items}
      style={{ marginBottom: 12, fontSize: 13 }}
    />
  )
}

export default PageBreadcrumb
