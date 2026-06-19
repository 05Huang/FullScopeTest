/**
 * 数据驱动执行弹窗组件
 *
 * 支持上传 CSV 文件作为测试数据源，批量执行用例。
 */
import { useState, useCallback } from "react"
import { Modal, Upload, Table, Button, Space, Typography, Alert, message } from "antd"
import { UploadOutlined, PlayCircleOutlined } from "@ant-design/icons"
import { useTranslation } from "react-i18next"

const { Text } = Typography

interface DataDrivenModalProps {
  open: boolean;
  onClose: () => void;
  onExecute: (data: Record<string, string>[]) => void;
  executing?: boolean;
}

const DataDrivenModal: React.FC<DataDrivenModalProps> = ({ open, onClose, onExecute, executing }) => {
  const { t } = useTranslation()
  const [csvData, setCsvData] = useState<Record<string, string>[]>([])
  const [columns, setColumns] = useState<string[]>([])
  const [fileName, setFileName] = useState("")

  const parseCSV = useCallback((text: string) => {
    const lines = text.split("
").filter(l => l.trim())
    if (lines.length < 2) { message.error("CSV 文件至少需要包含表头和一行数据"); return }
    const headers = lines[0].split(",").map(h => h.trim().replace(/^"|"$/g, ""))
    const rows: Record<string, string>[] = []
    for (let i = 1; i < lines.length; i++) {
      const values = lines[i].split(",").map(v => v.trim().replace(/^"|"$/g, ""))
      const row: Record<string, string> = {}
      headers.forEach((h, idx) => { row[h] = values[idx] || "" })
      rows.push(row)
    }
    setColumns(headers)
    setCsvData(rows)
    message.success("已解析 " + rows.length + " 行数据")
  }, [])

  const handleUpload = useCallback((file: File) => {
    setFileName(file.name)
    const reader = new FileReader()
    reader.onload = (e) => { parseCSV(e.target?.result as string) }
    reader.readAsText(file)
    return false
  }, [parseCSV])

  return (
    <Modal title="数据驱动执行" open={open} onCancel={onClose} width={700}
      footer={[
        <Button key="cancel" onClick={onClose}>取消</Button>,
        <Button key="execute" type="primary" icon={<PlayCircleOutlined />}
          loading={executing} disabled={csvData.length === 0}
          onClick={() => onExecute(csvData)}>执行 ({csvData.length} 行)</Button>,
      ]}>)
      <Alert type="info" showIcon style={{ marginBottom: 12 }}
        description="上传 CSV 文件，每行数据将替换用例中的 {{column_name}} 变量并执行。" />
      <Upload beforeUpload={handleUpload} showUploadList={false} accept=".csv,.txt">
        <Button icon={<UploadOutlined />}>选择 CSV 文件</Button>
      </Upload>
      {fileName && <Text type="secondary" style={{ display: "block", marginTop: 8 }}>文件: {fileName} ({csvData.length} 行)</Text>}
      {csvData.length > 0 && (
        <div style={{ marginTop: 12 }}>
          <Text strong style={{ fontSize: 12, marginBottom: 4, display: "block" }}>数据预览 (前 5 行):</Text>
          <Table size="small" rowKey={(_, i) => String(i)}
            columns={columns.map(c => ({ title: c, dataIndex: c, key: c, ellipsis: true }))}
            dataSource={csvData.slice(0, 5)} pagination={false} />
        </div>
      )}
    </Modal>
  )
}

export default DataDrivenModal
