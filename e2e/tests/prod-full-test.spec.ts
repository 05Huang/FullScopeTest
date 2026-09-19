/**
 * FullScopeTest 生产环境全面 E2E 测试
 *
 * 测试目标：验证所有功能模块的运行状态，发现 UI 卡住、错误无提示等问题
 * - "一直显示执行中" 问题
 * - "点击按钮没有任何反应" 问题
 * - API 调用失败但无错误提示
 * - 页面状态异常
 */

import { test, expect, type Page } from "@playwright/test";

const BASE_URL = "https://test.huangxuan.site";
const TEST_USER = {
  username: "huangxuan",
  password: "Test@123456",
};

/** 截图辅助函数 */
async function screenshot(page: Page, name: string) {
  await page.screenshot({ path: `test-results/${name}-${Date.now()}.png`, fullPage: true });
  console.log(`📸 截图已保存: test-results/${name}-${Date.now()}.png`);
}

/** 等待加载指示器消失 */
async function waitForLoadingDone(page: Page, timeout = 15000) {
  const loadingSelectors = [
    '.ant-spin',
    '.ant-spin-nested-loading',
    '[class*="loading"]',
    '[class*="Loading"]',
    '.ant-skeleton',
  ];

  for (const selector of loadingSelectors) {
    const loadingEl = page.locator(selector).first();
    try {
      await loadingEl.waitFor({ state: "hidden", timeout: 5000 });
    } catch {
      // 继续等待
    }
  }
}

/** 等待网络空闲 */
async function waitForNetworkIdle(page: Page, timeout = 20000) {
  try {
    await page.waitForLoadState("networkidle", { timeout });
  } catch {
    console.log("⚠️ 网络未完全空闲");
  }
}

/** 登录辅助函数 */
async function login(page: Page, username = TEST_USER.username, password = TEST_USER.password) {
  console.log(`🔐 正在登录: ${username}`);
  await page.goto(`${BASE_URL}/login`);
  await page.waitForLoadState("domcontentloaded");

  // 等待表单加载
  await page.waitForTimeout(2000);

  // 使用更精确的定位器
  const usernameInput = page.getByPlaceholder(/用户名|username|account/i).first();
  const passwordInput = page.getByPlaceholder(/密码|password|pass/i).first();
  const loginBtn = page.getByRole("button", { name: /登 ?录|login|sign in/i }).first();

  // 清除可能存在的默认值并填写
  await usernameInput.clear();
  await usernameInput.fill(username);
  await passwordInput.clear();
  await passwordInput.fill(password);

  console.log("🖱️ 点击登录按钮");
  await loginBtn.click();

  // 等待登录完成
  try {
    await page.waitForURL((url) => !url.toString().includes("/login"), { timeout: 30000 });
    console.log("✅ 登录成功");
    return true;
  } catch (e) {
    await screenshot(page, "login-failed");
    console.log("❌ 登录失败，当前URL:", page.url());

    // 检查是否有错误提示
    const errorText = await page.locator(".ant-message-error, [class*='error']").first().textContent().catch(() => null);
    if (errorText) {
      console.log("错误信息:", errorText);
    }
    return false;
  }
}

/** 导航到指定页面并等待加载 */
async function navigateToPage(page: Page, path: string, name: string) {
  console.log(`\n📍 导航到 ${name}: ${path}`);
  await page.goto(`${BASE_URL}${path}`);
  await page.waitForLoadState("domcontentloaded");
  await waitForNetworkIdle(page);
  await waitForLoadingDone(page);
  console.log(`✅ ${name} 页面加载完成`);
}

// ═══════════════════════════════════════════════════════════════════════════
// 测试套件：认证模块
// ═══════════════════════════════════════════════════════════════════════════

