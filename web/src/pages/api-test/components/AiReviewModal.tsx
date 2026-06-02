import { useTranslation } from 'react-i18next'
import { Modal, Button, Space, Alert, Card, Tag, Typography, Spin } from 'antd'
import { RobotOutlined } from '@ant-design/icons'
import { methodColors } from '@/constants/api-test'

const { Text } = Typography

interface SuggestedCase {
  method: string
  name: string
  url: string
  description: string
}

interface AiReviewModalProps {
  open: boolean
  loading: boolean
  reviewSummary: string
  suggestedCases: SuggestedCase[]
  onStartReview: () => void
  onSaveCases: () => void
  onCancel: () => void
  onReset: () => void
}

const AiReviewModal = ({
  open,
  loading,
  reviewSummary,
  suggestedCases,
  onStartReview,
  onSaveCases,
  onCancel,
  onReset,
}: AiReviewModalProps) => {
  const { t } = useTranslation()

  return (
    <Modal
      title={
        <Space>
          <RobotOutlined style={{ color: '#1890ff' }} />
          <span>AI 智能用例评审与补全</span>
        </Space>
      }
      open={open}
      onCancel={() => {
        if (!loading) {
          onCancel()
          onReset()
        }
      }}
      width={900}
      footer={
        suggestedCases.length > 0 ? (
          <Space>
            <Button onClick={onReset}>重新评审</Button>
            <Button type="primary" onClick={onSaveCases}>
              一键保存所有补充用例
            </Button>
          </Space>
        ) : (
          <Button
            type="primary"
            onClick={onStartReview}
            loading={loading}
          >
            开始智能评审
          </Button>
        )
      }
    >
      {!reviewSummary && !loading ? (
        <div style={{ padding: '20px 0' }}>
          <Alert
            type="info"
            showIcon
            message="基于当前集合自动评审并补充用例"
            description="AI 将自动分析当前集合内的所有用例，指出哪些边界条件、异常场景或安全漏洞没有被覆盖，并提供一键生成补充用例的功能。"
            style={{ marginBottom: 24 }}
          />
        </div>
      ) : (
        <Spin spinning={loading} tip="AI 正在深度评审当前集合...">
          {reviewSummary && (
            <div style={{ padding: '10px 0' }}>
              <Alert
                type="success"
                showIcon
                message="评审总结"
                description={<div style={{ whiteSpace: 'pre-wrap' }}>{reviewSummary}</div>}
                style={{ marginBottom: 24 }}
              />

              {suggestedCases.length > 0 && (
                <div>
                  <div style={{ marginBottom: 12, fontWeight: 500 }}>
                    AI 建议补充的测试用例 ({suggestedCases.length} 个):
                  </div>
                  <div style={{ maxHeight: 400, overflow: 'auto', paddingRight: 8 }}>
                    {suggestedCases.map((c, i) => (
                      <Card key={i} size="small" style={{ marginBottom: 12 }}>
                        <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 8 }}>
                          <Space>
                            <Tag color={methodColors[c.method] || 'default'}>{c.method}</Tag>
                            <Text strong>{c.name}</Text>
                          </Space>
                        </div>
                        <div style={{ marginBottom: 8 }}>
                          <Text type="secondary" style={{ fontSize: 13 }}>URL: </Text>
                          <Text code>{c.url}</Text>
                        </div>
                        <div style={{ fontSize: 13, color: 'rgba(0,0,0,0.65)' }}>
                          {c.description}
                        </div>
                      </Card>
                    ))}
                  </div>
                </div>
              )}
            </div>
          )}
        </Spin>
      )}
    </Modal>
  )
}

export default AiReviewModal
