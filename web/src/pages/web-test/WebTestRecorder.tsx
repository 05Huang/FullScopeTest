import { useState, useEffect } from 'react'
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
  Modal,
  Form,
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
import { webTestService } from '@/services/webTestService'

const { Title, Text } = Typography
const { TextArea } = Input

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
  const [isSaveModalOpen, setIsSaveModalOpen] = useState(false)
  const [, setRecordingPid] = useState<number | null>(null)
  const [form] = Form.useForm()

  // 定期检查录制状态
  useEffect(() => {
    if (isRecording) {
      const timer = setInterval(async () => {
        try {
          const res = await webTestService.getRecordingStatus()
          if (res.code === 200 && !res.data.is_recording) {
            // 录制已停止
            setIsRecording(false)
            setRecordingPid(null)
            
            // 显示详细的退出信息
            if (res.data.exit_code !== undefined) {
              message.warning({
                content: `录制器已关闭（退出码: ${res.data.exit_code}）`,
                duration: 5
              })
            } else {
              message.warning('录制器已关闭（可能是关闭了 Inspector 窗口）')
            }
          }
        } catch (error) {
          console.error('检查录制状态失败:', error)
        }
      }, 3000) // 每3秒检查一次

      return () => clearInterval(timer)
    }
  }, [isRecording])

  const handleStartRecording = async () => {
    if (!targetUrl) {
      message.warning('请输入目标 URL')
      return
    }
    
    try {
      message.loading('正在启动录制器...', 0)
      
      const res = await webTestService.startRecording({
        url: targetUrl,
        browser: browser
      })
      
      message.destroy()
      
      if (res.code === 200) {
        setIsRecording(true)
        setIsPaused(false)
        setRecordingPid(res.data.pid)
        
        message.success({
          content: (
            <div>
              <div>{res.data.message}</div>
              <div style={{ marginTop: 8, fontSize: '12px', color: '#666' }}>
                <div>⚠️ 请保持 Playwright Inspector 窗口打开</div>
                <div>关闭窗口将自动结束录制会话</div>
                <div>录制完成后，请从 Inspector 中复制代码，然后点击"保存脚本"</div>
              </div>
            </div>
          ),
          duration: 10
        })
        
        // 模拟添加初始步骤
        const mockSteps: RecordedStep[] = [
          { id: 1, action: 'navigate', target: targetUrl, timestamp: Date.now() },
        ]
        setSteps(mockSteps)
      } else {
        message.error(res.message || '启动录制失败')
      }
    } catch (error: any) {
      message.destroy()
      message.error(error.response?.data?.message || '启动录制失败，请确保 Playwright 已安装')
    }
  }

  const handlePauseRecording = () => {
    setIsPaused(!isPaused)
    message.info(isPaused ? '继续录制' : '暂停录制')
  }

  const handleStopRecording = async () => {
    try {
      const res = await webTestService.stopRecording()
      
      if (res.code === 200) {
        setIsRecording(false)
        setIsPaused(false)
        setRecordingPid(null)
        message.success('录制已停止')
      } else {
        message.error(res.message || '停止录制失败')
      }
    } catch (error: any) {
      message.error('停止录制失败')
    }
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
    
    // 打开保存对话框，预填充信息
    form.setFieldsValue({
      target_url: targetUrl,
      browser: browser,
      name: `录制脚本_${new Date().toLocaleString('zh-CN')}`,
      description: `录制于 ${targetUrl || '未指定URL'}`
    })
    setIsSaveModalOpen(true)
  }
  
  const handleConfirmSave = async (values: any) => {
    try {
      // 生成基于步骤的脚本内容
      const scriptContent = generateScriptFromSteps(steps, values.target_url)
      
      const result = await webTestService.createScript({
        name: values.name,
        description: values.description,
        target_url: values.target_url,
        browser: values.browser,
        script_content: scriptContent,
      })
      
      if (result.code === 200 || result.code === 201) {
        message.success('脚本保存成功')
        setIsSaveModalOpen(false)
        form.resetFields()
        // 清空录制步骤
        setSteps([])
        setTargetUrl('')
      } else {
        message.error(result.message || '保存失败')
      }
    } catch (error: any) {
      message.error('保存脚本失败')
    }
  }
  
  const generateScriptFromSteps = (steps: RecordedStep[], url: string) => {
    // 根据录制的步骤生成 Playwright 脚本
    return `"""
自动录制的 Playwright 测试脚本
录制时间: ${new Date().toLocaleString('zh-CN')}
目标URL: ${url || 'N/A'}
"""
from playwright.sync_api import sync_playwright, expect

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        # 录制的步骤
${steps.map((step, index) => {
  if (step.action === 'navigate') {
    return `        # 步骤 ${index + 1}: 导航到页面\n        page.goto("${step.target}")`
  } else if (step.action === 'click') {
    return `        # 步骤 ${index + 1}: 点击元素\n        page.click("${step.target}")`
  } else if (step.action === 'input') {
    return `        # 步骤 ${index + 1}: 输入文本\n        page.fill("${step.target}", "${step.value || ''}")`
  } else {
    return `        # 步骤 ${index + 1}: ${step.action}\n        # TODO: 实现 ${step.action} 操作`
  }
}).join('\n        \n')}
        
        # 截图
        page.screenshot(path="test_result.png")
        
        browser.close()
        return {"status": "success"}