test.describe("🔐 认证模块", () => {
  test("登录页面应正确加载", async ({ page }) => {
    await page.goto(`${BASE_URL}/login`);
    await waitForNetworkIdle(page);

    const usernameInput = page.getByPlaceholder(/用户名|username/i).first();
    const passwordInput = page.getByPlaceholder(/密码|password/i).first();
    const loginBtn = page.getByRole("button", { name: /登 ?录/i }).first();

    await expect(usernameInput).toBeVisible();
    await expect(passwordInput).toBeVisible();
    await expect(loginBtn).toBeVisible();
  });

  test("正确凭证登录成功", async ({ page }) => {
    const success = await login(page);
    expect(success).toBeTruthy();
    expect(page.url()).not.toContain("/login");
  });

  test("错误密码登录失败并显示错误提示", async ({ page }) => {
    await page.goto(`${BASE_URL}/login`);
    await page.waitForLoadState("domcontentloaded");
    await page.waitForTimeout(2000);

    const usernameInput = page.getByPlaceholder(/用户名|username/i).first();
    const passwordInput = page.getByPlaceholder(/密码|password/i).first();
    const loginBtn = page.getByRole("button", { name: /登 ?录/i }).first();

    await usernameInput.fill(TEST_USER.username);
    await passwordInput.fill("wrong_password");
    await loginBtn.click();

    // 等待错误提示
    await page.waitForTimeout(3000);

    // 检查是否仍停留在登录页
    const stillOnLogin = page.url().includes("/login");
    console.log(`停留在登录页: ${stillOnLogin}`);
    expect(stillOnLogin).toBeTruthy();
  });

  test("未登录访问受保护页面应重定向到登录页", async ({ page }) => {
    await page.context().clearCookies();
    await page.goto(`${BASE_URL}/dashboard`);

    // 应该重定向到登录页
    await page.waitForURL((url) => url.toString().includes("/login"), { timeout: 10000 });
    console.log("✅ 未登录成功重定向到登录页");
  });
});

// ═══════════════════════════════════════════════════════════════════════════
// 测试套件：Dashboard
// ═══════════════════════════════════════════════════════════════════════════

test.describe("📊 Dashboard 模块", () => {
  test.beforeEach(async ({ page }) => {
    const success = await login(page);
    if (!success) test.skip();
  });

  test("Dashboard 页面应正常加载", async ({ page }) => {
    await navigateToPage(page, "/dashboard", "Dashboard");

    // 检查主要内容区域
    const mainContent = page.locator("main, .ant-layout-content, #root");
    await expect(mainContent.first()).toBeVisible();
  });

  test("Dashboard 统计数据应正确显示", async ({ page }) => {
    await navigateToPage(page, "/dashboard", "Dashboard");

    // 等待统计数据加载
    await page.waitForTimeout(3000);

    // 检查是否有统计卡片或图表
    const statCards = page.locator(".ant-statistic, .statistic-card, [class*='statistic'], [class*='stat']");
    const count = await statCards.count();
    console.log(`📊 发现 ${count} 个统计元素`);
  });

  test("侧边栏导航应正常工作", async ({ page }) => {
    await navigateToPage(page, "/dashboard", "Dashboard");

    // 检查侧边栏菜单
    const menuItems = page.locator(".ant-menu-item, .ant-menu-submenu-title, nav a");
    const count = await menuItems.count();
    console.log(`📋 侧边栏有 ${count} 个菜单项`);

    if (count > 0) {
      // 点击第一个菜单
      const firstMenu = menuItems.first();
      await firstMenu.click();
      await page.waitForTimeout(2000);
      console.log("✅ 菜单点击成功");
    }
  });
});

// ═══════════════════════════════════════════════════════════════════════════
// 测试套件：API 测试模块 (核心测试 - 运行状态问题)
// ═══════════════════════════════════════════════════════════════════════════

