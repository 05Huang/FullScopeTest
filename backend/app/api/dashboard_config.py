"""
仪表盘配置 API

提供用户自定义仪表盘布局的 CRUD 操作。
"""
from flask import request
from flask_jwt_extended import jwt_required
from . import api_bp
from ..extensions import db
from ..models.dashboard_widget import DashboardWidget, WIDGET_TYPES, create_default_widgets
from ..utils.response import success_response, error_response
from ..utils import get_current_user_id
from ..middleware.tenant import get_current_organization_id


@api_bp.route('/dashboard/widgets', methods=['GET'])
@jwt_required()
def get_widgets():
    """获取当前用户的仪表盘组件配置"""
    user_id = get_current_user_id()
    org_id = get_current_organization_id()

    query = DashboardWidget.query.filter_by(user_id=user_id)
    if org_id:
        query = query.filter_by(organization_id=org_id)

    widgets = query.order_by(
        DashboardWidget.position_y, DashboardWidget.position_x
    ).all()

    # 如果用户没有配置，创建默认布局
    if not widgets and org_id:
        default_widgets = create_default_widgets(user_id, org_id)
        db.session.add_all(default_widgets)
        db.session.commit()
        widgets = default_widgets

    return success_response(data=[w.to_dict() for w in widgets])


@api_bp.route('/dashboard/widgets', methods=['PUT'])
@jwt_required()
def update_widgets():
    """批量更新仪表盘组件配置（整体布局保存）"""
    user_id = get_current_user_id()
    org_id = get_current_organization_id()
    data = request.get_json()
    widgets_data = data.get('widgets', [])

    if not widgets_data:
        return error_response(400, '缺少 widgets 数据')

    # 删除旧配置
    query = DashboardWidget.query.filter_by(user_id=user_id)
    if org_id:
        query = query.filter_by(organization_id=org_id)
    query.delete()

    # 创建新配置
    for wd in widgets_data:
        widget = DashboardWidget(
            user_id=user_id,
            organization_id=org_id or 0,
            widget_type=wd.get('widget_type', ''),
            title=wd.get('title', ''),
            config=wd.get('config', {}),
            position_x=wd.get('position_x', 0),
            position_y=wd.get('position_y', 0),
            width=wd.get('width', 1),
            height=wd.get('height', 1),
            is_visible=wd.get('is_visible', True),
        )
        db.session.add(widget)

    db.session.commit()

    query = DashboardWidget.query.filter_by(user_id=user_id)
    if org_id:
        query = query.filter_by(organization_id=org_id)
    widgets = query.order_by(
        DashboardWidget.position_y, DashboardWidget.position_x
    ).all()

    return success_response(data=[w.to_dict() for w in widgets], message='布局已保存')


@api_bp.route('/dashboard/widgets/reset', methods=['POST'])
@jwt_required()
def reset_widgets():
    """恢复默认仪表盘布局"""
    user_id = get_current_user_id()
    org_id = get_current_organization_id()

    query = DashboardWidget.query.filter_by(user_id=user_id)
    if org_id:
        query = query.filter_by(organization_id=org_id)
    query.delete()

    if org_id:
        default_widgets = create_default_widgets(user_id, org_id)
        db.session.add_all(default_widgets)
        db.session.commit()
        return success_response(data=[w.to_dict() for w in default_widgets], message='已恢复默认布局')

    return success_response(data=[], message='已恢复默认布局')


@api_bp.route('/dashboard/widget-types', methods=['GET'])
@jwt_required()
def get_widget_types():
    """获取可用的组件类型列表"""
    return success_response(data=WIDGET_TYPES)
