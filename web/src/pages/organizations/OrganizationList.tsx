/**
 * 组织列表页面
 *
 * 展示当前用户所属的组织，支持创建/编辑/删除操作。
 */
import { useState, useEffect, useCallback } from 'react'
import {
  Card,
  Table,
  Button,
  Modal,
  Input,
  message,
  Space,
  Typography,
  Tag,
  Popconfirm,
  Empty,
  Spin,
} from 'antd'
import {
  PlusOutlined,
  EditOutlined,
  DeleteOutlined,
  TeamOutlined,
  SettingOutlined,
} from '@ant-design/icons'
import { useTranslation } from 'react-i18next'
import { useNavigate } from 'react-router-dom'
import type { ColumnsType } from 'antd/es/table'
import organizationService, { Organization } from '@/services/organizationService'

const { Title } = Typography

const OrganizationList = () => {
  const { t } = useTranslation()
  const navigate = useNavigate()
  const [organizations, setOrganizations] = useState<Organization[]>([])
  const [loading, setLoading] = useState(false)
  const [createModalOpen, setCreateModalOpen] = useState(false)
  const [editModalOpen, setEditModalOpen] = useState(false)
  const [editingOrg, setEditingOrg] = useState<Organization | null>(null)
  const [formName, setFormName] = useState('')
  const [formDesc, setFormDesc] = useState('')
  const [formSlug, setFormSlug] = useState('')
  const [submitLoading, setSubmitLoading] = useState(false)

  const fetchOrganizations = useCallback(async () => {
    setLoading(true)
    try {
      const res = await organizationService.getMyOrganizations()
      if (res.code === 200) {
        setOrganizations(res.data || [])
      }
    } catch {
      message.error(t('organizations.fetchFailed'))
    } finally {
      setLoading(false)
    }
  }, [t])

  useEffect(() => {
    fetchOrganizations()
  }, [fetchOrganizations])

  const handleCreate = async () => {
    if (!formName.trim()) return
    setSubmitLoading(true)
    try {
      const res = await organizationService.createOrganization({
        name: formName.trim(),
        slug: formSlug.trim() || undefined,
        description: formDesc.trim() || undefined,
      })
      if (res.code === 200 || res.code === 201) {
        message.success(t('organizations.createSuccess'))
        setCreateModalOpen(false)
        resetForm()
        await fetchOrganizations()
      } else {
        message.error(res.message || t('organizations.createFailed'))
      }
    } catch {
      message.error(t('organizations.createFailed'))
    } finally {
      setSubmitLoading(false)
    }
  }

  const handleEdit = async () => {
    if (!editingOrg || !formName.trim()) return
    setSubmitLoading(true)
    try {
      const res = await organizationService.updateOrganization(editingOrg.id, {
        name: formName.trim(),
        description: formDesc.trim() || undefined,
      })
      if (res.code === 200) {
        message.success(t('organizations.updateSuccess'))
        setEditModalOpen(false)
        setEditingOrg(null)
        resetForm()
        await fetchOrganizations()
      } else {
        message.error(res.message || t('organizations.updateFailed'))
      }
    } catch {
      message.error(t('organizations.updateFailed'))
    } finally {
      setSubmitLoading(false)
    }
  }

  const handleDelete = async (orgId: number) => {
    try {
      const res = await organizationService.deleteOrganization(orgId)
      if (res.code === 200) {
        message.success(t('organizations.deleteSuccess'))
        await fetchOrganizations()
      } else {
        message.error(res.message || t('organizations.deleteFailed'))
      }
    } catch {
      message.error(t('organizations.deleteFailed'))
    }
  }

  const resetForm = () => {
    setFormName('')
    setFormDesc('')
    setFormSlug('')
  }

  const openEditModal = (org: Organization) => {
    setEditingOrg(org)
    setFormName(org.name)
    setFormDesc(org.description || '')
    setFormSlug(org.slug)
    setEditModalOpen(true)
  }

  const columns: ColumnsType<Organization> = [
    {
      title: t('common.name'),
      dataIndex: 'name',
      key: 'name',
      render: (name: string, record: Organization) => (
        <a onClick={() => navigate(`/organizations/${record.id}`)} style={{ fontWeight: 500 }}>
          {name}
        </a>
      ),
    },
    {
      title: 'Slug',
      dataIndex: 'slug',
      key: 'slug',
      render: (slug: string) => <Tag>{slug}</Tag>,
    },
    {
      title: t('common.description'),
      dataIndex: 'description',
      key: 'description',
      ellipsis: true,
      render: (desc: string) => desc || '-',
    },
    {
      title: t('organizations.memberCount'),
      dataIndex: 'member_count',
      key: 'member_count',
      width: 100,
      render: (count: number) => (
        <Space>
          <TeamOutlined />
          <span>{count ?? '-'}</span>
        </Space>
      ),
    },
    {
      title: t('common.createdAt'),
      dataIndex: 'created_at',
      key: 'created_at',
      width: 180,
      render: (val: string) => (val ? new Date(val).toLocaleString() : '-'),
    },
    {
      title: t('common.actions'),
      key: 'actions',
      width: 160,
      render: (_: unknown, record: Organization) => (
        <Space>
          <Button
            type="link"
            size="small"
            icon={<SettingOutlined />}
            onClick={() => navigate(`/organizations/${record.id}`)}
          >
            {t('organizations.manage')}
          </Button>
          <Button
            type="link"
            size="small"
            icon={<EditOutlined />}
            onClick={() => openEditModal(record)}
          />
          <Popconfirm
            title={t('organizations.deleteConfirm')}
            onConfirm={() => handleDelete(record.id)}
            okText={t('common.confirm')}
            cancelText={t('common.cancel')}
          >
            <Button type="link" size="small" danger icon={<DeleteOutlined />} />
          </Popconfirm>
        </Space>
      ),
    },
  ]

  return (
    <div style={{ padding: 0 }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 16 }}>
        <Title level={4} style={{ margin: 0 }}>{t('organizations.title')}</Title>
        <Button
          type="primary"
          icon={<PlusOutlined />}
          onClick={() => {
            resetForm()
            setCreateModalOpen(true)
          }}
        >
          {t('organizations.create')}
        </Button>
      </div>

      <Card>
        <Table
          columns={columns}
          dataSource={organizations}
          rowKey="id"
          loading={loading}
          locale={{ emptyText: <Empty description={t('organizations.noOrganizations')} /> }}
          pagination={{ pageSize: 20, showSizeChanger: true, showTotal: (total) => `${total} ${t('common.count')}` }}
        />
      </Card>

      {/* 创建组织弹窗 */}
      <Modal
        title={t('organizations.create')}
        open={createModalOpen}
        onCancel={() => { setCreateModalOpen(false); resetForm() }}
        onOk={handleCreate}
        confirmLoading={submitLoading}
        okText={t('common.confirm')}
        cancelText={t('common.cancel')}
        destroyOnHidden
      >
        <div style={{ display: 'flex', flexDirection: 'column', gap: 16, marginTop: 8 }}>
          <div>
            <div style={{ marginBottom: 6, fontWeight: 500, fontSize: 13 }}>{t('organizations.orgName')}</div>
            <Input
              placeholder={t('organizations.orgNamePlaceholder')}
              value={formName}
              onChange={(e) => setFormName(e.target.value)}
              maxLength={100}
              autoFocus
            />
          </div>
          <div>
            <div style={{ marginBottom: 6, fontWeight: 500, fontSize: 13 }}>Slug</div>
            <Input
              placeholder={t('organizations.slugPlaceholder')}
              value={formSlug}
              onChange={(e) => setFormSlug(e.target.value)}
              maxLength={50}
            />
          </div>
          <div>
            <div style={{ marginBottom: 6, fontWeight: 500, fontSize: 13 }}>{t('common.description')}</div>
            <Input.TextArea
              placeholder={t('organizations.orgDescPlaceholder')}
              value={formDesc}
              onChange={(e) => setFormDesc(e.target.value)}
              rows={3}
              maxLength={200}
            />
          </div>
        </div>
      </Modal>

      {/* 编辑组织弹窗 */}
      <Modal
        title={t('organizations.edit')}
        open={editModalOpen}
        onCancel={() => { setEditModalOpen(false); setEditingOrg(null); resetForm() }}
        onOk={handleEdit}
        confirmLoading={submitLoading}
        okText={t('common.confirm')}
        cancelText={t('common.cancel')}
        destroyOnHidden
      >
        <div style={{ display: 'flex', flexDirection: 'column', gap: 16, marginTop: 8 }}>
          <div>
            <div style={{ marginBottom: 6, fontWeight: 500, fontSize: 13 }}>{t('organizations.orgName')}</div>
            <Input
              placeholder={t('organizations.orgNamePlaceholder')}
              value={formName}
              onChange={(e) => setFormName(e.target.value)}
              maxLength={100}
              autoFocus
            />
          </div>
          <div>
            <div style={{ marginBottom: 6, fontWeight: 500, fontSize: 13 }}>{t('common.description')}</div>
            <Input.TextArea
              placeholder={t('organizations.orgDescPlaceholder')}
              value={formDesc}
              onChange={(e) => setFormDesc(e.target.value)}
              rows={3}
              maxLength={200}
            />
          </div>
        </div>
      </Modal>
    </div>
  )
}

export default OrganizationList
