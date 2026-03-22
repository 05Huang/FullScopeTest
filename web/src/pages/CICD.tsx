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

const { Paragraph } = Typography

const CICD: React.FC = () => {
  const [activeTab, setActiveTab] = useState('webhooks')
  
  // 暂时使用全局固定的 project_id 或从 url 获取
  const currentProjectId = 1
  
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
    setLoading(true)
    try {
      if (activeTab === 'webhooks') {
        const response: any = await cicdService.getWebhooks(currentProjectId || 1)
        setWebhooks(response.data || [])
      } else {
        const response: any = await cicdService.getSchedules(currentProjectId || 1)
        setSchedules(response.data || [])
      }
    } catch (error: any) {
      message.error(`加载失败: ${error.message}`)
    } finally {
      setLoading(false)
    }
  }

  const fetchTargetOptions = async (type: string) => {
    try {
      let options: {label: string, value: number}[] = []
      if (type === 'api_collection') {
        const response: any = await apiTestService.getCollections(currentProjectId || 1)
        options = (response.data || []).map((item: any) => ({ label: item.name, value: item.id }))
      } else if (type === 'web_collection') {
        const response: any = await webTestService.getCollections(currentProjectId || 1)
        options = (response.data || []).map((item: any) => ({ label: item.name, value: item.id }))
      } else if (type === 'perf_scenario') {
        const response: any = await perfTestService.getScenarios(currentProjectId || 1)
        options = (response.data || []).map((item: any) => ({ label: item.name, value: item.id }))
      }
      setTargetOptions(options)
    } catch (error) {
      console.error('Failed to load targets', error)
    }
  }

  const handleCreateWebhook = async () => {
    try {
      const values = await webhookForm.validateFields()
      await cicdService.createWebhook({
        ...values,
        project_id: currentProjectId || 1
      })
      message.success('创建 Webhook 成功')
      setWebhookModalVisible(false)
      webhookForm.resetFields()
      fetchData()
    } catch (error: any) {
      if (error.errorFields) return
      message.error(`创建失败: ${error.message}`)
    }
  }

  const handleDeleteWebhook = async (id: number) => {
    try {
      await cicdService.deleteWebhook(id)
      message.success('删除成功')
      fetchData()
    } catch (error: any) {
      message.error(`删除失败: ${error.message}`)
    }
  }

  const handleSaveSchedule = async () => {
    try {
      const values = await scheduleForm.validateFields()
      if (editingSchedule) {
        await cicdService.updateSchedule(editingSchedule.id, values)
        message.success('更新成功')
      } else {
        await cicdService.createSchedule({
          ...values,
          project_id: currentProjectId || 1,
          is_active: true
        })
        message.success('创建成功')
      }
      setScheduleModalVisible(false)
      scheduleForm.resetFields()
      setEditingSchedule(null)
      fetchData()
    } catch (error: any) {
      if (error.errorFields) return
      message.error(`保存失败: ${error.message}`)
    }
  }

  const handleToggleSchedule = async (record: ScheduledTask, checked: boolean) => {
    try {
      await cicdService.updateSchedule(record.id, { is_active: checked })
      message.success(checked ? '已启用任务' : '已暂停任务')
      fetchData()
    } catch (error: any) {
      message.error(`操作失败: ${error.message}`)
    }
  }

  const handleDeleteSchedule = async (id: number) => {
    try {
      await cicdService.deleteSchedule(id)
      message.success('删除成功')
      fetchData()
    } catch (error: any) {
      message.error(`删除失败: ${error.message}`)
    }
  }

  const getTargetTypeName = (type: string) => {
    const map: Record<string, string> = {
      'api_collection': 'API 集合',
      'web_collection': 'Web 自动化集合',
      'perf_scenario': '性能压测场景'
    }
    return map[type] || type
  }

  const webhookColumns = [
    { title: '名称', dataIndex: 'name', key: 'name' },
    { 
      title: '目标类型', 
      dataIndex: 'target_type', 
      key: 'target_type',
      render: (text: string) => <Tag color="blue">{getTargetTypeName(text)}</Tag>
    },
    { title: '目标ID', dataIndex: 'target_id', key: 'target_id' },
    { 
      title: '触发地址 (Webhook URL)', 
      key: 'url',
      render: (_: any, record: WebhookToken) => {
        const url = `${window.location.origin}/api/v1/triggers/${record.token}`
        return (
          <Paragraph copyable={{ text: url }} style={{ margin: 0, maxWidth: 300 }} ellipsis>
            {url}
          </Paragraph>
        )
      }
    },
    { title: '创建时间', dataIndex: 'created_at', key: 'created_at' },
    {
      title: '操作',
      key: 'action',
      render: (_: any, record: WebhookToken) => (
        <Space>
          <Popconfirm title="确定要删除吗？" onConfirm={() => handleDeleteWebhook(record.id)}>
            <Button type="text" danger icon={<DeleteOutlined />} />
          </Popconfirm>
        </Space>
      ),
    },
  ]

  const scheduleColumns = [
    { title: '名称', dataIndex: 'name', key: 'name' },
    { title: 'Cron 表达式', dataIndex: 'cron_expression', key: 'cron_expression', render: (text: string) => <Tag>{text}</Tag> },
    { 
      title: '目标类型', 
      dataIndex: 'target_type', 
      key: 'target_type',
      render: (text: string) => <Tag color="blue">{getTargetTypeName(text)}</Tag>
    },
    { title: '状态', key: 'is_active', render: (_: any, record: ScheduledTask) => (
      <Switch checked={record.is_active} onChange={(checked) => handleToggleSchedule(record, checked)} />
    )},
    {
      title: '操作',
      key: 'action',
      render: (_: any, record: ScheduledTask) => (
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
          <Popconfirm title="确定要删除吗？" onConfirm={() => handleDeleteSchedule(record.id)}>
            <Button type="text" danger icon={<DeleteOutlined />} />
          </Popconfirm>
        </Space>
      ),
    },
  ]

  if (!currentProjectId) {
    return <div style={{ padding: 24 }}>请先选择一个项目</div>
  }

  return (
    <div style={{ padding: 24 }}>
      <div style={{ marginBottom: 16, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <Typography.Title level={4} style={{ margin: 0 }}>CI/CD 与 定时任务</Typography.Title>
      </div>

      <Card>
        <Tabs
          activeKey={activeTab}
          onChange={setActiveTab}
          items={[
            {
              key: 'webhooks',
              label: <span><ApiOutlined /> Webhook 触发器</span>,
              children: (
                <>
                  <div style={{ marginBottom: 16 }}>
                    <Button type="primary" icon={<PlusOutlined />} onClick={() => setWebhookModalVisible(true)}>
                      新建 Webhook
                    </Button>
                  </div>
                  <Table 
                    columns={webhookColumns} 
                    dataSource={webhooks} 
                    rowKey="id" 
                    loading={loading}
                    pagination={{ pageSize: 10 }}
                  />
                </>
              )
            },
            {
              key: 'schedules',
              label: <span><ClockCircleOutlined /> 定时任务</span>,
              children: (
                <>
                  <div style={{ marginBottom: 16 }}>
                    <Button type="primary" icon={<PlusOutlined />} onClick={() => {
                      setEditingSchedule(null)
                      scheduleForm.resetFields()
                      setScheduleModalVisible(true)
                    }}>
                      新建定时任务
                    </Button>
                  </div>
                  <Table 
                    columns={scheduleColumns} 
                    dataSource={schedules} 
                    rowKey="id" 
                    loading={loading}
                    pagination={{ pageSize: 10 }}
                  />
                </>
              )
            }
          ]}
        />
      </Card>

      {/* Webhook Modal */}
      <Modal
        title="新建 Webhook 触发器"
        open={webhookModalVisible}
        onOk={handleCreateWebhook}
        onCancel={() => setWebhookModalVisible(false)}
        destroyOnClose
      >
        <Form form={webhookForm} layout="vertical">
          <Form.Item name="name" label="触发器名称" rules={[{ required: true }]}>
            <Input placeholder="例如: 每日回归触发器" />
          </Form.Item>
          <Form.Item name="target_type" label="目标类型" rules={[{ required: true }]} initialValue="api_collection">
            <Select onChange={setTargetType}>
              <Select.Option value="api_collection">API 集合</Select.Option>
              <Select.Option value="web_collection">Web 自动化集合</Select.Option>
              <Select.Option value="perf_scenario">性能压测场景</Select.Option>
            </Select>
          </Form.Item>
          <Form.Item name="target_id" label="执行目标" rules={[{ required: true }]}>
            <Select placeholder="请选择要触发的集合/场景">
              {targetOptions.map(opt => (
                <Select.Option key={opt.value} value={opt.value}>{opt.label}</Select.Option>
              ))}
            </Select>
          </Form.Item>
        </Form>
      </Modal>

      {/* Schedule Modal */}
      <Modal
        title={editingSchedule ? "编辑定时任务" : "新建定时任务"}
        open={scheduleModalVisible}
        onOk={handleSaveSchedule}
        onCancel={() => setScheduleModalVisible(false)}
        destroyOnClose
      >
        <Form form={scheduleForm} layout="vertical">
          <Form.Item name="name" label="任务名称" rules={[{ required: true }]}>
            <Input placeholder="例如: 每日凌晨回归测试" />
          </Form.Item>
          <Form.Item name="cron_expression" label="Cron 表达式" rules={[{ required: true }]} tooltip="分 时 日 月 周，例如: 0 2 * * * 表示每天凌晨2点">
            <Input placeholder="0 2 * * *" />
          </Form.Item>
          <Form.Item name="target_type" label="目标类型" rules={[{ required: true }]} initialValue="api_collection">
            <Select onChange={setTargetType}>
              <Select.Option value="api_collection">API 集合</Select.Option>
              <Select.Option value="web_collection">Web 自动化集合</Select.Option>
              <Select.Option value="perf_scenario">性能压测场景</Select.Option>
            </Select>
          </Form.Item>
          <Form.Item name="target_id" label="执行目标" rules={[{ required: true }]}>
            <Select placeholder="请选择要触发的集合/场景">
              {targetOptions.map(opt => (
                <Select.Option key={opt.value} value={opt.value}>{opt.label}</Select.Option>
              ))}
            </Select>
          </Form.Item>
          <Form.Item name="notify_webhook" label="钉钉/飞书通知 Webhook URL">
            <Input placeholder="https://oapi.dingtalk.com/robot/send?access_token=..." />
          </Form.Item>
          <Form.Item name="notify_events" label="通知事件" initialValue="all">
            <Select>
              <Select.Option value="all">所有状态 (成功与失败)</Select.Option>
              <Select.Option value="failed">仅失败时通知</Select.Option>
            </Select>
          </Form.Item>
        </Form>
      </Modal>
    </div>
  )
}

export default CICD