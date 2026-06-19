/**
 * RBAC 路由守卫组件
 *
 * 根据用户角色控制页面/组件访问权限。
 * 不满足角色要求时展示「权限不足」页面。
 */
import React from 'react'
import { Result, Button } from 'antd'
import { LockOutlined } from '@ant-design/icons'
import { useNavigate } from 'react-router-dom'
import { useTranslation } from 'react-i18next'
import { useRole } from '@/hooks/useRole'

interface RequireRoleProps {
  /** 允许的角色列表 */
  roles: string[]
  /** 不满足时的自定义 fallback */
  fallback?: React.ReactNode
  /** 子组件 */
  children: React.ReactNode
}

/**
 * 用法：
 * <RequireRole roles={["admin", "member"]}>
 *   <BillingPage />
 * </RequireRole>
 */
const RequireRole: React.FC<RequireRoleProps> = ({ roles, fallback, children }) => {
  const { role } = useRole()
  const navigate = useNavigate()
  const { t } = useTranslation()

  if (roles.includes(role)) {
    return <>{children}</>
  }

  if (fallback) {
    return <>{fallback}</>
  }

  return (
    <Result
      status='403'
      icon={<LockOutlined />}
      title={t('common.noPermission') || 'No Permission'}
      subTitle={t('common.noPermissionDesc') || 'You do not have permission to access this page.'}
      extra={<Button type='primary' onClick={() => navigate('/dashboard')}>{t('common.backToHome') || 'Back to Home'}</Button>}
    />
  )
};

export default RequireRole
