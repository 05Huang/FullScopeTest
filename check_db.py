import sqlite3
import json

conn = sqlite3.connect('web/instance/test_cases.db')
cursor = conn.cursor()

# 查询所有表
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()

print('=== 数据库中的所有表 ===')
for table in tables:
    print(f'  - {table[0]}')

# 查询 environments 表中的数据
print('\n=== Environments 表中的数据 ===')
cursor.execute('SELECT id, name, base_url, headers, variables FROM environments')
rows = cursor.fetchall()

for row in rows:
    env_id, name, base_url, headers, variables = row
    print(f'\n--- 环境: {name} ---')
    print(f'ID: {env_id}')
    print(f'Base URL: {base_url}')
    
    # 解析 JSON
    try:
        headers_dict = json.loads(headers) if headers else {}
        print(f'Headers ({len(headers_dict)} 个):')
        for key, val in list(headers_dict.items())[:10]:
            print(f'  {key}: {val}')
        if len(headers_dict) > 10:
            print(f'  ... 还有 {len(headers_dict) - 10} 个')
    except Exception as e:
        print(f'Headers 解析失败: {e}')
        print(f'原始数据: {headers[:100]}')
    
    try:
        variables_dict = json.loads(variables) if variables else {}
        print(f'Variables ({len(variables_dict)} 个):')
        for key, val in variables_dict.items():
            print(f'  {key}: {val}')
    except Exception as e:
        print(f'Variables 解析失败: {e}')
        print(f'原始数据: {variables}')

conn.close()
