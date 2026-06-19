/**
 * 权限感知按钮组件
 *
 * 根据用户角色控制按钮的显示/禁用状态。
 * 支持 hide（隐藏）和 disable（禁用+Tooltip）两种模式。
 */
import React from 'react'
import { Button, Tooltip } from 'antd'
import type { ButtonProps } from 'antd'
import { useRole } from '@/hooks/useRole'

interface PermissionButtonProps extends ButtonProps {
  /** 所需角色列表 */
  roles?: string[]
  /** 所需权限（暂用角色判断，后续可扩展为细粒度权限） */
  resource?: string;
  action?: string;
  /** 无权限时的行为：hide 隐藏，disable 禁用+提示 */
  mode?: 'hide' | 'disable';
  /** 禁用时的提示文本 */
  noPermissionTip?: string;
}

// 角色权限映射表
const ROLE_PERMISSIONS: Record<string, Record<string, string[]>> = {
  project: { create: ['admin', 'member'], update: ['admin', 'member'], delete: ['admin'] },
  test_case: { create: ['admin', 'member'], update: ['admin', 'member'], delete: ['admin'] },
  environment: { create: ['admin', 'member'], update: ['admin', 'member'], delete: ['admin'] },
  billing: { update: ['admin'] },
  settings: { update: ['admin'] },
};

const PermissionButton: React.FC<PermissionButtonProps> = ({
  roles, resource, action, mode = 'hide', noPermissionTip, children, ...rest
}) => {
  const { role } = useRole()

  // 判断是否有权限
  let hasPermission = false
  if (roles) {
    hasPermission = roles.includes(role)
  } else if (resource && action) {
    const allowedRoles = ROLE_PERMISSIONS[resource]?.[action] || []
    hasPermission = allowedRoles.includes(role)
  } else {
    // 无角色和权限要求时默认允许
    hasPermission = true
  }

  if (hasPermission) {
    return <Button {...rest}>{children}</Button>
  }

  // 无权限：隐藏模式
  if (mode === 'hide') {
    return null
  }

  // 无权限：禁用模式
  const tip = noPermissionTip || 'No permission'
  return (
    <Tooltip title={tip}>
      <Button {...rest} disabled>{children}</Button>
    </Tooltip>
  )
};

export default PermissionButton
