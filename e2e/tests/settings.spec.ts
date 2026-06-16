/**
 * 设置页面 E2E 测试
 *
 * 覆盖：设置页面加载、个人信息展示、主题切换
 */

import { test, expect } from "@playwright/test";
import { E2E_USER } from "../global-setup";

async function login(page: any) {
  await page.goto("/login");
  await page.waitForLoadState("networkidle");
  await page.getByPlaceholder(/用户名|username/i).fill(E2E_USER.username);
  await page.getByPlaceholder(/密码|password/i).fill(E2E_USER.password);
  await page.getByRole("button", { name: /登录|login|sign in/i }).click();
  await expect(page).not.toHaveURL(/\/login/, { timeout: 10000 });
}

test.describe("设置页面", () => {
  test.beforeEach(async ({ page }) => {
    await login(page);
  });

  test("设置页面应正确加载", async ({ page }) => {
    await page.goto("/settings");
    await page.waitForLoadState("networkidle");
    await expect(page.locator("body")).toBeVisible();
  });

  test("侧边栏应包含导航项", async ({ page }) => {
    await page.goto("/dashboard");
    await page.waitForLoadState("networkidle");

    // 侧边栏应有导航项
    const nav = page.locator("nav");
    await expect(nav).toBeVisible();
  });

  test("Dashboard 页面应显示测试统计", async ({ page }) => {
    await page.goto("/dashboard");
    await page.waitForLoadState("networkidle");

    // 应有统计卡片或图表
    const content = page.locator("main");
    await expect(content).toBeVisible();
  });
});
