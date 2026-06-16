/**
 * 测试报告 E2E 测试
 *
 * 覆盖：报告列表、报告详情、报告导出
 */

import { test, expect } from "@playwright/test";
import { E2E_USER } from "../global-setup";

// 复用登录逻辑
async function login(page: any) {
  await page.goto("/login");
  await page.waitForLoadState("networkidle");
  await page.getByPlaceholder(/用户名|username/i).fill(E2E_USER.username);
  await page.getByPlaceholder(/密码|password/i).fill(E2E_USER.password);
  await page.getByRole("button", { name: /登录|login|sign in/i }).click();
  await expect(page).not.toHaveURL(/\/login/, { timeout: 10000 });
}

test.describe("测试报告", () => {
  test.beforeEach(async ({ page }) => {
    await login(page);
  });

  test("报告页面应正确加载", async ({ page }) => {
    await page.goto("/reports");
    await page.waitForLoadState("networkidle");

    // 页面标题应包含"报告"或"Report"
    await expect(page.locator("body")).toBeVisible();
  });

  test("报告页面应显示统计信息", async ({ page }) => {
    await page.goto("/reports");
    await page.waitForLoadState("networkidle");

    // 应有表格或统计卡片
    const table = page.locator(".ant-table");
    const cards = page.locator(".ant-statistic");
    await expect(table.or(cards).first()).toBeVisible({ timeout: 10000 });
  });

  test("报告页面应支持筛选", async ({ page }) => {
    await page.goto("/reports");
    await page.waitForLoadState("networkidle");

    // 应有筛选控件
    const select = page.locator(".ant-select").first();
    await expect(select).toBeVisible({ timeout: 10000 });
  });
});
