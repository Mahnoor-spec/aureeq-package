import requests

url = "http://127.0.0.1:8001/welcome?name=User"

try:
    response = requests.get(url)
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print("Response Text:", data.get("response"))
        audio_url = data.get("audio_url")
        if audio_url:
            print("Audio Data (Base64) Found! Length:", len(audio_url))
            if audio_url.startswith("data:audio/wav;base64,"):
                print("Format Check: Passed (data:audio/wav;base64,)")
            else:
                print("Format Check: FAILED (Unexpected prefix)")
        else:
            print("Audio Data NOT Found!")
    else:
        print(f"Error: {response.text}")
except Exception as e:
    print(f"Request failed: {e}")
