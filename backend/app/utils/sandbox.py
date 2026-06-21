"""
脚本沙箱执行工具 — 安全隔离用户脚本

功能：
- 将用户脚本写入临时文件后通过 subprocess 执行（禁止 shell=True）
- 限制执行超时和工作目录
- 通过 AST 检查拦截危险 API 调用
- 记录脚本执行审计日志
- 支持 SANDBOX_MODE 环境变量扩展（subprocess/docker）
"""

import ast
import hashlib
import ipaddress
import os
import subprocess
import sys
import tempfile
import time
from datetime import datetime, timezone
from typing import Optional
from urllib.parse import urlparse

from ..core.logging import get_logger

logger = get_logger(__name__)

# 默认执行超时（秒）
DEFAULT_TIMEOUT = 300

# AST 检查中拦截的危险模块和函数
BLOCKED_IMPORTS = {
    "os",          # os.system, os.popen 等
    "shutil",      # 文件删除等（部分场景）
    "pty",         # 伪终端
    "telnetlib",   # 远程连接
    "subprocess",  # 整体导入拦截，仅允许 from subprocess import run/Popen 等白名单
    "ctypes",      # 直接内存操作
    "socket",      # 原始网络套接字
    "http.server", # HTTP 服务器
    "http.client", # 底层 HTTP 客户端
    "xmlrpc",      # XML-RPC 远程调用
    "code",        # 交互式解释器
    "compileall",  # 编译所有 .py 文件
    "zipimport",   # 从 zip 导入
    "importlib",   # 动态导入（可绕过静态检查）
    "pkgutil",     # 包工具
    "pdb",         # 调试器
    "profile",     # 性能分析
    "cProfile",    # 性能分析
    "traceback",   # 堆栈跟踪（信息泄露）
    "faulthandler",# 崩溃转储
    "signal",      # 信号处理
    "multiprocessing",  # 多进程
    "threading",   # 多线程（可用于 DoS）
    "asyncio",     # 异步（可用于 DoS）
}

BLOCKED_FUNCTIONS = {
    "system",      # os.system
    "popen",       # os.popen
    "call",        # subprocess.call（当 shell=True 时）
    "check_output",  # subprocess.check_output（潜在滥用）
    "check_call",  # subprocess.check_call
    "spawn",       # multiprocessing.spawn
    "fork",        # os.fork
}

# subprocess 模块中允许的属性（白名单模式）
ALLOWED_SUBPROCESS_ATTRS = {"run", "PIPE", "STDOUT", "DEVNULL", "TimeoutExpired", "CompletedProcess"}


def _get_sandbox_mode() -> str:
    """
    获取沙箱执行模式

    环境变量 SANDBOX_MODE：
    - subprocess（默认）：子进程隔离
    - docker：Docker 容器隔离（预留扩展点）
    """
    return os.environ.get("SANDBOX_MODE", "subprocess").lower()


def _compute_script_hash(script_content: str) -> str:
    """计算脚本内容的 SHA-256 哈希值，用于审计日志"""
    return hashlib.sha256(script_content.encode("utf-8")).hexdigest()[:16]


