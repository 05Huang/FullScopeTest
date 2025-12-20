import React, { useState, useEffect } from 'react'
import {
  Modal,
  Button,
  Input,
  Form,
  message,
  Space,
  Popconfirm,
  List,
  Card,
  Select,
  Tag
} from 'antd'
import {
  FolderAddOutlined,
  PlayCircleOutlined,
  DeleteOutlined,
  EditOutlined
} from '@ant-design/icons'
import { apiTestService, environmentService } from '@/services'

const { TextArea } = Input

interface Collection {
  id: number
  name: string
  description: string
  case_count: number
  project_id?: number
}

interface Environment {
  id: number
  name: string
  base_url: string
  variables: Record<string, any>
  is_active: boolean
}

interface Props {
  onCollectionChange?: () => void
  onRunSuccess?: (result: any) => void
}

const CollectionManager: React.FC<Props> = ({ onCollectionChange, onRunSuccess }) => {
  const [collections, setCollections] = useState<Collection[]>([])
  const [environments, setEnvironments] = useState<Environment[]>([])
  const [loading, setLoading] = useState(false)
  const [modalVisible, setModalVisible] = useState(false)
  const [editingCollection, setEditingCollection] = useState<Collection | null>(null)
  const [runModalVisible, setRunModalVisible] = useState(false)
  const [selectedCollectionForRun, setSelectedCollectionForRun] = useState<Collection | null>(null)
  const [selectedEnvId, setSelectedEnvId] = useState<number | undefined>()
  const [form] = Form.useForm()

  useEffect(() => {
    loadData()
  }, [])

  const loadData = async () => {
    setLoading(true)
    try {
      const [collectionsRes, envsRes] = await Promise.all([
        apiTestService.getCollections(),
        environmentService.getEnvironments()
      ])
      
      if (collectionsRes.code === 200) {
        setCollections(collectionsRes.data || [])
      }
      
      if (envsRes.code === 200) {
        setEnvironments(envsRes.data || [])
      }
    } catch (error: any) {
      message.error(error.message || '加载数据失败')
    } finally {
      setLoading(false)
    }
  }

  // 创建或编辑集合
  const handleSubmit = async (values: any) => {
    try {
      if (editingCollection) {
        await apiTestService.updateCollection(editingCollection.id, values)
        message.success('更新成功')
      } else {
        await apiTestService.createCollection(values)
        message.success('创建成功')
      }
      
      setModalVisible(false)
      form.resetFields()
      setEditingCollection(null)
      loadData()
      onCollectionChange?.()
    } catch (error: any) {
      message.error(error.message || '操作失败')
    }
  }

  // 删除集合
  const handleDelete = async (id: number) => {
    try {
      await apiTestService.deleteCollection(id)
      message.success('删除成功')
      loadData()
      onCollectionChange?.()
    } catch (error: any) {
      message.error(error.message || '删除失败')
    }
  }

  // 批量运行集合
  const handleRunCollection = async () => {
    if (!selectedCollectionForRun) return
    
    try {
      setLoading(true)
      const result = await apiTestService.runCollection(
        selectedCollectionForRun.id,
        { env_id: selectedEnvId }
      )
      
      if (result.code === 200) {
        message.success(
          `测试完成！通过: ${result.data.passed}, 失败: ${result.data.failed}`
        )
        setRunModalVisible(false)
        onRunSuccess?.(result.data)
      }
    } catch (error: any) {
      message.error(error.message || '执行失败')
    } finally {
      setLoading(false)
    }
  }

  // 显示编辑模态框
  const showEditModal = (collection?: Collection) => {
    if (collection) {
      setEditingCollection(collection)
      form.setFieldsValue(collection)
    } else {
      setEditingCollection(null)
      form.resetFields()
    }
    setModalVisible(true)
  }

  // 显示运行模态框
  const showRunModal = (collection: Collection) => {
    setSelectedCollectionForRun(collection)
    setRunModalVisible(true)
  }

  return (
    <div>
      <Card
        title="用例集合"
        extra={
          <Button
            type="primary"
            icon={<FolderAddOutlined />}
            onClick={() => showEditModal()}
          >
            新建集合
          </Button>
        }
      >
        <List
          loading={loading}
          dataSource={collections}
          renderItem={(collection) => (
            <List.Item
              actions={[
                <Button
                  key="run"
                  type="primary"
                  size="small"
                  icon={<PlayCircleOutlined />}
                  onClick={() => showRunModal(collection)}
                  disabled={collection.case_count === 0}
                  title="运行"
                />,
                <Button
                  key="edit"
                  size="small"
                  icon={<EditOutlined />}
                  onClick={() => showEditModal(collection)}
                  title="编辑"
                />,
                <Popconfirm
                  key="delete"
                  title="确认删除这个集合吗？"
                  onConfirm={() => handleDelete(collection.id)}
                  okText="确认"
                  cancelText="取消"
                >
                  <Button
                    size="small"
                    danger
                    icon={<DeleteOutlined />}
                    title="删除"
                  />
                </Popconfirm>
              ]}
            >
              <List.Item.Meta
                title={
                  <Space>
                    {collection.name}
                    <Tag>{collection.case_count} 个用例</Tag>
                  </Space>
                }
                description={collection.description || '暂无描述'}
              />
            </List.Item>
          )}
        />
      </Card>

      {/* 创建/编辑集合模态框 */}
      <Modal
        title={editingCollection ? '编辑集合' : '新建集合'}
        visible={modalVisible}
        onOk={() => form.submit()}
        onCancel={() => {
          setModalVisible(false)
          form.resetFields()
          setEditingCollection(null)
        }}
        okText="确定"
        cancelText="取消"
      >
        <Form
          form={form}
          layout="vertical"
          onFinish={handleSubmit}
        >
          <Form.Item
            label="集合名称"
            name="name"
            rules={[{ required: true, message: '请输入集合名称' }]}
          >
            <Input placeholder="例如：用户模块接口" />
          </Form.Item>
          
          <Form.Item
            label="描述"
            name="description"
          >
            <TextArea
              rows={4}
              placeholder="对这个集合的简要描述"
            />
          </Form.Item>
        </Form>
      </Modal>

      {/* 运行集合模态框 */}
      <Modal
        title={`运行集合: ${selectedCollectionForRun?.name}`}
        visible={runModalVisible}
        onOk={handleRunCollection}
        onCancel={() => setRunModalVisible(false)}
        confirmLoading={loading}
        okText="开始运行"
        cancelText="取消"
      >
        <Form layout="vertical">
          <Form.Item label="选择环境">
            <Select
              placeholder="请选择运行环境"
              value={selectedEnvId}
              onChange={setSelectedEnvId}
              allowClear
            >
              {environments.map(env => (
                <Select.Option key={env.id} value={env.id}>
                  {env.name} {env.is_active && <Tag color="green">默认</Tag>}
                </Select.Option>
              ))}
            </Select>
          </Form.Item>
          
          <p style={{ color: '#666', fontSize: '12px' }}>
            将执行该集合下的所有启用用例，并生成测试报告
          </p>
        </Form>
      </Modal>
    </div>
  )
}

export default CollectionManager