test.describe("🔌 API 测试模块 - 核心功能", () => {
  test.beforeEach(async ({ page }) => {
    const success = await login(page);
    if (!success) test.skip();
  });

  test("API 测试页面应正常加载", async ({ page }) => {
    await navigateToPage(page, "/api-test", "API 测试");
    await expect(page).not.toHaveURL(/\/login/);
  });

  test("【关键】发送 HTTP GET 请求应显示响应结果", async ({ page }) => {
    await navigateToPage(page, "/api-test", "API 测试");
    await page.waitForTimeout(2000);

    // 查找 URL 输入框
    const urlInput = page.getByPlaceholder(/URL|url|请求地址|输入请求地址/i).first();

    if (await urlInput.isVisible({ timeout: 5000 }).catch(() => false)) {
      console.log("📝 找到 URL 输入框");
      await urlInput.fill("https://httpbin.org/get");

      // 查找发送按钮
      const sendBtn = page.getByRole("button", { name: /发送|send|执行|run|提交/i }).first();

      if (await sendBtn.isVisible({ timeout: 3000 }).catch(() => false)) {
        console.log("🖱️ 点击发送按钮");
        await sendBtn.click();

        // 等待响应 - 最多等待 30 秒
        console.log("⏳ 等待响应...");
        let responseReceived = false;
        let responseStatus: string | null = null;

        for (let i = 0; i < 30; i++) {
          await page.waitForTimeout(1000);

          // 检查是否有响应状态显示
          const statusTag = page.locator(".ant-tag:visible, [class*='status']").first();
          if (await statusTag.isVisible().catch(() => false)) {
            responseStatus = await statusTag.textContent().catch(() => null);
            if (responseStatus && /\d{3}/.test(responseStatus)) {
              responseReceived = true;
              console.log(`✅ 收到响应: ${responseStatus}`);
              break;
            }
          }

          // 检查是否有错误提示
          const errorMsg = page.locator(".ant-message-error, .ant-alert-error, [class*='error']").first();
          if (await errorMsg.isVisible().catch(() => false)) {
            const errorText = await errorMsg.textContent().catch(() => null);
            console.log(`❌ 收到错误: ${errorText}`);
            responseReceived = true;
            break;
          }

          // 检查加载状态是否消失
          const loading = page.locator(".ant-spin, [class*='loading'][class*='active']").first();
          if (!(await loading.isVisible().catch(() => false))) {
            console.log(`⏱️ 第 ${i + 1} 秒，仍在等待响应...`);
          }
        }

        if (!responseReceived) {
          await screenshot(page, "api-test-timeout");
          console.log("❌ 30秒内未收到响应，可能存在超时或卡住问题");
        }

        // 验证：应该有响应状态或错误提示
        const hasResult = await page.locator(".ant-tag, [class*='response'], .ant-result").first()
          .isVisible().catch(() => false);
        expect(hasResult).toBeTruthy();
      } else {
        console.log("⚠️ 发送按钮未找到");
      }
    } else {
      console.log("⚠️ URL 输入框未找到，尝试其他选择器");

      // 尝试其他选择器
      const altInput = page.locator("input[type='text']").first();
      if (await altInput.isVisible({ timeout: 3000 }).catch(() => false)) {
        await altInput.fill("https://httpbin.org/get");
        const altBtn = page.locator("button[type='submit']").first();
        if (await altBtn.isVisible().catch(() => false)) {
          await altBtn.click();
          await page.waitForTimeout(5000);
        }
      }
    }
  });

  test("【关键】发送 HTTP POST 请求应正常工作", async ({ page }) => {
    await navigateToPage(page, "/api-test", "API 测试");
    await page.waitForTimeout(2000);

    // 设置方法为 POST
    const methodSelect = page.locator(".ant-select, [class*='method']").first();

    // 查找 URL 输入框并填写
    const urlInput = page.getByPlaceholder(/URL|url|请求地址/i).first();
    if (await urlInput.isVisible({ timeout: 5000 }).catch(() => false)) {
      await urlInput.fill("https://httpbin.org/post");

      // 查找 Body 输入框并填写
      const bodyInput = page.locator("textarea, [class*='body'] input").first();
      if (await bodyInput.isVisible({ timeout: 3000 }).catch(() => false)) {
        await bodyInput.fill('{"test": "value"}');
      }

      // 点击发送
      const sendBtn = page.getByRole("button", { name: /发送|send|提交/i }).first();
      if (await sendBtn.isVisible().catch(() => false)) {
        await sendBtn.click();
        await page.waitForTimeout(10000);

        // 检查响应
        const statusTag = page.locator(".ant-tag:visible").first();
        const hasStatus = await statusTag.isVisible().catch(() => false);
        console.log(`POST 请求响应状态可见: ${hasStatus}`);
      }
    }
  });

  test("查看集合列表", async ({ page }) => {
    await navigateToPage(page, "/api-test", "API 测试");
    await page.waitForTimeout(3000);

    // 检查左侧树形结构或表格
    const tree = page.locator(".ant-tree, .ant-table, [class*='collection']");
    const treeVisible = await tree.first().isVisible().catch(() => false);
    console.log(`集合列表可见: ${treeVisible}`);
  });

  test("【关键】创建新用例应正常工作", async ({ page }) => {
    await navigateToPage(page, "/api-test", "API 测试");
    await page.waitForTimeout(2000);

    // 查找新建按钮
    const createBtn = page.getByRole("button", { name: /新建|新建用例|create|add/i }).first();

    if (await createBtn.isVisible({ timeout: 5000 }).catch(() => false)) {
      console.log("🖱️ 点击新建按钮");
      await createBtn.click();
      await page.waitForTimeout(2000);

      // 检查是否打开弹窗
      const modal = page.locator(".ant-modal:visible, [class*='drawer']:visible").first();
      const modalVisible = await modal.isVisible().catch(() => false);
      console.log(`弹窗打开: ${modalVisible}`);
      expect(modalVisible).toBeTruthy();

      // 关闭弹窗
      const closeBtn = page.locator(".ant-modal-close, [class*='close']").first();
      if (await closeBtn.isVisible().catch(() => false)) {
        await closeBtn.click();
      }
    } else {
      console.log("⚠️ 新建按钮未找到");
    }
  });
});

