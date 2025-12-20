import React, { useState, useEffect } from 'react'
import { Tag, Tooltip, Space, Typography, Divider } from 'antd'
import { InfoCircleOutlined, CopyOutlined } from '@ant-design/icons'
import { environmentService } from '@/services'

const { Text } = Typography

interface Environment {
  id: number
  name: string
  variables?: Record<string, any>
}

interface Props {
  envId?: number
  showUsage?: boolean
}

const EnvironmentVariableHint: React.FC<Props> = ({ envId, showUsage = true }) => {
  const [env, setEnv] = useState<Environment | null>(null)

  useEffect(() => {
    if (envId) {
      loadEnvironment()
    } else {
      setEnv(null)
    }
  }, [envId])

  const loadEnvironment = async () => {
    if (!envId) return
    
    try {
      const res = await environmentService.getEnvironment(envId)
      if (res.code === 200) {
        setEnv(res.data)
      }
    } catch (error) {
      console.error('加载环境失败', error)
    }
  }

  const copyVariable = (varName: string) => {
    navigator.clipboard.writeText(`{${varName}}`)
  }

  if (!envId || !env) {
    return (
      <div style={{ padding: '12px', background: '#f5f5f5', borderRadius: '4px' }}>
        <Text type="secondary">
          <InfoCircleOutlined /> 选择环境后可查看可用变量
        </Text>
      </div>
    )
  }

  // 确保variables是对象类型，避免字符串被当作对象处理
  const variables = (typeof env.variables === 'object' && env.variables !== null && !Array.isArray(env.variables)) 
    ? env.variables 
    : {}
  const variableKeys = Object.keys(variables).filter(key => key !== '')

  if (variableKeys.length === 0) {
    return (
      <div style={{ padding: '12px', background: '#fff7e6', borderRadius: '4px', border: '1px solid #ffd591' }}>
        <Text type="warning">
          <InfoCircleOutlined /> 当前环境 ({env.name}) 未配置变量。在环境配置页面添加变量后可在此处引用。
        </Text>
      </div>
    )
  }

  return (
    <div style={{ padding: '12px', background: '#f0f7ff', borderRadius: '4px', border: '1px solid #d6e4ff' }}>
      <div style={{ marginBottom: '8px' }}>
        <Text strong>
          <InfoCircleOutlined style={{ color: '#1890ff', marginRight: '4px' }} />
          可用环境变量 ({env.name})
        </Text>
      </div>
      
      {showUsage && (
        <div style={{ marginBottom: '8px' }}>
          <Text type="secondary" style={{ fontSize: '12px' }}>
            在 URL、请求头、参数、请求体中使用 <Tag color="blue">{`{变量名}`}</Tag> 格式引用变量
          </Text>
        </div>
      )}
      
      <Divider style={{ margin: '8px 0' }} />
      
      <Space wrap size="small">
        {variableKeys.map(key => (
          <Tooltip
            key={key}
            title={
              <div>
                <div>变量名: {key}</div>
                <div>值: {String(variables[key])}</div>
                <div style={{ marginTop: '4px', fontSize: '11px' }}>
                  点击复制 {`{${key}}`}
                </div>
              </div>
            }
          >
            <Tag
              color="processing"
              style={{ cursor: 'pointer', userSelect: 'none' }}
              onClick={() => copyVariable(key)}
            >
              {key}
              <CopyOutlined style={{ marginLeft: '4px' }} />
            </Tag>
          </Tooltip>
        ))}
      </Space>
      
      <Divider style={{ margin: '8px 0' }} />
      
      <div style={{ fontSize: '11px', color: '#666' }}>
        示例: 若有变量 <Tag color="default" style={{ fontSize: '10px' }}>token</Tag>，
        在请求头中使用 <Text code>{`{"Authorization": "Bearer {token}"}`}</Text>
      </div>
    </div>
  )
}

export default EnvironmentVariableHint
