"""
独立数据库模块

提供不依赖 Flask 的 SQLAlchemy 基础设施。
Flask 和 FastAPI 都可以使用此模块。

设计原则：
- models 可以在没有 Flask app context 的情况下导入和定义
- 提供与 Flask-SQLAlchemy 兼容的 API（db.Column, db.Model 等）
- 支持 Flask-SQLAlchemy 初始化（init_app）
"""

import os
from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Text,
    Boolean,
    DateTime,
    Float,
    ForeignKey,
    Index,
    JSON,
    Enum as SAEnum,
    UniqueConstraint,
)
from sqlalchemy.orm import (
    DeclarativeBase,
    sessionmaker,
    relationship,
    scoped_session,
    backref,
    Query,
)


def _paginate(self, page=None, per_page=None, error_out=True, max_per_page=None):
    """
    Flask-SQLAlchemy 兼容的分页方法，直接注入到 SQLAlchemy Query 类。

    这样 Project.query.filter_by(...).paginate(...) 等链式调用也能正常工作。
    """
    if page is None:
        page = 1
    if per_page is None:
        per_page = 20
    page = int(page)
    per_page = int(per_page)
    if max_per_page and per_page > max_per_page:
        per_page = max_per_page

    total = self.count()
    items = self.offset((page - 1) * per_page).limit(per_page).all()

    class _Pagination:
        def __init__(self, items, total, page, per_page):
            self.items = items
            self.total = total
            self.page = page
            self.per_page = per_page
            self.pages = (total + per_page - 1) // per_page if per_page > 0 else 0
            self.has_next = page < self.pages
            self.has_prev = page > 1

    return _Pagination(items, total, page, per_page)


# 猴子补丁：给 SQLAlchemy Query 添加 paginate 方法
if not hasattr(Query, 'paginate'):
    Query.paginate = _paginate


class Base(DeclarativeBase):
    """SQLAlchemy 声明式基类"""
    pass


