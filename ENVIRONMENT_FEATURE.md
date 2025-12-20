# API 测试环境配置功能实现说明

## 问题描述
之前实现了可以选择测试环境的UI，但缺少实际使用环境配置的功能。现已完整实现环境变量、Headers 和基础URL的应用。

## 功能实现

### 1. 前端实现 (ApiTestWorkspace.tsx)

#### 新增状态变量
- `environments`: 环境列表
- `selectedEnvId`: 当前选中的环境ID
- `currentEnv`: 当前选中的环境对象

#### 新增函数

##### `handleSelectEnv(envId)`
- 功能：选择并切换环境
- 参数：环境ID
- 效果：更新 `currentEnv` 并提示用户

##### `applyEnvironment()`
- 功能：将环境配置应用到当前请求
- 行为：
  - 将环境的基础URL应用到URL字段
  - 合并环境的Headers到请求Header列表
  - 提示用户应用完成

##### `getRequestWithEnv()`
- 功能：获取包含环境配置的完整请求参数
- 返回值：`{ finalUrl, finalHeaders, finalParams }`
- 支持变量替换：`{{variable_name}}` 格式
- 处理：
  1. 应用环境的基础URL（如果URL不是完整URL）
  2. 合并环境的Headers
  3. 替换环境变量（支持 `{{var}}` 语法）
  4. 保留用户手动设置的参数

##### `handleSend()`
- 修改：集成 `getRequestWithEnv()` 的结果
- 增强：传递 `env_id` 参数到后端
- 改进：环境变量在发送前自动替换

#### UI 增强
- 新增环境选择栏，位于URL输入栏下方
- 选择环境后显示环境标签和"应用配置"按钮
- 用户可以：
  - 选择环境自动应用配置
  - 手动点击"应用配置"按钮应用
  - 清除环境选择

### 2. 后端实现 (api_test.py)

#### 导入
- 添加 `Environment` 模型导入

#### 修改的函数

##### `execute_request()`
- 新增参数：`env_id` (可选)
- 功能：执行快速测试时支持环境配置
- 实现：
  1. 检查 `env_id` 是否存在
  2. 如果存在，加载对应的环境
  3. 合并环境的Headers到请求Headers
  4. 替换环境变量：`{{var_name}}` → 环境变量值
  5. 支持在URL、Headers、Params中替换变量

##### `run_case(case_id)`
- 新增参数：`env_id` (来自查询参数)
- 功能：执行单个用例时支持环境配置
- 实现：与 `execute_request()` 相同的环境配置逻辑
- 用例内的参数 + 环境配置 = 最终请求

##### `run_collection(collection_id)`
- 新增参数：`env_id` (来自查询参数)
- 功能：批量执行集合中的用例时支持环境配置
- 实现：为集合中的每个用例应用环境配置

### 3. 服务层修改 (apiTestService.ts)

#### 修改的接口

##### `executeRequest()`
```typescript
export const executeRequest = (data: {
  // ... 其他参数
  env_id?: number  // 新增
}): Promise<ApiResponse>
```

##### `runCollection()`
```typescript
export const runCollection = (
  collectionId: number, 
  envId?: number  // 新增参数
): Promise<ApiResponse>
```

## 使用流程

### 场景1：使用环境变量快速测试

1. **创建环境**（在环境管理页面）
   - 设置环境名称、基础URL、Headers、变量
   - 例如：
     ```
     名称: 生产环境
     基础URL: https://api.example.com
     Headers: { "Authorization": "Bearer {{token}}" }
     变量: { "token": "abc123", "api_version": "v2" }
     ```

2. **在API测试工作区选择环境**
   - 从"环境"下拉框选择"生产环境"
   - 显示蓝色标签表示已选择

3. **编写请求**
   - URL: `/users/{{user_id}}`
   - Headers: 自动合并环境的Headers

4. **点击"应用配置"**（可选）
   - 将环境的基础URL应用到URL字段
   - 将环境的Headers添加到Header列表

5. **发送请求**
   - 前端自动替换 `{{user_id}}`、`{{token}}` 等变量
   - 后端再次验证并应用环境配置
   - 最终请求：
     ```
     GET https://api.example.com/users/123
     Header: Authorization: Bearer abc123
     ```

