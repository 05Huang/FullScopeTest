import { useState, useCallback } from 'react'
import { Modal, Button, Space, Typography, message, Tag, List, Card, Empty } from 'antd'
import { PlayCircleOutlined, ImportOutlined, FileTextOutlined } from '@ant-design/icons'
import { useTranslation } from 'react-i18next'
import { apiTestService } from '@/services/apiTestService'

const { Title, Text } = Typography

interface BddStep { keyword: string; text: string }
interface BddScenario { name: string; steps: BddStep[] }
interface BddParseResult { feature: string; scenarios: BddScenario[] }
interface BddEditorProps { open: boolean; onClose: () => void; collectionId?: number; onImported?: () => void }

const STEP_COLORS: Record<string, string> = { Given: 'blue', When: 'orange', Then: 'green', And: 'default', But: 'red' };

const BddEditor = ({ open, onClose, collectionId, onImported }: BddEditorProps) => {
  const { t } = useTranslation()
  const [content, setContent] = useState('')
  const [parsing, setParsing] = useState(false)
  const [importing, setImporting] = useState(false)
  const [parseResult, setParseResult] = useState<BddParseResult | null>(null)

  const handleParse = async () => {
    if (!content.trim()) return
    setParsing(true)
    try {
      const res = await apiTestService.parseBdd({ content, collection_id: collectionId })
      if (res.code === 200) { setParseResult(res.data); message.success(t('bddEditor.parseSuccess')) }
      else message.error(res.message || t('bddEditor.parseFailed'))
    } catch { message.error(t('bddEditor.parseFailed')) } finally { setParsing(false) }
  };

  const handleImport = async () => {
    if (!parseResult) return
    setImporting(true)
    try {
      const res = await apiTestService.importBdd({ feature: parseResult.feature, scenarios: parseResult.scenarios, collection_id: collectionId })
      if (res.code === 200 || res.code === 201) { message.success(t('bddEditor.importSuccess')); onImported?.(); onClose() }
      else message.error(res.message || t('bddEditor.importFailed'))
    } catch { message.error(t('bddEditor.importFailed')) } finally { setImporting(false) }
  };

  const placeholderText = String.fromCharCode(70,101,97,116,117,114,101,58,32,85,115,101,114,32,108,111,103,105,110,10) + String.fromCharCode(32,32,83,99,101,110,97,114,105,111,58,32,83,117,99,99,101,115,115,102,117,108,32,108,111,103,105,110,10) + String.fromCharCode(32,32,32,32,71,105,118,101,110,32,117,115,101,114,110,97,109,101,32,34,116,101,115,116,34,10) + String.fromCharCode(32,32,32,32,87,104,101,110,32,80,79,83,84,32,47,97,112,105,47,108,111,103,105,110,10) + String.fromCharCode(32,32,32,32,84,104,101,110,32,115,116,97,116,117,115,32,99,111,100,101,32,105,115,32,50,48,48)

  return (
    <Modal
      title={<Space><FileTextOutlined />{t('bddEditor.title')}</Space>}
      open={open}
      onCancel={onClose}
      width={900}
      footer={
        <Space>
          <Button onClick={onClose}>{t('common.cancel')}</Button>
          <Button icon={<PlayCircleOutlined />} loading={parsing} onClick={handleParse}>{t('bddEditor.parse')}</Button>
          <Button type='primary' icon={<ImportOutlined />} loading={importing} disabled={!parseResult} onClick={handleImport}>{t('bddEditor.import')}</Button>
        </Space>
      }
    >
      <div style={{ display: 'flex', gap: 16 }}>
        <div style={{ flex: 1 }}>
          <Text strong style={{ display: 'block', marginBottom: 8 }}>Gherkin</Text>
          <textarea value={content} onChange={(e) => setContent(e.target.value)} placeholder={placeholderText}
            style={{ width: '100%', minHeight: 350, fontFamily: 'monospace', fontSize: 13, padding: 12, borderRadius: 8, border: '1px solid #d9d9d9', resize: 'vertical' }}
          />
        </div>
        <div style={{ flex: 1 }}>
          <Text strong style={{ display: 'block', marginBottom: 8 }}>{t('bddEditor.parse')}</Text>
          {!parseResult ? <Empty /> : (
            <div style={{ maxHeight: 380, overflow: 'auto' }}>
              <Card size='small' style={{ marginBottom: 8 }}>
                <Text strong>{t('bddEditor.feature')}: </Text><Text>{parseResult.feature}</Text>
              </Card>
              {parseResult.scenarios.map((scenario, i) => (
                <Card key={i} size='small' style={{ marginBottom: 8 }}>
                  <Text strong>{t('bddEditor.scenario')}: {scenario.name}</Text>
                  <List size='small' dataSource={scenario.steps} renderItem={(step: BddStep) => (
                    <List.Item style={{ padding: '4px 0' }}>
                      <Tag color={STEP_COLORS[step.keyword] || 'default'}>{step.keyword}</Tag>
                      <Text>{step.text}</Text>
                    </List.Item>
                  )} />
                </Card>
              ))}
            </div>
          )}
        </div>
      </div>
    </Modal>
  )
}

export default BddEditor
