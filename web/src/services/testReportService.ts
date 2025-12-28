import api, { ApiResponse } from './api'

// ==================== 测试报告 ====================

export const getTestReports = (params?: {
  project_id?: number
  test_type?: string
  page?: number
  per_page?: number
}): Promise<ApiResponse> => {
  return api.get('/test-reports', { params }) as Promise<ApiResponse>
}

export const getTestReport = (reportId: number): Promise<ApiResponse> => {
  return api.get(`/test-reports/${reportId}`) as Promise<ApiResponse>
}

export const getTestReportHtml = (reportId: number): Promise<string> => {
  return api.get(`/test-reports/${reportId}/html`, {
    responseType: 'text',
    headers: {
      'Accept': 'text/html'
    }
  }).then((res: any) => {
    // 响应拦截器现在返回完整的 response 对象
    return res.data || res
  }) as Promise<string>
}

export const deleteTestReport = (reportId: number): Promise<ApiResponse> => {
  return api.delete(`/test-reports/${reportId}`) as Promise<ApiResponse>
}

// 导出服务对象
export const testReportService = {
  getTestReports,
  getTestReport,
  getTestReportHtml,
  deleteTestReport
}

export default testReportService
