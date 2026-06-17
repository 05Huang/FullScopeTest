import React, { useState, useEffect } from 'react'
import { Card, Form, Input, Button, message, Typography, Row, Col, Space, Avatar, Upload, Spin, type UploadProps } from 'antd'
import { UserOutlined, MailOutlined, SaveOutlined, LockOutlined, UploadOutlined } from '@ant-design/icons'
import { authService } from '@/services/authService'
import { useTranslation } from 'react-i18next'
import { useAuthStore } from '@/stores/authStore'

const { Title, Text } = Typography

const Profile: React.FC = () => {
  const { t } = useTranslation();
  const { user, updateUser } = useAuthStore()
  const [profileForm] = Form.useForm()
  const [passwordForm] = Form.useForm()
  const [loading, setLoading] = useState(false)
  const [pwdLoading, setPwdLoading] = useState(false)
  const [uploading, setUploading] = useState(false)
  const isProduction = (import.meta as any).env?.MODE === 'production' || (import.meta as any).env?.VITE_DEPLOY_ENV === 'prod'

  useEffect(() => {
    if (user) {
      profileForm.setFieldsValue({
        username: user.username,
        email: user.email,
        avatar: user.avatar,
      })
    }
  }, [user, profileForm])

  const handleUploadAvatar: UploadProps['customRequest'] = async (options) => {
    const { file, onSuccess, onError } = options
    setUploading(true)
    try {
      const res = await authService.uploadAvatar(file as File)
      if (res.code === 200 && res.data?.avatar) {
        message.success(t('profile.avatarUploadSuccess'))
        profileForm.setFieldsValue({ avatar: res.data.avatar })
        updateUser({ avatar: res.data.avatar })
        onSuccess?.('ok')
      } else {
        message.error(res.message || t('profile.uploadFailed'))
        onError?.(new Error(res.message || t('profile.uploadFailed')))
      }
    } catch (error: any) {
      message.error(error.message || t('profile.uploadFailed'))
      onError?.(error)
    } finally {
      setUploading(false)
    }
  }

  const handleUpdateProfile = async (values: any) => {
    setLoading(true)
    try {
      const res = await authService.updateProfile(values)
      if (res.code === 200) {
        message.success(t('profile.profileUpdateSuccess'))
        // Update user context
        updateUser(res.data)
      } else {
        message.error(res.message || t('profile.updateFailed'))
      }
    } catch (error: any) {
      message.error(error.message || t('profile.updateFailed'))
    } finally {
      setLoading(false)
    }
  }

  const handleUpdatePassword = async (values: any) => {
    if (values.new_password !== values.confirm_password) {
      message.error(t('profile.passwordMismatch'))
      return
    }
    setPwdLoading(true)
    try {
      const res = await authService.changePassword(values.old_password, values.new_password)
      if (res.code === 200) {
        message.success(t('profile.passwordChangeSuccess'))
        passwordForm.resetFields()
      } else {
        message.error(res.message || t('profile.changeFailed'))
      }
    } catch (error: any) {
      message.error(error.message || t('profile.changeFailed'))
    } finally {
      setPwdLoading(false)
    }
  }

  return (
    <div className="fst-page" style={{ maxWidth: 800, margin: '0 auto' }}>
      <div className="fst-page-header fst-animate-in">
        <div>
          <h1 className="fst-page-title">{t('profile.title')}</h1>
          <div className="fst-ios-card-subtitle">{t('profile.subtitle')}</div>
        </div>
      </div>

      {/* Profile Card */}
      <div className="fst-ios-card fst-animate-in fst-animate-in-1">
        <div className="fst-ios-card-header">
          <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
            <div className="fst-stat-icon fst-stat-icon--primary"><UserOutlined style={{ fontSize: 18 }} /></div>
            <div>
              <div className="fst-ios-card-title">{t('profile.basicInfoTitle')}</div>
              <div className="fst-ios-card-subtitle">{t('profile.basicInfoSubtitle')}</div>
            </div>
          </div>
        </div>

        <Form form={profileForm} layout="vertical" onFinish={handleUpdateProfile}>
          <div style={{ textAlign: 'center', marginBottom: 24 }}>
            <Spin spinning={uploading}>
              <Upload name="file" showUploadList={false} customRequest={handleUploadAvatar} accept="image/*">
                <div style={{ cursor: 'pointer', position: 'relative', display: 'inline-block' }}>
                  <Avatar
                    size={88}
                    icon={<UserOutlined />}
                    src={user?.avatar}
                    style={{ backgroundColor: 'var(--fst-primary)', border: '3px solid var(--fst-surface-card)', boxShadow: 'var(--fst-shadow-md)' }}
                  />
                  <div style={{
                    position: 'absolute', bottom: 0, right: -4,
                    width: 28, height: 28, borderRadius: '50%',
                    background: 'var(--fst-primary)', color: '#fff',
                    display: 'grid', placeItems: 'center',
                    boxShadow: 'var(--fst-shadow-sm)',
                  }}>
                    <UploadOutlined style={{ fontSize: 12 }} />
                  </div>
                </div>
              </Upload>
            </Spin>
            <div style={{ marginTop: 12, fontSize: 13, color: 'var(--fst-on-surface-muted)' }}>
              {t('profile.avatarUploadHint')}
            </div>
          </div>

          <Row gutter={24}>
            <Col span={12}>
              <Form.Item
                label={<span style={{ fontWeight: 600, fontSize: 13 }}>{t('profile.usernameLabel')}</span>}
                name="username"
                rules={[{ required: true, message: t('profile.usernameRequired') }, { min: 3, max: 50 }]}
              >
                <Input prefix={<UserOutlined />} placeholder={t("profile.usernamePlaceholder")} />
              </Form.Item>
            </Col>
            <Col span={12}>
              <Form.Item
                label={<span style={{ fontWeight: 600, fontSize: 13 }}>{t('profile.emailLabel')}</span>}
                name="email"
                rules={[{ required: true, message: t('profile.emailRequired') }, { type: 'email' }]}
              >
                <Input prefix={<MailOutlined />} placeholder={t("profile.emailPlaceholder")} />
              </Form.Item>
            </Col>
            <Col span={24}>
              <Form.Item label={<span style={{ fontWeight: 600, fontSize: 13 }}>{t('profile.avatarUrlLabel')}</span>} name="avatar">
                <Input placeholder={t("profile.avatarUrlPlaceholder")} />
              </Form.Item>
            </Col>
          </Row>

          <div style={{ borderTop: '1px solid var(--fst-outline-soft)', paddingTop: 20 }}>
            <Form.Item style={{ marginBottom: 0 }}>
              <Button type="primary" htmlType="submit" icon={<SaveOutlined />} loading={loading}>{t('profile.saveBasicInfo')}</Button>
            </Form.Item>
          </div>
        </Form>
      </div>

      {/* Password Card — hidden in production/demo to prevent guest users from changing shared passwords */}
      {!isProduction && (
      <div className="fst-ios-card fst-animate-in fst-animate-in-2">
        <div className="fst-ios-card-header">
          <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
            <div className="fst-stat-icon fst-stat-icon--tertiary"><LockOutlined style={{ fontSize: 18 }} /></div>
            <div>
              <div className="fst-ios-card-title">{t('profile.passwordTitle')}</div>
              <div className="fst-ios-card-subtitle">{t('profile.passwordSubtitle')}</div>
            </div>
          </div>
        </div>

        <Form form={passwordForm} layout="vertical" onFinish={handleUpdatePassword}>
          <Form.Item
            label={<span style={{ fontWeight: 600, fontSize: 13 }}>{t('common.password')}</span>}
            name="old_password"
            rules={[{ required: true, message: t('profile.currentPasswordRequired') }]}
          >
            <Input.Password placeholder={t("profile.currentPasswordPlaceholder")} />
          </Form.Item>
          <Form.Item
            label={<span style={{ fontWeight: 600, fontSize: 13 }}>{t('profile.newPassword')}</span>}
            name="new_password"
            rules={[{ required: true, message: t('profile.newPasswordRequired') }, { min: 6 }]}
          >
            <Input.Password placeholder={t("profile.newPasswordPlaceholder")} />
          </Form.Item>
          <Form.Item
            label={<span style={{ fontWeight: 600, fontSize: 13 }}>{t('profile.confirmPasswordLabel')}</span>}
            name="confirm_password"
            rules={[{ required: true, message: t('profile.confirmPasswordRequired') }]}
          >
            <Input.Password placeholder={t("profile.confirmPasswordPlaceholder")} />
          </Form.Item>
          <div style={{ borderTop: '1px solid var(--fst-outline-soft)', paddingTop: 20 }}>
            <Form.Item style={{ marginBottom: 0 }}>
              <Button type="primary" htmlType="submit" icon={<SaveOutlined />} loading={pwdLoading}>{t('profile.updatePassword')}</Button>
            </Form.Item>
          </div>
        </Form>
      </div>
      )}
    </div>
  )
}

export default Profile
