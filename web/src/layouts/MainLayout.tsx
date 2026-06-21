import { useState, useEffect } from 'react'
import { Outlet, useNavigate, useLocation } from 'react-router-dom'
import { useBranding } from '@/hooks/useBranding'
import { useLocalStorage } from '@/hooks/useLocalStorage'
import { Layout, Avatar, Dropdown, Button, Tour, ConfigProvider, Popover, Typography, Modal, Input, FloatButton, message, type TourProps } from 'antd'
import {
  HomeOutlined,
  ApiOutlined,
  GlobalOutlined,
  MobileOutlined,
  ThunderboltOutlined,
  BarChartOutlined,
  FileTextOutlined,
  SettingOutlined,
  UserOutlined,
  LogoutOutlined,
  MenuFoldOutlined,
  MenuUnfoldOutlined,
  PhoneOutlined,
  MailOutlined,
  CustomerServiceOutlined,
  FolderOutlined,
  TranslationOutlined,
  DotChartOutlined,
  EditOutlined,
  DeleteOutlined,
  PushpinOutlined,
  PushpinFilled,
  TeamOutlined,
  FileSearchOutlined,
  KeyOutlined,
  ExperimentOutlined,
  SafetyOutlined,
  BellOutlined,
  LinkOutlined,
  SunOutlined,
  MoonOutlined,
  RobotOutlined,
  BugOutlined,
  ClockCircleOutlined,
  CopyOutlined,
  SyncOutlined,
  CloudServerOutlined,
  LineChartOutlined,
  HeartOutlined,
} from '@ant-design/icons'
import { useTranslation } from 'react-i18next'
import { useAuthStore } from '@/stores/authStore'
import { useRole } from '@/hooks/useRole'
import { useProjectStore } from '@/stores/projectStore'
import { projectService } from '@/services/projectService'
import { useThemeStore } from '@/stores/themeStore'
import GlobalCopilot from '../components/GlobalCopilot'
import PageBreadcrumb from '../components/PageBreadcrumb'
import SessionWarning from '../components/SessionWarning'
import NotificationPopover from '../components/NotificationPopover'
import GlobalSearch from '../components/GlobalSearch'
import ShortcutHelpModal from '../components/ShortcutHelpModal'
import { useKeyboardShortcut } from '../hooks/useKeyboardShortcut'

const { Content, Footer } = Layout
const { Text } = Typography

/* ─── iOS Sidebar Nav Item ─── */
interface SidebarItemProps {
  icon: React.ReactNode
  label: string
  path: string
  active: boolean
  expanded: boolean
  currentPath: string
  children?: { label: string; path: string }[]
  onClick: (path: string) => void
  onToggle: () => void
  tourId?: string
}

