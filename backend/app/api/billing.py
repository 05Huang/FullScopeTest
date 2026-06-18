"""
计费 API

提供套餐查询、订阅管理、用量查询端点。
"""
from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from ..extensions import db
from ..models.user import User
from ..models.organization import OrganizationMember
from ..services.billing_service import billing_service
from ..utils.response import success_response, error_response

billing_bp = Blueprint('billing', __name__)


def _get_user_org_id(user_id):
    """获取用户当前组织 ID"""
    membership = OrganizationMember.query.filter_by(user_id=user_id, is_active=True).first()
    return membership.organization_id if membership else None


@billing_bp.route('/billing/plans', methods=['GET'])
@jwt_required()
def list_plans():
    """获取所有套餐"""
    plans = billing_service.get_plans()
    return success_response(data=[p.to_dict() for p in plans])


@billing_bp.route('/billing/subscription', methods=['GET'])
@jwt_required()
def get_subscription():
    """获取当前订阅"""
    user_id = get_jwt_identity()
    org_id = _get_user_org_id(user_id)
    if not org_id:
        return error_response(400, '未加入任何组织')

    sub = billing_service.get_subscription(org_id)
    if not sub:
        sub = billing_service.get_or_create_free_subscription(org_id)

    return success_response(data=sub.to_dict())


@billing_bp.route('/billing/subscription', methods=['POST'])
@jwt_required()
def upgrade_subscription():
    """升级/变更套餐"""
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if not user or not user.is_admin():
        return error_response(403, '需要管理员权限')

    org_id = _get_user_org_id(user_id)
    if not org_id:
        return error_response(400, '未加入任何组织')

    data = request.get_json()
    plan_name = data.get('plan_name')
    billing_cycle = data.get('billing_cycle', 'monthly')

    if not plan_name:
        return error_response(400, 'plan_name is required')

    try:
        sub = billing_service.upgrade_plan(org_id, plan_name, billing_cycle)
        return success_response(data=sub.to_dict(), message='套餐已更新')
    except ValueError as e:
        return error_response(400, str(e))


@billing_bp.route('/billing/subscription', methods=['DELETE'])
@jwt_required()
def cancel_subscription():
    """取消订阅"""
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if not user or not user.is_admin():
        return error_response(403, '需要管理员权限')

    org_id = _get_user_org_id(user_id)
    if not org_id:
        return error_response(400, '未加入任何组织')

    try:
        sub = billing_service.cancel_subscription(org_id)
        return success_response(data=sub.to_dict(), message='订阅已取消')
    except ValueError as e:
        return error_response(400, str(e))


@billing_bp.route('/billing/usage', methods=['GET'])
@jwt_required()
def get_usage():
    """获取当前用量"""
    user_id = get_jwt_identity()
    org_id = _get_user_org_id(user_id)
    if not org_id:
        return error_response(400, '未加入任何组织')

    quotas = {}
    for resource in ['projects', 'test_cases', 'ai_calls', 'members', 'storage']:
        quotas[resource] = billing_service.check_quota(org_id, resource)

    return success_response(data=quotas)


@billing_bp.route('/billing/quota/<resource>', methods=['GET'])
@jwt_required()
def check_resource_quota(resource):
    """检查单项资源配额"""
    user_id = get_jwt_identity()
    org_id = _get_user_org_id(user_id)
    if not org_id:
        return error_response(400, '未加入任何组织')

    result = billing_service.check_quota(org_id, resource)
    return success_response(data=result)


# ── Stripe Webhook 回调预留 ──────────────────────────────────────────────────

@billing_bp.route('/billing/webhook/stripe', methods=['POST'])
def stripe_webhook():
    """Stripe Webhook 回调（预留接口）"""
    # TODO: 实现 Stripe Webhook 验证和处理
    # payload = request.get_data()
    # sig_header = request.headers.get('Stripe-Signature')
    # event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    return success_response(message='Webhook received', code=200)


@billing_bp.route('/billing/webhook/alipay', methods=['POST'])
def alipay_webhook():
    """支付宝 Webhook 回调（预留接口）"""
    # TODO: 实现支付宝异步通知验证
    return success_response(message='Webhook received', code=200)
