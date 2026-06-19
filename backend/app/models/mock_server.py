"""
独立 Mock Server 模型

支持为每个项目创建独立的 Mock 服务器，每个服务器可包含多条规则。
规则支持路径匹配、方法匹配、条件响应（根据请求参数返回不同响应）。
"""

from datetime import datetime, timezone
from ..extensions import db


class MockServer(db.Model):
    """独立 Mock 服务器"""
    __tablename__ = 'mock_servers'

    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False, index=True)
    name = db.Column(db.String(200), nullable=False, comment='服务器名称')
    description = db.Column(db.Text, default='', comment='描述')
    path_prefix = db.Column(db.String(200), default='/', comment='路径前缀')
    is_enabled = db.Column(db.Boolean, default=True, comment='是否启用')
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc),
                           onupdate=lambda: datetime.now(timezone.utc))

    # 关联规则
    rules = db.relationship('MockRule', backref='server', lazy='dynamic',
                            cascade='all, delete-orphan', order_by='MockRule.priority')

    def to_dict(self):
        return {
            'id': self.id,
            'project_id': self.project_id,
            'name': self.name,
            'description': self.description,
            'path_prefix': self.path_prefix,
            'is_enabled': self.is_enabled,
            'rule_count': self.rules.count(),
            'created_by': self.created_by,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }

    def to_detail_dict(self):
        """包含规则详情"""
        data = self.to_dict()
        data['rules'] = [r.to_dict() for r in self.rules.all()]
        return data


class MockRule(db.Model):
    """Mock 规则"""
    __tablename__ = 'mock_rules'

    id = db.Column(db.Integer, primary_key=True)
    server_id = db.Column(db.Integer, db.ForeignKey('mock_servers.id'), nullable=False, index=True)
    name = db.Column(db.String(200), nullable=False, comment='规则名称')
    match_method = db.Column(db.String(10), default='*', comment='匹配 HTTP 方法，* 表示全部')
    match_path = db.Column(db.String(500), nullable=False, comment='匹配路径模式，支持通配符')
    priority = db.Column(db.Integer, default=0, comment='规则优先级，数值越小越优先')
    is_enabled = db.Column(db.Boolean, default=True, comment='是否启用')

    # 条件匹配（可选）
    match_query = db.Column(db.JSON, default=dict, comment='匹配 query 参数 {key: value}')
    match_header = db.Column(db.JSON, default=dict, comment='匹配请求头 {key: value}')
    match_body_contains = db.Column(db.String(500), default='', comment='匹配请求体包含字符串')

    # 响应配置
    response_code = db.Column(db.Integer, default=200, comment='响应状态码')
    response_body = db.Column(db.Text, default='', comment='响应体')
    response_headers = db.Column(db.JSON, default=dict, comment='响应头')
    response_delay_ms = db.Column(db.Integer, default=0, comment='响应延迟(ms)')

    # 有状态 Mock
    is_stateful = db.Column(db.Boolean, default=False, comment='是否为有状态响应')
    state_sequence = db.Column(db.JSON, default=list, comment='有状态响应序列 [{code, body, headers}]')
    _current_state_idx = db.Column('current_state_idx', db.Integer, default=0, comment='当前状态索引')

    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def to_dict(self):
        return {
            'id': self.id,
            'server_id': self.server_id,
            'name': self.name,
            'match_method': self.match_method,
            'match_path': self.match_path,
            'priority': self.priority,
            'is_enabled': self.is_enabled,
            'match_query': self.match_query,
            'match_header': self.match_header,
            'match_body_contains': self.match_body_contains,
            'response_code': self.response_code,
            'response_body': self.response_body,
            'response_headers': self.response_headers,
            'response_delay_ms': self.response_delay_ms,
            'is_stateful': self.is_stateful,
            'state_sequence': self.state_sequence,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }

    def get_current_response(self):
        """获取当前响应（支持有状态序列）"""
        if self.is_stateful and self.state_sequence:
            idx = self._current_state_idx or 0
            if idx < len(self.state_sequence):
                state = self.state_sequence[idx]
                # 推进状态
                self._current_state_idx = (idx + 1) % len(self.state_sequence)
                return {
                    'code': state.get('code', self.response_code),
                    'body': state.get('body', self.response_body),
                    'headers': state.get('headers', self.response_headers),
                }
        return {
            'code': self.response_code,
            'body': self.response_body,
            'headers': self.response_headers,
        }


class MockRequestLog(db.Model):
    """Mock 请求日志"""
    __tablename__ = 'mock_request_logs'

    id = db.Column(db.Integer, primary_key=True)
    server_id = db.Column(db.Integer, db.ForeignKey('mock_servers.id'), nullable=False, index=True)
    rule_id = db.Column(db.Integer, db.ForeignKey('mock_rules.id'), nullable=True)
    method = db.Column(db.String(10), nullable=False)
    path = db.Column(db.String(500), nullable=False)
    query_params = db.Column(db.JSON, default=dict)
    request_headers = db.Column(db.JSON, default=dict)
    request_body = db.Column(db.Text, default='')
    response_code = db.Column(db.Integer, default=200)
    response_body_preview = db.Column(db.String(500), default='', comment='响应体前 500 字符')
    matched_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def to_dict(self):
        return {
            'id': self.id,
            'server_id': self.server_id,
            'rule_id': self.rule_id,
            'method': self.method,
            'path': self.path,
            'query_params': self.query_params,
            'response_code': self.response_code,
            'response_body_preview': self.response_body_preview,
            'matched_at': self.matched_at.isoformat() if self.matched_at else None,
        }
