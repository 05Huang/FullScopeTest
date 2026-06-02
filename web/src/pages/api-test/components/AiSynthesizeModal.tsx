import { useTranslation } from 'react-i18next'
import { Modal, Button, Space, Alert, Form, Select, Tag, Card, Typography } from 'antd'
import { ExperimentOutlined } from '@ant-design/icons'
import { methodColors } from '@/constants/api-test'

const { Text } = Typography

interface SynthesizedCase {
  method: string
  name: string
  url: string
  params?: Record<string, any>
  body?: Record<string, any>
}

interface AiSynthesizeModalProps {
  open: boolean
  loading: boolean
  synthesizedCases: SynthesizedCase[]
  synthesizeCount: number
  targetCollectionId?: number
  collections: Array<{ id: number; name: string }>
  onSynthesize: () => void
  onSaveAll: () => void
  onCancel: () => void
  onCountChange: (count: number) => void
  onTargetCollectionChange: (id: number | undefined) => void
  onReset: () => void
}

const AiSynthesizeModal = ({
  open,
  loading,
  synthesizedCases,
  synthesizeCount,
  targetCollectionId,
  collections,
  onSynthesize,
  onSaveAll,
  onCancel,
  onCountChange,
  onTargetCollectionChange,
  onReset,
}: AiSynthesizeModalProps) => {
  const { t } = useTranslation()

  return (
    <Modal
      title={
        <Space>
          <ExperimentOutlined style={{ color: '#3D6E66' }} />
          <span>AI 智能测试数据生成与用例裂变</span>
        </Space>
      }
      open={open}
      onCancel={() => {
        if (!loading) {
          onCancel()
          onReset()
        }
      }}
      width={800}
      footer={
        synthesizedCases.length > 0 ? (
          <Space>
            <Button onClick={onReset}>重新生成</Button>
            <Button type="primary" onClick={onSaveAll}>
              保存全部用例
            </Button>
          </Space>
        ) : (
          <Button
            type="primary"
            onClick={onSynthesize}
            loading={loading}
          >
            生成测试用例
          </Button>
        )
      }
    >
      {!synthesizedCases.length ? (
        <div style={{ padding: '20px 0' }}>
          <Alert
            type="info"
            showIcon
            message="基于当前 API 定义自动生成异常和边界测试用例"
            description="AI 将自动分析当前的请求 URL、Headers、Params 和 Body，并生成包含边界值、非法注入、空值等异常测试用例，极大提升测试覆盖率。"
            style={{ marginBottom: 24 }}
          />
          <Form layout="vertical">
            <Form.Item label="生成数量">
              <Select
                value={synthesizeCount}
                onChange={onCountChange}
                style={{ width: 120 }}
                options={[
                  { value: 3, label: '3 个' },
                  { value: 5, label: '5 个' },
                  { value: 10, label: '10 个' },
                ]}
              />
            </Form.Item>
            <Form.Item label="保存目标分组">
              <Select
                value={targetCollectionId}
                onChange={onTargetCollectionChange}
                placeholder="选择用例集合（默认未分组）"
                allowClear
                options={collections.map(c => ({
                  value: c.id,
                  label: c.name
                }))}
              />
            </Form.Item>
          </Form>
        </div>
      ) : (
        <div style={{ maxHeight: 500, overflow: 'auto' }}>
          <Alert
            type="success"
            message={`成功生成 ${synthesizedCases.length} 个测试用例，您可以预览并一键保存到左侧用例树中。`}
            style={{ marginBottom: 16 }}
          />
          {synthesizedCases.map((c, idx) => (
            <Card
              key={idx}
              size="small"
              title={<Space><Tag color={methodColors[c.method] || 'blue'}>{c.method}</Tag><Text strong>{c.name}</Text></Space>}
              style={{ marginBottom: 16 }}
            >
              <div style={{ marginBottom: 8 }}>
                <Text type="secondary" style={{ width: 60, display: 'inline-block' }}>URL:</Text>
                <Text code>{c.url}</Text>
              </div>
              {c.params && Object.keys(c.params).length > 0 && (
                <div style={{ marginBottom: 8 }}>
                  <Text type="secondary" style={{ width: 60, display: 'inline-block' }}>Params:</Text>
                  <Text code>{JSON.stringify(c.params)}</Text>
                </div>
              )}
              {c.body && Object.keys(c.body).length > 0 && (
                <div style={{ marginBottom: 8 }}>
                  <Text type="secondary" style={{ width: 60, display: 'inline-block', verticalAlign: 'top' }}>Body:</Text>
                  <pre style={{
                    display: 'inline-block',
                    margin: 0,
                    padding: '4px 8px',
                    background: '#f5f5f5',
                    borderRadius: 4,
                    width: 'calc(100% - 70px)'
                  }}>
                    {JSON.stringify(c.body, null, 2)}
                  </pre>
                </div>
              )}
            </Card>
          ))}
        </div>
      )}
    </Modal>
  )
}

export default AiSynthesizeModal
