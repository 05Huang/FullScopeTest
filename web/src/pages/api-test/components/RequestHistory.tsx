/**
 * 请求历史记录面板
 *
 * 自动保存最近 50 条请求到 localStorage
 * 支持点击回填到请求编辑器，支持清空历史
 */

import { useState, useEffect } from 'react'
import { List, Tag, Typography, Button, Empty, Popconfirm, Space, Tooltip } from 'antd'
import { DeleteOutlined, HistoryOutlined, ReloadOutlined } from '@ant-design/icons'
import { useTranslation } from 'react-i18next'

const { Text } = Typography

interface HistoryItem {
  method: string
  url: string
  status?: number
  duration?: number
  timestamp: number
}

const STORAGE_KEY = 'fst-request-history'
const MAX_ITEMS = 50

const METHOD_COLORS: Record<string, string> = {
  GET: 'green',
  POST: 'blue',
  PUT: 'orange',
  PATCH: 'gold',
  DELETE: 'red',
  HEAD: 'default',
  OPTIONS: 'default',
}

interface RequestHistoryProps {
  onSelect: (item: { method: string; url: string }) => void
}

const RequestHistory: React.FC<RequestHistoryProps> = ({ onSelect }) => {
  const { t } = useTranslation()
  const [history, setHistory] = useState<HistoryItem[]>([])

  useEffect(() => {
    loadHistory()
  }, [])

  const loadHistory = () => {
    try {
      const stored = localStorage.getItem(STORAGE_KEY)
      if (stored) {
        setHistory(JSON.parse(stored))
      }
    } catch {
      setHistory([])
    }
  }

  const clearHistory = () => {
    localStorage.removeItem(STORAGE_KEY)
    setHistory([])
  }

  const formatTime = (timestamp: number) => {
    const date = new Date(timestamp)
    const now = new Date()
    const isToday = date.toDateString() === now.toDateString()
    if (isToday) {
      return date.toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit', second: '2-digit' })
    }
    return date.toLocaleDateString('zh-CN', { month: '2-digit', day: '2-digit' }) + ' ' +
      date.toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' })
  }

  return (
    <div style={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '8px 0', marginBottom: 8 }}>
        <Space>
          <HistoryOutlined />
          <Text strong>{t('apiTest.history.title')}</Text>
        </Space>
        <Space>
          <Tooltip title={t('common.refresh')}>
            <Button type="text" size="small" icon={<ReloadOutlined />} onClick={loadHistory} />
          </Tooltip>
          {history.length > 0 && (
            <Popconfirm title={t('apiTest.history.confirmClear')} onConfirm={clearHistory}>
              <Button type="text" size="small" danger icon={<DeleteOutlined />} />
            </Popconfirm>
          )}
        </Space>
      </div>

      {history.length === 0 ? (
        <Empty
          description={t('apiTest.history.empty')}
          image={Empty.PRESENTED_IMAGE_SIMPLE}
          style={{ marginTop: 40 }}
        />
      ) : (
        <List
          size="small"
          dataSource={history}
          style={{ flex: 1, overflow: 'auto' }}
          renderItem={(item) => (
            <List.Item
              style={{ cursor: 'pointer', padding: '6px 4px' }}
              onClick={() => onSelect({ method: item.method, url: item.url })}
            >
              <div style={{ display: 'flex', alignItems: 'center', gap: 8, width: '100%' }}>
                <Tag color={METHOD_COLORS[item.method] || 'default'} style={{ minWidth: 50, textAlign: 'center' }}>
                  {item.method}
                </Tag>
                <Text
                  ellipsis
                  style={{ flex: 1, fontSize: 12 }}
                  title={item.url}
                >
                  {item.url}
                </Text>
                {item.status && (
                  <Tag color={item.status < 400 ? 'success' : 'error'} style={{ fontSize: 11 }}>
                    {item.status}
                  </Tag>
                )}
                {item.duration !== undefined && (
                  <Text type="secondary" style={{ fontSize: 11 }}>
                    {item.duration}ms
                  </Text>
                )}
                <Text type="secondary" style={{ fontSize: 11, whiteSpace: 'nowrap' }}>
                  {formatTime(item.timestamp)}
                </Text>
              </div>
            </List.Item>
          )}
        />
      )}
    </div>
  )
}

/** 将请求保存到历史记录 */
export const saveToHistory = (item: Omit<HistoryItem, 'timestamp'>) => {
  try {
    const stored = localStorage.getItem(STORAGE_KEY)
    const history: HistoryItem[] = stored ? JSON.parse(stored) : []
    const newItem: HistoryItem = { ...item, timestamp: Date.now() }

    // 去重：如果最近一条相同则不重复添加
    if (history.length > 0 && history[0].method === item.method && history[0].url === item.url) {
      return
    }

    history.unshift(newItem)
    if (history.length > MAX_ITEMS) {
      history.length = MAX_ITEMS
    }
    localStorage.setItem(STORAGE_KEY, JSON.stringify(history))
  } catch {
    // localStorage 写入失败时静默忽略
  }
}

export default RequestHistory
