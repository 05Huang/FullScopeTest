/**
 * 测试计划列表页面
 *
 * 展示项目下的测试计划，支持创建、编辑、删除和查看运行历史。
 */
import { useState, useEffect, useCallback } from 'react'
import {
  Card,
  Table,
  Button,
  Modal,
  Input,
  Tag,
  message,
  Space,
  Typography,
  Popconfirm,
  Empty,
} from 'antd'
import {
  PlusOutlined,
  PlayCircleOutlined,
  EyeOutlined,
  DeleteOutlined,
  ExperimentOutlined,
} from '@ant-design/icons'
import { useTranslation } from 'react-i18next'
import { useNavigate } from 'react-router-dom'
import type { ColumnsType } from 'antd/es/table'
import { useProjectStore } from '@/stores/projectStore'
import testPlanService, { TestPlan } from '@/services/testPlanService'
import PermissionButton from '@/components/PermissionButton'

const { Title } = Typography

const TestPlans = () => {
  const { t } = useTranslation()
  const navigate = useNavigate()
  const { currentProjectId } = useProjectStore()
  const [plans, setPlans] = useState<TestPlan[]>([])
  const [total, setTotal] = useState(0)
  const [loading, setLoading] = useState(false)
  const [page, setPage] = useState(1)
  const [pageSize, setPageSize] = useState(20)
  const [createModalOpen, setCreateModalOpen] = useState(false)
  const [createLoading, setCreateLoading] = useState(false)
  const [formName, setFormName] = useState('')
  const [formDesc, setFormDesc] = useState('')

  const fetchPlans = useCallback(async () => {
    if (!currentProjectId) return
    setLoading(true)
    try {
      const res = await testPlanService.getTestPlans({
        project_id: currentProjectId,
        page,
        per_page: pageSize,
      })
      if (res.code === 200 && res.data) {
        setPlans(res.data.items || [])
        setTotal(res.data.total || 0)
      }
    } catch {
      message.error(t('testPlans.fetchFailed'))
    } finally {
      setLoading(false)
    }
  }, [currentProjectId, page, pageSize, t])

  useEffect(() => {
    fetchPlans()
  }, [fetchPlans])

  const handleCreate = async () => {
    if (!formName.trim() || !currentProjectId) return
    setCreateLoading(true)
    try {
      const res = await testPlanService.createTestPlan({
        name: formName.trim(),
        project_id: currentProjectId,
        description: formDesc.trim(),
      })
      if ((res.code === 200 || res.code === 201) && res.data) {
        message.success(t('testPlans.createSuccess'))
        setCreateModalOpen(false)
        setFormName('')
        setFormDesc('')
        await fetchPlans()
      } else {
        message.error(res.message || t('testPlans.createFailed'))
      }
    } catch {
      message.error(t('testPlans.createFailed'))
    } finally {
      setCreateLoading(false)
    }
  }

  const handleDelete = async (planId: number) => {
    try {
      const res = await testPlanService.deleteTestPlan(planId)
      if (res.code === 200) {
        message.success(t('testPlans.deleteSuccess'))
        await fetchPlans()
      } else {
        message.error(res.message || t('testPlans.deleteFailed'))
      }
    } catch {
      message.error(t('testPlans.deleteFailed'))
    }
  }

  const handleRun = async (planId: number) => {
    try {
      const res = await testPlanService.createTestPlanRun(planId)
      if ((res.code === 200 || res.code === 201)) {
        message.success(t('testPlans.runCreated'))
        navigate(`/test-plans/${planId}`)
      } else {
        message.error(res.message || t('testPlans.runFailed'))
      }
    } catch {
      message.error(t('testPlans.runFailed'))
    }
  }

  const columns: ColumnsType<TestPlan> = [
    {
      title: t('common.name'),
      dataIndex: 'name',
      key: 'name',
      render: (name: string, record: TestPlan) => (
        <a onClick={() => navigate(`/test-plans/${record.id}`)} style={{ fontWeight: 500 }}>
          {name}
        </a>
      ),
    },
    {
      title: t('common.description'),
      dataIndex: 'description',
      key: 'description',
      ellipsis: true,
      render: (desc: string) => desc || '-',
    },
    {
      title: t('testPlans.caseCount'),
      dataIndex: 'case_count',
      key: 'case_count',
      width: 100,
      render: (count: number, record: TestPlan) => count ?? record.include_cases?.length ?? 0,
    },
    {
      title: t('testPlans.tags'),
      dataIndex: 'tags',
      key: 'tags',
      render: (tags: string[]) => (
        <Space size={4} wrap>
          {(tags || []).map((tag) => <Tag key={tag}>{tag}</Tag>)}
        </Space>
      ),
    },
    {
      title: t('testPlans.status'),
      dataIndex: 'status',
      key: 'status',
      width: 100,
      render: (status: string) => {
        const colorMap: Record<string, string> = {
          active: 'green',
          draft: 'default',
          archived: 'orange',
        }
        return <Tag color={colorMap[status] || 'default'}>{status || 'active'}</Tag>
      },
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
      width: 200,
      render: (_: unknown, record: TestPlan) => (
        <Space>
          <Button
            type="link"
            size="small"
            icon={<EyeOutlined />}
            onClick={() => navigate(`/test-plans/${record.id}`)}
          >
            {t('common.view')}
          </Button>
          <Button
            type="link"
            size="small"
            icon={<PlayCircleOutlined />}
            onClick={() => handleRun(record.id)}
          >
            {t('testPlans.run')}
          </Button>
          <Popconfirm
            title={t('testPlans.deleteConfirm')}
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
        <Title level={4} style={{ margin: 0 }}>
          <ExperimentOutlined style={{ marginRight: 8 }} />
          {t('testPlans.title')}
        </Title>
        <PermissionButton
          type="primary"
          icon={<PlusOutlined />}
          onClick={() => setCreateModalOpen(true)}
          disabled={!currentProjectId}
          roles={['admin', 'member']}
          mode="disable"
          noPermissionTip={t('common.noPermission') || 'No permission'}
        >
          {t('testPlans.create')}
        </PermissionButton>
      </div>

      {!currentProjectId && (
        <Card>
          <Empty description={t('testPlans.selectProjectFirst')} />
        </Card>
      )}

      {currentProjectId && (
        <Card>
          <Table
            columns={columns}
            dataSource={plans}
            rowKey="id"
            loading={loading}
            locale={{ emptyText: <Empty description={t('testPlans.noPlans')} /> }}
            pagination={{
              current: page,
              pageSize,
              total,
              showSizeChanger: true,
              showTotal: (totalVal) => `${totalVal} ${t('common.count')}`,
              onChange: (p, ps) => {
                setPage(p)
                setPageSize(ps)
              },
            }}
          />
        </Card>
      )}

      {/* 创建计划弹窗 */}
      <Modal
        title={t('testPlans.create')}
        open={createModalOpen}
        onCancel={() => { setCreateModalOpen(false); setFormName(''); setFormDesc('') }}
        onOk={handleCreate}
        confirmLoading={createLoading}
        okText={t('common.confirm')}
        cancelText={t('common.cancel')}
        destroyOnHidden
      >
        <div style={{ display: 'flex', flexDirection: 'column', gap: 16, marginTop: 8 }}>
          <div>
            <div style={{ marginBottom: 6, fontWeight: 500, fontSize: 13 }}>{t('testPlans.planName')}</div>
            <Input
              placeholder={t('testPlans.planNamePlaceholder')}
              value={formName}
              onChange={(e) => setFormName(e.target.value)}
              maxLength={100}
              autoFocus
            />
          </div>
          <div>
            <div style={{ marginBottom: 6, fontWeight: 500, fontSize: 13 }}>{t('common.description')}</div>
            <Input.TextArea
              placeholder={t('testPlans.planDescPlaceholder')}
              value={formDesc}
              onChange={(e) => setFormDesc(e.target.value)}
              rows={3}
              maxLength={500}
            />
          </div>
        </div>
      </Modal>
    </div>
  )
}

export default TestPlans
