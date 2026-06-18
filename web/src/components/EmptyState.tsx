/**
 * 统一空状态组件
 *
 * 提供品牌化的空状态展示：插图 + 主标题 + 副标题 + 操作按钮
 * 替代 Ant Design 默认的 Empty 组件，增强品牌感和引导性。
 */

import { Button, Typography } from 'antd'
import { PlusOutlined, PlayCircleOutlined, FileTextOutlined, CalendarOutlined } from '@ant-design/icons'
import { useTranslation } from 'react-i18next'

const { Title, Text } = Typography

interface EmptyStateProps {
  /** 场景类型 */
  variant: 'projects' | 'testCases' | 'reports' | 'testPlans' | 'default'
  /** 自定义标题 */
  title?: string
  /** 自定义副标题 */
  subtitle?: string
  /** 操作按钮点击回调 */
  onAction?: () => void
  /** 自定义操作按钮文案 */
  actionText?: string
}

const VARIANT_CONFIG = {
  projects: {
    icon: <PlusOutlined style={{ fontSize: 48, color: '#5FA59B' }} />,
    titleKey: 'emptyState.projects.title',
    subtitleKey: 'emptyState.projects.subtitle',
    actionKey: 'emptyState.projects.action',
  },
  testCases: {
    icon: <PlusOutlined style={{ fontSize: 48, color: '#5FA59B' }} />,
    titleKey: 'emptyState.testCases.title',
    subtitleKey: 'emptyState.testCases.subtitle',
    actionKey: 'emptyState.testCases.action',
  },
  reports: {
    icon: <PlayCircleOutlined style={{ fontSize: 48, color: '#5FA59B' }} />,
    titleKey: 'emptyState.reports.title',
    subtitleKey: 'emptyState.reports.subtitle',
    actionKey: 'emptyState.reports.action',
  },
  testPlans: {
    icon: <CalendarOutlined style={{ fontSize: 48, color: '#5FA59B' }} />,
    titleKey: 'emptyState.testPlans.title',
    subtitleKey: 'emptyState.testPlans.subtitle',
    actionKey: 'emptyState.testPlans.action',
  },
  default: {
    icon: <FileTextOutlined style={{ fontSize: 48, color: '#5FA59B' }} />,
    titleKey: 'emptyState.default.title',
    subtitleKey: 'emptyState.default.subtitle',
    actionKey: 'emptyState.default.action',
  },
}

const EmptyState: React.FC<EmptyStateProps> = ({ variant, title, subtitle, onAction, actionText }) => {
  const { t } = useTranslation()
  const config = VARIANT_CONFIG[variant] || VARIANT_CONFIG.default

  return (
    <div style={{
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
      justifyContent: 'center',
      padding: '48px 24px',
      textAlign: 'center',
    }}>
      <div style={{ marginBottom: 16 }}>{config.icon}</div>
      <Title level={5} style={{ marginBottom: 8, color: '#333' }}>
        {title || t(config.titleKey)}
      </Title>
      <Text type="secondary" style={{ marginBottom: 24, maxWidth: 320 }}>
        {subtitle || t(config.subtitleKey)}
      </Text>
      {onAction && (
        <Button type="primary" icon={<PlusOutlined />} onClick={onAction}>
          {actionText || t(config.actionKey)}
        </Button>
      )}
    </div>
  )
}

export default EmptyState
