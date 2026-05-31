# FullScopeTest GitHub Actions Integration Guide

## Quick Start

### 1. Get API Token
1. Login to FullScopeTest
2. Go to Settings -> API Tokens
3. Create new token with read-write permissions

### 2. Configure GitHub Secrets
- FST_SERVER_URL: FullScopeTest server URL
- FST_API_TOKEN: API token from step 1

### 3. Create Workflow
Create .github/workflows/test.yml with the following content:

```yaml
name: FullScopeTest Integration
on:
  push:
    branches: [main]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: 05Huang/FullScopeTest/.github/actions/fullscope-test@main
        with:
          server-url: ${{ secrets.FST_SERVER_URL }}
          api-token: ${{ secrets.FST_API_TOKEN }}
          project-id: 1
```


## Scenarios

### PR Auto Test
Add pull_request trigger to run tests on PRs.

### Daily Regression
Add schedule trigger for daily regression tests.

### Manual Trigger
Add workflow_dispatch for manual test execution.

## Quality Gate

Configure quality gates in FullScopeTest platform and reference them in your workflow.

## Troubleshooting

- 401 Unauthorized: Check token permissions
- Connection Timeout: Verify server accessibility
- Test Failed: Check detailed logs in FullScopeTest
