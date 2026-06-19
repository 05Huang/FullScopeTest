"""
状态 Badge 生成 API

为测试集合/项目生成 SVG 状态 Badge。
"""

from flask import request, Response
from . import api_bp
from ..models.test_run import TestRun
from ..models.api_test_case import ApiTestCollection
from ..core.logging import get_logger

logger = get_logger(__name__)


def _generate_svg(label: str, value: str, color: str) -> str:
    """生成 SVG Badge"""
    label_width = max(len(label) * 7 + 10, 60)
    value_width = max(len(value) * 7 + 10, 50)
    total_width = label_width + value_width
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{total_width}" height="20">
  <linearGradient id="s" x2="0" y2="100%">
    <stop offset="0" stop-color="#bbb" stop-opacity=".1"/>
    <stop offset="1" stop-opacity=".1"/>
  </linearGradient>
  <clipPath id="r"><rect width="{total_width}" height="20" rx="3"/></clipPath>
  <g clip-path="url(#r)">
    <rect width="{label_width}" height="20" fill="#555"/>
    <rect x="{label_width}" width="{value_width}" height="20" fill="{color}"/>
    <rect width="{total_width}" height="20" fill="url(#s)"/>
  </g>
  <g fill="#fff" text-anchor="middle" font-family="Verdana,Geneva,sans-serif" font-size="11">
    <text x="{label_width // 2}" y="14" fill="#010101" fill-opacity=".3">{label}</text>
    <text x="{label_width // 2}" y="13">{label}</text>
    <text x="{label_width + value_width // 2}" y="14" fill="#010101" fill-opacity=".3">{value}</text>
    <text x="{label_width + value_width // 2}" y="13">{value}</text>
  </g>
</svg>'''


@api_bp.route("/badge/<int:collection_id>", methods=["GET"])
def get_test_badge(collection_id):
    """
    获取测试集合的状态 Badge（SVG）

    无需认证，可在 README 中嵌入：
      ![](https://host/api/v1/badge/123)
    """
    collection = ApiTestCollection.query.get(collection_id)
    if not collection:
        svg = _generate_svg("tests", "not found", "#9f9f9f")
        return Response(svg, mimetype="image/svg+xml")

    # 获取最近一次执行结果
    latest_run = TestRun.query.filter_by(
        test_object_id=collection_id, test_type="api"
    ).order_by(TestRun.started_at.desc()).first()

    if not latest_run or latest_run.status == "running":
        svg = _generate_svg("tests", "pending", "#9f9f9f")
    elif latest_run.status == "success":
        passed = latest_run.passed or 0
        total = latest_run.total_cases or 0
        svg = _generate_svg("tests", f"{passed}/{total} passed", "#4c1")
    else:
        failed = latest_run.failed or 0
        total = latest_run.total_cases or 0
        svg = _generate_svg("tests", f"{failed} failed", "#e05d44")

    return Response(svg, mimetype="image/svg+xml", headers={
        "Cache-Control": "no-cache, no-store, must-revalidate",
        "Expires": "0",
    })
