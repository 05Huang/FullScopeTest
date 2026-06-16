"""
图表数据服务

为前端图表组件提供标准化的数据格式。
"""

from typing import Dict, Any, List
from ..core.logging import get_logger

logger = get_logger(__name__)


# 统一配色方案（遵循 --fst-* CSS 变量）
CHART_COLORS = {
    "primary": "#2D6A64",
    "secondary": "#629B95",
    "tertiary": "#D4B483",
    "info": "#5B8FB9",
    "error": "#C75450",
    "success": "#2D6A64",
    "warning": "#D4B483",
}


class ChartDataService:
    """图表数据服务"""

    def build_line_chart(self, title: str, x_data: list, series: List[Dict[str, Any]],
                         theme: str = "light") -> Dict[str, Any]:
        """构建折线图配置"""
        return {
            "type": "line",
            "title": title,
            "theme": theme,
            "colors": list(CHART_COLORS.values()),
            "xAxis": {"type": "category", "data": x_data},
            "yAxis": {"type": "value"},
            "series": series,
            "tooltip": {"trigger": "axis"},
            "legend": {"show": len(series) > 1},
        }

    def build_bar_chart(self, title: str, categories: list, data: list,
                        theme: str = "light") -> Dict[str, Any]:
        """构建柱状图配置"""
        return {
            "type": "bar",
            "title": title,
            "theme": theme,
            "colors": list(CHART_COLORS.values()),
            "xAxis": {"type": "category", "data": categories},
            "yAxis": {"type": "value"},
            "series": [{"type": "bar", "data": data}],
            "tooltip": {"trigger": "axis"},
        }

    def build_pie_chart(self, title: str, data: List[Dict[str, Any]],
                        theme: str = "light") -> Dict[str, Any]:
        """构建饼图配置"""
        return {
            "type": "pie",
            "title": title,
            "theme": theme,
            "colors": list(CHART_COLORS.values()),
            "series": [{"type": "pie", "data": data, "radius": ["40%", "70%"]}],
            "tooltip": {"trigger": "item"},
            "legend": {"show": True},
        }

    def build_gauge_chart(self, title: str, value: float, max_val: float = 100,
                          theme: str = "light") -> Dict[str, Any]:
        """构建仪表盘配置"""
        return {
            "type": "gauge",
            "title": title,
            "theme": theme,
            "series": [{"type": "gauge", "data": [{"value": value, "name": title}],
                       "max": max_val}],
        }


_instance = None


def get_chart_data_service():
    global _instance
    if _instance is None: _instance = ChartDataService()
    return _instance
