/**
 * 计费服务层
 *
 * 对接后端套餐查询、订阅管理、用量查询 API。
 */
import api, { ApiResponse } from './api'

// ── 类型定义 ────────────────────────────────────────────────────────────────

export interface BillingPlan {
  id: number
  name: string
  display_name: string
  price_monthly: number
  price_yearly: number
  max_projects: number
  max_test_cases: number
  max_ai_calls_per_month: number
  max_members: number
  max_storage_mb: number
  features: string[]
  is_active: boolean
}

export interface Subscription {
  id: number
  organization_id: number
  plan_name: string
  plan_display_name?: string
  billing_cycle: string
  status: string
  start_date: string
  end_date: string | null
  next_billing_date: string | null
  auto_renew: boolean
  created_at: string
}

export interface ResourceQuota {
  resource: string
  limit: number
  used: number
  remaining: number
  percentage: number
}

export interface UsageQuotas {
  projects: ResourceQuota
  test_cases: ResourceQuota
  ai_calls: ResourceQuota
  members: ResourceQuota
  storage: ResourceQuota
}

// ── API 调用 ────────────────────────────────────────────────────────────────

/** 获取所有套餐 */
export const getPlans = (): Promise<ApiResponse<BillingPlan[]>> => {
  return api.get('/billing/plans') as Promise<ApiResponse<BillingPlan[]>>
}

/** 获取当前订阅 */
export const getSubscription = (): Promise<ApiResponse<Subscription>> => {
  return api.get('/billing/subscription') as Promise<ApiResponse<Subscription>>
}

/** 升级/变更套餐 */
export const upgradeSubscription = (
  planName: string,
  billingCycle: string = 'monthly'
): Promise<ApiResponse<Subscription>> => {
  return api.post('/billing/subscription', {
    plan_name: planName,
    billing_cycle: billingCycle,
  }) as Promise<ApiResponse<Subscription>>
}

/** 取消订阅 */
export const cancelSubscription = (): Promise<ApiResponse<Subscription>> => {
  return api.delete('/billing/subscription') as Promise<ApiResponse<Subscription>>
}

/** 获取当前用量 */
export const getUsage = (): Promise<ApiResponse<UsageQuotas>> => {
  return api.get('/billing/usage') as Promise<ApiResponse<UsageQuotas>>
}

/** 检查单项资源配额 */
export const checkResourceQuota = (resource: string): Promise<ApiResponse<ResourceQuota>> => {
  return api.get(`/billing/quota/${resource}`) as Promise<ApiResponse<ResourceQuota>>
}

// ── 统一导出 ────────────────────────────────────────────────────────────────

export const billingService = {
  getPlans,
  getSubscription,
  upgradeSubscription,
  cancelSubscription,
  getUsage,
  checkResourceQuota,
}

export default billingService