class _DatabaseManager:
    """
    数据库管理器

    提供与 Flask-SQLAlchemy 兼容的 API，
    同时支持独立使用（无 Flask）。
    """

    def __init__(self):
        self._engine = None
        self._session_factory = None
        self._session = None
        self._initialized = False

        # Flask-SQLAlchemy 兼容属性
        self.Model = type('Model', (Base,), {
            '__abstract__': True,
            'query': None,  # Flask-SQLAlchemy 会覆盖此属性
        })

        # SQLAlchemy 类型快捷方式
        self.Column = Column
        self.Integer = Integer
        self.String = String
        self.Text = Text
        self.Boolean = Boolean
        self.DateTime = DateTime
        self.Float = Float
        self.ForeignKey = ForeignKey
        self.Index = Index
        self.JSON = JSON
        self.Enum = SAEnum
        self.UniqueConstraint = UniqueConstraint
        self.relationship = relationship
        self.backref = backref

        # SQLAlchemy 函数和操作符（Flask-SQLAlchemy 兼容）
        from sqlalchemy import or_, and_, not_, func, case, text
        self.or_ = or_
        self.and_ = and_
        self.not_ = not_
        self.func = func
        self.case = case
        self.text = text

    def init_app(self, app):
        """
        Flask-SQLAlchemy 风格的初始化

        从 Flask app config 中读取数据库 URL 并创建引擎。
        SQLite 自动使用 NullPool。
        """
        database_uri = app.config.get('SQLALCHEMY_DATABASE_URI')
        if not database_uri:
            database_uri = os.environ.get(
                'DATABASE_URL',
                'sqlite:///fullscopetest.db'
            )

        engine_options = app.config.get('SQLALCHEMY_ENGINE_OPTIONS', {})

        # SQLite 自动使用 NullPool（避免 "database is locked" 错误）
        if database_uri.startswith('sqlite'):
            from sqlalchemy.pool import NullPool
            engine_options.setdefault('poolclass', NullPool)

        self._engine = create_engine(database_uri, **engine_options)

        self._session_factory = sessionmaker(bind=self._engine)
        self._session = scoped_session(self._session_factory)
        self._initialized = True

        # 设置 Flask-SQLAlchemy 兼容的 query 属性
        self._setup_query_property()

        return self

    def init(self, database_url: str = None, **engine_options):
        """
        独立初始化（无 Flask）

        用于 FastAPI 或测试场景。
        SQLite 自动使用 NullPool 避免连接池问题。
        """
        if database_url is None:
            database_url = os.environ.get(
                'DATABASE_URL',
                'sqlite:///fullscopetest.db'
            )

        # SQLite 自动使用 NullPool（避免 "database is locked" 错误）
        if database_url.startswith('sqlite'):
            from sqlalchemy.pool import NullPool
            engine_options.setdefault('poolclass', NullPool)

        self._engine = create_engine(database_url, **engine_options)
        self._session_factory = sessionmaker(bind=self._engine)
        self._session = scoped_session(self._session_factory)
        self._initialized = True

        # 设置 Flask-SQLAlchemy 兼容的 query 属性
        self._setup_query_property()

        return self

    def _setup_query_property(self):
        """
        为 Model 设置 query 属性

        提供 User.query.filter_by(...) 风格的查询接口，
        兼容 Flask-SQLAlchemy 的使用方式。
        """
        db_instance = self

        class _QueryProxy:
            """代理查询对象，将 Model.query 转发到 session.query(Model)"""
            def __init__(self, model):
                self._model = model

            def __getattr__(self, name):
                return getattr(db_instance.session.query(self._model), name)

            def __call__(self, *args, **kwargs):
                return db_instance.session.query(self._model, *args, **kwargs)

            def paginate(self, page=None, per_page=None, error_out=True, max_per_page=None):
                """
                Flask-SQLAlchemy 兼容的分页方法

                当 page/per_page 为 None 时使用默认值，避免类型错误。
                """
                if page is None:
                    page = 1
                if per_page is None:
                    per_page = 20
                page = int(page)
                per_page = int(per_page)
                if max_per_page and per_page > max_per_page:
                    per_page = max_per_page

                query_obj = db_instance.session.query(self._model)
                total = query_obj.count()
                items = query_obj.offset((page - 1) * per_page).limit(per_page).all()

                # 返回一个与 Flask-SQLAlchemy Pagination 兼容的对象
                class _Pagination:
                    def __init__(self, items, total, page, per_page):
                        self.items = items
                        self.total = total
                        self.page = page
                        self.per_page = per_page
                        self.pages = (total + per_page - 1) // per_page if per_page > 0 else 0
                        self.has_next = page < self.pages
                        self.has_prev = page > 1

                return _Pagination(items, total, page, per_page)

        class _ModelMeta(type):
            """拦截 Model 类的 query 属性访问"""
            @property
            def query(cls):
                return _QueryProxy(cls)

        # 动态更新 Model 的 metaclass 不可行，
        # 改用 descriptor 方式
        class _QueryDescriptor:
            def __get__(self, obj, objtype=None):
                if objtype is None:
                    objtype = type(obj)
                return _QueryProxy(objtype)

        self.Model.query = _QueryDescriptor()

    @property
    def engine(self):
        return self._engine

    @property
    def session(self):
        if self._session is None:
            raise RuntimeError(
                "Database not initialized. Call db.init() or db.init_app() first."
            )
        return self._session

    @property
    def metadata(self):
        """SQLAlchemy Metadata，用于 Alembic 迁移和 create_all"""
        return Base.metadata

    def create_all(self):
        """创建所有表"""
        Base.metadata.create_all(self._engine)

    def drop_all(self):
        """删除所有表"""
        Base.metadata.drop_all(self._engine)

    def __repr__(self):
        if self._initialized:
            return f'<DatabaseManager engine={self._engine}>'
        return '<DatabaseManager (not initialized)>'


# 全局数据库实例
db = _DatabaseManager()

# 便捷导出
Base = Base
