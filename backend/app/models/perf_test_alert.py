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
        db.Index('idx_perf_alert_rules_scenario_id', 'scenario_id'),
        db.Index('idx_perf_alert_rules_enabled', 'is_enabled'),
    )

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, comment='告警规则名称')
    description = db.Column(db.Text, comment='规则描述')
    
    # 关联场景（可选，为空则对所有场景生效）
    scenario_id = db.Column(db.Integer, db.ForeignKey('perf_test_scenarios.id'), nullable=True, comment='关联的场景 ID，为空则全局生效')
    
    # 告警条件类型: absolute（绝对阈值）/ relative（相对劣化）
    condition_type = db.Column(db.String(20), nullable=False, default='absolute', comment='条件类型: absolute/relative')
    
    # 绝对阈值条件（condition_type='absolute'）
    metric_name = db.Column(db.String(50), nullable=True, comment='指标名称: p95_response_time/p99_response_time/error_rate/rps/avg_response_time')
    operator = db.Column(db.String(10), nullable=True, comment='比较运算符: >/</>=/<=')
    threshold_value = db.Column(db.Float, nullable=True, comment='阈值')
    
    # 相对劣化条件（condition_type='relative'）
    relative_metric = db.Column(db.String(50), nullable=True, comment='相对劣化的指标名称')
    degradation_percentage = db.Column(db.Float, nullable=True, comment='劣化百分比阈值（>0 表示劣化）')
    
    # 通知配置
    notify_webhook = db.Column(db.String(500), comment='Webhook URL（如钉钉/飞书/Slack）')
    notify_users = db.Column(db.JSON, default=list, comment='通知用户 ID 列表')
    
    # 状态
    is_enabled = db.Column(db.Boolean, default=True, comment='是否启用')
    
    # 时间戳
    created_at = db.Column(db.DateTime, default=datetime.utcnow, comment='创建时间')
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment='更新时间')

    # 关联关系
    scenario = db.relationship('PerfTestScenario', backref='alert_rules')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'scenario_id': self.scenario_id,
            'condition_type': self.condition_type,
            'metric_name': self.metric_name,
            'operator': self.operator,
            'threshold_value': self.threshold_value,
            'relative_metric': self.relative_metric,
            'degradation_percentage': self.degradation_percentage,
            'notify_webhook': self.notify_webhook,
            'notify_users': self.notify_users,
            'is_enabled': self.is_enabled,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }

    def __repr__(self):
        return f'<PerformanceAlertRule {self.name} type={self.condition_type}>'


class PerformanceAlertLog(db.Model):
    """性能测试告警日志表 - 记录触发的告警"""

    __tablename__ = 'performance_alert_logs'
    __table_args__ = (
        db.Index('idx_perf_alert_logs_rule_id', 'rule_id'),
        db.Index('idx_perf_alert_logs_test_result_id', 'test_result_id'),
        db.Index('idx_perf_alert_logs_created_at', 'created_at'),
    )

    id = db.Column(db.Integer, primary_key=True)
    rule_id = db.Column(db.Integer, db.ForeignKey('performance_alert_rules.id'), nullable=False, comment='关联的告警规则 ID')
    test_result_id = db.Column(db.Integer, db.ForeignKey('performance_test_results.id'), nullable=True, comment='关联的测试结果 ID')
    
    # 告警详情
    metric_name = db.Column(db.String(50), nullable=False, comment='触发告警的指标名称')
    current_value = db.Column(db.Float, comment='当前值')
    threshold_value = db.Column(db.Float, comment='阈值')
    message = db.Column(db.Text, nullable=False, comment='告警消息')
    severity = db.Column(db.String(20), default='warning', comment='严重程度: info/warning/critical')
    
    # 通知状态
    notification_sent = db.Column(db.Boolean, default=False, comment='是否已发送通知')
    notification_error = db.Column(db.Text, comment='通知发送失败的错误信息')
    
    # 时间戳
    created_at = db.Column(db.DateTime, default=datetime.utcnow, comment='创建时间')

    # 关联关系
    rule = db.relationship('PerformanceAlertRule', backref='alert_logs')
    test_result = db.relationship('PerformanceTestResult', backref='alert_logs')

    def to_dict(self):
        return {
            'id': self.id,
            'rule_id': self.rule_id,
            'test_result_id': self.test_result_id,
            'metric_name': self.metric_name,
            'current_value': self.current_value,
            'threshold_value': self.threshold_value,
            'message': self.message,
            'severity': self.severity,
            'notification_sent': self.notification_sent,
            'notification_error': self.notification_error,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }

    def __repr__(self):
        return f'<PerformanceAlertLog rule={self.rule_id} severity={self.severity}>'