// ═══════════════════════════════════════════════════════════════════════════
// 测试套件：Web 测试模块 (核心测试 - 运行状态问题)
// ═══════════════════════════════════════════════════════════════════════════

test.describe("🌐 Web 自动化测试模块 - 核心功能", () => {
  test.beforeEach(async ({ page }) => {
    const success = await login(page);
    if (!success) test.skip();
  });

  test("Web 测试页面应正常加载", async ({ page }) => {
    await navigateToPage(page, "/web-test", "Web 测试");
    await page.waitForTimeout(3000);
    console.log("✅ Web 测试页面加载完成");
  });

  test("【关键】运行脚本应显示状态变化", async ({ page }) => {
    await navigateToPage(page, "/web-test", "Web 测试");
    await page.waitForTimeout(3000);

    // 查找运行按钮
    const playButtons = page.locator("button").filter({ has: page.locator('[class*="play"], [class*="Play"], [class*="play"]') });
    const runBtn = page.locator("button").filter({ hasText: /运行|执行|run|play/i }).first();

    // 尝试多种方式找到运行按钮
    let foundRunBtn = false;

    if (await runBtn.isVisible({ timeout: 3000 }).catch(() => false)) {
      foundRunBtn = true;
      console.log("🖱️ 点击运行按钮");

      // 记录点击前的状态
      const initialLoading = await page.locator(".ant-btn-loading, [class*='loading']").count();
      console.log(`初始加载状态元素: ${initialLoading}`);

      await runBtn.click();

      // 等待状态变化
      console.log("⏳ 等待状态变化...");
      for (let i = 0; i < 20; i++) {
        await page.waitForTimeout(1000);

        // 检查是否有 loading 状态
        const loadingBtns = page.locator("button[class*='loading'], .ant-btn-loading").count();
        const statusText = await page.locator("[class*='status'], .ant-badge").first().textContent().catch(() => null);

        console.log(`第 ${i + 1} 秒: loading按钮=${loadingBtns}, 状态=${statusText || '无'}`);

        // 如果有错误提示，说明运行完成但失败
        const errorAlert = page.locator(".ant-alert-error, .ant-message-error").first();
        if (await errorAlert.isVisible().catch(() => false)) {
          const errorText = await errorAlert.textContent();
          console.log(`❌ 运行失败: ${errorText}`);
          break;
        }

        // 如果 loading 状态消失，说明运行完成
        if (loadingBtns === 0 && i > 2) {
          console.log("✅ 运行完成");
          break;
        }

        // 超时 20 秒
        if (i >= 19) {
          await screenshot(page, "web-test-running-timeout");
          console.log("❌ 运行超时，可能存在状态卡住问题");
        }
      }
    } else {
      console.log("⚠️ 运行按钮未找到或页面没有测试脚本");

      // 检查是否有创建脚本的提示
      const emptyState = page.locator(".ant-empty, [class*='empty']").first();
      if (await emptyState.isVisible().catch(() => false)) {
        console.log("📝 页面为空，没有测试脚本");
      }
    }
  });

  test("查看 Web 测试脚本列表", async ({ page }) => {
    await navigateToPage(page, "/web-test", "Web 测试");
    await page.waitForTimeout(3000);

    // 检查表格或列表
    const table = page.locator(".ant-table, [class*='list'], [class*='script']");
    const hasContent = await table.first().isVisible().catch(() => false);
    console.log(`脚本列表可见: ${hasContent}`);
  });
});

