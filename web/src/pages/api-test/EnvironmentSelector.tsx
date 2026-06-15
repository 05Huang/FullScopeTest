/**
 * 环境选择器组件
 *
 * 从 RequestEditor 拆分而来，展示环境下拉选择和变量提示。
 */
import { Select, Tag, Button, Typography } from 'antd'
import EnvironmentVariableHint from './EnvironmentVariableHint'

const { Text } = Typography

interface EnvironmentSelectorProps {
  environments: any[]
  selectedEnvId?: number
  onSelectEnv: (id: number) => void
  currentEnv: any
  onApplyEnv: () => void
}

const EnvironmentSelector: React.FC<EnvironmentSelectorProps> = ({
  environments, selectedEnvId, onSelectEnv, currentEnv, onApplyEnv,
}) => (
  <>
    <div style={{ display: 'flex', gap: 8, marginBottom: 12, alignItems: 'center' }}>
      <Text type="secondary" style={{ fontSize: 12, minWidth: 50 }}>环境:</Text>
      <Select
        placeholder="选择测试环境" allowClear
        style={{ flex: 1, maxWidth: 300 }}
        value={selectedEnvId} onChange={onSelectEnv}
        options={environments.map(e => ({ value: e.id, label: e.name }))}
      />
      {currentEnv && (
        <>
          <Tag color="blue">{currentEnv.name}</Tag>
          <Button type="dashed" size="small" onClick={onApplyEnv}>应用配置</Button>
        </>
      )}
    </div>
    {selectedEnvId && (
      <div style={{ marginBottom: 12 }}>
        <EnvironmentVariableHint envId={selectedEnvId} showUsage={true} />
      </div>
    )}
  </>
)

export default EnvironmentSelector
