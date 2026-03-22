import React, { useState, useEffect } from 'react'
import { Card, Form, Input, Button, message, Typography, Row, Col, Space, Divider, Avatar, Upload, Spin } from 'antd'
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
    <div style={{ maxWidth: 800, margin: '0 auto' }}>
      <div style={{ marginBottom: 24 }}>
        <Title level={4}>个人设置</Title>
        <Text type="secondary">管理您的个人基本信息与账号安全</Text>
      </div>

      <Row gutter={[24, 24]}>
        <Col span={24}>
          <Card title={
            <Space>
              <UserOutlined style={{ color: '#3D6E66' }} />
              <span>基本信息</span>
            </Space>
          }>
            <Form
              form={profileForm}
              layout="vertical"
              onFinish={handleUpdateProfile}
            >
              <Row gutter={24}>
                <Col span={24} style={{ textAlign: 'center', marginBottom: 24 }}>
                  <Spin spinning={uploading}>
                    <Upload
                      name="file"
                      showUploadList={false}
                      customRequest={handleUploadAvatar}
                      accept="image/*"
                    >
                      <div style={{ cursor: 'pointer', position: 'relative', display: 'inline-block' }}>
                        <Avatar 
                          size={80} 
                          icon={<UserOutlined />} 
                          src={user?.avatar}
                          style={{ backgroundColor: '#3D6E66' }}
                        />
                        <div style={{
                          position: 'absolute',
                          bottom: 0,
                          right: -8,
                          backgroundColor: '#fff',
                          borderRadius: '50%',
                          padding: 4,
                          boxShadow: '0 2px 8px rgba(0,0,0,0.15)'
                        }}>
                          <UploadOutlined style={{ color: '#3D6E66', fontSize: 16 }} />
                        </div>
                      </div>
                    </Upload>
                  </Spin>
                  <div style={{ marginTop: 16 }}>
                    <Text type="secondary">点击头像可直接上传更换 (支持 JPG/PNG 等格式)</Text>
                  </div>
                </Col>
                <Col span={12}>
                  <Form.Item
                    label="用户名"
                    name="username"
                    rules={[{ required: true, message: '请输入用户名' }, { min: 3, max: 50, message: '长度需在 3-50 个字符之间' }]}
                  >
                    <Input prefix={<UserOutlined />} placeholder="请输入用户名" />
                  </Form.Item>
                </Col>
                <Col span={12}>
                  <Form.Item
                    label="邮箱"
                    name="email"
                    rules={[
                      { required: true, message: '请输入邮箱' },
                      { type: 'email', message: '请输入有效的邮箱地址' }
                    ]}
                  >
                    <Input prefix={<MailOutlined />} placeholder="请输入邮箱" />
                  </Form.Item>
                </Col>
                <Col span={24}>
                  <Form.Item
                    label="头像 URL"
                    name="avatar"
                  >
                    <Input placeholder="请输入头像图片的 URL" />
                  </Form.Item>
                </Col>
              </Row>
              <Form.Item style={{ marginBottom: 0 }}>
                <Button type="primary" htmlType="submit" icon={<SaveOutlined />} loading={loading}>
                  保存基本信息
                </Button>
              </Form.Item>
            </Form>
          </Card>
        </Col>

        <Col span={24}>
          <Card title={
            <Space>
              <LockOutlined style={{ color: '#3D6E66' }} />
              <span>修改密码</span>
            </Space>
          }>
            <Form
              form={passwordForm}
              layout="vertical"
              onFinish={handleUpdatePassword}
            >
              <Form.Item
                label="原密码"
                name="old_password"
                rules={[{ required: true, message: '请输入原密码' }]}
              >
                <Input.Password placeholder="请输入原密码" />
              </Form.Item>
              <Form.Item
                label="新密码"
                name="new_password"
                rules={[{ required: true, message: '请输入新密码' }, { min: 6, message: '密码长度至少为 6 位' }]}
              >
                <Input.Password placeholder="请输入新密码" />
              </Form.Item>
              <Form.Item
                label="确认新密码"
                name="confirm_password"
                rules={[{ required: true, message: '请确认新密码' }]}
              >
                <Input.Password placeholder="请再次输入新密码" />
              </Form.Item>
              <Form.Item style={{ marginBottom: 0 }}>
                <Button type="primary" htmlType="submit" icon={<SaveOutlined />} loading={pwdLoading}>
                  更新密码
                </Button>
              </Form.Item>
            </Form>
          </Card>
        </Col>
      </Row>
    </div>
  )
}

export default Profile
