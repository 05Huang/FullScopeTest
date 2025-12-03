# 早护通后端API测试指南

## 环境准备

### 1. 了解系统架构
本项目包含两个独立的系统：

**系统 1：接口测试平台（Web UI）** ⭐ 测试工具
- 地址：`http://localhost:5000`
- 用途：提供 Web 界面来测试早护通 API
- 启动：`cd web && python app.py`

**系统 2：早护通后端 API** ⭐ 测试对象
- 地址：`https://backend.pinf.top`（或你的本地后端）
- 用途：被测试的目标服务
- 启动：取决于你的后端部署位置

### 2. 启动接口测试平台
如果使用 Web UI 测试：
```bash
cd web
python app.py
```
然后访问 `http://localhost:5000` 即可通过图形界面测试 API

#### 2.1 Web 平台中配置环境
1. 打开测试平台首页
2. 点击导航栏的"环境"按钮
3. 创建新环境，配置以下信息：
   - **名称**：`早护通-生产` 或任意名称
   - **Base URL**：`https://backend.pinf.top`
   - **Headers**：`{"Content-Type": "application/json"}` (可选)
   - **Variables**：`{}` (如需要可添加自定义变量)
4. 保存环境

#### 2.2 Web 平台中创建请求
1. 创建新集合，名称如 `早护通API测试`
2. 在集合中创建新请求
3. **URL 格式说明**：
   - ✅ **完整 URL 方式**（推荐）：`https://backend.pinf.top/api/test-login`
   - ✅ **环境变量方式**：`{{base_url}}/api/test-login`（需要先选择环境）
4. 填写其他信息（Headers、Body 等）
5. 点击"发送"按钮

**关键点**：使用 `{{base_url}}/api/test-login` 格式时，必须先在页面顶部的环境选择器中选择已配置的环境

### 3. Postman 环境配置
如果使用 Postman 直接测试，创建新的环境变量：
- `base_url`: `https://backend.pinf.top`（你的目标 API 地址）
  - 如果是本地后端，改为：`http://localhost:8000`（根据实际端口）
- `token`: 空（将在登录后自动设置）

### 4. 常见配置情景

**情景 A：测试远程 API（backend.pinf.top）**
```
base_url = https://backend.pinf.top
测试工具位置 = 本地（localhost:5000 或 Postman）
```

**情景 B：测试本地后端**
```
base_url = http://localhost:8000  # 根据实际后端端口修改
测试工具位置 = 本地（localhost:5000 或 Postman）
```

## 测试流程

### 使用接口测试平台（Web UI）的完整流程

#### 步骤 1：选择或创建环境
1. 在 Web 平台顶部找到"环境"下拉菜单
2. 选择已配置的环境（如 `早护通-生产`）
3. **关键**：必须选中环境后，`{{base_url}}` 变量才会被替换成实际的 URL

#### 步骤 2：创建测试集合
1. 在左侧集合列表点击"+ 新建集合"
2. 输入集合名称：`早护通API测试`
3. 选择所属环境：选择之前配置的环境

#### 步骤 3：在集合中创建请求

**示例：测试登录接口**
- 在集合卡片点击"编辑"或"+"图标
- 填写请求信息：
  - **名称**：`登录接口`
  - **方法**：`POST`
  - **URL**：`{{base_url}}/api/test-login`
  - **Headers**：
    ```
    Content-Type: application/json
    ```
  - **Body**：
    ```json
    {
      "openid": "test_user_123"
    }
    ```请求失败: HTTPSConnectionPool(host='backend.pinf.top', port=443): Max retries exceeded with url: /api/test-login (Caused by SSLError(SSLError(1, '[SSL: TLSV1_ALERT_INTERNAL_ERROR] tlsv1 alert internal error (_ssl.c:1028)')))
- 点击"保存"

#### 步骤 4：发送请求
1. 在编辑器中点击"发送"按钮
2. 平台会自动：
   - 替换 `{{base_url}}` 为当前环境的 Base URL（`https://backend.pinf.top`）
   - 生成完整 URL：`https://backend.pinf.top/api/test-login`
   - 发送请求到目标 API
3. 在右侧查看响应结果

#### 步骤 5：保存 token（如果需要）
1. 登录接口返回 token 后
2. 在环境配置中添加 `token` 变量
3. 之后在需要认证的请求中使用 `Authorization: Bearer {{token}}`

---

### 详细接口测试流程（按业务顺序）

