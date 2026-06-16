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
} from 'antd'
import {
  GithubOutlined,
  LinkOutlined,
  DisconnectOutlined,
  CheckCircleOutlined,
  CloseCircleOutlined,
  LockOutlined,
} from '@ant-design/icons'
import { useTranslation } from 'react-i18next'
import integrationService, { GitHubStatus } from '@/services/integrationService'

const { Title, Text, Paragraph } = Typography

const Integrations = () => {
  const { t } = useTranslation()
  const [githubStatus, setGithubStatus] = useState<GitHubStatus | null>(null)
  const [loading, setLoading] = useState(true)
  const [actionLoading, setActionLoading] = useState(false)

  const fetchStatus = useCallback(async () => {
    setLoading(true)
    try {
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
      // 清理 URL 参数
      window.history.replaceState({}, '', window.location.pathname)
      fetchStatus()
    }
    if (params.get('github_error')) {
      message.error(t('integrations.github.connectFailed'))
      window.history.replaceState({}, '', window.location.pathname)
    }
  }, [fetchStatus, t])

  const handleConnectGitHub = async () => {
    setActionLoading(true)
    try {
      const res = await integrationService.getGitHubAuthUrl()
      if (res.code === 200 && res.data?.authorize_url) {
        window.location.href = res.data.authorize_url
      } else {
        message.error(t('integrations.github.authFailed'))
      }
    } catch {
      message.error(t('integrations.github.authFailed'))
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
    <div style={{ padding: 0 }}>
      <Title level={4} style={{ marginBottom: 24 }}>
        {t('integrations.title')}
      </Title>

      {loading ? (
        <div style={{ display: 'flex', justifyContent: 'center', paddingTop: 80 }}>
          <Spin size="large" />
        </div>
      ) : (
        <Row gutter={[24, 24]}>
          {/* GitHub 集成卡片 */}
          <Col xs={24} sm={24} md={12} lg={8}>
            <Card
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
                  >
                    {t('integrations.github.connect')}
                  </Button>
                ),
              ]}
            >
              <div style={{ display: 'flex', alignItems: 'center', gap: 12, marginBottom: 16 }}>
                <GithubOutlined style={{ fontSize: 32 }} />
                <div>
                  <Text strong style={{ fontSize: 16 }}>GitHub</Text>
                  <br />
                  <Tag color={isGitHubConnected ? 'green' : 'default'}>
                    {isGitHubConnected ? t('integrations.connected') : t('integrations.notConnected')}
                  </Tag>
                </div>
              </div>
              <Paragraph type="secondary">
                {t('integrations.github.description')}
              </Paragraph>
              {isGitHubConnected && ghIntegration && (
                <div style={{ marginTop: 12, padding: 12, background: '#f6f8f8', borderRadius: 8 }}>
                  <Space direction="vertical" size={4} style={{ width: '100%' }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                      {ghIntegration.github_avatar && (
                        <Avatar src={ghIntegration.github_avatar} size={24} />
                      )}
                      <Text strong>{ghIntegration.github_username}</Text>
                    </div>
                    {ghIntegration.repo_full_name && (
                      <Text type="secondary" style={{ fontSize: 12 }}>
                        {ghIntegration.repo_full_name}
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
            <Card style={{ height: '100%', opacity: 0.6 }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: 12, marginBottom: 16 }}>
                <div style={{ fontSize: 32, width: 32, textAlign: 'center' }}>🦊</div>
                <div>
                  <Text strong style={{ fontSize: 16 }}>GitLab</Text>
                  <br />
                  <Tag>{t('integrations.comingSoon')}</Tag>
                </div>
              </div>
              <Paragraph type="secondary">
                {t('integrations.gitlab.description')}
              </Paragraph>
            </Card>
          </Col>

          {/* Jira 集成卡片（预留） */}
          <Col xs={24} sm={24} md={12} lg={8}>
            <Card style={{ height: '100%', opacity: 0.6 }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: 12, marginBottom: 16 }}>
                <div style={{ fontSize: 32, width: 32, textAlign: 'center' }}>📋</div>
                <div>
                  <Text strong style={{ fontSize: 16 }}>Jira</Text>
                  <br />
                  <Tag>{t('integrations.comingSoon')}</Tag>
                </div>
              </div>
              <Paragraph type="secondary">
                {t('integrations.jira.description')}
              </Paragraph>
            </Card>
          </Col>
        </Row>
      )}
    </div>
  )
}

export default Integrations
