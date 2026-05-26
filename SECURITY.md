# 安全政策

## 报告安全漏洞

我们非常重视 FullScopeTest 的安全问题。如果您发现了安全漏洞，请不要通过公开的 Issue 报告，而是按照以下方式联系我们：

### 报告方式

请发送邮件至 **3441578327@qq.com**，并包含以下信息：

1. **漏洞描述** - 清晰描述发现的安全问题
2. **复现步骤** - 详细的复现步骤
3. **影响范围** - 漏洞可能造成的影响
4. **修复建议** - 如果有修复建议请一并提供

### 响应时间

- **确认收到** - 24 小时内
- **初步评估** - 72 小时内
- **修复计划** - 7 天内
- **修复发布** - 根据严重程度，30 天内

### 漏洞严重程度

我们将根据 CVSS v3.1 标准评估漏洞严重程度：

| 严重程度 | 分数 | 响应时间 |
|----------|------|----------|
| 严重 (Critical) | 9.0-10.0 | 24 小时内修复 |
| 高危 (High) | 7.0-8.9 | 7 天内修复 |
| 中危 (Medium) | 4.0-6.9 | 30 天内修复 |
| 低危 (Low) | 0.1-3.9 | 下个版本修复 |

## 安全最佳实践

### 部署安全

1. **修改默认密码** — 部署后立即修改默认管理员密码（默认 `admin / admin123`）
2. **使用强密钥** — 生成随机的 `SECRET_KEY` 和 `JWT_SECRET_KEY`，禁止使用默认值
3. **启用 HTTPS** — 生产环境必须使用 HTTPS
4. **配置 CORS** — 仅允许受信任的域名
5. **限制访问** — 使用防火墙限制不必要的端口访问
6. **数据库** — 生产环境使用 PostgreSQL，禁止使用 SQLite

### 密钥生成

```bash
# 生成 Flask SECRET_KEY
python -c "import secrets; print(secrets.token_hex(32))"

# 生成 JWT SECRET_KEY
python -c "import secrets; print(secrets.token_hex(32))"
```

### 环境变量安全

- 永远不要将 `.env` 文件提交到版本控制系统（已在 `.gitignore` 中排除）
- 使用 `backend/.env.example` 作为模板
- 定期轮换 API 密钥和数据库密码
- 生产环境建议使用密钥管理服务（如 AWS Secrets Manager、HashiCorp Vault）

### CI/CD 安全

项目已配置 GitHub Actions 安全扫描：
- **CodeQL** — 自动检测 OWASP Top 10 漏洞（SQL 注入、XSS、路径遍历等）
- **依赖审计** — 自动检测已知漏洞的依赖包
- 所有 PR 合并前需通过 CI 检查

## 已知安全限制

1. **Webhook 端点** — Webhook 触发端点 (`/api/v1/triggers/<token>`) 使用 HMAC-SHA256 签名验证，建议配合 IP 白名单使用
2. **子进程执行** — Web 测试和 APP 测试通过 `subprocess.run()` 执行用户提交的脚本，确保仅授权用户可提交脚本
3. **AI API 密钥** — AI 助手功能需要配置第三方 LLM API 密钥，请确保密钥权限最小化，建议使用只读权限的 API Key
4. **Celery 任务** — 异步任务执行环境与 Web 服务共享数据库，建议生产环境对 Celery Worker 进行资源限制

## 安全更新

我们会在 GitHub Releases 中发布安全更新，并在 CHANGELOG.md 中记录安全相关的变更。建议订阅 Release 通知以获取最新的安全更新。

## 致谢

我们感谢以下安全研究人员的贡献：

<!-- 在此添加安全研究人员名单 -->

---

感谢您帮助我们保持 FullScopeTest 的安全！
