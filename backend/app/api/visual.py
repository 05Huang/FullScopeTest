"""
视觉回归测试 API 接口模块

提供基准截图管理、差异记录查询等接口
"""

from flask import request
from flask_jwt_extended import jwt_required

from . import api_bp
from ..extensions import db
from ..models.visual_baseline import VisualBaseline
from ..models.visual_diff import VisualDiff
from ..utils.response import success_response, error_response
from ..utils import get_current_user_id
from ..core.logging import get_logger

logger = get_logger(__name__)


@api_bp.route('/visual/baselines/<int:test_case_id>', methods=['GET'])
@jwt_required()
def get_baselines(test_case_id):
    """
    获取指定测试用例的所有基准截图

    查询参数:
        test_type: 测试类型过滤 (api/web/app，可选)
        step_index: 步骤索引过滤 (可选)
    """
    test_type = request.args.get('test_type', '').strip()
    step_index = request.args.get('step_index', type=int)

    query = VisualBaseline.query.filter_by(test_case_id=test_case_id)

    if test_type:
        query = query.filter_by(test_type=test_type)
    if step_index is not None:
        query = query.filter_by(step_index=step_index)

    baselines = query.order_by(VisualBaseline.step_index, VisualBaseline.version.desc()).all()

    return success_response(data=[b.to_dict() for b in baselines])


@api_bp.route('/visual/baselines/<int:baseline_id>/approve', methods=['POST'])
@jwt_required()
def approve_baseline(baseline_id):
    """
    批准基准截图

    将指定基准截图标记为已批准（状态设为 active），并记录批准人
    """
    user_id = get_current_user_id()
    baseline = VisualBaseline.query.get(baseline_id)

    if not baseline:
        return error_response(404, '基准截图不存在')

    baseline.approved_by = user_id
    from datetime import datetime
    baseline.approved_at = datetime.utcnow()
    baseline.status = 'active'
    db.session.commit()

    logger.info(
        "基准截图已批准",
        baseline_id=baseline_id,
        approved_by=user_id,
        test_case_id=baseline.test_case_id,
    )

    return success_response(
        data=baseline.to_dict(),
        message='基准截图已批准'
    )


@api_bp.route('/visual/diffs/<int:test_run_id>', methods=['GET'])
@jwt_required()
def get_diffs(test_run_id):
    """
    获取指定测试执行的视觉差异记录

    查询参数:
        test_case_id: 测试用例 ID 过滤 (可选)
        status: 状态过滤 (可选)
        page: 页码 (默认 1)
        per_page: 每页数量 (默认 20)
    """
    test_case_id = request.args.get('test_case_id', type=int)
    status = request.args.get('status', '').strip()
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)

    query = VisualDiff.query.filter_by(test_run_id=test_run_id)

    if test_case_id:
        query = query.filter_by(test_case_id=test_case_id)
    if status:
        query = query.filter_by(status=status)

    pagination = query.order_by(VisualDiff.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )

    from ..utils.response import paginate_response
    return paginate_response(
        items=[d.to_dict() for d in pagination.items],
        total=pagination.total,
        page=page,
        per_page=per_page
    )


@api_bp.route('/visual/baselines/<int:baseline_id>', methods=['DELETE'])
@jwt_required()
def delete_baseline(baseline_id):
    """
    删除基准截图（软删除，标记为 deprecated）

    同时删除物理文件
    """
    baseline = VisualBaseline.query.get(baseline_id)

    if not baseline:
        return error_response(404, '基准截图不存在')

    # 删除物理文件
    import os
    from flask import current_app
    base_path = current_app.config.get(
        'SCREENSHOT_STORAGE_PATH',
        os.path.join(os.path.dirname(os.path.dirname(__file__)), 'uploads', 'screenshots')
    )
    full_path = os.path.join(base_path, baseline.baseline_image_path)
    if os.path.exists(full_path):
        try:
            os.remove(full_path)
        except OSError as e:
            logger.warning("删除基准截图文件失败", path=full_path, error=str(e))

    # 软删除
    baseline.status = 'deprecated'
    db.session.commit()

    logger.info(
        "基准截图已删除",
        baseline_id=baseline_id,
        test_case_id=baseline.test_case_id,
    )

    return success_response(message='基准截图已删除')