def check_script_safety(script_content: str) -> tuple:
    """
    通过 AST 静态分析检查脚本安全性

    Args:
        script_content: 用户脚本源代码

    Returns:
        (is_safe, message):
            - (True, "") 安全
            - (False, "拦截原因") 不安全
    """
    try:
        tree = ast.parse(script_content)
    except SyntaxError as e:
        # 语法错误的脚本会在执行时报错，此处不拦截
        return True, ""

    for node in ast.walk(tree):
        # 检查 import 语句：import os / from os import system
        if isinstance(node, ast.Import):
            for alias in node.names:
                module_name = alias.name.split(".")[0]
                if module_name in BLOCKED_IMPORTS:
                    return False, f"脚本不允许导入模块: {alias.name}"

        # 检查 from X import Y 语句
        if isinstance(node, ast.ImportFrom):
            if node.module:
                module_name = node.module.split(".")[0]
                if module_name in BLOCKED_IMPORTS:
                    # 允许 from subprocess import run, Popen 等安全接口
                    if module_name == "subprocess":
                        for alias in node.names:
                            if alias.name not in ALLOWED_SUBPROCESS_ATTRS:
                                return False, f"脚本不允许使用 subprocess.{alias.name}"
                    else:
                        return False, f"脚本不允许从 {node.module} 导入"

        # 检查 __import__ 调用
        if isinstance(node, ast.Call):
            func = node.func
            if isinstance(func, ast.Name) and func.id == "__import__":
                if node.args and isinstance(node.args[0], ast.Constant):
                    if node.args[0].value in BLOCKED_IMPORTS:
                        return False, f"脚本不允许通过 __import__ 导入: {node.args[0].value}"

            # 检查 eval / exec 调用
            if isinstance(func, ast.Name) and func.id in ("eval", "exec"):
                return False, f"脚本不允许使用 {func.id}"

            # 检查 getattr 动态获取危险属性
            if isinstance(func, ast.Name) and func.id == "getattr":
                return False, "脚本不允许使用 getattr（防止动态属性访问）"

            # 检查 vars / locals / globals（可访问内部属性）
            if isinstance(func, ast.Name) and func.id in ("vars", "locals", "globals", "dir", "type", "super"):
                return False, f"脚本不允许使用 {func.id}（防止内部属性访问）"

        # 检查字符串拼接绕过：__import__('o' + 's')
        if isinstance(node, ast.Call):
            func = node.func
            if isinstance(func, ast.Name) and func.id == "__import__":
                for arg in node.args:
                    if not isinstance(arg, ast.Constant):
                        return False, "脚本不允许通过动态表达式调用 __import__"

    return True, ""


def _log_audit(
    user_id: Optional[int],
    script_hash: str,
    success: bool,
    duration: float,
    error: Optional[str] = None,
    extra: Optional[dict] = None,
):
    """
    记录脚本执行审计日志

    Args:
        user_id: 执行用户 ID
        script_hash: 脚本内容哈希
        success: 执行是否成功
        duration: 执行耗时（秒）
        error: 错误信息
        extra: 附加信息
    """
    log_data = {
        "user_id": user_id,
        "script_hash": script_hash,
        "success": success,
        "duration_s": round(duration, 2),
    }
    if error:
        log_data["error"] = error[:500]
    if extra:
        log_data.update(extra)

    if success:
        logger.info("脚本执行完成", **log_data)
    else:
        logger.warning("脚本执行失败", **log_data)


