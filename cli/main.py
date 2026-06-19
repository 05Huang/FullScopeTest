"""
FullScopeTest CLI 工具

使用方式:
    fst run --collection 123 --env staging
    fst run --tag smoke
    fst report --format junit --output report.xml
    fst import --har traffic.har --project 1
    fst health
"""

import argparse
import json
import sys
import os
from urllib.parse import urljoin

# 延迟导入 requests，仅在实际使用时需要
def _get_session():
    """创建 API 会话"""
    try:
        import requests
    except ImportError:
        print("错误: 请先安装 requests 库: pip install requests")
        sys.exit(1)

    base_url = os.environ.get('FST_API_URL', 'http://localhost:5211/api/v1')
    api_key = os.environ.get('FST_API_KEY', '')
    token = os.environ.get('FST_TOKEN', '')

    session = requests.Session()
    session.headers.update({'Content-Type': 'application/json'})

    if api_key:
        session.headers['X-API-Key'] = api_key
    elif token:
        session.headers['Authorization'] = f'Bearer {token}'
    else:
        print("警告: 未设置 FST_API_KEY 或 FST_TOKEN 环境变量")

    return session, base_url


def cmd_health(args):
    """健康检查"""
    session, base_url = _get_session()
    try:
        resp = session.get(f'{base_url}/api-test/health', timeout=10)
        data = resp.json()
        print(f"✓ API 状态: {data.get('message', 'OK')}")
        print(f"  服务器: {os.environ.get('FST_API_URL', 'http://localhost:5211/api/v1')}")
    except Exception as exc:
        print(f"✗ 连接失败: {exc}")
        sys.exit(1)


def cmd_run(args):
    """执行测试"""
    session, base_url = _get_session()

    if args.collection:
        # 执行用例集
        print(f"执行用例集 #{args.collection}...")
        resp = session.post(
            f'{base_url}/api-test/collections/{args.collection}/run',
            json={'env_id': args.env},
            timeout=args.timeout or 300,
        )
    elif args.tag:
        # 按标签执行
        print(f"按标签 '{args.tag}' 执行...")
        resp = session.post(
            f'{base_url}/api-test/tags/filter',
            json={'tags': args.tag.split(',')},
            timeout=30,
        )
        if resp.status_code == 200:
            data = resp.json().get('data', [])
            print(f"  找到 {len(data)} 个匹配用例")
            if not data:
                print("  无匹配用例，退出")
                return
            # 执行找到的用例
            case_ids = [c['id'] for c in data if 'id' in c]
            if args.case:
                # 如果也指定了 case，执行单个用例
                pass
        else:
            print(f"✗ 查询失败: {resp.text}")
            sys.exit(1)
    elif args.case:
        # 执行单个用例
        print(f"执行用例 #{args.case}...")
        resp = session.post(
            f'{base_url}/api-test/cases/{args.case}/run',
            params={'env_id': args.env} if args.env else {},
            timeout=args.timeout or 60,
        )
    else:
        print("错误: 请指定 --collection, --tag, 或 --case")
        sys.exit(1)

    if resp.status_code == 200:
        data = resp.json().get('data', {})
        print(f"✓ 执行完成")
        if isinstance(data, dict):
            for key in ('passed', 'failed', 'total', 'pass_rate', 'status'):
                if key in data:
                    print(f"  {key}: {data[key]}")
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"  结果已保存到: {args.output}")
    else:
        print(f"✗ 执行失败 ({resp.status_code}): {resp.text[:200]}")
        sys.exit(1)


