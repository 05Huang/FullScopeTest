/**
 * 角色管理组件
 *
 * 展示组织角色列表及权限矩阵，支持创建/编辑/删除自定义角色。
 */
import { useState, useEffect, useCallback } from 'react'
import {
  Table,
  Button,
  Modal,
  Input,
  Form,
  message,
  Space,
  Tag,
  Popconfirm,
  Empty,
  Collapse,
  Checkbox,
  Typography,
} from 'antd'
import { PlusOutlined, EditOutlined, DeleteOutlined, LockOutlined } from '@ant-design/icons'
import { useTranslation } from 'react-i18next'
import type { ColumnsType } from 'antd/es/table'
import organizationService, { RoleInfo } from '@/services/organizationService'

const { Text } = Typography

// 系统定义的资源和操作
const RESOURCES = ['project', 'test_case', 'test_run', 'environment', 'report', 'ai_feature']
const ACTIONS = ['create', 'read', 'update', 'delete', 'execute', 'manage']

interface RoleManagementProps {
  orgId: number
  isAdmin: boolean
}

const RoleManagement = ({ orgId, isAdmin }: RoleManagementProps) => {
  const { t } = useTranslation()
  const [roles, setRoles] = useState<RoleInfo[]>([])
  const [loading, setLoading] = useState(false)
  const [createModalOpen, setCreateModalOpen] = useState(false)
  const [editModalOpen, setEditModalOpen] = useState(false)
  const [editingRole, setEditingRole] = useState<RoleInfo | null>(null)
  const [formName, setFormName] = useState('')
  const [formDisplayName, setFormDisplayName] = useState('')
  const [formDesc, setFormDesc] = useState('')
  const [formPermissions, setFormPermissions] = useState<Record<string, string[]>>({})
  const [submitLoading, setSubmitLoading] = useState(false)

  const fetchRoles = useCallback(async () => {
    setLoading(true)
    try {
      const res = await organizationService.getRoles(orgId)
      if (res.code === 200) {
        setRoles(res.data || [])
      }
    } catch {
      message.error(t('organizations.fetchRolesFailed'))
    } finally {
      setLoading(false)
    }
  }, [orgId, t])

  useEffect(() => {
    fetchRoles()
  }, [fetchRoles])

  const resetForm = () => {
    setFormName('')
    setFormDisplayName('')
    setFormDesc('')
    setFormPermissions({})
  }

  const handleCreate = async () => {
    if (!formName.trim() || !formDisplayName.trim()) return
    setSubmitLoading(true)
    try {
      const res = await organizationService.createRole(orgId, {
        name: formName.trim(),
        display_name: formDisplayName.trim(),
        permissions: formPermissions,
        description: formDesc.trim(),
      })
      if (res.code === 200 || res.code === 201) {
        message.success(t('organizations.roleCreateSuccess'))
        setCreateModalOpen(false)
        resetForm()
        await fetchRoles()
      } else {
        message.error(res.message || t('organizations.roleCreateFailed'))
      }
    } catch {
      message.error(t('organizations.roleCreateFailed'))
    } finally {
      setSubmitLoading(false)
    }
  }

  const handleEdit = async () => {
    if (!editingRole || !formDisplayName.trim()) return
    setSubmitLoading(true)
    try {
      const res = await organizationService.updateRole(orgId, editingRole.id!, {
        display_name: formDisplayName.trim(),
        permissions: formPermissions,
        description: formDesc.trim(),
      })
      if (res.code === 200) {
        message.success(t('organizations.roleUpdateSuccess'))
        setEditModalOpen(false)
        setEditingRole(null)
        resetForm()
        await fetchRoles()
      } else {
        message.error(res.message || t('organizations.roleUpdateFailed'))
      }
    } catch {
      message.error(t('organizations.roleUpdateFailed'))
    } finally {
      setSubmitLoading(false)
    }
  }

  const handleDelete = async (roleId: number) => {
    try {
      const res = await organizationService.deleteRole(orgId, roleId)
      if (res.code === 200) {
        message.success(t('organizations.roleDeleteSuccess'))
        await fetchRoles()
      } else {
        message.error(res.message || t('organizations.roleDeleteFailed'))
      }
    } catch {
      message.error(t('organizations.roleDeleteFailed'))
    }
  }

  const openEditModal = (role: RoleInfo) => {
    setEditingRole(role)
    setFormName(role.name)
    setFormDisplayName(role.display_name)
    setFormDesc(role.description || '')
    setFormPermissions(role.permissions || {})
    setEditModalOpen(true)
  }

  const togglePermission = (resource: string, action: string) => {
    setFormPermissions((prev) => {
      const current = prev[resource] || []
      const has = current.includes(action)
      return {
        ...prev,
        [resource]: has ? current.filter((a) => a !== action) : [...current, action],
      }
    })
  }

  const toggleAllActions = (resource: string) => {
    setFormPermissions((prev) => {
      const current = prev[resource] || []
      const allSelected = ACTIONS.every((a) => current.includes(a))
      return {
        ...prev,
        [resource]: allSelected ? [] : [...ACTIONS],
      }
    })
  }

  const columns: ColumnsType<RoleInfo> = [
    {
      title: t('organizations.roleName'),
      dataIndex: 'display_name',
      key: 'display_name',
      render: (name: string, record: RoleInfo) => (
        <Space>
          <span style={{ fontWeight: 500 }}>{name}</span>
          {record.is_system && <LockOutlined style={{ color: '#999', fontSize: 12 }} />}
        </Space>
      ),
    },
    {
      title: 'Identifier',
      dataIndex: 'name',
      key: 'name',
      render: (name: string) => <Tag>{name}</Tag>,
    },
    {
      title: t('common.description'),
      dataIndex: 'description',
      key: 'description',
      ellipsis: true,
      render: (desc: string) => desc || '-',
    },
    {
      title: t('organizations.type'),
      dataIndex: 'is_system',
      key: 'is_system',
      width: 100,
      render: (isSystem: boolean) => (
        <Tag color={isSystem ? 'blue' : 'green'}>
          {isSystem ? t('organizations.systemRole') : t('organizations.customRole')}
        </Tag>
      ),
    },
    ...(isAdmin
      ? [
          {
            title: t('common.actions'),
            key: 'actions',
            width: 140,
            render: (_: unknown, record: RoleInfo) => (
              <Space>
                {!record.is_system && (
                  <>
                    <Button
                      type="link"
                      size="small"
                      icon={<EditOutlined />}
                      onClick={() => openEditModal(record)}
                    />
                    <Popconfirm
                      title={t('organizations.roleDeleteConfirm')}
                      onConfirm={() => handleDelete(record.id!)}
                      okText={t('common.confirm')}
                      cancelText={t('common.cancel')}
                    >
                      <Button type="link" size="small" danger icon={<DeleteOutlined />} />
                    </Popconfirm>
                  </>
                )}
              </Space>
            ),
          },
        ]
      : []),
  ]

  // 权限矩阵渲染
  const renderPermissionMatrix = () => (
    <div style={{ overflowX: 'auto' }}>
      <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: 13 }}>
        <thead>
          <tr>
            <th style={{ textAlign: 'left', padding: '8px 12px', borderBottom: '1px solid #f0f0f0' }}>
              {t('organizations.resource')}
            </th>
            {ACTIONS.map((action) => (
              <th
                key={action}
                style={{ textAlign: 'center', padding: '8px 8px', borderBottom: '1px solid #f0f0f0', textTransform: 'capitalize' }}
              >
                {action}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {RESOURCES.map((resource) => (
            <tr key={resource}>
              <td style={{ padding: '8px 12px', borderBottom: '1px solid #f0f0f0' }}>
                <Space>
                  <Checkbox
                    checked={(formPermissions[resource] || []).length === ACTIONS.length}
                    indeterminate={
                      (formPermissions[resource] || []).length > 0 &&
                      (formPermissions[resource] || []).length < ACTIONS.length
                    }
                    onChange={() => toggleAllActions(resource)}
                  />
                  <span style={{ textTransform: 'capitalize' }}>{resource.replace('_', ' ')}</span>
                </Space>
              </td>
              {ACTIONS.map((action) => (
                <td
                  key={action}
                  style={{ textAlign: 'center', padding: '8px 8px', borderBottom: '1px solid #f0f0f0' }}
                >
                  <Checkbox
                    checked={(formPermissions[resource] || []).includes(action)}
                    onChange={() => togglePermission(resource, action)}
                  />
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )

  // 角色权限展示（只读）
  const expandedRowRender = (record: RoleInfo) => {
    const perms = record.permissions || {}
    return (
      <div style={{ padding: '8px 0' }}>
        <Text strong style={{ fontSize: 13, marginBottom: 8, display: 'block' }}>
          {t('organizations.permissions')}
        </Text>
        <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: 12 }}>
          <thead>
            <tr>
              <th style={{ textAlign: 'left', padding: '4px 8px' }}>{t('organizations.resource')}</th>
              {ACTIONS.map((a) => (
                <th key={a} style={{ textAlign: 'center', padding: '4px 6px', textTransform: 'capitalize' }}>
                  {a}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {RESOURCES.map((resource) => {
              const allowed = perms[resource] || []
              return (
                <tr key={resource}>
                  <td style={{ padding: '4px 8px', textTransform: 'capitalize' }}>
                    {resource.replace('_', ' ')}
                  </td>
                  {ACTIONS.map((action) => (
                    <td key={action} style={{ textAlign: 'center', padding: '4px 6px' }}>
                      {allowed.includes(action) ? (
                        <Tag color="green" style={{ fontSize: 11, lineHeight: '18px', padding: '0 4px' }}>✓</Tag>
                      ) : (
                        <span style={{ color: '#ccc' }}>—</span>
                      )}
                    </td>
                  ))}
                </tr>
              )
            })}
          </tbody>
        </table>
      </div>
    )
  }

  return (
    <div>
      <div style={{ display: 'flex', justifyContent: 'flex-end', marginBottom: 16 }}>
        {isAdmin && (
          <Button
            type="primary"
            icon={<PlusOutlined />}
            onClick={() => {
              resetForm()
              setCreateModalOpen(true)
            }}
          >
            {t('organizations.createRole')}
          </Button>
        )}
      </div>

      <Table
        columns={columns}
        dataSource={roles}
        rowKey={(r) => r.id?.toString() || r.name}
        loading={loading}
        locale={{ emptyText: <Empty description={t('organizations.noRoles')} /> }}
        pagination={false}
        expandable={{
          expandedRowRender,
          rowExpandable: (record) => !!record.permissions && Object.keys(record.permissions).length > 0,
        }}
      />

      {/* 创建角色弹窗 */}
      <Modal
        title={t('organizations.createRole')}
        open={createModalOpen}
        onCancel={() => { setCreateModalOpen(false); resetForm() }}
        onOk={handleCreate}
        confirmLoading={submitLoading}
        okText={t('common.confirm')}
        cancelText={t('common.cancel')}
        width={720}
        destroyOnHidden
      >
        <div style={{ display: 'flex', flexDirection: 'column', gap: 16, marginTop: 8 }}>
          <div style={{ display: 'flex', gap: 16 }}>
            <div style={{ flex: 1 }}>
              <div style={{ marginBottom: 6, fontWeight: 500, fontSize: 13 }}>Identifier</div>
              <Input
                placeholder={t('organizations.roleNamePlaceholder')}
                value={formName}
                onChange={(e) => setFormName(e.target.value)}
                maxLength={50}
              />
            </div>
            <div style={{ flex: 1 }}>
              <div style={{ marginBottom: 6, fontWeight: 500, fontSize: 13 }}>{t('organizations.displayName')}</div>
              <Input
                placeholder={t('organizations.displayNamePlaceholder')}
                value={formDisplayName}
                onChange={(e) => setFormDisplayName(e.target.value)}
                maxLength={50}
              />
            </div>
          </div>
          <div>
            <div style={{ marginBottom: 6, fontWeight: 500, fontSize: 13 }}>{t('common.description')}</div>
            <Input.TextArea
              placeholder={t('organizations.roleDescPlaceholder')}
              value={formDesc}
              onChange={(e) => setFormDesc(e.target.value)}
              rows={2}
              maxLength={200}
            />
          </div>
          <div>
            <div style={{ marginBottom: 8, fontWeight: 500, fontSize: 13 }}>{t('organizations.permissions')}</div>
            {renderPermissionMatrix()}
          </div>
        </div>
      </Modal>

      {/* 编辑角色弹窗 */}
      <Modal
        title={t('organizations.editRole')}
        open={editModalOpen}
        onCancel={() => { setEditModalOpen(false); setEditingRole(null); resetForm() }}
        onOk={handleEdit}
        confirmLoading={submitLoading}
        okText={t('common.confirm')}
        cancelText={t('common.cancel')}
        width={720}
        destroyOnHidden
      >
        <div style={{ display: 'flex', flexDirection: 'column', gap: 16, marginTop: 8 }}>
          <div>
            <div style={{ marginBottom: 6, fontWeight: 500, fontSize: 13 }}>{t('organizations.displayName')}</div>
            <Input
              placeholder={t('organizations.displayNamePlaceholder')}
              value={formDisplayName}
              onChange={(e) => setFormDisplayName(e.target.value)}
              maxLength={50}
            />
          </div>
          <div>
            <div style={{ marginBottom: 6, fontWeight: 500, fontSize: 13 }}>{t('common.description')}</div>
            <Input.TextArea
              placeholder={t('organizations.roleDescPlaceholder')}
              value={formDesc}
              onChange={(e) => setFormDesc(e.target.value)}
              rows={2}
              maxLength={200}
            />
          </div>
          <div>
            <div style={{ marginBottom: 8, fontWeight: 500, fontSize: 13 }}>{t('organizations.permissions')}</div>
            {renderPermissionMatrix()}
          </div>
        </div>
      </Modal>
    </div>
  )
}

export default RoleManagement
