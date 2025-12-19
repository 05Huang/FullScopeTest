# Playwright 录制功能使用指南

## 📌 重要说明

EasyTest 现在支持**直接从 Web 界面启动录制器**！🎉

只需点击按钮，系统会自动启动 Playwright Inspector 和浏览器，无需手动输入命令。

**前提条件：** 后端服务必须在**本地运行**（远程服务器无法使用此功能）。

---

## 🚀 推荐方案：使用 Web 界面录制（最简单）

### 1. 前置准备

确保已安装 Playwright：

```bash
# 进入后端目录
cd backend

# 激活虚拟环境
.venv\Scripts\activate

# 安装 Playwright
pip install playwright

# 安装浏览器驱动
playwright install
```

### 2. 从 Web 界面启动录制

**操作步骤：**

1. **打开录制器页面**
   - 登录 EasyTest
   - 点击左侧菜单："Web 测试" → "测试录制器"

2. **配置录制参数**
   - 输入**目标 URL**：如 `https://www.baidu.com`
   - 选择**浏览器**：Chromium / Firefox / WebKit

3. **点击"开始录制"按钮**
   - 系统会自动启动两个窗口：
     - 📝 **Playwright Inspector**：显示生成的代码
     - 🌐 **浏览器窗口**：进行实际操作

4. **在浏览器中操作**
   - 像平常一样使用网站
   - 所有操作会被自动记录
   - Inspector 实时显示生成的代码

5. **复制生成的代码**
   - 在 Playwright Inspector 窗口
   - 确保语言选择为 **Python**
   - 点击 "Copy" 按钮复制所有代码

6. **保存到 EasyTest**
   - 返回 Web 界面
   - 点击"保存脚本"按钮
   - 粘贴复制的代码（需要调整格式）
   - 填写脚本名称和描述
   - 点击"创建"保存

7. **运行测试**
   - 在"测试脚本"列表中找到刚创建的脚本
   - 点击"运行"按钮执行

### 3. 代码格式调整

从 Inspector 复制的代码需要调整为 EasyTest 格式：

**原始代码（从 Inspector 复制）：**
```python
from playwright.sync_api import Playwright, sync_playwright

def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    
    page.goto("https://www.baidu.com/")
    page.click("#kw")
    page.fill("#kw", "playwright")
    page.click("#su")
    
    context.close()
    browser.close()

with sync_playwright() as playwright:
    run(playwright)
```

**调整后的代码（适配 EasyTest）：**
```python
"""
百度搜索测试
录制时间: 2025-12-24
"""
from playwright.sync_api import sync_playwright, expect

def run():
    with sync_playwright() as p:
        # 启动浏览器（headless=True 用于后台运行）
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        try:
            # === 从 Inspector 复制的操作 ===
            page.goto("https://www.baidu.com/")
            page.click("#kw")
            page.fill("#kw", "playwright")
            page.click("#su")
            
            # === 添加等待和断言 ===
            page.wait_for_load_state("networkidle")
            expect(page).to_have_title("playwright_百度搜索")
            
            # 截图
            page.screenshot(path="search_result.png")
            
            return {"status": "success", "message": "搜索测试通过"}
            
        except Exception as e:
            # 错误处理
            page.screenshot(path="error.png")
            return {"status": "failed", "error": str(e)}
            
        finally:
            browser.close()

if __name__ == "__main__":
    result = run()
    print(result)
```

### 4. 优化录制的脚本

**添加等待：**
```python
# 等待页面加载
page.wait_for_load_state("networkidle")

# 等待元素出现
page.wait_for_selector(".results")

# 等待特定时间
page.wait_for_timeout(1000)
```

**添加断言：**
```python
from playwright.sync_api import expect

# 检查标题
expect(page).to_have_title("预期标题")

# 检查元素可见
expect(page.locator(".success")).to_be_visible()

# 检查文本内容
expect(page.locator(".message")).to_contain_text("成功")
```