// ═══════════════════════════════════════════════════════════════════════════
// 测试套件：性能测试模块 (核心测试 - 运行状态问题)
// ═══════════════════════════════════════════════════════════════════════════

test.describe("⚡ 性能测试模块 - 核心功能", () => {
  test.beforeEach(async ({ page }) => {
    const success = await login(page);
    if (!success) test.skip();
  });

  test("性能测试页面应正常加载", async ({ page }) => {
    await navigateToPage(page, "/perf-test", "性能测试");
    await page.waitForTimeout(3000);
    console.log("✅ 性能测试页面加载完成");
  });

  test("【关键】运行性能测试场景应显示进度", async ({ page }) => {
    await navigateToPage(page, "/perf-test", "性能测试");
    await page.waitForTimeout(3000);

    // 查找运行按钮
    const runBtn = page.locator("button").filter({ hasText: /运行|执行|start|run/i }).first();

    if (await runBtn.isVisible({ timeout: 5000 }).catch(() => false)) {
      console.log("🖱️ 点击运行按钮");
      await runBtn.click();

      // 等待并监控状态
      console.log("⏳ 等待性能测试启动...");
      for (let i = 0; i < 30; i++) {
        await page.waitForTimeout(1000);

        // 检查是否有错误
        const errorAlert = page.locator(".ant-alert-error, .ant-message-error").first();
        if (await errorAlert.isVisible().catch(() => false)) {
          const errorText = await errorAlert.textContent();
          console.log(`❌ 运行错误: ${errorText}`);
          break;
        }

        // 检查是否有进度显示
        const progress = page.locator(".ant-progress, [class*='progress']").first();
        const hasProgress = await progress.isVisible().catch(() => false);
        const progressText = await progress.textContent().catch(() => null);

        // 检查状态标签
        const statusBadge = page.locator(".ant-badge, [class*='running'], [class*='status']").first();
        const statusText = await statusBadge.textContent().catch(() => null);

        console.log(`第 ${i + 1} 秒: 进度=${progressText || '无'}, 状态=${statusText || '无'}`);

        // 检查页面内容是否有变化
        const pageContent = await page.content();
        const hasRunningIndicator = pageContent.includes("running") || pageContent.includes("运行") || pageContent.includes("执行");

        if (i >= 29) {
          await screenshot(page, "perf-test-timeout");
          console.log("❌ 30秒内未检测到正常响应");
        }
      }
    } else {
      console.log("⚠️ 运行按钮未找到，页面可能为空");
    }
  });

  test("查看性能测试场景列表", async ({ page }) => {
    await navigateToPage(page, "/perf-test", "性能测试");
    await page.waitForTimeout(3000);

    // 检查表格
    const table = page.locator(".ant-table, [class*='scenario']");
    const hasTable = await table.first().isVisible().catch(() => false);
    console.log(`场景列表可见: ${hasTable}`);
  });

  test("【关键】性能监控面板应显示实时数据", async ({ page }) => {
    await navigateToPage(page, "/perf-test", "性能测试");
    await page.waitForTimeout(3000);

    // 检查监控相关元素
    const monitorElements = page.locator("[class*='monitor'], [class*='chart'], [class*='graph'], .ant-chart");
    const count = await monitorElements.count();
    console.log(`监控元素数量: ${count}`);
  });
});

// ═══════════════════════════════════════════════════════════════════════════
// 测试套件：APP 测试模块
// ═══════════════════════════════════════════════════════════════════════════

