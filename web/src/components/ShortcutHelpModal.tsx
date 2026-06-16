/**
 * 快捷键帮助弹窗
 *
 * 展示所有可用快捷键列表。
 */
import { Modal, Typography } from 'antd'
import { useTranslation } from 'react-i18next'

const { Text } = Typography

interface ShortcutHelpModalProps {
  open: boolean
  onClose: () => void
}

interface ShortcutItem {
  keys: string
  description: string
}

const ShortcutHelpModal = ({ open, onClose }: ShortcutHelpModalProps) => {
  const { t } = useTranslation()

  const isMac = navigator.platform.toUpperCase().indexOf('MAC') >= 0
  const mod = isMac ? '⌘' : 'Ctrl'

  const globalShortcuts: ShortcutItem[] = [
    { keys: `${mod} + K`, description: t('shortcuts.globalSearch') },
    { keys: `${mod} + /`, description: t('shortcuts.help') },
    { keys: `${mod} + B`, description: t('shortcuts.toggleSidebar') },
  ]

  const apiTestShortcuts: ShortcutItem[] = [
    { keys: `${mod} + Enter`, description: t('shortcuts.sendRequest') },
    { keys: `${mod} + S`, description: t('shortcuts.saveCase') },
    { keys: `${mod} + L`, description: t('shortcuts.clearResponse') },
    { keys: `${mod} + D`, description: t('shortcuts.duplicateCase') },
  ]

  const renderSection = (title: string, shortcuts: ShortcutItem[]) => (
    <div style={{ marginBottom: 16 }}>
      <Text strong style={{ fontSize: 13, display: 'block', marginBottom: 8 }}>{title}</Text>
      {shortcuts.map((s, i) => (
        <div
          key={i}
          style={{
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center',
            padding: '6px 0',
            borderBottom: '1px solid #f5f5f5',
          }}
        >
          <Text style={{ fontSize: 13 }}>{s.description}</Text>
          <kbd
            style={{
              padding: '2px 8px',
              background: '#f6f8f8',
              border: '1px solid #e0e0e0',
              borderRadius: 4,
              fontSize: 12,
              fontFamily: 'monospace',
            }}
          >
            {s.keys}
          </kbd>
        </div>
      ))}
    </div>
  )

  return (
    <Modal
      title={t('shortcuts.title')}
      open={open}
      onCancel={onClose}
      footer={null}
      width={480}
      destroyOnHidden
    >
      {renderSection(t('shortcuts.globalSection'), globalShortcuts)}
      {renderSection(t('shortcuts.apiTestSection'), apiTestShortcuts)}
    </Modal>
  )
}

export default ShortcutHelpModal
