import React, { useRef, useEffect, useState, useCallback } from 'react'
import { Card, Button, Space, Tag, Typography, Spin, message } from 'antd'
import { CheckOutlined, SwapOutlined } from '@ant-design/icons'
import api from '@/services/api'

const { Title } = Typography

interface VisualDiffViewerProps {
  baselineId?: number
  baselineImagePath?: string
  currentImagePath?: string
  diffPercentage?: number
  status?: string
  onClose?: () => void
  onApprove?: (baselineId: number) => void
}

const VisualDiffViewer: React.FC<VisualDiffViewerProps> = ({
  baselineId,
  baselineImagePath,
  currentImagePath,
  diffPercentage,
  status,
  onClose,
  onApprove,
}) => {
  const canvasRef = useRef<HTMLCanvasElement>(null)
  const [loading, setLoading] = useState(true)
  const [baselineImg, setBaselineImg] = useState<HTMLImageElement | null>(null)
  const [currentImg, setCurrentImg] = useState<HTMLImageElement | null>(null)
  const [viewMode, setViewMode] = useState<'side-by-side' | 'overlay' | 'diff'>('side-by-side')
  const [approving, setApproving] = useState(false)

  const loadImage = useCallback((url: string): Promise<HTMLImageElement> => {
    return new Promise((resolve, reject) => {
      const img = new Image()
      img.crossOrigin = 'anonymous'
      img.onload = () => resolve(img)
      img.onerror = () => reject(new Error(`Failed to load image: ${url}`))
      img.src = url
    })
  }, [])

  const generateDiffMask = useCallback((baseline: HTMLImageElement, current: HTMLImageElement): HTMLCanvasElement => {
    const canvas = document.createElement('canvas')
    canvas.width = baseline.width
    canvas.height = baseline.height
    const ctx = canvas.getContext('2d')!

    // Draw baseline
    ctx.drawImage(baseline, 0, 0)
    const baselineData = ctx.getImageData(0, 0, canvas.width, canvas.height)

    // Draw current
    ctx.drawImage(current, 0, 0)
    const currentData = ctx.getImageData(0, 0, canvas.width, canvas.height)

    // Create diff overlay
    ctx.clearRect(0, 0, canvas.width, canvas.height)
    ctx.drawImage(baseline, 0, 0)
    const overlay = ctx.createImageData(canvas.width, canvas.height)

    const threshold = 30
    let diffPixels = 0
    const totalPixels = baselineData.data.length / 4

    for (let i = 0; i < baselineData.data.length; i += 4) {
      const rDiff = Math.abs(baselineData.data[i] - currentData.data[i])
      const gDiff = Math.abs(baselineData.data[i + 1] - currentData.data[i + 1])
      const bDiff = Math.abs(baselineData.data[i + 2] - currentData.data[i + 2])

      if (rDiff > threshold || gDiff > threshold || bDiff > threshold) {
        overlay.data[i] = 255
        overlay.data[i + 1] = 0
        overlay.data[i + 2] = 0
        overlay.data[i + 3] = 128
        diffPixels++
      } else {
        overlay.data[i + 3] = 0
      }
    }

    ctx.putImageData(overlay, 0, 0)

    const diffPercentage = (diffPixels / totalPixels) * 100
    ctx.fillStyle = 'rgba(0, 0, 0, 0.7)'
    ctx.fillRect(0, canvas.height - 30, canvas.width, 30)
    ctx.fillStyle = '#fff'
    ctx.font = '14px sans-serif'
    ctx.fillText(`Diff: ${diffPercentage.toFixed(2)}% (${diffPixels} pixels)`, 10, canvas.height - 10)

    return canvas
  }, [])

  useEffect(() => {
    const loadAllImages = async () => {
      setLoading(true)
      try {
        const promises: Promise<void>[] = []

        if (baselineImagePath) {
          promises.push(
            loadImage(baselineImagePath)
              .then(img => setBaselineImg(img))
              .catch(() => setBaselineImg(null))
          )
        }

        if (currentImagePath) {
          promises.push(
            loadImage(currentImagePath)
              .then(img => setCurrentImg(img))
              .catch(() => setCurrentImg(null))
          )
        }


        await Promise.allSettled(promises)
      } catch (err) {
        message.error('Failed to load images')
      } finally {
        setLoading(false)
      }
    }

    loadAllImages()
  }, [baselineImagePath, currentImagePath, loadImage])

  useEffect(() => {
    const canvas = canvasRef.current
    if (!canvas || !baselineImg || !currentImg) return

    const ctx = canvas.getContext('2d')
    if (!ctx) return

    if (viewMode === 'side-by-side') {
      canvas.width = baselineImg.width + currentImg.width + 20
      canvas.height = Math.max(baselineImg.height, currentImg.height) + 40

      ctx.fillStyle = '#f0f0f0'
      ctx.fillRect(0, 0, canvas.width, canvas.height)

      ctx.fillStyle = '#333'
      ctx.font = 'bold 14px sans-serif'
      ctx.fillText('Baseline', 10, 20)
      ctx.drawImage(baselineImg, 10, 30)

      ctx.fillText('Current', baselineImg.width + 30, 20)
      ctx.drawImage(currentImg, baselineImg.width + 30, 30)
    } else if (viewMode === 'overlay') {
      canvas.width = baselineImg.width
      canvas.height = baselineImg.height

      ctx.globalAlpha = 0.5
      ctx.drawImage(baselineImg, 0, 0)
      ctx.globalAlpha = 0.5
      ctx.drawImage(currentImg, 0, 0)
      ctx.globalAlpha = 1.0
    } else if (viewMode === 'diff') {
      const diffCanvas = generateDiffMask(baselineImg, currentImg)
      canvas.width = diffCanvas.width
      canvas.height = diffCanvas.height
      ctx.drawImage(diffCanvas, 0, 0)
    }
  }, [viewMode, baselineImg, currentImg, generateDiffMask])

  const handleApprove = async () => {
    if (!baselineId) return
    setApproving(true)
    try {
      await api.post(`/api/v1/visual/baselines/${baselineId}/approve`)
      message.success('Baseline approved successfully')
      onApprove?.(baselineId)
    } catch (err) {
      message.error('Failed to approve baseline')
    } finally {
      setApproving(false)
    }
  }

  const statusColor = status === 'visual_pass' ? 'success' : status === 'visual_fail' ? 'error' : 'default'

  return (
    <Card
      title={
        <Space>
          <Title level={5} style={{ margin: 0 }}>Visual Diff Viewer</Title>
          {status && <Tag color={statusColor}>{status}</Tag>}
          {diffPercentage !== undefined && (
            <Tag color={diffPercentage > 5 ? 'error' : 'success'}>
              {diffPercentage.toFixed(2)}% diff
            </Tag>
          )}
        </Space>
      }
      extra={
        <Space>
          <Button
            size="small"
            icon={<SwapOutlined />}
            onClick={() => setViewMode(viewMode === 'side-by-side' ? 'overlay' : viewMode === 'overlay' ? 'diff' : 'side-by-side')}
          >
            {viewMode === 'side-by-side' ? 'Side by Side' : viewMode === 'overlay' ? 'Overlay' : 'Diff'}
          </Button>
          {baselineId && status === 'visual_fail' && (
            <Button
              type="primary"
              size="small"
              icon={<CheckOutlined />}
              onClick={handleApprove}
              loading={approving}
            >
              Approve as Baseline
            </Button>
          )}
          {onClose && (
            <Button size="small" onClick={onClose}>
              Close
            </Button>
          )}
        </Space>
      }
    >
      {loading ? (
        <div style={{ textAlign: 'center', padding: 40 }}>
          <Spin tip="Loading images..." />
        </div>
      ) : (
        <div style={{ textAlign: 'center' }}>
          <canvas
            ref={canvasRef}
            style={{
              maxWidth: '100%',
              border: '1px solid #d9d9d9',
              borderRadius: 4,
            }}
          />
        </div>
      )}
    </Card>
  )
}

export default VisualDiffViewer