**错误处理：**
```python
try:
    page.click("#submit")
except Exception as e:
    print(f"操作失败: {e}")
    page.screenshot(path="error.png")
    raise
```

### 5. 常见问题

**Q1: 点击"开始录制"后没有窗口打开？**
- 检查 Playwright 是否安装：`playwright --version`
- 确认浏览器驱动已安装：`playwright install`
- 查看浏览器控制台是否有错误

**Q2: 提示"Playwright 未安装"？**
```bash
cd backend
pip install playwright
playwright install
```

**Q3: 远程服务器能用吗？**
- 不能，录制器必须在本地运行
- 远程服务器没有图形界面，无法显示浏览器窗口

**Q4: 如何停止录制？**
- 方法1：关闭 Playwright Inspector 窗口
- 方法2：在 Web 界面点击"停止"按钮

---

## 🛠️ 方案二：使用 Playwright CLI 录制

Playwright Codegen 是官方提供的代码生成工具，可以录制浏览器操作并生成测试代码。

### 1. 安装 Playwright

如果还未安装，请先安装 Playwright：

```bash
# 进入后端目录
cd backend

# 激活虚拟环境（如果使用）
# Windows
.venv\Scripts\activate
# Linux/Mac
source .venv/bin/activate

# 安装 Playwright
pip install playwright

# 安装浏览器驱动
playwright install
```

**验证安装：**
```bash
playwright --version
# 应输出：Version 1.x.x
```

### 2. 启动录制器

```bash
# 基本用法：录制指定网站
playwright codegen https://example.com

# 指定浏览器
playwright codegen --browser=chromium https://baidu.com
playwright codegen --browser=firefox https://github.com
playwright codegen --browser=webkit https://apple.com

# 录制移动端网站
playwright codegen --device="iPhone 13" https://m.taobao.com
playwright codegen --device="Pixel 5" https://mobile.twitter.com

# 指定窗口大小
playwright codegen --viewport-size=1920,1080 https://example.com

# 保存存储状态（cookies、localStorage）
playwright codegen --save-storage=auth.json https://example.com

# 加载已保存的存储状态
playwright codegen --load-storage=auth.json https://example.com
```

### 3. 录制操作

命令执行后会打开两个窗口：

**浏览器窗口：**
- 用于执行实际操作
- 地址栏会显示正在录制的指示
- 像正常浏览网页一样操作

**Playwright Inspector 窗口：**
- 实时显示生成的代码
- 可以选择语言：Python、JavaScript、TypeScript、C#、Java
- 显示每个操作对应的代码

**录制步骤：**
1. 在浏览器窗口中进行操作
2. 观察 Inspector 中实时生成的代码
3. 支持的操作：
   - ✅ 页面导航
   - ✅ 点击按钮、链接
   - ✅ 填写表单
   - ✅ 选择下拉框
   - ✅ 勾选复选框/单选框
   - ✅ 文件上传
   - ✅ 拖拽
   - ✅ 右键菜单
   - ✅ 悬停操作

### 4. 复制代码

录制完成后：

1. 在 Playwright Inspector 中选择 **Python** 语言
2. 点击"Copy"按钮复制所有代码
3. 或手动选择并复制代码

**生成的代码示例：**

```python
from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    
    # 录制的操作
    page.goto("https://www.baidu.com/")
    page.get_by_role("textbox", name="搜索").click()
    page.get_by_role("textbox", name="搜索").fill("playwright")
    page.get_by_role("button", name="百度一下").click()
    page.get_by_role("link", name="Playwright: Fast and reliable end-to-end").click()
    
    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
```

### 5. 导入到 EasyTest

1. 登录 EasyTest Web 界面
2. 导航到"Web 测试" → "测试脚本"
3. 点击"新建脚本"
4. 填写信息：
   - **脚本名称**：如"百度搜索测试"
   - **目标 URL**：https://www.baidu.com
   - **浏览器**：chromium
   - **描述**：百度搜索功能测试