#### 1.1 测试登录接口w1
- **方法**: POST
- **URL**: `{{base_url}}/api/test-login`
- **Headers**: 
  ```
  Content-Type: application/json
  ```
- **Body** (raw JSON):
  ```json
  {
    "openid": "test_user_123"
  }
  ```
- **预期结果**: 返回token和用户信息
- **后续操作**: 将返回的token保存到环境变量中

#### 1.2 健康检查
- **方法**: GET
- **URL**: `{{base_url}}/api/health`
- **预期结果**: 返回服务状态

### 第二步：儿童管理测试

#### 2.1 获取儿童信息
- **方法**: GET
- **URL**: `{{base_url}}/api/getChildInfo`
- **Headers**: 
  ```
  Authorization: Bearer {{token}}
  ```
- **预期结果**: 返回当前用户的儿童列表

#### 2.2 添加儿童信息
- **方法**: POST
- **URL**: `{{base_url}}/api/addChild`
- **Headers**: 
  ```
  Content-Type: application/json
  Authorization: Bearer {{token}}
  ```
- **Body** (raw JSON):
  ```json
  {
    "name": "小明",
    "gender": "男",
    "birthDate": "2020-05-15",
    "avatar_url": "https://example.com/avatar.jpg",
    "gestationalAge":"2"
  }
  ```

#### 2.3 添加生长记录
- **方法**: POST
- **URL**: `{{base_url}}/api/addGrowthRecord`
- **Headers**: 
  ```
  Content-Type: application/json
  Authorization: Bearer {{token}}
  ```
- **Body** (raw JSON):
  ```json
  {
    "child_id": 1,
    "height": 85.5,
    "weight": 12.3,
    "head_circumference": 46.2,
    "record_date": "2024-01-15",
    "notes": "健康成长"
  }
  ```

### 第三步：内容管理测试

#### 3.1 获取视频列表
- **方法**: GET
- **URL**: `{{base_url}}/api/getVideos`
- **Headers**: 
  ```
  Authorization: Bearer {{token}}
  ```
- **查询参数** (可选):
  - `page`: 页码 (默认1)
  - `per_page`: 每页数量 (默认10)
  - `tag`: 标签筛选

#### 3.2 获取视频详情
- **方法**: GET
- **URL**: `{{base_url}}/api/getVideoDetail/1`
- **Headers**: 
  ```
  Authorization: Bearer {{token}}
  ```

#### 3.3 获取文章列表
- **方法**: GET
- **URL**: `{{base_url}}/api/getArticles`
- **Headers**: 
  ```
  Authorization: Bearer {{token}}
  ```
- **查询参数** (可选):
  - `page`: 页码
  - `per_page`: 每页数量
  - `tag`: 标签筛选

#### 3.4 获取文章详情
- **方法**: GET
- **URL**: `{{base_url}}/api/getArticleDetail/1`
- **Headers**: 
  ```
  Authorization: Bearer {{token}}
  ```

#### 3.5 搜索内容
- **方法**: GET
- **URL**: `{{base_url}}/api/searchContent`
- **Headers**: 
  ```
  Authorization: Bearer {{token}}
  ```
- **查询参数**:
  - `keyword`: 搜索关键词 (必需)
  - `type`: 内容类型 (all/video/article，可选，默认all)
  - `page`: 页码 (可选，默认1)
  - `per_page`: 每页数量 (可选，默认10)
- **示例URL**: `{{base_url}}/api/searchContent?keyword=护理&type=video&page=1&per_page=5`

### 第四步：预约管理测试

#### 4.1 获取预约列表
- **方法**: GET
- **URL**: `{{base_url}}/api/getAppointments`
- **Headers**: 
  ```
  Authorization: Bearer {{token}}
  ```
- **查询参数** (可选):
  - `page`: 页码 (整数，从1开始，默认1)
  - `per_page`: 每页数量 (整数，默认10，最大100)
  - `status`: 状态筛选 (all/pending/completed，默认all)
  - `showLoading`: 是否显示加载提示 (true/false，默认false)

#### 4.2 添加预约
- **方法**: POST
- **URL**: `{{base_url}}/api/addAppointment`
- **Headers**: 
  ```
  Content-Type: application/json
  Authorization: Bearer {{token}}
  ```
- **Body** (raw JSON):
  ```json
  {
    "childId": 1,
    "hospitalName": "儿童医院",
    "department": "儿科",
    "appointmentDate": "2024-02-15",
    "reminderDays": 1,
    "notes": "常规体检"
  }
  ```
