import { useState, useEffect } from 'react'
import { Outlet, useNavigate, useLocation } from 'react-router-dom'
import { Layout, Avatar, Dropdown, Button, Tour, ConfigProvider, Popover, Typography, Select } from 'antd'
import type { TourProps } from 'antd'
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
} from '@ant-design/icons'
import { useTranslation } from 'react-i18next'
import { useAuthStore } from '@/stores/authStore'
import { useProjectStore } from '@/stores/projectStore'
import GlobalCopilot from '../components/GlobalCopilot'
import NotificationPopover from '../components/NotificationPopover'
import GlobalSearch from '../components/GlobalSearch'

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
}

const SidebarItem = ({ icon, label, path, active, expanded, currentPath, children, onClick, onToggle }: SidebarItemProps) => {
  const isActive = active || (children?.some(c => currentPath === c.path) ?? false)
  return (
    <div style={{ marginBottom: 2 }}>
      <button
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
        <span style={{ flex: 1 }}>{label}</span>
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

const AppBrandMark = () => (
  <div className="fst-app-brand" aria-hidden="true">
    <svg viewBox="0 0 64 64" className="fst-app-brand-svg">
      <defs>
        <linearGradient id="fstAppBrandG" x1="10" y1="8" x2="56" y2="56" gradientUnits="userSpaceOnUse">
          <stop offset="0" stopColor="#5FA59B" />
          <stop offset="0.6" stopColor="#3D6E66" />
          <stop offset="1" stopColor="#D7B56D" />
        </linearGradient>
        <filter id="fstAppGlow" x="-40%" y="-40%" width="180%" height="180%">
          <feGaussianBlur stdDeviation="3.2" result="blur" />
          <feColorMatrix
            in="blur"
            type="matrix"
            values="1 0 0 0 0  0 1 0 0 0  0 0 1 0 0  0 0 0 0.85 0"
            result="glow"
          />
          <feMerge>
            <feMergeNode in="glow" />
            <feMergeNode in="SourceGraphic" />
          </feMerge>
        </filter>
      </defs>
      <path
        d="M18 16h28c1.7 0 3 1.3 3 3v7c0 1.7-1.3 3-3 3H25.2v6.2H42c1.7 0 3 1.3 3 3v7c0 1.7-1.3 3-3 3H18c-1.7 0-3-1.3-3-3V19c0-1.7 1.3-3 3-3Z"
        fill="url(#fstAppBrandG)"
        filter="url(#fstAppGlow)"
      />
      <path
        d="M22 23h24"
        stroke="rgba(255,255,255,0.55)"
        strokeWidth="2"
        strokeLinecap="round"
      />
      <path
        d="M22 45h18"
        stroke="rgba(255,255,255,0.38)"
        strokeWidth="2"
        strokeLinecap="round"
      />
    </svg>
  </div>
)

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
  const [collapsed, setCollapsed] = useState(false)
  const navigate = useNavigate()
  const location = useLocation()
  const { user, logout } = useAuthStore()
  const { currentProjectId, projects, setCurrentProject, fetchProjects } = useProjectStore()
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

  // 加载项目列表
  useEffect(() => {
    fetchProjects()
  }, [fetchProjects])

  const [tourOpen, setTourOpen] = useState(false)

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
      title: t('sidebar.dashboard'),
      description: t('tour.welcome'),
      target: () => document.querySelector('.fst-app-logo') as HTMLElement,
    },
    {
      title: t('sidebar.dashboard'),
      description: t('tour.dashboard'),
      target: () => document.getElementById('tour-step-dashboard-api') as HTMLElement,
    },
    {
      title: t('sidebar.apiTest'),
      description: t('tour.navigation'),
      target: () => document.querySelector('.fst-app-menu') as HTMLElement,
      placement: 'right',
    },
    {
      title: t('sidebar.aiInsights'),
      description: t('tour.search'),
      target: () => document.getElementById('tour-step-search') as HTMLElement,
    },
  ]

  // Sidebar nav configuration
  const sidebarNav = [
    { icon: <HomeOutlined />, label: t('sidebar.dashboard'), path: '/dashboard' },
    { icon: <ApiOutlined />, label: t('sidebar.apiTest'), path: '/api-test', children: [
      { label: t('sidebar.workspace'), path: '/api-test/workspace' },
      { label: t('sidebar.collections'), path: '/api-test/collections' },
      { label: t('sidebar.environments'), path: '/api-test/environments' },
    ]},
    { icon: <GlobalOutlined />, label: t('sidebar.webTest'), path: '/web-test', children: [
      { label: t('sidebar.scripts'), path: '/web-test/scripts' },
    ]},
    { icon: <MobileOutlined />, label: t('sidebar.appTest'), path: '/app-test', children: [
      { label: t('sidebar.scripts'), path: '/app-test/scripts' },
    ]},
    { icon: <ThunderboltOutlined />, label: t('sidebar.perfTest'), path: '/perf-test', children: [
      { label: t('sidebar.scenarios'), path: '/perf-test/scenarios' },
      { label: t('sidebar.monitor'), path: '/perf-test/monitor' },
      { label: t('sidebar.results'), path: '/perf-test/results' },
      { label: t('sidebar.perfDashboard'), path: '/perf-test/dashboard' },
    ]},
    { icon: <BarChartOutlined />, label: t('sidebar.reports'), path: '/reports' },
    { icon: <ApiOutlined />, label: t('sidebar.cicd'), path: '/ci-cd' },
    { icon: <FileTextOutlined />, label: t('sidebar.documents'), path: '/docs' },
    { icon: <SettingOutlined />, label: t('sidebar.settings'), path: '/settings' },
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
      {/* ─── iOS Sidebar ─── */}
      <aside style={{
        width: collapsed ? 72 : 260,
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
        <div style={{
          display: 'flex',
          alignItems: 'center',
          gap: 12,
          padding: '8px 4px 20px',
          borderBottom: '1px solid var(--fst-outline-soft)',
          marginBottom: 12,
          minWidth: 0,
        }}>
          <AppBrandMark />
          {!collapsed && (
            <div style={{ minWidth: 0 }}>
              <div style={{
                fontSize: 17,
                fontWeight: 700,
                letterSpacing: '0.01em',
                color: 'var(--fst-primary)',
                whiteSpace: 'nowrap',
              }}>FullScopeTest</div>
              <div style={{
                fontSize: 11,
                color: 'var(--fst-on-surface-muted)',
                letterSpacing: '0.02em',
              }}>Enterprise QA</div>
            </div>
          )}
        </div>

        {/* Navigation */}
        <nav style={{ flex: 1, overflowY: 'auto', overflowX: 'hidden' }}>
          {sidebarNav.map(item => (
            <SidebarItem
              key={item.path}
              icon={item.icon}
              label={item.label}
              path={item.path}
              active={location.pathname === item.path || location.pathname.startsWith(item.path + '/')}
              expanded={expandedGroups.has(item.path)}
              currentPath={location.pathname}
              children={item.children}
              onClick={(p) => navigate(p)}
              onToggle={() => toggleGroup(item.path)}
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
              <div style={{ width: 260, padding: '4px' }}>
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
                    查看个人主页 & 简历
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
      </aside>

      {/* ─── Main Content ─── */}
      <div style={{
        flex: 1,
        marginLeft: collapsed ? 72 : 260,
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
          background: 'rgba(249, 249, 248, 0.6)',
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
            <Select
              showSearch
              placeholder={t("layout.selectProject")}
              optionFilterProp="label"
              value={currentProjectId}
              onChange={setCurrentProject}
              options={projects.map(p => ({ value: p.id, label: p.name }))}
              style={{ width: 200 }}
              prefix={<FolderOutlined />}
              allowClear
              size="middle"
            />
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
                <div style={{ width: 260, padding: '4px' }}>
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
                      查看个人主页 & 简历
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
                  {user?.username || '用户'}
                </span>
              </div>
            </Dropdown>
          </div>
        </header>

        {/* ─── Page Content ─── */}
        <main style={{
          flex: 1,
          padding: 24,
          maxWidth: 1440,
          width: '100%',
          margin: '0 auto',
        }}>
          <Outlet />
        </main>

        {/* ─── Footer ─── */}
        <footer className="fst-app-footer">
          <div className="fst-site-footer" aria-label="网站页脚">
            <a className="fst-site-footer-link" href="https://beian.miit.gov.cn/" target="_blank" rel="noreferrer noopener">
              <FooterBeianIcon className="fst-site-footer-icon" />
              苏ICP备2025167047号-3
            </a>
            <span className="fst-site-footer-sep" aria-hidden="true" />
            <a className="fst-site-footer-link" href="https://github.com/05Huang/FullScopeTest" target="_blank" rel="noreferrer noopener">
              <FooterGithubIcon className="fst-site-footer-icon" />
              GitHub 开源
            </a>
          </div>
        </footer>
        <GlobalCopilot />
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
    </div>
  )
}

export default MainLayout
