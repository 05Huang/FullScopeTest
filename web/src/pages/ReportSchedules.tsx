/**
 * 定时报告管理页面
 */
import { useState, useEffect, useCallback } from "react"
import { Card, Table, Button, Space, Tag, Typography, Modal, Form, Input, Select, message, Popconfirm, Switch } from "antd"
import { PlusOutlined, ClockCircleOutlined, DeleteOutlined, MailOutlined } from "@ant-design/icons"
import { useTranslation } from "react-i18next"
import api from "@/services/api"

const { Text } = Typography

interface ReportSchedule {
  id: number; name: string; frequency: string; recipients: string[];
  is_active: boolean; next_run_at: string | null; last_run_at: string | null;
  project_id: number | null;
}

const ReportSchedules: React.FC = () => {
  const { t } = useTranslation()
  const [loading, setLoading] = useState(false)
  const [schedules, setSchedules] = useState<ReportSchedule[]>([])
  const [modalOpen, setModalOpen] = useState(false)
  const [form] = Form.useForm()

  const fetchSchedules = useCallback(async () => {
    setLoading(true)
    try {
      const res = await api.get("/report-schedules")
      if (res.data?.code === 200) setSchedules(res.data.data || [])
    } catch {} finally { setLoading(false) }
  }, [])

  useEffect(() => { fetchSchedules() }, [fetchSchedules])

  const handleCreate = async () => {
    try {
      const values = await form.validateFields()
      values.recipients = (values.recipients_str || "").split(",").map((s: string) => s.trim()).filter(Boolean)
      const res = await api.post("/report-schedules", values)
      if (res.data?.code === 200 || res.data?.code === 201) {
        message.success("定时报告已创建")
        setModalOpen(false); form.resetFields(); fetchSchedules()
      }
    } catch { message.error("创建失败") }
  }

  const freqLabels: Record<string, { label: string; color: string }> = {
    daily: { label: "每日", color: "blue" },
    weekly: { label: "每周", color: "green" },
    monthly: { label: "每月", color: "purple" },
  }

  return (
    <div style={{ padding: 16 }}>
      <Card title={<Space><ClockCircleOutlined /><Text strong>定时报告</Text></Space>}
        extra={<Button icon={<PlusOutlined />} onClick={() => setModalOpen(true)}>创建定时报告</Button>}>
        <Table size="small" rowKey="id" loading={loading} dataSource={schedules} columns={[
          { title: "名称", dataIndex: "name" },
          { title: "频率", dataIndex: "frequency", width: 100, render: (v: string) => <Tag color={freqLabels[v]?.color}>{freqLabels[v]?.label || v}</Tag> },
          { title: "收件人", dataIndex: "recipients", render: (v: string[]) => v?.join(", ") || "-" },
          { title: "状态", dataIndex: "is_active", width: 80, render: (v: boolean) => <Tag color={v ? "success" : "default"}>{v ? "启用" : "停用"}</Tag> },
          { title: "下次执行", dataIndex: "next_run_at", width: 160, render: (v: string) => v ? new Date(v).toLocaleString("zh-CN") : "-" },
          { title: "", width: 60, render: (_: any, r: ReportSchedule) => <Popconfirm title="删除？" onConfirm={async () => { await api.delete("/report-schedules/" + r.id); fetchSchedules() }}><Button type="text" size="small" danger icon={<DeleteOutlined />} /></Popconfirm> },
        ]} pagination={false} />
      </Card>
      <Modal title="创建定时报告" open={modalOpen} onCancel={() => setModalOpen(false)} onOk={handleCreate}>
        <Form form={form} layout="vertical">
          <Form.Item name="name" label="报告名称" rules={[{ required: true }]}><Input placeholder="每日测试报告" /></Form.Item>
          <Form.Item name="frequency" label="执行频率" rules={[{ required: true }]}>
            <Select options={[{ value: "daily", label: "每日" }, { value: "weekly", label: "每周" }, { value: "monthly", label: "每月" }]} />
          </Form.Item>
          <Form.Item name="recipients_str" label="收件人邮箱"><Input placeholder="多个邮箱用逗号分隔" /></Form.Item>
        </Form>
      </Modal>
    </div>
  )
}

export default ReportSchedules
