"""
基于 OpenAPI/Swagger 的智能用例生成服务

解析 Swagger JSON/YAML，AI 分析每个接口的业务语义，
自动生成正常值、边界值、异常值测试用例。
"""

import json
import yaml
from typing import Dict, Any, List, Optional

from .base import AIServiceBase
from ...core.logging import get_logger

logger = get_logger(__name__)

# ---- 系统 Prompt ----

SWAGGER_CASE_GEN_SYSTEM_PROMPT = """\
You are an expert QA engineer specializing in API testing.
Given an OpenAPI/Swagger specification, you analyze each endpoint's business semantics
and generate comprehensive test cases.

For each API endpoint, generate test cases in these categories:
1. **Normal (happy path)**: Valid requests with correct parameters
2. **Boundary**: Edge cases for numeric/string parameters (min, max, empty, special chars)
3. **Error/Exception**: Invalid parameters, missing required fields, wrong types, unauthorized access

Output format: Return a JSON array of test case objects. Each object must have:
- "name": Descriptive test case name (Chinese)
- "description": What this test case validates (Chinese)
- "method": HTTP method (GET/POST/PUT/DELETE/PATCH)
- "url": The full request path (use {baseUrl} as placeholder for base URL)
- "headers": Object of request headers (include Content-Type for POST/PUT)
- "params": URL query parameters object (or empty {})
- "body": Request body object (or null for GET/DELETE)
- "body_type": "json" / "form" / null
- "expected_status": Expected HTTP status code (integer)
- "expected_contains": Array of strings that should appear in response body (optional)
- "priority": 1 (high) / 2 (medium) / 3 (low)
- "category": "normal" / "boundary" / "error"
- "tags": Array of tag strings for the endpoint

Rules:
- Generate at least 2 normal, 2 boundary, and 2 error test cases per endpoint
- For endpoints with path parameters, generate cases with valid, invalid, and missing values
- For POST/PUT endpoints, test with missing required fields, wrong types, and oversized data
- Use realistic sample values based on field names and descriptions
- Always return valid JSON only, no markdown code fences or explanations
"""


