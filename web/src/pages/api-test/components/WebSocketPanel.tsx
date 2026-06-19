/**
 * WebSocket 测试面板组件
 */
import { useState, useRef, useCallback, useEffect } from "react"
import { Card, Input, Button, Space, Tag, Typography, Switch, message } from "antd"
import { SendOutlined, DisconnectOutlined, LinkOutlined, ClearOutlined } from "@ant-design/icons"
import { useTranslation } from "react-i18next"

const { Text } = Typography
const { TextArea } = Input

interface WsMessage { id: number; type: "sent" | "received" | "system"; content: string; timestamp: Date }

interface WebSocketPanelProps { defaultUrl?: string }

const WebSocketPanel: React.FC<WebSocketPanelProps> = ({ defaultUrl = "ws://localhost:8080/ws" }) => {
  const { t } = useTranslation()
  const [url, setUrl] = useState(defaultUrl)
  const [connected, setConnected] = useState(false)
  const [connecting, setConnecting] = useState(false)
  const [messageText, setMessageText] = useState("")
  const [messages, setMessages] = useState<WsMessage[]>([])
  const [autoScroll, setAutoScroll] = useState(true)
  const wsRef = useRef<WebSocket | null>(null)
  const msgIdRef = useRef(0)
  const listRef = useRef<HTMLDivElement>(null)

  const addMessage = useCallback((type: WsMessage["type"], content: string) => {
    setMessages(prev => [...prev, { id: ++msgIdRef.current, type, content, timestamp: new Date() }])
  }, [])

  const connect = useCallback(() => {
    if (!url) { message.warning("请输入 WebSocket 地址"); return }
    setConnecting(true)
    try {
      const ws = new WebSocket(url)
      ws.onopen = () => { setConnected(true); setConnecting(false); addMessage("system", "已连接: " + url) }
      ws.onmessage = (e) => { addMessage("received", typeof e.data === "string" ? e.data : JSON.stringify(e.data)) }
      ws.onerror = () => { addMessage("system", "连接错误"); setConnecting(false) }
      ws.onclose = (e) => {
        setConnected(false)
        addMessage("system", "已断开 (code: " + e.code + ")")
      }
      wsRef.current = ws
    } catch (err) { addMessage("system", "连接失败: " + String(err)); setConnecting(false) }
  }, [url, addMessage])

  const disconnect = useCallback(() => { wsRef.current?.close(); wsRef.current = null; setConnected(false) }, [])
  const sendMessage = useCallback(() => {
    if (!wsRef.current || !connected || !messageText.trim()) return
    wsRef.current.send(messageText); addMessage("sent", messageText); setMessageText("")
  }, [connected, messageText, addMessage])

  useEffect(() => { if (autoScroll && listRef.current) listRef.current.scrollTop = listRef.current.scrollHeight }, [messages, autoScroll])
  useEffect(() => () => { wsRef.current?.close() }, [])

  return (
    <Card size="small" title={<Space><Text strong>WebSocket 测试</Text>{connected && <Tag color="success">已连接</Tag>}</Space>}>
      <Space style={{ marginBottom: 8, width: "100%" }}>
        <Input placeholder="ws://localhost:8080/ws" value={url} onChange={e => setUrl(e.target.value)} style={{ flex: 1 }} disabled={connected} />
        {connected ? (
          <Button danger icon={<DisconnectOutlined />} onClick={disconnect}>断开</Button>
        ) : (
          <Button type="primary" icon={<LinkOutlined />} onClick={connect} loading={connecting}>连接</Button>
        )}
      </Space>
      <div ref={listRef} style={{ height: 200, overflow: "auto", background: "#fafafa", borderRadius: 4, padding: 8, marginBottom: 8 }}>
        {messages.length === 0 ? <Text type="secondary" style={{ fontSize: 12 }}>连接后消息将显示在这里</Text> : messages.map(msg => (
          <div key={msg.id} style={{ marginBottom: 4 }}>
            <Tag color={msg.type === "sent" ? "blue" : msg.type === "received" ? "green" : "default"} style={{ fontSize: 11 }}>
              {msg.type === "sent" ? "发送" : msg.type === "received" ? "接收" : "系统"}</Tag>
            <Text style={{ fontSize: 12, wordBreak: "break-all" }}>{msg.content}</Text>
            <Text type="secondary" style={{ fontSize: 10, marginLeft: 4 }}>{msg.timestamp.toLocaleTimeString()}</Text>
          </div>
        ))}
      </div>
      <Space style={{ width: "100%" }}>
        <TextArea placeholder="输入消息" value={messageText} onChange={e => setMessageText(e.target.value)} rows={2} style={{ flex: 1 }}
          onPressEnter={e => { if (!e.shiftKey) { e.preventDefault(); sendMessage() } }} disabled={!connected} />
        <Button type="primary" icon={<SendOutlined />} onClick={sendMessage} disabled={!connected}>发送</Button>
      </Space>
      <div style={{ marginTop: 4 }}><Space>
        <Switch size="small" checked={autoScroll} onChange={setAutoScroll} /><Text style={{ fontSize: 11 }}>自动滚动</Text>
        <Button size="small" type="text" icon={<ClearOutlined />} onClick={() => setMessages([])}>清空</Button>
      </Space></div>
    </Card>
  )
}

export default WebSocketPanel
