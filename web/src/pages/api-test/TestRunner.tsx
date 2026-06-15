/**
 * 测试执行控制栏组件
 *
 * 显示执行状态、耗时统计，提供重新发送等快捷操作。
 */
import { Space, Tag, Typography, Button, Tooltip } from 'antd'
import { ReloadOutlined, ThunderboltOutlined } from '@ant-design/icons'

const { Text } = Typography

interface TestRunnerProps {
  sending: boolean
  onResend: () => void
  response?: { status: number; time: number } | null
}

const TestRunner: React.FC<TestRunnerProps> = ({ sending, onResend, response }) => (
  <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 8 }}>
    <Space>
      {sending && <Tag color="processing">执行中...</Tag>}
      {response && !sending && (
        <>
          <Tag color={response.status < 400 ? 'success' : 'error'}>
            {response.status}
          </Tag>
          <Text type="secondary" style={{ fontSize: 12 }}>{response.time}ms</Text>
        </>
      )}
    </Space>
    <Tooltip title="重新发送">
      <Button size="small" icon={<ReloadOutlined />} onClick={onResend} disabled={sending} />
    </Tooltip>
  </div>
)

export default TestRunner
