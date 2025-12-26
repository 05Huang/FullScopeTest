"""
JavaScript 脚本执行器

使用 Node.js 执行前置脚本和后置断言
支持 Postman 风格的 API (pm.test, pm.expect, pm.environment)
"""

import subprocess
import json
import time
import logging
from typing import Dict, Any, Optional, List

logger = logging.getLogger(__name__)


# Postman 风格的 JavaScript 沙箱代码（内嵌在执行器中）
# 注意：REQUEST/RESPONSE 初始化为空对象，后面会重新赋值
_PM_SANDBOX_JS = '''
// 初始化 REQUEST 和 RESPONSE（占位符，后面会重新赋值）
let REQUEST = {};
let RESPONSE = {};

// Postman 风格的沙箱环境
const pm = {
    environment: {
        get: (key) => ENV[key],
        set: (key, value) => { ENV_CHANGES[key] = value; },
        keys: () => Object.keys(ENV),
        clear: () => { ENV_CHANGES = {}; }
    },
    variables: {
        get: (key) => VARS[key],
        set: (key, value) => { VARS[key] = value; },
        clear: () => { VARS = {}; }
    }
};

// 定义 request 和 response 的 getter，带辅助方法
Object.defineProperty(pm, 'request', {
    get: () => REQUEST
});

Object.defineProperty(pm, 'response', {
    get: () => RESPONSE
});

// pm.test 函数（带属性存储断言）
pm.test = function(name, fn) {
    try {
        fn();
        pm.test._assertions.push({ name, passed: true, error: null });
    } catch (error) {
        pm.test._assertions.push({ name, passed: false, error: error.message });
    }
};
// 附加属性到函数对象
pm.test._assertions = [];

// pm.expect 链式断言（简化实现，核心功能）
class ExpectChain {
    constructor(actual) {
        this.actual = actual;
        this.isNot = false;
    }

    // to 和 be 返回自身以支持链式调用
    get to() {
        return this;
    }

    get be() {
        return this;
    }

    get not() {
        this.isNot = true;
        return this;
    }

    eql(expected) {
        const pass = this.isNot ? this.actual !== expected : this.actual === expected;
        if (!pass) {
            throw new Error(`expected ${JSON.stringify(this.actual)} ${this.isNot ? 'not ' : ''}to equal ${JSON.stringify(expected)}`);
        }
    }

    equal(expected) { return this.eql(expected); }

    exist() {
        const pass = this.isNot ? this.actual == null : this.actual != null;
        if (!pass) {
            throw new Error(`expected ${this.actual} ${this.isNot ? 'not ' : ''}to exist`);
        }
    }

    property(prop) {
        if (this.actual == null || typeof this.actual !== 'object') {
            throw new Error(`value is not an object`);
        }
        if (!this.isNot && !(prop in this.actual)) {
            throw new Error(`${JSON.stringify(this.actual)} does not have property '${prop}'`);
        }
        if (this.isNot && (prop in this.actual)) {
            throw new Error(`${JSON.stringify(this.actual)} has property '${prop}'`);
        }
        return new ExpectChain(this.actual[prop]);
    }

    have = { property: this.property.bind(this) };

    above(value) {
        const pass = this.isNot ? this.actual <= value : this.actual > value;
        if (!pass) {
            throw new Error(`expected ${this.actual} ${this.isNot ? 'not ' : ''}to be above ${value}`);
        }
    }

    below(value) {
        const pass = this.isNot ? this.actual >= value : this.actual < value;
        if (!pass) {
            throw new Error(`expected ${this.actual} ${this.isNot ? 'not ' : ''}to be below ${value}`);
        }
    }

    include(value) {
        const pass = this.isNot ? !String(this.actual).includes(value) : String(this.actual).includes(value);
        if (!pass) {
            throw new Error(`expected '${this.actual}' ${this.isNot ? 'not ' : ''}to include '${value}'`);
        }
    }

    contains(value) { return this.include(value); }

    a(type) {
        const jsType = (val) => Array.isArray(val) ? 'array' : typeof val;
        const actualType = jsType(this.actual);
        if (actualType !== type) {
            throw new Error(`expected ${actualType} to be ${type}`);
        }
    }

    an(type) { return this.a(type); }
}

pm.expect = (actual) => new ExpectChain(actual);

// 响应断言辅助 - 定义在 pm 上，避免 getter 问题
pm.assertResponse = (code) => {
    if (RESPONSE.status !== code) {
        throw new Error(`expected status ${RESPONSE.status} to equal ${code}`);
    }
};
'''


