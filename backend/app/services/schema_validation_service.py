"""
API Schema 校验服务

导入 OpenAPI/Swagger Schema 后，校验 API 响应是否符合 Schema。
校验结果标记为 warning（不影响 pass/fail），但可在质量门禁中配置为阻断条件。
"""

import json
import re
from typing import Dict, Any, List, Optional
from ..extensions import db
from ..core.logging import get_logger

logger = get_logger(__name__)


class SchemaValidationService:
    """API Schema 校验服务"""

    def validate_response(
        self,
        schema: Dict[str, Any],
        response_body: str,
        status_code: int = 200,
    ) -> Dict[str, Any]:
        """
        校验响应是否符合 Schema

        Args:
            schema: JSON Schema 定义
            response_body: 响应体字符串
            status_code: 响应状态码

        Returns:
            Dict: {valid, errors, warnings, summary}
        """
        try:
            body = json.loads(response_body) if response_body else None
        except json.JSONDecodeError:
            return {
                'valid': False,
                'errors': [{'path': '/', 'message': '响应体不是有效的 JSON', 'type': 'json_parse'}],
                'warnings': [],
                'summary': 'JSON 解析失败',
            }

        errors = []
        warnings = []

        # 校验状态码
        if 'responses' in schema:
            expected_codes = schema['responses']
            if str(status_code) not in expected_codes and 'default' not in expected_codes:
                warnings.append({
                    'path': 'status_code',
                    'message': f'状态码 {status_code} 不在 Schema 定义的响应中',
                    'type': 'status_code',
                })

        # 校验响应体结构
        if body is not None and 'properties' in schema:
            self._validate_object(body, schema, '', errors, warnings)
        elif body is not None and 'type' in schema:
            self._validate_type(body, schema, '', errors, warnings)

        valid = len(errors) == 0
        total = len(errors) + len(warnings)

        return {
            'valid': valid,
            'errors': errors,
            'warnings': warnings,
            'summary': f'校验完成：{len(errors)} 个错误，{len(warnings)} 个警告',
            'total_issues': total,
        }

    def generate_schema_from_response(
        self,
        response_body: str,
        max_depth: int = 5,
    ) -> Dict[str, Any]:
        """
        从实际 API 响应自动生成 JSON Schema

        Args:
            response_body: 响应体字符串
            max_depth: 最大递归深度

        Returns:
            Dict: JSON Schema
        """
        try:
            body = json.loads(response_body) if response_body else None
        except json.JSONDecodeError:
            return {'type': 'string', 'description': '非 JSON 响应'}

        if body is None:
            return {'type': 'null'}

        return self._infer_schema(body, max_depth, 0)

    def merge_schemas(self, schemas: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        合并多个响应的 Schema（取并集）

        Args:
            schemas: 多个 JSON Schema

        Returns:
            合并后的 Schema
        """
        if not schemas:
            return {'type': 'object'}
        if len(schemas) == 1:
            return schemas[0]

        merged = schemas[0]
        for s in schemas[1:]:
            merged = self._merge_two(merged, s)
        return merged

    # ==================== 内部方法 ====================

    def _validate_object(
        self,
        value: Any,
        schema: Dict[str, Any],
        path: str,
        errors: List[Dict],
        warnings: List[Dict],
    ) -> None:
        """校验对象类型"""
        if not isinstance(value, dict):
            errors.append({'path': path or '/', 'message': f'期望 object，实际 {type(value).__name__}', 'type': 'type'})
            return

        properties = schema.get('properties', {})
        required = schema.get('required', [])

        # 检查必填字段
        for field in required:
            if field not in value:
                errors.append({
                    'path': f'{path}.{field}',
                    'message': f'缺少必填字段: {field}',
                    'type': 'required',
                })

        # 检查各字段类型
        for field, field_schema in properties.items():
            if field in value:
                self._validate_type(
                    value[field], field_schema, f'{path}.{field}', errors, warnings
                )

        # 检查额外字段
        extra = set(value.keys()) - set(properties.keys())
        if extra and schema.get('additionalProperties') is False:
            for f in extra:
                warnings.append({
                    'path': f'{path}.{f}',
                    'message': f'未知字段: {f}',
                    'type': 'additional_property',
                })

    def _validate_type(
        self,
        value: Any,
        schema: Dict[str, Any],
        path: str,
        errors: List[Dict],
        warnings: List[Dict],
    ) -> None:
        """校验字段类型"""
        expected_type = schema.get('type')
        if not expected_type:
            return

        # null 检查
        if value is None:
            if expected_type != 'null':
                warnings.append({'path': path, 'message': f'值为 null，期望 {expected_type}', 'type': 'null'})
            return

        type_map = {
            'string': str,
            'integer': int,
            'number': (int, float),
            'boolean': bool,
            'array': list,
            'object': dict,
        }

        expected_py = type_map.get(expected_type)
        if expected_py and not isinstance(value, expected_py):
            errors.append({
                'path': path,
                'message': f'期望 {expected_type}，实际 {type(value).__name__}',
                'type': 'type',
            })
            return

        # 递归校验数组元素
        if expected_type == 'array' and isinstance(value, list) and 'items' in schema:
            for i, item in enumerate(value[:10]):  # 最多校验前 10 个元素
                self._validate_type(item, schema['items'], f'{path}[{i}]', errors, warnings)

        # 递归校验对象
        if expected_type == 'object' and isinstance(value, dict):
            self._validate_object(value, schema, path, errors, warnings)

        # 字符串格式校验
        if expected_type == 'string' and isinstance(value, str):
            fmt = schema.get('format')
            if fmt == 'email' and '@' not in value:
                warnings.append({'path': path, 'message': '不是有效的 email 格式', 'type': 'format'})
            elif fmt == 'uri' and not value.startswith(('http://', 'https://')):
                warnings.append({'path': path, 'message': '不是有效的 URI 格式', 'type': 'format'})
            elif fmt == 'date' and not re.match(r'\d{4}-\d{2}-\d{2}', value):
                warnings.append({'path': path, 'message': '不是有效的 date 格式 (YYYY-MM-DD)', 'type': 'format'})

    def _infer_schema(self, value: Any, max_depth: int, current_depth: int) -> Dict[str, Any]:
        """推断单个值的 Schema"""
        if value is None:
            return {'type': 'null'}
        if isinstance(value, bool):
            return {'type': 'boolean'}
        if isinstance(value, int):
            return {'type': 'integer'}
        if isinstance(value, float):
            return {'type': 'number'}
        if isinstance(value, str):
            schema: Dict[str, Any] = {'type': 'string'}
            if re.match(r'\d{4}-\d{2}-\d{2}T', value):
                schema['format'] = 'date-time'
            elif re.match(r'\d{4}-\d{2}-\d{2}$', value):
                schema['format'] = 'date'
            elif '@' in value:
                schema['format'] = 'email'
            return schema
        if isinstance(value, list):
            if not value:
                return {'type': 'array', 'items': {}}
            if current_depth >= max_depth:
                return {'type': 'array'}
            # 推断每个元素的 Schema 并合并
            item_schemas = [self._infer_schema(item, max_depth, current_depth + 1) for item in value[:5]]
            merged = item_schemas[0]
            for s in item_schemas[1:]:
                merged = self._merge_two(merged, s)
            return {'type': 'array', 'items': merged}
        if isinstance(value, dict):
            if current_depth >= max_depth:
                return {'type': 'object'}
            properties = {}
            required = []
            for k, v in value.items():
                properties[k] = self._infer_schema(v, max_depth, current_depth + 1)
                if v is not None:
                    required.append(k)
            result: Dict[str, Any] = {'type': 'object', 'properties': properties}
            if required:
                result['required'] = required
            return result
        return {'type': 'string'}

    def _merge_two(self, a: Dict[str, Any], b: Dict[str, Any]) -> Dict[str, Any]:
        """合并两个 Schema"""
        if a.get('type') != b.get('type'):
            return {'type': 'string'}  # 类型不同则降级为 string
        t = a.get('type')
        if t == 'object':
            props = {**(a.get('properties') or {}), **(b.get('properties') or {})}
            for k, v in props.items():
                if k in (a.get('properties') or {}) and k in (b.get('properties') or {}):
                    props[k] = self._merge_two(a['properties'][k], b['properties'][k])
            return {'type': 'object', 'properties': props}
        if t == 'array':
            items_a = a.get('items', {})
            items_b = b.get('items', {})
            return {'type': 'array', 'items': self._merge_two(items_a, items_b)}
        return a


_instance = None


def get_schema_validation_service() -> SchemaValidationService:
    global _instance
    if _instance is None:
        _instance = SchemaValidationService()
    return _instance
