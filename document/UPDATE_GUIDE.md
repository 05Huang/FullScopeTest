# 功能优化更新说明

> 更新日期：2025-12-28  
> 版本：v1.1

## 📋 更新内容概述

本次更新主要包含以下四个方面的功能优化：

1. **环境变量支持** - 在测试用例中使用 `{变量名}` 引用环境变量
2. **集合管理增强** - 完善集合创建和批量测试功能
3. **测试报告生成** - 自动生成详细的测试报告
4. **前后端完善** - 数据库、后端 API、前端界面全面更新

---

## 🚀 应用更新步骤

### 1. 数据库迁移

运行数据库迁移以创建新的报告相关表：

```bash
cd backend
python manage.py db upgrade
```

或者在 PowerShell 中：

```powershell
cd backend
python manage.py db upgrade
```

### 2. 后端依赖

确保已安装所有必需的 Python 包：

```bash
pip install -r requirements.txt
```

### 3. 前端依赖

前端不需要额外安装依赖，新增的组件已包含在现有依赖中。

### 4. 启动服务

按正常流程启动后端和前端服务：

**后端：**
```bash
cd backend
python run_dev.py
```

**前端：**
```bash
cd web
npm run dev
```

---

## 📁 文件更新清单

### 后端文件

#### 新增文件

| 文件路径 | 说明 |
|---------|------|
| `backend/app/models/test_report.py` | 测试报告数据模型 |
| `backend/app/utils/env_variables.py` | 环境变量处理工具 |
| `backend/migrations/versions/add_test_report_features.py` | 数据库迁移文件 |

#### 修改文件

| 文件路径 | 修改内容 |
|---------|---------|
| `backend/app/models/__init__.py` | 导入 TestReport 模型 |
| `backend/app/api/api_test.py` | 集合批量测试、环境变量替换、报告生成 |
| `backend/app/api/reports.py` | 添加测试报告相关 API |

### 前端文件

#### 新增文件

| 文件路径 | 说明 |
|---------|------|
| `web/src/services/testReportService.ts` | 测试报告服务 |
| `web/src/pages/TestReports.tsx` | 测试报告列表页面 |
| `web/src/pages/api-test/CollectionManager.tsx` | 集合管理组件 |
| `web/src/pages/api-test/EnvironmentVariableHint.tsx` | 环境变量提示组件 |

#### 修改文件

| 文件路径 | 修改内容 |
|---------|---------|
| `web/src/services/index.ts` | 导出 testReportService |
| `web/src/services/apiTestService.ts` | 更新 runCollection 方法 |

### 文档文件

| 文件路径 | 说明 |
|---------|------|
| `document/API.md` | 更新 API 接口文档 |
| `document/NEW_FEATURES_GUIDE.md` | 新功能使用指南（新增） |
| `document/UPDATE_GUIDE.md` | 本更新说明文件（新增） |

---

## 🎯 功能使用指南

### 1. 环境变量使用

**配置环境变量：**

进入"环境管理"页面，创建或编辑环境：

```json
{
  "name": "开发环境",
  "variables": {
    "bearer": "your_token",
    "userId": "123"
  }
}
```

**在用例中使用：**

```json
{
  "url": "http://api.com/users/{userId}",
  "headers": {
    "Authorization": "Bearer {bearer}"
  }
}
```

