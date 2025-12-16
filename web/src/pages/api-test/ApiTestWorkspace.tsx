import { useState } from 'react'
import {
  Layout,
  Card,
  Tree,
  Input,
  Button,
  Tabs,
  Select,
  Form,
  Space,
  Table,
  Tag,
  Dropdown,
  Typography,
  Empty,
  Tooltip,
  message,
} from 'antd'
import {
  PlusOutlined,
  FolderOutlined,
  FileOutlined,
  SendOutlined,
  SaveOutlined,
  DeleteOutlined,
  CopyOutlined,
  MoreOutlined,
  SearchOutlined,
} from '@ant-design/icons'
import type { DataNode } from 'antd/es/tree'
import type { MenuProps } from 'antd'
import MonacoEditor from '@monaco-editor/react'
import { apiTestService } from '@/services/apiTestService'

const { Sider, Content } = Layout
const { Text } = Typography

// HTTP 方法颜色
const methodColors: Record<string, string> = {
  GET: '#52c41a',
  POST: '#1890ff',
  PUT: '#faad14',
  DELETE: '#ff4d4f',
  PATCH: '#722ed1',
}

// 模拟用例树数据
const mockTreeData: DataNode[] = [
  {
    title: '用户模块',
    key: 'user',
    icon: <FolderOutlined />,
    children: [
      { title: 'POST 用户登录', key: 'user-login', icon: <FileOutlined /> },
      { title: 'POST 用户注册', key: 'user-register', icon: <FileOutlined /> },
      { title: 'GET 获取用户信息', key: 'user-info', icon: <FileOutlined /> },
    ],
  },
  {
    title: '订单模块',
    key: 'order',
    icon: <FolderOutlined />,
    children: [
      { title: 'GET 订单列表', key: 'order-list', icon: <FileOutlined /> },
      { title: 'POST 创建订单', key: 'order-create', icon: <FileOutlined /> },
    ],
  },
]

