import { useTranslation } from 'react-i18next'
import { useGeoLanguage } from '@/hooks/useGeoLanguage'

/**
 * 演示系统语言切换提示组件
 *
 * 当检测到用户来自非中国地区时，弹出提示询问是否切换为英文。
 * 样式使用内联，不依赖额外 CSS 文件。
 */
export default function LanguageSwitchPrompt() {
  const { t } = useTranslation()
  const { showPrompt, loading, switchToEnglish, dismiss } = useGeoLanguage()

  if (loading || !showPrompt) return null

  return (
    <div
      style={{
        position: 'fixed',
        top: 0,
        left: 0,
        right: 0,
        bottom: 0,
        zIndex: 99999,
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        background: 'rgba(0, 0, 0, 0.3)',
        backdropFilter: 'blur(4px)',
        WebkitBackdropFilter: 'blur(4px)',
        animation: 'fst-fade-in 300ms ease both',
      }}
      onClick={dismiss}
    >
      <div
        style={{
          background: '#fff',
          borderRadius: '20px',
          padding: '32px 36px',
          maxWidth: '400px',
          width: '90%',
          boxShadow: '0 24px 80px rgba(0, 0, 0, 0.15)',
          textAlign: 'center',
          animation: 'fst-fade-in 300ms ease both',
        }}
        onClick={(e) => e.stopPropagation()}
      >
        {/* Globe Icon */}
        <div style={{
          width: 56,
          height: 56,
          borderRadius: '50%',
          background: 'linear-gradient(135deg, #5FA59B 0%, #3D6E66 100%)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          margin: '0 auto 16px',
        }}>
          <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="white" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
            <circle cx="12" cy="12" r="10" />
            <path d="M2 12h20" />
            <path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z" />
          </svg>
        </div>

        <h3 style={{
          fontSize: 18,
          fontWeight: 700,
          color: '#1a2b2a',
          margin: '0 0 8px',
        }}>
          {t('geo.title', 'Switch to English?')}
        </h3>

        <p style={{
          fontSize: 14,
          color: '#666',
          margin: '0 0 24px',
          lineHeight: 1.6,
        }}>
          {t('geo.description', 'We detected you might prefer English. Would you like to switch the interface language?')}
        </p>

        <div style={{ display: 'flex', gap: 12 }}>
          <button
            onClick={dismiss}
            style={{
              flex: 1,
              padding: '10px 0',
              borderRadius: 12,
              border: '1px solid #e0e0e0',
              background: '#fff',
              color: '#666',
              fontSize: 14,
              fontWeight: 600,
              cursor: 'pointer',
              transition: 'all 150ms ease',
            }}
            onMouseEnter={(e) => {
              e.currentTarget.style.background = '#f5f5f5'
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.background = '#fff'
            }}
          >
            {t('geo.keepChinese', '保持中文')}
          </button>

          <button
            onClick={switchToEnglish}
            style={{
              flex: 1,
              padding: '10px 0',
              borderRadius: 12,
              border: 'none',
              background: 'linear-gradient(135deg, #5FA59B 0%, #3D6E66 100%)',
              color: '#fff',
              fontSize: 14,
              fontWeight: 600,
              cursor: 'pointer',
              boxShadow: '0 4px 16px rgba(61, 110, 102, 0.25)',
              transition: 'all 150ms ease',
            }}
            onMouseEnter={(e) => {
              e.currentTarget.style.transform = 'translateY(-1px)'
              e.currentTarget.style.boxShadow = '0 6px 24px rgba(61, 110, 102, 0.35)'
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.transform = 'translateY(0)'
              e.currentTarget.style.boxShadow = '0 4px 16px rgba(61, 110, 102, 0.25)'
            }}
          >
            {t('geo.switchEnglish', 'Switch to English')}
          </button>
        </div>
      </div>
    </div>
  )
}
