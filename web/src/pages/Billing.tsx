import { useState, useEffect, useCallback } from 'react'
import {
  Card, Row, Col, Typography, Tag, Button, Progress, Space,
  Spin, message, Modal, Radio, Divider, Alert, Empty,
} from 'antd'
import {
  CrownOutlined, CheckCircleOutlined, WarningOutlined,
  TeamOutlined, ThunderboltOutlined, CloudOutlined,
  DatabaseOutlined, RobotOutlined, ProjectOutlined,
} from '@ant-design/icons'
import { useTranslation } from 'react-i18next'
import billingService, {
  BillingPlan, Subscription, UsageQuotas,
} from '@/services/billingService'
import { useRole } from '@/hooks/useRole'

const { Title, Text } = Typography
const RESOURCE_ICONS: Record<string, React.ReactNode> = {
  projects: <ProjectOutlined />, test_cases: <ThunderboltOutlined />,
  ai_calls: <RobotOutlined />, members: <TeamOutlined />, storage: <CloudOutlined />,
}

const Billing = () => {
  const { t } = useTranslation()
  const { isAdmin } = useRole()
  const [loading, setLoading] = useState(true)
  const [plans, setPlans] = useState<BillingPlan[]>([])
  const [subscription, setSubscription] = useState<Subscription | null>(null)
  const [usage, setUsage] = useState<UsageQuotas | null>(null)
  const [upgradeModalOpen, setUpgradeModalOpen] = useState(false)
  const [selectedPlan, setSelectedPlan] = useState('')
  const [billingCycle, setBillingCycle] = useState('monthly')
  const [upgrading, setUpgrading] = useState(false)

  const loadData = useCallback(async () => {
    setLoading(true)
    try {
      const [pRes, sRes, uRes] = await Promise.allSettled([
        billingService.getPlans(), billingService.getSubscription(), billingService.getUsage(),
      ])
      if (pRes.status === 'fulfilled' && pRes.value.code === 200) setPlans(pRes.value.data || [])
      if (sRes.status === 'fulfilled' && sRes.value.code === 200) setSubscription(sRes.value.data)
      if (uRes.status === 'fulfilled' && uRes.value.code === 200) setUsage(uRes.value.data)
    } catch {} finally { setLoading(false) }
  }, [])
  useEffect(() => { loadData() }, [loadData])

  const handleUpgrade = async () => {
    if (!selectedPlan) { message.error(t('billing.selectPlan')); return }
    setUpgrading(true)
    try {
      const res = await billingService.upgradeSubscription(selectedPlan, billingCycle)
      if (res.code === 200) { message.success(t('billing.upgradeSuccess')); setUpgradeModalOpen(false); await loadData() }
      else { message.error(res.message || t('billing.upgradeFailed')) }
    } catch { message.error(t('billing.upgradeFailed')) } finally { setUpgrading(false) }
  }
  const handleCancel = () => {
    Modal.confirm({
      title: t('billing.cancelConfirmTitle'), content: t('billing.cancelConfirmContent'),
      okText: t('common.confirm'), cancelText: t('common.cancel'), okButtonProps: { danger: true },
      onOk: async () => {
        try {
          const res = await billingService.cancelSubscription()
          if (res.code === 200) { message.success(t('billing.cancelSuccess')); await loadData() }
          else { message.error(res.message || t('billing.cancelFailed')) }
        } catch { message.error(t('billing.cancelFailed')) }
      },
    })
  }
  const getPlanPrice = (plan: BillingPlan) => {
    if (plan.price_monthly === 0) return t('billing.free')
    const price = billingCycle === 'yearly' ? plan.price_yearly : plan.price_monthly
    const unit = billingCycle === 'yearly' ? t('billing.year') : t('billing.month')
    return String.fromCharCode(165) + price + '/' + unit
  }
  const getUsageColor = (p: number) => p >= 90 ? '#ff4d4f' : p >= 70 ? '#faad14' : '#52c41a'
  const getPlanColor = (n: string) => n === 'free' ? 'default' : n === 'pro' ? 'blue' : 'gold'

  if (loading) return <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: '60vh' }}><Spin size='large' /></div>
  return (
    <div style={{ padding: 24 }}>
      <div style={{ marginBottom: 24 }}>
        <Title level={3} style={{ marginBottom: 4 }}>{t('billing.title')}</Title>
        <Text type='secondary'>{t('billing.subtitle')}</Text>
      </div>
      {subscription && (
        <Card style={{ marginBottom: 24 }}>
          <Row gutter={24} align='middle'>
            <Col flex='auto'>
              <Space size='middle'>
                <CrownOutlined style={{ fontSize: 28, color: '#faad14' }} />
                <div>
                  <Text strong style={{ fontSize: 16 }}>{subscription.plan_display_name || subscription.plan_name}</Text>
                  <Tag color={subscription.status === 'active' ? 'green' : 'orange'} style={{ marginLeft: 8 }}>{subscription.status === 'active' ? t('billing.active') : t('billing.inactive')}</Tag>
                  <div style={{ marginTop: 4 }}>
                    <Text type='secondary'>
                      {t('billing.billingCycle')}: {subscription.billing_cycle === 'monthly' ? t('billing.monthly') : t('billing.yearly')}{subscription.next_billing_date && (<> {t('billing.nextBilling')}: {new Date(subscription.next_billing_date).toLocaleDateString()}</>)}</Text>
                  </div>
                </div>
              </Space>
            </Col>
            <Col>
              <Space>
                <Button type='primary' onClick={() => { setSelectedPlan(''); setUpgradeModalOpen(true) }}>{t('billing.upgrade')}</Button>
                {subscription.plan_name !== 'free' && isAdmin && <Button danger onClick={handleCancel}>{t('billing.cancelSubscription')}</Button>}
              </Space>
            </Col>
          </Row>
        </Card>
      )}
      {usage && (
        <>
          <Title level={4} style={{ marginBottom: 16 }}>{t('billing.usageOverview')}</Title>
          <Row gutter={[16, 16]} style={{ marginBottom: 24 }}>
            {Object.entries(usage).map(([key, quota]) => (
              <Col xs={24} sm={12} md={8} lg={4} key={key}>
                <Card size='small'>
                  <Space direction='vertical' style={{ width: '100%' }}>
                    <Space>{RESOURCE_ICONS[key] || <DatabaseOutlined />}<Text strong>{t('billing.' + key)}</Text></Space>
                    <Progress percent={Math.min(quota.percentage, 100)} strokeColor={getUsageColor(quota.percentage)} format={() => quota.used + '/' + (quota.limit === -1 ? '∞' : quota.limit)} />
                    {quota.percentage >= 80 && <Text type='warning' style={{ fontSize: 12 }}><WarningOutlined /> {t('billing.nearLimit')}</Text>}
                  </Space>
                </Card>
              </Col>
            ))}
          </Row>
        </>
      )}
      <Title level={4} style={{ marginBottom: 16 }}>{t('billing.planComparison')}</Title>
      {plans.length === 0 ? <Empty description={t('billing.noPlans')} /> : (
        <Row gutter={[16, 16]}>
          {plans.map((plan) => {
            const isCurrent = subscription?.plan_name === plan.name
            return (
              <Col xs={24} sm={12} md={8} key={plan.name}>
                <Card hoverable style={{ borderColor: isCurrent ? 'var(--fst-primary)' : undefined, borderWidth: isCurrent ? 2 : 1, height: '100%' }}>
                  <Space direction='vertical' style={{ width: '100%' }} size='middle'>
                    <div style={{ textAlign: 'center' }}>
                      <Tag color={getPlanColor(plan.name)} style={{ fontSize: 14, padding: '2px 12px' }}>{plan.display_name || plan.name}</Tag>
                      {isCurrent && <Tag color='green' style={{ marginLeft: 4 }}><CheckCircleOutlined /> {t('billing.currentPlan')}</Tag>}
                    </div>
                    <div style={{ textAlign: 'center' }}><Title level={2} style={{ margin: 0 }}>{getPlanPrice(plan)}</Title></div>
                    <Divider style={{ margin: '8px 0' }} />
                    <div><Text type='secondary'>{t('billing.maxProjects')}: {plan.max_projects === -1 ? '∞' : plan.max_projects}</Text></div>
                    <div><Text type='secondary'>{t('billing.maxTestCases')}: {plan.max_test_cases === -1 ? '∞' : plan.max_test_cases}</Text></div>
                    <div><Text type='secondary'>{t('billing.maxAiCalls')}: {plan.max_ai_calls_per_month === -1 ? '∞' : plan.max_ai_calls_per_month}</Text></div>
                    <div><Text type='secondary'>{t('billing.maxMembers')}: {plan.max_members === -1 ? '∞' : plan.max_members}</Text></div>
                    {!isCurrent && isAdmin && <Button type='primary' block onClick={() => { setSelectedPlan(plan.name); setUpgradeModalOpen(true) }}>{t('billing.upgrade')}</Button>}
                  </Space>
                </Card>
              </Col>
            )
          })}
        </Row>
      )}
      <Modal title={t('billing.upgradeTitle')} open={upgradeModalOpen} onCancel={() => setUpgradeModalOpen(false)} onOk={handleUpgrade} confirmLoading={upgrading} okText={t('billing.confirmUpgrade')}>
        <Space direction='vertical' style={{ width: '100%' }} size='middle'>
          <div>
            <Text strong>{t('billing.selectPlan')}:</Text>
            <Radio.Group value={selectedPlan} onChange={(e) => setSelectedPlan(e.target.value)} style={{ width: '100%', marginTop: 8 }}>
              <Space direction='vertical' style={{ width: '100%' }}>
                {plans.filter(p => p.name !== subscription?.plan_name).map(plan => (
                  <Radio key={plan.name} value={plan.name}>{plan.display_name || plan.name} - {getPlanPrice(plan)}</Radio>
                ))}
              </Space>
            </Radio.Group>
          </div>
          <div>
            <Text strong>{t('billing.billingCycle')}:</Text>
            <Radio.Group value={billingCycle} onChange={(e) => setBillingCycle(e.target.value)} style={{ marginTop: 8 }}>
              <Radio.Button value='monthly'>{t('billing.monthly')}</Radio.Button>
              <Radio.Button value='yearly'>{t('billing.yearly')}</Radio.Button>
            </Radio.Group>
          </div>
          <Alert message={t('billing.upgradeNotice')} type='info' showIcon />
        </Space>
      </Modal>
    </div>
  )
}
export default Billing
