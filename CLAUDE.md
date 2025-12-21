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

### Quick Start

```bash
# One-click start all services (Redis + Celery + Backend + Nginx)
START.bat

# Or use the scripts directory
scripts/start/start-all.bat
```

### Frontend Development (web/)

```bash
cd web

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

### Backend Development (backend/)

```bash
cd backend

# Install dependencies
pip install -r requirements.txt

# Initialize database (creates admin user: admin/admin123)
python init_db.py

# Start Flask development server (localhost:5211)
# Option 1: Use the script
scripts/backend/run-server.bat

# Option 2: Direct command
python app.py

# Start Celery worker (required for async tasks)
# Option 1: Use the script
scripts/backend/run-celery.bat

# Option 2: Direct command
celery -A app.extensions:celery worker --loglevel=info --pool=solo  # Windows
```

### Development Scripts

All scripts are organized in the `scripts/` directory by function:

#### Start Scripts
```bash
# Start all services
scripts/start/start-all.bat

# Start only backend
scripts/start/start-backend.bat

# Start only Nginx
scripts/stop/start-nginx.bat
```

#### Restart Scripts
```bash
# Quick restart (build frontend + restart backend)
scripts/restart/quick-restart.bat

# Full restart (including Redis and Celery)
scripts/restart/restart-all.bat
```

#### Stop Scripts
```bash
# Stop all services
scripts/stop/stop-all.bat

# Stop only Nginx
scripts/stop/stop-nginx.bat
```

#### Build Scripts
```bash
# Build frontend only
scripts/build/build-frontend.bat
```

See [SCRIPTS_GUIDE.md](SCRIPTS_GUIDE.md) for more details.

### Database Operations

```bash
cd backend

# Initialize database with admin user
python init_db.py

# Create admin user manually
python manage.py create_admin
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
│   ├── scripts/         # Backend utility scripts
│   └── venv/            # Python virtual environment
├── web/                 # React frontend application
│   ├── src/
│   │   ├── pages/       # Page components
│   │   ├── services/    # API service layer
│   │   ├── stores/      # Zustand state management
│   │   └── layouts/     # Layout components
│   ├── dist/            # Build output
│   └── package.json
├── scripts/             # Development scripts (NEW)
│   ├── start/          # Start scripts
│   ├── restart/        # Restart scripts
│   ├── stop/           # Stop scripts
│   ├── build/          # Build scripts
│   └── backend/        # Backend-specific scripts
├── document/            # Project documentation
├── docker/              # Docker configuration
├── nginx/               # Nginx configuration (local)
├── CLAUDE.md            # This file - AI assistant guide
├── README.md            # Project overview
├── SCRIPTS_GUIDE.md     # Scripts usage guide
├── TEST_PLAN.md         # Test plan document
└── START.bat            # Quick start script
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
│   ├── reports.py       # Test reports
│   └── docs.py          # Documentation
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
- Auto token refresh via axios interceptor (web/src/services/api.ts:44-70)

### State Management

- **Zustand** with `persist` middleware for auth state
- Auth store persists to localStorage as `easytest-auth`
- Other modules use component state or React Query patterns

### Type System

- Strict TypeScript enabled (noUnusedLocals, noUnusedParameters, noFallthroughCasesInSwitch)
- Path alias: `@/*` maps to `src/*` (tsconfig.json:19-20)
- API response types defined in `web/src/services/api.ts`

### Key Architectural Patterns

1. **Service Layer Pattern**: Each domain has a corresponding `*Service.ts` in `web/src/services/`
2. **Page Components**: Route-level components in `web/src/pages/`, organized by module
3. **Monaco Editor**: Used for code/script editing in API and Web testing
4. **Async Tasks**: Web and performance tests run via Celery workers; check `backend/app/extensions.py` for celery config

## Working with Environment Variables

Environment variables are managed per project in the API Testing module. The `EnvironmentVariableHint.tsx` component provides autocomplete for variables. Variables are substituted using `{{variable_name}}` syntax.

See [document/ENVIRONMENT_GUIDE.md](document/ENVIRONMENT_GUIDE.md) for detailed information.

## Testing Your Changes

1. Build frontend: `npm run build` or `scripts/build/build-frontend.bat`
2. Restart Nginx to pick up new build artifacts
3. Backend changes auto-reload in dev mode
4. For Celery-related changes, restart the Celery worker
5. Run quick restart: `scripts/restart/quick-restart.bat`

Refer to [TEST_PLAN.md](TEST_PLAN.md) for comprehensive testing guidelines.

## Important Files

### Configuration
- `web/vite.config.ts` - Vite proxy config (proxies /api to backend)
- `backend/app/config.py` - Flask configuration
- `backend/app/extensions.py` - Flask extensions (db, jwt, celery)

### Frontend Core
- `web/src/services/api.ts` - Axios instance with auth interceptors
- `web/src/stores/authStore.ts` - Auth state with persistence
- `web/src/App.tsx` - Root component with routing

### Documentation
- `README.md` - Project overview
- `CLAUDE.md` - This file - AI assistant guide
- `SCRIPTS_GUIDE.md` - Development scripts usage
- `TEST_PLAN.md` - Comprehensive test plan
- `document/ENVIRONMENT_GUIDE.md` - Environment variables guide
- `document/API.md` - API documentation
- `document/QUICK_START.md` - Quick start guide

## Development Workflow

### Typical Development Session

1. **Start all services**: `START.bat` or `scripts/start/start-all.bat`
2. **Make changes**: Edit code in `web/` or `backend/`
3. **Quick restart**: `scripts/restart/quick-restart.bat` (builds frontend + restarts backend)
4. **Test changes**: Access http://localhost:8080
5. **Stop services**: `scripts/stop/stop-all.bat`

### Working on Specific Modules

**API Testing**: Use `scripts/restart/quick-restart.bat` after changes

**Web/Performance Testing**: These use Celery - restart includes:
```bash
scripts/restart/restart-all.bat
```

**Environment Variables**: See `document/ENVIRONMENT_GUIDE.md`

## Troubleshooting

### Common Issues

**Port conflicts**: Check if ports 5211 (backend), 6379 (Redis), or 8080 (Nginx) are in use

**Celery not connecting**: Ensure Redis is running before starting Celery

**Frontend not updating**: Run `npm run build` and refresh browser with Ctrl+Shift+R

**Database errors**: Run `python init_db.py` in backend directory

### Getting Help

- Check `document/` directory for detailed documentation
- Review `TEST_PLAN.md` for testing procedures
- See `SCRIPTS_GUIDE.md` for script usage