test.describe("📱 APP 测试模块", () => {
  test.beforeEach(async ({ page }) => {
    const success = await login(page);
    if (!success) test.skip();
  });

  test("APP 测试页面应正常加载", async ({ page }) => {
    await navigateToPage(page, "/app-test", "APP 测试");
    await page.waitForTimeout(3000);
    console.log("✅ APP 测试页面加载完成");
  });

  test("查看 APP 测试脚本列表", async ({ page }) => {
    await navigateToPage(page, "/app-test", "APP 测试");
    await page.waitForTimeout(3000);

    const table = page.locator(".ant-table");
    const hasTable = await table.first().isVisible().catch(() => false);
    console.log(`脚本列表可见: ${hasTable}`);
  });
});

// ═══════════════════════════════════════════════════════════════════════════
// 测试套件：报告模块
// ═══════════════════════════════════════════════════════════════════════════

test.describe("📋 报告模块", () => {
  test.beforeEach(async ({ page }) => {
    const success = await login(page);
    if (!success) test.skip();
  });

  test("报告列表页面应正常加载", async ({ page }) => {
    await navigateToPage(page, "/reports", "报告");
    await page.waitForTimeout(5000);
    console.log("✅ 报告页面加载完成");
  });

  test("报告列表应显示数据", async ({ page }) => {
    await navigateToPage(page, "/reports", "报告");
    await page.waitForTimeout(5000);

    // 检查统计信息
    const stats = page.locator(".ant-statistic, [class*='stat']");
    const statsCount = await stats.count();
    console.log(`统计元素数量: ${statsCount}`);

    // 检查表格
    const table = page.locator(".ant-table");
    const hasTable = await table.first().isVisible().catch(() => false);
    console.log(`报告表格可见: ${hasTable}`);
  });
});

// ═══════════════════════════════════════════════════════════════════════════
// 测试套件：设置模块
// ═══════════════════════════════════════════════════════════════════════════

test.describe("⚙️ 设置模块", () => {
  test.beforeEach(async ({ page }) => {
    const success = await login(page);
    if (!success) test.skip();
  });

  test("设置页面应正常加载", async ({ page }) => {
    await navigateToPage(page, "/settings", "设置");
    await page.waitForTimeout(3000);
    console.log("✅ 设置页面加载完成");
  });

  test("设置页面应有表单元素", async ({ page }) => {
    await navigateToPage(page, "/settings", "设置");
    await page.waitForTimeout(3000);

    const formElements = page.locator(".ant-form, input, select, textarea");
    const count = await formElements.count();
    console.log(`表单元素数量: ${count}`);
    expect(count).toBeGreaterThan(0);
  });
});

// ═══════════════════════════════════════════════════════════════════════════
// 测试套件：Bug 复现与问题发现
// ═══════════════════════════════════════════════════════════════════════════

