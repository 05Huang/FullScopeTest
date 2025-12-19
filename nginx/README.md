# Windows Nginx 反向代理配置指南

## 快速开始

### 1. 下载安装 Nginx

1. 访问 [Nginx 官网下载页](https://nginx.org/en/download.html)
2. 下载 **Stable version** 的 Windows 版本 (如 `nginx-1.24.0.zip`)
3. 解压到 `D:\nginx` (或其他目录)

### 2. 配置 Nginx

将本目录下的 `nginx.conf` 复制到 Nginx 安装目录的 `conf` 文件夹：

```powershell
# 备份原配置
Copy-Item D:\nginx\conf\nginx.conf D:\nginx\conf\nginx.conf.bak

# 复制新配置
Copy-Item D:\AutoTestingLearingProject\EasyTest-Web\nginx\nginx.conf D:\nginx\conf\nginx.conf
```

### 3. 启动服务

使用提供的批处理脚本：

```powershell
cd D:\AutoTestingLearingProject\EasyTest-Web\nginx
.\start-nginx.bat
```

或手动启动：

```powershell
cd D:\nginx
.\nginx.exe
```

### 4. 常用命令

| 命令 | 说明 |
|------|------|
| `.\start-nginx.bat` | 启动 Nginx |
| `.\stop-nginx.bat` | 停止 Nginx |
| `nginx.exe -s reload` | 重载配置 |
| `nginx.exe -t` | 测试配置文件 |

## 端口说明

| 端口 | 服务 | 说明 |
|------|------|------|
| **8080** | Nginx | 前端静态文件 + 后端 API 代理 |
| 5211 | Flask | 后端 API 服务 |

## 使用方式

### 启动步骤

1. 构建前端：
   ```powershell
   cd web
   npm run build
   ```

2. 启动后端：
   ```powershell
   cd backend
   .\run_server.bat
   ```

3. 启动 Nginx：
   ```powershell
   cd nginx
   .\start-nginx.bat
   ```

4. 访问 http://localhost:8080

## 常见问题

### 1. 端口 8080 被占用

检查占用程序：
```powershell
netstat -ano | findstr :8080
```

修改 `nginx.conf` 中的端口号，如改为 `listen 8000;`

### 2. 无法访问后端 API

确认 Flask 已启动且端口正确：
```powershell
curl http://localhost:5211/api/health
```

### 3. Nginx 启动失败

测试配置是否正确：
```powershell
cd D:\nginx
.\nginx.exe -t
```

查看错误日志：
```powershell
Get-Content D:\nginx\logs\error.log -Tail 50
```

### 4. HMR 热更新不工作

确保 Nginx 配置中包含 WebSocket 支持：
```nginx
proxy_set_header Upgrade $http_upgrade;
proxy_set_header Connection "upgrade";
```
