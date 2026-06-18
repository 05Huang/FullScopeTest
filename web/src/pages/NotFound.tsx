/**
 * 404 页面
 *
 * 访问不存在的路由时显示友好提示
 */
import { Button, Result } from 'antd'
import { useNavigate } from 'react-router-dom'
import { useTranslation } from 'react-i18next'

const NotFound = () => {
  const { t } = useTranslation()
  const navigate = useNavigate()

  return (
    <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: '100vh' }}>
      <Result
        status="404"
        title="404"
        subTitle={t('notFound.message') || '抱歉，您访问的页面不存在'}
        extra={
          <Button type="primary" onClick={() => navigate('/')}>
            {t('notFound.backHome') || '返回首页'}
          </Button>
        }
      />
    </div>
  )
}

export default NotFound