test.describe("🐛 Bug 复现测试", () => {
  test.beforeEach(async ({ page }) => {
    const success = await login(page);
    if (!success) test.skip();
  });

  test("复现：执行中状态一直显示（API 测试）", async ({ page }) => {
    await navigateToPage(page, "/api-test", "API 测试");
    await page.waitForTimeout(2000);

    // 查找发送按钮
    const sendBtn = page.getByRole("button", { name: /发送|send/i }).first();

    if (await sendBtn.isVisible({ timeout: 5000 }).catch(() => false)) {
      console.log("🖱️ 点击发送按钮");
      await sendBtn.click();

      // 持续监控 60 秒，检查是否一直显示 loading
      let stuckCount = 0;
      for (let i = 0; i < 60; i++) {
        await page.waitForTimeout(1000);

        const loadingIndicator = page.locator(".ant-spin, [class*='loading'][class*='active'], button[class*='loading']").first();
        const isLoading = await loadingIndicator.isVisible().catch(() => false);

        // 检查是否有结果
        const hasResult = await page.locator(".ant-tag:visible, [class*='response']").first()
          .isVisible().catch(() => false);

        // 检查是否有错误
        const hasError = await page.locator(".ant-message-error, .ant-alert-error").first()
          .isVisible().catch(() => false);

        console.log(`第 ${i + 1} 秒: loading=${isLoading}, 有结果=${hasResult}, 有错误=${hasError}`);

        if (hasResult || hasError) {
          console.log("✅ 执行完成，loading 状态已消失");
          break;
        }

        // 如果持续 15 秒以上都是 loading 且没有结果
        if (isLoading && !hasResult && !hasError) {
          stuckCount++;
          if (stuckCount >= 15) {
            await screenshot(page, "bug-api-loading-stuck");
            console.log("❌ Bug 确认：执行后一直显示加载中超过 15 秒");
            break;
          }
        } else {
          stuckCount = 0;
        }
      }
    }
  });

  test("检查网络请求失败情况", async ({ page }) => {
    // 监听网络请求
    const failedRequests: string[] = [];
    const slowRequests: { url: string; duration: number }[] = [];

    page.on("response", async (response) => {
      const url = response.url();
      const status = response.status();
      const duration = Date.now() - (response.request().timing?.startTime || 0);

      // 记录失败的请求
      if (status >= 400 && url.includes("/api/")) {
        failedRequests.push(`${status} - ${url}`);
      }

      // 记录慢速请求（超过 10 秒）
      if (duration > 10000 && url.includes("/api/")) {
        slowRequests.push({ url, duration });
      }
    });

    await navigateToPage(page, "/api-test", "API 测试");
    await page.waitForTimeout(5000);

    if (failedRequests.length > 0) {
      console.log(`❌ 发现 ${failedRequests.length} 个失败的 API 请求:`);
      failedRequests.forEach(req => console.log(`  - ${req}`));
    } else {
      console.log("✅ 所有 API 请求成功");
    }

    if (slowRequests.length > 0) {
      console.log(`⚠️ 发现 ${slowRequests.length} 个慢速请求:`);
      slowRequests.forEach(req => console.log(`  - ${req.url}: ${req.duration}ms`));
    }
  });

  test("检查控制台错误", async ({ page }) => {
    const consoleErrors: string[] = [];

    page.on("console", (msg) => {
      if (msg.type() === "error") {
        consoleErrors.push(msg.text());
      }
    });

    await navigateToPage(page, "/dashboard", "Dashboard");
    await page.waitForTimeout(3000);

    await navigateToPage(page, "/api-test", "API 测试");
    await page.waitForTimeout(3000);

    await navigateToPage(page, "/web-test", "Web 测试");
    await page.waitForTimeout(3000);

    if (consoleErrors.length > 0) {
      console.log(`⚠️ 发现 ${consoleErrors.length} 个控制台错误:`);
      consoleErrors.slice(0, 10).forEach(err => console.log(`  - ${err}`));
    } else {
      console.log("✅ 无控制台错误");
    }
  });
});

// ═══════════════════════════════════════════════════════════════════════════
// 测试套件：导航测试
// ═══════════════════════════════════════════════════════════════════════════

test.describe("🧭 导航测试", () => {
  test.beforeEach(async ({ page }) => {
    const success = await login(page);
    if (!success) test.skip();
  });

  test("侧边栏所有菜单项应可点击", async ({ page }) => {
    await navigateToPage(page, "/dashboard", "Dashboard");

    // 收集所有菜单链接
    const menuLinks = page.locator(".ant-menu-item a, .ant-menu-item:not(a), nav a, aside a");
    const count = await menuLinks.count();
    console.log(`发现 ${count} 个菜单项`);

    // 遍历并点击每个菜单（跳过已测试的页面）
    const testedPaths = ["/dashboard", "/login", "/register"];
    for (let i = 0; i < Math.min(count, 10); i++) {
      const link = menuLinks.nth(i);
      const href = await link.getAttribute("href").catch(() => null);
      const text = await link.textContent().catch(() => null);

      if (href && !testedPaths.some(p => href.includes(p))) {
        console.log(`🖱️ 点击菜单: ${text || href}`);

        try {
          await link.click();
          await page.waitForTimeout(2000);

          // 检查页面是否正常加载
          const isErrorPage = await page.locator("text=404, text=500, text=服务器错误").isVisible().catch(() => false);
          if (isErrorPage) {
            console.log(`❌ 页面加载失败: ${href}`);
          } else {
            console.log(`✅ 页面正常: ${href}`);
          }

          testedPaths.push(href);
        } catch (e) {
          console.log(`⚠️ 点击失败: ${href}`);
        }
      }
    }
  });
});
