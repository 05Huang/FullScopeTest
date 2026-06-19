/**
 * SSO 回调处理页面
 *
 * 处理 OIDC 授权码回调，用授权码换取 Token 后跳转到 Dashboard。
 */
import { useEffect, useState } from 'react'
import { useNavigate, useSearchParams } from 'react-router-dom'
import { Spin, Result, Button } from 'antd'
import { useTranslation } from 'react-i18next'
import api from '@/services/api'
import { useAuthStore } from '@/stores/authStore'

const SSOCallback = () => {
  const { t } = useTranslation()
  const navigate = useNavigate()
  const [searchParams] = useSearchParams()
  const { setAuth } = useAuthStore()
  const [status, setStatus] = useState<'loading' | 'success' | 'error'>('loading')
  const [errorMsg, setErrorMsg] = useState('')

  useEffect(() => {
    const code = searchParams.get('code')
    const error = searchParams.get('error')

    if (error) {
      setStatus('error')
      setErrorMsg(searchParams.get('error_description') || t('login.sso.error'))
      return
    }

    if (!code) {
      setStatus('error')
      setErrorMsg(t('login.sso.missingCode'))
      return
    }

    const handleCallback = async () => {
      try {
        const redirectUri = `${window.location.origin}/sso/callback`
        // 从 sessionStorage 获取 state 用于 CSRF 校验
        const state = sessionStorage.getItem('oidc_state')
        const res = await api.post('/auth/sso/oidc/callback', {
          code,
          state,
          redirect_uri: redirectUri,
        })
        // 校验完成后清除 state
        sessionStorage.removeItem('oidc_state')

        const data = (res as any)?.data || res
        if (data?.user) {
          setAuth(data.user)
          setStatus('success')
          setTimeout(() => navigate('/dashboard'), 1000)
        } else {
          setStatus('error')
          setErrorMsg(t('login.sso.error'))
        }
      } catch (err: any) {
        setStatus('error')
        setErrorMsg(err?.response?.data?.message || t('login.sso.error'))
      }
    }

    handleCallback()
  }, [searchParams, navigate, setAuth, t])

  if (status === 'loading') {
    return (
      <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: '100vh' }}>
        <Spin size="large" tip={t('login.sso.processing')} />
      </div>
    )
  }

  if (status === 'error') {
    return (
      <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: '100vh' }}>
        <Result
          status="error"
          title={t('login.sso.failed')}
          subTitle={errorMsg}
          extra={
            <Button type="primary" onClick={() => navigate('/login')}>
              {t('login.goLogin')}
            </Button>
          }
        />
      </div>
    )
  }

  return (
    <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: '100vh' }}>
      <Result
        status="success"
        title={t('login.sso.success')}
        subTitle={t('login.sso.redirecting')}
      />
    </div>
  )
}

export default SSOCallback
