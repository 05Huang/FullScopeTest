# 新功能快速开始

> 5分钟快速上手新功能

---

## 🚀 快速体验

### 前提条件

确保已完成数据库迁移：

```bash
cd backend
python manage.py db upgrade
```

---

## 📝 步骤一：配置环境变量

### 1. 创建测试环境

进入"环境管理"页面，点击"新建环境"：

```json
{
  "name": "开发环境",
  "base_url": "http://localhost:5211",
  "variables": {
    "token": "test_token_abc123",
    "version": "v1"
  }
}
```

### 2. 保存环境

点击确定，环境创建成功。

---

## 📦 步骤二：创建集合

### 1. 新建集合

在"接口测试工作台"或使用 `CollectionManager` 组件：

- 点击"新建集合"
- 填写：
  - 名称: `用户接口测试`
  - 描述: `用户相关接口的测试用例`
- 点击确定

### 2. 查看集合

集合列表中会显示新创建的集合。

---

## 🧪 步骤三：创建测试用例

### 1. 创建第一个用例

```json
{
  "name": "获取当前用户信息",
  "method": "GET",
  "url": "http://localhost:5211/api/{version}/auth/me",
  "headers": {
    "Authorization": "Bearer {token}"
  },
  "collection_id": 1
}
```

**注意变量使用：**
- URL 中的 `{version}` 会被替换为 `v1`
- 请求头中的 `{token}` 会被替换为 `test_token_abc123`

### 2. 创建第二个用例

```json
{
  "name": "获取项目列表",
  "method": "GET",
  "url": "http://localhost:5211/api/{version}/projects",
  "headers": {
    "Authorization": "Bearer {token}"
  },
  "collection_id": 1
}
```

---

## ▶️ 步骤四：批量运行测试

### 1. 选择集合

在集合列表中找到"用户接口测试"。

### 2. 点击运行

1. 点击集合右侧的"运行"按钮
2. 在弹出的对话框中选择"开发环境"
3. 点击"开始运行"

### 3. 查看结果

运行完成后会显示：
- 总用例数
- 通过数
- 失败数
- 报告 ID

---

## 📊 步骤五：查看报告

### 1. 进入报告页面

点击"测试报告"菜单。

### 2. 查看最新报告

- 列表中会显示刚刚生成的报告
- 点击"查看"按钮
- 查看详细的测试结果

### 3. 下载报告

在报告详情页面：
- 点击"下载 HTML"按钮
- 保存报告文件

---

## ✨ 功能验证

完成以上步骤后，你应该能够：

- [x] 在环境中配置变量
- [x] 创建测试集合
- [x] 在用例中使用变量（`{变量名}` 格式）
- [x] 批量运行集合中的所有用例
- [x] 自动生成测试报告
- [x] 查看和下载报告

---

## 🎯 完整示例

### 使用 curl 快速测试

```bash
# 1. 登录获取 token
TOKEN=$(curl -X POST http://localhost:5211/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"password123"}' \
  | jq -r '.data.access_token')

# 2. 创建环境
curl -X POST http://localhost:5211/api/v1/environments \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "name": "快速测试环境",
    "base_url": "http://localhost:5211",
    "variables": {
      "token": "'$TOKEN'",
      "version": "v1"
    }
  }'

# 3. 创建集合
COLLECTION_ID=$(curl -X POST http://localhost:5211/api/v1/api-test/collections \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"name":"快速测试集合","description":"快速开始示例"}' \
  | jq -r '.data.id')

# 4. 创建测试用例
curl -X POST http://localhost:5211/api/v1/api-test/cases \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "name": "获取用户信息",
    "method": "GET",
    "url": "http://localhost:5211/api/{version}/auth/me",
    "headers": {"Authorization": "Bearer {token}"},
    "collection_id": '$COLLECTION_ID'
  }'

# 5. 运行集合
curl -X POST http://localhost:5211/api/v1/api-test/collections/$COLLECTION_ID/run \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"env_id": 1}'

# 6. 查看报告列表
curl -X GET http://localhost:5211/api/v1/test-reports \
  -H "Authorization: Bearer $TOKEN"
```

---

## 💡 使用技巧

### 1. 变量命名建议

- 使用有意义的名称：`userToken` 而不是 `t1`
- 使用驼峰命名：`apiKey`、`baseUrl`
- 避免特殊字符

### 2. 集合组织建议

- 按模块划分：用户模块、订单模块等
- 按功能划分：登录注册、CRUD 操作等
- 按优先级划分：冒烟测试、回归测试等

### 3. 报告查看技巧

- 筛选特定类型的报告
- 定期清理旧报告
- 下载重要报告存档

---

## 🐛 常见问题

### Q: 变量没有被替换？

**A:** 检查：
1. 格式是否正确（`{变量名}` 不是 `{{变量名}}`）
2. 环境中是否配置了该变量
3. 运行时是否选择了环境

### Q: 批量测试失败？

**A:** 可以：
1. 单独运行失败的用例进行调试
2. 查看报告中的错误信息
3. 检查网络连接和服务状态

### Q: 找不到报告？

**A:** 确认：
1. 测试是否执行成功
2. 在正确的项目下查看
3. 使用筛选功能

---

## 📚 进阶学习

完成快速开始后，建议阅读：

1. [完整功能使用指南](./NEW_FEATURES_GUIDE.md)
2. [API 接口文档](./API.md)
3. [更新部署指南](./UPDATE_GUIDE.md)

---

**开始使用新功能吧！** 🎉

如有问题，请查看详细文档或联系技术支持。
