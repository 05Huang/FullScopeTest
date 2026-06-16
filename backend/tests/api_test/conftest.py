"""
API 测试模块测试 fixtures

提供项目、集合和用例的测试数据。
"""
import pytest


@pytest.fixture()
def sample_project(client, auth_headers):
    """创建测试项目"""
    resp = client.post("/api/v1/projects", json={
        "name": "API Test Project",
        "description": "用于测试的项目",
    }, headers=auth_headers)
    assert resp.status_code in (200, 201)
    data = resp.get_json()
    return data.get("data", {})


@pytest.fixture()
def sample_collection(client, auth_headers, sample_project):
    """创建测试集合"""
    resp = client.post("/api/v1/api-test/collections", json={
        "name": "Test Collection",
        "project_id": sample_project["id"],
        "description": "测试集合",
    }, headers=auth_headers)
    assert resp.status_code in (200, 201)
    data = resp.get_json()
    return data.get("data", {})


@pytest.fixture()
def sample_case(client, auth_headers, sample_project, sample_collection):
    """创建测试用例"""
    resp = client.post("/api/v1/api-test/cases", json={
        "name": "Sample GET Request",
        "method": "GET",
        "url": "https://httpbin.org/get",
        "collection_id": sample_collection["id"],
        "project_id": sample_project["id"],
    }, headers=auth_headers)
    assert resp.status_code in (200, 201)
    data = resp.get_json()
    return data.get("data", {})
