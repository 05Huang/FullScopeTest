"""
API 测试集合 Service

处理用例集合的 CRUD 操作
"""

from .base import BaseService
from ..extensions import db
from ..models.api_test_case import ApiTestCollection
from ..utils.exceptions import NotFoundError, ValidationError


class ApiCollectionService(BaseService):

    def get_collections(self, user_id: int, project_id: int = None):
        """获取用例集合列表"""
        query = ApiTestCollection.query.filter_by(user_id=user_id)
        if project_id:
            query = query.filter_by(project_id=project_id)
        collections = query.order_by(ApiTestCollection.created_at.desc()).all()
        return [c.to_dict() for c in collections]

    def create_collection(self, user_id: int, name: str, description: str = '', project_id: int = None):
        """创建用例集合"""
        if not name:
            raise ValidationError("name is required")

        collection = ApiTestCollection(
            name=name,
            description=description or '',
            project_id=project_id,
            user_id=user_id
        )
        with self.transaction():
            self.add(collection)
            self.flush()
            result = collection.to_dict()
        return result

    def update_collection(self, collection_id: int, user_id: int, data: dict):
        """更新用例集合"""
        collection = ApiTestCollection.query.filter_by(id=collection_id, user_id=user_id).first()
        if not collection:
            raise NotFoundError("集合", collection_id)

        if 'name' in data:
            collection.name = data['name']
        if 'description' in data:
            collection.description = data['description']

        with self.transaction():
            result = collection.to_dict()
        return result

    def delete_collection(self, collection_id: int, user_id: int):
        """删除用例集合"""
        collection = ApiTestCollection.query.filter_by(id=collection_id, user_id=user_id).first()
        if not collection:
            raise NotFoundError("集合", collection_id)

        with self.transaction():
            self.delete(collection)
