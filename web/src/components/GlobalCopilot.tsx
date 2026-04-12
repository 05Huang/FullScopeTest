import React, { useEffect, useMemo, useRef, useState } from 'react';
import { Button, Input, Card, Space, Avatar, Typography, Tooltip } from 'antd';
import { 
  UserOutlined, 
  SendOutlined, 
  CloseOutlined, 
  SettingOutlined 
} from '@ant-design/icons';
import ReactMarkdown from 'react-markdown';
import api, { ApiResponse } from '../services/api';

const { Text } = Typography;

interface Message {
  id: string;
  role: 'user' | 'assistant' | 'system';
  content: string;
  status?: 'pending' | 'done' | 'error';
}

const AppBrandMark = ({ size = 22 }: { size?: number }) => (
  <svg
    width={size}
    height={size}
    viewBox="0 0 64 64"
    style={{ display: 'block' }}
    aria-hidden="true"
    focusable="false"
  >
    <defs>
      <linearGradient id="fstAppBrandG" x1="10" y1="8" x2="56" y2="56" gradientUnits="userSpaceOnUse">
        <stop offset="0" stopColor="#5FA59B" />
        <stop offset="0.6" stopColor="#3D6E66" />
        <stop offset="1" stopColor="#D7B56D" />
      </linearGradient>
      <filter id="fstAppGlow" x="-40%" y="-40%" width="180%" height="180%">
        <feGaussianBlur stdDeviation="3.2" result="blur" />
        <feColorMatrix
          in="blur"
          type="matrix"
          values="1 0 0 0 0  0 1 0 0 0  0 0 1 0 0  0 0 0 0.85 0"
          result="glow"
        />
        <feMerge>
          <feMergeNode in="glow" />
          <feMergeNode in="SourceGraphic" />
        </feMerge>
      </filter>
    </defs>
    <path
      d="M18 16h28c1.7 0 3 1.3 3 3v7c0 1.7-1.3 3-3 3H25.2v6.2H42c1.7 0 3 1.3 3 3v7c0 1.7-1.3 3-3 3H18c-1.7 0-3-1.3-3-3V19c0-1.7 1.3-3 3-3Z"
      fill="url(#fstAppBrandG)"
      filter="url(#fstAppGlow)"
    />
    <path d="M22 23h24" stroke="rgba(255,255,255,0.55)" strokeWidth="2" strokeLinecap="round" />
    <path d="M22 45h18" stroke="rgba(255,255,255,0.38)" strokeWidth="2" strokeLinecap="round" />
  </svg>
);

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
  const createMessageId = () => {
    const cryptoId = globalThis.crypto?.randomUUID?.();
    if (cryptoId) return cryptoId;
    return `msg_${Date.now()}_${Math.random().toString(16).slice(2)}`;
  };

  const [messages, setMessages] = useState<Message[]>([
    {
      id: 'init',
      role: 'assistant',
      content: '你好！我是你的 AI 测试平台助手。你可以让我帮你创建性能测试任务，或者查询最近失败的 Web 测试记录。',
      status: 'done',
    },
  ]);
  const [inputValue, setInputValue] = useState('');
  const [loading, setLoading] = useState(false);
  const [showConfig, setShowConfig] = useState(false);
  const [nudgeOpen, setNudgeOpen] = useState(false);
  const [nudgeText, setNudgeText] = useState('');
  const [reduceMotion, setReduceMotion] = useState(false);
  const [hasInteracted, setHasInteracted] = useState(false);
  const [isSmallScreen, setIsSmallScreen] = useState(false);
  const [panelPos, setPanelPos] = useState<{ x: number; y: number } | null>(null);
  
  // AI Config (from localStorage)
  const [aiBaseUrl, setAiBaseUrl] = useState(() => localStorage.getItem('api-test-ai-base-url') || '');
  const [aiModel, setAiModel] = useState(() => localStorage.getItem('api-test-ai-model') || '');
  const [aiApiKey, setAiApiKey] = useState(() => localStorage.getItem('api-test-ai-api-key') || '');
  const [aiVisionBaseUrl, setAiVisionBaseUrl] = useState(() => localStorage.getItem('api-test-ai-vision-base-url') || '');
  const [aiVisionModel, setAiVisionModel] = useState(() => localStorage.getItem('api-test-ai-vision-model') || '');
  const [aiVisionApiKey, setAiVisionApiKey] = useState(() => localStorage.getItem('api-test-ai-vision-api-key') || '');

  // Global Config Loading
  const [globalAiConfig, setGlobalAiConfig] = useState<{
    base_url: string
    model: string
    api_key: string
    vision_base_url: string
    vision_model: string
    vision_api_key: string
  } | null>(null);

  useEffect(() => {
    if (showConfig && !globalAiConfig) {
      api.get('/api-test/ai/config')
        .then((res: any) => {
          if (res.code === 200 && res.data) {
            setGlobalAiConfig(res.data);
          }
        })
        .catch(err => console.error('Failed to load global AI config', err));
    }
  }, [showConfig]);

  const messagesEndRef = useRef<HTMLDivElement>(null);
  const nudgeTimersRef = useRef<{ show?: number; hide?: number }>({});
  const nudgeShownCountRef = useRef(0);
  const panelDragRef = useRef<{
    active: boolean;
    pointerId: number | null;
    startClientX: number;
    startClientY: number;
    originX: number;
    originY: number;
    rafId: number | null;
    pending: { x: number; y: number } | null;
  }>({
    active: false,
    pointerId: null,
    startClientX: 0,
    startClientY: 0,
    originX: 0,
    originY: 0,
    rafId: null,
    pending: null,
  });
  const panelPosRef = useRef(panelPos);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    panelPosRef.current = panelPos;
  }, [panelPos]);

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

  useEffect(() => {
    if (typeof window === 'undefined' || !window.matchMedia) return;
    const mq = window.matchMedia('(max-width: 480px)');
    const setFromMq = () => setIsSmallScreen(Boolean(mq.matches));
    setFromMq();
    mq.addEventListener?.('change', setFromMq);
    return () => mq.removeEventListener?.('change', setFromMq);
  }, []);

  const clampPanelPos = (x: number, y: number) => {
    const margin = 18;
    const width = 420;
    const height = 640;
    const maxX = Math.max(margin, window.innerWidth - width - margin);
    const maxY = Math.max(margin, window.innerHeight - height - margin);
    return {
      x: Math.min(maxX, Math.max(margin, x)),
      y: Math.min(maxY, Math.max(margin, y)),
    };
  };

  const ensurePanelPos = () => {
    if (typeof window === 'undefined') return;
    if (isSmallScreen) return;
    if (panelPosRef.current) return;
    let next: { x: number; y: number } | null = null;
    try {
      const raw = sessionStorage.getItem('fst-copilot-panel-pos');
      if (raw) {
        const parsed = JSON.parse(raw);
        if (typeof parsed?.x === 'number' && typeof parsed?.y === 'number') {
          next = clampPanelPos(parsed.x, parsed.y);
        }
      }
    } catch {}
    if (!next) {
      next = clampPanelPos(window.innerWidth - 420 - 28, window.innerHeight - 640 - 28);
    }
    setPanelPos(next);
  };

  useEffect(() => {
    if (!panelMounted || !isOpen || isSmallScreen) return;
    ensurePanelPos();
  }, [panelMounted, isOpen, isSmallScreen]);

  useEffect(() => {
    if (!panelMounted || isSmallScreen) return;
    const onResize = () => {
      if (!panelPosRef.current) return;
      setPanelPos(clampPanelPos(panelPosRef.current.x, panelPosRef.current.y));
    };
    window.addEventListener('resize', onResize);
    return () => window.removeEventListener('resize', onResize);
  }, [panelMounted, isSmallScreen]);

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

    const userMsg: Message = { id: createMessageId(), role: 'user', content: inputValue.trim(), status: 'done' };
    const pendingAssistantId = createMessageId();
    const pendingAssistantMsg: Message = { id: pendingAssistantId, role: 'assistant', content: '', status: 'pending' };

    const newMessages = [...messages, userMsg, pendingAssistantMsg];
    setMessages(newMessages);
    setInputValue('');
    setLoading(true);
    setHasInteracted(true);

    try {
      const res = (await api.post('/copilot/chat', {
        messages: newMessages
          .filter((m) => (m.role === 'user' || m.role === 'assistant') && m.status !== 'pending')
          .map((m) => ({ role: m.role, content: m.content })),
        base_url: aiBaseUrl,
        model: aiModel,
        api_key: aiApiKey,
        vision_base_url: aiVisionBaseUrl,
        vision_model: aiVisionModel,
        vision_api_key: aiVisionApiKey
      })) as unknown as ApiResponse<{ role: Message['role']; content: string }>;
      
      if (res?.code === 200 && res?.data) {
        setMessages((prev) =>
          prev.map((m) =>
            m.id === pendingAssistantId
              ? { ...m, role: 'assistant', content: res.data.content ?? '', status: 'done' }
              : m
          )
        );
      } else {
        setMessages((prev) =>
          prev.map((m) =>
            m.id === pendingAssistantId
              ? { ...m, role: 'assistant', content: `请求失败: ${res?.message || '未知错误'}`, status: 'error' }
              : m
          )
        );
      }
    } catch (error: any) {
      setMessages((prev) =>
        prev.map((m) =>
          m.id === pendingAssistantId
            ? { ...m, role: 'assistant', content: `网络错误: ${error?.message || '未知错误'}`, status: 'error' }
            : m
        )
      );
    } finally {
      setLoading(false);
    }
  };

  const saveConfig = () => {
    localStorage.setItem('api-test-ai-base-url', aiBaseUrl);
    localStorage.setItem('api-test-ai-model', aiModel);
    localStorage.setItem('api-test-ai-api-key', aiApiKey);
    localStorage.setItem('api-test-ai-vision-base-url', aiVisionBaseUrl);
    localStorage.setItem('api-test-ai-vision-model', aiVisionModel);
    localStorage.setItem('api-test-ai-vision-api-key', aiVisionApiKey);
    setShowConfig(false);
  };

  const handleOpen = () => {
    setHasInteracted(true);
    setIsOpen(true);
    hideNudge();
    ensurePanelPos();
  };

  const handleClose = () => {
    setIsOpen(false);
    setShowConfig(false);
  };

  const handlePanelPointerDown: React.PointerEventHandler<HTMLDivElement> = (e) => {
    if (isSmallScreen) return;
    const target = e.target as HTMLElement | null;
    if (target?.closest('.fst-copilot-header-actions')) return;
    if (!panelPosRef.current) ensurePanelPos();
    if (!panelPosRef.current) return;

    setHasInteracted(true);
    const state = panelDragRef.current;
    state.active = true;
    state.pointerId = e.pointerId;
    state.startClientX = e.clientX;
    state.startClientY = e.clientY;
    state.originX = panelPosRef.current.x;
    state.originY = panelPosRef.current.y;

    (e.currentTarget as HTMLElement).setPointerCapture?.(e.pointerId);

    const onMove = (ev: PointerEvent) => {
      if (!state.active) return;
      const dx = ev.clientX - state.startClientX;
      const dy = ev.clientY - state.startClientY;
      const next = clampPanelPos(state.originX + dx, state.originY + dy);
      state.pending = next;
      if (state.rafId) return;
      state.rafId = window.requestAnimationFrame(() => {
        state.rafId = null;
        if (state.pending) setPanelPos(state.pending);
        state.pending = null;
      });
    };

    const onUp = (ev: PointerEvent) => {
      state.active = false;
      state.pointerId = null;
      window.removeEventListener('pointermove', onMove);
      window.removeEventListener('pointerup', onUp);
      try {
        const current = panelPosRef.current;
        if (current) sessionStorage.setItem('fst-copilot-panel-pos', JSON.stringify(current));
      } catch {}
      (e.currentTarget as HTMLElement).releasePointerCapture?.(ev.pointerId);
    };

    window.addEventListener('pointermove', onMove);
    window.addEventListener('pointerup', onUp);
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
            <div className="fst-copilot-header" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }} onPointerDown={handlePanelPointerDown}>
              <Space>
                <span className="fst-copilot-header-icon" aria-hidden="true">
                  <AppBrandMark size={20} />
                </span>
                <span className="fst-copilot-header-title">AI Copilot</span>
              </Space>
              <Space className="fst-copilot-header-actions">
                <Button type="text" icon={<SettingOutlined />} onClick={() => setShowConfig(!showConfig)} />
                <Button type="text" icon={<CloseOutlined />} onClick={handleClose} />
              </Space>
            </div>
          }
          className={`fst-copilot-panel ${isOpen ? 'is-open' : 'is-closing'}`}
          style={{
            position: 'fixed',
            left: isSmallScreen ? undefined : (panelPos?.x ?? 28),
            top: isSmallScreen ? undefined : (panelPos?.y ?? 28),
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
                <Input addonBefore="Base URL" placeholder={globalAiConfig?.base_url || "https://api.openai.com/v1"} value={aiBaseUrl} onChange={e => setAiBaseUrl(e.target.value)} />
                <Input addonBefore="Model" placeholder={globalAiConfig?.model || "gpt-4o-mini"} value={aiModel} onChange={e => setAiModel(e.target.value)} />
                <Input.Password addonBefore="API Key" placeholder={globalAiConfig?.api_key || "请输入模型提供商的 API Key"} value={aiApiKey} onChange={e => setAiApiKey(e.target.value)} />
                <Input addonBefore="Vision URL" placeholder={globalAiConfig?.vision_base_url || globalAiConfig?.base_url || "https://api.openai.com/v1"} value={aiVisionBaseUrl} onChange={e => setAiVisionBaseUrl(e.target.value)} />
                <Input addonBefore="Vision Model" placeholder={globalAiConfig?.vision_model || "gpt-4o-mini"} value={aiVisionModel} onChange={e => setAiVisionModel(e.target.value)} />
                <Input.Password addonBefore="Vision Key" placeholder={globalAiConfig?.vision_api_key || "请输入视觉模型 API Key"} value={aiVisionApiKey} onChange={e => setAiVisionApiKey(e.target.value)} />
                <Button type="primary" block onClick={saveConfig}>保存配置</Button>
              </Space>
            </div>
          ) : (
            <>
              {/* 消息列表区 */}
              <div className="fst-copilot-messages">
                {messages.filter(m => m.role !== 'system').map((msg, index) => (
                  <div 
                    key={msg.id || index} 
                    style={{ 
                      display: 'flex', 
                      justifyContent: msg.role === 'user' ? 'flex-end' : 'flex-start',
                      alignItems: 'flex-start',
                      gap: 8
                    }}
                  >
                    {msg.role === 'assistant' && (
                      <Avatar
                        shape="square"
                        icon={<AppBrandMark size={18} />}
                        className="fst-copilot-avatar-ai"
                        style={{
                          background: 'rgba(255, 255, 255, 0.56)',
                          border: '1px solid rgba(15, 45, 40, 0.12)',
                          boxShadow: '0 10px 22px rgba(15, 45, 40, 0.10)',
                          borderRadius: 12,
                        }}
                      />
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
                        msg.status === 'pending' ? (
                          <div role="status" aria-label="Copilot 正在思考" style={{ display: 'flex', alignItems: 'center', gap: 6, padding: 2 }}>
                            <span className="fst-copilot-typing-dot" />
                            <span className="fst-copilot-typing-dot" />
                            <span className="fst-copilot-typing-dot" />
                          </div>
                        ) : (
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
                                    fontFamily:
                                      'ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace',
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
                        )
                      ) : (
                        msg.content
                      )}
                    </div>
                    {msg.role === 'user' && (
                      <Avatar icon={<UserOutlined />} style={{ backgroundColor: '#D7B56D' }} />
                    )}
                  </div>
                ))}
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
