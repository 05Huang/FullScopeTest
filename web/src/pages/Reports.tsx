import { useEffect, useState } from 'react'
import {
  Button,
  Card,
  Col,
  DatePicker,
  Dropdown,
  Input,
  Modal,
  Popconfirm,
  Row,
  Select,
  Space,
  Statistic,
  Table,
  Tag,
  Tooltip,
  Typography,
  message,
} from 'antd'
import {
  CheckCircleOutlined,
  ClockCircleOutlined,
  CloseCircleOutlined,
  DeleteOutlined,
  DownloadOutlined,
  EyeOutlined,
  FileTextOutlined,
  MoreOutlined,
  SearchOutlined,
} from '@ant-design/icons'
import type { MenuProps } from 'antd'
import type { ColumnsType } from 'antd/es/table'
import ReactECharts from 'echarts-for-react'
import type { TestReport } from '@/services/reportService'
import { reportService } from '@/services'
import api from '@/services/api'

const { Title, Text } = Typography
const { RangePicker } = DatePicker

interface TestRun {
  id: number
  project_id: number
  test_type: string
  test_object_id?: number
  test_object_name?: string
  status: string
  total_cases: number
  passed: number
  failed: number
  skipped: number
  error: number
  pass_rate: number
  duration?: number
  started_at?: string
  finished_at?: string
  environment_name?: string
  triggered_by: string
  created_at: string
}

const typeConfig: Record<string, { color: string; text: string }> = {
  api: { color: 'blue', text: 'API测试' },
  web: { color: 'purple', text: 'Web测试' },
  performance: { color: 'orange', text: '性能测试' },
  perf: { color: 'orange', text: '性能测试' },
}

const statusConfig: Record<string, { color: string; text: string }> = {
  pending: { color: 'default', text: '等待中' },
  running: { color: 'processing', text: '执行中' },
  success: { color: 'success', text: '成功' },
  failed: { color: 'error', text: '失败' },
  cancelled: { color: 'warning', text: '已取消' },
}

