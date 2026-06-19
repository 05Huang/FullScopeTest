"""
测试数据自动清理服务

为用例配置清理策略，集合执行完毕后自动执行清理步骤。
"""

import json
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone
from ..extensions import db
from ..core.logging import get_logger
from ..utils.exceptions import NotFoundError

logger = get_logger(__name__)


class CleanupService:
    """测试数据自动清理服务"""

    def execute_cleanup(
        self,
        case_id: int,
        cleanup_config: Dict[str, Any],
        execution_context: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        执行单个用例的清理操作

        Args:
            case_id: 用例 ID
            cleanup_config: 清理配置 {method, url, headers, body, extract_vars}
            execution_context: 执行上下文（包含变量值等）

        Returns:
            Dict: {success, status_code, message}
        """
        method = cleanup_config.get('method', 'DELETE')
        url = cleanup_config.get('url', '')
        headers = cleanup_config.get('headers', {})
        body = cleanup_config.get('body', '')

        if not url:
            return {'success': False, 'message': '未配置清理 URL', 'case_id': case_id}

        # 变量替换
        ctx = execution_context or {}
        for key, value in ctx.items():
            url = url.replace(f'{{{{{key}}}}}', str(value))
            for h_key, h_value in headers.items():
                headers[h_key] = str(h_value).replace(f'{{{{{key}}}}}', str(value))
            body = body.replace(f'{{{{{key}}}}}', str(value))

        try:
            import requests
            resp = requests.request(
                method, url, headers=headers,
                data=body if body else None,
                timeout=30,
            )
            success = resp.status_code < 400
            logger.info(
                '清理请求已执行',
                case_id=case_id, method=method, url=url,
                status_code=resp.status_code, success=success,
            )
            return {
                'success': success,
                'case_id': case_id,
                'status_code': resp.status_code,
                'message': '清理成功' if success else f'清理失败: HTTP {resp.status_code}',
            }
        except ImportError:
            return {'success': False, 'case_id': case_id, 'message': 'requests 库未安装'}
        except Exception as exc:
            logger.error('清理请求失败', case_id=case_id, error=str(exc))
            return {'success': False, 'case_id': case_id, 'message': str(exc)[:200]}

    def execute_collection_cleanup(
        self,
        collection_id: int,
        execution_contexts: Optional[Dict[int, Dict[str, Any]]] = None,
    ) -> Dict[str, Any]:
        """
        执行用例集的清理操作

        Args:
            collection_id: 用例集 ID
            execution_contexts: 每个用例的执行上下文 {case_id: {var: value}}

        Returns:
            Dict: {total, success, failed, results}
        """
        from ..models.api_test_case import ApiTestCase

        cases = ApiTestCase.query.filter_by(collection_id=collection_id).all()
        results = []
        success_count = 0

        for case in cases:
            if not case.cleanup_config:
                continue
            ctx = (execution_contexts or {}).get(case.id, {})
            result = self.execute_cleanup(case.id, case.cleanup_config, ctx)
            results.append(result)
            if result.get('success'):
                success_count += 1

        return {
            'total': len(results),
            'success': success_count,
            'failed': len(results) - success_count,
            'results': results,
        }


_instance = None


def get_cleanup_service() -> CleanupService:
    global _instance
    if _instance is None:
        _instance = CleanupService()
    return _instance
