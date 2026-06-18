/**
 * 响应对比组件
 *
 * 支持两次请求的 JSON Diff 对比。
 * 点击"对比"按钮后，将当前响应锁定为"基准"。
 * 下一次请求的响应与基准进行对比。
 */

import { useState } from 'react'
import { Button, Space, Typography, Tooltip, message } from 'antd'
import { LockOutlined, UnlockOutlined, SwapOutlined } from '@ant-design/icons'
import MonacoEditor from '@monaco-editor/react'
import { useTranslation } from 'react-i18next'
import { useThemeStore } from '@/stores/themeStore'

const { Text } = Typography

interface ResponseDiffProps {
  currentResponse?: any
  onLockBaseline?: (response: any) => void
}

const ResponseDiff: React.FC<ResponseDiffProps> = ({ currentResponse, onLockBaseline }) => {
  const { t } = useTranslation()
  const { resolvedTheme } = useThemeStore()
  const monacoTheme = resolvedTheme === 'dark' ? 'vs-dark' : 'vs-light'

  const [baseline, setBaseline] = useState<any>(null)
  const [isLocked, setIsLocked] = useState(false)

  const handleLockBaseline = () => {
    if (!currentResponse) {
      message.warning(t('apiTest.diff.noResponse'))
      return
    }
    setBaseline(currentResponse)
    setIsLocked(true)
    message.success(t('apiTest.diff.baselineLocked'))
    onLockBaseline?.(currentResponse)
  }

  const handleUnlock = () => {
    setBaseline(null)
    setIsLocked(false)
    message.info(t('apiTest.diff.baselineUnlocked'))
  }

  const formatJson = (data: any) => {
    try {
      if (typeof data === 'string') {
        return JSON.stringify(JSON.parse(data), null, 2)
      }
      return JSON.stringify(data, null, 2)
    } catch {
      return String(data)
    }
  }

  const baselineJson = baseline ? formatJson(baseline.data || baseline) : ''
  const currentJson = currentResponse ? formatJson(currentResponse.data || currentResponse) : ''

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 8, height: '100%' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <Space>
          <SwapOutlined />
          <Text strong>{t('apiTest.diff.title')}</Text>
        </Space>
        <Space>
          {isLocked ? (
            <Tooltip title={t('apiTest.diff.unlock')}>
              <Button size="small" icon={<UnlockOutlined />} onClick={handleUnlock}>
                {t('apiTest.diff.unlock')}
              </Button>
            </Tooltip>
          ) : (
            <Tooltip title={t('apiTest.diff.lockBaseline')}>
              <Button size="small" type="primary" icon={<LockOutlined />} onClick={handleLockBaseline}>
                {t('apiTest.diff.lockBaseline')}
              </Button>
            </Tooltip>
          )}
        </Space>
      </div>

      {!baseline ? (
        <div style={{
          display: 'flex', alignItems: 'center', justifyContent: 'center',
          height: 200, color: '#999', background: '#fafafa', borderRadius: 8,
        }}>
          {t('apiTest.diff.noBaseline')}
        </div>
      ) : (
        <div style={{ display: 'flex', gap: 8, flex: 1, minHeight: 300 }}>
          <div style={{ flex: 1, display: 'flex', flexDirection: 'column' }}>
            <Text type="secondary" style={{ marginBottom: 4, fontSize: 12 }}>
              {t('apiTest.diff.baseline')}
            </Text>
            <MonacoEditor
              height="100%"
              language="json"
              theme={monacoTheme}
              value={baselineJson}
              options={{ readOnly: true, minimap: { enabled: false }, fontSize: 12, scrollBeyondLastLine: false }}
            />
          </div>
          <div style={{ flex: 1, display: 'flex', flexDirection: 'column' }}>
            <Text type="secondary" style={{ marginBottom: 4, fontSize: 12 }}>
              {t('apiTest.diff.current')}
            </Text>
            <MonacoEditor
              height="100%"
              language="json"
              theme={monacoTheme}
              value={currentJson}
              options={{ readOnly: true, minimap: { enabled: false }, fontSize: 12, scrollBeyondLastLine: false }}
            />
          </div>
        </div>
      )}
    </div>
  )
}

export default ResponseDiff
