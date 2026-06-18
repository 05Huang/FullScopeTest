# Kubernetes 部署指南

## 概述

FullScopeTest 提供 Helm Chart，支持一键部署到 Kubernetes 集群。

## 前置要求

- Kubernetes 1.24+
- Helm 3.10+
- kubectl 已配置并连接到目标集群
- Ingress Controller（推荐 nginx-ingress）

## 快速开始

### 1. 克隆仓库

```bash
git clone https://github.com/05Huang/FullScopeTest.git
cd FullScopeTest
```

### 2. 创建 Secret

生产环境必须设置 JWT 和 Flask Secret Key：

```bash
kubectl create secret generic fullscopetest-secrets \
  --from-literal=jwt-secret-key=$(openssl rand -hex 32) \
  --from-literal=secret-key=$(openssl rand -hex 32)
```

### 3. 安装 Helm Chart

```bash
# 使用默认配置安装（开发/测试环境）
helm install fullscopetest deploy/helm/fullscopetest/

# 生产环境：使用自定义配置
helm install fullscopetest deploy/helm/fullscopetest/ \
  --set env.DATABASE_URL=postgresql://user:pass@external-pg:5432/fullscopetest \
  --set env.REDIS_URL=redis://external-redis:6379/0 \
  --set env.CORS_ORIGINS=https://your-domain.com \
  --set ingress.hosts[0].host=fullscopetest.your-domain.com
```

### 4. 验证部署

```bash
kubectl get pods -l app.kubernetes.io/instance=fullscopetest
kubectl get svc -l app.kubernetes.io/instance=fullscopetest
```

## 配置说明

### values.yaml 关键配置

| 配置项 | 默认值 | 说明 |
|--------|--------|------|
| `replicaCount` | 1 | 后端/前端副本数 |
| `backend.image.repository` | fullscopetest/backend | 后端镜像地址 |
| `backend.service.port` | 8000 | 后端服务端口 |
| `backend.resources.requests.cpu` | 250m | 后端 CPU 请求 |
| `backend.resources.limits.memory` | 1Gi | 后端内存上限 |
| `ingress.enabled` | true | 是否创建 Ingress |
| `ingress.hosts[0].host` | fullscopetest.example.com | 域名 |
| `postgresql.enabled` | true | 使用内置 PostgreSQL |
| `redis.enabled` | true | 使用内置 Redis |
| `env.FLASK_ENV` | production | Flask 环境 |
| `env.DATABASE_URL` | postgresql://... | 数据库连接串 |
| `env.REDIS_URL` | redis://... | Redis 连接串 |

### 生产环境建议

1. **使用外部数据库**：将 `postgresql.enabled` 设为 `false`，使用云数据库（AWS RDS / 阿里云 RDS）
2. **使用外部 Redis**：将 `redis.enabled` 设为 `false`，使用 ElastiCache 或云 Redis
3. **配置 TLS**：通过 cert-manager 自动申请 Let's Encrypt 证书
4. **资源限制**：根据实际负载调整 `resources.requests/limits`
5. **Horizontal Pod Autoscaler**：对后端 Deployment 配置 HPA

### TLS 配置示例

```yaml
# values-override.yaml
ingress:
  enabled: true
  className: "nginx"
  annotations:
    cert-manager.io/cluster-issuer: letsencrypt-prod
  hosts:
    - host: fullscopetest.your-domain.com
      paths:
        - path: /api
          pathType: Prefix
          backend: backend
        - path: /
          pathType: Prefix
          backend: frontend
  tls:
    - secretName: fullscopetest-tls
      hosts:
        - fullscopetest.your-domain.com
```

```bash
helm install fullscopetest deploy/helm/fullscopetest/ -f values-override.yaml
```

## 升级

```bash
helm upgrade fullscopetest deploy/helm/fullscopetest/ \
  --set backend.image.tag=v1.1.0 \
  --set frontend.image.tag=v1.1.0
```

## 卸载

```bash
helm uninstall fullscopetest
# 如需清理 PVC
kubectl delete pvc -l app.kubernetes.io/instance=fullscopetest
```

## 监控

平台内置 Prometheus 指标端点：

- 后端：`/api/v1/metrics`
- 健康检查：`/api/v1/health/live`、`/api/v1/health/ready`

建议安装 Prometheus Operator + Grafana 进行监控。

## 故障排查

```bash
# 查看 Pod 日志
kubectl logs -l app=fullscopetest-backend --tail=100

# 进入 Pod 调试
kubectl exec -it deploy/fullscopetest-backend -- bash

# 检查服务端点
kubectl get endpoints fullscopetest-backend
```

## 架构图

```
Internet → Ingress (nginx) → Frontend Service (80)
                           → Backend Service (8000) → Flask App (Gunicorn)
                                                    → Celery Worker
                           → Redis (6379)
                           → PostgreSQL (5432)
```
