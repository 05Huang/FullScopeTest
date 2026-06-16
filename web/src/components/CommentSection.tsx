/**
 * 评论区组件
 *
 * 可复用组件，接收 resourceType 和 resourceId 两个 props。
 * 支持评论列表、发表评论、编辑、删除。
 */
import { useState, useEffect, useCallback } from 'react'
import {
  List,
  Button,
  Input,
  Avatar,
  Space,
  Popconfirm,
  message,
  Empty,
  Typography,
  Spin,
} from 'antd'
import {
  EditOutlined,
  DeleteOutlined,
  SendOutlined,
  UserOutlined,
} from '@ant-design/icons'
import { useTranslation } from 'react-i18next'
import commentService, { Comment } from '@/services/commentService'
import { useAuthStore } from '@/stores/authStore'

const { Text } = Typography
const { TextArea } = Input

interface CommentSectionProps {
  resourceType: string
  resourceId: number
}

const CommentSection = ({ resourceType, resourceId }: CommentSectionProps) => {
  const { t } = useTranslation()
  const { user } = useAuthStore()
  const [comments, setComments] = useState<Comment[]>([])
  const [total, setTotal] = useState(0)
  const [loading, setLoading] = useState(false)
  const [submitting, setSubmitting] = useState(false)
  const [content, setContent] = useState('')
  const [editingId, setEditingId] = useState<number | null>(null)
  const [editContent, setEditContent] = useState('')
  const [page, setPage] = useState(1)

  const fetchComments = useCallback(async () => {
    setLoading(true)
    try {
      const res = await commentService.getComments(resourceType, resourceId, {
        page,
        per_page: 20,
      })
      if (res.code === 200 && res.data) {
        setComments(res.data.items || [])
        setTotal(res.data.total || 0)
      }
    } catch {
      // 静默失败
    } finally {
      setLoading(false)
    }
  }, [resourceType, resourceId, page])

  useEffect(() => {
    fetchComments()
  }, [fetchComments])

  const handleSubmit = async () => {
    if (!content.trim()) return
    setSubmitting(true)
    try {
      const res = await commentService.createComment({
        resource_type: resourceType,
        resource_id: resourceId,
        content: content.trim(),
      })
      if ((res.code === 200 || res.code === 201) && res.data) {
        setContent('')
        await fetchComments()
      } else {
        message.error(res.message || t('comments.submitFailed'))
      }
    } catch {
      message.error(t('comments.submitFailed'))
    } finally {
      setSubmitting(false)
    }
  }

  const handleEdit = async (commentId: number) => {
    if (!editContent.trim()) return
    try {
      const res = await commentService.updateComment(commentId, editContent.trim())
      if (res.code === 200) {
        setEditingId(null)
        setEditContent('')
        await fetchComments()
      } else {
        message.error(res.message || t('comments.editFailed'))
      }
    } catch {
      message.error(t('comments.editFailed'))
    }
  }

  const handleDelete = async (commentId: number) => {
    try {
      const res = await commentService.deleteComment(commentId)
      if (res.code === 200) {
        message.success(t('comments.deleteSuccess'))
        await fetchComments()
      } else {
        message.error(res.message || t('comments.deleteFailed'))
      }
    } catch {
      message.error(t('comments.deleteFailed'))
    }
  }

  const startEdit = (comment: Comment) => {
    setEditingId(comment.id)
    setEditContent(comment.content)
  }

  const cancelEdit = () => {
    setEditingId(null)
    setEditContent('')
  }

  const isOwner = (comment: Comment) => user?.id === comment.user_id

  const formatTime = (timeStr: string) => {
    const date = new Date(timeStr)
    const now = new Date()
    const diffMs = now.getTime() - date.getTime()
    const diffMins = Math.floor(diffMs / 60000)
    if (diffMins < 1) return t('dashboard.time.justNow')
    if (diffMins < 60) return t('dashboard.time.minutesAgo', { minutes: diffMins })
    const diffHours = Math.floor(diffMins / 60)
    if (diffHours < 24) return t('dashboard.time.hoursAgo', { hours: diffHours })
    return date.toLocaleString()
  }

  return (
    <div>
      {/* 评论输入 */}
      <div style={{ marginBottom: 16 }}>
        <TextArea
          placeholder={t('comments.placeholder')}
          value={content}
          onChange={(e) => setContent(e.target.value)}
          rows={3}
          maxLength={2000}
          style={{ marginBottom: 8 }}
        />
        <div style={{ display: 'flex', justifyContent: 'flex-end' }}>
          <Button
            type="primary"
            icon={<SendOutlined />}
            onClick={handleSubmit}
            loading={submitting}
            disabled={!content.trim()}
            size="small"
          >
            {t('comments.send')}
          </Button>
        </div>
      </div>

      {/* 评论列表 */}
      {loading ? (
        <div style={{ display: 'flex', justifyContent: 'center', padding: 24 }}>
          <Spin />
        </div>
      ) : comments.length === 0 ? (
        <Empty
          description={t('comments.noComments')}
          image={Empty.PRESENTED_IMAGE_SIMPLE}
          style={{ padding: '24px 0' }}
        />
      ) : (
        <List
          dataSource={comments}
          pagination={
            total > 20
              ? {
                  current: page,
                  pageSize: 20,
                  total,
                  onChange: setPage,
                  size: 'small',
                }
              : undefined
          }
          renderItem={(comment) => (
            <List.Item
              style={{ padding: '8px 0' }}
              actions={
                isOwner(comment)
                  ? [
                      <Button
                        key="edit"
                        type="text"
                        size="small"
                        icon={<EditOutlined />}
                        onClick={() => startEdit(comment)}
                      />,
                      <Popconfirm
                        key="delete"
                        title={t('comments.deleteConfirm')}
                        onConfirm={() => handleDelete(comment.id)}
                        okText={t('common.confirm')}
                        cancelText={t('common.cancel')}
                      >
                        <Button type="text" size="small" danger icon={<DeleteOutlined />} />
                      </Popconfirm>,
                    ]
                  : undefined
              }
            >
              <List.Item.Meta
                avatar={
                  <Avatar
                    size={32}
                    icon={<UserOutlined />}
                    src={comment.avatar}
                    style={{ backgroundColor: 'var(--fst-primary)' }}
                  />
                }
                title={
                  <Space size={8}>
                    <Text strong style={{ fontSize: 13 }}>
                      {comment.username || `User #${comment.user_id}`}
                    </Text>
                    <Text type="secondary" style={{ fontSize: 11 }}>
                      {formatTime(comment.created_at)}
                    </Text>
                  </Space>
                }
                description={
                  editingId === comment.id ? (
                    <div>
                      <TextArea
                        value={editContent}
                        onChange={(e) => setEditContent(e.target.value)}
                        rows={3}
                        maxLength={2000}
                        style={{ marginBottom: 8 }}
                      />
                      <Space>
                        <Button size="small" type="primary" onClick={() => handleEdit(comment.id)}>
                          {t('common.save')}
                        </Button>
                        <Button size="small" onClick={cancelEdit}>
                          {t('common.cancel')}
                        </Button>
                      </Space>
                    </div>
                  ) : (
                    <div style={{ whiteSpace: 'pre-wrap', fontSize: 13, color: 'var(--fst-on-surface)' }}>
                      {comment.content}
                    </div>
                  )
                }
              />
            </List.Item>
          )}
        />
      )}
    </div>
  )
}

export default CommentSection
