import React, { Component, ErrorInfo, ReactNode } from "react"
import { Result, Button } from "antd"

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
    console.error("Uncaught error:", error, errorInfo)
  }

  public render() {
    if (this.state.hasError) {
      if (this.props.fallback) {
        return this.props.fallback
      }

      return (
        <Result
          status="error"
          title="页面出错了"
          subTitle={this.state.error?.message || "发生未知错误"}
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
        />
      )
    }

    return this.props.children
  }
}

export default ErrorBoundary
