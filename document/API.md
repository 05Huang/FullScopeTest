# EasyTest-Web API 接口文档

> 文档版本：1.0  
> 基础URL：`http://localhost:5211/api/v1`  
> 最后更新：2025-12-28

---

## 目录

1. [概述](#概述)
2. [认证机制](#认证机制)
3. [响应格式](#响应格式)
4. [认证接口](#认证接口)
5. [项目管理](#项目管理)
6. [环境管理](#环境管理)
7. [接口测试](#接口测试)
8. [性能测试](#性能测试)
9. [Web自动化测试](#web自动化测试)
10. [测试报告](#测试报告)
11. [文档管理](#文档管理)

---

## 概述

EasyTest-Web 是一个综合性的测试平台，支持：
- **接口测试**：HTTP/HTTPS 接口的功能测试
- **性能测试**：基于 Locust 的压力测试
- **Web 自动化测试**：基于 Playwright 的 UI 自动化测试

### 测试场景

本项目本身也是一个完整的测试目标，用户可以参照此 API 文档进行以下测试：

1. **使用接口测试功能** - 通过创建 API 测试用例来测试本项目的接口
2. **使用性能测试功能** - 对本项目进行性能压力测试
3. **使用 Web 自动化功能** - 对前端界面进行自动化测试

---

## 认证机制

### JWT Token 认证

所有需要认证的接口都需要在请求头中携带 Bearer Token：

```http
Authorization: Bearer <access_token>
```

### Token 有效期

| Token 类型 | 有效期 |
|-----------|--------|
| Access Token | 24 小时 |
| Refresh Token | 30 天 |

---

## 响应格式

### 成功响应

```json
{
    "success": true,
    "code": 200,
    "message": "操作成功",
    "data": { ... }
}
```

### 分页响应

```json
{
    "success": true,
    "code": 200,
    "data": {
        "items": [ ... ],
        "total": 100,
        "page": 1,
        "per_page": 20,
        "pages": 5
    }
}
```

### 错误响应

```json
{
    "success": false,
    "code": 400,
    "message": "错误描述"
}
```

---

## 认证接口

### 1. 用户注册

**POST** `/auth/register`

**请求体：**

```json
{
    "username": "testuser",
    "email": "test@example.com",
    "password": "password123"
}
```

**参数说明：**

| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| username | string | ✓ | 用户名，3-50字符 |
| email | string | ✓ | 邮箱地址 |
| password | string | ✓ | 密码，至少8字符 |

**成功响应：**

```json
{
    "success": true,
    "code": 201,
    "message": "注册成功",
    "data": {
        "user_id": 1,
        "username": "testuser"
    }
}
```

---

### 2. 用户登录

**POST** `/auth/login`

**请求体：**

```json
{
    "username": "testuser",
    "password": "password123"
}
```

**参数说明：**

| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| username | string | ✓ | 用户名或邮箱 |
| password | string | ✓ | 密码 |

**成功响应：**

```json
{
    "success": true,
    "code": 200,
    "message": "登录成功",
    "data": {
        "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
        "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
        "user": {
            "id": 1,
            "username": "testuser",
            "email": "test@example.com",
            "is_active": true,
            "created_at": "2025-12-27T10:00:00"
        }
    }
}
```

---

### 3. 获取当前用户信息

**GET** `/auth/me`

**请求头：** 需要 Bearer Token

**成功响应：**

```json
{
    "success": true,
    "code": 200,
    "data": {
        "id": 1,
        "username": "testuser",
        "email": "test@example.com",
        "is_active": true,
        "created_at": "2025-12-27T10:00:00",
        "last_login_at": "2025-12-27T12:00:00"
    }
}
```

---

### 4. 刷新 Token

**POST** `/auth/refresh`

**请求头：** 需要 Refresh Token

**成功响应：**

```json
{
    "success": true,
    "code": 200,
    "message": "Token 刷新成功",
    "data": {
        "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
    }
}
```

---

### 5. 修改密码

**PUT** `/auth/password`

**请求头：** 需要 Bearer Token

**请求体：**

```json
{
    "old_password": "password123",
    "new_password": "newpassword456"
}
```

---

## 项目管理

### 1. 获取项目列表

**GET** `/projects`

**请求头：** 需要 Bearer Token

**查询参数：**

| 参数 | 类型 | 默认值 | 描述 |
|------|------|--------|------|
| page | int | 1 | 页码 |
| per_page | int | 20 | 每页数量 |
| keyword | string | - | 搜索关键词 |

**成功响应：**

```json
{
    "success": true,
    "code": 200,
    "data": {
        "items": [
            {
                "id": 1,
                "name": "测试项目",
                "description": "项目描述",
                "owner_id": 1,
                "created_at": "2025-12-27T10:00:00"
            }
        ],
        "total": 1,
        "page": 1,
        "per_page": 20,
        "pages": 1
    }
}
```

---

### 2. 创建项目

**POST** `/projects`

**请求头：** 需要 Bearer Token

**请求体：**

```json
{
    "name": "测试项目",
    "description": "项目描述（可选）"
}
```

**参数说明：**

| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| name | string | ✓ | 项目名称，1-100字符 |
| description | string | ✗ | 项目描述 |

---

### 3. 获取项目详情

**GET** `/projects/{project_id}`

**请求头：** 需要 Bearer Token

---

### 4. 更新项目

**PUT** `/projects/{project_id}`

**请求头：** 需要 Bearer Token

---

### 5. 删除项目

**DELETE** `/projects/{project_id}`

**请求头：** 需要 Bearer Token

---

## 环境管理

### 1. 获取所有环境

**GET** `/environments`

**请求头：** 需要 Bearer Token

**查询参数：**

| 参数 | 类型 | 描述 |
|------|------|------|
| project_id | int | 筛选特定项目的环境 |

---

### 2. 创建环境

**POST** `/environments`

**请求头：** 需要 Bearer Token

**请求体：**

```json
{
    "name": "开发环境",
    "base_url": "http://localhost:5211",
    "project_id": 1,
    "variables": {
        "api_key": "xxx",
        "timeout": "30"
    },
    "headers": {
        "Content-Type": "application/json"
    },
    "is_active": true
}
```

**参数说明：**

| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| name | string | ✓ | 环境名称 |
| base_url | string | ✓ | 基础 URL |
| project_id | int | ✓ | 关联项目 ID |
| variables | object | ✗ | 环境变量 |
| headers | object | ✗ | 公共请求头 |
| is_active | boolean | ✗ | 是否为默认环境 |

---

### 3. 获取项目环境列表

**GET** `/projects/{project_id}/environments`

**请求头：** 需要 Bearer Token

---

### 4. 获取环境详情

**GET** `/environments/{env_id}`

**请求头：** 需要 Bearer Token

---

### 5. 更新环境

**PUT** `/environments/{env_id}`

**请求头：** 需要 Bearer Token

---

### 6. 删除环境

**DELETE** `/environments/{env_id}`

**请求头：** 需要 Bearer Token

---

### 7. 设置默认环境

**POST** `/environments/{env_id}/default`

**请求头：** 需要 Bearer Token

---

## 接口测试

### 健康检查

**GET** `/api-test/health`

**成功响应：**

```json
{
    "success": true,
    "code": 200,
    "message": "接口测试模块正常"
}
```

---

### 用例集合管理

#### 1. 获取用例集合列表

**GET** `/api-test/collections`

**请求头：** 需要 Bearer Token

**查询参数：**

| 参数 | 类型 | 描述 |
|------|------|------|
| project_id | int | 筛选特定项目 |

---

#### 2. 创建用例集合

**POST** `/api-test/collections`

**请求头：** 需要 Bearer Token

**请求体：**

```json
{
    "name": "用户接口集合",
    "description": "用户相关接口测试",
    "project_id": 1
}
```

---

#### 3. 更新用例集合

**PUT** `/api-test/collections/{collection_id}`

**请求头：** 需要 Bearer Token

---

#### 4. 删除用例集合

**DELETE** `/api-test/collections/{collection_id}`

**请求头：** 需要 Bearer Token

---

### 测试用例管理

#### 1. 获取测试用例列表

**GET** `/api-test/cases`

**请求头：** 需要 Bearer Token

**查询参数：**

| 参数 | 类型 | 描述 |
|------|------|------|
| collection_id | int | 筛选特定集合 |
| project_id | int | 筛选特定项目 |

---

#### 2. 创建测试用例

**POST** `/api-test/cases`

**请求头：** 需要 Bearer Token

**请求体：**

```json
{
    "name": "登录接口测试",
    "description": "测试用户登录功能",
    "method": "POST",
    "url": "http://localhost:5211/api/v1/auth/login",
    "headers": {
        "Content-Type": "application/json"
    },
    "params": {},
    "body": {
        "username": "testuser",
        "password": "password123"
    },
    "body_type": "json",
    "assertions": [
        {
            "type": "status_code",
            "expected": 200
        },
        {
            "type": "json_path",
            "path": "$.success",
            "expected": true
        }
    ],
    "collection_id": 1,
    "project_id": 1
}
```

**参数说明：**

| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| name | string | ✓ | 用例名称 |
| method | string | ✓ | HTTP 方法 (GET/POST/PUT/DELETE/PATCH) |
| url | string | ✓ | 请求 URL |
| description | string | ✗ | 用例描述 |
| headers | object | ✗ | 请求头 |
| params | object | ✗ | 查询参数 |
| body | any | ✗ | 请求体 |
| body_type | string | ✗ | 请求体类型 (json/form/raw) |
| pre_script | string | ✗ | 前置脚本 |
| post_script | string | ✗ | 后置脚本 |
| assertions | array | ✗ | 断言列表 |
| collection_id | int | ✗ | 所属集合 ID |
| project_id | int | ✓ | 所属项目 ID |

---

#### 3. 获取用例详情

**GET** `/api-test/cases/{case_id}`

**请求头：** 需要 Bearer Token

---

#### 4. 更新测试用例

**PUT** `/api-test/cases/{case_id}`

**请求头：** 需要 Bearer Token

---

#### 5. 删除测试用例

**DELETE** `/api-test/cases/{case_id}`

**请求头：** 需要 Bearer Token

---

### 执行测试

#### 1. 快速执行 HTTP 请求

**POST** `/api-test/execute`

**请求头：** 需要 Bearer Token

**请求体：**

```json
{
    "method": "GET",
    "url": "https://httpbin.org/get",
    "headers": {
        "User-Agent": "EasyTest/1.0"
    },
    "params": {
        "name": "test"
    },
    "body": null,
    "body_type": "json",
    "timeout": 30
}
```

**成功响应：**

```json
{
    "success": true,
    "code": 200,
    "data": {
        "success": true,
        "status_code": 200,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": { ... },
        "response_time": 156.32,
        "response_size": "1.25 KB",
        "cookies": {}
    }
}
```

---

#### 2. 执行单个测试用例

**POST** `/api-test/cases/{case_id}/run`

**请求头：** 需要 Bearer Token

---

#### 3. 批量执行集合中的用例

**POST** `/api-test/collections/{collection_id}/run`

**请求头：** 需要 Bearer Token

**成功响应：**

```json
{
    "success": true,
    "code": 200,
    "data": {
        "total": 10,
        "passed": 8,
        "failed": 2,
        "results": [
            {
                "case_id": 1,
                "name": "登录接口测试",
                "passed": true,
                "status_code": 200,
                "response_time": 125.5
            }
        ]
    }
}
```

---

## 性能测试

### 健康检查

**GET** `/perf-test/health`

---

### 场景管理

#### 1. 获取场景列表

**GET** `/perf-test/scenarios`

**请求头：** 需要 Bearer Token

**查询参数：**

| 参数 | 类型 | 描述 |
|------|------|------|
| project_id | int | 筛选特定项目 |

---

#### 2. 创建性能测试场景

**POST** `/perf-test/scenarios`

**请求头：** 需要 Bearer Token

**请求体：**

```json
{
    "name": "首页压力测试",
    "description": "测试首页在高并发下的表现",
    "target_url": "http://localhost:5211",
    "user_count": 100,
    "spawn_rate": 10,
    "duration": 60,
    "project_id": 1
}
```

**参数说明：**

| 参数 | 类型 | 必填 | 默认值 | 描述 |
|------|------|------|--------|------|
| name | string | ✓ | - | 场景名称 |
| description | string | ✗ | "" | 场景描述 |
| target_url | string | ✓ | http://localhost:8080 | 目标 URL |
| user_count | int | ✗ | 10 | 并发用户数 |
| spawn_rate | int | ✗ | 1 | 每秒启动用户数 |
| duration | int | ✗ | 60 | 测试持续时间（秒） |
| project_id | int | ✓ | - | 所属项目 ID |

---

#### 3. 获取场景详情

**GET** `/perf-test/scenarios/{scenario_id}`

**请求头：** 需要 Bearer Token

---

#### 4. 更新场景

**PUT** `/perf-test/scenarios/{scenario_id}`

**请求头：** 需要 Bearer Token

---

#### 5. 删除场景

**DELETE** `/perf-test/scenarios/{scenario_id}`

**请求头：** 需要 Bearer Token

---

### 执行性能测试

#### 1. 运行性能测试场景

**POST** `/perf-test/scenarios/{scenario_id}/run`

**请求头：** 需要 Bearer Token

**请求体（可选，覆盖场景默认配置）：**

```json
{
    "user_count": 50,
    "spawn_rate": 5,
    "duration": 120
}
```

**成功响应：**

```json
{
    "success": true,
    "code": 200,
    "data": {
        "message": "测试已启动",
        "run_key": "1_1",
        "config": {
            "users": 50,
            "spawn_rate": 5,
            "run_time": 120
        }
    }
}
```

---

#### 2. 停止性能测试

**POST** `/perf-test/scenarios/{scenario_id}/stop`

**请求头：** 需要 Bearer Token

---

#### 3. 获取测试状态

**GET** `/perf-test/scenarios/{scenario_id}/status`

**请求头：** 需要 Bearer Token

**成功响应：**

```json
{
    "success": true,
    "code": 200,
    "data": {
        "status": "running",
        "is_running": true,
        "running_time": 45.5,
        "last_run_at": "2025-12-27T12:00:00"
    }
}
```

---

#### 4. 快速性能测试

**POST** `/perf-test/quick-test`

**请求头：** 需要 Bearer Token

**请求体：**

```json
{
    "target_host": "http://localhost:5211",
    "endpoint": "/api/v1/auth/me",
    "method": "GET",
    "user_count": 10,
    "spawn_rate": 2,
    "run_time": 30
}
```

**参数说明：**

| 参数 | 类型 | 必填 | 默认值 | 描述 |
|------|------|------|--------|------|
| target_host | string | ✓ | - | 目标主机 |
| endpoint | string | ✗ | "/" | 测试端点 |
| method | string | ✗ | "GET" | HTTP 方法 |
| user_count | int | ✗ | 5 | 并发用户数 |
| spawn_rate | int | ✗ | 1 | 每秒启动用户数 |
| run_time | int | ✗ | 10 | 测试时间（秒） |

---

#### 5. 获取性能测试模板

**GET** `/perf-test/templates`

**成功响应：**

```json
{
    "success": true,
    "code": 200,
    "data": [
        {
            "name": "基础负载测试",
            "description": "简单的 GET 请求负载测试",
            "code": "..."
        }
    ]
}
```

---

#### 6. 获取运行中的测试

**GET** `/perf-test/running`

**请求头：** 需要 Bearer Token

---

## Web 自动化测试

### 健康检查

**GET** `/web-test/health`

---

### 脚本管理

#### 1. 获取脚本列表

**GET** `/web-test/scripts`

**请求头：** 需要 Bearer Token

**查询参数：**

| 参数 | 类型 | 描述 |
|------|------|------|
| project_id | int | 筛选特定项目 |

---

#### 2. 创建 Web 测试脚本

**POST** `/web-test/scripts`

**请求头：** 需要 Bearer Token

**请求体：**

```json
{
    "name": "登录流程测试",
    "description": "测试用户登录流程",
    "script_content": "from playwright.sync_api import sync_playwright...",
    "target_url": "http://localhost:3000",
    "browser": "chromium",
    "headless": true,
    "timeout": 30000,
    "project_id": 1
}
```

**参数说明：**

| 参数 | 类型 | 必填 | 默认值 | 描述 |
|------|------|------|--------|------|
| name | string | ✓ | - | 脚本名称 |
| description | string | ✗ | "" | 脚本描述 |
| script_content | string | ✗ | 默认模板 | Playwright 脚本代码 |
| target_url | string | ✗ | "" | 目标 URL |
| browser | string | ✗ | "chromium" | 浏览器类型 (chromium/firefox/webkit) |
| headless | boolean | ✗ | true | 是否无头模式 |
| timeout | int | ✗ | 30000 | 超时时间（毫秒） |
| project_id | int | ✓ | - | 所属项目 ID |

---

#### 3. 获取脚本详情

**GET** `/web-test/scripts/{script_id}`

**请求头：** 需要 Bearer Token

---

#### 4. 更新脚本

**PUT** `/web-test/scripts/{script_id}`

**请求头：** 需要 Bearer Token

---

#### 5. 删除脚本

**DELETE** `/web-test/scripts/{script_id}`

**请求头：** 需要 Bearer Token

---

### 执行脚本

#### 运行 Web 测试脚本

**POST** `/web-test/scripts/{script_id}/run`

**请求头：** 需要 Bearer Token

---

## 测试报告

### 健康检查

**GET** `/reports/health`

---

### 测试执行记录

#### 1. 获取测试执行记录列表

**GET** `/test-runs`

**请求头：** 需要 Bearer Token

**查询参数：**

| 参数 | 类型 | 默认值 | 描述 |
|------|------|--------|------|
| project_id | int | - | 项目 ID |
| test_type | string | - | 测试类型 (api/web/performance) |
| status | string | - | 状态 (pending/running/success/failed/cancelled) |
| page | int | 1 | 页码 |
| per_page | int | 20 | 每页数量 |

---

#### 2. 获取测试执行记录详情

**GET** `/test-runs/{run_id}`

**请求头：** 需要 Bearer Token

---

### 统计与仪表盘

#### 1. 获取报告统计数据

**GET** `/reports/statistics`

**请求头：** 需要 Bearer Token

**查询参数：**

| 参数 | 类型 | 默认值 | 描述 |
|------|------|--------|------|
| project_id | int | - | 项目 ID |
| days | int | 7 | 统计天数 |

**成功响应：**

```json
{
    "success": true,
    "code": 200,
    "data": {
        "summary": {
            "total_runs": 100,
            "success_runs": 85,
            "failed_runs": 15,
            "success_rate": 85.0
        },
        "by_type": [
            {
                "type": "api",
                "count": 50,
                "passed": 45,
                "failed": 5
            }
        ]
    }
}
```

---

#### 2. 获取仪表盘统计

**GET** `/reports/dashboard`

**请求头：** 需要 Bearer Token

---

## 文档管理

### 健康检查

**GET** `/docs/health`

---

### 文档 CRUD

#### 1. 获取项目文档列表

**GET** `/projects/{project_id}/docs`

**请求头：** 需要 Bearer Token

**查询参数：**

| 参数 | 类型 | 默认值 | 描述 |
|------|------|--------|------|
| category | string | - | 分类筛选 |
| keyword | string | - | 搜索关键词 |
| page | int | 1 | 页码 |
| per_page | int | 20 | 每页数量 |

---

#### 2. 创建文档

**POST** `/projects/{project_id}/docs`

**请求头：** 需要 Bearer Token

**请求体：**

```json
{
    "title": "测试计划",
    "content": "# 测试计划\n\n## 目标\n...",
    "category": "test_plan",
    "tags": ["重要", "Q1"]
}
```

**参数说明：**

| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| title | string | ✓ | 文档标题，1-255字符 |
| content | string | ✓ | 文档内容（Markdown） |
| category | string | ✗ | 分类 (test_plan/test_case/test_report/other) |
| tags | array | ✗ | 标签列表 |

---

#### 3. 获取文档详情

**GET** `/docs/{doc_id}`

**请求头：** 需要 Bearer Token

---

#### 4. 更新文档

**PUT** `/docs/{doc_id}`

**请求头：** 需要 Bearer Token

---

#### 5. 删除文档

**DELETE** `/docs/{doc_id}`

**请求头：** 需要 Bearer Token

---

## 错误码说明

| 错误码 | 描述 |
|--------|------|
| 200 | 成功 |
| 201 | 创建成功 |
| 400 | 请求参数错误 |
| 401 | 未认证或认证失败 |
| 403 | 无权限访问 |
| 404 | 资源不存在 |
| 500 | 服务器内部错误 |

---

## 附录：常见示例

### 注册用户

```bash
curl -X POST http://localhost:5211/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","email":"test@example.com","password":"password123"}'
```

### 登录

```bash
curl -X POST http://localhost:5211/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"password123"}'
```

### 创建项目

```bash
curl -X POST http://localhost:5211/api/v1/projects \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <your_access_token>" \
  -d '{"name":"测试项目","description":"项目描述"}'
```

### 执行 HTTP 请求

```bash
curl -X POST http://localhost:5211/api/v1/api-test/execute \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <your_access_token>" \
  -d '{"method":"GET","url":"https://httpbin.org/get"}'
```

### 快速性能测试

```bash
curl -X POST http://localhost:5211/api/v1/perf-test/quick-test \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <your_access_token>" \
  -d '{"target_host":"http://localhost:5211","endpoint":"/api/v1/auth/me","user_count":10,"run_time":30}'
```
