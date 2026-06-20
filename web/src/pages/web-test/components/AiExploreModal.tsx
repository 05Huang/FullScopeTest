import { useTranslation } from 'react-i18next'
import { Modal, Button, Space, Alert, Form, Input, Select, Card, Table, Tag, Typography } from 'antd'
import { GlobalOutlined } from '@ant-design/icons'

const { Text } = Typography
const { TextArea } = Input

interface ExploreHistoryItem {
  id: string
  started_at: string
  start_url: string
  objective: string
  max_steps: number
  report: Record<string, unknown>
  console_lines: string[]
}

interface AiExploreModalProps {
  open: boolean
  onClose: () => void
  exploring: boolean
  onExplore: () => void
  startUrl: string
  onStartUrlChange: (v: string) => void
  objective: string
  onObjectiveChange: (v: string) => void
  maxSteps: number
  onMaxStepsChange: (v: number) => void
  history: ExploreHistoryItem[]
  onClearHistory: () => void
  onViewResult: (report: Record<string, unknown>, consoleLines: string[]) => void
  onReuseParams: (url: string, objective: string, maxSteps: number) => void
  livePreview?: string
  liveViewUrl?: string
  liveUrl?: string
  liveStep: number
  liveMaxSteps: number
  liveAction?: string
  report?: Record<string, unknown>
  consoleLines: string[]
}

const AiExploreModal = ({
  open, onClose, exploring, onExplore,
  startUrl, onStartUrlChange, objective, onObjectiveChange,
  maxSteps, onMaxStepsChange,
  history, onClearHistory, onViewResult, onReuseParams,
  livePreview, liveViewUrl, liveUrl, liveStep, liveMaxSteps, liveAction,
  report, consoleLines,
}: AiExploreModalProps) => {
  const { t } = useTranslation()
  const stepOptions = [
    { value: 5, label: '5 steps (fast)' },
    { value: 10, label: '10 steps (standard)' },
    { value: 20, label: '20 steps (deep)' },
  ]
  return (
    <Modal
      title={<Space><GlobalOutlined style={{ color: '#3D6E66' }} /><span>AI Exploratory Test</span></Space>}
      open={open} onCancel={onClose} width={1080}
      footer={report ? <Button onClick={onClose}>{t('common.close')}</Button> : <Button type="primary" onClick={onExplore} loading={exploring}>Start</Button>}
    >
      {!report ? (
        <Form layout="vertical">
          <Alert type="info" showIcon message="AI will analyze page elements and decide next actions." style={{ marginBottom: 24 }} />
          <Form.Item label="Start URL" required>
            <Input placeholder="https://example.com" value={startUrl} onChange={(e) => onStartUrlChange(e.target.value)} disabled={exploring} />
          </Form.Item>
          <Form.Item label="Goal">
            <TextArea rows={2} placeholder="e.g. Click as many pages as possible" value={objective} onChange={(e) => onObjectiveChange(e.target.value)} disabled={exploring} />
          </Form.Item>
          <Form.Item label="Max Steps">
            <Select value={maxSteps} onChange={onMaxStepsChange} style={{ width: 120 }} disabled={exploring} options={stepOptions} />
          </Form.Item>
          {history.length > 0 && !exploring && (
            <Form.Item>
              <Card size="small" title={`History (${history.length})`} extra={<Button type="link" onClick={onClearHistory}>Clear</Button>}>
                <Table size="small" dataSource={history} pagination={false} rowKey="id"
                  columns={[
                    { title: 'Time', dataIndex: 'started_at', width: 160, render: (v: string) => new Date(v).toLocaleString() },
                    { title: 'URL', dataIndex: 'start_url', ellipsis: true },
                    { title: 'Status', width: 100, render: (_: Record<string, unknown>, r: ExploreHistoryItem) => <Tag color={r.report?.status === 'failed' ? 'red' : 'green'}>{r.report?.status || 'unknown'}</Tag> },
                    { title: 'Actions', width: 150, render: (_: Record<string, unknown>, r: ExploreHistoryItem) => (
                      <Space size={4}>
                        <Button type="link" size="small" onClick={() => onViewResult(r.report, r.console_lines || [])}>View</Button>
                        <Button type="link" size="small" onClick={() => onReuseParams(r.start_url, r.objective, r.max_steps)}>Reuse</Button>
                      </Space>
                    )},
                  ]}
                />
              </Card>
            </Form.Item>
          )}
          {(exploring || consoleLines.length > 0) && (
            <Form.Item>
              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 12 }}>
                <Card size="small" title="Console">
                  <div style={{ background: '#0f172a', color: '#e2e8f0', borderRadius: 8, padding: 12, height: 260, overflowY: 'auto', fontFamily: 'monospace', fontSize: 12, whiteSpace: 'pre-wrap' as const }}>
                    {consoleLines.length > 0 ? consoleLines.join('\n') : 'Waiting...'}
                  </div>
                </Card>
                <Card size="small" title="Browser" extra={<Tag color={exploring ? 'processing' : 'default'}>{exploring ? 'Running' : 'Done'}</Tag>}>
                  <div style={{ border: '1px solid #d9d9d9', borderRadius: 8, overflow: 'hidden', background: '#0b1220', height: 260, display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                    {livePreview ? <img src={livePreview} alt="preview" style={{ width: '100%', height: '100%', objectFit: 'cover' }} />
                    : liveViewUrl ? <iframe title="live" src={liveViewUrl} style={{ width: '100%', height: '100%', border: 0 }} />
                    : <iframe title="fb" src={liveUrl || startUrl || 'about:blank'} style={{ width: '100%', height: '100%', border: 0 }} />}
                  </div>
                  <div style={{ marginTop: 8, display: 'flex', justifyContent: 'space-between' }}>
                    <Text type="secondary" ellipsis style={{ maxWidth: '72%' }}>{liveUrl || startUrl || 'Loading...'}</Text>
                    <Text type="secondary">{liveStep}/{liveMaxSteps || maxSteps}</Text>
                  </div>
                </Card>
              </div>
            </Form.Item>
          )}
        </Form>
      ) : (
        <div style={{ maxHeight: 600, overflow: 'auto' }}>
          <Alert type={report.status === 'failed' ? 'error' : 'success'} message={`Done (${report.status})`} style={{ marginBottom: 16 }} />
          <Card size="small" title="Errors">
            {report.errors_found?.length > 0 ? (
              <Table size="small" dataSource={report.errors_found} pagination={false} rowKey={(_: Record<string, unknown>, i: Record<string, unknown>) => String(i)}
                columns={[
                  { title: 'Type', dataIndex: 'type', width: 120, render: (v: string) => <Tag color="red">{v}</Tag> },
                  { title: 'Level', dataIndex: 'severity', width: 100 },
                  { title: 'Error', dataIndex: 'text', ellipsis: true },
                ]}
              />
            ) : <Text type="secondary">No errors</Text>}
          </Card>
        </div>
      )}
    </Modal>
  )
}

export default AiExploreModal
