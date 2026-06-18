/**
 * 500 错误页面
 *
 * 网络断开或后端 500 时展示友好提示
 */

import { Result, Button, Typography } from 'antd'

const { Paragraph } = Typography

interface ServerErrorProps {
  requestId?: string
  onRetry?: () => void
}

const ServerError: React.FC<ServerErrorProps> = ({ requestId, onRetry }) => (
  <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: '100vh' }}>
    <Result
      status="500"
      title="服务器错误"
      subTitle="服务器处理请求时发生错误，请稍后重试"
      extra={[
        <Button type="primary" key="retry" onClick={onRetry || (() => window.location.reload())}>
          重试
        </Button>,
        <Button key="home" onClick={() => window.location.href = "/"}>
          返回首页
        </Button>,
      ]}
    >
      {requestId && (
        <Paragraph
          copyable
          style={{
            maxWidth: 400,
            fontSize: 12,
            color: '#999',
            background: '#f5f5f5',
            padding: 12,
            borderRadius: 6,
            textAlign: 'center',
          }}
        >
          Request ID: {requestId}
        </Paragraph>
      )}
    </Result>
  </div>
)

export default ServerError
