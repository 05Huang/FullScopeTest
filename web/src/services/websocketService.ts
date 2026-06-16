/**
 * WebSocket 客户端服务
 *
 * 提供自动连接/重连（指数退避）、心跳保活、消息类型分发。
 * 替代轮询机制，实现性能测试实时数据、告警推送等功能。
 */

type MessageHandler = (data: any) => void
type StatusHandler = (connected: boolean) => void

class WebSocketService {
  private ws: WebSocket | null = null
  private url: string = ''
  private reconnectAttempts: number = 0
  private maxReconnectAttempts: number = 10
  private reconnectTimer: ReturnType<typeof setTimeout> | null = null
  private heartbeatTimer: ReturnType<typeof setInterval> | null = null
  private heartbeatInterval: number = 30000 // 30 秒
  private handlers: Map<string, Set<MessageHandler>> = new Map()
  private statusHandlers: Set<StatusHandler> = new Set()
  private _connected: boolean = false

  /** 获取连接状态 */
  get connected(): boolean {
    return this._connected
  }

  /** 连接到 WebSocket 服务器 */
  connect(token?: string): void {
    if (this.ws && (this.ws.readyState === WebSocket.OPEN || this.ws.readyState === WebSocket.CONNECTING)) {
      return
    }

    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:'
    const base = `${protocol}//${window.location.host}/ws`
    this.url = token ? `${base}?token=${token}` : base

    try {
      this.ws = new WebSocket(this.url)
      this.ws.onopen = this.onOpen.bind(this)
      this.ws.onmessage = this.onMessage.bind(this)
      this.ws.onclose = this.onClose.bind(this)
      this.ws.onerror = this.onError.bind(this)
    } catch {
      this.scheduleReconnect()
    }
  }

  /** 断开连接 */
  disconnect(): void {
    this.clearTimers()
    this.reconnectAttempts = this.maxReconnectAttempts // 阻止自动重连
    if (this.ws) {
      this.ws.close()
      this.ws = null
    }
    this.setConnected(false)
  }

  /** 订阅消息类型 */
  on(type: string, handler: MessageHandler): () => void {
    if (!this.handlers.has(type)) {
      this.handlers.set(type, new Set())
    }
    this.handlers.get(type)!.add(handler)
    return () => this.handlers.get(type)?.delete(handler)
  }

  /** 监听连接状态变化 */
  onStatusChange(handler: StatusHandler): () => void {
    this.statusHandlers.add(handler)
    return () => this.statusHandlers.delete(handler)
  }

  /** 发送消息 */
  send(type: string, data: any): void {
    if (this.ws && this.ws.readyState === WebSocket.OPEN) {
      this.ws.send(JSON.stringify({ type, data }))
    }
  }

  private onOpen(): void {
    this.reconnectAttempts = 0
    this.setConnected(true)
    this.startHeartbeat()
  }

  private onMessage(event: MessageEvent): void {
    try {
      const msg = JSON.parse(event.data)
      const type = msg.type || 'unknown'
      const handlers = this.handlers.get(type)
      if (handlers) {
        handlers.forEach((h) => h(msg.data || msg))
      }
      // 通配符处理器
      const allHandlers = this.handlers.get('*')
      if (allHandlers) {
        allHandlers.forEach((h) => h(msg))
      }
    } catch {
      // 非 JSON 消息忽略
    }
  }

  private onClose(): void {
    this.setConnected(false)
    this.clearTimers()
    this.scheduleReconnect()
  }

  private onError(): void {
    this.setConnected(false)
  }

  private setConnected(value: boolean): void {
    this._connected = value
    this.statusHandlers.forEach((h) => h(value))
  }

  private startHeartbeat(): void {
    this.heartbeatTimer = setInterval(() => {
      if (this.ws && this.ws.readyState === WebSocket.OPEN) {
        this.ws.send(JSON.stringify({ type: 'ping' }))
      }
    }, this.heartbeatInterval)
  }

  private scheduleReconnect(): void {
    if (this.reconnectAttempts >= this.maxReconnectAttempts) return
    const delay = Math.min(1000 * Math.pow(2, this.reconnectAttempts), 30000)
    this.reconnectTimer = setTimeout(() => {
      this.reconnectAttempts++
      this.connect()
    }, delay)
  }

  private clearTimers(): void {
    if (this.reconnectTimer) {
      clearTimeout(this.reconnectTimer)
      this.reconnectTimer = null
    }
    if (this.heartbeatTimer) {
      clearInterval(this.heartbeatTimer)
      this.heartbeatTimer = null
    }
  }
}

// 全局单例
export const wsService = new WebSocketService()
export default wsService
