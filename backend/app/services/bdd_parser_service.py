"""
BDD/Gherkin 测试解析服务

支持用 Gherkin 语法编写测试场景，自动转换为可执行的 API 测试用例。
"""

import re
from typing import Dict, Any, List, Optional
from ..core.logging import get_logger

logger = get_logger(__name__)

# Gherkin 关键字映射
STEP_PATTERNS = [
    # Given 步骤
    (r'用户名\s*["\'](.+?)["\']\s*密码\s*["\'](.+?)["\']', 'setup_auth', {'username': 1, 'password': 2}),
    (r'请求头\s*["\'](.+?)["\']\s*为\s*["\'](.+?)["\']', 'set_header', {'name': 1, 'value': 2}),
    (r'基础URL为\s*["\'](.+?)["\']', 'set_base_url', {'base_url': 1}),

    # When 步骤
    (r'(GET|POST|PUT|DELETE|PATCH)\s+(.+)', 'send_request', {'method': 1, 'url': 2}),
    (r'发送\s*(GET|POST|PUT|DELETE|PATCH)\s*请求到\s*["\'](.+?)["\']', 'send_request', {'method': 1, 'url': 2}),
    (r'请求体为\s*["\'](.+?)["\']', 'set_body', {'body': 1}),
    (r'请求体为:', 'set_body_multiline', {}),

    # Then 步骤
    (r'状态码为\s*(\d+)', 'assert_status', {'status_code': 1}),
    (r'响应包含\s*["\'](.+?)["\']', 'assert_contains', {'text': 1}),
    (r'响应不包含\s*["\'](.+?)["\']', 'assert_not_contains', {'text': 1}),
    (r'响应字段\s*["\'](.+?)["\']\s*等于\s*["\'](.+?)["\']', 'assert_field_equals', {'path': 1, 'value': 2}),
    (r'响应字段\s*["\'](.+?)["\']\s*不为空', 'assert_field_not_empty', {'path': 1}),
    (r'响应时间小于\s*(\d+)\s*毫秒', 'assert_response_time', {'max_ms': 1}),
    (r'响应类型为\s*["\'](.+?)["\']', 'assert_content_type', {'content_type': 1}),
]


