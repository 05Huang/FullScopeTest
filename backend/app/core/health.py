"""
健康检查端点

提供 Kubernetes 兼容的健康检查：
- /health/live  — 存活探针（liveness probe），返回 200 表示进程存活
- /health/ready — 就绪探针（readiness probe），检查 DB/Redis/Celery 连通性
- /health       — 综合健康检查（兼容旧版本）

返回格式：
{
    "status": "ok",
    "service": "fullscopetest",
    "version": "1.0.0",
    "checks": {
        "database": {"status": "ok"},
        "redis": {"status": "ok"},
        "celery": {"status": "ok", "workers": [...]}
    }
}
"""

from datetime import datetime, timezone
from flask import Blueprint, jsonify
from sqlalchemy import text as sa_text
from app.extensions import db, celery
from app.core.logging import get_logger
import redis
import os

logger = get_logger(__name__)
health_bp = Blueprint('health', __name__)

# 版本号（可通过环境变量覆盖）
SERVICE_VERSION = os.environ.get('APP_VERSION', '1.0.0')


@health_bp.route('/health/live', methods=['GET'])
def liveness_probe():
    """
    存活探针（Kubernetes liveness probe）

    仅检查进程是否存活，不检查依赖服务。
    始终返回 200，除非进程完全不可用。
    """
    return jsonify({
        'status': 'ok',
        'service': 'fullscopetest',
        'version': SERVICE_VERSION,
        'timestamp': datetime.now(timezone.utc).replace(tzinfo=None).isoformat() + 'Z',
    }), 200


@health_bp.route('/health/ready', methods=['GET'])
def readiness_probe():
    """
    就绪探针（Kubernetes readiness probe）

    检查所有关键依赖的连通性：
    - database: PostgreSQL 连接
    - redis: Redis 连接
    - celery: Celery Worker 状态

    任一关键组件（database）失败返回 503。
    Redis 和 Celery 为非关键组件，失败时状态为 degraded 但仍返回 200。
    """
    checks = {}
    all_critical_ok = True

    # 检查数据库连通性（关键组件）
    checks['database'] = _check_database()
    if checks['database']['status'] == 'error':
        all_critical_ok = False

    # 检查 Redis 连通性（非关键）
    checks['redis'] = _check_redis()

    # 检查 Celery Worker 连通性（非关键）
    checks['celery'] = _check_celery()

    # 判断整体状态
    has_warning = any(c.get('status') in ('warning', 'error') for c in checks.values())
    if not all_critical_ok:
        overall_status = 'error'
    elif has_warning:
        overall_status = 'degraded'
    else:
        overall_status = 'ok'

    status_code = 200 if all_critical_ok else 503

    response = {
        'status': overall_status,
        'service': 'fullscopetest',
        'version': SERVICE_VERSION,
        'checks': checks,
        'timestamp': datetime.now(timezone.utc).replace(tzinfo=None).isoformat() + 'Z',
    }

    return jsonify(response), status_code


@health_bp.route('/health', methods=['GET'])
def health_check():
    """
    综合健康检查（兼容旧版本）

    等同于 /health/ready，保持向后兼容。
    """
    return readiness_probe()


# ── 组件检查函数 ──────────────────────────────────────────────────────────────

def _check_database() -> dict:
    """检查数据库连通性和连接池状态"""
    try:
        db.session.execute(sa_text('SELECT 1'))
        result = {'status': 'ok'}
        # 连接池状态（仅在有真实连接池时报告，跳过 NullPool）
        try:
            pool = db.engine.pool
            from sqlalchemy.pool import NullPool
            if isinstance(pool, NullPool):
                # NullPool 不维护连接池，跳过统计
                return result
            pool_status = {
                'pool_size': pool.size(),
                'checked_in': pool.checkedin(),
                'checked_out': pool.checkedout(),
                'overflow': pool.overflow(),
            }
            result['pool'] = pool_status
            # 连接池使用率告警（超过 80%）
            total_capacity = pool.size() + pool.overflow()
            if total_capacity > 0:
                usage = pool.checkedout() / total_capacity
                if usage > 0.8:
                    result['status'] = 'warning'
                    result['message'] = f'连接池使用率过高: {usage:.0%}'
                    logger.warning(
                        "数据库连接池使用率过高",
                        checked_out=pool.checkedout(),
                        total_capacity=total_capacity,
                        usage=f"{usage:.0%}",
                    )
        except (AttributeError, NotImplementedError, TypeError):
            pass  # 某些 pool 实现不支持这些方法
        return result
    except Exception as e:
        logger.error("数据库健康检查失败", error=str(e))
        return {'status': 'error', 'message': str(e)}


def _check_redis() -> dict:
    """检查 Redis 连通性"""
    try:
        redis_url = os.environ.get('REDIS_URL', 'redis://localhost:6379/0')
        r = redis.from_url(redis_url, socket_timeout=2)
        r.ping()
        return {'status': 'ok'}
    except Exception as e:
        logger.warning("Redis 健康检查失败", error=str(e))
        return {'status': 'warning', 'message': str(e)}


def _check_celery() -> dict:
    """检查 Celery Worker 状态"""
    try:
        # 检查 Celery 配置是否启用
        if not os.environ.get('CELERY_ENABLE', 'false').lower() == 'true':
            return {'status': 'disabled', 'message': 'Celery is disabled'}

        inspect = celery.control.inspect(timeout=2)
        active_workers = inspect.active() or {}
        if active_workers:
            return {
                'status': 'ok',
                'workers': list(active_workers.keys()),
            }
        else:
            return {'status': 'warning', 'message': 'No active workers'}
    except Exception as e:
        logger.warning("Celery 健康检查失败", error=str(e))
        return {'status': 'warning', 'message': str(e)}
