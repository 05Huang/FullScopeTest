import React, { useState, useEffect } from 'react';
import { Card, Form, Input, Button, message, Divider, Typography, Row, Col, Alert, Space } from 'antd';
import { RobotOutlined, SaveOutlined } from '@ant-design/icons';
import { apiTestService } from '../services/apiTestService';

const { Title, Text } = Typography;

const Settings: React.FC = () => {
  const [form] = Form.useForm();
  const [loading, setLoading] = useState(false);
  const [globalAiConfig, setGlobalAiConfig] = useState<{
    base_url: string
    model: string
    api_key: string
    vision_base_url: string
    vision_model: string
    vision_api_key: string
  } | null>(null);

  useEffect(() => {
    apiTestService.getAiConfig()
      .then((res: any) => {
        if (res.code === 200 && res.data) {
          setGlobalAiConfig(res.data);
        }
      })
      .catch(err => console.error('Failed to load global AI config', err));

    const aiBaseUrl = localStorage.getItem('api-test-ai-base-url') || '';
    const aiModel = localStorage.getItem('api-test-ai-model') || '';
    const aiApiKey = localStorage.getItem('api-test-ai-api-key') || '';
    const aiVisionBaseUrl = localStorage.getItem('api-test-ai-vision-base-url') || '';
    const aiVisionModel = localStorage.getItem('api-test-ai-vision-model') || '';
    const aiVisionApiKey = localStorage.getItem('api-test-ai-vision-api-key') || '';

    form.setFieldsValue({
      aiBaseUrl,
      aiModel,
      aiApiKey,
      aiVisionBaseUrl,
      aiVisionModel,
      aiVisionApiKey
    });
  }, [form]);

  const handleSave = async (values: any) => {
    setLoading(true);
    try {
      const payload = {
        base_url: values.aiBaseUrl || '',
        model: values.aiModel || '',
        api_key: values.aiApiKey || '',
        vision_base_url: values.aiVisionBaseUrl || '',
        vision_model: values.aiVisionModel || '',
        vision_api_key: values.aiVisionApiKey || '',
      };
      const res = await apiTestService.saveAiConfig(payload);
      if (res.code !== 200) {
        message.error(res.message || '保存失败');
        return;
      }

      localStorage.setItem('api-test-ai-base-url', values.aiBaseUrl || '');
      localStorage.setItem('api-test-ai-model', values.aiModel || '');
      localStorage.setItem('api-test-ai-api-key', values.aiApiKey || '');
      localStorage.setItem('api-test-ai-vision-base-url', values.aiVisionBaseUrl || '');
      localStorage.setItem('api-test-ai-vision-model', values.aiVisionModel || '');
      localStorage.setItem('api-test-ai-vision-api-key', values.aiVisionApiKey || '');
      if (res.data) {
        setGlobalAiConfig(res.data);
      }
      
      message.success('设置保存成功，已写入后端 .env');
    } catch (error) {
      message.error('保存失败');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fst-page" style={{ maxWidth: 1000, margin: '0 auto' }}>
      <div className="fst-page-header fst-animate-in">
        <div>
          <h1 className="fst-page-title">系统设置</h1>
          <div className="fst-ios-card-subtitle">管理平台的基础配置和第三方服务接入参数</div>
        </div>
      </div>

      <div className="fst-ios-card fst-animate-in fst-animate-in-1">
        <div className="fst-ios-card-header">
          <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
            <div className="fst-stat-icon fst-stat-icon--primary"><RobotOutlined style={{ fontSize: 18 }} /></div>
            <div>
              <div className="fst-ios-card-title">AI 助手配置 (全局)</div>
              <div className="fst-ios-card-subtitle">配置大模型参数，全局生效</div>
            </div>
          </div>
        </div>

        <div style={{
          padding: '12px 16px',
          borderRadius: 'var(--fst-radius-lg)',
          background: 'rgba(45, 106, 100, 0.06)',
          border: '1px solid rgba(45, 106, 100, 0.12)',
          fontSize: 13,
          color: 'var(--fst-on-surface-variant)',
          marginBottom: 24,
          lineHeight: 1.6,
        }}>
          💡 在此处配置的大模型参数将全局生效，包括：AI 接口生成、Web 测试探索引擎、性能测试场景生成以及全局悬浮 Copilot。
        </div>

        <Form
          form={form}
          layout="vertical"
          onFinish={handleSave}
          initialValues={{
            aiBaseUrl: '',
            aiModel: '',
            aiApiKey: '',
            aiVisionBaseUrl: '',
            aiVisionModel: '',
            aiVisionApiKey: ''
          }}
        >
          <Row gutter={24}>
            <Col span={12}>
              <Form.Item
                label={<span style={{ fontWeight: 600, fontSize: 13 }}>Base URL</span>}
                name="aiBaseUrl"
                rules={[{ required: true, message: '请输入 Base URL' }]}
                tooltip="支持 OpenAI 兼容格式的 API 接口地址"
              >
                <Input placeholder={globalAiConfig?.base_url || "https://api.openai.com/v1"} />
              </Form.Item>
            </Col>
            <Col span={12}>
              <Form.Item
                label={<span style={{ fontWeight: 600, fontSize: 13 }}>模型名称 (Model)</span>}
                name="aiModel"
                rules={[{ required: true, message: '请输入模型名称' }]}
                tooltip="如 deepseek-chat, gpt-4o 等"
              >
                <Input placeholder={globalAiConfig?.model || "gpt-4o-mini"} />
              </Form.Item>
            </Col>
          </Row>

          <Row gutter={24}>
            <Col span={12}>
              <Form.Item
                label={<span style={{ fontWeight: 600, fontSize: 13 }}>API Key</span>}
                name="aiApiKey"
                rules={[{ required: true, message: '请输入 API Key' }]}
              >
                <Input.Password placeholder={globalAiConfig?.api_key || "sk-..."} />
              </Form.Item>
            </Col>
          </Row>

          <Row gutter={24}>
            <Col span={12}>
              <Form.Item
                label={<span style={{ fontWeight: 600, fontSize: 13 }}>视觉模型 Base URL</span>}
                name="aiVisionBaseUrl"
                rules={[{ required: true, message: '请输入视觉模型 Base URL' }]}
              >
                <Input placeholder={globalAiConfig?.vision_base_url || globalAiConfig?.base_url || "https://api.openai.com/v1"} />
              </Form.Item>
            </Col>
            <Col span={12}>
              <Form.Item
                label={<span style={{ fontWeight: 600, fontSize: 13 }}>视觉模型名称</span>}
                name="aiVisionModel"
                rules={[{ required: true, message: '请输入视觉模型名称' }]}
              >
                <Input placeholder={globalAiConfig?.vision_model || "gpt-4o-mini"} />
              </Form.Item>
            </Col>
          </Row>

          <Row gutter={24}>
            <Col span={12}>
              <Form.Item
                label={<span style={{ fontWeight: 600, fontSize: 13 }}>视觉模型 API Key</span>}
                name="aiVisionApiKey"
                rules={[{ required: true, message: '请输入视觉模型 API Key' }]}
              >
                <Input.Password placeholder={globalAiConfig?.vision_api_key || "sk-..."} />
              </Form.Item>
            </Col>
          </Row>

          <div style={{ borderTop: '1px solid var(--fst-outline-soft)', paddingTop: 20, marginTop: 8 }}>
            <Form.Item style={{ marginBottom: 0 }}>
              <Button type="primary" htmlType="submit" icon={<SaveOutlined />} loading={loading}>
                保存设置
              </Button>
            </Form.Item>
          </div>
        </Form>
      </div>
    </div>
  );
};

export default Settings;