5. 在"脚本内容"编辑器中粘贴录制的代码
6. **调整代码格式**（重要）：

```python
"""
百度搜索测试脚本
录制时间: 2025-12-24
"""
from playwright.sync_api import sync_playwright, expect

def run():
    with sync_playwright() as p:
        # 启动浏览器（设置 headless=True 用于后台运行）
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        # 录制的操作（从 codegen 复制的代码）
        page.goto("https://www.baidu.com/")
        page.get_by_role("textbox", name="搜索").click()
        page.get_by_role("textbox", name="搜索").fill("playwright")
        page.get_by_role("button", name="百度一下").click()
        
        # 等待搜索结果加载
        page.wait_for_load_state("networkidle")
        
        # 添加断言
        expect(page).to_have_title("playwright_百度搜索")
        
        # 截图保存
        page.screenshot(path="search_result.png")
        
        # 关闭浏览器
        browser.close()
        
        return {"status": "success", "message": "搜索测试通过"}

if __name__ == "__main__":
    result = run()
    print(result)
```

7. 点击"创建"保存脚本
8. 点击"运行"执行测试

### 6. 优化录制的代码

Codegen 生成的代码可能需要优化：

**添加等待：**
```python
# 等待页面加载完成
page.wait_for_load_state("networkidle")

# 等待特定元素出现
page.wait_for_selector(".search-results")

# 等待特定时间
page.wait_for_timeout(1000)  # 等待1秒
```

**添加断言：**
```python
from playwright.sync_api import expect

# 检查页面标题
expect(page).to_have_title("预期标题")

# 检查元素是否可见
expect(page.locator(".success-message")).to_be_visible()

# 检查文本内容
expect(page.locator(".result")).to_contain_text("成功")

# 检查 URL
expect(page).to_have_url("https://example.com/success")
```

**错误处理：**
```python
try:
    page.click("#submit-button", timeout=5000)
except Exception as e:
    print(f"点击失败: {e}")
    page.screenshot(path="error.png")
    raise
```

**设置 headless 模式：**
```python
# 录制时使用 headless=False（可见浏览器）
browser = p.chromium.launch(headless=False)

# 生产环境使用 headless=True（后台运行）
browser = p.chromium.launch(headless=True)
```

---

## 🛠️ 方案二：使用 Playwright Inspector

Playwright Inspector 提供更强大的调试功能。

### 启动 Inspector

```bash
# 使用环境变量启动
PWDEBUG=1 python your_test.py

# Windows PowerShell
$env:PWDEBUG=1; python your_test.py

# Windows CMD
set PWDEBUG=1 && python your_test.py
```

### Inspector 功能

**1. 逐步执行**
- 暂停脚本执行
- 单步调试
- 查看每步的效果

**2. 选择器检查**
- 点击"Pick Locator"
- 在浏览器中点击元素
- 自动生成最优定位器

**3. 元素高亮**
- 悬停在代码上查看对应元素
- 验证定位器是否正确

**4. 控制台**
- 执行 Playwright 命令
- 测试定位器
- 调试脚本

---

## 📝 方案三：手动编写脚本

如果不需要录制，可以直接编写 Playwright 脚本。

### 基础模板

```python
"""
自定义 Playwright 测试脚本
"""
from playwright.sync_api import sync_playwright, expect

def run():
    with sync_playwright() as p:
        # 1. 启动浏览器
        browser = p.chromium.launch(headless=True)
        
        # 2. 创建浏览器上下文（可设置 cookies、权限等）
        context = browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Custom User Agent',
            locale='zh-CN',
            timezone_id='Asia/Shanghai'
        )
        
        # 3. 创建页面
        page = context.new_page()
        
        try:
            # 4. 执行测试步骤
            page.goto("https://example.com")
            
            # 你的测试代码...
            
            # 5. 断言
            expect(page).to_have_title("Expected Title")
            
            # 6. 截图
            page.screenshot(path="result.png")
            
            return {"status": "success"}
            
        except Exception as e:
            # 错误处理
            page.screenshot(path="error.png")
            return {"status": "failed", "error": str(e)}
            
        finally:
            # 7. 清理
            context.close()
            browser.close()

if __name__ == "__main__":
    result = run()
    print(result)
```

