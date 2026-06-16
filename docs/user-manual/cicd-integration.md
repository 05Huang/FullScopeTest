# CI/CD 集成指南

## 概述

FullScopeTest 支持与 CI/CD 工具集成，实现自动化测试执行。支持三种触发方式：

1. **API Token 触发** — 通过 REST API 触发测试执行
2. **Webhook 触发** — 通过 Webhook Token 触发
3. **定时触发** — 通过 Cron 表达式定时执行

## 方式一：API Token 触发

### 1. 创建 API Token

1. 进入「API Token 管理」页面
2. 点击「创建 Token」
3. 配置 Token 名称、权限（read/execute）和项目范围
4. 保存 Token（仅显示一次，请妥善保存）

### 2. 在 CI 中调用

```bash
# 触发 API 测试执行
curl -X POST https://your-domain.com/api/v1/test-runs \
  -H "Authorization: Bearer YOUR_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "project_id": 1,
    "test_type": "api",
    "test_object_id": 5,
    "triggered_by": "ci"
  }'

# 查询执行结果
curl https://your-domain.com/api/v1/test-runs/RUN_ID \
  -H "Authorization: Bearer YOUR_API_TOKEN"
```

### 3. Python SDK

```python
from fullscopetest import FullScopeTestClient

client = FullScopeTestClient(
    base_url="https://your-domain.com",
    token="YOUR_API_TOKEN"
)

# 创建并执行测试
run = client.create_test_run(project_id=1, test_type="api", test_object_id=5)
result = client.wait_for_run(run["id"])
print(f"Pass rate: {result['pass_rate']}%")
```

### 4. GitHub Actions 示例

```yaml
- name: Run API Tests
  run: |
    pip install fullscopetest
    fst run --project-id 1 --type api --token ${{ secrets.FST_TOKEN }}
```

## 方式二：Webhook 触发

1. 在「CI/CD 与定时任务」页面创建 Webhook
2. 复制 Webhook URL
3. 在代码仓库的 Webhook 设置中添加该 URL
4. 代码推送时自动触发测试

## 方式三：定时任务

1. 在「CI/CD 与定时任务」页面创建定时任务
2. 配置 Cron 表达式（如 `0 2 * * *` 每天凌晨 2 点）
3. 选择要执行的测试目标
4. 启用定时任务

## GitHub 集成

支持将测试结果回写到 GitHub PR：

1. 在「集成管理」页面连接 GitHub
2. 启用 Check Run 回写
3. PR 创建时自动执行测试并将结果写入 PR 状态

## 质量门禁

配置质量门禁规则，在 CI 中自动检查测试质量：

- 最低通过率阈值
- P95 响应时间上限
- 视觉差异百分比上限

测试结果不满足门禁条件时，CI 流水线将失败。
