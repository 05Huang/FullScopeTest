/**
 * 组织详情页面
 *
 * 包含成员管理和角色管理两个 Tab。
 * 根据当前用户角色动态展示操作按钮。
 */
import { useState, useEffect, useCallback } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { Card, Tabs, Typography, Button, Spin, Result, message } from 'antd'
import { ArrowLeftOutlined, TeamOutlined, SafetyOutlined } from '@ant-design/icons'
import { useTranslation } from 'react-i18next'
import organizationService, { Organization } from '@/services/organizationService'
import MemberManagement from './MemberManagement'
import RoleManagement from './RoleManagement'

const { Title } = Typography

const OrganizationDetail = () => {
  const { orgId } = useParams<{ orgId: string }>()
  const navigate = useNavigate()
  const { t } = useTranslation()
  const [organization, setOrganization] = useState<Organization | null>(null)
  const [loading, setLoading] = useState(true)
  const [activeTab, setActiveTab] = useState('members')
  const [userRole, setUserRole] = useState<string | null>(null)

  const orgIdNum = orgId ? parseInt(orgId, 10) : null

  const fetchOrganization = useCallback(async () => {
    if (!orgIdNum) return
    setLoading(true)
    try {
      // 从组织列表中获取当前组织信息
      const res = await organizationService.getMyOrganizations()
      if (res.code === 200 && res.data) {
        const found = res.data.find((o) => o.id === orgIdNum)
        if (found) {
          setOrganization(found)
        }
      }
      // 获取当前用户在该组织中的角色
      const permRes = await organizationService.getMyPermissions(orgIdNum)
      if (permRes.code === 200 && permRes.data) {
        setUserRole(permRes.data.role)
      }
    } catch {
      message.error(t('organizations.fetchFailed'))
    } finally {
      setLoading(false)
    }
  }, [orgIdNum, t])

  useEffect(() => {
    fetchOrganization()
  }, [fetchOrganization])

  if (loading) {
    return (
      <div style={{ display: 'flex', justifyContent: 'center', paddingTop: 120 }}>
        <Spin size="large" />
      </div>
    )
  }

  if (!organization) {
    return (
      <Result
        status="404"
        title={t('organizations.notFound')}
        subTitle={t('organizations.notFoundDesc')}
        extra={
          <Button type="primary" onClick={() => navigate('/organizations')}>
            {t('common.back')}
          </Button>
        }
      />
    )
  }

  const isAdmin = userRole === 'admin'

  return (
    <div style={{ padding: 0 }}>
      {/* 顶部导航 */}
      <div style={{ display: 'flex', alignItems: 'center', gap: 12, marginBottom: 16 }}>
        <Button
          type="text"
          icon={<ArrowLeftOutlined />}
          onClick={() => navigate('/organizations')}
        />
        <Title level={4} style={{ margin: 0 }}>{organization.name}</Title>
        {organization.description && (
          <span style={{ color: 'var(--fst-on-surface-variant)', fontSize: 14 }}>
            {organization.description}
          </span>
        )}
      </div>

      <Card>
        <Tabs
          activeKey={activeTab}
          onChange={setActiveTab}
          items={[
            {
              key: 'members',
              label: (
                <span>
                  <TeamOutlined style={{ marginRight: 6 }} />
                  {t('organizations.members')}
                </span>
              ),
              children: (
                <MemberManagement
                  orgId={orgIdNum!}
                  isAdmin={isAdmin}
                  userRole={userRole}
                />
              ),
            },
            {
              key: 'roles',
              label: (
                <span>
                  <SafetyOutlined style={{ marginRight: 6 }} />
                  {t('organizations.roles')}
                </span>
              ),
              children: (
                <RoleManagement
                  orgId={orgIdNum!}
                  isAdmin={isAdmin}
                />
              ),
            },
          ]}
        />
      </Card>
    </div>
  )
}

export default OrganizationDetail
