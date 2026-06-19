/**
 * 页面级 Tour 引导配置
 *
 * 为各核心工作页面提供 Tour 步骤配置，用于新手引导。
 * 使用方式：在页面组件中调用 usePageTour(steps) 获取 Tour 状态。
 */
import { useState, useEffect, useCallback } from 'react'
import type { TourProps } from 'antd'

interface PageTourConfig {
  /** Tour 唯一标识，用于 localStorage 存储 */
  key: string
  /** Tour 步骤 */
  steps: TourProps['steps']
  /** 是否在首次访问时自动触发 */
  autoStart?: boolean
}

/**
 * 页面级 Tour Hook
 *
 * 提供 Tour 状态管理、首次访问自动触发、"重新触发"支持。
 */
export function usePageTour(config: PageTourConfig) {
  const [open, setOpen] = useState(false)
  const storageKey = `fst_page_toured_${config.key}`

  // 首次访问自动触发
  useEffect(() => {
    if (config.autoStart !== false) {
      const hasToured = localStorage.getItem(storageKey)
      if (!hasToured) {
        const timer = setTimeout(() => setOpen(true), 500)
        return () => clearTimeout(timer)
      }
    }
  }, [config.autoStart, storageKey])

  const handleClose = useCallback(() => {
    setOpen(false)
    localStorage.setItem(storageKey, 'true')
  }, [storageKey])

  const startTour = useCallback(() => {
    setOpen(true)
  }, [])

  const resetTour = useCallback(() => {
    localStorage.removeItem(storageKey)
  }, [storageKey])

  return { open, handleClose, startTour, resetTour }
}

// ==================== 预定义 Tour 配置 ====================

/** API 测试工作台 Tour */
export const apiWorkspaceTour: TourProps['steps'] = [
  {
    title: '🧪 接口测试工作台',
    description: '这里是你的核心工作区。左侧是请求编辑器，右侧是响应查看器。',
    target: () => document.querySelector('[class*="ApiTestWorkspace"]') as HTMLElement,
  },
  {
    title: '📝 请求编辑',
    description: '选择 HTTP 方法（GET/POST/PUT/DELETE），输入 URL，配置 Headers 和 Body。',
    target: () => document.querySelector('[data-tour-id="request-method"]') as HTMLElement,
  },
  {
    title: '✅ 断言配置',
    description: '切换到「断言」Tab 可以配置可视化断言规则，无需编写代码。',
    target: () => document.querySelector('[data-tour-id="assertion-tab"]') as HTMLElement,
  },
  {
    title: '💾 保存用例',
    description: '点击「保存」将请求保存为测试用例，方便后续复用和批量执行。',
    target: () => document.querySelector('[data-tour-id="save-case"]') as HTMLElement,
  },
]

/** 集合管理 Tour */
export const collectionsTour: TourProps['steps'] = [
  {
    title: '📁 测试集合',
    description: '集合是用例的分组单元。每个集合可以包含多个测试用例。',
    target: () => document.querySelector('[class*="ApiTestCollections"]') as HTMLElement,
  },
  {
    title: '▶️ 执行集合',
    description: '点击集合的「执行」按钮，将按顺序运行集合中的所有用例。',
    target: () => document.querySelector('[data-tour-id="run-collection"]') as HTMLElement,
  },
]

/** 环境管理 Tour */
export const environmentsTour: TourProps['steps'] = [
  {
    title: '🌍 环境管理',
    description: '环境变量用于存储不同环境（开发/测试/生产）的配置，如 base_url、token 等。',
    target: () => document.querySelector('[class*="ApiTestEnvironments"]') as HTMLElement,
  },
  {
    title: '🔗 变量引用',
    description: '在请求中使用 {{variable_name}} 引用环境变量，执行时自动替换为实际值。',
    target: () => document.querySelector('[data-tour-id="env-variable"]') as HTMLElement,
  },
]
