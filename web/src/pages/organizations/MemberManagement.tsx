/**
 * 成员管理组件
 *
 * 展示组织成员列表，支持邀请成员、修改角色、移除成员。
 */
import { useState, useEffect, useCallback } from 'react'
import {
  Table,
  Button,
  Modal,
  Select,
  InputNumber,
  message,
  Space,
  Tag,
  Popconfirm,
  Empty,
} from 'antd'
import { PlusOutlined, DeleteOutlined, UserSwitchOutlined } from '@ant-design/icons'
import { useTranslation } from 'react-i18next'
import type { ColumnsType } from 'antd/es/table'
import organizationService, { OrganizationMember } from '@/services/organizationService'

const VALID_ROLES = ['admin', 'manager', 'tester', 'viewer']

interface MemberManagementProps {
  orgId: number
  isAdmin: boolean
  userRole: string | null
}

const MemberManagement = ({ orgId, isAdmin, userRole }: MemberManagementProps) => {
  const { t } = useTranslation()
  const [members, setMembers] = useState<OrganizationMember[]>([])
  const [loading, setLoading] = useState(false)
  const [inviteModalOpen, setInviteModalOpen] = useState(false)
  const [inviteUserId, setInviteUserId] = useState<number | null>(null)
  const [inviteRole, setInviteRole] = useState('tester')
  const [inviteLoading, setInviteLoading] = useState(false)
  const [roleModalOpen, setRoleModalOpen] = useState(false)
  const [editingMember, setEditingMember] = useState<OrganizationMember | null>(null)
  const [newRole, setNewRole] = useState('')
  const [roleLoading, setRoleLoading] = useState(false)

  const fetchMembers = useCallback(async () => {
    setLoading(true)
    try {
      const res = await organizationService.getMembers(orgId)
      if (res.code === 200) {
        setMembers(res.data || [])
      }
    } catch {
      message.error(t('organizations.fetchMembersFailed'))
    } finally {
      setLoading(false)
    }
  }, [orgId, t])

  useEffect(() => {
    fetchMembers()
  }, [fetchMembers])

  const handleInvite = async () => {
    if (!inviteUserId) return
    setInviteLoading(true)
    try {
      const res = await organizationService.inviteMember(orgId, {
        user_id: inviteUserId,
        role: inviteRole,
      })
      if (res.code === 200 || res.code === 201) {
        message.success(t('organizations.inviteSuccess'))
        setInviteModalOpen(false)
        setInviteUserId(null)
        setInviteRole('tester')
        await fetchMembers()
      } else {
        message.error(res.message || t('organizations.inviteFailed'))
      }
    } catch {
      message.error(t('organizations.inviteFailed'))
    } finally {
      setInviteLoading(false)
    }
  }

  const handleRemove = async (userId: number) => {
    try {
      const res = await organizationService.removeMember(orgId, userId)
      if (res.code === 200) {
        message.success(t('organizations.removeSuccess'))
        await fetchMembers()
      } else {
        message.error(res.message || t('organizations.removeFailed'))
      }
    } catch {
      message.error(t('organizations.removeFailed'))
    }
  }

  const handleChangeRole = async () => {
    if (!editingMember || !newRole) return
    setRoleLoading(true)
    try {
      const res = await organizationService.updateMemberRole(orgId, editingMember.user_id, newRole)
      if (res.code === 200) {
        message.success(t('organizations.roleChangeSuccess'))
        setRoleModalOpen(false)
        setEditingMember(null)
        await fetchMembers()
      } else {
        message.error(res.message || t('organizations.roleChangeFailed'))
      }
    } catch {
      message.error(t('organizations.roleChangeFailed'))
    } finally {
      setRoleLoading(false)
    }
  }

  const getRoleColor = (role: string) => {
    switch (role) {
      case 'admin':
      case 'owner':
        return 'red'
      case 'manager':
        return 'orange'
      case 'tester':
        return 'green'
      case 'viewer':
        return 'default'
      default:
        return 'default'
    }
  }

  const columns: ColumnsType<OrganizationMember> = [
    {
      title: t('organizations.userId'),
      dataIndex: 'user_id',
      key: 'user_id',
      width: 80,
    },
    {
      title: t('organizations.username'),
      dataIndex: 'username',
      key: 'username',
      render: (name: string, record: OrganizationMember) => name || `User #${record.user_id}`,
    },
    {
      title: 'Email',
      dataIndex: 'email',
      key: 'email',
      render: (email: string) => email || '-',
    },
    {
      title: t('organizations.role'),
      dataIndex: 'role',
      key: 'role',
      width: 120,
      render: (role: string) => (
        <Tag color={getRoleColor(role)}>{role.toUpperCase()}</Tag>
      ),
    },
    {
      title: t('common.status'),
      dataIndex: 'is_active',
      key: 'is_active',
      width: 80,
      render: (active: boolean) => (
        <Tag color={active ? 'green' : 'default'}>
          {active ? t('organizations.active') : t('organizations.inactive')}
        </Tag>
      ),
    },
    {
      title: t('common.createdAt'),
      dataIndex: 'created_at',
      key: 'created_at',
      width: 180,
      render: (val: string) => (val ? new Date(val).toLocaleString() : '-'),
    },
    ...(isAdmin
      ? [
          {
            title: t('common.actions'),
            key: 'actions',
            width: 160,
            render: (_: unknown, record: OrganizationMember) => (
              <Space>
                <Button
                  type="link"
                  size="small"
                  icon={<UserSwitchOutlined />}
                  onClick={() => {
                    setEditingMember(record)
                    setNewRole(record.role)
                    setRoleModalOpen(true)
                  }}
                >
                  {t('organizations.changeRole')}
                </Button>
                <Popconfirm
                  title={t('organizations.removeMemberConfirm')}
                  onConfirm={() => handleRemove(record.user_id)}
                  okText={t('common.confirm')}
                  cancelText={t('common.cancel')}
                >
                  <Button type="link" size="small" danger icon={<DeleteOutlined />} />
                </Popconfirm>
              </Space>
            ),
          },
        ]
      : []),
  ]

  return (
    <div>
      <div style={{ display: 'flex', justifyContent: 'flex-end', marginBottom: 16 }}>
        {isAdmin && (
          <Button
            type="primary"
            icon={<PlusOutlined />}
            onClick={() => setInviteModalOpen(true)}
          >
            {t('organizations.inviteMember')}
          </Button>
        )}
      </div>

      <Table
        columns={columns}
        dataSource={members}
        rowKey="id"
        loading={loading}
        locale={{ emptyText: <Empty description={t('organizations.noMembers')} /> }}
        pagination={{ pageSize: 20 }}
      />

      {/* 邀请成员弹窗 */}
      <Modal
        title={t('organizations.inviteMember')}
        open={inviteModalOpen}
        onCancel={() => setInviteModalOpen(false)}
        onOk={handleInvite}
        confirmLoading={inviteLoading}
        okText={t('common.confirm')}
        cancelText={t('common.cancel')}
        destroyOnHidden
      >
        <div style={{ display: 'flex', flexDirection: 'column', gap: 16, marginTop: 8 }}>
          <div>
            <div style={{ marginBottom: 6, fontWeight: 500, fontSize: 13 }}>{t('organizations.userId')}</div>
            <InputNumber
              placeholder={t('organizations.userIdPlaceholder')}
              value={inviteUserId}
              onChange={(val) => setInviteUserId(val)}
              style={{ width: '100%' }}
              min={1}
            />
          </div>
          <div>
            <div style={{ marginBottom: 6, fontWeight: 500, fontSize: 13 }}>{t('organizations.role')}</div>
            <Select
              value={inviteRole}
              onChange={setInviteRole}
              style={{ width: '100%' }}
              options={VALID_ROLES.map((r) => ({
                value: r,
                label: r.charAt(0).toUpperCase() + r.slice(1),
              }))}
            />
          </div>
        </div>
      </Modal>

      {/* 修改角色弹窗 */}
      <Modal
        title={t('organizations.changeRole')}
        open={roleModalOpen}
        onCancel={() => { setRoleModalOpen(false); setEditingMember(null) }}
        onOk={handleChangeRole}
        confirmLoading={roleLoading}
        okText={t('common.confirm')}
        cancelText={t('common.cancel')}
        destroyOnHidden
      >
        <div style={{ marginTop: 8 }}>
          <div style={{ marginBottom: 6, fontWeight: 500, fontSize: 13 }}>
            {t('organizations.selectNewRole')}
          </div>
          <Select
            value={newRole}
            onChange={setNewRole}
            style={{ width: '100%' }}
            options={VALID_ROLES.map((r) => ({
              value: r,
              label: r.charAt(0).toUpperCase() + r.slice(1),
            }))}
          />
        </div>
      </Modal>
    </div>
  )
}

export default MemberManagement
