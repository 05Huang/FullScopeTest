/**
 * 响应展示区组件
 *
 * 从 ApiTestWorkspace 拆分而来，展示 HTTP 响应的 Body、Headers、Cookies、测试结果。
 */

import { useState, useCallback } from 'react'
import { Card, Tabs, Space, Tag, Typography, Table, Empty, Button, message, Tooltip } from 'antd'
import { CopyOutlined, FormatPainterOutlined } from '@ant-design/icons'
import MonacoEditor from '@monaco-editor/react'
import { useTranslation } from 'react-i18next'
import ScriptTestResults from './components/ScriptTestResults'
import { useThemeStore } from '@/stores/themeStore'

const { Text } = Typography

interface ResponseData {
  status: number
  statusText: string
  time: number
  size: string
  data: any
  headers: Record<string, string>
  script_execution?: any
}

interface ResponseViewerProps {
  response: ResponseData | null
}

const ResponseViewer: React.FC<ResponseViewerProps> = ({ response }) => {
  const { t } = useTranslation()
  const [responseTab, setResponseTab] = useState('body')
  const { resolvedTheme } = useThemeStore()
  const monacoTheme = resolvedTheme === 'dark' ? 'vs-dark' : 'vs-light'

  return (
    <Card
      size="small"
      style={{ borderRadius: 8, flex: 1 }}
      bodyStyle={{ padding: 12, height: '100%' }}
      title={
        response ? (
          <Space>
            <Tag color={response.status < 400 ? 'success' : 'error'}>
              {response.status} {response.statusText}
            </Tag>
            <Text type="secondary">Time: {response.time}ms</Text>
            <Text type="secondary">Size: {response.size}</Text>
          </Space>
        ) : (
          t('responseViewer.response')
        )
      }
    >
      {response ? (
        <Tabs
          activeKey={responseTab}
          onChange={setResponseTab}
          size="small"
          items={[
            {
              key: 'body',
              label: t('responseViewer.body'),
              children: (
                <div>
                  <div style={{ display: 'flex', justifyContent: 'flex-end', gap: 4, marginBottom: 4 }}>
                    <Tooltip title={t('responseViewer.format')}>
                      <Button
                        size="small"
                        type="text"
                        icon={<FormatPainterOutlined />}
                        onClick={() => {
                          try {
                            const formatted = JSON.stringify(response.data, null, 2)
                            navigator.clipboard.writeText(formatted)
                            message.success(t('responseViewer.formatted'))
                          } catch {
                            message.error(t('responseViewer.formatError'))
                          }
                        }}
                      />
                    </Tooltip>
                    <Tooltip title={t('responseViewer.copy')}>
                      <Button
                        size="small"
                        type="text"
                        icon={<CopyOutlined />}
                        onClick={() => {
                          navigator.clipboard.writeText(JSON.stringify(response.data, null, 2))
                          message.success(t('responseViewer.copied'))
                        }}
                      />
                    </Tooltip>
                  </div>
                  <MonacoEditor
                    height={250}
                    language="json"
                    theme={monacoTheme}
                    value={JSON.stringify(response.data, null, 2)}
                    options={{
                      readOnly: true,
                      minimap: { enabled: false },
                      fontSize: 13,
                      scrollBeyondLastLine: false,
                      automaticLayout: true,
                      find: { addExtraSpaceOnTop: false },
                    }}
                  />
                </div>
              ),
            },
            {
              key: 'headers',
              label: t('responseViewer.headers'),
              children: (
                <Table
                  size="small"
                  dataSource={Object.entries(response.headers).map(
                    ([key, value]) => ({ key, value })
                  )}
                  columns={[
                    { title: t('responseViewer.key'), dataIndex: 'key', key: 'key' },
                    { title: t('responseViewer.value'), dataIndex: 'value', key: 'value' },
                  ]}
                  pagination={false}
                />
              ),
            },
            {
              key: 'cookies',
              label: t('responseViewer.cookies'),
              children: <Empty description={t('responseViewer.noCookies')} />,
            },
            {
              key: 'test-results',
              label: t('responseViewer.testResults'),
              children: (
                <ScriptTestResults
                  scriptExecution={response?.script_execution}
                />
              ),
            },
          ]}
        />
      ) : (
        <Empty
          description={t('responseViewer.sendRequest')}
          style={{ marginTop: 60 }}
        />
      )}
    </Card>
  )
}

export default ResponseViewer