### 场景2：批量执行用例时使用环境

```typescript
// 前端代码示例
const handleRunCollection = async () => {
  await apiTestService.runCollection(collectionId, selectedEnvId)
  // 集合中的所有用例都将使用该环境的配置
}
```

## 环境变量替换规则

### 支持的格式
- `{{variable_name}}` - 标准变量引用格式
- 支持位置：
  - 请求URL
  - 请求Headers的值
  - 请求Params的值
  - 请求Body（如果支持）

### 替换流程
1. **前端**（`getRequestWithEnv()`）
   - 首次替换环境变量
   - 结果发送到后端

2. **后端**（`execute_request()`、`run_case()`、`run_collection()`）
   - 再次应用环境配置和替换
   - 确保环境配置生效

### 示例

**环境配置：**
```json
{
  "name": "测试环境",
  "base_url": "https://api.test.com",
  "variables": {
    "user_id": "123",
    "token": "test_token_xyz"
  },
  "headers": {
    "Authorization": "Bearer {{token}}",
    "X-Request-ID": "req_{{user_id}}"
  }
}
```

**请求配置：**
```
URL: /users/{{user_id}}/profile
Headers: {
  "Authorization": "Bearer {{token}}",
  "X-API-Version": "v2"
}
```

**最终请求：**
```
GET https://api.test.com/users/123/profile
Headers: {
  "Authorization": "Bearer test_token_xyz",
  "X-Request-ID": "req_123",
  "X-API-Version": "v2"
}
```

## 技术细节

### 变量替换实现
```python
# 后端替换逻辑示例
if env_id and env:
    for var_name, var_value in env.variables.items():
        # 替换所有 {{var_name}} 为对应的值
        url = url.replace(f'{{{{{var_name}}}}}', str(var_value))
        # 在headers中也进行替换
        for key, value in headers.items():
            if isinstance(value, str):
                value = value.replace(f'{{{{{var_name}}}}}', str(var_value))
```

## 优先级和合并规则

### Headers 合并（优先级从高到低）
1. 用户在界面手动设置的Headers（最高优先级）
2. 环境配置中的Headers（次优先级）
3. 默认Headers（最低优先级）

### 变量替换
- 环境变量在请求发送前被替换
- 同名变量：后定义的覆盖先定义的
- 未定义的变量：保留原始格式不替换

## 后续改进建议

1. **支持嵌套变量**
   - 例如：`{{env.base_url}}/users`

2. **支持变量函数**
   - 例如：`{{timestamp()}}`, `{{uuid()}}`

3. **变量作用域**
   - 全局变量（环境级）
   - 集合变量
   - 用例变量
   - 请求级变量

4. **动态变量提取**
   - 从前一个请求的响应中提取变量
   - 自动传递到后续请求

5. **环境切换按钮**
   - 快速在多个常用环境间切换
   - 保存最近使用的环境

## 文件修改列表

### 前端文件
- [web/src/pages/api-test/ApiTestWorkspace.tsx](web/src/pages/api-test/ApiTestWorkspace.tsx)
  - 添加环境选择UI
  - 实现环境配置应用逻辑
  
- [web/src/services/apiTestService.ts](web/src/services/apiTestService.ts)
  - 更新 `executeRequest()` 支持 `env_id`
  - 更新 `runCollection()` 支持 `env_id`

### 后端文件
- [backend/app/api/api_test.py](backend/app/api/api_test.py)
  - 导入 `Environment` 模型
  - 修改 `execute_request()` 支持环境配置
  - 修改 `run_case()` 支持环境配置
  - 修改 `run_collection()` 支持环境配置

## 测试建议

1. **环境选择测试**
   - 选择/切换环境是否正确更新显示

2. **变量替换测试**
   - 单个变量替换
   - 多个变量替换
   - 未定义变量的处理

3. **Headers合并测试**
   - 环境Headers + 用户Headers的合并结果
   - 优先级是否正确

4. **集合执行测试**
   - 批量执行时环境配置是否对所有用例生效
   - 每个用例的结果是否正确

5. **集成测试**
   - 快速测试 + 环境
   - 保存用例后再执行 + 环境
