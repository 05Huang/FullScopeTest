/**
 * AI 用例自愈修复建议抽屉组件
 *
 * 展示 AI 分析的失败原因和修复建议，支持一键应用修复。
 * 修复前展示 Diff 对比，用户确认后应用。
 */
import { useState, useCallback, useEffect } from 'react'
import {
  Drawer,
  Button,
  Space,
  Typography,
  Tag,
  Alert,
  List,
  Spin,
  Empty,
  Divider,
  Descriptions,
  Progress,
  Checkbox,
  message,
} from 'antd'
import {
  MedicineBoxOutlined,
  CheckCircleOutlined,
  ExclamationCircleOutlined,
  ExperimentOutlined,
  SwapOutlined,
} from '@ant-design/icons'
import { useTranslation } from 'react-i18next'
import {
  healTestCase,
  applyHealFix,
  type HealSuggestion,
} from '@/services/apiTestService'

const { Text, Title, Paragraph } = Typography

/** 失败原因中文映射 */
const failureReasonLabels: Record<string, { label: string; color: string }> = {
  path_changed: { label: '接口路径变更', color: 'red' },
  field_missing: { label: '字段缺失', color: 'orange' },
  status_changed: { label: '状态码变更', color: 'gold' },
  auth_expired: { label: '认证过期', color: 'purple' },
  timeout: { label: '超时', color: 'volcano' },
  server_error: { label: '服务端错误', color: 'magenta' },
  data_format: { label: '数据格式错误', color: 'cyan' },
  unknown: { label: '未知原因', color: 'default' },
}

interface HealSuggestionDrawerProps {
  open: boolean
  onClose: () => void
  caseId: number | null
  failureInfo?: Record<string, unknown>
  onApplied?: () => void
}

