#!/usr/bin/env bash
set -e

APP_DIR="$(cd "$(dirname "$0")" && pwd)"
APP_ROOT="$(cd "${APP_DIR}/../.." && pwd)"
DATA_DIR="${DATA_DIR:-${APP_ROOT}/data}"
BRANCH="${BRANCH:-main}"
PROJECT_NAME="${PROJECT_NAME:-easytest}"
COMPOSE_FILE="${COMPOSE_FILE:-docker-compose.prod.yml}"

cd "$APP_DIR"
git fetch --all
git reset --hard "origin/${BRANCH}"

# Ensure bind-mount directories exist for multi-project layout.
mkdir -p \
  "${DATA_DIR}/redis" \
  "${DATA_DIR}/uploads" \
  "${DATA_DIR}/reports"

# Build frontend using a Node container (no host Node required).
# Limit Node memory to reduce swapping on small servers.
docker run --rm -v "$APP_DIR/web:/app" -w /app node:18-alpine \
  sh -c "export NODE_OPTIONS=--max-old-space-size=1024 && npm ci && npm run build"

# Sync built frontend to 1Panel OpenResty site directory (if present).
if [ -d "/opt/1panel/apps/openresty/openresty/www/sites/easy/index" ]; then
  rsync -a --delete "$APP_DIR/web/dist/" /opt/1panel/apps/openresty/openresty/www/sites/easy/index/
fi

# Run pytest using a Python container (no host Python required).
# Use host network so tests can reach the shared Postgres on localhost.
docker run --rm --network host -v "$APP_DIR/backend:/app" -w /app python:3.11-slim \
  sh -c "pip install -r requirements.txt -r requirements-test.txt && TEST_DATABASE_URL=postgresql://easytest:easytest123@127.0.0.1:5432/easytest_test pytest -q tests"

# Deploy services.
docker compose -p "$PROJECT_NAME" -f "$COMPOSE_FILE" --env-file "$APP_DIR/.env" up -d --build

# Health checks (backend only; OpenResty proxies externally).
for i in {1..10}; do
  if curl -fsS "http://127.0.0.1:5211/api/v1/api-test/health" > /dev/null; then
    echo "Health check OK"
    break
  fi
  echo "Health check retry ($i/10) ..."
  sleep 3
  if [ "$i" -eq 10 ]; then
    echo "Health check failed"
    exit 1
  fi
done
