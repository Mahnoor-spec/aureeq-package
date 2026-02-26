import requests
import base64

text = "مرحباً Mahnoor، أنا أورِيق مساعدك الشخصي. كيف يمكنني مساعدتك اليوم؟"
url = "http://localhost:8880/generate"
payload = {
    "text": text,
    "voice": "am_adam",
    "lang_code": "ar"
}

try:
    print(f"Testing TTS with payload...")
    response = requests.post(url, json=payload, timeout=10)
    if response.status_code == 200:
        data = response.json()
        if "audio" in data:
            print("Success! Audio generated.")
            with open("test_mixed.wav", "wb") as f:
                f.write(base64.b64decode(data["audio"]))
        else:
            print("Error: No audio in response")
    else:
        print(f"Error: Status code {response.status_code}")
        print(response.text)
except Exception as e:
    print(f"Failed to process: {e}")
