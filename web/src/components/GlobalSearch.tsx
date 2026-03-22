import { useState, useEffect } from 'react'
import { Modal, Input, List, Tag, Typography, Spin } from 'antd'
import { SearchOutlined, ApiOutlined, GlobalOutlined, ThunderboltOutlined, SettingOutlined } from '@ant-design/icons'
import { useNavigate } from 'react-router-dom'
import { globalSearchAI, GlobalSearchResult } from '@/services/aiSearchService'

const { Text } = Typography

const GlobalSearch = () => {
  const [open, setOpen] = useState(false)
  const [query, setQuery] = useState('')
  const [loading, setLoading] = useState(false)
  const [results, setResults] = useState<GlobalSearchResult[]>([])
  const navigate = useNavigate()

  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
        e.preventDefault()
        setOpen(true)
      }
    }
    window.addEventListener('keydown', handleKeyDown)
    return () => window.removeEventListener('keydown', handleKeyDown)
  }, [])

  const handleSearch = async (value: string) => {
    if (!value.trim()) {
      setResults([])
      return
    }
    setLoading(true)
    try {
      const res = await globalSearchAI({ query: value })
      if (res.code === 200 && res.data?.results) {
        setResults(res.data.results)
      }
    } catch (e) {
      console.error(e)
    } finally {
      setLoading(false)
    }
  }

  const getIcon = (type: string) => {
    switch (type) {
      case 'api_case': return <ApiOutlined style={{ color: '#1890ff' }} />
      case 'web_script': return <GlobalOutlined style={{ color: '#52c41a' }} />
      case 'perf_scenario': return <ThunderboltOutlined style={{ color: '#faad14' }} />
      case 'environment': return <SettingOutlined style={{ color: '#722ed1' }} />
      default: return <SearchOutlined />
    }
  }

  const getTypeTag = (type: string) => {
    switch (type) {
      case 'api_case': return <Tag color="blue">接口用例</Tag>
      case 'web_script': return <Tag color="green">Web脚本</Tag>
      case 'perf_scenario': return <Tag color="orange">性能场景</Tag>
      case 'environment': return <Tag color="purple">环境变量</Tag>
      default: return <Tag>{type}</Tag>
    }
  }

  const handleSelect = (item: GlobalSearchResult) => {
    setOpen(false)
    navigate(item.url)
  }

  return (
    <>
      <div 
        onClick={() => setOpen(true)}
        style={{
          display: 'flex',
          alignItems: 'center',
          background: 'rgba(0,0,0,0.04)',
          padding: '4px 12px',
          borderRadius: 6,
          cursor: 'pointer',
          width: 240,
          color: 'rgba(0,0,0,0.45)',
          border: '1px solid transparent',
          transition: 'all 0.3s'
        }}
        onMouseEnter={e => e.currentTarget.style.borderColor = '#d9d9d9'}
        onMouseLeave={e => e.currentTarget.style.borderColor = 'transparent'}
      >
        <SearchOutlined style={{ marginRight: 8 }} />
        <span style={{ flex: 1 }}>搜索 (Ctrl+K)</span>
      </div>

      <Modal
        title={null}
        open={open}
        onCancel={() => setOpen(false)}
        footer={null}
        closable={false}
        width={600}
        styles={{ body: { padding: 0 } }}
        modalRender={(node) => (
          <div style={{ borderRadius: 8, overflow: 'hidden' }}>{node}</div>
        )}
      >
        <div style={{ padding: '16px 24px', borderBottom: '1px solid #f0f0f0' }}>
          <Input
            prefix={<SearchOutlined style={{ color: '#bfbfbf', fontSize: 18 }} />}
            placeholder="使用自然语言搜索（例如：查找关于支付的所有接口和脚本）"
            bordered={false}
            autoFocus
            value={query}
            onChange={e => setQuery(e.target.value)}
            onPressEnter={() => handleSearch(query)}
            style={{ fontSize: 16 }}
          />
        </div>
        
        <div style={{ maxHeight: 400, overflow: 'auto', padding: '8px 0' }}>
          {loading ? (
            <div style={{ textAlign: 'center', padding: 40 }}><Spin /></div>
          ) : results.length > 0 ? (
            <List
              dataSource={results}
              renderItem={(item) => (
                <List.Item
                  onClick={() => handleSelect(item)}
                  style={{
                    padding: '12px 24px',
                    cursor: 'pointer',
                    transition: 'background 0.2s',
                  }}
                  onMouseEnter={e => e.currentTarget.style.background = '#f5f5f5'}
                  onMouseLeave={e => e.currentTarget.style.background = 'transparent'}
                >
                  <List.Item.Meta
                    avatar={getIcon(item.type)}
                    title={
                      <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                        {getTypeTag(item.type)}
                        <span>{item.title}</span>
                      </div>
                    }
                    description={<Text type="secondary" ellipsis>{item.description}</Text>}
                  />
                </List.Item>
              )}
            />
          ) : query ? (
            <div style={{ textAlign: 'center', padding: 40, color: '#bfbfbf' }}>未找到相关资产</div>
          ) : (
            <div style={{ textAlign: 'center', padding: 40, color: '#bfbfbf' }}>输入内容并按回车搜索</div>
          )}
        </div>
      </Modal>
    </>
  )
}

export default GlobalSearch
