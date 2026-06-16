/**
 * 语义去重结果弹窗
 *
 * 展示 AI 语义去重结果，支持批量选择和删除重复用例。
 */
import { useState } from 'react'
import {
  Modal,
  Table,
  Button,
  Checkbox,
  Tag,
  Space,
  Typography,
  message,
  Empty,
  Progress,
} from 'antd'
import { DeleteOutlined, CheckCircleOutlined } from '@ant-design/icons'
import { useTranslation } from 'react-i18next'

const { Text } = Typography

interface DuplicateGroup {
  cases: Array<{ id: number; name: string; method?: string; url?: string }>
  similarity: number
  recommended_keep_id?: number
}

interface DedupResultModalProps {
  open: boolean
  onClose: () => void
  results: DuplicateGroup[] | null
  loading: boolean
  onDelete?: (caseIds: number[]) => Promise<void>
}

const DedupResultModal = ({ open, onClose, results, loading, onDelete }: DedupResultModalProps) => {
  const { t } = useTranslation()
  const [selectedIds, setSelectedIds] = useState<Set<number>>(new Set())
  const [deleteLoading, setDeleteLoading] = useState(false)

  const toggleSelect = (caseId: number) => {
    setSelectedIds((prev) => {
      const next = new Set(prev)
      if (next.has(caseId)) next.delete(caseId)
      else next.add(caseId)
      return next
    })
  }

  const selectAllDuplicates = () => {
    if (!results) return
    const ids = new Set<number>()
    results.forEach((group) => {
      group.cases.forEach((c) => {
        if (c.id !== group.recommended_keep_id) {
          ids.add(c.id)
        }
      })
    })
    setSelectedIds(ids)
  }

  const handleDelete = async () => {
    if (!onDelete || selectedIds.size === 0) return
    setDeleteLoading(true)
    try {
      await onDelete(Array.from(selectedIds))
      message.success(t('apiTest.dedup.deleteSuccess', { count: selectedIds.size }))
      setSelectedIds(new Set())
      onClose()
    } catch {
      message.error(t('apiTest.dedup.deleteFailed'))
    } finally {
      setDeleteLoading(false)
    }
  }

  const columns = [
    {
      title: '',
      key: 'select',
      width: 40,
      render: (_: any, record: any) => (
        <Checkbox
          checked={selectedIds.has(record.id)}
          onChange={() => toggleSelect(record.id)}
        />
      ),
    },
    {
      title: t('common.name'),
      dataIndex: 'name',
      key: 'name',
      render: (name: string, record: any) => (
        <Space>
          {record.id === record._recommended_keep_id && (
            <Tag color="green" style={{ fontSize: 11 }}>{t('apiTest.dedup.recommended')}</Tag>
          )}
          <Text>{name}</Text>
        </Space>
      ),
    },
    {
      title: 'Method',
      dataIndex: 'method',
      key: 'method',
      width: 80,
      render: (m: string) => m ? <Tag>{m}</Tag> : '-',
    },
    {
      title: 'URL',
      dataIndex: 'url',
      key: 'url',
      ellipsis: true,
    },
  ]

  return (
    <Modal
      title={t('apiTest.dedup.title')}
      open={open}
      onCancel={onClose}
      width={720}
      footer={
        <Space>
          <Button onClick={onClose}>{t('common.close')}</Button>
          {results && results.length > 0 && onDelete && (
            <>
              <Button onClick={selectAllDuplicates}>
                {t('apiTest.dedup.selectAllDuplicates')}
              </Button>
              <Button
                type="primary"
                danger
                icon={<DeleteOutlined />}
                onClick={handleDelete}
                loading={deleteLoading}
                disabled={selectedIds.size === 0}
              >
                {t('apiTest.dedup.deleteSelected')} ({selectedIds.size})
              </Button>
            </>
          )}
        </Space>
      }
      destroyOnHidden
    >
      {loading ? (
        <div style={{ textAlign: 'center', padding: 48 }}>
          <Text type="secondary">{t('apiTest.dedup.analyzing')}</Text>
        </div>
      ) : !results || results.length === 0 ? (
        <Empty description={t('apiTest.dedup.noDuplicates')} />
      ) : (
        <div>
          <div style={{ marginBottom: 16 }}>
            <Text type="secondary">
              {t('apiTest.dedup.foundGroups', { count: results.length })}
            </Text>
          </div>
          {results.map((group, groupIdx) => (
            <div
              key={groupIdx}
              style={{
                marginBottom: 16,
                border: '1px solid #f0f0f0',
                borderRadius: 8,
                overflow: 'hidden',
              }}
            >
              <div style={{ padding: '8px 12px', background: '#f6f8f8', display: 'flex', alignItems: 'center', gap: 8 }}>
                <Text strong style={{ fontSize: 13 }}>
                  {t('apiTest.dedup.group')} #{groupIdx + 1}
                </Text>
                <Progress
                  percent={Math.round(group.similarity * 100)}
                  size="small"
                  style={{ width: 120 }}
                  strokeColor="#D4B483"
                />
                <Text type="secondary" style={{ fontSize: 12 }}>
                  {t('apiTest.dedup.similarity')}
                </Text>
              </div>
              <Table
                columns={columns}
                dataSource={group.cases.map((c) => ({
                  ...c,
                  _recommended_keep_id: group.recommended_keep_id,
                }))}
                rowKey="id"
                pagination={false}
                size="small"
              />
            </div>
          ))}
        </div>
      )}
    </Modal>
  )
}

export default DedupResultModal
