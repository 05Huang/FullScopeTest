"""Tests for FastAPI OpenAPI documentation enhancement module"""

import uuid
import pytest
from fastapi.testclient import TestClient
from app.fastapi_app import create_fastapi_app


@pytest.fixture()
def v2_client(app):
    fastapi_app = create_fastapi_app("testing", flask_app=app)
    with app.app_context():
        from app.extensions import db as flask_db
        flask_db.create_all()
        client = TestClient(fastapi_app)
        client.flask_app = app
        yield client


def _register_and_login(client, username=None):
    if username is None:
        username = f"v2openapi_{uuid.uuid4().hex[:8]}"
    email = f"{username}@example.com"
    client.post("/api/v2/auth/register", json={"username": username, "email": email, "password": "Str0ng!Pass"})
    resp = client.post("/api/v2/auth/login", json={"username": username, "password": "Str0ng!Pass"})
    data = resp.json()
    return {"username": username, "access_token": data["access_token"]}


class TestV2OpenAPIDocs:
    def test_postman_export_unauthorized(self, v2_client):
        resp = v2_client.get("/api/v2/openapi/postman")
        assert resp.status_code == 200

    def test_postman_export_returns_valid_json(self, v2_client):
        resp = v2_client.get("/api/v2/openapi/postman")
        assert resp.status_code == 200
        data = resp.json()
        assert "info" in data
        assert "item" in data
        assert data["info"]["name"] == "FullScopeTest API v2"
        assert data["info"]["schema"] == "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"

    def test_postman_export_has_auth(self, v2_client):
        resp = v2_client.get("/api/v2/openapi/postman")
        data = resp.json()
        assert "auth" in data
        assert data["auth"]["type"] == "bearer"

    def test_postman_export_has_variables(self, v2_client):
        resp = v2_client.get("/api/v2/openapi/postman")
        data = resp.json()
        assert "variable" in data
        var_keys = [v["key"] for v in data["variable"]]
        assert "base_url" in var_keys
        assert "access_token" in var_keys

    def test_metersphere_export_unauthorized(self, v2_client):
        resp = v2_client.get("/api/v2/openapi/metersphere")
        assert resp.status_code == 200

    def test_metersphere_export_returns_valid_json(self, v2_client):
        resp = v2_client.get("/api/v2/openapi/metersphere")
        assert resp.status_code == 200
        data = resp.json()
        assert "project_name" in data
        assert "modules" in data
        assert data["project_name"] == "FullScopeTest"
        assert data["version"] == "2.0.0"

    def test_metersphere_export_has_modules(self, v2_client):
        resp = v2_client.get("/api/v2/openapi/metersphere")
        data = resp.json()
        assert len(data["modules"]) > 0
        module_names = [m["name"] for m in data["modules"]]
        assert "auth" in module_names

    def test_schema_export(self, v2_client):
        resp = v2_client.get("/api/v2/openapi/schema")
        assert resp.status_code == 200
        data = resp.json()
        assert "openapi" in data
        assert "paths" in data
        assert "components" in data

    def test_stats_export(self, v2_client):
        resp = v2_client.get("/api/v2/openapi/stats")
        assert resp.status_code == 200
        data = resp.json()
        assert "total_endpoints" in data
        assert "by_method" in data
        assert "by_tag" in data
        assert data["total_endpoints"] > 0

    def test_stats_has_expected_tags(self, v2_client):
        resp = v2_client.get("/api/v2/openapi/stats")
        data = resp.json()
        assert "auth" in data["by_tag"]
        assert "test-cases" in data["by_tag"]
        assert "api-tests" in data["by_tag"]

    def test_postman_collection_has_items(self, v2_client):
        resp = v2_client.get("/api/v2/openapi/postman")
        data = resp.json()
        assert len(data["item"]) > 0
        first_item = data["item"][0]
        assert "name" in first_item
        assert "item" in first_item
