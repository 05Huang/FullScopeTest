import { useTranslation } from 'react-i18next'
import { Modal, Button, Typography } from 'antd'
import { BugOutlined } from '@ant-design/icons'

const { Text } = Typography

interface LogViewerModalProps {
  open: boolean
  scriptName: string
  scriptResult?: {
    success: boolean
    stdout?: string
    stderr?: string
    error?: string
  }
  aiHealing: boolean
  onClose: () => void
  onAiHeal: () => void
}

const LogViewerModal = ({
  open,
  scriptName,
  scriptResult,
  aiHealing,
  onClose,
  onAiHeal,
}: LogViewerModalProps) => {
  return (
    <Modal
      title={
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', paddingRight: 24 }}>
          <span>执行日志 - {scriptName}</span>
          {scriptResult && !scriptResult.success && (
            <Button
              type="primary"
              danger
              icon={<BugOutlined />}
              onClick={onAiHeal}
              loading={aiHealing}
            >
              AI 修复
            </Button>
          )}
        </div>
      }
      open={open}
      onCancel={onClose}
      footer={null}
      width={800}
    >
      {scriptResult ? (
        <div>
          {scriptResult.stdout && (
            <div style={{ marginBottom: 16 }}>
              <Text strong style={{ color: '#52c41a' }}>
                标准输出 (stdout):
              </Text>
              <pre style={{ background: '#f6ffed', padding: 12, borderRadius: 4, maxHeight: 300, overflow: 'auto', marginTop: 8 }}>
                {scriptResult.stdout}
              </pre>
            </div>
          )}
          {scriptResult.stderr && (
            <div style={{ marginBottom: 16 }}>
              <Text strong style={{ color: '#f5222d' }}>标准错误 (stderr):</Text>
              <pre style={{ background: '#fff2f0', padding: 12, borderRadius: 4, maxHeight: 300, overflow: 'auto', marginTop: 8, color: '#f5222d' }}>
                {scriptResult.stderr}
              </pre>
            </div>
          )}
          {scriptResult.error && (
            <div>
              <Text strong style={{ color: '#f5222d' }}>错误信息:</Text>
              <pre style={{ background: '#fff2f0', padding: 12, borderRadius: 4, maxHeight: 300, overflow: 'auto', marginTop: 8, color: '#f5222d' }}>
                {scriptResult.error}
              </pre>
            </div>
          )}
          {!scriptResult.stdout && !scriptResult.stderr && !scriptResult.error && (
            <Text type="secondary">无输出信息</Text>
          )}
        </div>
      ) : (
        <Text type="secondary">脚本未执行</Text>
      )}
    </Modal>
  )
}

export default LogViewerModal
