/**
 * 通用批量操作栏组件
 *
 * 在列表页面中展示已选数量和批量操作按钮。
 * 当 selectedRowKeys 不为空时显示。
 */
import { Button, Space, Typography, Popconfirm } from 'antd'
import {
  DeleteOutlined,
  PlayCircleOutlined,
  ExportOutlined,
  TagsOutlined,
} from '@ant-design/icons'
import { useTranslation } from 'react-i18next'

const { Text } = Typography

interface BatchAction {
  key: string
  label: string
  icon?: React.ReactNode
  danger?: boolean
  confirmTitle?: string
  onClick: (selectedKeys: React.Key[]) => void | Promise<void>
}

interface BatchActionBarProps {
  selectedKeys: React.Key[]
  onClearSelection: () => void
  actions?: BatchAction[]
}

const BatchActionBar = ({ selectedKeys, onClearSelection, actions = [] }: BatchActionBarProps) => {
  const { t } = useTranslation()

  if (selectedKeys.length === 0) return null

  return (
    <div
      style={{
        display: 'flex',
        alignItems: 'center',
        gap: 12,
        padding: '8px 16px',
        marginBottom: 12,
        background: 'rgba(45, 106, 100, 0.06)',
        borderRadius: 8,
        border: '1px solid rgba(45, 106, 100, 0.15)',
      }}
    >
      <Text style={{ fontSize: 13 }}>
        {t('common.selected')}: <Text strong>{selectedKeys.length}</Text>
      </Text>
      <div style={{ flex: 1 }} />
      <Space size={8}>
        {actions.map((action) =>
          action.confirmTitle ? (
            <Popconfirm
              key={action.key}
              title={action.confirmTitle}
              onConfirm={() => action.onClick(selectedKeys)}
              okText={t('common.confirm')}
              cancelText={t('common.cancel')}
            >
              <Button
                size="small"
                danger={action.danger}
                icon={action.icon}
              >
                {action.label}
              </Button>
            </Popconfirm>
          ) : (
            <Button
              key={action.key}
              size="small"
              danger={action.danger}
              icon={action.icon}
              onClick={() => action.onClick(selectedKeys)}
            >
              {action.label}
            </Button>
          )
        )}
        <Button size="small" type="link" onClick={onClearSelection}>
          {t('common.cancel')}
        </Button>
      </Space>
    </div>
  )
}

export default BatchActionBar
