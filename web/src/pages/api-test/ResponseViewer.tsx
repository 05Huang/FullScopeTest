/**
 * 响应展示区组件
 *
 * 从 ApiTestWorkspace 拆分而来，展示 HTTP 响应的 Body、Headers、Cookies、测试结果。
 */

import { useState } from 'react'
import { Card, Tabs, Space, Tag, Typography, Table, Empty } from 'antd'
import MonacoEditor from '@monaco-editor/react'
import ScriptTestResults from './components/ScriptTestResults'

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
  const [responseTab, setResponseTab] = useState('body')

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
          '响应'
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
              label: 'Body',
              children: (
                <MonacoEditor
                  height={250}
                  language="json"
                  theme="vs-light"
                  value={JSON.stringify(response.data, null, 2)}
                  options={{
                    readOnly: true,
                    minimap: { enabled: false },
                    fontSize: 13,
                    scrollBeyondLastLine: false,
                    automaticLayout: true,
                  }}
                />
              ),
            },
            {
              key: 'headers',
              label: 'Headers',
              children: (
                <Table
                  size="small"
                  dataSource={Object.entries(response.headers).map(
                    ([key, value]) => ({ key, value })
                  )}
                  columns={[
                    { title: 'Key', dataIndex: 'key', key: 'key' },
                    { title: 'Value', dataIndex: 'value', key: 'value' },
                  ]}
                  pagination={false}
                />
              ),
            },
            {
              key: 'cookies',
              label: 'Cookies',
              children: <Empty description="暂无 Cookie" />,
            },
            {
              key: 'test-results',
              label: '测试结果',
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
          description="发送请求查看响应"
          style={{ marginTop: 60 }}
        />
      )}
    </Card>
  )
}

export default ResponseViewer
