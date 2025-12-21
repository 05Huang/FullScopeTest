# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

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

### Frontend Development (web/)

```bash
# Install dependencies
npm install

# Development server (with hot reload at localhost:3000)
npm run dev

# Type check
tsc --noEmit

# Build for production
npm run build

# Lint
npm run lint
```

**Note:** The project uses Nginx reverse proxy in production. The dev server proxies `/api` requests to `http://localhost:5211` (backend). See `vite.config.ts`.

### Backend Development (cd ../backend)

```bash
# Install dependencies
pip install -r requirements.txt

# Initialize database (creates admin user: admin/admin123)
python init_db.py

# Start Flask development server (localhost:5211)
python app.py

# Start Celery worker (required for async tasks)
celery -A app.extensions:celery worker --loglevel=info --pool=solo  # Windows
# or use: .\run_celery.bat
```

### Database Operations

```bash
# Initialize database with admin user
python init_db.py

# Create admin user manually
python manage.py create_admin
```

### Starting the Full Application

The standard workflow starts all services:
1. Backend: `cd backend && python app.py`
2. Celery: `cd backend && celery -A app.extensions:celery worker --loglevel=info --pool=solo`
3. Frontend build: `cd web && npm run build`
4. Nginx: `cd nginx && .\start-nginx.bat`
5. Access: http://localhost:8080

## Architecture

### Frontend Structure

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

### Backend Structure (../backend/app/)

```
app/
├── api/                 # API routes (one file per domain)
│   ├── auth.py          # Authentication endpoints
│   ├── api_test.py      # API testing endpoints
│   ├── web_test.py      # Web automation endpoints
│   ├── perf_test.py     # Performance testing endpoints
│   ├── projects.py      # Project CRUD
│   ├── environments.py   # Environment management
│   ├── reports.py        # Test reports
│   └── docs.py           # Documentation
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
- Auto token refresh via axios interceptor (src/services/api.ts:44-70)

### State Management

- **Zustand** with `persist` middleware for auth state
- Auth store persists to localStorage as `easytest-auth`
- Other modules use component state or React Query patterns

### Type System

- Strict TypeScript enabled (noUnusedLocals, noUnusedParameters, noFallthroughCasesInSwitch)
- Path alias: `@/*` maps to `src/*` (tsconfig.json:19-20)
- API response types defined in `src/services/api.ts`

### Key Architectural Patterns

1. **Service Layer Pattern**: Each domain has a corresponding `*Service.ts` in `src/services/`
2. **Page Components**: Route-level components in `src/pages/`, organized by module
3. **Monaco Editor**: Used for code/script editing in API and Web testing
4. **Async Tasks**: Web and performance tests run via Celery workers; check `../backend/app/extensions.py` for celery config

## Working with Environment Variables

Environment variables are managed per project in the API Testing module. The `EnvironmentVariableHint.tsx` component provides autocomplete for variables. Variables are substituted using `{{variable_name}}` syntax.

## Testing Your Changes

1. Build frontend: `npm run build`
2. Restart Nginx to pick up new build artifacts
3. Backend changes auto-reload in dev mode
4. For Celery-related changes, restart the Celery worker

## Important Files

- `vite.config.ts` - Vite proxy config (proxies /api to backend)
- `src/services/api.ts` - Axios instance with auth interceptors
- `src/stores/authStore.ts` - Auth state with persistence
- `../backend/app/config.py` - Flask configuration
- `../backend/app/extensions.py` - Flask extensions (db, jwt, celery)
