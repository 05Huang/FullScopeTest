/**
 * 用例版本历史抽屉
 *
 * 展示用例的版本历史列表，支持版本对比。
 */
import { useState, useEffect, useCallback } from 'react'
import {
  Drawer,
  List,
  Button,
  Tag,
  Space,
  Typography,
  Empty,
  Spin,
  Radio,
  message,
} from 'antd'
import { HistoryOutlined, SwapOutlined } from '@ant-design/icons'
import { useTranslation } from 'react-i18next'
import api from '@/services/api'

const { Text } = Typography

interface Version {
  id: number
  case_id: number
  version_number: number
  created_by: number
  created_at: string
  change_summary?: string
}

interface VersionHistoryDrawerProps {
  open: boolean
  onClose: () => void
  caseId: number
  caseName?: string
}

const VersionHistoryDrawer = ({ open, onClose, caseId, caseName }: VersionHistoryDrawerProps) => {
  const { t } = useTranslation()
  const [versions, setVersions] = useState<Version[]>([])
  const [loading, setLoading] = useState(false)
  const [selectedVersions, setSelectedVersions] = useState<number[]>([])
  const [diffResult, setDiffResult] = useState<any>(null)
  const [diffLoading, setDiffLoading] = useState(false)

  const fetchVersions = useCallback(async () => {
    if (!caseId) return
    setLoading(true)
    try {
      const res = await api.get(`/api-test/cases/${caseId}/versions`, {
        params: { per_page: 50 },
      })
      const data = (res as any)?.data || res
      setVersions(data?.items || data || [])
    } catch {
      // 静默失败
    } finally {
      setLoading(false)
    }
  }, [caseId])

  useEffect(() => {
    if (open) {
      fetchVersions()
      setSelectedVersions([])
      setDiffResult(null)
    }
  }, [open, fetchVersions])

  const toggleVersion = (versionId: number) => {
    setSelectedVersions((prev) => {
      if (prev.includes(versionId)) {
        return prev.filter((id) => id !== versionId)
      }
      if (prev.length >= 2) {
        return [prev[1], versionId]
      }
      return [...prev, versionId]
    })
  }

  const handleDiff = async () => {
    if (selectedVersions.length !== 2) return
    setDiffLoading(true)
    try {
      const res = await api.get('/api-test/versions/diff', {
        params: { v1: selectedVersions[0], v2: selectedVersions[1] },
      })
      const data = (res as any)?.data || res
      setDiffResult(data)
    } catch {
      message.error(t('apiTest.versions.diffFailed'))
    } finally {
      setDiffLoading(false)
    }
  }

  const renderDiffValue = (key: string, value: any, type: 'added' | 'removed' | 'changed') => {
    const colors = { added: '#f6ffed', removed: '#fff2f0', changed: '#fffbe6' }
    const borderColors = { added: '#2D6A64', removed: '#C75450', changed: '#D4B483' }
    return (
      <div
        key={key}
        style={{
          padding: '6px 10px',
          background: colors[type],
          borderLeft: `3px solid ${borderColors[type]}`,
          marginBottom: 4,
          fontSize: 12,
          fontFamily: 'monospace',
        }}
      >
        <Text strong style={{ fontSize: 12 }}>{key}: </Text>
        <Text style={{ fontSize: 12 }}>{typeof value === 'object' ? JSON.stringify(value) : String(value)}</Text>
      </div>
    )
  }

  return (
    <Drawer
      title={
        <Space>
          <HistoryOutlined />
          <span>{t('apiTest.versions.title')}</span>
          {caseName && <Tag>{caseName}</Tag>}
        </Space>
      }
      open={open}
      onClose={onClose}
      width={520}
      extra={
        selectedVersions.length === 2 && (
          <Button
            type="primary"
            icon={<SwapOutlined />}
            onClick={handleDiff}
            loading={diffLoading}
            size="small"
          >
            {t('apiTest.versions.compare')}
          </Button>
        )
      }
    >
      {loading ? (
        <div style={{ display: 'flex', justifyContent: 'center', padding: 48 }}>
          <Spin />
        </div>
      ) : versions.length === 0 ? (
        <Empty description={t('apiTest.versions.noVersions')} />
      ) : (
        <>
          <div style={{ marginBottom: 12, fontSize: 12, color: '#999' }}>
            {t('apiTest.versions.selectHint')}
          </div>
          <List
            dataSource={versions}
            renderItem={(version: Version) => (
              <List.Item
                style={{
                  cursor: 'pointer',
                  background: selectedVersions.includes(version.id) ? 'rgba(45, 106, 100, 0.08)' : undefined,
                  borderRadius: 8,
                  padding: '8px 12px',
                  marginBottom: 4,
                }}
                onClick={() => toggleVersion(version.id)}
              >
                <List.Item.Meta
                  title={
                    <Space>
                      <Text strong>v{version.version_number}</Text>
                      {selectedVersions.includes(version.id) && (
                        <Tag color="green">{selectedVersions.indexOf(version.id) === 0 ? 'V1' : 'V2'}</Tag>
                      )}
                    </Space>
                  }
                  description={
                    <Space direction="vertical" size={2}>
                      <Text type="secondary" style={{ fontSize: 12 }}>
                        {version.created_at ? new Date(version.created_at).toLocaleString() : '-'}
                        {version.created_by && ` · User #${version.created_by}`}
                      </Text>
                      {version.change_summary && (
                        <Text style={{ fontSize: 12 }}>{version.change_summary}</Text>
                      )}
                    </Space>
                  }
                />
              </List.Item>
            )}
          />

          {/* Diff 结果 */}
          {diffResult && (
            <div style={{ marginTop: 16, borderTop: '1px solid #f0f0f0', paddingTop: 16 }}>
              <Text strong style={{ marginBottom: 8, display: 'block' }}>
                {t('apiTest.versions.diffResult')}
              </Text>
              {diffResult.added && Object.keys(diffResult.added).map((k) =>
                renderDiffValue(k, diffResult.added[k], 'added')
              )}
              {diffResult.removed && Object.keys(diffResult.removed).map((k) =>
                renderDiffValue(k, diffResult.removed[k], 'removed')
              )}
              {diffResult.changed && Object.keys(diffResult.changed).map((k) =>
                renderDiffValue(k, diffResult.changed[k], 'changed')
              )}
              {diffResult.changes && Array.isArray(diffResult.changes) && diffResult.changes.map((c: any, i: number) =>
                renderDiffValue(c.field || `change_${i}`, c.new_value ?? c.value ?? c, 'changed')
              )}
            </div>
          )}
        </>
      )}
    </Drawer>
  )
}

export default VersionHistoryDrawer
