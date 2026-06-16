/**
 * API Token 管理页面
 *
 * 展示 Token 列表，支持创建（一次性显示 Token 值）、删除操作。
 */
import { useState, useEffect, useCallback } from 'react'
import {
  Card,
  Table,
  Button,
  Modal,
  Input,
  Select,
  Form,
  message,
  Space,
  Typography,
  Tag,
  Popconfirm,
  Empty,
  Alert,
  Tooltip,
} from 'antd'
import {
  PlusOutlined,
  DeleteOutlined,
  CopyOutlined,
  KeyOutlined,
  ExclamationCircleOutlined,
} from '@ant-design/icons'
import { useTranslation } from 'react-i18next'
import type { ColumnsType } from 'antd/es/table'
import tokenService, { ApiToken, CreateTokenResponse } from '@/services/tokenService'

const { Title, Text, Paragraph } = Typography

const VALID_ACTIONS = ['read', 'write', 'execute', 'delete']

const ApiTokens = () => {
  const { t } = useTranslation()
  const [tokens, setTokens] = useState<ApiToken[]>([])
  const [total, setTotal] = useState(0)
  const [loading, setLoading] = useState(false)
  const [page, setPage] = useState(1)
  const [pageSize, setPageSize] = useState(20)
  const [createModalOpen, setCreateModalOpen] = useState(false)
  const [createLoading, setCreateLoading] = useState(false)
  const [newTokenResult, setNewTokenResult] = useState<CreateTokenResponse | null>(null)
  const [tokenRevealed, setTokenRevealed] = useState(false)

  // 创建表单状态
  const [formName, setFormName] = useState('')
  const [formActions, setFormActions] = useState<string[]>(['read'])
  const [formProjectIds, setFormProjectIds] = useState<string>('')
  const [formExpiresDays, setFormExpiresDays] = useState<number | null>(null)

  const fetchTokens = useCallback(async () => {
    setLoading(true)
    try {
      const res = await tokenService.getTokens({ page, per_page: pageSize })
      if (res.code === 200 && res.data) {
        setTokens(res.data.items || [])
        setTotal(res.data.pagination?.total || 0)
      }
    } catch {
      message.error(t('tokens.fetchFailed'))
    } finally {
      setLoading(false)
    }
  }, [page, pageSize, t])

  useEffect(() => {
    fetchTokens()
  }, [fetchTokens])

  const handleCreate = async () => {
    if (!formName.trim()) return
    setCreateLoading(true)
    try {
      const projectIds = formProjectIds
        .split(',')
        .map((s) => parseInt(s.trim(), 10))
        .filter((n) => !isNaN(n) && n > 0)

      const res = await tokenService.createToken({
        name: formName.trim(),
        actions: formActions,
        project_ids: projectIds,
        expires_in_days: formExpiresDays,
      })
      if ((res.code === 200 || res.code === 201) && res.data) {
        message.success(t('tokens.createSuccess'))
        setNewTokenResult(res.data)
        setTokenRevealed(true)
        setCreateModalOpen(false)
        resetForm()
        await fetchTokens()
      } else {
        message.error(res.message || t('tokens.createFailed'))
      }
    } catch {
      message.error(t('tokens.createFailed'))
    } finally {
      setCreateLoading(false)
    }
  }

  const handleDelete = async (tokenId: number) => {
    try {
      const res = await tokenService.deleteToken(tokenId)
      if (res.code === 200) {
        message.success(t('tokens.deleteSuccess'))
        await fetchTokens()
      } else {
        message.error(res.message || t('tokens.deleteFailed'))
      }
    } catch {
      message.error(t('tokens.deleteFailed'))
    }
  }

  const resetForm = () => {
    setFormName('')
    setFormActions(['read'])
    setFormProjectIds('')
    setFormExpiresDays(null)
  }

  const copyToClipboard = (text: string) => {
    navigator.clipboard.writeText(text).then(() => {
      message.success(t('tokens.copied'))
    })
  }

  const columns: ColumnsType<ApiToken> = [
    {
      title: t('common.name'),
      dataIndex: 'name',
      key: 'name',
      render: (name: string) => <span style={{ fontWeight: 500 }}>{name}</span>,
    },
    {
      title: t('tokens.actions'),
      dataIndex: 'actions',
      key: 'actions',
      render: (actions: string[]) => (
        <Space size={4} wrap>
          {(actions || []).map((action) => (
            <Tag key={action} color="blue">{action}</Tag>
          ))}
        </Space>
      ),
    },
    {
      title: t('tokens.projectScope'),
      dataIndex: 'project_ids',
      key: 'project_ids',
      render: (ids: number[]) => {
        if (!ids || ids.length === 0) return <Tag>{t('tokens.allProjects')}</Tag>
        return (
          <Space size={4} wrap>
            {ids.map((id) => <Tag key={id}>#{id}</Tag>)}
          </Space>
        )
      },
    },
    {
      title: t('tokens.expiresAt'),
      dataIndex: 'expires_at',
      key: 'expires_at',
      width: 180,
      render: (val: string | null) => {
        if (!val) return <Tag>{t('tokens.neverExpires')}</Tag>
        const date = new Date(val)
        const isExpired = date < new Date()
        return (
          <Tag color={isExpired ? 'red' : 'default'}>
            {date.toLocaleString()}
          </Tag>
        )
      },
    },
    {
      title: t('common.createdAt'),
      dataIndex: 'created_at',
      key: 'created_at',
      width: 180,
      render: (val: string) => (val ? new Date(val).toLocaleString() : '-'),
    },
    {
      title: t('common.actions'),
      key: 'actions',
      width: 100,
      render: (_: unknown, record: ApiToken) => (
        <Popconfirm
          title={t('tokens.deleteConfirm')}
          onConfirm={() => handleDelete(record.id)}
          okText={t('common.confirm')}
          cancelText={t('common.cancel')}
        >
          <Button type="link" size="small" danger icon={<DeleteOutlined />}>
            {t('common.delete')}
          </Button>
        </Popconfirm>
      ),
    },
  ]

  return (
    <div style={{ padding: 0 }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 16 }}>
        <Title level={4} style={{ margin: 0 }}>
          <KeyOutlined style={{ marginRight: 8 }} />
          {t('tokens.title')}
        </Title>
        <Button
          type="primary"
          icon={<PlusOutlined />}
          onClick={() => {
            resetForm()
            setCreateModalOpen(true)
          }}
        >
          {t('tokens.create')}
        </Button>
      </div>

      {/* Token 创建成功提示 */}
      {tokenRevealed && newTokenResult && (
        <Alert
          type="warning"
          showIcon
          icon={<ExclamationCircleOutlined />}
          message={t('tokens.tokenRevealedTitle')}
          description={
            <div>
              <Paragraph style={{ marginBottom: 8 }}>{t('tokens.tokenRevealedDesc')}</Paragraph>
              <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 8 }}>
                <Input
                  readOnly
                  value={newTokenResult.token}
                  style={{ fontFamily: 'monospace', flex: 1 }}
                />
                <Tooltip title={t('common.copy')}>
                  <Button
                    icon={<CopyOutlined />}
                    onClick={() => copyToClipboard(newTokenResult.token)}
                  />
                </Tooltip>
              </div>
              <Button size="small" onClick={() => { setTokenRevealed(false); setNewTokenResult(null) }}>
                {t('common.close')}
              </Button>
            </div>
          }
          closable={false}
          style={{ marginBottom: 16 }}
        />
      )}

      <Card>
        <Table
          columns={columns}
          dataSource={tokens}
          rowKey="id"
          loading={loading}
          locale={{ emptyText: <Empty description={t('tokens.noTokens')} /> }}
          pagination={{
            current: page,
            pageSize,
            total,
            showSizeChanger: true,
            showTotal: (totalVal) => `${totalVal} ${t('common.count')}`,
            onChange: (p, ps) => {
              setPage(p)
              setPageSize(ps)
            },
          }}
        />
      </Card>

      {/* 创建 Token 弹窗 */}
      <Modal
        title={t('tokens.create')}
        open={createModalOpen}
        onCancel={() => setCreateModalOpen(false)}
        onOk={handleCreate}
        confirmLoading={createLoading}
        okText={t('common.confirm')}
        cancelText={t('common.cancel')}
        destroyOnHidden
      >
        <div style={{ display: 'flex', flexDirection: 'column', gap: 16, marginTop: 8 }}>
          <div>
            <div style={{ marginBottom: 6, fontWeight: 500, fontSize: 13 }}>{t('common.name')}</div>
            <Input
              placeholder={t('tokens.namePlaceholder')}
              value={formName}
              onChange={(e) => setFormName(e.target.value)}
              maxLength={100}
              autoFocus
            />
          </div>
          <div>
            <div style={{ marginBottom: 6, fontWeight: 500, fontSize: 13 }}>{t('tokens.permissions')}</div>
            <Select
              mode="multiple"
              value={formActions}
              onChange={setFormActions}
              style={{ width: '100%' }}
              options={VALID_ACTIONS.map((a) => ({
                value: a,
                label: a.charAt(0).toUpperCase() + a.slice(1),
              }))}
            />
          </div>
          <div>
            <div style={{ marginBottom: 6, fontWeight: 500, fontSize: 13 }}>
              {t('tokens.projectScope')}
              <Text type="secondary" style={{ fontSize: 12, marginLeft: 8 }}>
                {t('tokens.projectScopeHint')}
              </Text>
            </div>
            <Input
              placeholder={t('tokens.projectIdsPlaceholder')}
              value={formProjectIds}
              onChange={(e) => setFormProjectIds(e.target.value)}
            />
          </div>
        </div>
      </Modal>
    </div>
  )
}

export default ApiTokens