### 常用操作参考

#### 导航操作
```python
# 访问 URL
page.goto("https://example.com")

# 后退
page.go_back()

# 前进
page.go_forward()

# 刷新
page.reload()

# 等待导航完成
page.wait_for_load_state("load")  # load, domcontentloaded, networkidle
```

#### 元素定位
```python
# CSS 选择器
page.locator("#id")
page.locator(".class")
page.locator("div > p")

# 文本匹配
page.locator("text=登录")
page.locator("text=/正则表达式/")

# 角色定位（推荐）
page.get_by_role("button", name="提交")
page.get_by_role("textbox", name="用户名")
page.get_by_role("link", name="首页")

# 标签定位
page.get_by_label("用户名")

# 占位符定位
page.get_by_placeholder("请输入手机号")

# 测试 ID 定位
page.get_by_test_id("submit-button")
```

#### 交互操作
```python
# 点击
page.click("#button")
page.click("text=提交")
page.double_click("#item")
page.click("#button", button="right")  # 右键点击

# 输入
page.fill("#input", "文本内容")
page.type("#input", "逐字输入", delay=100)
page.press("#input", "Enter")

# 清空
page.fill("#input", "")

# 选择
page.select_option("#select", "value")
page.select_option("#select", label="选项文本")

# 复选框
page.check("#checkbox")
page.uncheck("#checkbox")

# 单选框
page.check("input[type=radio][value=yes]")

# 悬停
page.hover("#menu")

# 拖拽
page.drag_and_drop("#source", "#target")

# 文件上传
page.set_input_files("#file", "path/to/file.txt")
page.set_input_files("#file", ["file1.txt", "file2.txt"])  # 多文件
```

#### 等待操作
```python
# 等待时间
page.wait_for_timeout(1000)  # 毫秒

# 等待元素
page.wait_for_selector(".result")
page.wait_for_selector(".loading", state="hidden")  # 等待元素消失

# 等待导航
page.wait_for_load_state("networkidle")

# 等待函数返回 true
page.wait_for_function("window.loadComplete === true")

# 等待事件
with page.expect_navigation():
    page.click("#submit")

with page.expect_popup() as popup_info:
    page.click("#open-popup")
popup = popup_info.value
```

#### 获取信息
```python
# 获取文本
text = page.inner_text(".title")
text = page.text_content(".description")

# 获取 HTML
html = page.inner_html(".content")

# 获取属性
href = page.get_attribute("a", "href")
src = page.get_attribute("img", "src")

# 获取输入值
value = page.input_value("#input")

# 检查元素状态
is_visible = page.is_visible(".element")
is_enabled = page.is_enabled("#button")
is_checked = page.is_checked("#checkbox")

# 获取元素数量
count = page.locator(".item").count()

# 获取页面信息
title = page.title()
url = page.url()
```

#### 断言
```python
from playwright.sync_api import expect

# 页面断言
expect(page).to_have_title("标题")
expect(page).to_have_url("https://example.com")

# 元素断言
expect(page.locator(".message")).to_be_visible()
expect(page.locator(".error")).to_be_hidden()
expect(page.locator(".title")).to_contain_text("成功")
expect(page.locator(".title")).to_have_text("完全匹配")
expect(page.locator(".count")).to_have_count(5)
expect(page.locator("#input")).to_have_value("预期值")
expect(page.locator("#input")).to_be_enabled()
expect(page.locator("#checkbox")).to_be_checked()

# 自定义断言
assert page.title() == "预期标题", "标题不匹配"
```

