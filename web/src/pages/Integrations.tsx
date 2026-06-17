/**
 * 集成管理页面
 *
 * 展示 GitHub 集成卡片，支持授权、状态查看和解绑。
 * 预留 GitLab 和 Jira 集成入口。
 */
import { useState, useEffect, useCallback } from 'react'
import {
  Card,
  Button,
  Tag,
  Space,
  Typography,
  Avatar,
  message,
  Popconfirm,
  Empty,
  Spin,
  Row,
  Col,
  Divider,
  Alert,
} from 'antd'
import {
  GithubOutlined,
  LinkOutlined,
  DisconnectOutlined,
  CheckCircleOutlined,
  CloseCircleOutlined,
  LockOutlined,
  SettingOutlined,
  GitlabOutlined,
  BugOutlined,
} from '@ant-design/icons'
import { useTranslation } from 'react-i18next'
import integrationService, { GitHubStatus } from '@/services/integrationService'

const { Title, Text, Paragraph } = Typography

const Integrations = () => {
  const { t } = useTranslation()
  const [githubStatus, setGithubStatus] = useState<GitHubStatus | null>(null)
  const [githubConfigured, setGithubConfigured] = useState<boolean | null>(null)
  const [loading, setLoading] = useState(true)
  const [actionLoading, setActionLoading] = useState(false)

  const fetchStatus = useCallback(async () => {
    setLoading(true)
    try {
      // 先检查 GitHub OAuth 是否配置
      try {
        const configRes = await integrationService.getGitHubConfig()
        setGithubConfigured(configRes.code === 200 && configRes.data?.configured === true)
      } catch {
        setGithubConfigured(false)
      }

      const res = await integrationService.getGitHubStatus()
      if (res.code === 200 && res.data) {
        setGithubStatus(res.data)
      }
    } catch {
      // 静默失败
    } finally {
      setLoading(false)
    }
  }, [])

  useEffect(() => {
    fetchStatus()
    // 检查 URL 参数是否有 GitHub 回调结果
    const params = new URLSearchParams(window.location.search)
    if (params.get('github_success') === 'true') {
      message.success(t('integrations.github.connectSuccess'))
      window.history.replaceState({}, '', window.location.pathname)
      fetchStatus()
    }
    if (params.get('github_error')) {
      message.error(t('integrations.github.connectFailed'))
      window.history.replaceState({}, '', window.location.pathname)
    }
  }, [fetchStatus, t])

  const handleConnectGitHub = async () => {
    if (githubConfigured === false) {
      message.warning(t('integrations.github.notConfigured') || 'GitHub OAuth 尚未配置，请联系管理员在后端配置 GITHUB_CLIENT_ID 和 GITHUB_CLIENT_SECRET。')
      return
    }
    setActionLoading(true)
    try {
      const res = await integrationService.getGitHubAuthUrl()
      if (res.code === 200 && res.data?.authorize_url) {
        window.location.href = res.data.authorize_url
      } else {
        message.error(res?.message || t('integrations.github.authFailed') || 'GitHub 授权失败，请检查后端 OAuth 配置。')
      }
    } catch (err: any) {
      message.error(t('integrations.github.authFailed') || 'GitHub 授权失败，请检查后端 OAuth 配置。')
    } finally {
      setActionLoading(false)
    }
  }

  const handleUnbindGitHub = async () => {
    setActionLoading(true)
    try {
      const res = await integrationService.unbindGitHub()
      if (res.code === 200) {
        message.success(t('integrations.github.unbindSuccess'))
        await fetchStatus()
      } else {
        message.error(res.message || t('integrations.github.unbindFailed'))
      }
    } catch {
      message.error(t('integrations.github.unbindFailed'))
    } finally {
      setActionLoading(false)
    }
  }

  const isGitHubConnected = githubStatus?.connected ?? false
  const ghIntegration = githubStatus?.integration

  return (
    <div className="fst-page" style={{ padding: 0 }}>
      <div className="fst-page-header fst-animate-in">
        <div>
          <h1 className="fst-page-title">{t('integrations.title')}</h1>
          <div className="fst-ios-card-subtitle">
            {t('integrations.subtitle') || '连接外部服务以增强测试工作流'}
          </div>
        </div>
      </div>

      {loading ? (
        <div style={{ display: 'flex', justifyContent: 'center', paddingTop: 80 }}>
          <Spin size="large" />
        </div>
      ) : (
        <>
          {githubConfigured === false && (
            <Alert
              message={t('integrations.github.notConfiguredTitle') || 'GitHub OAuth 未配置'}
              description={
                <span>
                  {t('integrations.github.notConfiguredDesc') || '要使用 GitHub 集成，请在后端环境变量中配置 '}
                  <Text code>GITHUB_CLIENT_ID</Text>
                  {' 和 '}
                  <Text code>GITHUB_CLIENT_SECRET</Text>
                  {'。详见部署文档。'}
                </span>
              }
              type="info"
              showIcon
              icon={<SettingOutlined />}
              style={{ marginBottom: 24 }}
              closable
            />
          )}

          <Row gutter={[24, 24]}>
            {/* GitHub 集成卡片 */}
            <Col xs={24} sm={24} md={12} lg={8}>
              <Card
                className="fst-ios-card"
                style={{ height: '100%' }}
                actions={[
                  isGitHubConnected ? (
                    <Popconfirm
                      title={t('integrations.github.unbindConfirm')}
                      onConfirm={handleUnbindGitHub}
                      okText={t('common.confirm')}
                      cancelText={t('common.cancel')}
                    >
                      <Button
                        type="link"
                        danger
                        icon={<DisconnectOutlined />}
                        loading={actionLoading}
                      >
                        {t('integrations.github.unbind')}
                      </Button>
                    </Popconfirm>
                  ) : (
                    <Button
                      type="link"
                      icon={<LinkOutlined />}
                      onClick={handleConnectGitHub}
                      loading={actionLoading}
                      disabled={githubConfigured === false}
                    >
                      {t('integrations.github.connect')}
                    </Button>
                  ),
                ]}
              >
                <div style={{ display: 'flex', alignItems: 'center', gap: 12, marginBottom: 16 }}>
                  <div style={{
                    width: 44,
                    height: 44,
                    borderRadius: 12,
                    background: 'linear-gradient(135deg, #24292e 0%, #586069 100%)',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                  }}>
                    <GithubOutlined style={{ fontSize: 24, color: '#fff' }} />
                  </div>
                  <div>
                    <Text strong style={{ fontSize: 16 }}>GitHub</Text>
                    <br />
                    <Tag color={isGitHubConnected ? 'green' : githubConfigured === false ? 'orange' : 'default'}>
                      {isGitHubConnected
                        ? t('integrations.connected')
                        : githubConfigured === false
                          ? (t('integrations.notConfigured') || '未配置')
                          : t('integrations.notConnected')}
                    </Tag>
                  </div>
                </div>
                <Paragraph type="secondary" style={{ fontSize: 13, marginBottom: 12 }}>
                  {t('integrations.github.description')}
                </Paragraph>
                {githubConfigured === false && (
                  <div style={{
                    padding: '8px 12px',
                    borderRadius: 8,
                    background: 'rgba(232, 207, 160, 0.12)',
                    border: '1px solid rgba(232, 207, 160, 0.25)',
                    fontSize: 12,
                    color: 'var(--fst-on-surface-variant)',
                  }}>
                    {t('integrations.github.setupHint') || '需要管理员配置 GitHub OAuth App 才能使用此功能'}
                  </div>
                )}
                {isGitHubConnected && ghIntegration && (
                  <div style={{ marginTop: 12, padding: 12, background: 'var(--fst-surface-container, #f6f8f8)', borderRadius: 8 }}>
                    <Space direction="vertical" size={4} style={{ width: '100%' }}>
                      <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                        {ghIntegration.github_avatar && (
                          <Avatar src={ghIntegration.github_avatar} size={24} />
                        )}
                        <Text strong>{ghIntegration.github_username}</Text>
                      </div>
                      {ghIntegration.repo_full_name && (
                        <Text type="secondary" style={{ fontSize: 12 }}>
                          📦 {ghIntegration.repo_full_name}
                        </Text>
                      )}
                      <div>
                        <Text type="secondary" style={{ fontSize: 12 }}>
                          {t('integrations.github.checkRun')}: {' '}
                          {ghIntegration.check_run_enabled ? (
                            <Tag color="green" style={{ fontSize: 11 }}>{t('integrations.enabled')}</Tag>
                          ) : (
                            <Tag style={{ fontSize: 11 }}>{t('integrations.disabled')}</Tag>
                          )}
                        </Text>
                      </div>
                    </Space>
                  </div>
                )}
              </Card>
            </Col>

            {/* GitLab 集成卡片（预留） */}
            <Col xs={24} sm={24} md={12} lg={8}>
              <Card className="fst-ios-card" style={{ height: '100%', opacity: 0.6 }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: 12, marginBottom: 16 }}>
                  <div style={{
                    width: 44,
                    height: 44,
                    borderRadius: 12,
                    background: 'linear-gradient(135deg, #FC6D26 0%, #E24329 100%)',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                  }}>
                    <GitlabOutlined style={{ fontSize: 24, color: '#fff' }} />
                  </div>
                  <div>
                    <Text strong style={{ fontSize: 16 }}>GitLab</Text>
                    <br />
                    <Tag>{t('integrations.comingSoon')}</Tag>
                  </div>
                </div>
                <Paragraph type="secondary" style={{ fontSize: 13 }}>
                  {t('integrations.gitlab.description')}
                </Paragraph>
              </Card>
            </Col>

            {/* Jira 集成卡片（预留） */}
            <Col xs={24} sm={24} md={12} lg={8}>
              <Card className="fst-ios-card" style={{ height: '100%', opacity: 0.6 }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: 12, marginBottom: 16 }}>
                  <div style={{
                    width: 44,
                    height: 44,
                    borderRadius: 12,
                    background: 'linear-gradient(135deg, #0052CC 0%, #2684FF 100%)',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                  }}>
                    <BugOutlined style={{ fontSize: 24, color: '#fff' }} />
                  </div>
                  <div>
                    <Text strong style={{ fontSize: 16 }}>Jira</Text>
                    <br />
                    <Tag>{t('integrations.comingSoon')}</Tag>
                  </div>
                </div>
                <Paragraph type="secondary" style={{ fontSize: 13 }}>
                  {t('integrations.jira.description')}
                </Paragraph>
              </Card>
            </Col>
          </Row>
        </>
      )}
    </div>
  )
}

export default Integrations
