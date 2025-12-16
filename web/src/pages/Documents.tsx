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
  Popconfirm,
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
import type { MenuProps } from 'antd'
import MonacoEditor from '@monaco-editor/react'
import ReactMarkdown from 'react-markdown'
import { documentService } from '@/services'

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
  const [loading, setLoading] = useState(false)
  const [documents, setDocuments] = useState<Document[]>([])
  const [selectedDoc, setSelectedDoc] = useState<Document | null>(null)
  const [content, setContent] = useState('')
  const [isEditing, setIsEditing] = useState(false)
  const [isModalOpen, setIsModalOpen] = useState(false)
  const [categories, setCategories] = useState<any[]>([])
  const [templates, setTemplates] = useState<any[]>([])
  const [form] = Form.useForm()
  
  // 假设使用项目 ID 1，实际应从项目选择器获取
  const projectId = 1

  useEffect(() => {
    fetchDocuments()
    fetchCategories()
    fetchTemplates()
  }, [])

  const fetchDocuments = async () => {
    setLoading(true)
    try {
      const res = await documentService.getDocuments(projectId)
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
      console.error('获取分类失败', error)
    }
  }

  const fetchTemplates = async () => {
    try {
      const res = await documentService.getTemplates()
      if (res.code === 200) {
        setTemplates(res.data || [])
      }
    } catch (error) {
      console.error('获取模板失败', error)
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
      message.error('获取文档详情失败')
    }
  }

  const handleSaveDoc = async () => {
    if (!selectedDoc) return
    try {
      const res = await documentService.updateDocument(selectedDoc.id, {
        content: content
      })
      if (res.code === 200) {
        message.success('保存成功')
        setIsEditing(false)
        setSelectedDoc({ ...selectedDoc, content })
      }
    } catch (error) {
      message.error('保存失败')
    }
  }

  const handleCreateDoc = async (values: any) => {
    try {
      // 如果选择了模板，使用模板内容
      let initialContent = defaultContent
      if (values.template) {
        const template = templates.find(t => t.id === values.template)
        if (template) {
          initialContent = template.content
        }
      }

      const res = await documentService.createDocument(projectId, {
        title: values.name,
        category: values.category,
        content: initialContent,
      })
      if (res.code === 200 || res.code === 201) {
        message.success('创建成功')
        setIsModalOpen(false)
        form.resetFields()
        fetchDocuments()
      }
    } catch (error) {
      message.error('创建失败')
    }
  }

  const handleDeleteDoc = async (docId: number) => {
    try {
      const res = await documentService.deleteDocument(docId)
      if (res.code === 200) {
        message.success('删除成功')
        if (selectedDoc?.id === docId) {
          setSelectedDoc(null)
          setContent('')
        }
        fetchDocuments()
      }
    } catch (error) {
      message.error('删除失败')
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
    documents.forEach(doc => {
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
    { key: 'export-md', icon: <ExportOutlined />, label: '导出 Markdown', onClick: () => handleExport('md') },
    { key: 'export-html', icon: <ExportOutlined />, label: '导出 HTML', onClick: () => handleExport('html') },
    { type: 'divider' },
    { 
      key: 'delete', 
      icon: <DeleteOutlined />, 
      label: '删除', 
      danger: true,
      onClick: () => {
        if (selectedDoc) {
          Modal.confirm({
            title: '确认删除',
            content: `确定要删除文档 "${selectedDoc.title}" 吗？`,
            onOk: () => handleDeleteDoc(selectedDoc.id)
          })
        }
      }
    },
  ]

  return (
    <Layout style={{ height: 'calc(100vh - 160px)', background: 'transparent' }}>
      {/* 左侧文档树 */}
      <Sider
        width={280}
        style={{
          background: '#fff',
          borderRadius: 8,
          marginRight: 16,
          overflow: 'hidden',
        }}
      >
        <div style={{ padding: 12 }}>
          <Space.Compact style={{ width: '100%', marginBottom: 12 }}>
            <Input
              placeholder="搜索文档..."
              prefix={<SearchOutlined />}
              allowClear
            />
            <Tooltip title="刷新">
              <Button
                icon={<ReloadOutlined />}
                onClick={fetchDocuments}
                loading={loading}
              />
            </Tooltip>
            <Tooltip title="新建文档">
              <Button
                icon={<PlusOutlined />}
                onClick={() => setIsModalOpen(true)}
              />
            </Tooltip>
          </Space.Compact>

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
                      if (doc) {
                        handleSelectDoc(doc)
                      }
                    }
                  }
                }}
                style={{ background: 'transparent' }}
              />
            ) : (
              <Empty description="暂无文档" style={{ marginTop: 40 }}>
                <Button type="primary" onClick={() => setIsModalOpen(true)}>
                  创建第一个文档
                </Button>
              </Empty>
            )}
          </Spin>
        </div>
      </Sider>

      {/* 右侧文档内容 */}
      <Content
        style={{
          background: '#fff',
          borderRadius: 8,
          display: 'flex',
          flexDirection: 'column',
          overflow: 'hidden',
        }}
      >
        {selectedDoc ? (
          <>
            {/* 工具栏 */}
            <div
              style={{
                padding: '12px 16px',
                borderBottom: '1px solid #f0f0f0',
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'center',
              }}
            >
              <Title level={5} style={{ margin: 0 }}>
                {selectedDoc.title}
              </Title>
              <Space>
                {isEditing ? (
                  <>
                    <Button onClick={() => {
                      setContent(selectedDoc.content || '')
                      setIsEditing(false)
                    }}>
                      取消
                    </Button>
                    <Button
                      type="primary"
                      icon={<SaveOutlined />}
                      onClick={handleSaveDoc}
                    >
                      保存
                    </Button>
                  </>
                ) : (
                  <>
                    <Button
                      icon={<EditOutlined />}
                      onClick={() => setIsEditing(true)}
                    >
                      编辑
                    </Button>
                    <Dropdown menu={{ items: moreMenuItems }}>
                      <Button icon={<MoreOutlined />} />
                    </Dropdown>
                  </>
                )}
              </Space>
            </div>

            {/* 内容区域 */}
            <div style={{ flex: 1, overflow: 'auto' }}>
              {isEditing ? (
                <div style={{ display: 'flex', height: '100%' }}>
                  {/* 编辑器 */}
                  <div style={{ flex: 1, borderRight: '1px solid #f0f0f0' }}>
                    <MonacoEditor
                      height="100%"
                      language="markdown"
                      theme="vs-light"
                      value={content}
                      onChange={(value) => setContent(value || '')}
                      options={{
                        minimap: { enabled: false },
                        fontSize: 14,
                        wordWrap: 'on',
                        scrollBeyondLastLine: false,
                        automaticLayout: true,
                      }}
                    />
                  </div>
                  {/* 预览 */}
                  <div
                    style={{
                      flex: 1,
                      padding: 24,
                      overflow: 'auto',
                      background: '#fafafa',
                    }}
                  >
                    <div className="markdown-body">
                      <ReactMarkdown>{content}</ReactMarkdown>
                    </div>
                  </div>
                </div>
              ) : (
                <div style={{ padding: 24, overflow: 'auto', height: '100%' }}>
                  <div className="markdown-body">
                    <ReactMarkdown>{content}</ReactMarkdown>
                  </div>
                </div>
              )}
            </div>
          </>
        ) : (
          <div
            style={{
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              height: '100%',
            }}
          >
            <Empty description="请从左侧选择文档或创建新文档">
              <Button type="primary" onClick={() => setIsModalOpen(true)}>
                创建新文档
              </Button>
            </Empty>
          </div>
        )}
      </Content>

      {/* 新建文档弹窗 */}
      <Modal
        title="新建文档"
        open={isModalOpen}
        onCancel={() => {
          setIsModalOpen(false)
          form.resetFields()
        }}
        onOk={() => {
          form.validateFields().then(handleCreateDoc)
        }}
      >
        <Form form={form} layout="vertical">
          <Form.Item
            name="name"
            label="文档名称"
            rules={[{ required: true, message: '请输入文档名称' }]}
          >
            <Input placeholder="请输入文档名称" />
          </Form.Item>
          <Form.Item
            name="category"
            label="文档分类"
            rules={[{ required: true, message: '请选择文档分类' }]}
          >
            <Select
              placeholder="请选择文档分类"
              options={categories.map(cat => ({
                value: cat.value,
                label: `${cat.icon} ${cat.label}`
              }))}
            />
          </Form.Item>
          <Form.Item
            name="template"
            label="使用模板"
          >
            <Select
              placeholder="选择模板（可选）"
              allowClear
              options={templates.map(tpl => ({
                value: tpl.id,
                label: tpl.name
              }))}
            />
          </Form.Item>
        </Form>
      </Modal>
    </Layout>
  )
}

export default Documents
