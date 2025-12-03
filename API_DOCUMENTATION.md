# 接口测试平台 API 文档

**版本**: v1.0  
**更新时间**: 2025-12-07  
**文档用途**: 前端开发者、API 集成者的参考文档

---

## 目录

1. [基础信息](#基础信息)
2. [认证](#认证)
3. [API 端点](#api-端点)
4. [环境管理 API](#环境管理-api)
5. [集合管理 API](#集合管理-api)
6. [请求管理 API](#请求管理-api)
7. [核心功能 API](#核心功能-api)
8. [错误处理](#错误处理)
9. [使用示例](#使用示例)

---

## 基础信息

### 服务器地址

| 环境 | 地址 | 说明 |
|------|------|------|
| 开发 | `http://localhost:5000` | 本地开发环境 |
| 生产 | `https://api.example.com` | 生产环境地址（示例） |

### 请求格式

所有请求都应该使用 `Content-Type: application/json` 头。

```bash
curl -X GET http://localhost:5000/api/environments \
  -H "Content-Type: application/json"
```

### 响应格式

所有 API 响应都返回 JSON 格式：

```json
{
  "success": true,
  "data": {...},
  "message": "成功",
  "timestamp": "2025-12-07T15:30:45.123456"
}
```

---

## 认证

当前版本**不需要认证**，所有 API 端点都是公开的。

⚠️ **生产环境建议**：添加 JWT Token 或 API Key 认证。

---

## API 端点

### 快速索引

| 分类 | HTTP 方法 | 端点 | 功能 |
|------|----------|------|------|
| **环境** | GET | `/api/environments` | 列出所有环境 |
| | POST | `/api/environments` | 创建环境 |
| | PUT | `/api/environments/<id>` | 更新环境 |
| | DELETE | `/api/environments/<id>` | 删除环境 |
| **集合** | GET | `/api/collections` | 列出所有集合 |
| | POST | `/api/collections` | 创建集合 |
| | GET | `/api/collections/<id>` | 获取集合详情 |
| | PUT | `/api/collections/<id>` | 更新集合 |
| | DELETE | `/api/collections/<id>` | 删除集合 |
| **请求** | GET | `/api/requests/<id>` | 获取单个请求 |
| | POST | `/api/requests` | 创建请求 |
| | PUT | `/api/requests/<id>` | 更新请求 |
| | DELETE | `/api/requests/<id>` | 删除请求 |
| **核心** | **POST** | **`/api/send`** | ⭐ **发送 HTTP 请求** |
| | POST | `/api/run-tests` | 运行测试集合 |
| | GET | `/api/reports` | 获取测试报告 |
| | GET | `/api/health` | 健康检查 |

---

## 环境管理 API

### 获取所有环境

```
GET /api/environments
```

**响应示例**：

```json
[
  {
    "id": 1,
    "name": "开发环境",
    "base_url": "https://dev.api.example.com",
    "headers": {
      "Authorization": "Bearer token123",
      "X-API-Key": "key123"
    },
    "variables": {
      "version": "v1",
      "user_id": "123"
    },
    "created_at": "2025-12-07T15:30:45.123456"
  },
  {
    "id": 2,
    "name": "测试环境",
    "base_url": "https://test.api.example.com",
    ...
  }
]
```

---

### 创建环境

```
POST /api/environments
Content-Type: application/json

{
  "name": "生产环境",
  "base_url": "https://api.example.com",
  "headers": {
    "Authorization": "Bearer token123"
  },
  "variables": {
    "version": "v1"
  }
}
```

**响应**：

```json
{
  "id": 3,
  "message": "环境创建成功"
}
```

**错误响应** (400)：

```json
{
  "success": false,
  "error": "环境名称已存在"
}
```

---

### 更新环境

```
PUT /api/environments/1
Content-Type: application/json

{
  "name": "开发环境 V2",
  "base_url": "https://dev-v2.api.example.com",
  "headers": {...},
  "variables": {...}
}
```

---

### 删除环境

```
DELETE /api/environments/1
```

---

## 集合管理 API

### 获取所有集合

```
GET /api/collections
```

**响应**：

```json
[
  {
    "id": 1,
    "env_id": 1,
    "name": "用户管理 API",
    "description": "用户相关的 API 接口",
    "created_at": "2025-12-07T15:30:45.123456",
    "updated_at": "2025-12-07T15:30:45.123456",
    "request_count": 5
  }
]
```

---

### 创建集合

```
POST /api/collections
Content-Type: application/json

{
  "name": "订单管理 API",
  "description": "订单相关的 API 接口",
  "env_id": 1
}
```

---

### 获取集合详情

```
GET /api/collections/1
```

**响应**：

```json
{
  "id": 1,
  "name": "用户管理 API",
  "description": "用户相关的 API 接口",
  "requests": [
    {
      "id": 1,
      "name": "获取用户列表",
      "method": "GET",
      "url": "{{base_url}}/api/users",
      ...
    }
  ]
}
```

---

## 请求管理 API

### 创建请求

```
POST /api/requests
Content-Type: application/json

{
  "collection_id": 1,
  "name": "创建新用户",
  "method": "POST",
  "url": "{{base_url}}/api/users",
  "headers": {
    "Content-Type": "application/json"
  },
  "body": {
    "name": "John",
    "email": "john@example.com"
  },
  "params": {},
  "description": "创建一个新用户"
}
```

---

### 更新请求

```
PUT /api/requests/1
Content-Type: application/json

{
  "name": "创建新用户 (更新)",
  "method": "POST",
  "url": "{{base_url}}/api/users/new",
  ...
}
```

---

### 删除请求

```
DELETE /api/requests/1
```

---

## 核心功能 API

### ⭐ 发送 HTTP 请求（最重要！）

```
POST /api/send
Content-Type: application/json
```

#### 请求体

```json
{
  "method": "POST",
  "url": "{{base_url}}/api/users",
  "headers": {
    "Content-Type": "application/json",
    "Authorization": "Bearer token123"
  },
  "body": {
    "name": "John",
    "email": "john@example.com"
  },
  "params": {
    "page": 1,
    "limit": 10
  },
  "environment": {
    "id": 1,
    "name": "开发环境",
    "base_url": "https://dev.api.example.com"
  }
}
```

#### 响应 - 成功 (200)

```json
{
  "success": true,
  "response": {
    "status_code": 200,
    "headers": {
      "Content-Type": "application/json",
      "Server": "nginx/1.21.0"
    },
    "body": "{\"id\": 123, \"name\": \"John\"}",
    "body_json": {
      "id": 123,
      "name": "John"
    },
    "time": 0.234
  },
  "timestamp": "2025-12-07T15:30:45.123456"
}
```

#### 响应 - 错误 (400)

```json
{
  "success": false,
  "error": "ConnectionError: [Errno -2] Name or service not known",
  "timestamp": "2025-12-07T15:30:45.123456"
}
```

#### URL 环境变量支持

支持在 URL 中使用环境变量：

| 格式 | 说明 | 示例 |
|------|------|------|
| `{{base_url}}` | 环境的 base_url | `{{base_url}}/api/users` |
| `{{var_name}}` | 自定义环境变量 | `{{base_url}}/{{version}}/users` |

---

### 运行测试集合

```
POST /api/run-tests
Content-Type: application/json

{
  "collection_id": 1
}
```

**响应**：

```json
{
  "success": true,
  "return_code": 0,
  "report_url": "/allure-report/index.html"
}
```

---

### 获取测试报告

```
GET /api/reports
```

**响应**：

```json
[
  {
    "id": "report_001",
    "collection_name": "用户管理 API",
    "timestamp": "2025-12-07T15:30:45.123456",
    "pass": 8,
    "fail": 2,
    "url": "/allure-report/report_001/index.html"
  }
]
```

---

### 健康检查

```
GET /api/health
```

**响应**：

```json
{
  "status": "ok",
  "timestamp": "2025-12-07T15:30:45.123456"
}
```

---

## 错误处理

### 错误响应格式

所有错误响应都遵循以下格式：

```json
{
  "success": false,
  "error": "错误信息描述",
  "timestamp": "2025-12-07T15:30:45.123456"
}
```

### 常见 HTTP 状态码

| 状态码 | 含义 | 常见原因 |
|--------|------|---------|
| 200 | OK | 请求成功 |
| 201 | Created | 资源创建成功 |
| 400 | Bad Request | 请求参数错误、目标 API 错误 |
| 404 | Not Found | 资源不存在 |
| 500 | Internal Server Error | 服务器内部错误 |

### 常见错误

#### 1. URL 不能为空

```json
{
  "success": false,
  "error": "URL 不能为空"
}
```

**原因**：请求没有提供 URL  
**解决**：确保请求体中包含 `url` 字段

---

#### 2. 连接错误

```json
{
  "success": false,
  "error": "ConnectionError: [Errno -2] Name or service not known"
}
```

**原因**：目标服务器无法连接  
**解决**：
- 检查 base_url 是否正确
- 检查目标服务器是否在线
- 检查网络连接

---

#### 3. SSL 证书错误

```json
{
  "success": false,
  "error": "SSLError(1, '[SSL: TLSV1_ALERT_INTERNAL_ERROR]...')"
}
```

**原因**：目标服务器的 SSL 证书配置有问题  
**解决**：联系目标服务器管理员

---

#### 4. 超时错误

```json
{
  "success": false,
  "error": "ReadTimeout: HTTPSConnectionPool read timed out"
}
```

**原因**：请求超过 15 秒  
**解决**：检查目标服务器是否响应缓慢

---

## 使用示例

### 示例 1：发送简单的 GET 请求

```bash
curl -X POST http://localhost:5000/api/send \
  -H "Content-Type: application/json" \
  -d '{
    "method": "GET",
    "url": "https://api.example.com/users",
    "headers": {
      "Authorization": "Bearer token123"
    },
    "environment": {
      "id": 1,
      "name": "开发环境",
      "base_url": "https://api.example.com"
    }
  }'
```

---

### 示例 2：发送 POST 请求（带请求体）

```bash
curl -X POST http://localhost:5000/api/send \
  -H "Content-Type: application/json" \
  -d '{
    "method": "POST",
    "url": "{{base_url}}/api/users",
    "headers": {
      "Content-Type": "application/json",
      "Authorization": "Bearer token123"
    },
    "body": {
      "name": "John Doe",
      "email": "john@example.com"
    },
    "environment": {
      "id": 1,
      "name": "开发环境",
      "base_url": "https://dev.api.example.com"
    }
  }'
```

---

### 示例 3：Python 客户端代码

```python
import requests
import json

# 配置
API_URL = "http://localhost:5000/api/send"
HEADERS = {"Content-Type": "application/json"}

# 请求数据
payload = {
    "method": "POST",
    "url": "{{base_url}}/api/users",
    "headers": {"Content-Type": "application/json"},
    "body": {"name": "John", "email": "john@example.com"},
    "environment": {
        "id": 1,
        "name": "开发环境",
        "base_url": "https://dev.api.example.com"
    }
}

# 发送请求
response = requests.post(API_URL, headers=HEADERS, json=payload)
result = response.json()

# 处理结果
if result['success']:
    print("✅ 请求成功")
    print(f"状态码: {result['response']['status_code']}")
    print(f"响应: {result['response']['body_json']}")
else:
    print(f"❌ 请求失败: {result['error']}")
```

---

### 示例 4：JavaScript/Fetch 代码

```javascript
const payload = {
    method: 'POST',
    url: '{{base_url}}/api/users',
    headers: { 'Content-Type': 'application/json' },
    body: { name: 'John', email: 'john@example.com' },
    environment: {
        id: 1,
        name: '开发环境',
        base_url: 'https://dev.api.example.com'
    }
};

fetch('/api/send', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload)
})
.then(response => response.json())
.then(result => {
    if (result.success) {
        console.log('✅ 请求成功:', result.response);
    } else {
        console.log('❌ 请求失败:', result.error);
    }
});
```

---

## 最佳实践

### 1. 环境管理

- 为不同的环境（开发、测试、生产）创建独立的环境配置
- 在环境变量中存储敏感信息（Token、API Key）
- 定期更新环境配置

### 2. 请求组织

- 使用集合来逻辑性地组织相关的请求
- 为每个请求提供清晰的名称和描述
- 使用 URL 环境变量减少重复代码

### 3. 错误处理

- 始终检查 `success` 字段
- 记录详细的错误信息用于调试
- 实现重试机制处理临时网络错误

### 4. 安全性

- 不要在请求中硬编码 Token 或密钥
- 使用环境变量存储敏感信息
- 定期轮换认证凭证

---

## 常见问题 (FAQ)

**Q: 如何使用环境变量？**  
A: 在 URL 中使用 `{{variable_name}}` 的格式，例如 `{{base_url}}/api/users`。确保在环境配置中定义了对应的变量。

---

**Q: 支持哪些 HTTP 方法？**  
A: 支持所有标准 HTTP 方法：GET、POST、PUT、DELETE、PATCH、HEAD 等。

---

**Q: 请求超时时间是多少？**  
A: 默认 15 秒。如果目标 API 响应较慢，可能会超时。

---

**Q: 是否支持文件上传？**  
A: 当前版本不支持。你可以通过在 `body` 中发送 base64 编码的文件内容。

---

**Q: 日志在哪里？**  
A: 日志文件位于 `temp/logs/` 目录下，按日期命名。同时也会输出到控制台。

---

## 版本历史

| 版本 | 日期 | 更改 |
|------|------|------|
| v1.0 | 2025-12-07 | 初始版本发布 |

---

## 支持

如有问题，请检查：
1. 服务器日志（`temp/logs/`）
2. 浏览器控制台（F12 -> Console）
3. 后端日志输出

---

**文档结束**
