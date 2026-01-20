#!/usr/bin/env bash
set -e

APP_DIR="$(cd "$(dirname "$0")" && pwd)"
APP_ROOT="$(cd "${APP_DIR}/.." && pwd)"
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
docker run --rm -v "$APP_DIR/web:/app" -w /app node:18-alpine \
  sh -c "npm ci && npm run build"

# Run pytest using a Python container (no host Python required).
docker run --rm -v "$APP_DIR/backend:/app" -w /app python:3.11-slim \
  sh -c "pip install -r requirements.txt -r requirements-test.txt && pytest -q tests"

# Deploy services.
docker compose -p "$PROJECT_NAME" -f "$COMPOSE_FILE" up -d --build

# Health checks (backend only; OpenResty proxies externally).
curl -fsS "http://127.0.0.1:5211/api/v1/api-test/health"
