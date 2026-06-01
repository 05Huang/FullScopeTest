#!/usr/bin/env python3
"""Safe i18n replacement script - only replaces Chinese in JSX attributes and text nodes, not inside string literals."""
import re
import sys
import json

# Translation map: Chinese text -> translation key
TRANSLATIONS = {
    # Common
    "加载中...": "common.loading",
    "暂无数据": "common.noData",
    "确认": "common.confirm",
    "取消": "common.cancel",
    "保存": "common.save",
    "删除": "common.delete",
    "编辑": "common.edit",
    "创建": "common.create",
    "搜索": "common.search",
    "刷新": "common.refresh",
    "导出": "common.export",
    "导入": "common.import",
    "重试": "common.retry",
    "关闭": "common.close",
    "提交": "common.submit",
    "重置": "common.reset",
    "返回": "common.back",
    "成功": "common.success",
    "失败": "common.failed",
    "执行中": "common.running",
    "等待中": "common.pending",
    "通过": "common.passed",
    "总计": "common.total",
    "操作": "common.actions",
    "状态": "common.status",
    "名称": "common.name",
    "描述": "common.description",
    "创建时间": "common.createdAt",
    "更新时间": "common.updatedAt",
    "类型": "common.type",
    
    # Dashboard
    "工作台": "dashboard.title",
    "测试执行趋势": "dashboard.testTrend",
    "测试类型分布": "dashboard.testDistribution",
    "最近测试执行": "dashboard.recentExecutions",
    "暂无测试记录": "dashboard.noRecords",
    "获取数据失败": "dashboard.fetchFailed",
    
    # Sidebar
    "接口测试": "sidebar.apiTest",
    "测试工作台": "sidebar.workspace",
    "测试集合": "sidebar.collections",
    "环境管理": "sidebar.environments",
    "Web自动化": "sidebar.webTest",
    "测试脚本": "sidebar.scripts",
    "APP测试": "sidebar.appTest",
    "性能测试": "sidebar.perfTest",
    "测试报告": "sidebar.reports",
    "CI/CD与定时任务": "sidebar.cicd",
    "测试文档": "sidebar.documents",
    "系统设置": "sidebar.settings",
    "个人中心": "sidebar.profile",
    
    # API Test
    "接口测试工作台": "apiTest.title",
    "新建集合": "apiTest.createCollection",
    "新建用例": "apiTest.createCase",
    "全部执行": "apiTest.runAll",
    "请求方法": "apiTest.method",
    "请求地址": "apiTest.url",
    "请求头": "apiTest.headers",
    "请求体": "apiTest.body",
    "查询参数": "apiTest.params",
    "响应结果": "apiTest.response",
    "状态码": "apiTest.status",
    "耗时": "apiTest.time",
    "大小": "apiTest.size",
    "断言": "apiTest.assertions",
    "前置脚本": "apiTest.preScript",
    "后置脚本": "apiTest.postScript",
    "暂无测试集合": "apiTest.noCollections",
    "暂无测试用例": "apiTest.noCases",
    "环境变量": "apiTest.environments.variables",
    "新建环境": "apiTest.environments.createEnv",
    "环境名称": "apiTest.environments.envName",
    "暂无环境配置": "apiTest.environments.noEnvironments",
    
    # Web Test
    "Web 自动化测试": "webTest.title",
    "新建脚本": "webTest.createScript",
    "执行脚本": "webTest.runScript",
    "编辑脚本": "webTest.editScript",
    "实时预览": "webTest.liveView",
    "视觉回归": "webTest.visualRegression",
    "暂无测试脚本": "webTest.noScripts",
    
    # Perf Test
    "性能测试": "perfTest.title",
    "新建场景": "perfTest.createScenario",
    "开始执行": "perfTest.runTest",
    "并发用户数": "perfTest.concurrentUsers",
    "响应时间": "perfTest.responseTime",
    "错误率": "perfTest.errorRate",
    "实时指标": "perfTest.realtimeMetrics",
    "历史对比": "perfTest.historyComparison",
    "告警规则": "perfTest.alertRules",
    "暂无测试场景": "perfTest.noScenarios",
    
    # Reports
    "测试报告": "reports.title",
    "暂无测试报告": "reports.noReports",
    "查看报告": "reports.viewReport",
    "导出报告": "reports.exportReport",
    "报告详情": "reports.reportDetails",
    "通过率": "reports.passRate",
    "执行时间": "reports.executionTime",
    "持续时间": "reports.duration",
    "用例总数": "reports.totalCases",
    "通过用例": "reports.passedCases",
    "失败用例": "reports.failedCases",
    
    # Settings
    "系统设置": "settings.title",
    
    # Documents
    "测试文档": "documents.title",
    
    # Notifications
    "通知": "notification.title",
    "暂无通知": "notification.noNotifications",
    
    # Copilot
    "AI Copilot": "copilot.title",
    "发送": "copilot.send",
    "思考中...": "copilot.thinking",
    
    # Search
    "搜索...": "search.placeholder",
    "未找到结果": "search.noResults",
}

