import { lazy, Suspense } from 'react'
import { Routes, Route, Navigate } from 'react-router-dom'
import { Spin } from 'antd'
import MainLayout from './layouts/MainLayout'
import Login from './pages/Login'
import ForgotPassword from './pages/ForgotPassword'
import ResetPassword from './pages/ResetPassword'
import ErrorBoundary from './components/ErrorBoundary'
import LanguageSwitchPrompt from './components/LanguageSwitchPrompt'
import RequireRole from './components/RequireRole'
import NotFound from './pages/NotFound'
import i18n from './i18n'
import { useAuthStore } from './stores/authStore'

// 懒加载页面组件
const Dashboard = lazy(() => import('./pages/Dashboard'))
const ApiTestWorkspace = lazy(() => import('./pages/api-test/ApiTestWorkspace'))
const ApiTestCollections = lazy(() => import('./pages/api-test/ApiTestCollections'))
const ApiTestEnvironments = lazy(() => import('./pages/api-test/ApiTestEnvironments'))
const WebTestScripts = lazy(() => import('./pages/web-test/WebTestScripts'))
const AppTestScripts = lazy(() => import('./pages/app-test/AppTestScripts'))
const PerfTestScenarios = lazy(() => import('./pages/perf-test/PerfTestScenarios'))
const PerfTestMonitor = lazy(() => import('./pages/perf-test/PerfTestMonitor'))
const PerfTestResults = lazy(() => import('./pages/perf-test/PerfTestResults'))
const PerfTestAlertRules = lazy(() => import('./pages/perf-test/PerfTestAlertRules'))
const PerformanceDashboard = lazy(() => import('./pages/perf-test/PerformanceDashboard'))
const Reports = lazy(() => import('./pages/Reports'))
const CICD = lazy(() => import('./pages/CICD'))
const Documents = lazy(() => import('./pages/Documents'))
const Settings = lazy(() => import('./pages/Settings'))
const Profile = lazy(() => import('./pages/Profile'))
const VisualRegressionHistory = lazy(() => import('./pages/VisualRegressionHistory'))
const AIInsightsDashboard = lazy(() => import('./pages/AIInsightsDashboard'))
const OrganizationList = lazy(() => import('./pages/organizations/OrganizationList'))
const OrganizationDetail = lazy(() => import('./pages/organizations/OrganizationDetail'))
const AuditLogs = lazy(() => import('./pages/AuditLogs'))
const ApiTokens = lazy(() => import('./pages/ApiTokens'))
const TestPlans = lazy(() => import('./pages/TestPlans'))
const TestPlanDetail = lazy(() => import('./pages/TestPlanDetail'))
const TestPlanRunDetail = lazy(() => import('./pages/TestPlanRunDetail'))
const SSOCallback = lazy(() => import('./pages/SSOCallback'))
const QualityGates = lazy(() => import('./pages/QualityGates'))
const TriggerRules = lazy(() => import('./pages/TriggerRules'))
const NotificationSettings = lazy(() => import('./pages/NotificationSettings'))
const TeamMetrics = lazy(() => import('./pages/TeamMetrics'))
const Integrations = lazy(() => import('./pages/Integrations'))
const UserManagement = lazy(() => import('./pages/admin/UserManagement'))
const MockServers = lazy(() => import('./pages/MockServers'))
const Billing = lazy(() => import('./pages/Billing'))
const HealthMonitor = lazy(() => import('./pages/HealthMonitor'))
const WebhookDebugger = lazy(() => import('./pages/WebhookDebugger'))
const DataFactory = lazy(() => import('./pages/DataFactory'))
const FlakyTestDashboard = lazy(() => import('./pages/FlakyTestDashboard'))
const TestCaseTemplates = lazy(() => import('./pages/TestCaseTemplates'))
const ReportSchedules = lazy(() => import('./pages/ReportSchedules'))
const ReportTemplateEditor = lazy(() => import('./pages/ReportTemplateEditor'))
const ApiDocumentation = lazy(() => import('./pages/ApiDocumentation'))
const DeviceManager = lazy(() => import('./pages/app-test/DeviceManager'))

// 加载中组件
const PageLoading = () => (
  <div
    style={{
      display: 'flex',
      justifyContent: 'center',
      alignItems: 'center',
      minHeight: '60vh',
    }}
  >
    <Spin size="large" tip={i18n.t('common.pageLoading')} />
  </div>
)

// 受保护的路由组件
const ProtectedRoute = ({ children }: { children: React.ReactNode }) => {
  const { isAuthenticated } = useAuthStore()

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />
  }

  return <>{children}</>
}