#### 截图和录制
```python
# 整页截图
page.screenshot(path="screenshot.png")

# 全页截图（包括滚动部分）
page.screenshot(path="full.png", full_page=True)

# 元素截图
page.locator(".header").screenshot(path="header.png")

# 录制视频（需要在 context 创建时配置）
context = browser.new_context(
    record_video_dir="videos/"
)
# 测试完成后视频自动保存
```

---

## 🎯 最佳实践

### 1. 使用页面对象模式（POM）

```python
class LoginPage:
    def __init__(self, page):
        self.page = page
        self.username_input = page.locator("#username")
        self.password_input = page.locator("#password")
        self.login_button = page.locator("button[type=submit]")
    
    def login(self, username, password):
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.login_button.click()
        self.page.wait_for_load_state("networkidle")

# 使用
def run():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        
        login_page = LoginPage(page)
        page.goto("https://example.com/login")
        login_page.login("admin", "password")
        
        browser.close()
```

### 2. 优先使用语义化定位器

```python
# ✅ 推荐：使用角色和文本
page.get_by_role("button", name="登录")
page.get_by_label("用户名")
page.get_by_placeholder("请输入密码")

# ❌ 不推荐：使用 CSS/XPath
page.locator("#btn-login")
page.locator("//button[@id='login']")
```

### 3. 添加适当的等待

```python
# ✅ 显式等待
page.wait_for_selector(".results")
expect(page.locator(".loading")).to_be_hidden()

# ❌ 避免固定等待
page.wait_for_timeout(3000)  # 不够灵活
```

### 4. 处理动态内容

```python
# 等待元素稳定
page.wait_for_load_state("networkidle")

# 重试机制
for i in range(3):
    try:
        page.click("#dynamic-button", timeout=2000)
        break
    except:
        page.wait_for_timeout(500)
```

### 5. 保存测试状态

```python
# 保存登录状态
context = browser.new_context()
page = context.new_page()
# ... 执行登录 ...
context.storage_state(path="auth.json")

# 复用登录状态
context = browser.new_context(storage_state="auth.json")
page = context.new_page()
# 已登录，无需重复登录
```

---

## 🔧 故障排查

### 问题1：Playwright 未安装

**错误：** `ModuleNotFoundError: No module named 'playwright'`

**解决：**
```bash
pip install playwright
playwright install
```

### 问题2：浏览器驱动未安装

**错误：** `Executable doesn't exist`

**解决：**
```bash
playwright install chromium
playwright install firefox
playwright install webkit
```

### 问题3：元素定位失败

**错误：** `TimeoutError: Timeout 30000ms exceeded`

**排查步骤：**
1. 检查定位器是否正确
2. 增加等待时间
3. 使用 Inspector 调试

```python
# 增加超时时间
page.click("#button", timeout=60000)

# 等待元素出现
page.wait_for_selector("#button")
```

### 问题4：无头模式运行失败

**解决：** 先使用可见模式调试
```python
browser = p.chromium.launch(headless=False, slow_mo=100)
```

---

## 📚 参考资源

- **Playwright 官方文档**：https://playwright.dev/python/
- **Playwright API 参考**：https://playwright.dev/python/docs/api/class-playwright
- **Codegen 文档**：https://playwright.dev/python/docs/codegen
- **示例代码**：https://github.com/microsoft/playwright-python/tree/main/examples

---

## 💡 总结

1. **EasyTest 录制器暂不可用** - 使用 Playwright Codegen 替代
2. **本地录制** - `playwright codegen https://example.com`
3. **复制代码** - 从 Inspector 复制 Python 代码
4. **导入 EasyTest** - 粘贴到脚本管理中
5. **调整优化** - 添加断言、等待、错误处理
6. **运行测试** - 在 EasyTest 中执行

通过这种方式，您仍然可以享受可视化录制的便利，并在 EasyTest 平台上管理和执行测试！
