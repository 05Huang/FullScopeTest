# API 测试环境配置功能实现总结

## 问题确认
用户报告：**接口测试里可以选择配置环境，但是并没有解决如何使用已有配置环境的功能**

## 解决方案

### ✅ 已完整实现以下功能

#### 1. 前端环境选择器（ApiTestWorkspace.tsx）
- 在URL输入栏下方添加环境选择器
- 用户可以从下拉列表选择测试环境
- 选择环境后显示环境标签和"应用配置"按钮

#### 2. 环境配置应用（前端）
- **应用按钮**：点击后将环境的基础URL和Headers应用到当前请求
- **自动替换**：发送请求前自动替换环境变量（`{{var_name}}` 格式）
- **发送时包含环境**：请求时将环境ID发送到后端

#### 3. 后端环境变量支持（api_test.py）
- **execute_request()**：支持 `env_id` 参数，快速测试时应用环境
- **run_case()**：执行单个用例时支持环境配置
- **run_collection()**：批量执行集合时支持环境配置

#### 4. 环境变量替换逻辑
**前后端都实现了变量替换**：
- 替换范围：URL、Headers、Params
- 格式：`{{variable_name}}` → 环境变量值
- 例如：
  - URL: `/users/{{user_id}}` → `/users/123`
  - Headers: `Authorization: Bearer {{token}}` → `Authorization: Bearer abc123`

#### 5. Headers合并策略
- 环境的Headers + 用户手动设置的Headers 合并
- 用户设置的Headers优先级更高

#### 6. API接口更新
- `executeRequest()` 新增 `env_id` 参数
- `runCollection()` 新增 `envId` 参数

## 使用示例

### 场景：调用生产环境API

#### 第1步：在环境管理创建环境
```json
{
  "name": "生产环境",
  "base_url": "https://api.prod.com",
  "variables": {
    "user_id": "123",
    "token": "prod_token_xyz"
  },
  "headers": {
    "Authorization": "Bearer {{token}}",
    "X-App-Version": "1.0"
  }
}
```

#### 第2步：在API测试工作区
1. 从环境下拉框选择"生产环境"
2. 输入相对路径URL：`/users/{{user_id}}/profile`
3. 点击"应用配置"或直接"发送"

#### 第3步：最终请求
```
GET https://api.prod.com/users/123/profile
Headers:
  Authorization: Bearer prod_token_xyz
  X-App-Version: 1.0
```

## 技术实现细节

### 前端流程
```
用户选择环境 
    ↓
handleSelectEnv() → 更新 selectedEnvId 和 currentEnv
    ↓
用户点击"发送"或"应用配置"
    ↓
getRequestWithEnv() → 应用环境配置 + 替换变量
    ↓
handleSend() → 发送请求，传递 env_id 到后端
```

### 后端流程
```
receive request with env_id
    ↓
fetch Environment 对象
    ↓
merge environment headers into request headers
    ↓
replace all {{var}} in url, headers, params
    ↓
execute request with final parameters
```

## 核心代码改动

### 前端新增函数（ApiTestWorkspace.tsx）
```typescript
// 选择环境
const handleSelectEnv = (envId: number | undefined) => { ... }

// 应用环境配置
const applyEnvironment = () => { ... }

// 获取包含环境配置的请求参数
const getRequestWithEnv = async () => { ... }

// 修改的发送请求函数
const handleSend = async () => {
  const { finalUrl, finalHeaders, finalParams } = await getRequestWithEnv()
  // 使用 finalUrl, finalHeaders, finalParams 发送请求
}
```

### 后端修改（api_test.py）
```python
# execute_request() 新增逻辑
if env_id:
    env = Environment.query.filter_by(id=env_id).first()
    if env:
        # 合并headers
        headers = {**env.headers, **headers}
        # 替换变量
        for var_name, var_value in env.variables.items():
            url = url.replace(f'{{{{{var_name}}}}}', str(var_value))
            # 对headers、params也做替换

# run_case() 和 run_collection() 使用相同逻辑
```

## 文件修改清单

| 文件 | 修改内容 |
|------|--------|
| `web/src/pages/api-test/ApiTestWorkspace.tsx` | 添加环境选择UI、环境配置应用逻辑、变量替换 |
| `web/src/services/apiTestService.ts` | 更新 `executeRequest` 和 `runCollection` 支持 env_id |
| `backend/app/api/api_test.py` | 导入Environment、修改execute_request/run_case/run_collection实现环境变量替换 |

## 状态验证

✅ 前端编译：无错误
✅ 后端检查：无错误
✅ 功能完整：选择 → 应用 → 发送 完整流程
✅ 环境变量：支持前后端替换，确保可靠性

## 已解决的问题

| 问题 | 解决方案 |
|------|--------|
| 无法使用环境配置 | 实现环境应用和变量替换逻辑 |
| 环境配置不生效 | 前后端双重验证和应用 |
| 变量值不替换 | 支持 {{var}} 格式的双重替换 |
| Headers冲突 | 实现headers合并和优先级管理 |

## 使用建议

1. **快速测试**：选择环境 → 输入相对URL → 点击发送（环境自动应用）
2. **保存用例**：可以在用例中使用 `{{var}}` 格式，执行时指定环境
3. **批量执行**：运行集合时可以选择环境，所有用例使用同一环境配置
4. **多环境开发**：定义dev/test/prod环境，快速切换测试

---

**状态**：✅ 功能实现完成，已验证无错误，可直接使用
