/**
 * API 导入弹窗组件
 *
 * 支持 Postman Collection (JSON)、CSV 和 cURL 命令导入。
 * 提供模板下载、导入预览和结果展示。
 */
import { useState } from 'react'
import {
  Modal,
  Upload,
  Button,
  Select,
  Space,
  Typography,
  Alert,
  message,
  Divider,
  List,
  Tag,
  Input,
  type UploadFile,
} from 'antd'
import {
  UploadOutlined,
  DownloadOutlined,
  FileTextOutlined,
  CheckCircleOutlined,
  CloseCircleOutlined,
  CodeOutlined,
} from '@ant-design/icons'
import { useTranslation } from 'react-i18next'
import api from '@/services/api'

const { Text, Paragraph } = Typography

interface ImportModalProps {
  open: boolean
  onClose: () => void
  onSuccess: () => void
  projectId: number
  collections?: Array<{ id: number; name: string }>
}

interface ImportResult {
  total: number
  success: number
  failed: number
  errors: string[]
}

const ImportModal = ({ open, onClose, onSuccess, projectId, collections = [] }: ImportModalProps) => {
  const { t } = useTranslation()
  const [importType, setImportType] = useState<'postman' | 'csv' | 'curl'>('postman')
  const [fileContent, setFileContent] = useState<string>('')
  const [fileName, setFileName] = useState<string>('')
  const [collectionId, setCollectionId] = useState<number | undefined>(undefined)
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState<ImportResult | null>(null)

  // P31-4: cURL 导入状态
  const [curlInput, setCurlInput] = useState<string>('')
  const [curlPreview, setCurlPreview] = useState<any>(null)

  const handleFileRead = (file: File) => {
    const reader = new FileReader()
    reader.onload = (e) => {
      const content = e.target?.result as string
      setFileContent(content)
      setFileName(file.name)
    }
    reader.readAsText(file)
    return false // 阻止自动上传
  }

  const handleImport = async () => {
    // cURL 导入走单独逻辑
    if (importType === 'curl') {
      if (!curlInput.trim()) {
        message.warning(t('apiTest.import.curlPlaceholder'))
        return
      }
      setLoading(true)
      try {
        const res = await api.post('/api-test/import-curl', { curl: curlInput })
        const data = (res as any)?.data || res
        if (data) {
          setCurlPreview(data)
        }
      } catch (err: any) {
        message.error(err?.response?.data?.message || t('apiTest.import.curlParseFailed'))
      } finally {
        setLoading(false)
      }
      return
    }

    if (!fileContent) {
      message.warning(t('apiTest.import.selectFile'))
      return
    }
    setLoading(true)
    setResult(null)
    try {
      const endpoint = importType === 'postman'
        ? '/api-test/import/postman'
        : '/api-test/import/csv'

      const res = await api.post(endpoint, {
        project_id: projectId,
        collection_id: collectionId,
        content: fileContent,
      })

      const data = (res as any)?.data || res
      if (data) {
        setResult({
          total: data.total ?? 0,
          success: data.success ?? data.imported ?? 0,
          failed: data.failed ?? 0,
          errors: data.errors ?? [],
        })
        if ((data.success ?? data.imported ?? 0) > 0) {
          onSuccess()
        }
      }
    } catch (err: any) {
      message.error(err?.response?.data?.message || t('apiTest.import.importFailed'))
    } finally {
      setLoading(false)
    }
  }

  const handleDownloadTemplate = async () => {
    try {
      const res = await api.get('/api-test/import/template', { responseType: 'blob' })
      const blob = new Blob([(res as any).data || res], { type: 'text/csv' })
      const link = document.createElement('a')
      link.href = URL.createObjectURL(blob)
      link.download = 'api_test_cases_template.csv'
      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)
      URL.revokeObjectURL(link.href)
    } catch {
      message.error(t('apiTest.import.templateFailed'))
    }
  }

  const handleClose = () => {
    setFileContent('')
    setFileName('')
    setResult(null)
    setCollectionId(undefined)
    setCurlInput('')
    setCurlPreview(null)
    onClose()
  }

  return (
    <Modal
      title={t('apiTest.import.title')}
      open={open}
      onCancel={handleClose}
      width={600}
      footer={
        result || curlPreview ? (
          <Button onClick={handleClose}>{t('common.close')}</Button>
        ) : (
          <Space>
            <Button onClick={handleClose}>{t('common.cancel')}</Button>
            <Button
              type="primary"
              onClick={handleImport}
              loading={loading}
              disabled={importType === 'curl' ? !curlInput.trim() : !fileContent}
            >
              {importType === 'curl'
                ? (t('apiTest.import.parseCurl') || '解析 cURL')
                : t('apiTest.import.startImport')}
            </Button>
          </Space>
        )
      }
      destroyOnHidden
    >
      {!result ? (
        <div style={{ display: 'flex', flexDirection: 'column', gap: 16 }}>
          {/* 导入类型选择 */}
          <div>
            <div style={{ marginBottom: 6, fontWeight: 500, fontSize: 13 }}>
              {t('apiTest.import.importType')}
            </div>
            <Select
              value={importType}
              onChange={(v) => { setImportType(v); setFileContent(''); setFileName(''); setCurlPreview(null) }}
              style={{ width: '100%' }}
              options={[
                { value: 'postman', label: 'Postman Collection (JSON)' },
                { value: 'csv', label: 'CSV' },
                { value: 'curl', label: 'cURL' },
              ]}
            />
          </div>

          {/* 目标集合 */}
          {collections.length > 0 && importType !== 'curl' && (
            <div>
              <div style={{ marginBottom: 6, fontWeight: 500, fontSize: 13 }}>
                {t('apiTest.import.targetCollection')}
              </div>
              <Select
                allowClear
                placeholder={t('apiTest.import.collectionPlaceholder')}
                value={collectionId}
                onChange={setCollectionId}
                style={{ width: '100%' }}
                options={collections.map((c) => ({ value: c.id, label: c.name }))}
              />
            </div>
          )}

          {/* P31-4: cURL 输入 */}
          {importType === 'curl' ? (
            <div>
              <div style={{ marginBottom: 6, fontWeight: 500, fontSize: 13 }}>
                {t('apiTest.import.curlInput') || 'cURL 命令'}
              </div>
              <Input.TextArea
                rows={6}
                value={curlInput}
                onChange={(e) => setCurlInput(e.target.value)}
                placeholder={'curl -X POST https://api.example.com/users \\\n  -H "Content-Type: application/json" \\\n  -d \'{"name": "test"}\''}
                style={{ fontFamily: 'monospace', fontSize: 13 }}
              />
              {curlPreview && (
                <div style={{ marginTop: 12, padding: 12, borderRadius: 8, background: 'var(--fst-surface-variant, #f5f5f5)', border: '1px solid var(--fst-outline-soft, #e8e8e8)' }}>
                  <div style={{ fontWeight: 600, marginBottom: 8, fontSize: 13 }}>{t('apiTest.import.curlPreview') || '解析预览'}</div>
                  <div style={{ fontSize: 13, lineHeight: 2 }}>
                    <div><strong>{t('apiTest.import.method') || '方法'}:</strong> <Tag color="blue">{curlPreview.method}</Tag></div>
                    <div><strong>URL:</strong> <code>{curlPreview.url}</code></div>
                    {curlPreview.headers && Object.keys(curlPreview.headers).length > 0 && (
                      <div><strong>{t('apiTest.import.headers') || '请求头'}:</strong> {Object.keys(curlPreview.headers).length} {t('apiTest.import.count') || '个'}</div>
                    )}
                    {curlPreview.body && (
                      <div><strong>{t('apiTest.import.body') || '请求体'}:</strong> <code style={{ fontSize: 12 }}>{typeof curlPreview.body === 'string' ? curlPreview.body : JSON.stringify(curlPreview.body)}</code></div>
                    )}
                  </div>
                  <Button
                    type="primary"
                    size="small"
                    style={{ marginTop: 8 }}
                    onClick={() => {
                      onSuccess()
                      handleClose()
                    }}
                  >
                    {t('apiTest.import.applyToEditor') || '应用到编辑器'}
                  </Button>
                </div>
              )}
            </div>
          ) : (
            <>
          {/* 文件上传 */}
          <div>
            <div style={{ marginBottom: 6, fontWeight: 500, fontSize: 13 }}>
              {t('apiTest.import.uploadFile')}
            </div>
            <Upload.Dragger
              accept={importType === 'postman' ? '.json' : '.csv'}
              beforeUpload={handleFileRead}
              showUploadList={false}
              maxCount={1}
            >
              <p style={{ margin: '16px 0' }}>
                <UploadOutlined style={{ fontSize: 32, color: '#999' }} />
              </p>
              <p>{t('apiTest.import.dragHint')}</p>
              <p style={{ fontSize: 12, color: '#999' }}>
                {importType === 'postman' ? 'JSON' : 'CSV'} {t('apiTest.import.fileSizeHint')}
              </p>
            </Upload.Dragger>
            {fileName && (
              <div style={{ marginTop: 8 }}>
                <Tag icon={<FileTextOutlined />} color="blue">{fileName}</Tag>
              </div>
            )}
          </div>

          {/* CSV 模板下载 */}
          {importType === 'csv' && (
            <>
              <Divider plain style={{ fontSize: 12 }}>{t('common.or')}</Divider>
              <Button
                type="link"
                icon={<DownloadOutlined />}
                onClick={handleDownloadTemplate}
                style={{ padding: 0 }}
              >
                {t('apiTest.import.downloadTemplate')}
              </Button>
            </>
          )}
            </>
          )}
        </div>
      ) : (
        /* 导入结果 */
        <div>
          <Alert
            type={result.failed === 0 ? 'success' : 'warning'}
            message={t('apiTest.import.resultTitle')}
            description={
              <Space direction="vertical" size={4}>
                <Text>{t('apiTest.import.total')}: {result.total}</Text>
                <Text style={{ color: '#2D6A64' }}>
                  <CheckCircleOutlined style={{ marginRight: 4 }} />
                  {t('apiTest.import.imported')}: {result.success}
                </Text>
                {result.failed > 0 && (
                  <Text style={{ color: '#C75450' }}>
                    <CloseCircleOutlined style={{ marginRight: 4 }} />
                    {t('apiTest.import.failed')}: {result.failed}
                  </Text>
                )}
              </Space>
            }
            style={{ marginBottom: 16 }}
          />
          {result.errors.length > 0 && (
            <div>
              <Text strong style={{ fontSize: 13 }}>{t('apiTest.import.errorDetails')}:</Text>
              <List
                size="small"
                dataSource={result.errors.slice(0, 10)}
                renderItem={(err) => (
                  <List.Item style={{ padding: '4px 0' }}>
                    <Text type="danger" style={{ fontSize: 12 }}>{err}</Text>
                  </List.Item>
                )}
              />
              {result.errors.length > 10 && (
                <Text type="secondary" style={{ fontSize: 12 }}>
                  {t('apiTest.import.moreErrors', { count: result.errors.length - 10 })}
                </Text>
              )}
            </div>
          )}
        </div>
      )}
    </Modal>
  )
}

export default ImportModal