const SidebarItem = ({ icon, label, path, active, expanded, currentPath, children, onClick, onToggle, tourId }: SidebarItemProps) => {
  const isActive = active || (children?.some(c => currentPath === c.path) ?? false)
  return (
    <div style={{ marginBottom: 2 }}>
      <button
        data-tour-id={tourId}
        onClick={() => children && children.length ? onToggle() : onClick(path)}
        style={{
          width: '100%',
          display: 'flex',
          alignItems: 'center',
          gap: 12,
          padding: '10px 14px',
          borderRadius: 12,
          border: 'none',
          background: isActive && !children ? 'rgba(45, 106, 100, 0.12)' : 'transparent',
          color: isActive && !children ? 'var(--fst-primary)' : 'var(--fst-on-surface-variant)',
          fontSize: 14,
          fontWeight: isActive && !children ? 600 : 400,
          cursor: 'pointer',
          transition: 'all 150ms ease',
          textAlign: 'left',
        }}
        onMouseEnter={e => {
          if (!isActive || children) e.currentTarget.style.background = 'rgba(0,0,0,0.04)'
        }}
        onMouseLeave={e => {
          if (!isActive || children) e.currentTarget.style.background = 'transparent'
        }}
      >
        <span style={{ fontSize: 18, width: 22, textAlign: 'center', flexShrink: 0 }}>{icon}</span>
        <span style={{ flex: 1, overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>{label}</span>
        {children && children.length > 0 && (
          <span style={{
            fontSize: 10,
            transition: 'transform 200ms ease',
            transform: expanded ? 'rotate(90deg)' : 'rotate(0deg)',
            opacity: 0.5,
          }}>▶</span>
        )}
      </button>
      {children && children.length > 0 && expanded && (
        <div style={{ paddingLeft: 28, paddingTop: 2 }}>
          {children.map(child => (
            <button
              key={child.path}
              onClick={() => onClick(child.path)}
              style={{
                width: '100%',
                display: 'flex',
                alignItems: 'center',
                padding: '8px 14px',
                borderRadius: 10,
                border: 'none',
                background: currentPath === child.path ? 'rgba(45, 106, 100, 0.10)' : 'transparent',
                color: currentPath === child.path ? 'var(--fst-primary)' : 'var(--fst-on-surface-muted)',
                fontSize: 13,
                fontWeight: currentPath === child.path ? 600 : 400,
                cursor: 'pointer',
                transition: 'all 150ms ease',
                textAlign: 'left',
              }}
              onMouseEnter={e => { e.currentTarget.style.background = 'rgba(0,0,0,0.03)' }}
              onMouseLeave={e => {
                e.currentTarget.style.background = currentPath === child.path ? 'rgba(45, 106, 100, 0.10)' : 'transparent'
              }}
            >
              {child.label}
            </button>
          ))}
        </div>
      )}
    </div>
  )
}

const FooterBeianIcon = ({ className }: { className?: string }) => (
  <svg viewBox="0 0 24 24" fill="none" className={className} aria-hidden="true">
    <path
      d="M12 2.8 19.4 6.2v6.1c0 5-3.1 9.2-7.4 10.9C7.7 21.5 4.6 17.3 4.6 12.3V6.2L12 2.8Z"
      stroke="currentColor"
      strokeWidth="1.6"
      strokeLinejoin="round"
    />
    <path
      d="M9.2 12.2 11 14l3.9-4.1"
      stroke="currentColor"
      strokeWidth="1.6"
      strokeLinecap="round"
      strokeLinejoin="round"
    />
  </svg>
)

const FooterGithubIcon = ({ className, style }: { className?: string; style?: React.CSSProperties }) => (
  <svg viewBox="0 0 24 24" fill="none" className={className} style={style} aria-hidden="true">
    <path
      d="M12 2.6c-5.3 0-9.6 4.3-9.6 9.6 0 4.2 2.7 7.8 6.5 9.1.5.1.7-.2.7-.5v-1.7c-2.6.6-3.2-1.1-3.2-1.1-.4-1-1.1-1.3-1.1-1.3-.9-.6.1-.6.1-.6 1 .1 1.5 1 1.5 1 .9 1.5 2.3 1.1 2.9.8.1-.7.4-1.1.6-1.3-2.1-.2-4.3-1.1-4.3-4.8 0-1 .4-1.9 1-2.6-.1-.2-.4-1.2.1-2.5 0 0 .8-.3 2.6 1a9 9 0 0 1 4.8 0c1.8-1.3 2.6-1 2.6-1 .5 1.3.2 2.3.1 2.5.6.7 1 1.6 1 2.6 0 3.7-2.2 4.6-4.3 4.8.4.3.7.9.7 1.9v2.8c0 .3.2.6.7.5 3.8-1.3 6.5-4.9 6.5-9.1 0-5.3-4.3-9.6-9.6-9.6Z"
      fill="currentColor"
      opacity="0.88"
    />
  </svg>
)

// 用户下拉菜单

const MainLayout = () => {
  const { t, i18n } = useTranslation()
  const [collapsed, setCollapsed] = useLocalStorage('fst-sidebar-collapsed', false)
  const navigate = useNavigate()
  const location = useLocation()
  const { user, logout } = useAuthStore()
  const { branding } = useBranding()
  const { isAdmin, isMember } = useRole()
  const { currentProjectId, projects, setCurrentProject, fetchProjects } = useProjectStore()
  const { resolvedTheme, toggle: toggleTheme } = useThemeStore()
  const [projectModalOpen, setProjectModalOpen] = useState(false)
  const [newProjectName, setNewProjectName] = useState('')
  const [newProjectDesc, setNewProjectDesc] = useState('')
  const [createProjectLoading, setCreateProjectLoading] = useState(false)
  const [editProjectModalOpen, setEditProjectModalOpen] = useState(false)
  const [editingProject, setEditingProject] = useState<{ id: number; name: string; description?: string } | null>(null)
  const [editProjectName, setEditProjectName] = useState('')
  const [editProjectDesc, setEditProjectDesc] = useState('')
  const [editProjectLoading, setEditProjectLoading] = useState(false)
  const rawEnvNotice = (import.meta as any).env?.VITE_ENV_NOTICE as string | undefined
  const envMode = (import.meta as any).env?.MODE as string | undefined
  const deployEnv = (import.meta as any).env?.VITE_DEPLOY_ENV as string | undefined
  const isProduction = envMode === 'production' || deployEnv === 'prod' || deployEnv === 'production'
  const noticeOverride = (rawEnvNotice ?? '').trim()
  const noticeDisabled = ['off', 'none', 'false', '0'].includes(noticeOverride.toLowerCase())
  const envNotice = noticeDisabled
    ? ''
    : noticeOverride || t('layout.envNotice')

  // 用户下拉菜单
  const userMenuItems = [
    {
      key: 'profile',
      icon: <UserOutlined />,
      label: t('header.profile'),
    },
    {
      key: 'settings',
      icon: <SettingOutlined />,
      label: t('header.settings'),
    },
    { type: 'divider' as const },
    {
      key: 'logout',
      icon: <LogoutOutlined />,
      label: t('header.logout'),
      danger: true,
    },
  ]

  const handleUserMenuClick = ({ key }: { key: string }) => {
    if (key === 'logout') {
      logout()
      navigate('/login')
    } else if (key === 'settings') {
      navigate('/settings')
    } else if (key === 'profile') {
      navigate('/profile')
    }
  }

  const handleCreateProject = async () => {
    if (!newProjectName.trim()) return
    setCreateProjectLoading(true)
    try {
      const res = await projectService.createProject({
        name: newProjectName.trim(),
        description: newProjectDesc.trim() || undefined,
      })
      if (res.code === 200 || res.code === 201) {
        message.success(t('layout.createProjectSuccess'))
        setProjectModalOpen(false)
        setNewProjectName('')
        setNewProjectDesc('')
        await fetchProjects()
        if (res.data?.id) setCurrentProject(res.data.id)
      } else {
        message.error(res.message || t('layout.createProjectFailed'))
      }
    } catch {
      message.error(t('layout.createProjectFailed'))
    } finally {
      setCreateProjectLoading(false)
    }
  }

  const handleEditProject = async () => {
    if (!editingProject || !editProjectName.trim()) return
    setEditProjectLoading(true)
    try {
      const res = await projectService.updateProject(editingProject.id, {
        name: editProjectName.trim(),
        description: editProjectDesc.trim() || undefined,
      })
      if (res.code === 200) {
        message.success(t('layout.updateProjectSuccess'))
        setEditProjectModalOpen(false)
        setEditingProject(null)
        await fetchProjects()
      } else {
        message.error(res.message || t('layout.updateProjectFailed'))
      }
    } catch {
      message.error(t('layout.updateProjectFailed'))
    } finally {
      setEditProjectLoading(false)
    }
  }

  const handleDeleteProject = async (projectId: number, projectName: string) => {
    Modal.confirm({
      title: t('layout.deleteProjectConfirm', { name: projectName }),
      okText: t('common.confirm'),
      cancelText: t('common.cancel'),
      okButtonProps: { danger: true },
      onOk: async () => {
        try {
          const res = await projectService.deleteProject(projectId)
          if (res.code === 200) {
            message.success(t('layout.deleteProjectSuccess'))
            if (currentProjectId === projectId) {
              setCurrentProject(undefined)
            }
            await fetchProjects()
          } else {
            message.error(res.message || t('layout.deleteProjectFailed'))
          }
        } catch {
          message.error(t('layout.deleteProjectFailed'))
        }
      },
    })
  }

  // P31-6: 置顶/取消置顶项目
  const handleTogglePin = async (projectId: number) => {
    try {
      const res = await projectService.togglePinProject(projectId)
      if (res.code === 200) {
        message.success(res.message || t('layout.pinToggleSuccess') || '操作成功')
        await fetchProjects()
      }
    } catch {
      message.error(t('common.failed') || '操作失败')
    }
  }

  // 加载项目列表
  useEffect(() => {
    fetchProjects()
  }, [fetchProjects])

  const [tourOpen, setTourOpen] = useState(false)
  const [shortcutModalOpen, setShortcutModalOpen] = useState(false)

  // Ctrl+/ 打开快捷键帮助
  useKeyboardShortcut('/', () => setShortcutModalOpen(prev => !prev), { ctrl: true })

  useEffect(() => {
    // 检查是否是首次访问首页
    const hasToured = localStorage.getItem('fst_has_toured')
    if (!hasToured && location.pathname === '/dashboard') {
      // 延迟确保 Dashboard 中的 DOM 元素渲染完毕
      const timer = setTimeout(() => {
        setTourOpen(true)
      }, 1000)
      return () => clearTimeout(timer)
    }
  }, [location.pathname])

  const handleTourClose = () => {
    setTourOpen(false)
    localStorage.setItem('fst_has_toured', 'true')
  }

  const tourSteps: TourProps['steps'] = [
    {
      title: t('tour.step1Title') || `👋 欢迎使用 ${branding.platform_name}`,
      description: t('tour.step1Desc') || '这是一个企业级 AI 测试平台，支持接口测试、Web 自动化、APP 测试、性能压测等全方位测试能力。',
      target: () => document.querySelector('.fst-app-logo') as HTMLElement,
    },
    {
      title: t('tour.step2Title') || '📊 工作台概览',
      description: t('tour.step2Desc') || '在这里你可以一览所有测试数据：API 用例数、Web 脚本数、性能场景数、最近测试执行记录，以及测试趋势图表。',
      target: () => document.getElementById('tour-step-dashboard-api') as HTMLElement,
    },
    {
      title: t('tour.step3Title') || '🧪 接口测试',
      description: t('tour.step3Desc') || '左侧导航包含所有测试模块：接口测试（工作台/集合/环境）、Web 自动化、APP 测试、性能压测等。点击展开子菜单。',
      target: () => document.querySelector('[data-tour-id="tour-api-test"]') as HTMLElement,
      placement: 'right',
    },
    {
      title: t('tour.step4Title') || '🔍 全局搜索',
      description: t('tour.step4Desc') || '按 Ctrl+K 可以快速搜索任何内容：测试用例、项目、文档、成员等。这是你最高效的导航方式。',
      target: () => document.getElementById('tour-step-search') as HTMLElement,
    },
    {
      title: t('tour.step5Title') || '🤖 AI 助手',
      description: t('tour.step5Desc') || '右下角的 AI 助手可以帮你：生成测试用例、分析失败原因、创建性能场景、解释数据含义。试试和它对话！',
      target: () => document.querySelector('.fst-copilot-sprite') as HTMLElement,
      placement: 'left',
    },
    {
      title: t('tour.step6Title') || '🌙 主题切换',
      description: t('tour.step6Desc') || '点击顶栏的太阳/月亮图标可以切换亮色/暗色主题。系统也会自动跟随你的操作系统主题。',
      target: () => document.querySelector('header') as HTMLElement,
      placement: 'bottom',
    },
    {
      title: t('tour.step7Title') || '⚙️ 系统设置',
      description: t('tour.step7Desc') || '在系统设置中可以配置 AI 模型参数、主题外观、安全策略、通知渠道、GitHub 集成等。前往 /settings 查看。',
      target: () => document.querySelector('[data-tour-id="tour-settings"]') as HTMLElement,
      placement: 'left',
    },
  ]

  // Sidebar nav configuration
  const sidebarNav = [
    { icon: <HomeOutlined />, label: t('sidebar.dashboard'), path: '/dashboard' },
    { icon: <ApiOutlined />, label: t('sidebar.apiTest'), path: '/api-test', children: [
      { label: t('sidebar.workspace'), path: '/api-test/workspace' },
      { label: t('sidebar.collections'), path: '/api-test/collections' },
      { label: t('sidebar.environments'), path: '/api-test/environments' },
      { label: t('sidebar.apiDocs'), path: '/api-docs' },
      { label: t('sidebar.testTemplates'), path: '/test-templates' },
    ]},
    { icon: <GlobalOutlined />, label: t('sidebar.webTest'), path: '/web-test', children: [
      { label: t('sidebar.scripts'), path: '/web-test/scripts' },
    ]},
    { icon: <MobileOutlined />, label: t('sidebar.appTest'), path: '/app-test', children: [
      { label: t('sidebar.scripts'), path: '/app-test/scripts' },
      ...(isAdmin ? [{ label: t('sidebar.deviceManager'), path: '/app-test/devices' }] : []),
    ]},
    { icon: <ThunderboltOutlined />, label: t('sidebar.perfTest'), path: '/perf-test', children: [
      { label: t('sidebar.scenarios'), path: '/perf-test/scenarios' },
      { label: t('sidebar.monitor'), path: '/perf-test/monitor' },
      { label: t('sidebar.results'), path: '/perf-test/results' },
      { label: t('sidebar.perfDashboard'), path: '/perf-test/dashboard' },
      { label: t('sidebar.alertRules'), path: '/perf-test/alerts' },
    ]},
    { icon: <BarChartOutlined />, label: t('sidebar.reports'), path: '/reports' },
    ...(isMember ? [
      { icon: <ClockCircleOutlined />, label: t('sidebar.reportSchedules'), path: '/report-schedules' },
      { icon: <CopyOutlined />, label: t('sidebar.reportTemplates'), path: '/report-templates' },
    ] : []),
    { icon: <ExperimentOutlined />, label: t('sidebar.testPlans'), path: '/test-plans' },
    { icon: <SafetyOutlined />, label: t('sidebar.qualityGates'), path: '/quality-gates' },
    { icon: <DotChartOutlined />, label: t('sidebar.aiInsights'), path: '/ai-insights' },
    { icon: <RobotOutlined />, label: t('sidebar.dataFactory'), path: '/data-factory' },
    { icon: <BugOutlined />, label: t('sidebar.flakyTests'), path: '/flaky-tests' },
    { icon: <SyncOutlined />, label: t('sidebar.cicd'), path: '/ci-cd', children: [
      { label: t('sidebar.cicdMain'), path: '/ci-cd' },
      { label: t('sidebar.triggerRules'), path: '/trigger-rules' },
    ]},
    { icon: <CloudServerOutlined />, label: t('sidebar.mockServers'), path: '/mock-servers' },
    { icon: <BellOutlined />, label: t('sidebar.notifications'), path: '/notification-settings' },
    { icon: <LineChartOutlined />, label: t('sidebar.teamMetrics'), path: '/team-metrics' },
    { icon: <TeamOutlined />, label: t('sidebar.organizations'), path: '/organizations' },
    { icon: <KeyOutlined />, label: t('sidebar.apiTokens'), path: '/api-tokens' },
    { icon: <LinkOutlined />, label: t('sidebar.integrations'), path: '/integrations' },
    { icon: <HeartOutlined />, label: t('sidebar.healthMonitor'), path: '/health-monitor' },
    { icon: <ApiOutlined />, label: t('sidebar.webhookDebugger'), path: '/webhook-debugger' },
    { icon: <FileSearchOutlined />, label: t('sidebar.documents'), path: '/docs' },
    ...(isAdmin ? [
      { icon: <FileSearchOutlined />, label: t('sidebar.auditLogs'), path: '/audit-logs' },
      { icon: <CustomerServiceOutlined />, label: t('sidebar.billing'), path: '/billing' },
    ] : []),
    { icon: <SettingOutlined />, label: t('sidebar.settings'), path: '/settings' },
  ]

  // 管理员专属菜单
  const adminNav = [
    { icon: <TeamOutlined />, label: t('sidebar.userManagement') || '用户管理', path: '/admin/users' },
  ]

  // Track expanded sidebar groups
  const [expandedGroups, setExpandedGroups] = useState<Set<string>>(() => {
    const path = location.pathname
    const parts = path.split('/').filter(Boolean)
    if (parts.length > 1) return new Set([`/${parts[0]}`])
    return new Set()
  })

  const toggleGroup = (key: string) => {
    setExpandedGroups(prev => {
      const next = new Set(prev)
      if (next.has(key)) next.delete(key)
      else next.add(key)
      return next
    })
  }

  return (
    <div className="fst-app-root" style={{ minHeight: '100vh', display: 'flex' }}>
      {/* 无障碍：跳过导航链接 */}
      <a href="#main-content" className="fst-skip-nav">
        {t('layout.skipToContent') || '跳转到主内容'}
      </a>

      {/* ─── iOS Sidebar ─── */}
      <aside style={{
        width: collapsed ? 72 : 280,
        height: '100vh',
        position: 'fixed',
        left: 0,
        top: 0,
        display: 'flex',
        flexDirection: 'column',
        padding: '16px 12px',
        background: 'var(--fst-glass-bg)',
        backdropFilter: 'var(--fst-glass-blur)',
        WebkitBackdropFilter: 'var(--fst-glass-blur)',
        borderRight: '1px solid var(--fst-glass-border)',
        zIndex: 50,
        transition: 'width 250ms cubic-bezier(0.25,0.1,0.25,1)',
        overflow: 'hidden',
      }}>
        {/* Logo */}
        <div className="fst-app-logo" style={{
          display: 'flex',
          alignItems: 'center',
          justifyContent: collapsed ? 'center' : 'flex-start',
          padding: collapsed ? '8px 4px 20px' : '8px 4px 20px',
          borderBottom: '1px solid var(--fst-outline-soft)',
          marginBottom: 12,
          minWidth: 0,
        }}>
          {collapsed ? (
            <img src={branding.logo_url || '/logo-icon.webp'} alt={branding.platform_name} style={{ width: 36, height: 36, objectFit: 'contain', display: 'block' }} />
          ) : (
            <img src={branding.logo_url || '/logo-full.webp'} alt={branding.platform_name} style={{ height: 44, width: 'auto', objectFit: 'contain', display: 'block' }} />
          )}
        </div>

        {/* Navigation */}
        <nav className="fst-app-menu" role="navigation" aria-label={t('layout.mainNavigation') || '主导航'} style={{ flex: 1, overflowY: 'auto', overflowX: 'hidden' }}>
          {sidebarNav.map(item => (
            <SidebarItem
              key={item.path}
              icon={item.icon}
              label={item.label}
              path={item.path}
              active={location.pathname === item.path || location.pathname.startsWith(item.path + '/')}
              expanded={expandedGroups.has(item.path)}
              tourId={item.path === '/settings' ? 'tour-settings' : item.path === '/api-test' ? 'tour-api-test' : undefined}
              currentPath={location.pathname}
              children={item.children}
              onClick={(p) => navigate(p)}
              onToggle={() => toggleGroup(item.path)}
            />
          ))}
          {/* 管理员专属菜单 */}
          {isAdmin && adminNav.map(item => (
            <SidebarItem
              key={item.path}
              icon={item.icon}
              label={item.label}
              path={item.path}
              active={location.pathname === item.path}
              expanded={false}
              currentPath={location.pathname}
              onClick={(p) => navigate(p)}
              onToggle={() => {}}
            />
          ))}
        </nav>

        {/* Bottom actions */}
        <div style={{
          paddingTop: 12,
          borderTop: '1px solid var(--fst-outline-soft)',
          display: 'flex',
          flexDirection: 'column',
          gap: 4,
        }}>
          <Popover
            content={
              <div style={{ width: 280, padding: '4px' }}>
                <div style={{ textAlign: 'center', marginBottom: 16 }}>
                  <div style={{ fontSize: 16, fontWeight: 600, color: '#3D6E66', marginBottom: 4 }}>
                    {t("layout.contactAuthor")}
                  </div>
                  <div style={{ fontSize: 12, color: '#8c8c8c' }}>
                    {t("layout.authorRole")}
                  </div>
                </div>
                <div style={{ display: 'flex', flexDirection: 'column', gap: 12 }}>
                  <Button
                    type="primary"
                    style={{ background: '#5FA59B', border: 'none', width: '100%' }}
                    href="https://huangxuan.chat/resume"
                    target="_blank"
                  >
                    {t('layout.viewProfile')}
                  </Button>
                  <div style={{ background: '#f6f8f8', padding: '12px', borderRadius: 12 }}>
                    <div style={{ display: 'flex', alignItems: 'center', marginBottom: 10 }}>
                      <PhoneOutlined style={{ color: '#5FA59B', marginRight: 10, fontSize: 16 }} />
                      <Text copyable={{ text: '18888888888' }} style={{ color: '#333' }}>+86 188-5212-2635</Text>
                    </div>
                    <div style={{ display: 'flex', alignItems: 'center' }}>
                      <MailOutlined style={{ color: '#5FA59B', marginRight: 10, fontSize: 16 }} />
                      <Text copyable={{ text: 'author@example.com' }} style={{ color: '#333' }}>3441578327@qq.com</Text>
                    </div>
                  </div>
                  <div style={{ textAlign: 'center', marginTop: 4 }}>
                    <div style={{ display: 'inline-block', padding: 8, background: '#fff', border: '1px solid #e8e8e8', borderRadius: 12 }}>
                      <img
                        src="https://res.huangxuan.chat/thrivex/album/69c008b2e4b01ee6a7b76b39.png"
                        alt="WeChat QRCode"
                        style={{ width: 120, height: 120, objectFit: 'contain', display: 'block' }}
                      />
                    </div>
                    <div style={{ fontSize: 12, color: '#8c8c8c', marginTop: 8 }}>{t("layout.scanWechat")}</div>
                  </div>
                </div>
              </div>
            }
            trigger="click"
            placement="right"
          >
            <SidebarItem
              icon={<CustomerServiceOutlined />}
              label={t('header.help') || 'Support'}
              path="#support"
              active={false}
              expanded={false}
              currentPath={location.pathname}
              onClick={() => {}}
              onToggle={() => {}}
            />
          </Popover>
        </div>

        {/* ─── 版本号与环境标识 ─── */}
        <div style={{
          padding: collapsed ? '8px 0' : '8px 16px',
          textAlign: 'center',
          borderTop: '1px solid #f0f0f0',
          marginTop: 'auto',
        }}>
          {collapsed ? (
            <div style={{ fontSize: 10, color: '#999' }}>v1.0</div>
          ) : (
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 6 }}>
              <span style={{ fontSize: 11, color: '#999' }}>v1.0.0</span>
              {(import.meta as any).env?.VITE_DEPLOY_ENV === 'demo' && (
                <span style={{
                  fontSize: 10,
                  color: '#fff',
                  background: '#fa8c16',
                  padding: '1px 6px',
                  borderRadius: 4,
                  fontWeight: 600,
                }}>Demo</span>
              )}
              {(import.meta as any).env?.MODE === 'development' && (
                <span style={{
                  fontSize: 10,
                  color: '#fff',
                  background: '#52c41a',
                  padding: '1px 6px',
                  borderRadius: 4,
                  fontWeight: 600,
                }}>Dev</span>
              )}
            </div>
          )}
        </div>
      </aside>

      {/* ─── Main Content ─── */}
      <div style={{
        flex: 1,
        marginLeft: collapsed ? 72 : 280,
        display: 'flex',
        flexDirection: 'column',
        minHeight: '100vh',
        transition: 'margin-left 250ms cubic-bezier(0.25,0.1,0.25,1)',
      }}>
        {/* ─── iOS Top Bar ─── */}
        <header style={{
          position: 'sticky',
          top: 0,
          zIndex: 40,
          height: 64,
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          padding: '0 32px',
          background: 'var(--fst-glass-bg)',
          backdropFilter: 'blur(20px)',
          WebkitBackdropFilter: 'blur(20px)',
          borderBottom: '1px solid var(--fst-outline-soft)',
        }}>
          {/* Left */}
          <div style={{ display: 'flex', alignItems: 'center', gap: 16, flex: 1 }}>
            <button
              onClick={() => setCollapsed(!collapsed)}
              style={{
                width: 36, height: 36, borderRadius: 10,
                border: 'none', background: 'transparent',
                display: 'grid', placeItems: 'center',
                cursor: 'pointer', color: 'var(--fst-on-surface-variant)',
                transition: 'background 150ms ease',
              }}
              onMouseEnter={e => e.currentTarget.style.background = 'rgba(0,0,0,0.05)'}
              onMouseLeave={e => e.currentTarget.style.background = 'transparent'}
            >
              {collapsed ? <MenuUnfoldOutlined style={{ fontSize: 18 }} /> : <MenuFoldOutlined style={{ fontSize: 18 }} />}
            </button>
            <Dropdown
              trigger={['click']}
              menu={{
                items: [
                  // P31-6: 置顶项目排在前面
                  ...[...projects].sort((a, b) => {
                    if (a.is_pinned && !b.is_pinned) return -1
                    if (!a.is_pinned && b.is_pinned) return 1
                    return 0
                  }).map(p => ({
                    key: `project-${p.id}`,
                    label: (
                      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', gap: 12 }}>
                        <span style={{ flex: 1, overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
                          {p.is_pinned && <PushpinFilled style={{ fontSize: 12, color: '#2D6A64', marginRight: 6 }} />}
                          {p.name}
                        </span>
                        <span style={{ display: 'flex', gap: 4, flexShrink: 0 }}>
                          {/* P31-6: 置顶/取消置顶按钮 */}
                          {p.is_pinned ? (
                            <PushpinFilled
                              style={{ fontSize: 13, color: '#2D6A64', cursor: 'pointer' }}
                              onClick={(e) => { e.stopPropagation(); handleTogglePin(p.id) }}
                            />
                          ) : (
                            <PushpinOutlined
                              style={{ fontSize: 13, color: '#999', cursor: 'pointer' }}
                              onClick={(e) => { e.stopPropagation(); handleTogglePin(p.id) }}
                            />
                          )}
                          <EditOutlined
                            style={{ fontSize: 13, color: '#999' }}
                            onClick={(e) => {
                              e.stopPropagation()
                              setEditingProject(p)
                              setEditProjectName(p.name)
                              setEditProjectDesc(p.description || '')
                              setEditProjectModalOpen(true)
                            }}
                          />
                          <DeleteOutlined
                            style={{ fontSize: 13, color: '#ff4d4f' }}
                            onClick={(e) => {
                              e.stopPropagation()
                              handleDeleteProject(p.id, p.name)
                            }}
                          />
                        </span>
                      </div>
                    ),
                    onClick: () => setCurrentProject(p.id),
                    style: currentProjectId === p.id ? { fontWeight: 600 } : {},
                  })),
                  { type: 'divider' },
                  {
                    key: '__create__',
                    label: <span style={{ color: '#2D5A52', fontWeight: 500 }}>+ {t('layout.createNewProject')}</span>,
                    onClick: () => setProjectModalOpen(true),
                  },
                ],
              }}
            >
              <Button
                style={{ display: 'flex', alignItems: 'center', gap: 8, minWidth: 180, justifyContent: 'flex-start' }}
                icon={<FolderOutlined />}
              >
                {currentProjectId
                  ? projects.find(p => p.id === currentProjectId)?.name || t('layout.selectProject')
                  : t('layout.selectProject')}
              </Button>
            </Dropdown>
            <div id="tour-step-search">
              <GlobalSearch />
            </div>
          </div>

          {/* Center notice */}
          <div style={{ flex: 1, display: 'flex', justifyContent: 'center', overflow: 'hidden' }}>
            {isProduction && envNotice && <div className="fst-env-notice">{envNotice}</div>}
          </div>

          {/* Right */}
          <div style={{ display: 'flex', alignItems: 'center', gap: 16 }}>
            <Popover
              content={
                <div style={{ width: 280, padding: '4px' }}>
                  <div style={{ textAlign: 'center', marginBottom: 16 }}>
                    <div style={{ fontSize: 16, fontWeight: 600, color: '#3D6E66', marginBottom: 4 }}>
                      {t("layout.contactAuthor")}
                    </div>
                    <div style={{ fontSize: 12, color: '#8c8c8c' }}>
                      {t("layout.authorRole")}
                    </div>
                  </div>
                  <div style={{ display: 'flex', flexDirection: 'column', gap: 12 }}>
                    <Button
                      type="primary"
                      style={{ background: '#5FA59B', border: 'none', width: '100%' }}
                      href="https://huangxuan.chat/resume"
                      target="_blank"
                    >
                      {t('layout.viewProfile')}
                    </Button>
                    <div style={{ background: '#f6f8f8', padding: '12px', borderRadius: 12 }}>
                      <div style={{ display: 'flex', alignItems: 'center', marginBottom: 10 }}>
                        <PhoneOutlined style={{ color: '#5FA59B', marginRight: 10, fontSize: 16 }} />
                        <Text copyable={{ text: '18888888888' }} style={{ color: '#333' }}>+86 188-5212-2635</Text>
                      </div>
                      <div style={{ display: 'flex', alignItems: 'center' }}>
                        <MailOutlined style={{ color: '#5FA59B', marginRight: 10, fontSize: 16 }} />
                        <Text copyable={{ text: 'author@example.com' }} style={{ color: '#333' }}>3441578327@qq.com</Text>
                      </div>
                    </div>
                    <div style={{ textAlign: 'center', marginTop: 4 }}>
                      <div style={{ display: 'inline-block', padding: 8, background: '#fff', border: '1px solid #e8e8e8', borderRadius: 12 }}>
                        <img
                          src="https://res.huangxuan.chat/thrivex/album/69c008b2e4b01ee6a7b76b39.png"
                          alt="WeChat QRCode"
                          style={{ width: 120, height: 120, objectFit: 'contain', display: 'block' }}
                        />
                      </div>
                      <div style={{ fontSize: 12, color: '#8c8c8c', marginTop: 8 }}>{t("layout.scanWechat")}</div>
                    </div>
                  </div>
                </div>
              }
              trigger="hover"
              placement="bottom"
            >
              <button
                style={{
                  width: 36, height: 36, borderRadius: 10,
                  border: 'none', background: 'transparent',
                  display: 'grid', placeItems: 'center',
                  cursor: 'pointer', color: 'var(--fst-on-surface-variant)',
                  transition: 'all 150ms ease',
                }}
                onMouseEnter={e => { e.currentTarget.style.background = 'rgba(0,0,0,0.05)'; e.currentTarget.style.color = 'var(--fst-primary)' }}
                onMouseLeave={e => { e.currentTarget.style.background = 'transparent'; e.currentTarget.style.color = 'var(--fst-on-surface-variant)' }}
                aria-label={t('layout.contactAuthor')}
              >
                <CustomerServiceOutlined style={{ fontSize: 18 }} />
              </button>
            </Popover>

            <a
              href="https://github.com/05Huang/FullScopeTest"
              target="_blank"
              rel="noreferrer noopener"
              aria-label="GitHub"
              style={{
                display: 'grid', placeItems: 'center',
                width: 36, height: 36, borderRadius: 10,
                color: 'var(--fst-on-surface-variant)',
                transition: 'all 150ms ease',
              }}
              onMouseEnter={e => { e.currentTarget.style.background = 'rgba(0,0,0,0.05)'; e.currentTarget.style.color = 'var(--fst-primary)' }}
              onMouseLeave={e => { e.currentTarget.style.background = 'transparent'; e.currentTarget.style.color = 'var(--fst-on-surface-variant)' }}
            >
              <FooterGithubIcon style={{ width: 18, height: 18 }} />
            </a>

            <NotificationPopover />

            <Dropdown
              menu={{
                items: [
                  { key: 'zh', label: '中文' },
                  { key: 'en', label: 'English' },
                ],
                onClick: ({ key }) => {
                  i18n.changeLanguage(key)
                  localStorage.setItem('fst-language', key)
                },
              }}
              trigger={['click']}
            >
              <button
                style={{
                  width: 36, height: 36, borderRadius: 10,
                  border: 'none', background: 'transparent',
                  display: 'grid', placeItems: 'center',
                  cursor: 'pointer', color: 'var(--fst-on-surface-variant)',
                  transition: 'all 150ms ease',
                }}
                onMouseEnter={e => { e.currentTarget.style.background = 'rgba(0,0,0,0.05)'; e.currentTarget.style.color = 'var(--fst-primary)' }}
                onMouseLeave={e => { e.currentTarget.style.background = 'transparent'; e.currentTarget.style.color = 'var(--fst-on-surface-variant)' }}
                aria-label={t('header.language')}
              >
                <TranslationOutlined style={{ fontSize: 18 }} />
              </button>
            </Dropdown>

            {/* 主题切换按钮 */}
            <button
              onClick={toggleTheme}
              style={{
                width: 36, height: 36, borderRadius: 10,
                border: 'none', background: 'transparent',
                display: 'grid', placeItems: 'center',
                cursor: 'pointer', color: 'var(--fst-on-surface-variant)',
                transition: 'all 150ms ease',
              }}
              onMouseEnter={e => { e.currentTarget.style.background = 'rgba(0,0,0,0.05)'; e.currentTarget.style.color = 'var(--fst-primary)' }}
              onMouseLeave={e => { e.currentTarget.style.background = 'transparent'; e.currentTarget.style.color = 'var(--fst-on-surface-variant)' }}
              aria-label={resolvedTheme === 'dark' ? t('layout.switchToLight') : t('layout.switchToDark')}
            >
              {resolvedTheme === 'dark' ? <SunOutlined style={{ fontSize: 18 }} /> : <MoonOutlined style={{ fontSize: 18 }} />}
            </button>

            <div style={{ width: 1, height: 20, background: 'var(--fst-outline-soft)', margin: '0 4px' }} />

            <Dropdown
              menu={{ items: userMenuItems, onClick: handleUserMenuClick }}
              placement="bottomRight"
            >
              <div
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: 10,
                  cursor: 'pointer',
                  padding: '6px 12px 6px 6px',
                  borderRadius: 12,
                  transition: 'background 150ms ease',
                }}
                onMouseEnter={e => e.currentTarget.style.background = 'rgba(0,0,0,0.04)'}
                onMouseLeave={e => e.currentTarget.style.background = 'transparent'}
              >
                <Avatar
                  size={34}
                  icon={<UserOutlined />}
                  src={user?.avatar}
                  style={{ backgroundColor: 'var(--fst-primary)' }}
                />
                <span style={{ fontWeight: 600, fontSize: 14, color: 'var(--fst-on-surface)' }}>
                  {user?.username || t('layout.user')}
                </span>
              </div>
            </Dropdown>
          </div>
        </header>

        {/* ─── Page Content ─── */}
        <main
          id="main-content"
          role="main"
          aria-label={t('layout.mainContent') || '主内容区'}
          style={{
            flex: 1,
            padding: 24,
            maxWidth: 1440,
            width: '100%',
            margin: '0 auto',
          }}
        >
          <PageBreadcrumb />
          <Outlet />
        </main>

        {/* ─── Footer ─── */}
        <footer className="fst-app-footer">
          <div className="fst-site-footer" aria-label={t('layout.footerAriaLabel') || '网站页脚'}>
            <a className="fst-site-footer-link" href="https://beian.miit.gov.cn/" target="_blank" rel="noreferrer noopener">
              <FooterBeianIcon className="fst-site-footer-icon" />
              苏ICP备2025167047号-3
            </a>
            <span className="fst-site-footer-sep" aria-hidden="true" />
            <a className="fst-site-footer-link" href="https://github.com/05Huang/FullScopeTest" target="_blank" rel="noreferrer noopener">
              <FooterGithubIcon className="fst-site-footer-icon" />
              GitHub 开源
            </a>
            <span className="fst-site-footer-sep" aria-hidden="true" />
            <span
              className="fst-site-footer-link"
              style={{
                display: 'inline-flex', alignItems: 'center', gap: 5,
                padding: '2px 8px', borderRadius: 6,
                background: 'rgba(45, 106, 100, 0.08)',
                border: '1px solid rgba(45, 106, 100, 0.15)',
                fontSize: 12, fontWeight: 500,
              }}
              title={t('layout.accessibilityTitle') || '本系统支持无障碍访问：键盘导航、屏幕阅读器、高对比度模式、减少动画'}
              role="note"
              aria-label={t('layout.accessibilityTitle') || '本系统支持无障碍访问'}
            >
              <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
                <circle cx="12" cy="12" r="10"/>
                <path d="m8 12 2 0m4 0 2 0"/>
                <path d="M12 8a2 2 0 1 0 0-4 2 2 0 0 0 0 4z" fill="currentColor" stroke="none"/>
                <path d="M9 16c1.5 1 4.5 1 6 0"/>
                <path d="M8 12l-3 4m11-4 3 4"/>
              </svg>
              {t('layout.accessibility') || '无障碍'}
            </span>
            {branding.footer_text && (
              <>
                <span className="fst-site-footer-sep" aria-hidden="true" />
                <span className="fst-site-footer-link">{branding.footer_text}</span>
              </>
            )}
          </div>
        </footer>
        <GlobalCopilot />
        <SessionWarning />
        <FloatButton.BackTop visibilityHeight={300} />
      </div>

      {/* 用户引导 */}
      <ConfigProvider
        theme={{
          token: { colorPrimary: '#2D6A64' },
          components: {
            Tour: {
              boxShadowSecondary: '0 6px 16px 0 rgba(45, 106, 100, 0.15), 0 3px 6px -4px rgba(45, 106, 100, 0.1), 0 9px 28px 8px rgba(45, 106, 100, 0.08)',
            }
          }
        }}
      >
        <Tour open={tourOpen} onClose={handleTourClose} steps={tourSteps} />
      </ConfigProvider>

      {/* 快捷键帮助弹窗 */}
      <ShortcutHelpModal open={shortcutModalOpen} onClose={() => setShortcutModalOpen(false)} />

      {/* 创建项目弹窗 */}
      <Modal
        title={t('layout.createNewProject')}
        open={projectModalOpen}
        onCancel={() => {
          setProjectModalOpen(false)
          setNewProjectName('')
          setNewProjectDesc('')
        }}
        onOk={handleCreateProject}
        confirmLoading={createProjectLoading}
        okText={t('common.confirm')}
        cancelText={t('common.cancel')}
        destroyOnHidden
      >
        <div style={{ display: 'flex', flexDirection: 'column', gap: 16, marginTop: 8 }}>
          <div>
            <div style={{ marginBottom: 6, fontWeight: 500, fontSize: 13 }}>{t('layout.projectName')}</div>
            <Input
              placeholder={t('layout.projectNamePlaceholder')}
              value={newProjectName}
              onChange={e => setNewProjectName(e.target.value)}
              onPressEnter={handleCreateProject}
              maxLength={50}
              autoFocus
            />
          </div>
          <div>
            <div style={{ marginBottom: 6, fontWeight: 500, fontSize: 13 }}>{t('layout.projectDesc')}</div>
            <Input.TextArea
              placeholder={t('layout.projectDescPlaceholder')}
              value={newProjectDesc}
              onChange={e => setNewProjectDesc(e.target.value)}
              rows={3}
              maxLength={200}
            />
          </div>
        </div>
      </Modal>

      {/* 编辑项目弹窗 */}
      <Modal
        title={t('layout.editProject')}
        open={editProjectModalOpen}
        onCancel={() => {
          setEditProjectModalOpen(false)
          setEditingProject(null)
        }}
        onOk={handleEditProject}
        confirmLoading={editProjectLoading}
        okText={t('common.confirm')}
        cancelText={t('common.cancel')}
        destroyOnHidden
      >
        <div style={{ display: 'flex', flexDirection: 'column', gap: 16, marginTop: 8 }}>
          <div>
            <div style={{ marginBottom: 6, fontWeight: 500, fontSize: 13 }}>{t('layout.projectName')}</div>
            <Input
              placeholder={t('layout.projectNamePlaceholder')}
              value={editProjectName}
              onChange={e => setEditProjectName(e.target.value)}
              onPressEnter={handleEditProject}
              maxLength={50}
              autoFocus
            />
          </div>
          <div>
            <div style={{ marginBottom: 6, fontWeight: 500, fontSize: 13 }}>{t('layout.projectDesc')}</div>
            <Input.TextArea
              placeholder={t('layout.projectDescPlaceholder')}
              value={editProjectDesc}
              onChange={e => setEditProjectDesc(e.target.value)}
              rows={3}
              maxLength={200}
            />
          </div>
        </div>
      </Modal>
    </div>
  )
}

export default MainLayout
