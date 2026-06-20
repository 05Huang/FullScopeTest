/**
 * 定时报告管理页面
 */
import { useState, useEffect } from "react"
import { Card, Table, Button, Space, Tag, Typography, Modal, Form, Input, Select, message, Popconfirm } from "antd"
import { PlusOutlined, ClockCircleOutlined, DeleteOutlined } from "@ant-design/icons"
import { useTranslation } from "react-i18next"
import api from "@/services/api"
import { useTableOperations } from "@/hooks/useTableOperations"

const { Text } = Typography

interface ReportSchedule {
  id: number; name: string; frequency: string; recipients: string[];
  is_active: boolean; next_run_at: string | null; last_run_at: string | null;
  project_id: number | null;
}

const ReportSchedules: React.FC = () => {
  const { t } = useTranslation()
  const [modalOpen, setModalOpen] = useState(false)
  const [form] = Form.useForm()

  const {
    loading, data: schedules, fetchData: fetchSchedules, deleteItem,
  } = useTableOperations<ReportSchedule>({
    fetchFn: async () => {
      const res = await api.get("/report-schedules")
      return { code: res.data?.code, data: res.data?.data }
    },
    deleteFn: async (id) => {
      const res = await api.delete("/report-schedules/" + id)
      return { code: res.data?.code }
    },
  })

  useEffect(() => { fetchSchedules() }, [])

  const handleCreate = async () => {
    try {
      const values = await form.validateFields()
      values.recipients = (values.recipients_str || "").split(",").map((s: string) => s.trim()).filter(Boolean)
      const res = await api.post("/report-schedules", values)
      if (res.data?.code === 200 || res.data?.code === 201) {
        message.success(t("reportSchedules.createSuccess"))
        setModalOpen(false); form.resetFields(); fetchSchedules()
      }
    } catch { message.error(t("reportSchedules.createFailed")) }
  }

  const freqLabels: Record<string, { label: string; color: string }> = {
    daily: { label: t("reportSchedules.frequencies.daily"), color: "blue" },
    weekly: { label: t("reportSchedules.frequencies.weekly"), color: "green" },
    monthly: { label: t("reportSchedules.frequencies.monthly"), color: "purple" },
  }

  return (
    <div className="fst-page">
      <div className="fst-page-header fst-animate-in">
        <h1 className="fst-page-title">{t("reportSchedules.title")}</h1>
        <div className="fst-ios-card-subtitle">{t("reportSchedules.subtitle")}</div>
      </div>
      <Card className="fst-ios-card fst-animate-in fst-animate-in-1"
        title={<Space><ClockCircleOutlined /><Text strong>{t("reportSchedules.title")}</Text></Space>}
        extra={<Button icon={<PlusOutlined />} onClick={() => setModalOpen(true)}>{t("reportSchedules.create")}</Button>}>
        <Table size="small" rowKey="id" loading={loading} dataSource={schedules} columns={[
          { title: t("reportSchedules.name"), dataIndex: "name" },
          { title: t("reportSchedules.frequency"), dataIndex: "frequency", width: 100, render: (v: string) => <Tag color={freqLabels[v]?.color}>{freqLabels[v]?.label || v}</Tag> },
          { title: t("reportSchedules.recipients"), dataIndex: "recipients", render: (v: string[]) => v?.join(", ") || "-" },
          { title: t("reportSchedules.status"), dataIndex: "is_active", width: 80, render: (v: boolean) => <Tag color={v ? "success" : "default"}>{v ? t("reportSchedules.enabled") : t("reportSchedules.disabled")}</Tag> },
          { title: t("reportSchedules.nextRun"), dataIndex: "next_run_at", width: 160, render: (v: string) => v ? new Date(v).toLocaleString() : "-" },
          { title: "", width: 60, render: (_: unknown, r: ReportSchedule) => <Popconfirm title={t("reportSchedules.deleteConfirm")} onConfirm={() => deleteItem(r.id)}><Button type="text" size="small" danger icon={<DeleteOutlined />} /></Popconfirm> },
        ]} pagination={false} />
      </Card>
      <Modal title={t("reportSchedules.create")} open={modalOpen} onCancel={() => setModalOpen(false)} onOk={handleCreate}
        okText={t("common.confirm")} cancelText={t("common.cancel")}>
        <Form form={form} layout="vertical">
          <Form.Item name="name" label={t("reportSchedules.name")} rules={[{ required: true }]}><Input placeholder={t("reportSchedules.namePlaceholder")} /></Form.Item>
          <Form.Item name="frequency" label={t("reportSchedules.frequency")} rules={[{ required: true }]}>
            <Select options={[
              { value: "daily", label: t("reportSchedules.frequencies.daily") },
              { value: "weekly", label: t("reportSchedules.frequencies.weekly") },
              { value: "monthly", label: t("reportSchedules.frequencies.monthly") },
            ]} />
          </Form.Item>
          <Form.Item name="recipients_str" label={t("reportSchedules.recipients")}><Input placeholder={t("reportSchedules.emailPlaceholder")} /></Form.Item>
        </Form>
      </Modal>
    </div>
  )
}

export default ReportSchedules
