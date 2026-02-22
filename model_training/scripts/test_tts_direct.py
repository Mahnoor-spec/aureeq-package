import requests
import os

url = "http://127.0.0.1:8880/generate"
payload = {
    "text": "The kitchen is ready. What would you like to order?",
    "voice": "am_adam"
}

try:
    response = requests.post(url, json=payload)
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        with open("debug_tts_output.wav", "wb") as f:
            f.write(response.content)
        print("Success: debug_tts_output.wav created. Size:", os.path.getsize("debug_tts_output.wav"))
    else:
        print(f"Error: {response.text}")
except Exception as e:
    print(f"Request failed: {e}")
