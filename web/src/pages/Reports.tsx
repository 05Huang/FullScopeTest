import { useState, useEffect } from 'react'
import {
  Card,
  Table,
  Button,
  Space,
  Input,
  Tag,
  Typography,
  Dropdown,
  Tooltip,
  Row,
  Col,
  Statistic,
  DatePicker,
  Select,
  message,
  Popconfirm,
  Tabs,
} from 'antd'
import {
  SearchOutlined,
  DownloadOutlined,
  EyeOutlined,
  DeleteOutlined,
  MoreOutlined,
  CheckCircleOutlined,
  CloseCircleOutlined,
  ClockCircleOutlined,
  FileTextOutlined,
} from '@ant-design/icons'
import type { ColumnsType } from 'antd/es/table'
import type { MenuProps } from 'antd'
import ReactECharts from 'echarts-for-react'
import { reportService } from '@/services'
import TestReports from './TestReports'

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
  const [statistics, setStatistics] = useState({
    total_runs: 0,
    success_runs: 0,
    failed_runs: 0,
    success_rate: 0
  })
  const [dailyTrend, setDailyTrend] = useState<any[]>([])
  const [pagination, setPagination] = useState({ current: 1, pageSize: 10, total: 0 })
  const [filters, setFilters] = useState({ test_type: '', keyword: '' })

  useEffect(() => {
    fetchData()
  }, [pagination.current, pagination.pageSize, filters.test_type])

  const fetchData = async () => {
    setLoading(true)
    try {
      // 获取测试运行记录
      const runsRes = await reportService.getTestRuns({
        page: pagination.current,
        per_page: pagination.pageSize,
        test_type: filters.test_type || undefined,
      })
      
      if (runsRes.code === 200) {
        setTestRuns(runsRes.data.items || [])
        setPagination(prev => ({ ...prev, total: runsRes.data.total || 0 }))
      }

      // 获取统计数据
      const statsRes = await reportService.getReportStatistics({ days: 7 })
      if (statsRes.code === 200) {
        setStatistics(statsRes.data.summary)
        setDailyTrend(statsRes.data.daily_trend || [])
      }
    } catch (error) {
      message.error('获取数据失败')
    } finally {
      setLoading(false)
    }
  }

  // 删除记录
  const handleDelete = async (id: number) => {
    try {
      const res = await reportService.deleteTestRun(id)
      if (res.code === 200) {
        message.success('删除成功')
        fetchData()
      }
    } catch (error) {
      message.error('删除失败')
    }
  }

  // 批量删除
  const handleBatchDelete = async () => {
    if (selectedRowKeys.length === 0) return
    try {
      for (const id of selectedRowKeys) {
        await reportService.deleteTestRun(id as number)
      }
      message.success('批量删除成功')
      setSelectedRowKeys([])
      fetchData()
    } catch (error) {
      message.error('删除失败')
    }
  }

  // 批量下载
  const handleBatchDownload = () => {
    if (selectedRowKeys.length === 0) return
    for (const id of selectedRowKeys) {
      handleExport(id as number, 'json')
    }
    message.success('已开始下载')
  }

  // 导出报告
  const handleExport = (id: number, format: 'json' | 'html') => {
    const url = reportService.getReportExportUrl(id, format)
    window.open(url, '_blank')
  }

  // 趋势图配置
  const trendOption = {
    tooltip: {
      trigger: 'axis',
    },
    legend: {
      data: ['通过', '失败'],
      bottom: 0,
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '15%',
      top: '10%',
      containLabel: true,
    },
    xAxis: {
      type: 'category',
      data: dailyTrend.length > 0 ? dailyTrend.map(d => d.date) : [],
    },
    yAxis: {
      type: 'value',
    },
    series: [
      {
        name: '通过',
        type: 'bar',
        stack: 'total',
        data: dailyTrend.length > 0 ? dailyTrend.map(d => d.passed) : [],
        itemStyle: { color: '#52c41a' },
      },
      {
        name: '失败',
        type: 'bar',
        stack: 'total',
        data: dailyTrend.length > 0 ? dailyTrend.map(d => d.failed) : [],
        itemStyle: { color: '#ff4d4f' },
      },
    ],
  }

  // 格式化时长
  const formatDuration = (seconds?: number) => {
    if (!seconds) return '-'
    if (seconds < 60) return `${seconds.toFixed(1)}秒`
    const minutes = Math.floor(seconds / 60)
    const secs = Math.round(seconds % 60)
    return `${minutes}分${secs}秒`
  }

  // 表格列配置
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
      render: (type) => (
        <Tag color={typeConfig[type]?.color}>{typeConfig[type]?.text || type}</Tag>
      ),
    },
    {
      title: '状态',
      dataIndex: 'status',
      key: 'status',
      width: 100,
      render: (status) => (
        <Tag color={statusConfig[status]?.color}>{statusConfig[status]?.text || status}</Tag>
      ),
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
          <Text type="secondary">
            ({record.pass_rate}%)
          </Text>
        </Space>
      ),
    },
    {
      title: '执行耗时',
      dataIndex: 'duration',
      key: 'duration',
      width: 100,
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
      }
    },
    {
      title: '执行时间',
      dataIndex: 'created_at',
      key: 'created_at',
      width: 160,
      render: (time) => time ? new Date(time).toLocaleString() : '-'
    },
    {
      title: '操作',
      key: 'action',
      width: 150,
      render: (_, record) => (
        <Space>
          <Tooltip title="查看报告">
            <Button
              type="text"
              size="small"
              icon={<EyeOutlined style={{ color: '#1890ff' }} />}
              onClick={() => handleExport(record.id, 'html')}
            />
          </Tooltip>
          <Tooltip title="下载JSON">
            <Button
              type="text"
              size="small"
              icon={<DownloadOutlined />}
              onClick={() => handleExport(record.id, 'json')}
            />
          </Tooltip>
          <Popconfirm
            title="确定删除该记录吗？"
            onConfirm={() => handleDelete(record.id)}
          >
            <Tooltip title="删除">
              <Button
                type="text"
                size="small"
                danger
                icon={<DeleteOutlined />}
              />
            </Tooltip>
          </Popconfirm>
        </Space>
      ),
    },
  ]

  // 更多操作菜单
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

      <Tabs
        defaultActiveKey="runs"
        items={[
          {
            key: 'runs',
            label: '执行记录',
            children: (
              <>
                {/* 统计卡片 */}
                <Row gutter={16} style={{ marginBottom: 24 }}>
                  <Col xs={24} sm={12} lg={6}>
                    <Card>
                      <Statistic
                        title="执行总数"
                        value={statistics.total_runs}
                        prefix={<FileTextOutlined style={{ color: '#1890ff' }} />}
                      />
                    </Card>
                  </Col>
                  <Col xs={24} sm={12} lg={6}>
                    <Card>
                      <Statistic
                        title="成功执行"
                        value={statistics.success_runs}
                        valueStyle={{ color: '#52c41a' }}
                        prefix={<CheckCircleOutlined />}
                      />
                    </Card>
                  </Col>
                  <Col xs={24} sm={12} lg={6}>
                    <Card>
                      <Statistic
                        title="失败执行"
                        value={statistics.failed_runs}
                        valueStyle={{ color: '#ff4d4f' }}
                        prefix={<CloseCircleOutlined />}
                      />
                    </Card>
                  </Col>
                  <Col xs={24} sm={12} lg={6}>
                    <Card>
                      <Statistic
                        title="成功率"
                        value={statistics.success_rate}
                        suffix="%"
                        valueStyle={{ color: '#52c41a' }}
                      />
                    </Card>
                  </Col>
                </Row>

                {/* 趋势图 */}
                <Card title="测试趋势（近7天）" style={{ marginBottom: 24 }}>
                  <ReactECharts option={trendOption} style={{ height: 250 }} />
                </Card>

                {/* 报告列表 */}
                <Card
                  title="执行记录"
                  extra={
                    <Space>
                      <RangePicker size="small" />
                      <Select
                        placeholder="类型"
                        size="small"
                        style={{ width: 100 }}
                        allowClear
                        value={filters.test_type || undefined}
                        onChange={(val) => setFilters(prev => ({ ...prev, test_type: val || '' }))}
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
                        onChange={(e) => setFilters(prev => ({ ...prev, keyword: e.target.value }))}
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
                          }
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
                    rowSelection={{
                      selectedRowKeys,
                      onChange: setSelectedRowKeys,
                    }}
                    columns={columns}
                    dataSource={testRuns.filter(run =>
                      !filters.keyword || 
                      run.test_object_name?.toLowerCase().includes(filters.keyword.toLowerCase()) ||
                      run.environment_name?.toLowerCase().includes(filters.keyword.toLowerCase())
                    )}
                    rowKey="id"
                    loading={loading}
                    pagination={{
                      ...pagination,
                      showTotal: (total) => `共 ${total} 条`,
                      showSizeChanger: true,
                      showQuickJumper: true,
                      onChange: (page, pageSize) => setPagination(prev => ({ ...prev, current: page, pageSize })),
                    }}
                  />
                </Card>
              </>
            ),
          },
          {
            key: 'reports',
            label: '测试报告',
            children: <TestReports />,
          },
        ]}
      />
    </div>
  )
}

export default Reports
