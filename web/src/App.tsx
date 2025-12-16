import { Routes, Route, Navigate } from 'react-router-dom'
import MainLayout from './layouts/MainLayout'
import Login from './pages/Login'
import Register from './pages/Register'
import Dashboard from './pages/Dashboard'
import ApiTestWorkspace from './pages/api-test/ApiTestWorkspace'
import ApiTestCollections from './pages/api-test/ApiTestCollections'
import ApiTestEnvironments from './pages/api-test/ApiTestEnvironments'
import WebTestScripts from './pages/web-test/WebTestScripts'
import WebTestRecorder from './pages/web-test/WebTestRecorder'
import WebTestElements from './pages/web-test/WebTestElements'
import PerfTestScenarios from './pages/perf-test/PerfTestScenarios'
import PerfTestMonitor from './pages/perf-test/PerfTestMonitor'
import PerfTestResults from './pages/perf-test/PerfTestResults'
import Reports from './pages/Reports'
import Documents from './pages/Documents'
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
      <Route path="/login" element={<Login />} />
      <Route path="/register" element={<Register />} />
      
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
          <Route path="recorder" element={<WebTestRecorder />} />
          <Route path="elements" element={<WebTestElements />} />
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
        
        {/* 测试文档 */}
        <Route path="docs" element={<Documents />} />
      </Route>
      
      {/* 404 */}
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  )
}

export default App
