"""
测试计划管理 API

提供测试计划的 CRUD、执行轮次管理、用例结果更新和通过率趋势查询。
"""
from flask import request
from flask_jwt_extended import jwt_required

from . import api_bp
from ..utils.response import success_response, error_response
from ..utils.validators import validate_json
from ..utils import get_current_user_id
from ..services.plan_service import PlanService
from ..utils.exceptions import AppError
from ..core.logging import get_logger

logger = get_logger(__name__)
plan_service = PlanService()


# ── 计划 CRUD ────────────────────────────────────────────────────────────────

@api_bp.route('/test-plans', methods=['POST'])
@jwt_required()
@validate_json('name', 'project_id')
def create_test_plan():
    """
    创建测试计划

    请求体:
        name: 计划名称 (必填)
        project_id: 项目 ID (必填)
        description: 描述
        include_cases: 用例列表 [{case_type, case_id}]
        tags: 标签
    """
    user_id = int(get_current_user_id())
    data = request.get_json()

    try:
        plan = plan_service.create_plan(
            user_id=user_id,
            project_id=data['project_id'],
            name=data['name'],
            description=data.get('description', ''),
            include_cases=data.get('include_cases', []),
            tags=data.get('tags', []),
        )
        return success_response(data=plan, message='测试计划创建成功', code=201)
    except AppError as e:
        return error_response(e.code, e.message, errors=e.errors)


@api_bp.route('/test-plans', methods=['GET'])
@jwt_required()
def list_test_plans():
    """
    获取项目下的测试计划列表

    查询参数:
        project_id: 项目 ID (必填)
        page: 页码
        per_page: 每页数量
        status: 状态过滤
    """
    project_id = request.args.get('project_id', type=int)
    if not project_id:
        return error_response(400, '缺少 project_id 参数')

    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    status = request.args.get('status')

    try:
        result = plan_service.get_plans(project_id, page, per_page, status)
        return success_response(data=result)
    except AppError as e:
        return error_response(e.code, e.message)


@api_bp.route('/test-plans/<int:plan_id>', methods=['GET'])
@jwt_required()
def get_test_plan(plan_id):
    """获取测试计划详情（包含最近轮次）"""
    try:
        plan = plan_service.get_plan(plan_id)
        return success_response(data=plan)
    except AppError as e:
        return error_response(e.code, e.message)


@api_bp.route('/test-plans/<int:plan_id>', methods=['PUT'])
@jwt_required()
def update_test_plan(plan_id):
    """
    更新测试计划

    请求体（均可选）:
        name, description, include_cases, tags, status
    """
    data = request.get_json()
    try:
        plan = plan_service.update_plan(plan_id, **data)
        return success_response(data=plan, message='更新成功')
    except AppError as e:
        return error_response(e.code, e.message)


@api_bp.route('/test-plans/<int:plan_id>', methods=['DELETE'])
@jwt_required()
def delete_test_plan(plan_id):
    """删除测试计划"""
    try:
        plan_service.delete_plan(plan_id)
        return success_response(message='测试计划已删除')
    except AppError as e:
        return error_response(e.code, e.message)


# ── 执行轮次 ─────────────────────────────────────────────────────────────────

@api_bp.route('/test-plans/<int:plan_id>/runs', methods=['POST'])
@jwt_required()
def create_test_plan_run(plan_id):
    """
    创建执行轮次

    请求体:
        environment_id: 环境 ID (可选)
        environment_name: 环境名称 (可选)
        notes: 备注 (可选)
    """
    user_id = int(get_current_user_id())
    data = request.get_json(silent=True) or {}

    try:
        run = plan_service.create_run(
            plan_id=plan_id,
            user_id=user_id,
            environment_id=data.get('environment_id'),
            environment_name=data.get('environment_name', ''),
            notes=data.get('notes', ''),
        )
        return success_response(data=run, message='执行轮次已创建', code=201)
    except AppError as e:
        return error_response(e.code, e.message)


@api_bp.route('/test-plans/<int:plan_id>/runs', methods=['GET'])
@jwt_required()
def list_test_plan_runs(plan_id):
    """获取计划的执行轮次列表"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)

    try:
        result = plan_service.get_runs(plan_id, page, per_page)
        return success_response(data=result)
    except AppError as e:
        return error_response(e.code, e.message)


@api_bp.route('/test-plan-runs/<int:run_id>', methods=['GET'])
@jwt_required()
def get_test_plan_run(run_id):
    """获取执行轮次详情（包含用例结果）"""
    try:
        run = plan_service.get_run(run_id)
        return success_response(data=run)
    except AppError as e:
        return error_response(e.code, e.message)


@api_bp.route('/test-plan-runs/<int:run_id>/case-results', methods=['PATCH'])
@jwt_required()
@validate_json('case_type', 'case_id', 'status')
def update_case_result(run_id):
    """
    更新用例执行结果

    请求体:
        case_type: 用例类型 (必填)
        case_id: 用例 ID (必填)
        status: 状态 passed/failed/skipped/error (必填)
        duration: 执行耗时
        error_message: 错误信息
        result_detail: 详细结果
        test_run_id: 关联的 TestRun ID
    """
    data = request.get_json()

    try:
        result = plan_service.update_case_result(
            run_id=run_id,
            case_type=data['case_type'],
            case_id=data['case_id'],
            status=data['status'],
            duration=data.get('duration'),
            error_message=data.get('error_message'),
            result_detail=data.get('result_detail'),
            test_run_id=data.get('test_run_id'),
        )
        return success_response(data=result, message='结果已更新')
    except AppError as e:
        return error_response(e.code, e.message)


@api_bp.route('/test-plan-runs/<int:run_id>/complete', methods=['POST'])
@jwt_required()
def complete_test_plan_run(run_id):
    """标记执行轮次完成"""
    try:
        run = plan_service.complete_run(run_id)
        return success_response(data=run, message='轮次已完成')
    except AppError as e:
        return error_response(e.code, e.message)


# ── 趋势查询 ─────────────────────────────────────────────────────────────────

@api_bp.route('/test-plans/<int:plan_id>/trend', methods=['GET'])
@jwt_required()
def get_pass_rate_trend(plan_id):
    """
    获取通过率趋势

    查询参数:
        limit: 返回的轮次数 (默认 20)
    """
    limit = request.args.get('limit', 20, type=int)

    try:
        trend = plan_service.get_pass_rate_trend(plan_id, limit)
        return success_response(data=trend)
    except AppError as e:
        return error_response(e.code, e.message)