function App() {
  return (
    <ErrorBoundary>
      <LanguageSwitchPrompt />
      <Routes>
        {/* 公开路由 */}
        <Route element={<Login />}>
          <Route path="/login" element={<></>} />
          <Route path="/register" element={<></>} />
        </Route>
        <Route path="/forgot-password" element={<ForgotPassword />} />
        <Route path="/reset-password" element={<ResetPassword />} />
        <Route
          path="/sso/callback"
          element={
            <Suspense fallback={<PageLoading />}>
              <SSOCallback />
            </Suspense>
          }
        />

        {/* 受保护的路由 */}
        <Route
          path="/"
          element={
            <ProtectedRoute>
              <MainLayout />
            </ProtectedRoute>
          }
        >
        <Route index element={<Navigate to="/dashboard" replace />} />
        <Route
          path="dashboard"
          element={
            <Suspense fallback={<PageLoading />}>
              <Dashboard />
            </Suspense>
          }
        />

        {/* 接口测试 */}
        <Route path="api-test">
          <Route index element={<Navigate to="workspace" replace />} />
          <Route
            path="workspace"
            element={
              <Suspense fallback={<PageLoading />}>
                <ApiTestWorkspace />
              </Suspense>
            }
          />
          <Route
            path="collections"
            element={
              <Suspense fallback={<PageLoading />}>
                <ApiTestCollections />
              </Suspense>
            }
          />
          <Route
            path="environments"
            element={
              <Suspense fallback={<PageLoading />}>
                <ApiTestEnvironments />
              </Suspense>
            }
          />
        </Route>

        {/* Web 自动化测试 */}
        <Route path="web-test">
          <Route index element={<Navigate to="scripts" replace />} />
          <Route
            path="scripts"
            element={
              <Suspense fallback={<PageLoading />}>
                <WebTestScripts />
              </Suspense>
            }
          />
          <Route path="recorder" element={<Navigate to="/web-test/scripts" replace />} />
          <Route
            path="visual-history/:test_case_id"
            element={
              <Suspense fallback={<PageLoading />}>
                <VisualRegressionHistory />
              </Suspense>
            }
          />
        </Route>

        {/* APP 自动化测试 */}
        <Route path="app-test">
          <Route index element={<Navigate to="scripts" replace />} />
          <Route
            path="scripts"
            element={
              <Suspense fallback={<PageLoading />}>
                <AppTestScripts />
              </Suspense>
            }
          />
        </Route>

        {/* 性能测试 */}
        <Route path="perf-test">
          <Route index element={<Navigate to="scenarios" replace />} />
          <Route
            path="scenarios"
            element={
              <Suspense fallback={<PageLoading />}>
                <PerfTestScenarios />
              </Suspense>
            }
          />
          <Route
            path="monitor"
            element={
              <Suspense fallback={<PageLoading />}>
                <PerfTestMonitor />
              </Suspense>
            }
          />
          <Route
            path="results"
            element={
              <Suspense fallback={<PageLoading />}>
                <PerfTestResults />
              </Suspense>
            }
          />
          <Route
            path="dashboard"
            element={
              <Suspense fallback={<PageLoading />}>
                <PerformanceDashboard />
              </Suspense>
            }
          />
          <Route
            path="alerts"
            element={
              <Suspense fallback={<PageLoading />}>
                <PerfTestAlertRules />
              </Suspense>
            }
          />
        </Route>

        {/* 组织管理 */}
        <Route path="organizations">
          <Route
            index
            element={
              <Suspense fallback={<PageLoading />}>
                <OrganizationList />
              </Suspense>
            }
          />
          <Route
            path=":orgId"
            element={
              <Suspense fallback={<PageLoading />}>
                <OrganizationDetail />
              </Suspense>
            }
          />
        </Route>

        {/* AI 统计看板 */}
        <Route
          path="ai-insights"
          element={
            <Suspense fallback={<PageLoading />}>
              <AIInsightsDashboard />
            </Suspense>
          }
        />

        {/* 测试报告 */}
        <Route
          path="reports"
          element={
            <Suspense fallback={<PageLoading />}>
              <Reports />
            </Suspense>
          }
        />

        {/* 质量门禁 */}
        <Route
          path="quality-gates"
          element={
            <Suspense fallback={<PageLoading />}>
              <QualityGates />
            </Suspense>
          }
        />

        {/* CI/CD与定时任务 */}
        <Route
          path="ci-cd"
          element={
            <Suspense fallback={<PageLoading />}>
              <CICD />
            </Suspense>
          }
        />

        {/* 测试计划 */}
        <Route path="test-plans">
          <Route
            index
            element={
              <Suspense fallback={<PageLoading />}>
                <TestPlans />
              </Suspense>
            }
          />
          <Route
            path=":planId"
            element={
              <Suspense fallback={<PageLoading />}>
                <TestPlanDetail />
              </Suspense>
            }
          />
        </Route>
        <Route
          path="test-plan-runs/:runId"
          element={
            <Suspense fallback={<PageLoading />}>
              <TestPlanRunDetail />
            </Suspense>
          }
        />

        {/* 集成管理 */}
        <Route
          path="integrations"
          element={
            <Suspense fallback={<PageLoading />}>
              <Integrations />
            </Suspense>
          }
        />

        {/* 触发规则 */}
        <Route
          path="trigger-rules"
          element={
            <Suspense fallback={<PageLoading />}>
              <TriggerRules />
            </Suspense>
          }
        />

        {/* 通知设置 */}
        <Route
          path="notification-settings"
          element={
            <Suspense fallback={<PageLoading />}>
              <NotificationSettings />
            </Suspense>
          }
        />

        {/* 团队效能 */}
        <Route
          path="team-metrics"
          element={
            <Suspense fallback={<PageLoading />}>
              <TeamMetrics />
            </Suspense>
          }
        />

        {/* 审计日志（admin） */}
        <Route
          path="audit-logs"
          element={
            <Suspense fallback={<PageLoading />}>
              <RequireRole roles={['admin']}>
                <AuditLogs />
              </RequireRole>
            </Suspense>
          }
        />

        {/* Mock 服务器 */}
        <Route
          path="mock-servers"
          element={
            <Suspense fallback={<PageLoading />}>
              <MockServers />
            </Suspense>
          }
        />

        {/* 计费管理（admin） */}
        <Route
          path="billing"
          element={
            <Suspense fallback={<PageLoading />}>
              <RequireRole roles={['admin']}>
                <Billing />
              </RequireRole>
            </Suspense>
          }
        />

        {/* API 健康监控 */}
        <Route
          path="health-monitor"
          element={
            <Suspense fallback={<PageLoading />}>
              <HealthMonitor />
            </Suspense>
          }
        />

        {/* Webhook 调试器 */}
        <Route
          path="webhook-debugger"
          element={
            <Suspense fallback={<PageLoading />}>
              <WebhookDebugger />
            </Suspense>
          }
        />

        {/* API Token 管理 */}
        <Route
          path="api-tokens"
          element={
            <Suspense fallback={<PageLoading />}>
              <ApiTokens />
            </Suspense>
          }
        />

        {/* 测试文档 */}
        <Route
          path="docs"
          element={
            <Suspense fallback={<PageLoading />}>
              <Documents />
            </Suspense>
          }
        />
        <Route
          path="settings"
          element={
            <Suspense fallback={<PageLoading />}>
              <Settings />
            </Suspense>
          }
        />
        <Route
          path="profile"
          element={
            <Suspense fallback={<PageLoading />}>
              <Profile />
            </Suspense>
          }
        />

        {/* 用户管理（管理员） */}
        <Route
          path="admin/users"
          element={
            <Suspense fallback={<PageLoading />}>
              <RequireRole roles={['admin']}>
                <UserManagement />
              </RequireRole>
            </Suspense>
          }
        />

        {/* AI 数据工厂（member+） */}
        <Route
          path="data-factory"
          element={
            <Suspense fallback={<PageLoading />}>
              <RequireRole roles={['admin', 'member']}>
                <DataFactory />
              </RequireRole>
            </Suspense>
          }
        />

        {/* Flaky 检测（viewer+） */}
        <Route
          path="flaky-tests"
          element={
            <Suspense fallback={<PageLoading />}>
              <FlakyTestDashboard />
            </Suspense>
          }
        />

        {/* 用例模板库（viewer+） */}
        <Route
          path="test-templates"
          element={
            <Suspense fallback={<PageLoading />}>
              <TestCaseTemplates />
            </Suspense>
          }
        />

        {/* API 文档生成（viewer+） */}
        <Route
          path="api-docs"
          element={
            <Suspense fallback={<PageLoading />}>
              <ApiDocumentation />
            </Suspense>
          }
        />

        {/* 定时报告（member+） */}
        <Route
          path="report-schedules"
          element={
            <Suspense fallback={<PageLoading />}>
              <RequireRole roles={['admin', 'member']}>
                <ReportSchedules />
              </RequireRole>
            </Suspense>
          }
        />

        {/* 报告模板编辑器（member+） */}
        <Route
          path="report-templates"
          element={
            <Suspense fallback={<PageLoading />}>
              <RequireRole roles={['admin', 'member']}>
                <ReportTemplateEditor />
              </RequireRole>
            </Suspense>
          }
        />

        {/* 设备管理（admin） */}
        <Route
          path="app-test/devices"
          element={
            <Suspense fallback={<PageLoading />}>
              <RequireRole roles={['admin']}>
                <DeviceManager />
              </RequireRole>
            </Suspense>
          }
        />
      </Route>

      {/* 404 */}
      <Route path="*" element={<NotFound />} />
      </Routes>
    </ErrorBoundary>
  )
}

export default App
