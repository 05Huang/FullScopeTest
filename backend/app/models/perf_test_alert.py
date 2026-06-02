"""
性能测试告警规则模型

存储可配置的告警规则，支持绝对阈值和相对劣化告警
"""

from datetime import datetime
from ..extensions import db


class PerformanceAlertRule(db.Model):
    """性能测试告警规则表"""

    __tablename__ = 'performance_alert_rules'
    __table_args__ = (
        db.Index('idx_alert_rules_scenario_id', 'scenario_id'),
        db.Index('idx_alert_rules_enabled', 'enabled'),
    )

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, comment='告警规则名称')
    description = db.Column(db.Text, comment='告警规则描述')

    # 关联的测试场景（可选，为空则适用于所有场景）
    scenario_id = db.Column(db.Integer, db.ForeignKey('perf_test_scenarios.id'), nullable=True, comment='关联的性能测试场景 ID')

    # 告警条件 - 绝对值告警
    p95_threshold = db.Column(db.Float, comment='P95 响应时间阈值 (ms)')
    p99_threshold = db.Column(db.Float, comment='P99 响应时间阈值 (ms)')
    error_rate_threshold = db.Column(db.Float, comment='错误率阈值 (%)')
    rps_min_threshold = db.Column(db.Float, comment='最小 RPS 阈值')

    # 告警条件 - 相对告警（相比上次运行劣化超过 X%）
    relative_p95_degradation = db.Column(db.Float, comment='P95 劣化百分比阈值 (%)')
    relative_rps_degradation = db.Column(db.Float, comment='RPS 劣化百分比阈值 (%)')
    relative_error_rate_degradation = db.Column(db.Float, comment='错误率劣化百分比阈值 (%)')

    # 通知配置
    notify_webhook = db.Column(db.String(500), comment='Webhook 通知 URL')
    notify_email = db.Column(db.Text, comment='邮件通知列表 (JSON 数组)')

    # 状态
    enabled = db.Column(db.Boolean, default=True, comment='是否启用')

    # 统计
    last_triggered_at = db.Column(db.DateTime, comment='最后触发时间')
    trigger_count = db.Column(db.Integer, default=0, comment='触发次数')

    created_at = db.Column(db.DateTime, default=datetime.utcnow, comment='创建时间')
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment='更新时间')

    # 关联关系
    scenario = db.relationship('PerfTestScenario', backref='alert_rules')

    def to_dict(self):
        # Derive metric and threshold for frontend display
        metric = 'P95 Response Time'
        threshold = self.p95_threshold
        operator = '<='
        if self.p99_threshold:
            metric = 'P99 Response Time'
            threshold = self.p99_threshold
            operator = '<='
        if self.error_rate_threshold:
            metric = 'Error Rate'
            threshold = self.error_rate_threshold
            operator = '<='
        if self.rps_min_threshold:
            metric = 'RPS'
            threshold = self.rps_min_threshold
            operator = '>='
        if self.relative_p95_degradation:
            metric = 'P95 Degradation'
            threshold = self.relative_p95_degradation
            operator = '<='

        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'scenario_id': self.scenario_id,
            'scenario_name': self.scenario.name if self.scenario else None,
            'metric': metric,
            'threshold': threshold,
            'operator': operator,
            'is_active': self.enabled,
            'p95_threshold': self.p95_threshold,
            'p99_threshold': self.p99_threshold,
            'error_rate_threshold': self.error_rate_threshold,
            'rps_min_threshold': self.rps_min_threshold,
            'relative_p95_degradation': self.relative_p95_degradation,
            'relative_rps_degradation': self.relative_rps_degradation,
            'relative_error_rate_degradation': self.relative_error_rate_degradation,
            'notify_webhook': self.notify_webhook,
            'notify_email': self.notify_email,
            'enabled': self.enabled,
            'last_triggered_at': self.last_triggered_at.isoformat() if self.last_triggered_at else None,
            'trigger_count': self.trigger_count,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }

    def __repr__(self):
        return f'<PerformanceAlertRule {self.name}>'


class PerformanceAlertLog(db.Model):
    """性能测试告警日志表 - 记录告警触发历史"""

    __tablename__ = 'performance_alert_logs'
    __table_args__ = (
        db.Index('idx_alert_logs_rule_id', 'rule_id'),
        db.Index('idx_alert_logs_result_id', 'result_id'),
        db.Index('idx_alert_logs_created_at', 'created_at'),
    )

    id = db.Column(db.Integer, primary_key=True)
    rule_id = db.Column(db.Integer, db.ForeignKey('performance_alert_rules.id'), nullable=False, comment='关联的告警规则 ID')
    result_id = db.Column(db.Integer, db.ForeignKey('performance_test_results.id'), nullable=False, comment='关联的性能测试结果 ID')

    # 告警详情
    alert_type = db.Column(db.String(50), nullable=False, comment='告警类型: absolute/relative')
    metric_name = db.Column(db.String(50), nullable=False, comment='触发告警的指标名称')
    threshold_value = db.Column(db.Float, nullable=False, comment='阈值')
    actual_value = db.Column(db.Float, nullable=False, comment='实际值')
    message = db.Column(db.Text, nullable=False, comment='告警消息')

    # 通知状态
    notification_sent = db.Column(db.Boolean, default=False, comment='是否已发送通知')
    notification_error = db.Column(db.Text, comment='通知发送失败的错误信息')

    created_at = db.Column(db.DateTime, default=datetime.utcnow, comment='创建时间')

    # 关联关系
    rule = db.relationship('PerformanceAlertRule', backref='alert_logs')
    test_result = db.relationship('PerformanceTestResult', backref='alert_logs')

    def to_dict(self):
        return {
            'id': self.id,
            'rule_id': self.rule_id,
            'result_id': self.result_id,
            'alert_type': self.alert_type,
            'metric_name': self.metric_name,
            'threshold_value': self.threshold_value,
            'actual_value': self.actual_value,
            'message': self.message,
            'notification_sent': self.notification_sent,
            'notification_error': self.notification_error,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }

    def __repr__(self):
        return f'<PerformanceAlertLog {self.metric_name}={self.actual_value}>'
