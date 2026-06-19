/**
 * 请求编辑区组件
 *
 * 从 ApiTestWorkspace 拆分而来，包含：
 * - 请求名称输入、URL + 方法选择 + 操作按钮
 * - 环境选择器
 * - 请求配置 Tabs（Params / Headers / Body / Scripts / 断言 / Mock）
 */
import { useState } from 'react'
import { useTranslation } from 'react-i18next'
import {
  Card, Input, Button, Tabs, Select, Space, Table, Tag, Dropdown,
  Typography, Tooltip, Switch, InputNumber, Badge, message, type MenuProps,
} from 'antd'
import {
  PlusOutlined, SendOutlined, SaveOutlined, DeleteOutlined,
  FileAddOutlined, InfoCircleOutlined, RobotOutlined,
  ExperimentOutlined, MoreOutlined,
} from '@ant-design/icons'
import MonacoEditor from '@monaco-editor/react'
import EnvironmentVariableHint from './EnvironmentVariableHint'
import AssertionBuilder, { type AssertionRule } from './components/AssertionBuilder'

const { Text } = Typography

const methodColors: Record<string, string> = {
  GET: '#52c41a', POST: '#1890ff', PUT: '#faad14', DELETE: '#ff4d4f', PATCH: '#722ed1',
}

interface RequestEditorProps {
  requestName: string; setRequestName: (v: string) => void
  method: string; setMethod: (v: string) => void
  url: string; setUrl: (v: string) => void
  sending: boolean; onSend: () => void
  currentCaseId?: number; hasUnsavedChanges: boolean
  onNewCase: () => void; onSaveCase: () => void; onOpenSaveModal: () => void
  onDeleteCase: (id: number, name: string) => void
  environments: any[]; selectedEnvId?: number; onSelectEnv: (id: number) => void
  currentEnv: any; onApplyEnv: () => void
  activeTab: string; setActiveTab: (v: string) => void
  params: { key: string; value: string }[]; setParams: (v: any) => void; paramsColumns: any[]
  headers: { key: string; value: string }[]; setHeaders: (v: any) => void; headersColumns: any[]
  bodyType: string; setBodyType: (v: string) => void
  requestBody: string; setRequestBody: (v: string) => void
  preScript: string; setPreScript: (v: string) => void
  postScript: string; setPostScript: (v: string) => void
  mockEnabled: boolean; setMockEnabled: (v: boolean) => void
  mockResponseCode: number; setMockResponseCode: (v: number) => void
  mockResponseBody: string; setMockResponseBody: (v: string) => void
  mockResponseHeaders: { key: string; value: string }[]; setMockResponseHeaders: (v: any) => void
  mockDelayMs: number; setMockDelayMs: (v: number) => void
  onOpenAiDrawer: () => void; onOpenSynthesize: () => void; onOpenReview: () => void
  selectedCollectionId?: number; activeCollectionId?: number
  moreMenuItems: MenuProps['items']
  response?: any
  /** 可视化断言规则 */
  assertions: AssertionRule[]; setAssertions: (v: AssertionRule[]) => void
  /** 最近一次执行的可视化断言结果 */
  assertionResults?: {
    total: number; passed: number; failed: number
    details?: Array<{
      name: string; passed: boolean; actual?: unknown
      expected?: unknown; error?: string; assertion_type?: string
    }>
  }
}

