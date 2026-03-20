import React from 'react'
import ReactDOM from 'react-dom/client'
import { BrowserRouter } from 'react-router-dom'
import { ConfigProvider } from 'antd'
import zhCN from 'antd/locale/zh_CN'
import App from './App'
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

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <ConfigProvider locale={zhCN} theme={theme}>
      <BrowserRouter>
        <App />
      </BrowserRouter>
    </ConfigProvider>
  </React.StrictMode>,
)
