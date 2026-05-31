"""
测试用例管理 Pydantic schemas
"""

from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


# ====== ApiTestCollection schemas ======

class ApiTestCollectionCreate(BaseModel):
    """创建 API 测试集合"""
    name: str = Field(..., min_length=1, max_length=100, description='集合名称')
    description: Optional[str] = Field(None, max_length=500, description='集合描述')
    parent_id: Optional[int] = Field(None, description='父集合 ID')


class ApiTestCollectionUpdate(BaseModel):
    """更新 API 测试集合"""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    parent_id: Optional[int] = None


class ApiTestCollectionResponse(BaseModel):
    """API 测试集合响应"""
    id: int
    name: str
    description: Optional[str]
    parent_id: Optional[int]
    project_id: int
    user_id: int
    case_count: Optional[int] = 0
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


# ====== ApiTestCase schemas ======

class ApiTestCaseCreate(BaseModel):
    """创建 API 测试用例"""
    name: str = Field(..., min_length=1, max_length=255, description='用例名称')
    collection_id: Optional[int] = Field(None, description='所属集合 ID')
    description: Optional[str] = Field(None, max_length=1000, description='用例描述')
    method: str = Field('GET', description='HTTP 方法')
    url: str = Field(..., min_length=1, description='请求 URL')
    headers: Optional[Dict[str, Any]] = Field(None, description='请求头')
    params: Optional[Dict[str, Any]] = Field(None, description='查询参数')
    body: Optional[Dict[str, Any]] = Field(None, description='请求体')
    body_type: Optional[str] = Field('json', description='请求体类型')
    assertions: Optional[List[Dict[str, Any]]] = Field(None, description='断言规则')
    pre_script: Optional[str] = Field(None, description='前置脚本')
    post_script: Optional[str] = Field(None, description='后置脚本')
    variables: Optional[Dict[str, Any]] = Field(None, description='变量')
    environment_id: Optional[int] = Field(None, description='环境 ID')
    priority: int = Field(2, ge=1, le=3, description='优先级: 1=高 2=中 3=低')
    tags: Optional[List[str]] = Field(None, description='标签')


class ApiTestCaseUpdate(BaseModel):
    """更新 API 测试用例"""
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    collection_id: Optional[int] = None
    description: Optional[str] = Field(None, max_length=1000)
    method: Optional[str] = None
    url: Optional[str] = Field(None, min_length=1)
    headers: Optional[Dict[str, Any]] = None
    params: Optional[Dict[str, Any]] = None
    body: Optional[Dict[str, Any]] = None
    body_type: Optional[str] = None
    assertions: Optional[List[Dict[str, Any]]] = None
    pre_script: Optional[str] = None
    post_script: Optional[str] = None
    variables: Optional[Dict[str, Any]] = None
    environment_id: Optional[int] = None
    priority: Optional[int] = Field(None, ge=1, le=3)
    tags: Optional[List[str]] = None


class ApiTestCaseResponse(BaseModel):
    """API 测试用例响应"""
    id: int
    name: str
    description: Optional[str]
    method: str
    url: str
    headers: Optional[Dict[str, Any]]
    params: Optional[Dict[str, Any]]
    body: Optional[Dict[str, Any]]
    body_type: Optional[str]
    assertions: Optional[List[Dict[str, Any]]]
    pre_script: Optional[str]
    post_script: Optional[str]
    variables: Optional[Dict[str, Any]]
    environment_id: Optional[int]
    priority: int
    tags: Optional[List[str]]
    collection_id: Optional[int]
    project_id: Optional[int]
    user_id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = {"from_attributes": True}