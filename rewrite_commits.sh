#!/bin/bash
# 脚本名称: rewrite_commits.sh
# 功能:
#   1. 修改所有 commit 作者/提交者为你的信息
#   2. 修改 commit message 为中文描述
#   3. 每条 commit 时间提前2天
# 使用方法:
#   1. 打开 Git Bash
#   2. cd 到你的仓库目录
#   3. bash rewrite_commits.sh

# 先确保 filter-repo 生效（避免缓存问题）
git filter-repo --force --commit-callback '

import re
from datetime import datetime, timedelta, timezone

# ==== 作者信息 ====
commit.author_name = "Xuan Huang".encode("utf-8")
commit.author_email = "xuan83165@gmail.com".encode("utf-8")
commit.committer_name = "Xuan Huang".encode("utf-8")
commit.committer_email = "xuan83165@gmail.com".encode("utf-8")

# ==== 提交信息映射 ====
commit_map = {
    "new env": "配置：新增环境配置文件",
    "correct .env": "配置：修正.env文件中的环境变量配置",
    "chore(docker): make Playwright-related apt packages conditional on SKIP_PLAYWRIGHT_BROWSERS": "构建：Docker构建时根据SKIP_PLAYWRIGHT_BROWSERS参数条件安装Playwright相关apt包",
    "chore(docker): make Playwright browser install optional via SKIP_PLAYWRIGHT_BROWSERS build-arg": "构建：Docker构建支持通过SKIP_PLAYWRIGHT_BROWSERS参数跳过Playwright浏览器安装",
    "chore(docker): add Playwright/Chromium runtime deps to Dockerfile.backend.dev to fix Playwright build": "构建：Dockerfile.backend.dev中添加Playwright/Chromium运行依赖，修复Playwright构建失败问题",
    "chore: trigger ci run 3": "构建：触发CI流水线第三次运行",
    "chore: trigger ci run 2": "构建：触发CI流水线第二次运行",
    "chore: trigger ci pipeline check": "构建：触发CI流水线校验",
    "chore: trigger webhook": "构建：触发Webhook通知",
    "chore: cleanup and include web dist": "构建：清理无用文件，包含Web前端dist目录",
    "Fix Windows key ACLs for Jenkins service user": "修复：修正Windows系统下Jenkins服务用户的密钥ACL权限",
    "Fix Windows SSH key permissions before scp/ssh": "修复：在执行scp/ssh前修正Windows系统SSH密钥权限",
    "Use SSH key credential without sshagent": "优化：无需sshagent即可使用SSH密钥凭证",
    "Build frontend locally and deploy dist via SSH": "优化：本地构建前端资源，通过SSH部署dist目录",
    "Allow skipping frontend build on server": "优化：支持在服务器端跳过前端构建步骤",
    "Limit Node memory during frontend build": "优化：限制前端构建时Node.js的内存使用量",
    "Fix Jenkinsfile for Linux agent and correct deploy path": "修复：适配Linux代理节点修正Jenkinsfile，调整部署路径",
    "Sync dist to 1Panel site and update deploy guide": "优化：同步dist目录到1Panel站点，更新部署文档",
    "Retry health check in deploy script": "优化：部署脚本中增加健康检查重试机制",
    "Force docker compose to use project .env": "优化：强制docker compose使用项目根目录的.env配置文件",
    "Fix data directory path in deploy script": "修复：修正部署脚本中数据目录路径配置",
    "Fix Playwright install in backend Dockerfile": "修复：修正后端Dockerfile中Playwright的安装逻辑",
    "Run tests against shared Postgres": "优化：使用共享Postgres数据库执行测试用例",
    "Force sqlite for pytest in deploy script": "优化：部署脚本中强制pytest使用SQLite数据库",
    "Make deploy.sh executable": "配置：设置deploy.sh脚本为可执行权限",
    "Use sqlite for tests by setting TEST_DATABASE_URL": "配置：通过TEST_DATABASE_URL环境变量指定测试使用SQLite",
    "Limit pytest to tests directory": "优化：限制pytest仅扫描tests目录下的测试用例",
    "Fix f-string in perf test script generation": "修复：修正性能测试脚本生成中的f-string语法错误",
    "Update deploy guide and ignore batch files": "文档：更新部署文档，添加批量文件到.gitignore",
    "Use shared Postgres and update deploy guide": "优化：使用共享Postgres数据库，同步更新部署文档",
    "Add OpenResty installer and production deployment setup": "功能：新增OpenResty安装脚本，完善生产环境部署配置",
    "chore: cleanup unused code and docs": "构建：清理未使用的代码和文档",
    "Remove pytest references": "重构：移除代码中对pytest的引用",
    "cleanup docs and harden perf tests": "优化：清理文档内容，强化性能测试用例健壮性",
    "chore: add review summary and remove local test scripts": "构建：添加评审总结文档，移除本地测试脚本",
    "refactor: 重构测试报告模块，整合到执行记录页面": "重构：重构测试报告模块，将功能整合到执行记录页面",
    "feat: 性能测试支持自定义 Headers 和 Body": "功能：性能测试模块支持自定义请求Headers和Body参数",
    "feat: 实现性能测试实时监控功能": "功能：实现性能测试过程的实时监控展示功能",
    "docs: 更新并移动 CLAUDE.md 到根目录": "文档：更新CLAUDE.md内容并迁移至项目根目录",
    "feat: 完善环境变量功能": "功能：完善环境变量管理功能，支持更多配置项",
    "docs: 添加测试计划和脚本工具": "文档：补充测试计划说明，新增脚本工具使用文档",
    "refactor: 重组启动脚本目录结构": "重构：重新组织启动脚本的目录结构，提升可读性",
    "docs: 合并环境配置相关文档": "文档：合并分散的环境配置相关文档，统一管理",
    "refactor: 删除重复的文档和配置文件": "重构：删除重复的文档和配置文件，精简项目结构",
    "fix: 修复 Redis 和 Celery 启动配置问题": "修复：修复Redis和Celery服务启动配置错误",
    "chore: 添加开发辅助脚本和测试文件": "构建：新增开发辅助脚本和测试用例文件",
    "feat: 实现API测试环境配置功能完整应用": "功能：完整实现API测试环境配置功能并落地使用",
    "feat: 集成 Celery + Redis 异步任务系统": "功能：集成Celery+Redis异步任务系统，处理后台耗时任务",
    "refactor: 移除 Vite 开发服务器，统一使用 Nginx 托管前端": "重构：移除Vite开发服务器，统一通过Nginx托管前端资源",
    "docs: 更新 README 项目结构和文档": "文档：更新README，补充项目结构说明和文档链接",
    "docs: 更新项目README，添加详细的项目介绍和使用文档": "文档：完善项目README，新增详细的项目介绍和使用指南",
    "feat: 完成前后端完整功能实现": "功能：完成前后端所有核心功能的开发和整合"
}

