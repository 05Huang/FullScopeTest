import pytest
import yaml
import os
from common.request_util import RequestUtil
import subprocess

@pytest.fixture(scope="session")
def config():
    """读取配置"""
    config_path = os.path.join(os.path.dirname(__file__), "..", "config", "config.yaml")
    with open(config_path, encoding="utf-8") as f:
        cfg = yaml.safe_load(f)["env"]["dev"]
        if "headers" not in cfg:
            cfg["headers"] = {"Content-Type": "application/json"}
        return cfg

@pytest.fixture(scope="session")
def token(config):
    """登录接口获取 token"""
    r = RequestUtil(config["base_url"]).send(
        "POST",
        "/api/test-login",
        headers=config["headers"],
        json={"openid": config["account"]["username"]}
    )
    return r.json().get("token")

@pytest.fixture(scope="session")
def auth_headers(config, token):
    headers = config["headers"].copy()
    headers["Authorization"] = f"Bearer {token}"
    return headers


def pytest_sessionfinish(session, exitstatus):
    """测试结束后自动生成并打开报告"""
    result_dir = "./reports/allure_results"  # 与 pytest.ini 保持一致
    
    if os.path.exists(result_dir) and os.listdir(result_dir):
        # 生成带时间戳的报告目录
        import time
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        report_dir = f"./reports/allure_report_{timestamp}"
        
        # 生成报告
        result = subprocess.run(
            f"allure generate \"{result_dir}\" -o \"{report_dir}\" --clean",
            shell=True,
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print(f"\n[SUCCESS] Allure报告已生成: {report_dir}")
            # 自动打开报告
            subprocess.Popen(f"allure open \"{report_dir}\"", shell=True)
        else:
            print(f"\n[ERROR] 报告生成失败: {result.stderr}")
    else:
        print(f"\n[WARNING] 没有找到Allure结果文件，请检查测试是否正常运行")
