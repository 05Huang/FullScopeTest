import { useTranslation } from 'react-i18next'
import { Modal, Form, Input, Select, Card, Space, Tag, Typography } from 'antd'
import { methodColors } from '@/constants/api-test'

const { Text } = Typography

interface SaveCaseModalProps {
  open: boolean
  caseName: string
  method: string
  url: string
  selectedCollectionId?: number
  collections: Array<{ id: number; name: string }>
  onCaseNameChange: (name: string) => void
  onCollectionChange: (id: number | undefined) => void
  onSave: () => void
  onCancel: () => void
}

const SaveCaseModal = ({
  open,
  caseName,
  method,
  url,
  selectedCollectionId,
  collections,
  onCaseNameChange,
  onCollectionChange,
  onSave,
  onCancel,
}: SaveCaseModalProps) => {
  const { t } = useTranslation()

  return (
    <Modal
      title="保存到用例"
      open={open}
      onCancel={onCancel}
      onOk={onSave}
    >
      <Form layout="vertical">
        <Form.Item label="用例名称" required>
          <Input
            placeholder="请输入用例名称"
            value={caseName}
            onChange={(e) => onCaseNameChange(e.target.value)}
          />
        </Form.Item>
        <Form.Item label="所属集合">
          <Select
            placeholder="选择集合（可选）"
            allowClear
            value={selectedCollectionId}
            onChange={onCollectionChange}
            options={collections.map(c => ({
              value: c.id,
              label: c.name
            }))}
          />
        </Form.Item>
        <Form.Item label="请求信息">
          <Card size="small">
            <Space direction="vertical" style={{ width: '100%' }}>
              <div>
                <Text type="secondary">方法:</Text> <Tag color={methodColors[method]}>{method}</Tag>
              </div>
              <div>
                <Text type="secondary">URL:</Text> <Text code>{url || '未设置'}</Text>
              </div>
            </Space>
          </Card>
        </Form.Item>
      </Form>
    </Modal>
  )
}

export default SaveCaseModal
