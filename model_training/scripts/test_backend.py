import requests
import json

url = "http://127.0.0.1:8001/chat"
payload = {
    "message": "i am a vegetarian suggest me something",
    "user_id": "test_user_vegetarian",
    "was_voice": True
}

try:
    response = requests.post(url, json=payload, stream=True)
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        print("Response stream:")
        for chunk in response.iter_content(chunk_size=None):
            if chunk:
                print(chunk.decode('utf-8'), end='', flush=True)
    else:
        print(f"Error Response: {response.text}")
except Exception as e:
    print(f"Request failed: {e}")
