import api, { ApiResponse } from './api'

// ==================== 脚本管理 ====================

export const getScripts = (params?: {
  project_id?: number
  collection_id?: number
}): Promise<ApiResponse> => {
  return api.get('/web-test/scripts', { params }) as Promise<ApiResponse>
}

export const createScript = (data: {
  name: string
  description?: string
  collection_id?: number | null
  target_url?: string
  browser?: string
  script_content?: string
  config?: Record<string, any>
  project_id?: number
}): Promise<ApiResponse> => {
  return api.post('/web-test/scripts', data) as Promise<ApiResponse>
}

export const getScript = (id: number): Promise<ApiResponse> => {
  return api.get(`/web-test/scripts/${id}`) as Promise<ApiResponse>
}

export const updateScript = (id: number, data: {
  name?: string
  description?: string
  collection_id?: number | null
  target_url?: string
  browser?: string
  script_content?: string
  config?: Record<string, any>
}): Promise<ApiResponse> => {
  return api.put(`/web-test/scripts/${id}`, data) as Promise<ApiResponse>
}

export const deleteScript = (id: number): Promise<ApiResponse> => {
  return api.delete(`/web-test/scripts/${id}`) as Promise<ApiResponse>
}

// ==================== 用例集管理 ====================

export const getCollections = (projectId?: number): Promise<ApiResponse> => {
  return api.get('/web-test/collections', { params: { project_id: projectId } }) as Promise<ApiResponse>
}

export const createCollection = (data: {
  name: string
  description?: string
  project_id?: number
  sort_order?: number
}): Promise<ApiResponse> => {
  return api.post('/web-test/collections', data) as Promise<ApiResponse>
}

export const updateCollection = (id: number, data: {
  name?: string
  description?: string
  sort_order?: number
}): Promise<ApiResponse> => {
  return api.put(`/web-test/collections/${id}`, data) as Promise<ApiResponse>
}

export const deleteCollection = (id: number): Promise<ApiResponse> => {
  return api.delete(`/web-test/collections/${id}`) as Promise<ApiResponse>
}

export const runCollection = (collectionId: number): Promise<ApiResponse> => {
  return api.post(`/web-test/collections/${collectionId}/run`) as Promise<ApiResponse>
}

// ==================== 执行测试 ====================

export const runScript = (scriptId: number, headless?: boolean): Promise<ApiResponse> => {
  return api.post(`/web-test/scripts/${scriptId}/run`, { headless }) as Promise<ApiResponse>
}

// ==================== 录制功能 ====================

export const startRecording = (data: {
  url: string
  browser?: string
}): Promise<ApiResponse> => {
  return api.post('/web-test/record/start', data) as Promise<ApiResponse>
}

export const stopRecording = (): Promise<ApiResponse> => {
  return api.post('/web-test/record/stop') as Promise<ApiResponse>
}

export const getRecordingStatus = (): Promise<ApiResponse> => {
  return api.get('/web-test/record/status') as Promise<ApiResponse>
}

// ==================== AI ====================

export const generateScriptAI = (data: {
  prompt: string
  base_url?: string
  model?: string
  api_key?: string
  vision_base_url?: string
  vision_model?: string
  vision_api_key?: string
}): Promise<ApiResponse> => {
  return api.post('/web-test/ai/generate', data) as Promise<ApiResponse>
}

export const analyzeErrorAI = (data: {
  script_id: number
  error_log: string
  base_url?: string
  model?: string
  api_key?: string
  vision_base_url?: string
  vision_model?: string
  vision_api_key?: string
}): Promise<ApiResponse> => {
  return api.post('/web-test/ai/analyze-error', data) as Promise<ApiResponse>
}

export const exploreWebAppAI = (data: {
  start_url: string
  objective?: string
  max_steps?: number
  base_url?: string
  model?: string
  api_key?: string
  vision_base_url?: string
  vision_model?: string
  vision_api_key?: string
}): Promise<ApiResponse> => {
  return api.post('/web-test/ai/explore', data) as Promise<ApiResponse>
}

export const exploreWebAppAIStream = async (
  data: {
    start_url: string
    objective?: string
    max_steps?: number
    base_url?: string
    model?: string
    api_key?: string
    vision_base_url?: string
    vision_model?: string
    vision_api_key?: string
  },
  options: {
    token?: string | null
    onLog?: (line: string) => void
    onReport?: (report: any) => void
    onError?: (message: string) => void
    signal?: AbortSignal
  }
): Promise<void> => {
  const response = await fetch('/api/v1/web-test/ai/explore/stream', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      ...(options.token ? { Authorization: `Bearer ${options.token}` } : {}),
    },
    body: JSON.stringify(data),
    signal: options.signal,
  })

  if (!response.ok) {
    const text = await response.text()
    throw new Error(text || `HTTP ${response.status}`)
  }

  if (!response.body) {
    throw new Error('未获取到流式响应体')
  }

  const reader = response.body.getReader()
  const decoder = new TextDecoder('utf-8')
  let buffer = ''
  let finished = false

  const handleEventBlock = (block: string) => {
    const lines = block.split('\n')
    let eventName = 'message'
    const dataLines: string[] = []

    for (const line of lines) {
      if (line.startsWith('event:')) {
        eventName = line.slice(6).trim()
      } else if (line.startsWith('data:')) {
        dataLines.push(line.slice(5).trim())
      }
    }

    if (dataLines.length === 0) {
      return
    }

    const rawData = dataLines.join('\n')
    let payload: any = {}
    try {
      payload = JSON.parse(rawData)
    } catch {
      payload = { message: rawData }
    }

    if (eventName === 'log') {
      options.onLog?.(String(payload?.line || ''))
      return
    }
    if (eventName === 'report') {
      options.onReport?.(payload)
      return
    }
    if (eventName === 'error') {
      options.onError?.(String(payload?.message || '探索任务失败'))
      return
    }
    if (eventName === 'done') {
      finished = true
    }
  }

  while (!finished) {
    const { done, value } = await reader.read()
    if (done) {
      break
    }
    buffer += decoder.decode(value, { stream: true })

    let boundary = buffer.indexOf('\n\n')
    while (boundary !== -1) {
      const block = buffer.slice(0, boundary).trim()
      buffer = buffer.slice(boundary + 2)
      if (block) {
        handleEventBlock(block)
      }
      boundary = buffer.indexOf('\n\n')
    }
  }
}

// 导出服务对象
export const webTestService = {
  getScripts,
  createScript,
  getScript,
  updateScript,
  deleteScript,
  getCollections,
  createCollection,
  updateCollection,
  deleteCollection,
  runCollection,
  runScript,
  startRecording,
  stopRecording,
  getRecordingStatus,
  generateScriptAI,
  analyzeErrorAI,
  exploreWebAppAI,
  exploreWebAppAIStream,
}
