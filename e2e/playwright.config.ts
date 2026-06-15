import { defineConfig, devices } from "@playwright/test";

/**
 * FullScopeTest E2E 测试配置
 *
 * 运行前置条件：
 *   1. 后端运行在 http://localhost:5211
 *   2. 前端通过 Nginx 运行在 http://localhost:8080
 *   3. 已安装 Chromium: npx playwright install chromium
 *
 * 运行命令：
 *   cd e2e && npm test          # 无头模式
 *   cd e2e && npm run test:ui   # UI 模式
 */

const BASE_URL = process.env.E2E_BASE_URL || "http://localhost:8080";
const API_URL = process.env.E2E_API_URL || "http://localhost:5211";

export default defineConfig({
  testDir: "./tests",
  fullyParallel: false,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: 1,
  reporter: [["html", { open: "never" }], ["list"]],

  use: {
    baseURL: BASE_URL,
    trace: "on-first-retry",
    screenshot: "only-on-failure",
    video: "retain-on-failure",
  },

  projects: [
    {
      name: "chromium",
      use: { ...devices["Desktop Chrome"] },
    },
  ],

  /* 全局 setup：通过 API 创建测试数据 */
  globalSetup: require.resolve("./global-setup.ts"),

  /* Web server 配置（可选，如果服务已运行则跳过） */
  // webServer: {
  //   command: "cd ../web && npm run dev",
  //   url: BASE_URL,
  //   reuseExistingServer: !process.env.CI,
  //   timeout: 60000,
  // },
});
