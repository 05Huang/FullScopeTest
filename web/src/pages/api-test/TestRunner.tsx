/**
 * 测试执行控制栏组件
 *
 * 显示执行状态、耗时统计、集合执行进度条，提供重新发送等快捷操作。
 */
import { Space, Tag, Typography, Button, Tooltip, Progress } from 'antd'
import { ReloadOutlined, ThunderboltOutlined } from '@ant-design/icons'
import { useTranslation } from 'react-i18next'

const { Text } = Typography

export interface CollectionProgress {
  current: number
  total: number
  passed: number
  failed: number
  status: string
}

interface TestRunnerProps {
  sending: boolean
  onResend: () => void
  response?: { status: number; time: number } | null
  /** P30-5: 集合执行进度 */
  progress?: CollectionProgress | null
}

const TestRunner: React.FC<TestRunnerProps> = ({ sending, onResend, response, progress }) => {
  const { t } = useTranslation()
  const percent = progress && progress.total > 0 ? Math.round((progress.current / progress.total) * 100) : 0

  return (
    <div style={{ marginBottom: 8 }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
        <Space>
          {sending && !progress && <Tag color="processing">{t('common.running') || '执行中...'}</Tag>}
          {response && !sending && !progress && (
            <>
              <Tag color={response.status < 400 ? 'success' : 'error'}>
                {response.status}
              </Tag>
              <Text type="secondary" style={{ fontSize: 12 }}>{response.time}ms</Text>
            </>
          )}
        </Space>
        <Tooltip title={t('apiTest.resend') || '重新发送'}>
          <Button size="small" icon={<ReloadOutlined />} onClick={onResend} disabled={sending} />
        </Tooltip>
      </div>

      {/* P30-5: 集合执行进度条 */}
      {progress && (
        <div style={{ marginTop: 8, padding: '8px 12px', background: 'var(--fst-surface-dim, #f6f8f8)', borderRadius: 8 }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 6 }}>
            <Text style={{ fontSize: 13, fontWeight: 500 }}>
              {progress.current}/{progress.total} {t('apiTest.progressDone') || '已完成'}
            </Text>
            <Space size={12}>
              <Text style={{ fontSize: 12, color: '#52c41a' }}>
                ✓ {progress.passed} {t('common.passed') || '通过'}
              </Text>
              {progress.failed > 0 && (
                <Text style={{ fontSize: 12, color: '#ff4d4f' }}>
                  ✗ {progress.failed} {t('common.failed') || '失败'}
                </Text>
              )}
            </Space>
          </div>
          <Progress
            percent={percent}
            size="small"
            status={progress.status === 'failed' ? 'exception' : percent === 100 ? 'success' : 'active'}
            strokeColor={progress.failed > 0 ? '#faad14' : '#2D6A64'}
            showInfo={false}
          />
        </div>
      )}
    </div>
  )
}

export default TestRunner
