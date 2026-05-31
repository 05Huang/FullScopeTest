"""
FastAPI 应用骨架

与 Flask 并行运行，通过 Nginx 路由：
- /api/v2/* -> FastAPI
- /api/* -> Flask (保持兼容)
"""

import os
from contextlib import asynccontextmanager
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp, Receive, Scope, Send
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from .core.logging import get_logger

logger = get_logger(__name__)


class FlaskContextMiddleware(BaseHTTPMiddleware):
    """
    ASGI 中间件：在每个请求前后 push/pop Flask app context。

    FastAPI 路由使用 Flask-SQLAlchemy 模型（如 User.query），
    这些模型需要 Flask app context 才能正常工作。
    此中间件确保每次 FastAPI 请求都在 Flask app context 中执行。
    """

    def __init__(self, app: ASGIApp, flask_app=None):
        super().__init__(app)
        self._flask_app = flask_app

    async def dispatch(self, request: Request, call_next):
        flask_app = self._flask_app
        if flask_app is None:
            try:
                from . import create_app
                flask_app = create_app(os.environ.get("FLASK_ENV", "development"))
            except Exception:
                return await call_next(request)

        # If an app context is already active (e.g. from test fixture),
        # reuse it to share the same DB session scope.
        from flask import has_app_context
        if has_app_context():
            return await call_next(request)

        with flask_app.app_context():
            response = await call_next(request)
            return response


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    logger.info("FastAPI application starting...")
    yield
    logger.info("FastAPI application shutting down...")


def create_fastapi_app(config_name: str = "development", flask_app=None) -> FastAPI:
    """
    创建 FastAPI 应用实例

    与 Flask 应用共享同一个数据库连接池，
    通过 Nginx 路由将新接口导向 FastAPI (/api/v2/)。

    Args:
        config_name: 配置环境名称
        flask_app: Flask 应用实例（用于共享 app context）

    Returns:
        FastAPI: 配置好的 FastAPI 应用实例
    """
    app = FastAPI(
        title="FullScopeTest API v2",
        description="FullScopeTest 自动化测试平台 API v2 - FastAPI 版本",
        version="2.0.0",
        docs_url="/api/v2/docs",
        redoc_url="/api/v2/redoc",
        openapi_url="/api/v2/openapi.json",
        lifespan=lifespan,
    )

    # 添加 Flask Context 中间件（确保 Flask-SQLAlchemy 模型可用）
    # 注意：中间件按 LIFO 顺序执行，所以 FlaskContext 要先加
    if flask_app is not None:
        app.add_middleware(FlaskContextMiddleware, flask_app=flask_app)

    # 配置 CORS
    cors_origins = os.environ.get('CORS_ORIGINS', 'http://localhost:3000,http://localhost:8080').split(',')
    app.add_middleware(
        CORSMiddleware,
        allow_origins=cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # 注册异常处理器
    register_exception_handlers(app)

    # 注册路由
    register_v2_routes(app)

    logger.info("FastAPI application created", config=config_name)
    return app


def register_exception_handlers(app: FastAPI):
    """注册全局异常处理器"""

    @app.exception_handler(400)
    async def bad_request(request: Request, exc):
        return JSONResponse(
            status_code=400,
            content={"code": 400, "message": "请求参数错误", "data": None},
        )

    @app.exception_handler(401)
    async def unauthorized(request: Request, exc):
        return JSONResponse(
            status_code=401,
            content={"code": 401, "message": "未授权访问", "data": None},
        )

    @app.exception_handler(404)
    async def not_found(request: Request, exc):
        return JSONResponse(
            status_code=404,
            content={"code": 404, "message": "资源不存在", "data": None},
        )

    @app.exception_handler(500)
    async def internal_error(request: Request, exc):
        logger.error("Internal server error", error=str(exc))
        return JSONResponse(
            status_code=500,
            content={"code": 500, "message": "服务器内部错误", "data": None},
        )


def register_v2_routes(app: FastAPI):
    """注册 v2 API 路由"""

    @app.get("/api/v2/health")
    async def health_check():
        """健康检查端点"""
        return {"status": "ok", "version": "2.0.0"}

    @app.get("/api/v2/health/ready")
    async def readiness_check():
        """就绪检查端点"""
        return {"status": "ok", "version": "2.0.0"}

    # 认证路由 - P5-02
    from .api.v2.auth import router as auth_router
    app.include_router(auth_router, prefix="/api/v2/auth")

    # 测试用例路由 - P5-03
    from .api.v2.test_cases import router as test_cases_router
    app.include_router(test_cases_router, prefix="/api/v2/test-cases")

    # 接口测试路由 - P5-04
    from .api.v2.api_tests import router as api_tests_router
    app.include_router(api_tests_router, prefix="/api/v2/api-tests")

    # Web 测试路由 - P5-05
    from .api.v2.ui_tests import router as ui_tests_router
    app.include_router(ui_tests_router, prefix="/api/v2/ui-tests")

    # 性能测试路由 - P5-06
    from .api.v2.perf_tests import router as perf_tests_router
    app.include_router(perf_tests_router, prefix="/api/v2/perf-tests")

    # OpenAPI 文档增强路由 - P5-07
    from .api.v2.openapi_docs import router as openapi_router
    app.include_router(openapi_router, prefix="/api/v2")


def get_database_url():
    """获取数据库 URL（与 Flask 共享）"""
    return os.environ.get(
        'DATABASE_URL',
        'postgresql://localhost:5432/fullscopetest_dev'
    )
