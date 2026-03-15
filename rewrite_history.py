# rewrite_history.py
from datetime import datetime, timedelta

DELTA_DAYS = 2

# 提交信息映射（普通 str）
MESSAGE_MAP = {
    "renameProjectName": "重构：统一项目命名规范",
    "docs: update README for AI orchestration and web capability changes": "文档：更新README，补充AI编排能力和Web功能变更说明",
    "fix(web-test): disable 5s polling and update frontend build assets": "修复：Web测试模块关闭5秒轮询机制，同步更新前端构建资源",
    "fix(migration): make perf script_content migration idempotent": "修复：迁移脚本保证script_content字段迁移幂等性",
    "fix(migrations): make historical schema upgrades idempotent": "修复：历史Schema升级脚本保证幂等执行",
    "fix(deploy): auto-heal alembic drift and upgrade all heads": "修复：部署流程自动修复alembic版本漂移问题，升级所有分支头版本",
    "fix(migration): merge alembic heads for web/perf branches": "修复：合并Web/性能测试分支的alembic版本头",
    "feat: 对齐Web自动化用例管理、报告落库并更新部署迁移": "功能：对齐Web自动化用例管理、报告落库逻辑，更新部署迁移脚本",
    "feat(ai-workspace): allow runtime model config from frontend panel": "功能：AI工作台支持从前端面板配置运行时模型参数",
    "feat(api-workspace): add AI assistant planning and execution flow": "功能：API工作台新增AI助手用例规划与执行流程",
    "feat(api-test): split save/new/delete actions and remove clear button": "功能：API测试模块拆分保存/新建/删除操作，移除清空按钮",
    "ci: simplify frontend asset verification and print assets list": "构建：简化前端资源校验逻辑，增加资源列表打印",
    "ci: avoid Windows cmd pipe parsing in remote asset verification": "构建：修复Windows CMD管道解析导致的远程资源校验失败问题",
    "ci: remove Groovy-conflicting dollar syntax from asset verification": "构建：移除资产校验脚本中与Groovy冲突的美元符号语法",
    "ci: fix Jenkins Groovy parse error in frontend cleanup command": "构建：修复Jenkins前端清理命令的Groovy语法解析错误",
    "ci: force full frontend sync and verify asset hash exists": "构建：强制全量同步前端资源，校验资源哈希值存在性",
    "ci: upload dist to site path after backend deploy": "构建：后端部署完成后自动上传dist目录到站点路径",
    "feat(api-test): 优化用例工作台新建/树选择/删除交互": "功能：API测试用例工作台优化新建/树选择/删除交互体验",
    "fix(web-test): unify async run status handling": "修复：Web测试模块统一异步运行状态处理逻辑",
    "perf: 提升并发吞吐并优化批量调度": "性能：提升系统并发吞吐能力，优化批量调度逻辑",
    "ci: 修正Jenkins部署目录路径": "构建：修正Jenkins部署目录路径配置",
    "feat: 支持Locust阶梯加压与前后端透传": "功能：支持Locust阶梯加压模式，实现前后端参数透传",
    "correct deploy.sh": "修复：修正deploy.sh脚本执行逻辑",
    "new env": "配置：新增环境配置文件",
    "correct .env": "配置：修正.env环境变量配置",
    "chore(docker): make Playwright-related apt packages conditional on SKIP_PLAYWRIGHT_BROWSERS": "构建：Docker构建时根据SKIP_PLAYWRIGHT_BROWSERS参数条件安装Playwright相关apt包",
    "chore(docker): make Playwright browser install optional via SKIP_PLAYWRIGHT_BROWSERS build-arg": "构建：Docker构建支持通过SKIP_PLAYWRIGHT_BROWSERS参数跳过Playwright浏览器安装",
    "chore(docker): add Playwright/Chromium runtime deps to Dockerfile.backend.dev to fix Playwright build": "构建：Dockerfile.backend.dev中添加Playwright/Chromium运行依赖，修复Playwright构建失败问题",
    "chore: trigger ci run 3": "构建：触发CI流水线第三次运行"
}

def commit_callback(commit):
    commit.author_name = b"Xuan Huang"
    commit.author_email = b"xuan83165@gmail.com"
    commit.committer_name = b"Xuan Huang"
    commit.committer_email = b"xuan83165@gmail.com"

    commit.author_time -= DELTA_DAYS * 24 * 3600
    commit.committer_time -= DELTA_DAYS * 24 * 3600

    msg_str = commit.message.decode("utf-8")
    if msg_str in MESSAGE_MAP:
        commit.message = MESSAGE_MAP[msg_str].encode("utf-8")