# EasyTest Deployment (Full Flow)

This guide covers the full end-to-end flow:
- Local development pushes code to GitHub.
- Jenkins (Windows) pulls the repo and SSH deploys to the server.
- The server runs EasyTest via Docker and serves through 1Panel (OpenResty).

Assumptions:
- Server IP: 104.236.22.107
- Domain: asuka.codes (A record + www already bound)
- Repo: https://github.com/Asukadaisiki/AutoTestingPlatform.git
- Deployment layout: /opt/apps/easytest/{repo,data,logs}
- Jenkins runs on Windows

---

## 1) Server Initialization (Ubuntu)

```bash
ssh root@104.236.22.107

apt update && apt upgrade -y
apt install -y git curl ufw

ufw allow OpenSSH
ufw allow 80
ufw allow 443
ufw allow 8888
ufw enable
```

---

## 2) Install Docker + Compose

```bash
curl -fsSL https://get.docker.com | sh
apt install -y docker-compose-plugin
```

---

## 3) Install 1Panel

```bash
curl -sSL https://resource.fit2cloud.com/1panel/package/quick_start.sh | bash
```

After install, open:
```
http://<server-ip>:21887
```
Use the default account printed by the installer, then change the password.

---

## 4) Clone the Repo

```bash
mkdir -p /opt/apps/easytest/{repo,data,logs}
cd /opt/apps/easytest/repo
git clone https://github.com/Asukadaisiki/AutoTestingPlatform.git .
```

---

## 5) Create .env

```bash
cat > /opt/apps/easytest/repo/.env << 'EOF'
DATABASE_URL=postgresql://easytest:easytest123@host.docker.internal:5432/easytest_prod
REDIS_URL=redis://redis:6379/0

SECRET_KEY=dev-secret-key-for-testing
JWT_SECRET_KEY=dev-jwt-secret-key-for-testing
EOF
```

Notes:
- This is the production `.env` at `/opt/apps/easytest/repo/.env` (root `.env` does not exist in the repo).
- Redis in `docker-compose.prod.yml` has no password, so `REDIS_URL` must NOT include a password.
- Nginx is managed by 1Panel on the host; there is no nginx container in production.
- This deployment uses a shared PostgreSQL instance on the host (see step 5.1 below).
- Do NOT install Redis/PostgreSQL from 1Panel App Store to avoid duplicate services; use Docker as defined in this guide.

---

## 5.1) Shared PostgreSQL (Single Instance)

Run a single PostgreSQL container (shared by multiple projects) on the host:

```bash
docker run -d --name postgres-shared \
  -e POSTGRES_USER=easytest \
  -e POSTGRES_PASSWORD=easytest123 \
  -p 127.0.0.1:5432:5432 \
  -v /opt/apps/postgres/data:/var/lib/postgresql/data \
  postgres:15-alpine
```

Create a database for this project:

```bash
docker exec -it postgres-shared psql -U easytest -c "CREATE DATABASE easytest_prod;"
```

---

## 6) Deploy Once on the Server (Manual)

```bash
cd /opt/apps/easytest/repo/AutoTestingPlatform
chmod +x deploy.sh
./deploy.sh
```

Check containers:
```bash
docker compose -p easytest -f docker-compose.prod.yml ps
```

---

## 7) Configure 1Panel Website (HTTP)

In 1Panel:
1. Create a **Static Website**
2. Domains: `asuka.codes` and `www.asuka.codes`
3. Root path: `/opt/apps/easytest/repo/web/dist`
4. Add reverse proxy rule:
   - Path: `/api/`
   - Target: `http://127.0.0.1:5211`

---

## 8) Jenkins (Windows) Setup

### 8.1 Create Credentials
- **GitHub access**: Username + PAT
- **Server deploy**: SSH Username with private key
  - Username: `root` (or your deploy user)
  - ID: `easytest-ssh` (example)

### 8.2 Create Pipeline Job
- New Item → **Pipeline**
- Definition: **Pipeline script from SCM**
  - SCM: Git
  - Repository URL: https://github.com/Asukadaisiki/AutoTestingPlatform.git
  - Credentials: GitHub credential
  - Script Path: `Jenkinsfile`

### 8.3 Jenkinsfile (verify values)

```groovy
environment {
  DEPLOY_HOST = "104.236.22.107"
  DEPLOY_USER = "root"
  DEPLOY_PATH = "/opt/apps/easytest/repo"
  SSH_CREDENTIALS_ID = "easytest-ssh"
  DEPLOY_BRANCH = "main"
}
```

Commit and push Jenkinsfile after updating `SSH_CREDENTIALS_ID`.

---

## 9) Trigger Deploy

### Manual
Jenkins → Project → **Build Now**

### Automatic (GitHub Webhook)
- GitHub repo → Settings → Webhooks
- Payload URL:
  ```
  http://<your-jenkins-host>/github-webhook/
  ```
- Content type: `application/json`
- Events: **Just the push event**

Jenkins job → Enable:
```
GitHub hook trigger for GITScm polling
```

---

## 10) Validation

```bash
curl -I http://asuka.codes
curl -I http://asuka.codes/api/v1/api-test/health
```

---

## Notes
- Docker data is isolated under `/opt/apps/easytest/data`.
- OpenResty runs via 1Panel and does not require domain HTTPS yet.
- Add HTTPS later using 1Panel certificate management.
