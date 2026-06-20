import React, { Component, ErrorInfo, ReactNode } from "react"
import ServerError from "../pages/ServerError"

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
        <ServerError
          requestId={this.state.error?.message}
          onRetry={() => window.location.reload()}
        />
      )
    }

    return this.props.children
  }
}

export default ErrorBoundary
