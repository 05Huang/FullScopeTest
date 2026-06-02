import { useTranslation } from 'react-i18next'
import { Modal, Button, Typography, Tag, Card, Image } from 'antd'
import { BugOutlined, RobotOutlined, CheckCircleOutlined, EyeOutlined } from '@ant-design/icons'

const { Text, Title } = Typography

interface VisionResult {
  name: string
  status: 'new' | 'passed' | 'failed'
  mismatch_ratio: number
  mismatch_pixels: number
  baseline_id?: number
  baseline_image_path?: string
  current_image_path?: string
}

interface ScriptResult {
  success: boolean
  stdout?: string
  stderr?: string
  error?: string
  duration?: number
  return_code?: number
  vision_results?: VisionResult[]
}

interface AiAnalysisResult {
  analysis: string
  fixed_script: string | null
}

interface LogViewerModalProps {
  open: boolean
  scriptName: string
  scriptId?: number
  scriptResult?: ScriptResult
  aiHealing: boolean
  aiAnalysisResult?: AiAnalysisResult | null
  token: string
  onClose: () => void
  onAiHeal: () => void
  onApplyFix: () => void
  onViewVisualDiff: (diff: any) => void
}

const LogViewerModal = ({
  open, scriptName, scriptId, scriptResult, aiHealing, aiAnalysisResult, token,
  onClose, onAiHeal, onApplyFix, onViewVisualDiff,
}: LogViewerModalProps) => {
  const { t } = useTranslation()
  return (
    <Modal
      title={
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', paddingRight: 24 }}>
          <span>执行日志 - {scriptName}</span>
          {scriptResult && !scriptResult.success && (
            <Button type="primary" danger icon={<BugOutlined />} onClick={onAiHeal} loading={aiHealing}>AI 智能诊断</Button>
          )}
        </div>
      }
      open={open} onCancel={onClose} footer={null} width={800}
    >
      {aiAnalysisResult && (
        <div style={{ marginBottom: 24, padding: 16, backgroundColor: '#f9f0ff', border: '1px solid #d9d9d9', borderRadius: 8 }}>
          <Title level={5} style={{ color: '#722ed1', marginTop: 0 }}><RobotOutlined style={{ marginRight: 8 }} /> AI 诊断结果</Title>
          <div style={{ whiteSpace: 'pre-wrap', marginBottom: 16 }}>{aiAnalysisResult.analysis}</div>
          {aiAnalysisResult.fixed_script && <Button type="primary" icon={<CheckCircleOutlined />} onClick={onApplyFix}>一键修复脚本</Button>}
        </div>
      )}
      {scriptResult ? (
        <div style={{ fontFamily: 'monospace' }}>
          <div style={{ marginBottom: 16 }}>
            <Tag color={scriptResult.success ? 'success' : 'error'}>{scriptResult.success ? '执行成功' : '执行失败'}</Tag>
            {scriptResult.duration && <Text type="secondary">耗时: {scriptResult.duration.toFixed(2)}ms</Text>}
            {scriptResult.return_code !== undefined && <Text type="secondary" style={{ marginLeft: 16 }}>返回码: {scriptResult.return_code}</Text>}
          </div>
          {scriptResult.stdout && (
            <div style={{ marginBottom: 16 }}>
              <Text strong>标准输出 (stdout):</Text>
              <pre style={{ background: '#f5f5f5', padding: 12, borderRadius: 4, maxHeight: 300, overflow: 'auto', marginTop: 8 }}>{scriptResult.stdout}</pre>
            </div>
          )}
          {scriptResult.vision_results && scriptResult.vision_results.length > 0 && (
            <div style={{ marginBottom: 16 }}>
              <Text strong>视觉回归测试结果:</Text>
              {scriptResult.vision_results.map((vr, idx) => (
                <Card key={idx} size="small" style={{ marginTop: 8 }}>
                  <div style={{ marginBottom: 8 }}>
                    <Text strong style={{ marginRight: 8 }}>{vr.name}</Text>
                    <Tag color={vr.status === 'passed' ? 'success' : vr.status === 'failed' ? 'error' : 'processing'}>
                      {vr.status === 'passed' ? '匹配通过' : vr.status === 'failed' ? '匹配失败' : '新基线'}
                    </Tag>
                    {vr.status !== 'new' && <Text type="secondary">差异率: {(vr.mismatch_ratio * 100).toFixed(2)}%</Text>}
                    {vr.status === 'failed' && scriptId && (
                      <Button size="small" icon={<EyeOutlined />} style={{ marginLeft: 8 }}
                        onClick={() => onViewVisualDiff({ testCaseId: scriptId, baselineId: vr.baseline_id, baselineImagePath: vr.baseline_image_path, currentImagePath: vr.current_image_path, diffPercentage: vr.mismatch_ratio * 100, status: vr.status })}
                      >查看对比</Button>
                    )}
                  </div>
                  {vr.status === 'failed' && scriptId && (
                    <div style={{ display: 'flex', gap: 16, marginTop: 8 }}>
                      <div style={{ flex: 1 }}><Text type="secondary" style={{ display: 'block', marginBottom: 4 }}>预期</Text><Image src={`/api/v1/web-test/scripts/${scriptId}/snapshots/baseline/${vr.name}?token=${token}`} width="100%" /></div>
                      <div style={{ flex: 1 }}><Text type="secondary" style={{ display: 'block', marginBottom: 4 }}>实际</Text><Image src={`/api/v1/web-test/scripts/${scriptId}/snapshots/actual/${vr.name}?token=${token}`} width="100%" /></div>
                      <div style={{ flex: 1 }}><Text type="secondary" style={{ display: 'block', marginBottom: 4 }}>差异</Text><Image src={`/api/v1/web-test/scripts/${scriptId}/snapshots/diff/${vr.name}?token=${token}`} width="100%" /></div>
                    </div>
                  )}
                </Card>
              ))}
            </div>
          )}
          {scriptResult.stderr && (
            <div><Text strong style={{ color: '#f5222d' }}>标准错误 (stderr):</Text>
              <pre style={{ background: '#fff2f0', padding: 12, borderRadius: 4, maxHeight: 300, overflow: 'auto', marginTop: 8, color: '#f5222d' }}>{scriptResult.stderr}</pre>
            </div>
          )}
          {scriptResult.error && (
            <div><Text strong style={{ color: '#f5222d' }}>错误信息:</Text>
              <pre style={{ background: '#fff2f0', padding: 12, borderRadius: 4, maxHeight: 300, overflow: 'auto', marginTop: 8, color: '#f5222d' }}>{scriptResult.error}</pre>
            </div>
          )}
          {!scriptResult.stdout && !scriptResult.stderr && !scriptResult.error && <Text type="secondary">无输出信息</Text>}
        </div>
      ) : (
        <Text type="secondary">{t('webTest.scriptNotExecuted')}</Text>
      )}
    </Modal>
  )
}

export default LogViewerModal
