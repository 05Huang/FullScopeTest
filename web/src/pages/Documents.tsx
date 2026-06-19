import logger from "@/utils/logger"
import { useState, useEffect } from 'react'
import {
  Layout,
  Tree,
  Input,
  Button,
  Space,
  Typography,
  Modal,
  Form,
  Select,
  message,
  Tooltip,
  Dropdown,
  Empty,
  Spin,
  type MenuProps,
} from 'antd'
import {
  PlusOutlined,
  SearchOutlined,
  FolderOutlined,
  FileTextOutlined,
  EditOutlined,
  DeleteOutlined,
  SaveOutlined,
  MoreOutlined,
  ExportOutlined,
  ReloadOutlined,
} from '@ant-design/icons'
import type { DataNode } from 'antd/es/tree'
import MonacoEditor from '@monaco-editor/react'
import ReactMarkdown from 'react-markdown'
import { useTranslation } from 'react-i18next'
import { documentService } from '@/services'
import { useProjectStore } from '@/stores/projectStore'

const { Sider, Content } = Layout
const { Title } = Typography

interface Document {
  id: number
  title: string
  content?: string
  category: string
  tags: string[]
  updated_at: string
}

// 默认 Markdown 模板
const defaultContent = `# 新文档

## 概述

请在这里编写文档内容...

## 内容

### 1. 第一部分

描述...

### 2. 第二部分

描述...
`

