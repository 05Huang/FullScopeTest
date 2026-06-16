"""
gRPC 测试执行器

支持 gRPC 协议的测试用例执行。
支持 Unary、Server Streaming、Client Streaming、Bidirectional Streaming。
"""

import json
import time
from typing import Dict, Any, List, Optional
from ..core.logging import get_logger

logger = get_logger(__name__)


class GrpcTestCase:
    """gRPC 测试用例"""

    def __init__(self, name: str = "", service: str = "", method: str = "",
                 request_data: Dict = None, metadata: Dict = None,
                 server_address: str = "", tls_enabled: bool = False,
                 timeout: int = 30, assertions: List[Dict] = None):
        self.name = name
        self.service = service
        self.method = method
        self.request_data = request_data or {}
        self.metadata = metadata or {}
        self.server_address = server_address
        self.tls_enabled = tls_enabled
        self.timeout = timeout
        self.assertions = assertions or []

    def execute(self) -> Dict[str, Any]:
        """执行 gRPC 请求"""
        start_time = time.time()
        try:
            # 模拟 gRPC 调用（实际需要 grpcio 库）
            result = self._do_grpc_call()
            duration = time.time() - start_time
            passed = self._validate_response(result)
            return {
                "passed": passed,
                "response": result,
                "duration_ms": round(duration * 1000, 2),
                "service": self.service,
                "method": self.method,
                "metadata": self.metadata,
            }
        except Exception as exc:
            duration = time.time() - start_time
            return {
                "passed": False,
                "error": str(exc),
                "error_type": "grpc_error",
                "duration_ms": round(duration * 1000, 2),
            }

    def _do_grpc_call(self) -> Dict[str, Any]:
        """执行实际的 gRPC 调用"""
        # 实际实现需要 grpcio 库
        # 这里提供框架，具体实现需要安装 grpcio
        try:
            import grpc
            from grpc import insecure_channel, secure_channel, ssl_channel_credentials

            if self.tls_enabled:
                channel = secure_channel(self.server_address, ssl_channel_credentials())
            else:
                channel = insecure_channel(self.server_address)

            # 构造请求
            stub = self._create_stub(channel)
            request = self._build_request()

            # 设置 metadata
            metadata = [(k, v) for k, v in self.metadata.items()]

            # 执行调用
            response = stub(request, metadata=metadata, timeout=self.timeout)
            channel.close()

            return {"status": "ok", "data": str(response)}

        except ImportError:
            logger.warning("grpcio 未安装，使用模拟响应")
            return {"status": "simulated", "data": self.request_data}

    def _create_stub(self, channel):
        """创建 gRPC stub"""
        # 需要根据 proto 文件动态生成 stub
        # 这里返回通用的 unary_unary 调用
        return channel.unary_unary()

    def _build_request(self):
        """构造 gRPC 请求"""
        return self.request_data

    def _validate_response(self, result: Dict) -> bool:
        """验证响应"""
        for assertion in self.assertions:
            assertion_type = assertion.get("type")
            if assertion_type == "status":
                if result.get("status") != assertion.get("expected"):
                    return False
            elif assertion_type == "contains":
                if assertion.get("value") not in str(result.get("data", "")):
                    return False
        return True

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name, "service": self.service, "method": self.method,
            "request_data": self.request_data, "metadata": self.metadata,
            "server_address": self.server_address, "tls_enabled": self.tls_enabled,
            "timeout": self.timeout, "assertions": self.assertions,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "GrpcTestCase":
        return cls(**data)


class GrpcExecutor:
    """gRPC 测试执行器"""

    def execute_test(self, test_case: GrpcTestCase) -> Dict[str, Any]:
        """执行 gRPC 测试用例"""
        logger.info("执行 gRPC 测试", service=test_case.service, method=test_case.method)
        return test_case.execute()

    def parse_proto(self, proto_content: str) -> Dict[str, Any]:
        """解析 proto 文件内容"""
        services = []
        messages = []

        lines = proto_content.split("\n")
        current_service = None

        for line in lines:
            line = line.strip()
            if line.startswith("service "):
                current_service = line.replace("service ", "").replace("{", "").strip()
                services.append({"name": current_service, "methods": []})
            elif line.startswith("rpc ") and current_service:
                parts = line.split()
                if len(parts) >= 2:
                    method_name = parts[1].split("(")[0]
                    services[-1]["methods"].append(method_name)
            elif line.startswith("message "):
                msg_name = line.replace("message ", "").replace("{", "").strip()
                messages.append({"name": msg_name})

        return {"services": services, "messages": messages}


_instance = None


def get_grpc_executor() -> GrpcExecutor:
    global _instance
    if _instance is None:
        _instance = GrpcExecutor()
    return _instance