const RequestEditor: React.FC<RequestEditorProps> = (p) => {
  const { t } = useTranslation()
  return (
    <Card size="small" style={{ borderRadius: 8 }} bodyStyle={{ padding: 12 }}>
      <div style={{ marginBottom: 12, display: 'flex', alignItems: 'center', gap: 8 }}>
        <Input placeholder="请输入请求名称（可选）" value={p.requestName}
          onChange={(e) => p.setRequestName(e.target.value)}
          prefix={<Text type="secondary" style={{ fontSize: 12 }}>名称:</Text>}
          allowClear style={{ flex: 1 }} />
        <Tooltip title="表单内容会自动保存为草稿，切换页面不会丢失">
          <Text type="secondary" style={{ fontSize: 12, whiteSpace: 'nowrap' }}>
            <InfoCircleOutlined /> 自动保存草稿
          </Text>
        </Tooltip>
      </div>
      <div style={{ display: 'flex', gap: 8, marginBottom: 12, flexWrap: 'wrap' }}>
        <Select value={p.method} onChange={p.setMethod} style={{ width: 100 }}
          options={['GET','POST','PUT','DELETE','PATCH'].map(m => ({
            value: m, label: <span style={{ color: methodColors[m], fontWeight: 600 }}>{m}</span>,
          }))} />
        <Input placeholder="请输入请求 URL" value={p.url} onChange={(e) => p.setUrl(e.target.value)} style={{ flex: 1, minWidth: 200 }} />
        <Button type="primary" icon={<SendOutlined />} loading={p.sending} onClick={p.onSend}>{t('copilot.send')}</Button>
        <Button icon={<FileAddOutlined />} onClick={p.onNewCase}>{t('apiTest.createCase')}</Button>
        <Button type={p.currentCaseId && p.hasUnsavedChanges ? "primary" : "default"} icon={<SaveOutlined />}
          onClick={p.currentCaseId ? p.onSaveCase : p.onOpenSaveModal}>{t('common.save')}</Button>
        <Button danger disabled={!p.currentCaseId} icon={<DeleteOutlined />}
          onClick={() => p.currentCaseId && p.onDeleteCase(p.currentCaseId, p.requestName || `ID:${p.currentCaseId}`)}>删除</Button>
        <Button icon={<RobotOutlined />} onClick={p.onOpenAiDrawer}>AI</Button>
        <Button icon={<ExperimentOutlined />} onClick={p.onOpenSynthesize}>AI 扩充</Button>
        <Button type="dashed" icon={<RobotOutlined />} onClick={() => {
          if (!(p.selectedCollectionId || p.activeCollectionId)) { message.warning('请先选择用例集合'); return }
          p.onOpenReview()
        }}>AI 评审</Button>
        <Dropdown menu={{ items: p.moreMenuItems }}><Button icon={<MoreOutlined />} /></Dropdown>
      </div>
      <div style={{ display: 'flex', gap: 8, marginBottom: 12, alignItems: 'center' }}>
        <Text type="secondary" style={{ fontSize: 12, minWidth: 50 }}>环境:</Text>
        <Select placeholder="选择测试环境" allowClear style={{ flex: 1, maxWidth: 300 }}
          value={p.selectedEnvId} onChange={p.onSelectEnv}
          options={p.environments.map(e => ({ value: e.id, label: e.name }))} />
        {p.currentEnv && (<><Tag color="blue">{p.currentEnv.name}</Tag>
          <Button type="dashed" size="small" onClick={p.onApplyEnv}>应用配置</Button></>)}
      </div>
      {p.selectedEnvId && <div style={{ marginBottom: 12 }}><EnvironmentVariableHint envId={p.selectedEnvId} showUsage={true} /></div>}
      <Tabs activeKey={p.activeTab} onChange={p.setActiveTab} size="small" items={[
        { key: 'params', label: 'Params', children: (
          <Table size="small" rowKey="rowKey" columns={p.paramsColumns}
            dataSource={p.params.map((x, i) => ({ ...x, rowKey: String(i) }))}
            pagination={false}
            footer={() => <Button type="dashed" size="small" icon={<PlusOutlined />} block
              onClick={() => p.setParams([...p.params, { key: '', value: '' }])}>添加参数</Button>} />
        )},
        { key: 'headers', label: 'Headers', children: (
          <Table size="small" rowKey="rowKey" columns={p.headersColumns}
            dataSource={p.headers.map((x, i) => ({ ...x, rowKey: String(i) }))}
            pagination={false}
            footer={() => <Button type="dashed" size="small" icon={<PlusOutlined />} block
              onClick={() => p.setHeaders([...p.headers, { key: '', value: '' }])}>添加请求头</Button>} />
        )},
        { key: 'body', label: 'Body', children: (
          <div>
            <Space style={{ marginBottom: 8 }}>
              <Select value={p.bodyType} onChange={p.setBodyType} size="small"
                options={[{value:'none',label:'none'},{value:'json',label:'JSON'},{value:'graphql',label:'GraphQL'},{value:'form',label:'form-data'},{value:'urlencoded',label:'x-www-form-urlencoded'},{value:'raw',label:'raw'}]} />
            </Space>
            {p.bodyType === 'graphql' ? (
              <div>
                <Text type="secondary" style={{ fontSize: 11, marginBottom: 4, display: 'block' }}>Query / Mutation</Text>
                <MonacoEditor height={120} language="graphql" theme="vs-light"
                  value={p.requestBody} onChange={(v) => p.setRequestBody(v || '')}
                  options={{ minimap: { enabled: false }, fontSize: 13, scrollBeyondLastLine: false, automaticLayout: true }} />
              </div>
            ) : (
              <MonacoEditor height={150} language={p.bodyType === 'json' ? 'json' : 'plaintext'} theme="vs-light"
                value={p.requestBody} onChange={(v) => p.setRequestBody(v || '{}')}
                options={{ minimap: { enabled: false }, fontSize: 13, scrollBeyondLastLine: false, automaticLayout: true }} />
            )}
          </div>
        )},
        { key: 'pre-script', label: t('apiTest.preScript'), children: (
          <MonacoEditor height={150} language="javascript" theme="vs-light"
            value={p.preScript} onChange={(v) => p.setPreScript(v || '')}
            options={{ minimap: { enabled: false }, fontSize: 13, scrollBeyondLastLine: false, automaticLayout: true }} />
        )},
        { key: 'tests', label: '断言脚本', children: (
          <MonacoEditor height={150} language="javascript" theme="vs-light"
            value={p.postScript} onChange={(v) => p.setPostScript(v || '')}
            options={{ minimap: { enabled: false }, fontSize: 13, scrollBeyondLastLine: false, automaticLayout: true }} />
        )},
        { key: 'visual-assertions', label: (
          <Space size={4}>
            <span>断言</span>
            {p.assertions.length > 0 && <Badge count={p.assertions.length} size="small" style={{ backgroundColor: '#1890ff' }} />}
          </Space>
        ), children: (
          <AssertionBuilder
            assertions={p.assertions}
            onChange={p.setAssertions}
            assertionResults={p.assertionResults}
            showResults={!!p.assertionResults}
          />
        )},
        { key: 'mock', label: <Space size={4}><span>Mock</span>{p.mockEnabled && <Badge status="success" />}</Space>,
          children: (
            <div style={{ padding: '8px 0' }}>
              <Space direction="vertical" style={{ width: '100%' }} size="middle">
                {/* P32-4: Mock URL 展示 */}
                {p.mockEnabled && p.currentCaseId && (
                  <div style={{ padding: '8px 12px', borderRadius: 8, background: 'var(--fst-surface-dim, #f6f6f6)', border: '1px solid var(--fst-outline-soft, #e8e8e8)', display: 'flex', alignItems: 'center', justifyContent: 'space-between', gap: 8 }}>
                    <div style={{ minWidth: 0 }}>
                      <Text style={{ fontSize: 12, color: 'var(--fst-on-surface-muted, #999)' }}>{t('apiTest.mock.mockUrl') || 'Mock URL'}</Text>
                      <div style={{ fontSize: 13, fontFamily: 'monospace', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
                        {`${window.location.origin}/api/v1/api-test/mock/${p.currentCaseId}`}
                      </div>
                    </div>
                    <Button
                      size="small"
                      onClick={() => {
                        navigator.clipboard.writeText(`${window.location.origin}/api/v1/api-test/mock/${p.currentCaseId}`)
                        message.success(t('apiTest.mock.urlCopied') || 'Mock URL 已复制')
                      }}
                    >
                      {t('common.copy') || '复制'}
                    </Button>
                  </div>
                )}
                <div style={{ display: 'flex', alignItems: 'center', gap: 16, flexWrap: 'wrap' }}>
                  <Space><Text>{t('apiTest.mock.enableMock')}:</Text><Switch checked={p.mockEnabled} onChange={p.setMockEnabled} size="small" /></Space>
                  <Space><Text>{t('apiTest.mock.statusCode')}:</Text><Select value={p.mockResponseCode} onChange={v => p.setMockResponseCode(v)} size="small" style={{width:90}}
                    options={[200,201,204,400,401,403,404,500,502,503].map(c => ({value:c,label:c}))} /></Space>
                  <Space><Text>{t('apiTest.mock.delayMs')}:</Text><InputNumber value={p.mockDelayMs} onChange={v => p.setMockDelayMs(v||0)} size="small" style={{width:80}} min={0} /></Space>
                </div>
                <div>
                  <Text style={{ fontSize: 12, marginBottom: 4, display: 'block' }}>{t('apiTest.mock.responseHeaders')}</Text>
                  <Table size="small" rowKey="rowKey"
                    columns={[
                      { title: 'Key', dataIndex: 'key', render: (_:any,__:any,i:number) => <Input size="small" value={p.mockResponseHeaders[i]?.key||''} onChange={e => { const h=[...p.mockResponseHeaders]; h[i]={...h[i],key:e.target.value}; p.setMockResponseHeaders(h) }} /> },
                      { title: 'Value', dataIndex: 'value', render: (_:any,__:any,i:number) => <Input size="small" value={p.mockResponseHeaders[i]?.value||''} onChange={e => { const h=[...p.mockResponseHeaders]; h[i]={...h[i],value:e.target.value}; p.setMockResponseHeaders(h) }} /> },
                      { title: '', width: 40, render: (_:any,__:any,i:number) => <Button type="text" size="small" danger icon={<DeleteOutlined/>} onClick={() => { const h=[...p.mockResponseHeaders]; h.splice(i,1); p.setMockResponseHeaders(h) }} /> },
                    ]}
                    dataSource={p.mockResponseHeaders.map((x,i)=>({...x,rowKey:String(i)}))}
                    pagination={false}
                    footer={() => <Button type="dashed" size="small" icon={<PlusOutlined/>} block onClick={() => p.setMockResponseHeaders([...p.mockResponseHeaders,{key:'',value:''}])}>{t('apiTest.mock.addHeader')}</Button>} />
                </div>
                <div>
                  <Text style={{ fontSize: 12, marginBottom: 4, display: 'block' }}>{t('apiTest.mock.responseBody')}</Text>
                  <MonacoEditor height={150} language="json" theme="vs-light"
                    value={p.mockResponseBody} onChange={v => p.setMockResponseBody(v||'')}
                    options={{ minimap:{enabled:false}, fontSize:13, scrollBeyondLastLine:false, automaticLayout:true }} />
                </div>
              </Space>
            </div>
          ),
        },
      ]} />
    </Card>
  )
}

export default RequestEditor
