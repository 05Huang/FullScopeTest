/**
 * E2E 全局 Setup
 *
 * 在所有测试运行前通过 API 创建测试用户和基础数据。
 * 使用 node 内置 fetch 调用后端 API。
 */

import type { FullConfig } from "@playwright/test";

const API_URL = process.env.E2E_API_URL || "https://test.huangxuan.site/api/v1";

/** E2E 测试用户凭证（与后端默认管理员区分） */
export const E2E_USER = {
  username: "e2e_tester",
  email: "e2e@fullscopetest.local",
  password: "E2E_Test@2026!",
};

async function globalSetup(_config: FullConfig) {
  console.log("\n🔧 FullScopeTest E2E Global Setup");
  console.log(`   API: ${API_URL}`);

  // 检查是否是生产环境测试（通过环境变量或 URL 判断）
  const isProdTest = API_URL.includes('test.huangxuan.site');

  if (isProdTest) {
    console.log("   ℹ️  生产环境测试模式，跳过测试用户创建");
    console.log("   ℹ️  使用已有账户: huangxuan / Test@123456");
    console.log("   ✅ Global Setup 完成\n");
    return;
  }

  // 本地开发环境：尝试注册测试用户（如果已存在会返回错误，忽略即可）
  try {
    const registerResp = await fetch(`${API_URL}/api/v1/auth/register`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(E2E_USER),
    });

    if (registerResp.ok) {
      console.log("   ✅ 测试用户已创建");
    } else {
      const body = await registerResp.json().catch(() => ({}));
      if (body.message?.includes("已存在") || body.message?.includes("already")) {
        console.log("   ℹ️  测试用户已存在，跳过创建");
      } else {
        console.log(`   ⚠️  注册响应: ${registerResp.status} - ${body.message || "unknown"}`);
      }
    }
  } catch (err) {
    console.error("   ❌ 后端不可达，请确认后端已启动:", (err as Error).message);
    process.exit(1);
  }

  console.log("   ✅ Global Setup 完成\n");
}

export default globalSetup;