- **注意**: 
  - `childId`: 必需字段，儿童ID
  - `hospitalName`: 必需字段，医院名称
  - `department`: 必需字段，科室
  - `appointmentDate`: 必需字段，预约日期，格式为YYYY-MM-DD，必须是未来日期
  - `reminderDays`: 可选字段，提醒天数，默认1天
  - `notes`: 可选字段，备注信息

#### 4.3 更新预约
- **方法**: PUT
- **URL**: `{{base_url}}/api/updateAppointment/5b264df5-0c09-4993-b224-bc64fa3ffe6a`
- **Headers**: 
  ```
  Content-Type: application/json
  Authorization: Bearer {{token}}
  ```
- **Body** (raw JSON):
  ```json
  {
    "hospitalName": "新儿童医院",
    "department": "内科",
    "appointmentDate": "2026-02-16",
    "reminderDays": 2,
    "notes": "更新后的预约"
  }
  ```
- **注意**: 
  - 所有字段都是可选的，只更新提供的字段
  - `appointmentDate`: 日期格式为YYYY-MM-DD，必须是未来日期
  - 预约ID通过URL路径传递，使用实际存在的UUID格式ID

#### 4.4 删除预约
- **方法**: DELETE
- **URL**: `{{base_url}}/api/deleteAppointment/633c199b-c34c-4153-b59a-4833822e46e2`
- **Headers**: 
  ```
  Authorization: Bearer {{token}}
  ```
- **注意**: 使用实际存在的预约UUID格式ID

#### 4.5 完成预约
- **方法**: PUT
- **URL**: `{{base_url}}/api/completeAppointment/5b264df5-0c09-4993-b224-bc64fa3ffe6a`
- **Headers**: 
  ```
  Authorization: Bearer {{token}}
  ```
- **注意**: 
  - 使用PUT方法，不是POST
  - 预约ID通过URL路径传递，使用实际存在的UUID格式ID
  - 无需请求体，只需要正确的认证头

#### 4.6 获取即将到来的预约
- **方法**: GET
- **URL**: `{{base_url}}/api/getUpcomingAppointments`
- **Headers**: 
  ```
  Authorization: Bearer {{token}}
  ```
- **查询参数** (可选):
  
  - `days`: 未来天数 (默认7天)

### 第五步：聊天管理测试

#### 5.1 发送消息
- **方法**: POST
- **URL**: `{{base_url}}/api/sendMessage`
- **Headers**: 
  ```
  Content-Type: application/json
  Authorization: Bearer {{token}}
  ```
- **Body** (raw JSON):
  ```json
  {
    "content": "你好，我想咨询一下婴儿护理的问题",
    "message_type": "text"
  }
  ```

#### 5.2 获取聊天历史
- **方法**: GET
- **URL**: `{{base_url}}/api/getChatHistory`
- **Headers**: 
  ```
  Authorization: Bearer {{token}}
  ```
- **查询参数** (可选):
  - `page`: 页码
  - `per_page`: 每页数量

#### 5.3 删除消息
- **方法**: DELETE
- **URL**: `{{base_url}}/api/deleteMessage/1`
- **Headers**: 
  ```
  Authorization: Bearer {{token}}
  ```

#### 5.4 清空聊天历史
- **方法**: DELETE
- **URL**: `{{base_url}}/api/clearChatHistory`
- **Headers**: 
  ```
  Authorization: Bearer {{token}}
  ```

#### 5.5 获取快捷回复
- **方法**: GET
- **URL**: `{{base_url}}/api/getQuickReplies`
- **Headers**: 
  ```
  Authorization: Bearer {{token}}
  ```

## 常见错误处理

### Web 平台特定问题

#### URL 中的 `{{base_url}}` 没有被替换
- **原因**：未选择环境或环境配置错误
- **现象**：请求返回 404，URL 显示为 `{{base_url}}/api/test-login` 而不是实际的 URL
- **解决**：
  1. 检查页面顶部是否已选择环境
  2. 确认环境的 Base URL 配置正确：`https://backend.pinf.top`
  3. 如果环境丢失，重新创建环境

#### 请求始终返回 404
- **原因**：
  1. 环境未正确选择
  2. URL 路径错误（检查接口路径）
  3. 后端服务离线
- **解决**：
  1. 在环境选择器中明确选择环境
  2. 查看请求的完整 URL（平台会显示替换后的 URL）
  3. 用 curl 直接测试：`curl https://backend.pinf.top/api/test-login`