class JSExecutor:
    """JavaScript 脚本执行器"""

    def __init__(self, timeout: int = 3):
        """
        初始化执行器

        Args:
            timeout: 执行超时时间（秒）
        """
        self.timeout = timeout

    def _build_script(self, user_script: str, context: Dict[str, Any], is_post: bool = False) -> str:
        """
        构建完整的可执行脚本

        Args:
            user_script: 用户编写的脚本
            context: 执行上下文（包含 ENV, REQUEST, RESPONSE 等）
            is_post: 是否为后置脚本

        Returns:
            完整的 Node.js 可执行代码
        """
        # 序列化上下文数据
        env_json = json.dumps(context.get('environment', {}), ensure_ascii=False)
        vars_json = json.dumps(context.get('variables', {}), ensure_ascii=False)
        request_json = json.dumps(context.get('request', {}), ensure_ascii=False) if context.get('request') else '{}'
        response_json = json.dumps(context.get('response', {}), ensure_ascii=False) if context.get('response') else '{}'

        # 构建完整脚本
        full_script = f'''
// ==================== 内置沙箱环境 ====================
{_PM_SANDBOX_JS}

// ==================== 初始化上下文 ====================
const ENV = {env_json};
const ENV_CHANGES = {{}};
const VARS = {vars_json};
// 重新赋值 REQUEST 和 RESPONSE（已在沙箱中声明）
REQUEST = {request_json};
RESPONSE = {response_json};

// 为 RESPONSE 添加辅助方法（如果需要）
if (RESPONSE && typeof RESPONSE.body === 'object') {{
    RESPONSE.json = () => RESPONSE.body;
}} else if (RESPONSE && typeof RESPONSE.body === 'string') {{
    RESPONSE.json = () => JSON.parse(RESPONSE.body);
}}

// ==================== 用户脚本 ====================
try {{
    {user_script}
}} catch (error) {{
    console.error("Script Error:", error.message);
    throw error;
}}

// ==================== 输出结果 ====================
console.log("__RESULT_OUTPUT__");
console.log(JSON.stringify({{
    env_changes: ENV_CHANGES,
    variables: VARS,
    request_changes: REQUEST._changes || {{}},
    assertions: pm.test._assertions || []
}}));
'''
        return full_script

    def execute_pre_script(self, script: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        执行前置脚本

        Args:
            script: JavaScript 脚本代码
            context: 执行上下文
                - environment: 环境变量字典
                - variables: 临时变量字典
                - request: 请求对象 { method, url, headers, params, body }

        Returns:
            执行结果
                - passed: 是否成功
                - error: 错误信息（如果失败）
                - env_changes: 环境变量修改
                - request_changes: 请求修改
                - duration: 执行耗时(ms)
        """
        if not script or not script.strip():
            return {
                'passed': True,
                'executed': False,
                'message': '无前置脚本'
            }

        start_time = time.time()

        try:
            # 构建完整脚本
            full_script = self._build_script(script, context, is_post=False)

            # 执行脚本
            result = subprocess.run(
                ['node', '-e', full_script],
                capture_output=True,
                text=True,
                timeout=self.timeout,
                encoding='utf-8',
                errors='replace'  # 替换无法解码的字符
            )

            duration = (time.time() - start_time) * 1000

            # 检查执行是否成功
            if result.returncode != 0:
                error_msg = result.stderr or result.stdout or '未知错误'
                logger.warning(f"前置脚本执行失败: {error_msg}")
                return {
                    'executed': True,
                    'passed': False,
                    'error': self._extract_error_message(error_msg),
                    'duration': round(duration, 2)
                }

            # 解析输出结果
            output_data = self._parse_output(result.stdout)
            if not output_data:
                return {
                    'executed': True,
                    'passed': True,
                    'env_changes': {},
                    'request_changes': {},
                    'duration': round(duration, 2)
                }

            return {
                'executed': True,
                'passed': True,
                'env_changes': output_data.get('env_changes', {}),
                'variables': output_data.get('variables', {}),
                'request_changes': output_data.get('request_changes', {}),
                'duration': round(duration, 2)
            }

        except subprocess.TimeoutExpired:
            duration = (time.time() - start_time) * 1000
            logger.warning(f"前置脚本执行超时（{self.timeout}秒）")
            return {
                'executed': True,
                'passed': False,
                'error': f'脚本执行超时（超过 {self.timeout} 秒）',
                'duration': round(duration, 2)
            }
        except Exception as e:
            duration = (time.time() - start_time) * 1000
            logger.error(f"前置脚本执行异常: {str(e)}")
            return {
                'executed': True,
                'passed': False,
                'error': str(e),
                'duration': round(duration, 2)
            }

    def execute_post_script(self, script: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        执行后置断言脚本

        Args:
            script: JavaScript 脚本代码
            context: 执行上下文
                - environment: 环境变量字典
                - variables: 临时变量字典
                - response: 响应对象 { status, headers, body, responseTime }

        Returns:
            执行结果
                - passed: 是否通过（所有断言通过）
                - assertions: 断言结果列表
                - env_changes: 环境变量修改
                - error: 错误信息（如果失败）
                - duration: 执行耗时(ms)
        """
        if not script or not script.strip():
            return {
                'passed': True,
                'executed': False,
                'message': '无后置断言'
            }

        start_time = time.time()

        try:
            # 构建完整脚本
            full_script = self._build_script(script, context, is_post=True)

            # 执行脚本
            result = subprocess.run(
                ['node', '-e', full_script],
                capture_output=True,
                text=True,
                timeout=self.timeout,
                encoding='utf-8',
                errors='replace'
            )

            duration = (time.time() - start_time) * 1000

            # 检查执行是否成功
            if result.returncode != 0:
                error_msg = result.stderr or result.stdout or '未知错误'
                logger.warning(f"后置断言执行失败: {error_msg}")
                return {
                    'executed': True,
                    'passed': False,
                    'error': self._extract_error_message(error_msg),
                    'assertions': [],
                    'duration': round(duration, 2)
                }

            # 解析输出结果
            output_data = self._parse_output(result.stdout)
            if not output_data:
                return {
                    'executed': True,
                    'passed': True,
                    'assertions': [],
                    'env_changes': {},
                    'duration': round(duration, 2)
                }

            assertions = output_data.get('assertions', [])
            passed = all(a.get('passed', True) for a in assertions) if assertions else True

            return {
                'executed': True,
                'passed': passed,
                'assertions': {
                    'total': len(assertions),
                    'passed': sum(1 for a in assertions if a.get('passed', True)),
                    'failed': sum(1 for a in assertions if not a.get('passed', True)),
                    'details': assertions
                },
                'env_changes': output_data.get('env_changes', {}),
                'variables': output_data.get('variables', {}),
                'duration': round(duration, 2)
            }

        except subprocess.TimeoutExpired:
            duration = (time.time() - start_time) * 1000
            logger.warning(f"后置断言执行超时（{self.timeout}秒）")
            return {
                'executed': True,
                'passed': False,
                'error': f'脚本执行超时（超过 {self.timeout} 秒）',
                'assertions': [],
                'duration': round(duration, 2)
            }
        except Exception as e:
            duration = (time.time() - start_time) * 1000
            logger.error(f"后置断言执行异常: {str(e)}")
            return {
                'executed': True,
                'passed': False,
                'error': str(e),
                'assertions': [],
                'duration': round(duration, 2)
            }

    def _parse_output(self, stdout: str) -> Optional[Dict[str, Any]]:
        """
        解析脚本输出

        Args:
            stdout: Node.js 进程的标准输出

        Returns:
            解析后的结果字典，如果解析失败则返回 None
        """
        try:
            # 查找结果标记
            marker = "__RESULT_OUTPUT__"
            if marker not in stdout:
                logger.warning(f"脚本输出未找到结果标记")
                return None

            # 提取 JSON 部分
            parts = stdout.split(marker)
            if len(parts) < 2:
                return None

            json_str = parts[1].strip()
            return json.loads(json_str)

        except json.JSONDecodeError as e:
            logger.warning(f"解析脚本输出失败: {e}")
            return None
        except Exception as e:
            logger.error(f"解析输出异常: {e}")
            return None

    def _extract_error_message(self, error_output: str) -> str:
        """
        从错误输出中提取有意义的错误信息

        Args:
            error_output: 原始错误输出

        Returns:
            清理后的错误信息
        """
        # 移除 Node.js 的堆栈信息，只保留核心错误
        lines = error_output.split('\n')
        for line in lines:
            line = line.strip()
            if line and not line.startswith('at ') and not line.startswith('    ') and 'Error:' in line:
                # 提取错误描述
                if ':' in line:
                    return line.split(':', 1)[1].strip()

        # 如果没有找到，返回前 200 字符
        return error_output[:200] if len(error_output) > 200 else error_output


# 全局单例
_executor_instance = None


def get_executor(timeout: int = 3) -> JSExecutor:
    """获取执行器单例"""
    global _executor_instance
    if _executor_instance is None:
        _executor_instance = JSExecutor(timeout=timeout)
    return _executor_instance
