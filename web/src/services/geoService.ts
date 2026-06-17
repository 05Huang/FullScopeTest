import api from './api'

interface GeoDetectResponse {
  country: string
  country_code: string
  timezone: string
  is_china: boolean
}

/**
 * 检测客户端所在地区（用于演示系统智能语言切换）
 */
export async function detectRegion(): Promise<GeoDetectResponse | null> {
  try {
    const res = await api.get('/geo/detect')
    const data = (res as any)?.data || res
    return data?.data || null
  } catch {
    return null
  }
}
