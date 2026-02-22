import requests
import json
import base64

url = "http://127.0.0.1:8002/welcome?name=TestUser"
print(f"Testing /welcome endpoint...")
try:
    resp = requests.get(url, timeout=10)
    print(f"Status Code: {resp.status_code}")
    data = resp.json()
    print(f"Response Text: {data.get('response')}")
    audio_url = data.get('audio_url', "")
    if audio_url.startswith("data:audio"):
        print(f"Audio URL: Found base64 audio (length: {len(audio_url)})")
        if len(audio_url) > 1000:
            print("Audio looks valid.")
        else:
            print("Audio looks TOO SHORT. Possible error.")
    else:
        print(f"Audio URL: {audio_url} (NOT b64)")
except Exception as e:
    print(f"Error: {e}")
