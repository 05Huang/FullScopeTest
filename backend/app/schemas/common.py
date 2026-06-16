"""
通用 Pydantic Schema

提供 API 通用的请求/响应 Schema，供 v2 端点复用。
"""
from datetime import datetime
from typing import Any, Dict, Generic, List, Optional, TypeVar
from pydantic import BaseModel, Field

T = TypeVar('T')


# ── 通用响应 ──────────────────────────────────────────────────────────────────

class ApiResponse(BaseModel, Generic[T]):
    """统一 API 响应格式"""
    code: int = Field(200, description='状态码')
    message: str = Field('success', description='响应消息')
    data: Optional[T] = Field(None, description='响应数据')
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat() + 'Z')

    class Config:
        json_schema_extra = {
            'example': {
                'code': 200,
                'message': 'success',
                'data': {},
                'timestamp': '2026-06-16T12:00:00Z',
            },
        }


class PaginationMeta(BaseModel):
    """分页元数据"""
    total: int = Field(..., description='总记录数')
    page: int = Field(..., description='当前页码')
    per_page: int = Field(..., description='每页数量')
    pages: int = Field(..., description='总页数')


class PaginatedResponse(BaseModel, Generic[T]):
    """分页响应格式"""
    code: int = 200
    message: str = 'success'
    data: Optional[Dict[str, Any]] = None

    class Config:
        json_schema_extra = {
            'example': {
                'code': 200,
                'message': 'success',
                'data': {
                    'items': [],
                    'pagination': {'total': 0, 'page': 1, 'per_page': 20, 'pages': 0},
                },
            },
        }


# ── 项目 ─────────────────────────────────────────────────────────────────────

class ProjectBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description='项目名称')
    description: Optional[str] = Field(None, description='项目描述')


class ProjectCreate(ProjectBase):
    """创建项目请求"""
    pass


class ProjectResponse(ProjectBase):
    """项目响应"""
    id: int
    owner_id: int
    organization_id: Optional[int] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    class Config:
        json_schema_extra = {
            'example': {
                'id': 1,
                'name': 'My Project',
                'description': 'Test project',
                'owner_id': 1,
                'organization_id': 1,
                'created_at': '2026-06-16T12:00:00Z',
            },
        }


# ── 测试用例 ─────────────────────────────────────────────────────────────────

class TestCaseBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255, description='用例名称')
    method: str = Field('GET', description='HTTP 方法')
    url: str = Field(..., description='请求 URL')
    headers: Optional[Dict[str, str]] = Field(default_factory=dict, description='请求头')
    body: Optional[Any] = Field(None, description='请求体')


class TestCaseCreate(TestCaseBase):
    """创建测试用例请求"""
    project_id: int = Field(..., description='项目 ID')
    collection_id: Optional[int] = Field(None, description='集合 ID')
    description: Optional[str] = Field(None, description='用例描述')


class TestCaseResponse(TestCaseBase):
    """测试用例响应"""
    id: int
    project_id: int
    user_id: int
    collection_id: Optional[int] = None
    description: Optional[str] = None
    assertions: Optional[List[Dict]] = Field(default_factory=list)
    tags: Optional[List[str]] = Field(default_factory=list)
    priority: int = Field(2, description='优先级: 1-高 2-中 3-低')
    is_enabled: bool = True
    last_status: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


# ── 测试执行 ─────────────────────────────────────────────────────────────────

class TestRunCreate(BaseModel):
    """创建测试执行请求"""
    project_id: int = Field(..., description='项目 ID')
    test_type: str = Field(..., description='测试类型: api/web/performance')
    test_object_name: Optional[str] = Field(None, description='测试对象名称')


class TestRunResponse(BaseModel):
    """测试执行响应"""
    id: int
    project_id: int
    test_type: str
    status: str
    total_cases: int = 0
    passed: int = 0
    failed: int = 0
    pass_rate: float = 0.0
    duration: Optional[float] = None
    started_at: Optional[str] = None
    finished_at: Optional[str] = None
    triggered_by: Optional[str] = None
    created_at: Optional[str] = None


# ── 测试计划 ─────────────────────────────────────────────────────────────────

class TestPlanCreate(BaseModel):
    """创建测试计划请求"""
    name: str = Field(..., min_length=1, max_length=200, description='计划名称')
    project_id: int = Field(..., description='项目 ID')
    description: Optional[str] = Field(None, description='计划描述')
    include_cases: Optional[List[Dict]] = Field(default_factory=list, description='用例列表')
    tags: Optional[List[str]] = Field(default_factory=list, description='标签')


class TestPlanResponse(BaseModel):
    """测试计划响应"""
    id: int
    name: str
    project_id: int
    status: str = 'draft'
    total_runs: int = 0
    last_pass_rate: Optional[float] = None
    created_at: Optional[str] = None


# ── 评论 ─────────────────────────────────────────────────────────────────────

class CommentCreate(BaseModel):
    """创建评论请求"""
    resource_type: str = Field(..., description='资源类型: test_case/test_run/test_plan')
    resource_id: int = Field(..., description='资源 ID')
    content: str = Field(..., min_length=1, description='评论内容（Markdown）')
    parent_id: Optional[int] = Field(None, description='父评论 ID（回复）')


class CommentResponse(BaseModel):
    """评论响应"""
    id: int
    resource_type: str
    resource_id: int
    content: str
    user_id: int
    username: Optional[str] = None
    mentions: List[int] = Field(default_factory=list)
    parent_id: Optional[int] = None
    is_edited: bool = False
    is_deleted: bool = False
    created_at: Optional[str] = None


# ── 错误响应 ─────────────────────────────────────────────────────────────────

class ErrorResponse(BaseModel):
    """错误响应"""
    code: int = Field(..., description='HTTP 状态码')
    message: str = Field(..., description='错误消息')
    errors: Optional[Dict[str, Any]] = Field(None, description='详细错误信息')
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat() + 'Z')

    class Config:
        json_schema_extra = {
            'example': {
                'code': 400,
                'message': '参数错误',
                'errors': {'name': '不能为空'},
                'timestamp': '2026-06-16T12:00:00Z',
            },
        }