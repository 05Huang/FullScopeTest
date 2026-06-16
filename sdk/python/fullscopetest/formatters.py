"""
CLI 输出格式化

支持 text（人类可读）和 json（机器可读）两种格式。
"""

import json
import sys
from typing import Any, Dict


def format_output(data: Any, fmt: str = "text", title: str = "") -> str:
    """
    格式化输出

    Args:
        data: 输出数据
        fmt: 格式类型（text/json）
        title: 输出标题
    """
    if fmt == "json":
        return json.dumps(data, ensure_ascii=False, indent=2)
    return _format_text(data, title)


def _format_text(data: Any, title: str = "") -> str:
    """格式化为人类可读文本"""
    lines = []
    if title:
        lines.append(f"=== {title} ===")
        lines.append("")

    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, (dict, list)):
                lines.append(f"{key}:")
                lines.append(f"  {json.dumps(value, ensure_ascii=False, indent=2)}")
            else:
                lines.append(f"{key}: {value}")
    elif isinstance(data, list):
        for i, item in enumerate(data, 1):
            if isinstance(item, dict):
                name = item.get("name", item.get("id", i))
                lines.append(f"  {i}. {name}")
                for k, v in item.items():
                    if k not in ("name", "id"):
                        lines.append(f"     {k}: {v}")
            else:
                lines.append(f"  {i}. {item}")
    else:
        lines.append(str(data))

    return "\n".join(lines)


def print_result(data: Any, fmt: str = "text", title: str = ""):
    """打印格式化结果"""
    print(format_output(data, fmt, title))


def print_table(headers: list, rows: list, fmt: str = "text"):
    """打印表格"""
    if fmt == "json":
        result = [dict(zip(headers, row)) for row in rows]
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    # 计算列宽
    widths = [len(h) for h in headers]
    for row in rows:
        for i, cell in enumerate(row):
            widths[i] = max(widths[i], len(str(cell)))

    # 打印表头
    header_line = " | ".join(h.ljust(widths[i]) for i, h in enumerate(headers))
    print(header_line)
    print("-" * len(header_line))

    # 打印行
    for row in rows:
        line = " | ".join(str(cell).ljust(widths[i]) for i, cell in enumerate(row))
        print(line)


def print_error(message: str, exit_code: int = 1):
    """打印错误并退出"""
    print(f"错误: {message}", file=sys.stderr)
    sys.exit(exit_code)
