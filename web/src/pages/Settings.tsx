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
    <div style={{ maxWidth: 1000, margin: '0 auto' }}>
      <div style={{ marginBottom: 24 }}>
        <Title level={4}>系统设置</Title>
        <Text type="secondary">管理平台的基础配置和第三方服务接入参数</Text>
      </div>

      <Card title={
        <Space>
          <RobotOutlined style={{ color: '#3D6E66' }} />
          <span>AI 助手配置 (全局)</span>
        </Space>
      }>
        <Alert
          message="配置说明"
          description="在此处配置的大模型参数将全局生效，包括：AI 接口生成、Web 测试探索引擎、性能测试场景生成以及全局悬浮 Copilot。"
          type="info"
          showIcon
          style={{ marginBottom: 24 }}
        />
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
                label="Base URL"
                name="aiBaseUrl"
                rules={[{ required: true, message: '请输入 Base URL' }]}
                tooltip="支持 OpenAI 兼容格式的 API 接口地址，例如 DeepSeek 或其他自建模型。"
              >
                <Input placeholder={globalAiConfig?.base_url || "https://api.openai.com/v1"} />
              </Form.Item>
            </Col>
            <Col span={12}>
              <Form.Item
                label="模型名称 (Model)"
                name="aiModel"
                rules={[{ required: true, message: '请输入模型名称' }]}
                tooltip="填写具体的模型名称，如 deepseek-chat, gpt-4o 等。"
              >
                <Input placeholder={globalAiConfig?.model || "gpt-4o-mini"} />
              </Form.Item>
            </Col>
          </Row>

          <Row gutter={24}>
            <Col span={12}>
              <Form.Item
                label="API Key"
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
                label="视觉模型 Base URL"
                name="aiVisionBaseUrl"
                rules={[{ required: true, message: '请输入视觉模型 Base URL' }]}
              >
                <Input placeholder={globalAiConfig?.vision_base_url || globalAiConfig?.base_url || "https://api.openai.com/v1"} />
              </Form.Item>
            </Col>
            <Col span={12}>
              <Form.Item
                label="视觉模型名称 (Vision Model)"
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
                label="视觉模型 API Key"
                name="aiVisionApiKey"
                rules={[{ required: true, message: '请输入视觉模型 API Key' }]}
              >
                <Input.Password placeholder={globalAiConfig?.vision_api_key || "sk-..."} />
              </Form.Item>
            </Col>
          </Row>

          <Divider />
          
          <Form.Item style={{ marginBottom: 0 }}>
            <Button type="primary" htmlType="submit" icon={<SaveOutlined />} loading={loading}>
              保存设置
            </Button>
          </Form.Item>
        </Form>
      </Card>
    </div>
  );
};

export default Settings;