const Documents = () => {
  const { t } = useTranslation();
  const [loading, setLoading] = useState(false)
  const [documents, setDocuments] = useState<Document[]>([])
  const [selectedDoc, setSelectedDoc] = useState<Document | null>(null)
  const [content, setContent] = useState('')
  const [isEditing, setIsEditing] = useState(false)
  const [isModalOpen, setIsModalOpen] = useState(false)
  const [categories, setCategories] = useState<any[]>([])
  const [templates, setTemplates] = useState<any[]>([])
  const [searchText, setSearchText] = useState('')
  const [form] = Form.useForm()
  const { currentProjectId } = useProjectStore()

  useEffect(() => {
    fetchDocuments()
    fetchCategories()
    fetchTemplates()
  }, [currentProjectId])

  const fetchDocuments = async () => {
    if (!currentProjectId) return
    setLoading(true)
    try {
      const res = await documentService.getDocuments(currentProjectId)
      if (res.code === 200) {
        setDocuments(res.data.items || res.data || [])
      }
    } catch (error) {
      // 如果后端没有数据，使用空数组
      setDocuments([])
    } finally {
      setLoading(false)
    }
  }

  const fetchCategories = async () => {
    try {
      const res = await documentService.getCategories()
      if (res.code === 200) {
        setCategories(res.data || [])
      }
    } catch (error) {
      logger.error('获取分类失败', error)
    }
  }

  const fetchTemplates = async () => {
    try {
      const res = await documentService.getTemplates()
      if (res.code === 200) {
        setTemplates(res.data || [])
      }
    } catch (error) {
      logger.error('获取模板失败', error)
    }
  }

  const handleSelectDoc = async (doc: Document) => {
    try {
      const res = await documentService.getDocument(doc.id)
      if (res.code === 200) {
        setSelectedDoc(res.data)
        setContent(res.data.content || '')
        setIsEditing(false)
      }
    } catch (error) {
      message.error(t('documents.fetchFailed'))
    }
  }

  const handleSaveDoc = async () => {
    if (!selectedDoc) return
    try {
      const res = await documentService.updateDocument(selectedDoc.id, {
        content: content
      })
      if (res.code === 200) {
        message.success(t('documents.saveSuccess'))
        setIsEditing(false)
        setSelectedDoc({ ...selectedDoc, content })
      }
    } catch (error) {
      message.error(t('documents.saveFailed'))
    }
  }

  const handleCreateDoc = async (values: any) => {
    if (!currentProjectId) return
    try {
      // 如果选择了模板，使用模板内容
      let initialContent = defaultContent
      if (values.template) {
        const template = templates.find(t => t.id === values.template)
        if (template) {
          initialContent = template.content
        }
      }

      const res = await documentService.createDocument(currentProjectId, {
        title: values.name,
        category: values.category,
        content: initialContent,
      })
      if (res.code === 200 || res.code === 201) {
        message.success(t('documents.createSuccess'))
        setIsModalOpen(false)
        form.resetFields()
        fetchDocuments()
      }
    } catch (error) {
      message.error(t('documents.createFailed'))
    }
  }

  const handleDeleteDoc = async (docId: number) => {
    try {
      const res = await documentService.deleteDocument(docId)
      if (res.code === 200) {
        message.success(t('documents.deleteSuccess'))
        if (selectedDoc?.id === docId) {
          setSelectedDoc(null)
          setContent('')
        }
        fetchDocuments()
      }
    } catch (error) {
      message.error(t('documents.deleteFailed'))
    }
  }

  const handleExport = (format: 'md' | 'html') => {
    if (!selectedDoc) return
    const url = documentService.getDocExportUrl(selectedDoc.id, format)
    window.open(url, '_blank')
  }

  // 构建文档树
  const buildTreeData = (): DataNode[] => {
    const categoryMap: Record<string, DataNode> = {}
    
    // 过滤文档
    const filteredDocs = documents.filter(doc =>
      !searchText || 
      doc.title.toLowerCase().includes(searchText.toLowerCase()) ||
      doc.category?.toLowerCase().includes(searchText.toLowerCase())
    )
    
    // 初始化分类节点
    categories.forEach(cat => {
      categoryMap[cat.value] = {
        title: `${cat.icon} ${cat.label}`,
        key: cat.value,
        icon: <FolderOutlined />,
        children: [],
      }
    })

    // 添加默认分类
    if (!categoryMap['other']) {
      categoryMap['other'] = {
        title: '📄 其他',
        key: 'other',
        icon: <FolderOutlined />,
        children: [],
      }
    }

    // 将文档添加到对应分类
    filteredDocs.forEach(doc => {
      const category = doc.category || 'other'
      if (!categoryMap[category]) {
        categoryMap[category] = {
          title: category,
          key: category,
          icon: <FolderOutlined />,
          children: [],
        }
      }
      (categoryMap[category].children as DataNode[]).push({
        title: doc.title,
        key: `doc-${doc.id}`,
        icon: <FileTextOutlined />,
        isLeaf: true,
      })
    })

    return Object.values(categoryMap).filter(node => 
      (node.children as DataNode[]).length > 0
    )
  }

  // 更多操作菜单
  const moreMenuItems: MenuProps['items'] = [
    { key: 'export-md', icon: <ExportOutlined />, label: t('documents.exportMd'), onClick: () => handleExport('md') },
    { key: 'export-html', icon: <ExportOutlined />, label: t('documents.exportHtml'), onClick: () => handleExport('html') },
    { type: 'divider' },
    { 
      key: 'delete', 
      icon: <DeleteOutlined />, 
      label: t('common.delete'), 
      danger: true,
      onClick: () => {
        if (selectedDoc) {
          Modal.confirm({
            title: t('documents.confirmDelete'),
            content: `确定要删除文档 "${selectedDoc.title}" 吗？`,
            onOk: () => handleDeleteDoc(selectedDoc.id)
          })
        }
      }
    },
  ]

  return (
    <div style={{ display: 'flex', gap: 16, height: 'calc(100vh - 160px)' }}>
      {/* Left: Document Tree */}
      <div className="fst-ios-card" style={{ width: 280, flexShrink: 0, display: 'flex', flexDirection: 'column', overflow: 'hidden' }}>
        <div style={{ padding: '12px 12px 0', display: 'flex', gap: 6, marginBottom: 12 }}>
          <Input
            placeholder={t("documents.searchPlaceholder")}
            prefix={<SearchOutlined />}
            allowClear
            value={searchText}
            onChange={(e) => setSearchText(e.target.value)}
            size="small"
            style={{ flex: 1 }}
          />
          <Tooltip title={t("common.refresh")}>
            <Button icon={<ReloadOutlined />} onClick={fetchDocuments} loading={loading} size="small" />
          </Tooltip>
          <Tooltip title={t("documents.createNew")}>
            <Button icon={<PlusOutlined />} onClick={() => setIsModalOpen(true)} size="small" type="primary" />
          </Tooltip>
        </div>
        <div style={{ flex: 1, overflow: 'auto', padding: '0 4px' }}>
          <Spin spinning={loading}>
            {documents.length > 0 || categories.length > 0 ? (
              <Tree
                showIcon
                defaultExpandAll
                selectedKeys={selectedDoc ? [`doc-${selectedDoc.id}`] : []}
                treeData={buildTreeData()}
                onSelect={(keys) => {
                  if (keys.length > 0 && typeof keys[0] === 'string') {
                    const key = keys[0] as string
                    if (key.startsWith('doc-')) {
                      const docId = parseInt(key.replace('doc-', ''))
                      const doc = documents.find(d => d.id === docId)
                      if (doc) handleSelectDoc(doc)
                    }
                  }
                }}
                style={{ background: 'transparent' }}
              />
            ) : (
              <div className="fst-empty" style={{ padding: '40px 16px' }}>
                <div className="fst-empty-title" style={{ fontSize: 14 }}>{t("documents.noDocuments")}</div>
                <button className="fst-btn fst-btn--primary fst-btn--sm" style={{ marginTop: 12 }} onClick={() => setIsModalOpen(true)}>
                  {t("documents.createFirst")}
                </button>
              </div>
            )}
          </Spin>
        </div>
      </div>

      {/* Right: Document Content */}
      <div className="fst-ios-card" style={{ flex: 1, display: 'flex', flexDirection: 'column', overflow: 'hidden' }}>
        {selectedDoc ? (
          <>
            <div style={{ padding: '12px 16px', borderBottom: '1px solid var(--fst-outline-soft)', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <div style={{ fontWeight: 600, fontSize: 16, color: 'var(--fst-on-surface)' }}>{selectedDoc.title}</div>
              <div style={{ display: 'flex', gap: 8 }}>
                {isEditing ? (
                  <>
                    <button className="fst-btn fst-btn--ghost fst-btn--sm" onClick={() => { setContent(selectedDoc.content || ''); setIsEditing(false) }}>{t("common.cancel")}</button>
                    <button className="fst-btn fst-btn--primary fst-btn--sm" onClick={handleSaveDoc}><SaveOutlined /> {t("common.save")}</button>
                  </>
                ) : (
                  <>
                    <button className="fst-btn fst-btn--ghost fst-btn--sm" onClick={() => setIsEditing(true)}><EditOutlined /> {t("common.edit")}</button>
                    <Dropdown menu={{ items: moreMenuItems }}>
                      <button className="fst-btn fst-btn--ghost fst-btn--sm"><MoreOutlined /></button>
                    </Dropdown>
                  </>
                )}
              </div>
            </div>
            <div style={{ flex: 1, overflow: 'auto' }}>
              {isEditing ? (
                <div style={{ display: 'flex', height: '100%' }}>
                  <div style={{ flex: 1, borderRight: '1px solid var(--fst-outline-soft)' }}>
                    <MonacoEditor
                      height="100%"
                      language="markdown"
                      theme="vs-light"
                      value={content}
                      onChange={(value) => setContent(value || '')}
                      options={{ minimap: { enabled: false }, fontSize: 14, wordWrap: 'on', scrollBeyondLastLine: false, automaticLayout: true }}
                    />
                  </div>
                  <div style={{ flex: 1, padding: 24, overflow: 'auto', background: 'var(--fst-surface)' }}>
                    <div className="markdown-body"><ReactMarkdown>{content}</ReactMarkdown></div>
                  </div>
                </div>
              ) : (
                <div style={{ padding: 24, overflow: 'auto', height: '100%' }}>
                  <div className="markdown-body"><ReactMarkdown>{content}</ReactMarkdown></div>
                </div>
              )}
            </div>
          </>
        ) : (
          <div className="fst-empty" style={{ flex: 1 }}>
            <div className="fst-empty-icon"><FileTextOutlined /></div>
            <div className="fst-empty-title">{t("documents.selectOrCreate")}</div>
            <button className="fst-btn fst-btn--primary" style={{ marginTop: 16 }} onClick={() => setIsModalOpen(true)}>{t("documents.createNew")}</button>
          </div>
        )}
      </div>

      {/* New Document Modal */}
      <Modal
        title={t("documents.createNew")}
        open={isModalOpen}
        onCancel={() => { setIsModalOpen(false); form.resetFields() }}
        onOk={() => form.validateFields().then(handleCreateDoc)}
      >
        <Form form={form} layout="vertical">
          <Form.Item name="name" label={<span style={{ fontWeight: 600, fontSize: 13 }}>{t('documents.docName')}</span>} rules={[{ required: true, message: t('documents.docNameRequired') }]}>
            <Input placeholder={t("documents.docNamePlaceholder")} />
          </Form.Item>
          <Form.Item name="category" label={<span style={{ fontWeight: 600, fontSize: 13 }}>{t('documents.docCategory')}</span>} rules={[{ required: true, message: t('documents.docCategoryRequired') }]}>
            <Select placeholder={t("documents.docCategoryPlaceholder")} options={categories.map(cat => ({ value: cat.value, label: `${cat.icon} ${cat.label}` }))} />
          </Form.Item>
          <Form.Item name="template" label={<span style={{ fontWeight: 600, fontSize: 13 }}>{t('documents.useTemplate')}</span>}>
            <Select placeholder={t("documents.templatePlaceholder")} allowClear options={templates.map(tpl => ({ value: tpl.id, label: tpl.name }))} />
          </Form.Item>
        </Form>
      </Modal>
    </div>
  )
}

export default Documents
