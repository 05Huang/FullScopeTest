"""
协议扩展测试（gRPC/GraphQL/WebSocket）
"""

import pytest


class TestGrpcExecutor:
    """gRPC 执行器测试"""

    def test_grpc_test_case_to_dict(self, app):
        """gRPC 用例序列化"""
        with app.app_context():
            from app.services.grpc_executor import GrpcTestCase
            case = GrpcTestCase(
                name="test_login", service="UserService", method="Login",
                request_data={"username": "test"}, server_address="localhost:50051",
            )
            d = case.to_dict()
            assert d["name"] == "test_login"
            assert d["service"] == "UserService"

    def test_grpc_test_case_from_dict(self, app):
        """gRPC 用例反序列化"""
        with app.app_context():
            from app.services.grpc_executor import GrpcTestCase
            data = {"name": "test", "service": "Svc", "method": "Mtd", "request_data": {}}
            case = GrpcTestCase.from_dict(data)
            assert case.name == "test"
            assert case.service == "Svc"

    def test_grpc_parse_proto(self, app):
        """解析 proto 文件"""
        with app.app_context():
            from app.services.grpc_executor import GrpcExecutor
            executor = GrpcExecutor()
            proto = """service UserService {
    rpc Login (LoginRequest) returns (LoginResponse);
    rpc GetUser (GetUserRequest) returns (User);
}
message LoginRequest {
    string username = 1;
}
message LoginResponse {
    string token = 1;
}"""
            result = executor.parse_proto(proto)
            assert len(result["services"]) == 1
            assert result["services"][0]["name"] == "UserService"
            assert "Login" in result["services"][0]["methods"]
            assert len(result["messages"]) >= 2

    def test_grpc_simulated_execution(self, app):
        """gRPC 模拟执行"""
        with app.app_context():
            from app.services.grpc_executor import GrpcTestCase
            case = GrpcTestCase(
                name="test", service="Svc", method="Mtd",
                request_data={"key": "value"},
            )
            result = case.execute()
            assert "passed" in result
            assert "duration_ms" in result


class TestGraphQLExecutor:
    """GraphQL 执行器测试"""

    def test_graphql_test_case_to_dict(self, app):
        """GraphQL 用例序列化"""
        with app.app_context():
            from app.services.graphql_executor import GraphQLTestCase
            case = GraphQLTestCase(
                name="test_query", endpoint="http://localhost:4000/graphql",
                query="query { users { id name } }",
            )
            d = case.to_dict()
            assert d["name"] == "test_query"
            assert "users" in d["query"]

    def test_graphql_test_case_from_dict(self, app):
        """GraphQL 用例反序列化"""
        with app.app_context():
            from app.services.graphql_executor import GraphQLTestCase
            data = {"name": "test", "endpoint": "http://localhost:4000", "query": "{ hello }"}
            case = GraphQLTestCase.from_dict(data)
            assert case.query == "{ hello }"

    def test_graphql_validate_no_errors(self, app):
        """验证无错误的 GraphQL 响应"""
        with app.app_context():
            from app.services.graphql_executor import GraphQLTestCase
            case = GraphQLTestCase(assertions=[{"type": "no_errors"}])
            assert case._validate_response(200, {"data": {"users": []}}) is True
            assert case._validate_response(200, {"errors": [{"message": "error"}]}) is False

    def test_graphql_validate_data_path(self, app):
        """验证数据路径断言"""
        with app.app_context():
            from app.services.graphql_executor import GraphQLTestCase
            case = GraphQLTestCase(assertions=[{"type": "data_path", "path": "user.name", "expected": "test"}])
            response = {"data": {"user": {"name": "test"}}}
            assert case._validate_response(200, response) is True


class TestWebSocketExecutor:
    """WebSocket 执行器测试"""

    def test_ws_test_case_to_dict(self, app):
        """WebSocket 用例序列化"""
        with app.app_context():
            from app.services.ws_executor import WebSocketTestCase
            case = WebSocketTestCase(
                name="test_ws", url="ws://localhost:8080/ws",
                messages=[{"type": "send", "data": "hello"}],
            )
            d = case.to_dict()
            assert d["url"] == "ws://localhost:8080/ws"
            assert len(d["messages"]) == 1

    def test_ws_test_case_from_dict(self, app):
        """WebSocket 用例反序列化"""
        with app.app_context():
            from app.services.ws_executor import WebSocketTestCase
            data = {"name": "test", "url": "ws://localhost:8080", "messages": []}
            case = WebSocketTestCase.from_dict(data)
            assert case.url == "ws://localhost:8080"

    def test_ws_validate_contains(self, app):
        """WebSocket 消息断言（contains）"""
        with app.app_context():
            from app.services.ws_executor import WebSocketTestCase
            case = WebSocketTestCase(assertions=[{"type": "contains", "value": "hello"}])
            assert case._validate_message("hello world", [{"type": "contains", "value": "hello"}]) is True
            assert case._validate_message("goodbye", [{"type": "contains", "value": "hello"}]) is False

    def test_ws_validate_json_path(self, app):
        """WebSocket JSON 路径断言"""
        with app.app_context():
            from app.services.ws_executor import WebSocketTestCase
            case = WebSocketTestCase()
            msg = '{"type": "response", "data": {"status": "ok"}}'
            assert case._validate_message(msg, [{"type": "json_path", "path": "data.status", "expected": "ok"}]) is True
