import requests
import json

url = "http://127.0.0.1:5211/api/v1/auth/register"
headers = {"Content-Type": "application/json"}
data = {
    "username": "testuser444",
    "email": "test444@example.com",
    "password": "password123"
}

response = requests.post(url, json=data, headers=headers)
print(f"Status Code: {response.status_code}")
print(f"Response: {response.json()}")