const ApiTestWorkspace = () => {
  const [method, setMethod] = useState('GET')
  const [url, setUrl] = useState('')
  const [activeTab, setActiveTab] = useState('params')
  const [responseTab, setResponseTab] = useState('body')
  const [sending, setSending] = useState(false)
  const [response, setResponse] = useState<any>(null)
  const [requestBody, setRequestBody] = useState('{}')
  const [bodyType, setBodyType] = useState('json')

  // 参数表格列
  const paramsColumns = [
    {
      title: '参数名',
      dataIndex: 'key',
      key: 'key',
      render: () => <Input placeholder="参数名" size="small" />,
    },
    {
      title: '参数值',
      dataIndex: 'value',
      key: 'value',
      render: () => <Input placeholder="参数值" size="small" />,
    },
    {
      title: '描述',
      dataIndex: 'description',
      key: 'description',
      render: () => <Input placeholder="描述" size="small" />,
    },
    {
      title: '操作',
      key: 'action',
      width: 80,
      render: () => (
        <Button type="text" danger size="small" icon={<DeleteOutlined />} />
      ),
    },
  ]

  // 请求头表格列
  const headersColumns = [...paramsColumns]

  // 发送请求
  const handleSend = async () => {
    if (!url) {
      message.warning('请输入请求URL')
      return
    }

    setSending(true)
    const startTime = Date.now()
    
    try {
      // 准备请求头
      const headers: Record<string, string> = {}
      if (bodyType === 'json') {
        headers['Content-Type'] = 'application/json'
      } else if (bodyType === 'form') {
        headers['Content-Type'] = 'application/x-www-form-urlencoded'
      }
      
      // 准备请求体
      let body = undefined
      if (['POST', 'PUT', 'PATCH'].includes(method)) {
        if (bodyType === 'json') {
          try {
            body = JSON.parse(requestBody)
          } catch {
            message.error('JSON 格式错误')
            setSending(false)
            return
          }
        } else {
          body = requestBody
        }
      }

      // 调用后端 API 执行请求
      const result = await apiTestService.executeRequest({
        method,
        url,
        headers,
        body,
        body_type: bodyType,
        timeout: 30,
      })

      const elapsed = Date.now() - startTime

      // 后端返回格式: { code: 200, data: { success: true, status_code: 200, ... } }
      if (result.code === 200 && result.data) {
        const respData = result.data
        if (respData.success) {
          setResponse({
            status: respData.status_code,
            statusText: respData.status_code < 400 ? 'OK' : 'Error',
            time: respData.response_time || elapsed,
            size: respData.response_size || '-',
            headers: respData.headers || {},
            data: respData.body,
          })
          message.success('请求发送成功')
        } else {
          setResponse({
            status: 0,
            statusText: 'Error',
            time: respData.response_time || elapsed,
            size: '-',
            headers: {},
            data: { error: respData.error || '请求失败' },
          })
          message.error(respData.error || '请求失败')
        }
      } else {
        setResponse({
          status: 0,
          statusText: 'Error',
          time: elapsed,
          size: '-',
          headers: {},
          data: { error: result.message || '请求失败' },
        })
        message.error(result.message || '请求失败')
      }
    } catch (error: any) {
      const elapsed = Date.now() - startTime
      setResponse({
        status: 0,
        statusText: 'Error',
        time: elapsed,
        size: '-',
        headers: {},
        data: { error: error.message || '请求失败' },
      })
      message.error('请求失败: ' + (error.message || '未知错误'))
    } finally {
      setSending(false)
    }
  }

  // 更多操作菜单
  const moreMenuItems: MenuProps['items'] = [
    { key: 'copy', icon: <CopyOutlined />, label: '复制为 cURL' },
    { key: 'save', icon: <SaveOutlined />, label: '保存到用例' },
    { type: 'divider' },
    { key: 'delete', icon: <DeleteOutlined />, label: '删除', danger: true },
  ]

  return (
    <Layout style={{ height: 'calc(100vh - 160px)', background: 'transparent' }}>
      {/* 左侧用例树 */}
      <Sider
        width={280}
        style={{
          background: '#fff',
          borderRadius: 8,
          marginRight: 16,
          overflow: 'hidden',
        }}
      >
        <div style={{ padding: 12 }}>
          <Space.Compact style={{ width: '100%', marginBottom: 12 }}>
            <Input
              placeholder="搜索用例..."
              prefix={<SearchOutlined />}
              allowClear
            />
            <Tooltip title="新建集合">
              <Button icon={<PlusOutlined />} />
            </Tooltip>
          </Space.Compact>

          <Tree
            showIcon
            defaultExpandAll
            treeData={mockTreeData}
            style={{ background: 'transparent' }}
          />
        </div>
      </Sider>

      {/* 右侧工作区 */}
      <Content style={{ display: 'flex', flexDirection: 'column', gap: 16 }}>
        {/* 请求区域 */}
        <Card
          size="small"
          style={{ borderRadius: 8 }}
          bodyStyle={{ padding: 12 }}
        >
          {/* URL 输入栏 */}
          <div style={{ display: 'flex', gap: 8, marginBottom: 12 }}>
            <Select
              value={method}
              onChange={setMethod}
              style={{ width: 100 }}
              options={['GET', 'POST', 'PUT', 'DELETE', 'PATCH'].map((m) => ({
                value: m,
                label: (
                  <span style={{ color: methodColors[m], fontWeight: 600 }}>
                    {m}
                  </span>
                ),
              }))}
            />
            <Input
              placeholder="请输入请求 URL，例如：https://api.example.com/users"
              value={url}
              onChange={(e) => setUrl(e.target.value)}
              style={{ flex: 1 }}
            />
            <Button
              type="primary"
              icon={<SendOutlined />}
              loading={sending}
              onClick={handleSend}
            >
              发送
            </Button>
            <Dropdown menu={{ items: moreMenuItems }}>
              <Button icon={<MoreOutlined />} />
            </Dropdown>
          </div>

          {/* 请求配置 Tabs */}
          <Tabs
            activeKey={activeTab}
            onChange={setActiveTab}
            size="small"
            items={[
              {
                key: 'params',
                label: 'Params',
                children: (
                  <Table
                    size="small"
                    columns={paramsColumns}
                    dataSource={[{ key: '1' }]}
                    pagination={false}
                    footer={() => (
                      <Button
                        type="dashed"
                        size="small"
                        icon={<PlusOutlined />}
                        block
                      >
                        添加参数
                      </Button>
                    )}
                  />
                ),
              },
              {
                key: 'headers',
                label: 'Headers',
                children: (
                  <Table
                    size="small"
                    columns={headersColumns}
                    dataSource={[{ key: '1' }]}
                    pagination={false}
                    footer={() => (
                      <Button
                        type="dashed"
                        size="small"
                        icon={<PlusOutlined />}
                        block
                      >
                        添加请求头
                      </Button>
                    )}
                  />
                ),
              },
              {
                key: 'body',
                label: 'Body',
                children: (
                  <div>
                    <Space style={{ marginBottom: 8 }}>
                      <Select
                        value={bodyType}
                        onChange={setBodyType}
                        size="small"
                        options={[
                          { value: 'none', label: 'none' },
                          { value: 'json', label: 'JSON' },
                          { value: 'form', label: 'form-data' },
                          { value: 'urlencoded', label: 'x-www-form-urlencoded' },
                          { value: 'raw', label: 'raw' },
                        ]}
                      />
                    </Space>
                    <MonacoEditor
                      height={150}
                      language={bodyType === 'json' ? 'json' : 'plaintext'}
                      theme="vs-light"
                      value={requestBody}
                      onChange={(value) => setRequestBody(value || '{}')}
                      options={{
                        minimap: { enabled: false },
                        fontSize: 13,
                        lineNumbers: 'on',
                        scrollBeyondLastLine: false,
                        automaticLayout: true,
                      }}
                    />
                  </div>
                ),
              },
              {
                key: 'auth',
                label: 'Auth',
                children: (
                  <Form layout="vertical" size="small">
                    <Form.Item label="认证类型">
                      <Select
                        defaultValue="none"
                        options={[
                          { value: 'none', label: '无' },
                          { value: 'bearer', label: 'Bearer Token' },
                          { value: 'basic', label: 'Basic Auth' },
                          { value: 'apikey', label: 'API Key' },
                        ]}
                      />
                    </Form.Item>
                  </Form>
                ),
              },
              {
                key: 'pre-script',
                label: '前置脚本',
                children: (
                  <MonacoEditor
                    height={150}
                    language="javascript"
                    theme="vs-light"
                    value="// 在请求发送前执行"
                    options={{
                      minimap: { enabled: false },
                      fontSize: 13,
                      scrollBeyondLastLine: false,
                      automaticLayout: true,
                    }}
                  />
                ),
              },
              {
                key: 'tests',
                label: '断言脚本',
                children: (
                  <MonacoEditor
                    height={150}
                    language="javascript"
                    theme="vs-light"
                    value="// 在请求完成后执行断言"
                    options={{
                      minimap: { enabled: false },
                      fontSize: 13,
                      scrollBeyondLastLine: false,
                      automaticLayout: true,
                    }}
                  />
                ),
              },
            ]}
          />
        </Card>

        {/* 响应区域 */}
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
                  children: <Empty description="暂无测试结果" />,
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
      </Content>
    </Layout>
  )
}

export default ApiTestWorkspace
