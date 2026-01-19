def test_health_endpoints(client):
    endpoints = [
        "/api/v1/api-test/health",
        "/api/v1/web-test/health",
        "/api/v1/perf-test/health",
        "/api/v1/reports/health",
    ]

    for endpoint in endpoints:
        response = client.get(endpoint)
        assert response.status_code == 200
        payload = response.get_json()
        assert payload["code"] == 200