if __name__ == "__main__":
    result = run()
    print(result)
`
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
        description={
          <div>
            <p>点击"开始录制"后，系统会在本地启动 Playwright Inspector 和浏览器窗口。</p>
            <p style={{ marginTop: 8 }}>
              <strong>使用步骤：</strong>
            </p>
            <ol style={{ marginTop: 4, paddingLeft: 20 }}>
              <li>输入目标网址并点击"开始录制"</li>
              <li>在打开的浏览器窗口中进行操作</li>
              <li>从 Playwright Inspector 窗口复制生成的 Python 代码</li>
              <li>返回此页面，点击"保存脚本"并粘贴代码</li>
            </ol>
            <p style={{ marginTop: 8, color: '#ff4d4f' }}>
              <strong>⚠️ 重要提示：</strong>关闭 Playwright Inspector 窗口会自动结束录制会话，请确保在关闭前已复制好生成的代码。
            </p>
            <p style={{ marginTop: 4, color: '#faad14' }}>
              <strong>注意：</strong>后端服务必须在本地运行，远程服务器无法使用此功能。
            </p>
          </div>
        }
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

      {/* 保存脚本对话框 */}
      <Modal
        title="保存录制脚本"
        open={isSaveModalOpen}
        onCancel={() => {
          setIsSaveModalOpen(false)
          form.resetFields()
        }}
        onOk={() => {
          form.validateFields().then((values) => {
            handleConfirmSave(values)
          })
        }}
        width={600}
      >
        <Form form={form} layout="vertical">
          <Form.Item
            name="name"
            label="脚本名称"
            rules={[{ required: true, message: '请输入脚本名称' }]}
          >
            <Input placeholder="请输入脚本名称" />
          </Form.Item>
          <Form.Item name="description" label="描述">
            <TextArea rows={2} placeholder="请输入脚本描述" />
          </Form.Item>
          <Form.Item
            name="target_url"
            label="目标 URL"
            rules={[{ required: true, message: '请输入目标URL' }]}
          >
            <Input placeholder="https://example.com" />
          </Form.Item>
          <Form.Item
            name="browser"
            label="目标浏览器"
            initialValue="chromium"
          >
            <Select
              options={[
                { value: 'chromium', label: 'Chromium' },
                { value: 'firefox', label: 'Firefox' },
                { value: 'webkit', label: 'WebKit (Safari)' },
              ]}
            />
          </Form.Item>
        </Form>
      </Modal>
    </div>
  )
}

export default WebTestRecorder