def cmd_report(args):
    """导出报告"""
    session, base_url = _get_session()

    if not args.run_id:
        print("错误: 请指定 --run-id")
        sys.exit(1)

    fmt = args.format or 'json'
    output = args.output or f'report.{fmt}'

    print(f"导出报告 #{args.run_id} (格式: {fmt})...")

    resp = session.get(f'{base_url}/reports/{args.run_id}', timeout=30)
    if resp.status_code != 200:
        print(f"✗ 获取报告失败: {resp.text[:200]}")
        sys.exit(1)

    data = resp.json().get('data', {})

    if fmt == 'json':
        with open(output, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    elif fmt == 'junit':
        # 生成 JUnit XML
        _generate_junit(data, output)
    elif fmt == 'csv':
        _generate_csv(data, output)
    else:
        print(f"错误: 不支持的格式 '{fmt}'，支持: json, junit, csv")
        sys.exit(1)

    print(f"✓ 报告已导出到: {output}")


def cmd_import(args):
    """导入文件"""
    session, base_url = _get_session()

    if not args.file:
        print("错误: 请指定 --file")
        sys.exit(1)

    if not os.path.exists(args.file):
        print(f"错误: 文件不存在: {args.file}")
        sys.exit(1)

    project_id = args.project or 1
    fmt = args.format or 'har'

    with open(args.file, 'r', encoding='utf-8') as f:
        content = f.read()

    if fmt == 'har':
        print(f"导入 HAR 文件: {args.file}...")
        resp = session.post(
            f'{base_url}/api-test/import-har',
            json={'har_content': content, 'project_id': project_id},
            timeout=60,
        )
    elif fmt == 'curl':
        print(f"导入 cURL: {args.file}...")
        resp = session.post(
            f'{base_url}/api-test/import-curl',
            json={'curl_text': content, 'project_id': project_id},
            timeout=30,
        )
    else:
        print(f"错误: 不支持的格式 '{fmt}'，支持: har, curl")
        sys.exit(1)

    if resp.status_code == 200:
        data = resp.json().get('data', {})
        count = data.get('cases_count', 0) or data.get('imported', 0)
        print(f"✓ 导入完成: {count} 个用例")
        if data.get('collection_id'):
            print(f"  集合 ID: {data['collection_id']}")
    else:
        print(f"✗ 导入失败 ({resp.status_code}): {resp.text[:200]}")
        sys.exit(1)


def cmd_config(args):
    """查看/设置配置"""
    config_file = os.path.expanduser('~/.fst/config.json')

    if args.show:
        config = {}
        if os.path.exists(config_file):
            with open(config_file, 'r') as f:
                config = json.load(f)
        # 也显示环境变量
        print("FST 配置:")
        print(f"  API URL: {os.environ.get('FST_API_URL', config.get('api_url', 'http://localhost:5211/api/v1'))}")
        print(f"  API Key: {'***' if os.environ.get('FST_API_KEY') or config.get('api_key') else '(未设置)'}")
        print(f"  Token:   {'***' if os.environ.get('FST_TOKEN') or config.get('token') else '(未设置)'}")
        return

    if args.set_api_url:
        os.makedirs(os.path.dirname(config_file), exist_ok=True)
        config = {}
        if os.path.exists(config_file):
            with open(config_file, 'r') as f:
                config = json.load(f)
        config['api_url'] = args.set_api_url
        with open(config_file, 'w') as f:
            json.dump(config, f, indent=2)
        print(f"✓ API URL 已设置: {args.set_api_url}")


def _generate_junit(data, output):
    """生成 JUnit XML 报告"""
    try:
        import xml.etree.ElementTree as ET
        from xml.dom import minidom

        testsuite = ET.Element('testsuite')
        testsuite.set('name', data.get('name', 'FullScopeTest Report'))
        testsuite.set('tests', str(data.get('total', 0)))
        testsuite.set('failures', str(data.get('failed', 0)))

        results = data.get('results', [])
        for r in results:
            tc = ET.SubElement(testsuite, 'testcase')
            tc.set('name', r.get('name', 'unknown'))
            tc.set('classname', r.get('collection', ''))
            tc.set('time', str(r.get('duration', 0) / 1000))

            if r.get('status') == 'failed':
                failure = ET.SubElement(tc, 'failure')
                failure.set('message', r.get('error', 'Unknown error'))
                failure.text = r.get('response_body', '')[:1000]

        rough = ET.tostring(testsuite, encoding='unicode')
        pretty = minidom.parseString(rough).toprettyxml(indent='  ')
        with open(output, 'w', encoding='utf-8') as f:
            f.write(pretty)
    except Exception as exc:
        print(f"  JUnit 生成失败: {exc}")
        # 回退到 JSON
        with open(output.replace('.xml', '.json'), 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)


def _generate_csv(data, output):
    """生成 CSV 报告"""
    import csv
    results = data.get('results', [])
    with open(output, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['name', 'method', 'url', 'status', 'duration', 'error'])
        writer.writeheader()
        for r in results:
            writer.writerow({
                'name': r.get('name', ''),
                'method': r.get('method', ''),
                'url': r.get('url', ''),
                'status': r.get('status', ''),
                'duration': r.get('duration', 0),
                'error': r.get('error', ''),
            })


def main():
    parser = argparse.ArgumentParser(
        prog='fst',
        description='FullScopeTest CLI - 测试平台命令行工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  fst health                                    检查 API 状态
  fst run --collection 123 --env staging        执行用例集
  fst run --tag smoke                           按标签执行
  fst run --case 456                            执行单个用例
  fst report --run-id 789 --format junit        导出 JUnit 报告
  fst import --har traffic.har --project 1      导入 HAR 文件
  fst config --show                             查看配置
  fst config --set-api-url https://api.fst.com  设置 API 地址
        """,
    )

    subparsers = parser.add_subparsers(dest='command', help='子命令')

    # health
    subparsers.add_parser('health', help='检查 API 健康状态')

    # run
    p_run = subparsers.add_parser('run', help='执行测试')
    p_run.add_argument('--collection', type=int, help='用例集 ID')
    p_run.add_argument('--case', type=int, help='单个用例 ID')
    p_run.add_argument('--tag', help='按标签执行（逗号分隔）')
    p_run.add_argument('--env', type=int, help='环境 ID')
    p_run.add_argument('--timeout', type=int, help='超时秒数')
    p_run.add_argument('--output', '-o', help='输出文件')

    # report
    p_report = subparsers.add_parser('report', help='导出报告')
    p_report.add_argument('--run-id', type=int, help='运行 ID')
    p_report.add_argument('--format', choices=['json', 'junit', 'csv'], default='json', help='输出格式')
    p_report.add_argument('--output', '-o', help='输出文件')

    # import
    p_import = subparsers.add_parser('import', help='导入文件')
    p_import.add_argument('--file', '-f', help='文件路径')
    p_import.add_argument('--format', choices=['har', 'curl'], default='har', help='文件格式')
    p_import.add_argument('--project', type=int, help='目标项目 ID')

    # config
    p_config = subparsers.add_parser('config', help='查看/设置配置')
    p_config.add_argument('--show', action='store_true', help='显示当前配置')
    p_config.add_argument('--set-api-url', help='设置 API 地址')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(0)

    commands = {
        'health': cmd_health,
        'run': cmd_run,
        'report': cmd_report,
        'import': cmd_import,
        'config': cmd_config,
    }
    commands[args.command](args)


if __name__ == '__main__':
    main()
