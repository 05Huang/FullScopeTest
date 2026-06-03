# FullScopeTest — AI-Nowered Full-Stack Automated Testing Platform

<div align="center">
  <img src="images/docs/banner.webp" alt="FullScopeTest Banner" width="100%" />

  <br />

  **AI-Native End-to-End Automated Testing Platform**
  <br />
  AI Orchestration · API Testing · Web Automation · APP Testing · Performance Testing · Smart Reports

  <a href="README.md">中文</a> | <a href="README_EN.md">English</a>

  [![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
  [![Python](https://img.shields.io/badge/python-3.10+-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/)
  [![TypeScript](https://img.shields.io/badge/typescript-5.x-3178C6?style=flat&logo=typescript&logoColor=white)](https://www.typescriptlang.org/)
  [![React](https://img.shields.io/badge/react-18-61DAFB?style=flat&logo=react&logoColor=black)](https://reactjs.org/)
  [![Vite](https://img.shields.io/badge/vite-5-646CFF?style=flat&logo=vite&logoColor=white)](https://vitejs.dev/)
  [![Flask](https://img.shields.io/badge/flask-3.0-000000?style=flat&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
  [![SQLAlchemy](https://img.shields.io/badge/sqlalchemy-ORM-D71F00?style=flat&logo=sqlalchemy&logoColor=white)](https://www.sqlalchemy.org/)
  [![Ant Design](https://img.shields.io/badge/ant--design-5-0170FE?style=flat&logo=antdesign&logoColor=white)](https://ant.design/)
  [![Playwright](https://img.shields.io/badge/playwright-e2e-2EAD33?style=flat&logo=playwright)](https://playwright.dev/)
  [![Celery](https://img.shields.io/badge/celery-task--queue-37814A?style=flat&logo=celery&logoColor=white)](https://docs.celeryq.dev/)
  [![Redis](https://img.shields.io/badge/redis-broker-DC382D?style=flat&logo=redis&logoColor=white)](https://redis.io/)
  [![PostgreSQL](https://img.shields.io/badge/postgresql-15-4169E1?style=flat&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
  [![Docker](https://img.shields.io/badge/docker-compose-2496ED?style=flat&logo=docker&logoColor=white)](https://www.docker.com/)
  [![Vitest](https://img.shields.io/badge/vitest-testing-6E9F18?style=flat&logo=vitest&logoColor=white)](https://vitest.dev/)

  <h2>Live Demo: <a href="http://test.huangxuan.chat">test.huangxuan.chat</a></h2>
</div>

## About

**FullScopeTest** is an AI-driven end-to-end automated testing platform covering API testing, Web UI automation, mobile APP testing, and performance testing. Built with an **AI-Native** design philosophy, it provides natural language orchestration, automatic script generation, intelligent error analysis and self-healing to lower the barrier of test authoring and maintenance.

<div align="center">
  <img src="images/docs/dashboard.webp" alt="Dashboard Preview" width="80%" />
  <p><em>Platform Dashboard</em></p>
</div>

---

## Features

### AI Capabilities (AI-Native)

#### 1. AI Auto-Orchestration

Input a natural language test goal — the AI parses intent, generates a structured execution plan, then calls platform APIs to automatically create environments, collections, and test cases before running them. The frontend panel supports runtime configuration of `base_url` / `model` / `api_key`, compatible with OpenAI, DeepSeek, and other major LLMs.

<div align="center">
  <img src="images/docs/ai-orchestration.webp" alt="AI Orchestration — Input" width="45%" />
  <img src="images/docs/ai-orchestration-exec.webp" alt="AI Orchestration — Execution" width="45%" />
  <p><em>Natural Language → Structured Plan → Auto Execution</em></p>
</div>

#### 2. NL2Script — Natural Language to Test Scripts

Input a natural language description (e.g. "Log in, navigate to dashboard, create a user, verify success message"), and the AI Agent converts it into executable Playwright web test scripts or Locust performance test scripts. Generated code is displayed in Monaco Editor with syntax highlighting for review and editing.

<div align="center">
  <img src="images/docs/nl2script.webp" alt="NL2Script" width="80%" />
</div>

#### 3. Intelligent Error Analysis & Self-Healing

When a test fails, AI diagnosis is triggered automatically: analyzing error logs, API responses, or DOM structure to identify root causes (e.g. selector changes, missing fields). Supports one-click fix — the AI automatically corrects assertions or selectors and re-executes, reducing test maintenance cost.

<div align="center">
  <img src="images/docs/error-analysis.webp" alt="Error Analysis" width="45%" />
  <img src="images/docs/self-healing.webp" alt="Self-Healing" width="45%" />
  <p><em>Error Detection → AI Diagnosis → One-Click Fix</em></p>
</div>

#### 4. Smart Test Data Generation & Case Fission

Based on API definitions or existing test cases, the AI infers field semantics and batch-generates boundary values, empty values, injection attacks, and other abnormal test data — fissioning a single case into a multi-scenario test set to improve coverage.

<div align="center">
  <img src="images/docs/ai-data-gen.webp" alt="AI Data Generation" width="45%" />
  <img src="images/docs/case-fission.webp" alt="Case Fission" width="45%" />
  <p><em>Single Case → AI Fission → Multi-Scenario Coverage</em></p>
</div>

#### 5. Exploratory Testing Agent

Given a starting URL and test objective, the AI Agent autonomously traverses pages — parsing DOM, clicking buttons, filling forms, recording anomalies. Combined with Vision models for visual verification, it outputs an exploration test report (JS errors, 404 dead links, security risks).

<div align="center">
  <img src="images/docs/exploratory-testing.webp" alt="Exploratory Testing Agent" width="80%" />
</div>

#### 6. Global Copilot

A unified AI conversation interface that supports natural language commands: "Create a performance test scenario with 100 concurrent users for 5 minutes", "Show yesterday's failed Web tests". The backend uses Function Calling to parse intent and directly invoke platform APIs.

<div align="center">
  <img src="images/docs/global-copilot.webp" alt="Global Copilot" width="80%" />
</div>

---

### Core Workspace

#### API Testing

A complete HTTP/REST API testing workspace supporting `{variable}` environment substitution, pre/post script engines, variable extraction and assertions, and one-click cURL import/export.

<div align="center">
  <img src="images/docs/api-testing.webp" alt="API Testing Workspace" width="80%" />
</div>

#### Web Automation (Playwright)

Built-in Playwright engine for writing, editing, and executing Python test scripts online. Supports `playwright codegen` for recording interactions and auto-generating scripts. Tasks execute asynchronously via Celery with real-time status tracking and error localization.

<div align="center">
  <img src="images/docs/web-automation.webp" alt="Web Automation" width="80%" />
</div>

#### Performance Testing (Locust)

Locust-based distributed load testing with configurable concurrent users and step load patterns. Real-time collection and visualization of response time, throughput (RPS), error rate, and other key metrics.

<div align="center">
  <img src="images/docs/performance.webp" alt="Performance Dashboard" width="80%" />
</div>

#### APP Mobile Testing (Appium)

Appium-based mobile application automation supporting both Android and iOS. Configure package/activity (Android) or bundle_id (iOS) to connect real devices or emulators, write Appium Python scripts online and execute them asynchronously via Celery.

#### Test Report Center

Aggregates execution results from API, Web, APP, and Performance tests with type-based statistics, daily trends, and success rate visualization. Supports HTML and JSON export. The Dashboard provides a global testing overview.

#### Environment Management

A standalone environment module supporting multiple environment configurations (dev/test/staging/prod), each with custom variables and headers. Automatic `{variable}` substitution in API tests with default environment support.

#### Test Document Management

Built-in test document management with Markdown editing, category filtering, and keyword search. Provides templates for test plans, test cases, and API documents. Supports Markdown/HTML export.

#### Mock Server

Per-API-case Mock support — when enabled, returns preset responses (status code, body, headers, delay) without depending on real backend services, enabling parallel frontend development and integration.

#### Webhook Triggers & Scheduled Tasks

Supports creating Webhook triggers (HMAC-SHA256 signature verification) to execute test collections via HTTP requests. Scheduled tasks support Cron expression scheduling, implemented with APScheduler and file-locking for multi-process safety.

---

## System Architecture

### Overall Architecture

```mermaid
graph LR
    subgraph Client
        Browser["Browser"]
    end

    subgraph Nginx / OpenResty
        Static["Static Assets<br/>(React SPA)"]
        Proxy["Reverse Proxy<br/>/api → :5000(Dev)<br/>/api → :8000(Prod)"]
        WS["WebSocket<br/>(Live View)"]
    end

    subgraph Flask Backend :5000(Dev) / :8000(Prod)
        API["API Blueprint Layer<br/>25 Modules"]
        Auth["JWT Auth<br/>+ RBAC"]
        ORM["SQLAlchemy ORM<br/>31 Models"]
    end

    subgraph Async Workers
        Celery["Celery Worker<br/>(Web / Perf Tests)"]
        Scheduler["APScheduler<br/>(Scheduled Tasks)"]
    end

    subgraph AI Layer
        Copilot["AI Copilot"]
        Agent["AI Agent<br/>(Orchestration / Script Gen)"]
    end

    subgraph Data Stores
        PG["PostgreSQL"]
        Redis["Redis<br/>(Message Queue + Cache)"]
    end

    Browser --> Static
    Browser --> Proxy
    Proxy --> API
    API --> Auth
    Auth --> ORM
    ORM --> PG
    API --> Celery
    Celery --> Redis
    Scheduler --> Celery
    API --> Copilot
    Copilot --> Agent
    Agent -->|OpenAI / DeepSeek etc.| LLM["LLM API"]
    WS -->|VNC Live View| VNC["x11vnc + websockify"]
    Celery -->|Playwright| VNC
```

### Request Flow

```mermaid
sequenceDiagram
    participant U as User Browser
    participant N as Nginx / OpenResty
    participant F as Flask API
    participant DB as PostgreSQL
    participant R as Redis
    participant C as Celery Worker
    participant AI as LLM API

    U->>N: HTTPS Request
    N->>F: Reverse Proxy /api/*
    F->>F: JWT Auth + RBAC Check
    F->>DB: Read/Write Data
    F-->>U: Sync Response (JSON)

    Note over U,F: Async Task (Web/Perf Test)
    F->>R: Send Celery Task
    F-->>U: Return task_id
    R->>C: Consume Task
    C->>DB: Write Test Results
    C->>R: Update Task State
    U->>F: Poll Task Status
    F->>R: Query Celery Status
    F-->>U: Return Progress & Results

    Note over F,AI: AI-Assisted Scenario
    F->>AI: Send Prompt (with context)
    AI-->>F: Return Structured Result
    F-->>U: AI-Generated Cases / Scripts / Analysis
```

### Tech Stack

| Layer | Technology | Description |
|-------|-----------|-------------|
| **Frontend** | React 18 + TypeScript | Component-based SPA with strict type checking |
| **Build Tool** | Vite 6 | Fast HMR, out-of-the-box TS/JSX support |
| **UI Library** | Ant Design 5 | Enterprise-grade UI with ProComponents |
| **Code Editor** | Monaco Editor | VS Code's editor with syntax highlighting & autocomplete |
| **State Management** | Zustand | Lightweight store with persist + devtools middleware |
| **HTTP Client** | Axios | Interceptor-based JWT injection with auto token refresh |
| **Frontend Testing** | Vitest + Testing Library | jsdom environment, component-level unit tests |
| **Backend Framework** | Flask 3.0 | Application factory pattern + Blueprint modularization |
| **ORM** | SQLAlchemy + Alembic | Declarative models + database migrations |
| **Authentication** | Flask-JWT-Extended | Dual token mechanism (access + refresh) |
| **Task Queue** | Celery + Redis | Async execution for Web/Performance tests |
| **Scheduler** | APScheduler | File-lock singleton, multi-process safe |
| **Web Automation** | Playwright | Chromium-based, supports recording & headless execution |
| **Load Testing** | Locust | Python-based load testing with distributed support |
| **Database** | PostgreSQL (prod) / SQLite (dev) | Zero-config for development |
| **Cache / Message** | Redis | Celery Broker + Result Backend |
| **Reverse Proxy** | Nginx / OpenResty | Static hosting + API proxy + SSL |
| **Containerization** | Docker Compose | One-click deployment, dev/prod configurations |
| **CI/CD** | GitHub Actions | CodeQL security scanning + pytest + npm test + Docker build |

---

## Backend Architecture

### Application Factory

The backend uses Flask's standard **Application Factory** pattern, creating app instances via `create_app(config_name)` for testability and multi-environment configuration:

```mermaid
graph TD
    Entry["app.py / wsgi.py"] --> Factory["create_app()"]
    Factory --> Config["Load Config<br/>(Development / Testing / Production)"]
    Factory --> Ext["Init Extensions<br/>(db, jwt, celery, migrate)"]
    Factory --> BP["Register Blueprint<br/>api_bp → /api/v1"]
    Factory --> CORS["Configure CORS"]
    Factory --> ErrorH["Register Error Handlers"]
    Factory --> Scheduler["Start APScheduler"]
```

### API Modules

All API routes are mounted under a single `api_bp` blueprint (prefix `/api/v1`), organized into 25 functional modules:

| Module | Route Prefix | Core Functions |
|--------|-------------|----------------|
| `auth` | `/auth` | Registration, login, token refresh, user profile |
| `projects` | `/projects` | Project CRUD, member management, RBAC |
| `environments` | `/environments` | Environment variable management, variable substitution |
| `api_test` | `/api-test` | Collection/case CRUD, Mock Server, cURL import/export |
| `web_test` | `/web-test` | Web script management, Playwright execution, recording |
| `app_test` | `/app-test` | APP script management, Appium device connection |
| `perf_test` | `/perf-test` | Performance scenario config, Locust distributed testing |
| `reports` | `/test-reports` | Test report aggregation, historical trend analysis |
| `docs` | `/docs` | Test document management, Markdown editor |
| `ai_copilot` | `/ai` | AI conversation, case generation, error analysis |
| `triggers` | `/triggers` | Webhook triggers, scheduled task management |
| `global_search` | `/ai/global-search` | Global search (cross-module fuzzy query) |

### Data Model ER Diagram

```mermaid
erDiagram
    User ||--o{ Project : "owns"
    User ||--o{ WebTestScript : "creates"
    User ||--o{ TestRun : "triggers"
    User ||--o{ ScheduledTask : "schedules"

    Project ||--o{ Environment : "has"
    Project ||--o{ ApiTestCollection : "contains"
    Project ||--o{ WebTestCollection : "contains"
    Project ||--o{ AppTestCollection : "contains"
    Project ||--o{ PerfTestScenario : "contains"

    ApiTestCollection ||--o{ ApiTestCase : "contains"
    WebTestCollection ||--o{ WebTestScript : "contains"
    AppTestCollection ||--o{ AppTestScript : "contains"

    TestRun ||--o| TestReport : "generates"
    Project ||--o{ TestRun : "tracks"
    Project ||--o{ TestReport : "aggregates"
    Project ||--o{ TestDocument : "documents"

    WebhookToken }o--|| Project : "belongs to"

    User {
        int id PK
        string username UK
        string email UK
        string password_hash
        string role "admin | member | viewer"
    }
    Project {
        int id PK
        string name
        int owner_id FK
    }
    Environment {
        int id PK
        string name
        json variables
        int project_id FK
    }
    ApiTestCase {
        int id PK
        string name
        string method
        string url
        int collection_id FK
    }
    TestRun {
        int id PK
        string test_type "api | web | app | perf"
        string status "pending | running | success | failed"
        int total_cases
        int passed
        int failed
    }
    TestReport {
        int id PK
        string test_type
        json summary
        int test_run_id FK
    }
```

### Authentication & Authorization

```mermaid
graph LR
    subgraph Authentication
        Login["Login Request"] --> Validate["Verify Credentials"]
        Validate --> GenToken["Generate Dual Tokens"]
        GenToken --> Access["Access Token<br/>TTL: 24h"]
        GenToken --> Refresh["Refresh Token<br/>TTL: 30d"]
        Access --> Header["Authorization Header"]
    end

    subgraph Authorization
        Request["API Request"] --> JWT["JWT Parse<br/>Extract user_id + role"]
        JWT --> RBAC{"Role Check"}
        RBAC -->|admin| Admin["Full Access"]
        RBAC -->|member| Member["Read/Write"]
        RBAC -->|viewer| Viewer["Read Only"]
    end
```

- **Access Token**: Short-lived (24 hours) for API request authentication
- **Refresh Token**: Long-lived (30 days) for seamless token renewal
- **Auto Refresh**: Axios interceptor catches 401 responses, automatically calls refresh endpoint and retries
- **RBAC Roles**: `admin` (full control), `member` (default, read/write), `viewer` (read-only)

### Async Task Architecture

Web and performance tests execute asynchronously via Celery to avoid blocking API requests:

```mermaid
graph LR
    API["Flask API"] -->|send_task| Broker["Redis Broker"]
    Broker -->|consume| Worker["Celery Worker"]
    Worker -->|Playwright| WebTest["Web Test Execution"]
    Worker -->|Locust| PerfTest["Perf Test Execution"]
    Worker -->|update_state| Backend["Redis Backend"]
    API -->|AsyncResult| Backend
    API -->|Poll Status| Client["Frontend Polling"]
```

- **Web Tests**: Celery Worker calls `subprocess.run()` to execute Playwright Python scripts
- **Performance Tests**: Celery Worker launches Locust processes, collecting RPS, response time, error rate in real-time
- **Scheduled Tasks**: APScheduler with file-lock singleton, supporting Cron expressions and one-shot triggers

---

## Frontend Architecture

### Component Hierarchy

```mermaid
graph TD
    App["App.tsx<br/>Router Entry"] --> Layout["MainLayout<br/>Sidebar + Header + Content"]
    Layout --> Suspense["React.Suspense<br/>Lazy Loading Boundary"]
    Suspense --> Pages["Page Components"]
    Pages --> Dashboard["Dashboard"]
    Pages --> APITest["API Testing"]
    Pages --> WebTest["Web Automation"]
    Pages --> AppTest["APP Testing"]
    Pages --> PerfTest["Performance Testing"]
    Pages --> Reports["Reports"]
    Pages --> Settings["Settings"]

    APITest --> Components["Business Components"]
    Components --> RequestEditor["Request Editor"]
    Components --> EnvManager["Environment Manager"]
    Components --> MockServer["Mock Panel"]

    Layout --> Global["Global Components"]
    Global --> Copilot["GlobalCopilot<br/>AI Assistant Float"]
    Global --> Search["GlobalSearch<br/>Global Search"]
    Global --> EnvHint["EnvironmentVariableHint<br/>Variable Autocomplete"]
```

### State Management (Zustand)

```mermaid
graph LR
    subgraph Stores
        AuthStore["authStore<br/>Auth State<br/>(persist → localStorage)"]
        ProjectStore["projectStore<br/>Current Project<br/>(persist → localStorage)"]
        APITestStore["apiTestStore<br/>Collections/Cases/Mock"]
        WebTestStore["webTestStore<br/>Scripts/Execution"]
        PerfTestStore["perfTestStore<br/>Scenarios/Metrics"]
    end

    subgraph Middleware
        Persist["persist<br/>localStorage Persistence"]
        Devtools["devtools<br/>Redux DevTools Debugging"]
    end

    AuthStore --> Persist
    ProjectStore --> Persist
    APITestStore --> Devtools
    WebTestStore --> Devtools
    PerfTestStore --> Devtools
```

### Service Layer Pattern

The frontend encapsulates all API calls through a unified **Service layer** with clear separation of concerns:

| Service File | Backend Module | Key Methods |
|-------------|----------------|-------------|
| `authService.ts` | auth | login, register, refreshToken, getProfile |
| `projectService.ts` | projects | getProjects, createProject, updateProject |
| `environmentService.ts` | environments | getEnvironments, createEnvironment |
| `apiTestService.ts` | api_test | getCollections, createCase, runCase, curlImport |
| `webTestService.ts` | web_test | getScripts, createScript, runScript |
| `appTestService.ts` | app_test | getScripts, createScript, runScript |
| `perfTestService.ts` | perf_test | getScenarios, createScenario, runScenario |
| `reportService.ts` | reports | getReports, getReportDetail |
| `aiCopilotService.ts` | ai_copilot | chat, generateCases, analyzeError |
| `documentService.ts` | docs | getDocuments, createDocument |
| `triggerService.ts` | triggers | getTriggers, createTrigger |

**Axios Interceptor Chain**:
1. **Request Interceptor**: Auto-injects `Authorization: Bearer <token>` header
2. **Response Interceptor**: Catches 401 → auto-refreshes token → retries original request
3. **Error Interceptor**: Unified handling of network/business errors with antd notification

### Routing & Lazy Loading

```typescript
// React Router v6 + lazy() for code splitting
const Dashboard = lazy(() => import('./pages/Dashboard'))
const APITestWorkspace = lazy(() => import('./pages/api-test/APITestWorkspace'))
const WebTestWorkspace = lazy(() => import('./pages/web-test/WebTestWorkspace'))
// ...

<Suspense fallback={<Spin />}>
  <Routes>
    <Route path="/" element={<Dashboard />} />
    <Route path="/api-test/*" element={<APITestWorkspace />} />
    {/* ... */}
  </Routes>
</Suspense>
```

All non-critical pages use `lazy()` dynamic imports with `<Suspense>` for route-level code splitting, significantly reducing initial load size.

---

## Security Architecture

```mermaid
graph TD
    subgraph Authentication
        JWT["JWT Dual Token<br/>Access: 24h / Refresh: 30d"]
        Header["Authorization Header<br/>Bearer <token>"]
    end

    subgraph Authorization
        RBAC["RBAC Role Control<br/>admin / member / viewer"]
        Decorator["@require_role Decorator<br/>Route-level Permission Guard"]
    end

    subgraph Transport
        HTTPS["HTTPS (SSL/TLS)"]
        CORS["CORS Whitelist"]
    end

    subgraph Data
        Hash["Password Hashing<br/>(bcrypt / werkzeug)"]
        EnvVars["Environment Variables<br/>Secrets Not in Code"]
        Webhook["Webhook Signature<br/>HMAC-SHA256"]
    end

    Header --> JWT --> RBAC --> Decorator
    HTTPS --> CORS
    Hash --> EnvVars --> Webhook
```

| Security Mechanism | Implementation | Purpose |
|-------------------|----------------|---------|
| **Authentication** | JWT (Flask-JWT-Extended) | Stateless auth with auto token refresh |
| **Authorization** | RBAC 3 roles + decorators | Fine-grained admin/member/viewer permissions |
| **Password Storage** | werkzeug secure hashing | Irreversible encryption, prevents data leaks |
| **Webhook Security** | HMAC-SHA256 signature verification | Prevents forged trigger requests |
| **Transport** | HTTPS + CORS whitelist | Encrypted transport + cross-origin restriction |
| **Secrets** | `.env` files + `.gitignore` | API keys, passwords excluded from codebase |
| **Security Scanning** | GitHub CodeQL | CI auto-detects OWASP Top 10 vulnerabilities |
| **Dependency Audit** | npm audit + pip-audit | CI auto-detects known vulnerable dependencies |

---

## Documentation

- Overview: `document/overview.md`
- Startup Guide: `document/STARTUP.md`
- API Documentation: `document/API.md`
- Development Guide: `document/DEVELOPMENT.md`
- Script Guide: `document/SCRIPT_GUIDE.md`

---

## Quick Start (Local Development)

The project uses a frontend-backend separated architecture: Flask + SQLAlchemy backend, React + TypeScript frontend.

Two startup options: **Option A** — Manual setup (recommended for development), **Option B** — Docker Compose one-click start.

### Prerequisites

| Component | Version | Description |
|-----------|---------|-------------|
| Python | 3.10+ | Backend runtime |
| Node.js | 18+ | Frontend build / dev server |
| Redis | 5.0+ | **Required** — Celery message queue (`app.py` auto-enables Celery) |

> **Database**: Local development uses **SQLite** by default (zero config). PostgreSQL recommended for production.

### Option A: Manual Setup (Recommended)

#### 1) Start Redis

```bash
# Verify Redis is running
redis-cli ping
# Should return PONG, otherwise start Redis first
```

#### 2) Start Backend

```bash
cd backend
python -m venv venv

# Windows
.\venv\Scripts\activate

# Linux/macOS
# source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Optional: Install Playwright browsers (required for Web automation/recording)
python -m playwright install chromium

# Prepare config (copy from template, most variables have defaults)
cp .env.example .env
# Edit .env, at minimum confirm:
#   DATABASE_URL=sqlite:///fullscopetest_dev.db   # SQLite for local dev
#   SECRET_KEY=any_random_string
#   JWT_SECRET_KEY=another_random_string

# Initialize database (WARNING: drops existing data, dev only)
python init_db.py

# Create admin account
python create_admin.py
# Default: admin / admin123

# Start backend API server
python app.py
```

> Backend runs at: `http://127.0.0.1:5211/api/v1` (manual dev mode)
>
> **Port Summary**:
> - **Manual dev**: Backend on port `5211`, Vite proxy configured
> - **Docker Compose dev**: Backend on port `5000`
> - **Docker Compose prod**: Backend on port `8000`
>
> **Note**: `app.py` auto-sets `CELERY_ENABLE=true`, so Redis must be running first. To disable async tasks, set `CELERY_ENABLE=false` in `.env`.

#### 3) Start Celery Worker (new terminal)

```bash
cd backend
.\venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/macOS
celery -A app.extensions:celery worker --loglevel=info --pool=solo  # Windows needs --pool=solo
```

> Celery Worker handles async tasks like Web automation and performance tests. Skip if only using API testing.

#### 4) Start Frontend (dev mode)

```bash
cd web
npm install
npm run dev
```

> Frontend dev server runs at: `http://localhost:3000` (auto-proxies `/api/*` to `http://localhost:5211`)

Visit `http://localhost:3000` and log in with `admin / admin123`.

### Option B: Docker Compose

```bash
# Development environment (PostgreSQL + Redis + Backend + Celery)
docker-compose up -d

# View logs
docker-compose logs -f backend
```

> Docker Compose backend runs at `http://localhost:5000` (different from manual setup's 5211).
> Frontend still needs manual start: `cd web && npm install && npm run dev`, or build and serve via Nginx.
>
> **Port Summary**:
>
> | Deployment | Backend Port | Notes |
> |-----------|-------------|-------|
> | Manual dev | `5211` | `python app.py`, Vite proxy configured |
> | Docker dev | `5000` | `docker-compose up -d` |
> | Docker prod | `8000` | `docker-compose -f docker-compose.prod.yml up -d` |

---

## Build & Deploy (Production)

### Frontend Build

```bash
cd web
npm install
npm run build
```

Build output is in `web/dist`, served by Nginx/OpenResty with reverse proxy to `http://127.0.0.1:8000`. See `nginx/` for config examples.

### Production Deployment

#### Docker Compose (Recommended)

```bash
docker-compose -f docker-compose.prod.yml up -d
```

#### Manual Deployment

```bash
# 1. Build frontend
cd web && npm install && npm run build

# 2. Deploy backend (use Gunicorn instead of Flask dev server)
cd ../backend
pip install -r requirements.txt
gunicorn -w 4 -b 0.0.0.0:8000 "app:create_app('production')"

# 3. Start Celery Worker
celery -A app.extensions:celery worker --loglevel=info

# 4. Configure Nginx reverse proxy (see nginx/ directory)
```

#### One-Click Deploy Script

```bash
bash deploy.sh
```

### Key Configuration (`backend/.env`)

See `backend/.env.example` for all options. Production essentials:

```bash
# ================= Database =================
DATABASE_URL=postgresql://user:password@localhost:5432/fullscopetest

# ================= Async Tasks =================
REDIS_URL=redis://localhost:6379/0
CELERY_ENABLE=true

# ================= Security (CHANGE IN PRODUCTION!) =================
SECRET_KEY=<random_long_string>
JWT_SECRET_KEY=<another_random_long_string>

# ================= AI Assistant (Optional) =================
AI_ASSISTANT_ENABLED=true
AI_ASSISTANT_BASE_URL=https://api.openai.com/v1
AI_ASSISTANT_MODEL=gpt-4o-mini
AI_ASSISTANT_API_KEY=your_api_key_here
```

> **Notes:**
> - Always change `SECRET_KEY` and `JWT_SECRET_KEY` in production.
> - Web recording uses local `playwright codegen` and won't work on headless servers.
> - Windows requires `--pool=solo` for Celery (no prefork support).

---

## Project Structure

```text
FullScopeTest/
├── backend/                    # Flask backend
│   ├── app/
│   │   ├── api/                # API routes (25 modules)
│   │   ├── models/             # SQLAlchemy models (31 models)
│   │   ├── tasks/              # Celery async tasks
│   │   ├── utils/              # Utilities (response, validators, security)
│   │   ├── __init__.py         # Application factory create_app()
│   │   ├── config.py           # Multi-env config (Dev / Test / Prod)
│   │   └── extensions.py       # Extension init (db, jwt, celery, migrate)
│   ├── migrations/             # Alembic database migrations
│   ├── tests/                  # Pytest automated tests (470+ cases)
│   ├── app.py                  # Backend entry point
│   ├── init_db.py              # Database initialization
│   └── requirements.txt        # Python dependencies
├── web/                        # React + TypeScript frontend
│   ├── src/
│   │   ├── pages/              # Page components (by module)
│   │   ├── components/         # Shared components
│   │   ├── services/           # API service layer (11 services)
│   │   ├── stores/             # Zustand state management (5 stores)
│   │   ├── hooks/              # Custom hooks
│   │   ├── layouts/            # Layout components (MainLayout)
│   │   └── test/               # Vitest test config & cases
│   ├── vite.config.ts          # Vite config + API proxy
│   └── tsconfig.json           # TypeScript strict mode config
├── document/                   # Project documentation
├── nginx/                      # Nginx deployment config
├── docker/                     # Dockerfiles + orchestration
├── scripts/                    # Utility/build scripts
├── docker-compose.yml          # Development Docker Compose
├── docker-compose.prod.yml     # Production Docker Compose
└── deploy.sh                   # One-click deploy script
```

---

## FAQ

<details>
<summary><strong>Redis connection error on backend startup?</strong></summary>

`app.py` auto-sets `CELERY_ENABLE=true` and tries to connect Redis on startup. To disable async tasks, add to `backend/.env`:

```bash
CELERY_ENABLE=false
```

To keep Celery, ensure Redis is running:

```bash
redis-cli ping  # Should return PONG
```

Windows users can download [Redis for Windows](https://github.com/tporadowski/redis/releases) or use WSL/Docker.
</details>

<details>
<summary><strong>SQLite tables missing / database errors after init?</strong></summary>

Make sure you've run the initialization script:

```bash
cd backend
python init_db.py
```

> **Note**: `init_db.py` **drops and recreates** all tables — dev only. For production, use migrations: `python manage.py db upgrade`.
</details>

<details>
<summary><strong>Blank page / API 404 after frontend startup?</strong></summary>

1. Confirm backend is running at `http://127.0.0.1:5211` (manual mode) or `http://localhost:5000` (Docker dev)
2. Confirm frontend dev server is at `http://localhost:3000` (Vite auto-proxies `/api`)
3. If using Docker Compose, backend port is **5000** not 5211 — update proxy target in `web/vite.config.ts`
4. If using Docker Compose production, backend port is **8000** — configure Nginx reverse proxy
5. Try clearing browser cache with hard refresh (`Ctrl + Shift + R`)
</details>

<details>
<summary><strong>Web automation recorder fails to start?</strong></summary>

Web recording depends on a local Playwright installation:

```bash
pip install playwright
python -m playwright install chromium
```

> **Note**: Recording (`playwright codegen`) requires a GUI environment and won't work on headless/remote servers. Write scripts locally and upload to the platform instead.
</details>

<details>
<summary><strong>Celery Worker started but tasks not executing?</strong></summary>

1. Verify Redis is running and accessible
2. Windows users must add `--pool=solo`:
   ```bash
   celery -A app.extensions:celery worker --loglevel=info --pool=solo
   ```
3. Check Worker terminal for errors, verify Redis Broker connection
</details>

<details>
<summary><strong>Celery NotImplementedError on Windows?</strong></summary>

Celery 4+ doesn't support `prefork` pool on Windows. Use `solo` mode:

```bash
celery -A app.extensions:celery worker --loglevel=info --pool=solo
```

Or run Celery Worker in WSL2 / Docker.
</details>

<details>
<summary><strong>AI assistant not working?</strong></summary>

Configure an LLM API in `backend/.env`:

```bash
AI_ASSISTANT_ENABLED=true
AI_ASSISTANT_BASE_URL=https://api.openai.com/v1  # or other OpenAI-compatible API
AI_ASSISTANT_MODEL=gpt-4o-mini
AI_ASSISTANT_API_KEY=your_api_key_here
```

You can also configure dynamically in the AI Copilot panel — no backend restart needed.
</details>

<details>
<summary><strong>Backend test cases failing?</strong></summary>

Backend tests use SQLite in-memory database, no extra config needed:

```bash
cd backend
pip install -r requirements-test.txt
pytest -q tests
```

If you see `ModuleNotFoundError`, install all dependencies: `pip install -r requirements.txt`.
</details>

<details>
<summary><strong>TypeScript build errors?</strong></summary>

The project uses strict TypeScript checking. Common fixes:

```bash
# View all type errors
cd web && npx tsc --noEmit

# Common causes:
# 1. Unused variables/params — remove or prefix with _
# 2. Missing type assertions — add type annotations
# 3. API return type mismatches — check types in services/
```
</details>

<details>
<summary><strong>How to switch to PostgreSQL?</strong></summary>

1. Install PostgreSQL and create database:
   ```bash
   createdb fullscopetest_dev
   ```

2. Update `backend/.env`:
   ```bash
   DATABASE_URL=postgresql://user:password@localhost:5432/fullscopetest_dev
   ```

3. Re-initialize database:
   ```bash
   python init_db.py
   ```
</details>

---

## Contributing

Contributions are welcome!
- Found a bug or have a suggestion? Open an Issue.
- Want to contribute code? Submit a Pull Request.
- Before submitting, please run local checks:
  - Frontend: `cd web && npm run lint`
  - Backend: `cd backend && pytest -q`

---

## Contact

For deployment issues, usage questions, or business inquiries:

- **Blog**: [huangxuan.chat](http://huangxuan.chat)
- **Email**: 3441578327@qq.com or huangxuandev@126.com
- **Phone**: (+86)188-5212-2635
- **WeChat**:

  <div align="left">
    <img src="images/docs/wechat-qr.webp" alt="WeChat QR Code" width="150px" />
  </div>

---

## License

This project is licensed under the [MIT License](LICENSE).

<div align="center">
  <sub>Built with love by FullScopeTest Team</sub>
</div>
