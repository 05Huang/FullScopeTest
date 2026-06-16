/**
 * 组织管理服务层
 *
 * 对接后端组织 CRUD、成员管理、角色管理 API。
 */
import api, { ApiResponse } from './api'

// ── 类型定义 ────────────────────────────────────────────────────────────────

export interface Organization {
  id: number
  name: string
  slug: string
  description?: string
  owner_id: number
  member_count?: number
  created_at: string
  updated_at?: string
}

export interface OrganizationMember {
  id: number
  user_id: number
  username?: string
  email?: string
  role: string
  is_active: boolean
  invited_by?: number
  created_at: string
}

export interface RoleInfo {
  id?: number
  name: string
  display_name: string
  description?: string
  is_system: boolean
  permissions: Record<string, string[]>
}

export interface PermissionMap {
  [resource: string]: string[]
}

// ── 组织 CRUD ──────────────────────────────────────────────────────────────

/** 获取当前用户的组织列表 */
export const getMyOrganizations = (): Promise<ApiResponse<Organization[]>> => {
  return api.get('/organizations/me') as Promise<ApiResponse<Organization[]>>
}

/** 创建组织 */
export const createOrganization = (data: {
  name: string
  slug?: string
  description?: string
}): Promise<ApiResponse<Organization>> => {
  return api.post('/organizations', data) as Promise<ApiResponse<Organization>>
}

/** 更新组织 */
export const updateOrganization = (
  orgId: number,
  data: { name?: string; description?: string }
): Promise<ApiResponse<Organization>> => {
  return api.put(`/organizations/${orgId}`, data) as Promise<ApiResponse<Organization>>
}

/** 删除组织 */
export const deleteOrganization = (orgId: number): Promise<ApiResponse> => {
  return api.delete(`/organizations/${orgId}`) as Promise<ApiResponse>
}

// ── 成员管理 ───────────────────────────────────────────────────────────────

/** 获取组织成员列表 */
export const getMembers = (orgId: number): Promise<ApiResponse<OrganizationMember[]>> => {
  return api.get(`/organizations/${orgId}/members`) as Promise<ApiResponse<OrganizationMember[]>>
}

/** 邀请成员 */
export const inviteMember = (
  orgId: number,
  data: { user_id: number; role?: string }
): Promise<ApiResponse<OrganizationMember>> => {
  return api.post(
    `/organizations/${orgId}/members`,
    data
  ) as Promise<ApiResponse<OrganizationMember>>
}

/** 移除成员 */
export const removeMember = (orgId: number, userId: number): Promise<ApiResponse> => {
  return api.delete(`/organizations/${orgId}/members/${userId}`) as Promise<ApiResponse>
}

/** 修改成员角色 */
export const updateMemberRole = (
  orgId: number,
  userId: number,
  role: string
): Promise<ApiResponse<OrganizationMember>> => {
  return api.patch(
    `/organizations/${orgId}/members/${userId}/role`,
    { role }
  ) as Promise<ApiResponse<OrganizationMember>>
}

// ── 角色与权限 ─────────────────────────────────────────────────────────────

/** 获取组织可用角色列表 */
export const getRoles = (orgId: number): Promise<ApiResponse<RoleInfo[]>> => {
  return api.get(`/organizations/${orgId}/roles`) as Promise<ApiResponse<RoleInfo[]>>
}

/** 创建自定义角色 */
export const createRole = (
  orgId: number,
  data: { name: string; display_name: string; permissions?: Record<string, string[]>; description?: string }
): Promise<ApiResponse<RoleInfo>> => {
  return api.post(
    `/organizations/${orgId}/roles`,
    data
  ) as Promise<ApiResponse<RoleInfo>>
}

/** 更新自定义角色 */
export const updateRole = (
  orgId: number,
  roleId: number,
  data: { display_name?: string; permissions?: Record<string, string[]>; description?: string }
): Promise<ApiResponse<RoleInfo>> => {
  return api.put(
    `/organizations/${orgId}/roles/${roleId}`,
    data
  ) as Promise<ApiResponse<RoleInfo>>
}

/** 删除自定义角色 */
export const deleteRole = (orgId: number, roleId: number): Promise<ApiResponse> => {
  return api.delete(`/organizations/${orgId}/roles/${roleId}`) as Promise<ApiResponse>
}

/** 获取系统角色定义 */
export const getSystemRoles = (): Promise<ApiResponse<RoleInfo[]>> => {
  return api.get('/roles/system') as Promise<ApiResponse<RoleInfo[]>>
}

/** 获取当前用户在组织中的权限 */
export const getMyPermissions = (
  orgId: number
): Promise<ApiResponse<{ role: string; permissions: PermissionMap }>> => {
  return api.get(
    `/organizations/${orgId}/my-permissions`
  ) as Promise<ApiResponse<{ role: string; permissions: PermissionMap }>>
}

// ── 统一导出 ──────────────────────────────────────────────────────────────

export const organizationService = {
  getMyOrganizations,
  createOrganization,
  updateOrganization,
  deleteOrganization,
  getMembers,
  inviteMember,
  removeMember,
  updateMemberRole,
  getRoles,
  createRole,
  updateRole,
  deleteRole,
  getSystemRoles,
  getMyPermissions,
}

export default organizationService
