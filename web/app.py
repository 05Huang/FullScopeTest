"""
接口测试平台 - Flask 后端服务

项目描述：
    提供 Web 界面进行 HTTP 接口测试，支持多环境配置、请求模板、
    自动化测试执行等功能。参考 Postman 设计，基于 Flask + Vue.js。

主要功能：
    1. 环境管理 - 支持多环境配置（开发、测试、生产等）
    2. 集合管理 - 组织和分组管理 API 请求
    3. 请求编辑 - Postman 风格的请求编辑器
    4. 响应预览 - 实时显示 API 响应结果
    5. 自动化测试 - 集成 Pytest 框架
    6. 报告生成 - 使用 Allure 生成美观的测试报告

作者：学习项目
版本：v1.0
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import os
import json
import subprocess
from datetime import datetime
import sys
import yaml  # 用于加载 config.yaml

# 添加项目根目录到 Python 路径（便于导入 common 模块）
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 导入工具类
from common.request_util import RequestUtil
from common.logger_util import LoggerUtil

# 初始化日志记录器
logger = LoggerUtil.get_logger("web_app")

logger.info("="*60)
logger.info("🚀 启动接口测试平台后端服务")
logger.info("="*60)

# ============= Flask 应用初始化 =============

app = Flask(__name__, static_folder='static', static_url_path='/static')
CORS(app)  # 启用跨域资源共享 (CORS)

# 配置数据库
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./test_cases.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# ============= 数据库模型 (ORM) =============
# 使用 SQLAlchemy ORM 定义数据模型
# 优点：
# - 数据库独立性：可以轻松从 SQLite 迁移到 PostgreSQL 等
# - 安全性：自动防止 SQL 注入
# - 关系管理：自动处理外键和级联删除

class Environment(db.Model):
    """
    环境配置表
    
    用途：存储多环境配置（开发、测试、生产等）
    每个环境包含：Base URL、请求头、自定义变量等
    
    属性：
        id: 环境 ID（主键）
        name: 环境名称（唯一）
        base_url: API 基础 URL（如 https://api.example.com）
        headers: 环境默认请求头（JSON 格式）
        variables: 环境变量（JSON 格式，用于 {{var}} 替换）
        created_at: 创建时间
    """
    __tablename__ = 'environments'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True, comment='环境名称')
    base_url = db.Column(db.String(255), nullable=False, comment='API 基础 URL')
    headers = db.Column(db.Text, default='{}', comment='环境请求头（JSON）')
    variables = db.Column(db.Text, default='{}', comment='环境变量（JSON）')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # 关系：一个环境对应多个集合
    collections = db.relationship('TestCollection', backref='environment', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        """转换为字典（便于 JSON 序列化）"""
        return {
            'id': self.id,
            'name': self.name,
            'base_url': self.base_url,
            'headers': json.loads(self.headers) if isinstance(self.headers, str) else self.headers,
            'variables': json.loads(self.variables) if isinstance(self.variables, str) else self.variables,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class TestCollection(db.Model):
    """
    测试集合表
    
    用途：组织和分组管理相关的 API 请求
    例如：用户管理 API、订单管理 API 等集合
    
    属性：
        id: 集合 ID（主键）
        env_id: 所属环境 ID（外键）
        name: 集合名称
        description: 集合描述
        created_at: 创建时间
        updated_at: 更新时间
    """
    __tablename__ = 'test_collections'
    
    id = db.Column(db.Integer, primary_key=True)
    env_id = db.Column(db.Integer, db.ForeignKey('environments.id'), nullable=False)
    name = db.Column(db.String(255), nullable=False, comment='集合名称')
    description = db.Column(db.String(500), comment='集合描述')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关系：一个集合对应多个请求
    requests = db.relationship('TestRequest', backref='collection', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        """转换为字典（便于 JSON 序列化）"""
        return {
            'id': self.id,
            'env_id': self.env_id,
            'name': self.name,
            'description': self.description,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'request_count': len(self.requests) if self.requests else 0
        }


class TestRequest(db.Model):
    """
    单个 HTTP 请求表
    
    用途：存储单个 HTTP 请求的详细信息
    包括：URL、方法、请求头、请求体、预期响应等
    
    属性：
        id: 请求 ID（主键）
        collection_id: 所属集合 ID（外键）
        name: 请求名称
        method: HTTP 方法 (GET, POST, PUT, DELETE, PATCH)
        url: 完整 URL（支持 {{base_url}} 和其他环境变量）
        headers: 请求头（JSON）
        body: 请求体（JSON）
        params: URL 查询参数（JSON）
        created_at: 创建时间
        updated_at: 更新时间
    """
    __tablename__ = 'test_requests'
    
    id = db.Column(db.Integer, primary_key=True)
    collection_id = db.Column(db.Integer, db.ForeignKey('test_collections.id'), nullable=False)
    name = db.Column(db.String(255), nullable=False, comment='请求名称')
    method = db.Column(db.String(10), nullable=False, default='GET', comment='HTTP 方法')
    url = db.Column(db.String(500), nullable=False, comment='请求 URL')
    headers = db.Column(db.Text, default='{}', comment='请求头（JSON）')
    body = db.Column(db.Text, comment='请求体（JSON）')
    params = db.Column(db.Text, default='{}', comment='URL 参数（JSON）')
    description = db.Column(db.String(500), comment='请求描述')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        """转换为字典（便于 JSON 序列化）"""
        return {
            'id': self.id,
            'collection_id': self.collection_id,
            'name': self.name,
            'method': self.method,
            'url': self.url,
            'headers': json.loads(self.headers) if isinstance(self.headers, str) else self.headers,
            'body': json.loads(self.body) if self.body and isinstance(self.body, str) else self.body,
            'params': json.loads(self.params) if isinstance(self.params, str) else self.params,
            'description': self.description,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


# 初始化数据库表
def init_db():
    """初始化数据库（创建所有表）"""
    with app.app_context():
        db.create_all()
        logger.info("✅ 数据库初始化完成")


# ============= 数据库初始化 Hook =============

@app.before_request
def before_request():
    """在每个请求之前执行"""
    # 确保数据库表存在
    with app.app_context():
        db.create_all()

# ============= 路由 - 环境管理 =============

@app.route('/api/environments', methods=['GET'])
def get_environments():
    """获取所有环境配置"""
    try:
        envs = Environment.query.all()
        result = []
        for env in envs:
            # 解析 JSON 字符串为字典
            headers = json.loads(env.headers) if isinstance(env.headers, str) else env.headers
            variables = json.loads(env.variables) if isinstance(env.variables, str) else env.variables
            
            result.append({
                'id': env.id,
                'name': env.name,
                'base_url': env.base_url,
                'headers': headers,  # ← 现在是字典而不是字符串
                'variables': variables  # ← 现在是字典而不是字符串
            })
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error getting environments: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/environments', methods=['POST'])
def create_environment():
    """创建新环境"""
    try:
        data = request.get_json()
        env = Environment(
            name=data.get('name'),
            base_url=data.get('base_url'),
            headers=data.get('headers', {}),
            variables=data.get('variables', {})
        )
        db.session.add(env)
        db.session.commit()
        logger.info(f"Environment created: {env.name}")
        return jsonify({'id': env.id, 'message': 'Environment created successfully'}), 201
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error creating environment: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/environments/<int:env_id>', methods=['PUT'])
def update_environment(env_id):
    """更新环境配置"""
    try:
        data = request.get_json()
        env = Environment.query.get(env_id)
        if not env:
            return jsonify({'error': 'Environment not found'}), 404
        
        env.name = data.get('name', env.name)
        env.base_url = data.get('base_url', env.base_url)
        env.headers = data.get('headers', env.headers)
        env.variables = data.get('variables', env.variables)
        
        db.session.commit()
        logger.info(f"Environment updated: {env.name}")
        return jsonify({'message': 'Environment updated successfully'})
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error updating environment: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/environments/<int:env_id>', methods=['DELETE'])
def delete_environment(env_id):
    """删除环境"""
    try:
        env = Environment.query.get(env_id)
        if not env:
            return jsonify({'error': 'Environment not found'}), 404
        
        db.session.delete(env)
        db.session.commit()
        logger.info(f"Environment deleted: {env.name}")
        return jsonify({'message': 'Environment deleted successfully'})
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error deleting environment: {e}")
        return jsonify({'error': str(e)}), 500

# ============= 路由 - 集合管理 =============

@app.route('/api/collections', methods=['GET'])
def get_collections():
    """获取所有测试集合"""
    try:
        collections = TestCollection.query.all()
        return jsonify([{
            'id': c.id,
            'name': c.name,
            'description': c.description,
            'created_at': c.created_at.isoformat(),
            'updated_at': c.updated_at.isoformat(),
            'request_count': len(c.requests)
        } for c in collections])
    except Exception as e:
        logger.error(f"Error getting collections: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/collections', methods=['POST'])
def create_collection():
    """创建新测试集合"""
    try:
        data = request.get_json()
        collection = TestCollection(
            name=data.get('name'),
            description=data.get('description', '')
        )
        db.session.add(collection)
        db.session.commit()
        logger.info(f"Collection created: {collection.name}")
        return jsonify({'id': collection.id, 'message': 'Collection created successfully'}), 201
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error creating collection: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/collections/<int:collection_id>', methods=['GET'])
def get_collection_detail(collection_id):
    """获取集合详情（包含所有请求）"""
    try:
        collection = TestCollection.query.get(collection_id)
        if not collection:
            return jsonify({'error': 'Collection not found'}), 404
        
        return jsonify({
            'id': collection.id,
            'name': collection.name,
            'description': collection.description,
            'created_at': collection.created_at.isoformat(),
            'updated_at': collection.updated_at.isoformat(),
            'requests': [{
                'id': r.id,
                'name': r.name,
                'method': r.method,
                'url': r.url,
                'headers': r.headers,
                'body': r.body,
                'params': r.params,
                'expected_status': r.expected_status,
                'expected_body': r.expected_body,
                'description': r.description
            } for r in collection.requests]
        })
    except Exception as e:
        logger.error(f"Error getting collection detail: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/collections/<int:collection_id>', methods=['PUT'])
def update_collection(collection_id):
    """更新集合"""
    try:
        data = request.get_json()
        collection = TestCollection.query.get(collection_id)
        if not collection:
            return jsonify({'error': 'Collection not found'}), 404
        
        collection.name = data.get('name', collection.name)
        collection.description = data.get('description', collection.description)
        db.session.commit()
        logger.info(f"Collection updated: {collection.name}")
        return jsonify({'message': 'Collection updated successfully'})
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error updating collection: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/collections/<int:collection_id>', methods=['DELETE'])
def delete_collection(collection_id):
    """删除集合"""
    try:
        collection = TestCollection.query.get(collection_id)
        if not collection:
            return jsonify({'error': 'Collection not found'}), 404
        
        db.session.delete(collection)
        db.session.commit()
        logger.info(f"Collection deleted: {collection.name}")
        return jsonify({'message': 'Collection deleted successfully'})
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error deleting collection: {e}")
        return jsonify({'error': str(e)}), 500

# ============= 路由 - 请求管理 =============

@app.route('/api/requests', methods=['POST'])
def create_request():
    """创建新的测试请求"""
    try:
        data = request.get_json()
        test_req = TestRequest(
            collection_id=data.get('collection_id'),
            name=data.get('name'),
            method=data.get('method', 'GET'),
            url=data.get('url'),
            headers=data.get('headers', {}),
            body=data.get('body'),
            params=data.get('params'),
            expected_status=data.get('expected_status', 200),
            expected_body=data.get('expected_body'),
            description=data.get('description', '')
        )
        db.session.add(test_req)
        db.session.commit()
        logger.info(f"Request created: {test_req.name}")
        return jsonify({'id': test_req.id, 'message': 'Request created successfully'}), 201
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error creating request: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/requests/<int:request_id>', methods=['PUT'])
def update_request(request_id):
    """更新测试请求"""
    try:
        data = request.get_json()
        test_req = TestRequest.query.get(request_id)
        if not test_req:
            return jsonify({'error': 'Request not found'}), 404
        
        test_req.name = data.get('name', test_req.name)
        test_req.method = data.get('method', test_req.method)
        test_req.url = data.get('url', test_req.url)
        test_req.headers = data.get('headers', test_req.headers)
        test_req.body = data.get('body', test_req.body)
        test_req.params = data.get('params', test_req.params)
        test_req.expected_status = data.get('expected_status', test_req.expected_status)
        test_req.expected_body = data.get('expected_body', test_req.expected_body)
        test_req.description = data.get('description', test_req.description)
        
        db.session.commit()
        logger.info(f"Request updated: {test_req.name}")
        return jsonify({'message': 'Request updated successfully'})
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error updating request: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/requests/<int:request_id>', methods=['DELETE'])
def delete_request(request_id):
    """删除请求"""
    try:
        test_req = TestRequest.query.get(request_id)
        if not test_req:
            return jsonify({'error': 'Request not found'}), 404
        
        db.session.delete(test_req)
        db.session.commit()
        logger.info(f"Request deleted: {test_req.name}")
        return jsonify({'message': 'Request deleted successfully'})
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error deleting request: {e}")
        return jsonify({'error': str(e)}), 500

# ============= 路由 - 请求执行 =============

@app.route('/api/send', methods=['POST'])
def send_request():
    """
    发送 HTTP 请求到目标 API
    
    这是平台的核心功能 - 接收前端的请求配置，转发到目标 API，
    然后返回响应结果给前端显示。
    
    请求体 (JSON)：
    {
        "method": "POST",              # HTTP 方法
        "url": "{{base_url}}/api/users",  # 完整 URL（支持环境变量）
        "headers": {...},              # 请求头
        "body": {...},                 # 请求体（JSON）
        "params": {...},               # URL 查询参数
        "environment": {id, name, ...}  # 环境配置
    }
    
    返回 (JSON)：
    {
        "success": true,
        "response": {
            "status_code": 200,
            "headers": {...},
            "body": "...",
            "body_json": {...},  # 如果是 JSON 响应
            "time": 0.123        # 响应时间（秒）
        },
        "timestamp": "2025-12-07T15:30:45.REDACTED_PASSWORD"
    }
    """
    
    try:
        # ========== Step 1: 从前端请求中提取数据 ==========
        # 这里的 request 是 Flask 的，用来获取 HTTP 请求信息
        data = request.get_json()
        
        method = data.get('method', 'GET').upper()
        url = data.get('url')
        headers = data.get('headers', {})
        body = data.get('body')
        params = data.get('params')
        environment = data.get('environment')
        
        # 参数验证
        if not url:
            logger.warning("❌ 请求参数不完整：缺少 URL")
            return jsonify({
                'success': False,
                'error': 'URL 不能为空'
            }), 400
        
        logger.info(f"📝 前端请求: {method} {url}")
        
        # ========== Step 2: 环境变量注入 ==========
        # 如果指定了环境，从数据库加载环境配置并注入
        if environment:
            env_obj = Environment.query.get(environment['id'])
            if env_obj:
                logger.info(f"🔧 应用环境: {env_obj.name} (ID: {env_obj.id})")
                
                # 如果 URL 不是完整 URL（没有 http/https），加上 base_url
                if not url.startswith('http'):
                    url = f"{env_obj.base_url}{url}"
                    logger.info(f"   + Base URL: {env_obj.base_url}")
                
                # 合并环境的 headers 和请求的 headers
                # 请求的 headers 优先级更高（可以覆盖环境设置）
                if env_obj.headers:
                    try:
                        env_headers = json.loads(env_obj.headers) if isinstance(env_obj.headers, str) else env_obj.headers
                        headers = {**env_headers, **headers}
                        logger.info(f"   + 合并 Headers: {list(headers.keys())}")
                    except json.JSONDecodeError:
                        logger.warning(f"   ⚠️  无法解析环境 headers: {env_obj.headers}")
        
        # ========== Step 3: 使用 RequestUtil 发送请求 ==========
        # RequestUtil 是我们的工具类，统一管理 HTTP 请求
        # 它会自动处理 SSL、日志、错误等
        try:
            response = RequestUtil.send(
                method=method,
                url=url,
                headers=headers,
                json=body,
                params=params,
                timeout=15,
                verify=False  # 禁用 SSL 验证（仅用于测试环境）
            )
            
            # ========== Step 4: 格式化响应 ==========
            response_data = {
                'status_code': response.status_code,
                'headers': dict(response.headers),
                'body': response.text,
                'time': response.elapsed.total_seconds() if hasattr(response, 'elapsed') else 0
            }
            
            # 尝试解析 JSON 响应（便于前端美化展示）
            try:
                response_data['body_json'] = response.json()
                logger.info(f"   ✅ 响应已解析为 JSON")
            except:
                logger.info(f"   ℹ️  响应不是 JSON 格式")
            
            # ========== Step 5: 返回成功响应 ==========
            logger.info(f"✅ 请求成功: {response.status_code}")
            return jsonify({
                'success': True,
                'response': response_data,
                'timestamp': datetime.utcnow().isoformat()
            })
            
        except Exception as e:
            # 请求发送失败（网络错误、SSL 错误等）
            logger.error(f"❌ 请求发送失败: {type(e).__name__}: {str(e)}")
            return jsonify({
                'success': False,
                'error': f"{type(e).__name__}: {str(e)}",
                'timestamp': datetime.utcnow().isoformat()
            }), 400
            
    except Exception as e:
        # 处理请求过程中的其他错误
        logger.error(f"❌ 处理请求出错: {type(e).__name__}: {str(e)}", exc_info=True)
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# ============= 路由 - 测试运行 =============

@app.route('/api/run-tests', methods=['POST'])
def run_tests():
    """
    运行 Pytest 测试
    """
    try:
        data = request.get_json()
        collection_id = data.get('collection_id')
        
        # 如果指定了集合，生成对应的测试文件
        # 这里简化处理，实际可以动态生成 pytest 测试
        
        result = subprocess.run(
            ['pytest', 'tests/', '-v', '--alluredir=./reports/allure_results'],
            cwd=os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            capture_output=True,
            text=True
        )
        
        return jsonify({
            'success': result.returncode == 0,
            'output': result.stdout,
            'errors': result.stderr,
            'timestamp': datetime.utcnow().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error running tests: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/reports', methods=['GET'])
def get_reports():
    """获取测试报告列表"""
    try:
        reports_dir = './reports'
        reports = []
        
        if os.path.exists(reports_dir):
            for item in os.listdir(reports_dir):
                if item.startswith('allure_report_'):
                    item_path = os.path.join(reports_dir, item)
                    if os.path.isdir(item_path):
                        reports.append({
                            'name': item,
                            'path': f'/reports/{item}/index.html',
                            'created': datetime.fromtimestamp(
                                os.path.getmtime(item_path)
                            ).isoformat()
                        })
        
        return jsonify(sorted(reports, key=lambda x: x['created'], reverse=True))
    except Exception as e:
        logger.error(f"Error getting reports: {e}")
        return jsonify([])

# ============= 路由 - 配置导入导出 =============

@app.route('/api/import-postman', methods=['POST'])
def import_postman():
    """
    导入 Postman 集合
    支持 Postman 导出的 JSON 格式
    """
    try:
        data = request.get_json()
        postman_data = data.get('collection')
        
        # 创建集合
        collection = TestCollection(
            name=postman_data.get('info', {}).get('name', 'Imported Collection'),
            description=postman_data.get('info', {}).get('description', '')
        )
        db.session.add(collection)
        db.session.flush()
        
        # 导入请求
        def import_items(items, parent_collection):
            for item in items:
                if 'item' in item:  # 文件夹
                    import_items(item['item'], parent_collection)
                else:  # 请求
                    request_data = item.get('request', {})
                    
                    # 解析 URL
                    url = request_data.get('url')
                    if isinstance(url, dict):
                        url = url.get('raw', '')
                    
                    # 解析 headers
                    headers = {}
                    for h in request_data.get('header', []):
                        headers[h.get('key')] = h.get('value')
                    
                    # 解析 body
                    body = None
                    body_obj = request_data.get('body', {})
                    if body_obj.get('mode') == 'raw':
                        body = json.loads(body_obj.get('raw', '{}'))
                    
                    test_req = TestRequest(
                        collection_id=parent_collection.id,
                        name=item.get('name', 'Unnamed'),
                        method=request_data.get('method', 'GET'),
                        url=url,
                        headers=headers,
                        body=body,
                        description=item.get('description', '')
                    )
                    db.session.add(test_req)
        
        import_items(postman_data.get('item', []), collection)
        db.session.commit()
        
        logger.info(f"Postman collection imported: {collection.name}")
        return jsonify({
            'success': True,
            'collection_id': collection.id,
            'message': f'Collection "{collection.name}" imported successfully'
        }), 201
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error importing Postman collection: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/export-postman/<int:collection_id>', methods=['GET'])
def export_postman(collection_id):
    """
    导出为 Postman 格式
    """
    try:
        collection = TestCollection.query.get(collection_id)
        if not collection:
            return jsonify({'error': 'Collection not found'}), 404
        
        postman_collection = {
            'info': {
                'name': collection.name,
                'description': collection.description,
                'schema': 'https://schema.getpostman.com/json/collection/v2.1.0/collection.json'
            },
            'item': []
        }
        
        for req in collection.requests:
            item = {
                'name': req.name,
                'description': req.description or '',
                'request': {
                    'method': req.method,
                    'header': [{'key': k, 'value': v} for k, v in (req.headers or {}).items()],
                    'url': req.url,
                    'body': {
                        'mode': 'raw',
                        'raw': json.dumps(req.body) if req.body else '{}'
                    }
                }
            }
            postman_collection['item'].append(item)
        
        return jsonify(postman_collection)
    except Exception as e:
        logger.error(f"Error exporting collection: {e}")
        return jsonify({'error': str(e)}), 500

# ============= 路由 - 根页面 =============

@app.route('/')
def index():
    """提供前端 HTML"""
    return send_from_directory('static', 'index.html')

@app.route('/api/health', methods=['GET'])
def health_check():
    """健康检查"""
    return jsonify({'status': 'ok'})

# ============= 数据库初始化 =============

def init_db():
    """初始化数据库（创建表并加载默认数据）"""
    with app.app_context():
        db.create_all()
        logger.info("✅ 数据库表创建完成")
        
        # 创建默认环境（如果不存在）
        if Environment.query.count() == 0:
            config_path = os.path.join(
                os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
                'config', 'config.yaml'
            )
            try:
                with open(config_path, encoding='utf-8') as f:
                    config = yaml.safe_load(f)
                    for env_name, env_config in config.get('env', {}).items():
                        # 将 dict 转换为 JSON 字符串存储
                        env = Environment(
                            name=env_name,
                            base_url=env_config.get('base_url', ''),
                            headers=json.dumps(env_config.get('headers', {})),
                            variables=json.dumps(env_config.get('variables', {}))
                        )
                        db.session.add(env)
                    db.session.commit()
                    logger.info(f"✅ 从 config.yaml 加载了 {Environment.query.count()} 个环境")
            except FileNotFoundError:
                logger.info("ℹ️  config.yaml 不存在，跳过加载默认环境")
            except Exception as e:
                logger.warning(f"⚠️  加载 config.yaml 失败: {e}")


if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)
