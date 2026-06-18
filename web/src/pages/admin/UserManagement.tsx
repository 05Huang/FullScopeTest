import React, { useState, useEffect, useCallback } from 'react'
import { Table, Button, Tag, Space, Input, Select, Modal, Form, message, Typography, Avatar, Switch, Popconfirm, Tooltip, Row, Col, Statistic } from 'antd'
import { UserOutlined, SearchOutlined, ReloadOutlined, SafetyOutlined, StopOutlined, CheckCircleOutlined, KeyOutlined, TeamOutlined } from '@ant-design/icons'
import { useTranslation } from 'react-i18next'
import { adminService, AdminUser } from '@/services/adminService'
import { useRole } from '@/hooks/useRole'

const { Text } = Typography

const UserManagement: React.FC = () => {
  const { t } = useTranslation()
  const { isAdmin } = useRole()
  const [users, setUsers] = useState<AdminUser[]>([])
  const [loading, setLoading] = useState(false)
  const [total, setTotal] = useState(0)
  const [page, setPage] = useState(1)
  const [pageSize, setPageSize] = useState(20)
  const [search, setSearch] = useState('')
  const [roleFilter, setRoleFilter] = useState('')
  const [resetModalVisible, setResetModalVisible] = useState(false)
  const [resetUserId, setResetUserId] = useState<number | null>(null)
  const [resetForm] = Form.useForm()

  const fetchUsers = useCallback(async () => {
    setLoading(true)
    try {
      const res = await adminService.getUsers({ page, per_page: pageSize, search, role: roleFilter })
      if (res.code === 200 && res.data) { setUsers(res.data.items || []); setTotal(res.data.total || 0) }
    } catch (err: any) { message.error(err?.message || t('common.failed')) }
    finally { setLoading(false) }
  }, [page, pageSize, search, roleFilter, t])

  useEffect(() => { fetchUsers() }, [fetchUsers])

  const handleToggleStatus = async (user: AdminUser) => {
    try { await adminService.updateUserStatus(user.id, !user.is_active); message.success(user.is_active ? 'User disabled' : 'User enabled'); fetchUsers()
    } catch (err: any) { message.error(err?.response?.data?.message || 'Failed') }
  }

  const handleRoleChange = async (userId: number, newRole: string) => {
    try { await adminService.updateUserRole(userId, newRole); message.success('Role updated'); fetchUsers()
    } catch (err: any) { message.error(err?.response?.data?.message || 'Failed') }
  }

  const handleResetPassword = async () => {
    try {
      const values = await resetForm.validateFields()
      if (!resetUserId) return
      await adminService.resetPassword(resetUserId, values.password)
      message.success('Password reset'); setResetModalVisible(false); resetForm.resetFields()
    } catch (err: any) { if (err?.response?.data?.message) message.error(err.response.data.message) }
  }

  const columns = [
    { title: 'User', key: 'user', render: (_: any, r: AdminUser) => (
      <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
        <Avatar size={36} icon={<UserOutlined />} src={r.avatar} style={{ backgroundColor: 'var(--fst-primary)' }} />
        <div><div style={{ fontWeight: 600, fontSize: 14 }}>{r.username}</div><div style={{ fontSize: 12, color: 'var(--fst-on-surface-muted)' }}>{r.email}</div></div>
      </div>
    )},
    { title: 'Role', dataIndex: 'role', key: 'role', width: 140, render: (role: string, r: AdminUser) => (
      <Select value={role} onChange={v => handleRoleChange(r.id, v)} size="small" style={{ width: 120 }} disabled={r.username === 'huangxuan'}>
        <Select.Option value="admin"><Tag color="red" style={{ margin: 0 }}>Admin</Tag></Select.Option>
        <Select.Option value="member"><Tag color="blue" style={{ margin: 0 }}>Member</Tag></Select.Option>
        <Select.Option value="viewer"><Tag style={{ margin: 0 }}>Viewer</Tag></Select.Option>
      </Select>
    )},
    { title: 'Status', dataIndex: 'is_active', key: 'status', width: 100, render: (active: boolean, r: AdminUser) => (
      <Switch checked={active} onChange={() => handleToggleStatus(r)} disabled={r.username === 'huangxuan'} checkedChildren="On" unCheckedChildren="Off" size="small" />
    )},
    { title: 'Created', dataIndex: 'created_at', key: 'created_at', width: 130, render: (v: string) => v ? new Date(v).toLocaleDateString() : '-' },
    { title: 'Last Login', dataIndex: 'last_login', key: 'last_login', width: 130, render: (v: string) => {
      if (!v) return <Text type="secondary">Never</Text>
      const h = Math.floor((Date.now() - new Date(v).getTime()) / 3600000)
      if (h < 1) return <Text type="success">Just now</Text>
      if (h < 24) return <Text>{h}h ago</Text>
      return <Text>{Math.floor(h/24)}d ago</Text>
    }},
    { title: 'Actions', key: 'actions', width: 100, render: (_: any, r: AdminUser) => (
      <Space size={4}>
        <Tooltip title="Reset password"><Button type="text" size="small" icon={<KeyOutlined />} onClick={() => { setResetUserId(r.id); setResetModalVisible(true); resetForm.resetFields() }} /></Tooltip>
        <Popconfirm title={r.is_active ? 'Disable this user?' : 'Enable this user?'} onConfirm={() => handleToggleStatus(r)} disabled={r.username === 'huangxuan'}>
          <Tooltip title={r.is_active ? 'Disable' : 'Enable'}><Button type="text" size="small" danger={r.is_active} icon={r.is_active ? <StopOutlined /> : <CheckCircleOutlined />} disabled={r.username === 'huangxuan'} /></Tooltip>
        </Popconfirm>
      </Space>
    )},
  ]

  if (!isAdmin) return (
    <div style={{ textAlign: 'center', padding: 80 }}>
      <SafetyOutlined style={{ fontSize: 48, color: 'var(--fst-error)', marginBottom: 16 }} />
      <div style={{ fontSize: 18, fontWeight: 600, marginBottom: 8 }}>Access Denied</div>
      <div style={{ color: 'var(--fst-on-surface-muted)' }}>Only administrators can access user management</div>
    </div>
  )

  return (
    <div className="fst-page" style={{ maxWidth: 1200, margin: '0 auto' }}>
      <div className="fst-page-header fst-animate-in">
        <div>
          <h1 className="fst-page-title"><TeamOutlined style={{ marginRight: 8 }} />{t('admin.userManagement') || 'User Management'}</h1>
          <div className="fst-ios-card-subtitle">{t('admin.userManagementSubtitle') || 'Manage user accounts, roles and permissions'}</div>
        </div>
      </div>
      <Row gutter={16} style={{ marginBottom: 20 }} className="fst-animate-in fst-animate-in-1">
        <Col span={6}><div className="fst-ios-card" style={{ padding: 16 }}><Statistic title="Total Users" value={total} prefix={<TeamOutlined />} /></div></Col>
        <Col span={6}><div className="fst-ios-card" style={{ padding: 16 }}><Statistic title="Admins" value={users.filter(u => u.role === 'admin').length} valueStyle={{ color: '#cf1322' }} prefix={<SafetyOutlined />} /></div></Col>
        <Col span={6}><div className="fst-ios-card" style={{ padding: 16 }}><Statistic title="Active" value={users.filter(u => u.is_active).length} valueStyle={{ color: '#3f8600' }} prefix={<CheckCircleOutlined />} /></div></Col>
        <Col span={6}><div className="fst-ios-card" style={{ padding: 16 }}><Statistic title="Disabled" value={users.filter(u => !u.is_active).length} valueStyle={{ color: '#999' }} prefix={<StopOutlined />} /></div></Col>
      </Row>
      <div className="fst-ios-card fst-animate-in fst-animate-in-2" style={{ marginBottom: 16, padding: '12px 16px' }}>
        <div style={{ display: 'flex', gap: 12, alignItems: 'center' }}>
          <Input prefix={<SearchOutlined />} placeholder={t('admin.searchPlaceholder')} value={search} onChange={e => { setSearch(e.target.value); setPage(1) }} onPressEnter={fetchUsers} style={{ width: 280 }} allowClear />
          <Select value={roleFilter || undefined} onChange={v => { setRoleFilter(v || ''); setPage(1) }} placeholder={t('admin.filterRole')} style={{ width: 140 }} allowClear>
            <Select.Option value="admin">Admin</Select.Option><Select.Option value="member">Member</Select.Option><Select.Option value="viewer">Viewer</Select.Option>
          </Select>
          <Button icon={<ReloadOutlined />} onClick={fetchUsers}>Refresh</Button>
        </div>
      </div>
      <div className="fst-ios-card fst-animate-in fst-animate-in-3">
        <Table columns={columns} dataSource={users} rowKey="id" loading={loading}
          pagination={{ current: page, pageSize, total, showSizeChanger: true, showTotal: t => 'Total ' + t + ' users', onChange: (p, ps) => { setPage(p); setPageSize(ps) } }} size="middle" />
      </div>
      <Modal title="Reset Password" open={resetModalVisible} onOk={handleResetPassword} onCancel={() => { setResetModalVisible(false); resetForm.resetFields() }} okText="Reset" cancelText="Cancel">
        <Form form={resetForm} layout="vertical">
          <Form.Item label="New Password" name="password" rules={[{ required: true, message: 'Please enter new password' }, { min: 6, message: 'At least 6 characters' }]}>
            <Input.Password placeholder={t('admin.enterPassword')} />
          </Form.Item>
        </Form>
      </Modal>
    </div>
  )
}

export default UserManagement
