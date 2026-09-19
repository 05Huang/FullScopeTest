/**
 * FullScopeTest 生产环境 E2E 测试配置
 *
 * 针对远程服务器 https://test.huangxuan.site 进行完整功能测试
 * 使用 Playwright 模拟真实用户操作，发现前端与后端交互的 Bug
 *
 * 运行条件：
 *   1. Chromium 已安装: npx playwright install chromium
 *   2. 测试账户: admin / admin123
 *
 * 运行命令：
 *   cd e2e && npm run test:prod          # 无头模式测试
 *   cd e2e && npm run test:prod:headed   # 有头模式（可以看到浏览器）
 */

import { defineConfig, devices } from "@playwright/test";

const BASE_URL = "https://test.huangxuan.site";
const API_URL = "https://test.huangxuan.site/api/v1";

export default defineConfig({
  testDir: "./tests",
  fullyParallel: false,
  forbidOnly: !!process.env.CI,
  retries: 2,
  workers: 1,
  reporter: [
    ["html", { open: "never" }],
    ["list"],
    ["json", { outputFile: "test-results/results.json" }]
  ],

  use: {
    baseURL: BASE_URL,
    trace: "on-first-retry",
    screenshot: "always",  // 每次都截图，方便调试
    video: "retain-on-failure",
    actionTimeout: 15000,
    navigationTimeout: 30000,
  },

  projects: [
    {
      name: "chromium",
      use: { ...devices["Desktop Chrome"] },
    },
  ],

  globalSetup: require.resolve("./global-setup.ts"),
});