const Reports = () => {
  const [loading, setLoading] = useState(false)
  const [selectedRowKeys, setSelectedRowKeys] = useState<React.Key[]>([])
  const [testRuns, setTestRuns] = useState<TestRun[]>([])
  const [testReports, setTestReports] = useState<TestReport[]>([])
  const [reportHtml, setReportHtml] = useState('')
  const [htmlModalVisible, setHtmlModalVisible] = useState(false)
  const [currentReportTitle, setCurrentReportTitle] = useState('')
  const [statistics, setStatistics] = useState({
    total_runs: 0,
    success_runs: 0,
    failed_runs: 0,
    success_rate: 0,
  })
  const [dailyTrend, setDailyTrend] = useState<Array<{ date: string; passed: number; failed: number }>>([])
  const [pagination, setPagination] = useState({ current: 1, pageSize: 10, total: 0 })
  const [filters, setFilters] = useState({ keyword: '', test_type: '' })

  useEffect(() => {
    fetchData()
  }, [pagination.current, pagination.pageSize, filters.keyword, filters.test_type])

  const fetchData = async () => {
    try {
      setLoading(true)
      const [runsRes, reportsRes, statsRes] = await Promise.all([
        reportService.getTestRuns({
          page: pagination.current,
          per_page: pagination.pageSize,
          test_type: filters.test_type || undefined,
        }),
        reportService.getTestReports({
          page: pagination.current,
          per_page: pagination.pageSize,
          test_type: filters.test_type || undefined,
        }),
        reportService.getReportStatistics({ days: 7 }),
      ])

      const runsData: any = runsRes?.data
      const runsList: TestRun[] = Array.isArray(runsData?.items)
        ? runsData.items
        : Array.isArray(runsData)
          ? runsData
          : []
      const runsTotal = (runsData && typeof runsData.total === 'number') ? runsData.total : runsList.length

      const reportsData: any = reportsRes?.data
      const reportsList: TestReport[] = Array.isArray(reportsData?.items)
        ? reportsData.items
        : Array.isArray(reportsData)
          ? reportsData
          : []

      setTestRuns(runsList)
      setPagination((prev) => ({ ...prev, total: runsTotal }))
      setTestReports(reportsList)

      const statsData = statsRes?.data
      setStatistics(statsData?.summary || { total_runs: 0, success_runs: 0, failed_runs: 0, success_rate: 0 })
      setDailyTrend(statsData?.daily_trend || [])
    } catch (error) {
      message.error('获取数据失败')
      console.error(error)
    } finally {
      setLoading(false)
    }
  }

  const findReportByRunId = (runId: number) =>
    testReports.find((report) => report.test_run_id === runId)

  const downloadReportJson = async (runId: number, filename?: string) => {
    const response = await api.get(`/reports/${runId}/export`, {
      params: { format: 'json' },
      responseType: 'blob',
    })
    const blob = new Blob([response.data], { type: 'application/json' })
    const link = document.createElement('a')
    link.href = URL.createObjectURL(blob)
    link.download = filename || `test-report-${runId}.json`
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    URL.revokeObjectURL(link.href)
  }

  const getReportName = (report: TestReport) => {
    const run = testRuns.find((r) => r.id === report.test_run_id)
    return run?.test_object_name || report.title || 'test-run'
  }

  const handleViewReport = async (runId: number, title: string) => {
    const report = findReportByRunId(runId)
    if (!report) {
      message.warning('未找到该执行的报告')
      return
    }

    try {
      setCurrentReportTitle(title)
      const html = await reportService.getTestReportHtml(report.id)
      setReportHtml(html)
      setHtmlModalVisible(true)
    } catch (error) {
      message.error('获取报告失败')
      console.error(error)
    }
  }

  const handleExportJson = async (runId: number) => {
    const report = findReportByRunId(runId)
    if (!report) {
      message.warning('未找到该执行的报告')
      return
    }

    try {
      await downloadReportJson(report.test_run_id, `${getReportName(report)}-${report.id}.json`)
      message.success('已开始下载')
    } catch (error) {
      message.error('下载失败')
      console.error(error)
    }
  }

  const handleDelete = async (runId: number) => {
    const report = findReportByRunId(runId)

    try {
      if (report) {
        await reportService.deleteTestReport(report.id)
      } else {
        // 回退删除执行记录，避免无匹配报告时无请求
        await reportService.deleteTestRun(runId)
      }
      message.success('删除成功')
      setSelectedRowKeys((prev) => prev.filter((key) => key !== runId))
      fetchData()
    } catch (error) {
      message.error('删除失败')
      console.error(error)
    }
  }

  const handleBatchDelete = async () => {
    if (selectedRowKeys.length === 0) {
      message.warning('请选择要删除的执行记录')
      return
    }

    try {
      setLoading(true)
      await Promise.all(
        selectedRowKeys.map(async (key) => {
          const runId = Number(key)
          const report = findReportByRunId(runId)
          if (report) {
            await reportService.deleteTestReport(report.id)
          } else {
            await reportService.deleteTestRun(runId)
          }
        }),
      )
      message.success('已删除选中记录')
      setSelectedRowKeys([])
      fetchData()
    } catch (error) {
      message.error('批量删除失败')
      console.error(error)
    } finally {
      setLoading(false)
    }
  }

  const handleBatchDownload = async () => {
    if (selectedRowKeys.length === 0) {
      message.warning('请选择要下载的执行记录')
      return
    }

    try {
      for (const key of selectedRowKeys) {
        const runId = Number(key)
        const report = findReportByRunId(runId)
        if (report) {
          await downloadReportJson(report.test_run_id, `${getReportName(report)}-${report.id}.json`)
        }
      }
      message.success('下载完成')
    } catch (error) {
      message.error('批量下载失败')
      console.error(error)
    }
  }

  const trendOption = {
    tooltip: { trigger: 'axis' },
    legend: { data: ['通过', '失败'] },
    grid: { left: '3%', right: '4%', bottom: '3%', containLabel: true },
    xAxis: {
      type: 'category',
      boundaryGap: true,
      data: dailyTrend.length > 0 ? dailyTrend.map((d) => d.date) : [],
    },
    yAxis: { type: 'value' },
    series: [
      {
        name: '通过',
        type: 'bar',
        stack: 'total',
        data: dailyTrend.length > 0 ? dailyTrend.map((d) => d.passed) : [],
        itemStyle: { color: '#52c41a' },
      },
      {
        name: '失败',
        type: 'bar',
        stack: 'total',
        data: dailyTrend.length > 0 ? dailyTrend.map((d) => d.failed) : [],
        itemStyle: { color: '#ff4d4f' },
      },
    ],
  }

  const formatDuration = (seconds?: number) => {
    if (!seconds) return '-'
    if (seconds < 60) return `${seconds.toFixed(1)}秒`
    const minutes = Math.floor(seconds / 60)
    const secs = Math.round(seconds % 60)
    return `${minutes}分${secs}秒`
  }

  const columns: ColumnsType<TestRun> = [
    {
      title: '测试名称',
      dataIndex: 'test_object_name',
      key: 'test_object_name',
      render: (text, record) => (
        <Space>
          <FileTextOutlined style={{ color: '#1890ff' }} />
          <Text strong>{text || `测试执行 #${record.id}`}</Text>
        </Space>
      ),
    },
    {
      title: '类型',
      dataIndex: 'test_type',
      key: 'test_type',
      width: 100,
      render: (type) => <Tag color={typeConfig[type]?.color}>{typeConfig[type]?.text || type}</Tag>,
    },
    {
      title: '状态',
      dataIndex: 'status',
      key: 'status',
      width: 100,
      render: (status) => <Tag color={statusConfig[status]?.color}>{statusConfig[status]?.text || status}</Tag>,
    },
    {
      title: '测试结果',
      key: 'result',
      width: 200,
      render: (_, record) => (
        <Space>
          <Tag icon={<CheckCircleOutlined />} color="success">
            {record.passed}
          </Tag>
          <Tag icon={<CloseCircleOutlined />} color="error">
            {record.failed}
          </Tag>
          <Text type="secondary">({record.pass_rate}%)</Text>
        </Space>
      ),
    },
    {
      title: '执行耗时',
      dataIndex: 'duration',
      key: 'duration',
      width: 120,
      render: (duration) => (
        <Text>
          <ClockCircleOutlined style={{ marginRight: 4 }} />
          {formatDuration(duration)}
        </Text>
      ),
    },
    {
      title: '触发方式',
      dataIndex: 'triggered_by',
      key: 'triggered_by',
      width: 100,
      render: (by) => {
        const map: Record<string, string> = { manual: '手动', schedule: '定时', ci: 'CI/CD' }
        return map[by] || by
      },
    },
    {
      title: '执行时间',
      dataIndex: 'created_at',
      key: 'created_at',
      width: 170,
      render: (time) => (time ? new Date(time).toLocaleString() : '-'),
    },
    {
      title: '操作',
      key: 'action',
      width: 170,
      render: (_, record) => (
        <Space>
          <Tooltip title="查看报告">
            <Button
              type="text"
              size="small"
              icon={<EyeOutlined style={{ color: '#1890ff' }} />}
              onClick={() => handleViewReport(record.id, record.test_object_name || `测试执行 #${record.id}`)}
            />
          </Tooltip>
          <Tooltip title="下载JSON">
            <Button type="text" size="small" icon={<DownloadOutlined />} onClick={() => handleExportJson(record.id)} />
          </Tooltip>
          <Popconfirm title="确定删除该记录吗？" onConfirm={() => handleDelete(record.id)}>
            <Tooltip title="删除">
              <Button type="text" size="small" danger icon={<DeleteOutlined />} />
            </Tooltip>
          </Popconfirm>
        </Space>
      ),
    },
  ]

  const moreMenuItems: MenuProps['items'] = [
    { key: 'download', icon: <DownloadOutlined />, label: '批量下载' },
    { type: 'divider' },
    { key: 'delete', icon: <DeleteOutlined />, label: '批量删除', danger: true },
  ]

  return (
    <div>
      <Title level={4} style={{ marginBottom: 24 }}>
        测试报告
      </Title>

      <Row gutter={16} style={{ marginBottom: 24 }}>
        <Col xs={24} sm={12} lg={6}>
          <Card>
            <Statistic title="执行总数" value={statistics.total_runs} prefix={<FileTextOutlined style={{ color: '#1890ff' }} />} />
          </Card>
        </Col>
        <Col xs={24} sm={12} lg={6}>
          <Card>
            <Statistic title="成功执行" value={statistics.success_runs} valueStyle={{ color: '#52c41a' }} prefix={<CheckCircleOutlined />} />
          </Card>
        </Col>
        <Col xs={24} sm={12} lg={6}>
          <Card>
            <Statistic title="失败执行" value={statistics.failed_runs} valueStyle={{ color: '#ff4d4f' }} prefix={<CloseCircleOutlined />} />
          </Card>
        </Col>
        <Col xs={24} sm={12} lg={6}>
          <Card>
            <Statistic title="成功率" value={statistics.success_rate} suffix="%" valueStyle={{ color: '#52c41a' }} />
          </Card>
        </Col>
      </Row>

      <Card title="测试趋势（近7天）" style={{ marginBottom: 24 }}>
        <ReactECharts option={trendOption} style={{ height: 250 }} />
      </Card>

      <Card
        title="执行记录"
        extra={
          <Space>
            <RangePicker size="small" />
            <Select
              placeholder="类型"
              size="small"
              style={{ width: 120 }}
              allowClear
              value={filters.test_type || undefined}
              onChange={(val) => setFilters((prev) => ({ ...prev, test_type: val || '' }))}
              options={[
                { value: 'api', label: 'API测试' },
                { value: 'web', label: 'Web测试' },
                { value: 'performance', label: '性能测试' },
              ]}
            />
            <Input
              placeholder="搜索..."
              prefix={<SearchOutlined />}
              size="small"
              style={{ width: 200 }}
              allowClear
              value={filters.keyword}
              onChange={(e) => setFilters((prev) => ({ ...prev, keyword: e.target.value }))}
            />
            <Dropdown
              menu={{
                items: moreMenuItems,
                onClick: ({ key }) => {
                  if (key === 'delete') {
                    handleBatchDelete()
                  } else if (key === 'download') {
                    handleBatchDownload()
                  }
                },
              }}
              disabled={selectedRowKeys.length === 0}
            >
              <Button size="small" icon={<MoreOutlined />}>
                更多
              </Button>
            </Dropdown>
          </Space>
        }
      >
        <Table
          rowSelection={{ selectedRowKeys, onChange: setSelectedRowKeys }}
          columns={columns}
          dataSource={testRuns.filter(
            (run) =>
              !filters.keyword ||
              run.test_object_name?.toLowerCase().includes(filters.keyword.toLowerCase()) ||
              run.environment_name?.toLowerCase().includes(filters.keyword.toLowerCase()),
          )}
          rowKey="id"
          loading={loading}
          pagination={{
            ...pagination,
            showTotal: (total) => `共 ${total} 条`,
            showSizeChanger: true,
            showQuickJumper: true,
            onChange: (page, pageSize) => setPagination((prev) => ({ ...prev, current: page, pageSize })),
          }}
        />
      </Card>

      <Modal
        title={currentReportTitle}
        open={htmlModalVisible}
        onCancel={() => setHtmlModalVisible(false)}
        width="90%"
        footer={[
          <Button key="close" onClick={() => setHtmlModalVisible(false)}>
            关闭
          </Button>,
        ]}
        style={{ top: 20 }}
      >
        <div
          style={{
            height: '70vh',
            overflow: 'auto',
            border: '1px solid #d9d9d9',
            borderRadius: 4,
          }}
          dangerouslySetInnerHTML={{ __html: reportHtml }}
        />
      </Modal>
    </div>
  )
}

export default Reports
