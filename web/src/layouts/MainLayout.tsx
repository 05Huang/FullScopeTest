import { useState } from 'react'
import { Outlet, useNavigate, useLocation } from 'react-router-dom'
import { Layout, Menu, Avatar, Dropdown, Button, theme } from 'antd'
import {
  HomeOutlined,
  ApiOutlined,
  GlobalOutlined,
  ThunderboltOutlined,
  BarChartOutlined,
  FileTextOutlined,
  SettingOutlined,
  UserOutlined,
  LogoutOutlined,
  MenuFoldOutlined,
  MenuUnfoldOutlined,
  BellOutlined,
} from '@ant-design/icons'
import type { MenuProps } from 'antd'
import { useAuthStore } from '@/stores/authStore'

const { Header, Sider, Content } = Layout

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

// 侧边栏菜单配置
const menuItems: MenuProps['items'] = [
  {
    key: '/dashboard',
    icon: <HomeOutlined />,
    label: '首页',
  },
  {
    key: '/api-test',
    icon: <ApiOutlined />,
    label: '接口测试',
    children: [
      { key: '/api-test/workspace', label: '工作台' },
      { key: '/api-test/collections', label: '用例管理' },
      { key: '/api-test/environments', label: '环境配置' },
    ],
  },
  {
    key: '/web-test',
    icon: <GlobalOutlined />,
    label: 'Web测试',
    children: [
      { key: '/web-test/scripts', label: '脚本管理' },
    ],
  },
  {
    key: '/perf-test',
    icon: <ThunderboltOutlined />,
    label: '性能测试',
    children: [
      { key: '/perf-test/scenarios', label: '场景管理' },
      { key: '/perf-test/monitor', label: '实时监控' },
      { key: '/perf-test/results', label: '结果分析' },
    ],
  },
  {
    key: '/reports',
    icon: <BarChartOutlined />,
    label: '测试报告',
  },
  {
    key: '/docs',
    icon: <FileTextOutlined />,
    label: '测试文档',
  },
]

const MainLayout = () => {
  const [collapsed, setCollapsed] = useState(false)
  const navigate = useNavigate()
  const location = useLocation()
  const { user, logout } = useAuthStore()
  const { token: themeToken } = theme.useToken()

  // 用户下拉菜单
  const userMenuItems: MenuProps['items'] = [
    {
      key: 'profile',
      icon: <UserOutlined />,
      label: '个人设置',
    },
    {
      key: 'settings',
      icon: <SettingOutlined />,
      label: '系统设置',
    },
    { type: 'divider' },
    {
      key: 'logout',
      icon: <LogoutOutlined />,
      label: '退出登录',
      danger: true,
    },
  ]

  const handleMenuClick: MenuProps['onClick'] = ({ key }) => {
    navigate(key)
  }

  const handleUserMenuClick: MenuProps['onClick'] = ({ key }) => {
    if (key === 'logout') {
      logout()
      navigate('/login')
    } else if (key === 'settings') {
      navigate('/settings')
    }
  }

  // 获取当前选中的菜单项
  const getSelectedKeys = () => {
    const path = location.pathname
    return [path]
  }

  // 获取展开的子菜单
  const getOpenKeys = () => {
    const path = location.pathname
    const parts = path.split('/').filter(Boolean)
    if (parts.length > 1) {
      return [`/${parts[0]}`]
    }
    return []
  }

  return (
    <Layout className="fst-app-root" style={{ minHeight: '100vh' }}>
      {/* 侧边栏 */}
      <Sider
        trigger={null}
        collapsible
        collapsed={collapsed}
        width={220}
        className="fst-app-sider"
      >
        {/* Logo */}
        <div className={`fst-app-logo ${collapsed ? 'is-collapsed' : ''}`}>
          <AppBrandMark />
          {!collapsed && <span className="fst-app-logo-text">FullScopeTest</span>}
        </div>

        {/* 菜单 */}
        <Menu
          mode="inline"
          selectedKeys={getSelectedKeys()}
          defaultOpenKeys={getOpenKeys()}
          items={menuItems}
          onClick={handleMenuClick}
          className="fst-app-menu"
        />
      </Sider>

      <Layout>
        {/* 顶部栏 */}
        <Header
          className="fst-app-header"
          style={{ padding: '0 24px' }}
        >
          {/* 左侧：折叠按钮 */}
          <Button
            type="text"
            icon={collapsed ? <MenuUnfoldOutlined /> : <MenuFoldOutlined />}
            onClick={() => setCollapsed(!collapsed)}
            style={{ fontSize: 16, width: 48, height: 48 }}
          />

          {/* 右侧：通知和用户 */}
          <div style={{ display: 'flex', alignItems: 'center', gap: 16 }}>
            <Button
              type="text"
              icon={<BellOutlined />}
              style={{ fontSize: 18 }}
            />

            <Dropdown
              menu={{ items: userMenuItems, onClick: handleUserMenuClick }}
              placement="bottomRight"
            >
              <div
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  cursor: 'pointer',
                  padding: '4px 8px',
                  borderRadius: 8,
                }}
              >
                <Avatar
                  size={32}
                  icon={<UserOutlined />}
                  src={user?.avatar}
                  style={{ backgroundColor: themeToken.colorPrimary }}
                />
                <span style={{ marginLeft: 8, fontWeight: 500 }}>
                  {user?.username || '用户'}
                </span>
              </div>
            </Dropdown>
          </div>
        </Header>

        {/* 内容区域 */}
        <Content
          className="fst-app-content"
          style={{ margin: 24, padding: 24, minHeight: 'calc(100vh - 64px - 48px)' }}
        >
          <Outlet />
        </Content>
      </Layout>
    </Layout>
  )
}

export default MainLayout
