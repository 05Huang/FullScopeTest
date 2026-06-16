/**
 * 评论服务层
 *
 * 对接后端评论 CRUD API。
 */
import api, { ApiResponse } from './api'

export interface Comment {
  id: number
  user_id: number
  username?: string
  avatar?: string
  resource_type: string
  resource_id: number
  content: string
  parent_id: number | null
  is_deleted: boolean
  created_at: string
  updated_at?: string
}

export interface CommentListResponse {
  items: Comment[]
  total: number
  page: number
  per_page: number
}

/** 获取资源的评论列表 */
export const getComments = (
  resourceType: string,
  resourceId: number,
  params?: { page?: number; per_page?: number }
): Promise<ApiResponse<CommentListResponse>> => {
  return api.get(`/comments/${resourceType}/${resourceId}`, {
    params,
  }) as Promise<ApiResponse<CommentListResponse>>
}

/** 创建评论 */
export const createComment = (data: {
  resource_type: string
  resource_id: number
  content: string
  parent_id?: number
}): Promise<ApiResponse<Comment>> => {
  return api.post('/comments', data) as Promise<ApiResponse<Comment>>
}

/** 编辑评论 */
export const updateComment = (
  commentId: number,
  content: string
): Promise<ApiResponse<Comment>> => {
  return api.put(`/comments/${commentId}`, { content }) as Promise<ApiResponse<Comment>>
}

/** 删除评论 */
export const deleteComment = (commentId: number): Promise<ApiResponse> => {
  return api.delete(`/comments/${commentId}`) as Promise<ApiResponse>
}

export const commentService = {
  getComments,
  createComment,
  updateComment,
  deleteComment,
}

export default commentService
