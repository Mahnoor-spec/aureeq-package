import requests
import json

url = "http://127.0.0.1:8002/chat"
headers = {"Content-Type": "application/json"}

print("TURN 1: Greeting (Text mode - Expected: Audio)")
payload1 = {"user_id": "final_verify_user_actual_1", "message": "hi"}
resp1 = requests.post(url, json=payload1, stream=True)
for chunk in resp1.iter_content(chunk_size=None):
    if chunk: print(chunk.decode(), end="", flush=True)

print("\n\nTURN 2: Add to cart (Typed - Expected: Silent + Tag)")
payload2 = {"user_id": "final_verify_user_actual_1", "message": "add lamb chops to cart", "was_voice": False}
resp2 = requests.post(url, json=payload2, stream=True)
for chunk in resp2.iter_content(chunk_size=None):
    if chunk: print(chunk.decode(), end="", flush=True)

print("\n\nTURN 3: Recommendation (Mic - Expected: Audio)")
payload3 = {"user_id": "final_verify_user_actual_1", "message": "tell me about baklava", "was_voice": True}
resp3 = requests.post(url, json=payload3, stream=True)
for chunk in resp3.iter_content(chunk_size=None):
    if chunk: print(chunk.decode(), end="", flush=True)