# ==== 处理Commit Message ====
# 1. 解码并清理message（去除换行、多余空格）
msg_str = commit.message.decode("utf-8").strip()
# 2. 只取第一行message（Git默认第一行为主题）
msg_first_line = msg_str.split("\\n")[0].strip()

# 3. 优先精确匹配，匹配失败则尝试关键字匹配
if msg_first_line in commit_map:
    new_msg = commit_map[msg_first_line]
else:
    # 模糊匹配（按关键字）
    new_msg = msg_first_line
    for en_key, cn_key in commit_map.items():
        if en_key in msg_first_line:
            new_msg = cn_key
            break

# 4. 替换message（保留原始换行结构，只改第一行）
if "\\n" in msg_str:
    commit.message = (new_msg + msg_str[len(msg_first_line):]).encode("utf-8")
else:
    commit.message = new_msg.encode("utf-8")

# ==== 修改提交时间：提前2天 ====
# 解析Git时间格式（timestamp tz）
def adjust_time(time_str):
    parts = time_str.decode("utf-8").split()
    ts = int(parts[0])
    tz = parts[1] if len(parts) > 1 else "+0000"
    
    # 转换为datetime并减2天
    dt = datetime.fromtimestamp(ts, timezone.utc) - timedelta(days=2)
    new_ts = int(dt.timestamp())
    return f"{new_ts} {tz}".encode("utf-8")

commit.author_date = adjust_time(commit.author_date)
commit.committer_date = adjust_time(commit.committer_date)
'

# 清理Git缓存，确保修改生效
git reflog expire --expire=now --all
git gc --prune=now --aggressive

echo "✅ 提交历史修改完成！"
echo "🔍 验证结果："
git log --oneline -10  # 打印前10条提交验证