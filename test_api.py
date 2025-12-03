import requests
import json

# 调用 /api/environments 端点
response = requests.get('http://localhost:5000/api/environments')

if response.status_code == 200:
    data = response.json()
    print('=== API 返回的数据 ===\n')
    print(json.dumps(data, indent=2, ensure_ascii=False))
    
    for env in data:
        print(f'\n--- {env["name"]} 环境 ---')
        print(f'Headers 类型: {type(env.get("headers"))}')
        print(f'Headers 数量: {len(env.get("headers", {}))}')
        if isinstance(env.get("headers"), dict):
            print(f'Headers 内容: {list(env.get("headers", {}).keys())}')
        else:
            print(f'Headers 原始值: {env.get("headers")[:100]}')
else:
    print(f'请求失败: {response.status_code}')
