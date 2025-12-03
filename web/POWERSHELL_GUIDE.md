# PowerShell 执行策略问题解决指南

## ❌ 问题

运行 `run.bat` 时出现错误：
```
找不到命令 run.bat，但它确实存在于当前位置。
默认情况下，Windows PowerShell 不会从当前位置加载命令。
如果信任此命令，请改为键入".\run.bat"。
```

## 🔍 原因

Windows PowerShell 出于安全考虑，**不允许直接执行当前目录的脚本或批处理文件**。这是系统的 **执行策略（Execution Policy）** 限制。

---

## ✅ 解决方案

### 方案 1：使用 `.\` 前缀（最简单，推荐！）

直接在脚本名前加 `.\` 前缀：

```powershell
cd web
.\run.bat
```

**优点**：
- ✅ 无需管理员权限
- ✅ 立即生效
- ✅ 简单易记
- ✅ 最安全

---

### 方案 2：使用 `&` 操作符

```powershell
cd web
& ".\run.bat"
```

**优点**：
- ✅ 对于包含空格的路径适用
- ✅ 更灵活

---

### 方案 3：切换到 CMD 命令提示符

在 Windows 上还有一个传统的命令行工具 CMD，它对批处理文件没有限制：

```cmd
cd web
run.bat
```

**切换方法**：
1. 按 `Win + R`
2. 输入 `cmd`
3. 按 Enter

---

### 方案 4：修改 PowerShell 执行策略（需要管理员权限）

如果你想永久解决这个问题，可以修改执行策略：

#### 步骤 1：以管理员身份打开 PowerShell

1. 按 `Win + X`
2. 选择 "Windows PowerShell (Admin)" 或 "终端 (Admin)"
3. 点击"是"确认管理员权限

#### 步骤 2：执行以下命令

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

#### 步骤 3：确认修改

当提示是否继续时，输入 `Y` 并按 Enter：

```
执行策略更改
执行策略可帮助你防止执行你不信任的脚本。更改执行策略可能会产生安全风险，如 about_Execution_Policies
帮助主题中所述。是否要更改执行策略?
[Y] 是  [A] 全是  [N] 否  [L] 全否  [S] 暂停  [?] 帮助 (默认值为"N"): y
```

#### 步骤 4：验证修改成功

```powershell
Get-ExecutionPolicy
```

如果输出是 `RemoteSigned`，说明修改成功。

---

## 📊 执行策略对比

| 策略 | 说明 | 安全性 | 用途 |
|------|------|--------|------|
| **Restricted** | 不执行任何脚本（默认） | 最高 | 不允许脚本 |
| **AllSigned** | 只执行签名脚本 | 高 | 企业环保 |
| **RemoteSigned** | 本地脚本随意，远程脚本须签名 | 中 | 开发环境（推荐） |
| **Unrestricted** | 执行所有脚本 | 低 | 不推荐 |
| **Bypass** | 绕过所有限制 | 最低 | 测试用 |

---

## 🎯 推荐方案总结

### 对于普通用户
👉 **使用 `.\run.bat` 前缀** - 最简单，无需任何权限修改

```powershell
cd web
.\run.bat
```

### 对于开发者
👉 **修改执行策略为 RemoteSigned** - 一次配置，永久解决

```powershell
# 管理员权限下执行
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### 对于企业环境
👉 **使用 CMD 命令提示符** - 避免 PowerShell 限制

```cmd
cd web
run.bat
```

---

## 🔄 其他相关命令

### 查看当前执行策略
```powershell
Get-ExecutionPolicy
```

### 查看所有执行策略范围
```powershell
Get-ExecutionPolicy -List
```

### 恢复为默认值
```powershell
# 管理员权限下执行
Set-ExecutionPolicy -ExecutionPolicy Restricted -Scope CurrentUser
```

### 只在当前 PowerShell 会话中改变策略
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
```

---

## ❓ 常见问题

### Q: 为什么 PowerShell 要有这个限制？
A: 为了防止恶意脚本自动执行。这是安全设计。

### Q: 修改执行策略会有风险吗？
A: `RemoteSigned` 策略足够安全，本地脚本可以执行，远程脚本需要签名。

### Q: 可以针对某个文件修改执行策略吗？
A: 不行。执行策略是全局的，但可以按范围设置（CurrentUser/LocalMachine/Process）。

### Q: 如何在脚本中临时改变执行策略？
A: 不推荐。建议在 PowerShell 会话中手动执行，或使用 CMD。

### Q: Linux/Mac 有这个问题吗？
A: 没有。Linux/Mac 使用 Bash 或 Zsh，没有这种限制。

---

## 🚀 完整启动流程

### 方案 A：简单方式（推荐新用户）
```powershell
# 1. 打开 PowerShell
# 2. 进入项目目录
cd "D:\AutoTestingLearingProject\pt_project"

# 3. 进入 web 目录
cd web

# 4. 使用 .\ 前缀运行
.\run.bat

# 5. 等待输出"应用启动中..."
# 6. 打开浏览器访问 http://localhost:5000
```

### 方案 B：一行命令
```powershell
cd "D:\AutoTestingLearingProject\pt_project\web"; .\run.bat
```

### 方案 C：使用 CMD（如果 PowerShell 有问题）
```cmd
cd D:\AutoTestingLearingProject\pt_project\web
run.bat
```

---

## 📚 参考资源

- [PowerShell 执行策略官方文档](https://learn.microsoft.com/zh-cn/powershell/module/microsoft.powershell.core/about/about_execution_policies)
- [Set-ExecutionPolicy 文档](https://learn.microsoft.com/zh-cn/powershell/module/microsoft.powershell.security/set-executionpolicy)

---

## 💡 快速记忆

| 问题 | 解决 |
|------|------|
| `找不到命令 run.bat` | 使用 `.\run.bat` |
| 想永久解决 | `Set-ExecutionPolicy RemoteSigned` |
| 不想折腾 | 用 CMD 代替 PowerShell |

---

**记住：最简单的解决方案就是在命令前加 `.\`**

```powershell
.\run.bat
```

祝你使用愉快！ 🎉
