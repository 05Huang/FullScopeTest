/**
 * 智能测试选择组件
 *
 * 根据变更文件列表智能推荐需要执行的测试用例。
 * 支持手动输入变更文件、从 Git commit 导入、按标签过滤。
 */
import { useState, useCallback } from 'react'
import {
  Drawer,
  Button,
  Input,
  Space,
  Typography,
  Tag,
  List,
  Checkbox,
  Progress,
  Alert,
  Spin,
  Empty,
  Divider,
  Tooltip,
  message,
} from 'antd'
import {
  ThunderboltOutlined,
  FileOutlined,
  CheckCircleOutlined,
  ClockCircleOutlined,
  RocketOutlined,
  ReloadOutlined,
} from '@ant-design/icons'
import { useTranslation } from 'react-i18next'
import {
  smartTestSelect,
  type SmartSelectResult,
} from '@/services/apiTestService'

const { Text, Title, Paragraph } = Typography
const { TextArea } = Input

interface SmartTestSelectorProps {
  open: boolean
  onClose: () => void
  onExecute: (caseIds: number[]) => void
  projectId?: number
}

/** 优先级颜色映射 */
const priorityColors: Record<string, string> = {
  p0: '#C75450',
  p1: '#D4B483',
  p2: '#5B8FB9',
  p3: '#629B95',
}

/** HTTP 方法颜色 */
const methodColors: Record<string, string> = {
  GET: '#61affe',
  POST: '#49cc90',
  PUT: '#fca130',
  DELETE: '#f93e3e',
  PATCH: '#50e3c2',
}

