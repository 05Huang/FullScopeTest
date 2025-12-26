# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## TOP RULES
- 沟通机制：回复必须使用中文。对于非纯文本修改的任务，必须优先提供设计方案，待我确认后方可编写代码。
- 复用原则：严格优先使用项目现有的组件、工具类和架构模式。
    - 注意：由于你可能无法读取全量代码，如果你推测可能存在相关组件但不确定位置，请先询问我，而不是直接制造重复轮子。
- 代码质量与兼容性：在重构或修改功能时，若发现兼容性冲突：
    - 首选策略：暴露问题，提出彻底的改进方案（不妥协）。
    - 备选策略：如果彻底改进影响范围过大（超过5个文件或涉及核心底层），请同时提供一个"最小侵入性"的兼容方案（如适配器模式），并说明两者的利弊，由我决策。

## Project Overview

EasyTest is a full-stack automated testing platform with three main testing modules:
- **API Testing** - Postman-like interface for HTTP testing with environments, assertions, and cURL export
- **Web Automation** - Playwright-based browser automation with recording and element library
- **Performance Testing** - Locust-based load testing with real-time monitoring

**Technology Stack:**
- Frontend: React 18 + TypeScript + Vite + Ant Design 5 + Zustand
- Backend: Flask 3.0 + SQLAlchemy + Celery + Redis
- Database: PostgreSQL (prod) / SQLite (dev)

## Common Commands

### Quick Start

```bash
# One-click start all services
START.bat

# Or use the scripts directory
scripts/start/start-all.bat
```

### Frontend Development (web/)

```bash
cd web

# Install dependencies
npm install

# Development server (with hot reload at http://localhost:3000)
npm run dev

# Type check
tsc --noEmit

# Build for production
npm run build

# Lint
npm run lint
```

**Note:** The project uses Nginx reverse proxy in production. The dev server proxies `/api` requests to `http://localhost:5211` (backend). See `vite.config.ts`.

### Backend Development (backend/)

```bash
cd backend

# Install dependencies
pip install -r requirements.txt

# Initialize database (creates admin user: admin/admin123)
python init_db.py

# Start Flask development server (localhost:5211)
scripts/backend/run-server.bat
# or directly: python app.py

# Start Celery worker (required for async tasks)
scripts/backend/run-celery.bat
# or directly: celery -A app.extensions:celery worker --loglevel=info --pool=solo  # Windows
```

### Development Scripts

```bash
# Start all services (Redis + Celery + Backend + Nginx)
scripts/start/start-all.bat

# Start only backend
scripts/start/start-backend.bat

# Start only Nginx
scripts/start/start-nginx.bat

# Rebuild frontend
scripts/build/rebuild.bat
```

### Database Operations

```bash
cd backend

# Initialize database with admin user
python init_db.py

# Run database migrations
python manage.py db upgrade

# Create migration
python manage.py db migrate -m "description"
```

### Service Addresses

| Service | Address | Description |
|---------|---------|-------------|
| Frontend | http://localhost:8080 | Via Nginx |
| Backend API | http://localhost:5211/api/v1 | Flask Backend |
| Redis | localhost:6379 | Message Queue |

### Default Test Account

- Username: `admin`
- Password: `admin123`

## Architecture

### Project Structure

```
EasyTest-Web/
├── backend/              # Flask backend application
│   ├── app/             # Application core
│   │   ├── api/         # API routes
│   │   ├── models/      # SQLAlchemy models
│   │   └── utils/       # Utilities
│   └── migrations/      # Database migrations
├── web/                 # React frontend application
│   ├── src/
│   │   ├── pages/       # Page components
│   │   ├── services/    # API service layer
│   │   ├── stores/      # Zustand state management
│   │   └── layouts/     # Layout components
│   └── dist/            # Build output
├── scripts/             # Development scripts
│   ├── start/          # Start scripts
│   ├── backend/        # Backend-specific scripts
│   └── build/          # Build scripts
├── document/            # Project documentation
├── nginx/               # Nginx configuration
├── START.bat            # Quick start script
└── CLAUDE.md            # This file
```

### Frontend Structure (web/src/)

```
src/
├── pages/               # Page components (route-level)
│   ├── api-test/        # API testing workspace, collections, environments
│   ├── web-test/        # Web automation scripts, recorder, elements
│   ├── perf-test/       # Performance test scenarios, monitor, results
│   ├── Login.tsx        # Authentication
│   ├── Dashboard.tsx    # Main dashboard
│   └── Reports.tsx      # Test reports
├── services/            # API service layer (one file per domain)
├── stores/              # Zustand state management
├── layouts/             # Layout components (MainLayout.tsx)
├── styles/              # Global styles
├── App.tsx              # Root component with routing
└── main.tsx             # Entry point
```

