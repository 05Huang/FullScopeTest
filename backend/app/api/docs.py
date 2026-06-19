"""
测试文档模块 - API

实现测试文档相关功能：文档 CRUD、分类、导出
"""

from flask import request, send_file
from flask_jwt_extended import jwt_required
from datetime import datetime, timezone
import tempfile
import markdown

from . import api_bp
from ..extensions import db
from ..models.test_document import TestDocument
from ..models.project import Project
from ..utils.response import success_response, error_response, paginate_response
from ..utils.validators import validate_json
from ..utils import get_current_user_id


@api_bp.route('/docs/health', methods=['GET'])
def docs_health():
    """文档模块健康检查"""
    return success_response(message='文档模块正常')


# ==================== 文档管理 ====================

@api_bp.route('/projects/<int:project_id>/docs', methods=['GET'])
@jwt_required()
def get_documents(project_id):
    """
    获取项目文档列表
    
    查询参数:
        category: 分类筛选
        keyword: 搜索关键词
        page: 页码
        per_page: 每页数量
    """
    user_id = get_current_user_id()
    
    # 验证项目权限
    project = Project.query.filter_by(id=project_id, owner_id=user_id).first()
    if not project:
        return error_response(404, '项目不存在')
    
    # 获取查询参数
    category = request.args.get('category')
    keyword = request.args.get('keyword', '').strip()
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    
    # 构建查询
    query = TestDocument.query.filter_by(project_id=project_id)
    
    if category:
        query = query.filter_by(category=category)
    if keyword:
        query = query.filter(
            db.or_(
                TestDocument.title.ilike(f'%{keyword}%'),
                TestDocument.content.ilike(f'%{keyword}%')
            )
        )
    
    # 分页
    pagination = query.order_by(TestDocument.updated_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    return paginate_response(
        items=[d.to_dict() for d in pagination.items],
        total=pagination.total,
        page=page,
        per_page=per_page
    )


@api_bp.route('/projects/<int:project_id>/docs', methods=['POST'])
@jwt_required()
@validate_json('title')
def create_document(project_id):
    """
    创建文档
    
    请求体:
        title: 文档标题
        content: 文档内容 (Markdown)
        category: 分类 (test_plan/test_case/test_report/other)
        tags: 标签列表
    """
    user_id = get_current_user_id()
    
    # 验证项目权限
    project = Project.query.filter_by(id=project_id, owner_id=user_id).first()
    if not project:
        return error_response(404, '项目不存在')
    
    data = request.get_json()
    
    title = data['title'].strip()
    if len(title) < 1 or len(title) > 255:
        return error_response(400, '文档标题长度应为 1-255 个字符')
    
    doc = TestDocument(
        project_id=project_id,
        title=title,
        content=data.get('content', ''),
        category=data.get('category', 'other'),
        tags=data.get('tags', []),
        created_by=user_id,
        updated_by=user_id
    )
    
    db.session.add(doc)
    db.session.commit()
    
    return success_response(data=doc.to_dict(), message='创建成功', code=201)


@api_bp.route('/docs/<int:doc_id>', methods=['GET'])
@jwt_required()
def get_document(doc_id):
    """获取文档详情"""
    user_id = get_current_user_id()
    
    doc = db.session.query(TestDocument).join(
        Project, TestDocument.project_id == Project.id
    ).filter(
        TestDocument.id == doc_id,
        Project.owner_id == user_id
    ).first()
    
    if not doc:
        return error_response(404, '文档不存在')
    
    return success_response(data=doc.to_dict())


@api_bp.route('/docs/<int:doc_id>', methods=['PUT'])
@jwt_required()
def update_document(doc_id):
    """更新文档"""
    user_id = get_current_user_id()
    
    doc = db.session.query(TestDocument).join(
        Project, TestDocument.project_id == Project.id
    ).filter(
        TestDocument.id == doc_id,
        Project.owner_id == user_id
    ).first()
    
    if not doc:
        return error_response(404, '文档不存在')
    
    data = request.get_json()
    
    # 更新字段
    if 'title' in data:
        title = data['title'].strip()
        if len(title) < 1 or len(title) > 255:
            return error_response(400, '文档标题长度应为 1-255 个字符')
        doc.title = title
    
    if 'content' in data:
        doc.content = data['content']
    
    if 'category' in data:
        doc.category = data['category']
    
    if 'tags' in data:
        doc.tags = data['tags']
    
    if 'is_published' in data:
        doc.is_published = data['is_published']
    
    if 'version' in data:
        doc.version = data['version']
    
    doc.updated_by = user_id
    doc.updated_at = datetime.now(timezone.utc).replace(tzinfo=None)
    
    db.session.commit()
    
    return success_response(data=doc.to_dict(), message='更新成功')


@api_bp.route('/docs/<int:doc_id>', methods=['DELETE'])
@jwt_required()
def delete_document(doc_id):
    """删除文档"""
    user_id = get_current_user_id()
    
    doc = db.session.query(TestDocument).join(
        Project, TestDocument.project_id == Project.id
    ).filter(
        TestDocument.id == doc_id,
        Project.owner_id == user_id
    ).first()
    
    if not doc:
        return error_response(404, '文档不存在')
    
    db.session.delete(doc)
    db.session.commit()
    
    return success_response(message='删除成功')


# ==================== 文档分类 ====================

@api_bp.route('/docs/categories', methods=['GET'])
@jwt_required()
def get_document_categories():
    """获取文档分类列表"""
    categories = [
        {'value': 'test_plan', 'label': '测试计划', 'icon': '📋'},
        {'value': 'test_case', 'label': '测试用例', 'icon': '📝'},
        {'value': 'test_report', 'label': '测试报告', 'icon': '📊'},
        {'value': 'api_doc', 'label': '接口文档', 'icon': '📡'},
        {'value': 'design', 'label': '设计文档', 'icon': '🎨'},
        {'value': 'other', 'label': '其他', 'icon': '📄'}
    ]
    return success_response(data=categories)


# ==================== 文档导出 ====================

@api_bp.route('/docs/<int:doc_id>/export', methods=['GET'])
@jwt_required()
def export_document(doc_id):
    """
    导出文档
    
    查询参数:
        format: 导出格式 (md/html)
    """
    user_id = get_current_user_id()
    export_format = request.args.get('format', 'md')
    
    doc = db.session.query(TestDocument).join(
        Project, TestDocument.project_id == Project.id
    ).filter(
        TestDocument.id == doc_id,
        Project.owner_id == user_id
    ).first()
    
    if not doc:
        return error_response(404, '文档不存在')
    
    if export_format == 'md':
        # 导出 Markdown 格式
        content = f"# {doc.title}\n\n{doc.content or ''}"
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False, encoding='utf-8') as f:
            f.write(content)
            temp_path = f.name
        
        return send_file(
            temp_path,
            mimetype='text/markdown',
            as_attachment=True,
            download_name=f'{doc.title}.md'
        )
    
    elif export_format == 'html':
        # 导出 HTML 格式
        html_content = generate_doc_html(doc)
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False, encoding='utf-8') as f:
            f.write(html_content)
            temp_path = f.name
        
        return send_file(
            temp_path,
            mimetype='text/html',
            as_attachment=True,
            download_name=f'{doc.title}.html'
        )
    
    else:
        return error_response(400, '不支持的导出格式')


