# 快速开始指南

## 🚀 5 分钟快速启动

### Windows (PowerShell) ⭐ 推荐
```powershell
cd web
.\run.bat
```

### Windows (命令提示符 CMD)
```cmd
cd web
run.bat
```

### Linux / Mac
```bash
cd web
chmod +x run.sh
./run.sh
```

然后访问：http://localhost:5000

---

## 📖 常见操作

### 1. 创建第一个测试集合
```
1. 点击左上角"新建集合"
2. 输入名称：用户管理模块
3. 输入描述：包含用户相关的所有接口
4. 点击保存
```

### 2. 添加测试请求
```
1. 在左侧集合列表中找到刚创建的集合
2. 点击集合卡片的"打开"按钮
3. 点击左侧"+ 添加请求"
4. 输入请求信息：
   - 名称：用户登录
   - 方法：POST
   - URL：/api/login
5. 添加 Headers（如果需要）
6. 输入 Request Body（JSON 格式）
7. 点击"发送"测试请求
8. 在 Response 标签页查看结果
9. 点击"保存"保存请求
```

### 3. 设置环境
```
1. 在顶部导航栏找到"环境"
2. 点击"新建环境"
3. 输入：
   - 环境名称：Dev
   - Base URL：https://api-dev.example.com
   - Headers（JSON）：{"Authorization": "Bearer xxxx"}
4. 点击保存
5. 在顶部右侧选择环境
```

### 4. 运行测试生成报告
```
1. 在集合卡片点击"运行测试"
2. 等待测试完成
3. 打开"报告"页面查看结果
4. 点击"查看报告"打开详细的 Allure 报告
```

### 5. 导入 Postman 集合
```
1. 在 Postman 中选择集合 → Export → JSON 格式
2. 在平台中找到导入功能（后续版本会添加）
3. 粘贴 JSON 数据
4. 自动创建集合和请求
```

---

## 🎮 快捷操作

| 操作 | 快捷键 | 说明 |
|------|--------|------|
| 发送请求 | Ctrl+Enter | 在请求编辑器中 |
| 保存请求 | Ctrl+S | 编辑完成后 |
| 切换标签页 | Ctrl+1~4 | Headers/Body/Params/Response |

---

## 🔍 API 速查

### 获取环境列表
```bash
curl http://localhost:5000/api/environments
```

### 创建新环境
```bash
curl -X POST http://localhost:5000/api/environments \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Dev",
    "base_url": "https://api-dev.example.com",
    "headers": {"Authorization": "Bearer token"}
  }'
```

### 发送请求
```bash
curl -X POST http://localhost:5000/api/send \
  -H "Content-Type: application/json" \
  -d '{
    "method": "GET",
    "url": "https://api.example.com/users",
    "headers": {"Content-Type": "application/json"}
  }'
```

### 获取测试报告
```bash
curl http://localhost:5000/api/reports
```

---

## 🐛 常见问题

### Q: 无法访问 localhost:5000
**A:** 检查：
- Flask 是否正常启动（看控制台输出）
- 5000 端口是否被占用
- 尝试访问 http://127.0.0.1:5000

### Q: 发送请求出错
**A:** 检查：
- URL 格式是否正确
- 网络连接是否正常
- 环境配置是否完整
- 查看浏览器控制台错误信息

### Q: 请求保存失败
**A:** 检查：
- 数据库是否可写
- test_cases.db 文件权限
- Flask 日志输出

### Q: 数据库被锁定
**A:** 解决：
```bash
# 删除数据库并重新创建
rm test_cases.db
python app.py
```

---

## 📊 数据库备份

### 备份数据库
```bash
# Windows
copy test_cases.db test_cases_backup.db

# Linux/Mac
cp test_cases.db test_cases_backup.db
```

### 恢复数据库
```bash
# Windows
copy test_cases_backup.db test_cases.db

# Linux/Mac
cp test_cases_backup.db test_cases.db
```

---

## 🔗 相关资源

### 官方文档
- [Flask 官方文档](https://flask.palletsprojects.com/)
- [Vue.js 3 文档](https://vuejs.org/)
- [SQLAlchemy 文档](https://www.sqlalchemy.org/)
- [Pytest 文档](https://docs.pytest.org/)

### 参考项目
- [Postman](https://www.postman.com/)
- [Insomnia](https://insomnia.rest/)
- [Thunder Client](https://www.thunderclient.com/)

### 学习资源
- HTTP/REST API 基础
- Vue.js 前端框架
- Flask Web 开发
- pytest 自动化测试

---

## 📝 配置示例

### config/config.yaml 示例
```yaml
default: dev

env:
  dev:
    base_url: "https://api-dev.example.com"
    headers:
      Content-Type: "application/json"
      Authorization: ""
    account:
      username: "test_user"
      password: "test_password"
    variables:
      timeout: 30
      retry_count: 3

  test:
    base_url: "https://api-test.example.com"
    headers:
      Content-Type: "application/json"
    account:
      username: "test_user_qa"
      password: "test_password_qa"

  prod:
    base_url: "https://api.example.com"
    headers:
      Content-Type: "application/json"
```

### Pytest 测试示例
```python
import pytest
from common.request_util import RequestUtil

@pytest.mark.parametrize("user", [
    {"username": "user1", "password": "pwd1"},
    {"username": "user2", "password": "pwd2"}
])
def test_login(config, user):
    """参数化测试登录"""
    r = RequestUtil(config["base_url"]).send(
        "POST",
        "/api/login",
        headers=config["headers"],
        json=user
    )
    assert r.status_code == 200
    assert r.json()["code"] == 200
```

---

## 🎯 下一步

1. **熟悉操作**
   - 创建集合和请求
   - 体验发送和响应
   - 查看生成的报告

2. **定制配置**
   - 添加自己的环境
   - 导入现有的 Postman 集合
   - 调整 UI 主题

3. **集成测试**
   - 编写 Pytest 测试
   - 运行测试生成报告
   - 分析测试结果

4. **部署上线**
   - 配置 Docker
   - 部署到服务器
   - 邀请团队成员

---

## 📞 反馈和建议

如有问题或建议，欢迎反馈！

- 📧 Email: support@example.com
- 💬 Issue: GitHub Issues
- 💭 Discussion: GitHub Discussions

---

祝你使用愉快！🎉