const HealSuggestionDrawer = ({
  open,
  onClose,
  caseId,
  failureInfo = {},
  onApplied,
}: HealSuggestionDrawerProps) => {
  const { t } = useTranslation()
  const [loading, setLoading] = useState(false)
  const [applying, setApplying] = useState(false)
  const [suggestion, setSuggestion] = useState<HealSuggestion | null>(null)
  const [selectedFixes, setSelectedFixes] = useState<number[]>([])

  const fetchSuggestion = useCallback(async () => {
    if (!caseId) return
    setLoading(true)
    setSuggestion(null)
    try {
      const res = await healTestCase({
        case_id: caseId,
        failure_info: failureInfo,
      })
      if (res.data) {
        setSuggestion(res.data)
        // 默认全选
        setSelectedFixes(res.data.fixes.map((_, i) => i))
      }
    } catch {
      message.error(t('heal.error'))
    } finally {
      setLoading(false)
    }
  }, [caseId, failureInfo, t])

  useEffect(() => {
    if (open && caseId) {
      fetchSuggestion()
    }
  }, [open, caseId, fetchSuggestion])

  const handleApply = async () => {
    if (!suggestion || !caseId) return
    const fixesToApply = selectedFixes.map((i) => suggestion.fixes[i]).filter(Boolean)
    if (fixesToApply.length === 0) {
      message.warning(t('heal.selectFixes'))
      return
    }
    setApplying(true)
    try {
      const res = await applyHealFix({
        case_id: caseId,
        fixes: fixesToApply,
      })
      if (res.data) {
        message.success(t('heal.appliedSuccess'))
        onApplied?.()
        onClose()
      }
    } catch {
      message.error(t('heal.applyError'))
    } finally {
      setApplying(false)
    }
  }

  const reasonInfo = suggestion?.failure_reason
    ? failureReasonLabels[suggestion.failure_reason] || failureReasonLabels.unknown
    : null

  return (
    <Drawer
      title={
        <Space>
          <MedicineBoxOutlined style={{ color: '#52c41a' }} />
          {t('heal.title')}
        </Space>
      }
      open={open}
      onClose={onClose}
      width={560}
      extra={
        <Space>
          <Button onClick={onClose}>{t('common.cancel')}</Button>
          <Button
            type="primary"
            icon={<CheckCircleOutlined />}
            onClick={handleApply}
            loading={applying}
            disabled={!suggestion || suggestion.fixes.length === 0 || selectedFixes.length === 0}
          >
            {t('heal.applyFix')}
          </Button>
        </Space>
      }
    >
      {loading && (
        <div style={{ textAlign: 'center', padding: '60px 0' }}>
          <Spin size="large" />
          <Paragraph style={{ marginTop: 16 }}>{t('heal.analyzing')}</Paragraph>
        </div>
      )}

      {!loading && suggestion && (
        <>
          {/* 失败分析 */}
          <Descriptions
            column={1}
            size="small"
            title={
              <Space>
                <ExclamationCircleOutlined style={{ color: '#faad14' }} />
                {t('heal.analysis')}
              </Space>
            }
            style={{ marginBottom: 16 }}
          >
            <Descriptions.Item label={t('heal.failureReason')}>
              {reasonInfo && (
                <Tag color={reasonInfo.color}>{reasonInfo.label}</Tag>
              )}
            </Descriptions.Item>
            <Descriptions.Item label={t('heal.confidence')}>
              <Progress
                percent={Math.round((suggestion.confidence || 0) * 100)}
                size="small"
                status={suggestion.confidence >= 0.7 ? 'success' : 'normal'}
                style={{ width: 200 }}
              />
            </Descriptions.Item>
          </Descriptions>

          {/* 分析详情 */}
          <Alert
            message={t('heal.aiAnalysis')}
            description={suggestion.analysis}
            type="info"
            showIcon
            icon={<ExperimentOutlined />}
            style={{ marginBottom: 16 }}
          />

          {/* 修复建议 Diff */}
          <Divider orientation="left">
            <Space>
              <SwapOutlined />
              {t('heal.fixSuggestions')} ({suggestion.fixes.length})
            </Space>
          </Divider>

          {suggestion.fixes.length === 0 ? (
            <Empty description={t('heal.noFixes')} />
          ) : (
            <List
              size="small"
              dataSource={suggestion.fixes}
              renderItem={(fix, index) => {
                const isSelected = selectedFixes.includes(index)
                return (
                  <List.Item
                    style={{
                      background: isSelected ? '#f6ffed' : '#fafafa',
                      borderRadius: 6,
                      padding: '10px 12px',
                      marginBottom: 6,
                      border: isSelected ? '1px solid #b7eb8f' : '1px solid #e8e8e8',
                    }}
                  >
                    <div style={{ width: '100%' }}>
                      <div style={{ display: 'flex', alignItems: 'center', marginBottom: 8 }}>
                        <Checkbox
                          checked={isSelected}
                          onChange={() =>
                            setSelectedFixes((prev) =>
                              isSelected
                                ? prev.filter((i) => i !== index)
                                : [...prev, index]
                            )
                          }
                          style={{ marginRight: 8 }}
                        />
                        <Tag color="blue">{fix.field}</Tag>
                        <Text type="secondary" style={{ fontSize: 12, marginLeft: 'auto' }}>
                          {fix.reason}
                        </Text>
                      </div>
                      {/* Diff 对比 */}
                      <div
                        style={{
                          display: 'grid',
                          gridTemplateColumns: '1fr 1fr',
                          gap: 8,
                          marginLeft: 24,
                        }}
                      >
                        <div
                          style={{
                            background: '#fff1f0',
                            borderRadius: 4,
                            padding: '6px 8px',
                            fontFamily: 'monospace',
                            fontSize: 12,
                            wordBreak: 'break-all',
                          }}
                        >
                          <Text type="secondary" style={{ fontSize: 11 }}>
                            {t('heal.current')}
                          </Text>
                          <div>{fix.current || '(空)'}</div>
                        </div>
                        <div
                          style={{
                            background: '#f6ffed',
                            borderRadius: 4,
                            padding: '6px 8px',
                            fontFamily: 'monospace',
                            fontSize: 12,
                            wordBreak: 'break-all',
                          }}
                        >
                          <Text type="secondary" style={{ fontSize: 11 }}>
                            {t('heal.suggested')}
                          </Text>
                          <div>{fix.suggested || '(空)'}</div>
                        </div>
                      </div>
                    </div>
                  </List.Item>
                )
              }}
            />
          )}

          {/* 自动修复提示 */}
          {suggestion.can_auto_apply && (
            <Alert
              message={t('heal.canAutoApply')}
              type="success"
              showIcon
              style={{ marginTop: 16 }}
            />
          )}
        </>
      )}

      {!loading && !suggestion && (
        <Empty description={t('heal.emptyHint')} style={{ padding: '60px 0' }} />
      )}
    </Drawer>
  )
}

export default HealSuggestionDrawer