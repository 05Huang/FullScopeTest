"""
API 蓝图模块

集中注册所有 API 路由
"""

from flask import Blueprint

# 创建 API 蓝图
api_bp = Blueprint('api', __name__)


# 导入并注册各模块路由
from . import auth
from . import projects
from . import environments
from . import api_test
from . import web_test
from . import perf_test
from . import reports
from . import docs
