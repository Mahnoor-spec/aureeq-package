import requests
import json

url = "http://127.0.0.1:8001/chat"
payload = {
    "message": "hello",
    "user_id": "test_script_user",
    "was_voice": True
}

try:
    with requests.post(url, json=payload, stream=True) as response:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                print(chunk.decode('utf-8'))
except Exception as e:
    print(f"Request failed: {e}")