def generate_doc_html(doc):
    """生成文档 HTML"""
    # 将 Markdown 转换为 HTML
    try:
        content_html = markdown.markdown(doc.content or '', extensions=['tables', 'fenced_code'])
    except Exception:
        content_html = doc.content or ''
    
    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{doc.title}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif; line-height: 1.6; color: #333; max-width: 900px; margin: 0 auto; padding: 40px 20px; }}
        h1 {{ font-size: 2.5em; margin-bottom: 10px; color: #1a1a1a; border-bottom: 2px solid #667eea; padding-bottom: 10px; }}
        h2 {{ font-size: 1.8em; margin-top: 30px; margin-bottom: 15px; color: #333; }}
        h3 {{ font-size: 1.4em; margin-top: 25px; margin-bottom: 10px; color: #444; }}
        p {{ margin: 15px 0; }}
        code {{ background: #f4f4f4; padding: 2px 6px; border-radius: 4px; font-family: 'Consolas', 'Monaco', monospace; }}
        pre {{ background: #2d2d2d; color: #f8f8f2; padding: 15px; border-radius: 8px; overflow-x: auto; margin: 15px 0; }}
        pre code {{ background: none; padding: 0; }}
        table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
        th, td {{ padding: 12px; text-align: left; border: 1px solid #ddd; }}
        th {{ background: #f5f5f5; font-weight: 600; }}
        ul, ol {{ margin: 15px 0; padding-left: 30px; }}
        li {{ margin: 5px 0; }}
        blockquote {{ border-left: 4px solid #667eea; padding-left: 20px; margin: 20px 0; color: #666; font-style: italic; }}
        .meta {{ color: #999; font-size: 14px; margin-bottom: 30px; }}
        .tags {{ margin-top: 5px; }}
        .tag {{ display: inline-block; background: #e8e8e8; padding: 2px 8px; border-radius: 4px; margin-right: 5px; font-size: 12px; }}
    </style>
</head>
<body>
    <h1>{doc.title}</h1>
    <div class="meta">
        <div>分类: {doc.category} | 版本: {doc.version} | 更新时间: {doc.updated_at.strftime('%Y-%m-%d %H:%M') if doc.updated_at else '-'}</div>
        <div class="tags">
            {''.join([f'<span class="tag">{tag}</span>' for tag in (doc.tags or [])])}
        </div>
    </div>
    <div class="content">
        {content_html}
    </div>
</body>
</html>'''
    
    return html


# ==================== 文档模板 ====================

@api_bp.route('/docs/templates', methods=['GET'])
@jwt_required()
def get_document_templates():
    """获取文档模板列表"""
    templates = [
        {
            'id': 'test_plan',
            'name': '测试计划模板',
            'category': 'test_plan',
            'content': '''# 测试计划

## 1. 项目概述

### 1.1 项目背景
[描述项目背景和测试目的]

### 1.2 测试范围
[描述测试覆盖的功能模块]

## 2. 测试策略

### 2.1 测试类型
- 功能测试
- 接口测试
- 性能测试
- 安全测试

### 2.2 测试环境
| 环境 | 地址 | 说明 |
|------|------|------|
| 开发环境 | | |
| 测试环境 | | |
| 预发环境 | | |

## 3. 测试进度

### 3.1 里程碑
| 阶段 | 开始时间 | 结束时间 | 负责人 |
|------|----------|----------|--------|
| 测试准备 | | | |
| 功能测试 | | | |
| 回归测试 | | | |

## 4. 风险与应对
[描述可能的风险及应对措施]

## 5. 交付物
- 测试用例
- 测试报告
- Bug 列表
'''
        },
        {
            'id': 'test_case',
            'name': '测试用例模板',
            'category': 'test_case',
            'content': '''# 测试用例设计

## 模块名称
[填写模块名称]

## 测试用例

### TC-001: [用例名称]

**前置条件：**
- [条件1]
- [条件2]

**测试步骤：**
1. [步骤1]
2. [步骤2]
3. [步骤3]

**预期结果：**
- [预期1]
- [预期2]

**测试数据：**
```json
{
  "key": "value"
}
```

---

### TC-002: [用例名称]

**前置条件：**
- 

**测试步骤：**
1. 

**预期结果：**
- 

'''
        },
        {
            'id': 'api_doc',
            'name': '接口文档模板',
            'category': 'api_doc',
            'content': '''# 接口文档

## 基本信息
- 接口名称：
- 接口地址：
- 请求方式：GET/POST/PUT/DELETE
- Content-Type：application/json

## 请求参数

### Headers
| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| Authorization | string | 是 | Bearer Token |

### Body
| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| | | | |

### 请求示例
```json
{
  
}
```

## 响应参数

| 参数名 | 类型 | 说明 |
|--------|------|------|
| code | int | 状态码 |
| message | string | 提示信息 |
| data | object | 数据 |

### 响应示例
```json
{
  "code": 200,
  "message": "success",
  "data": {}
}
```

## 错误码
| 错误码 | 说明 |
|--------|------|
| 400 | 请求参数错误 |
| 401 | 未授权 |
| 404 | 资源不存在 |
| 500 | 服务器错误 |
'''
        }
    ]
    
    return success_response(data=templates)


