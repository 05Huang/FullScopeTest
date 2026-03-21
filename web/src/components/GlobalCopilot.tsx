import React, { useState, useEffect, useRef } from 'react';
import { Button, Input, Card, Space, Avatar, Typography, Tooltip, ConfigProvider } from 'antd';
import { 
  RobotOutlined, 
  UserOutlined, 
  SendOutlined, 
  CloseOutlined, 
  SettingOutlined 
} from '@ant-design/icons';
import api from '../services/api';

const { Text } = Typography;

interface Message {
  role: 'user' | 'assistant' | 'system';
  content: string;
}

const GlobalCopilot: React.FC = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState<Message[]>([
    { role: 'assistant', content: '你好！我是你的 AI 测试平台助手。你可以让我帮你创建性能测试任务，或者查询最近失败的 Web 测试记录。' }
  ]);
  const [inputValue, setInputValue] = useState('');
  const [loading, setLoading] = useState(false);
  const [showConfig, setShowConfig] = useState(false);
  
  // AI Config (from localStorage)
  const [aiBaseUrl, setAiBaseUrl] = useState(() => localStorage.getItem('api-test-ai-base-url') || 'https://api.openai.com/v1');
  const [aiModel, setAiModel] = useState(() => localStorage.getItem('api-test-ai-model') || 'gpt-4o-mini');
  const [aiApiKey, setAiApiKey] = useState(() => localStorage.getItem('api-test-ai-api-key') || '');

  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    if (isOpen) {
      scrollToBottom();
    }
  }, [messages, isOpen]);

  const handleSend = async () => {
    if (!inputValue.trim() || loading) return;

    const userMsg: Message = { role: 'user', content: inputValue.trim() };
    const newMessages = [...messages, userMsg];
    setMessages(newMessages);
    setInputValue('');
    setLoading(true);

    try {
      const res = await api.post('/copilot/chat', {
        messages: newMessages.filter(m => m.role === 'user' || m.role === 'assistant'),
        base_url: aiBaseUrl,
        model: aiModel,
        api_key: aiApiKey
      });

      // 适配 Axios 拦截器后的响应结构
      // 如果使用了统一拦截器，res.data 已经被解包，或者 res 本身就是解包后的数据
      const responseData = res.data || res;
      
      if (responseData?.code === 200 && responseData?.data) {
        setMessages(prev => [...prev, responseData.data]);
      } else {
        setMessages(prev => [...prev, { role: 'assistant', content: `请求失败: ${responseData?.message || '未知错误'}` }]);
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

  return (
    <>
      {/* 悬浮按钮 */}
      {!isOpen && (
        <Tooltip title="AI 测试助手" placement="left">
          <Button
            type="primary"
            shape="circle"
            size="large"
            icon={<RobotOutlined style={{ fontSize: 24 }} />}
            style={{
              position: 'fixed',
              bottom: 40,
              right: 40,
              width: 60,
              height: 60,
              boxShadow: '0 8px 24px rgba(61, 110, 102, 0.25)',
              zIndex: 9999,
              background: 'linear-gradient(135deg, #5FA59B 0%, #3D6E66 100%)',
              border: 'none'
            }}
            onClick={() => setIsOpen(true)}
          />
        </Tooltip>
      )}

      {/* 聊天窗口 */}
      {isOpen && (
        <Card
          title={
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <Space>
                <RobotOutlined style={{ color: '#3D6E66', fontSize: 20 }} />
                <span style={{ fontWeight: 600, color: '#3D6E66' }}>AI Copilot</span>
              </Space>
              <Space>
                <Button type="text" icon={<SettingOutlined />} onClick={() => setShowConfig(!showConfig)} />
                <Button type="text" icon={<CloseOutlined />} onClick={() => setIsOpen(false)} />
              </Space>
            </div>
          }
          style={{
            position: 'fixed',
            bottom: 40,
            right: 40,
            width: 380,
            height: 600,
            display: 'flex',
            flexDirection: 'column',
            boxShadow: '0 8px 24px rgba(0,0,0,0.15)',
            zIndex: 9999,
            borderRadius: 12,
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
            <div style={{ padding: 16, flex: 1, background: '#fafafa' }}>
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
              <div style={{ 
                flex: 1, 
                padding: '16px', 
                overflowY: 'auto', 
                background: '#f0f2f5',
                display: 'flex',
                flexDirection: 'column',
                gap: 16
              }}>
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
                      <Avatar icon={<RobotOutlined />} style={{ background: 'linear-gradient(135deg, #5FA59B 0%, #3D6E66 100%)' }} />
                    )}
                    <div style={{
                      maxWidth: '80%',
                      padding: '10px 14px',
                      borderRadius: 12,
                      background: msg.role === 'user' ? '#3D6E66' : '#ffffff',
                      color: msg.role === 'user' ? '#fff' : 'rgba(0, 0, 0, 0.88)',
                      boxShadow: '0 2px 6px rgba(0,0,0,0.05)',
                      whiteSpace: 'pre-wrap',
                      wordBreak: 'break-word',
                      border: msg.role === 'assistant' ? '1px solid rgba(61, 110, 102, 0.1)' : 'none'
                    }}>
                      {msg.content}
                    </div>
                    {msg.role === 'user' && (
                      <Avatar icon={<UserOutlined />} style={{ backgroundColor: '#D7B56D' }} />
                    )}
                  </div>
                ))}
                {loading && (
                  <div style={{ display: 'flex', gap: 8, alignItems: 'center' }}>
                    <Avatar icon={<RobotOutlined />} style={{ background: 'linear-gradient(135deg, #5FA59B 0%, #3D6E66 100%)' }} />
                    <div style={{ padding: '10px', background: '#fff', borderRadius: 12, border: '1px solid rgba(61, 110, 102, 0.1)' }}>
                      <span className="loading-dots" style={{ color: '#3D6E66' }}>思考中...</span>
                    </div>
                  </div>
                )}
                <div ref={messagesEndRef} />
              </div>

              {/* 输入区 */}
              <div style={{ padding: '12px 16px', background: '#fff', borderTop: '1px solid #f0f0f0' }}>
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
                  style={{ borderRadius: 20, borderColor: 'rgba(61, 110, 102, 0.2)' }}
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