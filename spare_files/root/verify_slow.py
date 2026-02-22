import requests
import time
import json

url = "http://localhost:8001/chat"
payload = {"message": "What is in the Chapli Kebab?", "user_id": "latency_tester"}

print(f"Sending request to {url}...")
start_time = time.time()
try:
    response = requests.post(url, json=payload, timeout=60) # 60s timeout
    end_time = time.time()
    
    print(f"Status: {response.status_code}")
    print(f"Time: {end_time - start_time:.2f} seconds")
    print(f"Response len: {len(response.text)}")
    print("Response preview:", response.text[:200])

except Exception as e:
    print(f"Error: {e}")
