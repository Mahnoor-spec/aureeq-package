import requests
import json

url = "http://localhost:8001/chat"
payload = {"message": "Hello", "user_id": "crash_tester"}

print(f"Sending crash test request to {url}...")
try:
    response = requests.post(url, json=payload, timeout=10)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"Error: {e}")
