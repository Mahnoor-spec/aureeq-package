import requests

urls = ["http://127.0.0.1:8880", "http://localhost:8880"]
for url in urls:
    print(f"Testing {url} with requests...")
    try:
        resp = requests.get(url, timeout=5.0)
        print(f"Success! Status: {resp.status_code}, Content: {resp.text[:50]}")
    except Exception as e:
        print(f"Failed: {e}")
