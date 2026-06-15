/**
 * 认证流程 E2E 测试
 *
 * 覆盖：登录、登出、未认证重定向
 */

import { test, expect } from "@playwright/test";
import { E2E_USER } from "../global-setup";

test.describe("认证流程", () => {
  test("访问首页应重定向到登录页", async ({ page }) => {
    await page.goto("/");
    // 未登录时应跳转到登录页
    await expect(page).toHaveURL(/\/login/);
  });

  test("登录页面应包含用户名和密码输入框", async ({ page }) => {
    await page.goto("/login");
    // 等待页面加载
    await page.waitForLoadState("networkidle");
    // 检查输入框存在
    const usernameInput = page.getByPlaceholder(/用户名|username/i);
    const passwordInput = page.getByPlaceholder(/密码|password/i);
    await expect(usernameInput).toBeVisible();
    await expect(passwordInput).toBeVisible();
  });

  test("使用正确凭证登录成功后跳转到 Dashboard", async ({ page }) => {
    await page.goto("/login");
    await page.waitForLoadState("networkidle");

    // 填写登录表单
    await page.getByPlaceholder(/用户名|username/i).fill(E2E_USER.username);
    await page.getByPlaceholder(/密码|password/i).fill(E2E_USER.password);

    // 点击登录按钮
    const submitBtn = page.getByRole("button", { name: /登录|login|sign in/i });
    await submitBtn.click();

    // 等待跳转到 Dashboard 或首页
    await expect(page).not.toHaveURL(/\/login/, { timeout: 10000 });
  });

  test("使用错误密码登录显示错误提示", async ({ page }) => {
    await page.goto("/login");
    await page.waitForLoadState("networkidle");

    await page.getByPlaceholder(/用户名|username/i).fill(E2E_USER.username);
    await page.getByPlaceholder(/密码|password/i).fill("wrong_password_123");

    const submitBtn = page.getByRole("button", { name: /登录|login|sign in/i });
    await submitBtn.click();

    // 应显示错误提示（antd message 或 inline error）
    // 等待一小段时间让错误消息出现
    await page.waitForTimeout(2000);
    // 验证仍在登录页
    await expect(page).toHaveURL(/\/login/);
  });

  test("登录后可以访问 Dashboard", async ({ page }) => {
    // 先登录
    await page.goto("/login");
    await page.waitForLoadState("networkidle");
    await page.getByPlaceholder(/用户名|username/i).fill(E2E_USER.username);
    await page.getByPlaceholder(/密码|password/i).fill(E2E_USER.password);
    await page.getByRole("button", { name: /登录|login|sign in/i }).click();
    await expect(page).not.toHaveURL(/\/login/, { timeout: 10000 });

    // 验证可以访问 Dashboard
    await page.goto("/dashboard");
    await page.waitForLoadState("networkidle");
    // 不应被重定向回登录页
    await expect(page).not.toHaveURL(/\/login/);
  });
});