### SSL/TLS 错误：`TLSV1_ALERT_INTERNAL_ERROR`
- **原因**: 远程服务器的 SSL 证书配置有问题或服务离线
- **现象**: 
  ```
  HTTPSConnectionPool(host='backend.pinf.top'): Max retries exceeded
  SSLError(1, '[SSL: TLSV1_ALERT_INTERNAL_ERROR] tlsv1 alert internal error')
  ```
- **解决方案**：
  1. 检查远程服务器是否在线：`ping backend.pinf.top`
  2. 尝试用浏览器访问：`https://backend.pinf.top`，查看证书是否有效
  3. 联系后端维护人员检查 SSL 证书配置
  4. **临时方案**（仅用于开发/测试）：如果远程服务器无法修复，使用本地后端或使用 HTTP（如果服务支持）

### 401 Unauthorized
- **原因**: Token无效或过期
- **解决**: 重新调用登录接口获取新token

### 404 Not Found
- **原因**: 接口路径不存在或 API 版本不匹配
- **现象**: 请求返回 404 响应
- **解决方案**：
  1. 检查 base_url 是否正确：`https://backend.pinf.top`
  2. 检查接口路径是否正确（可能不需要 `/api` 前缀）
  3. 验证后端服务是否在线：
     ```bash
     curl https://backend.pinf.top/api/health
     curl https://backend.pinf.top/health
     ```
  4. 联系后端维护人员确认登录接口的正确路径
  5. **如果远程 API 无法访问**，使用本地后端进行测试：
     ```
     base_url = http://localhost:8000  # 改用本地地址
     ```

### 400 Bad Request
- **原因**: 请求参数格式错误
- **解决**: 检查JSON格式和必需字段

### 500 Internal Server Error
- **原因**: 服务器内部错误
- **解决**: 检查服务器日志，确认数据库连接正常

## 测试数据说明

系统启动时会自动创建以下测试数据：
- 测试用户：openid为"test_user_123"
- 测试儿童：小明（男，2020-05-15出生）
- 测试视频：婴儿护理基础知识
- 测试文章：新生儿护理指南
- 预约ID示例：从获取预约列表接口返回的实际UUID，如：
  - 5b264df5-0c09-4993-b224-bc64fa3ffe6a
  - 633c199b-c34c-4153-b59a-4833822e46e2

## 注意事项

1. 所有需要认证的接口都必须在Headers中包含`Authorization: Bearer {{token}}`
2. POST/PUT请求需要设置`Content-Type: application/json`
3. 日期格式统一使用`YYYY-MM-DD`或`YYYY-MM-DD HH:MM:SS`
4. 分页参数：page从1开始，per_page默认为10
5. 测试前确保数据库文件存在且服务正常启动
6. 预约ID格式：预约ID是UUID格式（如：5b264df5-0c09-4993-b224-bc64fa3ffe6a），不是数字
7. 测试顺序：建议先调用获取预约列表接口，获取实际存在的预约ID，再进行更新、删除、完成等操作
8. 预约状态：预约状态包括 pending（待处理）和 completed（已完成）

## 完整接口列表

### 认证相关
- POST `/api/test-login` - 测试登录
- GET `/api/health` - 健康检查

### 儿童管理
- GET `/api/getChildInfo` - 获取儿童信息
- POST `/api/addChild` - 添加儿童
- POST `/api/addGrowthRecord` - 添加生长记录

### 内容管理
- GET `/api/getVideos` - 获取视频列表
- GET `/api/getVideoDetail/<id>` - 获取视频详情
- GET `/api/getArticles` - 获取文章列表
- GET `/api/getArticleDetail/<id>` - 获取文章详情
- GET `/api/searchContent` - 搜索内容

### 预约管理
- GET `/api/getAppointments` - 获取预约列表
- POST `/api/addAppointment` - 添加预约
- PUT `/api/updateAppointment/<id>` - 更新预约
- DELETE `/api/deleteAppointment/<id>` - 删除预约
- POST `/api/completeAppointment/<id>` - 完成预约
- GET `/api/getUpcomingAppointments` - 获取即将到来的预约

### 聊天管理
- POST `/api/sendMessage` - 发送消息
- GET `/api/getChatHistory` - 获取聊天历史
- DELETE `/api/deleteMessage/<id>` - 删除消息
- DELETE `/api/clearChatHistory` - 清空聊天历史
- GET `/api/getQuickReplies` - 获取快捷回复
