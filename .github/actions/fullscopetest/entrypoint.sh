#!/bin/bash
set -e

# FullScopeTest GitHub Action Entry Point
# Executes tests via API and collects results

echo "=== FullScopeTest GitHub Action ==="
echo "Project ID: $FST_PROJECT_ID"
echo "Test Type: $FST_TEST_TYPE"
echo "Base URL: $FST_BASE_URL"

# Build API endpoint
API_URL="${FST_BASE_URL}/api/v1"

# Trigger test execution
echo "Triggering test execution..."
RESPONSE=$(curl -s -w "
%{http_code}"   -X POST "${API_URL}/test-runs/execute"   -H "Authorization: Bearer ${FST_API_TOKEN}"   -H "Content-Type: application/json"   -d "{
    \"project_id\": ${FST_PROJECT_ID},
    \"test_type\": \"${FST_TEST_TYPE}\",
    \"collection_id\": ${FST_COLLECTION_ID:-null},
    \"triggered_by\": \"github_actions\"
  }")

HTTP_CODE=$(echo "$RESPONSE" | tail -1)
BODY=$(echo "$RESPONSE" | head -n -1)

if [ "$HTTP_CODE" -ne 200 ] && [ "$HTTP_CODE" -ne 201 ]; then
  echo "::error::Test execution failed with HTTP $HTTP_CODE"
  echo "$BODY"
  exit 1
fi

# Parse results
PASS_RATE=$(echo "$BODY" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('data',{}).get('pass_rate', 0))" 2>/dev/null || echo "0")
TOTAL_CASES=$(echo "$BODY" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('data',{}).get('total', 0))" 2>/dev/null || echo "0")
FAILED_CASES=$(echo "$BODY" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('data',{}).get('failed', 0))" 2>/dev/null || echo "0")
REPORT_ID=$(echo "$BODY" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('data',{}).get('report_id', ''))" 2>/dev/null || echo "")

REPORT_URL="${FST_BASE_URL}/reports/${REPORT_ID}"

# Set outputs
echo "pass_rate=${PASS_RATE}" >> $GITHUB_OUTPUT
echo "total_cases=${TOTAL_CASES}" >> $GITHUB_OUTPUT
echo "failed_cases=${FAILED_CASES}" >> $GITHUB_OUTPUT
echo "report_url=${REPORT_URL}" >> $GITHUB_OUTPUT

echo ""
echo "=== Results ==="
echo "Pass Rate: ${PASS_RATE}%"
echo "Total Cases: ${TOTAL_CASES}"
echo "Failed Cases: ${FAILED_CASES}"
echo "Report URL: ${REPORT_URL}"

# Quality gate check
if [ -n "$FST_QUALITY_GATE_ID" ] && [ "$FST_QUALITY_GATE_ID" != "null" ]; then
  echo ""
  echo "Evaluating quality gate..."
  GATE_RESPONSE=$(curl -s     -X POST "${API_URL}/quality-gates/${FST_QUALITY_GATE_ID}/evaluate"     -H "Authorization: Bearer ${FST_API_TOKEN}"     -H "Content-Type: application/json")

  GATE_PASSED=$(echo "$GATE_RESPONSE" | python3 -c "import sys,json; d=json.load(sys.stdin); print(str(d.get('data',{}).get('passed', False)).lower())" 2>/dev/null || echo "false")
  echo "quality_gate_passed=${GATE_PASSED}" >> $GITHUB_OUTPUT
  echo "Quality Gate: ${GATE_PASSED}"

  if [ "$GATE_PASSED" = "false" ] && [ "$FST_CONTINUE_ON_ERROR" != "true" ]; then
    echo "::error::Quality gate failed"
    exit 1
  fi
fi

# Check if tests failed
if [ "$FAILED_CASES" -gt 0 ] && [ "$FST_CONTINUE_ON_ERROR" != "true" ]; then
  echo "::error::${FAILED_CASES} test(s) failed"
  exit 1
fi
