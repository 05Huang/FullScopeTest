# FullScopeTest 用户使用指南

> 本文档为 FullScopeTest 全栈自动化测试平台的完整使用说明，包含快速开始和详细功能介绍

---

## 目录

# 第一部分：快速开始
- [1. 快速入门](#1-快速入门)
- [2. 核心概念](#2-核心概念)
- [3. 首次使用指南](#3-首次使用指南)

# 第二部分：详细使用说明
- [4. 用户与认证](#4-用户与认证)
- [5. 项目管理](#5-项目管理)
- [6. API 测试](#6-api-测试)
- [7. Web 自动化测试](#7-web-自动化测试)
- [8. APP 自动化测试](#8-app-自动化测试)
- [9. 性能测试](#9-性能测试)
- [10. 测试计划](#10-测试计划)
- [11. 测试报告](#11-测试报告)
- [12. Mock 服务](#12-mock-服务)
- [13. 质量门禁](#13-质量门禁)
- [14. 触发器与自动化](#14-触发器与自动化)
- [15. 通知配置](#15-通知配置)
- [16. CI/CD 集成](#16-cicd-集成)
- [17. AI 助手](#17-ai-助手)
- [18. 视觉回归测试](#18-视觉回归测试)
- [19. 团队协作](#19-团队协作)
- [20. 系统设置](#20-系统设置)

---

# 第一部分：快速开始

## 1. 快速入门

### 1.1 登录系统

访问 **https://test.huangxuan.chat** 进入登录页面。

**登录凭证：**
- 用户名：`admin`
- 密码：`admin123`

**操作步骤：**
1. 在登录页面输入用户名和密码
2. 点击「登录」按钮
3. 首次登录后建议修改默认密码

### 1.2 创建第一个项目

**操作步骤：**
1. 登录后进入「仪表盘」页面
2. 点击左侧菜单「项目管理」→「创建项目」
3. 填写项目信息：
   - 项目名称：`我的第一个项目`
   - 项目描述：`用于测试的项目`
4. 点击「创建」按钮

### 1.3 创建第一个 API 测试

**操作步骤：**
1. 进入刚创建的项目
2. 点击左侧菜单「API 测试」→「创建集合」
3. 填写集合信息：
   - 集合名称：`HTTP Bin 测试`
4. 点击「创建」按钮进入集合
5. 点击「新建请求」按钮
6. 填写请求信息：
   - 请求名称：`测试 GET 请求`
   - 方法：`GET`
   - URL：`https://httpbin.org/get`
7. 点击「发送」按钮执行请求

### 1.4 执行测试并查看报告

**操作步骤：**
1. 在请求编辑器中配置好请求
2. 点击「发送」按钮
3. 在下方「响应」面板查看结果
4. 点击「保存」按钮保存用例
5. 返回集合列表，点击「运行」按钮
6. 在「报告」页面查看执行结果

---

## 2. 核心概念

### 2.1 项目 (Project)

项目是测试工作的容器，包含：
- 多个 API 集合
- Web 自动化测试脚本
- APP 自动化测试脚本
- 性能测试场景
- 测试计划

**最佳实践：**
- 按业务线或服务创建项目
- 一个项目对应一个微服务或业务模块

### 2.2 环境 (Environment)

环境代表不同的部署阶段：
- **开发环境**：`http://dev.example.com`
- **测试环境**：`http://test.example.com`
- **生产环境**：`https://api.example.com`

**变量示例：**
```
BASE_URL = https://{{env}}.example.com
API_KEY = your-secret-key-{{env}}
```

### 2.3 集合 (Collection)

集合是一组相关测试用例的容器：
- API 测试集合：按功能模块分组
- Web 测试集合：按用户流程分组
- APP 测试集合：按测试场景分组

### 2.4 测试用例 (Test Case)

单个测试单位，包含：
- 请求配置（URL、方法、头、body）
- 前置脚本（发送前执行）
- 断言（验证响应）
- 后置脚本（发送后执行）

### 2.5 测试执行 (Test Run)

测试执行记录，包含：
- 执行时间
- 执行结果（通过/失败）
- 响应数据
- 执行日志

---

## 3. 首次使用指南

### 3.1 系统界面介绍

**顶部导航栏：**
- 左侧：项目切换器
- 中间：全局搜索
- 右侧：通知、设置、用户头像

**左侧菜单：**
- 仪表盘
- 项目管理
- API 测试
- Web 测试
- APP 测试
- 性能测试
- 测试计划
- 报告中心
- Mock 服务
- 触发器
- 系统设置

### 3.2 创建环境

**操作步骤：**
1. 进入项目
2. 点击「设置」→「环境管理」
3. 点击「添加环境」
4. 填写环境信息：
   - 环境名称：`测试环境`
   - Base URL：`https://api.test.example.com`
5. 点击「添加变量」：
   - 变量名：`token`
   - 变量值：`test-token-123`
6. 点击「保存」

### 3.3 创建第一个 Web 测试

**操作步骤：**
1. 进入项目
2. 点击「Web 测试」→「创建集合」
3. 点击「开始录制」
4. 在弹出窗口中选择浏览器（Chrome/Firefox）
5. 开始在浏览器中操作
6. 点击「停止录制」
7. 系统自动生成测试脚本
8. 点击「保存」

---

# 第二部分：详细使用说明

## 4. 用户与认证

### 4.1 用户注册

**操作步骤：**
1. 访问 https://test.huangxuan.chat
2. 点击「注册」链接
3. 填写注册信息：
   - 邮箱：`user@example.com`
   - 用户名：`testuser`
   - 密码：`Password123!`
   - 确认密码：`Password123!`
4. （可选）输入组织邀请码加入已有组织
5. 点击「注册」按钮
6. 查收邮箱验证链接完成注册

### 4.2 用户登录

**操作步骤：**
1. 输入邮箱/用户名
2. 输入密码
3. （可选）勾选「记住我」
4. 点击「登录」

**登录失败处理：**
- 连续 5 次登录失败后账户将被锁定 15 分钟
- 锁定期间可使用「忘记密码」功能重置

### 4.3 忘记密码

**操作步骤：**
1. 登录页面点击「忘记密码」
2. 输入注册邮箱：`user@example.com`
3. 点击「发送重置链接」
4. 查收邮件，点击重置链接
5. 设置新密码
6. 使用新密码登录

### 4.4 修改个人信息

**操作步骤：**
1. 点击右上角用户头像
2. 选择「个人设置」
3. 修改信息：
   - 用户名：`新用户名`
   - 邮箱：`new-email@example.com`
4. 点击「保存」

### 4.5 上传头像

**操作步骤：**
1. 进入「个人设置」
2. 点击当前头像区域
3. 选择本地图片文件（支持 JPG/PNG，最大 2MB）
4. 点击「上传」
5. 图片自动裁剪为正方形
6. 点击「保存」

### 4.6 修改密码

**操作步骤：**
1. 进入「个人设置」
2. 点击「修改密码」
3. 填写表单：
   - 当前密码：`OldPassword123!`
   - 新密码：`NewPassword456!`
   - 确认新密码：`NewPassword456!`
4. 点击「确认修改」

**密码强度要求：**
- 至少 8 个字符
- 包含大写字母 (A-Z)
- 包含小写字母 (a-z)
- 包含数字 (0-9)
- 包含特殊字符 (!@#$%^&*)

### 4.7 双因素认证 (2FA)

**启用步骤：**
1. 进入「个人设置」→「安全设置」
2. 点击「启用双因素认证」
3. 下载认证应用（如 Google Authenticator）
4. 扫描显示的二维码
5. 输入 6 位验证码确认
6. 保存备份码（用于恢复）

**登录时使用：**
1. 输入邮箱和密码
2. 打开认证应用获取 6 位码
3. 输入验证码完成登录

### 4.8 GitHub OAuth 登录

**首次绑定：**
1. 登录页面点击「使用 GitHub 登录」
2. 授权 FullScopeTest 访问 GitHub
3. 自动创建或关联账户

**后续登录：**
1. 点击「使用 GitHub 登录」
2. 自动完成登录（无需密码）

### 4.9 SSO 单点登录

**配置 SSO（管理员）：**
1. 进入「系统设置」→「SSO 配置」
2. 选择 SSO 类型（OIDC/LDAP）
3. 填写配置信息：
   - OIDC：Issuer URL、Client ID、Client Secret
   - LDAP：服务器地址、Base DN、管理员账号
4. 点击「保存」

**用户登录：**
1. 点击「企业账号登录」
2. 跳转到 SSO 登录页面
3. 完成 SSO 认证后自动登录

---

## 5. 项目管理

### 5.1 创建项目

**操作步骤：**
1. 点击左侧菜单「项目管理」
2. 点击「新建项目」按钮
3. 填写项目信息：
   - 项目名称：`电商后端 API`
   - 项目描述：`电商系统后端接口测试`
   - 项目图标：（可选）上传图标
4. 点击「创建」

### 5.2 编辑项目

**操作步骤：**
1. 在项目列表点击项目名称
2. 点击右上角「编辑」按钮
3. 修改项目信息
4. 点击「保存」

### 5.3 删除项目

**操作步骤：**
1. 在项目列表点击项目名称
2. 点击右上角「设置」→「删除项目」
3. 在弹出确认框输入项目名称确认
4. 点击「确认删除」

**注意：** 删除操作会同时删除项目下所有测试数据，请谨慎操作。

### 5.4 置顶项目

**操作步骤：**
1. 在项目列表，将鼠标悬停在项目上
2. 点击出现的「置顶」图标
3. 项目移动到列表顶部
4. 再次点击可取消置顶

### 5.5 环境管理

**创建环境：**
1. 进入项目
2. 点击「设置」→「环境管理」
3. 点击「添加环境」
4. 填写环境信息：
   - 环境名称：`生产环境`
   - Base URL：`https://api.production.com`
5. 添加变量：
   | 变量名 | 值 | 说明 |
   |--------|-----|------|
   | api_key | prod-key-xxx | API 密钥 |
   | timeout | 30 | 超时时间（秒）|
   | enable_log | true | 是否启用日志 |

**变量引用语法：**
```
在请求中使用 {变量名} 引用
例如：{api_key}、{BASE_URL}/users
```

**导出环境为 Docker Compose：**
1. 环境列表点击「导出」
2. 选择「Docker Compose 格式」
3. 复制生成的 .env 内容

### 5.6 密钥管理

**敏感变量加密：**
1. 在环境变量中，将敏感变量标记为「密钥」
2. 密钥值在界面中显示为 `********`
3. 仅项目管理员可查看实际值

---

## 6. API 测试

### 6.1 创建集合

**操作步骤：**
1. 进入项目
2. 点击左侧菜单「API 测试」
3. 点击「创建集合」
4. 填写集合信息：
   - 集合名称：`用户管理模块`
   - 描述：`包含用户注册、登录、信息修改等接口`
5. 点击「创建」

### 6.2 创建请求

**基础请求创建：**
1. 进入集合
2. 点击「新建请求」
3. 填写请求配置：

**请求配置示例：**
```
请求名称：创建用户
HTTP 方法：POST
URL：{BASE_URL}/users
```

**请求头配置：**
```
Content-Type: application/json
Authorization: Bearer {token}
X-Request-ID: {uuid}
```

**请求体配置（JSON）：**
```json
{
  "username": "testuser",
  "email": "test@example.com",
  "password": "Password123!",
  "age": 25
}
```

**查询参数配置：**
| 参数名 | 值 | 说明 |
|--------|-----|------|
| page | 1 | 页码 |
| page_size | 20 | 每页数量 |
| sort | created_at | 排序字段 |

### 6.3 认证配置

**Bearer Token：**
1. 点击「认证」标签
2. 选择类型：「Bearer Token」
3. 输入 Token：`{auth_token}`

**Basic Auth：**
```
用户名：admin
密码：password
```

**API Key：**
```
Key 名称：X-API-Key
值：{api_key}
位置：Header
```

**OAuth 2.0：**
```
授权 URL：https://auth.example.com/oauth/authorize
Token URL：https://auth.example.com/oauth/token
客户端 ID：your-client-id
客户端密钥：your-client-secret
范围：read write
```

### 6.4 环境变量使用

**变量类型：**
| 类型 | 语法 | 说明 |
|------|------|------|
| 环境变量 | `{variable_name}` | 环境管理中定义的变量 |
| 系统变量 | `{{timestamp}}` | 当前时间戳 |
| 系统变量 | `{{uuid}}` | 随机 UUID |
| 系统变量 | `{{randomInt}}` | 随机整数 |
| 系统变量 | `{{randomInt:1-100}}` | 1-100 随机整数 |

**实际使用示例：**
```
URL: https://api.example.com/users/{user_id}
Header: Authorization: Bearer {access_token}
Body: {"created_at": "{{timestamp}}"}
```

### 6.5 预请求脚本

**用途：** 在发送请求前执行 JavaScript 代码

**示例代码：**
```javascript
// 生成随机用户名
const randomSuffix = Math.floor(Math.random() * 10000);
const username = "user_" + randomSuffix;

// 设置环境变量供后续请求使用
pm.environment.set("generatedUsername", username);

// 添加时间戳 header
const timestamp = Date.now();
pm.request.headers.add({
    key: "X-Timestamp",
    value: timestamp
});

// 生成签名
const data = pm.request.body.raw;
const signature = CryptoJS.HmacSHA256(data, "secret-key").toString();
pm.request.headers.add({
    key: "X-Signature",
    value: signature
});
```

### 6.6 断言配置

**添加断言：**
1. 请求编辑器下方点击「测试」标签
2. 点击「添加断言」

**常用断言类型：**

**状态码断言：**
```
Status code: 状态码等于 200
pm.response.code === 200
```

**响应时间断言：**
```
Response time: 小于 500ms
pm.response.responseTime < 500
```

**JSON 响应断言：**
```javascript
// 验证返回的 JSON 数据
const responseJson = pm.response.json();

// 验证用户 ID 存在
pm.test("用户 ID 存在", function() {
    pm.expect(responseJson.data.id).to.exist;
});

// 验证用户名为测试值
pm.test("用户名正确", function() {
    pm.expect(responseJson.data.username).to.equal("testuser");
});

// 验证数组长度
pm.test("返回至少 5 条数据", function() {
    pm.expect(responseJson.data).to.have.length.above(4);
});

// 验证字段类型
pm.test("用户 ID 是数字", function() {
    pm.expect(responseJson.data.id).to.be.a('number');
});
```

**Header 断言：**
```javascript
pm.test("Content-Type 正确", function() {
    pm.expect(pm.response.headers.get("Content-Type"))
        .to.include("application/json");
});
```

**响应体文本断言：**
```javascript
pm.test("响应包含成功消息", function() {
    pm.expect(pm.response.text()).to.include("success");
});
```

### 6.7 后置脚本

**用途：** 在收到响应后执行 JavaScript 代码

**示例代码：**
```javascript
// 解析响应
const responseJson = pm.response.json();

// 保存 Token 供后续请求使用
if (responseJson.data && responseJson.data.token) {
    pm.environment.set("access_token", responseJson.data.token);
}

// 提取用户 ID
if (responseJson.data && responseJson.data.id) {
    pm.collectionVariables.set("user_id", responseJson.data.id);
}

// 验证并保存数据
if (responseJson.data && responseJson.data.list) {
    const firstItem = responseJson.data.list[0];
    if (firstItem) {
        pm.environment.set("first_item_id", firstItem.id);
    }
}

// 记录响应日志
console.log("响应状态:", pm.response.code);
console.log("响应时间:", pm.response.responseTime + "ms");
console.log("用户数量:", responseJson.data.total);
```

### 6.8 执行请求

**单请求执行：**
1. 配置好请求
2. 选择运行环境（下拉框）
3. 点击「发送」按钮
4. 查看响应结果

**响应查看：**
- 「Body」标签：查看响应内容（支持 JSON/HTML/XML 格式化）
- 「Header」标签：查看响应头
- 「Cookie」标签：查看设置的 Cookie
- 「Timeline」标签：查看请求时间线

**批量执行：**
1. 返回集合列表
2. 点击集合右侧「···」→「运行」
3. 选择运行环境
4. （可选）勾选「失败时停止」
5. 点击「开始运行」

### 6.9 导入 Postman 集合

**操作步骤：**
1. 点击集合列表「导入」
2. 选择导入方式：
   - 上传文件：选择 Postman 导出的 JSON 文件
   - 粘贴文本：将 JSON 内容粘贴到文本框
3. 选择导入选项：
   - 「覆盖」：同名集合会被覆盖
   - 「新建」：总是创建新集合
   - 「合并」：合并到现有集合
4. 点击「导入」

### 6.10 导入 HAR 文件

**操作步骤：**
1. 打开浏览器开发者工具（F12）
2. 切换到「Network」标签
3. 访问需要抓取的页面
4. 右键选择「Save all as HAR」
5. 在 FullScopeTest 点击「导入 HAR」
6. 选择保存的 HAR 文件
7. 系统自动解析生成测试用例

### 6.11 cURL 导入

**操作步骤：**
1. 复制 cURL 命令
2. 点击「导入」→「粘贴 cURL」
3. 粘贴命令内容
4. 点击「解析并导入」

**示例 cURL：**
```bash
curl -X POST https://api.example.com/users \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer {token}" \
  -d '{"username": "test", "email": "test@example.com"}'
```

### 6.12 版本历史

**查看版本历史：**
1. 打开任意请求
2. 点击右上角「历史」图标
3. 列表显示所有版本：
   - 版本号
   - 修改时间
   - 修改人
   - 修改内容摘要

**对比版本：**
1. 勾选两个版本
2. 点击「对比」
3. 差异高亮显示

**回滚版本：**
1. 选择要回滚的版本
2. 点击「恢复到此版本」
3. 确认恢复

### 6.13 响应历史

**查看历史响应：**
1. 请求执行完成后
2. 点击「保存响应」按钮
3. 在「响应历史」面板查看保存的响应

**对比响应：**
1. 选择两个响应记录
2. 点击「对比」
3. 查看差异

### 6.14 数据驱动测试

**创建数据源：**
1. 点击集合「数据驱动」
2. 点击「添加数据源」
3. 选择类型（CSV/JSON）
4. 粘贴或上传数据

**CSV 数据示例：**
```csv
username,email,age,expected_status
user1,user1@example.com,25,200
user2,user2@example.com,30,200
user3,user3@example.com,35,400
```

**JSON 数据示例：**
```json
[
  {"username": "user1", "email": "user1@example.com", "age": 25},
  {"username": "user2", "email": "user2@example.com", "age": 30}
]
```

**配置数据迭代：**
1. 在请求中使用 `{username}` 引用数据
2. 设置迭代次数或「运行所有数据」
3. 系统自动使用每行数据执行请求

### 6.13 BDD/Gherkin 场景导入

**BDD 简介：**
BDD（行为驱动开发）使用自然语言风格的 Gherkin 语法描述测试场景，使非技术人员也能理解测试用例。

**支持的 Gherkin 关键字：**
- `Feature`：功能描述
- `Scenario`：测试场景
- `Scenario Outline`：参数化场景
- `Given`：前置条件
- `When`：用户操作
- `Then`：预期结果
- `And`：连接多个步骤
- `But`：连接多个步骤（表示相反）

**示例 Gherkin 场景：**
```gherkin
Feature: 用户登录功能

  Scenario: 使用正确的凭据登录成功
    Given 用户在登录页面
    When 用户输入用户名 "admin" 和密码 "admin123"
    And 用户点击登录按钮
    Then 系统显示登录成功提示
    And 用户被重定向到仪表盘页面

  Scenario: 使用错误的密码登录失败
    Given 用户在登录页面
    When 用户输入用户名 "admin" 和密码 "wrongpassword"
    And 用户点击登录按钮
    Then 系统显示错误提示 "用户名或密码错误"
    And 用户保持在登录页面

  Scenario Outline: 使用不同的用户名格式登录
    Given 用户在登录页面
    When 用户输入用户名 "<username>" 和密码 "<password>"
    And 用户点击登录按钮
    Then 系统显示结果 "<expected_result>"

    Examples: 邮箱格式
      | username         | password   | expected_result         |
      | user@example.com | pass123   | 登录成功              |
      | user@            | pass123   | 格式错误提示          |
      | @example.com     | pass123   | 格式错误提示          |
      | invalid.email    | pass123   | 用户不存在            |
```

**导入步骤：**
1. 在 API 测试页面点击「导入」
2. 选择「BDD/Gherkin」
3. 粘贴或上传 Gherkin 文件
4. 系统自动解析生成测试用例：
   - 每个 `Scenario` 生成一个测试用例
   - `Given/When/Then` 步骤转换为请求配置
5. 点击「确认导入」

**手动编写 BDD 场景：**
1. 在测试编辑器点击「切换到 BDD 视图」
2. 使用语法高亮编辑器编写场景
3. 系统实时验证语法正确性

---

### 6.14 GraphQL 请求支持

**GraphQL 简介：**
GraphQL 是一种 API 查询语言，相比 REST API 更加灵活。

**发送 GraphQL 请求：**
1. 请求方法选择「POST」
2. URL 填写 GraphQL 端点
3. 请求头设置：
```
Content-Type: application/json
```
4. 请求体格式：
```json
{
  "query": "{ user(id: 1) { id name email } }"
}
```

**带变量的 GraphQL 请求：**
```json
{
  "query": "mutation CreateUser($input: UserInput!) { createUser(input: $input) { id name } }",
  "variables": {
    "input": {
      "username": "newuser",
      "email": "new@example.com",
      "password": "Password123!"
    }
  }
}
```

**GraphQL 片段复用：**
```json
{
  "query": "{ users { ...UserFields } }",
  "fragments": {
    "UserFields": "fragment UserFields on User { id name email createdAt }"
  }
}
```

**断言 GraphQL 响应：**
```javascript
// 验证 GraphQL 响应
const response = pm.response.json();

// 验证 errors 字段为空
pm.test("无 GraphQL 错误", function() {
    pm.expect(response.errors).to.be.undefined;
});

// 验证数据存在
pm.test("用户数据存在", function() {
    pm.expect(response.data.user).to.exist;
    pm.expect(response.data.user.name).to.equal("张三");
});
```

---

### 6.15 WebSocket 测试

**WebSocket 简介：**
WebSocket 是一种双向通信协议，适用于实时应用。

**配置 WebSocket 连接：**
1. 点击「添加请求」→「WebSocket」
2. 填写连接信息：
```
URL: wss://api.example.com/ws
协议: (可选，如需认证)
```

**连接参数：**
```
连接超时: 10 (秒)
Ping 间隔: 30 (秒)
```

**发送消息：**
1. 连接成功后，在消息编辑器输入：
```json
{
  "type": "subscribe",
  "channel": "user_updates",
  "user_id": 123
}
```
2. 点击「发送」按钮

**接收消息：**
1. 消息列表自动显示接收到的消息
2. 支持消息时间戳
3. 支持消息类型筛选

**设置断言：**
```javascript
// 验证 WebSocket 消息内容
pm.test("收到正确类型的消息", function() {
    const messages = pm.ws.getMessages();
    const lastMessage = messages[messages.length - 1];
    const data = JSON.parse(lastMessage.data);
    pm.expect(data.type).to.equal("update");
});
```

---

### 6.16 gRPC 请求支持

**gRPC 简介：**
gRPC 是高性能、开源的通用 RPC 框架。

**配置 gRPC 请求：**
1. 点击「添加请求」→「gRPC」
2. 填写服务信息：
```
URL: api.example.com:50051
服务定义: (proto 文件内容或 URL)
```

**proto 服务定义示例：**
```protobuf
syntax = "proto3";

package user;

service UserService {
  rpc GetUser (UserRequest) returns (UserResponse);
  rpc CreateUser (CreateUserRequest) returns (UserResponse);
}

message UserRequest {
  int32 id = 1;
}

message CreateUserRequest {
  string username = 1;
  string email = 2;
  string password = 3;
}

message UserResponse {
  int32 id = 1;
  string username = 2;
  string email = 3;
  string created_at = 4;
}
```

**发送 gRPC 请求：**
1. 选择服务和方法：`UserService.GetUser`
2. 填写请求体：
```json
{
  "id": 1
}
```
3. 点击「调用」按钮
4. 查看响应结果

---

### 6.17 请求场景编排

**场景简介：**
场景编排可以将多个请求串联起来，实现复杂的业务流程测试。

**创建场景：**
1. 点击集合中的「新建场景」
2. 填写场景信息：
   - 场景名称：`用户完整注册流程`
3. 从左侧拖拽请求到场景中

**场景配置：**
```
请求 1: 创建用户
  ↓
请求 2: 获取用户信息（使用请求1的user_id）
  ↓
请求 3: 更新用户信息
  ↓
请求 4: 删除用户
```

**变量传递：**
```javascript
// 请求1后置脚本：保存返回的 user_id
const response = pm.response.json();
if (response.data && response.data.id) {
    pm.variables.set("created_user_id", response.data.id);
}

// 请求2中引用变量
URL: {BASE_URL}/users/{created_user_id}

// 请求3中继续使用
URL: {BASE_URL}/users/{created_user_id}
Body: {"name": "新名称"}
```

**条件执行：**
```javascript
// 前置脚本：根据条件决定是否执行
if (pm.variables.get("skip_update") === "true") {
    // 跳过此步骤
    throw new Error("SKIP_STEP");
}
```

**循环执行：**
```
循环配置:
  数据源: [1, 2, 3, 4, 5]
  变量名: user_id
  请求: {BASE_URL}/users/{user_id}
```

**错误处理：**
```
错误处理配置:
  遇到错误: 停止执行
  重试次数: 3
  重试间隔: 1 (秒)
```

---

### 6.18 并发执行配置

**并发执行简介：**
并发执行可以同时运行多个请求，模拟真实用户行为。

**配置并发：**
1. 点击集合的「高级运行」
2. 勾选「启用并发」
3. 设置并发参数：
```
并发数: 10
每个请求执行次数: 5
总执行次数: 50
```

**执行模式：**
- 恒定并发：始终保持 10 个并发请求
- 阶梯并发：逐步增加并发数

**阶梯并发配置：**
```
阶段 1: 5 并发，持续 10 秒
阶段 2: 10 并发，持续 20 秒
阶段 3: 20 并发，持续 30 秒
阶段 4: 10 并发，持续 10 秒
阶段 5: 5 并发，持续 10 秒
```

**查看并发结果：**
- 总执行时间
- 成功/失败统计
- 平均响应时间
- P95 响应时间
- 吞吐量 (TPS)

---

### 6.19 请求加密与签名

**常用加密方式：**

**MD5 签名：**
```javascript
// 前置脚本
const timestamp = Date.now();
const data = pm.request.body.raw + timestamp;
const signature = CryptoJS.MD5(data).toString();

pm.request.headers.add({
    key: "X-Timestamp",
    value: timestamp
});
pm.request.headers.add({
    key: "X-Signature",
    value: signature
});
```

**SHA-256 签名：**
```javascript
const secret = "your-secret-key";
const timestamp = Math.floor(Date.now() / 1000);
const nonce = pm.variables.get("nonce") || pm.lodash.random(100000, 999999);
const signStr = secret + timestamp + nonce;

pm.request.headers.add({
    key: "X-Timestamp",
    value: timestamp.toString()
});
pm.request.headers.add({
    key: "X-Nonce",
    value: nonce.toString()
});
pm.request.headers.add({
    key: "X-Sign",
    value: CryptoJS.SHA256(signStr).toString()
});
```

**AES 加密请求体：**
```javascript
const key = CryptoJS.enc.Utf8.parse("your-16-byte-key");
const iv = CryptoJS.enc.Utf8.parse("your-16-byte-iv");
const encrypted = CryptoJS.AES.encrypt(pm.request.body.raw, key, {
    iv: iv,
    mode: CryptoJS.mode.CBC,
    padding: CryptoJS.pad.Pkcs7
});

pm.request.body.raw = JSON.stringify({
    data: encrypted.toString()
});
```

---

### 6.20 响应脱敏与数据处理

**响应脱敏规则：**
1. 进入项目设置
2. 点击「数据脱敏」
3. 添加脱敏规则：
```
字段: response.body.data.user.phone
规则: 掩码
模式: 138****5678
```

**可用脱敏模式：**
| 模式 | 原值 | 脱敏后 |
|------|------|--------|
| 手机号掩码 | 13812345678 | 138****5678 |
| 邮箱掩码 | user@example.com | u***@example.com |
| 身份证掩码 | 110101199001011234 | 110101********1234 |
| 姓名掩码 | 张三 | 张* |
| 自定义正则 | - | 自定义匹配规则 |

**后置脚本数据处理：**
```javascript
// 提取并处理响应数据
const response = pm.response.json();

// 提取嵌套数据
const userName = response.data.user.profile.name;
const userId = response.data.user.id;

// 过滤数组
const activeUsers = response.data.users.filter(u => u.status === "active");

// 转换数据格式
const formattedUsers = activeUsers.map(u => ({
    id: u.id,
    name: u.name,
    email: u.email
}));

// 保存处理后的数据
pm.environment.set("processedUsers", JSON.stringify(formattedUsers));
```

---

## 7. Web 自动化测试

### 7.1 创建 Web 测试集合

**操作步骤：**
1. 进入项目
2. 点击左侧菜单「Web 测试」
3. 点击「创建集合」
4. 填写信息：
   - 集合名称：`登录流程测试`
   - 描述：`测试用户登录全流程`
5. 点击「创建」

### 7.2 录制测试脚本

**开始录制：**
1. 进入 Web 测试集合
2. 点击「开始录制」
3. 选择浏览器（Chrome/Firefox/Safari）
4. 浏览器启动并打开目标网站
5. 开始操作（如：登录、填写表单、点击按钮）

**录制过程：**
- 录制器自动捕获操作
- 每个操作显示为一行步骤
- 支持暂停/继续录制

**停止录制：**
1. 完成所有操作
2. 点击浏览器插件中的「停止录制」
3. 系统自动生成测试脚本

**录制选项：**
- 截图模式：每步截图 vs 仅失败时截图
- 等待策略：智能等待 vs 固定等待
- 隐式等待时间（毫秒）

### 7.3 元素选择器

**选择器类型：**
| 类型 | 示例 | 说明 |
|------|------|------|
| CSS | `#username` | ID 选择器 |
| CSS | `.btn-submit` | Class 选择器 |
| CSS | `input[name="email"]` | 属性选择器 |
| CSS | `form > button` | 层级选择器 |
| XPath | `//input[@id="username"]` | XPath 选择器 |
| XPath | `//button[contains(text(),"登录")]` | 文本选择器 |

**优化选择器：**
1. 右键点击元素
2. 选择「复制选择器」
3. 选择「AI 优化选择器」让 AI 优化

### 7.4 脚本编辑器

**查看录制的步骤：**
```
步骤 1: 打开 URL https://example.com/login
步骤 2: 点击元素 #username (输入框)
步骤 3: 输入文本 admin
步骤 4: 点击元素 #password (密码框)
步骤 5: 输入密码 **********
步骤 6: 点击元素 button[type="submit"]
步骤 7: 等待元素 .success-message 出现
```

**添加新步骤：**
1. 点击「添加步骤」
2. 选择操作类型：
   - 打开 URL
   - 点击元素
   - 输入文本
   - 悬停
   - 下拉选择
   - 等待元素
   - 滚动
   - 截图
   - 断言

**配置步骤：**
```
操作类型: 输入文本
选择器: #search-input
文本: {{搜索关键词}}
等待时间: 3000 (毫秒)
```

### 7.5 断言配置

**Web 测试断言类型：**

**元素存在断言：**
```
选择器: .error-message
条件: 存在
超时: 5000ms
```

**文本内容断言：**
```
选择器: .user-name
条件: 文本等于 "张三"
```

**元素可见断言：**
```
选择器: .modal
条件: 可见
```

**URL 断言：**
```
条件: URL 包含 "/dashboard"
```

**页面标题断言：**
```
条件: 标题等于 "控制台"
```

### 7.6 执行 Web 测试

**本地执行：**
1. 点击「运行」按钮
2. 选择浏览器
3. 观察执行过程
4. 查看执行结果

**执行配置：**
- 浏览器类型：Chrome/Firefox/Safari
- 视口大小：1920x1080/1366x768/自定义
- 失败截图：开/关
- 视频录制：开/关

**查看执行结果：**
- 通过/失败状态
- 执行时间
- 截图（如有失败）
- 详细日志

### 7.7 视觉回归测试

**配置视觉对比：**
1. 编辑脚本步骤
2. 勾选「视觉回归」
3. 选择对比方式：
   - 与上次运行对比
   - 与基准截图对比

**查看差异：**
1. 执行完成后
2. 点击「视觉差异」标签
3. 查看差异区域（红色高亮）
4. 选择「接受差异」或「拒绝」

### 7.8 批量执行

**执行配置：**
1. 集合列表勾选多个脚本
2. 点击「批量运行」
3. 设置执行参数：
   - 并发数：2
   - 失败重试：1 次
   - 超时时间：5 分钟

### 7.9 浏览器配置

**视口配置：**
| 视口类型 | 尺寸 | 用途 |
|---------|------|------|
| 桌面 1080P | 1920x1080 | 标准桌面 |
| 桌面 720P | 1366x768 | 笔记本 |
| iPad | 768x1024 | 平板 |
| iPhone 14 | 390x844 | 手机 |
| 自定义 | 自定义尺寸 | 特殊需求 |

**浏览器选项配置：**
```
Chrome 配置:
  --disable-popup-blocking  禁用弹窗拦截
  --disable-extensions     禁用扩展
  --start-maximized       启动时最大化
  --disable-notifications  禁用通知
  --no-sandbox           禁用沙箱
  --disable-dev-shm-usage 禁用/dev/shm使用
```

**地理位置模拟：**
```
模拟位置:
  纬度: 39.9042
  经度: 116.4074
  位置: 中国北京
```

---

### 7.10 元素等待策略

**等待策略类型：**

| 策略 | 说明 | 示例 |
|------|------|------|
| 智能等待 | 系统自动判断 | 默认选项 |
| 固定等待 | 强制等待固定时间 | 5000ms |
| 元素可见 | 等待元素可见 | visibilityOf |
| 元素可点击 | 等待元素可点击 | elementToBeClickable |
| 元素存在 | 等待元素存在于 DOM | presenceOf |
| 文本匹配 | 等待文本出现 | textToBePresentInElement |

**配置等待时间：**
```
全局超时: 30000 (毫秒)
轮询间隔: 500 (毫秒)
重试次数: 3
```

**自定义等待条件：**
```javascript
// 自定义等待：等待特定元素包含特定文本
await page.waitForFunction(() => {
    const el = document.querySelector('.status');
    return el && el.textContent.includes('已完成');
}, { timeout: 60000 });
```

---

### 7.11 脚本调试技巧

**逐步执行：**
1. 在脚本中设置断点
2. 点击「调试运行」
3. 逐步执行观察每步效果
4. 查看变量值和页面状态

**日志输出：**
```javascript
// 添加日志输出
console.log('开始执行登录步骤');
console.log('用户名:', username);
console.log('页面标题:', await page.title());

await page.fill('#username', username);
console.log('已输入用户名');

await page.click('#login-btn');
console.log('已点击登录按钮');
```

**截图调试：**
```javascript
// 在关键步骤截图
await page.screenshot({ path: 'step1_before.png', fullPage: true });
await page.click('#submit-btn');
await page.waitForTimeout(2000);
await page.screenshot({ path: 'step2_after_click.png', fullPage: true });
```

**控制台日志查看：**
1. 执行时点击「打开控制台」
2. 查看 JavaScript 控制台输出
3. 查看网络请求详情
4. 查看元素定位信息

---

### 7.12 高级选择器

**文本定位：**
```javascript
// 包含文本
await page.click('text=登录');

// 精确文本
await page.click('text="提交"');

// 正则匹配
await page.click('text=/^确定/');
```

**组合选择器：**
```javascript
// 父元素内定位
await page.click('#form >> text=提交');

// 表格行定位
await page.click('table tr:nth-child(2) >> text=编辑');

// 多个条件
await page.click('button:has-text("删除"):not([disabled])');
```

**Shadow DOM 定位：**
```javascript
// 定位 Shadow DOM 内的元素
const shadowHost = await page.locator('custom-component');
const shadowRoot = await shadowHost.evaluateHandle(el => el.shadowRoot);
const button = await shadowRoot.$('button');
```

**iframe 内定位：**
```javascript
// 定位 iframe
const frame = page.frameLocator('#iframe-id');

// 在 iframe 内定位
await frame.locator('#username').fill('admin');

// 切换到默认内容
await page.frameLocator('iframe[name="content"]').locator('#submit').click();
```

---

### 7.13 文件上传自动化

**基础文件上传：**
```javascript
// 方法1：使用选择器
await page.setInputFiles('input[type="file"]', 'path/to/file.pdf');

// 方法2：拖拽上传
await page.locator('.upload-area').setInputFiles('path/to/image.jpg');

// 方法3：多个文件
await page.locator('input[type="file"]').setInputFiles([
    'file1.pdf',
    'file2.pdf'
]);
```

**处理动态上传：**
```javascript
// 先触发文件选择对话框
await page.evaluate(() => {
    const input = document.createElement('input');
    input.type = 'file';
    input.onchange = e => console.log(e.target.files);
    document.body.appendChild(input);
    input.click();
});

// 上传文件
await page.setInputFiles('input[type="file"]', 'path/to/file.pdf');
```

**验证上传结果：**
```javascript
// 检查上传文件名显示
const fileName = await page.locator('.uploaded-file-name').textContent();
console.log('上传的文件:', fileName);

// 检查上传进度
await page.waitForSelector('.upload-progress[style="width: 100%"]', { timeout: 30000 });
console.log('上传完成');
```

---

### 7.14 下载处理

**配置下载选项：**
```javascript
// 设置下载行为
const [download] = await Promise.all([
    page.waitForEvent('download'),
    page.click('#download-btn')
]);

// 获取下载路径
const path = await download.path();
console.log('下载文件路径:', path);

// 保存到指定位置
await download.saveAs('C:/downloads/file.pdf');
```

**无头模式下载：**
```javascript
// 配置浏览器下载
const context = await browser.newContext({
    acceptDownloads: true
});

const page = await context.newPage();
await page.goto('https://example.com');

// 下载文件
const downloadPromise = page.waitForEvent('download');
await page.click('#download-btn');
const download = await downloadPromise;
```

---

### 7.15 键盘和鼠标操作

**键盘操作：**
```javascript
// 模拟键盘输入
await page.keyboard.type('Hello World');

// 按键操作
await page.keyboard.press('Enter');
await page.keyboard.press('Tab');
await page.keyboard.press('Escape');

// 组合键
await page.keyboard.press('Control+a');  // 全选
await page.keyboard.press('Control+c');  // 复制
await page.keyboard.press('Control+v');  // 粘贴
await page.keyboard.press('Control+z');  // 撤销

// 按键修饰符
await page.keyboard.down('Shift');
await page.keyboard.press('ArrowLeft');
await page.keyboard.up('Shift');
```

**鼠标操作：**
```javascript
// 单击
await page.mouse.click(100, 200);

// 双击
await page.mouse.dblclick(100, 200);

// 右键
await page.mouse.click(100, 200, { button: 'right' });

// 拖拽
await page.mouse.move(100, 100);
await page.mouse.down();
await page.mouse.move(200, 200);
await page.mouse.up();
```

**悬停和下拉菜单：**
```javascript
// 悬停
await page.hover('.dropdown-trigger');

// 点击下拉项
await page.click('.dropdown-menu >> text=选项1');

// 选择下拉选项
await page.selectOption('select#country', 'CN');
await page.selectOption('select#country', { label: '中国' });
await page.selectOption('select#country', { value: 'cn' });
```

---

### 7.16 滚动操作

**页面滚动：**
```javascript
// 滚动到顶部
await page.evaluate(() => window.scrollTo(0, 0));

// 滚动到底部
await page.evaluate(() => window.scrollTo(0, document.body.scrollHeight));

// 滚动到元素
await page.locator('#target-element').scrollIntoViewIfNeeded();

// 平滑滚动
await page.evaluate(() => {
    window.scrollBy({
        top: 500,
        behavior: 'smooth'
    });
});
```

**无限滚动加载：**
```javascript
// 等待新内容加载
let previousCount = 0;
let currentCount = await page.locator('.item').count();

while (currentCount > previousCount) {
    previousCount = currentCount;
    await page.evaluate(() => window.scrollBy(0, 1000));
    await page.waitForTimeout(2000);  // 等待加载
    currentCount = await page.locator('.item').count();
}
```

---

### 7.17 Cookie 和缓存管理

**操作 Cookie：**
```javascript
// 获取 Cookie
const cookies = await page.context().cookies();
console.log('当前 Cookie:', cookies);

// 设置 Cookie
await page.context().addCookies([{
    name: 'session_id',
    value: 'abc123',
    domain: 'example.com',
    path: '/',
    httpOnly: true,
    secure: true
}]);

// 删除 Cookie
await page.context().clearCookies();
await page.context().clearCookies([{ name: 'session_id' }]);
```

**清除缓存：**
```javascript
// 清除所有缓存
await page.context().clearCookies();
await page.context().clearPermissions();

// 清除特定域名的缓存
await page.context().clearCookies([{
    domain: 'example.com'
}]);
```

---

### 7.18 弹窗处理

**对话框类型：**

**Alert 弹窗：**
```javascript
page.on('dialog', async dialog => {
    console.log('Alert 内容:', dialog.message());
    await dialog.accept();  // 点击确定
    // 或 await dialog.dismiss();  // 点击取消
});
await page.click('#alert-btn');
```

**Confirm 确认框：**
```javascript
page.on('dialog', async dialog => {
    console.log('Confirm 内容:', dialog.message());
    await dialog.accept();  // 确认
});
await page.click('#confirm-btn');
```

**Prompt 输入框：**
```javascript
page.on('dialog', async dialog => {
    await dialog.accept('用户输入的内容');  // 输入内容并确认
});
await page.click('#prompt-btn');
```

**iframe 弹窗：**
```javascript
// 等待 iframe 加载
const frame = page.frameLocator('iframe[name="modal"]');
await frame.locator('button.confirm').click();
```

---

### 7.19 网络请求拦截

**拦截请求：**
```javascript
// 监听请求
page.on('request', request => {
    console.log('请求 URL:', request.url());
    console.log('请求方法:', request.method());
    console.log('请求头:', request.headers());
});

// 拦截并修改请求
await page.route('**/api/**', route => {
    route.continue({
        url: 'https://mock.example.com' + route.request().url().replace('**/api', '')
    });
});
```

**Mock 响应：**
```javascript
// Mock API 响应
await page.route('**/api/users', route => {
    route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({
            data: [
                { id: 1, name: '用户1' },
                { id: 2, name: '用户2' }
            ]
        })
    });
});

// 模拟延迟
await page.route('**/api/**', route => {
    setTimeout(() => route.continue(), 3000);  // 3秒延迟
});
```

**阻止请求：**
```javascript
// 阻止特定请求
await page.route('**/analytics/**', route => route.abort());
await page.route('**/ads/**', route => route.abort());
```

---

### 7.20 多标签页和窗口

**处理多标签：**
```javascript
// 打开新标签页
const [newPage] = await Promise.all([
    page.context().waitForEvent('page'),
    page.click('#open-new-tab')  // 点击触发新标签页的按钮
]);

// 在新标签页操作
await newPage.goto('https://example.com');
await newPage.fill('#search', '关键词');
await newPage.click('#search-btn');

// 关闭标签页
await newPage.close();

// 切换回主标签页
await page.bringToFront();
```

**处理多窗口：**
```javascript
// 监听新窗口
page.on('popup', async popup => {
    await popup.waitForLoadState();
    console.log('新窗口 URL:', popup.url());
});

// 等待窗口打开
const [popup] = await Promise.all([
    page.context().waitForEvent('page'),
    page.click('#open-window')
]);

// 操作完成后关闭
await popup.close();
```

---

### 7.21 性能监控

**收集性能指标：**
```javascript
// 获取性能指标
const metrics = await page.metrics();
console.log('JS堆大小:', metrics.JSHeapUsedSize);
console.log('节点数量:', metrics.Nodes);

// 收集性能日志
await page.evaluate(() => {
    const observer = new PerformanceObserver(list => {
        for (const entry of list.getEntries()) {
            console.log(entry.name, entry.startTime, entry.duration);
        }
    });
    observer.observe({ entryTypes: ['measure', 'paint', 'navigation'] });
});
```

**测量页面加载时间：**
```javascript
// 测量页面加载时间
const [response] = await Promise.all([
    page.waitForNavigation(),
    page.click('#submit-btn')
]);

const timing = await page.evaluate(() => {
    const [navigation] = performance.getEntriesByType('navigation');
    return {
        dns: navigation.domainLookupEnd - navigation.domainLookupStart,
        tcp: navigation.connectEnd - navigation.connectStart,
        ttfb: navigation.responseStart - navigation.requestStart,
        download: navigation.responseEnd - navigation.responseStart,
        total: navigation.loadEventEnd - navigation.startTime
    };
});

console.log('DNS查询:', timing.dns + 'ms');
console.log('TCP连接:', timing.tcp + 'ms');
console.log('首字节时间:', timing.ttfb + 'ms');
console.log('内容下载:', timing.download + 'ms');
console.log('总加载时间:', timing.total + 'ms');
```

---

### 7.22 异常处理与重试

**配置重试：**
```
重试配置:
  自动重试: 是
  重试次数: 3
  重试间隔: 1 (秒)
  重试条件: 网络错误/超时
```

**脚本内重试逻辑：**
```javascript
// 自定义重试逻辑
async function retryOperation(operation, maxRetries = 3) {
    for (let i = 0; i < maxRetries; i++) {
        try {
            return await operation();
        } catch (error) {
            if (i === maxRetries - 1) throw error;
            console.log(`重试 ${i + 1}/${maxRetries}`);
            await page.waitForTimeout(1000 * (i + 1));
        }
    }
}

// 使用
await retryOperation(async () => {
    await page.click('#dynamic-button');
    await page.waitForSelector('.result', { timeout: 5000 });
});
```

**错误处理：**
```javascript
try {
    await page.click('#may-not-exist');
} catch (error) {
    if (error.message.includes('Timeout')) {
        console.log('操作超时');
        // 处理超时
    } else if (error.message.includes('not visible')) {
        console.log('元素不可见');
        // 处理不可见情况
    } else {
        console.log('其他错误:', error.message);
        throw error;
    }
}
```

---

## 8. APP 自动化测试

### 8.1 设备管理

**连接设备：**
1. 点击左侧菜单「APP 测试」→「设备管理」
2. 点击「添加设备」
3. 选择设备类型：
   - Android 真机
   - iOS 真机（需要 Mac）
   - Android 模拟器

**Android 真机配置：**
```
设备类型: Android 真机
连接方式: USB
ADB 地址: 127.0.0.1:5555
```

**模拟器配置：**
```
设备类型: Android 模拟器
模拟器: 自定义
地址: localhost:7555
```

### 8.2 创建 APP 测试脚本

**新建脚本：**
1. 点击「APP 测试」→「创建脚本」
2. 选择目标 APP：
   - 已安装应用：选择已安装的应用
   - APK 文件：上传 APK 文件
   - 应用包名：输入包名（如 com.example.app）
3. 配置应用入口 Activity
4. 点击「开始录制」

### 8.3 录制 APP 操作

**录制步骤：**
1. 设备上应用启动
2. 在 FullScopeTest 点击录制
3. 在设备上进行操作
4. 系统自动记录操作步骤

**支持的录制动操作：**
- 点击元素
- 长按元素
- 输入文本
- 滑动
- 滚动
- 截图
- 等待

### 8.4 元素检查器

**打开元素检查器：**
1. 在 APP 测试页面
2. 点击「元素检查器」按钮
3. 在右侧查看当前页面元素树

**查看元素信息：**
```
元素类型: android.widget.EditText
资源 ID: com.example.app:id/username
文本: (空)
位置: (100, 200)
尺寸: (300, 80)
```

### 8.5 APP 测试断言

**支持的断言：**
- 元素存在
- 元素文本包含
- 元素可见
- 元素可点击
- 当前 Activity
- 屏幕截图对比

### 8.6 执行 APP 测试

**执行步骤：**
1. 选择目标设备
2. 点击「运行」
3. 观察执行过程
4. 查看执行结果

**多设备并发执行：**
1. 勾选多个设备
2. 点击「并发运行」
3. 查看各设备执行结果

### 8.7 APP 测试断言详解

**元素存在断言：**
```javascript
// 验证元素存在
assert(element_exists("#username"), "用户名输入框应该存在");

// 验证元素不存在
assert(!element_exists(".error-message"), "错误提示应该消失");
```

**元素文本断言：**
```javascript
// 验证文本内容
assert(get_text(".welcome-message") === "欢迎, 用户", "欢迎消息正确");

// 验证文本包含
assert(get_text(".status").includes("在线"), "状态应该包含'在线'");

// 验证正则匹配
assert(get_text(".phone").match(/^1[3-9]\d{9}$/), "手机号格式正确");
```

**元素状态断言：**
```javascript
// 验证元素可见
assert(is_visible(".submit-btn"), "提交按钮应该可见");

// 验证元素可点击
assert(is_enabled(".submit-btn"), "提交按钮应该可点击");

// 验证元素选中
assert(is_selected(".checkbox"), "复选框应该被选中");

// 验证元素获取焦点
assert(has_focus("#input-field"), "输入框应该获取焦点");
```

**元素属性断言：**
```javascript
// 验证属性值
assert(get_attribute(".avatar", "src").includes("avatar.jpg"), "头像URL正确");

// 验证样式
assert(get_css(".status", "color") === "rgb(0, 128, 0)", "颜色正确");

// 验证元素数量
assert(count(".list-item") === 5, "列表应该有5项");
```

**Activity 断言：**
```javascript
// 验证当前 Activity
assert(get_current_activity() === "com.example.MainActivity", "应该在主界面");

// 验证 Activity 包含
assert(get_current_activity().includes("Login"), "应该在登录相关界面");
```

**截图对比断言：**
```javascript
// 像素差异阈值
assert(screenshot_compare("baseline.png", 0.95), "相似度应该>=95%");

// 允许抖动区域
assert(screenshot_compare("baseline.png", 0.90, ignore_regions=[".dynamic-content"]), 
    "允许动态内容差异");
```

---

### 8.8 APP 测试数据驱动

**CSV 数据源：**
```csv
username,password,expected_result
testuser1,pass123,登录成功
testuser2,pass456,登录成功
invalid,123,登录失败
```

**JSON 数据源：**
```json
[
    {
        "username": "user1",
        "password": "pass1",
        "test_data": {
            "nickname": "用户1",
            "age": 25
        }
    },
    {
        "username": "user2",
        "password": "pass2",
        "test_data": {
            "nickname": "用户2",
            "age": 30
        }
    }
]
```

**Excel 数据源：**
```
用户数据.xlsx:
| username | password | age | expected |
|----------|----------|-----|----------|
| user1    | pass1   | 25  | 成功     |
| user2    | pass2   | 30  | 成功     |
```

---

### 8.9 APP 测试最佳实践

**元素定位策略：**
| 优先级 | 定位方式 | 示例 |
|--------|----------|------|
| 1 | resource-id | `com.example.app:id/username` |
| 2 | accessibility-id | `username_input` |
| 3 | text | `text="登录"` |
| 4 | class + index | `android.widget.EditText[0]` |

**等待策略：**
```javascript
// 推荐：使用智能等待
await wait_for_element("#username", timeout=10000);

// 避免：使用固定等待
await sleep(5000); // 不推荐
```

**测试分层：**
```
Page Object Model 结构:
├── pages/
│   ├── LoginPage.js
│   ├── HomePage.js
│   └── ProfilePage.js
├── tests/
│   ├── login.test.js
│   └── profile.test.js
└── data/
    └── test-data.json
```

---

## 9. 性能测试

### 9.1 创建性能测试场景

**基础配置：**
1. 点击左侧菜单「性能测试」
2. 点击「创建场景」
3. 填写场景信息：
   - 场景名称：`API 负载测试`
   - 描述：`测试用户接口在并发下的性能`

### 9.2 配置负载参数

**基础参数：**
```
用户数: 100
Spawn Rate: 10 (每秒启动用户数)
持续时间: 300 (秒)
预热时间: 30 (秒)
```

**负载模式：**
- 恒定负载：固定用户数持续运行
- 阶梯负载：逐步增加用户数
- 峰值负载：瞬间达到高并发
- 自定义曲线：自定义用户变化

**阶梯负载配置示例：**
```
阶段 1: 10 用户，持续 60 秒
阶段 2: 50 用户，持续 60 秒
阶段 3: 100 用户，持续 120 秒
阶段 4: 50 用户，持续 60 秒
阶段 5: 10 用户，持续 60 秒
```

### 9.3 添加请求

**添加单个请求：**
1. 点击「添加请求」
2. 配置请求信息：
```
请求名称: 获取用户列表
HTTP 方法: GET
URL: {BASE_URL}/api/users
权重: 10 (请求被选中的概率)
```

**请求权重说明：**
- 权重用于模拟真实用户行为
- 高频请求设置高权重
- 示例：首页请求权重 50，详情页权重 30，搜索权重 20

### 9.4 配置断言

**性能断言：**
```
平均响应时间 < 500ms
P95 响应时间 < 1000ms
错误率 < 1%
```

### 9.5 配置告警规则

**创建告警规则：**
1. 点击「告警规则」→「添加规则」
2. 配置规则：
   - 规则名称：`响应超时告警`
   - 指标：平均响应时间
   - 条件：`>` (大于)
   - 阈值：2000 (ms)
   - 触发次数：3 (连续 3 次超标触发)

**告警通知：**
- 勾选「启用通知」
- 选择通知方式：邮件/钉钉/飞书
- 设置通知接收人

### 9.6 执行性能测试

**立即执行：**
1. 点击「运行」按钮
2. 确认配置信息
3. 点击「开始测试」
4. 观察实时监控面板

**实时监控指标：**
- 总请求数
- 失败请求数
- 当前并发用户数
- 平均响应时间
- P50/P90/P95/P99 响应时间
- TPS (每秒请求数)

### 9.7 查看性能报告

**报告内容：**
- 执行概览（总请求数、通过率、执行时长）
- 响应时间统计（平均值、最小值、最大值）
- 分位数统计（P50/P90/P95/P99）
- 错误分布
- TPS 趋势图
- 响应时间趋势图

**导出报告：**
1. 点击「导出报告」
2. 选择格式（PDF/HTML/Excel）
3. 下载报告文件

### 9.8 性能基线

**创建基线：**
1. 测试执行完成后
2. 点击「保存为基线」
3. 输入基线名称：`v1.0 性能基线`
4. 点击「保存」

**基线对比：**
1. 执行新测试
2. 点击「对比基线」
3. 选择要对比的基线
4. 查看性能变化百分比

### 9.9 Locust 脚本自定义

**Locust 脚本结构：**
```python
from locust import HttpUser, task, between, events

class WebsiteUser(HttpUser):
    # 模拟用户行为权重
    weight = 3  # 此用户类型占比
    
    # 任务间隔时间
    wait_time = between(1, 3)  # 1-3秒内随机等待
    
    def on_start(self):
        """用户开始时执行一次"""
        # 登录操作
        response = self.client.post("/api/login", json={
            "username": "testuser",
            "password": "test123"
        })
        if response.status_code == 200:
            self.token = response.json()["data"]["token"]
    
    @task(5)  # 权重为5，较高概率执行
    def view_homepage(self):
        """访问首页"""
        self.client.get("/")
    
    @task(3)
    def search_products(self):
        """搜索商品"""
        self.client.get("/api/products?keyword=手机")
    
    @task(2)
    def view_product_detail(self):
        """查看商品详情"""
        self.client.get("/api/products/123")
    
    @task(1)
    def add_to_cart(self):
        """添加购物车"""
        self.client.post("/api/cart", json={
            "product_id": 123,
            "quantity": 1
        }, headers={
            "Authorization": f"Bearer {self.token}"
        })
    
    def on_stop(self):
        """用户结束时执行一次"""
        # 清理操作
        self.client.delete("/api/cart")

class APIPerformanceUser(HttpUser):
    """API 性能测试用户"""
    weight = 2
    
    @task
    def api_metrics(self):
        """获取指标数据"""
        self.client.get("/api/v1/metrics")
    
    @task
    def api_users_list(self):
        """获取用户列表"""
        self.client.get("/api/v1/users?page=1&page_size=20")
```

**高级 Locust 配置：**
```python
# 自定义负载形状
class StepLoadShape(HttpUser):
    """阶梯负载"""
    task_weight = 3
    
    def tick(self):
        """返回 (用户数, 生成速率) 元组"""
        run_time = self.runner.time
        if run_time < 60:
            return 10, 2  # 前1分钟: 10用户
        elif run_time < 120:
            return 50, 5  # 第2分钟: 50用户
        elif run_time < 180:
            return 100, 10  # 第3分钟: 100用户
        elif run_time < 240:
            return 50, 5  # 第4分钟: 50用户
        else:
            return 10, 2  # 第5分钟: 10用户

# 钩子函数
@events.request.add_listener
def on_request(request_type, name, response_time, response_length, exception, **kwargs):
    """请求完成回调"""
    if exception:
        print(f"请求失败: {name}, 错误: {exception}")
    else:
        print(f"请求成功: {name}, 耗时: {response_time}ms")

@events.quitting.add_listener
def on_quitting(environment, **kwargs):
    """测试结束回调"""
    print("测试结束，生成报告...")
```

---

### 9.10 分布式性能测试

**架构说明：**
```
        ┌─────────────┐
        │  Master    │
        │  (协调节点) │
        └──────┬──────┘
               │
       ┌─────┴─────┐
       ▼           ▼
  ┌────────┐  ┌────────┐
  │Worker 1│  │Worker 2│
  │(负载节点)│  │(负载节点)│
  └────┬────┘  └────┬────┘
       │           │
       ▼           ▼
   ┌─────────┐ ┌─────────┐
   │ Target  │ │ Target  │
   │ Server  │ │ Server  │
   └─────────┘ └─────────┘
```

**配置步骤：**
1. 在所有 Worker 机器上安装 Locust
2. 确保 Master 可以 SSH 连接所有 Worker
3. 配置防火墙允许端口 5557 (Master-Worker 通信)

**启动分布式测试：**
```bash
# Master 节点
locust -f locustfile.py \
    --master \
    --master-bind-port=5557 \
    --master-bind-host=192.168.1.10

# Worker 节点
locust -f locustfile.py \
    --worker \
    --master-host=192.168.1.10 \
    --master-port=5557

# 启动 4 个 Worker
for i in {1..4}; do
    locust -f locustfile.py \
        --worker \
        --master-host=192.168.1.10 &
done
```

**Web 界面访问：**
```
http://192.168.1.10:8089
```

---

### 9.11 性能测试指标详解

**关键指标说明：**

| 指标 | 说明 | 优秀标准 |
|------|------|----------|
| RPS (Requests Per Second) | 每秒请求数 | > 1000 |
| 平均响应时间 | 所有请求的平均耗时 | < 200ms |
| P50 (中位数) | 50%请求在此时间内完成 | < 150ms |
| P90 | 90%请求在此时间内完成 | < 500ms |
| P95 | 95%请求在此时间内完成 | < 1000ms |
| P99 | 99%请求在此时间内完成 | < 2000ms |
| 错误率 | 失败请求占比 | < 0.1% |
| 并发用户数 | 同时在线用户数 | 根据实际需求 |
| 吞吐量 | 每秒处理数据量 | > 10MB/s |

**性能测试目标示例：**
```
性能目标:
  目标系统: 用户管理服务
  
  正常场景 (100 并发):
    - 平均响应时间 < 200ms
    - P95 < 500ms
    - 错误率 < 0.1%
    - RPS > 500
  
  峰值场景 (500 并发):
    - 平均响应时间 < 500ms
    - P95 < 1500ms
    - 错误率 < 1%
    - RPS > 2000
```

---

### 9.12 性能瓶颈分析

**常见瓶颈类型：**

| 瓶颈类型 | 症状 | 排查方法 |
|---------|------|----------|
| CPU 瓶颈 | 系统 CPU 100% | 查看 Prometheus CPU 监控 |
| 内存瓶颈 | OOM 或频繁 GC | 查看内存使用和 GC 频率 |
| 数据库瓶颈 | 慢查询增多 | 查看数据库慢查询日志 |
| 网络瓶颈 | 带宽饱和 | 查看网络流量监控 |
| 连接池瓶颈 | 连接等待 | 查看数据库连接数 |

**分析工具：**
```bash
# 查看 CPU 使用
top -Hp <pid>

# 查看内存使用
free -h

# 查看磁盘 IO
iostat -x 1

# 查看网络连接
netstat -an | grep ESTABLISHED | wc -l

# 查看数据库连接
SELECT count(*) FROM pg_stat_activity;
```

---

### 9.13 性能测试报告解读

**报告结构：**
```
性能测试报告 - 用户管理服务
测试时间: 2024-01-15 14:00 - 15:00
测试环境: 测试服务器 (8核16G)

1. 执行摘要
   - 总请求数: 1,234,567
   - 成功请求: 1,232,890 (99.86%)
   - 失败请求: 1,677 (0.14%)
   - 总耗时: 3600秒

2. 响应时间统计
   ┌─────────┬──────────┐
   │  指标   │   耗时   │
   ├─────────┼──────────┤
   │ 平均    │  156ms   │
   │ 最小    │   23ms   │
   │ 最大    │ 2,340ms  │
   │ P50     │  145ms   │
   │ P90     │  312ms   │
   │ P95     │  456ms   │
   │ P99     │  823ms   │
   └─────────┴──────────┘

3. 吞吐量统计
   - 峰值 RPS: 543.21
   - 平均 RPS: 342.93

4. 错误分析
   - 400 错误: 1,234 (超时)
   - 500 错误: 443 (服务异常)

5. 结论
   ✓ 满足性能目标
   ⚠ 建议优化 P99 响应时间
```

---

## 10. 测试计划

### 10.1 创建测试计划

**操作步骤：**
1. 点击左侧菜单「测试计划」
2. 点击「创建计划」
3. 填写信息：
   - 计划名称：`Sprint 15 回归测试`
   - 描述：`Sprint 15 迭代功能回归测试`
   - 开始日期：2024-01-01
   - 结束日期：2024-01-07

### 10.2 添加测试用例

**添加方式：**
1. 进入测试计划
2. 点击「添加用例」
3. 选择用例类型：
   - API 测试用例
   - Web 测试脚本
   - APP 测试脚本
4. 从列表中选择用例
5. 点击「添加」

**用例排序：**
- 拖拽调整执行顺序
- 点击「自动排序」按优先级排序

### 10.3 配置执行环境

**设置运行环境：**
1. 点击测试计划「设置」
2. 选择运行环境：`测试环境`
3. 配置环境变量覆盖

### 10.4 执行测试计划

**手动执行：**
1. 点击「执行」按钮
2. 选择执行选项：
   - 执行所有用例
   - 仅执行选中用例
   - 跳过失败用例重跑
3. 点击「开始执行」

**查看执行结果：**
- 总体进度条
- 通过/失败/跳过统计
- 用例执行明细
- 执行日志

### 10.5 测试用例模板

**创建模板：**
1. 进入项目
2. 点击「测试模板」→「创建模板」
3. 填写模板信息：
   - 模板名称：`标准 API 测试模板`
   - 描述：`包含通用断言的 API 测试模板`

**模板内容：**
```yaml
模板内容:
  包含:
    - 响应时间断言 (< 1000ms)
    - JSON Schema 验证
    - 错误码检查
    - 必填字段检查
```

**使用模板：**
1. 新建测试用例时
2. 选择「从模板创建」
3. 选择需要的模板
4. 自动填充预置内容

---

### 10.6 测试计划报告

**查看计划执行报告：**
1. 进入测试计划详情
2. 点击「执行历史」
3. 选择要查看的执行
4. 查看详细报告

**报告对比：**
1. 勾选多个执行结果
2. 点击「对比」
3. 查看变化趋势：
   - 通过率变化
   - 执行时间变化
   - 失败用例变化

---

### 10.7 测试覆盖率

**覆盖率配置：**
1. 进入测试计划设置
2. 点击「覆盖率配置」
3. 配置覆盖率统计规则：
```
覆盖率统计:
  API 覆盖率: /api/users → 已测试
  API 覆盖率: /api/orders → 未测试
  API 覆盖率: /api/products → 已测试
```

**覆盖率报告：**
- 接口覆盖率
- 用例执行覆盖率
- 功能模块覆盖率

---

### 10.8 缺陷关联

**关联缺陷：**
1. 测试用例执行失败时
2. 点击「关联缺陷」
3. 输入缺陷 ID 或创建新缺陷
4. 缺陷自动同步到测试计划

**缺陷看板：**
- 待处理
- 修复中
- 已修复
- 重新打开

---

## 11. 测试报告

### 11.1 报告中心

**查看所有报告：**
1. 点击左侧菜单「报告中心」
2. 列表显示所有测试报告
3. 支持筛选：
   - 报告类型：API/Web/APP/性能
   - 执行结果：通过/失败
   - 时间范围

### 11.2 报告详情

**报告内容包括：**
- 执行概览
- 用例明细（每个用例的状态、耗时、错误信息）
- 失败用例的详细错误
- 执行时间线
- 环境信息

### 11.3 导出报告

**支持格式：**
- PDF：适合打印和分享
- HTML：适合在线查看
- Excel：适合数据分析
- JSON：适合程序处理

**导出步骤：**
1. 打开报告
2. 点击「导出」
3. 选择格式
4. 点击「生成」
5. 下载文件

### 11.4 定时发送报告

**配置定时报告：**
1. 点击「报告中心」→「定时发送」
2. 点击「新建定时任务」
3. 配置：
   - 任务名称：`每日回归报告`
   - 报告类型：选择测试计划
   - 发送周期：每天 09:00
   - 收件人：user@example.com
4. 点击「保存」

---

## 12. Mock 服务

### 12.1 创建 Mock 服务器

**操作步骤：**
1. 点击左侧菜单「Mock 服务」
2. 点击「创建服务器」
3. 填写信息：
   - 服务器名称：`开发环境 Mock`
   - 描述：`开发阶段使用的 API Mock`
   - Base Path：`/mock-api`

### 12.2 创建 Mock 规则

**基础规则配置：**
1. 进入 Mock 服务器
2. 点击「添加规则」
3. 配置规则：
```
名称：获取用户列表
请求方法：GET
请求路径：/users
```

**响应配置：**
```
状态码：200
响应头：Content-Type: application/json
延迟时间：500 (ms)
```

**响应体：**
```json
{
  "code": 0,
  "message": "success",
  "data": [
    {
      "id": 1,
      "username": "user1",
      "email": "user1@example.com"
    },
    {
      "id": 2,
      "username": "user2",
      "email": "user2@example.com"
    }
  ]
}
```

### 12.3 条件匹配

**参数匹配：**
```
条件类型：Query 参数
参数名：status
匹配方式：等于
值：active
```

**Header 匹配：**
```
条件类型：Header
Header 名：Authorization
匹配方式：包含
值：Bearer
```

**Body 匹配：**
```
条件类型：Body
匹配方式：JSON 包含
内容：{"role": "admin"}
```

### 12.4 动态响应

**多状态响应：**
1. 添加多个响应
2. 设置匹配条件和优先级
3. 系统按优先级匹配第一个满足条件的响应

**随机响应：**
```
响应策略：随机选择
响应1: {"status": "A"}
响应2: {"status": "B"}
响应3: {"status": "C"}
```

**序列响应：**
```
响应策略：按顺序循环
响应1: {"count": 1}
响应2: {"count": 2}
响应3: {"count": 3}
```

### 12.5 测试 Mock

**测试配置：**
1. 配置好 Mock 规则
2. 点击「测试」按钮
3. 填写测试请求：
```
方法: GET
路径: /users?status=active
Headers: {"Authorization": "Bearer test-token"}
```
4. 点击「发送」
5. 查看返回的响应

### 12.6 使用 Mock

**前端开发使用：**
1. 在环境变量中配置：
```
API_BASE_URL: https://test.huangxuan.chat/mock/{mock_server_id}/mock-api
```
2. 前端请求会自动打到 Mock 服务

### 12.7 Mock 服务最佳实践

**使用场景：**
- 前端开发阶段，后端 API 未完成
- 隔离测试，避免外部依赖
- 模拟异常情况
- 第三方服务不可用时

**Mock 响应示例：**
```json
// 正常响应
{
  "code": 200,
  "message": "success",
  "data": { "id": 1, "name": "产品A" }
}

// 错误响应
{
  "code": 404,
  "message": "资源不存在",
  "data": null
}

// 延迟响应
{
  "code": 200,
  "message": "success",
  "data": { "status": "processing" }
}
// 延迟: 3000ms
```

---

## 13. 质量门禁

### 13.1 创建质量门禁规则

**操作步骤：**
1. 点击左侧菜单「质量门禁」
2. 点击「创建规则」
3. 填写信息：
   - 规则名称：`API 测试质量门禁`
   - 描述：`确保 API 测试通过率 >= 95%`

### 13.2 配置评估条件

**配置评估指标：**
```
指标类型：通过率
条件：>=
阈值：95 (%)
```

**支持的条件类型：**
- 通过率
- 失败用例数
- 执行时长
- 覆盖率

### 13.3 配置触发条件

**触发方式：**
- 手动评估：需要时手动触发
- 定时评估：每天定时评估
- CI 触发：CI/CD 流水线触发
- PR 触发：Pull Request 时触发

### 13.4 评估质量门禁

**手动评估：**
1. 点击规则「评估」按钮
2. 选择要评估的测试执行
3. 点击「开始评估」
4. 查看评估结果

**评估结果：**
- 通过：绿色标记
- 失败：红色标记，显示具体失败原因
- 建议：AI 提供的改进建议

### 13.5 质量门禁最佳实践

**门禁规则示例：**

| 规则名称 | 指标 | 条件 | 阈值 | 说明 |
|---------|------|------|------|------|
| API 通过率 | 通过率 | >= | 95% | 确保 API 测试通过率 |
| 核心用例通过率 | 通过率 | >= | 100% | P0 用例必须全部通过 |
| 执行时长 | 总时长 | <= | 300s | 确保执行效率 |
| 失败数上限 | 失败数 | <= | 10 | 限制失败数量 |

**门禁分级：**
```
P0 门禁 (阻断发布):
  - 核心用例必须 100% 通过
  - 响应时间 P95 < 1000ms

P1 门禁 (警告):
  - 通过率 >= 95%
  - 无阻塞性错误

P2 门禁 (提示):
  - 通过率 >= 90%
  - 无严重问题
```

---

## 14. 触发器与自动化

### 14.1 创建触发规则

**操作步骤：**
1. 点击左侧菜单「触发器」
2. 点击「创建规则」
3. 填写基本信息：
   - 规则名称：`代码提交自动测试`
   - 描述：`Git Push 时自动运行测试`

### 14.2 配置触发条件

**Git Push 触发：**
```
触发类型：Git Push
仓库：https://github.com/example/repo
分支：main (支持通配符: feature/*)
```

**定时触发：**
```
触发类型：定时执行
Cron 表达式：0 9 * * * (每天 9 点)
说明：每天早上 9 点执行
```

**Webhook 触发：**
```
触发类型：Webhook
触发 URL：https://test.huangxuan.chat/api/v1/triggers/{token}
说明：通过 HTTP 请求触发
```

### 14.3 配置执行动作

**执行测试：**
```
动作类型：执行测试
测试类型：API 测试集合
目标：选择要执行的集合
运行环境：测试环境
```

**发送通知：**
```
动作类型：发送通知
通知方式：钉钉机器人
消息模板：测试执行完成，通过率 {{pass_rate}}%
```

### 14.4 管理定时任务

**创建定时任务：**
1. 点击「定时任务」→「新建任务」
2. 配置：
   - 任务名称：`每日冒烟测试`
   - Cron：`0 8 * * 1-5` (工作日 8 点)
   - 执行动作：选择要执行的测试

**查看任务执行历史：**
1. 进入定时任务详情
2. 点击「执行历史」标签
3. 查看每次执行的时间、结果、耗时

### 14.5 触发器高级配置

**条件组合：**
```
触发条件组合:
  AND 条件:
    - 分支: main
    - 文件变更: 包含 src/api/*
  
  OR 条件:
    - 提交消息: contains [test]
    - 提交消息: contains [ci skip]
```

**执行策略：**
```
执行配置:
  超时时间: 30 分钟
  并发执行: 禁止 (同一分支串行执行)
  失败策略: 发送通知后继续
  重试次数: 0
```

**变量传递：**
```
触发时传递变量:
  - GIT_BRANCH: {{branch}}
  - GIT_COMMIT: {{commit}}
  - GIT_AUTHOR: {{author}}
  - CHANGED_FILES: {{changed_files}}
```

---

### 14.6 GitHub Webhook 配置

**配置 Webhook：**
1. 在 GitHub 仓库设置中点击「Webhooks」→「Add webhook」
2. 配置：
```
Payload URL: https://test.huangxuan.chat/api/v1/webhooks/github
Content type: application/json
Secret: (设置 Webhook Secret)
Events: Push, Pull requests
```

**验证 Webhook：**
1. 在 GitHub 点击「Test」→「Push events」
2. 查看 FullScopeTest 是否收到推送

---

## 15. 通知配置

### 15.1 创建通知配置

**创建钉钉通知：**
1. 点击左侧菜单「系统设置」→「通知配置」
2. 点击「添加通知」
3. 选择类型：钉钉机器人
4. 配置：
   - 名称：`测试结果通知`
   - Webhook 地址：`https://oapi.dingtalk.com/robot/send?access_token=xxx`
   - 签名密钥：（可选）

**创建飞书通知：**
```
类型：飞书机器人
名称：测试通知
Webhook 地址：https://open.feishu.cn/open-apis/bot/v2/hook/xxx
```

**创建邮件通知：**
```
类型：邮件
名称：报告邮件
SMTP 服务器：smtp.example.com
端口：587
用户名：notify@example.com
密码：******
收件人：team@example.com
```

### 15.2 配置通知事件

**支持的通知事件：**
- 测试执行完成
- 测试执行失败
- 定时任务失败
- 性能告警
- 系统异常

**配置示例：**
```
事件：测试执行失败
通知方式：钉钉
触发条件：任何失败时
```

---

## 16. CI/CD 集成

### 16.1 GitHub Actions 集成

**创建 Workflow 文件：**
```yaml
# .github/workflows/api-test.yml
name: API Tests

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  api-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Run API Tests
        run: |
          curl -X POST https://test.huangxuan.chat/api/v1/triggers/${{ secrets.TRIGGER_TOKEN }}
          echo "Tests triggered"
```

### 16.2 Jenkins 集成

**Jenkins Pipeline 配置：**
```groovy
pipeline {
    stages {
        stage('API Test') {
            steps {
                script {
                    def response = httpRequest(
                        url: "https://test.huangxuan.chat/api/v1/triggers/${TRIGGER_TOKEN}",
                        httpMode: 'POST',
                        contentType: 'APPLICATION_JSON',
                        requestBody: '''{"collection_id": 1}'''
                    )
                    echo "Response: ${response.content}"
                }
            }
        }
    }
}
```

### 16.3 GitLab CI 集成

**.gitlab-ci.yml 配置：**
```yaml
api-test:
  script:
    - curl -X POST "https://test.huangxuan.chat/api/v1/triggers/${TRIGGER_TOKEN}"
  only:
    - main
    - develop
```

---

## 17. AI 助手

### 17.1 AI Copilot 聊天

**打开 Copilot：**
1. 点击右下角「AI Copilot」按钮
2. 在弹出窗口中输入问题
3. AI 自动回答

**常用问题示例：**
- "如何创建 API 测试集合？"
- "帮我分析这个测试失败的原因"
- "推荐一些接口测试的边界场景"

### 17.2 AI 生成测试用例

**智能生成：**
1. 在 API 测试页面
2. 点击「AI 助手」图标
3. 输入自然语言描述：
   ```
   生成一个测试用户注册的用例，包括：
   - 正常注册流程
   - 邮箱格式错误
   - 密码强度不足
   - 用户名已存在
   ```
4. 点击「生成」
5. AI 自动生成测试用例
6. 点击「采纳」添加到集合

### 17.3 AI 生成断言

**智能断言：**
1. 执行请求获得响应
2. 点击「AI 生成断言」
3. AI 分析响应结构
4. 自动生成断言：
   - 验证必要字段存在
   - 验证数据类型正确
   - 验证业务规则

### 17.4 AI 评审测试用例

**评审功能：**
1. 打开测试集合
2. 点击「AI 评审」
3. AI 分析用例质量
4. 提供改进建议：
   - 缺少的测试场景
   - 断言不完整
   - 潜在的问题

### 17.5 AI 自愈

**失败用例修复：**
1. 测试用例执行失败
2. 点击「AI 修复建议」
3. AI 分析失败原因
4. 提供修复方案
5. 点击「应用修复」自动更新用例

---

## 18. 视觉回归测试

### 18.1 配置视觉回归

**设置基线截图：**
1. 执行 Web 测试
2. 在执行结果中点击「保存为基线」
3. 系统保存当前页面截图作为基线

### 18.2 执行视觉对比

**对比配置：**
1. 下次执行时勾选「视觉回归」
2. 系统自动截图对比
3. 查看差异报告

### 18.3 查看差异

**差异报告包含：**
- 差异区域标记（红色框）
- 差异百分比
- 像素级差异图

**处理差异：**
- 「接受差异」：更新基线
- 「拒绝差异」：标记为 Bug
- 「忽略」：在配置中忽略此区域

---

## 19. 团队协作

### 19.1 组织管理

**创建组织：**
1. 点击用户头像
2. 选择「创建组织」
3. 填写信息：
   - 组织名称：`测试团队`
   - 组织描述：`QA 团队`
4. 点击「创建」

### 19.2 邀请成员

**邀请步骤：**
1. 进入组织设置
2. 点击「成员管理」→「邀请成员」
3. 输入邮箱地址
4. 选择角色：
   - 管理员：全部权限
   - 成员：普通权限
   - 访客：只读权限
5. 点击「发送邀请」

### 19.3 角色权限

**系统角色：**
| 角色 | 说明 |
|------|------|
| 所有者 | 组织的创建者，拥有全部权限，可删除组织 |
| 管理员 | 管理成员、配置、设置，不能删除组织 |
| 成员 | 创建和执行测试，默认角色 |
| 访客 | 只读权限，可查看测试和报告 |

**自定义角色：**
1. 进入「角色管理」
2. 点击「创建角色」
3. 配置权限：
   - API 测试：创建、编辑、执行、删除
   - Web 测试：创建、编辑、执行、删除
   - 报告：查看、导出
   - 设置：查看、编辑

### 19.4 评论与讨论

**添加评论：**
1. 打开任意测试用例
2. 点击「评论」标签
3. 输入评论内容
4. 支持 @提及 团队成员
5. 点击「发送」

### 19.5 查看审计日志

**审计日志内容：**
- 用户登录/登出
- 测试用例创建/修改/删除
- 环境配置变更
- 成员权限变更

**查看日志：**
1. 点击左侧菜单「审计日志」
2. 选择时间范围
3. 选择操作类型
4. 查看详细记录

---

## 20. 系统设置

### 20.1 个人设置

**基本设置：**
- 修改用户名
- 修改邮箱
- 上传头像
- 修改密码

**通知偏好：**
- 邮件通知：开/关
- 站内通知：开/关
- 通知频率：即时/每日摘要/关闭

### 20.2 界面设置

**主题配置：**
- 浅色模式
- 深色模式
- 跟随系统

**语言设置：**
- 简体中文
- English

### 20.3 API Token 管理

**创建 Token：**
1. 进入「个人设置」→「API Token」
2. 点击「创建 Token」
3. 填写信息：
   - Token 名称：`CI/CD 使用`
   - 过期时间：30 天
   - 权限：执行、读取
4. 点击「创建」
5. 复制生成的 Token（仅显示一次）

**使用 Token：**
```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
     https://test.huangxuan.chat/api/v1/projects
```

### 20.4 品牌定制

**定制项：**
- Logo 上传
- 主题色配置
- 登录页背景图
- 登录页欢迎语
- 页脚版权信息

---

---

## 21. 数据工厂

### 21.1 数据工厂概述

数据工厂是 FullScopeTest 的 AI 驱动测试数据生成工具，可以根据 Schema 配置或自然语言描述自动生成大量高质量的测试数据。

**访问路径：** 点击左侧菜单「数据工厂」

### 21.2 创建数据 Schema

**操作步骤：**
1. 进入「数据工厂」页面
2. 点击「新建 Schema」按钮
3. 填写 Schema 配置：
   - Schema 名称：`用户数据模板`
   - 描述：`用于注册测试的用户数据`

**Schema 字段配置：**
| 字段名 | 数据类型 | 生成规则 | 示例值 |
|--------|---------|---------|--------|
| username | string | 用户名格式 | user_001 |
| email | string | 邮箱格式 | user@example.com |
| password | string | 强密码 | P@ssw0rd123 |
| age | integer | 范围 18-80 | 25 |
| phone | string | 手机号格式 | 13812345678 |
| avatar | string | URL格式 | https://... |
| status | enum | [active,inactive,pending] | active |
| created_at | datetime | 时间范围 | 2024-01-01 |
| address | object | 嵌套对象 | {city, street} |

**数据类型详解：**

| 数据类型 | 说明 | 配置参数 |
|---------|------|---------|
| string | 字符串 | 格式、长度范围、正则 |
| integer | 整数 | 最小值、最大值 |
| float | 浮点数 | 最小值、最大值、小数位 |
| boolean | 布尔值 | - |
| enum | 枚举 | 可选值列表 |
| date | 日期 | 格式、范围 |
| datetime | 日期时间 | 格式、范围 |
| email | 邮箱 | 域名 |
| phone | 手机号 | 国家代码 |
| uuid | UUID | - |
| url | URL | - |
| ip | IP地址 | IPv4/IPv6 |
| object | 对象 | 嵌套字段 |
| array | 数组 | 元素类型、数量范围 |

### 21.3 使用 AI 生成数据

**AI 生成模式：**
1. 在 Schema 编辑器中点击「AI 辅助」
2. 输入自然语言描述：
   ```
   生成一个用户数据集，包含：
   - 用户名使用英文名
   - 邮箱使用 Gmail
   - 年龄在 20-40 岁之间
   - 必须包含企业用户和管理员角色
   ```
3. 点击「生成 Schema」
4. AI 自动生成字段配置
5. 点击「确认」保存

**生成规则示例：**

```javascript
// 自定义生成规则
{
  "field": "username",
  "type": "string",
  "rule": {
    "pattern": "user_{{seq(1000,9999)}}",
    // 序列号：1000-9999
  }
}

// 条件生成
{
  "field": "role",
  "type": "enum",
  "rule": {
    "values": ["admin", "user", "guest"],
    "weights": [0.1, 0.7, 0.2]
    // 权重：admin 10%, user 70%, guest 20%
  }
}

// 关联生成
{
  "field": "full_name",
  "type": "string",
  "rule": {
    "expression": "{{firstName}} {{lastName}}"
  }
}
```

### 21.4 生成测试数据

**基础生成：**
1. 选择已创建好的 Schema
2. 设置生成数量：`1000` 条
3. 点击「生成数据」按钮
4. 等待生成完成
5. 预览生成的数据

**高级配置：**
```
生成配置:
  数据量: 1000
  并发数: 4
  输出格式: JSON
  唯一约束: email, username
  排除重复: 是
```

### 21.5 导出数据

**支持格式：**
| 格式 | 说明 | 适用场景 |
|------|------|---------|
| JSON | JSON 数组 | API 测试数据源 |
| CSV | 逗号分隔 | Excel 分析、数据库导入 |
| SQL | INSERT 语句 | 数据库初始化 |
| XML | XML 格式 | 遗留系统集成 |
| Excel | .xlsx 文件 | 数据分析 |

**导出配置示例：**
```
CSV 导出:
  分隔符: 逗号
  编码: UTF-8
  包含表头: 是
  引号处理: 自动
```

### 21.6 数据预览与验证

**预览功能：**
- 分页查看生成的数据
- 筛选特定字段
- 搜索数据内容
- 统计字段分布

**数据验证：**
- 唯一性检查
- 格式校验
- 范围检查
- 自定义规则验证

### 21.7 数据模板管理

**模板库：**
- 内置常用模板（用户、订单、商品、地址等）
- 自定义模板保存
- 模板分类管理
- 模板分享

**导入导出模板：**
1. 点击「导出模板」下载 JSON 文件
2. 在其他项目中点击「导入模板」
3. 选择下载的 JSON 文件
4. 模板自动导入

---

## 22. Flaky 测试检测

### 22.1 Flaky 测试概述

Flaky 测试是指结果不稳定的测试用例，有时通过、有时失败。FullScopeTest 提供自动检测和统计分析功能。

**访问路径：** 点击左侧菜单「Flaky 测试」

### 22.2 Flaky 检测机制

**检测规则：**
- 同一用例连续 3 次执行结果不一致
- 过去 10 次执行中有 3 次以上失败
- 执行时间波动超过 200%

**统计指标：**
| 指标 | 说明 | 计算方式 |
|------|------|---------|
| 稳定性评分 | 用例稳定性 0-100 | 通过次数/总执行次数 |
| Flaky 率 | Flaky 用例占比 | Flaky数/总用例数 |
| 失败模式 | 常见失败原因 | 聚类分析 |

### 22.3 Flaky 仪表盘

**仪表盘内容：**
- Flaky 用例总数和占比
- 稳定性趋势图
- Top 10 最不稳定的用例
- 失败模式分布饼图
- 最近 Flaky 事件时间线

**查看详情：**
1. 点击任意 Flaky 用例
2. 查看执行历史时间线
3. 分析失败原因分布
4. 查看最近 20 次执行详情

### 22.4 Flaky 用例管理

**标记 Flaky：**
1. 用例详情页点击「标记为 Flaky」
2. 选择 Flaky 类型：
   - 网络相关
   - 依赖服务不稳定
   - 并发竞态
   - 环境问题
   - 定时触发
3. 添加备注说明
4. 点击「确认」

**排除 Flaky 用例：**
- 在测试计划中排除 Flaky 用例
- 不计入通过率统计
- 单独统计 Flaky 通过率

### 22.5 Flaky 分析报告

**报告内容：**
- Flaky 用例清单
- 失败原因分类统计
- 稳定性趋势分析
- 改进建议

**导出报告：**
1. 点击「导出报告」
2. 选择格式（PDF/HTML）
3. 下载报告文件

---

## 23. API 文档生成

### 23.1 文档生成概述

FullScopeTest 可以根据已有的 API 测试用例自动生成 OpenAPI 文档，支持导出为 YAML 或 JSON 格式。

**访问路径：** 点击左侧菜单「API 文档」

### 23.2 生成文档

**操作步骤：**
1. 进入「API 文档」页面
2. 点击「生成文档」按钮
3. 选择要包含的集合或用例
4. 点击「开始生成」

**生成配置：**
```
文档配置:
  标题: 用户管理 API 文档
  版本: 1.0.0
  描述: 用户管理相关接口
  联系人: api@example.com
  许可证: MIT
```

### 23.3 文档预览

**预览内容：**
- API 端点列表
- 请求/响应示例
- Schema 定义
- 认证说明
- 错误码说明

**交互预览：**
- 查看所有接口
- 查看接口详情
- 复制 cURL 命令
- 导出文档

### 23.4 导出文档

**支持格式：**
| 格式 | 说明 |
|------|------|
| OpenAPI YAML | 标准 YAML 格式 |
| OpenAPI JSON | 标准 JSON 格式 |
| Swagger JSON | Swagger 2.0 格式 |
| Postman Collection | Postman 导入格式 |

**导出步骤：**
1. 点击「导出」按钮
2. 选择导出格式
3. 选择导出范围（全部/选中）
4. 点击「下载」

### 23.5 文档版本管理

**版本历史：**
- 自动保存文档版本
- 对比不同版本差异
- 回滚到历史版本

**版本对比：**
1. 选择两个版本
2. 点击「对比」
3. 查看差异高亮

---

## 24. 健康监控

### 24.1 健康监控概述

健康监控模块提供系统级和 API 级的健康状态监控，帮助及时发现和处理问题。

**访问路径：** 点击左侧菜单「健康监控」

### 24.2 系统健康状态

**监控指标：**
| 指标 | 说明 | 正常范围 |
|------|------|---------|
| API 响应时间 | 平均响应耗时 | < 500ms |
| API 可用率 | 服务可用时间占比 | > 99.9% |
| 错误率 | 4xx/5xx 占比 | < 1% |
| QPS | 每秒请求数 | - |

**健康状态标识：**
- 🟢 健康：所有指标正常
- 🟡 警告：部分指标接近阈值
- 🔴 异常：关键指标异常

### 24.3 API 端点监控

**配置监控：**
1. 点击「添加监控」
2. 选择要监控的 API
3. 设置检查频率：1分钟/5分钟/15分钟
4. 设置告警阈值

**监控详情：**
- 响应时间趋势图
- 可用率趋势图
- 错误分布
- 最近告警记录

### 24.4 告警配置

**创建告警规则：**
```
规则配置:
  名称: API 响应超时告警
  监控指标: 响应时间
  条件: > (大于)
  阈值: 2000ms
  持续时间: 5分钟
  告警级别: 严重
```

**告警通知：**
- 勾选「启用通知」
- 选择通知渠道：邮件/钉钉/飞书
- 设置通知接收人

### 24.5 健康报告

**报告内容：**
- 健康评分（0-100）
- 各服务健康状态
- 异常事件汇总
- 改进建议

**定时报告：**
1. 点击「定时报告」
2. 设置发送周期：每日/每周
3. 选择发送时间
4. 设置收件人

---

## 25. Webhook 调试器

### 25.1 调试器概述

Webhook 调试器用于测试和调试 Webhook 配置，查看请求/响应详情。

**访问路径：** 点击左侧菜单「Webhook 调试器」

### 25.2 发送测试请求

**发送测试：**
1. 选择 Webhook 配置
2. 填写测试请求：
   - 请求方法：GET/POST
   - 请求 URL
   - 请求头
   - 请求体
3. 点击「发送」按钮
4. 查看响应详情

**响应查看：**
- 响应状态码
- 响应头
- 响应体
- 响应时间

### 25.3 请求日志

**日志记录：**
- 每次发送记录
- 请求详情
- 响应详情
- 错误信息

**日志筛选：**
- 按 Webhook 筛选
- 按状态筛选
- 按时间筛选
- 关键词搜索

### 25.4 常用测试用例

**内置测试用例：**
- Ping 测试
- 事件测试
- 签名验证测试

**自定义测试用例：**
1. 点击「保存为测试用例」
2. 填写用例名称
3. 配置请求内容
4. 期望响应
5. 点击「保存」

---

## 26. AI 使用统计

### 26.1 统计仪表盘

**访问路径：** 点击左侧菜单「AI 洞察」

**仪表盘内容：**
- AI 调用总次数
- Token 消耗总量
- 成功率趋势图
- 各功能使用分布
- 成本分析

### 26.2 调用统计

**统计维度：**
| 维度 | 说明 |
|------|------|
| 按日统计 | 每日调用量趋势 |
| 按功能统计 | Copilot/生成/分析占比 |
| 按用户统计 | 用户调用排名 |
| 按模型统计 | 不同模型使用量 |

**图表类型：**
- 折线图：趋势分析
- 饼图：占比分布
- 柱状图：对比分析
- 热力图：使用时段分布

### 26.3 Token 消耗分析

**消耗统计：**
- 输入 Token 消耗
- 输出 Token 消耗
- 总 Token 消耗
- 成本估算

**成本分析：**
- 各功能成本占比
- 成本趋势
- 优化建议

### 26.4 Prompt 版本管理

**版本对比：**
1. 选择两个 Prompt 版本
2. 点击「对比」
3. 查看版本差异
4. 评估效果变化

**版本回滚：**
1. 选择要回滚的版本
2. 点击「回滚到此版本」
3. 确认回滚操作

---

## 27. 报告定时发送

### 27.1 创建定时任务

**操作步骤：**
1. 点击左侧菜单「定时报告」
2. 点击「新建定时任务」
3. 填写配置：
   - 任务名称：`每日回归测试报告`
   - 报告类型：选择测试计划或项目
   - 发送周期：每天/每周/每月
   - 发送时间：09:00
   - 收件人：team@example.com

### 27.2 报告模板

**模板配置：**
1. 点击「报告模板」
2. 选择要包含的模块：
   - 执行概览
   - 通过率统计
   - 失败用例详情
   - 趋势分析
   - 截图附件
3. 设置主题色和 Logo

### 27.3 发送历史

**历史记录：**
- 发送时间
- 发送状态
- 收件人
- 查看报告链接

---

## 28. 用例模板库

### 28.1 模板库概述

用例模板库提供预置的测试用例模板，帮助快速创建标准化的测试用例。

**访问路径：** 点击左侧菜单「用例模板」

### 28.2 内置模板

**API 测试模板：**
| 模板名称 | 适用场景 | 包含内容 |
|---------|---------|---------|
| 标准 CRUD | 增删改查接口 | 创建/读取/更新/删除/列表 |
| 认证测试 | 登录注册接口 | 登录/登出/注册/修改密码 |
| 分页列表 | 列表类接口 | 分页/排序/筛选 |
| 表单验证 | 数据提交接口 | 必填/格式/边界/重复 |
| 错误处理 | 异常情况 | 401/403/404/500 |

**Web 测试模板：**
| 模板名称 | 适用场景 | 包含步骤 |
|---------|---------|---------|
| 登录流程 | 用户登录 | 打开页面/输入/提交/验证 |
| 表单提交 | 表单操作 | 填写/验证/提交/确认 |
| 列表操作 | 列表页面 | 搜索/筛选/排序/分页 |
| 弹窗操作 | 弹窗交互 | 打开/操作/关闭 |

### 28.3 创建自定义模板

**操作步骤：**
1. 点击「新建模板」
2. 选择模板类型：API/Web/APP
3. 填写基本信息：
   - 模板名称：`订单创建流程`
   - 描述：订单创建完整流程
4. 配置模板内容
5. 点击「保存」

### 28.4 使用模板

**从模板创建用例：**
1. 新建用例页面点击「从模板创建」
2. 选择模板
3. 修改参数
4. 点击「创建」

---

## 29. 团队效能指标

### 29.1 指标仪表盘

**访问路径：** 点击左侧菜单「团队效能」

**仪表盘内容：**
- 测试覆盖率趋势
- 用例执行统计
- 缺陷发现率
- 团队贡献排名

### 29.2 个人贡献统计

**统计指标：**
| 指标 | 说明 |
|------|------|
| 用例创建数 | 本月创建用例数 |
| 用例执行数 | 本月执行次数 |
| 缺陷发现数 | 发现的缺陷数 |
| 代码提交数 | 相关代码提交 |

### 29.3 趋势分析

**趋势图表：**
- 用例增长趋势
- 执行通过率趋势
- 缺陷修复趋势
- 覆盖率变化

---

## 30. LDAP/OIDC SSO 配置

### 30.1 LDAP 配置

**配置步骤：**
1. 进入「系统设置」→「SSO 配置」
2. 选择认证类型：LDAP
3. 填写配置：
   ```
   LDAP 配置:
     服务器地址: ldap://ldap.example.com
     端口: 389
     Base DN: dc=example,dc=com
     管理员 DN: cn=admin,dc=example,dc=com
     管理员密码: ********
     用户过滤: (uid={username})
     用户属性映射:
       用户名: uid
       邮箱: mail
       显示名: cn
   ```
4. 点击「测试连接」
5. 连接成功后点击「保存」

### 30.2 OIDC 配置

**配置步骤：**
1. 进入「系统设置」→「SSO 配置」
2. 选择认证类型：OIDC
3. 填写配置：
   ```
   OIDC 配置:
     Issuer URL: https://auth.example.com
     Client ID: your-client-id
     Client Secret: your-client-secret
     范围: openid profile email
     用户信息端点: /userinfo
     令牌端点: /token
     授权端点: /authorize
   ```
4. 配置属性映射：
   ```
   属性映射:
     用户名: preferred_username
     邮箱: email
     显示名: name
   ```
5. 点击「保存」

### 30.3 SSO 登录测试

**测试流程：**
1. 配置完成后点击「测试登录」
2. 跳转到 SSO 登录页面
3. 使用 SSO 账号登录
4. 验证能否成功登录

---

## 31. 品牌定制

### 31.1 定制项列表

**访问路径：** 进入「系统设置」→「品牌定制」

**可定制内容：**
| 定制项 | 说明 | 建议尺寸 |
|--------|------|---------|
| Logo | 网站 Logo | 200x60px |
| Favicon | 浏览器图标 | 32x32px |
| 登录页背景 | 登录页背景图 | 1920x1080px |
| 主题色 | 主色调 | - |
| 欢迎语 | 登录页欢迎文字 | - |
| 页脚版权 | 底部版权信息 | - |

### 31.2 主题配置

**配色方案：**
```
主题配置:
  主色调: #1890ff
  辅助色: #52c41a
  警告色: #faad14
  错误色: #f5222d
  文字色: #262626
  背景色: #f5f5f5
```

**深色模式：**
- 开启深色模式支持
- 配置深色主题配色

---

## 32. 计费管理

### 32.1 订阅计划

**访问路径：** 点击左侧菜单「计费管理」

**查看订阅：**
- 当前计划：专业版/企业版
- 到期时间
- 可用配额

### 32.2 配额使用

**配额明细：**
| 配额项 | 已用/总量 | 使用率 |
|--------|----------|--------|
| 项目数 | 5/10 | 50% |
| API 调用 | 10,000/100,000 | 10% |
| 存储空间 | 2GB/10GB | 20% |
| 团队成员 | 8/20 | 40% |

### 32.3 升级/续费

**升级计划：**
1. 点击「升级」
2. 选择目标计划
3. 确认价格
4. 完成支付

**续费：**
1. 点击「续费」
2. 选择续费时长
3. 完成支付

---

## 附录

### 附录 A：快捷键

| 快捷键 | 功能 |
|--------|------|
| Ctrl + S | 保存当前内容 |
| Ctrl + Enter | 发送请求 |
| Ctrl + F | 搜索 |
| Ctrl + Z | 撤销 |
| Ctrl + Shift + Z | 重做 |
| Ctrl + / | 打开快捷键帮助 |
| Ctrl + Space | 触发代码补全 |
| Ctrl + Shift + L | 格式化代码 |
| Alt + Up/Down | 移动代码行 |
| Shift + Alt + Up/Down | 复制代码行 |
| Ctrl + D | 选中下一个相同词 |
| Ctrl + Shift + E | 打开文件资源管理器 |
| Ctrl + B | 显示/隐藏侧边栏 |

### 附录 B：环境变量参考

**系统内置变量：**

| 变量名 | 说明 | 示例值 |
|--------|------|--------|
| {{timestamp}} | 当前时间戳（毫秒） | 1704067200000 |
| {{unix_timestamp}} | Unix 时间戳（秒） | 1704067200 |
| {{date}} | 当前日期 | 2024-01-01 |
| {{datetime}} | 当前日期时间 | 2024-01-01 12:00:00 |
| {{uuid}} | 随机 UUID | abc123-def456 |
| {{randomInt}} | 随机整数 | 12345 |
| {{randomInt:1-100}} | 指定范围随机数 | 42 |
| {{randomString}} | 随机字符串 | a1b2c3d4 |
| {{randomEmail}} | 随机邮箱 | user123@example.com |
| {{randomPhone}} | 随机手机号 | 13812345678 |
| {{randomName}} | 随机姓名 | 张三 |
| {{randomUrl}} | 随机 URL | https://example.com |
| {{randomIp}} | 随机 IP | 192.168.1.1 |

### 附录 C：常见问题排查

**Q1: 请求执行失败，显示网络错误**
```
排查步骤：
1. 检查网络连接是否正常
2. 确认目标服务器是否可达
3. 检查防火墙是否阻止请求
4. 尝试使用 curl 命令测试
5. 查看浏览器开发者工具网络面板
```

**Q2: 响应显示乱码**
```
排查步骤：
1. 检查响应头的 Content-Type
2. 确认请求的 Accept 头
3. 检查浏览器编码设置
4. 尝试手动指定编码（UTF-8/GBK）
```

**Q3: 断言失败，不知道原因**
```
排查步骤：
1. 查看断言详情和实际值
2. 使用 AI 分析功能获取原因
3. 检查数据类型的匹配
4. 确认环境变量是否正确
```

**Q4: 性能测试结果波动大**
```
排查步骤：
1. 增加预热时间
2. 增加执行样本量
3. 检查网络稳定性
4. 确认测试服务器负载
5. 使用 P95/P99 指标评估
```

**Q5: Web 测试元素定位失败**
```
排查步骤：
1. 检查选择器语法是否正确
2. 确认元素是否在 iframe 内
3. 检查元素是否动态加载
4. 使用 AI 优化选择器
5. 尝试等待元素出现
```

**Q6: CI/CD 集成失败**
```
排查步骤：
1. 确认 Webhook URL 是否正确
2. 检查 Token 是否有效
3. 验证触发条件配置
4. 查看触发器执行日志
5. 测试 Webhook 是否可达
```

### 附录 D：最佳实践

**API 测试最佳实践：**
1. 每个用例只测试一个功能点
2. 用例之间保持独立，不依赖执行顺序
3. 使用环境变量管理不同环境配置
4. 断言要具体，避免过于宽松
5. 合理使用前置脚本准备测试数据
6. 定期清理无用的测试数据

**Web 测试最佳实践：**
1. 使用稳定的元素选择器（ID > data-testid > class）
2. 添加合理的等待时间
3. 使用 Page Object 模式组织代码
4. 重要步骤添加截图
5. 失败的用例要保留截图用于分析
6. 定期更新选择器以适应 UI 变化

**性能测试最佳实践：**
1. 测试环境要与生产环境尽可能一致
2. 设置足够的预热时间
3. 执行时间要足够长以获得稳定数据
4. 监控服务器资源使用情况
5. 记录详细的测试配置和结果
6. 与历史结果进行对比分析

### 附录 E：联系方式

如有问题，请联系技术支持：
- 邮箱：support@example.com
- 文档：https://docs.example.com
- 技术支持群：[扫码加入]

---

*文档更新时间：2026-09-15*
*FullScopeTest 版本：v1.0.0*
