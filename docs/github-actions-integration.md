# FullScopeTest GitHub Actions 集成指南

> 本文档指导你将 FullScopeTest 测试平台集成到 GitHub Actions CI/CD 流程中，实现 PR 自动测试、定时回归和按需触发。

---

## 目录

- [1. 前置条件](#1-前置条件)
- [2. 从零到一：5 分钟完成集成](#2-从零到一5-分钟完成集成)
- [3. 创建 API Token](#3-创建-api-token)
- [4. 配置 Quality Gate（可选）](#4-配置-quality-gate可选)
- [5. 场景一：PR 自动触发测试](#5-场景一pr-自动触发测试)
- [6. 场景二：定时回归测试](#6-场景二定时回归测试)
- [7. 场景三：手动触发测试](#7-场景三手动触发测试)
- [8. GitHub Action 输入参数参考](#8-github-action-输入参数参考)
- [9. GitHub Action 输出变量参考](#9-github-action-输出变量参考)
- [10. 进阶：自定义触发规则](#10-进阶自定义触发规则)
- [11. 进阶：使用 GitHub Webhook 自动触发](#11-进阶使用-github-webhook-自动触发)
- [12. 安全最佳实践](#12-安全最佳实践)
- [13. 常见问题排查](#13-常见问题排查)

---

## 1. 前置条件

在开始之前，请确保你已经准备好以下内容：

| 条件 | 说明 |
|------|------|
| FullScopeTest 实例 | 已部署并可访问的 FullScopeTest 服务（可以是自托管或云端） |
| GitHub 仓库 | 你的项目代码仓库，且有 `Actions` 读写权限 |
| API Token | FullScopeTest 中生成的 API Token（用于认证） |
| 测试项目 ID | FullScopeTest 中已创建的项目 ID |
| 测试套件 ID | FullScopeTest 中已配置的测试套件 ID（可选） |
| Quality Gate ID | 已配置的质量门禁 ID（可选） |

> **提示**：如果你还没有部署 FullScopeTest，请参考 [部署文档](deployment.md) 完成部署。

---

## 2. 从零到一：5 分钟完成集成

以下是最快集成路径：

```bash
# 步骤 1：登录 FullScopeTest → 设置 → API Token → 创建 Token
# 步骤 2：获取项目 ID（从项目列表 URL 中查看，如 /projects/1 中的 1）
# 步骤 3：在 GitHub 仓库中设置 Secrets：
#         Settings → Secrets and variables → Actions → New repository secret
#         Name: FULLSCOPETEST_SERVER_URL   Value: https://your-fst-instance.com
#         Name: FULLSCOPETEST_API_TOKEN    Value: 你的 API Token
#         Name: FULLSCOPETEST_PROJECT_ID   Value: 你的项目 ID
# 步骤 4：在 .github/workflows/ 创建 fst-ci.yml（参考本文档的 YAML 示例）
# 步骤 5：推送代码，验证 Actions 运行
```

---

## 3. 创建 API Token

FullScopeTest 支持两种认证方式，推荐在 CI/CD 中使用 **API Token**（更安全、更方便）：

### 方式一：通过 Web 界面创建

1. 登录 FullScopeTest 平台
2. 点击右上角头像 → **设置**
3. 选择 **API Token** 标签页
4. 点击 **创建 Token**
5. 输入名称（如 `github-actions-ci`）
6. 选择权限范围（CI/CD 推荐选择 `read-write`）
7. 点击确认，**立即复制 Token**（仅展示一次）

### 方式二：通过 API 创建

```bash
# 先获取 JWT Token（登录）
JWT_TOKEN=$(curl -s -X POST https://your-fst-instance.com/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "your-password"}' | python3 -c "import sys,json; print(json.load(sys.stdin)['data']['access_token'])")

# 创建 API Token
curl -s -X POST https://your-fst-instance.com/api/v1/tokens \
  -H "Authorization: Bearer $JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "github-actions-ci",
    "permissions": "read-write",
    "description": "CI/CD pipeline token"
  }'
```

### 验证 Token

```bash
# 用 API Token 获取当前用户信息，验证 Token 是否有效
curl -s https://your-fst-instance.com/api/v1/auth/me \
  -H "Authorization: Bearer YOUR_API_TOKEN"
```

---

## 4. 配置 Quality Gate（可选）

Quality Gate 可以在测试执行后自动评估结果，判断是否满足质量标准：

### 4.1 通过 Web 界面创建

1. 进入 FullScopeTest → **项目设置** → **质量门禁**
2. 点击 **新建门禁**
3. 配置规则：
   - **最小通过率**：如 `95.0`（表示测试通过率需 ≥ 95%）
   - **P95 响应时间上限**：如 `2000`（毫秒，仅性能测试生效）
   - **视觉差异上限**：如 `5.0`（百分比，仅 UI 测试生效）
4. 保存后获取门禁 ID

### 4.2 通过 API 创建

```bash
curl -s -X POST https://your-fst-instance.com/api/v1/quality-gates \
  -H "Authorization: Bearer $JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "project_id": 1,
    "name": "PR Quality Gate",
    "description": "PR 合并前的质量标准",
    "min_pass_rate": 95.0,
    "max_p95_response_time": 2000,
    "max_visual_diff_percentage": 5.0,
    "is_active": true
  }'
```

### 4.3 门禁字段说明

| 字段 | 类型 | 说明 | 示例 |
|------|------|------|------|
| `min_pass_rate` | float | 最小通过率（%） | `95.0` |
| `max_p95_response_time` | float | P95 响应时间上限（ms） | `2000` |
| `max_visual_diff_percentage` | float | 视觉差异上限（%） | `5.0` |

> **提示**：Quality Gate 评估结果会自动同步到 GitHub Check Run，PR 页面可直接看到门禁状态。

---

## 5. 场景一：PR 自动触发测试

当 Pull Request 被创建或更新时，自动运行测试并将结果回写到 PR 页面。

### 工作流程

```
PR 创建/更新 → GitHub Actions 触发 → 创建测试运行 → 等待完成 → 评估 Quality Gate → 更新 PR 状态
```

### 工作流文件

创建文件 `.github/workflows/fst-pr-test.yml`：

```yaml
name: FullScopeTest PR Testing

# 触发条件：PR 被创建或有新的 push
on:
  pull_request:
    branches: [main, develop, 'release/**']
    types: [opened, synchronize, reopened]

# 取消同一 PR 的重复运行
concurrency:
  group: fst-pr-${{ github.event.pull_request.number }}
  cancel-in-progress: true

jobs:
  api-tests:
    name: API Integration Tests
    runs-on: ubuntu-latest
    timeout-minutes: 15

    steps:
      - name: Run FullScopeTest API Tests
        uses: 05Huang/FullScopeTest/.github/actions/fullscope-test@main
        with:
          server-url: ${{ secrets.FULLSCOPETEST_SERVER_URL }}
          api-token: ${{ secrets.FULLSCOPETEST_API_TOKEN }}
          project-id: ${{ secrets.FULLSCOPETEST_PROJECT_ID }}
          test-suite-id: ${{ secrets.FULLSCOPETEST_API_SUITE_ID }}

  quality-gate:
    name: Quality Gate
    needs: api-tests
    if: always() && needs.api-tests.result != 'cancelled'
    runs-on: ubuntu-latest
    timeout-minutes: 5

    steps:
      - name: Run FullScopeTest Quality Gate
        uses: 05Huang/FullScopeTest/.github/actions/fullscope-test@main
        with:
          server-url: ${{ secrets.FULLSCOPETEST_SERVER_URL }}
          api-token: ${{ secrets.FULLSCOPETEST_API_TOKEN }}
          project-id: ${{ secrets.FULLSCOPETEST_PROJECT_ID }}
          quality-gate-id: ${{ secrets.FULLSCOPETEST_PR_QUALITY_GATE_ID }}
```

### 需要配置的 Secrets

| Secret 名称 | 说明 | 示例 |
|-------------|------|------|
| `FULLSCOPETEST_SERVER_URL` | FullScopeTest 服务地址 | `https://fst.example.com` |
| `FULLSCOPETEST_API_TOKEN` | API Token | `fst_xxx...` |
| `FULLSCOPETEST_PROJECT_ID` | 项目 ID | `1` |
| `FULLSCOPETEST_API_SUITE_ID` | API 测试套件 ID | `10` |
| `FULLSCOPETEST_PR_QUALITY_GATE_ID` | PR 质量门禁 ID（可选） | `1` |

### 效果

- PR 页面会显示 **FullScopeTest - API Test** Check Run 状态
- 测试进行中显示 🟡，通过显示 🟢，失败显示 🔴
- Quality Gate 评估结果单独显示在 PR Checks 列表中
- 点击 Check Run 可查看详细的测试报告和失败用例摘要

---

## 6. 场景二：定时回归测试

在指定时间自动运行完整回归测试，确保系统稳定性。

### 工作流文件

创建文件 `.github/workflows/fst-scheduled-regression.yml`：

```yaml
name: FullScopeTest Scheduled Regression

# 触发条件：定时运行（每周一到周五，凌晨 2 点 UTC）
on:
  schedule:
    - cron: '0 2 * * 1-5'

  # 允许手动触发，覆盖定时
  workflow_dispatch:
    inputs:
      test_type:
        description: '测试类型'
        required: false
        default: 'all'
        type: choice
        options:
          - all
          - api
          - web
          - performance

jobs:
  regression-tests:
    name: Full Regression Suite
    runs-on: ubuntu-latest
    timeout-minutes: 30

    steps:
      - name: Run FullScopeTest Regression
        uses: 05Huang/FullScopeTest/.github/actions/fullscope-test@main
        with:
          server-url: ${{ secrets.FULLSCOPETEST_SERVER_URL }}
          api-token: ${{ secrets.FULLSCOPETEST_API_TOKEN }}
          project-id: ${{ secrets.FULLSCOPETEST_PROJECT_ID }}
          test-suite-id: ${{ secrets.FULLSCOPETEST_REGRESSION_SUITE_ID }}
          quality-gate-id: ${{ secrets.FULLSCOPETEST_REGRESSION_GATE_ID }}

  notify:
    name: Notify Team
    needs: regression-tests
    if: always()
    runs-on: ubuntu-latest

    steps:
      - name: Send Slack Notification
        if: ${{ secrets.SLACK_WEBHOOK_URL != '' }}
        run: |
          STATUS="${{ needs.regression-tests.result }}"
          EMOJI="🟢"
          if [ "$STATUS" != "success" ]; then
            EMOJI="🔴"
          fi

          curl -s -X POST "${{ secrets.SLACK_WEBHOOK_URL }}" \
            -H "Content-Type: application/json" \
            -d "{
              \"text\": \"$EMOJI 回归测试完成\",
              \"blocks\": [
                {
                  \"type\": \"section\",
                  \"text\": {
                    \"type\": \"mrkdwn\",
                    \"text\": \"$EMOJI *FullScopeTest 回归测试*\n*结果*: ${STATUS}\n*分支*: ${{ github.ref_name }}\n*详情*: ${{ github.server_url }}/${{ github.repository }}/actions/runs/${{ github.run_id }}\"
                  }
                }
              ]
            }"

      - name: Create GitHub Issue on Failure
        if: ${{ needs.regression-tests.result == 'failure' }}
        uses: actions/github-script@v7
        with:
          script: |
            await github.rest.issues.create({
              owner: context.repo.owner,
              repo: context.repo.repo,
              title: `🔴 回归测试失败 - ${new Date().toISOString().split('T')[0]}`,
              body: `## 回归测试失败报告\n\n` +
                    `- **分支**: ${context.ref}\n` +
                    `- **触发时间**: ${new Date().toISOString()}\n` +
                    `- **Actions 链接**: ${context.serverUrl}/${context.repo.owner}/${context.repo.repo}/actions/runs/${context.runId}\n\n` +
                    `请检查测试报告并修复相关问题。`,
              labels: ['bug', 'test-failure']
            });
```

### 效果

- 每周一到周五凌晨 2 点（UTC）自动运行回归测试
- 也可通过 GitHub Actions 界面手动触发，支持选择测试类型
- 测试失败自动创建 GitHub Issue
- 可选：发送 Slack 通知

---

## 7. 场景三：手动触发测试

在特定场景下（如发布前验证、环境部署后验证）手动触发测试。

### 工作流文件

创建文件 `.github/workflows/fst-manual-test.yml`：

```yaml
name: FullScopeTest Manual Testing

on:
  workflow_dispatch:
    inputs:
      environment:
        description: '测试环境'
        required: true
        type: choice
        options:
          - staging
          - production
      test_suite_id:
        description: '测试套件 ID（留空则运行项目默认套件）'
        required: false
        type: string
      run_performance:
        description: '是否运行性能测试'
        required: false
        type: boolean
        default: false

jobs:
  run-tests:
    name: Run Tests - ${{ inputs.environment }}
    runs-on: ubuntu-latest
    timeout-minutes: 30

    environment: ${{ inputs.environment }}

    steps:
      - name: Run FullScopeTest Tests
        uses: 05Huang/FullScopeTest/.github/actions/fullscope-test@main
        with:
          server-url: ${{ secrets.FULLSCOPETEST_SERVER_URL }}
          api-token: ${{ secrets.FULLSCOPETEST_API_TOKEN }}
          project-id: ${{ secrets.FULLSCOPETEST_PROJECT_ID }}
          test-suite-id: ${{ inputs.test_suite_id || secrets.FULLSCOPETEST_DEFAULT_SUITE_ID }}
          quality-gate-id: ${{ secrets.FULLSCOPETEST_QA_GATE_ID }}

  run-performance:
    name: Run Performance Tests
    needs: run-tests
    if: inputs.run_performance == true && needs.run-tests.result == 'success'
    runs-on: ubuntu-latest
    timeout-minutes: 30

    environment: ${{ inputs.environment }}

    steps:
      - name: Run FullScopeTest Performance Tests
        uses: 05Huang/FullScopeTest/.github/actions/fullscope-test@main
        with:
          server-url: ${{ secrets.FULLSCOPETEST_SERVER_URL }}
          api-token: ${{ secrets.FULLSCOPETEST_API_TOKEN }}
          project-id: ${{ secrets.FULLSCOPETEST_PROJECT_ID }}
          test-suite-id: ${{ secrets.FULLSCOPETEST_PERF_SUITE_ID }}

  report:
    name: Generate Report
    needs: [run-tests, run-performance]
    if: always()
    runs-on: ubuntu-latest

    steps:
      - name: Upload Test Report
        run: |
          echo "## Test Results" >> $GITHUB_STEP_SUMMARY
          echo "| Test Type | Status |" >> $GITHUB_STEP_SUMMARY
          echo "|-----------|--------|" >> $GITHUB_STEP_SUMMARY
          echo "| Functional | ${{ needs.run-tests.result }} |" >> $GITHUB_STEP_SUMMARY
          if [ "${{ inputs.run_performance }}" = "true" ]; then
            echo "| Performance | ${{ needs.run-performance.result }} |" >> $GITHUB_STEP_SUMMARY
          fi
          echo "" >> $GITHUB_STEP_SUMMARY
          echo "**Environment**: ${{ inputs.environment }}" >> $GITHUB_STEP_SUMMARY
          echo "**Triggered by**: ${{ github.actor }}" >> $GITHUB_STEP_SUMMARY
          echo "**Time**: $(date -u +'%Y-%m-%d %H:%M:%S UTC')" >> $GITHUB_STEP_SUMMARY
```

### 效果

- 在 GitHub Actions 页面点击 **Run workflow**
- 选择环境（staging/production）、测试套件、是否运行性能测试
- 基于 GitHub Environment 机制，可配置环境保护规则（如需要审批）
- 自动生成测试结果摘要到 Actions Summary

---

## 8. GitHub Action 输入参数参考

| 参数 | 必填 | 默认值 | 说明 |
|------|------|--------|------|
| `server-url` | ✅ | - | FullScopeTest 服务 URL |
| `api-token` | ✅ | - | API Token（需 `read-write` 权限） |
| `project-id` | ✅ | - | 项目 ID |
| `test-suite-id` | ❌ | `''` | 测试套件 ID（为空则运行项目默认套件） |
| `quality-gate-id` | ❌ | `''` | 质量门禁 ID（为空则跳过评估） |

---

## 9. GitHub Action 输出变量参考

| 输出变量 | 说明 |
|----------|------|
| `test-run-id` | 创建的测试运行 ID |
| `status` | 最终测试状态（`success` / `failed` / `cancelled`） |

### 使用输出变量

```yaml
steps:
  - name: Run FullScopeTest
    id: fst
    uses: 05Huang/FullScopeTest/.github/actions/fullscope-test@main
    with:
      server-url: ${{ secrets.FULLSCOPETEST_SERVER_URL }}
      api-token: ${{ secrets.FULLSCOPETEST_API_TOKEN }}
      project-id: ${{ secrets.FULLSCOPETEST_PROJECT_ID }}
      test-suite-id: 10

  - name: Use outputs
    run: |
      echo "Test Run ID: ${{ steps.fst.outputs.test-run-id }}"
      echo "Status: ${{ steps.fst.outputs.status }}"
```

---

## 10. 进阶：自定义触发规则

FullScopeTest 支持通过 **触发规则引擎** 配置更精细的触发条件，实现「变更感知测试」。

### 通过 API 创建触发规则

```bash
# 创建规则：当 PR 目标分支为 main 时，运行标签为 regression 的 API 测试
curl -s -X POST https://your-fst-instance.com/api/v1/trigger-rules \
  -H "Authorization: Bearer $JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "project_id": 1,
    "name": "PR to main - API Regression",
    "trigger_event": "pull_request",
    "target_branches": ["main"],
    "include_paths": ["backend/**", "web/src/api/**"],
    "exclude_paths": ["docs/**", "**/*.md"],
    "test_types": ["api"],
    "tags": ["regression"],
    "target_type": "api_collection",
    "target_id": 10,
    "is_active": true
  }'
```

```bash
# 创建规则：当后端代码变更时，运行接口测试
curl -s -X POST https://your-fst-instance.com/api/v1/trigger-rules \
  -H "Authorization: Bearer $JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "project_id": 1,
    "name": "Backend changes - API tests",
    "trigger_event": "push",
    "target_branches": ["main", "develop"],
    "include_paths": ["backend/**"],
    "exclude_paths": ["backend/tests/**", "backend/docs/**"],
    "test_types": ["api"],
    "target_type": "api_collection",
    "target_id": 10,
    "is_active": true
  }'
```

### 触发规则字段说明

| 字段 | 类型 | 说明 |
|------|------|------|
| `trigger_event` | string | 触发事件：`push` / `pull_request` / `tag` |
| `target_branches` | list | 目标分支模式（支持 `*` 通配符） |
| `include_paths` | list | 包含的文件路径模式（如 `backend/**`） |
| `exclude_paths` | list | 排除的文件路径模式 |
| `test_types` | list | 测试类型：`api` / `web` / `perf` |
| `tags` | list | 测试标签过滤 |
| `target_id` | int | 测试套件 ID（为空则运行所有匹配的测试） |

> **提示**：配合 GitHub Webhook 使用时，FullScopeTest 会根据变更的文件自动匹配触发规则，只运行相关测试。

---

## 11. 进阶：使用 GitHub Webhook 自动触发

除了 GitHub Actions，FullScopeTest 还支持通过 GitHub Webhook 直接触发测试，无需额外的 GitHub Actions 工作流。

### 配置步骤

#### 步骤 1：绑定 GitHub 账号

```bash
# 通过 OAuth 绑定 GitHub 账号
# 在 FullScopeTest 平台中：设置 → 集成 → GitHub → 绑定账号
# 或通过 API：
curl -s -X GET https://your-fst-instance.com/api/v1/integrations/github/auth \
  -H "Authorization: Bearer $JWT_TOKEN"
```

#### 步骤 2：配置 GitHub Webhook

1. 打开你的 GitHub 仓库 → **Settings** → **Webhooks** → **Add webhook**
2. 配置：
   - **Payload URL**: `https://your-fst-instance.com/api/v1/webhooks/github`
   - **Content type**: `application/json`
   - **Secret**: 与 FullScopeTest 中配置的 `GITHUB_WEBHOOK_SECRET` 一致
   - **Events**: 选择 `Pull requests` 和 `Pushes`

#### 步骤 3：验证 Webhook

```bash
# FullScopeTest 提供的 Webhook 端点
# POST /api/v1/webhooks/github
#
# 支持的事件：
# - push（push 到目标分支时触发）
# - pull_request（PR opened/synchronize/reopened 时触发）
# - ping（返回 pong，用于验证连通性）
```

### Webhook 与 GitHub Actions 的对比

| 特性 | GitHub Actions | GitHub Webhook |
|------|----------------|----------------|
| 执行环境 | GitHub Runner | FullScopeTest 服务端 |
| 测试结果展示 | GitHub Check Run | GitHub Check Run |
| 配置复杂度 | 需要 YAML 文件 | 仅需 Webhook URL |
| 灵活度 | 高（支持矩阵、并行） | 中（依赖触发规则） |
| 适用场景 | 需要额外构建步骤 | 纯 API/Web UI 测试 |

> **建议**：两种方式可以并存。简单场景用 Webhook，需要自定义流程（如构建、部署后测试）用 Actions。

---

## 12. 安全最佳实践

### 12.1 Token 安全

```yaml
# ✅ 正确：使用 GitHub Secrets
with:
  api-token: ${{ secrets.FULLSCOPETEST_API_TOKEN }}

# ❌ 错误：直接硬编码
with:
  api-token: fst_xxxxx  # 永远不要这样做！
```

### 12.2 Secrets 配置建议

| 实践 | 说明 |
|------|------|
| 使用 Organization Secrets | 在 GitHub Organization 层面配置，所有仓库共享 |
| 限制 Environment 访问 | 为 production 配置审批流程 |
| 定期轮换 Token | 建议每 90 天轮换一次 API Token |
| 最小权限原则 | CI/CD Token 只需要 `read-write`，不需要 `admin` |

### 12.3 Webhook 安全

```bash
# 1. 配置 Webhook Secret（在 FullScopeTest 的 .env 中）
GITHUB_WEBHOOK_SECRET=your-random-secret-here

# 2. 在 GitHub Webhook 设置中使用相同的 Secret
# 3. FullScopeTest 会验证 HMAC-SHA256 签名
```

---

## 13. 常见问题排查

### Q1: Action 报错 "Failed to create test run"

**可能原因**：
- API Token 无效或已过期
- Server URL 不正确
- 项目 ID 不存在

**排查步骤**：
```bash
# 1. 验证 Token
curl -s https://your-fst-instance.com/api/v1/auth/me \
  -H "Authorization: Bearer $YOUR_TOKEN"

# 2. 检查项目 ID
curl -s https://your-fst-instance.com/api/v1/projects \
  -H "Authorization: Bearer $YOUR_TOKEN"
```

### Q2: 测试运行卡住不结束

**可能原因**：
- Celery Worker 未运行
- Redis 连接问题

**排查步骤**：
```bash
# 检查 Worker 状态
docker compose logs celery | tail -20

# 检查 Redis
docker compose exec redis redis-cli ping
```

### Q3: Quality Gate 评估失败但测试通过

**可能原因**：
- Quality Gate 的阈值设置过于严格
- 测试结果数据尚未完全写入

**排查步骤**：
```bash
# 查看 Quality Gate 配置
curl -s https://your-fst-instance.com/api/v1/quality-gates/$GATE_ID \
  -H "Authorization: Bearer $YOUR_TOKEN"

# 查看最近的评估结果
curl -s "https://your-fst-instance.com/api/v1/quality-gates/$GATE_ID/evaluations" \
  -H "Authorization: Bearer $YOUR_TOKEN"
```

### Q4: GitHub Check Run 未显示在 PR 中

**可能原因**：
- GitHub App 权限不足
- Check Run 创建失败

**排查步骤**：
```bash
# 查看 FullScopeTest 日志
docker compose logs backend | grep -i "check run"
```

### Q5: Action 运行时间过长

**建议**：
- 为 Action 添加 `timeout-minutes` 限制
- 检查测试套件中是否有耗时的测试用例
- 使用 `concurrency` 配置避免重复运行

```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    timeout-minutes: 15  # 添加超时限制
```

### Q6: Webhook 接收但未触发测试

**可能原因**：
- 触发规则未匹配
- Webhook Secret 配置不一致

**排查步骤**：
```bash
# 查看 FullScopeTest Webhook 日志
docker compose logs backend | grep -i "webhook"

# 检查触发规则
curl -s https://your-fst-instance.com/api/v1/trigger-rules?project_id=1 \
  -H "Authorization: Bearer $YOUR_TOKEN"
```

---

## 附录：完整的 GitHub Actions Secrets 配置清单

```
# 必须配置
FULLSCOPETEST_SERVER_URL=https://fst.example.com
FULLSCOPETEST_API_TOKEN=fst_xxxxx...
FULLSCOPETEST_PROJECT_ID=1

# 可选配置（按需使用）
FULLSCOPETEST_API_SUITE_ID=10
FULLSCOPETEST_REGRESSION_SUITE_ID=20
FULLSCOPETEST_PERF_SUITE_ID=30
FULLSCOPETEST_PR_QUALITY_GATE_ID=1
FULLSCOPETEST_REGRESSION_GATE_ID=2
FULLSCOPETEST_DEFAULT_SUITE_ID=10
FULLSCOPETEST_QA_GATE_ID=1
```

---

> 如有问题，请访问 [FullScopeTest GitHub](https://github.com/05Huang/FullScopeTest) 提交 Issue，或参考 [部署文档](deployment.md) 和 [API 参考文档](api-reference.md)。
