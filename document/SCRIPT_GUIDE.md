# 前置脚本与断言使用指南

## 概述

EasyTest 平台支持在 API 测试中编写 JavaScript 脚本，实现类似 Postman 的前置脚本和后置断言功能。脚本在沙箱环境中执行，支持 Postman 风格的 API。

## 目录

- [前置脚本](#前置脚本)
- [后置断言](#后置断言)
- [可用的 API 对象](#可用的-api-对象)
- [上下文变量](#上下文变量)
- [执行流程](#执行流程)
- [注意事项](#注意事项)
- [常见示例](#常见示例)

---

## 前置脚本

### 功能说明

前置脚本在发送请求**之前**执行，可以用于：

- 动态修改请求参数（URL、Headers、Body）
- 设置环境变量
- 生成时间戳、随机数等动态数据
- 计算签名
- 执行预请求逻辑

### 使用位置

在 API 测试工作台的 **前置脚本** 标签页中编写。

### 可用操作

在前置脚本中，你可以：

1. **修改请求**
   ```javascript
   // 修改 URL
   pm.request.url = "https://api.example.com/new-path";

   // 添加或修改 Headers
   pm.request.headers["X-Custom-Header"] = "custom-value";

   // 修改请求体
   pm.request.body = JSON.stringify({ key: "value" });
   ```

2. **操作环境变量**
   ```javascript
   // 设置环境变量
   pm.environment.set("token", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...");

   // 获取环境变量
   const baseUrl = pm.environment.get("base_url");

   // 获取所有环境变量名
   const keys = pm.environment.keys();

   // 清除所有环境变量
   pm.environment.clear();
   ```

3. **操作临时变量**
   ```javascript
   // 设置临时变量（仅在当前脚本执行期间有效）
   pm.variables.set("timestamp", Date.now());

   // 获取临时变量
   const timestamp = pm.variables.get("timestamp");
   ```

---

## 后置断言

### 功能说明

后置断言在收到响应**之后**执行，可以用于：

- 验证响应状态码
- 验证响应体内容
- 验证响应头
- 提取响应数据并保存为环境变量
- 执行复杂的测试逻辑

### 使用位置

在 API 测试工作台的 **断言脚本** 标签页中编写。

### 可用操作

在后置断言中，你可以：

1. **使用 pm.test 编写断言**
   ```javascript
   // 基本断言
   pm.test("状态码是 200", function() {
       pm.assertResponse(200);
   });

   // 使用 pm.expect 进行链式断言
   pm.test("响应体包含用户数据", function() {
       pm.expect(pm.response.body).to.have.property("data");
       pm.expect(pm.response.body.data).to.exist;
   });
   ```

2. **访问响应数据**
   ```javascript
   // 访问响应状态码
   const status = pm.response.status;  // 或 pm.response.code

   // 访问响应头
   const contentType = pm.response.headers["Content-Type"];

   // 访问响应体（自动解析 JSON）
   const body = pm.response.json();
   ```

3. **提取数据并保存**
   ```javascript
   pm.test("保存返回的 token", function() {
       const response = pm.response.json();
       pm.expect(response.data.token).to.exist;
       pm.environment.set("token", response.data.token);
   });
   ```

---

## 可用的 API 对象

### pm.test

编写测试断言的基本函数。

```javascript
pm.test(testName, function) {
    // 断言逻辑
}
```

- **参数**：
  - `testName` (string): 断言名称
  - `function` (Function): 包含断言逻辑的函数
- **说明**：函数内抛出的任何错误都会被捕获，标记该断言失败

### pm.expect

链式断言函数，支持丰富的断言方法。

```javascript
pm.expect(actual).to.eql(expected);
pm.expect(actual).to.have.property("prop");
```

#### 支持的断言方法

| 方法 | 说明 | 示例 |
|------|------|------|
| `eql(value)` | 严格相等 | `pm.expect(1).to.eql(1)` |
| `equal(value)` | 同 eql | `pm.expect("a").to.equal("a")` |
| `exist` | 值存在（非 null/undefined） | `pm.expect(data).to.exist` |
| `property(prop)` | 对象包含指定属性 | `pm.expect(obj).to.have.property("id")` |
| `above(value)` | 数值大于 | `pm.expect(count).to.be.above(0)` |
| `below(value)` | 数值小于 | `pm.expect(time).to.be.below(1000)` |
| `include(value)` | 字符串包含 | `pm.expect(text).to.include("keyword")` |
| `contains(value)` | 同 include | `pm.expect(url).to.contains("/api")` |
| `a(type)` | 类型判断 | `pm.expect(data).to.be.a("object")` |
| `an(type)` | 同 a | `pm.expect(arr).to.be.an("array")` |

#### 修饰符

| 修饰符 | 说明 | 示例 |
|--------|------|------|
| `.to` | 语法连接词 | `pm.expect(x).to.eql(y)` |
| `.be` | 同 to | `pm.expect(x).to.be.a("string")` |
| `.not` | 反向断言 | `pm.expect(x).not.to.eql(y)` |

### pm.environment

环境变量的操作接口。

| 方法 | 说明 | 示例 |
|------|------|------|
| `get(key)` | 获取环境变量 | `pm.environment.get("base_url")` |
| `set(key, value)` | 设置环境变量 | `pm.environment.set("token", "xxx")` |
| `keys()` | 获取所有键名 | `pm.environment.keys()` |
| `clear()` | 清除所有环境变量 | `pm.environment.clear()` |

### pm.variables

临时变量的操作接口（仅当前脚本有效）。

| 方法 | 说明 | 示例 |
|------|------|------|
| `get(key)` | 获取临时变量 | `pm.variables.get("temp")` |
| `set(key, value)` | 设置临时变量 | `pm.variables.set("temp", 123)` |
| `clear()` | 清除所有临时变量 | `pm.variables.clear()` |

### pm.assertResponse

快捷断言响应状态码。

```javascript
pm.assertResponse(200);  // 断言状态码为 200
```

---

## 上下文变量

### pm.request

前置脚本中可用，表示当前请求对象。

```javascript
{
    method: "POST",
    url: "https://api.example.com/users",
    headers: {
        "Content-Type": "application/json"
    },
    params: {
        "page": "1"
    },
    body: { ... }
}
```

### pm.response

后置断言中可用，表示响应对象。

```javascript
{
    status: 200,          // HTTP 状态码
    code: 200,            // 状态码别名
    headers: {            // 响应头
        "Content-Type": "application/json"
    },
    body: { ... },        // 响应体（已解析 JSON）
    json(): { ... },      // 获取 JSON 响应体的方法
    responseTime: 156,    // 响应时间（毫秒）
    size: 1024           // 响应大小（字节）
}
```

---

## 执行流程

### 单个请求的执行顺序

```
1. 前置脚本执行
   ↓
2. 应用环境变量和请求修改
   ↓
3. 发送 HTTP 请求
   ↓
4. 后置断言执行
   ↓
5. 返回测试结果
```

### 用例通过/失败判定

| 情况 | 结果 |
|------|------|
| 前置脚本执行失败 | ❌ 用例失败 |
| 后置断言存在失败 | ❌ 用例失败 |
| 无脚本且 HTTP 状态码 < 400 | ✅ 用例通过 |
| 无脚本且 HTTP 状态码 ≥ 400 | ❌ 用例失败 |
| 有脚本且全部通过 | ✅ 用例通过 |

---

## 注意事项

### 1. Node.js 环境

脚本使用 Node.js 执行，支持 ES6+ 语法，但不支持浏览器 API（如 `fetch`、`window`）。

### 2. 超时限制

单个脚本执行超时时间为 **3 秒**，超时后会中断执行并返回错误。

### 3. 错误处理

- 前置脚本错误会阻止请求发送
- 后置断言中的单个断言失败不会影响其他断言执行
- 语法错误会导致整个脚本执行失败

### 4. 环境变量持久化

- `pm.environment.set()` 修改的环境变量会保存到后端
- `pm.variables` 中的临时变量仅在当前脚本中有效

### 5. JSON 响应

- `pm.response.body` 自动解析 JSON，无需手动 `JSON.parse()`
- 对于非 JSON 响应，`body` 为原始字符串

---

## 常见示例

### 示例 1：动态生成请求头

```javascript
// 前置脚本
const timestamp = Date.now();
const nonce = Math.random().toString(36).substring(7);

pm.request.headers["X-Timestamp"] = timestamp;
pm.request.headers["X-Nonce"] = nonce;

// 保存供断言使用
pm.variables.set("timestamp", timestamp);
```

### 示例 2：签名计算

```javascript
// 前置脚本
const secret = pm.environment.get("app_secret");
const body = JSON.stringify(pm.request.body);
const signature = require('crypto')
    .createHmac('sha256', secret)
    .update(body)
    .digest('hex');

pm.request.headers["X-Signature"] = signature;
```

### 示例 3：基础响应验证

```javascript
// 后置断言
pm.test("状态码为 200", function() {
    pm.assertResponse(200);
});

pm.test("响应头是 JSON", function() {
    pm.expect(pm.response.headers["content-type"]).to.include("application/json");
});

pm.test("响应时间小于 500ms", function() {
    pm.expect(pm.response.responseTime).to.be.below(500);
});
```

### 示例 4：验证响应结构

```javascript
// 后置断言
pm.test("响应体结构正确", function() {
    const body = pm.response.json();

    pm.expect(body).to.be.a("object");
    pm.expect(body).to.have.property("code");
    pm.expect(body).to.have.property("data");
    pm.expect(body).to.have.property("message");

    pm.expect(body.code).to.eql(200);
    pm.expect(body.data).to.be.an("array");
});
```

### 示例 5：提取响应数据

```javascript
// 后置断言
pm.test("提取用户 ID", function() {
    const body = pm.response.json();

    pm.expect(body.data.id).to.exist;
    pm.environment.set("user_id", body.data.id);
});

pm.test("提取分页信息", function() {
    const body = pm.response.json();

    pm.expect(body.pagination).to.exist;
    pm.environment.set("total", body.pagination.total);
    pm.environment.set("page", body.pagination.page);
});
```

### 示例 6：条件断言

```javascript
// 后置断言
pm.test("根据条件验证", function() {
    const body = pm.response.json();
    const userType = pm.environment.get("user_type");

    if (userType === "admin") {
        pm.expect(body.data.permissions).to.include("delete");
    } else {
        pm.expect(body.data.permissions).not.to.include("delete");
    }
});
```

### 示例 7：数组验证

```javascript
// 后置断言
pm.test("验证用户列表", function() {
    const body = pm.response.json();

    pm.expect(body.data.users).to.be.an("array");
    pm.expect(body.data.users.length).to.be.above(0);

    // 验证数组元素结构
    body.data.users.forEach(user => {
        pm.expect(user).to.have.property("id");
        pm.expect(user).to.have.property("name");
        pm.expect(user).to.have.property("email");
    });
});
```

### 示例 8：完整的登录流程

```javascript
// 前置脚本：准备登录数据
const loginData = {
    username: pm.environment.get("username"),
    password: pm.environment.get("password")
};

pm.request.body = JSON.stringify(loginData);

// 后置断言：验证响应并保存 token
pm.test("登录成功", function() {
    pm.assertResponse(200);
});

pm.test("返回 token", function() {
    const body = pm.response.json();
    pm.expect(body.data.token).to.exist;
    pm.expect(body.data.token).to.be.a("string");

    // 保存 token 供后续请求使用
    pm.environment.set("auth_token", body.data.token);
});
```

---

## 测试结果查看

在 API 测试工作台中，点击 **发送** 按钮后：

1. 切换到 **测试结果** 标签页查看断言结果
2. 绿色标记表示断言通过，红色表示失败
3. 可以看到每个断言的详细信息（名称、状态、错误信息）

示例输出：

```
✅ 前置脚本
   状态：执行成功
   耗时：15ms

✅ 后置断言
   状态：全部通过
   耗时：8ms
   总计：5  通过：5  失败：0

   断言详情：
   ✅ 状态码为 200
   ✅ 响应体包含数据
   ✅ 响应时间小于 500ms
   ✅ 返回有效的 token
   ✅ token 类型为字符串
```

---

## 调试技巧

### 1. 使用 console.log

```javascript
console.log("当前 URL:", pm.request.url);
console.log("环境变量:", pm.environment.keys());
```

**注意**：console.log 输出不会显示在界面上，主要用于调试脚本。

### 2. 分步测试

在断言中添加描述性的名称，方便定位问题：

```javascript
pm.test("步骤1：检查响应状态码", function() {
    pm.assertResponse(200);
});

pm.test("步骤2：检查响应格式", function() {
    pm.expect(pm.response.headers["content-type"]).to.include("json");
});

pm.test("步骤3：检查数据完整性", function() {
    const body = pm.response.json();
    pm.expect(body.data).to.have.property("id");
});
```

### 3. 保存中间结果

```javascript
pm.test("调试响应结构", function() {
    const body = pm.response.json();

    // 保存到环境变量，方便查看
    pm.environment.set("debug_response", JSON.stringify(body));

    pm.expect(body).to.exist;
});
```

---

## 参考资源

- [Postman Sandbox API](https://learning.postman.com/docs/writing-scripts/script-references/postman-sandbox-api-reference/)
- [Postman 断言示例](https://learning.postman.com/docs/writing-scripts/test-examples/)
