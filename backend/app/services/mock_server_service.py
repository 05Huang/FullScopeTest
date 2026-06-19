"""
独立 Mock Server 服务

提供 Mock Server 的管理能力：创建/更新/删除服务器和规则、
路径匹配、请求日志记录等。
"""

import fnmatch
import time
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional

from ..extensions import db
from ..models.mock_server import MockServer, MockRule, MockRequestLog
from ..core.logging import get_logger
from ..utils.exceptions import NotFoundError, ValidationError

logger = get_logger(__name__)


class MockServerService:
    """独立 Mock Server 服务"""

    # ==================== Mock Server 管理 ====================

    def create_server(self, data: Dict[str, Any], user_id: Optional[int] = None) -> Dict[str, Any]:
        """创建 Mock 服务器"""
        server = MockServer(
            project_id=data['project_id'],
            name=data['name'],
            description=data.get('description', ''),
            path_prefix=data.get('path_prefix', '/'),
            is_enabled=data.get('is_enabled', True),
            created_by=user_id,
        )
        db.session.add(server)
        db.session.commit()
        logger.info('Mock 服务器已创建', server_id=server.id, name=server.name)
        return server.to_dict()

    def get_servers(self, project_id: int) -> List[Dict[str, Any]]:
        """获取项目下的所有 Mock 服务器"""
        servers = MockServer.query.filter_by(project_id=project_id).order_by(
            MockServer.created_at.desc()
        ).all()
        return [s.to_dict() for s in servers]

    def get_server(self, server_id: int) -> Dict[str, Any]:
        """获取 Mock 服务器详情（含规则）"""
        server = MockServer.query.get(server_id)
        if not server:
            raise NotFoundError('Mock 服务器', server_id)
        return server.to_detail_dict()

    def update_server(self, server_id: int, data: Dict[str, Any]) -> Dict[str, Any]:
        """更新 Mock 服务器"""
        server = MockServer.query.get(server_id)
        if not server:
            raise NotFoundError('Mock 服务器', server_id)

        for field in ('name', 'description', 'path_prefix', 'is_enabled'):
            if field in data:
                setattr(server, field, data[field])
        db.session.commit()
        return server.to_dict()

    def delete_server(self, server_id: int) -> None:
        """删除 Mock 服务器"""
        server = MockServer.query.get(server_id)
        if not server:
            raise NotFoundError('Mock 服务器', server_id)
        db.session.delete(server)
        db.session.commit()
        logger.info('Mock 服务器已删除', server_id=server_id)

    # ==================== Mock Rule 管理 ====================

    def create_rule(self, server_id: int, data: Dict[str, Any]) -> Dict[str, Any]:
        """创建 Mock 规则"""
        server = MockServer.query.get(server_id)
        if not server:
            raise NotFoundError('Mock 服务器', server_id)

        rule = MockRule(
            server_id=server_id,
            name=data['name'],
            match_method=data.get('match_method', '*'),
            match_path=data['match_path'],
            priority=data.get('priority', 0),
            is_enabled=data.get('is_enabled', True),
            match_query=data.get('match_query', {}),
            match_header=data.get('match_header', {}),
            match_body_contains=data.get('match_body_contains', ''),
            response_code=data.get('response_code', 200),
            response_body=data.get('response_body', ''),
            response_headers=data.get('response_headers', {}),
            response_delay_ms=data.get('response_delay_ms', 0),
            is_stateful=data.get('is_stateful', False),
            state_sequence=data.get('state_sequence', []),
        )
        db.session.add(rule)
        db.session.commit()
        logger.info('Mock 规则已创建', rule_id=rule.id, server_id=server_id)
        return rule.to_dict()

    def update_rule(self, rule_id: int, data: Dict[str, Any]) -> Dict[str, Any]:
        """更新 Mock 规则"""
        rule = MockRule.query.get(rule_id)
        if not rule:
            raise NotFoundError('Mock 规则', rule_id)

        for field in ('name', 'match_method', 'match_path', 'priority', 'is_enabled',
                      'match_query', 'match_header', 'match_body_contains',
                      'response_code', 'response_body', 'response_headers',
                      'response_delay_ms', 'is_stateful', 'state_sequence'):
            if field in data:
                setattr(rule, field, data[field])
        db.session.commit()
        return rule.to_dict()

    def delete_rule(self, rule_id: int) -> None:
        """删除 Mock 规则"""
        rule = MockRule.query.get(rule_id)
        if not rule:
            raise NotFoundError('Mock 规则', rule_id)
        db.session.delete(rule)
        db.session.commit()

    # ==================== 请求匹配与响应 ====================

    def handle_request(
        self,
        server_id: int,
        method: str,
        path: str,
        query_params: Optional[Dict] = None,
        headers: Optional[Dict] = None,
        body: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        处理 Mock 请求：匹配规则并返回响应

        Returns:
            Dict: {code, body, headers, rule_id, delay_ms}
        """
        server = MockServer.query.get(server_id)
        if not server:
            raise NotFoundError('Mock 服务器', server_id)
        if not server.is_enabled:
            return {'code': 503, 'body': '{"error": "Mock server is disabled"}', 'headers': {}, 'delay_ms': 0}

        # 裁剪 path_prefix
        relative_path = path
        if server.path_prefix and server.path_prefix != '/':
            if relative_path.startswith(server.path_prefix):
                relative_path = relative_path[len(server.path_prefix):]
            if not relative_path.startswith('/'):
                relative_path = '/' + relative_path

        # 按优先级匹配规则
        rules = MockRule.query.filter_by(server_id=server_id, is_enabled=True).order_by(
            MockRule.priority.asc()
        ).all()

        matched_rule = None
        for rule in rules:
            if self._match_rule(rule, method, relative_path, query_params, headers, body):
                matched_rule = rule
                break

        # 记录请求日志
        log = MockRequestLog(
            server_id=server_id,
            rule_id=matched_rule.id if matched_rule else None,
            method=method,
            path=relative_path,
            query_params=query_params or {},
            request_headers=headers or {},
            request_body=(body or '')[:2000],
        )

        if matched_rule:
            resp = matched_rule.get_current_response()
            log.response_code = resp['code']
            log.response_body_preview = (resp['body'] or '')[:500]
            db.session.add(log)
            db.session.commit()

            delay = matched_rule.response_delay_ms or 0
            if delay > 0:
                time.sleep(delay / 1000.0)

            return {
                'code': resp['code'],
                'body': resp['body'] or '',
                'headers': resp['headers'] or {},
                'delay_ms': delay,
                'rule_id': matched_rule.id,
                'rule_name': matched_rule.name,
            }
        else:
            log.response_code = 404
            log.response_body_preview = '{"error": "No matching rule"}'
            db.session.add(log)
            db.session.commit()
            return {
                'code': 404,
                'body': '{"error": "No matching mock rule found"}',
                'headers': {},
                'delay_ms': 0,
                'rule_id': None,
            }

    def get_request_logs(self, server_id: int, limit: int = 100) -> List[Dict[str, Any]]:
        """获取 Mock 请求日志"""
        logs = MockRequestLog.query.filter_by(server_id=server_id).order_by(
            MockRequestLog.matched_at.desc()
        ).limit(limit).all()
        return [l.to_dict() for l in logs]

    def clear_request_logs(self, server_id: int) -> int:
        """清空 Mock 请求日志"""
        count = MockRequestLog.query.filter_by(server_id=server_id).delete()
        db.session.commit()
        return count

    # ==================== 内部方法 ====================

    def _match_rule(
        self,
        rule: MockRule,
        method: str,
        path: str,
        query_params: Optional[Dict],
        headers: Optional[Dict],
        body: Optional[str],
    ) -> bool:
        """匹配单条规则"""
        # 方法匹配
        if rule.match_method and rule.match_method != '*':
            if rule.match_method.upper() != method.upper():
                return False

        # 路径匹配（支持通配符）
        if not fnmatch.fnmatch(path, rule.match_path):
            # 也检查包含关系
            if rule.match_path not in path:
                return False

        # query 参数匹配
        if rule.match_query:
            qp = query_params or {}
            for k, v in rule.match_query.items():
                if qp.get(k) != v:
                    return False

        # header 匹配
        if rule.match_header:
            h = headers or {}
            for k, v in rule.match_header.items():
                if h.get(k) != v:
                    return False

        # body 包含匹配
        if rule.match_body_contains:
            if rule.match_body_contains not in (body or ''):
                return False

        return True


_instance = None


def get_mock_server_service() -> MockServerService:
    """获取 Mock Server 服务单例"""
    global _instance
    if _instance is None:
        _instance = MockServerService()
    return _instance
