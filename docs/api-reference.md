# FullScopeTest API Reference

## Authentication

### JWT Token
Authorization: Bearer <access_token>

### API Token
Authorization: Bearer <api_token>

## v1 API Endpoints

### POST /api/v1/auth/register
Register new user

### POST /api/v1/auth/login
User login

### GET /api/v1/auth/me
Get current user info

### GET /api/v1/projects
Get project list

### POST /api/v1/projects
Create project

### GET /api/v1/environments
Get environment list

### GET /api/v1/api-test/collections
Get test collection list

### POST /api/v1/api-test/cases/{id}/run
Execute test case

### GET /api/v1/perf-test/scenarios
Get performance test scenarios

### POST /api/v1/tokens
Create API token

### POST /api/v1/quality-gates/{id}/evaluate
Evaluate quality gate

## v2 API Endpoints (FastAPI)

### POST /api/v2/auth/login
User login

### GET /api/v2/test-cases/collections
Get test collection list

### POST /api/v2/api-tests/run
Execute API test

## WebSocket Protocol

ws://localhost:5000/ws/api-test-logs/{run_id} (Docker) 或 ws://localhost:5211/ws/api-test-logs/{run_id} (手动)

## Error Codes

- 400: Bad Request
- 401: Unauthorized
- 403: Forbidden
- 404: Not Found
- 429: Rate Limited
- 500: Internal Server Error
