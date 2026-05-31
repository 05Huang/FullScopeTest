import React from 'react'
import ReactDOM from 'react-dom/client'
import { BrowserRouter } from 'react-router-dom'
import { ConfigProvider } from 'antd'
import zhCN from 'antd/locale/zh_CN'
import enUS from 'antd/locale/en_US'
import { useTranslation } from 'react-i18next'
import App from './App'
import './i18n'
import './styles/index.css'

// Ant Design 主题配置
const theme = {
  token: {
    colorPrimary: '#3D6E66',
    colorInfo: '#3D6E66',
    borderRadius: 8,
    colorSuccess: '#2F8F6B',
    colorWarning: '#D7B56D',
    colorError: '#D24C3F',
  },
}

const AppWithLocale = () => {
  const { i18n } = useTranslation()
  const locale = i18n.language === 'en' ? enUS : zhCN

  return (
    <ConfigProvider locale={locale} theme={theme}>
      <BrowserRouter>
        <App />
      </BrowserRouter>
    </ConfigProvider>
  )
}

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <AppWithLocale />
  </React.StrictMode>,
)