class SwaggerCaseGeneratorService(AIServiceBase):
    """基于 OpenAPI/Swagger 的智能用例生成服务"""

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        super().__init__(config=config)

    def parse_swagger(self, content: str, content_type: str = 'json') -> Dict[str, Any]:
        """
        解析 Swagger/OpenAPI 内容

        Args:
            content: Swagger JSON 或 YAML 字符串
            content_type: 'json' 或 'yaml'

        Returns:
            解析后的 OpenAPI 规范字典
        """
        try:
            if content_type == 'yaml':
                spec = yaml.safe_load(content)
            else:
                spec = json.loads(content)

            if not isinstance(spec, dict):
                raise ValueError('Swagger 内容不是一个有效的 JSON/YAML 对象')

            # 验证是否包含 paths
            if 'paths' not in spec:
                raise ValueError('Swagger 规范中未找到 paths 定义')

            return spec

        except json.JSONDecodeError as exc:
            raise ValueError(f'JSON 解析失败: {exc}')
        except yaml.YAMLError as exc:
            raise ValueError(f'YAML 解析失败: {exc}')

    def extract_endpoints(self, spec: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        从 OpenAPI 规范中提取所有接口信息

        Args:
            spec: OpenAPI 规范字典

        Returns:
            接口信息列表
        """
        endpoints = []
        paths = spec.get('paths', {})

        for path, path_item in paths.items():
            # 路径级别的公共参数
            common_params = path_item.get('parameters', [])

            for method in ['get', 'post', 'put', 'delete', 'patch', 'head', 'options']:
                operation = path_item.get(method)
                if not operation:
                    continue

                # 合并参数
                parameters = common_params + operation.get('parameters', [])

                endpoint = {
                    'method': method.upper(),
                    'path': path,
                    'operation_id': operation.get('operationId', ''),
                    'summary': operation.get('summary', ''),
                    'description': operation.get('description', ''),
                    'tags': operation.get('tags', []),
                    'parameters': self._extract_parameters(parameters, spec),
                    'request_body': self._extract_request_body(operation, spec),
                    'responses': self._extract_responses(operation, spec),
                    'required': operation.get('security', []),
                }
                endpoints.append(endpoint)

        return endpoints

    def generate_cases(
        self,
        swagger_content: str,
        content_type: str = 'json',
        *,
        user_id: Optional[int] = None,
        max_endpoints: int = 50,
    ) -> Dict[str, Any]:
        """
        基于 Swagger 生成测试用例

        Args:
            swagger_content: Swagger JSON/YAML 内容
            content_type: 'json' 或 'yaml'
            user_id: 调用用户 ID
            max_endpoints: 最多处理的接口数量

        Returns:
            dict: {
                'spec_info': {...},          # 规范基本信息
                'endpoints_count': int,       # 提取的接口数量
                'generated_cases': [...],     # 生成的测试用例
                'summary': {...},             # 统计摘要
            }
        """
        # 1. 解析 Swagger
        spec = self.parse_swagger(swagger_content, content_type)

        # 2. 提取接口
        endpoints = self.extract_endpoints(spec)
        if not endpoints:
            raise ValueError('Swagger 规范中未找到可用的 API 接口')

        # 限制处理数量
        if len(endpoints) > max_endpoints:
            logger.warning(
                'Swagger has too many endpoints, limiting',
                total=len(endpoints),
                max=max_endpoints,
            )
            endpoints = endpoints[:max_endpoints]

        # 3. 提取规范信息
        info = spec.get('info', {})
        spec_info = {
            'title': info.get('title', 'Unknown API'),
            'version': info.get('version', 'unknown'),
            'description': info.get('description', ''),
        }

        # 4. 分批调用 AI 生成用例
        all_cases = []
        batch_size = 10  # 每批处理的接口数

        for i in range(0, len(endpoints), batch_size):
            batch = endpoints[i:i + batch_size]
            batch_cases = self._generate_batch(
                batch, user_id=user_id, batch_index=i // batch_size + 1
            )
            all_cases.extend(batch_cases)

        # 5. 统计
        summary = {
            'total_cases': len(all_cases),
            'by_category': {
                'normal': sum(1 for c in all_cases if c.get('category') == 'normal'),
                'boundary': sum(1 for c in all_cases if c.get('category') == 'boundary'),
                'error': sum(1 for c in all_cases if c.get('category') == 'error'),
            },
            'by_method': {},
        }
        for case in all_cases:
            method = case.get('method', 'UNKNOWN')
            summary['by_method'][method] = summary['by_method'].get(method, 0) + 1

        return {
            'spec_info': spec_info,
            'endpoints_count': len(endpoints),
            'generated_cases': all_cases,
            'summary': summary,
        }

    def _generate_batch(
        self,
        endpoints: List[Dict[str, Any]],
        *,
        user_id: Optional[int] = None,
        batch_index: int = 1,
    ) -> List[Dict[str, Any]]:
        """调用 AI 为一批接口生成测试用例"""

        # 构造 prompt
        endpoint_descriptions = []
        for ep in endpoints:
            desc = self._format_endpoint_for_prompt(ep)
            endpoint_descriptions.append(desc)

        user_prompt = (
            f"Please generate test cases for the following {len(endpoints)} API endpoint(s):\n\n"
            + "\n---\n".join(endpoint_descriptions)
            + "\n\nReturn a JSON array containing test cases for ALL endpoints above."
        )

        messages = [
            {'role': 'user', 'content': user_prompt},
        ]

        response = self.simple_chat(
            messages,
            feature='swagger_gen',
            user_id=user_id,
            system_prompt=SWAGGER_CASE_GEN_SYSTEM_PROMPT,
            temperature=0.2,
        )

        content = self.get_content(response)
        cases = self._parse_cases_response(content)

        # 为每个 case 添加来源信息
        for case in cases:
            case['_batch_index'] = batch_index

        return cases

    def _format_endpoint_for_prompt(self, endpoint: Dict[str, Any]) -> str:
        """将接口信息格式化为 AI 可读的文本"""
        parts = [
            f"Method: {endpoint['method']}",
            f"Path: {endpoint['path']}",
        ]

        if endpoint.get('summary'):
            parts.append(f"Summary: {endpoint['summary']}")
        if endpoint.get('description'):
            parts.append(f"Description: {endpoint['description']}")
        if endpoint.get('tags'):
            parts.append(f"Tags: {', '.join(endpoint['tags'])}")

        # 参数
        params = endpoint.get('parameters', [])
        if params:
            param_strs = []
            for p in params:
                param_strs.append(
                    f"  - {p['name']} (in: {p['in']}, type: {p.get('type', 'string')}"
                    f"{', required' if p.get('required') else ''})"
                )
            parts.append("Parameters:\n" + "\n".join(param_strs))

        # 请求体
        req_body = endpoint.get('request_body')
        if req_body:
            parts.append(f"Request Body: {json.dumps(req_body, ensure_ascii=False)[:500]}")

        # 响应
        responses = endpoint.get('responses', {})
        if responses:
            resp_strs = []
            for code, desc in responses.items():
                resp_strs.append(f"  - {code}: {desc}")
            parts.append("Responses:\n" + "\n".join(resp_strs))

        return "\n".join(parts)

    def _parse_cases_response(self, content: str) -> List[Dict[str, Any]]:
        """解析 AI 返回的测试用例 JSON"""
        # 清理 markdown 代码块
        text = content.strip()
        if text.startswith('```json'):
            text = text[7:]
        elif text.startswith('```'):
            text = text[3:]
        if text.endswith('```'):
            text = text[:-3]
        text = text.strip()

        try:
            cases = json.loads(text)
        except json.JSONDecodeError:
            # 尝试找到 JSON 数组
            start = text.find('[')
            end = text.rfind(']')
            if start != -1 and end != -1 and end > start:
                try:
                    cases = json.loads(text[start:end + 1])
                except json.JSONDecodeError:
                    logger.error('Failed to parse AI response as JSON', content_preview=text[:200])
                    return []
            else:
                logger.error('No JSON array found in AI response', content_preview=text[:200])
                return []

        if not isinstance(cases, list):
            return [cases] if isinstance(cases, dict) else []

        # 验证每个 case 的必要字段
        valid_cases = []
        for case in cases:
            if isinstance(case, dict) and 'method' in case and 'url' in case:
                # 确保必要字段存在
                case.setdefault('name', f"{case['method']} {case['url']}")
                case.setdefault('description', '')
                case.setdefault('headers', {})
                case.setdefault('params', {})
                case.setdefault('body', None)
                case.setdefault('body_type', None)
                case.setdefault('expected_status', 200)
                case.setdefault('expected_contains', [])
                case.setdefault('priority', 2)
                case.setdefault('category', 'normal')
                case.setdefault('tags', [])
                valid_cases.append(case)

        return valid_cases

    def _extract_parameters(self, parameters: List[Dict], spec: Dict) -> List[Dict]:
        """提取并解析接口参数"""
        result = []
        for param in parameters:
            if '$ref' in param:
                param = self._resolve_ref(param['$ref'], spec)
            schema = param.get('schema', {})
            result.append({
                'name': param.get('name', ''),
                'in': param.get('in', 'query'),
                'required': param.get('required', False),
                'description': param.get('description', ''),
                'type': schema.get('type', param.get('type', 'string')),
                'schema': schema,
            })
        return result

    def _extract_request_body(self, operation: Dict, spec: Dict) -> Optional[Dict]:
        """提取请求体定义"""
        req_body = operation.get('requestBody')
        if not req_body:
            return None
        if '$ref' in req_body:
            req_body = self._resolve_ref(req_body['$ref'], spec)

        content_dict = req_body.get('content', {})
        json_content = content_dict.get('application/json', {})
        schema = json_content.get('schema', {})
        if '$ref' in schema:
            schema = self._resolve_ref(schema['$ref'], spec)

        return {
            'required': req_body.get('required', False),
            'schema': schema,
        }

    def _extract_responses(self, operation: Dict, spec: Dict) -> Dict[str, str]:
        """提取响应定义"""
        responses = {}
        for code, resp_def in operation.get('responses', {}).items():
            if '$ref' in resp_def:
                resp_def = self._resolve_ref(resp_def['$ref'], spec)
            desc = resp_def.get('description', '')
            responses[str(code)] = desc
        return responses

    def _resolve_ref(self, ref: str, spec: Dict) -> Dict:
        """解析 $ref 引用"""
        if not ref.startswith('#/'):
            return {}
        parts = ref[2:].split('/')
        current = spec
        for part in parts:
            if isinstance(current, dict):
                current = current.get(part, {})
            else:
                return {}
        return current if isinstance(current, dict) else {}


# 模块级单例
swagger_case_generator = SwaggerCaseGeneratorService()
