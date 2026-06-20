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
  alerts: 'sidebar.alertRules',
  reports: 'sidebar.reports',
  settings: 'sidebar.settings',
  profile: 'sidebar.profile',
  organizations: 'sidebar.organizations',
  'audit-logs': 'sidebar.auditLogs',
  users: 'sidebar.userManagement',
  docs: 'sidebar.documents',
  'quality-gates': 'sidebar.qualityGates',
  'test-plans': 'sidebar.testPlans',
  'test-plan-runs': 'testPlan.runDetail',
  'ai-insights': 'sidebar.aiInsights',
  'visual-history': 'sidebar.visualRegression',
  integrations: 'sidebar.integrations',
  'api-tokens': 'sidebar.apiTokens',
  'notification-settings': 'sidebar.notifications',
  'team-metrics': 'sidebar.teamMetrics',
  'ci-cd': 'sidebar.cicd',
  'trigger-rules': 'sidebar.triggerRules',
  'mock-servers': 'sidebar.mockServers',
  billing: 'sidebar.billing',
  'health-monitor': 'sidebar.healthMonitor',
  'webhook-debugger': 'sidebar.webhookDebugger',
  devices: 'sidebar.deviceManager',
  'data-factory': 'sidebar.dataFactory',
  'flaky-tests': 'sidebar.flakyTests',
  'api-docs': 'sidebar.apiDocs',
  'report-schedules': 'sidebar.reportSchedules',
  'report-templates': 'sidebar.reportTemplates',
  'test-templates': 'sidebar.testTemplates',
}

// 纯前缀段：不产生独立面包屑条目，仅用于路径拼接
const PREFIX_SEGMENTS = new Set(['admin'])

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
    ...pathSegments.reduce<Array<{ title: React.ReactNode }>>((acc, segment, originalIndex) => {
        // 跳过纯前缀段
        if (PREFIX_SEGMENTS.has(segment)) return acc

        const path = '/' + pathSegments.slice(0, originalIndex + 1).join('/')
        const isLast = originalIndex === pathSegments.length - 1
        const labelKey = ROUTE_LABEL_MAP[segment]
        const label = labelKey ? t(labelKey) : segment

        acc.push({
          title: isLast ? (
            <span>{label}</span>
          ) : (
            <span onClick={() => navigate(path)} style={{ cursor: 'pointer' }}>
              {label}
            </span>
          ),
        })
        return acc
      }, []),
  ]

  return (
    <Breadcrumb
      items={items}
      style={{ marginBottom: 12, fontSize: 13 }}
    />
  )
}

export default PageBreadcrumb
