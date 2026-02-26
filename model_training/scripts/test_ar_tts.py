import requests
import os

url = "http://127.0.0.1:8880/generate"
payload = {
    "text": "مرحباً، أنا أورِيق مساعدك الشخصي.",
    "voice": "am_adam",
    "lang": "ar"
}

try:
    print("Testing Arabic with lang='ar'...")
    response = requests.post(url, json=payload, timeout=10)
    if response.status_code == 200:
        print("Success! Arabic text accepted with lang='ar'.")
        with open("test_ar.mp3", "wb") as f:
            f.write(response.content)
        print("Saved to test_ar.mp3")
    else:
        print(f"Failed with status {response.status_code}: {response.text}")
except Exception as e:
    print(f"Error: {e}")