详细说明请查看：[NEW_FEATURES_GUIDE.md](./NEW_FEATURES_GUIDE.md#环境变量使用)

### 2. 集合批量测试

**创建集合：**

1. 进入接口测试工作台
2. 点击"新建集合"按钮
3. 填写集合信息并保存

**批量运行：**

1. 在集合列表中找到目标集合
2. 点击"运行"按钮
3. 选择测试环境
4. 开始执行，自动生成报告

详细说明请查看：[NEW_FEATURES_GUIDE.md](./NEW_FEATURES_GUIDE.md#集合管理与批量测试)

### 3. 查看测试报告

**查看报告列表：**

进入"测试报告"页面，可以：
- 按类型筛选（接口/Web/性能）
- 查看测试统计
- 查看详细结果
- 下载 HTML 报告

**报告内容：**
- 执行摘要（总数、通过、失败、成功率、耗时）
- 详细结果（每个用例的执行情况）
- 环境信息
- 错误详情

详细说明请查看：[NEW_FEATURES_GUIDE.md](./NEW_FEATURES_GUIDE.md#测试报告生成与查看)

---

## 🔄 API 接口更新

### 新增接口

| 接口 | 方法 | 说明 |
|------|------|------|
| `/test-reports` | GET | 获取测试报告列表 |
| `/test-reports/{id}` | GET | 获取报告详情 |
| `/test-reports/{id}/html` | GET | 获取 HTML 格式报告 |
| `/test-reports/{id}` | DELETE | 删除测试报告 |

### 修改接口

| 接口 | 变更 | 说明 |
|------|------|------|
| `/api-test/collections/{id}/run` | 增强 | 支持环境变量、生成报告 |
| `/api-test/execute` | 增强 | 支持环境变量替换 |

完整 API 文档请查看：[API.md](./API.md)

---

## 📊 数据库变更

### 新增表

**test_reports** - 测试报告表

| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER | 主键 |
| test_run_id | INTEGER | 关联测试执行记录 |
| project_id | INTEGER | 关联项目 |
| test_type | VARCHAR(20) | 测试类型 |
| title | VARCHAR(255) | 报告标题 |
| summary | JSON | 报告摘要 |
| report_data | JSON | 详细数据 |
| report_html | TEXT | HTML 报告 |
| status | VARCHAR(20) | 状态 |
| created_at | DATETIME | 创建时间 |
| updated_at | DATETIME | 更新时间 |

### 修改表

**test_runs** - 添加字段

| 字段 | 类型 | 说明 |
|------|------|------|
| report_id | INTEGER | 关联报告 ID |

---

## 🧪 测试建议

### 1. 环境变量测试

```bash
# 1. 创建测试环境
curl -X POST http://localhost:5211/api/v1/environments \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "测试环境",
    "base_url": "http://localhost:5211",
    "variables": {"bearer": "test_token", "userId": "123"}
  }'

# 2. 创建使用变量的测试用例
curl -X POST http://localhost:5211/api/v1/api-test/cases \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "测试变量替换",
    "method": "GET",
    "url": "http://localhost:5211/api/v1/users/{userId}",
    "headers": {"Authorization": "Bearer {bearer}"}
  }'
```

### 2. 批量测试

```bash
# 运行集合并生成报告
curl -X POST http://localhost:5211/api/v1/api-test/collections/1/run \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"env_id": 1}'
```

### 3. 查看报告

```bash
# 获取报告列表
curl -X GET "http://localhost:5211/api/v1/test-reports?test_type=api" \
  -H "Authorization: Bearer YOUR_TOKEN"

# 获取报告详情
curl -X GET http://localhost:5211/api/v1/test-reports/1 \
  -H "Authorization: Bearer YOUR_TOKEN"

# 获取 HTML 报告
curl -X GET http://localhost:5211/api/v1/test-reports/1/html \
  -H "Authorization: Bearer YOUR_TOKEN"
```

---

## ⚠️ 注意事项

### 1. 数据迁移

- **务必备份数据库**后再执行迁移
- 迁移会创建新表，不影响现有数据
- 如果迁移失败，可以使用 `python manage.py db downgrade` 回滚

### 2. 环境变量格式

- 使用 `{变量名}` 格式，不是 `{{变量名}}`
- 变量名区分大小写
- 确保变量在环境中已配置

### 3. 性能考虑

- 批量测试可能耗时较长，建议合理控制集合大小
- 报告数据会随时间增长，定期清理旧报告
- 大量并发测试可能影响目标服务器

### 4. 兼容性

- 前端组件依赖 Ant Design 4.x
- 后端需要 Python 3.8+
- 数据库支持 MySQL/SQLite/PostgreSQL

---

## 🐛 已知问题

目前暂无已知问题。如发现 bug，请及时反馈。

---

## 📞 技术支持

如有问题或建议，请：

1. 查看 [NEW_FEATURES_GUIDE.md](./NEW_FEATURES_GUIDE.md)
2. 查看 [API.md](./API.md)
3. 提交 Issue 或联系开发团队

---

## 📝 后续规划

### 待开发功能

- [ ] 断言功能增强
- [ ] 数据驱动测试
- [ ] 定时任务执行
- [ ] CI/CD 集成
- [ ] 报告导出为 PDF
- [ ] 测试数据管理
- [ ] Mock 服务支持

---

## ✅ 更新检查清单

使用以下清单确保更新完整：

- [ ] 已备份数据库
- [ ] 已拉取最新代码
- [ ] 已执行数据库迁移
- [ ] 后端服务正常启动
- [ ] 前端服务正常启动
- [ ] 可以创建环境变量
- [ ] 可以创建集合
- [ ] 可以批量运行测试
- [ ] 可以查看测试报告
- [ ] 变量替换功能正常
- [ ] 报告数据完整

---

**更新完成！享受新功能吧！** 🎉
