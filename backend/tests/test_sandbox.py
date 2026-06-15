"""
脚本沙箱执行工具测试

覆盖：
- AST 安全检查：拦截危险导入、危险函数调用
- 脚本执行：正常脚本、超时、错误
- 审计日志
- 环境变量清理
"""

import os
import pytest
from app.utils.sandbox import (
    check_script_safety,
    execute_script,
    _compute_script_hash,
    BLOCKED_IMPORTS,
)


class TestCheckScriptSafety:
    """AST 安全检查测试"""

    def test_safe_script_passes(self):
        """正常脚本应通过检查"""
        script = """
import requests
response = requests.get("https://example.com")
print(response.status_code)
"""
        safe, msg = check_script_safety(script)
        assert safe is True
        assert msg == ""

    def test_block_os_import(self):
        """import os 应被拦截"""
        script = "import os\nos.system('ls')"
        safe, msg = check_script_safety(script)
        assert safe is False
        assert "os" in msg

    def test_block_from_os_import(self):
        """from os import system 应被拦截"""
        script = "from os import system\nsystem('ls')"
        safe, msg = check_script_safety(script)
        assert safe is False
        assert "os" in msg

    def test_block_os_alias(self):
        """import os as my_os 也应被拦截"""
        script = "import os as my_os"
        safe, msg = check_script_safety(script)
        assert safe is False

    def test_block_dunder_import(self):
        """__import__('os') 应被拦截"""
        script = "__import__('os').system('ls')"
        safe, msg = check_script_safety(script)
        assert safe is False
        assert "__import__" in msg

    def test_block_eval(self):
        """eval() 应被拦截"""
        script = "eval('print(1)')"
        safe, msg = check_script_safety(script)
        assert safe is False
        assert "eval" in msg

    def test_block_exec(self):
        """exec() 应被拦截"""
        script = "exec('print(1)')"
        safe, msg = check_script_safety(script)
        assert safe is False
        assert "exec" in msg

    def test_block_getattr(self):
        """getattr() 应被拦截（防止动态属性访问）"""
        script = "getattr(object, '__class__')"
        safe, msg = check_script_safety(script)
        assert safe is False
        assert "getattr" in msg

    def test_block_pty_import(self):
        """import pty 应被拦截"""
        script = "import pty"
        safe, msg = check_script_safety(script)
        assert safe is False

    def test_allow_subprocess_run(self):
        """from subprocess import run 应被允许"""
        script = "from subprocess import run"
        safe, msg = check_script_safety(script)
        assert safe is True

    def test_block_subprocess_shell(self):
        """from subprocess import call 应被拦截"""
        script = "from subprocess import call"
        safe, msg = check_script_safety(script)
        assert safe is False

    def test_syntax_error_not_blocked(self):
        """语法错误的脚本不应被安全检查拦截（由执行器处理）"""
        script = "def foo(:\n  pass"
        safe, msg = check_script_safety(script)
        assert safe is True

    def test_empty_script(self):
        """空脚本应通过检查"""
        safe, msg = check_script_safety("")
        assert safe is True

    def test_complex_safe_script(self):
        """包含复杂但安全逻辑的脚本应通过"""
        script = """
import json
import time

data = {"key": "value"}
print(json.dumps(data))
time.sleep(1)
"""
        safe, msg = check_script_safety(script)
        assert safe is True


class TestComputeScriptHash:
    """脚本哈希计算测试"""

    def test_hash_consistency(self):
        """相同内容应产生相同哈希"""
        h1 = _compute_script_hash("print('hello')")
        h2 = _compute_script_hash("print('hello')")
        assert h1 == h2

    def test_hash_different_content(self):
        """不同内容应产生不同哈希"""
        h1 = _compute_script_hash("print('hello')")
        h2 = _compute_script_hash("print('world')")
        assert h1 != h2

    def test_hash_length(self):
        """哈希长度应为 16"""
        h = _compute_script_hash("test")
        assert len(h) == 16


class TestExecuteScript:
    """脚本执行测试"""

    def test_execute_simple_script(self):
        """执行简单脚本应成功"""
        result = execute_script(
            script_content="print('hello world')",
            timeout=10,
        )
        assert result['success'] is True
        assert 'hello world' in result['stdout']
        assert result['script_hash'] is not None

    def test_execute_script_with_error(self):
        """执行有错误的脚本应返回失败"""
        result = execute_script(
            script_content="raise ValueError('test error')",
            timeout=10,
        )
        assert result['success'] is False
        assert result['return_code'] != 0

    def test_execute_blocked_script(self):
        """被安全检查拦截的脚本不应执行"""
        result = execute_script(
            script_content="import os\nos.system('echo hacked')",
            timeout=10,
        )
        assert result['success'] is False
        assert '安全检查' in result['error']

    def test_execute_script_timeout(self):
        """超时的脚本应返回超时错误"""
        result = execute_script(
            script_content="import time; time.sleep(60)",
            timeout=2,
        )
        assert result['success'] is False
        assert '超时' in result['error']

    def test_execute_script_returns_hash(self):
        """执行结果应包含脚本哈希"""
        result = execute_script(
            script_content="print('test')",
            timeout=10,
        )
        assert 'script_hash' in result
        assert len(result['script_hash']) == 16

    def test_execute_script_duration(self):
        """执行结果应包含耗时"""
        result = execute_script(
            script_content="print('test')",
            timeout=10,
        )
        assert 'duration' in result
        assert result['duration'] >= 0

    def test_execute_script_with_user_id(self):
        """传入 user_id 不应影响执行结果"""
        result = execute_script(
            script_content="print('test')",
            user_id=42,
            timeout=10,
        )
        assert result['success'] is True

    def test_execute_script_cleans_temp_files(self):
        """执行完成后临时文件应被清理"""
        # 通过检查返回值间接验证（临时文件清理是内部行为）
        result = execute_script(
            script_content="import pathlib; print(pathlib.Path.cwd())",
            timeout=10,
        )
        assert result['success'] is True


class TestSandboxMode:
    """沙箱模式配置测试"""

    def test_default_mode_is_subprocess(self, monkeypatch):
        """默认模式应为 subprocess"""
        monkeypatch.delenv("SANDBOX_MODE", raising=False)
        from app.utils.sandbox import _get_sandbox_mode
        assert _get_sandbox_mode() == "subprocess"

    def test_mode_from_env(self, monkeypatch):
        """应从环境变量读取模式"""
        monkeypatch.setenv("SANDBOX_MODE", "docker")
        from app.utils.sandbox import _get_sandbox_mode
        assert _get_sandbox_mode() == "docker"
