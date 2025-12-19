# 🎬 录制器快速开始指南

## ✅ 1 分钟快速开始

### 第一步：安装 Playwright（只需一次）

```bash
cd backend
.venv\Scripts\activate
pip install playwright
playwright install
```

### 第二步：使用 Web 界面录制

1. **打开录制器**
   ```
   Web 界面 → Web 测试 → 测试录制器
   ```

2. **输入网址并开始**
   - 输入目标 URL（如：`https://www.baidu.com`）
   - 选择浏览器（Chromium 推荐）
   - 点击 **"开始录制"** 按钮

3. **等待窗口打开**
   - 会自动打开两个窗口：
     - 📝 Playwright Inspector（左侧，显示代码）
     - 🌐 浏览器（右侧，用于操作）

4. **在浏览器中操作**
   - 像平常一样使用网站
   - 所有操作自动记录

5. **复制代码**
   - 在 Inspector 窗口中
   - 确保选择 **Python** 语言
   - 点击 **Copy** 按钮

6. **保存脚本**
   - 返回 Web 界面
   - 点击 **"保存脚本"**
   - 粘贴代码（调整格式）
   - 填写名称，点击创建

7. **运行测试**
   ```
   测试脚本 → 找到刚创建的脚本 → 点击"运行"
   ```

---

## 📝 代码格式模板

### Inspector 生成的代码（需要调整）

```python
from playwright.sync_api import Playwright, sync_playwright

def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    # ... 录制的操作 ...
    browser.close()

with sync_playwright() as playwright:
    run(playwright)
```

### 调整为 EasyTest 格式（复制此模板）

```python
"""
[脚本名称]
"""
from playwright.sync_api import sync_playwright, expect

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        try:
            # === 在这里粘贴 Inspector 中的操作代码 ===
            page.goto("https://example.com")
            # ... 其他操作 ...
            
            # === 添加等待 ===
            page.wait_for_load_state("networkidle")
            
            # === 添加断言 ===
            expect(page).to_have_title("预期标题")
            
            return {"status": "success"}
            
        except Exception as e:
            page.screenshot(path="error.png")
            return {"status": "failed", "error": str(e)}
            
        finally:
            browser.close()

if __name__ == "__main__":
    result = run()
    print(result)
```

---

## 🎯 完整示例

### 示例：录制百度搜索

**1. 录制的操作：**
- 打开 `https://www.baidu.com`
- 点击搜索框
- 输入 "playwright"
- 点击搜索按钮

**2. Inspector 生成的代码：**
```python
page.goto("https://www.baidu.com/")
page.click("#kw")
page.fill("#kw", "playwright")
page.click("#su")
```

**3. 调整后的完整脚本：**
```python
"""
百度搜索测试 - Playwright 关键词
"""
from playwright.sync_api import sync_playwright, expect

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        try:
            print("开始测试：百度搜索")
            
            # 访问百度
            page.goto("https://www.baidu.com/")
            print("✓ 已打开百度首页")
            
            # 填写搜索框
            page.click("#kw")
            page.fill("#kw", "playwright")
            print("✓ 已输入搜索关键词")
            
            # 点击搜索
            page.click("#su")
            print("✓ 已点击搜索按钮")
            
            # 等待结果加载
            page.wait_for_load_state("networkidle")
            page.wait_for_selector("#content_left")
            print("✓ 搜索结果已加载")
            
            # 断言：检查标题
            expect(page).to_have_title("playwright_百度搜索")
            print("✓ 页面标题正确")
            
            # 断言：检查搜索结果存在
            results = page.locator("#content_left .result")
            expect(results.first).to_be_visible()
            print(f"✓ 找到 {results.count()} 条搜索结果")
            
            # 截图保存
            page.screenshot(path="baidu_search_result.png")
            print("✓ 已保存截图")
            
            return {
                "status": "success",
                "message": "百度搜索测试通过",
                "result_count": results.count()
            }
            
        except Exception as e:
            print(f"✗ 测试失败: {e}")
            page.screenshot(path="baidu_search_error.png")
            return {"status": "failed", "error": str(e)}
            
        finally:
            browser.close()

if __name__ == "__main__":
    result = run()
    print("\n测试结果:", result)
```

---

## ⚡ 常用操作速查

### 点击操作
```python
page.click("#button")              # ID
page.click(".submit")              # Class
page.click("text=登录")            # 文本
page.click("button >> text=提交")  # 组合
```

### 输入操作
```python
page.fill("#input", "内容")        # 填写
page.type("#input", "内容", delay=100)  # 逐字输入
page.press("#input", "Enter")      # 按键
```

### 选择操作
```python
page.select_option("#select", "value")       # 下拉框
page.check("#checkbox")                       # 复选框
page.locator("input[value='option']").check() # 单选框
```

### 等待操作
```python
page.wait_for_load_state("networkidle")  # 等待网络空闲
page.wait_for_selector(".result")        # 等待元素出现
page.wait_for_timeout(1000)              # 等待 1 秒
```

### 断言操作
```python
from playwright.sync_api import expect

expect(page).to_have_title("标题")
expect(page).to_have_url("https://example.com")
expect(page.locator(".message")).to_be_visible()
expect(page.locator(".title")).to_contain_text("成功")
```

---

## ❓ 常见问题

### Q1: 点击"开始录制"没反应？
**检查清单：**
- [ ] 后端服务在本地运行（不是远程服务器）
- [ ] Playwright 已安装：`playwright --version`
- [ ] 浏览器驱动已安装：`playwright install`
- [ ] 查看浏览器控制台错误信息

### Q2: 窗口打开了但看不到代码？
- 确保 Inspector 窗口没有被最小化
- 调整窗口位置和大小
- 检查语言选择是否为 Python

### Q3: 代码粘贴后无法运行？
- 检查代码格式是否正确
- 是否使用了推荐的模板结构
- 是否添加了 `def run()` 函数
- 是否设置了 `headless=True`

### Q4: 如何录制登录后的操作？
**方法1：保存登录状态**
```python
# 首次登录并保存状态
context = browser.new_context()
page = context.new_page()
# ... 执行登录 ...
context.storage_state(path="auth.json")

# 后续使用保存的状态
context = browser.new_context(storage_state="auth.json")
page = context.new_page()
# 已登录，继续操作
```

**方法2：录制完整流程**
- 从登录页开始录制
- 包含登录步骤
- 继续录制后续操作

---

## 🎓 学习资源

- **Playwright 官方文档**: https://playwright.dev/python/
- **EasyTest 用户手册**: [USER_MANUAL.md](USER_MANUAL.md)
- **详细录制指南**: [PLAYWRIGHT_RECORDING_GUIDE.md](PLAYWRIGHT_RECORDING_GUIDE.md)

---

## 💡 最佳实践

1. **先录制，后优化**
   - 使用录制器快速生成基础代码
   - 手动添加等待、断言、错误处理

2. **合理使用等待**
   - 优先使用 `wait_for_selector()`
   - 避免固定时间等待 `wait_for_timeout()`

3. **添加详细断言**
   - 不仅检查元素存在
   - 还要验证内容正确性

4. **优化定位器**
   - 优先使用 ID、Test ID
   - 避免使用复杂的 CSS/XPath

5. **添加日志输出**
   - 使用 `print()` 记录执行步骤
   - 便于调试和查看进度

6. **错误处理**
   - 使用 try-except 捕获异常
   - 失败时保存截图

---

开始使用吧！🚀 只需 1 分钟即可完成第一个录制测试！
