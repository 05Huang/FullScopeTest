import React, { useState, useEffect } from 'react'
import { Card, Form, Input, Button, message, Typography, Row, Col, Space, Avatar, Upload, Spin } from 'antd'
import { UserOutlined, MailOutlined, SaveOutlined, LockOutlined, UploadOutlined } from '@ant-design/icons'
import type { UploadProps } from 'antd'
import { authService } from '@/services/authService'
import { useAuthStore } from '@/stores/authStore'

const { Title, Text } = Typography

const Profile: React.FC = () => {
  const { user, updateUser } = useAuthStore()
  const [profileForm] = Form.useForm()
  const [passwordForm] = Form.useForm()
  const [loading, setLoading] = useState(false)
  const [pwdLoading, setPwdLoading] = useState(false)
  const [uploading, setUploading] = useState(false)

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
        message.success('头像上传成功')
        profileForm.setFieldsValue({ avatar: res.data.avatar })
        updateUser({ avatar: res.data.avatar })
        onSuccess?.('ok')
      } else {
        message.error(res.message || '上传失败')
        onError?.(new Error(res.message || '上传失败'))
      }
    } catch (error: any) {
      message.error(error.message || '上传失败')
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
        message.success('个人信息更新成功')
        // Update user context
        updateUser(res.data)
      } else {
        message.error(res.message || '更新失败')
      }
    } catch (error: any) {
      message.error(error.message || '更新失败')
    } finally {
      setLoading(false)
    }
  }

  const handleUpdatePassword = async (values: any) => {
    if (values.new_password !== values.confirm_password) {
      message.error('两次输入的新密码不一致')
      return
    }
    setPwdLoading(true)
    try {
      const res = await authService.changePassword(values.old_password, values.new_password)
      if (res.code === 200) {
        message.success('密码修改成功')
        passwordForm.resetFields()
      } else {
        message.error(res.message || '修改失败')
      }
    } catch (error: any) {
      message.error(error.message || '修改失败')
    } finally {
      setPwdLoading(false)
    }
  }

  return (
    <div className="fst-page" style={{ maxWidth: 800, margin: '0 auto' }}>
      <div className="fst-page-header fst-animate-in">
        <div>
          <h1 className="fst-page-title">个人设置</h1>
          <div className="fst-ios-card-subtitle">管理您的个人基本信息与账号安全</div>
        </div>
      </div>

      {/* Profile Card */}
      <div className="fst-ios-card fst-animate-in fst-animate-in-1">
        <div className="fst-ios-card-header">
          <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
            <div className="fst-stat-icon fst-stat-icon--primary"><UserOutlined style={{ fontSize: 18 }} /></div>
            <div>
              <div className="fst-ios-card-title">基本信息</div>
              <div className="fst-ios-card-subtitle">更新您的头像、用户名和邮箱</div>
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
              点击头像可直接上传更换
            </div>
          </div>

          <Row gutter={24}>
            <Col span={12}>
              <Form.Item
                label={<span style={{ fontWeight: 600, fontSize: 13 }}>用户名</span>}
                name="username"
                rules={[{ required: true, message: '请输入用户名' }, { min: 3, max: 50 }]}
              >
                <Input prefix={<UserOutlined />} placeholder="请输入用户名" />
              </Form.Item>
            </Col>
            <Col span={12}>
              <Form.Item
                label={<span style={{ fontWeight: 600, fontSize: 13 }}>邮箱</span>}
                name="email"
                rules={[{ required: true, message: '请输入邮箱' }, { type: 'email' }]}
              >
                <Input prefix={<MailOutlined />} placeholder="请输入邮箱" />
              </Form.Item>
            </Col>
            <Col span={24}>
              <Form.Item label={<span style={{ fontWeight: 600, fontSize: 13 }}>头像 URL</span>} name="avatar">
                <Input placeholder="请输入头像图片的 URL" />
              </Form.Item>
            </Col>
          </Row>

          <div style={{ borderTop: '1px solid var(--fst-outline-soft)', paddingTop: 20 }}>
            <Form.Item style={{ marginBottom: 0 }}>
              <Button type="primary" htmlType="submit" icon={<SaveOutlined />} loading={loading}>保存基本信息</Button>
            </Form.Item>
          </div>
        </Form>
      </div>

      {/* Password Card */}
      <div className="fst-ios-card fst-animate-in fst-animate-in-2">
        <div className="fst-ios-card-header">
          <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
            <div className="fst-stat-icon fst-stat-icon--tertiary"><LockOutlined style={{ fontSize: 18 }} /></div>
            <div>
              <div className="fst-ios-card-title">修改密码</div>
              <div className="fst-ios-card-subtitle">确保您的账号安全</div>
            </div>
          </div>
        </div>

        <Form form={passwordForm} layout="vertical" onFinish={handleUpdatePassword}>
          <Form.Item
            label={<span style={{ fontWeight: 600, fontSize: 13 }}>原密码</span>}
            name="old_password"
            rules={[{ required: true, message: '请输入原密码' }]}
          >
            <Input.Password placeholder="请输入原密码" />
          </Form.Item>
          <Form.Item
            label={<span style={{ fontWeight: 600, fontSize: 13 }}>新密码</span>}
            name="new_password"
            rules={[{ required: true, message: '请输入新密码' }, { min: 6 }]}
          >
            <Input.Password placeholder="请输入新密码" />
          </Form.Item>
          <Form.Item
            label={<span style={{ fontWeight: 600, fontSize: 13 }}>确认新密码</span>}
            name="confirm_password"
            rules={[{ required: true, message: '请确认新密码' }]}
          >
            <Input.Password placeholder="请再次输入新密码" />
          </Form.Item>
          <div style={{ borderTop: '1px solid var(--fst-outline-soft)', paddingTop: 20 }}>
            <Form.Item style={{ marginBottom: 0 }}>
              <Button type="primary" htmlType="submit" icon={<SaveOutlined />} loading={pwdLoading}>更新密码</Button>
            </Form.Item>
          </div>
        </Form>
      </div>
    </div>
  )
}

export default Profile
