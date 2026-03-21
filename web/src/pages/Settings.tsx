import React, { useState, useEffect } from 'react';
import { Card, Form, Input, Button, message, Divider, Typography, Row, Col, Alert, Space } from 'antd';
import { RobotOutlined, SaveOutlined } from '@ant-design/icons';

const { Title, Text } = Typography;

const Settings: React.FC = () => {
  const [form] = Form.useForm();
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    // 从 localStorage 加载配置
    const aiBaseUrl = localStorage.getItem('api-test-ai-base-url') || 'https://api.openai.com/v1';
    const aiModel = localStorage.getItem('api-test-ai-model') || 'gpt-4o-mini';
    const aiApiKey = localStorage.getItem('api-test-ai-api-key') || '';

    form.setFieldsValue({
      aiBaseUrl,
      aiModel,
      aiApiKey
    });
  }, [form]);

  const handleSave = async (values: any) => {
    setLoading(true);
    try {
      // 保存到 localStorage，供全局使用
      localStorage.setItem('api-test-ai-base-url', values.aiBaseUrl || '');
      localStorage.setItem('api-test-ai-model', values.aiModel || '');
      localStorage.setItem('api-test-ai-api-key', values.aiApiKey || '');
      
      message.success('设置保存成功');
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
            aiBaseUrl: 'https://api.openai.com/v1',
            aiModel: 'gpt-4o-mini'
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
                <Input placeholder="https://api.openai.com/v1" />
              </Form.Item>
            </Col>
            <Col span={12}>
              <Form.Item
                label="模型名称 (Model)"
                name="aiModel"
                rules={[{ required: true, message: '请输入模型名称' }]}
                tooltip="填写具体的模型名称，如 deepseek-chat, gpt-4o 等。"
              >
                <Input placeholder="gpt-4o-mini" />
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
                <Input.Password placeholder="sk-..." />
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