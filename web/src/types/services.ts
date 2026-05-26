/**
 * 服务层通用类型定义
 */

// API 响应基础结构
export interface ApiResponse<T = any> {
  code: number
  message: string
  data: T
  timestamp: number
}

// 分页参数
export interface PaginationParams {
  page?: number
  per_page?: number
}

// 分页响应
export interface PaginatedData<T> {
  items: T[]
  pagination: {
    total: number
    page: number
    per_page: number
    pages: number
  }
}

// 排序参数
export interface SortParams {
  sort_by?: string
  sort_order?: 'asc' | 'desc'
}

// 过滤参数
export interface FilterParams {
  [key: string]: any
}

// 列表查询参数
export interface ListParams extends PaginationParams, SortParams, FilterParams {
  project_id?: number
  search?: string
}