class BDDParserService:
    """BDD/Gherkin 解析服务"""

    def parse_gherkin(self, gherkin_text: str) -> Dict[str, Any]:
        """
        解析 Gherkin 文本为结构化场景

        Args:
            gherkin_text: Gherkin 格式的文本

        Returns:
            Dict: {feature, scenarios: [{name, steps, tags}]}
        """
        lines = gherkin_text.strip().split('\n')
        feature = {'name': '', 'description': '', 'scenarios': []}
        current_scenario = None
        current_step_type = None
        in_multiline = False
        multiline_content = []

        for line in lines:
            stripped = line.strip()

            # 跳过空行和注释
            if not stripped or stripped.startswith('#'):
                continue

            # Feature
            if stripped.startswith('Feature:'):
                feature['name'] = stripped[8:].strip()
                continue

            # Scenario
            if stripped.startswith('Scenario:') or stripped.startswith('场景:'):
                if current_scenario:
                    feature['scenarios'].append(current_scenario)
                name = stripped.split(':', 1)[1].strip()
                current_scenario = {'name': name, 'steps': [], 'tags': []}
                in_multiline = False
                continue

            # Tags
            if stripped.startswith('@'):
                if current_scenario:
                    current_scenario['tags'] = [t.strip() for t in stripped.split() if t.startswith('@')]
                continue

            # Given/When/Then/And
            step_match = re.match(r'^(Given|When|Then|And|But|假如|当|那么|而且|但是)\s+(.+)', stripped)
            if step_match:
                in_multiline = False
                keyword = step_match.group(1)
                text = step_match.group(2).strip()

                if keyword in ('Given', '假如'):
                    step_type = 'given'
                elif keyword in ('When', '当'):
                    step_type = 'when'
                elif keyword in ('Then', '那么'):
                    step_type = 'then'
                else:
                    step_type = current_step_type or 'given'
                current_step_type = step_type

                # 检查是否是多行体开始
                for pattern, action, params in STEP_PATTERNS:
                    if re.search(pattern, text):
                        if action == 'set_body_multiline':
                            in_multiline = True
                            multiline_content = []
                            current_scenario['steps'].append({
                                'type': step_type,
                                'action': action,
                                'params': {},
                                'raw': text,
                            })
                            break
                        else:
                            m = re.search(pattern, text)
                            extracted = {}
                            for key, idx in params.items():
                                extracted[key] = m.group(idx)
                            current_scenario['steps'].append({
                                'type': step_type,
                                'action': action,
                                'params': extracted,
                                'raw': text,
                            })
                            break
                else:
                    # 未匹配到模式，记录原始文本
                    if current_scenario:
                        current_scenario['steps'].append({
                            'type': step_type,
                            'action': 'raw',
                            'params': {'text': text},
                            'raw': text,
                        })
                continue

            # 多行体内容
            if in_multiline and stripped.startswith('"') and stripped.endswith('"'):
                multiline_content.append(stripped[1:-1])
                continue
            if in_multiline and stripped == '"""':
                in_multiline = False
                if current_scenario and current_scenario['steps']:
                    current_scenario['steps'][-1]['params']['body'] = '\n'.join(multiline_content)
                continue
            if in_multiline:
                multiline_content.append(stripped)
                continue

            # Feature 描述
            if not current_scenario and feature['name'] and not feature['description']:
                feature['description'] = stripped

        # 收尾
        if current_scenario:
            feature['scenarios'].append(current_scenario)

        logger.info('Gherkin 解析完成', feature=feature['name'], scenarios=len(feature['scenarios']))
        return feature

    def convert_to_test_cases(self, gherkin_text: str, project_id: Optional[int] = None) -> Dict[str, Any]:
        """
        将 Gherkin 文本转换为可执行的测试用例

        Args:
            gherkin_text: Gherkin 文本
            project_id: 项目 ID

        Returns:
            Dict: {cases: [...], feature_name}
        """
        feature = self.parse_gherkin(gherkin_text)
        cases = []

        for scenario in feature['scenarios']:
            case_data = self._scenario_to_case(scenario, project_id)
            if case_data:
                cases.append(case_data)

        return {
            'feature_name': feature['name'],
            'cases': cases,
            'total': len(cases),
        }

    def _scenario_to_case(self, scenario: Dict, project_id: Optional[int]) -> Optional[Dict[str, Any]]:
        """将单个场景转换为测试用例"""
        steps = scenario.get('steps', [])
        if not steps:
            return None

        # 提取请求信息
        method = 'GET'
        url = ''
        headers = {}
        body = None
        assertions = []
        pre_script = ''

        for step in steps:
            action = step.get('action', '')
            params = step.get('params', {})

            if action == 'send_request':
                method = params.get('method', 'GET')
                url = params.get('url', '')
            elif action == 'set_header':
                headers[params['name']] = params['value']
            elif action == 'set_body':
                body = params.get('body', '')
            elif action == 'set_body_multiline':
                body = params.get('body', '')
            elif action == 'assert_status':
                assertions.append({
                    'type': 'status_code',
                    'operator': 'equals',
                    'expected': int(params['status_code']),
                })
            elif action == 'assert_contains':
                assertions.append({
                    'type': 'body',
                    'operator': 'contains',
                    'expected': params['text'],
                })
            elif action == 'assert_field_equals':
                assertions.append({
                    'type': 'jsonpath',
                    'path': params['path'],
                    'operator': 'equals',
                    'expected': params['value'],
                })
            elif action == 'assert_field_not_empty':
                assertions.append({
                    'type': 'jsonpath',
                    'path': params['path'],
                    'operator': 'not_empty',
                })
            elif action == 'assert_response_time':
                assertions.append({
                    'type': 'response_time',
                    'operator': 'less_than',
                    'expected': int(params['max_ms']),
                })

        if not url:
            return None

        return {
            'name': scenario['name'],
            'method': method,
            'url': url,
            'headers': headers,
            'body': body,
            'body_type': 'json' if body and body.strip().startswith('{') else 'raw',
            'assertions': assertions,
            'description': f'BDD 场景: {scenario["name"]}',
            'project_id': project_id,
            'tags': scenario.get('tags', []),
        }


_instance = None


def get_bdd_parser_service() -> BDDParserService:
    global _instance
    if _instance is None:
        _instance = BDDParserService()
    return _instance
