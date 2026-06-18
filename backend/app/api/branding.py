"""
品牌配置 API

支持管理员配置品牌外观，前端启动时获取品牌配置。
"""
from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from ..extensions import db
from ..models.user import User
from ..models.branding_config import BrandingConfig
from ..models.organization import OrganizationMember
from ..utils.response import success_response, error_response

branding_bp = Blueprint('branding', __name__)

# 默认品牌配置
DEFAULT_BRANDING = {
    'platform_name': 'FullScopeTest',
    'logo_url': None,
    'favicon_url': None,
    'primary_color': '#5FA59B',
    'login_background_url': None,
    'footer_text': '',
    'custom_css': '',
}


def _get_user_org_id(user_id):
    """获取用户当前组织 ID"""
    membership = OrganizationMember.query.filter_by(user_id=user_id, is_active=True).first()
    return membership.organization_id if membership else None


@branding_bp.route('/branding/config', methods=['GET'])
def get_branding_config():
    """
    获取品牌配置（无需认证，前端启动时调用）

    优先返回组织级配置，回退到全局默认配置。
    """
    org_id = request.args.get('org_id', type=int)
    config = None

    if org_id:
        config = BrandingConfig.query.filter_by(
            organization_id=org_id, is_active=True
        ).first()

    if not config:
        config = BrandingConfig.query.filter_by(
            organization_id=None, is_active=True
        ).first()

    if config:
        return success_response(data=config.to_dict())

    return success_response(data=DEFAULT_BRANDING)


@branding_bp.route('/branding/config', methods=['PUT'])
@jwt_required()
def update_branding_config():
    """更新品牌配置（管理员）"""
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if not user or not user.is_admin():
        return error_response(403, '需要管理员权限')

    org_id = _get_user_org_id(user_id)
    data = request.get_json()

    config = BrandingConfig.query.filter_by(organization_id=org_id).first()
    if not config:
        config = BrandingConfig(organization_id=org_id)
        db.session.add(config)

    for field in ['platform_name', 'logo_url', 'favicon_url', 'primary_color',
                  'login_background_url', 'footer_text', 'custom_css']:
        if field in data:
            setattr(config, field, data[field])

    db.session.commit()
    return success_response(data=config.to_dict(), message='品牌配置已更新')
