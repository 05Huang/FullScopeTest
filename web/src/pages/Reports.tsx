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
  type MenuProps,
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
  ArrowUpOutlined,
} from '@ant-design/icons'
import type { ColumnsType } from 'antd/es/table'
import ReactECharts from 'echarts-for-react'
import type { TestReport } from '@/services/reportService'
import { useTranslation } from 'react-i18next'
import { reportService } from '@/services'
import api from '@/services/api'
import { useProjectStore } from '@/stores/projectStore'

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

const Reports = () => {
  const { t } = useTranslation();
  const { currentProjectId } = useProjectStore();

  const typeConfig: Record<string, { color: string; text: string }> = {
    api: { color: 'blue', text: t('reports.apiTest') },
    web: { color: 'purple', text: t('reports.webTest') },
    performance: { color: 'orange', text: t('reports.perfTest') },
    perf: { color: 'orange', text: t('reports.perfTest') },
  }

  const statusConfig: Record<string, { color: string; text: string }> = {
    pending: { color: 'default', text: t('reports.pending') },
    running: { color: 'processing', text: t('reports.running') },
    success: { color: 'success', text: t('reports.success') },
    failed: { color: 'error', text: t('reports.failed') },
    cancelled: { color: 'warning', text: t('reports.cancelled') },
  }
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
  const [filters, setFilters] = useState({ keyword: '', test_type: '', date_range: null as [string, string] | null })

  useEffect(() => {
    fetchData()
  }, [currentProjectId, pagination.current, pagination.pageSize, filters.keyword, filters.test_type, filters.date_range])

  const fetchData = async () => {
    try {
      setLoading(true)
      const dateParams = filters.date_range ? {
        start_date: filters.date_range[0],
        end_date: filters.date_range[1],
      } : {}

      const [runsRes, reportsRes, statsRes] = await Promise.all([
        reportService.getTestRuns({
          page: pagination.current,
          per_page: pagination.pageSize,
          test_type: filters.test_type || undefined,
          project_id: currentProjectId,
          ...dateParams,
        }),
        reportService.getTestReports({
          page: pagination.current,
          per_page: pagination.pageSize,
          test_type: filters.test_type || undefined,
          project_id: currentProjectId,
          ...dateParams,
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
      message.error(t('reports.fetchDataFailed'))
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
      message.warning(t('reports.reportNotFound'))
      return
    }

    try {
      setCurrentReportTitle(title)
      const html = await reportService.getTestReportHtml(report.id)
      setReportHtml(html)
      setHtmlModalVisible(true)
    } catch (error) {
      message.error(t('reports.fetchReportFailed'))
      console.error(error)
    }
  }

  const handleExportJson = async (runId: number) => {
    const report = findReportByRunId(runId)
    if (!report) {
      message.warning(t('reports.reportNotFound'))
      return
    }

    try {
      await downloadReportJson(report.test_run_id, `${getReportName(report)}-${report.id}.json`)
      message.success(t('reports.downloadStarted'))
    } catch (error) {
      message.error(t('reports.downloadFailed'))
      console.error(error)
    }
  }

  /** 多格式导出：Excel / PDF / CSV */
  const handleExportFormat = async (runId: number, format: 'excel' | 'pdf' | 'csv') => {
    const report = findReportByRunId(runId)
    const baseName = report ? getReportName(report) : `test-run-${runId}`
    const dateStr = new Date().toISOString().slice(0, 10)
    const extMap = { excel: 'xlsx', pdf: 'pdf', csv: 'csv' }
    const filename = `${baseName}_${dateStr}.${extMap[format]}`

    try {
      let blob: Blob
      if (format === 'excel') {
        blob = await reportService.exportTestRunExcel(runId)
      } else if (format === 'pdf') {
        blob = await reportService.exportTestRunPdf(runId)
      } else {
        blob = await reportService.exportTestRunCsv(runId)
      }
      reportService.downloadFile(blob, filename)
      message.success(t('reports.downloadStarted'))
    } catch (error) {
      message.error(t('reports.downloadFailed'))
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
      message.success(t('reports.deleteSuccess'))
      setSelectedRowKeys((prev) => prev.filter((key) => key !== runId))
      fetchData()
    } catch (error) {
      message.error(t('reports.deleteFailed'))
      console.error(error)
    }
  }

  const handleBatchDelete = async () => {
    if (selectedRowKeys.length === 0) {
      message.warning(t('reports.selectToDelete'))
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
      message.success(t('reports.batchDeleteSuccess'))
      setSelectedRowKeys([])
      fetchData()
    } catch (error) {
      message.error(t('reports.batchDeleteFailed'))
      console.error(error)
    } finally {
      setLoading(false)
    }
  }

  const handleBatchDownload = async () => {
    if (selectedRowKeys.length === 0) {
      message.warning(t('reports.selectToDownload'))
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
      message.success(t('reports.downloadComplete'))
    } catch (error) {
      message.error(t('reports.batchDownloadFailed'))
      console.error(error)
    }
  }

  const trendOption = {
    tooltip: { trigger: 'axis' },
    legend: { data: [t('common.passed'), t('common.failed')] },
    grid: { left: '3%', right: '4%', bottom: '3%', containLabel: true },
    xAxis: {
      type: 'category',
      boundaryGap: true,
      data: dailyTrend.length > 0 ? dailyTrend.map((d) => d.date) : [],
    },
    yAxis: { type: 'value' },
    series: [
      {
        name: t('common.passed'),
        type: 'bar',
        stack: 'total',
        data: dailyTrend.length > 0 ? dailyTrend.map((d) => d.passed) : [],
        itemStyle: { color: '#52c41a' },
      },
      {
        name: t('common.failed'),
        type: 'bar',
        stack: 'total',
        data: dailyTrend.length > 0 ? dailyTrend.map((d) => d.failed) : [],
        itemStyle: { color: '#ff4d4f' },
      },
    ],
  }

  const formatDuration = (seconds?: number) => {
    if (!seconds) return '-'
    if (seconds < 60) return `${seconds.toFixed(1)}s`
    const minutes = Math.floor(seconds / 60)
    const secs = Math.round(seconds % 60)
    return `${minutes}m ${secs}s`
  }

  const columns: ColumnsType<TestRun> = [
    {
      title: t('reports.testName'),
      dataIndex: 'test_object_name',
      key: 'test_object_name',
      render: (text, record) => (
        <Space>
          <FileTextOutlined style={{ color: '#1890ff' }} />
          <Text strong>{text || `${t('reports.testRunPrefix')}${record.id}`}</Text>
        </Space>
      ),
    },
    {
      title: t('reports.type'),
      dataIndex: 'test_type',
      key: 'test_type',
      width: 100,
      render: (type) => <Tag color={typeConfig[type]?.color}>{typeConfig[type]?.text || type}</Tag>,
    },
    {
      title: t('reports.statusCol'),
      dataIndex: 'status',
      key: 'status',
      width: 100,
      render: (status) => <Tag color={statusConfig[status]?.color}>{statusConfig[status]?.text || status}</Tag>,
    },
    {
      title: t('reports.testResult'),
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
      title: t('reports.durationCol'),
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
      title: t('reports.triggeredBy'),
      dataIndex: 'triggered_by',
      key: 'triggered_by',
      width: 100,
      render: (by) => {
        const map: Record<string, string> = { manual: t('reports.manual'), schedule: t('reports.schedule'), ci: 'CI/CD' }
        return map[by] || by
      },
    },
    {
      title: t('reports.executionTime'),
      dataIndex: 'created_at',
      key: 'created_at',
      width: 170,
      render: (time) => (time ? new Date(time).toLocaleString() : '-'),
    },
    {
      title: t('reports.actionCol'),
      key: 'action',
      width: 170,
      render: (_, record) => (
        <Space>
          <Tooltip title={t("reports.viewReport")}>
            <Button
              type="text"
              size="small"
              icon={<EyeOutlined style={{ color: '#1890ff' }} />}
              onClick={() => handleViewReport(record.id, record.test_object_name || `测试执行 #${record.id}`)}
            />
          </Tooltip>
          <Dropdown
            menu={{
              items: [
                { key: 'json', label: 'JSON', onClick: () => handleExportJson(record.id) },
                { key: 'excel', label: 'Excel (.xlsx)', onClick: () => handleExportFormat(record.id, 'excel') },
                { key: 'pdf', label: 'PDF', onClick: () => handleExportFormat(record.id, 'pdf') },
                { key: 'csv', label: 'CSV', onClick: () => handleExportFormat(record.id, 'csv') },
              ],
            }}
            trigger={['click']}
          >
            <Tooltip title={t('reports.exportReport')}>
              <Button type="text" size="small" icon={<DownloadOutlined />} />
            </Tooltip>
          </Dropdown>
          <Popconfirm title={t('reports.confirmDeleteRecord')} onConfirm={() => handleDelete(record.id)}>
            <Tooltip title={t("common.delete")}>
              <Button type="text" size="small" danger icon={<DeleteOutlined />} />
            </Tooltip>
          </Popconfirm>
        </Space>
      ),
    },
  ]

  const moreMenuItems: MenuProps['items'] = [
    { key: 'download', icon: <DownloadOutlined />, label: t('reports.batchDownload') },
    { type: 'divider' },
    { key: 'delete', icon: <DeleteOutlined />, label: t('reports.batchDelete'), danger: true },
  ]

  return (
    <div className="fst-page">
      <div className="fst-page-header fst-animate-in">
        <h1 className="fst-page-title">{t("reports.title")}</h1>
      </div>

      <div className="fst-stat-row fst-animate-in fst-animate-in-1">
        <div className="fst-stat-card">
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
            <div>
              <div className="fst-stat-label">{t("reports.totalRuns")}</div>
              <div className="fst-stat-value">{statistics.total_runs}</div>
            </div>
            <div className="fst-stat-icon fst-stat-icon--info"><FileTextOutlined style={{ fontSize: 20 }} /></div>
          </div>
        </div>
        <div className="fst-stat-card">
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
            <div>
              <div className="fst-stat-label">{t("reports.successRuns")}</div>
              <div className="fst-stat-value">{statistics.success_runs}</div>
            </div>
            <div className="fst-stat-icon fst-stat-icon--primary"><CheckCircleOutlined style={{ fontSize: 20 }} /></div>
          </div>
          <div><span className="fst-stat-trend fst-stat-trend--up"><ArrowUpOutlined /> {statistics.success_rate}%</span></div>
        </div>
        <div className="fst-stat-card">
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
            <div>
              <div className="fst-stat-label">{t("reports.failedRuns")}</div>
              <div className="fst-stat-value">{statistics.failed_runs}</div>
            </div>
            <div className="fst-stat-icon" style={{ background: '#FDECEA', color: 'var(--fst-error)' }}><CloseCircleOutlined style={{ fontSize: 20 }} /></div>
          </div>
        </div>
        <div className="fst-stat-card">
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
            <div>
              <div className="fst-stat-label">{t("reports.successRate")}</div>
              <div className="fst-stat-value">{statistics.success_rate}%</div>
            </div>
            <div className="fst-stat-icon fst-stat-icon--secondary"><CheckCircleOutlined style={{ fontSize: 20 }} /></div>
          </div>
        </div>
      </div>

      <div className="fst-ios-card fst-animate-in fst-animate-in-2">
        <div className="fst-ios-card-header">
          <div className="fst-ios-card-title">{t("reports.trendTitle")}</div>
        </div>
        <ReactECharts option={trendOption} style={{ height: 250 }} />
      </div>

      <div className="fst-ios-card fst-animate-in fst-animate-in-3">
        <div className="fst-toolbar">
          <div className="fst-toolbar-left">
            <div className="fst-ios-card-title">{t("reports.executionRecords")}</div>
          </div>
          <div className="fst-toolbar-right">
            <RangePicker
              size="small"
              onChange={(dates) => {
                if (dates) {
                  setFilters((prev) => ({
                    ...prev,
                    date_range: [dates[0]!.format('YYYY-MM-DD'), dates[1]!.format('YYYY-MM-DD')]
                  }))
                } else {
                  setFilters((prev) => ({ ...prev, date_range: null }))
                }
              }}
            />
            <Select
              placeholder={t("reports.typePlaceholder")}
              size="small"
              style={{ width: 120 }}
              allowClear
              value={filters.test_type || undefined}
              onChange={(val) => setFilters((prev) => ({ ...prev, test_type: val || '' }))}
              options={[
                { value: 'api', label: t('reports.apiTest') },
                { value: 'web', label: t('reports.webTest') },
                { value: 'performance', label: t('reports.perfTest') },
              ]}
            />
            <Input
              placeholder={t("reports.searchPlaceholder")}
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
                  if (key === 'delete') handleBatchDelete()
                  else if (key === 'download') handleBatchDownload()
                },
              }}
              disabled={selectedRowKeys.length === 0}
            >
              <Button size="small" icon={<MoreOutlined />}>{t("reports.more")}</Button>
            </Dropdown>
          </div>
        </div>
        <div className="fst-table-wrap">
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
              showTotal: (total) => `${total} items`,
              showSizeChanger: true,
              showQuickJumper: true,
              onChange: (page, pageSize) => setPagination((prev) => ({ ...prev, current: page, pageSize })),
            }}
          />
        </div>
      </div>

      <Modal
        title={currentReportTitle}
        open={htmlModalVisible}
        onCancel={() => setHtmlModalVisible(false)}
        width="90%"
        footer={[
          <Button key="close" onClick={() => setHtmlModalVisible(false)}>{t("reports.close")}</Button>,
        ]}
        style={{ top: 20 }}
      >
        <div style={{ height: '70vh', overflow: 'auto', borderRadius: 12, border: '1px solid var(--fst-outline-soft)' }} dangerouslySetInnerHTML={{ __html: reportHtml }} />
      </Modal>
    </div>
  )
}

export default Reports
