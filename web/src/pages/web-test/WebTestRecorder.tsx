import { useState } from 'react'
import {
  Card,
  Button,
  Space,
  Typography,
  Input,
  Select,
  Empty,
  List,
  Tag,
  message,
  Alert,
  Tooltip,
  Row,
  Col,
  Statistic,
} from 'antd'
import {
  PlayCircleOutlined,
  PauseCircleOutlined,
  StopOutlined,
  SaveOutlined,
  DeleteOutlined,
  EyeOutlined,
  VideoCameraOutlined,
} from '@ant-design/icons'

const { Title, Text } = Typography

interface RecordedStep {
  id: number
  action: string
  target: string
  value?: string
  timestamp: number
}

const WebTestRecorder = () => {
  const [isRecording, setIsRecording] = useState(false)
  const [isPaused, setIsPaused] = useState(false)
  const [targetUrl, setTargetUrl] = useState('')
  const [browser, setBrowser] = useState('chromium')
  const [steps, setSteps] = useState<RecordedStep[]>([])
  const [elapsedTime] = useState(0)

  const handleStartRecording = () => {
    if (!targetUrl) {
      message.warning('请输入目标 URL')
      return
    }
    
    message.info('录制功能需要配置 Playwright 录制服务，目前为演示模式')
    setIsRecording(true)
    setIsPaused(false)
    
    // 模拟添加一些录制步骤
    const mockSteps: RecordedStep[] = [
      { id: 1, action: 'navigate', target: targetUrl, timestamp: Date.now() },
    ]
    setSteps(mockSteps)
  }

  const handlePauseRecording = () => {
    setIsPaused(!isPaused)
    message.info(isPaused ? '继续录制' : '暂停录制')
  }

  const handleStopRecording = () => {
    setIsRecording(false)
    setIsPaused(false)
    message.success('录制已停止')
  }

  const handleClearSteps = () => {
    setSteps([])
    message.success('已清空录制步骤')
  }

  const handleSaveScript = () => {
    if (steps.length === 0) {
      message.warning('没有可保存的录制步骤')
      return
    }
    message.success('脚本已保存（演示模式）')
  }

  const handleDeleteStep = (stepId: number) => {
    setSteps(steps.filter(s => s.id !== stepId))
    message.success('已删除步骤')
  }

  const getActionColor = (action: string) => {
    const colors: Record<string, string> = {
      click: 'blue',
      input: 'green',
      navigate: 'purple',
      scroll: 'orange',
      hover: 'cyan',
      select: 'magenta',
    }
    return colors[action] || 'default'
  }

  const formatTime = (ms: number) => {
    const seconds = Math.floor((ms / 1000) % 60)
    const minutes = Math.floor((ms / (1000 * 60)) % 60)
    return `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`
  }

  return (
    <div>
      <Title level={4} style={{ marginBottom: 24 }}>
        <VideoCameraOutlined style={{ marginRight: 8 }} />
        录制器
      </Title>

      <Alert
        message="功能说明"
        description="录制器可以自动记录您在浏览器中的操作，并生成 Playwright 测试脚本。目前为演示模式，完整功能需要配置 Playwright 录制服务。"
        type="info"
        showIcon
        style={{ marginBottom: 24 }}
      />

      {/* 录制配置 */}
      <Card title="录制配置" style={{ marginBottom: 24 }}>
        <Row gutter={16}>
          <Col span={12}>
            <div style={{ marginBottom: 16 }}>
              <Text strong>目标 URL</Text>
              <Input
                placeholder="https://example.com"
                value={targetUrl}
                onChange={(e) => setTargetUrl(e.target.value)}
                style={{ marginTop: 8 }}
                disabled={isRecording}
              />
            </div>
          </Col>
          <Col span={6}>
            <div style={{ marginBottom: 16 }}>
              <Text strong>浏览器</Text>
              <Select
                value={browser}
                onChange={setBrowser}
                style={{ width: '100%', marginTop: 8 }}
                disabled={isRecording}
                options={[
                  { value: 'chromium', label: 'Chromium' },
                  { value: 'firefox', label: 'Firefox' },
                  { value: 'webkit', label: 'WebKit' },
                ]}
              />
            </div>
          </Col>
          <Col span={6}>
            <div style={{ marginBottom: 16 }}>
              <Text strong>状态</Text>
              <div style={{ marginTop: 8 }}>
                {isRecording ? (
                  isPaused ? (
                    <Tag color="warning" style={{ padding: '4px 12px' }}>已暂停</Tag>
                  ) : (
                    <Tag color="processing" style={{ padding: '4px 12px' }}>录制中...</Tag>
                  )
                ) : (
                  <Tag color="default" style={{ padding: '4px 12px' }}>未开始</Tag>
                )}
              </div>
            </div>
          </Col>
        </Row>

        <Space>
          {!isRecording ? (
            <Button
              type="primary"
              icon={<PlayCircleOutlined />}
              onClick={handleStartRecording}
            >
              开始录制
            </Button>
          ) : (
            <>
              <Button
                icon={isPaused ? <PlayCircleOutlined /> : <PauseCircleOutlined />}
                onClick={handlePauseRecording}
              >
                {isPaused ? '继续' : '暂停'}
              </Button>
              <Button
                danger
                icon={<StopOutlined />}
                onClick={handleStopRecording}
              >
                停止
              </Button>
            </>
          )}
          <Button
            icon={<DeleteOutlined />}
            onClick={handleClearSteps}
            disabled={steps.length === 0}
          >
            清空
          </Button>
          <Button
            type="primary"
            icon={<SaveOutlined />}
            onClick={handleSaveScript}
            disabled={steps.length === 0}
          >
            保存脚本
          </Button>
        </Space>
      </Card>

      {/* 录制统计 */}
      <Row gutter={16} style={{ marginBottom: 24 }}>
        <Col span={8}>
          <Card>
            <Statistic
              title="录制步骤"
              value={steps.length}
              suffix="步"
            />
          </Card>
        </Col>
        <Col span={8}>
          <Card>
            <Statistic
              title="录制时长"
              value={formatTime(elapsedTime)}
            />
          </Card>
        </Col>
        <Col span={8}>
          <Card>
            <Statistic
              title="目标浏览器"
              value={browser.charAt(0).toUpperCase() + browser.slice(1)}
            />
          </Card>
        </Col>
      </Row>

      {/* 录制步骤 */}
      <Card title={`录制步骤 (${steps.length})`}>
        {steps.length > 0 ? (
          <List
            dataSource={steps}
            renderItem={(step, index) => (
              <List.Item
                actions={[
                  <Tooltip title="查看详情" key="view">
                    <Button type="text" size="small" icon={<EyeOutlined />} />
                  </Tooltip>,
                  <Tooltip title="删除" key="delete">
                    <Button
                      type="text"
                      size="small"
                      danger
                      icon={<DeleteOutlined />}
                      onClick={() => handleDeleteStep(step.id)}
                    />
                  </Tooltip>,
                ]}
              >
                <List.Item.Meta
                  avatar={
                    <div
                      style={{
                        width: 32,
                        height: 32,
                        borderRadius: '50%',
                        background: '#f0f0f0',
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                        fontWeight: 'bold',
                      }}
                    >
                      {index + 1}
                    </div>
                  }
                  title={
                    <Space>
                      <Tag color={getActionColor(step.action)}>{step.action}</Tag>
                      <Text code>{step.target}</Text>
                    </Space>
                  }
                  description={step.value && <Text type="secondary">值: {step.value}</Text>}
                />
              </List.Item>
            )}
          />
        ) : (
          <Empty
            description={
              <span>
                暂无录制步骤
                <br />
                <Text type="secondary">点击"开始录制"并在浏览器中操作</Text>
              </span>
            }
          />
        )}
      </Card>
    </div>
  )
}

export default WebTestRecorder
