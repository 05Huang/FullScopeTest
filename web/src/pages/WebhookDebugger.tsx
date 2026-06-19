import { useState, useEffect, useCallback } from 'react'
import { Card, Button, Table, Space, Typography, Tag, message, Empty, Modal, Descriptions, Tooltip, Badge, Spin } from 'antd'
import { PlusOutlined, CopyOutlined, DeleteOutlined, EyeOutlined, ReloadOutlined, LinkOutlined } from '@ant-design/icons'
import { useTranslation } from 'react-i18next'
import type { ColumnsType } from 'antd/es/table'
import webhookDebuggerService, { WebhookSession, WebhookRequest } from '@/services/webhookDebuggerService'

const { Title, Text } = Typography
const METHOD_COLORS: Record<string, string> = { GET: 'green', POST: 'blue', PUT: 'orange', DELETE: 'red', PATCH: 'purple' };

const WebhookDebugger = () => {
  const { t } = useTranslation()
  const [loading, setLoading] = useState(true)
  const [sessions, setSessions] = useState<WebhookSession[]>([])
  const [selectedSession, setSelectedSession] = useState<WebhookSession | null>(null)
  const [requests, setRequests] = useState<WebhookRequest[]>([])
  const [requestsLoading, setRequestsLoading] = useState(false)
  const [detailModalOpen, setDetailModalOpen] = useState(false)
  const [selectedRequest, setSelectedRequest] = useState<WebhookRequest | null>(null)

  const loadSessions = useCallback(async () => {
    setLoading(true)
    try { const res = await webhookDebuggerService.getSessions(); if (res.code === 200) setSessions(res.data || []) } catch {} finally { setLoading(false) }
  }, [])
  useEffect(() => { loadSessions() }, [loadSessions])

  const handleCreateSession = async () => {
    try {
      const res = await webhookDebuggerService.createSession()
      if (res.code === 200 || res.code === 201) { message.success(t('webhookDebugger.createSuccess')); await loadSessions(); if (res.data) setSelectedSession(res.data) }
      else message.error(res.message || t('webhookDebugger.createFailed'))
    } catch { message.error(t('webhookDebugger.createFailed')) }
  };
  const loadRequests = async (session: WebhookSession) => {
    setSelectedSession(session); setRequestsLoading(true)
    try { const res = await webhookDebuggerService.getRequests(session.token); if (res.code === 200) setRequests(res.data || []) } catch {} finally { setRequestsLoading(false) }
  };
  const handleClearRequests = async () => {
    if (!selectedSession) return
    try {
      const res = await webhookDebuggerService.clearRequests(selectedSession.token)
      if (res.code === 200) { message.success(t('webhookDebugger.clearSuccess')); setRequests([]) }
      else message.error(res.message || t('webhookDebugger.clearFailed'))
    } catch { message.error(t('webhookDebugger.clearFailed')) }
  };
  const handleCopyUrl = (url: string) => {
    navigator.clipboard.writeText(url).then(() => message.success(t('webhookDebugger.copied'))).catch(() => {
      const ta = document.createElement('textarea'); ta.value = url; document.body.appendChild(ta); ta.select(); document.execCommand('copy'); document.body.removeChild(ta); message.success(t('webhookDebugger.copied'))
    })
  };

  const requestColumns: ColumnsType<WebhookRequest> = [
    { title: t('webhookDebugger.method'), dataIndex: 'method', key: 'method', width: 80, render: (v: string) => <Tag color={METHOD_COLORS[v] || 'default'}>{v}</Tag> },
    { title: 'IP', dataIndex: 'source_ip', key: 'source_ip', width: 140, render: (v: string) => <Text code>{v}</Text> },
    { title: t('webhookDebugger.body'), dataIndex: 'body', key: 'body', ellipsis: true, render: (v: string) => <Text type='secondary' style={{ fontSize: 12 }}>{v ? v.slice(0, 80) : ''}</Text> },
    { title: t('webhookDebugger.time'), dataIndex: 'received_at', key: 'time', width: 160, render: (v: string) => new Date(v).toLocaleString() },
    { title: '', key: 'actions', width: 60, render: (_: unknown, record: WebhookRequest) => <Button size='small' icon={<EyeOutlined />} onClick={() => { setSelectedRequest(record); setDetailModalOpen(true) }} /> },
  ];

  return (
    <div style={{ padding: 24 }}>
      <div style={{ marginBottom: 24, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <div>
          <Title level={3} style={{ marginBottom: 4 }}>{t('webhookDebugger.title')}</Title>
          <Text type='secondary'>{t('webhookDebugger.subtitle')}</Text>
        </div>
        <Button type='primary' icon={<PlusOutlined />} onClick={handleCreateSession}>{t('webhookDebugger.createSession')}</Button>
      </div>
      <div style={{ display: 'flex', gap: 16 }}>
        <Card style={{ width: 320, flexShrink: 0 }} title={t('webhookDebugger.title')} extra={<Button size='small' icon={<ReloadOutlined />} onClick={loadSessions} />}>
          {sessions.length === 0 ? <Empty description={t('webhookDebugger.noSessions')} /> : (
            <Space direction='vertical' style={{ width: '100%' }}>
              {sessions.map(session => (
                <Card key={session.token} size='small' hoverable style={{ borderColor: selectedSession?.token === session.token ? 'var(--fst-primary)' : undefined }} onClick={() => loadRequests(session)}>
                  <Space>
                    <Badge status={session.is_active ? 'success' : 'default'} />
                    <Text code style={{ fontSize: 11 }}>{session.token.substring(0, 8)}...</Text>
                    <Text type='secondary'>{session.request_count} req</Text>
                  </Space>
                </Card>
              ))}
            </Space>
          )}
        </Card>
        <Card style={{ flex: 1 }} title={selectedSession ? <Space><LinkOutlined /><Text copyable={{ text: selectedSession.webhook_url }}>{t('webhookDebugger.webhookUrl')}</Text></Space> : t('webhookDebugger.requests')}
          extra={selectedSession && (<Space>
            <Button size='small' icon={<CopyOutlined />} onClick={() => handleCopyUrl(selectedSession.webhook_url)}>{t('webhookDebugger.copyUrl')}</Button>
            <Button size='small' danger icon={<DeleteOutlined />} onClick={handleClearRequests}>{t('webhookDebugger.clearHistory')}</Button>
            <Button size='small' icon={<ReloadOutlined />} onClick={() => loadRequests(selectedSession)} />
          </Space>)}
        >
          {!selectedSession ? <Empty description={t('webhookDebugger.noRequests')} /> : <Table columns={requestColumns} dataSource={requests} rowKey='id' loading={requestsLoading} size='small' pagination={{ pageSize: 20 }} />}
        </Card>
      </div>
      <Modal title={t('webhookDebugger.requests')} open={detailModalOpen} onCancel={() => setDetailModalOpen(false)} footer={null} width={700}>
        {selectedRequest && (
          <Descriptions column={1} bordered size='small'>
            <Descriptions.Item label={t('webhookDebugger.method')}><Tag color={METHOD_COLORS[selectedRequest.method]}>{selectedRequest.method}</Tag></Descriptions.Item>
            <Descriptions.Item label='IP'><Text code>{selectedRequest.source_ip}</Text></Descriptions.Item>
            <Descriptions.Item label={t('webhookDebugger.time')}>{new Date(selectedRequest.received_at).toLocaleString()}</Descriptions.Item>
            <Descriptions.Item label={t('webhookDebugger.headers')}><pre style={{ maxHeight: 200, overflow: 'auto', fontSize: 12, background: '#f5f5f5', padding: 8, borderRadius: 4 }}>{JSON.stringify(selectedRequest.headers, null, 2)}</pre></Descriptions.Item>
            <Descriptions.Item label={t('webhookDebugger.body')}><pre style={{ maxHeight: 300, overflow: 'auto', fontSize: 12, background: '#f5f5f5', padding: 8, borderRadius: 4 }}>{(() => { try { return JSON.stringify(JSON.parse(selectedRequest.body), null, 2) } catch { return selectedRequest.body } })()}</pre></Descriptions.Item>
          </Descriptions>
        )}
      </Modal>
    </div>
  )
}

export default WebhookDebugger
