"""
FullScopeTest CLI

提供命令行接口用于 CI/CD 集成。

用法：
    fst run --project-id 1 --type api
    fst list-runs --project-id 1
    fst create-case --project-id 1 --name "Login Test" --method POST --url "https://api.example.com/login"
    fst import-postman --project-id 1 --file collection.json
"""
import argparse
import json
import sys
import os

from .client import FullScopeTestClient


def get_client(args) -> FullScopeTestClient:
    """从参数创建客户端"""
    base_url = args.base_url or os.environ.get("FST_BASE_URL", "http://localhost:8000")
    api_token = args.api_token or os.environ.get("FST_API_TOKEN")
    jwt_token = args.jwt_token or os.environ.get("FST_JWT_TOKEN")

    if not api_token and not jwt_token:
        print("错误: 必须提供 --api-token 或 --jwt-token（或设置 FST_API_TOKEN/FST_JWT_TOKEN 环境变量）")
        sys.exit(1)

    return FullScopeTestClient(base_url=base_url, api_token=api_token, jwt_token=jwt_token)


def cmd_run(args):
    """执行测试"""
    client = get_client(args)
    result = client.create_test_run(
        project_id=args.project_id,
        test_type=args.type,
        test_object_name=args.name,
    )
    data = result.get("data", {})
    print(f"测试执行已创建: Run ID={data.get('id')}, Status={data.get('status')}")
    if args.wait:
        import time
        run_id = data["id"]
        while True:
            run = client.get_test_run(run_id)
            status = run.get("data", {}).get("status", "unknown")
            if status in ("success", "failed", "cancelled"):
                print(f"执行完成: Status={status}")
                print(json.dumps(run.get("data", {}), indent=2, ensure_ascii=False))
                break
            print(f"等待中... Status={status}")
            time.sleep(5)


def cmd_list_runs(args):
    """列出执行记录"""
    client = get_client(args)
    result = client.list_test_runs(project_id=args.project_id, test_type=args.type, page=args.page)
    data = result.get("data", {})
    items = data.get("items", [])
    print(f"共 {data.get('pagination', {}).get('total', 0)} 条记录:")
    for run in items:
        print(f"  #{run['id']} | {run['test_type']} | {run['status']} | {run.get('created_at', '')}")


def cmd_create_case(args):
    """创建测试用例"""
    client = get_client(args)
    result = client.create_test_case(
        project_id=args.project_id,
        name=args.name,
        method=args.method,
        url=args.url,
    )
    data = result.get("data", {})
    print(f"用例已创建: ID={data.get('id')}, Name={data.get('name')}")


def cmd_import_postman(args):
    """导入 Postman Collection"""
    client = get_client(args)
    with open(args.file, "r", encoding="utf-8") as f:
        content = f.read()
    result = client.import_postman(project_id=args.project_id, content=content)
    data = result.get("data", {})
    print(f"导入完成: Total={data.get('total')}, Imported={data.get('imported')}, Skipped={data.get('skipped')}")


def cmd_import_csv(args):
    """导入 CSV 用例"""
    client = get_client(args)
    with open(args.file, "r", encoding="utf-8") as f:
        content = f.read()
    result = client.import_csv(project_id=args.project_id, content=content)
    data = result.get("data", {})
    print(f"导入完成: Total={data.get('total')}, Imported={data.get('imported')}, Skipped={data.get('skipped')}")


def cmd_stats(args):
    """查看统计"""
    client = get_client(args)
    result = client.get_report_statistics(project_id=args.project_id, days=args.days)
    data = result.get("data", {})
    summary = data.get("summary", {})
    print(f"统计 ({args.days} 天):")
    print(f"  总执行: {summary.get('total_runs', 0)}")
    print(f"  成功: {summary.get('success_runs', 0)}")
    print(f"  失败: {summary.get('failed_runs', 0)}")
    print(f"  通过率: {summary.get('success_rate', 0)}%")


def main():
    parser = argparse.ArgumentParser(prog="fst", description="FullScopeTest CLI")
    parser.add_argument("--base-url", help="API 基础 URL")
    parser.add_argument("--api-token", help="API Token")
    parser.add_argument("--jwt-token", help="JWT Token")

    subparsers = parser.add_subparsers(dest="command", help="可用命令")

    # fst run
    p_run = subparsers.add_parser("run", help="执行测试")
    p_run.add_argument("--project-id", type=int, required=True, help="项目 ID")
    p_run.add_argument("--type", default="api", help="测试类型 (api/web/performance)")
    p_run.add_argument("--name", help="测试名称")
    p_run.add_argument("--wait", action="store_true", help="等待执行完成")
    p_run.set_defaults(func=cmd_run)

    # fst list-runs
    p_list = subparsers.add_parser("list-runs", help="列出执行记录")
    p_list.add_argument("--project-id", type=int, help="项目 ID")
    p_list.add_argument("--type", help="测试类型过滤")
    p_list.add_argument("--page", type=int, default=1, help="页码")
    p_list.set_defaults(func=cmd_list_runs)

    # fst create-case
    p_case = subparsers.add_parser("create-case", help="创建测试用例")
    p_case.add_argument("--project-id", type=int, required=True, help="项目 ID")
    p_case.add_argument("--name", required=True, help="用例名称")
    p_case.add_argument("--method", default="GET", help="HTTP 方法")
    p_case.add_argument("--url", required=True, help="请求 URL")
    p_case.set_defaults(func=cmd_create_case)

    # fst import-postman
    p_imp = subparsers.add_parser("import-postman", help="导入 Postman Collection")
    p_imp.add_argument("--project-id", type=int, required=True, help="项目 ID")
    p_imp.add_argument("--file", required=True, help="Postman JSON 文件路径")
    p_imp.set_defaults(func=cmd_import_postman)

    # fst import-csv
    p_csv = subparsers.add_parser("import-csv", help="导入 CSV 用例")
    p_csv.add_argument("--project-id", type=int, required=True, help="项目 ID")
    p_csv.add_argument("--file", required=True, help="CSV 文件路径")
    p_csv.set_defaults(func=cmd_import_csv)

    # fst stats
    p_stats = subparsers.add_parser("stats", help="查看统计")
    p_stats.add_argument("--project-id", type=int, help="项目 ID")
    p_stats.add_argument("--days", type=int, default=7, help="统计天数")
    p_stats.set_defaults(func=cmd_stats)

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(1)

    args.func(args)


if __name__ == "__main__":
    main()