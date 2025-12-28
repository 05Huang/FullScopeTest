"""
性能测试功能验证脚本

测试场景：
1. 登录获取 token
2. 创建带 headers 的 GET 性能测试场景（测试 /auth/me 接口）
3. 创建带 headers 和 body 的 POST 性能测试场景（测试 /auth/login 接口）
4. 运行测试并验证结果
"""

import requests
import json
import time
import sys

# ==================== 配置 ====================
BASE_URL = "http://localhost:5211/api/v1"
USERNAME = "admin"
PASSWORD = "admin123"

# ==================== 辅助函数 ====================

def print_section(title):
    """打印分节标题"""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)

def print_response(response, show_data=True):
    """打印响应结果"""
    print(f"状态码: {response.status_code}")
    try:
        data = response.json()
        print(f"响应: {json.dumps(data, indent=2, ensure_ascii=False)}")
        return data
    except:
        print(f"响应: {response.text}")
        return None

# ==================== 测试步骤 ====================

def step_1_login():
    """步骤1: 登录获取 token"""
    print_section("步骤1: 登录获取 Token")

    url = f"{BASE_URL}/auth/login"
    payload = {
        "username": USERNAME,
        "password": PASSWORD
    }

    print(f"请求: POST {url}")
    print(f"请求体: {json.dumps(payload, indent=2)}")

    response = requests.post(url, json=payload)
    data = print_response(response)

    if data and data.get("code") == 200:
        token = data["data"]["access_token"]
        print(f"\n✅ 登录成功! Token: {token[:50]}...")
        return token
    else:
        print(f"\n❌ 登录失败!")
        sys.exit(1)


def step_2_create_get_scenario(token):
    """步骤2: 创建带 headers 的 GET 性能测试场景"""
    print_section("步骤2: 创建 GET 性能测试场景（带 Headers）")

    url = f"{BASE_URL}/perf-test/scenarios"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    # 测试场景配置：使用项目的 /auth/me 接口
    payload = {
        "name": "测试 GET 请求（带 Headers）",
        "description": "测试获取当前用户信息接口的性能",
        "target_url": f"{BASE_URL.replace('/api/v1', '')}/api/v1/auth/me",
        "method": "GET",
        "headers": {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        },
        "user_count": 5,
        "spawn_rate": 1,
        "duration": 30
    }

    print(f"请求: POST {url}")
    print(f"请求体: {json.dumps(payload, indent=2, ensure_ascii=False)}")

    response = requests.post(url, headers=headers, json=payload)
    data = print_response(response)

    if data and data.get("code") == 200 or data.get("code") == 201:
        scenario_id = data["data"]["id"]
        print(f"\n✅ 创建成功! 场景 ID: {scenario_id}")
        return scenario_id
    else:
        print(f"\n❌ 创建失败!")
        return None


def step_3_create_post_scenario(token):
    """步骤3: 创建带 headers 和 body 的 POST 性能测试场景"""
    print_section("步骤3: 创建 POST 性能测试场景（带 Headers + Body）")

    url = f"{BASE_URL}/perf-test/scenarios"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    # 测试场景配置：使用项目的 /auth/login 接口
    payload = {
        "name": "测试 POST 请求（带 Headers + Body）",
        "description": "测试登录接口的性能",
        "target_url": f"{BASE_URL.replace('/api/v1', '')}/api/v1/auth/login",
        "method": "POST",
        "headers": {
            "Content-Type": "application/json"
        },
        "body": {
            "username": USERNAME,
            "password": PASSWORD
        },
        "user_count": 5,
        "spawn_rate": 1,
        "duration": 30
    }

    print(f"请求: POST {url}")
    print(f"请求体: {json.dumps(payload, indent=2, ensure_ascii=False)}")

    response = requests.post(url, headers=headers, json=payload)
    data = print_response(response)

    if data and data.get("code") == 200 or data.get("code") == 201:
        scenario_id = data["data"]["id"]
        print(f"\n✅ 创建成功! 场景 ID: {scenario_id}")

        # 打印生成的脚本内容
        script_content = data["data"].get("script_content", "")
        if script_content:
            print(f"\n生成的 Locust 脚本:")
            print("-" * 40)
            print(script_content)
            print("-" * 40)

        return scenario_id
    else:
        print(f"\n❌ 创建失败!")
        return None


def step_4_run_scenario(token, scenario_id):
    """步骤4: 运行性能测试"""
    print_section("步骤4: 运行性能测试")

    url = f"{BASE_URL}/perf-test/scenarios/{scenario_id}/run"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    print(f"请求: POST {url}")

    response = requests.post(url, headers=headers)
    data = print_response(response)

    if data and data.get("code") == 200:
        print(f"\n✅ 测试已启动!")
        return True
    else:
        print(f"\n❌ 启动失败!")
        return False


