import React, { useState, useEffect } from 'react'
import { Button, Table, Space, Tag, message, Modal, Select, Card } from 'antd'
import { DeleteOutlined, EyeOutlined, ReloadOutlined } from '@ant-design/icons'
import { testReportService } from '@/services'

const { Option } = Select

interface TestReport {
  id: number
  test_run_id: number
  project_id: number
  test_type: string
  title: string
  summary: {
    total: number
    passed: number
    failed: number
    success_rate: number
    duration: number
    environment?: string
  }
  status: string
  created_at: string
  updated_at: string
}

const TestReports: React.FC = () => {
  const [reports, setReports] = useState<TestReport[]>([])
  const [loading, setLoading] = useState(false)
  const [currentReport, setCurrentReport] = useState<TestReport | null>(null)
  const [reportHtml, setReportHtml] = useState<string>('')
  const [htmlModalVisible, setHtmlModalVisible] = useState(false)
  const [filters, setFilters] = useState({
    test_type: undefined as string | undefined,
    project_id: undefined as number | undefined
  })
  const [pagination, setPagination] = useState({
    current: 1,
    pageSize: 20,
    total: 0
  })

  // 加载报告列表
  const loadReports = async () => {
    setLoading(true)
    try {
      const res = await testReportService.getTestReports({
        test_type: filters.test_type,
        project_id: filters.project_id,
        page: pagination.current,
        per_page: pagination.pageSize
      })
      
      if (res.code === 200 && res.data) {
        setReports(res.data.items || [])
        setPagination({
          ...pagination,
          total: res.data.total || 0
        })
      }
    } catch (error: any) {
      message.error(error.message || '加载报告列表失败')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    loadReports()
  }, [filters, pagination.current])

  // 查看报告详情
  const handleViewReport = async (report: TestReport) => {
    try {
      setLoading(true)
      const html = await testReportService.getTestReportHtml(report.id)
      setReportHtml(html)
      setCurrentReport(report)
      setHtmlModalVisible(true)
    } catch (error: any) {
      message.error(error.message || '获取报告详情失败')
    } finally {
      setLoading(false)
    }
  }

  // 删除报告
  const handleDeleteReport = async (reportId: number) => {
    Modal.confirm({
      title: '确认删除',
      content: '删除后将无法恢复，确定要删除这个报告吗？',
      onOk: async () => {
        try {
          await testReportService.deleteTestReport(reportId)
          message.success('删除成功')
          loadReports()
        } catch (error: any) {
          message.error(error.message || '删除失败')
        }
      }
    })
  }

  // 下载报告 HTML
  const handleDownloadHtml = () => {
    if (!reportHtml || !currentReport) return
    
    const blob = new Blob([reportHtml], { type: 'text/html' })
    const url = window.URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `${currentReport.title}_${new Date().getTime()}.html`
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    window.URL.revokeObjectURL(url)
    message.success('下载成功')
  }

  // 表格列定义
  const columns = [
    {
      title: 'ID',
      dataIndex: 'id',
      key: 'id',
      width: 80
    },
    {
      title: '报告标题',
      dataIndex: 'title',
      key: 'title',
      ellipsis: true
    },
    {
      title: '测试类型',
      dataIndex: 'test_type',
      key: 'test_type',
      width: 120,
      render: (type: string) => {
        const typeMap: Record<string, { color: string; text: string }> = {
          api: { color: 'blue', text: '接口测试' },
          web: { color: 'green', text: 'Web测试' },
          performance: { color: 'orange', text: '性能测试' }
        }
        const config = typeMap[type] || { color: 'default', text: type }
        return <Tag color={config.color}>{config.text}</Tag>
      }
    },
    {
      title: '测试统计',
      key: 'summary',
      width: 200,
      render: (_: any, record: TestReport) => (
        <Space size="small">
          <Tag color="green">通过: {record.summary.passed}</Tag>
          <Tag color="red">失败: {record.summary.failed}</Tag>
        </Space>
      )
    },
    {
      title: '成功率',
      key: 'success_rate',
      width: 100,
      render: (_: any, record: TestReport) => (
        <Tag color={record.summary.success_rate >= 80 ? 'green' : 'red'}>
          {record.summary.success_rate}%
        </Tag>
      )
    },
    {
      title: '耗时',
      key: 'duration',
      width: 100,
      render: (_: any, record: TestReport) => `${record.summary.duration}s`
    },
    {
      title: '状态',
      dataIndex: 'status',
      key: 'status',
      width: 100,
      render: (status: string) => {
        const statusMap: Record<string, { color: string; text: string }> = {
          generated: { color: 'success', text: '已生成' },
          generating: { color: 'processing', text: '生成中' },
          failed: { color: 'error', text: '失败' }
        }
        const config = statusMap[status] || { color: 'default', text: status }
        return <Tag color={config.color}>{config.text}</Tag>
      }
    },
    {
      title: '生成时间',
      dataIndex: 'created_at',
      key: 'created_at',
      width: 180,
      render: (text: string) => new Date(text).toLocaleString('zh-CN')
    },
    {
      title: '操作',
      key: 'action',
      width: 150,
      fixed: 'right' as const,
      render: (_: any, record: TestReport) => (
        <Space size="small">
          <Button
            type="link"
            size="small"
            icon={<EyeOutlined />}
            onClick={() => handleViewReport(record)}
          >
            查看
          </Button>
          <Button
            type="link"
            size="small"
            danger
            icon={<DeleteOutlined />}
            onClick={() => handleDeleteReport(record.id)}
          >
            删除
          </Button>
        </Space>
      )
    }
  ]

  return (
    <div style={{ padding: '24px' }}>
      <Card>
        <div style={{ marginBottom: 16 }}>
          <Space>
            <Select
              placeholder="测试类型"
              style={{ width: 150 }}
              allowClear
              value={filters.test_type}
              onChange={(value) => setFilters({ ...filters, test_type: value })}
            >
              <Option value="api">接口测试</Option>
              <Option value="web">Web测试</Option>
              <Option value="performance">性能测试</Option>
            </Select>
            <Button
              icon={<ReloadOutlined />}
              onClick={loadReports}
            >
              刷新
            </Button>
          </Space>
        </div>

        <Table
          columns={columns}
          dataSource={reports}
          rowKey="id"
          loading={loading}
          pagination={{
            current: pagination.current,
            pageSize: pagination.pageSize,
            total: pagination.total,
            showSizeChanger: true,
            showQuickJumper: true,
            showTotal: (total) => `共 ${total} 条`,
            onChange: (page, pageSize) => {
              setPagination({ ...pagination, current: page, pageSize: pageSize || 20 })
            }
          }}
          scroll={{ x: 1200 }}
        />
      </Card>

      {/* 报告详情模态框 */}
      <Modal
        title={currentReport?.title}
        visible={htmlModalVisible}
        onCancel={() => setHtmlModalVisible(false)}
        width="90%"
        style={{ top: 20 }}
        footer={[
          <Button key="download" type="primary" onClick={handleDownloadHtml}>
            下载 HTML
          </Button>,
          <Button key="close" onClick={() => setHtmlModalVisible(false)}>
            关闭
          </Button>
        ]}
      >
        <div
          style={{
            height: '70vh',
            overflow: 'auto',
            border: '1px solid #d9d9d9',
            borderRadius: '4px'
          }}
          dangerouslySetInnerHTML={{ __html: reportHtml }}
        />
      </Modal>
    </div>
  )
}

export default TestReports