const SmartTestSelector = ({
  open,
  onClose,
  onExecute,
  projectId,
}: SmartTestSelectorProps) => {
  const { t } = useTranslation()
  const [fileInput, setFileInput] = useState('')
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState<SmartSelectResult | null>(null)
  const [selectedIds, setSelectedIds] = useState<number[]>([])

  const handleSelect = useCallback(async () => {
    const files = fileInput
      .split('\n')
      .map((f) => f.trim())
      .filter(Boolean)
    if (files.length === 0) {
      message.warning(t('smartSelect.enterFiles'))
      return
    }
    setLoading(true)
    try {
      const res = await smartTestSelect({
        changed_files: files,
        project_id: projectId,
        max_cases: 50,
      })
      if (res.data) {
        setResult(res.data)
        // 默认全选
        const ids = res.data.cases.map((item) => item.case?.id).filter(Boolean) as number[]
        setSelectedIds(ids)
      }
    } catch {
      message.error(t('smartSelect.error'))
    } finally {
      setLoading(false)
    }
  }, [fileInput, projectId, t])

  const handleExecute = () => {
    if (selectedIds.length === 0) {
      message.warning(t('smartSelect.selectCases'))
      return
    }
    onExecute(selectedIds)
    onClose()
  }

  const handleToggleAll = (checked: boolean) => {
    if (checked && result) {
      setSelectedIds(result.cases.map((item) => item.case?.id).filter(Boolean) as number[])
    } else {
      setSelectedIds([])
    }
  }

  return (
    <Drawer
      title={
        <Space>
          <ThunderboltOutlined style={{ color: '#1677ff' }} />
          {t('smartSelect.title')}
        </Space>
      }
      open={open}
      onClose={onClose}
      width={640}
      extra={
        <Space>
          <Button onClick={onClose}>{t('common.cancel')}</Button>
          <Button
            type="primary"
            icon={<RocketOutlined />}
            onClick={handleExecute}
            disabled={!result || selectedIds.length === 0}
          >
            {t('smartSelect.execute', { count: selectedIds.length })}
          </Button>
        </Space>
      }
    >
      {/* 输入区域 */}
      <div style={{ marginBottom: 16 }}>
        <Text strong style={{ display: 'block', marginBottom: 8 }}>
          {t('smartSelect.inputLabel')}
        </Text>
        <TextArea
          rows={5}
          placeholder={t('smartSelect.inputPlaceholder')}
          value={fileInput}
          onChange={(e) => setFileInput(e.target.value)}
          style={{ fontFamily: 'monospace', fontSize: 13 }}
        />
        <Space style={{ marginTop: 8 }}>
          <Button
            type="primary"
            icon={<ThunderboltOutlined />}
            onClick={handleSelect}
            loading={loading}
          >
            {t('smartSelect.analyze')}
          </Button>
          <Button
            icon={<ReloadOutlined />}
            onClick={() => {
              setFileInput('')
              setResult(null)
              setSelectedIds([])
            }}
          >
            {t('common.reset')}
          </Button>
        </Space>
      </div>

      <Divider />

      {/* 结果区域 */}
      {loading && (
        <div style={{ textAlign: 'center', padding: '40px 0' }}>
          <Spin size="large" />
          <Paragraph style={{ marginTop: 16 }}>{t('smartSelect.analyzing')}</Paragraph>
        </div>
      )}

      {!loading && result && (
        <>
          {/* 智能选测理由 */}
          <Alert
            message={t('smartSelect.reasoning')}
            description={result.reasoning}
            type="info"
            showIcon
            style={{ marginBottom: 16 }}
          />

          {/* 统计信息 */}
          <Space style={{ marginBottom: 16 }} wrap>
            <Tag icon={<FileOutlined />} color="blue">
              {t('smartSelect.affectedPaths', { count: result.affected_paths.length })}
            </Tag>
            <Tag icon={<CheckCircleOutlined />} color="green">
              {t('smartSelect.casesFound', { count: result.cases.length })}
            </Tag>
            <Tag icon={<ClockCircleOutlined />} color="orange">
              {t('smartSelect.estimatedTime', {
                time: Math.round(result.total_estimated_time / 60),
              })}
            </Tag>
          </Space>

          {/* 全选 */}
          <div style={{ marginBottom: 8 }}>
            <Checkbox
              checked={selectedIds.length === result.cases.length}
              indeterminate={selectedIds.length > 0 && selectedIds.length < result.cases.length}
              onChange={(e) => handleToggleAll(e.target.checked)}
            >
              <Text type="secondary">
                {t('smartSelect.selectAll')} ({selectedIds.length}/{result.cases.length})
              </Text>
            </Checkbox>
          </div>

          {/* 用例列表 */}
          <List
            size="small"
            dataSource={result.cases}
            renderItem={(item, index) => {
              const c = item.case as Record<string, unknown>
              const caseId = c.id as number
              const method = (c.method as string) || 'GET'
              const isSelected = selectedIds.includes(caseId)
              return (
                <List.Item
                  style={{
                    background: isSelected ? '#f0f5ff' : undefined,
                    borderRadius: 6,
                    padding: '8px 12px',
                    marginBottom: 4,
                    border: isSelected ? '1px solid #91caff' : '1px solid transparent',
                  }}
                >
                  <div style={{ display: 'flex', alignItems: 'center', width: '100%', gap: 8 }}>
                    <Checkbox
                      checked={isSelected}
                      onChange={() => {
                        setSelectedIds((prev) =>
                          isSelected ? prev.filter((id) => id !== caseId) : [...prev, caseId]
                        )
                      }}
                    />
                    <Tag
                      color={methodColors[method] || '#999'}
                      style={{ fontFamily: 'monospace', minWidth: 50, textAlign: 'center' }}
                    >
                      {method}
                    </Tag>
                    <div style={{ flex: 1, minWidth: 0 }}>
                      <Tooltip title={c.name as string}>
                        <Text strong ellipsis style={{ display: 'block' }}>
                          {(index + 1)}. {c.name as string}
                        </Text>
                      </Tooltip>
                      <Text type="secondary" ellipsis style={{ fontSize: 12, display: 'block' }}>
                        {c.url as string}
                      </Text>
                    </div>
                    <div style={{ textAlign: 'right', flexShrink: 0 }}>
                      <Tag color={priorityColors[(c.priority as string)?.toLowerCase()] || undefined}>
                        {(c.priority as string) || 'P2'}
                      </Tag>
                      <Tooltip title={item.match_reason}>
                        <Tag color="purple" style={{ cursor: 'help' }}>
                          {item.match_reason}
                        </Tag>
                      </Tooltip>
                      {item.history_bonus && (
                        <Tooltip title={item.history_bonus}>
                          <Tag color="red" style={{ cursor: 'help' }}>
                            ⚠
                          </Tag>
                        </Tooltip>
                      )}
                    </div>
                  </div>
                </List.Item>
              )
            }}
          />
        </>
      )}

      {!loading && !result && (
        <Empty
          description={t('smartSelect.emptyHint')}
          style={{ padding: '40px 0' }}
        />
      )}
    </Drawer>
  )
}

export default SmartTestSelector