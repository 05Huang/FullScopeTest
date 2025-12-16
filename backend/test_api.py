"""
测试后端 API
"""

import requests
import json

BASE_URL = 'http://127.0.0.1:5211/api/v1'

def test_login():
    """测试登录"""
    print("=" * 50)
    print("测试登录...")
    response = requests.post(
        f'{BASE_URL}/auth/login',
        json={'username': 'admin', 'password': 'admin123'}
    )
    print(f"状态码: {response.status_code}")
    print(f"响应: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    
    if response.status_code == 200:
        return response.json()['data']['access_token']
    return None

def test_get_projects(token):
    """测试获取项目列表"""
    print("=" * 50)
    print("测试获取项目列表...")
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(f'{BASE_URL}/projects', headers=headers)
    print(f"状态码: {response.status_code}")
    print(f"响应: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")

def test_create_project(token):
    """测试创建项目"""
    print("=" * 50)
    print("测试创建项目...")
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.post(
        f'{BASE_URL}/projects',
        json={'name': '测试项目', 'description': '这是一个测试项目'},
        headers=headers
    )
    print(f"状态码: {response.status_code}")
    print(f"响应: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    
    if response.status_code in (200, 201):
        return response.json()['data']['id']
    return None

if __name__ == '__main__':
    # 测试登录
    token = test_login()
    
    if token:
        # 测试获取项目列表
        test_get_projects(token)
        
        # 测试创建项目
        project_id = test_create_project(token)
        
        # 再次获取项目列表
        if project_id:
            test_get_projects(token)
    else:
        print("登录失败，无法继续测试")
