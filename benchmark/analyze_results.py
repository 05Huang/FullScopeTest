"""
性能基准测试结果分析脚本

解析 Locust 生成的 CSV 文件，生成对比报告
"""

import csv
import os
import sys
from datetime import datetime


def parse_locust_csv(csv_file):
    """解析 Locust CSV 统计文件"""
    if not os.path.exists(csv_file):
        return None

    stats = {
        "total_requests": 0,
        "total_failures": 0,
        "avg_response_time": 0,
        "p95_response_time": 0,
        "p99_response_time": 0,
        "requests_per_second": 0,
    }

    with open(csv_file, "r") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

        if not rows:
            return stats

        last_row = rows[-1]
        stats["total_requests"] = int(last_row.get("Requests", 0))
        stats["total_failures"] = int(last_row.get("Fails", 0))
        stats["avg_response_time"] = float(last_row.get("Average Response Time", 0))
        stats["p95_response_time"] = float(last_row.get("95%", 0))
        stats["p99_response_time"] = float(last_row.get("99%", 0))
        stats["requests_per_second"] = float(last_row.get("Requests/s", 0))

    return stats


def compare_results(flask_stats, fastapi_stats):
    """对比 Flask 和 FastAPI 结果"""
    if not flask_stats or not fastapi_stats:
        return None

    comparison = {}

    # 响应时间对比
    if flask_stats["avg_response_time"] > 0:
        improvement = (flask_stats["avg_response_time"] - fastapi_stats["avg_response_time"]) / flask_stats["avg_response_time"] * 100
        comparison["avg_response_time_improvement"] = improvement

    if flask_stats["p95_response_time"] > 0:
        improvement = (flask_stats["p95_response_time"] - fastapi_stats["p95_response_time"]) / flask_stats["p95_response_time"] * 100
        comparison["p95_response_time_improvement"] = improvement

    if flask_stats["p99_response_time"] > 0:
        improvement = (flask_stats["p99_response_time"] - fastapi_stats["p99_response_time"]) / flask_stats["p99_response_time"] * 100
        comparison["p99_response_time_improvement"] = improvement

    # 吞吐量对比
    if flask_stats["requests_per_second"] > 0:
        improvement = (fastapi_stats["requests_per_second"] - flask_stats["requests_per_second"]) / flask_stats["requests_per_second"] * 100
        comparison["throughput_improvement"] = improvement

    # 错误率对比
    if flask_stats["total_requests"] > 0:
        flask_error_rate = flask_stats["total_failures"] / flask_stats["total_requests"] * 100
        fastapi_error_rate = fastapi_stats["total_failures"] / fastapi_stats["total_requests"] * 100
        comparison["flask_error_rate"] = flask_error_rate
        comparison["fastapi_error_rate"] = fastapi_error_rate

    return comparison


def generate_report(flask_stats, fastapi_stats, comparison, output_file):
    """生成对比报告"""
    report = []
    report.append("# 性能基准测试结果分析报告")
    report.append(f"\n生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append("\n## Flask v1 统计")
    report.append(f"- 总请求数: {flask_stats['total_requests']}")
    report.append(f"- 失败请求数: {flask_stats['total_failures']}")
    report.append(f"- 平均响应时间: {flask_stats['avg_response_time']:.2f} ms")
    report.append(f"- P95 响应时间: {flask_stats['p95_response_time']:.2f} ms")
    report.append(f"- P99 响应时间: {flask_stats['p99_response_time']:.2f} ms")
    report.append(f"- 请求吞吐量: {flask_stats['requests_per_second']:.2f} req/s")

    report.append("\n## FastAPI v2 统计")
    report.append(f"- 总请求数: {fastapi_stats['total_requests']}")
    report.append(f"- 失败请求数: {fastapi_stats['total_failures']}")
    report.append(f"- 平均响应时间: {fastapi_stats['avg_response_time']:.2f} ms")
    report.append(f"- P95 响应时间: {fastapi_stats['p95_response_time']:.2f} ms")
    report.append(f"- P99 响应时间: {fastapi_stats['p99_response_time']:.2f} ms")
    report.append(f"- 请求吞吐量: {fastapi_stats['requests_per_second']:.2f} req/s")

    if comparison:
        report.append("\n## 性能对比")
        if "avg_response_time_improvement" in comparison:
            report.append(f"- 平均响应时间改进: {comparison['avg_response_time_improvement']:.1f}%")
        if "p95_response_time_improvement" in comparison:
            report.append(f"- P95 响应时间改进: {comparison['p95_response_time_improvement']:.1f}%")
        if "p99_response_time_improvement" in comparison:
            report.append(f"- P99 响应时间改进: {comparison['p99_response_time_improvement']:.1f}%")
        if "throughput_improvement" in comparison:
            report.append(f"- 吞吐量改进: {comparison['throughput_improvement']:.1f}%")
        if "flask_error_rate" in comparison:
            report.append(f"- Flask 错误率: {comparison['flask_error_rate']:.2f}%")
        if "fastapi_error_rate" in comparison:
            report.append(f"- FastAPI 错误率: {comparison['fastapi_error_rate']:.2f}%")

    report_text = "\n".join(report)

    with open(output_file, "w") as f:
        f.write(report_text)

    print(f"报告已生成: {output_file}")
    return report_text


def main():
    if len(sys.argv) < 3:
        print("用法: python analyze_results.py <flask_csv> <fastapi_csv> [output_file]")
        print("示例: python analyze_results.py reports/flask_v1_stats.csv reports/fastapi_v2_stats.csv report.md")
        sys.exit(1)

    flask_csv = sys.argv[1]
    fastapi_csv = sys.argv[2]
    output_file = sys.argv[3] if len(sys.argv) > 3 else "benchmark_report.md"

    flask_stats = parse_locust_csv(flask_csv)
    fastapi_stats = parse_locust_csv(fastapi_csv)

    if not flask_stats:
        print(f"错误: 无法解析 Flask CSV 文件: {flask_csv}")
        sys.exit(1)

    if not fastapi_stats:
        print(f"错误: 无法解析 FastAPI CSV 文件: {fastapi_csv}")
        sys.exit(1)

    comparison = compare_results(flask_stats, fastapi_stats)
    generate_report(flask_stats, fastapi_stats, comparison, output_file)


if __name__ == "__main__":
    main()
