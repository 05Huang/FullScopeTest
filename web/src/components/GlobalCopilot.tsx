import React, { useState, useEffect, useMemo, useRef } from 'react';
import { Button, Input, Card, Space, Avatar, Typography, Tooltip } from 'antd';
import { 
  RobotOutlined, 
  UserOutlined, 
  SendOutlined, 
  CloseOutlined, 
  SettingOutlined 
} from '@ant-design/icons';
import ReactMarkdown from 'react-markdown';
import api, { ApiResponse } from '../services/api';

const { Text } = Typography;

interface Message {
  role: 'user' | 'assistant' | 'system';
  content: string;
}

const normalizeMarkdownLineBreaks = (text: string) => {
  const lines = String(text ?? '').split('\n');
  let inFence = false;
  const out: string[] = [];

  for (const line of lines) {
    const trimmed = line.trimStart();
    if (trimmed.startsWith('```')) {
      inFence = !inFence;
      out.push(line);
      continue;
    }
    out.push(inFence ? line : `${line}  `);
  }

  return out.join('\n');
};

const GlobalCopilot: React.FC = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [panelMounted, setPanelMounted] = useState(false);
  const [messages, setMessages] = useState<Message[]>([
    { role: 'assistant', content: '你好！我是你的 AI 测试平台助手。你可以让我帮你创建性能测试任务，或者查询最近失败的 Web 测试记录。' }
  ]);
  const [inputValue, setInputValue] = useState('');
  const [loading, setLoading] = useState(false);
  const [showConfig, setShowConfig] = useState(false);
  const [nudgeOpen, setNudgeOpen] = useState(false);
  const [nudgeText, setNudgeText] = useState('');
  const [reduceMotion, setReduceMotion] = useState(false);
  const [hasInteracted, setHasInteracted] = useState(false);
  
  // AI Config (from localStorage)
  const [aiBaseUrl, setAiBaseUrl] = useState(() => localStorage.getItem('api-test-ai-base-url') || 'https://api.openai.com/v1');
  const [aiModel, setAiModel] = useState(() => localStorage.getItem('api-test-ai-model') || 'gpt-4o-mini');
  const [aiApiKey, setAiApiKey] = useState(() => localStorage.getItem('api-test-ai-api-key') || '');

  const messagesEndRef = useRef<HTMLDivElement>(null);
  const nudgeTimersRef = useRef<{ show?: number; hide?: number }>({});
  const nudgeShownCountRef = useRef(0);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    if (isOpen) {
      scrollToBottom();
    }
  }, [messages, isOpen]);

  useEffect(() => {
    if (isOpen) {
      setPanelMounted(true);
      return;
    }
    if (!panelMounted) return;
    const t = window.setTimeout(() => setPanelMounted(false), 180);
    return () => window.clearTimeout(t);
  }, [isOpen, panelMounted]);

  useEffect(() => {
    if (typeof window === 'undefined' || !window.matchMedia) return;
    const mq = window.matchMedia('(prefers-reduced-motion: reduce)');
    const setFromMq = () => setReduceMotion(Boolean(mq.matches));
    setFromMq();
    mq.addEventListener?.('change', setFromMq);
    return () => mq.removeEventListener?.('change', setFromMq);
  }, []);

  const nudgeCandidates = useMemo(
    () => [
      '需要我帮你查看最近失败的 Web 测试记录吗？',
      '要不要我帮你创建一个性能测试任务？',
      '需要我帮你解释这页数据的含义吗？',
      '想快速定位问题？把报错信息发我就行。',
    ],
    []
  );

  const clearNudgeTimers = () => {
    if (nudgeTimersRef.current.show) window.clearTimeout(nudgeTimersRef.current.show);
    if (nudgeTimersRef.current.hide) window.clearTimeout(nudgeTimersRef.current.hide);
    nudgeTimersRef.current = {};
  };

  const hideNudge = (dismiss?: boolean) => {
    setNudgeOpen(false);
    if (dismiss) {
      try {
        sessionStorage.setItem('fst-copilot-nudge-dismissed', '1');
      } catch {}
    }
  };

  useEffect(() => {
    if (reduceMotion) {
      clearNudgeTimers();
      return;
    }
    if (isOpen) {
      clearNudgeTimers();
      setNudgeOpen(false);
      return;
    }
    if (hasInteracted) {
      clearNudgeTimers();
      setNudgeOpen(false);
      return;
    }
    let dismissed = false;
    try {
      dismissed = sessionStorage.getItem('fst-copilot-nudge-dismissed') === '1';
    } catch {}
    if (dismissed) return;

    const scheduleNext = () => {
      if (nudgeShownCountRef.current >= 3) return;
      const delay = 45000 + Math.floor(Math.random() * 45000);
      nudgeTimersRef.current.show = window.setTimeout(() => {
        if (isOpen) return;
        const text = nudgeCandidates[Math.floor(Math.random() * nudgeCandidates.length)];
        setNudgeText(text);
        setNudgeOpen(true);
        nudgeShownCountRef.current += 1;
        nudgeTimersRef.current.hide = window.setTimeout(() => {
          setNudgeOpen(false);
          scheduleNext();
        }, 7000);
      }, delay);
    };

    scheduleNext();
    return () => clearNudgeTimers();
  }, [reduceMotion, isOpen, hasInteracted, nudgeCandidates]);

  const handleSend = async () => {
    if (!inputValue.trim() || loading) return;

    const userMsg: Message = { role: 'user', content: inputValue.trim() };
    const newMessages = [...messages, userMsg];
    setMessages(newMessages);
    setInputValue('');
    setLoading(true);
    setHasInteracted(true);

    try {
      const res = (await api.post('/copilot/chat', {
        messages: newMessages.filter(m => m.role === 'user' || m.role === 'assistant'),
        base_url: aiBaseUrl,
        model: aiModel,
        api_key: aiApiKey
      })) as unknown as ApiResponse<Message>;
      
      if (res?.code === 200 && res?.data) {
        setMessages(prev => [...prev, res.data]);
      } else {
        setMessages(prev => [...prev, { role: 'assistant', content: `请求失败: ${res?.message || '未知错误'}` }]);
      }
    } catch (error: any) {
      setMessages(prev => [...prev, { role: 'assistant', content: `网络错误: ${error.message || '未知错误'}` }]);
    } finally {
      setLoading(false);
    }
  };

  const saveConfig = () => {
    localStorage.setItem('api-test-ai-base-url', aiBaseUrl);
    localStorage.setItem('api-test-ai-model', aiModel);
    localStorage.setItem('api-test-ai-api-key', aiApiKey);
    setShowConfig(false);
  };

  const handleOpen = () => {
    setHasInteracted(true);
    setIsOpen(true);
    hideNudge();
  };

  const handleClose = () => {
    setIsOpen(false);
    setShowConfig(false);
  };

  return (
    <>
      {/* 悬浮按钮 */}
      {!isOpen && (
        <>
          <Tooltip title="AI 测试助手" placement="left">
            <button className="fst-copilot-sprite" type="button" onClick={handleOpen} aria-label="打开 AI Copilot">
              <span className="fst-copilot-sprite-glow" aria-hidden="true" />
              <span className="fst-copilot-sprite-spark s1" aria-hidden="true" />
              <span className="fst-copilot-sprite-spark s2" aria-hidden="true" />
              <span className="fst-copilot-sprite-spark s3" aria-hidden="true" />
              <svg viewBox="0 0 64 64" className="fst-copilot-sprite-svg" aria-hidden="true">
                <defs>
                  <linearGradient id="fstCopilotG" x1="10" y1="10" x2="54" y2="54" gradientUnits="userSpaceOnUse">
                    <stop offset="0" stopColor="#5FA59B" />
                    <stop offset="0.6" stopColor="#3D6E66" />
                    <stop offset="1" stopColor="#D7B56D" />
                  </linearGradient>
                </defs>
                <path
                  d="M32 9c9.2 0 16.9 7.6 16.9 16.9 0 6.4-2.7 10.7-6.4 15.3-2 2.5-3.8 5.3-4.6 9.2-.3 1.5-1.6 2.7-3.2 2.7h-5.4c-1.6 0-2.9-1.2-3.2-2.7-.8-3.9-2.6-6.7-4.6-9.2-3.7-4.6-6.4-8.9-6.4-15.3C15.1 16.6 22.8 9 32 9z"
                  fill="url(#fstCopilotG)"
                  opacity="0.92"
                />
                <path
                  d="M20.5 26.2c4.2-4.7 11.7-6.6 19-3.7 2.2.9 4.2 2.2 5.9 4.1"
                  fill="none"
                  stroke="rgba(255,255,255,0.75)"
                  strokeWidth="3.4"
                  strokeLinecap="round"
                />
                <circle cx="26.8" cy="32.2" r="2.3" fill="rgba(255,255,255,0.9)" />
                <circle cx="37.2" cy="32.2" r="2.3" fill="rgba(255,255,255,0.9)" />
                <path
                  d="M28.5 38.5c2.1 2.3 4.9 2.3 7 0"
                  fill="none"
                  stroke="rgba(255,255,255,0.9)"
                  strokeWidth="3.2"
                  strokeLinecap="round"
                />
                <path
                  d="M26 54.2c1.8 1.4 3.9 2.2 6 2.2s4.2-.8 6-2.2"
                  fill="none"
                  stroke="rgba(15,45,40,0.22)"
                  strokeWidth="3"
                  strokeLinecap="round"
                />
              </svg>
            </button>
          </Tooltip>

          {nudgeOpen && (
            <div className="fst-copilot-nudge" role="dialog" aria-label="Copilot 提示">
              <div className="fst-copilot-nudge-bubble">
                <button
                  type="button"
                  className="fst-copilot-nudge-close"
                  onClick={() => hideNudge(true)}
                  aria-label="关闭提示"
                >
                  <CloseOutlined />
                </button>
                <div className="fst-copilot-nudge-title">
                  <span className="fst-copilot-nudge-dot" aria-hidden="true" />
                  <span>需要我帮忙吗？</span>
                </div>
                <div className="fst-copilot-nudge-text">{nudgeText}</div>
                <div className="fst-copilot-nudge-actions">
                  <button type="button" className="fst-copilot-nudge-primary" onClick={handleOpen}>
                    打开 Copilot
                  </button>
                  <button type="button" className="fst-copilot-nudge-secondary" onClick={() => hideNudge(true)}>
                    暂不需要
                  </button>
                </div>
              </div>
            </div>
          )}
        </>
      )}

      {/* 聊天窗口 */}
      {panelMounted && (
        <Card
          title={
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <Space>
                <span className="fst-copilot-header-icon" aria-hidden="true">
                  <RobotOutlined />
                </span>
                <span className="fst-copilot-header-title">AI Copilot</span>
              </Space>
              <Space>
                <Button type="text" icon={<SettingOutlined />} onClick={() => setShowConfig(!showConfig)} />
                <Button type="text" icon={<CloseOutlined />} onClick={handleClose} />
              </Space>
            </div>
          }
          className={`fst-copilot-panel ${isOpen ? 'is-open' : 'is-closing'}`}
          style={{
            position: 'fixed',
            bottom: 28,
            right: 28,
            width: 420,
            height: 640,
            display: 'flex',
            flexDirection: 'column',
            zIndex: 9999,
            borderRadius: 18,
            overflow: 'hidden'
          }}
          bodyStyle={{
            padding: 0,
            flex: 1,
            display: 'flex',
            flexDirection: 'column',
            height: 'calc(100% - 58px)'
          }}
        >
          {showConfig ? (
            <div className="fst-copilot-config">
              <div style={{ marginBottom: 16 }}><Text strong>Copilot 配置 (与 API 测试共享)</Text></div>
              <Space direction="vertical" style={{ width: '100%' }}>
                <Input addonBefore="Base URL" value={aiBaseUrl} onChange={e => setAiBaseUrl(e.target.value)} />
                <Input addonBefore="Model" value={aiModel} onChange={e => setAiModel(e.target.value)} />
                <Input.Password addonBefore="API Key" value={aiApiKey} onChange={e => setAiApiKey(e.target.value)} />
                <Button type="primary" block onClick={saveConfig}>保存配置</Button>
              </Space>
            </div>
          ) : (
            <>
              {/* 消息列表区 */}
              <div className="fst-copilot-messages">
                {messages.filter(m => m.role !== 'system').map((msg, index) => (
                  <div 
                    key={index} 
                    style={{ 
                      display: 'flex', 
                      justifyContent: msg.role === 'user' ? 'flex-end' : 'flex-start',
                      alignItems: 'flex-start',
                      gap: 8
                    }}
                  >
                    {msg.role === 'assistant' && (
                      <Avatar icon={<RobotOutlined />} className="fst-copilot-avatar-ai" />
                    )}
                    <div style={{
                      maxWidth: '80%',
                      padding: '10px 14px',
                      borderRadius: 12,
                      background: msg.role === 'user' ? 'rgba(61, 110, 102, 0.94)' : 'rgba(255, 255, 255, 0.78)',
                      color: msg.role === 'user' ? '#fff' : 'rgba(0, 0, 0, 0.88)',
                      boxShadow: msg.role === 'user' ? '0 10px 22px rgba(15, 45, 40, 0.18)' : '0 10px 22px rgba(15, 45, 40, 0.10)',
                      whiteSpace: msg.role === 'assistant' ? 'normal' : 'pre-wrap',
                      wordBreak: 'break-word',
                      border: msg.role === 'assistant' ? '1px solid rgba(15, 45, 40, 0.10)' : 'none',
                      backdropFilter: msg.role === 'assistant' ? 'blur(12px)' : 'none'
                    }}>
                      {msg.role === 'assistant' ? (
                        <ReactMarkdown
                          components={{
                            p: (props) => <p style={{ margin: 0 }} {...props} />,
                            ol: (props) => <ol style={{ margin: 0, paddingLeft: 20 }} {...props} />,
                            ul: (props) => <ul style={{ margin: 0, paddingLeft: 20 }} {...props} />,
                            li: (props) => <li style={{ margin: '4px 0' }} {...props} />,
                            a: ({ href, children, ...rest }) => (
                              <a href={href} target="_blank" rel="noreferrer" {...rest}>
                                {children}
                              </a>
                            ),
                            code: ({ children, ...rest }) => (
                              <code
                                style={{
                                  background: 'rgba(0,0,0,0.06)',
                                  borderRadius: 4,
                                  padding: '0 6px',
                                  fontFamily: 'ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace',
                                }}
                                {...rest}
                              >
                                {children}
                              </code>
                            ),
                            pre: (props) => (
                              <pre
                                style={{
                                  margin: 0,
                                  padding: 12,
                                  background: 'rgba(0,0,0,0.06)',
                                  borderRadius: 8,
                                  overflowX: 'auto',
                                }}
                                {...props}
                              />
                            ),
                          }}
                        >
                          {normalizeMarkdownLineBreaks(msg.content)}
                        </ReactMarkdown>
                      ) : (
                        msg.content
                      )}
                    </div>
                    {msg.role === 'user' && (
                      <Avatar icon={<UserOutlined />} style={{ backgroundColor: '#D7B56D' }} />
                    )}
                  </div>
                ))}
                {loading && (
                  <div style={{ display: 'flex', gap: 8, alignItems: 'center' }}>
                    <Avatar icon={<RobotOutlined />} className="fst-copilot-avatar-ai" />
                    <div className="fst-copilot-typing">
                      <span className="fst-copilot-typing-dot" />
                      <span className="fst-copilot-typing-dot" />
                      <span className="fst-copilot-typing-dot" />
                    </div>
                  </div>
                )}
                <div ref={messagesEndRef} />
              </div>

              {/* 输入区 */}
              <div className="fst-copilot-input">
                <Input
                  size="large"
                  placeholder="给 Copilot 发送指令..."
                  value={inputValue}
                  onChange={e => setInputValue(e.target.value)}
                  onPressEnter={handleSend}
                  disabled={loading}
                  suffix={
                    <Button 
                      type="text" 
                      icon={<SendOutlined style={{ color: inputValue.trim() ? '#3D6E66' : '#ccc' }} />} 
                      onClick={handleSend}
                      disabled={!inputValue.trim() || loading}
                    />
                  }
                  style={{ borderRadius: 20, borderColor: 'rgba(15, 45, 40, 0.14)', background: 'rgba(255, 255, 255, 0.78)', backdropFilter: 'blur(12px)' }}
                />
              </div>
            </>
          )}
        </Card>
      )}
    </>
  );
};

export default GlobalCopilot;
