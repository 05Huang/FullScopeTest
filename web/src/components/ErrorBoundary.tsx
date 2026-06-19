import React, { Component, ErrorInfo, ReactNode } from "react"
import { Result, Button, Typography } from "antd"

const { Paragraph } = Typography

interface Props {
  children: ReactNode
  fallback?: ReactNode
}

interface State {
  hasError: boolean
  error?: Error
}

class ErrorBoundary extends Component<Props, State> {
  public state: State = {
    hasError: false
  }

  public static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error }
  }

  public componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    if (import.meta.env.DEV) {
      console.error("Uncaught error:", error, errorInfo)
    }
    // 生产环境可接入 Sentry 等错误追踪服务
  }

  public render() {
    if (this.state.hasError) {
      if (this.props.fallback) {
        return this.props.fallback
      }

      return (
        <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: '100vh' }}>
          <Result
            status="error"
            title="页面出错了"
            subTitle="渲染过程中发生错误，请尝试刷新页面"
            extra={[
              <Button
                type="primary"
                key="refresh"
                onClick={() => window.location.reload()}
              >
                刷新页面
              </Button>,
              <Button
                key="home"
                onClick={() => window.location.href = "/"}
              >
                返回首页
              </Button>,
            ]}
          >
            {this.state.error?.message && (
              <Paragraph
                copyable
                style={{
                  maxWidth: 480,
                  fontSize: 12,
                  color: '#999',
                  background: '#f5f5f5',
                  padding: 12,
                  borderRadius: 6,
                  wordBreak: 'break-all',
                }}
              >
                {this.state.error.message}
              </Paragraph>
            )}
          </Result>
        </div>
      )
    }

    return this.props.children
  }
}

export default ErrorBoundary
