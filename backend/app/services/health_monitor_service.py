"""
API 健康监控服务

提供 API 端点的健康检查、可用率统计和响应时间趋势。
"""

import time
from datetime import datetime, timezone, timedelta
from typing import Dict, Any, List, Optional
from ..core.logging import get_logger

logger = get_logger(__name__)

# 内存存储：monitor_id -> {config, checks: [...], created_at}
_monitor_store: Dict[int, Dict[str, Any]] = {}
_next_id = 1


class HealthMonitorService:
    """API 健康监控服务"""

    def create_monitor(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """
        创建监控规则

        Args:
            config: {name, url, method, expected_status, interval_minutes, headers}
        """
        global _next_id
        monitor_id = _next_id
        _next_id += 1

        _monitor_store[monitor_id] = {
            'id': monitor_id,
            'name': config.get('name', ''),
            'url': config['url'],
            'method': config.get('method', 'GET'),
            'expected_status': config.get('expected_status', 200),
            'interval_minutes': config.get('interval_minutes', 5),
            'headers': config.get('headers', {}),
            'is_enabled': True,
            'checks': [],
            'created_at': datetime.now(timezone.utc).isoformat(),
        }
        logger.info('监控规则已创建', monitor_id=monitor_id, url=config['url'])
        return _monitor_store[monitor_id]

    def list_monitors(self) -> List[Dict[str, Any]]:
        """列出所有监控规则"""
        result = []
        for monitor in _monitor_store.values():
            checks = monitor['checks']
            total = len(checks)
            up = sum(1 for c in checks if c.get('is_up'))
            result.append({
                **{k: v for k, v in monitor.items() if k != 'checks'},
                'total_checks': total,
                'up_count': up,
                'availability': round(up / max(total, 1) * 100, 2),
                'last_check': checks[-1] if checks else None,
            })
        return result

    def get_monitor(self, monitor_id: int) -> Optional[Dict[str, Any]]:
        """获取监控详情"""
        monitor = _monitor_store.get(monitor_id)
        if not monitor:
            return None
        checks = monitor['checks']
        total = len(checks)
        up = sum(1 for c in checks if c.get('is_up'))
        return {
            **monitor,
            'total_checks': total,
            'up_count': up,
            'availability': round(up / max(total, 1) * 100, 2),
        }

    def delete_monitor(self, monitor_id: int) -> bool:
        """删除监控规则"""
        if monitor_id in _monitor_store:
            del _monitor_store[monitor_id]
            return True
        return False

    def run_check(self, monitor_id: int) -> Dict[str, Any]:
        """
        执行一次健康检查

        Returns:
            检查结果
        """
        monitor = _monitor_store.get(monitor_id)
        if not monitor:
            return {'error': '监控规则不存在'}

        url = monitor['url']
        method = monitor.get('method', 'GET').upper()
        expected = monitor.get('expected_status', 200)
        headers = monitor.get('headers', {})

        start = time.time()
        status_code = 0
        error = None
        is_up = False

        try:
            import requests
            resp = requests.request(method, url, headers=headers, timeout=10, allow_redirects=True)
            status_code = resp.status_code
            is_up = status_code == expected
            if not is_up:
                error = f'期望状态码 {expected}，实际 {status_code}'
        except ImportError:
            error = 'requests 库未安装'
        except Exception as exc:
            error = str(exc)[:200]

        duration_ms = round((time.time() - start) * 1000, 1)

        check_result = {
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'status_code': status_code,
            'response_time_ms': duration_ms,
            'is_up': is_up,
            'error': error,
        }
        monitor['checks'].append(check_result)

        # 保留最近 1000 次检查
        if len(monitor['checks']) > 1000:
            monitor['checks'] = monitor['checks'][-1000:]

        logger.info(
            '健康检查完成',
            monitor_id=monitor_id,
            url=url,
            status_code=status_code,
            is_up=is_up,
            duration_ms=duration_ms,
        )

        return check_result

    def get_uptime_stats(self, monitor_id: int, days: int = 7) -> Dict[str, Any]:
        """获取可用率统计"""
        monitor = _monitor_store.get(monitor_id)
        if not monitor:
            return {'error': '监控规则不存在'}

        cutoff = datetime.now(timezone.utc) - timedelta(days=days)
        checks = [
            c for c in monitor['checks']
            if c.get('timestamp', '') >= cutoff.isoformat()
        ]

        if not checks:
            return {'availability': 0, 'avg_response_time': 0, 'total_checks': 0, 'days': days}

        total = len(checks)
        up = sum(1 for c in checks if c.get('is_up'))
        avg_time = sum(c.get('response_time_ms', 0) for c in checks) / total

        return {
            'availability': round(up / total * 100, 2),
            'avg_response_time': round(avg_time, 1),
            'total_checks': total,
            'up_count': up,
            'down_count': total - up,
            'days': days,
        }


_instance = None


def get_health_monitor_service() -> HealthMonitorService:
    global _instance
    if _instance is None:
        _instance = HealthMonitorService()
    return _instance
