/**
 * 脚本列表组件
 *
 * 从 WebTestScripts 拆分而来，包含筛选工具栏和脚本表格。
 */
import { useTranslation } from 'react-i18next'
import { Card, Table, Button, Space, Input, Select, Dropdown } from 'antd'
import {
  PlusOutlined, SearchOutlined, ReloadOutlined, MoreOutlined,
  FolderOpenOutlined, FolderAddOutlined, RobotOutlined, GlobalOutlined,
} from '@ant-design/icons'

interface ScriptListProps {
  scripts: any[]
  columns: any[]
  loading: boolean
  searchText: string
  setSearchText: (v: string) => void
  selectedCollectionId?: number
  setSelectedCollectionId: (v: number | undefined) => void
  collections: any[]
  selectedRowKeys: React.Key[]
  setSelectedRowKeys: (v: React.Key[]) => void
  onRefresh: () => void
  onCreateCollection: () => void
  onRunCollection: () => void
  onAiGenerate: () => void
  onExplore: () => void
  onCreateScript: () => void
  moreMenuItems: any[]
  onMoreClick: (info: { key: string }) => void
}

const ScriptList: React.FC<ScriptListProps> = (p) => {
  const { t } = useTranslation()
  return (
    <>
      <div className="fst-page-header fst-animate-in">
        <h1 className="fst-page-title">{t('webTest.scriptManagement')}</h1>
        <Space>
          <Select placeholder="按用例集筛选" allowClear style={{ width: 220 }}
            value={p.selectedCollectionId} onChange={p.setSelectedCollectionId}
            options={p.collections.map(c => ({ value: c.id, label: `${c.name} (${c.script_count || 0})` }))} />
          <Input placeholder={t('webTest.searchScripts')} prefix={<SearchOutlined />}
            style={{ width: 250 }} allowClear value={p.searchText}
            onChange={e => p.setSearchText(e.target.value)} />
          <Button icon={<ReloadOutlined />} onClick={p.onRefresh} loading={p.loading}>{t('common.refresh')}</Button>
          <Button icon={<FolderAddOutlined />} onClick={p.onCreateCollection}>用例集</Button>
          <Button icon={<FolderOpenOutlined />} disabled={!p.selectedCollectionId} onClick={p.onRunCollection}>运行用例集</Button>
          <Button type="primary" icon={<RobotOutlined />} onClick={p.onAiGenerate}>AI 生成</Button>
          <Button icon={<GlobalOutlined />} onClick={p.onExplore}>探索测试</Button>
          <Button type="primary" icon={<PlusOutlined />} onClick={p.onCreateScript}>{t('webTest.createScript')}</Button>
          <Dropdown menu={{ items: p.moreMenuItems, onClick: p.onMoreClick }} disabled={p.selectedRowKeys.length === 0}>
            <Button icon={<MoreOutlined />}>更多</Button>
          </Dropdown>
        </Space>
      </div>
      <div className="fst-ios-card fst-animate-in fst-animate-in-1">
        <div className="fst-table-wrap">
          <Table
            rowSelection={{ selectedRowKeys: p.selectedRowKeys, onChange: p.setSelectedRowKeys }}
            columns={p.columns}
            dataSource={p.scripts.filter(s =>
              !p.searchText || s.name.toLowerCase().includes(p.searchText.toLowerCase()) ||
              s.description?.toLowerCase().includes(p.searchText.toLowerCase())
            )}
            rowKey="id" loading={p.loading}
            pagination={{ total: p.scripts.length, showTotal: total => `共 ${total} 条`, showSizeChanger: true, showQuickJumper: true }}
          />
        </div>
      </div>
    </>
  )
}

export default ScriptList
