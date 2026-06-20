import logger from "@/utils/logger"
import React, { useState, useEffect } from 'react'
import {
  Card,
  Tabs,
  Table,
  Button,
  Space,
  Modal,
  Form,
  Input,
  Select,
  Switch,
  message,
  Popconfirm,
  Typography,
  Tag
} from 'antd'
import {
  PlusOutlined,
  DeleteOutlined,
  EditOutlined,
  ApiOutlined,
  ClockCircleOutlined
} from '@ant-design/icons'
import { cicdService, WebhookToken, ScheduledTask } from '@/services/cicdService'
import * as apiTestService from '@/services/apiTestService'
import * as webTestService from '@/services/webTestService'
import { perfTestService } from '@/services/perfTestService'
import { useTranslation } from 'react-i18next'
import { useProjectStore } from '@/stores/projectStore'

const { Paragraph } = Typography

const CICD: React.FC = () => {
  const { t } = useTranslation();
  const [activeTab, setActiveTab] = useState('webhooks')
  const { currentProjectId } = useProjectStore()
  
  const [webhooks, setWebhooks] = useState<WebhookToken[]>([])
  const [schedules, setSchedules] = useState<ScheduledTask[]>([])
  const [loading, setLoading] = useState(false)
  
  const [webhookModalVisible, setWebhookModalVisible] = useState(false)
  const [scheduleModalVisible, setScheduleModalVisible] = useState(false)
  
  const [webhookForm] = Form.useForm()
  const [scheduleForm] = Form.useForm()
  const [editingSchedule, setEditingSchedule] = useState<ScheduledTask | null>(null)
  
  // 用于下拉列表的测试目标
  const [targetType, setTargetType] = useState<string>('api_collection')
  const [targetOptions, setTargetOptions] = useState<{label: string, value: number}[]>([])

  useEffect(() => {
    fetchData()
  }, [currentProjectId, activeTab])

  useEffect(() => {
    if (webhookModalVisible || scheduleModalVisible) {
      fetchTargetOptions(targetType)
    }
  }, [targetType, webhookModalVisible, scheduleModalVisible])

  const fetchData = async () => {
    if (!currentProjectId) return
    setLoading(true)
    try {
      if (activeTab === 'webhooks') {
        const response = await cicdService.getWebhooks(currentProjectId)
        setWebhooks(response.data || [])
      } else {
        const response = await cicdService.getSchedules(currentProjectId)
        setSchedules(response.data || [])
      }
    } catch (error: unknown) {
      const err = error as { response?: { data?: { message?: string } }; message?: string }
      message.error(`${t('cicd.loadFailed')}: ${err.message}`)
    } finally {
      setLoading(false)
    }
  }

  const fetchTargetOptions = async (type: string) => {
    if (!currentProjectId) return
    try {
      let options: {label: string, value: number}[] = []
      if (type === 'api_collection') {
        const response = await apiTestService.getCollections(currentProjectId)
        options = (response.data || []).map((item: Record<string, unknown>) => ({ label: item.name, value: item.id }))
      } else if (type === 'web_collection') {
        const response = await webTestService.getCollections(currentProjectId)
        options = (response.data || []).map((item: Record<string, unknown>) => ({ label: item.name, value: item.id }))
      } else if (type === 'perf_scenario') {
        const response = await perfTestService.getScenarios(currentProjectId)
        options = (response.data || []).map((item: Record<string, unknown>) => ({ label: item.name, value: item.id }))
      }
      setTargetOptions(options)
    } catch (error) {
      logger.error('Failed to load targets', error)
    }
  }

  const handleCreateWebhook = async () => {
    if (!currentProjectId) {
      message.warning(t('cicd.selectProjectFirst', '请先选择一个项目'))
      return
    }
    try {
      const values = await webhookForm.validateFields()
      await cicdService.createWebhook({
        ...values,
        project_id: currentProjectId
      })
      message.success(t('cicd.createSuccess'))
      setWebhookModalVisible(false)
      webhookForm.resetFields()
      fetchData()
    } catch (error: unknown) {
      const err = error as { response?: { data?: { message?: string } }; message?: string; errorFields?: unknown }
      if (err.errorFields) return
      message.error(`${t('cicd.createFailed')}: ${err.message}`)
    }
  }

  const handleDeleteWebhook = async (id: number) => {
    try {
      await cicdService.deleteWebhook(id)
      message.success(t('cicd.deleteSuccess'))
      fetchData()
    } catch (error: unknown) {
      const err = error as { response?: { data?: { message?: string } }; message?: string }
      message.error(`${t('cicd.deleteFailed')}: ${err.message}`)
    }
  }

  const handleSaveSchedule = async () => {
    try {
      const values = await scheduleForm.validateFields()
      if (editingSchedule) {
        await cicdService.updateSchedule(editingSchedule.id, values)
        message.success(t('cicd.updateSuccess'))
      } else {
        if (!currentProjectId) {
          message.warning(t('cicd.selectProjectFirst', '请先选择一个项目'))
          return
        }
        await cicdService.createSchedule({
          ...values,
          project_id: currentProjectId,
          is_active: true
        })
        message.success(t('cicd.createSuccess'))
      }
      setScheduleModalVisible(false)
      scheduleForm.resetFields()
      setEditingSchedule(null)
      fetchData()
    } catch (error: unknown) {
      const err = error as { response?: { data?: { message?: string } }; message?: string; errorFields?: unknown }
      if (err.errorFields) return
      message.error(`${t('cicd.saveFailed')}: ${err.message}`)
    }
  }

  const handleToggleSchedule = async (record: ScheduledTask, checked: boolean) => {
    try {
      await cicdService.updateSchedule(record.id, { is_active: checked })
      message.success(checked ? t('cicd.enabledTask') : t('cicd.disabledTask'))
      fetchData()
    } catch (error: unknown) {
      const err = error as { response?: { data?: { message?: string } }; message?: string }
      message.error(`${t('cicd.operationFailed')}: ${err.message}`)
    }
  }

  const handleDeleteSchedule = async (id: number) => {
    try {
      await cicdService.deleteSchedule(id)
      message.success(t('cicd.deleteSuccess'))
      fetchData()
    } catch (error: unknown) {
      const err = error as { response?: { data?: { message?: string } }; message?: string }
      message.error(`${t('cicd.deleteFailed')}: ${err.message}`)
    }
  }

  const getTargetTypeName = (type: string) => {
    const map: Record<string, string> = {
      'api_collection': t('cicd.apiCollection'),
      'web_collection': t('cicd.webCollection'),
      'perf_scenario': t('cicd.perfScenario')
    }
    return map[type] || type
  }

  const webhookColumns = [
    { title: t('cicd.taskName'), dataIndex: 'name', key: 'name' },
    { 
      title: t('cicd.targetType'), 
      dataIndex: 'target_type', 
      key: 'target_type',
      render: (text: string) => <Tag color="blue">{getTargetTypeName(text)}</Tag>
    },
    { title: t('cicd.targetId'), dataIndex: 'target_id', key: 'target_id' },
    { 
      title: t('cicd.triggerUrl'), 
      key: 'url',
      render: (_: unknown, record: WebhookToken) => {
        const url = `${window.location.origin}/api/v1/triggers/${record.token}`
        return (
          <Paragraph copyable={{ text: url }} style={{ margin: 0, maxWidth: 300 }} ellipsis>
            {url}
          </Paragraph>
        )
      }
    },
    { title: t('cicd.createdAt'), dataIndex: 'created_at', key: 'created_at' },
    {
      title: t('common.actions'),
      key: 'action',
      render: (_: unknown, record: WebhookToken) => (
        <Space>
          <Popconfirm title={t('cicd.confirmDelete')} onConfirm={() => handleDeleteWebhook(record.id)}>
            <Button type="text" danger icon={<DeleteOutlined />} />
          </Popconfirm>
        </Space>
      ),
    },
  ]

  const scheduleColumns = [
    { title: t('cicd.taskName'), dataIndex: 'name', key: 'name' },
    { title: t('cicd.cronExpression'), dataIndex: 'cron_expression', key: 'cron_expression', render: (text: string) => <Tag>{text}</Tag> },
    { 
      title: t('cicd.targetType'), 
      dataIndex: 'target_type', 
      key: 'target_type',
      render: (text: string) => <Tag color="blue">{getTargetTypeName(text)}</Tag>
    },
    { title: t('cicd.statusLabel'), key: 'is_active', render: (_: unknown, record: ScheduledTask) => (
      <Switch checked={record.is_active} onChange={(checked) => handleToggleSchedule(record, checked)} />
    )},
    {
      title: t('common.actions'),
      key: 'action',
      render: (_: unknown, record: ScheduledTask) => (
        <Space>
          <Button 
            type="text" 
            icon={<EditOutlined />} 
            onClick={() => {
              setEditingSchedule(record)
              setTargetType(record.target_type)
              scheduleForm.setFieldsValue(record)
              setScheduleModalVisible(true)
            }}
          />
          <Popconfirm title={t('cicd.confirmDelete')} onConfirm={() => handleDeleteSchedule(record.id)}>
            <Button type="text" danger icon={<DeleteOutlined />} />
          </Popconfirm>
        </Space>
      ),
    },
  ]

  if (!currentProjectId) {
    return <div className="fst-page"><div className="fst-empty"><div className="fst-empty-title">{t("cicd.selectProject")}</div></div></div>
  }

  return (
    <div className="fst-page">
      <div className="fst-page-header fst-animate-in">
        <h1 className="fst-page-title">{t("sidebar.cicd")}</h1>
      </div>

      <div className="fst-ios-card fst-animate-in fst-animate-in-1">
        <div className="fst-tabs" style={{ marginBottom: 20 }}>
          <button className={`fst-tab ${activeTab === 'webhooks' ? 'fst-tab--active' : ''}`} onClick={() => setActiveTab('webhooks')}>
            <ApiOutlined style={{ marginRight: 6 }} /> {t('cicd.webhookTab')}
          </button>
          <button className={`fst-tab ${activeTab === 'schedules' ? 'fst-tab--active' : ''}`} onClick={() => setActiveTab('schedules')}>
            <ClockCircleOutlined style={{ marginRight: 6 }} /> {t('cicd.scheduleTab')}
          </button>
        </div>

        {activeTab === 'webhooks' ? (
          <>
            <div className="fst-toolbar">
              <div />
              <div className="fst-toolbar-right">
                <button className="fst-btn fst-btn--primary fst-btn--sm" onClick={() => setWebhookModalVisible(true)}>
                  <PlusOutlined /> {t('cicd.newWebhook')}
                </button>
              </div>
            </div>
            <div className="fst-table-wrap">
              <Table columns={webhookColumns} dataSource={webhooks} rowKey="id" loading={loading} pagination={{ pageSize: 10 }} />
            </div>
          </>
        ) : (
          <>
            <div className="fst-toolbar">
              <div />
              <div className="fst-toolbar-right">
                <button className="fst-btn fst-btn--primary fst-btn--sm" onClick={() => {
                  setEditingSchedule(null)
                  scheduleForm.resetFields()
                  setScheduleModalVisible(true)
                }}>
                  <PlusOutlined /> {t('cicd.newSchedule')}
                </button>
              </div>
            </div>
            <div className="fst-table-wrap">
              <Table columns={scheduleColumns} dataSource={schedules} rowKey="id" loading={loading} pagination={{ pageSize: 10 }} />
            </div>
          </>
        )}
      </div>

      {/* Webhook Modal */}
      <Modal
        title={t("cicd.newWebhookTitle")}
        open={webhookModalVisible}
        onOk={handleCreateWebhook}
        onCancel={() => setWebhookModalVisible(false)}
        destroyOnClose
      >
        <Form form={webhookForm} layout="vertical">
          <Form.Item name="name" label={t("cicd.triggerName")} rules={[{ required: true }]}>
            <Input placeholder={t("cicd.triggerNamePlaceholder")} />
          </Form.Item>
          <Form.Item name="target_type" label={t("cicd.targetType")} rules={[{ required: true }]} initialValue="api_collection">
            <Select onChange={setTargetType}>
              <Select.Option value="api_collection">{t("cicd.apiCollection")}</Select.Option>
              <Select.Option value="web_collection">{t("cicd.webCollection")}</Select.Option>
              <Select.Option value="perf_scenario">{t("cicd.perfScenario")}</Select.Option>
            </Select>
          </Form.Item>
          <Form.Item name="target_id" label={t("cicd.targetId")} rules={[{ required: true }]}>
            <Select placeholder={t("cicd.targetIdPlaceholder")}>
              {targetOptions.map(opt => (
                <Select.Option key={opt.value} value={opt.value}>{opt.label}</Select.Option>
              ))}
            </Select>
          </Form.Item>
        </Form>
      </Modal>

      {/* Schedule Modal */}
      <Modal
        title={editingSchedule ? t("cicd.editSchedule") : t("cicd.newScheduleTitle")}
        open={scheduleModalVisible}
        onOk={handleSaveSchedule}
        onCancel={() => setScheduleModalVisible(false)}
        destroyOnClose
      >
        <Form form={scheduleForm} layout="vertical">
          <Form.Item name="name" label={t("cicd.taskName")} rules={[{ required: true }]}>
            <Input placeholder={t("cicd.taskNamePlaceholder")} />
          </Form.Item>
          <Form.Item name="cron_expression" label={t("cicd.cronExpression")} rules={[{ required: true }]} tooltip={t('cicd.cronTooltip')}>
            <Input placeholder="0 2 * * *" />
          </Form.Item>
          <Form.Item name="target_type" label={t("cicd.targetType")} rules={[{ required: true }]} initialValue="api_collection">
            <Select onChange={setTargetType}>
              <Select.Option value="api_collection">{t("cicd.apiCollection")}</Select.Option>
              <Select.Option value="web_collection">{t("cicd.webCollection")}</Select.Option>
              <Select.Option value="perf_scenario">{t("cicd.perfScenario")}</Select.Option>
            </Select>
          </Form.Item>
          <Form.Item name="target_id" label={t("cicd.targetId")} rules={[{ required: true }]}>
            <Select placeholder={t("cicd.targetIdPlaceholder")}>
              {targetOptions.map(opt => (
                <Select.Option key={opt.value} value={opt.value}>{opt.label}</Select.Option>
              ))}
            </Select>
          </Form.Item>
          <Form.Item name="notify_webhook" label={t("cicd.notifyWebhook")}>
            <Input placeholder="https://oapi.dingtalk.com/robot/send?access_token=..." />
          </Form.Item>
          <Form.Item name="notify_events" label={t("cicd.notifyEvents")} initialValue="all">
            <Select>
              <Select.Option value="all">{t("cicd.allEvents")}</Select.Option>
              <Select.Option value="failed">{t("cicd.failedOnly")}</Select.Option>
            </Select>
          </Form.Item>
        </Form>
      </Modal>
    </div>
  )
}

export default CICD