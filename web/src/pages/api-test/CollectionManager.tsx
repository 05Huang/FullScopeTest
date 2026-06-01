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
  Tag,
  Tooltip
} from 'antd'
import {
  FolderAddOutlined,
  PlayCircleOutlined,
  DeleteOutlined,
  EditOutlined,
  InfoCircleOutlined
} from '@ant-design/icons'
import { useTranslation } from 'react-i18next'
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
  onSelectCollection?: (collectionId: number) => void
  onAiReview?: (collectionId: number) => void
}

const CollectionManager: React.FC<Props> = ({ onCollectionChange, onRunSuccess, onSelectCollection, onAiReview }) => {
  const { t } = useTranslation();
  const [collections, setCollections] = useState<Collection[]>([])
  const [environments, setEnvironments] = useState<Environment[]>([])
  const [loading, setLoading] = useState(false)
  const [modalVisible, setModalVisible] = useState(false)
  const [editingCollection, setEditingCollection] = useState<Collection | null>(null)
  const [runModalVisible, setRunModalVisible] = useState(false)
  const [selectedCollectionForRun, setSelectedCollectionForRun] = useState<Collection | null>(null)
  const [selectedEnvId, setSelectedEnvId] = useState<number | undefined>()
  const [form] = Form.useForm()

  // 默认环境选项：使用用例自身的环境配置
  const USE_CASE_OWN_ENV = -1

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
      message.error(error.message || t('apiTest.loadFailed'))
    } finally {
      setLoading(false)
    }
  }

  // 创建或编辑集合
  const handleSubmit = async (values: any) => {
    try {
      if (editingCollection) {
        await apiTestService.updateCollection(editingCollection.id, values)
        message.success(t('apiTest.environments.updateSuccess'))
      } else {
        await apiTestService.createCollection(values)
        message.success(t('apiTest.environments.createSuccess'))
      }
      
      setModalVisible(false)
      form.resetFields()
      setEditingCollection(null)
      loadData()
      onCollectionChange?.()
    } catch (error: any) {
      message.error(error.message || t('apiTest.operationFailed'))
    }
  }

  // 删除集合
  const handleDelete = async (id: number) => {
    try {
      await apiTestService.deleteCollection(id)
      message.success(t('apiTest.environments.deleteSuccess'))
      loadData()
      onCollectionChange?.()
    } catch (error: any) {
      message.error(error.message || t('apiTest.environments.deleteFailed'))
    }
  }

  // 批量运行集合
  const handleRunCollection = async () => {
    if (!selectedCollectionForRun) return
    
    try {
      setLoading(true)
      // 如果选择了“使用用例自身环境”，不传递 env_id（或传递 undefined）
      const envIdToSend = selectedEnvId === USE_CASE_OWN_ENV ? undefined : selectedEnvId
      
      const result = await apiTestService.runCollection(
        selectedCollectionForRun.id,
        envIdToSend !== undefined ? { env_id: envIdToSend } : {}
      )
      
      if (result.code === 200) {
        message.success(t('apiTest.runComplete', {passed: result.data.passed, failed: result.data.failed}))
        setRunModalVisible(false)
        onRunSuccess?.(result.data)
      }
    } catch (error: any) {
      message.error(error.message || t('apiTest.operationFailed'))
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
    setSelectedEnvId(USE_CASE_OWN_ENV) // 默认使用用例自身环境
    setRunModalVisible(true)
  }

  return (
    <div>
      <Card
        title={t("apiTest.collectionManager")}
        extra={
          <Button
            type="primary"
            icon={<FolderAddOutlined />}
            onClick={() => showEditModal()}
          >
            {t('apiTest.createCollection')}
          </Button>
        }
      >
        <List
          loading={loading}
          dataSource={collections}
          renderItem={(collection) => (
            <List.Item
              style={{
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'flex-start',
                padding: '12px 16px',
                gap: '12px'
              }}
            >
              <div 
                style={{ width: '100%', cursor: 'pointer' }}
                onClick={() => onSelectCollection?.(collection.id)}
              >
                <List.Item.Meta
                  title={
                    <Space style={{ width: '100%', wordBreak: 'break-all' }}>
                      <span style={{ fontSize: '15px', fontWeight: 500 }}>{collection.name}</span>
                      <Tag color="blue" style={{ marginLeft: '4px' }}>{t('apiTest.casesCount', {count: collection.case_count})}</Tag>
                    </Space>
                  }
                  description={collection.description || t('apiTest.noDescription')}
                  style={{ width: '100%' }}
                />
              </div>
              <div style={{ width: '100%', display: 'flex', justifyContent: 'flex-end', gap: '8px', flexWrap: 'wrap' }}>
                <Button
                  key="ai-review"
                  type="dashed"
                  size="small"
                  icon={<InfoCircleOutlined />}
                  onClick={(e) => {
                    e.stopPropagation()
                    onAiReview?.(collection.id)
                  }}
                  title="AI 评审"
                >
                  AI 评审
                </Button>
                <Button
                  key="run"
                  type="primary"
                  size="small"
                  icon={<PlayCircleOutlined />}
                  onClick={(e) => {
                    e.stopPropagation()
                    showRunModal(collection)
                  }}
                  disabled={collection.case_count === 0}
                  title="运行"
                >
                  运行
                </Button>
                <Button
                  key="edit"
                  size="small"
                  icon={<EditOutlined />}
                  onClick={(e) => {
                    e.stopPropagation()
                    showEditModal(collection)
                  }}
                  title={t('common.edit')}
                >
                  {t('common.edit')}
                </Button>
                <Popconfirm
                  key="delete"
                  title={t('apiTest.confirmDeleteCollection')}
                  onConfirm={(e) => {
                    e?.stopPropagation()
                    handleDelete(collection.id)
                  }}
                  onCancel={(e) => e?.stopPropagation()}
                  okText={t('common.confirm')}
                  cancelText={t('common.cancel')}
                >
                  <Button
                    size="small"
                    danger
                    icon={<DeleteOutlined />}
                    title={t('common.delete')}
                    onClick={(e) => e.stopPropagation()}
                  >
                    {t('common.delete')}
                  </Button>
                </Popconfirm>
              </div>
            </List.Item>
          )}
        />
      </Card>

      {/* 创建/编辑集合模态框 */}
      <Modal
        title={editingCollection ? t('apiTest.editCollection') : t('apiTest.newCollection')}
        visible={modalVisible}
        onOk={() => form.submit()}
        onCancel={() => {
          setModalVisible(false)
          form.resetFields()
          setEditingCollection(null)
        }}
        okText={t('common.confirm')}
        cancelText={t('common.cancel')}
      >
        <Form
          form={form}
          layout="vertical"
          onFinish={handleSubmit}
        >
          <Form.Item
            label={t('apiTest.collectionName')}
            name="name"
            rules={[{ required: true, message: t('apiTest.collectionNameRequired') }]}
          >
            <Input placeholder={t("apiTest.collectionNamePlaceholder")} />
          </Form.Item>
          
          <Form.Item
            label={t('apiTest.collectionDescription')}
            name="description"
          >
            <TextArea
              rows={4}
              placeholder={t("apiTest.collectionDescPlaceholder")}
            />
          </Form.Item>
        </Form>
      </Modal>

      {/* 运行集合模态框 */}
      <Modal
        title={t('apiTest.runCollection', {name: selectedCollectionForRun?.name})}
        visible={runModalVisible}
        onOk={handleRunCollection}
        onCancel={() => setRunModalVisible(false)}
        confirmLoading={loading}
        okText="开始运行"
        cancelText={t('common.cancel')}
      >
        <Form layout="vertical">
          <Form.Item label={(
            <Space>
              <span>{t("apiTest.selectEnvironment")}</span>
              <Tooltip title="可以选择“使用用例自身环境”，或选择具体环境覆盖所有用例">
                <InfoCircleOutlined style={{ color: '#1890ff' }} />
              </Tooltip>
            </Space>
          )}>
            <Select
              placeholder={t("apiTest.envSelectPlaceholder")}
              value={selectedEnvId}
              onChange={setSelectedEnvId}
            >
              <Select.Option key="default" value={USE_CASE_OWN_ENV}>
                <Tag color="blue">{t('apiTest.useCaseOwnEnv')}</Tag>
              </Select.Option>
              <Select.OptGroup label={t('apiTest.unifiedEnv')}>
                {environments.map(env => (
                  <Select.Option key={env.id} value={env.id}>
                    {env.name} {env.is_active && <Tag color="green">默认</Tag>}
                  </Select.Option>
                ))}
              </Select.OptGroup>
            </Select>
          </Form.Item>
          
          <p style={{ color: '#666', fontSize: '12px', marginTop: '8px' }}>
            {selectedEnvId === USE_CASE_OWN_ENV ? (
              <>
                🔹 {t('apiTest.envHintOwn')}
              </>
            ) : (
              <>
                🔸 {t('apiTest.envHintOverride', { env: <strong>{environments.find(e => e.id === selectedEnvId)?.name || ''}</strong> })}
              </>
            )}
          </p>
        </Form>
      </Modal>
    </div>
  )
}

export default CollectionManager
