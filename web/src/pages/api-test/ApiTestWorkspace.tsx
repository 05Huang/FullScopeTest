import { useState, useEffect } from 'react'
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
  Modal,
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
  ReloadOutlined,
  InfoCircleOutlined,
} from '@ant-design/icons'
import type { DataNode } from 'antd/es/tree'
import type { MenuProps } from 'antd'
import MonacoEditor from '@monaco-editor/react'
import { apiTestService } from '@/services/apiTestService'
import { environmentService } from '@/services/environmentService'
import CollectionManager from './CollectionManager'
import EnvironmentVariableHint from './EnvironmentVariableHint'

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

const ApiTestWorkspace = () => {
  const [method, setMethod] = useState('GET')
  const [url, setUrl] = useState('')
  const [requestName, setRequestName] = useState('')  // 自定义请求名称
  const [activeTab, setActiveTab] = useState('params')
  const [responseTab, setResponseTab] = useState('body')
  const [sending, setSending] = useState(false)
  const [response, setResponse] = useState<any>(null)
  const [requestBody, setRequestBody] = useState('{}')
  const [bodyType, setBodyType] = useState('json')
  const [headers, setHeaders] = useState<{ key: string; value: string }[]>([{ key: '', value: '' }])
  const [params, setParams] = useState<{ key: string; value: string }[]>([{ key: '', value: '' }])
  const [collections, setCollections] = useState<any[]>([])
  const [cases, setCases] = useState<any[]>([])
  const [treeData, setTreeData] = useState<DataNode[]>([])
  const [saveModalOpen, setSaveModalOpen] = useState(false)
  const [saveCaseName, setSaveCaseName] = useState('')
  const [selectedCollectionId, setSelectedCollectionId] = useState<number | undefined>()
  const [searchText, setSearchText] = useState('')
  const [environments, setEnvironments] = useState<any[]>([])
  const [selectedEnvId, setSelectedEnvId] = useState<number | undefined>()
  const [currentEnv, setCurrentEnv] = useState<any>(null)
  const [sidebarTab, setSidebarTab] = useState<string>('cases') // 侧边栏标签页

  // 加载用例数据
  useEffect(() => {
    loadData()
    // 恢复表单草稿
    restoreFormDraft()
  }, [])

  // 表单状态自动保存到localStorage
  useEffect(() => {
    const draft = {
      method,
      url,
      requestName,
      requestBody,
      bodyType,
      headers: headers.filter(h => h.key || h.value),
      params: params.filter(p => p.key || p.value),
    }
    // 只有当表单有实际内容时才保存
    if (url || requestName || draft.headers.length > 0 || draft.params.length > 0) {
      localStorage.setItem('api-test-form-draft', JSON.stringify(draft))
    }
  }, [method, url, requestName, requestBody, bodyType, headers, params])

  // 从localStorage恢复表单草稿
  const restoreFormDraft = () => {
    try {
      const draftStr = localStorage.getItem('api-test-form-draft')
      if (draftStr) {
        const draft = JSON.parse(draftStr)
        if (draft.method) setMethod(draft.method)
        if (draft.url) setUrl(draft.url)
        if (draft.requestName) setRequestName(draft.requestName)
        if (draft.requestBody) setRequestBody(draft.requestBody)
        if (draft.bodyType) setBodyType(draft.bodyType)
        if (draft.headers && draft.headers.length > 0) {
          setHeaders([...draft.headers, { key: '', value: '' }])
        }
        if (draft.params && draft.params.length > 0) {
          setParams([...draft.params, { key: '', value: '' }])
        }
        message.info('已恢复上次未保存的草稿')
      }
    } catch (error) {
      console.error('恢复草稿失败', error)
    }
  }

  // 清除表单草稿
  const clearFormDraft = () => {
    Modal.confirm({
      title: '确认清除',
      content: '确定要清空当前表单内容吗？此操作不可恢复。',
      okText: '确认清除',
      cancelText: '取消',
      okButtonProps: { danger: true },
      onOk: () => {
        setUrl('')
        setRequestName('')
        setMethod('GET')
        setRequestBody('{}')
        setHeaders([{ key: '', value: '' }])
        setParams([{ key: '', value: '' }])
        setResponse(null)
        // 清除localStorage中的草稿
        localStorage.removeItem('api-test-form-draft')
        message.success('已清空表单')
      },
    })
  }

  const loadData = async () => {
    try {
      const [collectionsRes, casesRes, environmentsRes] = await Promise.all([
        apiTestService.getCollections(),
        apiTestService.getCases({}),
        environmentService.getEnvironments()
      ])
      
      if (collectionsRes.code === 200) {
        setCollections(collectionsRes.data || [])
      }
      if (casesRes.code === 200) {
        setCases(casesRes.data || [])
      }
      if (environmentsRes.code === 200) {
        setEnvironments(environmentsRes.data || [])
      }
      
      // 构建树形数据
      buildTreeData(collectionsRes.data || [], casesRes.data || [])
    } catch (error) {
      console.error('加载数据失败', error)
    }
  }

  const buildTreeData = (collectionsData: any[], casesData: any[]) => {
    const tree: DataNode[] = []
    
    // 添加集合节点
    collectionsData.forEach(collection => {
      const collectionCases = casesData.filter(c => c.collection_id === collection.id)
      tree.push({
        title: collection.name,
        key: `collection-${collection.id}`,
        icon: <FolderOutlined />,
        children: collectionCases.map(c => ({
          title: `${c.method} ${c.name}`,
          key: `case-${c.id}`,
          icon: <FileOutlined />,
          isLeaf: true,
        }))
      })
    })
    
    // 添加未分组的用例
    const ungroupedCases = casesData.filter(c => !c.collection_id)
    if (ungroupedCases.length > 0) {
      tree.push({
        title: '未分组',
        key: 'ungrouped',
        icon: <FolderOutlined />,
        children: ungroupedCases.map(c => ({
          title: `${c.method} ${c.name}`,
          key: `case-${c.id}`,
          icon: <FileOutlined />,
          isLeaf: true,
        }))
      })
    }
    
    setTreeData(tree)
  }

  // 选择用例
  const handleSelectCase = async (keys: React.Key[]) => {
    if (keys.length === 0) return
    const key = String(keys[0])
    
    if (key.startsWith('case-')) {
      const caseId = parseInt(key.replace('case-', ''))
      const caseData = cases.find(c => c.id === caseId)
      if (caseData) {
        setRequestName(caseData.name || '')  // 加载用例名称
        setMethod(caseData.method)
        setUrl(caseData.url || '')
        setRequestBody(JSON.stringify(caseData.body || {}, null, 2))
        if (caseData.headers) {
          setHeaders(Object.entries(caseData.headers).map(([k, v]) => ({ key: k, value: String(v) })))
        }
        message.success(`已加载用例: ${caseData.name}`)
      }
    }
  }

  // 选择环境
  const handleSelectEnv = (envId: number | undefined) => {
    setSelectedEnvId(envId)
    if (envId) {
      const env = environments.find(e => e.id === envId)
      setCurrentEnv(env)
      if (env) {
        message.success(`已选择环境: ${env.name}`)
      }
    } else {
      setCurrentEnv(null)
      message.info('已取消环境选择')
    }
  }

  // 应用环境配置到当前请求
  const applyEnvironment = () => {
    if (!currentEnv) {
      message.warning('请先选择环境')
      return
    }

    // 应用 base_url 到 URL - 自动拼接而不是覆盖
    if (currentEnv.base_url) {
      let newUrl = currentEnv.base_url
      
      // 如果用户已输入URL，则与base_url拼接
      if (url && url.trim()) {
        // 如果用户输入的URL已经是完整URL（以http开头），则保持不变
        if (!url.startsWith('http://') && !url.startsWith('https://')) {
          // 拼接相对路径URL
          newUrl = currentEnv.base_url.replace(/\/$/, '') + (url.startsWith('/') ? url : '/' + url)
        } else {
          // 用户输入的是完整URL，保持不变
          newUrl = url
        }
      }
      
      setUrl(newUrl)
      message.success(`已拼接URL: ${newUrl}`)
    }

    // 应用环境变量到 headers
    if (currentEnv.headers && Object.keys(currentEnv.headers).length > 0) {
      const envHeaders = Object.entries(currentEnv.headers).map(([k, v]) => ({
        key: k,
        value: String(v)
      }))
      
      // 合并已有的 headers
      const existingHeaderKeys = new Set(headers.filter(h => h.key).map(h => h.key))
      const newHeaders = [...headers.filter((_, i) => i === headers.length - 1 && !headers[i].key)]
      
      envHeaders.forEach(h => {
        if (!existingHeaderKeys.has(h.key)) {
          newHeaders.push(h)
        }
      })
      
      setHeaders(newHeaders.length > 0 ? newHeaders : [{ key: '', value: '' }])
      message.success('已应用环境Headers')
    }
  }

  // 获取当前请求的所有参数（包含环境变量和Headers）
  const getRequestWithEnv = async () => {
    let finalUrl = url
    let finalHeaders: Record<string, string> = {}
    let finalParams: Record<string, string> = {}

    // 应用环境配置
    if (currentEnv) {
      // 应用基础URL
      if (currentEnv.base_url && url && !url.startsWith('http')) {
        finalUrl = currentEnv.base_url.replace(/\/$/, '') + (url.startsWith('/') ? url : '/' + url)
      }

      // 应用环境headers
      if (currentEnv.headers) {
        Object.assign(finalHeaders, currentEnv.headers)
      }

      // 应用环境变量到URL和请求头（简单的 {{var}} 替换）
      if (currentEnv.variables) {
        const vars = currentEnv.variables
        finalUrl = finalUrl.replace(/\{\{(\w+)\}\}/g, (match, key) => vars[key] || match)
        
        Object.keys(finalHeaders).forEach(key => {
          finalHeaders[key] = String(finalHeaders[key]).replace(/\{\{(\w+)\}\}/g, (match, varKey) => vars[varKey] || match)
        })
      }
    }

    // 应用当前请求的headers
    headers.filter(h => h.key && h.value).forEach(h => {
      finalHeaders[h.key] = h.value
    })

    // 应用请求参数
    params.filter(p => p.key && p.value).forEach(p => {
      finalParams[p.key] = p.value
    })

    return { finalUrl, finalHeaders, finalParams }
  }

  // 生成 cURL 命令
  const generateCurl = () => {
    let curl = `curl -X ${method} '${url}'`
    
    // 添加 headers
    const headerEntries = headers.filter(h => h.key && h.value)
    headerEntries.forEach(h => {
      curl += ` \\\n  -H '${h.key}: ${h.value}'`
    })
    
    // 添加 body
    if (['POST', 'PUT', 'PATCH'].includes(method) && requestBody && requestBody !== '{}') {
      curl += ` \\\n  -d '${requestBody}'`
    }
    
    return curl
  }

  // 复制为 cURL
  const handleCopyCurl = () => {
    if (!url) {
      message.warning('请先输入请求 URL')
      return
    }
    const curlCommand = generateCurl()
    navigator.clipboard.writeText(curlCommand)
    message.success('已复制 cURL 命令到剪贴板')
  }

  // 保存为用例
  const handleSaveCase = async () => {
    if (!url) {
      message.warning('请先输入请求 URL')
      return
    }
    if (!saveCaseName) {
      message.warning('请输入用例名称')
      return
    }
    
    try {
      const headerObj: Record<string, string> = {}
      headers.filter(h => h.key && h.value).forEach(h => {
        headerObj[h.key] = h.value
      })
      
      let body = undefined
      if (['POST', 'PUT', 'PATCH'].includes(method) && requestBody) {
        try {
          body = JSON.parse(requestBody)
        } catch {
          body = requestBody
        }
      }
      
      const res = await apiTestService.createCase({
        name: saveCaseName,
        method,
        url,
        headers: headerObj,
        body,
        body_type: bodyType,
        collection_id: selectedCollectionId,
      })
      
      if (res.code === 200 || res.code === 201) {
        message.success('用例保存成功')
        setSaveModalOpen(false)
        setSaveCaseName('')
        setSelectedCollectionId(undefined)
        loadData()
      } else {
        message.error(res.message || '保存失败')
      }
    } catch (error) {
      message.error('保存失败')
    }
  }

  // 更多操作菜单
  const moreMenuItems: MenuProps['items'] = [
    { key: 'copy', icon: <CopyOutlined />, label: '复制为 cURL', onClick: handleCopyCurl },
    { key: 'save', icon: <SaveOutlined />, label: '保存到用例', onClick: () => {
      // 保存时默认使用当前请求名称
      setSaveCaseName(requestName)
      setSaveModalOpen(true)
    }},
    { type: 'divider' },
    { key: 'clear', icon: <DeleteOutlined />, label: '清空表单', danger: true, onClick: clearFormDraft },
  ]

  // 参数表格列
  const paramsColumns = [
    {
      title: '序号',
      key: 'index',
      width: 60,
      align: 'center' as const,
      render: (_: any, __: any, index: number) => (
        <Text type="secondary">{index + 1}</Text>
      ),
    },
    {
      title: '参数名',
      dataIndex: 'key',
      key: 'key',
      render: (_: any, record: any, index: number) => (
        <Input
          placeholder="参数名"
          size="small"
          value={record.key}
          onChange={(e) => {
            const newParams = [...params]
            newParams[index].key = e.target.value
            setParams(newParams)
          }}
        />
      ),
    },
    {
      title: '参数值',
      dataIndex: 'value',
      key: 'value',
      render: (_: any, record: any, index: number) => (
        <Input
          placeholder="参数值"
          size="small"
          value={record.value}
          onChange={(e) => {
            const newParams = [...params]
            newParams[index].value = e.target.value
            setParams(newParams)
          }}
        />
      ),
    },
    {
      title: '操作',
      key: 'action',
      width: 80,
      render: (_: any, __: any, index: number) => (
        <Button
          type="text"
          danger
          size="small"
          icon={<DeleteOutlined />}
          onClick={() => {
            const newParams = params.filter((_, i) => i !== index)
            setParams(newParams.length > 0 ? newParams : [{ key: '', value: '' }])
          }}
        />
      ),
    },
  ]

  // 请求头表格列
  const headersColumns = [
    {
      title: '序号',
      key: 'index',
      width: 60,
      align: 'center' as const,
      render: (_: any, __: any, index: number) => (
        <Text type="secondary">{index + 1}</Text>
      ),
    },
    {
      title: 'Header 名',
      dataIndex: 'key',
      key: 'key',
      render: (_: any, record: any, index: number) => (
        <Input
          placeholder="Header 名"
          size="small"
          value={record.key}
          onChange={(e) => {
            const newHeaders = [...headers]
            newHeaders[index].key = e.target.value
            setHeaders(newHeaders)
          }}
        />
      ),
    },
    {
      title: 'Header 值',
      dataIndex: 'value',
      key: 'value',
      render: (_: any, record: any, index: number) => (
        <Input
          placeholder="Header 值"
          size="small"
          value={record.value}
          onChange={(e) => {
            const newHeaders = [...headers]
            newHeaders[index].value = e.target.value
            setHeaders(newHeaders)
          }}
        />
      ),
    },
    {
      title: '操作',
      key: 'action',
      width: 80,
      render: (_: any, __: any, index: number) => (
        <Button
          type="text"
          danger
          size="small"
          icon={<DeleteOutlined />}
          onClick={() => {
            const newHeaders = headers.filter((_, i) => i !== index)
            setHeaders(newHeaders.length > 0 ? newHeaders : [{ key: '', value: '' }])
          }}
        />
      ),
    },
  ]

  // 发送请求
  const handleSend = async () => {
    if (!url) {
      message.warning('请输入请求URL')
      return
    }

    setSending(true)
    const startTime = Date.now()
    
    try {
      // 获取包含环境配置的请求参数
      const { finalUrl, finalHeaders, finalParams } = await getRequestWithEnv()

      // 准备请求头
      const reqHeaders: Record<string, string> = { ...finalHeaders }
      if (bodyType === 'json' && !reqHeaders['Content-Type']) {
        reqHeaders['Content-Type'] = 'application/json'
      } else if (bodyType === 'form' && !reqHeaders['Content-Type']) {
        reqHeaders['Content-Type'] = 'application/x-www-form-urlencoded'
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
        url: finalUrl,
        headers: reqHeaders,
        params: finalParams,
        body,
        body_type: bodyType,
        timeout: 30,
        env_id: selectedEnvId
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

  return (
    <Layout style={{ height: 'calc(100vh - 160px)', background: 'transparent' }}>
      {/* 左侧用例树和集合管理 */}
      <Sider
        width={320}
        style={{
          background: '#fff',
          borderRadius: 8,
          marginRight: 16,
          overflow: 'hidden',
        }}
      >
        <Tabs
          activeKey={sidebarTab}
          onChange={setSidebarTab}
          style={{ height: '100%' }}
          items={[
            {
              key: 'cases',
              label: '测试用例',
              children: (
                <div style={{ padding: 12, height: 'calc(100vh - 240px)', overflow: 'auto' }}>
                  <Space.Compact style={{ width: '100%', marginBottom: 12 }}>
                    <Input
                      placeholder="搜索用例..."
                      prefix={<SearchOutlined />}
                      allowClear
                      value={searchText}
                      onChange={(e) => setSearchText(e.target.value)}
                    />
                    <Tooltip title="刷新">
                      <Button icon={<ReloadOutlined />} onClick={loadData} />
                    </Tooltip>
                  </Space.Compact>

                  {treeData.length > 0 ? (
                    <Tree
                      showIcon
                      defaultExpandAll
                      treeData={treeData}
                      onSelect={handleSelectCase}
                      style={{ background: 'transparent' }}
                    />
                  ) : (
                    <Empty description="暂无用例" style={{ marginTop: 40 }} />
                  )}
                </div>
              ),
            },
            {
              key: 'collections',
              label: '集合管理',
              children: (
                <div style={{ padding: 12, height: 'calc(100vh - 240px)', overflow: 'auto' }}>
                  <CollectionManager onCollectionChange={loadData} />
                </div>
              ),
            },
          ]}
        />
      </Sider>

      {/* 右侧工作区 */}
      <Content style={{ display: 'flex', flexDirection: 'column', gap: 16 }}>
        {/* 请求区域 */}
        <Card
          size="small"
          style={{ borderRadius: 8 }}
          bodyStyle={{ padding: 12 }}
        >
          {/* 请求名称输入栏 */}
          <div style={{ marginBottom: 12, display: 'flex', alignItems: 'center', gap: 8 }}>
            <Input
              placeholder="请输入请求名称（可选）"
              value={requestName}
              onChange={(e) => setRequestName(e.target.value)}
              prefix={<Text type="secondary" style={{ fontSize: 12 }}>名称:</Text>}
              allowClear
              style={{ flex: 1 }}
            />
            <Tooltip title="表单内容会自动保存为草稿，切换页面不会丢失">
              <Text type="secondary" style={{ fontSize: 12, whiteSpace: 'nowrap' }}>
                <InfoCircleOutlined /> 自动保存草稿
              </Text>
            </Tooltip>
          </div>
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
            <Tooltip title="清空表单内容">
              <Button
                danger
                icon={<DeleteOutlined />}
                onClick={clearFormDraft}
              >
                清空
              </Button>
            </Tooltip>
            <Dropdown menu={{ items: moreMenuItems }}>
              <Button icon={<MoreOutlined />} />
            </Dropdown>
          </div>

          {/* 环境选择栏 */}
          <div style={{ display: 'flex', gap: 8, marginBottom: 12, alignItems: 'center' }}>
            <Text type="secondary" style={{ fontSize: 12, minWidth: 50 }}>环境:</Text>
            <Select
              placeholder="选择测试环境"
              allowClear
              style={{ flex: 1, maxWidth: 300 }}
              value={selectedEnvId}
              onChange={handleSelectEnv}
              options={environments.map(env => ({
                value: env.id,
                label: env.name
              }))}
            />
            {currentEnv && (
              <>
                <Tag color="blue">{currentEnv.name}</Tag>
                <Button
                  type="dashed"
                  size="small"
                  onClick={applyEnvironment}
                >
                  应用配置
                </Button>
              </>
            )}
          </div>

          {/* 环境变量提示 */}
          {selectedEnvId && (
            <div style={{ marginBottom: 12 }}>
              <EnvironmentVariableHint envId={selectedEnvId} showUsage={true} />
            </div>
          )}

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
                    dataSource={params.map((p, i) => ({ ...p, key: String(i) }))}
                    pagination={false}
                    footer={() => (
                      <Button
                        type="dashed"
                        size="small"
                        icon={<PlusOutlined />}
                        block
                        onClick={() => setParams([...params, { key: '', value: '' }])}
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
                    dataSource={headers.map((h, i) => ({ ...h, key: String(i) }))}
                    pagination={false}
                    footer={() => (
                      <Button
                        type="dashed"
                        size="small"
                        icon={<PlusOutlined />}
                        block
                        onClick={() => setHeaders([...headers, { key: '', value: '' }])}
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

      {/* 保存用例弹窗 */}
      <Modal
        title="保存到用例"
        open={saveModalOpen}
        onCancel={() => {
          setSaveModalOpen(false)
          setSaveCaseName('')
          setSelectedCollectionId(undefined)
        }}
        onOk={handleSaveCase}
      >
        <Form layout="vertical">
          <Form.Item label="用例名称" required>
            <Input
              placeholder="请输入用例名称"
              value={saveCaseName}
              onChange={(e) => setSaveCaseName(e.target.value)}
            />
          </Form.Item>
          <Form.Item label="所属集合">
            <Select
              placeholder="选择集合（可选）"
              allowClear
              value={selectedCollectionId}
              onChange={setSelectedCollectionId}
              options={collections.map(c => ({
                value: c.id,
                label: c.name
              }))}
            />
          </Form.Item>
          <Form.Item label="请求信息">
            <Card size="small">
              <Space direction="vertical" style={{ width: '100%' }}>
                <div>
                  <Text type="secondary">方法:</Text> <Tag color={methodColors[method]}>{method}</Tag>
                </div>
                <div>
                  <Text type="secondary">URL:</Text> <Text code>{url || '未设置'}</Text>
                </div>
              </Space>
            </Card>
          </Form.Item>
        </Form>
      </Modal>
    </Layout>
  )
}

export default ApiTestWorkspace
