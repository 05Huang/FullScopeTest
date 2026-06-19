import React, { useState, useEffect, useCallback } from 'react';
import { Card, Form, Input, Button, message, Typography, Row, Col, Space, Tabs, Switch, Select, Slider, Divider, Radio, Tag, Alert, Popconfirm, Table, Modal, InputNumber, Tooltip, Badge } from 'antd';
import {
  RobotOutlined, SaveOutlined, SettingOutlined, BulbOutlined,
  GlobalOutlined, BellOutlined, SafetyOutlined, KeyOutlined,
  SunOutlined, MoonOutlined, DesktopOutlined,
  LinkOutlined, GithubOutlined, DisconnectOutlined, ApiOutlined,
  PlusOutlined, EditOutlined, DeleteOutlined, CheckCircleOutlined,
  ReloadOutlined, ExperimentOutlined, ThunderboltOutlined,
} from '@ant-design/icons';
import { useTranslation } from 'react-i18next';
import { apiTestService } from '../services/apiTestService';
import { useThemeStore } from '../stores/themeStore';
import integrationService from '../services/integrationService';
import {
  promptVersionService, PromptVersion, PromptVersionPayload, PROMPT_FEATURES,
} from '../services/promptVersionService';

const { Text } = Typography;

/** 集成配置子组件 — 在系统设置内管理 GitHub OAuth 等 */
const SettingsIntegrationsTab: React.FC = () => {
  const { t } = useTranslation();
  const [githubConfig, setGithubConfig] = useState<{ configured: boolean; client_id?: string } | null>(null);
  const [githubStatus, setGithubStatus] = useState<{ connected: boolean; integration?: any } | null>(null);
  const [loading, setLoading] = useState(true);
  const [clientId, setClientId] = useState('');
  const [clientSecret, setClientSecret] = useState('');
  const [saving, setSaving] = useState(false);

  useEffect(() => {
    const load = async () => {
      setLoading(true);
      try {
        const [cfgRes, statusRes] = await Promise.allSettled([
          integrationService.getGitHubConfig(),
          integrationService.getGitHubStatus(),
        ]);
        if (cfgRes.status === 'fulfilled' && cfgRes.value?.code === 200) {
          setGithubConfig(cfgRes.value.data);
          if (cfgRes.value.data?.client_id) setClientId(cfgRes.value.data.client_id);
        }
        if (statusRes.status === 'fulfilled' && statusRes.value?.code === 200) {
          setGithubStatus(statusRes.value.data);
        }
      } catch { /* ignore */ } finally { setLoading(false); }
    };
    load();
  }, []);

  const handleSaveGitHubConfig = async () => {
    if (!clientId.trim()) { message.error(t('settings.githubClientIdRequired') || '请输入 Client ID'); return; }
    setSaving(true);
    try {
      // Save to localStorage for frontend use
      localStorage.setItem('fst-github-client-id', clientId);
      if (clientSecret) localStorage.setItem('fst-github-client-secret', clientSecret);
      message.success(t('settings.saveSuccess'));
    } finally { setSaving(false); }
  };

  const handleDisconnect = async () => {
    try {
      await integrationService.unbindGitHub();
      message.success(t('integrations.github.unbindSuccess'));
      const res = await integrationService.getGitHubStatus();
      if (res.code === 200) setGithubStatus(res.data);
    } catch { message.error(t('integrations.github.unbindFailed')); }
  };

  const labelStyle = { fontWeight: 600, fontSize: 13 };

  return (
    <div style={{ padding: '8px 0' }}>
      {/* GitHub Integration */}
      <div style={{ marginBottom: 24 }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 12, marginBottom: 16 }}>
          <div style={{
            width: 40, height: 40, borderRadius: 10,
            background: 'linear-gradient(135deg, #24292e 0%, #586069 100%)',
            display: 'flex', alignItems: 'center', justifyContent: 'center',
          }}>
            <GithubOutlined style={{ fontSize: 20, color: '#fff' }} />
          </div>
          <div>
            <Text strong style={{ fontSize: 15 }}>GitHub</Text>
            <div>
              <Tag color={githubStatus?.connected ? 'green' : githubConfig?.configured ? 'blue' : 'orange'}>
                {githubStatus?.connected
                  ? (t('integrations.connected') || '已连接')
                  : githubConfig?.configured
                    ? (t('integrations.notConnected') || '未连接')
                    : (t('integrations.notConfigured') || '未配置')}
              </Tag>
            </div>
          </div>
        </div>

        <Text type="secondary" style={{ fontSize: 13, display: 'block', marginBottom: 16 }}>
          {t('settings.githubOAuthHint') || '配置 GitHub OAuth App 以启用 PR Check Run 回写、Issue 关联等功能。需要在 GitHub Settings > Developer settings > OAuth Apps 中创建应用。'}
        </Text>

        <Row gutter={16}>
          <Col span={12}>
            <div style={{ marginBottom: 16 }}>
              <Text strong style={labelStyle}>Client ID</Text>
              <Input
                value={clientId}
                onChange={e => setClientId(e.target.value)}
                placeholder="Ov23li..."
                style={{ marginTop: 6 }}
              />
            </div>
          </Col>
          <Col span={12}>
            <div style={{ marginBottom: 16 }}>
              <Text strong style={labelStyle}>Client Secret</Text>
              <Input.Password
                value={clientSecret}
                onChange={e => setClientSecret(e.target.value)}
                placeholder={githubConfig?.configured ? '•••••••• (已配置)' : 'ghp_xxx...'}
                style={{ marginTop: 6 }}
              />
            </div>
          </Col>
        </Row>

        <div style={{ display: 'flex', gap: 8 }}>
          <Button type="primary" icon={<SaveOutlined />} onClick={handleSaveGitHubConfig} loading={saving}>
            {t('settings.saveBtn')}
          </Button>
          {githubStatus?.connected && (
            <Popconfirm
              title={t('integrations.github.unbindConfirm')}
              onConfirm={handleDisconnect}
              okText={t('common.confirm')}
              cancelText={t('common.cancel')}
            >
              <Button danger icon={<DisconnectOutlined />}>
                {t('integrations.github.unbind') || '断开连接'}
              </Button>
            </Popconfirm>
          )}
        </div>

        {!githubConfig?.configured && !githubStatus?.connected && (
          <Alert
            type="info"
            showIcon
            style={{ marginTop: 16 }}
            message={t('settings.githubSetupGuide') || '设置指南'}
            description={
              <ol style={{ margin: '4px 0 0', paddingLeft: 20, fontSize: 13, lineHeight: 2 }}>
                <li>{t('settings.githubStep1') || '访问 GitHub > Settings > Developer settings > OAuth Apps'}</li>
                <li>{t('settings.githubStep2') || '点击 "New OAuth App"，填写应用信息'}</li>
                <li>{t('settings.githubStep3') || `Callback URL 填写: ${window.location.origin}/integrations`}</li>
                <li>{t('settings.githubStep4') || '将获取到的 Client ID 和 Client Secret 填入上方'}</li>
              </ol>
            }
          />
        )}
      </div>

      <Divider />

      {/* Webhook / API Token 快捷入口 */}
      <div>
        <Text strong style={{ fontSize: 15, display: 'block', marginBottom: 8 }}>
          {t('settings.webhookAndTokens') || 'Webhook 与 API Token'}
        </Text>
        <Text type="secondary" style={{ fontSize: 13, display: 'block', marginBottom: 16 }}>
          {t('settings.webhookHint') || 'Webhook 和 API Token 的详细管理请前往专门页面。'}
        </Text>
        <Space>
          <Button icon={<ApiOutlined />} onClick={() => window.location.href = '/api-tokens'}>
            {t('sidebar.apiTokens') || 'API Token'}
          </Button>
          <Button icon={<BellOutlined />} onClick={() => window.location.href = '/notification-settings'}>
            {t('sidebar.notifications') || '通知设置'}
          </Button>
          <Button icon={<SettingOutlined />} onClick={() => window.location.href = '/ci-cd'}>
            {t('sidebar.cicd') || 'CI/CD'}
          </Button>
        </Space>
      </div>
    </div>
  );
};

