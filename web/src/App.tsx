import { lazy, Suspense } from 'react'
import { Routes, Route, Navigate } from 'react-router-dom'
import { Spin } from 'antd'
import MainLayout from './layouts/MainLayout'
import Login from './pages/Login'
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
const PerformanceDashboard = lazy(() => import('./pages/perf-test/PerformanceDashboard'))
const Reports = lazy(() => import('./pages/Reports'))
const CICD = lazy(() => import('./pages/CICD'))
const Documents = lazy(() => import('./pages/Documents'))
const Settings = lazy(() => import('./pages/Settings'))
const Profile = lazy(() => import('./pages/Profile'))
const VisualRegressionHistory = lazy(() => import('./pages/VisualRegressionHistory'))

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
    <Spin size="large" tip="加载中..." />
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
    <Routes>
      {/* 公开路由 */}
      <Route element={<Login />}>
        <Route path="/login" element={<></>} />
        <Route path="/register" element={<></>} />
      </Route>

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
        </Route>

        {/* 测试报告 */}
        <Route
          path="reports"
          element={
            <Suspense fallback={<PageLoading />}>
              <Reports />
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
      </Route>

      {/* 404 */}
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  )
}

export default App