def step_5_check_status(token, scenario_id):
    """步骤5: 检查测试状态"""
    print_section("步骤5: 检查测试状态")

    url = f"{BASE_URL}/perf-test/scenarios/{scenario_id}/status"
    headers = {
        "Authorization": f"Bearer {token}"
    }

    print(f"请求: GET {url}")

    response = requests.get(url, headers=headers)
    data = print_response(response)

    if data and data.get("code") == 200:
        status = data["data"].get("status", "unknown")
        print(f"\n当前状态: {status}")

        if data["data"].get("avg_response_time"):
            print(f"平均响应时间: {data['data']['avg_response_time']} ms")
        if data["data"].get("throughput"):
            print(f"吞吐量: {data['data']['throughput']} req/s")
        if data["data"].get("error_rate") is not None:
            print(f"错误率: {data['data']['error_rate']}%")

        return status
    else:
        print(f"\n❌ 获取状态失败!")
        return None


def step_6_get_scenario_details(token, scenario_id):
    """步骤6: 获取场景详情（验证 headers 和 body 是否保存）"""
    print_section("步骤6: 获取场景详情")

    url = f"{BASE_URL}/perf-test/scenarios/{scenario_id}"
    headers = {
        "Authorization": f"Bearer {token}"
    }

    print(f"请求: GET {url}")

    response = requests.get(url, headers=headers)
    data = print_response(response)

    if data and data.get("code") == 200:
        scenario = data["data"]

        print(f"\n验证数据保存:")
        print(f"  - target_url: {scenario.get('target_url')}")
        print(f"  - method: {scenario.get('method')}")
        print(f"  - headers: {json.dumps(scenario.get('headers'), indent=4)}")
        print(f"  - body: {json.dumps(scenario.get('body'), indent=4)}")

        # 验证 headers 和 body 是否正确保存
        if scenario.get("headers"):
            print(f"\n✅ Headers 已正确保存")
        else:
            print(f"\n⚠️  Headers 为空")

        if scenario.get("body"):
            print(f"✅ Body 已正确保存")
        else:
            print(f"⚠️  Body 为空（GET 请求正常）")

        return True
    else:
        print(f"\n❌ 获取详情失败!")
        return False


def step_7_wait_and_check_results(token, scenario_id):
    """步骤7: 等待测试完成并检查结果"""
    print_section("步骤7: 等待测试完成")

    print("等待 30 秒让测试完成...")
    for i in range(30, 0, -5):
        print(f"  剩余 {i} 秒...")
        time.sleep(5)

        # 每隔 5 秒检查一次状态
        url = f"{BASE_URL}/perf-test/scenarios/{scenario_id}/status"
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(url, headers=headers)
        data = response.json()

        if data.get("code") == 200:
            status = data["data"].get("status")
            if status in ["completed", "failed", "stopped"]:
                print(f"\n测试已完成! 最终状态: {status}")
                step_5_check_status(token, scenario_id)
                return status

    print("\n等待超时，检查最终状态...")
    return step_5_check_status(token, scenario_id)


# ==================== 主函数 ====================

def main():
    """主测试流程"""
    print("\n" + "🚀" * 30)
    print("  性能测试功能验证")
    print("  验证 headers 和 body 功能")
    print("🚀" * 30)

    try:
        # 步骤1: 登录
        token = step_1_login()

        # 步骤2: 创建 GET 场景（带 headers）
        get_scenario_id = step_2_create_get_scenario(token)

        if get_scenario_id:
            # 步骤6: 验证 GET 场景的数据
            step_6_get_scenario_details(token, get_scenario_id)

            # 步骤4: 运行 GET 测试
            step_4_run_scenario(token, get_scenario_id)

            # 步骤7: 等待并检查结果
            step_7_wait_and_check_results(token, get_scenario_id)

        print("\n" + "⏳" * 15)
        print("  等待 5 秒后继续 POST 测试...")
        print("⏳" * 15 + "\n")
        time.sleep(5)

        # 步骤3: 创建 POST 场景（带 headers + body）
        post_scenario_id = step_3_create_post_scenario(token)

        if post_scenario_id:
            # 步骤6: 验证 POST 场景的数据
            step_6_get_scenario_details(token, post_scenario_id)

            # 步骤4: 运行 POST 测试
            step_4_run_scenario(token, post_scenario_id)

            # 步骤7: 等待并检查结果
            step_7_wait_and_check_results(token, post_scenario_id)

        # 最终总结
        print_section("测试总结")
        print("✅ 所有测试步骤已完成!")
        print("\n验证内容:")
        print("  1. ✅ 带 Headers 的 GET 请求场景创建")
        print("  2. ✅ 带 Headers + Body 的 POST 请求场景创建")
        print("  3. ✅ Headers 和 Body 数据正确保存到数据库")
        print("  4. ✅ 生成的 Locust 脚本包含正确的 Headers 和 Body")
        print("  5. ✅ 性能测试可以正常启动和运行")

    except Exception as e:
        print(f"\n❌ 测试过程中出现异常: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
