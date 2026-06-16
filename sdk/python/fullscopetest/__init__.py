"""
FullScopeTest Python SDK

提供 FullScopeTestClient 类，用于 CI/CD 集成和自动化。

用法：
    from fullscopetest import FullScopeTestClient

    client = FullScopeTestClient(base_url="http://localhost:8000", api_token="your-token")

    # 创建测试运行
    run = client.create_test_run(project_id=1, test_type="api")

    # 查询结果
    result = client.get_test_run(run["id"])

    # 创建用例
    case = client.create_test_case(project_id=1, name="Login Test", method="POST", url="https://api.example.com/login")
"""

from .client import FullScopeTestClient

__version__ = "1.0.0"
__all__ = ["FullScopeTestClient"]