const Settings: React.FC = () => {
  const { t, i18n } = useTranslation();
  const [form] = Form.useForm();
  const [loading, setLoading] = useState(false);
  const { mode: themeMode, setMode: setThemeMode, resolvedTheme } = useThemeStore();
  const [globalAiConfig, setGlobalAiConfig] = useState<any>(null);

  // General settings state
  const [pageSize, setPageSize] = useState(() => Number(localStorage.getItem('fst-page-size') || 20));
  const [autoRefresh, setAutoRefresh] = useState(() => localStorage.getItem('fst-auto-refresh') === 'true');
  const [refreshInterval, setRefreshInterval] = useState(() => Number(localStorage.getItem('fst-refresh-interval') || 30));
  const [reduceMotion, setReduceMotion] = useState(() => localStorage.getItem('fst-reduce-motion') === 'true');

  useEffect(() => {
    apiTestService.getAiConfig()
      .then((res: any) => {
        if (res.code === 200 && res.data) setGlobalAiConfig(res.data);
      })
      .catch(() => {});

    form.setFieldsValue({
      aiBaseUrl: localStorage.getItem('api-test-ai-base-url') || '',
      aiModel: localStorage.getItem('api-test-ai-model') || '',
      aiApiKey: localStorage.getItem('api-test-ai-api-key') || '',
      aiVisionBaseUrl: localStorage.getItem('api-test-ai-vision-base-url') || '',
      aiVisionModel: localStorage.getItem('api-test-ai-vision-model') || '',
      aiVisionApiKey: localStorage.getItem('api-test-ai-vision-api-key') || '',
    });
  }, [form]);

  const handleSaveAi = async (values: any) => {
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
        message.error(res.message || t('common.failed'));
        return;
      }
      Object.entries(payload).forEach(([k, v]) => {
        const lk = `api-test-ai-${k.replace(/_/g, '-')}`;
        localStorage.setItem(lk, v as string);
      });
      if (res.data) setGlobalAiConfig(res.data);
      message.success(t('settings.saveSuccess'));
    } catch {
      message.error(t('common.failed'));
    } finally {
      setLoading(false);
    }
  };

  const handleSaveGeneral = () => {
    localStorage.setItem('fst-page-size', String(pageSize));
    localStorage.setItem('fst-auto-refresh', String(autoRefresh));
    localStorage.setItem('fst-refresh-interval', String(refreshInterval));
    localStorage.setItem('fst-reduce-motion', String(reduceMotion));
    if (reduceMotion) {
      document.documentElement.style.setProperty('--animation-duration', '0s');
    } else {
      document.documentElement.style.removeProperty('--animation-duration');
    }
    message.success(t('settings.saveSuccess'));
  };

  const handleLanguageChange = (lang: string) => {
    i18n.changeLanguage(lang);
    localStorage.setItem('fst-language', lang);
    message.success(t('settings.saveSuccess'));
  };

  const cardStyle = {
    marginBottom: 0,
  };

  const labelStyle = { fontWeight: 600, fontSize: 13 };

  /** Prompt 版本管理子组件 */
  const PromptManagementTab: React.FC = () => {
    const [versions, setVersions] = useState<PromptVersion[]>([]);
    const [loading, setLoading] = useState(false);
    const [total, setTotal] = useState(0);
    const [page, setPage] = useState(1);
    const [filterFeature, setFilterFeature] = useState<string | undefined>();
    const [modalOpen, setModalOpen] = useState(false);
    const [editingVersion, setEditingVersion] = useState<PromptVersion | null>(null);
    const [saving, setSaving] = useState(false);
    const [form] = Form.useForm();

    const loadVersions = useCallback(async (p = page, feature = filterFeature) => {
      setLoading(true);
      try {
        const res = await promptVersionService.list({ page: p, per_page: 10, feature });
        if (res.code === 200 && res.data) {
          setVersions(res.data.items || []);
          setTotal(res.data.total || 0);
        }
      } catch {
        message.error(t('common.failed') || '加载失败');
      } finally {
        setLoading(false);
      }
    }, [page, filterFeature, t]);

    useEffect(() => { loadVersions(1); }, [filterFeature]);

    const handleCreate = () => {
      setEditingVersion(null);
      form.resetFields();
      form.setFieldsValue({ temperature: 0.3, traffic_weight: 1.0, is_active: false });
      setModalOpen(true);
    };

    const handleEdit = (record: PromptVersion) => {
      setEditingVersion(record);
      form.setFieldsValue({
        feature: record.feature,
        name: record.name,
        system_prompt: record.system_prompt,
        user_prompt_template: record.user_prompt_template || '',
        temperature: record.temperature,
        model_name: record.model_name || '',
        is_active: record.is_active,
        traffic_weight: record.traffic_weight,
        change_notes: record.change_notes || '',
      });
      setModalOpen(true);
    };

    const handleSave = async () => {
      try {
        const values = await form.validateFields();
        setSaving(true);
        const payload: PromptVersionPayload = {
          feature: values.feature,
          name: values.name,
          system_prompt: values.system_prompt,
          user_prompt_template: values.user_prompt_template || undefined,
          temperature: values.temperature,
          model_name: values.model_name || undefined,
          is_active: values.is_active,
          traffic_weight: values.traffic_weight,
          change_notes: values.change_notes || undefined,
        };
        if (editingVersion) {
          const res = await promptVersionService.update(editingVersion.id, payload);
          if (res.code === 200) {
            message.success(t('prompt.updated') || '版本更新成功');
            setModalOpen(false);
            loadVersions();
          } else {
            message.error(res.message);
          }
        } else {
          const res = await promptVersionService.create(payload);
          if (res.code === 200 || res.code === 201) {
            message.success(t('prompt.created') || '版本创建成功');
            setModalOpen(false);
            loadVersions();
          } else {
            message.error(res.message);
          }
        }
      } catch {
        // 表单校验失败不处理
      } finally {
        setSaving(false);
      }
    };

    const handleDeactivate = async (id: number) => {
      try {
        const res = await promptVersionService.deactivate(id);
        if (res.code === 200) {
          message.success(t('prompt.deactivated') || '版本已停用');
          loadVersions();
        }
      } catch {
        message.error(t('common.failed') || '操作失败');
      }
    };

    const handleActivate = async (feature: string) => {
      try {
        const res = await promptVersionService.select(feature);
        if (res.code === 200) {
          message.success(t('prompt.activated') || '版本已激活');
          loadVersions();
        }
      } catch {
        message.error(t('common.failed') || '操作失败');
      }
    };

    const handleRefreshStats = async () => {
      try {
        const res = await promptVersionService.refreshStats(filterFeature);
        if (res.code === 200) {
          message.success(t('prompt.statsRefreshed') || '统计数据已刷新');
          loadVersions();
        }
      } catch {
        message.error(t('common.failed') || '刷新失败');
      }
    };

    const featureOptions = [
      { label: t('prompt.allFeatures') || '全部功能', value: '' },
      ...PROMPT_FEATURES.map(f => ({ label: f.label, value: f.value })),
    ];

    const columns = [
      {
        title: t('prompt.feature') || '功能',
        dataIndex: 'feature',
        key: 'feature',
        width: 120,
        render: (val: string) => {
          const found = PROMPT_FEATURES.find(f => f.value === val);
          return <Tag color="blue">{found?.label || val}</Tag>;
        },
      },
      {
        title: t('prompt.name') || '名称',
        dataIndex: 'name',
        key: 'name',
        width: 160,
        render: (val: string, record: PromptVersion) => (
          <Space size={4}>
            <span style={{ fontWeight: 500 }}>{val}</span>
            <span style={{ color: 'var(--fst-on-surface-muted, #999)', fontSize: 12 }}>v{record.version}</span>
          </Space>
        ),
      },
      {
        title: t('prompt.status') || '状态',
        dataIndex: 'is_active',
        key: 'is_active',
        width: 80,
        render: (val: boolean) => val
          ? <Badge status="success" text={t('prompt.active') || '激活'} />
          : <Badge status="default" text={t('prompt.inactive') || '停用'} />,
      },
      {
        title: t('prompt.temperature') || '温度',
        dataIndex: 'temperature',
        key: 'temperature',
        width: 70,
        render: (val: number) => val?.toFixed(1),
      },
      {
        title: t('prompt.trafficWeight') || '流量权重',
        dataIndex: 'traffic_weight',
        key: 'traffic_weight',
        width: 90,
        render: (val: number) => `${(val * 100).toFixed(0)}%`,
      },
      {
        title: t('prompt.invocations') || '调用次数',
        dataIndex: 'total_invocations',
        key: 'total_invocations',
        width: 90,
        render: (val: number) => val?.toLocaleString() || '0',
      },
      {
        title: t('prompt.successRate') || '成功率',
        dataIndex: 'success_rate',
        key: 'success_rate',
        width: 80,
        render: (val: number) => {
          const color = val >= 90 ? '#52c41a' : val >= 70 ? '#faad14' : '#ff4d4f';
          return <span style={{ color, fontWeight: 500 }}>{val?.toFixed(1)}%</span>;
        },
      },
      {
        title: t('prompt.actions') || '操作',
        key: 'actions',
        width: 160,
        render: (_: any, record: PromptVersion) => (
          <Space size="small">
            <Tooltip title={t('common.edit') || '编辑'}>
              <Button size="small" icon={<EditOutlined />} onClick={() => handleEdit(record)} />
            </Tooltip>
            {!record.is_active && (
              <Tooltip title={t('prompt.setActive') || '设为激活'}>
                <Button size="small" type="primary" icon={<CheckCircleOutlined />} onClick={() => handleActivate(record.feature)} />
              </Tooltip>
            )}
            {record.is_active && (
              <Popconfirm
                title={t('prompt.deactivateConfirm') || '确认停用此版本？'}
                onConfirm={() => handleDeactivate(record.id)}
                okText={t('common.confirm') || '确认'}
                cancelText={t('common.cancel') || '取消'}
              >
                <Tooltip title={t('prompt.deactivate') || '停用'}>
                  <Button size="small" danger icon={<DeleteOutlined />} />
                </Tooltip>
              </Popconfirm>
            )}
          </Space>
        ),
      },
    ];

    return (
      <div style={{ padding: '8px 0' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 16 }}>
          <Space>
            <Select
              value={filterFeature || ''}
              onChange={(v) => setFilterFeature(v || undefined)}
              options={featureOptions}
              style={{ width: 180 }}
              placeholder={t('prompt.filterFeature') || '筛选功能'}
            />
            <Tooltip title={t('prompt.refreshStats') || '刷新统计'}>
              <Button icon={<ReloadOutlined />} onClick={handleRefreshStats} />
            </Tooltip>
          </Space>
          <Button type="primary" icon={<PlusOutlined />} onClick={handleCreate}>
            {t('prompt.createVersion') || '新建版本'}
          </Button>
        </div>

        <Table
          rowKey="id"
          columns={columns}
          dataSource={versions}
          loading={loading}
          size="small"
          pagination={{
            current: page,
            total,
            pageSize: 10,
            onChange: (p) => { setPage(p); loadVersions(p); },
            showTotal: (t) => `${t} 条`,
            showSizeChanger: false,
          }}
        />

        {/* 创建/编辑弹窗 */}
        <Modal
          title={editingVersion ? (t('prompt.editVersion') || '编辑 Prompt 版本') : (t('prompt.createVersion') || '新建 Prompt 版本')}
          open={modalOpen}
          onCancel={() => setModalOpen(false)}
          onOk={handleSave}
          confirmLoading={saving}
          width={720}
          okText={t('common.save') || '保存'}
          cancelText={t('common.cancel') || '取消'}
        >
          <Form form={form} layout="vertical" style={{ marginTop: 16 }}>
            <Row gutter={16}>
              <Col span={12}>
                <Form.Item
                  label={t('prompt.feature') || '功能模块'}
                  name="feature"
                  rules={[{ required: true, message: t('prompt.featureRequired') || '请选择功能模块' }]}
                >
                  <Select
                    options={PROMPT_FEATURES.map(f => ({ label: f.label, value: f.value }))}
                    placeholder={t('prompt.selectFeature') || '选择功能'}
                    disabled={!!editingVersion}
                  />
                </Form.Item>
              </Col>
              <Col span={12}>
                <Form.Item
                  label={t('prompt.name') || '版本名称'}
                  name="name"
                  rules={[{ required: true, message: t('prompt.nameRequired') || '请输入版本名称' }]}
                >
                  <Input placeholder={t('prompt.namePlaceholder') || '例如：v1、baseline、experiment-A'} />
                </Form.Item>
              </Col>
            </Row>

            <Form.Item
              label={t('prompt.systemPrompt') || '系统提示词'}
              name="system_prompt"
              rules={[{ required: true, message: t('prompt.systemPromptRequired') || '请输入系统提示词' }]}
            >
              <Input.TextArea rows={6} placeholder={t('prompt.systemPromptPlaceholder') || '输入 Prompt 内容...'} style={{ fontFamily: 'monospace' }} />
            </Form.Item>

            <Form.Item
              label={t('prompt.userPromptTemplate') || '用户提示词模板'}
              name="user_prompt_template"
            >
              <Input.TextArea rows={3} placeholder={t('prompt.userPromptPlaceholder') || '可选，支持 {variable} 占位符'} style={{ fontFamily: 'monospace' }} />
            </Form.Item>

            <Row gutter={16}>
              <Col span={8}>
                <Form.Item label={t('prompt.temperature') || '温度'} name="temperature">
                  <InputNumber min={0} max={2} step={0.1} style={{ width: '100%' }} />
                </Form.Item>
              </Col>
              <Col span={8}>
                <Form.Item label={t('prompt.trafficWeight') || '流量权重'} name="traffic_weight">
                  <InputNumber min={0} max={1} step={0.1} style={{ width: '100%' }} />
                </Form.Item>
              </Col>
              <Col span={8}>
                <Form.Item label={t('prompt.modelName') || '指定模型'} name="model_name">
                  <Input placeholder={t('prompt.modelPlaceholder') || '留空使用全局默认'} />
                </Form.Item>
              </Col>
            </Row>

            <Form.Item label={t('prompt.changeNotes') || '变更说明'} name="change_notes">
              <Input.TextArea rows={2} placeholder={t('prompt.changeNotesPlaceholder') || '本次变更的说明（可选）'} />
            </Form.Item>

            <Form.Item label={t('prompt.isActive') || '激活'} name="is_active" valuePropName="checked">
              <Switch />
            </Form.Item>
          </Form>
        </Modal>
      </div>
    );
  };

  const hintBox = (text: string) => (
    <div style={{
      padding: '10px 14px',
      borderRadius: 'var(--fst-radius-lg)',
      background: resolvedTheme === 'dark' ? 'rgba(74, 158, 150, 0.08)' : 'rgba(45, 106, 100, 0.06)',
      border: `1px solid ${resolvedTheme === 'dark' ? 'rgba(74, 158, 150, 0.15)' : 'rgba(45, 106, 100, 0.12)'}`,
      fontSize: 13,
      color: 'var(--fst-on-surface-variant)',
      marginBottom: 20,
      lineHeight: 1.6,
    }}>
      {text}
    </div>
  );

  const tabItems = [
    {
      key: 'general',
      label: (
        <span style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
          <SettingOutlined /> {t('settings.generalTab') || '通用'}
        </span>
      ),
      children: (
        <div style={{ padding: '8px 0' }}>
          {hintBox(t('settings.generalHint') || '配置通用的平台行为偏好，包括分页大小、自动刷新和动画效果。')}

          <div style={{ marginBottom: 20 }}>
            <Text strong style={labelStyle}>{t('settings.language') || '语言'}</Text>
            <div style={{ marginTop: 8 }}>
              <Select
                value={i18n.language}
                onChange={handleLanguageChange}
                style={{ width: 200 }}
                options={[
                  { label: '简体中文', value: 'zh' },
                  { label: 'English', value: 'en' },
                ]}
              />
            </div>
          </div>

          <Divider style={{ margin: '16px 0' }} />

          <div style={{ marginBottom: 20 }}>
            <Text strong style={labelStyle}>{t('settings.pageSize') || '默认分页大小'}</Text>
            <div style={{ marginTop: 8 }}>
              <Slider
                min={10}
                max={100}
                step={10}
                value={pageSize}
                onChange={setPageSize}
                marks={{ 10: '10', 20: '20', 50: '50', 100: '100' }}
                style={{ maxWidth: 400 }}
              />
            </div>
          </div>

          <Divider style={{ margin: '16px 0' }} />

          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 16 }}>
            <div>
              <Text strong style={labelStyle}>{t('settings.autoRefresh') || '自动刷新'}</Text>
              <div style={{ fontSize: 12, color: 'var(--fst-on-surface-muted)', marginTop: 2 }}>
                {t('settings.autoRefreshHint') || '自动刷新页面数据'}
              </div>
            </div>
            <Switch checked={autoRefresh} onChange={setAutoRefresh} />
          </div>

          {autoRefresh && (
            <div style={{ marginBottom: 16, paddingLeft: 0 }}>
              <Text style={{ fontSize: 13 }}>{t('settings.refreshInterval') || '刷新间隔'}: {refreshInterval}s</Text>
              <Slider
                min={10}
                max={120}
                step={10}
                value={refreshInterval}
                onChange={setRefreshInterval}
                marks={{ 10: '10s', 30: '30s', 60: '60s', 120: '120s' }}
                style={{ maxWidth: 400, marginTop: 8 }}
              />
            </div>
          )}

          <Divider style={{ margin: '16px 0' }} />

          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 20 }}>
            <div>
              <Text strong style={labelStyle}>{t('settings.reduceMotion') || '减少动画'}</Text>
              <div style={{ fontSize: 12, color: 'var(--fst-on-surface-muted)', marginTop: 2 }}>
                {t('settings.reduceMotionHint') || '关闭过渡动画，提升无障碍体验'}
              </div>
            </div>
            <Switch checked={reduceMotion} onChange={setReduceMotion} />
          </div>

          <Button type="primary" icon={<SaveOutlined />} onClick={handleSaveGeneral}>
            {t('settings.saveBtn')}
          </Button>
        </div>
      ),
    },
    {
      key: 'appearance',
      label: (
        <span style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
          <BulbOutlined /> {t('settings.appearanceTab') || '外观'}
        </span>
      ),
      children: (
        <div style={{ padding: '8px 0' }}>
          {hintBox(t('settings.appearanceHint') || '自定义界面外观主题，支持亮色、暗色和跟随系统三种模式。')}

          <Text strong style={labelStyle}>{t('settings.theme') || '主题模式'}</Text>
          <div style={{ marginTop: 12 }}>
            <Radio.Group
              value={themeMode}
              onChange={(e) => setThemeMode(e.target.value)}
              buttonStyle="solid"
              size="large"
            >
              <Radio.Button value="light">
                <SunOutlined style={{ marginRight: 6 }} />{t('settings.light') || '亮色'}
              </Radio.Button>
              <Radio.Button value="dark">
                <MoonOutlined style={{ marginRight: 6 }} />{t('settings.dark') || '暗色'}
              </Radio.Button>
              <Radio.Button value="system">
                <DesktopOutlined style={{ marginRight: 6 }} />{t('settings.system') || '跟随系统'}
              </Radio.Button>
            </Radio.Group>
          </div>

          <div style={{
            marginTop: 24,
            padding: 16,
            borderRadius: 12,
            background: 'var(--fst-surface-variant, #f5f5f5)',
            border: '1px solid var(--fst-outline-soft, #e8e8e8)',
          }}>
            <Text style={{ fontSize: 13, color: 'var(--fst-on-surface-variant)' }}>
              {resolvedTheme === 'dark'
                ? (t('settings.darkPreview') || '当前为暗色模式，深色背景可减少眼部疲劳，适合夜间使用。')
                : (t('settings.lightPreview') || '当前为亮色模式，适合日间使用。')}
            </Text>
          </div>
        </div>
      ),
    },
    {
      key: 'ai',
      label: (
        <span style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
          <RobotOutlined /> {t('settings.aiConfig') || 'AI 配置'}
        </span>
      ),
      children: (
        <div style={{ padding: '8px 0' }}>
          {hintBox(t('settings.aiConfigHint'))}

          <Form
            form={form}
            layout="vertical"
            onFinish={handleSaveAi}
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
                <Form.Item label={<span style={labelStyle}>Base URL</span>} name="aiBaseUrl" rules={[{ required: true, message: t('settings.baseURLRequired') }]} tooltip={t('settings.baseURLTooltip')}>
                  <Input placeholder={globalAiConfig?.base_url || "https://api.openai.com/v1"} />
                </Form.Item>
              </Col>
              <Col span={12}>
                <Form.Item label={<span style={labelStyle}>{t('settings.modelLabel') || '模型名称'}</span>} name="aiModel" rules={[{ required: true, message: t('settings.modelRequired') }]} tooltip={t('settings.modelTooltip')}>
                  <Input placeholder={globalAiConfig?.model || "gpt-4o-mini"} />
                </Form.Item>
              </Col>
            </Row>

            <Row gutter={24}>
              <Col span={12}>
                <Form.Item label={<span style={labelStyle}>API Key</span>} name="aiApiKey" rules={[{ required: true, message: t('settings.apiKeyRequired') }]}>
                  <Input.Password placeholder={globalAiConfig?.api_key || "sk-..."} />
                </Form.Item>
              </Col>
            </Row>

            <Divider style={{ margin: '16px 0' }} />
            <Text strong style={{ ...labelStyle, display: 'block', marginBottom: 16 }}>{t('settings.visionModel') || '视觉模型'}</Text>

            <Row gutter={24}>
              <Col span={12}>
                <Form.Item label={<span style={labelStyle}>Vision Base URL</span>} name="aiVisionBaseUrl">
                  <Input placeholder={globalAiConfig?.vision_base_url || globalAiConfig?.base_url || "https://api.openai.com/v1"} />
                </Form.Item>
              </Col>
              <Col span={12}>
                <Form.Item label={<span style={labelStyle}>Vision Model</span>} name="aiVisionModel">
                  <Input placeholder={globalAiConfig?.vision_model || "gpt-4o-mini"} />
                </Form.Item>
              </Col>
            </Row>

            <Row gutter={24}>
              <Col span={12}>
                <Form.Item label={<span style={labelStyle}>Vision API Key</span>} name="aiVisionApiKey">
                  <Input.Password placeholder={globalAiConfig?.vision_api_key || "sk-..."} />
                </Form.Item>
              </Col>
            </Row>

            <Button type="primary" htmlType="submit" icon={<SaveOutlined />} loading={loading}>
              {t('settings.saveBtn')}
            </Button>
          </Form>
        </div>
      ),
    },
    {
      key: 'security',
      label: (
        <span style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
          <SafetyOutlined /> {t('settings.securityTab') || '安全'}
        </span>
      ),
      children: (
        <div style={{ padding: '8px 0' }}>
          {hintBox(t('settings.securityHint') || '管理密码策略、登录安全和会话超时设置。')}

          <div style={{ marginBottom: 20 }}>
            <Text strong style={labelStyle}>{t('settings.passwordPolicy') || '密码策略'}</Text>
            <div style={{ marginTop: 8, padding: 16, borderRadius: 12, background: 'var(--fst-surface-variant, #fafafa)', border: '1px solid var(--fst-outline-soft, #f0f0f0)' }}>
              <ul style={{ margin: 0, paddingLeft: 20, fontSize: 13, color: 'var(--fst-on-surface-variant)', lineHeight: 2 }}>
                <li>{t('settings.pwdMinLength') || '最少 8 个字符'}</li>
                <li>{t('settings.pwdRequireUpper') || '必须包含大写字母'}</li>
                <li>{t('settings.pwdRequireLower') || '必须包含小写字母'}</li>
                <li>{t('settings.pwdRequireDigit') || '必须包含数字'}</li>
                <li>{t('settings.pwdRequireSpecial') || '必须包含特殊字符'}</li>
              </ul>
            </div>
          </div>

          <Divider style={{ margin: '16px 0' }} />

          <div style={{ marginBottom: 20 }}>
            <Text strong style={labelStyle}>{t('settings.sessionTimeout') || '会话超时'}</Text>
            <div style={{ marginTop: 8 }}>
              <Select
                defaultValue="24h"
                style={{ width: 200 }}
                options={[
                  { label: '1 小时', value: '1h' },
                  { label: '4 小时', value: '4h' },
                  { label: '8 小时', value: '8h' },
                  { label: '24 小时', value: '24h' },
                  { label: '7 天', value: '7d' },
                  { label: '30 天', value: '30d' },
                ]}
              />
            </div>
          </div>

          <Divider style={{ margin: '16px 0' }} />

          <div style={{ marginBottom: 20 }}>
            <Text strong style={labelStyle}>{t('settings.loginAttempts') || '登录失败锁定'}</Text>
            <div style={{ marginTop: 8 }}>
              <Select
                defaultValue="5"
                style={{ width: 200 }}
                options={[
                  { label: '3 次失败后锁定', value: '3' },
                  { label: '5 次失败后锁定', value: '5' },
                  { label: '10 次失败后锁定', value: '10' },
                  { label: '不限制', value: '0' },
                ]}
              />
            </div>
          </div>

          <div style={{
            padding: 16,
            borderRadius: 12,
            background: resolvedTheme === 'dark' ? 'rgba(232, 112, 108, 0.08)' : 'rgba(232, 112, 108, 0.06)',
            border: `1px solid ${resolvedTheme === 'dark' ? 'rgba(232, 112, 108, 0.2)' : 'rgba(232, 112, 108, 0.15)'}`,
            marginTop: 16,
          }}>
            <Text style={{ fontSize: 13, color: 'var(--fst-error, #E8706C)' }}>
              {t('settings.securityWarning') || '安全设置修改需要管理员权限，修改后立即生效。'}
            </Text>
          </div>
        </div>
      ),
    },
    {
      key: 'notifications',
      label: (
        <span style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
          <BellOutlined /> {t('settings.notificationsTab') || '通知'}
        </span>
      ),
      children: (
        <div style={{ padding: '8px 0' }}>
          {hintBox(t('settings.notificationsHint') || '配置通知渠道和订阅事件，支持钉钉、飞书、Slack 等平台。')}

          {[
            { label: t('settings.notifyTestComplete') || '测试完成通知', desc: t('settings.notifyTestCompleteDesc') || '当测试执行完成时发送通知', key: 'test_complete' },
            { label: t('settings.notifyTestFailed') || '测试失败通知', desc: t('settings.notifyTestFailedDesc') || '当测试执行失败时发送通知', key: 'test_failed' },
            { label: t('settings.notifyAlert') || '性能告警通知', desc: t('settings.notifyAlertDesc') || '当性能指标超过阈值时发送通知', key: 'alert_triggered' },
            { label: t('settings.notifyQualityGate') || '质量门禁通知', desc: t('settings.notifyQualityGateDesc') || '当质量门禁评估失败时发送通知', key: 'quality_gate_failed' },
          ].map((item, index) => (
            <div key={item.key} style={{
              display: 'flex',
              justifyContent: 'space-between',
              alignItems: 'center',
              padding: '12px 0',
              borderBottom: index < 3 ? '1px solid var(--fst-outline-soft, #f0f0f0)' : 'none',
            }}>
              <div>
                <Text strong style={{ fontSize: 14 }}>{item.label}</Text>
                <div style={{ fontSize: 12, color: 'var(--fst-on-surface-muted, #999)', marginTop: 2 }}>{item.desc}</div>
              </div>
              <Switch defaultChecked />
            </div>
          ))}

          <Divider style={{ margin: '16px 0' }} />

          <Button type="primary" icon={<SaveOutlined />} onClick={() => message.success(t('settings.saveSuccess'))}>
            {t('settings.saveBtn')}
          </Button>
        </div>
      ),
    },
    {
      key: 'integrations',
      label: (
        <span style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
          <LinkOutlined /> {t('settings.integrationsTab') || '集成'}
        </span>
      ),
      children: (
        <SettingsIntegrationsTab />
      ),
    },
    {
      key: 'prompts',
      label: (
        <span style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
          <ExperimentOutlined /> {t('settings.promptManagementTab') || 'Prompt 管理'}
        </span>
      ),
      children: (
        <PromptManagementTab />
      ),
    },
  ];

  return (
    <div className="fst-page" style={{ maxWidth: 1000, margin: '0 auto' }}>
      <div className="fst-page-header fst-animate-in">
        <div>
          <h1 className="fst-page-title">{t('settings.title')}</h1>
          <div className="fst-ios-card-subtitle">{t('settings.platformSubtitle')}</div>
        </div>
      </div>

      <div className="fst-ios-card fst-animate-in fst-animate-in-1">
        <Tabs
          items={tabItems}
          tabPosition="left"
          style={{ minHeight: 500 }}
          tabBarStyle={{ width: 160, marginRight: 0 }}
        />
      </div>
    </div>
  );
};

export default Settings;