### Backend Structure (backend/app/)

```
app/
├── api/                 # API routes (one file per domain)
│   ├── auth.py          # Authentication endpoints
│   ├── api_test.py      # API testing endpoints
│   ├── web_test.py      # Web automation endpoints
│   ├── perf_test.py     # Performance testing endpoints
│   ├── projects.py      # Project CRUD
│   ├── environments.py   # Environment management
│   └── reports.py       # Test reports
├── models/              # SQLAlchemy ORM models
├── utils/               # Response formatting, validators
├── config.py            # Flask configuration
├── extensions.py        # Flask extensions (db, jwt, celery)
└── __init__.py          # Application factory
```

### API Design

- Base path: `/api/v1/`
- Consistent response format: `{ code, data, message, timestamp }`
- JWT authentication with refresh tokens
- Auto token refresh via axios interceptor (web/src/services/api.ts)

### State Management

- **Zustand** with `persist` middleware for auth state
- Auth store persists to localStorage as `easytest-auth`
- Other modules use component state or React Query patterns

### Type System

- Strict TypeScript enabled (noUnusedLocals, noUnusedParameters, noFallthroughCasesInSwitch)
- Path alias: `@/*` maps to `src/*` (tsconfig.json)
- API response types defined in `web/src/services/api.ts`

### Key Architectural Patterns

1. **Service Layer Pattern**: Each domain has a corresponding `*Service.ts` in `web/src/services/`
2. **Page Components**: Route-level components in `web/src/pages/`, organized by module
3. **Monaco Editor**: Used for code/script editing in API and Web testing
4. **Async Tasks**: Web and performance tests run via Celery workers; see `backend/app/extensions.py` for celery config

### Celery Integration

The project uses Celery for async task execution (Web tests, Performance tests):
- **Redis** as message broker and result backend
- Set `CELERY_ENABLE=true` environment variable to enable Celery features
- If Redis is unavailable, Celery features will be disabled automatically
- Start Celery worker: `scripts/backend/run-celery.bat`

## Working with Environment Variables

Environment variables are managed per project in the API Testing module. The `EnvironmentVariableHint.tsx` component provides autocomplete for variables. Variables are substituted using `{variable_name}` syntax (single braces, not double).

See [document/ENVIRONMENT_GUIDE.md](document/ENVIRONMENT_GUIDE.md) for detailed information.

## Testing Your Changes

1. Build frontend: `npm run build` or `scripts/build/rebuild.bat`
2. Restart Nginx to pick up new build artifacts
3. Backend changes auto-reload in dev mode
4. For Celery-related changes, restart the Celery worker

Refer to [document/STARTUP.md](document/STARTUP.md) for comprehensive startup and testing guidelines.

## Important Files

### Configuration
- `web/vite.config.ts` - Vite proxy config (proxies /api to backend)
- `backend/app/config.py` - Flask configuration (includes CELERY_ENABLE setting)
- `backend/app/extensions.py` - Flask extensions (db, jwt, celery)

### Frontend Core
- `web/src/services/api.ts` - Axios instance with auth interceptors
- `web/src/stores/authStore.ts` - Auth state with persistence
- `web/src/App.tsx` - Root component with routing

### Documentation
- `README.md` - Project overview
- `CLAUDE.md` - This file - AI assistant guide
- `document/STARTUP.md` - Startup and setup guide
- `document/DEVELOPMENT.md` - Development guide
- `document/ENVIRONMENT_GUIDE.md` - Environment variables guide
- `document/API.md` - API documentation
- `document/QUICK_START.md` - Feature quick start guide

## Development Workflow

### Typical Development Session

1. **Start all services**: `START.bat` or `scripts/start/start-all.bat`
2. **Make changes**: Edit code in `web/` or `backend/`
3. **Rebuild frontend**: `scripts/build/rebuild.bat`
4. **Test changes**: Access http://localhost:8080
5. **Restart services as needed**

### Working on Specific Modules

**API Testing**: Standard development flow - rebuild frontend after changes

**Web/Performance Testing**: These use Celery - restart Celery worker after changes:
```bash
scripts/backend/run-celery.bat
```

**Environment Variables**: See `document/ENVIRONMENT_GUIDE.md`

## Troubleshooting

### Common Issues

**Port conflicts**: Check if ports 5211 (backend), 6379 (Redis), or 8080 (Nginx) are in use

**Celery not connecting**: Ensure Redis is running before starting Celery. Set `CELERY_ENABLE=false` if Redis is unavailable.

**Frontend not updating**: Run `npm run build` and refresh browser with Ctrl+Shift+R

**Database errors**: Run `python init_db.py` in backend directory

**Async tasks not executing**: Check that Celery worker is running and Redis is accessible
