"""
健康检查端点

提供基础存活检查和就绪检查（数据库 + Redis + Celery 连通性）
"""

from flask import Blueprint, jsonify
from app.extensions import db, celery
import redis
import os

health_bp = Blueprint('health', __name__)


@health_bp.route('/health', methods=['GET'])
def health_check():
    """
    基础存活检查
    返回 200 表示服务正常运行
    """
    return jsonify({
        'status': 'ok',
        'service': 'fullscopetest',
        'version': '1.0.0'
    }), 200


@health_bp.route('/health/ready', methods=['GET'])
def readiness_check():
    """
    就绪检查 - 验证所有依赖服务的连通性
    检查项目：数据库、Redis、Celery
    """
    checks = {}
    all_healthy = True

    # 检查数据库连通性
    try:
        db.session.execute(db.text('SELECT 1'))
        checks['database'] = {'status': 'ok'}
    except Exception as e:
        checks['database'] = {'status': 'error', 'message': str(e)}
        all_healthy = False

    # 检查 Redis 连通性
    try:
        redis_url = os.environ.get('REDIS_URL', 'redis://localhost:6379/0')
        r = redis.from_url(redis_url, socket_timeout=2)
        r.ping()
        checks['redis'] = {'status': 'ok'}
    except Exception as e:
        checks['redis'] = {'status': 'error', 'message': str(e)}
        all_healthy = False

    # 检查 Celery Worker 连通性
    try:
        inspect = celery.control.inspect(timeout=2)
        active_workers = inspect.active() or {}
        if active_workers:
            checks['celery'] = {
                'status': 'ok',
                'workers': list(active_workers.keys())
            }
        else:
            checks['celery'] = {'status': 'warning', 'message': 'No active workers'}
            # 不阻止就绪状态，Worker 可能暂时不可用
    except Exception as e:
        checks['celery'] = {'status': 'warning', 'message': str(e)}
        # 不阻止就绪状态

    status_code = 200 if all_healthy else 503
    return jsonify({
        'status': 'ok' if all_healthy else 'degraded',
        'checks': checks
    }), status_code
