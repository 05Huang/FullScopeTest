import React, { useState, useEffect } from 'react'
import { Popover, List, Avatar, Typography, Badge, Button, Spin } from 'antd'
import {
  BellOutlined,
  CheckCircleOutlined,
  InfoCircleOutlined,
  CloseCircleOutlined,
  ClockCircleOutlined
} from '@ant-design/icons'
import { getTestRuns, TestRun } from '@/services/reportService'
import dayjs from 'dayjs'
import relativeTime from 'dayjs/plugin/relativeTime'
import 'dayjs/locale/zh-cn'

dayjs.extend(relativeTime)
dayjs.locale('zh-cn')

const { Text } = Typography

export const NotificationPopover: React.FC = () => {
  const [open, setOpen] = useState(false)
  const [notifications, setNotifications] = useState<any[]>([])
  const [loading, setLoading] = useState(false)
  const [unreadCount, setUnreadCount] = useState(0)

  const fetchNotifications = async () => {
    try {
      setLoading(true)
      // 获取最近的测试执行记录作为通知
      const res = await getTestRuns({ page: 1, per_page: 10 })
      if (res.code === 200 && res.data?.items) {
        const runs: TestRun[] = res.data.items
        
        const mappedNotifications = runs.map(run => {
          let type = 'info'
          let title = `测试执行: ${run.test_object_name || '未命名'}`
          let description = ''

          if (run.status === 'success' || run.status === 'passed' as any) {
            type = 'success'
            title = `测试执行成功: ${run.test_object_name || '未命名'}`
            description = `共执行 ${run.total_cases} 个用例，全部通过。`
          } else if (run.status === 'failed') {
            type = 'error'
            title = `测试执行失败: ${run.test_object_name || '未命名'}`
            description = `共执行 ${run.total_cases} 个用例，失败 ${run.failed} 个。`
          } else if (run.status === 'running') {
            type = 'warning' // or running
            title = `测试执行中: ${run.test_object_name || '未命名'}`
            description = `正在执行中，已完成 ${run.passed + run.failed} / ${run.total_cases}。`
          } else {
            description = `状态: ${run.status}`
          }

          return {
            id: String(run.id),
            type,
            title,
            description,
            time: dayjs(run.created_at).fromNow(),
            read: false, // 实际应用中可以存在后端或者 localStorage
            original: run
          }
        })
        
        setNotifications(mappedNotifications)
        setUnreadCount(mappedNotifications.filter(n => !n.read).length)
      }
    } catch (error) {
      console.error('Failed to fetch notifications:', error)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    if (open) {
      fetchNotifications()
    }
  }, [open])

  // 初始加载一次获取未读数量
  useEffect(() => {
    fetchNotifications()
  }, [])

  const handleOpenChange = (newOpen: boolean) => {
    setOpen(newOpen)
  }

  const markAllAsRead = () => {
    setNotifications(notifications.map(n => ({ ...n, read: true })))
    setUnreadCount(0)
  }

  const getIconByType = (type: string) => {
    switch (type) {
      case 'info':
        return <InfoCircleOutlined style={{ color: '#1890ff' }} />
      case 'success':
        return <CheckCircleOutlined style={{ color: '#52c41a' }} />
      case 'warning':
        return <ClockCircleOutlined style={{ color: '#faad14' }} />
      case 'error':
        return <CloseCircleOutlined style={{ color: '#ff4d4f' }} />
      default:
        return <BellOutlined style={{ color: '#1890ff' }} />
    }
  }

  const content = (
    <div style={{ width: 336, margin: '-12px -16px' }}>
      <div style={{ padding: '12px 24px', borderBottom: '1px solid #f0f0f0', fontWeight: 500 }}>
        通知 {unreadCount > 0 && `(${unreadCount})`}
      </div>
      <div style={{ maxHeight: 400, overflow: 'auto' }}>
        <Spin spinning={loading}>
          <List
            itemLayout="horizontal"
            dataSource={notifications}
            renderItem={(item) => (
              <List.Item
                style={{
                  padding: '12px 24px',
                  opacity: item.read ? 0.6 : 1,
                  cursor: 'pointer',
                  transition: 'all 0.3s',
                }}
                className="notification-item"
                onClick={() => {
                  const newNotifs = notifications.map(n => n.id === item.id ? { ...n, read: true } : n)
                  setNotifications(newNotifs)
                  setUnreadCount(newNotifs.filter(n => !n.read).length)
                }}
              >
                <List.Item.Meta
                  avatar={
                    <Avatar
                      style={{ backgroundColor: 'transparent' }}
                      icon={getIconByType(item.type)}
                    />
                  }
                  title={
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                      <Text strong={!item.read} ellipsis style={{ maxWidth: 200 }}>
                        {item.title}
                      </Text>
                      {!item.read && <Badge status="processing" />}
                    </div>
                  }
                  description={
                    <div>
                      <div style={{ marginBottom: 4, fontSize: 13, color: 'rgba(0,0,0,0.65)' }}>
                        {item.description}
                      </div>
                      <div style={{ fontSize: 12, color: 'rgba(0,0,0,0.45)' }}>{item.time}</div>
                    </div>
                  }
                />
              </List.Item>
            )}
            locale={{ emptyText: '暂无通知' }}
          />
        </Spin>
      </div>
      <div
        style={{
          borderTop: '1px solid #f0f0f0',
          padding: '12px 24px',
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
        }}
      >
        <Button type="link" size="small" onClick={markAllAsRead}>
          全部已读
        </Button>
        <Button type="link" size="small" href="/reports">
          查看所有执行记录
        </Button>
      </div>
    </div>
  )

  return (
    <Popover
      content={content}
      trigger="click"
      open={open}
      onOpenChange={handleOpenChange}
      placement="bottomRight"
      overlayClassName="notification-popover"
      arrow={false}
    >
      <Badge count={unreadCount} size="small" offset={[-4, 4]}>
        <Button
          type="text"
          icon={<BellOutlined />}
          style={{ fontSize: 18 }}
        />
      </Badge>
    </Popover>
  )
}

export default NotificationPopover
