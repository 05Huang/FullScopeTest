"""
HAR 文件导入服务

支持导入浏览器 DevTools 或 Charles/Fiddler 导出的 .har 文件，
自动解析 HTTP 请求并生成测试用例。
"""

import json
from typing import Dict, Any, List, Optional
from urllib.parse import urlparse, parse_qs
from ..extensions import db
from ..models.api_test_case import ApiTestCase, ApiTestCollection
from ..core.logging import get_logger
from ..utils.exceptions import ValidationError

logger = get_logger(__name__)


class HARImportService:
    """HAR 文件导入服务"""

    def parse_har(self, har_content: str, max_entries: int = 200) -> Dict[str, Any]:
        """
        解析 HAR 文件内容

        Args:
            har_content: HAR JSON 字符串
            max_entries: 最大解析条目数

        Returns:
            Dict: {entries: [...], summary: {...}}
        """
        try:
            har = json.loads(har_content)
        except json.JSONDecodeError:
            raise ValidationError('HAR 文件不是有效的 JSON')

        log = har.get('log', {})
        entries = log.get('entries', [])

        if not entries:
            raise ValidationError('HAR 文件中没有请求记录')

        parsed = []
        skipped = 0

        for entry in entries[:max_entries + skipped]:
            try:
                case_data = self._parse_entry(entry)
                if case_data:
                    parsed.append(case_data)
                else:
                    skipped += 1
            except Exception:
                skipped += 1

        # 统计信息
        methods = {}
        domains = set()
        for c in parsed:
            m = c.get('method', 'GET')
            methods[m] = methods.get(m, 0) + 1
            url = c.get('url', '')
            try:
                domains.add(urlparse(url).netloc)
            except Exception:
                pass

        logger.info('HAR 解析完成', total=len(entries), parsed=len(parsed), skipped=skipped)

        return {
            'entries': parsed,
            'summary': {
                'total_entries': len(entries),
                'parsed': len(parsed),
                'skipped': skipped,
                'methods': methods,
                'domains': list(domains),
            },
        }

    def import_to_collection(
        self,
        har_content: str,
        project_id: int,
        collection_id: Optional[int] = None,
        collection_name: str = 'HAR 导入',
        user_id: Optional[int] = None,
        max_entries: int = 200,
    ) -> Dict[str, Any]:
        """
        将 HAR 导入为用例集

        Args:
            har_content: HAR JSON 字符串
            project_id: 目标项目 ID
            collection_id: 目标集合 ID（为 None 则创建新集合）
            collection_name: 新集合名称
            user_id: 操作用户 ID
            max_entries: 最大导入条目数

        Returns:
            Dict: {collection_id, cases_count, skipped}
        """
        result = self.parse_har(har_content, max_entries)
        entries = result['entries']

        if not entries:
            return {'collection_id': None, 'cases_count': 0, 'skipped': 0, 'message': '无可导入的请求'}

        # 使用或创建集合
        if collection_id:
            collection = ApiTestCollection.query.get(collection_id)
            if not collection:
                raise ValidationError(f'集合 {collection_id} 不存在')
        else:
            collection = ApiTestCollection(
                name=collection_name,
                project_id=project_id,
                description=f'从 HAR 文件导入，共 {len(entries)} 个请求',
            )
            db.session.add(collection)
            db.session.flush()

        created = 0
        for entry in entries:
            try:
                case = ApiTestCase(
                    name=entry.get('name', f"{entry['method']} {entry['url']}")[:200],
                    method=entry['method'],
                    url=entry['url'],
                    headers=entry.get('headers', {}),
                    body=entry.get('body', ''),
                    body_type=entry.get('body_type', 'json'),
                    description=entry.get('description', ''),
                    collection_id=collection.id,
                    project_id=project_id,
                    priority=3,
                )
                db.session.add(case)
                created += 1
            except Exception as exc:
                logger.warning('导入用例失败', url=entry.get('url'), error=str(exc))

        db.session.commit()

        logger.info('HAR 导入完成', collection_id=collection.id, created=created)

        return {
            'collection_id': collection.id,
            'collection_name': collection.name,
            'cases_count': created,
            'skipped': result['summary']['skipped'],
            'summary': result['summary'],
        }

    def _parse_entry(self, entry: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """解析单个 HAR 条目"""
        request = entry.get('request', {})
        response = entry.get('response', {})

        method = request.get('method', 'GET').upper()

        # 跳过非 API 请求（静态资源、favicon 等）
        url = request.get('url', '')
        parsed_url = urlparse(url)
        path = parsed_url.path.lower()

        skip_extensions = ('.css', '.js', '.png', '.jpg', '.jpeg', '.gif', '.svg',
                           '.ico', '.woff', '.woff2', '.ttf', '.eot', '.map',
                           '.html', '.htm', '.xml', '.pdf')
        if any(path.endswith(ext) for ext in skip_extensions):
            return None

        # 跳过非 API 常见路径
        skip_paths = ('/favicon', '/assets/', '/static/', '/public/', '/__webpack')
        if any(p in path for p in skip_paths):
            return None

        # 解析 headers
        headers = {}
        for h in request.get('headers', []):
            name = h.get('name', '')
            value = h.get('value', '')
            # 跳过常见的动态 header
            skip_headers = ('cookie', 'host', 'connection', 'content-length',
                            'accept-encoding', 'user-agent', 'sec-ch-ua',
                            'sec-fetch', 'origin', 'referer')
            if name.lower() not in skip_headers:
                headers[name] = value

        # 解析 body
        body = ''
        body_type = 'json'
        post_data = request.get('postData', {})
        if post_data:
            body = post_data.get('text', '')
            mime = post_data.get('mimeType', '')
            if 'json' in mime:
                body_type = 'json'
            elif 'form' in mime:
                body_type = 'form'
            elif 'xml' in mime:
                body_type = 'xml'
            else:
                body_type = 'raw'

        # 构建完整 URL（不含 query 参数）
        base_url = f"{parsed_url.scheme}://{parsed_url.netloc}{parsed_url.path}"

        # 构建名称
        status = response.get('status', 0)
        name = f"[{method}] {parsed_url.path}"
        if len(name) > 100:
            # 截断长路径
            parts = parsed_url.path.split('/')
            name = f"[{method}] .../{'/'.join(parts[-3:])}"

        return {
            'name': name[:200],
            'method': method,
            'url': base_url,
            'headers': headers,
            'body': body,
            'body_type': body_type,
            'description': f'从 HAR 导入 (HTTP {status})',
        }


_instance = None


def get_har_import_service() -> HARImportService:
    global _instance
    if _instance is None:
        _instance = HARImportService()
    return _instance
