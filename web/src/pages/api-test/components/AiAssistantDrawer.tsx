import { useTranslation } from 'react-i18next'
import { Drawer, Space, Alert, Card, Form, Input, Button, Switch, Tag, Divider, Empty, Typography } from 'antd'
import { RobotOutlined } from '@ant-design/icons'

const { Text: AntText } = Typography
const { TextArea } = Input

interface AiExecutionLog {
  status: 'info' | 'success' | 'error'
  message: string
}

interface AiPlanOperation {
  type: string
  [key: string]: any
}

interface AiAssistantDrawerProps {
  open: boolean
  onClose: () => void
  loadingConfig: boolean
  globalAiConfig: any
  // Model config
  aiBaseUrl: string
  setAiBaseUrl: (v: string) => void
  aiModel: string
  setAiModel: (v: string) => void
  aiApiKey: string
  setAiApiKey: (v: string) => void
  aiVisionBaseUrl: string
  setAiVisionBaseUrl: (v: string) => void
  aiVisionModel: string
  setAiVisionModel: (v: string) => void
  aiVisionApiKey: string
  setAiVisionApiKey: (v: string) => void
  // Prompt & execution
  aiPrompt: string
  setAiPrompt: (v: string) => void
  aiAutoRun: boolean
  setAiAutoRun: (v: boolean) => void
  aiRunning: boolean
  aiSummary: string
  aiPlanSource: string
  aiPlanOperations: AiPlanOperation[]
  aiExecutionLogs: AiExecutionLog[]
  onExecute: () => void
}

const AiAssistantDrawer = ({
  open,
  onClose,
  loadingConfig,
  globalAiConfig,
  aiBaseUrl, setAiBaseUrl,
  aiModel, setAiModel,
  aiApiKey, setAiApiKey,
  aiVisionBaseUrl, setAiVisionBaseUrl,
  aiVisionModel, setAiVisionModel,
  aiVisionApiKey, setAiVisionApiKey,
  aiPrompt, setAiPrompt,
  aiAutoRun, setAiAutoRun,
  aiRunning,
  aiSummary,
  aiPlanSource,
  aiPlanOperations,
  aiExecutionLogs,
  onExecute,
}: AiAssistantDrawerProps) => {
  const { t } = useTranslation()

  return (
    <Drawer
      title={
        <Space>
          <RobotOutlined style={{ color: '#3D6E66' }} />
          <span style={{ color: '#3D6E66', fontWeight: 600 }}>AI Assistant (依赖全局系统设置)</span>
        </Space>
      }
      placement="right"
      width={520}
      open={open}
      onClose={onClose}
    >
      <Space direction="vertical" style={{ width: '100%' }} size="middle">
        <Alert
          type="info"
          showIcon
          message="AI 将通过调用平台现有的 API 来创建或更新环境、集合、用例，并执行测试。"
        />

        <Card size="small" title="模型配置" loading={loadingConfig}>
          <Form layout="vertical">
            <Form.Item label="Base URL" style={{ marginBottom: 12 }}>
              <Input
                placeholder={globalAiConfig?.base_url || "https://api.openai.com/v1"}
                value={aiBaseUrl}
                onChange={(e) => setAiBaseUrl(e.target.value)}
              />
            </Form.Item>
            <Form.Item label="Model" style={{ marginBottom: 12 }}>
              <Input
                placeholder={globalAiConfig?.model || "gpt-4o-mini"}
                value={aiModel}
                onChange={(e) => setAiModel(e.target.value)}
              />
            </Form.Item>
            <Form.Item label="API Key" style={{ marginBottom: 0 }}>
              <Input.Password
                placeholder={globalAiConfig?.api_key || "请输入模型提供商的 API Key"}
                value={aiApiKey}
                onChange={(e) => setAiApiKey(e.target.value)}
              />
            </Form.Item>
            <Form.Item label="Vision Base URL" style={{ marginTop: 12, marginBottom: 12 }}>
              <Input
                placeholder={globalAiConfig?.vision_base_url || globalAiConfig?.base_url || "https://api.openai.com/v1"}
                value={aiVisionBaseUrl}
                onChange={(e) => setAiVisionBaseUrl(e.target.value)}
              />
            </Form.Item>
            <Form.Item label="Vision Model" style={{ marginBottom: 12 }}>
              <Input
                placeholder={globalAiConfig?.vision_model || "gpt-4o-mini"}
                value={aiVisionModel}
                onChange={(e) => setAiVisionModel(e.target.value)}
              />
            </Form.Item>
            <Form.Item label="Vision API Key" style={{ marginBottom: 0 }}>
              <Input.Password
                placeholder={globalAiConfig?.vision_api_key || "请输入视觉模型 API Key"}
                value={aiVisionApiKey}
                onChange={(e) => setAiVisionApiKey(e.target.value)}
              />
            </Form.Item>
          </Form>
        </Card>

        <TextArea
          rows={8}
          placeholder="请用自然语言描述您的需求。例如：创建一个登录接口集合，包含3个测试用例，创建对应的测试环境，然后运行该集合。"
          value={aiPrompt}
          onChange={(e) => setAiPrompt(e.target.value)}
        />

        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <Space>
            <AntText type="secondary">自动运行测试</AntText>
            <Switch checked={aiAutoRun} onChange={setAiAutoRun} />
          </Space>
          <Button type="primary" icon={<RobotOutlined />} loading={aiRunning} onClick={onExecute}>
            执行 AI 指令
          </Button>
        </div>

        {aiSummary && <Alert type="success" showIcon message={aiSummary} />}

        {aiPlanSource && (
          <Tag color={aiPlanSource === 'llm' ? 'blue' : 'orange'}>
            来源: {aiPlanSource}
          </Tag>
        )}

        {aiPlanOperations.length > 0 && (
          <Card size="small" title={`计划执行的操作 (${aiPlanOperations.length})`}>
            <div style={{ maxHeight: 180, overflow: 'auto' }}>
              {aiPlanOperations.map((op, index) => (
                <div key={`${op.type}-${index}`} style={{ marginBottom: 6 }}>
                  <AntText code>{`${index + 1}. ${op.type}`}</AntText>
                </div>
              ))}
            </div>
          </Card>
        )}

        <Divider style={{ margin: '8px 0' }} />

        <Card size="small" title="执行日志">
          {aiExecutionLogs.length === 0 ? (
            <Empty description="暂无日志" image={Empty.PRESENTED_IMAGE_SIMPLE} />
          ) : (
            <div style={{ maxHeight: 220, overflow: 'auto' }}>
              {aiExecutionLogs.map((log, index) => (
                <div key={`${log.status}-${index}`} style={{ marginBottom: 8 }}>
                  <Tag
                    color={
                      log.status === 'success'
                        ? 'success'
                        : log.status === 'error'
                          ? 'error'
                          : 'default'
                    }
                  >
                    {log.status.toUpperCase()}
                  </Tag>
                  <AntText>{log.message}</AntText>
                </div>
              ))}
            </div>
          )}
        </Card>
      </Space>
    </Drawer>
  )
}

export default AiAssistantDrawer
