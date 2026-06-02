"""
Web 测试 Service

处理 Web 自动化测试的业务逻辑
"""

import json
import time
from datetime import datetime

from .base import BaseService
from ..extensions import db
from ..models.web_test_collection import WebTestCollection
from ..models.web_test_script import WebTestScript
from ..utils.exceptions import NotFoundError, ValidationError


class WebTestService(BaseService):

    def get_collections(self, user_id: int, project_id: int = None):
        """获取 Web 测试集合列表"""
        query = WebTestCollection.query.filter_by(user_id=user_id)
        if project_id:
            query = query.filter_by(project_id=project_id)
        collections = query.order_by(WebTestCollection.created_at.desc()).all()
        return [c.to_dict() for c in collections]

    def create_collection(self, user_id: int, data: dict):
        """创建 Web 测试集合"""
        if not data.get("name"):
            raise ValidationError("name is required")

        collection = WebTestCollection(
            name=data["name"],
            description=data.get("description", ""),
            project_id=data.get("project_id"),
            user_id=user_id
        )
        with self.transaction():
            self.add(collection)
            self.flush()
            result = collection.to_dict()
        return result

    def update_collection(self, collection_id: int, user_id: int, data: dict):
        """更新 Web 测试集合"""
        collection = WebTestCollection.query.filter_by(id=collection_id, user_id=user_id).first()
        if not collection:
            raise NotFoundError("集合", collection_id)

        if "name" in data:
            collection.name = data["name"]
        if "description" in data:
            collection.description = data["description"]

        with self.transaction():
            result = collection.to_dict()
        return result

    def delete_collection(self, collection_id: int, user_id: int):
        """删除 Web 测试集合"""
        collection = WebTestCollection.query.filter_by(id=collection_id, user_id=user_id).first()
        if not collection:
            raise NotFoundError("集合", collection_id)

        with self.transaction():
            self.delete(collection)

    def get_scripts(self, user_id: int, collection_id: int = None, project_id: int = None):
        """获取测试脚本列表"""
        query = WebTestScript.query.filter_by(user_id=user_id)
        if collection_id:
            query = query.filter_by(collection_id=collection_id)
        if project_id:
            query = query.filter_by(project_id=project_id)
        scripts = query.order_by(WebTestScript.created_at.desc()).all()
        return [s.to_dict() for s in scripts]

    def create_script(self, user_id: int, data: dict):
        """创建测试脚本"""
        if not data.get("name"):
            raise ValidationError("name is required")
        if not data.get("code"):
            raise ValidationError("code is required")

        script = WebTestScript(
            name=data["name"],
            description=data.get("description", ""),
            code=data["code"],
            collection_id=data.get("collection_id"),
            project_id=data.get("project_id"),
            user_id=user_id
        )
        with self.transaction():
            self.add(script)
            self.flush()
            result = script.to_dict()
        return result

    def update_script(self, script_id: int, user_id: int, data: dict):
        """更新测试脚本"""
        script = WebTestScript.query.filter_by(id=script_id, user_id=user_id).first()
        if not script:
            raise NotFoundError("脚本", script_id)

        updatable_fields = ["name", "description", "code", "collection_id", "project_id"]
        for field in updatable_fields:
            if field in data:
                setattr(script, field, data[field])

        with self.transaction():
            result = script.to_dict()
        return result

    def delete_script(self, script_id: int, user_id: int):
        """删除测试脚本"""
        script = WebTestScript.query.filter_by(id=script_id, user_id=user_id).first()
        if not script:
            raise NotFoundError("脚本", script_id)

        with self.transaction():
            self.delete(script)

    def get_script(self, script_id: int, user_id: int):
        """获取脚本详情"""
        script = WebTestScript.query.filter_by(id=script_id, user_id=user_id).first()
        if not script:
            raise NotFoundError("脚本", script_id)
        return script.to_dict()
