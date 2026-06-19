"""
接口变更检测服务

记录每次执行的响应结构（字段列表、类型），下次执行时自动对比。
新增/删除/类型变化的字段高亮提示，帮助发现未通知的 API Breaking Change。
"""

import json
from typing import Dict, Any, List, Optional, Set
from datetime import datetime, timezone
from ..extensions import db
from ..core.logging import get_logger

logger = get_logger(__name__)


# 内存缓存：case_id -> 最近一次的响应结构
_structure_cache: Dict[int, Dict[str, Any]] = {}


class APIChangeDetectionService:
    """接口变更检测服务"""

    def record_response_structure(
        self,
        case_id: int,
        response_body: str,
        status_code: int = 200,
    ) -> Dict[str, Any]:
        """
        记录响应结构到缓存

        Args:
            case_id: 用例 ID
            response_body: 响应体
            status_code: 状态码

        Returns:
            记录的结构信息
        """
        structure = self._extract_structure(response_body)
        record = {
            'structure': structure,
            'status_code': status_code,
            'recorded_at': datetime.now(timezone.utc).isoformat(),
        }
        _structure_cache[case_id] = record
        return record

    def detect_changes(
        self,
        case_id: int,
        response_body: str,
        status_code: int = 200,
    ) -> Dict[str, Any]:
        """
        检测响应结构变更

        Args:
            case_id: 用例 ID
            response_body: 当前响应体
            status_code: 当前状态码

        Returns:
            Dict: {has_changes, changes, summary}
        """
        previous = _structure_cache.get(case_id)
        if not previous:
            # 首次记录，无对比基准
            self.record_response_structure(case_id, response_body, status_code)
            return {
                'has_changes': False,
                'is_first_record': True,
                'changes': [],
                'summary': '首次记录响应结构',
            }

        current_structure = self._extract_structure(response_body)
        previous_structure = previous.get('structure', {})

        changes = self._diff_structures(previous_structure, current_structure, '')

        # 更新缓存
        self.record_response_structure(case_id, response_body, status_code)

        has_changes = len(changes) > 0
        added = sum(1 for c in changes if c['type'] == 'added')
        removed = sum(1 for c in changes if c['type'] == 'removed')
        modified = sum(1 for c in changes if c['type'] == 'type_changed')

        summary_parts = []
        if added:
            summary_parts.append(f'{added} 个新增字段')
        if removed:
            summary_parts.append(f'{removed} 个删除字段')
        if modified:
            summary_parts.append(f'{modified} 个类型变化')

        return {
            'has_changes': has_changes,
            'is_first_record': False,
            'changes': changes,
            'summary': '；'.join(summary_parts) if summary_parts else '无变更',
            'previous_recorded_at': previous.get('recorded_at'),
        }

    def get_cached_structure(self, case_id: int) -> Optional[Dict[str, Any]]:
        """获取缓存的响应结构"""
        return _structure_cache.get(case_id)

    # ==================== 内部方法 ====================

    def _extract_structure(self, body: str) -> Dict[str, Any]:
        """从响应体提取结构"""
        try:
            parsed = json.loads(body) if body else None
        except (json.JSONDecodeError, TypeError):
            return {'type': 'string', 'raw': True}

        if parsed is None:
            return {'type': 'null'}
        return self._extract_value_structure(parsed)

    def _extract_value_structure(self, value: Any, depth: int = 0) -> Dict[str, Any]:
        """递归提取值的结构"""
        if depth > 10:
            return {'type': 'unknown'}
        if value is None:
            return {'type': 'null'}
        if isinstance(value, bool):
            return {'type': 'boolean'}
        if isinstance(value, int):
            return {'type': 'integer'}
        if isinstance(value, float):
            return {'type': 'number'}
        if isinstance(value, str):
            return {'type': 'string'}
        if isinstance(value, list):
            if not value:
                return {'type': 'array', 'items': {'type': 'unknown'}}
            return {
                'type': 'array',
                'items': self._extract_value_structure(value[0], depth + 1),
                'length_sample': len(value),
            }
        if isinstance(value, dict):
            properties = {}
            for k, v in value.items():
                properties[k] = self._extract_value_structure(v, depth + 1)
            return {
                'type': 'object',
                'properties': properties,
                'keys': list(value.keys()),
            }
        return {'type': str(type(value).__name__)}

    def _diff_structures(
        self,
        old: Dict[str, Any],
        new: Dict[str, Any],
        path: str,
    ) -> List[Dict[str, Any]]:
        """对比两个结构的差异"""
        changes = []

        old_type = old.get('type')
        new_type = new.get('type')

        # 类型变化
        if old_type != new_type:
            changes.append({
                'type': 'type_changed',
                'path': path or '/',
                'old_type': old_type,
                'new_type': new_type,
                'severity': 'warning',
            })
            return changes  # 类型不同，不做深度对比

        # 对象类型：对比属性
        if old_type == 'object' and new_type == 'object':
            old_keys = set(old.get('keys', []))
            new_keys = set(new.get('keys', []))
            old_props = old.get('properties', {})
            new_props = new.get('properties', {})

            # 新增字段
            for k in new_keys - old_keys:
                changes.append({
                    'type': 'added',
                    'path': f'{path}.{k}' if path else f'/{k}',
                    'new_type': new_props.get(k, {}).get('type', 'unknown'),
                    'severity': 'info',
                })

            # 删除字段（Breaking Change）
            for k in old_keys - new_keys:
                changes.append({
                    'type': 'removed',
                    'path': f'{path}.{k}' if path else f'/{k}',
                    'old_type': old_props.get(k, {}).get('type', 'unknown'),
                    'severity': 'breaking',
                })

            # 递归对比共同字段
            for k in old_keys & new_keys:
                sub_path = f'{path}.{k}' if path else f'/{k}'
                changes.extend(
                    self._diff_structures(old_props.get(k, {}), new_props.get(k, {}), sub_path)
                )

        # 数组类型：对比元素结构
        elif old_type == 'array' and new_type == 'array':
            old_items = old.get('items', {})
            new_items = new.get('items', {})
            changes.extend(
                self._diff_structures(old_items, new_items, f'{path}[*]' if path else '/[*]')
            )

        return changes


    def check_and_alert(
        self,
        case_id: int,
        response_body: str,
        status_code: int = 200,
        case_name: str = '',
    ) -> Dict[str, Any]:
        """
        检测变更并在发现 Breaking Change 时触发告警

        Args:
            case_id: 用例 ID
            response_body: 响应体
            status_code: 状态码
            case_name: 用例名称（用于告警消息）

        Returns:
            Dict: 检测结果 + 是否触发告警
        """
        result = self.detect_changes(case_id, response_body, status_code)

        breaking_changes = [c for c in result.get('changes', []) if c.get('severity') == 'breaking']

        if breaking_changes:
            alert_message = f'接口变更告警：用例「{case_name or case_id}」检测到 {len(breaking_changes)} 个 Breaking Change'
            for change in breaking_changes:
                alert_message += f'\n  - [{change["type"]}] {change["path"]}'

            logger.warning('接口 Breaking Change 检测到', case_id=case_id, changes=len(breaking_changes))

            # 尝试触发通知（如果通知服务可用）
            try:
                from .notification_service import get_notification_service
                notify = get_notification_service()
                notify.send_notification(
                    title='接口变更告警',
                    content=alert_message,
                    level='warning',
                )
            except Exception:
                pass  # 通知服务不可用时静默忽略

            result['alert_triggered'] = True
            result['alert_message'] = alert_message
        else:
            result['alert_triggered'] = False

        return result


_instance = None


def get_api_change_detection_service() -> APIChangeDetectionService:
    global _instance
    if _instance is None:
        _instance = APIChangeDetectionService()
    return _instance