def replace_chinese_in_file(filepath):
    """Replace Chinese text in JSX with t() calls, being careful not to break string literals."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if useTranslation is already imported
    has_import = "useTranslation" in content
    has_hook = "{ t }" in content or "{ t," in content
    
    # Only replace in specific patterns:
    # 1. In JSX text content: >中文< -> >{t('key')}<
    # 2. In JSX attributes: prop="中文" -> prop={t('key')}
    # 3. In template literals: `中文` -> {t('key')}
    # 4. In object properties: { text: '中文' } -> { text: t('key') }
    
    modified = content
    for chinese, key in TRANSLATIONS.items():
        escaped = re.escape(chinese)
        tk = f"t('{key}')"

        # Pattern 1: In JSX text content - >中文<
        pattern1 = rf'>(\s*){escaped}(\s*)<'
        replacement1 = rf'>\1{{{tk}}}\2<'
        modified = re.sub(pattern1, replacement1, modified)

        # Pattern 2: In JSX attributes - prop="中文"
        pattern2 = rf'="({escaped})"'
        replacement2 = rf'={{{tk}}}'
        modified = re.sub(pattern2, replacement2, modified)

        # Pattern 3: In object properties - text: '中文' or text: "中文"
        pattern3 = rf": '({escaped})'"
        replacement3 = f": {tk}"
        modified = re.sub(pattern3, replacement3, modified)

        # Pattern 4: In function call args - message.error('中文') or message.success('中文')
        # Also handles: || '中文' and other standalone string contexts
        pattern4 = rf"('{escaped}')"
        replacement4 = f"{tk}"
        modified = re.sub(pattern4, replacement4, modified)

        # Pattern 5: In template literals - `中文 ${var}` -> {t('key')} (only if entire content is Chinese)
        pattern5 = rf'`({escaped})`'
        replacement5 = f'{{{tk}}}'
        modified = re.sub(pattern5, replacement5, modified)

        # Pattern 6: In ternary - ? '中文' : or : '中文' }
        pattern6 = rf"\? '({escaped})' :"
        replacement6 = f"? {tk} :"
        modified = re.sub(pattern6, replacement6, modified)

        # Pattern 7: In ternary else - : '中文' }
        pattern7 = rf": '({escaped})' \}}"
        replacement7 = f": {tk} }}"
        modified = re.sub(pattern7, replacement7, modified)
    
    if modified != content:
        # Add import if not present
        if not has_import:
            modified = "import { useTranslation } from 'react-i18next';\n" + modified
        
        # Add hook call if not present
        if not has_hook:
            # Find the component function and add useTranslation after it
            # Look for patterns like: const ComponentName = () => {
            modified = re.sub(
                r'(const \w+[:\s].*?=\s*\(\)\s*=>\s*\{)',
                r'\1\n  const { t } = useTranslation();',
                modified,
                count=1
            )
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(modified)
        return True
    return False

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python i18n_replace.py <file1.tsx> [file2.tsx ...]")
        sys.exit(1)
    
    for filepath in sys.argv[1:]:
        try:
            if replace_chinese_in_file(filepath):
                print(f"OK {filepath}")
            else:
                print(f"SKIP {filepath} (no changes)")
        except Exception as e:
            print(f"ERR {filepath}: {e}")
