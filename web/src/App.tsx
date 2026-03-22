import { Routes, Route, Navigate } from 'react-router-dom'
import MainLayout from './layouts/MainLayout'
import Login from './pages/Login'
import Dashboard from './pages/Dashboard'
import ApiTestWorkspace from './pages/api-test/ApiTestWorkspace'
import ApiTestCollections from './pages/api-test/ApiTestCollections'
import ApiTestEnvironments from './pages/api-test/ApiTestEnvironments'
import WebTestScripts from './pages/web-test/WebTestScripts'
import PerfTestScenarios from './pages/perf-test/PerfTestScenarios'
import PerfTestMonitor from './pages/perf-test/PerfTestMonitor'
import PerfTestResults from './pages/perf-test/PerfTestResults'
import Reports from './pages/Reports'
import CICD from './pages/CICD'
import Documents from './pages/Documents'
import Settings from './pages/Settings'
import Profile from './pages/Profile'
import { useAuthStore } from './stores/authStore'

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
        <Route path="dashboard" element={<Dashboard />} />
        
        {/* 接口测试 */}
        <Route path="api-test">
          <Route index element={<Navigate to="workspace" replace />} />
          <Route path="workspace" element={<ApiTestWorkspace />} />
          <Route path="collections" element={<ApiTestCollections />} />
          <Route path="environments" element={<ApiTestEnvironments />} />
        </Route>
        
        {/* Web 自动化测试 */}
        <Route path="web-test">
          <Route index element={<Navigate to="scripts" replace />} />
          <Route path="scripts" element={<WebTestScripts />} />
          <Route path="recorder" element={<Navigate to="/web-test/scripts" replace />} />
        </Route>
        
        {/* 性能测试 */}
        <Route path="perf-test">
          <Route index element={<Navigate to="scenarios" replace />} />
          <Route path="scenarios" element={<PerfTestScenarios />} />
          <Route path="monitor" element={<PerfTestMonitor />} />
          <Route path="results" element={<PerfTestResults />} />
        </Route>
        
        {/* 测试报告 */}
        <Route path="reports" element={<Reports />} />
        
        {/* CI/CD与定时任务 */}
        <Route path="ci-cd" element={<CICD />} />
        
        {/* 测试文档 */}
        <Route path="docs" element={<Documents />} />
        <Route path="settings" element={<Settings />} />
        <Route path="profile" element={<Profile />} />
      </Route>
      
      {/* 404 */}
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  )
}

export default App