def execute_script(
    script_content: str,
    user_id: Optional[int] = None,
    timeout: int = DEFAULT_TIMEOUT,
    work_dir: Optional[str] = None,
    env_extra: Optional[dict] = None,
    script_id: Optional[int] = None,
    script_type: str = "unknown",
) -> dict:
    """
    在沙箱中安全执行用户脚本

    流程：
    1. AST 静态检查脚本安全性
    2. 将脚本写入临时文件
    3. 通过 subprocess.run（禁止 shell=True）执行
    4. 记录审计日志

    Args:
        script_content: 用户脚本源代码
        user_id: 执行用户 ID（用于审计）
        timeout: 执行超时（秒），默认 300
        work_dir: 工作目录（自动创建临时目录）
        env_extra: 额外的环境变量
        script_id: 脚本 ID（用于审计）
        script_type: 脚本类型标识（web/perf/app）

    Returns:
        dict: {
            'success': bool,
            'return_code': int | None,
            'stdout': str,
            'stderr': str,
            'duration': float,
            'error': str | None,
            'script_hash': str,
        }
    """
    sandbox_mode = _get_sandbox_mode()
    script_hash = _compute_script_hash(script_content)
    start_time = time.time()

    # 步骤 1：AST 安全检查
    safe, reason = check_script_safety(script_content)
    if not safe:
        _log_audit(
            user_id=user_id,
            script_hash=script_hash,
            success=False,
            duration=0,
            error=f"脚本安全检查未通过: {reason}",
            extra={"script_id": script_id, "script_type": script_type, "blocked": True},
        )
        return {
            "success": False,
            "return_code": None,
            "stdout": "",
            "stderr": "",
            "duration": 0,
            "error": f"脚本安全检查未通过: {reason}",
            "script_hash": script_hash,
        }

    # 步骤 2：准备临时文件和工作目录
    created_temp_dir = False
    if work_dir is None:
        work_dir = tempfile.mkdtemp(prefix="sandbox_")
        created_temp_dir = True

    os.makedirs(work_dir, exist_ok=True)
    temp_file = None

    try:
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".py", delete=False, encoding="utf-8", dir=work_dir
        ) as f:
            f.write(script_content)
            temp_file = f.name

        # 步骤 3：构建安全的执行环境
        env = os.environ.copy()
        # 移除敏感环境变量
        for sensitive_key in ("SECRET_KEY", "JWT_SECRET_KEY", "DATABASE_URL", "REDIS_PASSWORD"):
            env.pop(sensitive_key, None)
        # 设置 PYTHONPATH
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        env["PYTHONPATH"] = project_root + os.pathsep + env.get("PYTHONPATH", "")
        # 追加额外环境变量
        if env_extra:
            env.update(env_extra)

        # 步骤 4：执行脚本
        if sandbox_mode == "docker":
            # Docker 模式（预留扩展点）
            logger.info("Docker 沙箱模式尚未实现，回退到 subprocess 模式")

        # subprocess 模式（默认）
        result = subprocess.run(
            [sys.executable, temp_file],
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=work_dir,
            env=env,
            # 禁止 shell=True（双重保障）
            shell=False,
        )

        duration = time.time() - start_time
        success = result.returncode == 0

        _log_audit(
            user_id=user_id,
            script_hash=script_hash,
            success=success,
            duration=duration,
            error=result.stderr[:500] if not success and result.stderr else None,
            extra={"script_id": script_id, "script_type": script_type},
        )

        return {
            "success": success,
            "return_code": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "duration": duration,
            "error": None if success else (result.stderr[:1000] or "执行失败"),
            "script_hash": script_hash,
        }

    except subprocess.TimeoutExpired:
        duration = time.time() - start_time
        _log_audit(
            user_id=user_id,
            script_hash=script_hash,
            success=False,
            duration=duration,
            error=f"执行超时（{timeout} 秒）",
            extra={"script_id": script_id, "script_type": script_type, "timeout": True},
        )
        return {
            "success": False,
            "return_code": None,
            "stdout": "",
            "stderr": "",
            "duration": duration,
            "error": f"执行超时（{timeout} 秒）",
            "script_hash": script_hash,
        }

    except Exception as e:
        duration = time.time() - start_time
        _log_audit(
            user_id=user_id,
            script_hash=script_hash,
            success=False,
            duration=duration,
            error=str(e),
            extra={"script_id": script_id, "script_type": script_type},
        )
        return {
            "success": False,
            "return_code": None,
            "stdout": "",
            "stderr": "",
            "duration": duration,
            "error": str(e),
            "script_hash": script_hash,
        }

    finally:
        # 清理临时文件
        if temp_file:
            try:
                os.unlink(temp_file)
            except OSError:
                pass
        # 清理临时目录（仅当由本函数创建时）
        if created_temp_dir and os.path.exists(work_dir):
            try:
                import shutil
                shutil.rmtree(work_dir, ignore_errors=True)
            except Exception:
                pass


# ─── SSRF 防护 ─────────────────────────────────────────────────────────────

# 内网 IP 段黑名单
BLOCKED_IP_RANGES = [
    ipaddress.ip_network("10.0.0.0/8"),
    ipaddress.ip_network("172.16.0.0/12"),
    ipaddress.ip_network("192.168.0.0/16"),
    ipaddress.ip_network("127.0.0.0/8"),
    ipaddress.ip_network("169.254.0.0/16"),  # 链路本地 / 云元数据
    ipaddress.ip_network("::1/128"),
    ipaddress.ip_network("fc00::/7"),
]


def validate_url_safety(url: str) -> tuple:
    """
    校验 URL 安全性，防止 SSRF 攻击

    Returns:
        (is_safe, message): (True, "") 安全；(False, "原因") 不安全
    """
    try:
        parsed = urlparse(url)
    except Exception:
        return False, "无效的 URL"

    # 仅允许 http/https
    if parsed.scheme not in ("http", "https"):
        return False, f"不允许的协议: {parsed.scheme}"

    hostname = parsed.hostname
    if not hostname:
        return False, "URL 缺少主机名"

    # 检查是否为 IP 地址
    try:
        ip = ipaddress.ip_address(hostname)
        for blocked in BLOCKED_IP_RANGES:
            if ip in blocked:
                return False, f"禁止访问内网/元数据地址: {hostname}"
    except ValueError:
        # 不是 IP 地址，是域名 — 检查常见内网域名
        blocked_domains = {"localhost", "metadata.google.internal", "169.254.169.254"}
        if hostname.lower() in blocked_domains:
            return False, f"禁止访问内网域名: {hostname}"

    return True, ""
